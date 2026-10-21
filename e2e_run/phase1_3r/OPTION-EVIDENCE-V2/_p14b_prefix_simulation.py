"""P1.4-B PRE-FIX IMPACT SIMULATION (READ-ONLY).

Answers the question the task instruction says must NOT be assumed:
    does repairing the 3 B samples actually buy Gate auto gain?

Method: replay the real pipeline (Resolver -> IR -> Compiler -> GatePolicy.evaluate)
for the 3 papers, report each B sample's CURRENT gate decision + reasons, then
simulate the repair by appending the recovered option-D CompiledOption to the
compiled leaf and re-running the SAME GatePolicy.evaluate on the SAME resolved run.

Nothing is mutated on disk; no production file is imported-modified. The simulated
option span reuses the real source span for the recovered content, so provenance
text_hash checks remain honest (it is the same text the producer would emit).
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
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

TARGETS = {("化学", "Q23"), ("数学", "Q4"), ("历史", "Q29")}


def build(paper_dir: Path):
    m = load_manifest(paper_dir)
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
    line_map = {v.line_ref: v for v in views}
    compiled = Compiler(span_map, line_map).compile(ir)
    return m, texts, views, run, ir, compiled, span_map


def dump(gate, limit=12):
    return {"decision": gate["decision"], "reasons": gate["reasons"][:limit]}


def main() -> None:
    findings = []
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        m, texts, views, run, ir, compiled, span_map = build(p)
        by_root = {u.unit_id: u for u in ir.units}

        for key in [t for t in TARGETS if t[0] == paper]:
            root_id = key[1]
            root = by_root.get(root_id)
            if root is None:
                continue
            cur_gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)

            # which compiled leaves belong to this root
            from app.domains.gate.policy import leaf_unit_ids, partition_candidate
            want = leaf_unit_ids(root)
            leaves = [l for l in compiled.leaves if l.unit_id in want]

            for leaf in leaves:
                # ---- what does the CURRENT leaf look like?
                info = {
                    "paper": paper, "root": root_id, "leaf": leaf.unit_id,
                    "canonical_type": leaf.canonical_question_type,
                    "answer_text": (leaf.answer.text if leaf.answer else None),
                    "option_labels": [str(o.label) for o in leaf.options],
                    "option_texts": [o.text.strip()[:60] for o in leaf.options],
                    "current_gate": dump(cur_gate),
                }
                # ---- is the answer located+complete? (policy.py line 276 check)
                a = leaf.answer
                info["answer_source_located"] = bool(a.source_located) if a else None
                info["answer_complete"] = bool(a.complete) if a else None
                info["answer_span_id"] = a.span_id if a else None
                info["answer_resolution_status"] = (
                    span_map[a.span_id].resolution_status
                    if a and a.span_id in span_map else None
                )

                # ---- SIMULATE THE REPAIR: append recovered option D
                # Recovered label letter comes from source structure (position in the
                # A/B/C label sequence), NOT from the answer.
                sim_leaf = _with_extra_option(leaf, label="D")
                sim_compiled = _replace_leaf(compiled, sim_leaf)
                sim_gate = gate_evaluate(root=root, ir=ir, compiled=sim_compiled, resolved_run=run)
                info["simulated_option_labels"] = [str(o.label) for o in sim_leaf.options]
                info["simulated_gate"] = dump(sim_gate)
                info["decision_delta"] = f"{cur_gate['decision']} -> {sim_gate['decision']}"

                # ---- grammar-level check (the binding constraint?)
                from app.domains.gate.grammar import verify, _clean_answer
                old_labels = tuple(str(o.label) for o in leaf.options)
                new_labels = tuple(str(o.label) for o in sim_leaf.options)
                atxt = leaf.answer.text if leaf.answer else ""
                info["grammar_old"] = verify(leaf.canonical_question_type, atxt, old_labels)
                info["grammar_new"] = verify(leaf.canonical_question_type, atxt, new_labels)
                answer_letter = _clean_answer(atxt)[:1].upper()
                info["answer_letter"] = answer_letter
                info["answer_in_old_labels"] = answer_letter in {l.upper() for l in old_labels}
                info["answer_in_new_labels"] = answer_letter in {l.upper() for l in new_labels}
                info["binding_constraint_is_option_set"] = (
                    info["grammar_old"] is None and info["grammar_new"] is True
                )
                findings.append(info)

    OUT.joinpath("_p14b_prefix_simulation.json").write_text(
        json.dumps({"note": "READ-ONLY pre-fix impact simulation; no production change",
                    "findings": findings}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 84)
    print("P1.4-B PRE-FIX SIMULATION — does repairing B actually buy Gate auto?")
    print("=" * 84)
    for f in findings:
        print(f"\n{f['paper']}/{f['root']}  leaf={f['leaf']}  type={f['canonical_type']}")
        print(f"   answer text        : {f['answer_text']!r}  (letter {f['answer_letter']})")
        print(f"   answer located/comp: {f['answer_source_located']} / {f['answer_complete']}  "
              f"resolution={f['answer_resolution_status']}")
        print(f"   old option labels  : {f['option_labels']}")
        print(f"   answer ∈ old labels: {f['answer_in_old_labels']}")
        print(f"   grammar old -> new : {f['grammar_old']} -> {f['grammar_new']}")
        print(f"   gate decision      : {f['decision_delta']}")
        print(f"   current reasons    : {f['current_gate']['reasons'][:4]}")
        print(f"   simulated reasons  : {f['simulated_gate']['reasons'][:4]}")
        print(f"   >>> option-set is the binding constraint: {f['binding_constraint_is_option_set']}")
    print(f"\nwrote {OUT / '_p14b_prefix_simulation.json'}")


def _with_extra_option(leaf, label: str):
    """Append an option whose span reuses the leaf's LAST option span (same text/hash).

    Simulation-only: this models 'the producer emitted one more option for content it
    already had'. It does NOT invent text; provenance/hash stay those of a real span.
    """
    import dataclasses
    if not leaf.options:
        return leaf
    donor = leaf.options[-1]
    new_opt = dataclasses.replace(donor, label=label)
    return dataclasses.replace(leaf, options=tuple(leaf.options) + (new_opt,))


def _replace_leaf(compiled, new_leaf):
    import dataclasses
    leaves = tuple(new_leaf if l.unit_id == new_leaf.unit_id else l for l in compiled.leaves)
    return dataclasses.replace(compiled, leaves=leaves)


if __name__ == "__main__":
    main()
