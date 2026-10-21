"""Option Evidence full-corpus survey (READ-ONLY).

Categories (Owner):
  A answer ∈ labels, options complete
  B answer ∉ labels, source HAS option content with missing label
  C answer ∉ labels, source has NO such option content
  D composite/sub decomposition → option attribution unclear
  E labels count abnormal but answer ∈ labels
  F answer evidence cannot be reliably located
  G option evidence inconsistent with question boundary

Baseline samples: 化学 Q23 (label-missing) vs 英语 Q5-6 (decomposition).
No code change. No DB write.
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
from app.domains.gate.grammar import _clean_answer  # noqa: E402
from app.domains.resolver.resolver import (  # noqa: E402
    SourceResolver,
    decode_answer_table_cell,
)
from app.domains.resolver.resolver import _label_offsets  # noqa: E402
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

CHOICE = {"single_choice", "multiple_choice", "true_false"}
# label markers in source (raw line): letter + separator
LAB_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])\s*[.．、:，,。)）]")


def source_labels_in_range(texts, lo, hi) -> dict[str, list[int]]:
    """All option-label tokens (first occurrence per letter) in [lo,hi] 1-based."""
    found: dict[str, list[int]] = {}
    if not lo or not hi:
        return found
    for i in range(max(1, lo), min(len(texts), hi) + 1):
        for m in LAB_RE.finditer(texts[i - 1]):
            lab = m.group(1).upper()
            found.setdefault(lab, []).append(i)
    return found


def answer_letter(text: str):
    """Best-effort canonical letter from answer text (for survey only)."""
    if not text:
        return None
    c = _clean_answer(text)
    m = re.fullmatch(r"[A-Za-z]", c)
    if m:
        return c.upper()
    # trailing/leading score forms
    m = re.fullmatch(r"(?:（\s*\d+\s*分\s*）|(\(\s*\d+\s*分\s*\)))?\s*([A-Za-z])\s*(?:（\s*\d+\s*分\s*）|\(\s*\d+\s*分\s*\))?", c)
    if m:
        return m.group(2).upper()
    # last ascii letter if short
    letters = [ch for ch in c if ch.isascii() and ch.isalpha()]
    if len(c) <= 8 and len(letters) == 1:
        return letters[0].upper()
    return None


def main() -> None:
    rows = []
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
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            is_comp = root.unit_type == "composite_unit"
            multi_qn = False
            try:
                multi_qn = len(leaves) > 1 or (
                    getattr(root, "question_number_range", None) and "-" in str(root.question_number_range)
                )
            except Exception:
                pass

            for leaf in leaves:
                canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
                if canonical not in CHOICE:
                    continue

                cl = c_by_id.get(leaf.unit_id)
                ans_c = next((c for c in leaf.content if c.role == "answer"), None)
                span = span_map.get(ans_c.span_id) if ans_c and ans_c.span_id else None
                ans_text = cl.answer.text if cl and cl.answer else None
                labels = tuple(str(o.label) for o in (cl.options if cl else ()))
                letter = answer_letter(ans_text)

                # question boundary: manifest unit for this root
                mu = next((u for u in m.units if u.unit_id == root.unit_id), None)
                q_lo = q_hi = None
                if mu:
                    if mu.questions_lines:
                        q_lo, q_hi = mu.questions_lines
                    elif mu.stem_lines:
                        q_lo, q_hi = mu.stem_lines
                o_lo = o_hi = None
                if mu and mu.options_lines:
                    o_lo, o_hi = mu.options_lines

                # source labels in options region / questions region
                scan_lo = o_lo or q_lo
                scan_hi = o_hi or q_hi
                src_labs = source_labels_in_range(texts, scan_lo, scan_hi)

                # F: answer evidence
                compiled_here = cl is not None
                if not compiled_here:
                    cat = "F0"
                    detail = "not compiled (IR incomplete / leaf absent) — out of answer-evidence scope"
                elif ans_c is None or ans_c.span_id is None or span is None:
                    cat = "F"
                    detail = "answer span missing/unresolved"
                elif not ans_text or not str(ans_text).strip():
                    cat = "F"
                    detail = "answer text empty after compile"
                elif letter is None:
                    cat = "F"
                    detail = f"answer text not a canonical letter: {(ans_text or '')[:40]!r}"
                # D: decomposition
                elif is_comp and (multi_qn or root.unit_id.startswith("U") or "-" in root.unit_id):
                    # composite with multi-qn or named as range → attribution risk
                    if letter not in labels:
                        cat = "D"
                        detail = (
                            f"composite {root.unit_id} letter {letter} ∉ labels={list(labels)}; "
                            f"sub={leaf.unit_id} qn={leaf.question_number}; "
                            f"SUB_QUESTION_DECOMPOSITION frozen"
                        )
                    else:
                        cat = "A"
                        detail = "composite but answer ∈ labels"
                # E: abnormal labels count but answer ∈ labels
                elif letter in labels and len(labels) < 2:
                    cat = "E"
                    detail = f"labels={list(labels)} abnormal but answer ∈ labels"
                # A: normal
                elif letter in labels:
                    cat = "A"
                    detail = f"answer {letter} ∈ labels={list(labels)}"
                else:
                    # answer ∉ labels — B vs C
                    if letter in src_labs:
                        cat = "B"
                        detail = (
                            f"answer {letter} ∉ resolved labels={list(labels)} BUT source has "
                            f"label {letter} at L{src_labs[letter][:3]} — label present, transport gap"
                        )
                    else:
                        # unlabeled option-like content inside the scanned region
                        # (use scan_hi = options_lines end, not just stem end)
                        last_opt_line = max(
                            [max(v) for v in src_labs.values()] or [scan_lo or 0]
                        )
                        has_extra = False
                        extra_line = None
                        extra_preview = None
                        if scan_hi:
                            for i in range(last_opt_line + 1, min(len(texts), scan_hi) + 1):
                                t = texts[i - 1].strip()
                                if t and not LAB_RE.search(t) and len(t) > 5:
                                    has_extra = True
                                    extra_line = i
                                    extra_preview = t[:80]
                                    break
                        if has_extra:
                            cat = "B"
                            detail = (
                                f"answer {letter} ∉ labels={list(labels)}; no {letter} label "
                                f"in source; OPTION_CONTENT_PRESENT_LABEL_MISSING at L{extra_line}: "
                                f"{extra_preview!r}"
                            )
                        else:
                            cat = "C"
                            detail = (
                                f"answer {letter} ∉ labels={list(labels)}; no {letter} label "
                                f"and no extra option content in scanned region "
                                f"L{scan_lo}-{scan_hi}"
                            )

                # G: option vs question boundary sanity
                g_note = ""
                if o_lo and q_lo and (o_lo < q_lo or (q_hi and o_hi and o_hi > q_hi)):
                    g_note = "options_lines outside questions_lines"

                rows.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "leaf": leaf.unit_id,
                    "unit_type": root.unit_type,
                    "qn": leaf.question_number,
                    "qtype": leaf.original_question_type,
                    "category": cat,
                    "detail": detail,
                    "answer_text_preview": (ans_text or "")[:80],
                    "answer_letter": letter,
                    "resolved_labels": list(labels),
                    "source_labels": {k: v[:3] for k, v in src_labs.items()},
                    "question_boundary": [q_lo, q_hi],
                    "options_lines": [o_lo, o_hi],
                    "answer_span": ans_c.span_id if ans_c else None,
                    "resolution_status": span.resolution_status if span else None,
                    "g_note": g_note or None,
                    "is_composite": is_comp,
                    "n_leaves_in_root": len(leaves),
                })

    tot = Counter(r["category"] for r in rows)
    by_paper = Counter((r["category"], r["paper"]) for r in rows)

    # baseline samples
    q23 = next((r for r in rows if r["paper"] == "化学" and r["root"] == "Q23"), None)
    q56 = [r for r in rows if r["paper"] == "英语" and "Q5-6" in r["root"]]

    report = {
        "metric_scope": "leaf (choice-type only)",
        "baseline": "af70d64",
        "note": (
            "READ-ONLY survey. Answer evidence may DETECT option-evidence "
            "inconsistency but must NEVER generate/infer option evidence "
            "(Authority: answer ↛ option)."
        ),
        "categories": {
            "A": "answer ∈ labels, options complete (normal)",
            "B": "answer ∉ labels, source HAS option content / missing label",
            "C": "answer ∉ labels, source has NO such option content",
            "D": "composite decomposition → option attribution unclear (frozen)",
            "E": "labels abnormal but answer ∈ labels",
            "F": "answer evidence cannot be reliably located (compiled)",
            "F0": "not compiled (IR incomplete) — excluded from answer-evidence scope",
            "G": "option evidence inconsistent with question boundary",
        },
        "totals": dict(tot),
        "by_category_paper": {f"{k[0]}|{k[1]}": v for k, v in by_paper.items()},
        "baseline_samples": {
            "chem_Q23_label_missing": q23,
            "english_Q5_6_decomposition": q56,
        },
        "rows": rows,
    }
    out = OUT / "option_evidence_survey.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("choice leaves surveyed:", len(rows))
    print("totals:", dict(tot))
    print()
    for cat in ("A", "B", "C", "D", "E", "F", "G", "F0"):
        sub = [r for r in rows if r["category"] == cat]
        if not sub:
            continue
        print(f"--- {cat} ({len(sub)}) ---")
        for r in sub[:8]:
            print(f"  {r['paper']} {r['root']:12} letter={r['answer_letter']} "
                  f"labels={r['resolved_labels']} src={list(r['source_labels'])}")
            print(f"     {r['detail'][:100]}")
        if len(sub) > 8:
            print(f"  ... +{len(sub)-8} more")
    print("\nchem Q23:", q23 and q23["category"], q23 and q23["detail"][:80])
    print("english Q5-6:", [(r["category"], r["detail"][:70]) for r in q56])
    print("wrote", out)


if __name__ == "__main__":
    main()
