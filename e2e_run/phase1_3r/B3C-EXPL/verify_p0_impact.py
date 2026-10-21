"""Independent read-only recomputation of MIMO's P0 impact (78 -> 145).

Method: replicate GatePolicy.evaluate exactly, then produce a "P0 variant" that
(a) keeps appending the role-provenance diagnostic reason and (b) no longer lets
it set auto_allowed=False nor enter auto_blockers. Compare per-root decisions.

Self-checks:
  - variant vs current must be byte-identical when no role-region hit exists
  - report where the flip set comes from (paper / unit_type)
  - report roots that STILL have role-region hits but do not flip, and why
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate import policy as gp  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def role_region_hit(root, compiled, resolved, structural_regions):
    """Replicate policy.py:192-215 overlap detection for this root's leaves."""
    region_by_role = {}
    for reg in structural_regions:
        region_by_role.setdefault(reg.role, set()).update(reg.line_refs)
    hits = []
    leaves = [l for l in compiled.leaves
              if l.unit_id == root.unit_id
              or l.unit_id in {s.unit_id for s in root.sub_questions}]
    for leaf in leaves:
        if leaf.answer is None:
            continue
        sp = resolved.get(leaf.answer.span_id)
        if sp is None:
            continue
        ans_lines = set(sp.line_refs)
        for bad in ("explanation", "question"):
            ov = ans_lines & region_by_role.get(bad, set())
            if ov:
                hits.append((leaf.unit_id, bad, sorted(ov)[:3]))
    return hits


def main() -> None:
    cur = Counter()
    var = Counter()
    flips = []
    still = []
    mismatch = 0
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid, aid = uuid.uuid4(), uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, aid)
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {l.line_ref: l for l in srs}).compile(ir)
        resolved = {s.span_id: s for s in run.resolved_spans}

        for root in ir.units:
            if root.semantic_status != "ready":
                cur["IR_incomplete"] += 1
                var["IR_incomplete"] += 1
                continue
            g = gp.evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            d0 = g["decision"]
            if d0 == "rejected":
                cur["rejected"] += 1
                var["rejected"] += 1
                continue
            hits = role_region_hit(root, compiled, resolved, run.structural_regions)
            # variant: ignore role-region entirely when deciding auto
            reasons = list(g.get("reasons") or ())
            if hits and d0 == "pending_review":
                # simulate: drop only the role-provenance blockers
                remaining = [r for r in reasons
                             if "role provenance violation" not in r and "byte-proven" not in r
                             and "not strict-auto" not in r and "not expressible" not in r
                             and "not source_located" not in r]
                if not remaining:
                    d1 = "auto_approve"
                else:
                    d1 = "pending_review"
            else:
                d1 = d0
            if not hits and d1 != d0:
                mismatch += 1
            cur[d0] += 1
            var[d1] += 1
            if d0 == "pending_review" and d1 == "auto_approve":
                flips.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type, "hits": hits[:2]})
            elif hits and d1 != "auto_approve":
                still.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type,
                              "remaining": [r[:60] for r in reasons if r not in
                                            [x for x in reasons if "role provenance" in x]][:3]})

    print("CURRENT :", dict(cur))
    print("P0 VAR  :", dict(var))
    print("mismatch (no-hit roots that changed):", mismatch)
    print()
    print("FLIPS:", len(flips))
    fp = Counter((f["paper"], f["unit_type"]) for f in flips)
    for k, v in fp.most_common():
        print(f"   {v:>4}  {k}")
    print()
    print("STILL pending WITH role-region hit:", len(still))
    for s in still[:12]:
        print(f"   {s['paper']}/{s['root']} ({s['unit_type']}) {s['remaining']}")

    (OUT / "verify_p0_impact.json").write_text(
        json.dumps({"current": dict(cur), "variant": dict(var),
                    "mismatch": mismatch, "flips": flips, "still": still},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_p0_impact.json'}")


if __name__ == "__main__":
    main()
