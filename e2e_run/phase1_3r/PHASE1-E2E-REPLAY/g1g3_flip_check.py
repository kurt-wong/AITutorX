# -*- coding: utf-8 -*-
"""Verify G1/G3 flips vs P0 baseline + add subsequent_contracts to 36 taxonomy."""
import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\PHASE1-E2E-REPLAY")
sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler
from app.domains.compile.ir import IRBuilder
from app.domains.compile import map_canonical_type
from app.domains.gate import STRICT_AUTO_TYPES
from app.domains.gate.grammar import verify, _clean_answer
from app.domains.gate.policy import evaluate
from app.domains.resolver.resolver import SourceResolver
from app.domains.resolver.span import SourceLineView
from scripts.preprocessing_consumer.annotation_adapter import (
    attach_material_boundary_markers, manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

# focus: the 36 classification samples
FOCUS = {
    ("化学", "Q23"), ("语文", "Q6"), ("语文", "Q7"),
}
FOCUS.update({("英语", x) for x in
              ["Q1", "Q2", "Q4", "Q5-6", "Q7-8", "Q9-11", "Q12-14", "Q15-17"]})
FOCUS.update({("数学", f"Q{i}") for i in range(1, 26)})


def main() -> None:
    rows = []
    tot = Counter()
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)
        c_by_id = {l.unit_id: l for l in compiled.leaves}

        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            dec = d.get("decision")
            tot[dec] += 1
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            for leaf in leaves:
                key = (p.parent.name, root.unit_id)
                if key not in FOCUS and not any(k in root.unit_id for k in ("Q23", "Q6", "Q7")):
                    continue
                cl = c_by_id.get(leaf.unit_id)
                ans_text = cl.answer.text if cl and cl.answer else None
                labels = tuple(str(o.label) for o in (cl.options if cl else ()))
                canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
                vret = verify(canonical, ans_text, labels) if has_text(ans_text) else None
                rows.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "leaf": leaf.unit_id,
                    "decision": dec,
                    "answer_text": (ans_text or "")[:60],
                    "labels": list(labels),
                    "verify": vret,
                    "cleaned": _clean_answer(ans_text)[:40] if ans_text else None,
                })

    print("totals", dict(tot))
    print("\nfocus rows:")
    for r in sorted(rows, key=lambda x: (x["paper"], x["root"])):
        mark = "AUTO" if r["decision"] == "auto_approve" else r["decision"][:4]
        print(f"  {mark:4} {r['paper']} {r['root']:12} verify={r['verify']} "
              f"labels={r['labels']} text={r['answer_text'][:40]!r} cleaned={r['cleaned']!r}")

    # subsequent_contracts enrichment on the 36 taxonomy
    tax_path = OUT / "answer_36_contract_first.json"
    if tax_path.exists():
        tax = json.loads(tax_path.read_text(encoding="utf-8"))
        for r in tax["rows"]:
            subs = []
            # if first is G1 (escaped-dot) and text would still fail G3 after clean
            if r["first_failed_contract"] == "G1":
                cleaned = _clean_answer(r["answer_text"])
                if cleaned and __import__("re").match(r"^[A-Za-z]\s*[（(]\s*\d+\s*分\s*[)）]", cleaned):
                    subs.append("G3")
            r["subsequent_contracts"] = subs
        tax["note_subsequent"] = (
            "subsequent_contracts = contract failures that remain after fixing "
            "first_failed_contract. Not counted as independent roots."
        )
        tax_path.write_text(json.dumps(tax, ensure_ascii=False, indent=2), encoding="utf-8")
        q7 = next((r for r in tax["rows"] if r["leaf_id"] == "Q7" or r["root_id"] == "Q7"), None)
        print("\nQ7 taxonomy:", q7 and {
            "first": q7["first_failed_contract"],
            "subsequent": q7.get("subsequent_contracts"),
        })


def has_text(t):
    return bool(t and str(t).strip())


if __name__ == "__main__":
    main()
