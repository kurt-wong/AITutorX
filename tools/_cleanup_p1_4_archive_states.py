#!/usr/bin/env python3
"""Phase 1-4: mark stale 50_OPERATIONS stage-state docs as ARCHIVED.

Does NOT rewrite document content. Inserts a status header block immediately
after the H1 title of each file, declaring the doc historical and pointing at
the single current-state document.

This is compliant with DOC-GOV Sec.7: it changes lifecycle STATUS, not location
(no physical move), and does not delete or rewrite any historical text.

Run with --apply to execute; default is dry-run.
"""
import sys
from pathlib import Path

OPS = Path(r"D:\Project\AITutor-X") / "Docs" / "50_OPERATIONS"
APPLY = "--apply" in sys.argv

HEADER = """
> **[ARCHIVED 2026-09-27]** 本文件是**历史阶段快照**，记录产生时点的状态，**不构成现行依据**。
> **Superseded By**: [`Docs/50_OPERATIONS/CURRENT_STATE.md`](CURRENT_STATE.md) — 当前状态的唯一权威来源。
> 正文保持原样不改写（DOC-GOV §7）。档案基线：tag `AITutor-X-before-cleanup` @ `43f46e8`。
"""


def main():
    targets = [p for p in sorted(OPS.glob("*.md")) if p.name != "CURRENT_STATE.md"]
    print(f"{'APPLY' if APPLY else 'DRY-RUN'}  {OPS}")
    print(f"targets: {len(targets)}\n")

    done = skipped = 0
    for p in targets:
        text = p.read_text(encoding="utf-8")
        if "[ARCHIVED 2026-09-27]" in text:
            print(f"   skip (already marked)  {p.name}")
            skipped += 1
            continue

        lines = text.split("\n")
        # find the H1 line
        h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
        if h1 is None:
            print(f"   SKIP (no H1)           {p.name}")
            skipped += 1
            continue

        new = lines[: h1 + 1] + HEADER.split("\n") + lines[h1 + 1:]
        out = "\n".join(new)

        if APPLY:
            # newline="" keeps existing line endings; no BOM.
            p.write_text(out, encoding="utf-8", newline="")
            print(f"   marked                 {p.name}")
        else:
            print(f"   would mark             {p.name}")
        done += 1

    print(f"\n{'marked' if APPLY else 'would mark'}: {done}   skipped: {skipped}")
    if not APPLY:
        print("(dry-run; re-run with --apply)")


if __name__ == "__main__":
    main()
