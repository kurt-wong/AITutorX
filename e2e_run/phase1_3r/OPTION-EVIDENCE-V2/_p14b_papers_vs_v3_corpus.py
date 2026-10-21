"""READ-ONLY: is V3's Phase-1 corpus a faithful copy of the Papers Producer output?

Papers producer output root : Papers/Ocr-markdown/reslice-batch-C/...
V3 Phase-1 consumed corpus  : AITutor-X/e2e_run/phase1_1_corpus_optspans/reslice-batch-C/...

For every file present in BOTH trees: compare sha256 byte-for-byte.
Establishes (or refutes) that the V3 .md/.manifest are the Producer's own output
rather than an independently assembled copy.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PAPERS = Path(r"D:\Project\Papers\Ocr-markdown\reslice-batch-C")
V3 = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")
FOCUS = ("2018北京春季高中会考数学（教师版）(1)",
         "2018北京春季高中会考化学（教师版）(1)",
         "2018北京夏季高中会考历史（教师版）(1)",
         "2018北京春季高中会考英语（教师版）(1)")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def index(root: Path, suffix: str) -> dict[str, Path]:
    """key = (relative dir, stem) so papers can be matched across trees."""
    out = {}
    for p in root.rglob(f"*{suffix}"):
        if p.suffix == ".bak" or p.name.endswith(".manifest.json.p14b.bak"):
            continue
        rel = p.relative_to(root)
        key = str(rel.parent / rel.name.replace(suffix, ""))
        out[key] = p
    return out


def main() -> None:
    for suffix in (".md", ".manifest.json"):
        a = index(PAPERS, suffix)
        b = index(V3, suffix)
        common = sorted(set(a) & set(b))
        only_a = sorted(set(a) - set(b))
        only_b = sorted(set(b) - set(a))
        same, diff = [], []
        for k in common:
            if sha(a[k]) == sha(b[k]):
                same.append(k)
            else:
                diff.append(k)
        print("=" * 96)
        print(f"SUFFIX {suffix}")
        print("=" * 96)
        print(f"   Papers only : {len(only_a)}")
        print(f"   V3 only     : {len(only_b)}")
        print(f"   common      : {len(common)}")
        print(f"   IDENTICAL   : {len(same)}")
        print(f"   DIFFERENT   : {len(diff)}")
        if only_a[:6]:
            print(f"   (papers-only sample) {only_a[:6]}")
        if only_b[:6]:
            print(f"   (v3-only sample)     {only_b[:6]}")
        if diff:
            print("   --- DIFFERENT files ---")
            for k in diff[:20]:
                print(f"      {k}")
                print(f"         papers sha {sha(a[k])[:16]}  {a[k]}")
                print(f"         v3     sha {sha(b[k])[:16]}  {b[k]}")
        print("   --- focus papers ---")
        for f in FOCUS:
            hits = [k for k in common if f in k]
            for k in hits:
                rel = "IDENTICAL" if k in same else "DIFFERENT"
                print(f"      {rel:<10} {k}")
        print()

    OUT.joinpath("_p14b_papers_vs_v3_corpus.json").write_text(
        json.dumps({"note": "see stdout"}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
