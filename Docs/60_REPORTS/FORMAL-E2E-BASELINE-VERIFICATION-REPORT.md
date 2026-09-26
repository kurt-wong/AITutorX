# FORMAL PRODUCTION-PIPELINE E2E BASELINE VERIFICATION REPORT

```text
Document ID   : FORMAL-E2E-BASELINE-VERIFICATION-REPORT
Document Type : Engineering Verification Execution Report (baseline evidence record)
Date          : 2026-09-26
Executor      : DSH (independent executor; no implementer involvement, no fix applied)
Authority     : Owner task book "Formal Production-Pipeline E2E Baseline Verification"
AITutors-v3   : d2b9a26f1a1c0297b4536b273b8999a071433079  @ od01-r3-convergence  (subject)
AITutor-X     : 77157035399830f9e7ab3f3c44341db700249fe7  @ main                 (evidence)
Papers        : 2b92898f05f6541a5fc65c8300cb8a59a06c4928  @ main                 (producer)
Evidence root : D:\Project\AITutor-X\e2e_baseline\
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.
```

---

## §0 EXECUTIVE SUMMARY

```text
FORMAL PIPELINE STATUS : BLOCKED
LAST SUCCESSFUL STAGE  : V3 SOURCE (Seal + Quality Check)
FIRST BLOCKING POINT   : SEMANTIC ANNOTATION  (LLMGateway denies the live call)
FIRST OBSERVED DEVIATION : UNRESOLVED / NOT REACHABLE  (no Question exists on the formal path)

FINAL OBJECTS PRODUCED BY THIS ROUND'S FORMAL RUN:
  questions = 0 · question_instances = 0 · materials = 0 · semantic_annotations = 0 · admission_candidates = 0
```

The formal production pipeline, entered **only** through its own documented entries
(`POST /api/documents/import`, `python -m app.worker run --allow-live`) with **no injected state,
no harness and no bypass**, executed as follows for a real 74-page PDF:

```text
Original PDF (74 pages, 1 108 984 B)
  → V3 Import        PASS   documents +1, tasks +1 queued
  → V3 Seal          PASS   2 180 lines / 68 713 chars / 83 figures / quality=valid
  → V3 Quality       PASS   status=valid
  → V3 Annotation    BLOCKED  GatewayDeniedError: "live denied: task context missing; budget unavailable"
  → Resolver/IR      NOT REACHED
  → Compiler/Admission NOT REACHED
  → Question/Instance/Material  NOT REACHED (0 rows)
  → API              no endpoint exists for these objects
  → Frontend         no page exists for these objects
```

Separately, the **producer-side preprocessing pipeline was really executed** and **failed**:
`RuntimeError LLM 调用失败: HTTP Error 400: Bad Request` (its configured model
`mimo-x-pro-preview` is rejected by the endpoint). Preprocessing is therefore **not reproducible**
in the current environment.

**This is a baseline, not a fix.** No production code, Frozen Spec, governance document, or test
object was modified. Every number below is an executed observation with preserved evidence.

---

## §1 FROZEN BASELINE (task book §22)

```text
captured_at            : 2026-09-26T08:45:21+08:00
AITutors-v3 HEAD       : d2b9a26f1a1c0297b4536b273b8999a071433079
AITutors-v3 branch     : od01-r3-convergence            (NOT main)
AITutor-X   HEAD       : 77157035399830f9e7ab3f3c44341db700249fe7
Papers HEAD            : 2b92898f05f6541a5fc65c8300cb8a59a06c4928
v3 Docs/V3_SPEC tree   : 14a7450809d4932036f415d765ab29c53671843c
v3 modified tracked    : 0
Papers modified        : 0
```

**Frozen Spec SHA256 (read before and after the run — identical both times):**

| file | SHA256 |
|---|---|
| `00_Master_Spec.md` | `c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4` |
| `10_Data_Model.md` | `529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1` |
| `20_Document_Pipeline.md` | `0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c` |
| `30_Task_LLM_Safety.md` | `db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89` |
| `40_Development_Rules.md` | `8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db` |
| `50_Migration_Assets.md` | `8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7` |

**Configuration summary (non-secret; `.env` unchanged by this run):**

```text
APP_ENV            = development
LLM_GATEWAY_MODE   = live
OCR_GATEWAY_MODE   = disabled
MIMO_BASE_URL      = https://api.xiaomimimo.com/v1
MIMO_MODEL         = mimo-x-pro-preview          <-- note: see E2E-BL-03 / E2E-BL-06
DATABASE_URL       = postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors
MIMO_API_KEY       = PRESENT (value never recorded)
alembic_version    = 0011 ; public tables = 26
```

**Formal entry points used (read from source, not inferred):**

| entry | exact form | source |
|---|---|---|
| ingest | `POST /api/documents/import` (multipart `file`) | `app/api/routers/documents.py:31` |
| worker | `python -m app.worker run --allow-live` | `app/worker/__main__.py:73-74,85-100,122-125` |
| retry (replay) | `python -m app.worker retry <task_id>` | `app/worker/__main__.py:80-81,115-119` |
| API | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8077` | `app/main.py` |

`--allow-live` is the worker's **own documented human-authorization parameter**
(`app/ai/live_guard.py:11-16`: "显式授权 live external 调用（缺省拒绝，30 §6 组合放行）"), i.e. a
business parameter the formal entry requires the caller to supply — permitted by task book §4.1.
**No other state was injected:** no `task_context`, no `budget_ok`, no constructed provider,
no direct call to any internal function in place of a formal entry.

---

## §2 INPUT (task book §7)

**Selected (real, unmodified):**

```text
original file : D:\Project\Papers\maintainess\PDF\2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf
bytes         : 1 108 984
sha256        : a51ba2cc2d435c7826e5300a4e4531df06025d4030799eb27632f0d5b195bfce
type          : application/pdf ; 74 pages
producer      : kurt-wong/Aitutors-preprocessing @ 2b92898f  (local: D:\Project\Papers)
V3 commit     : d2b9a26f1a1c0297b4536b273b8999a071433079
Frozen Spec   : 6/6 SHA256 above
config        : §1
```

**Existing preprocessing products for the same document (used as the Preprocessing stage's output
evidence, because re-execution failed — see E2E-BL-06):**

| stage | path | bytes | sha256 |
|---|---|---|---|
| OCR markdown | `Papers\Ocr-markdown\高考真题\生物\2012-2021…(1).md` | 213 367 | `b1fd784ddcc6468649f6b5e5955272e4405d74a546b6827e9470fd6a477fc11d` |
| reslice manifest | `Papers\Ocr-markdown\reslice-batch-C\高考真题\生物\2012-2021…(1).manifest.json` | 33 216 | `712ca35c10423e0e22cc77fb3e780bea8b63d346795b19cc39791d098c2fff88` |

The manifest's `source_content_sha256` **equals** the `.md` sha256 above — the `.md → manifest` link
is hash-verified ✅. The `PDF → .md` link is **by filename only** (no content hash binds the PDF to
the preprocessing product) — recorded as an INFO-level provenance observation.

**Coverage against task book §7** (from the manifest: 60 units, `identity_version=2`):

| requirement | present | evidence |
|---|---|---|
| 普通题目 | YES | 60 units |
| 选择题 | YES | `original_question_type`: single_choice=11, multiple_choice=1 |
| 至少一个可能涉及 Material 的题目 | YES | **48** units declare `material_lines` |
| composite question | YES | **48** `composite_question` |
| standalone question | YES | **12** `standalone_question` |
| 图片/图形/公式 | YES | V3 Seal extracted **83** `source_figures` from the PDF |

The original input file was **not modified** (verified in §14).

---

## §3 STAGED EVIDENCE CHAIN (task book §8)

### 3.1 Stage table

| # | Stage | Input | Output | Status |
|---|---|---|---|---|
| 0 | **Original** | — | PDF, 74 pages, 1 108 984 B, sha `a51ba2cc…` | **FIXED** |
| 1 | **Preprocessing** | OCR `.md` (213 367 B, 2 865 lines) | *existing* manifest (60 units) — **re-run FAILED: HTTP 400** | **FAIL (not reproducible)** |
| 2 | **V3 Source / Ingestion** | PDF bytes via `POST /api/documents/import` | `documents` +1 (`a7fbeb3a…`), `tasks` +1 queued (`3e29c3a0…`) | **PASS** |
| 3 | **V3 Seal** | imported PDF bytes + `NativeTextProvider` | `document_source_versions` +1 (`0cf4a8c9…`): 74 pages, 2 180 lines, 68 713 chars, 83 figures | **PASS** |
| 4 | **V3 Quality Check** | `version.body_text` | `source_meta.quality = {status: valid, cjk_ratio: 0.6948, total_chars: 68713, issues: []}` | **PASS** |
| 5 | **Semantic Annotation** | `build_annotation_prompt(body_text)` → **70 711 chars** | — | **BLOCKED — GatewayDenied** |
| 6 | **Resolver / IR** | — | — | **NOT REACHED** |
| 7 | **Compiler** | — | — | **NOT REACHED** |
| 8 | **Gate** | — | — | **NOT REACHED** |
| 9 | **Admission** | — | — | **NOT REACHED** |
| 10 | **DB objects** | — | `questions` +0 · `question_instances` +0 · `materials` +0 | **FAIL (0 rows)** |
| 11 | **API** | — | no route exists for these objects | **NOT IMPLEMENTED** |
| 12 | **Frontend** | — | no page exists for these objects | **BLOCKED** |

### 3.2 Command log (verbatim; `cd AITutors-v3\backend` unless stated)

```bash
# C1 baseline / hashes / config            (08:45)  -> 00-preflight.txt
# C2 DB Before (before ANY formal task)    (08:46)  -> 01-db-before.txt
# C3 input selection + hashes              (08:48)  -> 02-input-selection.txt

# C4 preprocessing (producer, real run)    (08:48)  -> producer log + result
cd D:\Project\Papers
python scripts/reslice_pipeline.py --file "<…>.md" --out D:\Project\AITutor-X\e2e_baseline\preproc_out
#   => [FAIL] RuntimeError LLM 调用失败: HTTP Error 400: Bad Request   (0/1 files, empty out dir)

# C5 formal API up                         (08:50)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8077      -> v3-api.log

# C6 formal ingest                         (08:50:32) -> 03-v3-ingestion.txt
curl.exe -s -X POST http://127.0.0.1:8077/api/documents/import -F "file=@<original pdf>"
#   => 200 {"document_id":"a7fbeb3a-…","task_id":"3e29c3a0-…","sha256":"a51ba2cc…","is_new":true}

# C7 formal worker (PRIMARY RUN)           (08:51:42 -> 08:51:45, 2.8s)
python -m app.worker run --allow-live
#   => processed 1 task(s)

# C8 DB After + task/claim/audit           (08:52:00) -> 04-db-after-primary.txt
# C9 replay: idempotent re-import          (08:52:43) -> 05-replay.txt
curl.exe -s -X POST …/api/documents/import -F "file=@<original pdf>"
#   => 200 {"document_id":"a7fbeb3a-…","task_id":null,"is_new":false}
python -m app.worker run --allow-live     # => processed 0 task(s)

# C10 formal retry/replay entry            (08:52:58) -> 06-replay-retry.txt
python -m app.worker retry 3e29c3a0-a08b-4d37-8fb5-2d64be6f87e8   # => → queued
python -m app.worker run --allow-live                              # => processed 1 task(s)

# C11 DB After (final) + audit             (08:53:09) -> 07-db-after-final.txt
# C12 API surface + probes                 (08:53:17) -> 08-api-surface.txt
# C13 fidelity cross-check                 (08:54:10) -> 09-fidelity.txt
# C14 post-run working-tree proof          (08:54:46) -> 10-post-run-proof.txt
```

Elapsed formal-pipeline wall time (worker, primary run): **2.8 s**.

### 3.3 Per-stage detail

**(2) V3 Source / Ingestion — PASS**

```text
POST /api/documents/import   ->  HTTP 200
document_id : a7fbeb3a-f3c0-464d-86b5-2d8e5197f0ed
task_id     : 3e29c3a0-a08b-4d37-8fb5-2d64be6f87e8
sha256      : a51ba2cc2d435c7826e5300a4e4531df06025d4030799eb27632f0d5b195bfce  (== input)
file_name   : 2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf          (CJK preserved)
is_new      : true
stored at   : backend/data/imports/a51ba2cc….pdf  (1 108 984 B, byte-exact)
```

**(3)(4) V3 Seal + Quality — PASS**

```text
document_source_versions.id   : 0cf4a8c9-f67f-4edd-bd69-81c5d7e01dc7
artifact_kind / role/provider : raw_l1 / native / native
page_count / line_count       : 74 / 2180
status                        : sealed
body_hash                     : 6526b8900d17706b804cb4c6080780be3628ab9776282838b3d22cd6bee4245f
length(body_text)             : 68713
source_meta.quality           : {"issues": [], "status": "valid", "cjk_ratio": 0.6948,
                                 "total_chars": 68713, "non_printable_ratio": 0.0,
                                 "replacement_char_ratio": 0.0}
source_figures                : 83
```

**(5) Semantic Annotation — BLOCKED**

```text
prompt built : 70711 chars  (full body_text of all 74 pages embedded)
gateway      : LLMGateway(mode=live, allow_live=True, task_context=None, budget_ok=False,
                          live_provider=HTTPLLMProvider(name="ollama", model="qwen3.5-9b",
                                                        base_url="" ))
result       : GatewayDeniedError -> task status=failed, error_type=conflict
recorded     : task_claims.lease_snapshot.error_detail =
               "live denied: task context missing; budget unavailable"
outbound HTTP LLM requests : 0
```

**(10) DB objects — 0 rows produced by this round**

`questions`, `question_instances`, `materials`, `semantic_annotations`, `admission_candidates`,
`admission_events` all show **Δ = 0** across this round's formal execution (§5).

---

## §4 DATABASE BEFORE / AFTER (task book §12)

**DB Before was captured at 08:46:40, before the formal task started (import at 08:50:32).**
Full 26-table snapshot: `01-db-before.txt`. **After (final): `07-db-after-final.txt`.**

| table | Before | After | Δ | explanation |
|---|---|---|---|---|
| `documents` | 3 | **4** | **+1** | the imported 74-page PDF (`a7fbeb3a…`) |
| `document_source_versions` | 2 | **3** | **+1** | its Seal (`0cf4a8c9…`) |
| `document_source_lines` | 2 039 | **4 219** | **+2 180** | exactly that version's `line_count` |
| `document_source_spans` | 3 579 | **14 254** | **+10 675** | exactly that version's spans |
| `source_figures` | 40 | **123** | **+83** | exactly that version's figures |
| `tasks` | 10 | **11** | **+1** | the import's queued task (`3e29c3a0…`) |
| `task_claims` | 10 | **12** | **+2** | claim_round 1 (primary) + claim_round 2 (retry) |
| `llm_call_audit` | 959 | **961** | **+2** | the two annotation denial records |
| `budget` | 3 415 | **3 421** | **+6** | +5 at the primary run, +1 at the retry (claim bookkeeping) |
| `semantic_annotations` | 2 | **2** | **0** | annotation never ran |
| `admission_candidates` | 6 | **6** | **0** | compile never reached |
| `admission_events` | 1 | **1** | **0** | — |
| `questions` | 1 | **1** | **0** | **no Question produced this round** |
| `question_instances` | 1 | **1** | **0** | **no Instance produced this round** |
| `materials` | 0 | **0** | **0** | **no Material produced this round** |
| `instance_role_contents` | 2 | **2** | **0** | — |
| `validation_events` | 1 | **1** | **0** | — |
| `unit_groups` / `unit_group_members` | 1 / 1 | 1 / 1 | 0 / 0 | — |
| `material_links` / `knowledge_nodes` / `instance_figure_links` | 0 | 0 | 0 | — |

**Every change is explained.** Per-document attribution (all three source versions):

```text
a7fbeb3a…  2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf   74p  2180 lines  10675 spans   83 fig   <- THIS ROUND
bffd8c7b…  extmatrix_real_pdf.pdf                                    8p  1701 lines   3034 spans   23 fig   <- earlier round
3a64909b…  caseA_real.pdf                                            2p   338 lines    545 spans   17 fig   <- earlier round
```

> **Note on the pre-existing rows.** `questions=1`, `question_instances=1`,
> `instance_role_contents=2`, `semantic_annotations=2`, `admission_candidates=6` are **not** this
> round's output; they predate it (created 2026-09-25 16:25–16:29 by a non-formal path). They are
> reported here only because §5/§10 of the task book require inspecting the persisted objects.
> **No result of this round's formal run was derived from them**, and §12 of this report keeps the
> distinction explicit wherever they are used.
>
> The §6 task-book permission to clear the DB was **deliberately not exercised**: Before/After deltas
> already satisfy §12, and preserving the prior state avoids destroying the referents of earlier
> evidence (workspace rule: 不删除旧文档/旧代码; 不修改 Producer 数据).

---

## §5 LLM AUDIT (task book §13)

**Question: how many LLM requests were actually sent? → 0.**
**Question: how many are recorded in `llm_call_audit`? → 2.**

```text
Observed outbound LLM request count : 0
Audit row count (this task)         : 2
=> these are NOT in conflict: the audit records the ATTEMPT/DENIAL, and no request was served.
   (no unrecorded request exists; there is no silent call)
```

| field (§13) | attempt 1 | attempt 2 |
|---|---|---|
| `request_id` | `af1b8d25-e24b-41e5-91b3-3bc1fa4121a5` | `1298c3d5-f56e-4f48-859d-e8645b39e6ee` |
| `task_id` | `3e29c3a0-a08b-4d37-8fb5-2d64be6f87e8` | same |
| `document_id` | `a7fbeb3a-f3c0-464d-86b5-2d8e5197f0ed` | same |
| `stage` / `logical_execution_stage` | `ann` / `ann` | `ann` / `ann` |
| `logical_execution_hash` | `b750d3d4839d…a324f` | **identical** (deterministic) |
| `provider` / `model` | `ollama` / `qwen3.5-9b` | `ollama` / `qwen3.5-9b` |
| `status` | `failed` | `failed` |
| `error_type` (reason) | `conflict` | `conflict` |
| reason detail (from `task_claims`) | `live denied: task context missing; budget unavailable` | same |
| `prompt_chars` | 70 711 | 70 711 |
| `input_tokens` / `output_tokens` / `total_tokens` / `estimated_cost` | **NULL** (nothing served) | **NULL** |
| `start` → `end` | `00:51:45.413` → `.440` (**27 ms**) | `00:53:00.285` → `.314` (**29 ms**) |
| invocation counter (`tasks.llm_invocations`) | **0** | **0** |

**Observations (P2, see §11):**
1. The audit's `provider`/`model` (`ollama` / `qwen3.5-9b`) denote a **configured but non-functional**
   provider (`ollama_base_url` is `""`, `config.py:27-28`) and are **not** the target provider (MIMO).
   The audit therefore records a provider identity that can never serve a request.
2. A **70 711-character prompt is fully constructed before the gateway denies**. The denial is
   deterministic and precedes any network activity, so the prompt build is pure waste on this path.
3. The producer's preprocessing LLM call (§2/E2E-BL-06) is **entirely outside** V3's
   `llm_call_audit` — the two systems have separate (or no) audit trails.

---

## §6 REPLAY (task book §14)

**Required precondition check (task book §14): first run must succeed with LLM calls > 0.**
**Observed: the first formal run FAILED (annotation denied; `llm_invocations = 0`).**
**⇒ §14's precondition is NOT MET and cannot be met on the current frozen code.**

Both formal replay routes were nevertheless executed:

| route | command | result |
|---|---|---|
| idempotent re-import | `POST /api/documents/import` (same file) | **200**, `document_id` identical, `sha256` identical, **`is_new=false`**, **`task_id=null`** |
| worker re-run | `python -m app.worker run --allow-live` | **`processed 0 task(s)`** (no queued task — the failed task was not re-queued) |
| **formal retry entry** | `python -m app.worker retry 3e29c3a0…` then `run --allow-live` | re-queued → **`processed 1 task(s)`** → **failed again, identical reason** (claim_round 2) |

| §14 verification point | result |
|---|---|
| first run LLM calls > 0 | **NO (0)** — precondition unmet |
| replay LLM calls = 0 | **YES (0)** — trivially, since the gateway denies every attempt |
| replay yields same business result | **N/A** — no business result existed to reproduce |
| duplicate Question / QuestionInstance / Material | **NONE CREATED** (Δ = 0 for all three) |
| abnormal audit rows | 1 additional denial row (deterministic, same `logical_execution_hash`) |
| admission state broken | **NO** (Δ = 0 for `admission_candidates` / `admission_events`) |

**Conclusion:** ingestion idempotency is **correct and demonstrated**. Pipeline-level replay /
determinism of a *successful* run is **NOT TESTABLE** on the current frozen code, because the
formal chain cannot produce a successful run. The retry path is deterministic in its failure.

---

## §7 API VERIFICATION (task book §15)

**Full route list of the formal API (11 routes, `GET /openapi.json`, commit `d2b9a26`):**

```text
POST /api/documents/import
GET  /api/documents
GET  /api/documents/{document_id}
GET  /api/documents/{document_id}/source-quality
GET  /api/documents/{document_id}/source-lines
GET  /api/candidates/{candidate_id}
POST /api/candidates/{candidate_id}/approve
POST /api/candidates/{candidate_id}/reject
GET  /api/admin/stats
GET  /api/tasks
GET  /health
```

**Routes whose path contains `question` / `instance` / `material`: NONE.**

```text
task book section 15 (verify Question / QuestionInstance / Material through the formal API)
=> NOT IMPLEMENTED — no such endpoint exists.  [E2E-BL-05, P1]
```

Live probes (all served by the formal server):

| probe | HTTP | note |
|---|---|---|
| `/health` | 200 | `{"status":"ok"}` |
| `/api/documents` | 200 | 4 documents; the new one shows `processing_status="sealed"`, `candidate_count=0` |
| `/api/tasks` | 200 | the new task listed as `status="failed"`, `llm_invocations=0` |
| `/api/admin/stats` | 200 | `{"pending_review":5,"failed_tasks":7,"approved_today":0}` |
| `/api/candidates/{id}` | 200 | returns the pre-existing candidate in full (§9.2) |

No DB-vs-API inconsistency was found for the objects that *are* exposed: `GET /api/candidates/…`
returns exactly the stored `payload`, `build_versions`, `input_identity`, `review_trail` and
`compiled_roles`, with `compiled_roles[].text_hash` matching the stored
`instance_role_contents.text_hash` values. **The reachable API surface is consistent with the DB.**

---

## §8 FRONTEND VERIFICATION (task book §16)

Frontend exists: `AITutors-v3/frontend/` (React + TypeScript, `dist/` present).

```text
routes (frontend/src/App.tsx):
  /admin                     AdminWorkspace
  /admin/documents           DocumentList
  /admin/documents/upload    DocumentUpload
  /admin/documents/:id       DocumentReview
  /admin/candidates/:id      CandidateReview
  *                          -> /admin
```

**There is no route and no page for a Question / QuestionInstance / Material.**
The only occurrence of "question" in the frontend is a display label inside `CandidateReview.tsx`
(`question_type:`), which renders the *candidate's* `original_question_type`, not a persisted
Question object.

```text
FRONTEND E2E BLOCKED BY MISSING IMPLEMENTATION
```

**Last verified stage: API** (and, on the formal path, the last stage that produced real data was
**V3 Source / Seal + Quality**). The DB → API → Frontend chain cannot be completed for
Question / Instance / Material because neither an API endpoint nor a frontend page exists for them.
Per task book §16, **no functionality was added to work around this**. [E2E-BL-08, P1]

---

## §9 FIRST OBSERVED DEVIATION · ANSWER CORRECTNESS · MATERIAL (task book §9, §10, §11)

### 9.1 FIRST OBSERVED DEVIATION

```text
FIRST OBSERVED DEVIATION : UNRESOLVED / NOT REACHABLE
```

**Reason (no guessing).** Task book §9 requires tracing one sample that **finally entered
Question**. On the formal pipeline **no Question was produced by this round** (`questions` Δ = 0),
because the chain stops at Annotation. The only persisted Question in the database was created
2026-09-25 16:25 by a **non-formal path**, and task book §19(D) forbids inheriting that round's
finding as a formal-pipeline defect. Therefore the content-deviation question **cannot be answered
from this round's execution** and is recorded as `UNRESOLVED` rather than attributed.

What *can* be established, layer by layer, for this round:

| link | method | result |
|---|---|---|
| **Original PDF → V3 Source (Seal)** | sealed `body_text` (68 713 chars / 2 180 lines) vs an independent read-only PyMuPDF extraction of the same PDF (70 701 chars raw / 2 332 lines) | **NO DEVIATION DETECTED.** Character delta 1 988 is fully accounted for by per-line leading/trailing whitespace trimming (head comparison: PDF `" 1 / 74 "` → seal `"1 / 74"`; PDF `"…（1） "` → seal `"…（1）"`). Landmark containment agrees: 基因工程 @27/28, 限制酶 @1934/2030, 电泳 @25065/25988, 选择题 @37/39. |
| **V3 Source → Annotation** | — | **BLOCKED** (this is the *blocking point*, not a data deviation) |
| **Original PDF → Preprocessing** | producer pipeline re-execution | **UNRESOLVED** — the pipeline fails before producing output (HTTP 400, E2E-BL-06), so the pre-existing `.md` (101 350 chars, a **restructured markdown** product) cannot be reproduced or verified against the PDF this round. |

### 9.2 Answer correctness (`complete` / `source_located` / `verified_correct`) — §10

The formal run produced no Question. The task book's §10 scenario was therefore examined on the
**only persisted Question** in the database, and on the **production code that writes it**.
Basis is stated explicitly (code at `d2b9a26` + production data + formal API), so this is **not**
an inheritance of the previous round's report.

**Persisted values (as returned by the formal API `GET /api/candidates/{id}` and read from the DB):**

```text
candidate payload  .payload.answer[0] = {"text":"11. ", "span_id":"sp-Q11.answer", "unit_id":"Q11",
                                         "complete":true, "source_located":true,
                                         "verified_correct":null, "question_number":"11"}
DB instance_role_contents(role=answer) = text "11. " (length 5)
                                         answer_status = {"complete": true,
                                                          "source_located": true,
                                                          "verified_correct": true}
```

**Content check (task book §10):**

| §10 question | answer |
|---|---|
| answer 是否真的存在 | The role exists, but its text is `"11. "` — the **question number**, not an answer value |
| answer 是否完整 | **NO** — 5 characters, no answer content |
| answer 是否与原始文档一致 | Source span `P6L031` resolves, but the located text contains no answer |
| source_located 是否指向真实位置 | YES — `line_refs:["P6L031"]`, `start_offset 0 / end_offset 5`, `resolution_status: exact` |
| verified_correct 是否有实际证据 | **NO evidence in content** |

```text
ASSERTION / CONTENT mismatch   [E2E-BL-01, P0]
```

**Root cause located in production source (`d2b9a26`):**

- `app/domains/compile/compiler.py:130` —
  `complete=bool(cr.text.strip()), verified_correct=None`.
  So `complete` means **"the compiled text is non-empty"**, not "the answer is complete". For an
  answer role whose located text is the fragment `"11. "`, `bool("11.".strip())` is `True`
  ⇒ **`complete=true` is asserted without content support**.
- `app/domains/gate/admission.py:423-429` — materialization writes
  `answer_status = {"source_located": ans["source_located"], "complete": ans["complete"],
  "verified_correct": True}`, with the in-code rationale
  *"approved 必经 auto 或人工确认（20 §8.3）；payload 冻结 verified 保持原值，物化侧以 approved 语义置 true"*.
  ⇒ `verified_correct` transitions **`null` (candidate payload) → `true` (materialized instance)**
  purely because the candidate was approved — **independent of content**.

**Consequences.** A Question whose answer role contains **no answer value** carries
`answer_status = {complete: true, source_located: true, verified_correct: true}`. Any consumer that
trusts `verified_correct` (including `gate/policy.py:282`, which admits leaves on the reason
`"strict-auto: all answers verified_correct=true"`) is reading an approval signal as a
content-verification signal. Whether "approval ⇒ verified_correct" is the intended reading of
`20 §8.3` is a **spec-interpretation question for the Owner** — this report records the
assertion/content mismatch as required by §10 and does **not** modify any code.

### 9.3 Material (`task book §11`) — NOT REACHABLE in V3

| §11 checkpoint | result |
|---|---|
| Material exists (in the selected input) | **YES, producer side** — 48 of 60 units declare `material_lines` |
| Material reaches V3 semantic representation | **NO** — the production annotation prompt has no `shared_material` role (E2E-BL-04); Annotation never ran |
| Material persisted (`materials`) | **NO** — Δ = 0 |
| Question references Material | **NOT REACHED** |
| API returns Material | **NOT IMPLEMENTED** — no route |
| Frontend displays Material | **BLOCKED** — no page |

```text
MATERIAL E2E: NOT REACHABLE ON THE FORMAL PIPELINE
(blocked twice over: Annotation is denied, and the prompt could not express shared_material even if it ran)
```

---

## §10 FINDINGS (task book §20 — new E2E finding series)

Classification: **P0** = formal business-chain error producing wrong final business data;
**P1** = key formal capability cannot complete (no final-data error proven);
**P2** = test / audit / log / statistics / reporting issue; **INFO** = observation only.

### P0

**E2E-BL-01 — `answer_status` asserts completeness and correctness that the content does not support**

```text
Severity  : P0  (final business data is wrong: a persisted answer-status triple that the payload
                 does not claim and the content cannot justify)
Evidence  : code  app/domains/compile/compiler.py:130        complete = bool(text.strip())
                  app/domains/gate/admission.py:423-429      verified_correct := True (hardcoded)
            data  instance_role_contents.answer_status = {complete:true, source_located:true, verified_correct:true}
                  with text "11. " (length 5, no answer value)
            api   GET /api/candidates/{id} -> payload.answer[0].verified_correct = null
Basis note: the persisted row predates this round (this round's formal run produced no Question).
            The finding is established from PRODUCTION SOURCE at d2b9a26 plus production data/API,
            NOT inherited from any previous round's report (task book §19D respected).
Impact    : any consumer trusting verified_correct reads an approval flag as content verification;
            gate/policy.py:282 admits leaves on the reason "strict-auto: all answers verified_correct=true".
Spec note : the in-code rationale cites 20 §8.3 ("approved 语义置 true"). Whether that is the
            correct reading of 20 §8.3 is an OWNER/SPEC question — not decided here.
Fix policy: NOT FIXED (task book §17: baseline first; §23: no fix-while-testing).
```

### P1

**E2E-BL-02 — the formal live-LLM path is structurally unreachable (reproduced on the formal entry)**

```text
Evidence : app/worker/__main__.py:87   build_gateway(allow_live=args.allow_live)
                                          -> task_context=None, budget_ok=False (factory defaults)
           app/ai/gateway.py:64-74     _live requires allow_live AND task_context is not None
                                          AND budget_ok AND a resolvable live provider
           runtime                     GatewayDeniedError: "live denied: task context missing;
                                          budget unavailable"  (2/2 attempts, deterministic)
           DB                          tasks.status=failed, llm_invocations=0, 0 outbound requests
Impact   : the formal Worker -> TaskExecutor -> Gateway -> LLM path can never annotate, so
           Question / QuestionInstance / Material can never be materialized by the formal pipeline.
Cross-ref: independently consistent with the previous round's BLOCKER-02, but established here
           WITHOUT any harness or injected state.
Fix policy: NOT FIXED — requires changing app/worker or app/ai/gateway (production code).
```

**E2E-BL-03 — the formal V3 provider is not MIMO (task book §5 requires this be recorded separately)**

```text
Evidence : app/ai/gateway.py:116-122   live branch constructs HTTPLLMProvider(name="ollama",
                                          api_key=None, base_url=settings.ollama_base_url,
                                          model=settings.ollama_model)
           app/core/config.py:27-28    ollama_base_url = "" ; ollama_model = ""  (empty)
           app/core/config.py:47-50    mimo_api_key / mimo_base_url / mimo_model / mimo_vl_model
                                          ARE defined but are NEVER read by build_gateway
           .env                        MIMO_MODEL=mimo-x-pro-preview ; MIMO_BASE_URL=https://api.xiaomimimo.com/v1
           llm_call_audit              provider=ollama / model=qwen3.5-9b
Impact   : "the formal V3 provider is not the target MIMO provider" — recorded as a distinct
           finding per task book §5. No attempt was made to fake a MIMO formal chain, and the
           provider architecture was NOT bypassed or temporarily modified.
```

**E2E-BL-04 — the production annotation prompt cannot express `composite_unit` / `shared_material`**

```text
Evidence : app/domains/task/executor.py:58-104  _ANNOTATION_PROMPT_PREFIX
             :71  only a "standalone_unit" example is given
             :86  unit_type in {"standalone_unit","composite_unit"}   (value allowed, no structure)
             :88  role in {"stem","option","answer","explanation"}    <-- shared_material ABSENT
             no shared_components / sub_questions / depends_on / question_number_range anywhere
Frozen Spec : 20_Document_Pipeline.md:130  role:"shared_material"
              :181-185  composite_unit + question_number_range + shared_components{} +
                        sub_questions[] + depends_on[{type:"material_dependency"}] +
                        requires_material_context
              :378-390  IR composite unit + invariants ("共享材料只出现一次" @391)
              :462      "shared material 只输出一次，绝不复制进任何子题 stem"
              :483      "每个 shared material 单独产一个 material dedup_key"
Impact   : composite / shared-material semantics defined by the Frozen Spec can never be produced
           by the formal annotation path => materials is structurally always 0 on that path, and
           task book §7's "at least one composite question" requirement can never reach Material
           persistence.
Fix policy: NOT FIXED — V3 production code.
```

**E2E-BL-05 — no formal API can return Question / QuestionInstance / Material**

```text
Evidence : GET /openapi.json -> 11 routes; none contains question | instance | material
Impact   : task book §15 is NOT IMPLEMENTED. Consumers (including any frontend) cannot read the
           final objects through the formal API even when they exist.
```

**E2E-BL-06 — the producer preprocessing pipeline cannot execute (stale model name)**

```text
Evidence : command  cd D:\Project\Papers
                    python scripts/reslice_pipeline.py --file "<…>.md" --out <evidence>\preproc_out
           output   [1/1] …md : 2865 行, prompt 127012 字
                    [FAIL] RuntimeError LLM 调用失败: HTTP Error 400: Bad Request
                    ===== 完成：0/1 无校验问题 =====
           config   Papers\data\.llm_config : provider=xiaomi MIMO,
                    base_url=https://api.xiaomimimo.com/v1, model=mimo-x-pro-preview
           artifact Papers\logs\reslice_preproc_out_log.txt ; Papers\data\reslice_preproc_out_result.json
Impact   : preprocessing is NOT reproducible in the current environment; the Original -> Preprocessing
           link cannot be verified; the only available preprocessing products are pre-existing.
Note     : the same stale model name appears in AITutors-v3's .env (E2E-BL-03) — the two repos share
           the failure mode independently.
```

**E2E-BL-07 — the chain drawn in task book §3 is not connected (Preprocessing -> V3)**

```text
Evidence : producer output  = *.md + *.manifest.json
           V3 formal ingest = app/domains/source/import_service.py:26
                              _ALLOWED_EXTENSIONS = {".pdf", ".docx"}
           => no formal path carries a preprocessing product into V3. The V3 formal pipeline
              re-derives everything itself (PyMuPDF seal) from the ORIGINAL PDF.
Impact   : "Preprocessing -> V3 Source" as drawn in task book §3 does not exist as a pipeline edge.
           The two subsystems must be executed and verified as two disjoint branches against the
           same original document (which is what §2/§3 of this report do).
```

**E2E-BL-08 — the frontend cannot display final Questions (task book §16)**

```text
Evidence : frontend/src/App.tsx routes = /admin, /admin/documents, /admin/documents/upload,
           /admin/documents/:id, /admin/candidates/:id   (no question/material route)
Impact   : FRONTEND E2E BLOCKED BY MISSING IMPLEMENTATION. Last verified stage: API.
           No frontend functionality was added to work around this (§16 respected).
```

### P2

**E2E-BL-09 — the LLM audit records denials whose `provider`/`model` can never serve**

```text
Evidence : 2 llm_call_audit rows for this task, provider=ollama, model=qwen3.5-9b,
           status=failed, error_type=conflict, all token/cost columns NULL.
           ollama_base_url is "" => the audited provider identity is non-functional and is not
           the target provider (MIMO).
Impact   : audit "Runtime Truth" for the annotation stage does not identify the provider that
           would actually serve a request; provider identity in the audit is a configuration
           artifact rather than a runtime fact.
Also     : the producer's preprocessing LLM call is not covered by any V3 audit (§5).
```

**E2E-BL-10 — an unwritable import store surfaces as HTTP 500 (unhandled OS error)**

```text
Evidence : POST /api/documents/import  -> HTTP 500
           traceback: app/domains/source/import_service.py:72  file_path.write_bytes(file_bytes)
                      PermissionError: [Errno 13] ... 'data\imports\<sha>.pdf'
                    -> escaped to the ASGI layer
Caveat   : the trigger in this run was the EXECUTOR's own file sandbox (the v3 tree was not
           writable), NOT a V3 defect. The code-level observation stands on its own: an OS-level
           write failure is not mapped to a controlled domain error and becomes an opaque 500.
           After granting the executor write access, the identical request returned 200.
```

### INFO

- **E2E-BL-11** — Seal fidelity: the sealed `body_text` (68 713 chars / 2 180 lines) equals an
  independent PyMuPDF extraction with per-line whitespace trimming (70 701 chars raw). No text
  deviation detected at the V3 Source stage.
- **E2E-BL-12** — `line_count` (2 180) exactly equals the newline count implied by
  `length(body_text)` (68 713) — internally consistent.
- **E2E-BL-13** — the only in-repo caller that supplies the live preconditions is a **dev smoke
  script**: `backend/scripts/live_smoke_ollama.py:138`
  `build_gateway(allow_live=True, task_context="smoke", budget_ok=True)` — literal placeholder
  values, and it targets Ollama. It is not the production entry and was not used.
- **E2E-BL-14** — the producer pipeline writes its own run accounting into the producer repo
  (`Papers/logs/…`, `Papers/data/…`). No producer *data* was modified (0 modified tracked files).
- **E2E-BL-15** — the `PDF → .md → manifest` chain is hash-verified only at the `.md → manifest`
  step; the `PDF → .md` step is linked by filename alone. Producers of the "same sample" evidence
  must therefore not assume hash-equality across that edge.
- **E2E-BL-16** — task book §19(D): no previous round's EV/EE finding is carried forward as a formal
  pipeline defect. Where a persisted object created by a non-formal path was inspected (§9.2), the
  basis is stated explicitly and the finding is grounded in production source at `d2b9a26`.

---

## §11 ANSWERS TO TASK BOOK §19

### A. 管线是否真正走通？

```text
BLOCKED
Last successful stage : V3 SOURCE (Seal + Quality Check) — real outputs written to the database
First blocked stage   : SEMANTIC ANNOTATION — LLMGateway denies the live call
```

### B. 每个阶段状态

| 阶段 | 状态 | 输入 | 输出 | 是否发现异常 | 首次异常 |
|---|---|---|---|---|---|
| Original | **FIXED** | — | 74-page PDF, sha `a51ba2cc…` | 否 | — |
| Preprocessing | **FAIL** | OCR `.md` 213 367 B / 2 865 lines | none (re-run: HTTP 400); existing manifest used as evidence | **是** | **producer LLM call (HTTP 400)** |
| V3 Source | **PASS** | PDF bytes (formal API) | `documents` +1, `tasks` +1 | 否 | — |
| Annotation | **BLOCKED** | prompt 70 711 chars | none | **是** | **GatewayDenied ("task context missing; budget unavailable")** |
| Resolver | **NOT REACHED** | — | — | — | — |
| Compiler / Admission | **NOT REACHED** | — | — | — | — |
| DB | **PASS (for what ran)** | Seal output | 2 180 lines / 10 675 spans / 83 figures | 否 | — |
| API | **PARTIAL** | — | 11 routes; **no** question/instance/material route | **是** | **route absent** |
| Frontend | **BLOCKED** | — | **no** question/material page | **是** | **page absent** |

### C. 如果出现最终数据错误，错误第一次出现在哪里？

```text
No final data error is reachable on the formal pipeline: this round produced NO Question,
NO QuestionInstance and NO Material, so there is no formal-pipeline final object to be wrong.
FIRST BLOCKING POINT (formal chain)         : SEMANTIC ANNOTATION (LLMGateway denial)
FIRST OBSERVED DEVIATION (content tracing)  : UNRESOLVED / NOT REACHABLE
```

One content-level defect **is** established, but at the code level rather than by this round's
execution, and it is not attributed to preprocessing or to any other stage by guesswork:
`answer_status.verified_correct` is hardcoded `True` at materialization
(`admission.py:428`) and `complete` reduces to `bool(text.strip())` (`compiler.py:130`), so a
Question with no answer content can carry `{complete: true, source_located: true,
verified_correct: true}` (**E2E-BL-01**). The stage where that occurs is precisely
**Compiler (`complete`) + Admission (`verified_correct`)**, not Source and not Preprocessing.

### D. 正式管线与上一轮测试的区别

| | previous round (2026-09-26 00:03–00:36) | this round (08:45–08:55) |
|---|---|---|
| entry | custom harness `e2e_run/e2e_live_full_chain.py` building its own `LLMGateway` | **formal** `POST /api/documents/import` + `python -m app.worker run --allow-live` |
| live preconditions | **self-supplied**: `allow_live=True`, `task_context=object()`, `budget_ok=True` | **only `--allow-live`** (the worker's own flag); `task_context`/`budget_ok` left to the production code — which never supplies them |
| LLM provider | MIMO `mimo-v2.6-pro` via an injected provider (**real external calls were made**) | **none** (gateway denied; 0 outbound requests) |
| path actually exercised | injected-provider path: annotation → compile → gate → admission → HTTP approve → Question | production path: import → seal → quality → **denial** |
| result | `questions=1`, `question_instances=1`, `materials=0` (harness-driven) | `questions=0`, `question_instances=0`, `materials=0` (formal) |

**Comparable:** the Seal/Quality behaviour, the ingestion API, the ingestion idempotency semantics,
and the existence (or absence) of API/frontend surface for the final objects.

**NOT comparable:** anything downstream of Annotation. The previous round's `questions=1` proves that
*some* code path can materialize an object; it does **not** prove the formal pipeline can, and this
round shows that with production wiring it does not even reach annotation. Conversely, this round's
`questions=0` must **not** be read as evidence that materialization is broken — it is blocked
upstream at the gateway. The two results answer different questions and neither inherits the other.

---

## §12 TASK BOOK §21 — TEN SEPARATE DIMENSIONS

```text
1.  Formal Pipeline Execution        : BLOCKED (V3 Source is the last successful stage)
2.  Data Correctness                 : NOT ESTABLISHED this round (no final object produced);
                                       one code-level assertion/content defect identified (E2E-BL-01)
3.  LLM Authorization Correctness    : FAIL — the formal path cannot obtain live authorization
                                       (task_context/budget_ok never supplied); NOT bypassed, NOT faked
4.  Audit Correctness                : PASS with a P2 qualification — attempts are recorded,
                                       no unrecorded request exists; but the recorded provider/model
                                       (ollama/qwen3.5-9b, empty base_url) cannot serve and is not MIMO
5.  Replay Correctness               : ingestion idempotency PASS (is_new=false, same id, task_id=null);
                                       pipeline replay NOT TESTABLE (no successful first run);
                                       retry path deterministic; NO duplicates created
6.  DB Persistence Correctness       : PASS for what was produced — every delta explained and
                                       attributed; 2 180 lines / 10 675 spans / 83 figures / 0 orphans implied
7.  API Correctness                  : PARTIAL — 11 routes behave correctly and are DB-consistent,
                                       but NOTHING exposes Question/QuestionInstance/Material (P1)
8.  Frontend Correctness             : BLOCKED BY MISSING IMPLEMENTATION (no question/material page)
9.  First Blocking Point             : SEMANTIC ANNOTATION — LLMGateway live denial
10. Integration Readiness            : NO
```

No single "E2E PASS" is claimed for any of these.

---

## §13 NOT-MODIFIED PROOF (task book §18, §22, §23)

```text
captured_at : 2026-09-26T08:54:46+08:00   (after the run)

AITutors-v3  HEAD d2b9a26f…3079 unchanged ; branch od01-r3-convergence unchanged
             Docs/V3_SPEC tree 14a7450809…843c unchanged
             modified tracked files = 0
             untracked entries = 10  (IDENTICAL set to preflight — no new file in the repo)
Papers       HEAD 2b92898f…4928 unchanged ; modified tracked files = 0
             new untracked = logs/reslice_preproc_out_log.txt
                             data/reslice_preproc_out_result.json
             (the producer pipeline's own run-accounting, by its design; no producer data modified)
AITutor-X    HEAD 77157035399…9fe7 unchanged (this report and e2e_baseline/ are new, uncommitted)
Frozen Spec  6/6 SHA256 identical before and after
```

- **Frozen Spec not modified** (§18). No implementation defect was "resolved" by changing the spec.
- **No fix applied** (§17). Findings are reported, not repaired; the failure scene was preserved.
- **No injected production state** (§4.1/§23): no `allow_live=True` construction in code, no
  `budget_ok`, no `task_context`, no bypass of Worker / TaskExecutor / Gateway, no internal
  function used in place of a formal entry.
- **Temporary artefacts are clearly distinguished** from code changes: all evidence lives under
  `AITutor-X\e2e_baseline\`; the only writes into the subject repo are the runtime import store
  (`backend/data/imports/a51ba2cc….pdf`, gitignored) and into the producer repo the two
  run-accounting files listed above.

---

## §14 TASK BOOK §24 — COMPLETION CHECKLIST

```text
[x] 原始输入已固定                        74-page PDF, sha256 a51ba2cc…, unmodified
[~] preprocessing 真实执行并保存证据       EXECUTED and FAILED (HTTP 400); log+result preserved;
                                          existing manifest used as the stage's output evidence
[x] V3 正式入口真实执行                   POST /api/documents/import (200) + worker (2 runs)
[x] Worker / TaskExecutor / Gateway 正式路径已验证
                                          import -> TaskExecutor stages -> Gateway -> DENIED (recorded)
[x] LLM provider 已明确                   formal: ollama/qwen3.5-9b (empty base_url);
                                          target: MIMO — MISMATCH recorded as E2E-BL-03
[x] 每个关键阶段均有输入/输出证据          §3 (12 stages, 10 evidence files)
[x] DB Before / After 完整                §4 (26 tables, every delta explained; Before taken pre-task)
[x] LLM audit 已核对                      §5 (0 requests vs 2 audit rows, reconciled)
[~] Question / Instance / Material 已核对 0 produced by the formal run; the only persisted
                                          Question audited under §9.2 with explicit basis
[x] Replay 已验证                         §6 (ingestion idempotent; retry deterministic; no duplicates;
                                          pipeline replay NOT TESTABLE — precondition unmet)
[x] API 已验证                            §7 (11 routes; question/material NOT IMPLEMENTED)
[x] Frontend 已验证或明确说明当前阻塞      §8 — FRONTEND E2E BLOCKED BY MISSING IMPLEMENTATION
[x] FIRST OBSERVED DEVIATION 已定位        §9 — UNRESOLVED / NOT REACHABLE, with the reason and with
                                          the one code-level defect localized to Compiler+Admission
[x] 每个 finding 均有证据                 §10 (16 findings, each with command/code/DB/API evidence)
[x] Frozen Spec 未被测试过程修改            §13 (6/6 SHA256 identical)
[x] 未把上一轮测试结果直接当成正式管线结论  §11(D), E2E-BL-16
```

---

## §15 EVIDENCE INDEX & THIRD-PARTY REPRODUCTION

All paths relative to `D:\Project\AITutor-X\e2e_baseline\` unless absolute.

| file | content |
|---|---|
| `00-preflight.txt` | git baseline, Frozen Spec SHA256, config summary, formal entry points |
| `01-db-before.txt` | 26-table DB Before snapshot (taken 08:46:40, **before** the formal task) |
| `02-input-selection.txt` | input path/size/sha256, preprocessing products, §7 coverage |
| `03-v3-ingestion.txt` | formal import request/response, HTTP 200, note on the sandbox-induced 500 |
| `04-db-after-primary.txt` | DB After (primary run), task row, claim, audit rows, new source version |
| `05-replay.txt` | idempotent re-import (is_new=false) and `processed 0 task(s)` |
| `06-replay-retry.txt` | formal `retry` + re-run, claim_round 2, identical denial |
| `07-db-after-final.txt` | final 26-table DB After + all this-round audit rows |
| `08-api-surface.txt` | 11 routes; no question/instance/material route |
| `09-fidelity.txt` | Seal vs producer `.md` vs PDF landmark/char comparison |
| `v3_body_text.txt` | the sealed `body_text` streamed out of the DB (fidelity source data) |
| `v3-api.log` | uvicorn log for the formal API server |
| `_fid.py`, `_fid2.py` | read-only fidelity measurement scripts |
| `preproc_out/` | producer output dir (empty — the run failed before writing) |
| `D:\Project\Papers\logs\reslice_preproc_out_log.txt` | producer's own run log (FAIL, HTTP 400) |
| `D:\Project\Papers\data\reslice_preproc_out_result.json` | producer's own run result (error record) |

**Third-party reproduction — what was run, when, with which commit, input and path:**

```text
when        : 2026-09-26 08:45–08:55 (+08:00)
commit      : AITutors-v3 d2b9a26f1a1c0297b4536b273b8999a071433079 (@ od01-r3-convergence)
input       : D:\Project\Papers\maintainess\PDF\2012-2021高考真题生物汇编：基因工程（1）（教师版）(1).pdf
              sha256 a51ba2cc2d435c7826e5300a4e4531df06025d4030799eb27632f0d5b195bfce
path        : POST /api/documents/import  ->  python -m app.worker run --allow-live
              (then: idempotent re-import; python -m app.worker retry <task>; run --allow-live again)
produced    : documents +1 · document_source_versions +1 · lines +2180 · spans +10675 · figures +83
              tasks +1 · task_claims +2 · llm_call_audit +2 · budget +6
              questions 0 · question_instances 0 · materials 0
first deviation : UNRESOLVED (no formal Question); first blocking point = Annotation
```

---

## §16 RECOMMENDED NEXT STEPS (proposals only — no fix applied, task book §17)

Ordered by what unblocks the most, **without** deciding architecture on the Owner's behalf:

1. **Decide whether the formal worker is allowed to obtain live authorization.**
   Either the production entry must supply `task_context` / `budget_ok` from real task/budget state,
   or the live path must be declared out of scope for the formal pipeline. Until then, no formal
   run can pass Annotation, and every downstream stage stays unverifiable
   (E2E-BL-02). *This is the single change that unblocks §3–§16 of the chain.*
2. **Connect the formal V3 gateway to MIMO** (or declare Ollama the target) and make the configured
   model name valid — `mimo-x-pro-preview` is rejected by the endpoint in both repos
   (E2E-BL-03, E2E-BL-06).
3. **Implement the composite / shared-material branch of the annotation prompt** so the Frozen
   Spec's composite semantics can be produced at all (E2E-BL-04).
4. **Add read endpoints for Question / QuestionInstance / Material**, and a frontend page that
   consumes them — otherwise §15/§16 can never pass even after (1)–(3) (E2E-BL-05, E2E-BL-08).
5. **Resolve the `answer_status` semantics**: decide whether "approved ⇒ `verified_correct=true`"
   is the intended reading of `20 §8.3`, and whether `complete` may be derived from
   `bool(text.strip())` (E2E-BL-01). If the intent is approval-semantics, the field name is
   misleading to every consumer; if the intent is content-verification, the assignment is wrong.
6. **Decide how (or whether) preprocessing output should reach V3** — today the two are disjoint
   branches joined only by the original document (E2E-BL-07).
7. **Map OS-level import-store failures to a controlled error** instead of a bare HTTP 500
   (E2E-BL-10).
8. **Make the audit's provider identity a runtime fact** rather than a configuration echo
   (E2E-BL-09).

---

*End of formal E2E baseline verification report. Baseline first; evidence; analysis; fix proposal —
no fix was applied and no failure scene was overwritten.*
