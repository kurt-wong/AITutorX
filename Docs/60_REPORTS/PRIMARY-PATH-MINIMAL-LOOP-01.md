# PRIMARY PATH MINIMAL LOOP-01

**Level**: LEVEL 1
**Date**: 2026-09-27
**Commits**: Papers `969d39a`, V3 `3bf7a09`
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

---

## Implemented

### 1. Producer — option span expansion（Papers `reslice_pipeline.py`）

- `_expand_option_spans()`: `options_lines` range → per-option label spans (`options: [{label, start_line, end_line}]`)
- Source-grounded detection: labels only from actual markers in source text (regex `A.` / `B.` / `C.` etc.)
- No fabrication: if no markers detected, gap is noted but options not invented

### 2. Consumer adapter — per-option span consumption

- `manifest_reader.py`: `ManifestUnit.options: tuple[ManifestOption, ...]` — reads per-option spans
- `annotation_adapter.py`: `content.options = [{role: "option", label: "A"}, ...]` when per-option data available
- `resolved_span_adapter.py` / `runner_b2.py`: per-label resolved spans (`sp-{unit_id}.option.{label}`)

### 3. Persistence — minimal open（`runner.py`）

- `rollback()` → `commit()` (success path)
- `rollback()` preserved on exception (no partial state)

---

## Validated

| Check | Result |
|-------|--------|
| Papers tests | **339 passed, 1 xfailed** |
| V3 tests | **2034 passed, 1 skipped, 1 xfailed** |
| Option span expansion | 12 units x A/B/C/D = 48 spans |
| Adapter consumption | `content.options` per-label declared, `known_gaps: 0` |
| Resolved spans | 99 spans, 0 unresolved, 48 option spans |
| **IR ready** | **17/17 ready, 0 incomplete** (was: choice types all incomplete due to "options missing") |
| IR option content | `sp-Q1.option.A` etc. span_ids all correct |

### Key breakthrough

Before: `Question Type = Choice` -> IR needs options -> adapter doesn't declare -> `semantic_status = incomplete` -> Gate reject

Now: producer expands option spans -> adapter declares per-label -> IR `ready` -> Gate can consume

---

## Known Remaining Boundary

- Gate -> Candidate persistence needs DB session (`commit()` implemented, needs real DB run)
- B1 (import extension) / B4 (downstream IR) still open
- Persistence provenance (`role: "native"` vs Primary Path) needs correction

---

## Evidence

```
commits: Papers 969d39a / V3 3bf7a09
input:   reslice_pipeline.py, manifest_reader.py, annotation_adapter.py,
         resolved_span_adapter.py, runner.py, runner_b2.py
output:  option spans + adapter consumption + persistence commit
tests:   Papers 339+1x / V3 2034+1s+1x
IR:      17/17 ready (was: incomplete for choice types)
```
