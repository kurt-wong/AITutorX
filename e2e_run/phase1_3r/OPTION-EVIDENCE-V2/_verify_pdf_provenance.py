"""READ-ONLY: locate the PDF sha mismatch found by _verify_acceptance_artifacts.py.

Two 01_INPUT_PDF files were not matched inside MANIFEST:
    2018北京夏季高中会考物理（教师版）.pdf   sha cc30e212...
    2018北京春季高中会考语文（教师版）.pdf   (needs re-check, output was truncated)

Determine, per subject, whether MANIFEST's declared sha equals the file actually
placed in 01_INPUT_PDF, and whether that file is the one recorded in the OCR
ledger (i.e. the artifact that produced the .md being accepted).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
LEDGER = Path(r"D:\Project\Papers\data\ocr_output_manifest.jsonl")
PDF_ROOT = Path(r"D:\Project\Papers\maintainess\PDF")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> None:
    man = json.loads((EA / "MANIFEST.json").read_text(encoding="utf-8"))
    subs = man["subjects"]

    ledger_by_sha = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        ledger_by_sha[d.get("source_sha256")] = d

    print("=" * 100)
    print("PER-SUBJECT PDF PROVENANCE: MANIFEST declared vs file in 01_INPUT_PDF vs OCR ledger")
    print("=" * 100)
    for name, e in subs.items():
        pdf_meta = e.get("pdf") or {}
        declared = pdf_meta.get("sha256")
        fname = pdf_meta.get("name")
        placed = EA / "01_INPUT_PDF" / str(fname) if fname else None
        actual = sha(placed) if placed and placed.exists() else None
        led = ledger_by_sha.get(declared or "")
        print(f"\n{name}")
        print(f"   declared name : {fname}")
        print(f"   declared sha  : {declared}")
        print(f"   placed exists : {bool(placed and placed.exists())}")
        print(f"   placed sha    : {actual}")
        print(f"   MATCH         : {declared == actual}")
        if led:
            print(f"   ledger source : {led.get('source_rel')}")
            print(f"   ledger output : {led.get('output_rel')}")
            print(f"   ledger pages  : {led.get('pages')}")
        else:
            print(f"   ledger        : *** declared sha NOT in OCR ledger ***")
        if declared != actual and placed and placed.exists():
            # is the PLACED file in the ledger under a different entry?
            alt = ledger_by_sha.get(actual)
            print(f"   placed sha in ledger? {'YES: ' + str(alt.get('output_rel')) if alt else 'NO'}")

    # extra files in 01_INPUT_PDF not referenced by MANIFEST
    declared_names = {(e.get("pdf") or {}).get("name") for e in subs.values()}
    print("\n" + "=" * 100)
    print("FILES IN 01_INPUT_PDF NOT REFERENCED BY MANIFEST")
    print("=" * 100)
    for f in sorted((EA / "01_INPUT_PDF").glob("*.pdf")):
        if f.name not in declared_names:
            print(f"   EXTRA: {f.name}  sha={sha(f)[:16]}  bytes={f.stat().st_size}")


if __name__ == "__main__":
    main()
