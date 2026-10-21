"""READ-ONLY: is 04_V3_INPUT/<subj>.manifest.json actually pointed at
02_PREPROCESSING_OUTPUT (the frozen, owner-accepted MD)?

The replay mismatch (frozen gate=auto_approve vs replay=rejected) has three
possible causes:
  (a) my replay used the wrong MD  -> check manifest.source_file + declared sha
  (b) the manifest and the frozen MD are inconsistent (acceptance package defect)
  (c) a genuine pipeline discrepancy

The manifest declares `source_content_sha256` of ITS source text. Compare that
against the sha256 of the MD I am feeding, and against 02/03 files.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    print("=" * 100)
    print("04_V3_INPUT manifest.source_file  vs  02_PREPROCESSING_OUTPUT / 03_OWNER_ACCEPTED")
    print("=" * 100)
    for man_p in sorted((EA / "04_V3_INPUT").glob("*.manifest.json")):
        subj = man_p.stem
        d = json.loads(man_p.read_text(encoding="utf-8"))
        decl_sha = d.get("source_content_sha256")
        src = Path(str(d.get("source_file", "")))
        cands = [p for p in (EA / "02_PREPROCESSING_OUTPUT").glob("*.md") if subj in p.name]
        acc = [p for p in (EA / "03_OWNER_ACCEPTED").glob("*.md") if subj in p.name]
        print(f"\n{subj}")
        print(f"   manifest source_file    : {src}")
        print(f"   manifest source exists  : {src.exists()}")
        print(f"   manifest declared sha   : {str(decl_sha)[:20]}")
        if src.exists():
            print(f"   actual sha of that file : {sha(src)[:20]}"
                  f"   MATCH={sha(src) == decl_sha}")
            try:
                print(f"   its first line          : {src.read_text(encoding='utf-8').splitlines()[0][:60]!r}")
            except Exception as e:
                print(f"   (unreadable: {e})")
        for label, group in (("02_PREPROCESSING_OUTPUT", cands), ("03_OWNER_ACCEPTED", acc)):
            for p in group:
                h = sha(p)
                print(f"   {label:<23}: {p.name[:52]:<54} sha={h[:20]}"
                      f"  ==declared:{h == decl_sha}")
        # line-count cross-check for the physics case that showed gate mismatch
        if src.exists() and cands:
            a = len(src.read_text(encoding="utf-8").splitlines())
            b = len(cands[0].read_text(encoding="utf-8").splitlines())
            print(f"   line counts: manifest-source={a}  02-md={b}  same={a == b}")


if __name__ == "__main__":
    main()
