#!/usr/bin/env python3
"""Post-cleanup verification: reference integrity + structural checks.

Confirms the Phase 1/2 productionization did not break any document reference.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(r"D:\Project\AITutor-X")
DOCS = ROOT / "Docs"

# only count references that carry a directory prefix - those are the ones a
# move can break. Bare filenames are location-independent.
REF = re.compile(
    r"(?:Docs[/\\])?"
    r"(00_GOVERNANCE|10_SPEC|20_ARCHITECTURE|30_CONTRACTS|"
    r"40_DECISIONS|50_OPERATIONS|60_REPORTS|90_ARCHIVE)"
    r"[/\\]([A-Za-z0-9._\u4e00-\u9fff\-]+\.(?:md|json|py|txt|html))")


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True,
                          text=True, encoding="utf-8").stdout


def main():
    files = [p for p in ROOT.rglob("*") if p.is_file()
             and p.suffix in {".md", ".py", ".json", ".yaml", ".yml"}
             and ".git" not in p.parts]
    print(f"scanning {len(files)} files\n")

    prefixed_broken, prefixed_ok = [], 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in REF.finditer(text):
            layer, target = m.group(1), m.group(2)
            cand = DOCS / layer / target
            if cand.exists():
                prefixed_ok += 1
            else:
                prefixed_broken.append((str(f.relative_to(ROOT)), layer, target))

    print(f"directory-prefixed references resolved : {prefixed_ok}")
    print(f"directory-prefixed references BROKEN   : {len(prefixed_broken)}")
    seen = set()
    for src, layer, t in prefixed_broken:
        key = (layer, t)
        if key in seen:
            continue
        seen.add(key)
        print(f"   ! {layer}/{t}   (first seen in {src})")

    # structural assertions
    print("\n--- structural checks ---")
    root_md = sorted(p.name for p in ROOT.glob("*.md"))
    expect = {"AGENTS.md", "README.md", "MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01.md"}
    print(f"root .md files        : {root_md}")
    print(f"root matches allowlist: {set(root_md) == expect}")
    print(f"CURRENT_STATE exists  : {(DOCS / '50_OPERATIONS' / 'CURRENT_STATE.md').exists()}")
    print(f"90_ARCHIVE populated  : {len(list((DOCS / '90_ARCHIVE').rglob('*.*'))) > 0}")
    print(f"ACTIVE status count   : ", end="")
    n = 0
    for p in DOCS.rglob("*.md"):
        head = p.read_text(encoding="utf-8", errors="ignore")[:1500]
        if re.search(r"^\*\*Status\*\*:\s*`?ACTIVE", head, re.M):
            n += 1
    print(n)

    print("\n--- last 4 commits ---")
    print(git("log", "--oneline", "-4"))
    st = git("status", "--porcelain")
    untracked = [l for l in st.splitlines() if l.startswith("??")]
    modified = [l for l in st.splitlines() if l and not l.startswith("??")]
    print(f"uncommitted modified/renamed: {len(modified)}")
    print(f"untracked (pre-existing)    : {len(untracked)}")


if __name__ == "__main__":
    main()
