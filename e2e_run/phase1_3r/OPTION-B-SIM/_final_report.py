from pathlib import Path
import json

out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")
report = {
    "task": "P1.4-B Phase 4 — Producer Option Label Parsing Compatibility",
    "status": "IMPLEMENTED + VERIFIED",
    "git": {
        "AITutors-v3": "ec62d298d68903cfa3d1e22f7cacd4a8474b7177",
        "Papers": "d42cde662f5b780634a206f9c47f6482de1ed26e",
    },
    "files_modified": {
        "Papers/scripts/reslice_pipeline.py": "Producer _detect_option_labels Rules A/B/C + _expand_option_spans merge-missing",
        "AITutor-X corpus manifests (3)": "option label backfill only (D recovered); .p14b.bak backups kept",
        "backend/app/domains/resolver/resolver.py": "_LABEL_DIGIT_GLUE_RE + _label_offsets + Rule A trailing fallback",
        "backend/app/domains/resolver/match_normalization.py": "_line_has_option_token Rules B/C",
        "backend/tests/test_p14b_option_label_compat.py": "24 positive/negative tests",
    },
    "rules": {
        "A_trailing_label_lost": "unlabeled option content after last label in options_lines -> next sequential letter (Chem Q23)",
        "B_digit_glued": "digit + uppercase letter + [.．、] -> letter (Math Q4 `2D.`). Rejects `2a)` and `2\\cos...`",
        "C_space_sep": "line-start letter + space + CJK, not prose (是/有/在/...) -> letter (History Q29 `D 麦哲伦`)",
        "hard_scope": "candidate evidence MUST be inside options_lines",
        "authority": "Source-local deterministic only; NEVER answer->option; NEVER LLM",
    },
    "tests": {
        "file": "tests/test_p14b_option_label_compat.py",
        "total": 24,
        "passed": 24,
        "positive": ["Q23 trailing D", "Q4 digit-glue D", "Q29 space-sep D", "merge-missing on partial lists", "clean A/B/C/D regression"],
        "negative": ["2\\cos^2a-1=2a) NOT label", "2a) NOT A", "3F. out of sequence", "B 是 1945... NOT option", "对A项/参见教材A册 NOT label", "outside options_lines NOT detected", "no fabrication when no evidence"],
    },
    "full_regression": {
        "passed": 2278,
        "failed": 3,
        "failed_detail": "test_adv_state_audit.py worktree-cleanliness audits — fail BECAUSE authorized local changes exist (Papers reslice_pipeline.py modified). Not functional failures.",
        "skipped": 1,
        "xfailed": 1,
    },
    "phase_replay": {
        "baseline_af70d64": {"root": 284, "ready": 227, "incomplete": 57, "auto": 154, "pending": 68, "rejected": 5},
        "after_B_repair": {"root": 284, "ready": 227, "incomplete": 57, "auto": 155, "pending": 67, "rejected": 5},
        "delta": {"root": 0, "ready": 0, "incomplete": 0, "auto": +1, "pending": -1, "rejected": 0},
    },
    "per_sample": [
        {
            "sample": "Chemistry Q23",
            "form": "trailing label lost",
            "old_labels": ["A", "B", "C"],
            "new_labels": ["A", "B", "C", "D"],
            "old_answer": "D",
            "new_answer": "D",
            "answer_in_old": False,
            "answer_in_new": True,
            "old_gate": "pending_review",
            "new_gate": "auto_approve",
            "gate_delta": +1,
            "evidence_delta": "repaired",
        },
        {
            "sample": "Math Q4",
            "form": "digit-glued 2D.",
            "old_labels": ["A", "B", "C"],
            "new_labels": ["A", "B", "C", "D"],
            "old_answer": "None (teacher block)",
            "new_answer": "None (unchanged)",
            "answer_in_old": None,
            "answer_in_new": None,
            "old_gate": "pending_review",
            "new_gate": "pending_review",
            "gate_delta": 0,
            "evidence_delta": "repaired",
            "note": "Gate blocker remains answer-slice / AnswerTokenContract (NOT in scope). Q4 B repair != Gate improvement.",
        },
        {
            "sample": "History Q29",
            "form": "separator loss D 麦哲伦",
            "old_labels": ["A", "B", "C"],
            "new_labels": ["A", "B", "C", "D"],
            "old_answer": "C",
            "new_answer": "C",
            "answer_in_old": True,
            "answer_in_new": True,
            "old_gate": "auto_approve",
            "new_gate": "auto_approve",
            "gate_delta": 0,
            "evidence_delta": "repaired",
            "note": "Already auto. Q29 B repair is Option Evidence completeness, NOT Gate improvement.",
        },
    ],
    "auto_delta_confirmed": {
        "predicted_simulation": 1,
        "measured_replay": 1,
        "match": True,
        "B3_to_auto3": "FALSIFIED (confirmed again by real replay)",
    },
    "stop_conditions_triggered": [],
    "boundary_precision": {
        "status": "observed (unchanged)",
        "b_repair_depends_on_boundary_change": False,
        "boundary_semantics_modified": False,
    },
    "not_modified": [
        "Gate policy",
        "AnswerTokenContract / grammar.verify contract",
        "STRICT_AUTO_TYPES",
        "S0 / B3c-B",
        "Decomposition / SUB_QUESTION_DECOMPOSITION",
        "Schema",
        "Admission",
        "P0-A role-region policy",
        "question boundary semantics",
        "DB production data",
    ],
    "future_opportunity_NOT_authorized": {
        "item": "Math S0 / answer-slice potentially unlocks +25 auto",
        "status": "NOT AUTHORIZED IN P1.4-B",
        "next": "separate S0 / answer-slice / B3c-B investigation",
    },
    "authority_red_line": {
        "implemented": "Source Evidence -> deterministic local parsing -> Option Label Evidence",
        "forbidden_and_not_used": "Answer Evidence -> guess missing option",
    },
}
(out / "p14b_phase4_final_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

md = f"""# P1.4-B Phase 4 — Final Report

## Status: IMPLEMENTED + VERIFIED

## Git
- AITutors-v3: `{report['git']['AITutors-v3']}`
- Papers: `{report['git']['Papers']}`

## Files modified
| File | Change |
|------|--------|
| Papers/scripts/reslice_pipeline.py | Producer Rules A/B/C + merge-missing |
| corpus manifests Q23/Q4/Q29 | option label backfill (D) only; .p14b.bak kept |
| backend/.../resolver.py | digit-glue + Rule A trailing fallback |
| backend/.../match_normalization.py | Rule B/C token match |
| backend/tests/test_p14b_option_label_compat.py | 24 tests |

## Rules (source-local, options_lines only)
- **A trailing label lost**: unlabeled content -> next sequential letter
- **B digit-glued**: `2D.` -> D (uppercase + [.．、]); rejects `2a)` / `2\\\\cos`
- **C space-sep**: `D 麦哲伦` -> D; rejects `B 是 1945...`

## Tests: 24/24 passed
Positive: Q23 / Q4 / Q29 + clean regression
Negative: formula `2\\\\cos...=2a)`, `3F.` out-of-seq, prose `B 是`, `对A项`, outside options_lines, no-fabrication

## Full regression
2278 passed, 3 failed (worktree-cleanliness audit only — expected with authorized local edits), 1 skipped, 1 xfailed

## Phase replay (af70d64 -> after)
| metric | before | after | delta |
|--------|--------|-------|-------|
| root | 284 | 284 | 0 |
| ready | 227 | 227 | 0 |
| incomplete | 57 | 57 | 0 |
| **auto** | **154** | **155** | **+1** |
| pending | 68 | 67 | -1 |
| rejected | 5 | 5 | 0 |

## Per-sample
| Sample | labels | answer | old gate | new gate | Gate Δ | Evidence |
|--------|--------|--------|----------|----------|-------:|----------|
| Chemistry Q23 | A,B,C -> A,B,C,D | D | pending | **auto** | **+1** | repaired |
| Math Q4 | A,B,C -> A,B,C,D | None | pending | pending | 0 | repaired |
| History Q29 | A,B,C -> A,B,C,D | C | auto | auto | 0 | repaired |

**+1 auto confirmed by real replay (matches simulation).**
Q4 Gate blocker is answer-slice (NOT in scope). Q29 was already auto — completeness only.

## STOP conditions triggered: NONE

## Boundary precision
`observed` (options outside questions_lines). **Not modified.** B repair does not depend on it.

## Not modified (confirmed)
Gate · AnswerTokenContract · STRICT_AUTO_TYPES · S0/B3c-B · Decomposition · Schema · Admission · P0-A · boundary semantics · DB

## Future opportunity (NOT authorized here)
Math S0 / answer-slice potentially unlocks +25 auto → separate S0 / answer-slice / B3c-B task.

## Authority
```
Source Evidence -> deterministic local parsing -> Option Label Evidence
FORBIDDEN: Answer Evidence -> guess missing option
```
"""
(out / "p14b_phase4_final_report.md").write_text(md, encoding="utf-8")
print("wrote final report")
print("auto delta", report["phase_replay"]["delta"])
