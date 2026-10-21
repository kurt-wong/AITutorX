"""Scope reconciliation: replay rejected roots vs accepted baseline rejected=5.

Read-only. Determines whether the replay's rejected count differs because of
DEFINITION (which roots are counted), not because of a pipeline deviation.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    rej, irstat, dec, per_paper = [], Counter(), Counter(), Counter()
    leaf_rows = []
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
        )
        sv = uuid.uuid4()
        run = SourceResolver(source_version_id=sv, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv, uuid.uuid4())
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)
        for root in ir.units:
            irstat[root.semantic_status] += 1
            g = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            dec[g["decision"]] += 1
            per_paper[(paper, g["decision"])] += 1
            if g["decision"] == "rejected":
                rej.append({
                    "paper": paper, "root": root.unit_id,
                    "semantic_status": root.semantic_status,
                    "n_sub": len(root.sub_questions),
                    "first_reason": g["reasons"][0][:110],
                })
            # leaf-level decisions (what the survey counts)
            from app.domains.gate.policy import leaf_unit_ids
            want = leaf_unit_ids(root)
            for l in compiled.leaves:
                if l.unit_id in want:
                    leaf_rows.append({"paper": paper, "root": root.unit_id, "leaf": l.unit_id,
                                      "decision": g["decision"]})

    print("IR semantic_status over roots:", dict(irstat))
    print("gate decisions over ROOTS   :", dict(dec))
    print()
    print("=== per paper x decision (roots) ===")
    for k, v in sorted(((str(k), v) for k, v in per_paper.items())):
        print(f"   {k:<40}{v}")
    print()
    print("=== rejected roots:", len(rej), "===")
    print("by semantic_status :", dict(Counter(r["semantic_status"] for r in rej)))
    print("by paper           :", dict(Counter(r["paper"] for r in rej)))
    print("first-reason prefix:")
    for k, v in Counter(r["first_reason"].split(":")[0][:70] for r in rej).most_common():
        print(f"   {v:>4}  {k}")
    print()
    print("=== gate decisions over CHOICE LEAVES ===")
    print(dict(Counter(r["decision"] for r in leaf_rows)), "total leaves", len(leaf_rows))
    print("rejected LEAVES:", [r for r in leaf_rows if r["decision"] == "rejected"])

    OUT.joinpath("_p14b_scope_reconciliation.json").write_text(
        json.dumps({
            "ir_semantic_status_roots": dict(irstat),
            "gate_decisions_roots": dict(dec),
            "gate_decisions_leaves": dict(Counter(r["decision"] for r in leaf_rows)),
            "rejected_roots": rej,
            "rejected_root_count": len(rej),
            "note": "replay is READ-ONLY; compares root-scope vs leaf-scope decision counts",
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_scope_reconciliation.json'}")


if __name__ == "__main__":
    main()
