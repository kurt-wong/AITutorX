#!/usr/bin/env python3
"""Phase 3-A evidence: classify the 23 remaining ACTIVE docs.

For each doc, measure:
  - refs from CODE (v3 backend app/scripts + Papers) -> does implementation depend on it?
  - refs from LIVE docs (README, CURRENT_STATE, DOC-GOV, AGENTS) -> is it on the read path?
  - refs from the V3 Frozen Spec / frozen Contract -> is it cited as a spec input?
  - refs from other docs -> general citation count
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(r"D:\Project\AITutor-X")
DOCS = ROOT / "Docs"
CODE_ROOTS = [Path(r"D:\Project\AITutors-v3\backend"), Path(r"D:\Project\Papers")]
SPEC_ROOT = Path(r"D:\Project\AITutors-v3\Docs")
LIVE = ["README.md", "AGENTS.md",
        r"Docs\50_OPERATIONS\CURRENT_STATE.md",
        r"Docs\00_GOVERNANCE\AITUTORX-DOC-GOVERNANCE.md"]

TARGETS = [p for p in DOCS.rglob("*.md")
           if re.search(r"^\*\*Status\*\*:\s*`?ACTIVE", p.read_text(encoding="utf-8",
                                                                   errors="ignore")[:1500], re.M)]


def count_refs(term, roots, exts):
    n = 0
    for r in roots:
        if not r.exists():
            continue
        for f in r.rglob("*"):
            if f.is_file() and f.suffix in exts and ".git" not in f.parts:
                try:
                    if term in f.read_text(encoding="utf-8", errors="ignore"):
                        n += 1
                except Exception:
                    pass
    return n


def main():
    print(f"{len(TARGETS)} ACTIVE docs\n")
    print(f"{'doc':<62} {'code':>5} {'live':>5} {'spec':>5} {'docs':>5}")
    print("-" * 90)
    rows = []
    for p in sorted(TARGETS):
        stem = p.stem
        code = count_refs(stem, CODE_ROOTS, {".py", ".json", ".yaml", ".yml", ".sql"})
        live = 0
        for lf in LIVE:
            fp = ROOT / lf
            if fp.exists() and stem in fp.read_text(encoding="utf-8", errors="ignore"):
                live += 1
        spec = count_refs(stem, [SPEC_ROOT], {".md"})
        docs = count_refs(stem, [DOCS], {".md"})
        rel = str(p.relative_to(DOCS))
        rows.append((rel, code, live, spec, docs))
        print(f"{rel:<62} {code:>5} {live:>5} {spec:>5} {docs:>5}")

    print("\n\nverdicts (rule from Owner):")
    print("  code>0 or live>0 or spec>0  -> RETAIN (status CLOSED)")
    print("  all zero                    -> ARCHIVE candidate")
    for rel, code, live, spec, docs in rows:
        keep = code > 0 or live > 0 or spec > 0
        print(f"  {'RETAIN ' if keep else 'ARCHIVE'}  {rel}")


if __name__ == "__main__":
    main()
