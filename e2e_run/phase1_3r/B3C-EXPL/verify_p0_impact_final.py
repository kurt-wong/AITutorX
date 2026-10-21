"""Authoritative P0 counterfactual (final).

Approach: run the REAL GatePolicy.evaluate to get the true decision, and
determine the P0 variant by removing ONLY the role-provenance contribution --
which policy.py routes through exactly two places:
  (1) `auto_allowed = False` inside the overlap branch (policy.py:208)
  (2) `role_provenance_violations` -> auto_blockers (policy.py:260-261)

Everything else (span-resolution auto_allowed, material auto_allowed, grammar,
answer source_located/complete, terminal rejected via hash mismatch) is unchanged.

Consequence used: `auto_allowed` is a single boolean, so the "not byte-proven"
reason in admission.reasons carries the role-region signal too. Recomputing the
variant therefore means: drop "not byte-proven" ONLY when the root's sole
auto_allowed source was role-region (i.e. no other unproven span exists), and
drop the role-provenance violation reasons.
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

_AUTO = gp._AUTO_RESOLUTIONS


def unproven_other_than_role(leaves, materials, resolved):
    """True if some span drives auto_allowed=False independently of role-region."""
    bad = []
    for leaf in leaves:
        for role, sid in gp._role_spans(leaf):
            sp = resolved.get(sid)
            res = sp.resolution_status if sp else "missing"
            if res not in _AUTO:
                bad.append((role, sid, res))
        if leaf.answer is not None:
            sp = resolved.get(leaf.answer.span_id)
            res = sp.resolution_status if sp else "missing"
            if res not in _AUTO:
                bad.append(("answer", leaf.answer.span_id, res))
    for m in materials:
        sp = resolved.get(m.span_id)
        res = sp.resolution_status if sp else "missing"
        if res not in _AUTO:
            bad.append(("material", m.span_id, res))
    return bad


def main() -> None:
    cur, var = Counter(), Counter()
    flips, still = [], []
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
            cur[d0] += 1
            if d0 != "pending_review":
                var[d0] += 1
                continue
            leaves = [l for l in compiled.leaves
                      if l.unit_id == root.unit_id
                      or l.unit_id in {s.unit_id for s in root.sub_questions}]
            materials = list(compiled.materials)
            reasons = list(g.get("reasons") or ())
            role_hits = [r for r in reasons if "role provenance violation" in r]
            other_unproven = unproven_other_than_role(leaves, materials, resolved)
            # variant: role-region no longer contributes
            rem = [r for r in reasons if "role provenance violation" not in r]
            if not other_unproven:
                rem = [r for r in rem if "not byte-proven" not in r]
            if not rem:
                d1 = "auto_approve"
            else:
                d1 = "pending_review"
            var[d1] += 1
            if d1 == "auto_approve":
                flips.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type})
            elif role_hits:
                still.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type,
                              "remaining": [r[:70] for r in rem][:3]})

    print("CURRENT :", dict(cur))
    print("P0 VAR  :", dict(var))
    print()
    print("FLIPS:", len(flips))
    for k, v in Counter((f["paper"], f["unit_type"]) for f in flips).most_common():
        print(f"   {v:>4}  {k}")
    print()
    print("role-region roots still pending after P0:", len(still))
    for s in still:
        print(f"   {s['paper']}/{s['root']} ({s['unit_type']}) {s['remaining']}")

    (OUT / "verify_p0_impact_final.json").write_text(
        json.dumps({"current": dict(cur), "variant": dict(var),
                    "flips": flips, "still": still}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_p0_impact_final.json'}")


if __name__ == "__main__":
    main()
