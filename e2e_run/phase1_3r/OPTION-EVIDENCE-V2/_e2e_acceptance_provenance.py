"""READ-ONLY: E2E acceptance-corpus provenance check.

Owner's requirement: an acceptance corpus must carry source PDF sha256, output
sha256, and be reproducible. The OCR ledger (data/ocr_output_manifest.jsonl)
already records source_rel / source_size / source_sha256 / output_rel / pages.

This independently verifies, for the candidate 9-subject corpus:
  1. source PDF exists at maintainess/PDF/<source_rel> AND its sha256 matches the ledger
  2. output .md exists at Ocr-markdown/<output_rel> and record its sha256
  3. whether that .md is line-numbered (i.e. already reslice-shaped)
     -> decides whether it can serve as the L0 "preprocessing output" artifact
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PAPERS = Path(r"D:\Project\Papers")
LEDGER = PAPERS / "data" / "ocr_output_manifest.jsonl"
PDF_ROOT = PAPERS / "maintainess" / "PDF"
OUT_ROOT = PAPERS / "Ocr-markdown"
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

CANDIDATES = [
    "2018北京春季高中会考语文（教师版）(1)",
    "2018北京春季高中会考数学（教师版）(1)",
    "2018北京春季高中会考英语（教师版）(1)",
    "2018北京春季高中会考物理（教师版）(1)",
    "2018北京春季高中会考化学（教师版）(1)",
    "2018北京春季高中会考生物（教师版）(1)",
    "2018北京春季高中会考政治（教师版）(1)",
    "2018北京春季高中会考历史（教师版）(1)",
    "2018北京春季高中会考地理（教师版）(1)",
]
LN = re.compile(r"^\[L\d+\]")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    entries = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        key = Path(str(d.get("output_rel", ""))).stem
        entries[key] = d

    print("=" * 100)
    print("E2E ACCEPTANCE CORPUS — PROVENANCE CHECK (9 subjects)")
    print("=" * 100)
    print(f"ledger entries: {len(entries)}   candidates: {len(CANDIDATES)}\n")

    rows = []
    for name in CANDIDATES:
        e = entries.get(name)
        rec = {"paper": name}
        if not e:
            rec["verdict"] = "NOT_IN_LEDGER"
            print(f"{name}\n   !! not found in OCR ledger")
            rows.append(rec)
            continue
        src = PDF_ROOT / str(e["source_rel"])
        dst = OUT_ROOT / str(e["output_rel"])
        rec["source_rel"] = str(e["source_rel"])
        rec["output_rel"] = str(e["output_rel"])
        rec["pages"] = e.get("pages")
        rec["written_at"] = e.get("written_at")
        rec["source_sha_ledger"] = e["source_sha256"]
        rec["source_size_ledger"] = e["source_size"]
        rec["source_exists"] = src.exists()
        rec["output_exists"] = dst.exists()
        if src.exists():
            actual = sha256_file(src)
            rec["source_sha_actual"] = actual
            rec["source_sha_match"] = (actual == e["source_sha256"])
            rec["source_size_actual"] = src.stat().st_size
        if dst.exists():
            txt = dst.read_text(encoding="utf-8")
            lines = txt.splitlines()
            rec["output_sha"] = hashlib.sha256(dst.read_bytes()).hexdigest()
            rec["output_lines"] = len(lines)
            rec["line_numbered"] = bool(LN.match(lines[0])) if lines else None
            rec["first_line"] = lines[0][:70] if lines else ""

        print(f"{name}")
        print(f"   source PDF   : {rec['source_rel']}")
        print(f"      exists={rec.get('source_exists')}  "
              f"ledger_sha={str(rec.get('source_sha_ledger'))[:16]}  "
              f"actual_sha={str(rec.get('source_sha_actual'))[:16]}  "
              f"MATCH={rec.get('source_sha_match')}")
        print(f"      size ledger={rec.get('source_size_ledger')} actual={rec.get('source_size_actual')}")
        print(f"   output .md   : {rec['output_rel']}")
        print(f"      exists={rec.get('output_exists')} pages={rec.get('pages')} "
              f"written_at={rec.get('written_at')}")
        print(f"      lines={rec.get('output_lines')} line_numbered={rec.get('line_numbered')}")
        print(f"      sha={str(rec.get('output_sha'))[:16]}")
        rows.append(rec)

    ok = sum(1 for r in rows if r.get("source_sha_match") and r.get("output_exists"))
    print("\n" + "=" * 100)
    print(f"VERIFIED (source-pdf sha matches ledger AND output exists): {ok} / {len(CANDIDATES)}")
    print(f"output .md line-numbered: "
          f"{sum(1 for r in rows if r.get('line_numbered'))} / {len(CANDIDATES)}")

    OUT.joinpath("_e2e_acceptance_provenance.json").write_text(
        json.dumps({"candidates": rows, "verified": ok}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"wrote {OUT / '_e2e_acceptance_provenance.json'}")


if __name__ == "__main__":
    main()
