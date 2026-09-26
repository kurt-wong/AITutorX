# FORMAL-E2E-ENABLEMENT-03-REPORT

```text
Document ID   : FORMAL-E2E-ENABLEMENT-03-REPORT
Task ID       : FORMAL-E2E-ENABLEMENT-03
Date          : 2026-09-26
E2E_RUN_ID    : E2E3-20260926T130248
DATABASE_MODE : fresh_test
Executor      : MIMO CODE (evidence stabilization; no Frozen Spec change; no architecture expansion)
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env.
```

---

## 0. 验收结论

```text
Evidence infrastructure stabilized  : YES
Business pipeline verification run  : YES
OUTCOME                             : PARTIAL
```

```text
Import → Seal → Annotation → Resolver → IR → Compiler/Admission : EXECUTED
Question / QuestionInstance / Material                           : 0 / 0 / 0
Admission candidates                                             : 13 (all pending_review)
```

结束定义：**Evidence infrastructure stabilized AND Business pipeline verification executed**。  
未声称 E2E PASS / FULL PRODUCT。

---

## 1. 修改列表

| File | Change | Issue |
|---|---|---|
| `AITutors-v3/backend/app/ai/providers/http.py` | 调用前 reset last_response_*；记录 finish_reason / response_chars / response_bytes / parse_error_type | C, D |
| `AITutors-v3/backend/app/ai/gateway.py` | `_live()` 调用前 reset actual 状态；透传 response evidence | D |
| `AITutors-v3/backend/app/ai/provider_reality.py` | 增加 finish_reason / response_chars / response_bytes / parse_error_type | C |
| `AITutors-v3/backend/app/ai/executor.py` | reality record 透传上述字段 | C, D |
| `AITutors-v3/backend/app/domains/annotation/service.py` | JSON 解析失败 ValueError 附 parse_error_type + response 大小（无原文/无 secret） | C |
| `AITutor-X/e2e_run/formal_e2e_v3.py` | evidence metadata；DATABASE_MODE reset 门控；双文档 staged evidence | A, B |
| `AITutor-X/e2e_run/formal-e2e-v3-E2E3-20260926T130248.json` | 运行证据 artifact | A |
| `AITutor-X/e2e_run/formal-e2e-v3-worker-E2E3-20260926T130248.log` | worker CLI 日志 | A |

### 1.1 A — Evidence metadata（已写入 artifact）

```text
E2E_RUN_ID              = E2E3-20260926T130248
DATABASE_MODE           = fresh_test
START_TIME              = 2026-09-26T05:02:48Z (approx)
END_TIME                = recorded in artifact
GIT_COMMIT.AITutors-v3  = 7702de9c36927a30907d23791d8ab64b09bc8c5a
V3_SPEC_HASH            = 6 files, SHA256 listed (unchanged vs ENABLEMENT-01/02)
PROVIDER                = mimo
MODEL                   = mimo-v2.6-pro
INPUT_DOCUMENT_SHA256   = standalone / composite_material_candidate (below)
```

### 1.2 B — reset_db 保护

```text
ALLOWED_RESET_MODES = {test, fresh_test}
DATABASE_MODE=production / dev / ""  →  REFUSE
DATABASE_MODE=test / fresh_test      →  ALLOW
```

本轮实际：`DATABASE_MODE=fresh_test` → TRUNCATE 25 tables（排除 alembic_version），已记录。

### 1.3 C — LLM response evidence

| request | finish_reason | response_chars | response_bytes | parse_error_type |
|---|---|---|---|---|
| 4daed945… (standalone) | **stop** | 4561 | 6520 | null |
| 87aac64f… (material) | **stop** | 7302 | 24995 | null |

说明：本轮两次 JSON 解析成功；finish_reason=stop 表示**非截断**。  
若失败，annotation ValueError 会带 `parse_error_type` + sizes（不存原文）。

### 1.4 D — Reality 防污染

每次 `complete()` / `_live()` **调用前清空** `last_actual_*` / `last_response_*`，调用后只写本响应。  
证据：两条 reality 记录各自绑定 request_id，usage 不同（2407/1558 vs 16341/5685），无继承。

---

## 2. 未修改列表（明确不做）

| Item | Status |
|---|---|
| `AITutors-v3/Docs/V3_SPEC/**` | **NOT MODIFIED** (hash unchanged) |
| Question IR / Admission / Resolver 业务语义 | NOT MODIFIED |
| 数据模型 / Schema / 新数据库 / Redis / Celery | NOT INTRODUCED |
| Gateway / Executor / Resolver / Admission 重写 | NOT DONE |
| Frontend | NOT DEVELOPED |
| Papers preprocessing 历史断言 / redact | NOT TOUCHED（任务排除） |
| 生产逻辑 | NOT MODIFIED |

---

## 3. E2E 运行命令

```bash
# env
E2E_RUN_ID=E2E3-20260926T130248
DATABASE_MODE=fresh_test

# formal entries only
POST http://127.0.0.1:8077/api/documents/import     # uvicorn app.main:app
python -m app.worker run --allow-live

# orchestration script (records evidence metadata)
python D:\Project\AITutor-X\e2e_run\formal_e2e_v3.py
```

禁止：直接实例化 Executor/Gateway、手工注入 task_context、hardcode budget_ok。

---

## 4. 输入文件 hash

| role | file | bytes | sha256 |
|---|---|---|---|
| standalone | `2021北京高三二模数学汇编：集合（教师版）.pdf` | 151212 | `89a26462e62f03a5a56cf6d36962ac4fdfc888cab999c057252da9048d61edc1` |
| composite_material_candidate | `2021北京高三一模二模政治汇编：生活与哲学（材料题）（教师版）(1).pdf` | 505671 | `0b8c0cc2bdd400b4530c7faa50b565327460f99c750f6b932fe1188f36e178cb` |

---

## 5. 每阶段结果

### 5.1 Import

| doc | HTTP | document_id | task_id | source |
|---|---|---|---|---|
| standalone | 200 | f45c7208-a840-44b4-b3d2-5b3b1940cd31 | c75d2e0d-b1a2-4651-b7ab-16498dd06bbe | sealed |
| material | 200 | c4e33dc0-84c5-4b1a-82d0-c95a5d7ca146 | 8dcd9f62-1b58-4cd5-970e-1e23b399d5c5 | sealed |

```text
source_figures         = 16
document_source_spans  = 855
document_source_lines  = (see artifact import_counts)
```

### 5.2 Annotation

| doc | provider | model | tokens (in/out/total) | status | payload |
|---|---|---|---|---|---|
| standalone | mimo | mimo-v2.6-pro | 2407 / 1558 / 3965 | completed + valid | 7× standalone_unit |
| material | mimo | mimo-v2.6-pro | 16341 / 5685 / 22026 | completed + valid | 21× standalone_unit |

**OBSERVATION**：材料题文档被标注为 **21 个 standalone_unit**，`shared_material=False`，未产生 `composite_unit`。  
→ 记为 `BLOCKED_BY_SEMANTIC_DECISION` 候选（composite 语义是否应由 LLM 声明 / 还是 resolver 结构推断 — **本轮不裁决**）。

### 5.3 Resolver

| doc | resolved | unresolved | reasons |
|---|---|---|---|
| standalone | 32 | 17 | stem:ambiguous×2, option:incomplete×8, explanation:missing×7 |
| material | 55 | 8 | stem:ambiguous×8 |

### 5.4 IR

| doc | ready | incomplete | structure |
|---|---|---|---|
| standalone | **0** | 7 | all standalone_unit, single_choice |
| material | **13** | 8 | all standalone_unit, short_answer/essay |

### 5.5 Compiler / Admission

```text
admission_candidates = 13
decision_status      = pending_review  (13/13)
admission_events     = 0
unit_groups          = 0
questions            = 0
question_instances   = 0
materials            = 0
```

**13 个 candidate 已生成**（Compiler/Admission 路径连通）。  
Question/Instance/Material **未生成**：candidate 停在 `pending_review`（Gate 未 auto_approve）。  
任务禁止自行 approve / 裁决 Admission 业务规则 → **不调用** `/api/candidates/{id}/approve`。

### 5.6 Frontend/API Exposure（只确认存在性）

| API | Exists? |
|---|---|
| Question API | **NOT PRESENT** |
| Material API | **NOT PRESENT** |
| Instance API | **NOT PRESENT** |
| POST /api/documents/import | YES |
| GET /api/documents/{id} / source-quality / source-lines | YES |
| GET /api/candidates/{id} / approve / reject | YES |
| GET /api/admin/stats | YES |

---

## 6. Blocker

```text
FIRST BLOCKING POINT (business chain tail)
  Stage   : Admission → Question materialization
  State   : 13/13 admission_candidates = pending_review
  Why     : Gate policy did not auto_approve real-content candidates
  Effect  : Question / QuestionInstance / Material remain 0
  Class   : BLOCKED_BY_SEMANTIC_DECISION (Admission/decision policy)
  Action  : RECORD ONLY — 不自行 approve，不改 Admission 规则
```

次要观察（非本轮阻塞，不修）：

| ID | Observation |
|---|---|
| OBS-03-01 | 材料题文档未产生 composite_unit / shared_material（LLM 声明语义 vs 预期） |
| OBS-03-02 | standalone 卷 explanation:missing / option:incomplete（Frozen resolver grammar vs 版式） |
| OBS-03-03 | Question/Material/Instance API 不存在（前端暴露面缺失） |

---

## 7. Next decision（需 Owner）

1. **Admission**：`pending_review` → Question 的放行策略（人工 approve / strict-auto grammar / 其它）？  
2. **Composite 语义**：材料题是否必须 `composite_unit`+`shared_material`，谁负责声明？  
3. **API 暴露**：是否需要 Question/Material/Instance 只读 API 供前端？

---

## 8. Git

```text
commit message:
FORMAL-E2E-ENABLEMENT-03 evidence stabilization and pipeline verification
```

涉及仓库：AITutors-v3（代码）/ AITutor-X（report + artifacts）。

---

## 9. 纪律自检

```text
Evidence first                  YES — 全部绑定 E2E_RUN_ID / request_id / claim_id
No assumption                   YES — composite 未产生记 OBS，不改语义
No silent fallback              YES — reset 门控、reality 清零、parse error 显式
No architecture expansion       YES
No Frozen Spec modification     YES — hash unchanged
禁止为 PASS 改事实               YES — 结果 PARTIAL，不粉饰
```
