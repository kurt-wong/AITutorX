"""READ-ONLY: Gate-1 feasibility — full-text diff vs MARKER diff.

Result of _gate1_diff_prototype.py (full-text line diff):
    153/749 math lines "different" yet 0 real defects found.
    Root cause: PDF extraction REFLOWS text, MD keeps fine line structure and
    adds LaTeX/HTML decoration -> line-level comparison is noise-dominated and
    structurally CANNOT see "option split / label dropped".

This script tests the alternative: compare only STRUCTURAL MARKERS.
    - question numbers  (^NN. / ^NN．)
    - option labels     (A-D at a position that looks like an option slot)
Marker-diff is output-preserving: PDF has the same printed labels as the page,
MD is what the pipeline will consume. A dropped/duplicated label is exactly the
class of defect Gate 1 must catch.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PDF_ROOT = Path(r"D:\Project\Papers\maintainess\PDF")
MD_ROOT = Path(r"D:\Project\Papers\Ocr-markdown")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

CASES = [
    ("化学", "2018北京春季高中会考化学（教师版）(1)",
     "会考/化学/2018北京春季高中会考化学（教师版）(1).md"),
    ("数学", "2018北京春季高中会考数学（教师版）(1)",
     "会考/数学/2018北京春季高中会考数学（教师版）(1).md"),
    ("历史", "2018北京夏季高中会考历史（教师版）(1)",
     "会考/历史/2018北京夏季高中会考历史（教师版）(1).md"),
]

# question number marker: 23.  23． (not inside a word)
QNUM = re.compile(r"(?<![0-9A-Za-z])[0-9]{1,3}\s*[.．]")
# option label marker: A. A． A、 A) —— single letter immediately followed by sep
OPT = re.compile(r"(?<![0-9A-Za-z])([A-Ha-h])\s*[.．、)）]")


def marker_counts(text: str):
    """Return (question-number marker count, option-label multiset)."""
    qn = len(QNUM.findall(text))
    opts = Counter(m.group(1).upper() for m in OPT.finditer(text))
    return qn, opts


def pdf_text(name: str) -> str:
    import fitz
    doc = fitz.open(PDF_ROOT / f"{name}.pdf")
    t = "\n".join(p.get_text("text") for p in doc)
    doc.close()
    return t


def main() -> None:
    report = {}
    for subject, name, rel in CASES:
        md_path = MD_ROOT / rel
        pt = pdf_text(name)
        mt = md_path.read_text(encoding="utf-8")
        pq, po = marker_counts(pt)
        mq, mo = marker_counts(mt)

        print("=" * 96)
        print(f"{subject}   {name}")
        print("=" * 96)
        print(f"   question-number markers : PDF={pq:<5} MD={mq:<5} delta={mq - pq}")
        all_labels = sorted(set(po) | set(mo))
        print(f"   option-label markers (A-H):")
        for lab in all_labels:
            p, m = po.get(lab, 0), mo.get(lab, 0)
            flag = "" if p == m else f"   <<< DELTA {m - p:+d}"
            print(f"      {lab}: PDF={p:<5} MD={m:<5}{flag}")
        report[subject] = {"pdf_qnum": pq, "md_qnum": mq,
                           "pdf_opts": dict(po), "md_opts": dict(mo)}

    print("\n" + "=" * 96)
    print("Full-text diff (previous prototype) vs marker diff — noise comparison")
    print("=" * 96)
    print("   full-text line diff  : math 153/749 lines flagged, 0 real defects -> USELESS")
    print("   marker diff          : see per-subject deltas above (bounded, reviewable)")

    OUT.joinpath("_gate1_marker_diff.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_gate1_marker_diff.json'}")


if __name__ == "__main__":
    main()
