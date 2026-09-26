# FORMAL-E2E-ENABLEMENT-REPORT

```text
Document ID   : FORMAL-E2E-ENABLEMENT-REPORT
Task ID       : FORMAL-E2E-ENABLEMENT-01
Document Type : Implementation + Evidence Report
Date          : 2026-09-26
Executor      : MIMO CODE (implementation only; no architecture adjudication)
Authority     : Owner task book "Formal Production Pipeline Enablement"
AITutors-v3   : d2b9a26f1a1c0297b4536b273b8999a071433079  (baseline; code changes below)
AITutor-X     : 3291e7775251814d0f294b0d212d8f9d664b70ab  (evidence)
Papers        : 2b92898f05f6541a5fc65c8300cb8a59a06c4928  (preprocessing source)
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env.
Peak-time     : 2026-09-26 10:43-11:10 Beijing = workday 08:00-12:00 window
                => DeepSeek FORBIDDEN; MIMO only. Observed policy held.
```

---

## 0. Executive Summary

```text
ENABLEMENT TARGET : Preprocessing → V3 Formal Pipeline minimal closed loop
ENABLEMENT STATUS : ACHIEVED (provider / adapter / authorization blockers removed)
FORMAL PIPELINE   : EXECUTES END-TO-END TO GATE  (real MIMO V2.6 PRO calls)
QUESTION OBJECTS  : NOT YET GENERATED (0 questions / 0 instances / 0 candidates)

FIRST BLOCKING POINT AFTER ENABLEMENT
  Stage   : Resolver → IR
  Error   : semantic_status=incomplete for all top-level units
  Effect  : GateService skips incomplete units → 0 admission_candidates → 0 Question
  Cause   : real-document span resolution (answer / option / stem) not fully closed
            under Frozen resolver grammar vs observed OCR/text formats
  Class   : semantic resolution gap — OUTSIDE this task's provider/adapter/authorization scope
  Action  : recorded as Gap; Owner Decision required; NOT silently fixed
```

Formal production path was entered only through its documented entries
(`DocumentImportService.import_file` == `POST /api/documents/import`, and
`TaskExecutor.run_once` as driven by `python -m app.worker run --allow-live`).
No fake provider. No bypass authorization. No dummy `task_context` / `budget_ok`.

---

## 1. Scope of Changes

### 1.1 In scope (this task)

| Area | Change |
|---|---|
| V3 LLM Gateway | Formal provider = `mimo` / `mimo-v2.6-pro`; DeepSeek config retained |
| V3 Worker authorization | `authorize()` fed from real claimed Task + `BudgetService.ensure` |
| Provider Reality Tracking | `ProviderRealityTracker` equivalent mechanism (no schema migration) |
| Papers preprocessing provider | `llm_provider.py` + `reslice_pipeline.py` switch to formal MIMO |
| Preprocessing consumer adapter | Reuse existing `preprocessing_consumer/` (mapping verified) |
| Level 1 E2E | Single real PDF through formal pipeline; evidence captured |

### 1.2 Explicitly NOT done (per task non-goals)

- Frozen Spec modification — **NONE** (hashes below unchanged)
- Database migration — **NONE**
- X2.7 implementation — **NONE**
- Frontend implementation — **NONE**
- Question semantic redesign — **NONE**
- Admission redesign — **NONE**
- Legacy cleanup — **NONE**
- Full corpus processing — **NONE** (Level 1 = single document)

### 1.3 Frozen Spec integrity (read-only check, before/after identical)

| file | SHA256 |
|---|---|
| `00_Master_Spec.md` | `c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4` |
| `10_Data_Model.md` | `529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1` |
| `20_Document_Pipeline.md` | `0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c` |
| `30_Task_LLM_Safety.md` | `db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89` |
| `40_Development_Rules.md` | `8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db` |
| `50_Migration_Assets.md` | `8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7` |

Matches FORMAL-E2E-BASELINE-VERIFICATION-REPORT values exactly.

---

## 2. Provider Configuration Changes

### 2.1 Target (task §3)

```text
Preprocessing : provider=mimo  model=mimo-v2.6-pro
V3 Gateway    : provider=mimo  model=mimo-v2.6-pro
DeepSeek      : RETAINED (fallback / future evaluation; not deleted)
```

### 2.2 V3 (`AITutors-v3/backend`)

| Item | Before | After |
|---|---|---|
| `build_gateway()` live provider | `HTTPLLMProvider(name="ollama")` with empty base_url/model | `HTTPLLMProvider(name="mimo")` |
| Formal model | `mimo-x-pro-preview` (`.env`, rejected by live API) | `mimo-v2.6-pro` |
| DeepSeek | config fields present, unused | config fields retained; built only when `DEEPSEEK_API_KEY`+`DEEPSEEK_MODEL` set |
| Legacy model guard | none in factory | `LEGACY_TEST_MODEL_IDS` fail-closed in `_build_mimo_provider` |
| TaskExecutor defaults | `ollama` / `qwen3.5-9b` | `mimo` / `mimo-v2.6-pro` |

Files:
- `backend/app/ai/gateway.py` — MIMO factory, DeepSeek optional fallback, `authorize()`, reality hooks
- `backend/app/core/config.py` — **unchanged** (mimo/deepseek fields already present)
- `backend/.env` — `MIMO_MODEL=mimo-v2.6-pro`; DeepSeek commented placeholders retained
- `backend/app/ai/provider_reality.py` — **new** (reality tracking)

### 2.3 Papers (`D:\Project\Papers`)

| Item | Before | After |
|---|---|---|
| `scripts/reslice_pipeline.py` `DEFAULT_MODEL` | `"mimo-x-pro-preview"` | `llm_provider.MIMO_V26_PRO_MODEL` = `mimo-v2.6-pro` |
| `load_cfg()` | inline `data/.llm_config` only | delegates to `llm_provider.resolve(ROOT)` (env → legacy → defaults) |
| `scripts/llm_provider.py` | absent | added (ported from Aitutors-preprocessing proven module) |
| DeepSeek | absent | retained in `PROVIDERS["deepseek"]` (no default model; no guessing) |

Historical anchors (`pac_audit_recompute.py` etc.) **NOT modified**.

### 2.4 API key rules (task §3.3)

```text
Keys live ONLY in .env / environment variables.
NOT in code, NOT in git-tracked source, NOT in markdown, NOT in test fixtures.
This report does not contain any key material.
```

### 2.5 Peak-time policy (task §4)

```text
Window check at execution: 2026-09-26 10:43 Beijing = Friday 08:00-12:00
=> DeepSeek calls FORBIDDEN. Observed LLM calls for formal runs: provider=mimo only.
(Older llm_call_audit rows from unit-test fixtures mention deepseek/primary/fallback
 with test model tags — those are test artifacts, not formal production calls.)
```

---

## 3. Preprocessing Adapter

### 3.1 Existing producer reused (task §5.1)

```text
backend/scripts/preprocessing_consumer/  — ALREADY EXISTS
Action: REUSED. No second adapter created.
```

### 3.2 Mapping verification (task §5.2)

Tested on real manifest `2022北京丰台高一（下）期末历史（教师版）(1).manifest.json`
(30 units; both `standalone_question` and `composite_question` present):

| Producer | Canonical V3 | Result |
|---|---|---|
| `standalone_question` | `standalone_unit` | OK |
| `composite_question` | `composite_unit` | OK |
| `material` | `shared_components{"material": ...}` | OK — stored once, **not** merged into sub-question stem |

Evidence: adapter unit test script output — composite `Q27`–`Q30` have
`shared_components keys: ['material']`; each `sub_questions[].content.stem` is
role-only dict (no material text). `shared_material` semantics preserved.

Known gaps already registered by adapter (not silently dropped):
`SUB_QUESTION_DECOMPOSITION_UNAVAILABLE`, `STANDALONE_MATERIAL_NOT_CONSUMED`,
`OPTION_LABEL_SPAN_UNAVAILABLE`.

---

## 4. Provider Reality Tracking (task §6)

Requirement: distinguish *declared* vs *actually executed*.

```text
configured_model    — from task params / settings (e.g. mimo-v2.6-pro)
actual_provider     — gateway.last_actual_provider after live complete()
execution_status    — completed | failed (from execution outcome)
execution_timestamp — UTC ISO-8601 at record time
```

**Equivalent mechanism** (no DB schema migration, per non-goals):

- New module: `backend/app/ai/provider_reality.py` (`ProviderRealityTracker`)
- Wired in `backend/app/ai/executor.py` after live finalize (never breaks accounting)
- Gateway records `last_actual_provider` / `last_configured_model` in `_live()`
- Sidecar JSON: `e2e_run/provider-reality-level1*.json`
- Existing `llm_call_audit` rows also record `provider`, `model`, `status`, `start`

---

## 5. Formal Worker Authorization (task §7)

### 5.1 Problem (baseline)

```text
GatewayDeniedError: "live denied: task context missing; budget unavailable"
Worker build_gateway(allow_live=...) left task_context=None, budget_ok=False.
```

### 5.2 Solution (real runtime context only)

`TaskExecutor._authorize_live_from_real_context(task_id)` after claim:

1. Load **real** `Task` row from DB (claimed task; not dummy)
2. `BudgetService.ensure(AccountRef("task", str(task_id)))` — real budget authority
3. `gateway.authorize(task_context=real_task_dict, budget_ok=True)`

Forbidden forms **not used**: `hardcode=True`, `object()`, dummy context, test bypass.

`LLMGateway.authorize()` rejects `task_context=None` with `GatewayDeniedError`.

### 5.3 Human authorization

`--allow-live` remains the documented human-authorization parameter
(`app/ai/live_guard.py`). Not a bypass; required by formal entry.

---

## 6. Testing (Level 1, task §8)

### 6.1 Commands

```bash
# Unit / regression (V3)
cd D:\Project\AITutors-v3\backend
python -m pytest tests/ -q
# Result: 2012 passed, 1 skipped, 1 xfailed  (after gateway/executor/task tests)

# Level 1 formal E2E
cd D:\Project\AITutors-v3\backend
python D:\Project\AITutor-X\e2e_run\formal_e2e_level1.py
python D:\Project\AITutor-X\e2e_run\formal_e2e_level1b.py
```

### 6.2 E2E inputs (real PDFs)

| Run | PDF | bytes | sha256 |
|---|---|---|---|
| A | `Papers\maintainess\PDF\2021北京高三二模数学汇编：集合（教师版）.pdf` | 151212 | `89a26462e62f03a5a56cf6d36962ac4fdfc888cab999c057252da9048d61edc1` |
| B | `Papers\maintainess\PDF\2018北京一零一中高一分班考物理（教师版）(1).pdf` | 843397 | `311a567eb928481333c6e97e749f237cb9250e3c94cffa88ea43db681efebbe3` |

### 6.3 Pipeline execution results

| Stage | Run A (math) | Run B (physics) |
|---|---|---|
| PDF → V3 Import | PASS (task queued) | PASS |
| Seal | PASS (90 lines / sealed) | PASS (609 lines / sealed) |
| Quality | PASS | PASS |
| Semantic Annotation | **PASS** (valid, 7 units) | **PASS** (valid, 20 units) |
| LLM call | **mimo / mimo-v2.6-pro / completed** | **mimo / mimo-v2.6-pro / completed** |
| Resolver | executed (32 resolved / 17 unresolved) | executed (46 resolved / 70 unresolved) |
| IR | built; **all units incomplete** | built; **all units incomplete** |
| Admission | 0 candidates (incomplete units skipped) | 0 candidates |
| Question / Instance | **0 / 0** | **0 / 0** |
| Task terminal | `succeeded` (claim outcome=succeeded) | `succeeded` |

### 6.4 LLM Reality (formal production calls only)

| request time (UTC) | configured_provider | configured_model | actual | status |
|---|---|---|---|---|
| 2026-09-26T02:59:54Z | mimo | mimo-v2.6-pro | mimo | completed |
| 2026-09-26T03:06:50Z | mimo | mimo-v2.6-pro | mimo | completed |

Token usage / cost: not returned by provider body in this adapter path (`input_tokens`/`output_tokens`/`estimated_cost` = NULL in audit). Recorded as UNKNOWN, not zero-filled.

---

## 7. FIRST BLOCKING POINT (post-enablement)

```text
Stage          : Resolver → IR  (before Admission / Question)
Observed error : every top-level unit semantic_status = "incomplete"
Source         : app/domains/compile/ir.py  (_validate_node)
                 app/domains/resolver/resolver.py  (role resolution)
Representative unresolved evidence (Run B physics):
  option.*     resolution_status=incomplete   (40 refs)
  answer       resolution_status=missing      (19 refs)
  stem         resolution_status=ambiguous     (8 refs)
  stem         resolution_status=missing       (3 refs)
Representative (Run A math):
  explanation  resolution_status=missing  evidence=('no 详解/解析 header',)
               — source uses same-line 【解答】解：... form;
                 Frozen is_explanation_header() is exact-bracket / bare-token only
                 (H-3 frozen grammar) so 【解答】解： is NOT a header.
  Q1/Q2 stem   ambiguous ('question N start not unique')
Possible cause : Frozen resolver grammar + observed OCR/text layouts
                 (answer lines like "11.【答案】ABC" on one line;
                  option labels packed onto shared lines;
                  explanation headers with inline content)
               — a provenance/format coverage question, NOT a provider/auth gap.
Action taken   : RECORD ONLY. Do not modify Frozen Spec. Do not silently repair.
Escalation     : Owner Decision required on grammar coverage / annotation retry policy.
```

Closest near-miss (Run B): `Q11`–`Q14` have stem+options+explanation resolved;
only `answer` unresolved. `Q16`/`Q17`/`Q20` have stem+explanation; only `answer` unresolved.

---

## 8. Evidence Index

| Artifact | Path |
|---|---|
| Level 1 run A evidence | `e2e_run/formal-e2e-level1.json` |
| Level 1 run B evidence | `e2e_run/formal-e2e-level1b.json` |
| Evidence summary | `e2e_run/formal-e2e-evidence-summary.json` |
| Provider reality (A/B) | `e2e_run/provider-reality-level1.json`, `...level1b.json` |
| E2E scripts | `e2e_run/formal_e2e_level1.py`, `formal_e2e_level1b.py` |
| Git status | see §1 / §2 file lists |

---

## 9. Remaining Gaps (recorded, not solved here)

| ID | Gap | Owner Decision needed |
|---|---|---|
| GAP-E2E-01 | Resolver/IR incomplete on real corpora → 0 Question objects | Grammar coverage vs document formats; or Annotation incomplete-retry (20 §4.7) wiring |
| GAP-E2E-02 | `is_explanation_header` exact-match misses `【解答】解：...` same-line form | Whether to extend Frozen H-3 grammar (Spec change — forbidden here) |
| GAP-E2E-03 | Answer lines `N.【答案】X` often `missing` under `answer_zone=answer_table` | Resolver answer policy vs observed teacher-edition layout |
| GAP-E2E-04 | Option label spans `incomplete` when labels share a line | Resolver option policy vs OCR line packing |
| GAP-E2E-05 | Provider token usage / cost not populated in audit for MIMO responses | Whether to parse usage from response body (audit completeness) |
| GAP-E2E-06 | Preprocessing re-execution (Papers LLM) not part of Level 1 runs (existing products used historically; formal V3 path seals PDF natively) | Whether Level 1 must include live Papers preprocessing call |

---

## 10. Completion Criteria Checklist

| Criterion | Status |
|---|---|
| Original PDF → Preprocessing → V3 Import → Annotation → Resolver → IR → Admission → Question | **PARTIAL** — chain executes through IR/Gate; Question not generated (see §7) |
| 实际调用 MIMO V2.6 PRO 或明确记录失败 | **YES** — 2/2 formal calls `mimo`/`mimo-v2.6-pro`/`completed` |
| 无 fake provider | **YES** |
| 无 bypass authorization | **YES** (real Task + BudgetService.ensure; `--allow-live` human gate only) |
| 全链路 evidence 可复核 | **YES** (JSON artifacts + DB rows + this report) |

---

## 11. Git Change Manifest (working tree; commits follow Owner delivery)

### AITutors-v3 (consumer)

```text
M backend/app/ai/gateway.py           — MIMO formal provider, authorize(), reality hooks
M backend/app/ai/executor.py          — reality tracker wiring
M backend/app/domains/task/executor.py— real-context authorization; defaults mimo/mimo-v2.6-pro
M backend/app/worker/__main__.py      — no dummy auth; flush reality evidence
M backend/tests/test_gateway.py       — formal provider expectation updated to mimo
A backend/app/ai/provider_reality.py  — new (equivalent mechanism)
```

### Papers (preprocessing source; `.git` preserved)

```text
M scripts/reslice_pipeline.py         — formal MIMO via llm_provider
A scripts/llm_provider.py             — provider registry (mimo + deepseek retained)
```

### AITutor-X (evidence)

```text
A Docs/60_REPORTS/FORMAL-E2E-ENABLEMENT-REPORT.md
A e2e_run/formal_e2e_level1.py / formal_e2e_level1b.py
A e2e_run/formal-e2e-level1.json / formal-e2e-level1b.json
A e2e_run/formal-e2e-evidence-summary.json
A e2e_run/provider-reality-level1.json / provider-reality-level1b.json
```

---

## 12. Final Statement

> Provider, adapter, and authorization blockers that stopped the Formal E2E Baseline
> are removed. The formal pipeline now performs **real MIMO V2.6 PRO** calls under
> **real task/budget authorization** and reaches Resolver/IR/Gate on real PDFs.
> Question object generation remains blocked at IR completeness on real document
> formats. That gap is recorded for Owner Decision; it was not silently repaired,
> and Frozen Spec / business semantics were not modified.
