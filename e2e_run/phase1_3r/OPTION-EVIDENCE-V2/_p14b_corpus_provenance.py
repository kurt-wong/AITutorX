"""READ-ONLY: corpus variant provenance census.

Phase 1 consumes preprocessed artifacts, NOT raw PDF. This census answers:
  - which preprocessing variants exist on disk
  - whether the same paper appears in several variants
  - whether those variants are byte-identical, near-identical, or unrelated
    (identical copies => variant is NOT the source of divergence;
     differing copies => each variant is its own input and conclusion cannot be
     transferred between them)

Also records the manifest-side provenance fields (model / identity_version /
source_content_sha256) that V3's manifest_reader preserves verbatim.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans")
MIN = Path(r"D:\Project\AITutor-X\e2e_run\phase1_min_corpus")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    # group every .md by basename across all variants
    by_name: dict[str, list[Path]] = defaultdict(list)
    for base in (ROOT, MIN):
        for p in base.rglob("*.md"):
            by_name[p.name].append(p)

    focus = [n for n in by_name if ("数学（教师版）" in n and "春季" in n)
             or ("化学（教师版）" in n and "春季" in n)
             or ("历史（教师版）" in n and "夏季" in n)]
    print("=" * 96)
    print("CORPUS VARIANT PROVENANCE")
    print("=" * 96)
    print(f"total distinct .md basenames: {len(by_name)}")

    print("\n--- focus papers across variants (byte identity) ---")
    for n in sorted(focus):
        paths = by_name[n]
        hashes = {sha(p): p for p in paths}
        print(f"\n{n}")
        print(f"   copies: {len(paths)}  distinct sha256: {len(hashes)}")
        for h, p in hashes.items():
            variant = p.relative_to(p.parents[len(p.parents) - 3]) if len(p.parents) > 3 else p
            print(f"      {h[:16]}  {p}")

    # how many papers have >1 variant and are NOT byte-identical
    multi, divergent, identical = 0, 0, 0
    for n, paths in by_name.items():
        if len(paths) < 2:
            continue
        multi += 1
        if len({sha(p) for p in paths}) == 1:
            identical += 1
        else:
            divergent += 1
    print("\n--- all papers with >1 variant ---")
    print(f"   papers with multiple copies : {multi}")
    print(f"   byte-identical across copies: {identical}")
    print(f"   DIVERGENT across copies     : {divergent}")

    # manifest-side provenance for every variant that has one
    print("\n--- manifest-side provenance (model / identity_version) ---")
    models, idvers = defaultdict(int), defaultdict(int)
    for mf in ROOT.rglob("*.manifest.json"):
        try:
            d = json.loads(mf.read_text(encoding="utf-8"))
        except Exception as e:
            print("   !! unreadable", mf, e)
            continue
        models[d.get("model")] += 1
        idvers[d.get("identity_version")] += 1
    print("   model            :", dict(models))
    print("   identity_version :", dict(idvers))

    # which variants carry manifests at all
    print("\n--- variants present on disk ---")
    for v in sorted({p.relative_to(ROOT).parts[0] for p in ROOT.iterdir() if p.is_dir()}):
        nmd = len(list((ROOT / v).rglob("*.md")))
        nman = len(list((ROOT / v).rglob("*.manifest.json")))
        print(f"   {v:<24} .md={nmd:<4} .manifest.json={nman}")

    OUT.joinpath("_p14b_corpus_provenance.json").write_text(
        json.dumps({
            "focus_copies": {n: [str(p) for p in by_name[n]] for n in sorted(focus)},
            "papers_multi": multi, "identical": identical, "divergent": divergent,
            "models": dict(models), "identity_versions": {str(k): v for k, v in idvers.items()},
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_corpus_provenance.json'}")


if __name__ == "__main__":
    main()
