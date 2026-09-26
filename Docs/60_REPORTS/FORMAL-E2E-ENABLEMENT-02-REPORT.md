# FORMAL-E2E-ENABLEMENT-02-REPORT

```text
Document ID   : FORMAL-E2E-ENABLEMENT-02-REPORT
Task ID       : FORMAL-E2E-ENABLEMENT-02
Document Type : Implementation + Verification Evidence Report
Date          : 2026-09-26
Executor      : MIMO CODE (smallest change; no Frozen Spec change; no architecture expansion)
Authority     : Owner task book "Production Pipeline E2E v2 — Evidence Chain Completion"
AITutors-v3   : d0a67da (base) + working tree changes (this task)
Papers        : 1662121 (base) + test assertion update (this task)
AITutor-X     : evidence + this report
E2E_RUN_ID    : E2E2-20260926T121829
DATABASE_MODE : fresh_test
Peak-time     : 2026-09-26 12:18 Beijing — workday 08:00-12:00 just ended;
                MIMO only used. No DeepSeek calls in this run.
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env.
```

---

## 0. 结果速览

```text
PASS 条件对照
  1. Formal worker/API path executed              YES
  2. No manually injected task_context            YES
  3. No hardcoded budget approval                 YES
  4. Actual provider/model traceable              YES (from API response body)
  5. preprocessing model config unified           YES (active defaults)
  6. E2E evidence reproducible                    YES (E2E_RUN_ID + DATABASE_MODE)

OUTCOME: FORMAL PIPELINE E2E PATH VERIFIED
         + FIRST BLOCKING POINT IDENTIFIED WITH REAL EVIDENCE
```

---

## 1. FACT（实测事实）

### 1.1 Formal entries actually executed

| Step | Command / call | Result |
|---|---|---|
| Fresh DB | `TRUNCATE ... CASCADE` (25 tables, excluding `alembic_version`) | recorded in evidence `db_reset` |
| Ingest | `POST http://127.0.0.1:8077/api/documents/import` | HTTP **200** |
| Worker | `python -m app.worker run --allow-live` | **exit_code=0** |

Import response:

```json
{
  "document_id": "5a5ca3bf-097c-4b91-88ac-748a658ccfe5",
  "task_id": "5a521864-6402-4ffa-884d-5f61e80868e4",
  "sha256": "311a567eb928481333c6e97e749f237cb9250e3c94cffa88ea43db681efebbe3",
  "file_name": "2018北京一零一中高一分班考物理（教师版）(1).pdf",
  "is_new": true
}
```

Worker log (`e2e_run/formal-e2e-v2-worker-E2E2-20260926T121829.log`):

```text
$ C:\...\python.exe -m app.worker run --allow-live
exit_code=0
provider reality evidence: provider_reality.json
processed 1 task(s)
```

### 1.2 Task / claim / authorization

```text
task_id     : 5a521864-6402-4ffa-884d-5f61e80868e4
claim_id    : 5646f2f8-9b46-435a-955a-07fe9d5e23b6
claim_round : 1
outcome     : failed
error_type  : validation_error
error_detail: LLM response not valid JSON: Expecting ',' delimiter: line 1 column 9898 (char 9897)
```

Authorization path (no injection):

```text
Worker CLI --allow-live
  → build_gateway(allow_live=args.allow_live)   # no task_context, no budget_ok
  → TaskExecutor._authorize_live_from_real_context(real Task row)
       → BudgetService.ensure(task_ref)
       → BudgetService.check([task_ref])        # fail-closed; default is False
       → gateway.authorize(task_context=real_task_dict, budget_ok=check_result)
```

`LLMGateway.authorize()` default `budget_ok=False`（Issue-03 取消 fail-open）。
`task_context=None` → `GatewayDeniedError`（已有测试 `test_authorize_rejects_none_context`）。

### 1.3 LLM audit + Provider Reality（Issue-02）

`llm_call_audit`（request_id `6123430d-f1db-4989-a2a1-68eeac4cd4f0`）:

```text
provider      = mimo
model         = mimo-v2.6-pro          # configured (local)
status        = completed
input_tokens  = 8607                   # from API response usage
output_tokens = 4510
total_tokens  = 13117
start         = 2026-09-26T04:18:33Z
```

Provider reality record（`provider_reality.json`）:

```json
{
  "configured_provider": "mimo",
  "configured_model": "mimo-v2.6-pro",
  "actual_provider": "mimo",
  "actual_model": "mimo-v2.6-pro",
  "execution_status": "completed",
  "actual_usage": {
    "prompt_tokens": 8607,
    "completion_tokens": 4510,
    "total_tokens": 13117,
    "completion_tokens_details": {"reasoning_tokens": 1323},
    "prompt_tokens_details": {"cached_tokens": 8576}
  }
}
```

**actual_model 来源** = HTTP response body `data["model"]`（`HTTPLLMProvider.last_response_model`），  
**不是** config 回填。usage 同样来自 response body，写入 audit 既有 token 列。

### 1.4 Source / final objects

```text
document_id   : 5a5ca3bf-097c-4b91-88ac-748a658ccfe5
sha256        : 311a567eb928481333c6e97e749f237cb9250e3c94cffa88ea43db681efebbe3
source_figures: 16
source_spans  : 855
questions     : 0
instances     : 0
materials     : 0
candidates    : 0
annotations   : 0
```

### 1.5 Preprocessing model config（Issue-04）

| Location | Before | After |
|---|---|---|
| `AITutors-v3/backend/scripts/step0_blind_test.py` default | `mimo-x-pro-preview` | `mimo-v2.6-pro` |
| `Papers/tests/test_no_config_import.py` assert | expects legacy tag | expects `mimo-v2.6-pro` |
| `Papers/scripts/reslice_pipeline.py` DEFAULT_MODEL | already `mimo-v2.6-pro` | unchanged |
| `llm_provider.py` / `gateway.py` | LEGACY reject-list only | unchanged (correct) |

历史产物（manifests / audit json / 历史锚点脚本）**保留未改**（任务允许）。

### 1.6 Frozen Spec integrity

```text
00_Master_Spec.md        c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4
20_Document_Pipeline.md  0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c
```

与 ENABLEMENT-01 报告一致 — **未修改**。

---

## 2. OBSERVATION（观察）

1. **正式链路已可复核**：API HTTP 状态码、worker CLI exit code、task id、claim id、gateway 放行（隐含于 LLM 调用发生）、llm_call_audit 行、provider_reality 记录 — 六段证据同 run_id 可对齐。
2. **tokens 已非空**：8607/4510/13117 来自 MIMO response usage；ENABLEMENT-01 中 token 为 NULL 的缺口已补。
3. **actual_model 有真实来源**：response `model` 字段；与 configured 相等是因为服务端确实返回 `mimo-v2.6-pro`，不是伪相等。
4. **budget 不再 fail-open**：`authorize()` 默认 `budget_ok=False`；`BudgetService.check()` 缺账户/无余量返回 False。单测覆盖：`test_budget_check_missing_account_unavailable` 等 4 条全绿。
5. **Annotation 校验 fail-loud**：LLM JSON 在 char 9897 处非法 → `validation_error` → 不落 invalid artifact（符合 H0-15 方案 B）。

---

## 3. LIMITATION（限制）

1. 本轮 **未** 修改 Resolver / IR / Admission 业务语义（任务禁止）。
2. **未** 实现完整计费；仅有 `BudgetService.check()` 可失败探针。
3. **未** 对 LLM JSON 解析失败做自动重试（20 §4.7 的 Annotation 聚焦重试未接线 — 架构扩展，超范围）。
4. historical corpus 中的 `mimo-x-pro-preview` 字符串保留（历史报告/fixture 语义）。
5. 单次 run 的 JSON 解析失败具有随机性；不能据此断言模型稳定失败。

---

## 4. CONCLUSION（结论）

### 4.1 验收对照

| # | PASS 条件 | 结论 |
|---|---|---|
| 1 | Formal worker/API path executed | **满足** — `POST /api/documents/import` + `python -m app.worker run --allow-live` |
| 2 | No manually injected task_context | **满足** — context 来自 DB claimed Task |
| 3 | No hardcoded budget approval | **满足** — `check()` 决定 `budget_ok`；默认 False |
| 4 | Actual provider/model traceable | **满足** — response body `model` + usage |
| 5 | preprocessing model config unified | **满足** — 活跃默认均为 `mimo-v2.6-pro` |
| 6 | E2E evidence reproducible | **满足** — `E2E_RUN_ID=E2E2-20260926T121829` / `DATABASE_MODE=fresh_test` |

### 4.2 FIRST BLOCKING POINT（真实证据，不推测后续）

```text
Stage         : Semantic Annotation (JSON parse)
Error         : LLM response not valid JSON: Expecting ',' delimiter: line 1 column 9898 (char 9897)
Source        : app/domains/annotation/service.py (json.loads)
Error type    : validation_error (task claim)
Effect        : no semantic_annotation artifact → Resolver/Compiler/Admission NOT REACHED
Evidence      : task_claims.lease_snapshot.error_detail
                llm_call_audit status=completed (provider call itself succeeded)
Action        : RECORD ONLY — 不隐藏、不静默修复
```

**说明**：Provider 调用本身成功（audit=completed，tokens 齐全）；失败发生在 **响应 JSON 结构** 校验。  
这与 ENABLEMENT-01 的 IR incomplete 是不同阶段的阻塞（前者在 Resolver/IR，本轮在 Annotation 解析）。

### 4.3 任务结束定义

```text
达到：FORMAL PIPELINE E2E PATH VERIFIED
      + FIRST BLOCKING POINT IDENTIFIED WITH REAL EVIDENCE
未声称：FULL PRODUCT COMPLETE
```

---

## 5. Code changes

### AITutors-v3/backend

| File | Reason |
|---|---|
| `app/ai/providers/http.py` | 抽取 response `model`/`usage` → `last_response_*`（Issue-02） |
| `app/ai/gateway.py` | `authorize(budget_ok=False)` 默认；记录 `last_actual_model/usage`；denial 文案 |
| `app/ai/provider_reality.py` | 增加 `actual_model`/`actual_usage` 字段 |
| `app/ai/executor.py` | reality 记录 actual_*；finalize 写入 token 列 |
| `app/ai/budget.py` | 新增 `BudgetService.check()` fail-closed 探针（Issue-03） |
| `app/repositories/runtime_repository.py` | 新增 `BudgetRepository.remaining` |
| `app/domains/task/executor.py` | 授权改为 `check()` 结果，禁止 fail-open |
| `scripts/step0_blind_test.py` | 默认 model → `mimo-v2.6-pro`（Issue-04） |
| `tests/test_budget_check.py` | 新增 4 条 fail-closed 测试 |
| `.env` | `E2E_RUN_ID` / `DATABASE_MODE=fresh_test`（Issue-05） |

### Papers

| File | Reason |
|---|---|
| `tests/test_no_config_import.py` | 断言改为正式默认 `mimo-v2.6-pro`（Issue-04） |

---

## 6. Test evidence

```text
2026-09-26  python -m pytest tests/test_gateway.py tests/test_executor.py \
                      tests/test_task_executor.py tests/test_budget.py \
                      tests/test_budget_check.py -q
            → 61 passed

2026-09-26T12:18:29Z  python e2e_run/formal_e2e_v2.py
            E2E_RUN_ID=E2E2-20260926T121829  DATABASE_MODE=fresh_test
            IMPORT HTTP 200
            WORKER exit 0
            OUTCOME=FIRST_BLOCKING_POINT_IDENTIFIED
            artifacts:
              e2e_run/formal-e2e-v2-E2E2-20260926T121829.json
              e2e_run/formal-e2e-v2-worker-E2E2-20260926T121829.log
              AITutors-v3/backend/provider_reality.json
```

---

## 7. 最终纪律自检

```text
Smallest Change Principle     YES — 未重构、未新架构
Evidence First                YES — 全部结论绑定 run_id / claim_id / audit row
No Frozen Spec Change         YES — hash 未变
No Architecture Expansion     YES — 未改 Resolver/IR/Admission 语义
No Unverified Completion Claim YES — 明确 FIRST BLOCKING POINT，不声称产品完成
```
