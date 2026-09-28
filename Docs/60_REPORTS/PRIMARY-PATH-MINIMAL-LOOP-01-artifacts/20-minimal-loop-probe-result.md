# Minimal-loop probe result (READ-ONLY validation)

Date: audit session, 2026-09-27
Corpus: `FORMAL-E2E-04-evidence/consumer_input_identity_ok/2018北京夏季高中会考历史（教师版）(1).manifest.json`
- identity: `sha=d4917437065bfcb8…`, `identity_version=2`  (passes Boundary Interface Scope)
- 53 units, 1045 source lines
- `STRICT_AUTO_TYPES = {single_choice, multiple_choice, true_false}`

Method: imported the **real** V3 modules from an untouched scratch copy of the backend.
No DB, no LLM. Chain: manifest → annotation payload → ResolvedRun → IR → Compiler → `gate.policy.evaluate`.

## Result

| | ready units | option spans | gate decisions |
|---|---|---|---|
| BASELINE (as shipped) | 3 / 53 (50 incomplete) | +0 | `pending_review: 3`, `auto_approve: 0` |
| PATCHED (+ per-label options) | **53 / 53** (0 incomplete) | +172 | `auto_approve: 42`, `pending_review: 11` |

The 11 residual `pending_review` = 8 `single_choice` (answer value not strict-auto-verifiable)
+ 3 `short_answer` (canonical type outside the Owner-frozen `STRICT_AUTO_TYPES` set).

## What the patch consisted of (nothing else changed)

1. `content["options"] = [{"label": "A", "role": "option", "question_label": "1"}, …]`
   in the annotation payload — derived **only** from the manifest's own declared
   `options_lines` range plus the per-line label token in the source markdown.
2. Emitting `sp-<uid>.option.<label>` `ResolvedSpan`s for the same labels.
   `runner_b2._make_resolved_span` already accepts a `label` parameter;
   `_try_options_region()` just declines to use it.

No V3 core edit. No Frozen Spec edit. No Contract edit. No answer/grammar/value invention —
only option labels that are literally present at the head of their own source lines
(`A. 早期奴隶制国家产生`), matched by the resolver's own frozen grammar
(`resolver/reference.py` / `match_normalization.py::_line_has_option_token`).

## Caveat (not yet demonstrated)

This probe stops at the Gate **decision**. It does not demonstrate:
- candidate persistence (the shipped `runner.py` still does `finally: session.rollback()`),
- Question/Material materialization,
- the end-to-end run through `runner_b2.py` with a live DB.

Those require the persistence-boundary decision plus a real run.
