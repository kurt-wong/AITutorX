"""INDEPENDENT P1.4-B post-fix replay (READ-ONLY).

Re-derives the phase-1 pipeline on the CURRENT (patched) corpus and reports
root/ready/incomplete/auto/pending/rejected, plus per-sample Q20/Q23/Q4/Q29
detail. Compares against the accepted af70d64 baseline.
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
from app.domains.gate.policy import evaluate as gate_evaluate, leaf_unit_ids  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

WATCH = {"化学": {"Q20", "Q23"}, "数学": {"Q4"}, "历史": {"Q29"}}


def main() -> None:
    roots = Counter()
    leaf_dec = Counter()
    watch_rows = []

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
            roots[root.semantic_status] += 1
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id in want:
                    leaf_dec[gate["decision"]] += 1
                    if root.unit_id in WATCH.get(paper, set()):
                        watch_rows.append({
                            "paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                            "decision": gate["decision"],
                            "labels": [str(o.label) for o in leaf.options],
                            "option_texts": [o.text.strip()[:48] for o in leaf.options],
                            "answer": (leaf.answer.text[:60] if leaf.answer else None),
                            "reasons": gate["reasons"][:3],
                        })

    print("=" * 92)
    print("INDEPENDENT POST-FIX REPLAY (current patched corpus)")
    print("=" * 92)
    print("root semantic_status :", dict(roots), " total roots:", sum(roots.values()))
    print("leaf decisions       :", dict(leaf_dec), " total leaves:", sum(leaf_dec.values()))
    print()
    print("baseline af70d64     : root 284 | ready 227 | incomplete 57 | auto 154 | pending 68 | rejected 5")
    print("MIMO claim (post)    : root 284 | ready 227 | incomplete 57 | auto 155 | pending 67 | rejected 5")
    print()
    print("--- watch units ---")
    for r in sorted(watch_rows, key=lambda x: (x["paper"], x["root"])):
        print(f"\n{r['paper']}/{r['root']}  decision={r['decision']}")
        print(f"   labels      : {r['labels']}")
        print(f"   option texts: {r['option_texts']}")
        print(f"   answer      : {r['answer']!r}")
        print(f"   reasons     : {r['reasons']}")

    OUT.joinpath("_p14b_indep_postfix_replay.json").write_text(
        json.dumps({"root_semantic_status": dict(roots),
                    "leaf_decisions": dict(leaf_dec),
                    "watch_rows": watch_rows}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_indep_postfix_replay.json'}")


if __name__ == "__main__":
    main()
