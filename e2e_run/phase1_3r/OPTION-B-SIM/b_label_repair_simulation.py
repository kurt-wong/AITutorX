"""P1.4-B Phase 1 — READ-ONLY pre-repair impact simulation.

For each confirmed B sample (Chem Q23 / Math Q4 / History Q29):
  1. run REAL Producer→Resolver→IR→Compiler→Gate.evaluate (old)
  2. simulate Producer recognizing the damaged/missing label (in-memory only)
  3. re-run grammar.verify + Gate.evaluate on a DEEPCOPY with simulated labels
  4. report delta table

HARD RULES:
  - NO production code / Schema / DB / Gate policy / Decomposition change
  - do NOT assume B=3 → auto +3
  - Answer evidence NEVER generates option evidence in the simulation itself:
    the simulated label is taken from SOURCE-LOCAL deterministic structure only
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.compile.snapshot import CompiledRole  # noqa: E402
from app.domains.gate.grammar import verify, _clean_answer, _answer_form_single_choice  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

TARGETS = {
    ("化学", "Q23"): {
        "sample": "Chemistry Q23",
        "form": "trailing_label_lost",
        "form_desc": "4th option content present; `D．` label token dropped",
        "source_proof": "L194 ionic equation content, no label token; L188/190/192 have A．B．C．",
        "simulated_label": "D",
        "simulated_label_source": (
            "SOURCE-LOCAL: parallel label sequence A./B./C. + 4th content position "
            "in options_lines=(188,194); NOT from answer"
        ),
    },
    ("数学", "Q4"): {
        "sample": "Math Q4",
        "form": "glued_label",
        "form_desc": "4th option content present; label glued as `2D.`",
        "source_proof": "L23 `C. ...对称 2D. 关于直线 y= -x 对称`; digit `2` is boundary glue",
        "simulated_label": "D",
        "simulated_label_source": (
            "SOURCE-LOCAL: digit-glued `2D.` deterministic parse (strip leading digit glue) "
            "→ label D + content 关于直线 y= -x 对称; NOT from answer"
        ),
    },
    ("历史", "Q29"): {
        "sample": "History Q29",
        "form": "separator_loss",
        "form_desc": "4th option content present; label `D ` missing `.` separator",
        "source_proof": "L307 `D 麦哲伦`; L301-305 have A. B. C.",
        "simulated_label": "D",
        "simulated_label_source": (
            "SOURCE-LOCAL: line-start `D` + CJK content parallel to A./B./C. "
            "→ label D with missing separator; NOT from answer"
        ),
    },
}

# synthetic option text for simulated label (content already in source; we only
# claim LABEL recognition). span_id is simulation-only, not a real ResolvedSpan.
SIM_SPAN = "sim-option-label"


def load_unit(paper: str, root_id: str):
    for p in find_manifests(CORPUS):
        if p.parent.name != paper:
            continue
        m = load_manifest(p)
        if not any(u.unit_id == root_id for u in m.units):
            continue
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload,
            {u.unit_id: u.material_lines for u in m.units if u.material_lines},
            [s.text for s in srs],
        )
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)
        root = next(u for u in ir.units if u.unit_id == root_id)
        mu = next(u for u in m.units if u.unit_id == root_id)
        return {
            "manifest_path": str(p),
            "source_file": m.source_file,
            "manifest_unit": mu,
            "texts": [s.text for s in srs],
            "run": run,
            "ir": ir,
            "compiled": compiled,
            "root": root,
            "span_map": span_map,
        }
    return None


def leaf_of(bundle, root_id: str):
    for l in bundle["compiled"].leaves:
        if l.unit_id == root_id or l.unit_id.startswith(root_id):
            return l
    return None


def grammar_probe(canonical, answer_text, labels):
    letter = _answer_form_single_choice(_clean_answer(answer_text)) if canonical == "single_choice" else None
    result = verify(canonical, answer_text, labels)
    return {
        "cleaned_answer": _clean_answer(answer_text),
        "parsed_letter": letter,
        "labels": list(labels),
        "answer_in_labels": (letter in {str(x).upper() for x in labels}) if letter else None,
        "verify_result": result,  # True / None
    }


def simulate_labels(bundle, root_id: str, new_label: str, source_line: int | None, source_text: str):
    """In-memory only: deepcopy compiled, append a synthetic option with the recovered label.

    Content is the already-present source option text. We do NOT invent content.
    """
    compiled2 = copy.deepcopy(bundle["compiled"])
    leaf = None
    for l in compiled2.leaves:
        if l.unit_id == root_id or l.unit_id.startswith(root_id):
            leaf = l
            break
    if leaf is None:
        return compiled2, None
    # if label already present, nothing to add
    existing = {str(o.label).upper() for o in leaf.options}
    if new_label.upper() not in existing:
        opt = CompiledRole(
            role="option",
            span_id=SIM_SPAN,
            line_refs=(f"SIM@L{source_line}",) if source_line else (),
            text=source_text,
            text_hash="sim",
            label=new_label.upper(),
        )
        import dataclasses
        new_opts = tuple(leaf.options) + (opt,)
        new_leaf = dataclasses.replace(leaf, options=new_opts)
        new_leaves = tuple(
            new_leaf if l.unit_id == leaf.unit_id else l for l in compiled2.leaves
        )
        compiled2 = dataclasses.replace(compiled2, leaves=new_leaves)
        leaf = new_leaf
    return compiled2, leaf


def summarize_gate(gd: dict) -> dict:
    layers = gd.get("layers", {})
    return {
        "decision": gd.get("decision"),
        "structural": layers.get("structural", {}).get("status"),
        "provenance": layers.get("provenance", {}).get("status"),
        "semantic": layers.get("semantic", {}).get("status"),
        "admission": layers.get("admission", {}).get("status"),
        "reasons": gd.get("reasons", [])[:8],
    }


def main() -> None:
    results = []
    for (paper, root_id), meta in TARGETS.items():
        bundle = load_unit(paper, root_id)
        if not bundle:
            results.append({"sample": meta["sample"], "error": "unit not found"})
            continue
        mu = bundle["manifest_unit"]
        root = bundle["root"]
        leaf = leaf_of(bundle, root_id)
        compiled = bundle["compiled"]

        # --- OLD ---
        old_labels = [str(o.label) for o in (leaf.options if leaf else [])]
        ans_text = leaf.answer.text if leaf and leaf.answer else None
        canonical = leaf.canonical_question_type if leaf else None
        old_g = grammar_probe(canonical, ans_text, old_labels)
        old_gate = summarize_gate(evaluate(
            root=root, ir=bundle["ir"], compiled=compiled, resolved_run=bundle["run"]
        ))

        # source-local simulated content text (the 4th option body already in source)
        src_texts = bundle["texts"]
        # pick content line from meta proof
        sim_content_line = None
        sim_content = ""
        if root_id == "Q23" and paper == "化学":
            sim_content_line = 194
            sim_content = src_texts[193][:120]
        elif root_id == "Q4" and paper == "数学":
            sim_content_line = 23
            # content AFTER glued label
            m = re.search(r"2D\.\s*(.*)$", src_texts[22])
            sim_content = m.group(1)[:120] if m else src_texts[22][:120]
        elif root_id == "Q29" and paper == "历史":
            sim_content_line = 307
            sim_content = src_texts[306][:120]

        new_label = meta["simulated_label"]
        simulated_labels = list(old_labels)
        if new_label not in simulated_labels:
            simulated_labels.append(new_label)

        # grammar with simulated labels (pure function — allowed)
        sim_g = grammar_probe(canonical, ans_text, simulated_labels)

        # full gate on in-memory mutated compiled copy
        compiled2, leaf2 = simulate_labels(bundle, root_id, new_label, sim_content_line, sim_content)
        try:
            sim_gate_full = summarize_gate(evaluate(
                root=root, ir=bundle["ir"], compiled=compiled2, resolved_run=bundle["run"]
            ))
            sim_gate_error = None
        except Exception as e:
            sim_gate_full = None
            sim_gate_error = f"{type(e).__name__}: {e}"

        # grammar-only simulated admission path (what auto needs at leaf level)
        # IF all other layers already pass AND all leaves pass grammar → auto
        other_layers_pass = (
            old_gate["structural"] == "pass"
            and old_gate["provenance"] == "pass"
            and old_gate["semantic"] == "pass"
        )
        # single-leaf units: grammar is the only admission variable we changed
        if other_layers_pass and sim_g["verify_result"] is True:
            sim_decision_grammar_path = "auto_approve"
        elif other_layers_pass and sim_g["verify_result"] is not True:
            sim_decision_grammar_path = "pending_review"
        else:
            sim_decision_grammar_path = f"blocked_by_others(structural={old_gate['structural']},provenance={old_gate['provenance']},semantic={old_gate['semantic']})"

        # deltas
        reason_delta = []
        if old_g["verify_result"] != sim_g["verify_result"]:
            reason_delta.append(
                f"grammar.verify: {old_g['verify_result']} -> {sim_g['verify_result']}"
            )
        if old_gate["decision"] != sim_decision_grammar_path:
            reason_delta.append(
                f"decision(grammar-path): {old_gate['decision']} -> {sim_decision_grammar_path}"
            )
        if old_g["answer_in_labels"] != sim_g["answer_in_labels"]:
            reason_delta.append(
                f"answer_in_labels: {old_g['answer_in_labels']} -> {sim_g['answer_in_labels']}"
            )

        # auto gain?
        if old_gate["decision"] == "auto_approve":
            auto_delta = 0
            auto_delta_reason = "already auto; label repair does not change AnswerTokenContract"
        elif sim_decision_grammar_path == "auto_approve":
            auto_delta = 1
            auto_delta_reason = "grammar flip enables auto IF no other blockers (see other_layers_pass)"
        else:
            auto_delta = 0
            auto_delta_reason = (
                "label repair alone does NOT flip gate to auto "
                f"(verify {old_g['verify_result']}->{sim_g['verify_result']}; "
                f"decision stays {sim_decision_grammar_path})"
            )

        row = {
            "sample": meta["sample"],
            "paper": paper,
            "root": root_id,
            "form": meta["form"],
            "form_desc": meta["form_desc"],
            "source_proof": meta["source_proof"],
            "simulated_label_source": meta["simulated_label_source"],
            "authority_check": "simulated label from SOURCE-LOCAL structure ONLY; answer not used to create label",
            "old_declared_labels": old_labels,
            "simulated_new_labels": simulated_labels,
            "old_answer_evidence": {
                "text_preview": (ans_text or "")[:100],
                "canonical_type": canonical,
                **old_g,
            },
            "simulated_answer_evidence": {
                **sim_g,
                "note": "answer text UNCHANGED; only labels list differs",
            },
            "answer_in_old_labels": old_g["answer_in_labels"],
            "answer_in_simulated_labels": sim_g["answer_in_labels"],
            "old_gate_decision": old_gate,
            "simulated_gate_decision_full_evaluate": sim_gate_full,
            "simulated_gate_error": sim_gate_error,
            "simulated_decision_grammar_path": sim_decision_grammar_path,
            "other_layers_pass": other_layers_pass,
            "simulated_reason_delta": reason_delta,
            "auto_delta_if_repair": auto_delta,
            "auto_delta_reason": auto_delta_reason,
            "boundary": {
                "question_boundary": list(mu.questions_lines or mu.stem_lines or []) if mu else None,
                "options_lines": list(mu.options_lines or []) if mu else None,
                "boundary_precision_issue": (
                    "observed: options_lines outside questions_lines"
                    if mu and mu.options_lines and (mu.questions_lines or mu.stem_lines)
                    and mu.options_lines[0] > (mu.questions_lines or mu.stem_lines or [0, 0])[-1]
                    else "none"
                ),
                "b_repair_depends_on_boundary": False,
                "note": (
                    "B label recognition uses options_lines content span + label token form; "
                    "does NOT require changing question boundary semantics. "
                    "boundary_precision_issue remains OBSERVED only (stop-condition monitor)."
                ),
            },
        }
        results.append(row)

        print(f"=== {meta['sample']} ({paper}/{root_id}) ===")
        print(f"  form: {meta['form']}")
        print(f"  labels: {old_labels} -> {simulated_labels}")
        print(f"  answer: {(ans_text or '')[:60]!r} letter={old_g['parsed_letter']}")
        print(f"  answer_in_labels: {old_g['answer_in_labels']} -> {sim_g['answer_in_labels']}")
        print(f"  verify: {old_g['verify_result']} -> {sim_g['verify_result']}")
        print(f"  old_gate: {old_gate['decision']} (S={old_gate['structural']} P={old_gate['provenance']} Sem={old_gate['semantic']})")
        print(f"  sim_decision_grammar_path: {sim_decision_grammar_path}")
        print(f"  auto_delta: {auto_delta} — {auto_delta_reason}")
        if reason_delta:
            print(f"  delta: {reason_delta}")
        print()

    # rollup
    total_auto_delta = sum(r.get("auto_delta_if_repair", 0) for r in results if "error" not in r)
    report = {
        "task": "P1.4-B Phase 1 READ-ONLY pre-repair impact simulation",
        "baseline": {
            "commit": "af70d64",
            "gate_auto": 154,
            "pending_review": 68,
            "rejected": 5,
            "option_survey": {"A": 151, "B": 3, "C": 1, "D": 29, "F": 23, "F0": 7},
        },
        "rules": {
            "no_assumption": "B=3 → auto+3 is FORBIDDEN; measured only",
            "authority": "Answer Evidence must NOT generate Option Evidence",
            "simulated_label_source": "SOURCE-LOCAL deterministic structure only",
            "production_changes": "NONE",
        },
        "samples": results,
        "rollup": {
            "b_samples": len(results),
            "sum_auto_delta_if_repair": total_auto_delta,
            "conclusion": (
                f"Simulated auto delta for repairing all 3 B labels = {total_auto_delta} "
                f"(NOT 3). Per-sample reasons in samples[].auto_delta_reason."
            ),
        },
    }
    out = OUT / "b_label_repair_simulation.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # markdown table
    lines = []
    lines.append("# P1.4-B Phase 1 — Pre-repair Impact Simulation (READ-ONLY)\n")
    lines.append("No production code / Schema / DB / Gate policy / Decomposition changed.")
    lines.append("Simulated labels come from SOURCE-LOCAL structure only. Answer never creates labels.\n")
    lines.append("## Delta table\n")
    lines.append("| sample | form | old labels | sim labels | ans | ans∈old | ans∈sim | old gate | sim gate (grammar path) | auto Δ |")
    lines.append("|--------|------|------------|------------|-----|---------|---------|----------|-------------------------|--------|")
    for r in results:
        if "error" in r:
            lines.append(f"| {r.get('sample')} | ERROR | | | | | | | | |")
            continue
        lines.append(
            f"| {r['sample']} | {r['form']} | {r['old_declared_labels']} | {r['simulated_new_labels']} "
            f"| {r['old_answer_evidence']['parsed_letter']} "
            f"| {r['answer_in_old_labels']} | {r['answer_in_simulated_labels']} "
            f"| {r['old_gate_decision']['decision']} | {r['simulated_decision_grammar_path']} "
            f"| {r['auto_delta_if_repair']} |"
        )
    lines.append(f"\n**Sum auto delta = {total_auto_delta}** (forbidden to assume 3).\n")
    lines.append("## Per-sample reasons\n")
    for r in results:
        if "error" in r:
            continue
        lines.append(f"### {r['sample']}\n")
        lines.append(f"- form: `{r['form']}` — {r['form_desc']}")
        lines.append(f"- source proof: {r['source_proof']}")
        lines.append(f"- simulated label source: {r['simulated_label_source']}")
        lines.append(f"- answer evidence: `{r['old_answer_evidence']['text_preview'][:80]}` → letter={r['old_answer_evidence']['parsed_letter']}")
        lines.append(f"- verify: {r['old_answer_evidence']['verify_result']} → {r['simulated_answer_evidence']['verify_result']}")
        lines.append(f"- old gate: `{r['old_gate_decision']['decision']}` (S={r['old_gate_decision']['structural']} P={r['old_gate_decision']['provenance']} Sem={r['old_gate_decision']['semantic']})")
        lines.append(f"- simulated decision (grammar path): `{r['simulated_decision_grammar_path']}`")
        lines.append(f"- other_layers_pass: {r['other_layers_pass']}")
        lines.append(f"- **auto Δ = {r['auto_delta_if_repair']}** — {r['auto_delta_reason']}")
        if r["simulated_reason_delta"]:
            lines.append(f"- reason delta: {r['simulated_reason_delta']}")
        bp = r["boundary"]
        lines.append(f"- boundary: q={bp['question_boundary']} o={bp['options_lines']} issue={bp['boundary_precision_issue']}")
        lines.append(f"- B repair depends on boundary change? **{bp['b_repair_depends_on_boundary']}**")
        lines.append("")
    lines.append("## Boundary precision (Q23)\n")
    lines.append("Q23 `q_boundary=[186,186]` / `options_lines=[188,194]` → `boundary_precision_issue = observed`.")
    lines.append("B label parsing uses options region content + label token form. **Does not require boundary semantics change.**")
    lines.append("If a future fix required boundary change → STOP CONDITION #1.\n")
    lines.append("## Authority red line\n")
    lines.append("```")
    lines.append("Answer Evidence → detect inconsistency ONLY")
    lines.append("Source Evidence → deterministic label parsing → recognize already-present label")
    lines.append("FORBIDDEN: answer letter → create option / infer missing content / LLM label")
    lines.append("```")
    (OUT / "b_label_repair_simulation.md").write_text("\n".join(lines), encoding="utf-8")
    print("rollup auto_delta_sum =", total_auto_delta)
    print("wrote", out)
    print("wrote", OUT / "b_label_repair_simulation.md")


if __name__ == "__main__":
    main()
