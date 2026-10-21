"""P1.4-B v2 — CORRECTED prediction model (READ-ONLY).

Fixes an instrumentation defect in _p14b_prefix_simulation.py:
  the ad-hoc `answer_letter = _clean_answer(text)[:1]` took the FIRST CHARACTER
  of the raw answer text, which for `29. 【答案】C` is '【' and for the math blob
  is '4'. Every real grammar verdict comes from verify() itself, which parses
  forms properly. The old table printed answer_in_old_labels=False for 历史 Q29
  even though grammar was True -> a self-contradiction in MY report, now fixed.

Also replaces the donor-span injection with the ADOPTED model:
    prediction = grammar(verify with recovered labels) AND other_layers_pass
because injecting a fabricated span into ResolvedRun creates a
'duplicate content span' provenance violation -- a simulation artifact, not an
authoritative outcome. A real repair binds content that ALREADY EXISTS in the
source (Q23 L194 / Q4 L23 / Q29 L307) to an exact ResolvedSpan.
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
from app.domains.gate.grammar import verify, _answer_form_single_choice, _clean_answer  # noqa: E402
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
FOCUS = {("化学", "Q23"), ("数学", "Q4"), ("历史", "Q29")}


def real_answer_letter(canonical: str, answer_text: str):
    """Ask the CONTRACT itself what letter it sees. No ad-hoc [:1] slicing."""
    cleaned = _clean_answer(answer_text)
    if canonical == "single_choice":
        return _answer_form_single_choice(cleaned)
    return None


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
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)

        for root in ir.units:
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            layers = gate["layers"]
            other_pass = (layers["structural"]["status"] == "pass"
                          and layers["provenance"]["status"] == "pass"
                          and layers["semantic"]["status"] == "pass")
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id not in want:
                    continue
                if leaf.canonical_question_type not in CHOICE:
                    continue
                labels = tuple(str(o.label) for o in leaf.options)
                atxt = leaf.answer.text if leaf.answer else ""
                g = verify(leaf.canonical_question_type, atxt, labels)
                letter = real_answer_letter(leaf.canonical_question_type, atxt)
                recovered = tuple(list(labels) + ["D"])
                g_new = verify(leaf.canonical_question_type, atxt, recovered)
                rows.append({
                    "paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                    "qn": leaf.question_number, "type": leaf.canonical_question_type,
                    "decision": gate["decision"],
                    "other_layers_pass": other_pass,
                    "structural": layers["structural"]["status"],
                    "provenance": layers["provenance"]["status"],
                    "semantic": layers["semantic"]["status"],
                    "labels": list(labels),
                    "answer_text": atxt[:70],
                    "answer_letter_from_contract": letter,
                    "letter_in_old": (letter in {l.upper() for l in labels}) if letter else None,
                    "letter_in_new": (letter in {l.upper() for l in recovered}) if letter else None,
                    "grammar_old": g,
                    "grammar_new": g_new,
                    "predicted_old": "auto_approve" if (g is True and other_pass) else "pending_review",
                    "predicted_new": "auto_approve" if (g_new is True and other_pass) else "pending_review",
                })

    def find(paper, root):
        return [r for r in rows if r["paper"] == paper and r["root"] == root]

    print("=" * 92)
    print("P1.4-B v2 CORRECTED — prediction = grammar(verify) AND other_layers_pass")
    print("=" * 92)
    delta = Counter()
    for paper, root in [("化学", "Q23"), ("数学", "Q4"), ("历史", "Q29")]:
        for r in find(paper, root):
            print(f"\n{paper}/{root}  type={r['type']}")
            print(f"   answer_text (raw)          : {r['answer_text']!r}")
            print(f"   letter via CONTRACT        : {r['answer_letter_from_contract']!r}"
                  f"   (old table wrongly showed first char)")
            print(f"   other layers P/S/Sem       : {r['structural']}/{r['provenance']}/{r['semantic']}"
                  f"  -> pass={r['other_layers_pass']}")
            print(f"   labels old -> new          : {r['labels']} -> {r['labels'] + ['D']}")
            print(f"   letter ∈ old / ∈ new       : {r['letter_in_old']} / {r['letter_in_new']}")
            print(f"   grammar old -> new         : {r['grammar_old']} -> {r['grammar_new']}")
            print(f"   PREDICTED decision         : {r['predicted_old']} -> {r['predicted_new']}")
            d = (r["predicted_old"] != "auto_approve") and (r["predicted_new"] == "auto_approve")
            print(f"   auto gain from B repair    : {'YES (+1)' if d else 'NO (0)'}")
            if d:
                delta["gained"] += 1

    # corpus-wide: how many pending units are pending ONLY because of the answer blob
    pend = [r for r in rows if r["decision"] == "pending_review"]
    blob_pend = [r for r in pend if r["grammar_old"] is None
                 and r["answer_letter_from_contract"] is None]
    print("\n" + "=" * 92)
    print("CORPUS-WIDE: pending units whose grammar is None because the CONTRACT cannot")
    print("parse the answer text (answer-slice), with declared labels intact:")
    print("=" * 92)
    print(f"pending (choice leaves): {len(pend)}")
    print(f"   grammar None AND contract sees no letter (answer-slice victims): {len(blob_pend)}")
    print(f"   by paper: {dict(Counter(r['paper'] for r in blob_pend))}")
    print("   NOTE: these are answer-side; recovering an option label does NOT flip them.")
    for r in blob_pend[:8]:
        print(f"      {r['paper']}/{r['root']:<6} labels={r['labels']} ans={r['answer_text'][:40]!r}")

    OUT.joinpath("_p14b_v2_corrected.json").write_text(
        json.dumps({"focus_rows": [r for r in rows if (r["paper"], r["root"]) in FOCUS],
                    "B_repair_auto_gain": delta.get("gained", 0),
                    "pending_answer_slice_victims": len(blob_pend),
                    "all_rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n>>> B repair total auto gain (corrected model) = {delta.get('gained', 0)}")
    print(f"wrote {OUT / '_p14b_v2_corrected.json'}")


if __name__ == "__main__":
    main()
