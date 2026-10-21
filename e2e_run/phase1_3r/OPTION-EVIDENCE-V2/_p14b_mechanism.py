"""P1.4-B mechanism confirmation (READ-ONLY).

Two jobs:
 1. Confirm WHY each B sample does/doesn't gain: classify every gate blocker into
    (a) option-set/grammar-family, (b) answer-form blob, (c) provenance/other.
 2. Corpus-wide cross-tab of choice leaves: decision x blocker family, so the
    "B=3 -> auto+3" assumption is replaced by a measured number.
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
from app.domains.compile import map_canonical_type  # noqa: E402
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


def blocker_family(reason: str) -> str:
    if "answer grammar" in reason:
        return "grammar_none (answer/option contract)"
    if "not strict-auto (grammar None)" in reason:
        return "type_not_strict_auto"
    if "not source_located+complete" in reason:
        return "answer_not_located_or_complete"
    if "not byte-proven" in reason:
        return "not_byte_proven"
    if "semantic_status" in reason:
        return "root_not_ready"
    if "no leaf unit" in reason or "missing compiled leaf" in reason:
        return "no_leaf"
    if "no non-empty stem" in reason or "no stem" in reason:
        return "no_stem"
    return "other:" + reason[:60]


def main() -> None:
    rows = []
    totals = Counter()
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
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        compiled = Compiler(span_map, {v.line_ref: v for v in views}).compile(ir)

        for root in ir.units:
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            totals[gate["decision"]] += 1
            want = leaf_unit_ids(root)
            leaves = [l for l in compiled.leaves if l.unit_id in want]
            fams = sorted({blocker_family(r) for r in gate["reasons"]})
            for leaf in leaves:
                canonical = leaf.canonical_question_type
                if canonical not in CHOICE:
                    continue
                labels = tuple(str(o.label) for o in leaf.options)
                atxt = leaf.answer.text if leaf.answer else ""
                g = verify(canonical, atxt, labels)
                cleaned = _clean_answer(atxt)
                # is the answer a CLEAN token or a blob carrying explanation prose?
                blob = len(cleaned) > 8
                answer_in_labels = cleaned[:1].upper() in {l.upper() for l in labels} if cleaned else False
                rows.append({
                    "paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                    "qn": leaf.question_number, "type": canonical,
                    "decision": gate["decision"],
                    "blocker_families": fams,
                    "grammar": g,
                    "labels": list(labels),
                    "answer_clean": cleaned[:60],
                    "answer_is_blob": blob,
                    "answer_in_labels": answer_in_labels,
                    "answer_resolution": (
                        span_map[leaf.answer.span_id].resolution_status
                        if leaf.answer and leaf.answer.span_id in span_map else None
                    ),
                })

    dec_x_grammar = Counter((r["decision"], "grammar_True" if r["grammar"] is True
                             else ("grammar_None" if r["grammar"] is None else "grammar_False"))
                            for r in rows)
    dec_x_blob = Counter((r["decision"], "answer_blob" if r["answer_is_blob"] else "answer_token")
                         for r in rows)
    dec_x_ansin = Counter((r["decision"], "ans_in_labels" if r["answer_in_labels"]
                           else "ans_NOT_in_labels") for r in rows)
    gram_none_not_ansin = [
        {k: r[k] for k in ("paper", "root", "qn", "labels", "answer_clean", "decision", "answer_is_blob")}
        for r in rows if r["grammar"] is None and not r["answer_in_labels"]
    ]
    bubble = [r for r in rows if r["grammar"] is None and r["answer_is_blob"]]

    report = {
        "gate_decisions_all_roots": dict(totals),
        "choice_leaf_rows": len(rows),
        "decision_x_grammar": {f"{k[0]}|{k[1]}": v for k, v in dec_x_grammar.items()},
        "decision_x_answer_shape": {f"{k[0]}|{k[1]}": v for k, v in dec_x_blob.items()},
        "decision_x_answer_in_labels": {f"{k[0]}|{k[1]}": v for k, v in dec_x_ansin.items()},
        "grammar_None_and_answer_not_in_labels": gram_none_not_ansin,
        "grammar_None_and_answer_is_explanation_blob": [
            {k: r[k] for k in ("paper", "root", "qn", "labels", "answer_clean", "decision")}
            for r in bubble
        ],
        "detail_rows": rows,
    }
    OUT.joinpath("_p14b_mechanism.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=" * 84)
    print("P1.4-B MECHANISM — what actually blocks auto?")
    print("=" * 84)
    print("gate decisions (all roots):", dict(totals))
    print("choice leaves:", len(rows))
    print("\ndecision x grammar:")
    for k, v in sorted(((str(k), v) for k, v in dec_x_grammar.items())):
        print(f"   {k:<28}{v}")
    print("\ndecision x answer shape (blob = answer text carries prose, not a token):")
    for k, v in sorted(((str(k), v) for k, v in dec_x_blob.items())):
        print(f"   {k:<28}{v}")
    print("\ndecision x answer-in-labels:")
    for k, v in sorted(((str(k), v) for k, v in dec_x_ansin.items())):
        print(f"   {k:<28}{v}")
    print(f"\ngrammar None AND answer not in labels (true option-set failures): {len(gram_none_not_ansin)}")
    for r in gram_none_not_ansin[:15]:
        print(f"   {r['paper']}/{r['root']} labels={r['labels']} blob={r['answer_is_blob']} "
              f"ans={r['answer_clean'][:40]!r}")
    print(f"\ngrammar None AND answer is explanation blob (NOT an option problem): {len(bubble)}")
    for r in bubble[:15]:
        print(f"   {r['paper']}/{r['root']} labels={r['labels']} ans={r['answer_clean'][:46]!r}")
    print(f"\nwrote {OUT / '_p14b_mechanism.json'}")


if __name__ == "__main__":
    main()
