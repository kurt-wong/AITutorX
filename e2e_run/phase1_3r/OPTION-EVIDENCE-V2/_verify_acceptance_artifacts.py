"""READ-ONLY: verify MIMO's E2E_ACCEPTANCE frozen artifacts against declared hashes.

Checks:
  A. MANIFEST.json declared pdf/md sha256  vs  files in 01_INPUT_PDF / 02_... / 03_...
  B. 02_PREPROCESSING_OUTPUT sha  vs  the official Papers Ocr-markdown sha
  C. is 03_OWNER_ACCEPTED really identical to 02 (the freeze requirement)
  D. does data.js (what the page loads) carry 'questions'?
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
PAPERS_MD = Path(r"D:\Project\Papers\Ocr-markdown\会考")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def by_subject_manifest():
    """subject -> paper_label (from MANIFEST.json)."""
    d = json.loads((EA / "MANIFEST.json").read_text(encoding="utf-8"))
    return d


def main() -> None:
    man = json.loads((EA / "MANIFEST.json").read_text(encoding="utf-8"))
    print("MANIFEST keys:", list(man.keys())[:14])
    corpus = man.get("corpus") or man.get("subjects") or []
    print(f"corpus entries: {len(corpus) if isinstance(corpus, list) else 'dict'}\n")

    datajs = (EA / "data.js").read_text(encoding="utf-8")
    print("D. does data.js carry question content?")
    print(f"   'questions' present : {'\"questions\"' in datajs}")
    print(f"   '无题目预览' used by app.js: {('无题目预览' in (EA / 'app.js').read_text(encoding='utf-8'))}")
    vd = json.loads((EA / "viewer_data.json").read_text(encoding="utf-8"))
    nq = sum(len(e.get("questions") or []) for e in vd["subjects"].values())
    print(f"   viewer_data.json questions: {nq}   <-- data exists but page loads data.js")
    print()

    # B/C: compare the three .md stages per paper
    print("B/C. preprocessing vs owner-accepted vs papers-official (sha256)")
    for f in sorted((EA / "02_PREPROCESSING_OUTPUT").glob("*.md")):
        name = f.name
        acc = EA / "03_OWNER_ACCEPTED" / name
        # find matching papers official file
        cands = list(PAPERS_MD.rglob(name))
        s2 = sha(f)
        s3 = sha(acc) if acc.exists() else None
        sp = sha(cands[0]) if cands else None
        print(f"   {name[:44]:<46}")
        print(f"      02 = {s2[:16]}   03 = {str(s3)[:16] if s3 else 'MISSING'}"
              f"   identical_02_03 = {s2 == s3}")
        print(f"      papers official = {sp[:16] if sp else 'not found'}"
              f"   identical_to_papers = {s2 == sp}")

    # A: pdf hashes vs MANIFEST
    print("\nA. 01_INPUT_PDF sha vs MANIFEST declared")
    for f in sorted((EA / "01_INPUT_PDF").glob("*.pdf")):
        h = sha(f)
        found = None
        s = json.dumps(man, ensure_ascii=False)
        # look for this hash anywhere in MANIFEST
        if h in s:
            found = "FOUND in MANIFEST"
        print(f"   {f.name[:44]:<46} {h[:16]}  {found or 'NOT IN MANIFEST'}")


if __name__ == "__main__":
    main()
