"""READ-ONLY: read the ORIGINAL PDFs to establish ground truth.

This is the top of the chain and the only layer we have never inspected.
For the focus questions it answers: does the ORIGINAL PDF contain a D label /
a separate option, or is the anomaly present in print?

If the PDF is a scan (image-only), extraction returns little text: in that case
the honest verdict is "PDF text layer unavailable -> OCR is the only source ->
cannot attribute to preprocessing vs source".
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PDF_ROOT = Path(r"D:\Project\Papers\maintainess\PDF")

TARGETS = [
    ("数学", "2018北京春季高中会考数学（教师版）(1).pdf",
     [r"关于\s*直线\s*y\s*=\s*x", r"2D", r"关于\s*y\s*轴", r"cos\s*x"]),
    ("化学", "2018北京春季高中会考化学（教师版）(1).pdf",
     [r"离子方程式书写不正确", r"金属钠与水", r"BaSO", r"还原反应", r"涉及了?氧"]),
    ("历史", "2018北京夏季高中会考历史（教师版）(1).pdf",
     [r"麦哲伦", r"迪亚士", r"哥伦布", r"达.?伽马"]),
]
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

try:
    import fitz  # PyMuPDF
except Exception as e:  # pragma: no cover
    sys.exit(f"PyMuPDF unavailable: {e}")


def main() -> None:
    report = {}
    for subject, fname, pats in TARGETS:
        pdf = PDF_ROOT / fname
        print("=" * 100)
        print(f"{subject}  {fname}")
        print("=" * 100)
        if not pdf.exists():
            print("   !! PDF not found at", pdf)
            continue
        doc = fitz.open(pdf)
        print(f"   pages={doc.page_count}")
        total_chars = 0
        hits = []
        per_page = []
        for pno in range(doc.page_count):
            page = doc[pno]
            text = page.get_text("text") or ""
            total_chars += len(text.strip())
            per_page.append(len(text.strip()))
            for pat in pats:
                for m in re.finditer(pat, text):
                    s = max(0, m.start() - 60)
                    e = min(len(text), m.end() + 60)
                    hits.append({"page": pno + 1, "pattern": pat,
                                 "context": text[s:e].replace("\n", "\\n")})
        print(f"   extracted chars (text layer): {total_chars}")
        print(f"   chars per page: {per_page[:12]}")
        if total_chars < 200:
            print("   >>> NO USABLE TEXT LAYER (likely scanned images).")
            print("   >>> OCR output cannot be attributed to preprocessing vs source "
                  "from this PDF alone.")
        print(f"   pattern hits: {len(hits)}")
        for h in hits[:14]:
            print(f"      p{h['page']:<3} [{h['pattern']}] ...{h['context']}...")
        report[subject] = {"file": fname, "pages": doc.page_count,
                           "text_chars": total_chars, "hits": hits[:40]}
        doc.close()

    # also: is there a text layer at all on one known page of each?
    OUT.joinpath("_e2e_pdf_ground_truth.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_e2e_pdf_ground_truth.json'}")


if __name__ == "__main__":
    main()
