#!/usr/bin/env python3
"""Phase 1-2a: relocate 11 root duplicate DSH reports into Docs/60_REPORTS/.

Rationale (verified before this script was written):
  - Each root file is content-identical to its Docs/60_REPORTS twin
    (differences are CRLF vs LF only).
  - All 29 inbound references to these files are BARE FILENAMES (no directory
    prefix), so relocation breaks zero references.
  - The root copies are git-TRACKED; the Docs/60_REPORTS copies are UNTRACKED.
    So this is a genuine `git mv` (history preserved), overwriting the
    untracked duplicate. This is the step DSH-X26-02 called for and whose
    DOC-GOV note was lost in the 2026-09-27 rewrite.

Run with --apply to execute; default is dry-run.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\Project\AITutor-X")
REPORTS = ROOT / "Docs" / "60_REPORTS"
APPLY = "--apply" in sys.argv

FILES = [
    "X2-DSH-ATTACK-REPORT.md",
    "X2-DSH-FINAL-ATTACK-SUMMARY.md",
    "X2-DSH-FINAL-REPORT.md",
    "X2-DSH-REPORT.md",
    "X2.1-DSH-AUDIT-REPORT.md",
    "X2.1-DSH-FINAL-VERDICT.md",
    "X2.5-DSH-AUDIT-REPORT.md",
    "X2.5.1-DSH-AUDIT-REPORT.md",
    "X2.5.1-DSH-FINAL-VERDICT.md",
    "X2.5.2-DSH-AUDIT-REPORT.md",
    "X2.5.2-DSH-FINAL-VERDICT.md",
]


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, encoding="utf-8")


def norm(b: bytes) -> str:
    return b.decode("utf-8").lstrip("\ufeff").replace("\r\n", "\n")


def main():
    print(f"{'APPLY' if APPLY else 'DRY-RUN'}  root -> Docs/60_REPORTS\n")
    planned, skipped = [], []
    for name in FILES:
        src, dst = ROOT / name, REPORTS / name
        if not src.exists():
            skipped.append((name, "root source missing"))
            continue
        if not dst.exists():
            skipped.append((name, "destination twin missing - NOT a duplicate"))
            continue
        if norm(src.read_bytes()) != norm(dst.read_bytes()):
            skipped.append((name, "CONTENT DIFFERS - manual review required"))
            continue
        # is the root copy tracked?
        t = git("ls-files", "--error-unmatch", name)
        if t.returncode != 0:
            skipped.append((name, "root copy not tracked - use plain move"))
            continue
        planned.append(name)

    print(f"safe to relocate: {len(planned)}")
    for n in planned:
        print(f"   + {n}")
    if skipped:
        print(f"\nSKIPPED ({len(skipped)}):")
        for n, why in skipped:
            print(f"   ! {n}: {why}")

    if not APPLY:
        print("\n(dry-run; re-run with --apply)")
        return

    print("\napplying...")
    ok = 0
    for n in planned:
        r = git("mv", "-f", n, f"Docs/60_REPORTS/{n}")
        status = "OK" if r.returncode == 0 else f"FAIL: {r.stderr.strip()}"
        print(f"   {status:60} {n}")
        if r.returncode == 0:
            ok += 1
    print(f"\nrelocated {ok}/{len(planned)}")


if __name__ == "__main__":
    main()
