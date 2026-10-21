"""answer_not_expressible root cause split (read-only).

Level 1 taxonomy — first failing contract in the grammar pipeline:
  A. no_answer_text
  B. answer_span_invalid
  C. answer_text_present_grammar_fail
  D. qtype_contract_mismatch
  E. impossible_state

Each row carries: paper, root/leaf, qtype, answer.text, span evidence,
resolution_status, grammar path, first failing contract, classification.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\PHASE1-E2E-REPLAY")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.compile import map_canonical_type  # noqa: E402
from app.domains.gate import STRICT_AUTO_TYPES  # noqa: E402
from app.domains.gate.grammar import verify, _clean_answer  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
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


def classify_leaf(leaf, span_map) -> dict:
    """First failing contract + proposed classification for one leaf."""
    ans_c = next((c for c in leaf.content if c.role == "answer"), None)
    span = span_map.get(ans_c.span_id) if ans_c and ans_c.span_id else None
    canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
    qt = leaf.canonical_question_type or canonical

    # --- first failing contract walk ---
    # A. no answer declared / no answer text
    if ans_c is None or ans_c.span_id is None:
        return {
            "level1": "A",
            "first_failing_contract": "answer not declared or span unresolved (IR content)",
            "grammar_path": "n/a",
        }
    if span is None:
        return {
            "level1": "B",
            "first_failing_contract": "answer span_id not in ResolvedRun",
            "grammar_path": "n/a",
        }
    # B. span contract (resolution)
    if span.resolution_status not in {"exact", "normalized"}:
        return {
            "level1": "B",
            "first_failing_contract": f"span resolution_status={span.resolution_status} not byte-proven",
            "grammar_path": "n/a (blocked before grammar)",
        }

    # text
    text = None
    # get compiled text if we can; fall back to reconstructing from span later
    return None  # filled by caller with compiled answer text


def classify_with_text(leaf, span, text, canonical, labels) -> dict:
    """Classification when we have answer text."""
    if text is None or not str(text).strip():
        return {
            "level1": "A",
            "first_failing_contract": "answer text empty after compile",
            "grammar_path": "verify() not reached — no text",
            "cleaned": "",
        }

    cleaned = _clean_answer(text)

    # D. qtype not in STRICT_AUTO — capability boundary, not grammar failure
    if canonical not in STRICT_AUTO_TYPES:
        return {
            "level1": "D",
            "first_failing_contract": f"qtype {canonical!r} ∉ STRICT_AUTO_TYPES (capability boundary)",
            "grammar_path": "grammar=None (not strict-auto)",
            "cleaned": cleaned[:80],
        }

    # C. grammar attempt
    result = verify(canonical, text, labels)
    if result is True:
        return {
            "level1": "PASS",
            "first_failing_contract": None,
            "grammar_path": "verify()=True",
            "cleaned": cleaned[:80],
        }

    # C vs D: if text looks like wrong-type content for the qtype
    # e.g. single_choice but text is long prose → could be D (qtype mismatch)
    # or C (grammar whitelist gap)
    level2 = _level2(text, cleaned, canonical, result)
    return {
        "level1": "C",
        "first_failing_contract": (
            f"answer text present; verify({canonical}, ...)={result!r} — "
            f"canonical grammar rejects"
        ),
        "grammar_path": f"verify()={result!r} after _clean_answer",
        "cleaned": cleaned[:120],
        "level2": level2,
    }


def _level2(text, cleaned, canonical, result) -> str:
    t = (text or "").strip()
    # long natural language in a choice type → qtype mismatch suspect
    if canonical in {"single_choice", "multiple_choice", "true_false"}:
        if len(cleaned) > 20:
            return "D-suspect: long prose in choice-type answer (qtype/answer mismatch?)"
        if any(ch in t for ch in "，。；：、！？") and len(cleaned) > 6:
            return "C-natural_language: Chinese prose not canonicalisable to option letter"
        if t.count("<") >= 2 or "table" in t.lower():
            return "C-html_table: table markup not decoded to cell"
        if any(x in t for x in ("甲", "乙", "丙", "①", "②", "③", "④")):
            return "C-non_ascii_token: circled/CJK tokens not in grammar whitelist"
        return "C-unknown_form: token not matching _SC_FORMS_RE / _MC_TOKEN_RE"
    # non-strict types shouldn't reach here; if they do treat as D
    return "D-other"


def main() -> None:
    rows = []
    tot = Counter()
    for p in find_manifests(CORPUS):
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
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)
        c_by_id = {l.unit_id: l for l in compiled.leaves}

        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if d.get("decision") == "auto_approve":
                continue  # only care about non-auto

            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            # classify each leaf; root classification = worst / first
            leaf_rows = []
            for leaf in leaves:
                ans_c = next((c for c in leaf.content if c.role == "answer"), None)
                span = span_map.get(ans_c.span_id) if ans_c and ans_c.span_id else None
                canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
                cl = c_by_id.get(leaf.unit_id)
                ans_text = cl.answer.text if cl and cl.answer else None
                labels = tuple(str(o.label) for o in (cl.options if cl else ()))

                if ans_c is None or ans_c.span_id is None:
                    info = {
                        "level1": "A",
                        "first_failing_contract": "answer not declared or span unresolved",
                        "grammar_path": "n/a",
                    }
                elif span is None:
                    info = {
                        "level1": "B",
                        "first_failing_contract": "answer span_id not in ResolvedRun",
                        "grammar_path": "n/a",
                    }
                elif span.resolution_status not in {"exact", "normalized"}:
                    info = {
                        "level1": "B",
                        "first_failing_contract": f"resolution_status={span.resolution_status}",
                        "grammar_path": "n/a (blocked before grammar)",
                    }
                elif ans_text is None or not str(ans_text).strip():
                    info = {
                        "level1": "A",
                        "first_failing_contract": "answer text empty after compile",
                        "grammar_path": "verify() not reached",
                    }
                else:
                    info = classify_with_text(leaf, span, ans_text, canonical, labels)

                leaf_rows.append({
                    "leaf": leaf.unit_id,
                    "qtype": leaf.original_question_type,
                    "canonical_qtype": canonical,
                    "answer_text_preview": (ans_text or "")[:160],
                    "answer_text_len": len(ans_text or ""),
                    "span_id": ans_c.span_id if ans_c else None,
                    "span_evidence": list(span.evidence) if span else [],
                    "resolution_status": span.resolution_status if span else None,
                    "granularity": span.granularity if span else None,
                    **info,
                })

            # root gate reasons for cross-check
            gate_reasons = [r[:100] for r in (d.get("reasons") or [])[:8]]
            has_grammar_reason = any("grammar" in r or "expressible" in r or "no answer" in r
                                     for r in gate_reasons)
            # root Level-1 = first non-PASS leaf classification priority A>B>C>D
            order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
            best = min(leaf_rows, key=lambda x: order.get(x["level1"], 9)) if leaf_rows else None

            rows.append({
                "paper": p.parent.name,
                "root": root.unit_id,
                "unit_type": root.unit_type,
                "decision": d.get("decision"),
                "gate_reasons": gate_reasons,
                "has_grammar_reason": has_grammar_reason,
                "root_level1": best["level1"] if best else "E",
                "root_first_failing": best["first_failing_contract"] if best else "no leaves",
                "leaves": leaf_rows,
            })
            tot[best["level1"] if best else "E"] += 1
            if has_grammar_reason:
                tot["gate_reason_mentions_grammar"] += 1

    # Level-2 rollup for C
    l2 = Counter()
    for r in rows:
        for lf in r["leaves"]:
            if lf["level1"] == "C" and lf.get("level2"):
                l2[lf["level2"]] += 1

    report = {
        "metric_scope": "root",
        "note": (
            "Only non-auto ready roots. Level-1 = first failing contract in "
            "answer/grammar pipeline. 'answer_not_expressible' is an EXIT label; "
            "this split names the FIRST failing contract layer."
        ),
        "totals_level1": dict(tot),
        "totals_level2_for_C": dict(l2),
        "n_roots": len(rows),
        "rows": rows,
    }
    out = OUT / "answer_not_expressible_split.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("roots analysed:", len(rows))
    print("Level-1:", dict(tot))
    print("Level-2 (C):")
    for k, v in l2.most_common():
        print(f"  {v:3d}  {k}")
    print("wrote", out)

    # compact table
    print("\nroot-level table:")
    for r in rows:
        print(f"  {r['paper']:4} {r['root']:14} {r['decision']:14} L1={r['root_level1']} "
              f"| {r['root_first_failing'][:60]}")


if __name__ == "__main__":
    main()
