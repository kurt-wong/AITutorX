"""READ-ONLY: integration-输入传递 check WITHOUT the official artifact.

The manifest declares `source_content_sha256` — the hash of the preprocessing
source text at annotation time. V3's `manifest_reader` preserves it verbatim
but does NOT verify it. So:

    declared_hash == sha256(source_file on disk)
        => the .md V3 consumes is byte-identical to the text the Producer annotated
           (input transfer did NOT deform the text)
    declared_hash != sha256(source_file on disk)
        => the consumed text CHANGED after annotation -> input transfer is suspect,
           and every downstream conclusion about this paper is unsound.

This is the strongest input-integrity statement obtainable on-disk.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")
FOCUS = ("2018北京春季高中会考数学（教师版）(1).md",
         "2018北京春季高中会考化学（教师版）(1).md",
         "2018北京夏季高中会考历史（教师版）(1).md",
         "2018北京春季高中会考英语（教师版）(1).md")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    rows, match, mismatch, nohash, nosrc = [], 0, 0, 0, 0
    for mf in sorted(ROOT.rglob("*.manifest.json")):
        try:
            d = json.loads(mf.read_text(encoding="utf-8"))
        except Exception as e:
            print("!! unreadable", mf, e)
            continue
        decl = d.get("source_content_sha256")
        sf = Path(d.get("source_file", ""))
        if not sf.exists():
            nosrc += 1
            rows.append({"manifest": str(mf), "verdict": "SOURCE_MISSING",
                         "declared": decl, "source_file": str(sf)})
            continue
        actual = sha256_file(sf)
        if not decl:
            nohash += 1
            verdict = "NO_DECLARED_HASH"
        elif decl == actual:
            match += 1
            verdict = "MATCH"
        else:
            mismatch += 1
            verdict = "MISMATCH"
        rows.append({"manifest": str(mf), "verdict": verdict,
                     "declared": decl, "actual": actual, "source_file": str(sf),
                     "paper": mf.parent.name})

    print("=" * 96)
    print("INPUT-TRANSFER INTEGRITY: manifest-declared source hash vs .md on disk")
    print("=" * 96)
    print(f"manifests scanned     : {len(rows)}")
    print(f"  MATCH               : {match}")
    print(f"  MISMATCH            : {mismatch}")
    print(f"  NO_DECLARED_HASH    : {nohash}")
    print(f"  SOURCE_MISSING      : {nosrc}")

    print("\n--- focus papers ---")
    for r in rows:
        if Path(r["source_file"]).name in FOCUS:
            print(f"   {r['verdict']:<18} {Path(r['source_file']).name}")
            print(f"       declared={r.get('declared')}")
            print(f"       actual  ={r.get('actual')}")

    if mismatch:
        print("\n--- MISMATCH detail (input text changed after annotation) ---")
        for r in rows:
            if r["verdict"] == "MISMATCH":
                print(f"   {r['source_file']}")

    print("\n--- verdict distribution by variant ---")
    def variant(p: str) -> str:
        try:
            return Path(p).relative_to(ROOT).parts[0]
        except Exception:
            return "?"
    c = Counter((variant(r["manifest"]), r["verdict"]) for r in rows)
    for k, v in sorted(((str(k), v) for k, v in c.items())):
        print(f"   {k:<52}{v}")

    OUT.joinpath("_p14b_input_integrity.json").write_text(
        json.dumps({"summary": {"match": match, "mismatch": mismatch,
                                "no_declared_hash": nohash, "source_missing": nosrc},
                    "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_input_integrity.json'}")


if __name__ == "__main__":
    main()
