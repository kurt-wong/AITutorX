"""INDEPENDENT read-only verification of OPTION-EVIDENCE-V2 claims.

Does NOT trust executive_summary.json / focus report. Re-derives every unit by
re-using the same production modules, then audits the *classifier branches*:

  Q1 Are there exactly 3 B samples, and which branch produced each?
  Q2 Does the broad `trailing` branch create B by importing the NEXT question's
     content across a composite/question boundary? (false-positive audit)
  Q3 Is D=29 reproducible and restricted to per-sub option composites?
  Q4 Independent C audit: units where the SOURCE has fewer option labels than
     declared/resolved -> label-shortfall census (is C=1 an undercount?)
  Q5 English Q5-6: what do declared_labels / question boundaries / leaves say?

Writes nothing except its own report JSON. No production code touched.
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter, defaultdict
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
DIGIT_GLUE = re.compile(r"(?<![A-Za-z0-9_])(\d)([A-Ha-h])\s*[.．、:：,，。)）]")
CHAR_GLUE = re.compile(r"(?<![A-Za-z0-9_\s.．、:：,，。)）])([^\sA-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]")
SPACE_SEP = re.compile(r"(?:^|(?<=[。；;：:\n]))([A-Ha-h])[  　]{1,3}(?=[一-鿿])", re.M)
HTMLISH = re.compile(r"<(table|div|img|tr|td|span|p)\b", re.I)
STEMISH = re.compile(
    r"^(听第|第\s*\d+\s*[题段]|#{1,6}\s|\d+\s*[.．、\\]|【|一、|二、|三、|四、|五、|六、|参考答案|---)"
)
# any line that starts a new numbered question (strong question-boundary signal)
QSTART = re.compile(r"^\s*(\d{1,3})\s*[.．、]")


def is_option_like_content(t: str) -> bool:
    s = t.strip()
    if not s or len(s) < 4:
        return False
    if HTMLISH.search(s) or STEMISH.search(s):
        return False
    if s.startswith("#") or s.startswith("---"):
        return False
    if re.fullmatch(r"[A-Da-d１-４1-4①-④]+", s):
        return False
    return True


def answer_letter(text: str):
    if not text:
        return None
    c = _clean_answer(text)
    if re.fullmatch(r"[A-Za-z]", c):
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
    clean, damaged, option_like = {}, [], []
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
                    "line": i, "kind": kind, "token": m.group(0),
                    "label": m.group(lab_g).upper(), "preview": t.strip()[:120],
                })
        if is_option_like_content(t):
            option_like.append({"line": i, "preview": t.strip()[:120]})
    return clean, damaged, option_like


def count_option_blocks(texts, lo, hi) -> int:
    if not lo or not hi:
        return 0
    blocks, seen = 0, set()
    for i in range(max(1, lo), min(len(texts), hi) + 1):
        t = texts[i - 1]
        labs = set(m.group(1).upper() for m in CLEAN_LABEL.finditer(t))
        labs |= set(m.group(2).upper() for m in DIGIT_GLUE.finditer(t))
        labs |= set(m.group(1).upper() for m in SPACE_SEP.finditer(t))
        if labs and "A" in labs and i not in seen:
            blocks += 1
            seen.add(i)
    return blocks


def classify_traced(**kw):
    """Same decision order as survey v2.2, but returns the BRANCH NAME."""
    src_clean = kw["src_clean"]
    src_damaged = kw["src_damaged"]
    src_option_like = kw["src_option_like"]
    declared = [str(x).upper() for x in kw["declared"]]
    resolved = [str(x).upper() for x in kw["resolved"]]
    ans_letter = kw["ans_letter"]
    ans_text = kw["ans_text"]
    expected = kw["expected"]
    n_leaves = kw["n_leaves"]
    sub_qns = kw["sub_qns"]
    option_blocks = kw["option_blocks"]
    o_boundary = kw["o_boundary"]
    q_boundary = kw["q_boundary"]

    src_clean_u = {k.upper(): v for k, v in src_clean.items()}
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
    trailing = [u for u in src_option_like if u["line"] > last_lab_line and u["line"] <= (scan_hi or 10**9)]

    n_declared = len(declared)
    n_clean = len(src_clean_u)
    per_sub = kw["is_comp"] and option_blocks >= 2 and len(sub_qns) >= 2
    d_gap = per_sub and n_leaves < len(sub_qns)

    ir_absent = (not declared) and (not resolved) and (not src_clean_u) and (not src_damaged)

    branch = primary = None
    if ir_absent and not src_option_like:
        primary, branch = "F0", "F0_ir_absent"
    elif ir_absent and src_option_like:
        primary, branch = "F0", "F0_ir_absent_raw"
    elif b_damaged_undeclared:
        primary, branch = "B", "B_damaged_undeclared_label"
    elif trailing and (expected or 4) > n_declared:
        primary, branch = "B", "B_trailing_option_like_content"
    elif b_clean_undeclared:
        primary, branch = "B", "B_clean_undeclared_label"
    else:
        if ans_letter and ans_letter not in declared and ans_letter not in src_clean_u:
            if any(d["label"] == ans_letter for d in src_damaged):
                primary, branch = "B", "B_damaged_label_for_answer_slot"
            elif trailing:
                primary, branch = "B", "B_trailing_for_answer_slot"
            else:
                primary, branch = "C", "C_no_source_for_answer_slot"
        elif expected and max(n_declared, n_clean) < expected and not trailing and not src_damaged:
            primary, branch = "C", "C_expected_shortfall"
        elif d_gap:
            primary, branch = "D", "D_decomposition_gap"
        else:
            if ans_letter is None:
                primary, branch = "F", "F_answer_not_canonical"
            else:
                primary, branch = "A", "A_structural_ok"

    return {
        "primary": primary, "branch": branch, "d_gap": d_gap, "trailing": trailing,
        "b_damaged_undeclared": b_damaged_undeclared,
        "b_clean_undeclared": b_clean_undeclared,
        "last_lab_line": last_lab_line, "scan_hi": scan_hi,
        "n_declared": n_declared, "n_clean": n_clean,
    }


def main() -> None:
    rows = []
    unit_dump = {}

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

        # ---- map every numbered-question start line in this paper (boundary truth)
        qstarts = []
        for idx, t in enumerate(texts, start=1):
            mm = QSTART.match(t)
            if mm:
                qstarts.append((idx, mm.group(1)))

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

                tr = classify_traced(
                    paper=paper, root_id=root.unit_id, leaf_id=leaf.unit_id, is_comp=is_comp,
                    expected=expected, src_clean=src_clean, src_damaged=src_damaged,
                    src_option_like=src_option_like, declared=declared, resolved=list(labels),
                    ans_letter=letter, ans_text=ans_text, n_leaves=len(leaves),
                    sub_qns=sub_qns, option_blocks=option_blocks,
                    o_boundary=[o_lo, o_hi], q_boundary=[q_lo, q_hi],
                )

                # ---- INDEPENDENT: source label set actually inside the unit's own span
                span_lo = scan_lo or 1
                span_hi = scan_hi or 1
                in_span = [t for t in texts[span_lo - 1:span_hi]]
                src_lab_in_span = set()
                for t in in_span:
                    src_lab_in_span |= {mm.group(1).upper() for mm in CLEAN_LABEL.finditer(t)}
                    src_lab_in_span |= {mm.group(2).upper() for mm in DIGIT_GLUE.finditer(t)}
                    src_lab_in_span |= {mm.group(1).upper() for mm in SPACE_SEP.finditer(t)}

                # first numbered-question start strictly after the unit's question lo
                next_qs = [(ln, num) for ln, num in qstarts if q_lo and ln > q_lo]

                rows.append({
                    "paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                    "qn": leaf.question_number, "qtype": leaf.original_question_type,
                    "canonical": canonical,
                    "primary": tr["primary"], "branch": tr["branch"],
                    "is_composite": is_comp, "option_blocks": option_blocks,
                    "n_leaves": len(leaves), "sub_qns": sub_qns, "d_gap": tr["d_gap"],
                    "expected": expected,
                    "declared": declared, "resolved": list(labels), "answer_letter": letter,
                    "answer_preview": (ans_text or "")[:100],
                    "q_boundary": [q_lo, q_hi], "options_lines": [o_lo, o_hi],
                    "scan_span": [span_lo, span_hi],
                    "src_labels_in_span": sorted(src_lab_in_span),
                    "src_labels_outside_declared": sorted(src_lab_in_span - set(declared)),
                    "last_lab_line": tr["last_lab_line"],
                    "trailing": tr["trailing"],
                    "b_damaged_undeclared": tr["b_damaged_undeclared"],
                    "b_clean_undeclared": tr["b_clean_undeclared"],
                    "next_question_start": next_qs[0] if next_qs else None,
                })

                if (paper, root.unit_id) in (("英语", "Q5-6"), ("数学", "Q4"), ("化学", "Q23"), ("历史", "Q29")):
                    unit_dump.setdefault(f"{paper}/{root.unit_id}", []).append({
                        "leaf": leaf.unit_id, "qn": leaf.question_number, "qtype": leaf.original_question_type,
                        "declared": declared, "resolved": list(labels), "answer": letter,
                        "q_boundary": [q_lo, q_hi], "options_lines": [o_lo, o_hi],
                        "sub_qns": sub_qns, "n_leaves": len(leaves), "option_blocks": option_blocks,
                        "branch": tr["branch"], "primary": tr["primary"],
                        "src_labels_in_span": sorted(src_lab_in_span),
                        "trailing": tr["trailing"],
                        "source_lines": [
                            {"line": i, "text": texts[i - 1][:100]}
                            for i in range(max(1, span_lo), min(len(texts), span_hi) + 1)
                        ][:40],
                    })

    tot = Counter(r["primary"] for r in rows)
    branches = Counter(r["branch"] for r in rows)
    b_rows = [r for r in rows if r["primary"] == "B"]

    # Q2: does any B_trailing instance cross into a later numbered question?
    b_trailing_cross = []
    for r in b_rows:
        if r["branch"] != "B_trailing_option_like_content":
            continue
        tr_lines = [u["line"] for u in r["trailing"]]
        if not tr_lines:
            continue
        first = tr_lines[0]
        if r["q_boundary"][1] and first > r["q_boundary"][1]:
            b_trailing_cross.append({**{k: r[k] for k in ("paper", "root", "leaf", "qn", "declared")},
                                     "first_trailing_line": first, "q_boundary": r["q_boundary"],
                                     "verdict": "trailing content lies AFTER declared question boundary"})
        else:
            # does the line itself start a new numbered question?
            if any(QSTART.match(x) for x in []):
                pass

    # Q4: independent shortfall census - source has fewer option labels than declared
    shortfall = []
    for r in rows:
        decl = set(r["declared"])
        src = set(r["src_labels_in_span"])
        missing = sorted(decl - src)
        if missing:
            shortfall.append({
                "paper": r["paper"], "root": r["root"], "leaf": r["leaf"], "qn": r["qn"],
                "primary": r["primary"], "branch": r["branch"],
                "declared": r["declared"], "src_labels_in_span": sorted(src),
                "declared_but_not_in_source": missing,
                "answer": r["answer_letter"], "span": r["scan_span"],
            })

    # Q: source labels present but NOT declared, yet unit still classed A (missed B?)
    missed = [r for r in rows if r["primary"] == "A" and r["src_labels_outside_declared"]]

    d_rows = [r for r in rows if r["primary"] == "D"]
    d_by_paper = Counter(r["paper"] for r in d_rows)
    d_comp = [r for r in d_rows if not r["is_composite"]]
    d_no_blocks = [r for r in d_rows if r["option_blocks"] < 2]

    report = {
        "totals_primary": dict(tot),
        "totals_rows": len(rows),
        "branches": dict(branches),
        "Q1_b_count": len(b_rows),
        "Q1_b_breakdown": [
            {"paper": r["paper"], "root": r["root"], "qn": r["qn"], "branch": r["branch"],
             "declared": r["declared"], "src_labels_in_span": r["src_labels_in_span"],
             "answer": r["answer_letter"], "expected": r["expected"],
             "b_damaged_undeclared": r["b_damaged_undeclared"]}
            for r in b_rows
        ],
        "Q2_b_trailing_crossing_question_boundary": b_trailing_cross,
        "Q3_d_count": len(d_rows),
        "Q3_d_by_paper": dict(d_by_paper),
        "Q3_d_but_not_composite": len(d_comp),
        "Q3_d_but_option_blocks_lt2": len(d_no_blocks),
        "Q3_d_sample": [
            {"paper": r["paper"], "root": r["root"], "qn": r["qn"], "sub_qns": r["sub_qns"],
             "n_leaves": r["n_leaves"], "option_blocks": r["option_blocks"]}
            for r in d_rows[:12]
        ],
        "Q4_shortfall_count": len(shortfall),
        "Q4_shortfall_by_primary": dict(Counter(s["primary"] for s in shortfall)),
        "Q4_shortfall_rows": shortfall[:40],
        "Q5_missed_source_labels_but_classed_A": [r["root"] for r in missed],
        "Q5_missed_detail": [
            {"paper": r["paper"], "root": r["root"], "qn": r["qn"],
             "declared": r["declared"], "src_only": r["src_labels_outside_declared"]}
            for r in missed[:20]
        ],
        "focus_units": unit_dump,
    }

    OUT.joinpath("_indep_verify_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=" * 78)
    print("INDEPENDENT RECOUNT (survey v2.2 logic, branch-instrumented)")
    print("=" * 78)
    print("rows:", len(rows), "totals:", dict(tot))
    print("\nbranch histogram:")
    for k, v in sorted(branches.items(), key=lambda x: -x[1]):
        print(f"   {k:<40}{v}")
    print(f"\nQ1 B samples = {len(b_rows)}")
    for b in report["Q1_b_breakdown"]:
        print(f"   {b['paper']}/{b['root']} qn={b['qn']} branch={b['branch']} declared={b['declared']}")
    print(f"\nQ2 B_trailing crossing declared question boundary: {len(b_trailing_cross)}")
    for c in b_trailing_cross:
        print(f"   {c['paper']}/{c['root']} first_trailing={c['first_trailing_line']} q_boundary={c['q_boundary']}")
    print(f"\nQ3 D={len(d_rows)}  by_paper={dict(d_by_paper)}")
    print(f"   D but not composite = {len(d_comp)}; D but option_blocks<2 = {len(d_no_blocks)}")
    print(f"\nQ4 declared-but-absent-from-source labels: {len(shortfall)} rows "
          f"{dict(Counter(s['primary'] for s in shortfall))}")
    for s in shortfall[:25]:
        print(f"   {s['paper']}/{s['root']} qn={s['qn']} primary={s['primary']} "
              f"missing={s['declared_but_not_in_source']} ans={s['answer']} span={s['span']}")
    print(f"\nQ5 units classed A despite source labels not declared: {len(missed)}")
    for r in missed[:15]:
        print(f"   {r['paper']}/{r['root']} qn={r['qn']} declared={r['declared']} src_only={r['src_labels_outside_declared']}")
    print(f"\nwrote {OUT / '_indep_verify_report.json'}")


if __name__ == "__main__":
    main()
