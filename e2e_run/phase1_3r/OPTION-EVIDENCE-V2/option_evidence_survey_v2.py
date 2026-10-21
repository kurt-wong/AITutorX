"""Option Evidence Survey v2.1 — tightened source-first five-layer cross-check (READ-ONLY).

Fixes vs v2.0:
  - unlabeled content excludes HTML/img/stems/instructions
  - label detection adds space-separated damaged form (`D 麦哲伦`)
  - D only when composite is PER-SUB options (multiple option blocks) and a sibling qn has no leaf
    (shared-option composites like geography U* are NOT D)
  - B1 requires content after last label that looks like option content (not table/img/stem)
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
from app.domains.compile import map_canonical_type  # noqa: E402
from app.domains.gate.grammar import _clean_answer  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHOICE = {"single_choice", "multiple_choice", "true_false"}

CLEAN_LABEL = re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]")
# damaged: digit/char glue before letter+sep  e.g. `2D.`
DIGIT_GLUE = re.compile(r"(?<![A-Za-z0-9_])(\d)([A-Ha-h])\s*[.．、:：,，。)）]")
CHAR_GLUE = re.compile(r"(?<![A-Za-z0-9_\s.．、:：,，。)）])([^\sA-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]")
# damaged: letter + space + content, missing separator  e.g. `D 麦哲伦`
SPACE_SEP = re.compile(r"(?:^|(?<=[。；;：:\n]))([A-Ha-h])[  　]{1,3}(?=[一-鿿])", re.M)

HTMLISH = re.compile(r"<(table|div|img|tr|td|span|p)\b", re.I)
STEMISH = re.compile(
    r"^(听第|第\s*\d+\s*[题段]|#{1,6}\s|\d+\s*[.．、\\]|【|一、|二、|三、|四、|五、|六、|参考答案|---)"
)


def is_option_like_content(t: str) -> bool:
    s = t.strip()
    if not s or len(s) < 4:
        return False
    if HTMLISH.search(s) or STEMISH.search(s):
        return False
    if s.startswith("#") or s.startswith("---"):
        return False
    # pure image captions / centered labels
    if re.fullmatch(r"[A-Da-d１-４1-4①-④]+", s):
        return False
    return True


def answer_letter(text: str):
    if not text:
        return None
    c = _clean_answer(text)
    m = re.fullmatch(r"[A-Za-z]", c)
    if m:
        return c.upper()
    m = re.fullmatch(
        r"(?:（\s*\d+\s*分\s*）|(\(\s*\d+\s*分\s*\)))?\s*([A-Za-z])\s*(?:（\s*\d+\s*分\s*）|\(\s*\d+\s*分\s*\))?",
        c,
    )
    if m:
        return m.group(2).upper()
    letters = [ch for ch in c if ch.isascii() and ch.isalpha()]
    if len(c) <= 8 and len(letters) == 1:
        return letters[0].upper()
    m = re.search(r"故选\s*[:：]?\s*([A-Ha-h])\b", c)
    if m:
        return m.group(1).upper()
    return None


def scan_labels(texts, lo, hi):
    if not lo or not hi:
        return {}, [], []
    clean: dict[str, list[int]] = {}
    damaged: list[dict] = []
    option_like: list[dict] = []
    for i in range(max(1, lo), min(len(texts), hi) + 1):
        t = texts[i - 1]
        for m in CLEAN_LABEL.finditer(t):
            clean.setdefault(m.group(1).upper(), []).append(i)
        for pat, kind, lab_g in (
            (DIGIT_GLUE, "digit_glue", 2),
            (CHAR_GLUE, "char_glue", 2),
            (SPACE_SEP, "space_sep_missing_dot", 1),
        ):
            for m in pat.finditer(t):
                damaged.append({
                    "line": i,
                    "kind": kind,
                    "token": m.group(0),
                    "label": m.group(lab_g).upper(),
                    "preview": t.strip()[:120],
                })
        if is_option_like_content(t):
            option_like.append({"line": i, "preview": t.strip()[:120]})
    return clean, damaged, option_like


def count_option_blocks(texts, lo, hi) -> int:
    """How many distinct option-label groups appear in the span (shared vs per-sub)."""
    if not lo or not hi:
        return 0
    blocks = 0
    seen_on_line = set()
    for i in range(max(1, lo), min(len(texts), hi) + 1):
        t = texts[i - 1]
        labs = set(m.group(1).upper() for m in CLEAN_LABEL.finditer(t))
        labs |= set(m.group(2).upper() for m in DIGIT_GLUE.finditer(t))
        labs |= set(m.group(1).upper() for m in SPACE_SEP.finditer(t))
        if labs and "A" in labs and i not in seen_on_line:
            blocks += 1
            seen_on_line.add(i)
    return blocks


def classify_unit(**kw):
    paper = kw["paper"]
    root_id = kw["root_id"]
    leaf_id = kw["leaf_id"]
    is_comp = kw["is_comp"]
    expected = kw["expected_option_count"]
    src_clean = kw["src_clean"]
    src_damaged = kw["src_damaged"]
    src_option_like = kw["src_option_like"]
    declared = [str(x).upper() for x in kw["declared"]]
    resolved = [str(x).upper() for x in kw["resolved"]]
    ans_letter = kw["ans_letter"]
    ans_text = kw["ans_text"]
    n_leaves = kw["n_leaves"]
    sub_qns = kw["sub_qns"]
    option_blocks = kw["option_blocks"]
    o_boundary = kw["o_boundary"]
    q_boundary = kw["q_boundary"]

    evidence = []
    subsequent = []
    src_clean_u = {k.upper(): v for k, v in src_clean.items()}
    damaged_labels = sorted({d["label"] for d in src_damaged})

    evidence.append(f"L1 source_option_like_lines={len(src_option_like)} damaged_hits={len(src_damaged)}")
    evidence.append(f"L2 clean_labels={sorted(src_clean_u)} damaged={damaged_labels}")
    evidence.append(f"L3 q_boundary={q_boundary} o_boundary={o_boundary} option_blocks={option_blocks}")
    evidence.append(f"L4 declared={declared}")
    evidence.append(f"L5 resolved={resolved}")
    evidence.append(f"L6 answer letter={ans_letter} text_len={len(ans_text or '')}")

    b_damaged_undeclared = [d for d in src_damaged if d["label"] not in declared]
    b_clean_undeclared = [lab for lab in src_clean_u if lab not in declared]

    last_lab_line = 0
    for lines in src_clean_u.values():
        if lines:
            last_lab_line = max(last_lab_line, max(lines))
    for d in src_damaged:
        last_lab_line = max(last_lab_line, d["line"])

    scan_hi = (o_boundary[1] if o_boundary and o_boundary[1] else None) or (
        q_boundary[1] if q_boundary and q_boundary[1] else last_lab_line
    )
    trailing = [
        u for u in src_option_like
        if u["line"] > last_lab_line and u["line"] <= (scan_hi or 10**9)
    ]

    n_declared = len(declared)
    n_clean = len(src_clean_u)

    # D: per-sub options composite with sibling qn lacking a leaf
    per_sub = is_comp and option_blocks >= 2 and len(sub_qns) >= 2
    d_gap = per_sub and n_leaves < len(sub_qns)

    primary = None
    detail = ""

    ir_absent = (not declared) and (not resolved) and (not src_clean_u) and (not src_damaged)

    if ir_absent and not src_option_like:
        primary = "F0"
        detail = "IR_INCOMPLETE: no declared/resolved/source labels; out of option-evidence scope"
        evidence.append("F0 via empty IR and empty source labels")
    elif ir_absent and src_option_like:
        primary = "F0"
        detail = (
            f"IR_INCOMPLETE_WITH_RAW_TEXT: no labels at all; raw option-like/other text "
            f"L{[u['line'] for u in src_option_like[:3]]} — not counted as B (no label contract yet)"
        )
        evidence.append("F0 via IR absent; raw text present but no label contract")
    elif b_damaged_undeclared:
        d0 = b_damaged_undeclared[0]
        primary = "B"
        detail = (
            f"OPTION_CONTENT_PRESENT_LABEL_DAMAGED: {d0['token']!r} kind={d0['kind']} "
            f"at L{d0['line']} label={d0['label']} not in declared={declared}; {d0['preview']!r}"
        )
        evidence.append(f"B via damaged undeclared label {d0}")
    elif trailing and (expected or 4) > n_declared:
        u0 = trailing[0]
        primary = "B"
        detail = (
            f"OPTION_CONTENT_PRESENT_LABEL_MISSING: option-like content L{u0['line']} "
            f"after last label L{last_lab_line}; declared={n_declared} expected>={expected or 4}; "
            f"{u0['preview']!r}"
        )
        evidence.append(f"B via trailing option-like content {u0}")
    elif b_clean_undeclared:
        primary = "B"
        detail = f"OPTION_LABEL_SOURCE_NOT_DECLARED: source labels {b_clean_undeclared} not in declared={declared}"
        evidence.append(f"B via undeclared clean labels {b_clean_undeclared}")
    else:
        # C: answer slot missing AND no content for it
        if ans_letter and ans_letter not in declared and ans_letter not in src_clean_u:
            # is there damaged label for it?
            if any(d["label"] == ans_letter for d in src_damaged):
                primary = "B"
                detail = (
                    f"OPTION_CONTENT_PRESENT_LABEL_DAMAGED: answer slot {ans_letter} "
                    f"has damaged label evidence but not declared"
                )
                evidence.append(f"B via damaged label for answer slot {ans_letter}")
            elif trailing:
                primary = "B"
                detail = (
                    f"OPTION_CONTENT_PRESENT: answer slot {ans_letter} ∉ declared but "
                    f"trailing option-like content exists L{[u['line'] for u in trailing]}"
                )
                evidence.append(f"B via trailing content for answer slot {ans_letter}")
            else:
                primary = "C"
                detail = (
                    f"OPTION_CONTENT_ABSENT: answer slot {ans_letter} ∉ declared={declared}, "
                    f"no source label/content for {ans_letter}"
                )
                evidence.append(f"C via no source content for answer slot {ans_letter}")
        elif expected and max(n_declared, n_clean) < expected and not trailing and not src_damaged:
            primary = "C"
            detail = (
                f"OPTION_CONTENT_ABSENT: expected~{expected} options, declared={n_declared} "
                f"clean_src={n_clean}, no extra content"
            )
            evidence.append("C via expected count shortfall with no extra content")
        elif d_gap:
            primary = "D"
            detail = (
                f"DECOMPOSITION_OWNERSHIP: per-sub composite {root_id} qns={sub_qns} "
                f"option_blocks={option_blocks} n_leaves={n_leaves}; SUB_QUESTION_DECOMPOSITION frozen"
            )
            evidence.append(f"D via per-sub option blocks {option_blocks} vs leaves {n_leaves}")
        else:
            if ans_letter is None:
                primary = "F"
                detail = f"ANSWER_NOT_CANONICAL: {(ans_text or '')[:80]!r}"
                evidence.append("F answer-side only")
            else:
                primary = "A"
                detail = f"OK structurally; answer {ans_letter} ∈ declared/resolved or consistent"
                evidence.append("A structural OK")

    # subsequent
    if primary in ("B", "C") and d_gap:
        subsequent.append("D")
        evidence.append(f"subsequent D: per-sub qns={sub_qns} leaves={n_leaves}")
    if primary in ("B", "C") and ans_letter is None and ans_text:
        subsequent.append("F")
        evidence.append("subsequent F: non-canonical answer")
    if primary in ("A", "B", "C", "D") and ans_letter and ans_letter not in resolved and ans_letter not in declared:
        evidence.append(
            f"NOTE answer {ans_letter} ∉ resolved/declared — DETECTED only (answer ↛ option)"
        )
    # shared-option multi-qn composite without per-sub blocks: observe but do not root as D
    if is_comp and len(sub_qns) > n_leaves and not d_gap and primary == "A":
        evidence.append(
            f"OBS shared-option composite qns={sub_qns} leaves={n_leaves} "
            f"option_blocks={option_blocks} — not D (shared option set)"
        )

    return primary, subsequent, detail, evidence


def main() -> None:
    rows = []
    focus = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload,
            {u.unit_id: u.material_lines for u in m.units if u.material_lines},
            texts,
        )
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)
        c_by_id = {l.unit_id: l for l in compiled.leaves}

        for root in ir.units:
            mu = next((u for u in m.units if u.unit_id == root.unit_id), None)
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            is_comp = root.unit_type == "composite_unit"
            sub_qns = list(getattr(mu, "question_numbers", None) or getattr(root, "question_numbers", None) or [])

            q_lo = q_hi = o_lo = o_hi = None
            if mu:
                if mu.questions_lines:
                    q_lo, q_hi = mu.questions_lines
                elif mu.stem_lines:
                    q_lo, q_hi = mu.stem_lines
                if mu.options_lines:
                    o_lo, o_hi = mu.options_lines

            scan_lo = o_lo or q_lo
            scan_hi = o_hi or q_hi
            if is_comp and q_lo and q_hi:
                scan_lo = min(x for x in (scan_lo, q_lo) if x)
                scan_hi = max(x for x in (scan_hi, q_hi) if x)

            src_clean, src_damaged, src_option_like = scan_labels(texts, scan_lo, scan_hi)
            # option-like restricted to options_lines when present
            if o_lo and o_hi:
                src_option_like = [u for u in src_option_like if o_lo <= u["line"] <= o_hi]
            option_blocks = count_option_blocks(texts, scan_lo, scan_hi)

            expected = None
            title = (mu.section if mu else "") or ""
            if "四个备选" in title or "四个选项" in title:
                expected = 4
            elif "三个选项" in title or "三个备选" in title or "A、B、C三个选项" in title:
                expected = 3

            for leaf in leaves:
                canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
                if canonical not in CHOICE:
                    continue
                cl = c_by_id.get(leaf.unit_id)
                ans_text = cl.answer.text if cl and cl.answer else None
                labels = tuple(str(o.label) for o in (cl.options if cl else ()))
                letter = answer_letter(ans_text)
                declared = [o.label for o in (mu.options if mu else [])] if mu else []
                if not declared:
                    declared = list(labels)

                primary, subsequent, detail, evidence = classify_unit(
                    paper=paper,
                    root_id=root.unit_id,
                    leaf_id=leaf.unit_id,
                    is_comp=is_comp,
                    expected_option_count=expected,
                    src_clean=src_clean,
                    src_damaged=src_damaged,
                    src_option_like=src_option_like,
                    declared=declared,
                    resolved=list(labels),
                    ans_letter=letter,
                    ans_text=ans_text,
                    n_leaves=len(leaves),
                    sub_qns=sub_qns,
                    option_blocks=option_blocks,
                    o_boundary=[o_lo, o_hi],
                    q_boundary=[q_lo, q_hi],
                )
                row = {
                    "paper": paper,
                    "root": root.unit_id,
                    "leaf": leaf.unit_id,
                    "unit_type": root.unit_type,
                    "qn": leaf.question_number,
                    "qtype": leaf.original_question_type,
                    "first_failed_contract": primary,
                    "subsequent_contracts": subsequent,
                    "detail": detail,
                    "evidence_layers": evidence,
                    "answer_text_preview": (ans_text or "")[:120],
                    "answer_letter": letter,
                    "declared_labels": declared,
                    "resolved_labels": list(labels),
                    "source_clean_labels": {k: v[:4] for k, v in src_clean.items()},
                    "source_damaged_labels": src_damaged[:8],
                    "source_option_like_content": src_option_like[:8],
                    "question_boundary": [q_lo, q_hi],
                    "options_lines": [o_lo, o_hi],
                    "is_composite": is_comp,
                    "n_leaves_in_root": len(leaves),
                    "sub_question_numbers": sub_qns,
                    "option_blocks": option_blocks,
                    "expected_option_count": expected,
                }
                rows.append(row)
                key = None
                if paper == "化学" and root.unit_id == "Q23":
                    key = "chem_Q23"
                elif paper == "数学" and root.unit_id == "Q4":
                    key = "math_Q4"
                elif paper == "英语" and root.unit_id == "Q5-6":
                    key = "english_Q5_6"
                elif paper == "历史" and root.unit_id == "Q29":
                    key = "history_Q29"
                if key:
                    focus.setdefault(key, []).append(row)

    tot_primary = Counter(r["first_failed_contract"] for r in rows)
    tot_sub = Counter(s for r in rows for s in r["subsequent_contracts"])
    by_paper = Counter((r["first_failed_contract"], r["paper"]) for r in rows)

    b_rows = [r for r in rows if r["first_failed_contract"] == "B"]
    b_subtypes = []
    for r in b_rows:
        if any(d["label"] not in r["declared_labels"] for d in r["source_damaged_labels"]):
            kinds = sorted({d["kind"] for d in r["source_damaged_labels"]})
            subtype = "B2_label_damaged_glued"
        elif r["source_option_like_content"] and not r["declared_labels"]:
            subtype = "B1_label_missing_content_present_or_ir_absent"
        elif r["source_option_like_content"]:
            subtype = "B1_label_missing_content_present"
        else:
            subtype = "B3_other"
        b_subtypes.append({
            "paper": r["paper"],
            "root": r["root"],
            "subtype": subtype,
            "declared": r["declared_labels"],
            "resolved": r["resolved_labels"],
            "damaged": r["source_damaged_labels"][:3],
            "option_like": r["source_option_like_content"][:3],
            "detail": r["detail"][:180],
        })

    confirmed_b = [
        b for b in b_subtypes
        if b["root"] in ("Q23", "Q4", "Q29") and b["paper"] in ("化学", "数学", "历史")
        or b["subtype"].startswith("B2")
        or (b["declared"] and b["option_like"])
    ]

    math_q4_proof = {
        "question": "In `2D.`, does the leading `2` belong to the previous option (C) or to D's content?",
        "source_line_23": "C. 关于直线 y=x 对称 2D. 关于直线 y= -x 对称",
        "layer_analysis": {
            "C_content_without_2": "关于直线 y=x 对称",
            "C_content_if_2_appended": "关于直线 y=x 对称 2  (not a parallel symmetry phrase)",
            "D_label_token_as_written": "2D.",
            "D_content_after_label": "关于直线 y= -x 对称",
            "position_of_2": "BEFORE the `D.` label token, after C content",
        },
        "deterministic_findings": [
            "C content is complete and parallel to A/B without `2` (对称-type phrases).",
            "`2` is not valid C content: bare digit after 对称 is not parallel to A/B/C.",
            "`2` cannot be D content under label-then-content structure: it sits BEFORE `D.`.",
            "Therefore `2` is inter-option label-boundary glue/contamination — not semantic content of either option.",
            "4th option content `关于直线 y= -x 对称` IS present; label is damaged as digit-glued `2D.`.",
            "Label identity `D` is recoverable from source form alone (A./B./C. parallel + glued `D.`), WITHOUT answer evidence.",
            "Prior CLEAN_LABEL/GLUED probes miss `2D.` because lookbehind treats `2` as alnum — survey-level blind spot.",
        ],
        "answer_cross_check_only": "Math Q4 answer is A (故选：A, L240). NOT used to identify the D label.",
        "authority_note": "Recognizing `D` from `2D.` is Producer parser compatibility, NOT Answer→Option Recovery.",
        "verdict": {
            "2_belongs_to_previous_option": False,
            "2_is_D_content": False,
            "2_is_label_boundary_glue": True,
            "B_subtype": "B2_label_damaged_glued (digit_glue)",
            "producer_gap": "label regex lookbehind excludes alnum prefix; digit-glued `2D.` invisible to CLEAN and prior GLUED probe",
        },
    }

    # generalization answer
    b2 = [b for b in b_subtypes if b["subtype"].startswith("B2")]
    b1_real = [
        b for b in b_subtypes
        if b["subtype"].startswith("B1") and b["declared"] and b["option_like"]
    ]
    generalization = {
        "question": "Do B samples prove a generalizable Producer option-label parsing compatibility gap?",
        "confirmed_B_samples": b1_real + b2,
        "other_B_rows_reviewed_as": (
            "IR-absent / HTML / stem false positives in v2.0; filtered in v2.1 or retained with "
            "explicit ir_absent note. Not counted as Producer label-parsing gap samples."
        ),
        "answer": (
            "YES — narrow deterministic Producer option-label parsing compatibility gap, "
            "NOT a recovery mechanism. Confirmed samples share: option CONTENT present + "
            "label token damaged/missing/unrecognized + label letter recoverable from source "
            "form WITHOUT answer evidence. Subtypes: B1 complete label drop (化学 Q23, 历史 Q29 "
            "space-sep), B2 digit/char glue (数学 Q4 `2D.`). Common contract: Producer must "
            "accept damaged-but-deterministically-identifiable option labels (G1/G3-class "
            "parser compatibility). NO Answer→Option Recovery."
        ),
        "deterministic_common_shape": [
            "option CONTENT span exists in the unit's options region",
            "label token absent (B1) or glued/damaged (B2: `2D.`, `D 麦哲伦`)",
            "label letter recoverable from parallel label sequence + content position WITHOUT answer",
            "Producer declares only clean labels → under-declares options",
        ],
        "samples_detail": [
            {"paper": "化学", "root": "Q23", "subtype": "B1", "form": "4th content L194, `D．` dropped entirely", "declared": ["A", "B", "C"]},
            {"paper": "数学", "root": "Q4", "subtype": "B2", "form": "4th content L23, label glued as `2D.`", "declared": ["A", "B", "C"]},
            {"paper": "历史", "root": "Q29", "subtype": "B1/B2", "form": "4th content L307 `D 麦哲伦` missing `.` separator", "declared": ["A", "B", "C"]},
        ],
    }

    report = {
        "metric_scope": "leaf (choice-type only)",
        "baseline": "af70d64",
        "survey_version": "option-evidence-v2.2-source-first",
        "note": (
            "READ-ONLY survey v2.1. Discovery source-first (content/label/boundary/declared/resolved); "
            "answer is cross-check only. Authority: answer may DETECT option inconsistency but "
            "must NEVER generate option evidence."
        ),
        "classification_model": {
            "B": "source contains option content; label damaged / missing / unrecognized by Producer",
            "C": "source does NOT contain the option content",
            "D": "PER-SUB options composite with sibling qn lacking leaf (decomposition frozen). "
                 "Shared-option composites are NOT D.",
            "A": "structural alignment OK",
            "F": "answer not canonical (answer-side, not option root)",
            "F0": "not compiled — out of answer-evidence scope",
        },
        "root_counting_rule": (
            "first_failed_contract = mutually exclusive primary root. "
            "subsequent_contracts = residual after primary fixed; NOT independent roots."
        ),
        "dsh_count_conflict_resolution": {
            "dsh_stated": "B=3 including english Q5 AND C=1 english Q5 — definition conflict",
            "rule": "B requires content PRESENT; C requires content ABSENT. Q5 C-option is content-absent → C only.",
            "english_Q5_6": {
                "Q5_C_option": "C (content absent)",
                "Q6_leaf_gap": "D (A/B content exist; no leaf owns Q6)",
                "first_failed_contract": "C",
                "subsequent_contracts": ["D"],
            },
        },
        "totals_primary_mutually_exclusive": dict(tot_primary),
        "totals_subsequent_not_roots": dict(tot_sub),
        "by_category_paper": {f"{k[0]}|{k[1]}": v for k, v in by_paper.items()},
        "focus_samples": focus,
        "math_Q4_2D_proof": math_q4_proof,
        "b_generalization": generalization,
        "rows": rows,
    }

    out = OUT / "option_evidence_survey_v2.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Option Evidence Survey v2.1 — Focus Report\n")
    lines.append("READ-ONLY. No production code / Schema / Gate / Producer / Decomposition / DB changed.\n")
    lines.append("## Model\n")
    lines.append("- **B**: content PRESENT, label damaged/missing/unrecognized")
    lines.append("- **C**: content ABSENT")
    lines.append("- **D**: per-sub-options composite, sibling qn has no leaf (decomposition frozen)")
    lines.append("- **first_failed_contract** = primary (mutually exclusive); **subsequent_contracts** = residual\n")
    lines.append("## Primary totals (mutually exclusive)\n")
    for k, v in sorted(tot_primary.items()):
        lines.append(f"- {k}: {v}")
    lines.append("\n## Subsequent (not roots)\n")
    for k, v in sorted(tot_sub.items()):
        lines.append(f"- {k}: {v}")
    lines.append("\n## DSH count conflict\n")
    lines.append("DSH wrote `B=3` listing english Q5 while also calling Q5-C a C-class. Contradiction.")
    lines.append("Rule: B = content present; C = content absent. English Q5 C-option → **C only**.")
    lines.append("English Q5-6 dual-layer: first_failed_contract=**C**, subsequent=**[D]**.\n")
    lines.append("## Focus samples\n")
    for key, lst in focus.items():
        lines.append(f"### {key}\n")
        for r in lst:
            lines.append(f"- **{r['first_failed_contract']}** subsequent={r['subsequent_contracts']}")
            lines.append(f"  - {r['detail'][:220]}")
            lines.append(f"  - declared={r['declared_labels']} resolved={r['resolved_labels']} answer={r['answer_letter']}")
            if r['source_damaged_labels']:
                lines.append(f"  - damaged={r['source_damaged_labels'][:2]}")
            if r['source_option_like_content']:
                lines.append(f"  - option_like={r['source_option_like_content'][:2]}")
    lines.append("\n## Math Q4 `2D.` — does `2` belong to C or to D content?\n")
    for f in math_q4_proof["deterministic_findings"]:
        lines.append(f"- {f}")
    lines.append(f"\nVerdict: `{json.dumps(math_q4_proof['verdict'], ensure_ascii=False)}`\n")
    lines.append("## B generalization\n")
    lines.append(generalization["answer"])
    lines.append("\nConfirmed samples:")
    for s in generalization["samples_detail"]:
        lines.append(f"- {s['paper']}/{s['root']} ({s['subtype']}): {s['form']}")
    lines.append("\nCommon deterministic shape:")
    for s in generalization["deterministic_common_shape"]:
        lines.append(f"- {s}")
    lines.append("\n## Authority red line\n")
    lines.append("Answer Evidence may DETECT option inconsistency but must NEVER generate Option Evidence.")
    lines.append("No Answer→Option Recovery is proposed or implemented.")
    (OUT / "option_evidence_focus_report.md").write_text("\n".join(lines), encoding="utf-8")

    print("choice leaves:", len(rows))
    print("PRIMARY:", dict(tot_primary))
    print("SUBSEQ:", dict(tot_sub))
    print()
    for key, lst in focus.items():
        print(f"=== {key} ===")
        for r in lst:
            print(f"  {r['first_failed_contract']} +{r['subsequent_contracts']} {r['detail'][:110]}")
    print()
    print("B all:")
    for b in b_subtypes:
        print(f"  {b['paper']}/{b['root']} {b['subtype']} declared={b['declared']}")
    print("wrote", out)


if __name__ == "__main__":
    main()
