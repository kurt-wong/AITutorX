"""READ-ONLY: how many pending_review units are blocked by ANSWER-slice granularity
(a 解析 blob) versus by a genuinely missing OPTION label?

For each grammar_None choice leaf, test whether the answer text CONTAINS a
canonical single-choice token as its terminal answer statement (故选：X / 【答案】X).
This is a counterfactual UPPER BOUND on what a cleaner answer slice would unlock.
It does NOT propose Answer->Option inference; it measures answer-side granularity.
"""
from __future__ import annotations

import json
import os
import re
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
from app.domains.gate.grammar import verify, _clean_answer  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate, leaf_unit_ids  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHOICE = {"single_choice", "multiple_choice", "true_false"}
TERMINAL_ANSWER = re.compile(r"(?:故选|答案)\s*[:：]?\s*([A-Ha-h])(?![A-Za-z])")


def main() -> None:
    rows = []
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
        span_map = {s.span_id: s for s in run.resolved_spans}
        compiled = Compiler(span_map, {v.line_ref: v for v in views}).compile(ir)
        mu_by_id = {u.unit_id: u for u in m.units}

        for root in ir.units:
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id not in want:
                    continue
                if leaf.canonical_question_type not in CHOICE:
                    continue
                labels = tuple(str(o.label) for o in leaf.options)
                atxt = leaf.answer.text if leaf.answer else ""
                g = verify(leaf.canonical_question_type, atxt, labels)
                cleaned = _clean_answer(atxt)
                mterm = TERMINAL_ANSWER.search(cleaned)
                terminal_letter = mterm.group(1).upper() if mterm else None
                mu = mu_by_id.get(leaf.unit_id) or mu_by_id.get(root.unit_id)
                rows.append({
                    "paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                    "decision": gate["decision"], "grammar": g,
                    "labels": list(labels),
                    "answer_len": len(cleaned),
                    "answer_head": cleaned[:40],
                    "terminal_answer_letter": terminal_letter,
                    "terminal_in_labels": (terminal_letter in {l.upper() for l in labels})
                                        if terminal_letter else None,
                    "manifest_answer_lines": list(mu.answer_lines) if mu and mu.answer_lines else None,
                    "manifest_options_lines": list(mu.options_lines) if mu and mu.options_lines else None,
                    "manifest_declared_labels": [o.label for o in (mu.options or [])] if mu else None,
                })

    pend = [r for r in rows if r["decision"] == "pending_review"]
    pend_blob = [r for r in pend if r["answer_len"] > 8]
    pend_tok = [r for r in pend if r["answer_len"] <= 8]
    # counterfactual: replace answer text with the terminal 故选/答案 letter
    unlock = [r for r in pend_blob
              if r["terminal_answer_letter"] and r["terminal_in_labels"]]
    no_unlock = [r for r in pend_blob if r not in unlock]

    print("=" * 88)
    print("ANSWER-SLICE GRANULARITY vs OPTION-LABEL — which blocks pending_review?")
    print("=" * 88)
    print(f"choice leaves           : {len(rows)}")
    print(f"pending_review (leaves) : {len(pend)}")
    print(f"   answer is a TOKEN (<=8 chars): {len(pend_tok)}")
    for r in pend_tok:
        print(f"      {r['paper']}/{r['root']} labels={r['labels']} ans={r['answer_head']!r} "
              f"grammar={r['grammar']}")
    print(f"   answer is a BLOB (>8 chars)  : {len(pend_blob)}")
    print(f"      of those, terminal 故选/答案 letter ∈ labels (ANSWER-SIDE fixable): {len(unlock)}")
    print(f"      of those, still not unlockable by answer slice alone      : {len(no_unlock)}")
    print()
    print("unlockable-by-answer-slice rows:")
    for r in unlock:
        print(f"   {r['paper']}/{r['root']:<10} labels={str(r['labels']):<22} "
              f"terminal={r['terminal_answer_letter']} len={r['answer_len']:<4} "
              f"answer_lines={r['manifest_answer_lines']}")
    print()
    print("NOT unlockable (真 option-set / 其它):")
    for r in no_unlock:
        print(f"   {r['paper']}/{r['root']:<10} labels={str(r['labels']):<22} "
              f"terminal={r['terminal_answer_letter']} len={r['answer_len']:<4} "
              f"head={r['answer_head'][:50]!r}")
    print()
    print("by paper, pending blob:", dict(Counter(r["paper"] for r in pend_blob)))

    OUT.joinpath("_p14b_answer_slice_counterfactual.json").write_text(
        json.dumps({
            "choice_leaves": len(rows),
            "pending_leaves": len(pend),
            "pending_answer_token": len(pend_tok),
            "pending_answer_blob": len(pend_blob),
            "answer_slice_unlockable_upper_bound": len(unlock),
            "not_unlockable": len(no_unlock),
            "rows": rows,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_answer_slice_counterfactual.json'}")


if __name__ == "__main__":
    main()
