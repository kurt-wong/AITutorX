#!/usr/bin/env python3
"""Fix relative links introduced by the Phase 1/3 status headers.

Checks every markdown link of the form [..](../../../path) in the docs touched by
the cleanup, resolves it against the file's directory, and if it does not exist
rewrites it to a path that does. Reports anything it cannot fix.

Run with --apply; default is dry-run.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"D:\Project\AITutor-X")
DOCS = ROOT / "Docs"
APPLY = "--apply" in sys.argv

LINK_RE = re.compile(r"\]\((\.\.?/[^)]+)\)")


def main():
    print(f"{'APPLY' if APPLY else 'DRY-RUN'}  scanning relative links under Docs/\n")
    fixed = checked = broken = 0
    for p in sorted(DOCS.rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        if "](" not in text:
            continue
        new_text = text
        for m in LINK_RE.finditer(text):
            raw = m.group(1)
            checked += 1
            target = (p.parent / raw).resolve()
            if target.exists():
                continue
            # try alternative prefixes: strip one leading '../' or add one
            cands = []
            if raw.startswith("../../"):
                cands.append("../" + raw[6:])
            if raw.startswith("../"):
                cands.append("../../" + raw[3:])
                cands.append(raw[3:])
            hit = None
            for c in cands:
                if (p.parent / c).resolve().exists():
                    hit = c
                    break
            if hit:
                new_text = new_text.replace("](" + raw + ")", "](" + hit + ")")
                print(f"   {p.relative_to(ROOT)}")
                print(f"      {raw}  ->  {hit}")
                fixed += 1
            else:
                broken += 1
                print(f"   !! UNFIXABLE in {p.relative_to(ROOT)}: {raw}")
        if new_text != text and APPLY:
            p.write_text(new_text, encoding="utf-8", newline="")

    print(f"\nlinks checked: {checked}   fixed: {fixed}   unfixable: {broken}")
    if not APPLY:
        print("(dry-run; re-run with --apply)")


if __name__ == "__main__":
    main()
