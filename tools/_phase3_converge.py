#!/usr/bin/env python3
"""Phase 3-A: Authority Layer convergence - resolve the last 24 ACTIVE docs.

Classification is NOT purely mechanical. The Sec.8A staleness rule flags all 24
(they are all >50 commits behind), so it has no discriminating power here - the
Owner explicitly rejected blanket archival. Verdicts below are per-document,
with the reason recorded inline.

Vocabulary (DOC-GOV Sec.8): OPEN / CLOSED / DEFERRED / ARCHIVED.
  CLOSED   = stage finished; document remains in the main plane (still readable,
             still cited), lifecycle complete. Used for the decision ledgers.
  ARCHIVED = historical; no longer part of the active read path.

Run with --apply; default is dry-run.
"""
import re
import sys
from pathlib import Path

DOCS = Path(r"D:\Project\AITutor-X") / "Docs"
APPLY = "--apply" in sys.argv

# rel_path -> (new_status, note)
VERDICT = {
    # ---- RETAIN in place: current cross-system vocabulary or current baseline ----
    r"10_SPEC\X2-03-CONCEPT-TERMINOLOGY-MAP.md": ("CLOSED",
        "CANONICAL cross-system vocabulary (source_content_sha256 / Seal / Manifest / PIS). "
        "Uniquely held here. Identity Domain decision is STILL OPEN -> must not archive."),
    r"10_SPEC\X2.5-02-CONCEPT-MATRIX.md": ("CLOSED",
        "Canonical concept matrix incl. Producer<->V3 conflict rows and byte-domain distinction. "
        "Required input for the open Identity Domain decision."),
    r"20_ARCHITECTURE\X2-01-UNIFIED-SYSTEM-BASELINE.md": ("CLOSED",
        "Current factual baseline of the two source systems being merged. "
        "Directly needed for the coming code merge."),
    r"20_ARCHITECTURE\X2-02-UNIFIED-ARCHITECTURE-BASELINE.md": ("CLOSED",
        "Current architecture baseline of the merged system."),
    r"30_CONTRACTS\X2-04-CROSS-SYSTEM-CONTRACT-AUDIT.md": ("CLOSED",
        "Cross-system contract surface (Producer<->Consumer). Integration work still ahead."),
    r"30_CONTRACTS\X2.5-03-PRODUCER-CONSUMER-AUDIT.md": ("CLOSED",
        "Producer/Consumer contract audit matrix; interface boundary still live."),

    # ---- ARCHIVE: superseded governance-process artifacts ----
    r"10_SPEC\X2-05-UNIFIED-DOCUMENTATION-MAP.md": ("ARCHIVED",
        "Documentation MIGRATION PLAN (27 MIGRATE/MERGE cells). Points at a direction now "
        "deprecated by DOC-GOV Sec.7/Sec.10/Sec.11. Misleading if left ACTIVE."),

    r"20_ARCHITECTURE\X2.5-01-PRE-MIGRATION-BASELINE.md": ("ARCHIVED",
        "X2.5 stage fact matrices; stage closed, superseded by X2.6 baseline closure."),
    r"20_ARCHITECTURE\X2.5.1-01-CORRECTIONS.md": ("ARCHIVED",
        "X2.5.1 mandatory corrections C1-C5; X2.5.1 stage closed."),

    # ---- 60_REPORTS: reports are historical records, never system state ----
    r"60_REPORTS\REPORT-X2.5-PRE-MIGRATION-BASELINE.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-CLOSURE-01-CLAUDE-AUDIT.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-CLOSURE-02-CLOSURE-MATRIX.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-CLOSURE-DSH-AUDIT.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-CLOSURE-REPORT-CLAUDE.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-CURRENT-STATE-REGISTRATION-CORRECTION-DSH.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-FINAL-REGISTRATION-DSH-AUDIT.md": ("ARCHIVED", "stage report"),
    r"60_REPORTS\X2.5-OWNER-CLOSURE-01-PACKAGE.md": ("ARCHIVED", "stage report"),

    # ---- 40_DECISIONS: Owner ruled group -> CLOSED, NOT archived ----
    r"40_DECISIONS\X2-06-DECISION-MAPPING.md": ("CLOSED", "decision record - value is the 'why', not recency"),
    r"40_DECISIONS\X2-07-DIFFERENCE-LEDGER.md": ("CLOSED", "decision record - value is the 'why', not recency"),
    r"40_DECISIONS\X2-08-MIGRATION-CANDIDATE-REGISTRY.md": ("CLOSED", "decision record - value is the 'why', not recency"),
    r"40_DECISIONS\X2.5-04-MIGRATION-CANDIDATE-MATRIX.md": ("CLOSED", "decision record - value is the 'why', not recency"),
    r"40_DECISIONS\X2.5-05-CONFLICT-LEDGER.md": ("CLOSED", "conflict ledger - retains unresolved items; document lifecycle closed, NOT the conflicts"),
    r"40_DECISIONS\X2.5-CLOSURE-03-CONFLICT-UPDATE.md": ("CLOSED", "conflict ledger update - same caveat"),
    r"40_DECISIONS\X2.5.1-03-CONFLICT-UPDATES.md": ("CLOSED", "conflict ledger update - same caveat"),
}
VERDICT = {k: v for k, v in VERDICT.items() if v}

STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*`?ACTIVE([^`\n]*)`?\s*$")

HEADER = {
    "CLOSED": ("> **[CLOSED 2026-09-27]** 本文件的生命周期已结束（阶段完成）。**正文保持原样不改写**（DOC-GOV §7）。\n"
               "> 保留在主视野：其内容仍具参考价值。当前状态见 [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../../50_OPERATIONS/CURRENT_STATE.md)。"),
    "ARCHIVED": ("> **[ARCHIVED 2026-09-27]** 本文件已退出主读取路径，**不构成现行依据**。**正文保持原样不改写**（DOC-GOV §7）。\n"
                 "> **Superseded By**: [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../../50_OPERATIONS/CURRENT_STATE.md) — 当前状态的唯一权威来源。\n"
                 "> 归档基线：tag `AITutor-X-before-cleanup` @ `43f46e8`。"),
}


def main():
    targets = []
    for p in sorted(DOCS.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^\*\*Status\*\*:\s*`?ACTIVE", text[:1500], re.M):
            targets.append(p)

    rel_all = {str(p.relative_to(DOCS)): p for p in targets}
    print(f"{'APPLY' if APPLY else 'DRY-RUN'}  ACTIVE docs found: {len(targets)}")
    missing = [r for r in VERDICT if r not in rel_all]
    if missing:
        print("!! verdict keys with no matching file:")
        for m in missing:
            print("   ", m)

    counts = {}
    for rel, p in sorted(rel_all.items()):
        v = VERDICT.get(rel)
        if v is None:
            print(f"   NO VERDICT (unchanged): {rel}")
            continue
        new_status, reason = v
        counts[new_status] = counts.get(new_status, 0) + 1
        print(f"\n   {rel}")
        print(f"      -> {new_status}: {reason}")

        if not APPLY:
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), 0)
        # replace the status line
        for i, ln in enumerate(lines):
            m = STATUS_RE.match(ln)
            if m:
                old = m.group(1).strip()
                lines[i] = f"**Status**: `{new_status}`（原状态：`ACTIVE{(' ' + old) if old else ''}`）"
                break
        block = HEADER[new_status].split("\n") + [""]
        lines = lines[: h1 + 1] + [""] + block + lines[h1 + 1:]
        p.write_text("\n".join(lines), encoding="utf-8", newline="")

    print(f"\nsummary: {counts}")
    if not APPLY:
        print("(dry-run; re-run with --apply)")


if __name__ == "__main__":
    main()
