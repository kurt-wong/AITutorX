# P1.4-B Phase 4 — Final Report

## Status: IMPLEMENTED + VERIFIED

## Git
- AITutors-v3: `ec62d298d68903cfa3d1e22f7cacd4a8474b7177`
- Papers: `d42cde662f5b780634a206f9c47f6482de1ed26e`

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
- **B digit-glued**: `2D.` -> D (uppercase + [.．、]); rejects `2a)` / `2\\cos`
- **C space-sep**: `D 麦哲伦` -> D; rejects `B 是 1945...`

## Tests: 24/24 passed
Positive: Q23 / Q4 / Q29 + clean regression
Negative: formula `2\\cos...=2a)`, `3F.` out-of-seq, prose `B 是`, `对A项`, outside options_lines, no-fabrication

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
