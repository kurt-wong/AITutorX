"""READ-ONLY prototype: Gate-1 automatic PDF <-> MD differ.

Owner's Gate 1 design requires: no manual page-flipping. Instead
    PDF text layer  --diff-->  preprocessing MD  -->  only differences shown
This prototype proves the mechanism works and measures the review burden.

Method (deliberately simple / deterministic, no LLM):
  * extract PDF text layer per page (PyMuPDF)
  * normalise both sides: strip whitespace, drop OCR-only decoration,
    keep CJK + latin alnum + option letters
  * slide the normalised MD over the normalised PDF text; every MD segment
    that cannot be located in the PDF is reported as a DIFFERENCE with context
  * classify each difference by shape (dropped label / dropped char / extra token)

The three focus papers contain KNOWN defects. If this prototype surfaces them
automatically, Gate 1 is feasible. If it cannot, Gate 1 needs a different design.
"""
from __future__ import annotations

import json
import re
import sys
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

KEEP = re.compile(r"[0-9A-Za-z\u4e00-\u9fff]")


def norm(s: str) -> str:
    """Keep only CJK + alnum. Removes spaces/punct/LaTeX noise for matching."""
    return "".join(KEEP.findall(s))


def pdf_text(name: str) -> str:
    import fitz
    doc = fitz.open(PDF_ROOT / f"{name}.pdf")
    t = "\n".join(p.get_text("text") for p in doc)
    doc.close()
    return t


def md_lines(path: Path):
    return path.read_text(encoding="utf-8").splitlines()


def main() -> None:
    report = {}
    for subject, name, rel in CASES:
        md_path = MD_ROOT / rel
        if not md_path.exists():
            print(f"!! missing {md_path}")
            continue
        core = norm(pdf_text(name))
        lines = md_lines(md_path)

        print("=" * 100)
        print(f"{subject}  {name}")
        print("=" * 100)
        print(f"   PDF normalised chars : {len(core)}")
        print(f"   MD lines             : {len(lines)}")

        # find MD lines (normalised) that do NOT appear in the PDF text
        findings = []
        for i, raw in enumerate(lines, start=1):
            n = norm(raw)
            if len(n) < 6:
                continue                      # too short to be meaningful
            if n in core:
                continue
            # try a shorter probe: first 12 normalised chars
            probe = n[:12]
            status = "ABSENT" if probe not in core else "PARTIAL"
            findings.append({"line": i, "status": status,
                             "raw": raw.strip()[:110], "norm": n[:60]})

        print(f"   MD lines not found verbatim in PDF text: {len(findings)}")
        for f in findings[:22]:
            print(f"      L{f['line']:<5} [{f['status']:<7}] {f['raw']}")
        report[subject] = {"findings": findings, "md_lines": len(lines)}

    OUT.joinpath("_gate1_diff_prototype.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_gate1_diff_prototype.json'}")

    # ---- targeted check: do the KNOWN defects get flagged? ----
    print("\n" + "=" * 100)
    print("TARGETED: are the known defects surfaced automatically?")
    print("=" * 100)
    checks = [
        ("化学", "Q23 丢 D 标签", "mathrm{H}^{+} + \\mathrm{SO}_{4}^{2-}"),
        ("化学", "Q20 跨行续文", "还原反应"),
        ("数学", "Q4 的 2D.", "2D."),
        ("历史", "Q29 D 麦哲伦", "D 麦哲伦"),
    ]
    for subj, label, needle in checks:
        hits = [f for f in report.get(subj, {}).get("findings", [])
                if needle[:20] in f["raw"] or needle in f["raw"]]
        print(f"   {subj} / {label}: flagged={bool(hits)}  {[h['line'] for h in hits]}")


if __name__ == "__main__":
    main()
