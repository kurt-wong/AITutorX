#!/usr/bin/env python3
"""Phase 1-4b: align the inline **Status** line of the archived stage docs.

Phase 1-4 added an ARCHIVED header block but left each file's original
`**Status**: `ACTIVE — ...`` line intact, so the body still contradicted the
header (and still used the now-illegal word ACTIVE, DOC-GOV Sec.8.1).

This rewrites ONLY the **Status** line of the 17 archived stage docs:
    **Status**: `ACTIVE — <trailing text>`
 -> **Status**: `ARCHIVED`（原状态：ACTIVE — <trailing text>）

The original claim is preserved inside the parenthetical for provenance.
No other line is touched.

Run with --apply; default is dry-run.
"""
import re
import sys
from pathlib import Path

OPS = Path(r"D:\Project\AITutor-X") / "Docs" / "50_OPERATIONS"
APPLY = "--apply" in sys.argv

STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*`ACTIVE([^`]*)`\s*$")


def main():
    targets = [p for p in sorted(OPS.glob("*.md")) if p.name != "CURRENT_STATE.md"]
    print(f"{'APPLY' if APPLY else 'DRY-RUN'}  targets={len(targets)}\n")
    done = skipped = 0
    for p in targets:
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        hit = None
        for i, ln in enumerate(lines):
            if STATUS_RE.match(ln):
                hit = i
                break
        if hit is None:
            print(f"   skip (no ACTIVE Status line)  {p.name}")
            skipped += 1
            continue
        original = STATUS_RE.match(lines[hit]).group(1).strip()
        new_line = f"**Status**: `ARCHIVED`（原状态：`ACTIVE{(' ' + original) if original else ''}`）"
        print(f"   {p.name}")
        print(f"      - {lines[hit]}")
        print(f"      + {new_line}")
        if APPLY:
            lines[hit] = new_line
            p.write_text("\n".join(lines), encoding="utf-8", newline="")
        done += 1
    print(f"\n{'rewritten' if APPLY else 'would rewrite'}: {done}   skipped: {skipped}")
    if not APPLY:
        print("(dry-run; re-run with --apply)")


if __name__ == "__main__":
    main()
