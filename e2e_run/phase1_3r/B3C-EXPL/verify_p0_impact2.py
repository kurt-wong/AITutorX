"""Faithful P0 counterfactual: mirror GatePolicy.evaluate, but with the
role-provenance branch's `auto_allowed = False` (policy.py:208) disabled and its
violations NOT entering auto_blockers. All OTHER auto_allowed sources
(span resolution not exact/normalized, material resolution) stay intact.

This is the exact change the Owner authorized, so the resulting counts are the
auditable P0 numbers.
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

from app.domains.compile import content_roles_for, map_canonical_type  # noqa: E402
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


def decide(root, compiled, resolved, run, *, p0: bool):
    """Mirror of policy.evaluate, restricted to the decisions we need.
    p0=True  -> role-provenance branch does NOT set auto_allowed=False and its
                violations do not become auto_blockers (diagnostic only).
    """
    leaves = [l for l in compiled.leaves
              if l.unit_id == root.unit_id
              or l.unit_id in {s.unit_id for s in root.sub_questions}]
    materials = [m for m in compiled.materials]

    # ---- provenance / auto_allowed (policy.py:140-176) ----
    auto_allowed = True
    provenance_fail = False
    for leaf in leaves:
        for role, sid in gp._role_spans(leaf):
            sp = resolved.get(sid)
            res = sp.resolution_status if sp else "missing"
            if res not in _AUTO:
                auto_allowed = False
        if leaf.answer is not None:
            sp = resolved.get(leaf.answer.span_id)
            res = sp.resolution_status if sp else "missing"
            if res not in _AUTO:
                auto_allowed = False
        for role, sid, th, txt in gp._compiled_hash_checks(leaf):
            if th != gp._raw_sha256(txt):
                provenance_fail = True
    for m in materials:
        sp = resolved.get(m.span_id)
        res = sp.resolution_status if sp else "missing"
        if res not in _AUTO:
            auto_allowed = False

    # ---- role provenance (policy.py:192-215) ----
    violations = []
    if run.structural_regions:
        by_role = {}
        for reg in run.structural_regions:
            by_role.setdefault(reg.role, set()).update(reg.line_refs)
        for leaf in leaves:
            if leaf.answer is None:
                continue
            sp = resolved.get(leaf.answer.span_id)
            if sp is None:
                continue
            ans = set(sp.line_refs)
            for bad in ("explanation", "question"):
                ov = ans & by_role.get(bad, set())
                if ov:
                    if not p0:
                        auto_allowed = False
                    violations.append((leaf.unit_id, bad, sorted(ov)[:3]))

    if provenance_fail:
        return "rejected", violations, auto_allowed

    # ---- admission / auto_blockers (policy.py:255-283) ----
    blockers = []
    if not auto_allowed:
        blockers.append("not byte-proven")
    if not p0:
        blockers.extend(violations)
    for leaf in leaves:
        g = gp._leaf_grammar(leaf)
        if g is None:
            blockers.append(f"leaf {leaf.unit_id} not strict-auto")
        else:
            ok, _ = g
            if not ok:
                blockers.append(f"leaf {leaf.unit_id} answer grammar")
        if leaf.answer is None or not leaf.answer.source_located or not leaf.answer.complete:
            blockers.append(f"leaf {leaf.unit_id} answer not located/complete")
    return ("auto_approve" if not blockers else "pending_review"), violations, auto_allowed


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
            # cross-check current mirror against the real evaluator
            real = gp.evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            d0r, _, _ = decide(root, compiled, resolved, run, p0=False)
            if d0r != real["decision"]:
                cur["MIRROR_MISMATCH"] += 1
            d0 = real["decision"]
            d1, viol, _ = decide(root, compiled, resolved, run, p0=True)
            cur[d0] += 1
            var[d1] += 1
            if d0 == "pending_review" and d1 == "auto_approve":
                flips.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type, "hits": [v[1] for v in viol]})
            elif viol and d1 != "auto_approve":
                still.append({"paper": paper, "root": root.unit_id,
                              "unit_type": root.unit_type})

    print("CURRENT :", dict(cur))
    print("P0 VAR  :", dict(var))
    print()
    print("FLIPS:", len(flips))
    for k, v in Counter((f["paper"], f["unit_type"]) for f in flips).most_common():
        print(f"   {v:>4}  {k}")
    print()
    print("STILL pending WITH role-region hit:", len(still))
    for s in still[:15]:
        print(f"   {s['paper']}/{s['root']} ({s['unit_type']})")

    (OUT / "verify_p0_impact.json").write_text(
        json.dumps({"current": dict(cur), "variant": dict(var),
                    "flips": flips, "still": still}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_p0_impact.json'}")


if __name__ == "__main__":
    main()
