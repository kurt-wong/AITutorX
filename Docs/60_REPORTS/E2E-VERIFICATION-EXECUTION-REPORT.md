# E2E Verification Report — AITutors-v3 Engineering Verification Execution

```text
Document ID   : E2E-VERIFICATION-EXECUTION-REPORT
Document Type : Engineering Verification Execution Report（执行证据记录）
Date          : 2026-09-26
Repository    : kurt-wong/AITutorX @ main（验证侧）
              : AITutors-v3 @ od01-r3-convergence d2b9a26f1a1c0297b4536b273b8999a071433079（被测实现）
Producer repo : kurt-wong/Aitutors-preprocessing @ 2b92898f05f6541a5fc65c8300cb8a59a06c4928（@ D:\Project\Papers）
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 治理定位（EV-03 / EV-04 处理）

**本次性质**：

```text
Engineering Verification Execution
```

**不是**：

```text
LIMIT-AUTH Phase 6 authorization claim
```

逐条自检（`AITutors-v3/Docs/COORDINATION/LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md`）：

| LIMIT-AUTH 条款 | 本次执行的处置 | 状态 |
|---|---|---|
| §4 Phase Order（Phase 0–6，End-to-End Verification = Phase 6） | 本次**未**声明进入 Phase 6；未修改任何 Phase 标注 | **UNCHANGED — Phase 6 NOT entered** |
| §5 STOP Conditions A–J | **全部继续有效**，本次未解除任一条 | **EFFECTIVE** |
| §3.5 Schema Change Boundary（硬性 STOP） | 未 ALTER TABLE、未改 schema | **EFFECTIVE** |
| §6 Forbidden Scope — V3 production code modification | `git status --porcelain` 非 `??` 条目 = **0**；未改任何 `app/` 文件 | **RESPECTED** |
| §6 — Gate modification / Admission modification | 只**调用** `GateService` / `AdmissionService`，未改其实现 | **RESPECTED** |
| §6 — DB migration | 未执行 `alembic upgrade`、未改 migration 文件 | **RESPECTED** |
| §6 — V3 Frozen Schema modification | 见 §1.2 SHA256，6/6 未变 | **RESPECTED** |
| §6 — historical corpus rerun | 语料只做**只读元数据扫描**计数（EV-01/EV-02），非 pipeline rerun | **RESPECTED** |
| `CR-003 §7:228` P1 Segment A 仍处 STOP | 未启动 P1 Segment A 实施 | **EFFECTIVE** |
| `LIMIT-AUTH §3.8` OD-01 re-freeze 条件 | 未满足、未主张满足 | **EFFECTIVE** |

与 `OD-R-01-CLOSURE-RECORD.md:206-231` 边界表的对账（EV-04）：

> 该记录明载：「Verification Phase STARTED **不等于** Phase 6 STARTED」「Phase 6 is **NOT** entered by this record」
> 「STOP remains effective（A–J）」「本记录**不授权** Migration / X3 Entry / Production Deployment」。

**本次执行与之无冲突**：本次是 Verification Phase（治理进程）范围内的
*integration validation / end-to-end testing / execution evidence collection*，
**不推进** `LIMIT-AUTH §4` 的任何 Phase，**不修改** Phase 状态，**不解除** STOP，
**不主张**进入 Phase 6。两套命名（Governance Process Phase vs V3 Authorized Phase）全程未混用。

---

## 1. 环境说明

### 1.1 运行环境

| 项 | 值 | 采集时间 |
|---|---|---|
| OS | `Windows-11-10.0.26200-SP0` | 2026-09-25T23:44:02+08:00 |
| Python | `3.12.9 (MSC v.1942 64 bit [AMD64])` | 同上 |
| 环境性质 | **本地开发验证环境（TEST ENVIRONMENT）** | — |
| 数据库 | PostgreSQL 16（Docker Compose），`localhost:5432/aitutors` | 全程 |
| DB 性质 | **Temporary Verification Database**（任务§二：可全部清理，不按生产数据保护） | — |
| `APP_ENV` | `development`（`.env`） | 全程 |
| `LLM_GATEWAY_MODE` | `live`（`.env`） | 全程 |
| `OCR_GATEWAY_MODE` | `disabled`（`.env`） | 全程 |
| LLM endpoint | `https://api.xiaomimimo.com/v1/chat/completions` | 全程 |
| LLM model（实际使用） | **`mimo-v2.6-pro`** | 全程 |
| API Key | 来自 `.env` 的 `MIMO_API_KEY`；**全文不记录任何密钥值** | 全程 |

**系统级边界**：未修改系统配置 / Windows 服务 / 系统 PATH / 用户环境变量；未删除非项目目录文件。
本次唯一进程级动作是启动 `uvicorn app.main:app --port 8077`（项目内 API，任务§一.2 允许）。

### 1.2 Frozen Spec 基线（只读，未修改）

```text
$ for f in 00 10 20 30 40 50_*.md; do sha256sum Docs/V3_SPEC/$f; done
c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4  00_Master_Spec.md
529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1  10_Data_Model.md
0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c  20_Document_Pipeline.md
db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89  30_Task_LLM_Safety.md
8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db  40_Development_Rules.md
8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7  50_Migration_Assets.md

$ git rev-parse HEAD:Docs/V3_SPEC
14a7450809d4932036f415d765ab29c53671843c          ← 与 DSH 复核基线一致，未变
```

### 1.3 生产代码基线（未修改）

```text
$ cd AITutors-v3 && git rev-parse HEAD
d2b9a26f1a1c0297b4536b273b8999a071433079

$ git status --porcelain | grep -v '^??'
（空）                                              ← 0 处生产文件被修改
```

本次新增文件全部位于 `AITutor-X/e2e_run/`（临时验证工具 + 证据），以及本报告
（`Docs/60_REPORTS/`）。**未触碰** `Docs/V3_SPEC/`、`OD-R-01-CLOSURE-RECORD.md`、
授权模型、核心架构定义。

---

## 2. 执行命令

全部命令的实际调用（`cd` 省略；`MIMO_MODEL` 为环境变量覆盖，见 MEDIUM-04）：

```bash
# C1 环境与基线
date -Iseconds
python -c "import sys,platform;print(sys.version);print(platform.platform())"
cd AITutors-v3 && git rev-parse HEAD && git status --porcelain
sha256sum Docs/V3_SPEC/*.md

# C2 MIMO 可用模型枚举（不打印密钥）
python -c "... httpx GET https://api.xiaomimimo.com/v1/models ..."

# C3 LIVE MIMO 连通性冒烟
MIMO_MODEL=mimo-v2.6-pro python -c "... HTTPLLMProvider(name='mimo',...).complete('Reply with exactly the single word: OK') ..."

# C4 真实生产链 E2E（caseA 参考答案卷 / caseB 真试卷）
cd AITutors-v3/backend
MIMO_MODEL=mimo-v2.6-pro python D:/Project/AITutor-X/e2e_run/e2e_live_full_chain.py
E2E_INPUT=D:/Project/AITutor-X/e2e_run/inputs/caseB_real_exam.pdf \
E2E_ARTIFACT=D:/Project/AITutor-X/e2e_run/e2e-live-caseB.json \
MIMO_MODEL=mimo-v2.6-pro python D:/Project/AITutor-X/e2e_run/e2e_live_full_chain.py

# C5 生产路径逐单元 IR 诊断（只读）
python D:/Project/AITutor-X/e2e_run/diag_prod_ir.py

# C6 下游 Material 能力验证（真实 producer manifest）
DIAG_MANIFEST=D:/Project/Papers/Ocr-markdown/reslice-pac-annotated/reslice-pac/ocr/pac-c08-01.manifest.json \
python D:/Project/AITutor-X/e2e_run/diag_ir.py

# C7 真实 HTTP API 验证
python -m uvicorn app.main:app --host 127.0.0.1 --port 8077 &
curl -s http://127.0.0.1:8077/health
curl -s http://127.0.0.1:8077/api/candidates/<cid>
curl -s -X POST http://127.0.0.1:8077/api/candidates/<cid>/approve \
     -H 'Content-Type: application/json' \
     -d '{"reviewer_id":"e2e-verify-human","confirmed_fields":["stem","answer"]}'
curl -s http://127.0.0.1:8077/api/admin/stats

# C8 语料只读统计（EV-01 / EV-02）
cd D:/Project/Papers
find maintainess/PDF -iname '*.pdf' | wc -l
find original -iname '*.pdf' | wc -l
find . -iname '*.pdf' | wc -l
python -c "... rglob('*.manifest.json') + json.load 统计 unit_type/material_lines/question_numbers ..."

# C9 DB 状态与约束/完整性
python -c "... asyncpg: count(*) per table, pg_constraint, FK orphan check ..."

# C10 Replay / 幂等
E2E_INPUT=...caseB_real_exam.pdf E2E_ARTIFACT=...e2e-live-caseB-replay.json MIMO_MODEL=mimo-v2.6-pro python .../e2e_live_full_chain.py
```

---

## 3. 测试范围

| # | 验证项 | 覆盖状态 | 手段 |
|---|---|---|---|
| T1 | 输入层（PDF/DOC/DOCX/JPG/PNG） | **已执行**（5 类扩展名 + txt） | 真实 `DocumentImportService.import_file` |
| T2 | manifest 生成 / source version 记录 | **已执行** | `document_source_versions/lines/spans/source_figures` |
| T3 | OCR / Extraction | **已执行** | `NativeTextProvider`（PyMuPDF 文本层） |
| T4 | Semantic Annotation（LLM） | **已执行（真实 live）** | `AnnotationService` + MIMO HTTP |
| T5 | Resolver | **已执行** | `SourceResolver.resolve` |
| T6 | Question IR + 校验 | **已执行** | `IRBuilder.build` + `validate_ir` |
| T7 | Compiler | **已执行** | `Compiler.compile`（leaves / materials） |
| T8 | Gate | **已执行** | `evaluate`（`admission-gate/v1` 四层） |
| T9 | Admission / Candidate | **已执行** | `AdmissionService` + `create_admission_candidate` |
| T10 | Persistence（含 FK / unique / audit） | **已执行** | 直连 PostgreSQL 校验 |
| T11 | Material / composite + shared material | **部分执行** —— 下游 PASS，生产标注层 NOT REACHABLE | 见 BLOCKER-01 |
| T12 | Failure / rejection path | **部分执行** | 见 §8 / §9 LOW-01 |
| T13 | Provenance | **已执行** | `source_span` / `text_hash` / `evidence` / `logical_execution_hash` |
| T14 | Replay / 幂等 | **已执行** | 同输入重跑 |
| T15 | API verification | **已执行（真实 HTTP）** | FastAPI + uvicorn |
| T16 | LLM authority boundary | **已执行** | prompt 约束 + `FORBIDDEN_FIELDS` 校验 |

**未覆盖**：Phase 6 授权主张（本次不是）；历史语料 pipeline 重跑（Forbidden Scope）；
Migration / X3 Entry / Production Deployment（各自需独立授权）。

---

## 4. 输入数据范围（EV-01 / EV-02 处理）

> **数字纪律**：以下每个数字均标注 `scope` / `dataset` / `source` / `timestamp`。
> 本轮**重新实测**，不沿用上一轮报告的数字。

### 4.1 真实输入规模（EV-02 更正）

| scope | dataset | source | timestamp | PDF 数 |
|---|---|---|---|---|
| `D:\Project\Papers\maintainess\PDF\` | Aitutors-preprocessing@`2b92898` | `find … -iname '*.pdf' \| wc -l` | 2026-09-26T00:28+08:00 | **12 707** |
| `D:\Project\Papers\original\` | 同上 | 同上 | 同上 | **75 366** |
| `D:\Project\Papers\` 全仓 | 同上 | 同上 | 同上 | **88 074** |
| `D:\Project\Papers\Ocr-markdown\` | 同上 | 同上 | 同上 | **0**（存 `.md`，非 PDF） |

**交叉验证**：producer 自身语料清单 `data/r64_corpus_inventory.json` 记
`"pdf_total_indexed": 12707` —— 与 `maintainess/PDF` 计数**一致**。

**结论（EV-02）**：上一轮报告把 **88 074**（全仓，含 gitignored `original/`）挂在
`maintainess\PDF\` 名下，属**归属错误**，输入规模被放大 **6.94×**。
正确表述 = **已索引语料 12 707；全仓 88 074**。本轮按此更正，见 §10 Q1。

### 4.2 语料结构统计（EV-01 更正）

```text
scope     : D:\Project\Papers\Ocr-markdown\ (recursive)
dataset   : Aitutors-preprocessing @ 2b92898f05f6541a5fc65c8300cb8a59a06c4928
source    : python rglob('*.manifest.json') + json.load → unit_type / material_lines / question_numbers
timestamp : 2026-09-26T00:32:00+08:00
command   : 见 §2 C8（第 2 条）
artifact  : e2e_run/corpus-scope-stats.txt
```

| scope | manifests | units | `standalone\|−\|qspan` | `composite\|mat\|qspan` | `composite\|−\|qspan` | 其它 |
|---|---|---|---|---|---|---|
| **全语料** `Ocr-markdown/` | **166** | **4 609** | **3 935** | **668** | **5** | `andalone\|−\|qspan` = **1** |
| 子集 `reslice-pac-annotated` | 22 | **530** | 472 | 55 | 3 | — |

**决定性定性结论（全语料口径实测）**：

```text
standalone_question + material  →  0 / 3935      （从未出现）
```

**结论（EV-01）**：上一轮报告标题写「全语料 472 + 58」，实为 `reslice-pac-annotated`
子集（530 units）统计，规模被低估 **8.7×**（530 → 4 609）。且该表第三列把 472 个
standalone 标为 `'-'`（无 question span），实测 3 935 个 standalone **全部有**
`question_numbers`（应为 `'qspan'`）。**定性结论正确，证据基被错误标注**。
本轮已按 `scope/dataset/source/timestamp` 重算并区分两层口径。

### 4.3 本次 E2E 实际输入

| ID | 文件 | scope/source | bytes | sha256 | 性质 |
|---|---|---|---|---|---|
| caseA | `e2e_run/inputs/caseA_real.pdf` | 上轮遗留真实 PDF | 182 605 | `a136e47bf01ed4420a935f799a0d807182a10758ad0cf3cc1d0d280a9377350e` | **参考答案**卷（无题干） |
| caseB | `e2e_run/inputs/caseB_real_exam.pdf` | `Papers\maintainess\PDF\2020北京四中高一（上）期中数学含答案.pdf` | 350 855 | `f58e39ae5e0eed28330a687d04b50a40ef4cf4d10511917643ef39161533b8ce` | **真试卷**（题干+选项+答案），8 页 / 7 214 字符 |
| pac-c08-01 | `Papers\Ocr-markdown\reslice-pac-annotated\reslice-pac\ocr\pac-c08-01.manifest.json` | producer 真实 manifest | — | — | 9 units / 8 composite+material |

**fixture 覆盖声明**：本次生产链 E2E 使用 **2 份**真实文档；相对 12 707 已索引语料
覆盖 **0.016%**。下游 Material 能力验证使用 **1 份** producer manifest（87 份含
composite+material 的 manifest 之一）。**不得**把本报告结论外推为全语料验证结论。

---

## 5. API 调用记录（EV-05 处理）

> 纪律：记录**模型 / 是否真实调用 / 是否 mock / 是否 fallback**。
> 「没有主动开启 mock」≠「权限验证完成」——本节逐项明示。

### 5.1 LLM API

| 项 | 值 |
|---|---|
| provider | `mimo`（`HTTPLLMProvider`，`app/ai/providers/http.py`） |
| model | **`mimo-v2.6-pro`** |
| endpoint | `https://api.xiaomimimo.com/v1/chat/completions` |
| **是否真实调用** | **是（真实 HTTP，非 mock）** |
| **是否 mock** | **否**（`llm_boundary.mock_used = false`） |
| **是否 fallback** | **否**（`fallback_used = false`；`settings.provider_fallback_enabled` 未触发） |
| **是否 DeepSeek** | **否**（本轮全程未调用 DeepSeek） |
| 认证 | `Authorization: Bearer <MIMO_API_KEY>`，密钥来自 `.env`，**未记录值** |
| 授权依据 | 任务§一.2「允许：调用外部 API」+ §三「第一优先 MIMO V2.6 PRO」 |

**真实调用证据（`llm_call_audit`，provider='mimo'）**：

| start (UTC) | status | prompt_chars | logical_execution_stage | error_type |
|---|---|---|---|---|
| 2026-09-25T16:03:12 | failed | 3 196 | ann | `conflict`（GatewayDenied，见 BLOCKER-02） |
| 2026-09-25T16:07:40 | **completed** | 3 196 | ann | — |
| 2026-09-25T16:24:14 | **completed** | 8 705 | ann | — |

冒烟测试：`Reply with exactly the single word: OK` → 返回 `'OK'`，耗时 1.38s。

**DeepSeek 时间限制自检**：任务§三规定工作日 08:00–12:00 / 14:00–18:00 禁止调用。
本轮**未调用 DeepSeek**，故无需记录调用时间/原因/成本。
（DB 中 `provider='deepseek'` 的 757 行审计为 **2026-09-15 ~ 2026-09-25 15:18（本地）**
历史遗留，非本次产生；本轮未新增。）

### 5.2 HTTP API（真实，非伪造）

```text
$ python -m uvicorn app.main:app --host 127.0.0.1 --port 8077
INFO:  Started server process [21176]
INFO:  Uvicorn running on http://127.0.0.1:8077

$ curl http://127.0.0.1:8077/health
HTTP 200

$ curl http://127.0.0.1:8077/api/candidates/54f869a3-ea87-41ab-9591-ff31f2a455b9
HTTP 200   {"id":"54f869a3…","unit_type":"standalone_unit","decision_status":"pending_review", …}

$ curl -X POST http://127.0.0.1:8077/api/candidates/54f869a3…/approve \
      -d '{"reviewer_id":"e2e-verify-human","confirmed_fields":["stem","answer"]}'
HTTP 200   {"decision_status":"approved",
            "review_trail":[{"decision":"approve","reviewer_id":"e2e-verify-human",
                             "verified_by":"human","confirmed_fields":["stem","answer"]}]}
```

`e2e_run/api-verify.log` 逐行留有上述请求（`21176` 进程），与本节一一对应。
**未伪造任何 HTTP 证据**；`GET /api/documents*` 等端点本轮**未调用**，故不列入结果表。

---

## 6. 数据库状态（EV-07 / EV-08 处理）

> 破坏性测试纪律：每次记录 **Before（DB snapshot / git state / environment）** 与
> **After（result / cleanup / restore）**。

### 6.1 Before 快照（2026-09-26T00:03:12+08:00，任务开始时）

| 表（真实表名） | 行数 |
|---|---|
| `alembic_version` | 1 |
| `documents` | 1 |
| `document_source_versions` | 1 |
| `document_source_lines` | 338 |
| `document_source_spans` | 545 |
| `source_figures` | 17 |
| `tasks` | 3 |
| `task_claims` | 2 |
| `llm_call_audit` | 956 |
| `budget` | 3 406 |
| `semantic_annotations` / `admission_candidates` / `admission_events` / `questions` / `question_instances` / `materials` / `validation_events` 等 16 表 | **0** |

git state Before：`AITutors-v3` HEAD `d2b9a26f`，`git status --porcelain` 非 `??` = 0。
environment Before：见 §1.1。

### 6.2 After 快照（2026-09-26T00:35+08:00）

| 表 | Before | After | Δ | 说明 |
|---|---|---|---|---|
| `documents` | 1 | 3 | +2 | caseB + 1 个扩展名矩阵 docx 样例 |
| `document_source_versions` | 1 | 2 | +1 | caseB seal |
| `document_source_lines` | 338 | 2 039 | +1 701 | caseB |
| `document_source_spans` | 545 | 3 579 | +3 034 | caseB |
| `source_figures` | 17 | 40 | +23 | caseB |
| `semantic_annotations` | 0 | 2 | +2 | 2 次真实 live 标注 |
| `admission_candidates` | 0 | 6 | +6 | caseB 6 个 ready unit |
| `admission_events` | 0 | 1 | +1 | approve 物化事件 |
| `questions` | 0 | **1** | +1 | **最终对象** |
| `question_instances` | 0 | **1** | +1 | **最终对象** |
| `materials` | 0 | 0 | 0 | 见 BLOCKER-01 |
| `material_links` / `validation_events` / `knowledge_nodes` | 0 | 0 | 0 | 未产生 |
| `tasks` / `task_claims` | 3 / 2 | 10 / 10 | +7 / +8 | 含扩展名矩阵与 replay |
| `llm_call_audit` | 956 | 959 | +3 | 见 §5.1 |

### 6.3 落库实证（最终对象）

```text
questions (1)
  id                       a35743e0-2e00-4b11-89af-138861b24c29
  canonical_question_type  fill_in
  subject / grade          数学 / 高一
  dedup_key                e09816aa8cb6c6f23910a71b0254bb268b26cf4d29dfa4b02f7068533fb8…
  created_at               2026-09-25T16:29:40.204791Z

question_instances (1)
  id                       953743dd-15bb-4656-b801-3ae0206e625f
  question_id              a35743e0-…            (FK → questions)
  document_id              bffd8c7b-5480-42ad-905f-023cb04104e9   (FK → documents)
  source_version_id        5ed951e5-a1f8-4c6a-8b48-71a60a0ea79a   (FK → document_source_versions)
  unit_group_id            2829dc0f-da0f-4b38-9fa6-7cf80b60d202   (FK → unit_groups)
  question_number / page   11 / 2
  occurrence_key           5cb44fde799f4f80014a0ca1a449a271769e1f23f542a3e4f9050bfa2383996a
  logical_execution_hash   2ba31a5355cff66196040bb5adffc68e72e3138371e97fddac99766272217b1d

instance_role_contents (2)  role=stem / role=answer
  stem   text_hash d48f0ffb…  source_span {"span_id":"sp-Q11.stem","line_refs":["P2L073",…]}
  answer text_hash e1a6dffe…  source_span {"span_id":"sp-Q11.answer","line_refs":["P6L031"]}
                              answer_status {"complete":true,"source_located":true,"verified_correct":true}

materials (0)  ← 见 BLOCKER-01
```

### 6.4 foreign key / unique constraint 校验

```text
FK 完整性（orphan check）:
  question_instances.question_id            not in questions              → 0
  instance_role_contents.instance_id        not in question_instances     → 0
  admission_events.candidate_id             not in admission_candidates   → 0

约束（pg_constraint 实测）:
  questions                PRIMARY KEY (id) ; UNIQUE (dedup_key)                      [uq_questions_dedup_key]
  question_instances       PRIMARY KEY (id)
                           FOREIGN KEY (question_id)         → questions(id)
                           FOREIGN KEY (document_id)         → documents(id)
                           FOREIGN KEY (source_version_id)   → document_source_versions(id)
                           FOREIGN KEY (unit_group_id)       → unit_groups(id)
                           UNIQUE (question_id, source_version_id, occurrence_key)
  materials                PRIMARY KEY (id) ; FK (source_version_id) → document_source_versions(id)
  admission_events         PRIMARY KEY (id) ; UNIQUE (candidate_id) ; FK (candidate_id) → admission_candidates(id)
  admission_candidates     PRIMARY KEY (id)
                           UNIQUE (logical_execution_stage, logical_execution_hash)
                           FK (annotation_id) → semantic_annotations(id)
                           FK (source_version_id) → document_source_versions(id)
  semantic_annotations     PRIMARY KEY (id)
                           UNIQUE (logical_execution_stage, logical_execution_hash)
                           FK (source_version_id) → document_source_versions(id)
  documents                PRIMARY KEY (id) ; UNIQUE (original_sha256)                [uq_documents_original_sha256]
```

**判定**：FK 关系**完整**（0 orphan）；unique constraint **齐备且生效**
（幂等依赖 `original_sha256` / `(stage,hash)` / `dedup_key` / `occurrence_key` 四层）。

### 6.5 audit 记录

| audit 对象 | 记录情况 |
|---|---|
| LLM 调用 | `llm_call_audit` 3 行（provider/model/status/prompt_chars/stage/start） |
| 预算 | `budget` +3（reserve/settle 成对） |
| Task 生命周期 | `task_claims`（claim_round/outcome/error_type/lease_snapshot） |
| 物化事务 | `admission_events`（candidate_id/materialized_at/created_question_ids） |
| 证据引用 | candidate payload 内 `evidence[]`（kind/role/span_id/evidence 词表） |

**缺陷（见 MEDIUM-03）**：`admission_events.created_instance_ids` 记为 `[None]`，
但 `question_instances` 同事务已物化 1 行（instance `created_at .210316` <
event `materialized_at .214326`）。审计事件**未记录**已物化的 instance id。

### 6.6 清理 / 恢复

本次**未执行清库**。按任务§二，该库为 Temporary Verification Database，
验证后可全部清理、测试数据无需保留。**未做**「wipe 后恢复」操作，
因为本次**未运行**任何全表 DELETE 测试（见 §8 EV-08 处置）。

---

## 7. Pipeline 结果

### 7.1 全链路阶段表（caseB 真试卷，决定性运行）

```text
command   : E2E_INPUT=...caseB_real_exam.pdf MIMO_MODEL=mimo-v2.6-pro python e2e_run/e2e_live_full_chain.py
timestamp : 2026-09-26T00:24:13+08:00 → 00:25:17+08:00   (wall 64.65s)
input     : caseB_real_exam.pdf  sha256 f58e39ae…33b8ce  350 855 bytes
task      : 6ec6bcec-814d-4ad7-82cb-55cb1c5f4ace   status=succeeded   llm_invocations=1
```

| # | Stage | INPUT | OUTPUT | STATUS | PERSISTENCE EFFECT |
|---|---|---|---|---|---|
| 1 | Import | `caseB_real_exam.pdf` 350 855 B | `documents` 行（`is_new=false`，SHA 命中） | **PASS** | `documents` 幂等，未重复 |
| 2 | Task enqueue | document_id + file_path | `tasks` `queued` | **PASS** | `tasks +1` |
| 3 | Seal | file bytes + `NativeTextProvider` | `DocumentSourceVersion`（`artifact_kind=raw_l1`, `role=native`, `provider=native`） | **PASS** | `document_source_versions 1→2`、`lines 338→2039`、`spans 545→3579`、`figures 17→40` |
| 4 | Quality Check | `version.body_text` | `SourceQualityGate` report → `source_meta.quality` | **PASS**（`valid`） | 写 `source_meta` |
| 5 | **Semantic Annotation** | `build_annotation_prompt(body_text)`（8 705 chars） | `SemanticAnnotation`（26 `semantic_units`，`status=valid`） | **PASS**（真实 MIMO） | `semantic_annotations 0→2`、`llm_call_audit +1 completed` |
| 6 | Resolver | annotation payload + 1 701 lines + 23 figures | `ResolvedRun`：**27 resolved spans / 82 unresolved** | **PARTIAL** | 内存（无表） |
| 7 | Question IR | `ResolvedRun` + payload | 26 top-level units：**ready 6 / incomplete 20** | **PARTIAL** | 内存 |
| 8 | Compiler | IR + span/line map | **leaves 6 / materials 0** | **PARTIAL** | 内存 |
| 9 | Gate | root unit + ir + compiled + resolved_run | 4 层判定，6 个 candidate | **PARTIAL**（0 auto_approve） | `admission_candidates 0→6`，全部 `pending_review` |
| 10 | Admission（candidate） | gate 决策 | `AdmissionCandidate` 落库 | **PASS** | 6 行 |
| 11 | **Admission（approve → 物化）** | HTTP `POST /api/candidates/{id}/approve` | `Question` + `QuestionInstance` + `unit_groups` + `instance_role_contents` | **PASS** | `questions 0→1`、`question_instances 0→1`、`admission_events 0→1` |
| 12 | Persistence 校验 | DB | FK 0 orphan、unique 齐备 | **PASS** | — |

### 7.2 逐单元 IR 结果（caseB，`e2e_run/diag-prod-ir.json`）

```text
annotation : 3fae271a-4b01-486b-8d2c-badd8188ad93  status=valid
schema     : semantic-metadata-annotation/v0.3      prompt_version: semantic-annotation/v1
resolver   : lines=1701 figures=23 resolved_spans=27 unresolved=82
IR tally   : ready=6  incomplete=20  unknown=0
compiled   : leaves=6  materials=0
leaf units : Q9, Q11, Q12, Q13, Q14, Q15
```

未解析原因直方图（82 条）：

| evidence | 含义 | 归类 |
|---|---|---|
| `option A/B/C/D` (`incomplete`) | 选项仅声明 label，无 per-label 文本 span | **PRODUCER / 证据粒度 GAP** |
| `question N start not unique` (`ambiguous`) | 试题段与答案段题号重复，起点不唯一 | **resolver 启发式限制 + 版式** |
| `answer row qn=N not found` (`missing`) | 答案表未覆盖该题 | 数据/版式 |
| `answer row qn=N spans multiple lines` (`ambiguous`) | 答案跨行 | 版式 |

单元问题直方图：`role option unresolved` ×48、`stem unresolved` ×16、
`answer unresolved` ×13、`role explanation unresolved` ×5。

### 7.3 Gate 四层判定（`gate_policy_version: admission-gate/v1`）

| layer | status | reasons |
|---|---|---|
| `semantic` | **pass** | — |
| `structural` | **pass** | — |
| `provenance` | **pass**（`auto_allowed: true`） | — |
| `admission` | **fail** | `leaf 'Qxx' type 'fill_in' not strict-auto (grammar None)` ×5<br>`leaf 'Q9' answer grammar: answer not expressible as canonical value` ×1 |

`decision` → **`pending_review`**（6/6，`auto_approve` = 0）。

**判定**：这是 **Gate 自身阻断**，不是测试造就的阻断 —— 任务§10 Case B 的证明点成立。
`fill_in` / `short_answer` 无 strict-auto grammar，Gate 明确拒绝自动放行，符合
`20 §8.2` 双入口设计（自动路径要求 `auto_approve`；人工路径要求 review_trail 人工确认）。

### 7.4 caseA（参考答案卷）对照

| 项 | caseA | caseB |
|---|---|---|
| 文档性质 | 参考答案（无题干/选项） | 真试卷（题干+选项+答案） |
| LLM 输出 | 22 units（含 Q1–Q22 题号与 A–D 选项标签） | 26 units |
| Resolver | 21 resolved / 66 unresolved | 27 resolved / 82 unresolved |
| IR | ready **0** / incomplete 22 | ready **6** / incomplete 20 |
| compiled | leaves 0 / materials 0 | leaves 6 / materials 0 |
| candidates | **0** | **6** |
| **分类** | **FIXTURE LIMITATION**（输入无题干） | 正常路径 |

caseA 中 LLM 对不存在的题干/选项仍输出结构标签，Resolver 正确 **fail-closed** 拒绝
（`question number 'N' not found`）。这是**正确行为**，不是缺陷；但提示
**LLM 结构声明可能超出源文证据**，见 §9 INFO-02。

### 7.5 下游 Material 能力（任务§7）

```text
command   : DIAG_MANIFEST=.../pac-c08-01.manifest.json python e2e_run/diag_ir.py
timestamp : 2026-09-26T00:33+08:00
input     : producer 真实 manifest（9 units，8 个 composite+material）
identity  : VERIFIED + AVAILABLE ；interface_scope accepted（identity_version==2）
IR        : 9 top-level units，26 spans，0 unresolved
IR tally  : ready=9  incomplete=0  unknown=0
COMPILED  : leaves=9  materials=8
```

8 个 `CompiledMaterial` 各含：`unit_id`、`role='material'`、`span_id='sp-<unit>.material'`、
**真实 material 正文**、`text_hash`（sha256）、`dedup_key`。
composite 单元 `shared=['material']` + `subs=['….sub']`，
**shared material 只输出一次，未复制进子题**（符合 `20 §4.5` 原文
「shared material 只输出一次，绝不复制进任何子题 stem」）。

**结论**：**下游 Material 能力存在且可用**（含 dedup_key、span、hash、不复制）。
生产路径 `materials=0` 的原因**不在 Compiler/Gate**，而在生产标注 prompt（BLOCKER-01）。

### 7.6 Replay / 幂等（任务§四.5）

```text
command   : E2E_INPUT=...caseB_real_exam.pdf E2E_ARTIFACT=...e2e-live-caseB-replay.json ...
baseline  : documents 3 / document_source_versions 2 / semantic_annotations 2
            admission_candidates 6 / questions 1 / question_instances 1 / materials 0 / llm_call_audit 959
result    : task 9720c624… status=succeeded  llm_invocations=0  wall 0.43s
DB delta  : tasks +1 / task_claims +1      ← 仅新增 task 记录
            semantic_annotations / admission_candidates / questions
            question_instances / materials  →  全部 Δ=0
```

| 验证点 | 结果 |
|---|---|
| 同 SHA256 重复导入 | **幂等**（`uq_documents_original_sha256`，`is_new=false`，同 document_id） |
| 同输入重跑 pipeline | **幂等**（`logical_execution_hash` 唯一约束 → annotation 复用，`llm_invocations=0`） |
| Question 物化重复 | **无重复**（`questions`/`question_instances` Δ=0） |
| seal 幂等 | **幂等**（`find_sealed_version_by_le` 命中既有版本） |

**判定：PASS —— 未产生非法重复。**

### 7.7 输入层支持矩阵（任务§四.1）

| 扩展名 | 结果 | 证据 |
|---|---|---|
| `.pdf` | **ACCEPTED** | 真实 PDF 导入成功 |
| `.docx` | **ACCEPTED** | `extmatrix_docx_stub.docx` 导入成功 |
| `.doc` | **REJECTED** | `ImportError_: unsupported file type: '.doc'; allowed: ['.docx', '.pdf']` |
| `.jpg` | **REJECTED** | 同上 |
| `.png` | **REJECTED** | 同上 |
| `.txt` | **REJECTED** | 同上 |

**分类：IMPLEMENTATION GAP**（相对任务§四.1「PDF/DOC/DOCX/JPG/PNG 输入正常」）。
实际实现 = `_ALLOWED_EXTENSIONS = {".pdf", ".docx"}`（`app/domains/source/import_service.py:26`）。
**DOC / JPG / PNG 不受支持**；拒绝路径本身工作正确（fail-closed + 明确错误信息）。
未修改实现以「制造支持」。

---

## 8. Known Limitations

| # | 限制 | 性质 | 影响面 |
|---|---|---|---|
| L-01 | 生产链 E2E 通过**验证 harness 的依赖注入**跑通，未经 `app/worker` 生产入口 | 设计边界（见 BLOCKER-02） | 生产入口可运行性未证实 |
| L-02 | fixture 覆盖 2 份文档 / 12 707 已索引语料 = **0.016%** | fixture limitation | 不得外推为全语料结论 |
| L-03 | Material / composite 仅在**下游**验证（1 份 producer manifest），生产标注层 NOT REACHABLE | BLOCKER-01 | 任务§7 未完全满足 |
| L-04 | `single + material`（standalone + material）**无样本可测** | fixture limitation | 全语料实测该组合 **0/3935**，本就不存在 |
| L-05 | Case B `rejected` 状态迁移**未执行** | 权限边界 | host auto-mode 拒绝不可逆 API reject；仅代码级确认 |
| L-06 | 未执行 migration 测试（`alembic upgrade`） | 治理边界 | `LIMIT-AUTH §6` 禁 DB migration；本次不改 migration |
| L-07 | 未做历史语料 pipeline 重跑 | 治理边界 | `LIMIT-AUTH §6` 禁 historical corpus rerun |
| L-08 | 性能未作为通过判据 | 任务§八（correctness 第一） | 仅记录 wall 64.65s / 0.43s |
| L-09 | `validation_events` / `knowledge_nodes` / `material_links` 恒为 0 | 未覆盖路径 | Evidence Promotion / 知识图谱未在本次对象上触发 |

**EV-07 / EV-08 破坏性测试处置**：

```text
Before  : DB snapshot（§6.1）· git state（§1.3）· environment（§1.1）
After   : result（§6.2/§6.3）· cleanup（未清库，Temporary Verification Database）· restore（不适用）
```

- 本轮**未运行**任何全表 `DELETE` 测试，故**无 wipe 事件、无需 restore 链**。
- 上一轮报告 §3 的 `python -m pytest -q`（2 032 项）**确实**会触发
  `tests/test_task_executor.py` 的 autouse 全表 DELETE（DEFECT-001）。
  本轮**刻意未重跑测试套件**，理由同 DSH §5：该套件具破坏性，
  重跑会再次销毁 DB 状态且**无隔离库**可用。
  **该基线结论标注为「运行本身具破坏性副作用，未在隔离库中执行」**（沿用 DSH EV-08 建议）。
- EV-08 要求的三项补齐中：①「§3 运行前 DB 快照」——上一轮缺失，本轮 §6.1 已为
  **本轮**建立 Before 快照；②「DEFECT-001 事件时间戳」——上一轮缺失；
  ③「wipe 后恢复链」——本轮未发生 wipe，故不适用。

---

## 9. Findings 分类

### BLOCKER

**BLOCKER-01 — 生产标注 prompt 无法表达 composite_unit / shared_material，Material 对象在生产路径结构性不可达**

```text
Frozen Spec ref : Docs/V3_SPEC/20_Document_Pipeline.md:130, 181-185, 378-390, 462, 483
                  （role:"shared_material"、shared_components{material/word_bank/...}、
                    sub_questions[]、depends_on[{type:"material_dependency"}]、
                    "shared material 只输出一次"、"每个 shared material 单独产一个 material dedup_key"）
Observed        : app/domains/task/executor.py::_ANNOTATION_PROMPT_PREFIX
                  · 只给出 standalone_unit 完整示例，无 composite_unit 示例
                  · role ∈ {"stem","option","answer","explanation"}  ← 缺 "shared_material"
                  · 无 shared_components / sub_questions / depends_on / question_number_range 字段说明
                  · 结果：caseB 26 units 全为 standalone_unit；materials=0
Expected        : prompt 实现其自称的 Schema Source of Truth（20 §4.1–4.5）
Actual          : prompt 只实现 standalone 子集
Root cause      : I-0-1 Prompt Contract Alignment 只对齐了 standalone 分支；
                  composite/shared-material 分支未落入 prompt 模板
Blocking stage  : SEMANTIC ANNOTATION（产不出 composite_unit）→ 下游 Compiler materials 恒 0
Cross-check     : 下游能力存在 —— pac-c08-01 经真实 IRBuilder/Compiler 得 materials=8
                  （§7.5），故缺口精确定位在 prompt 层
Classification  : 实现缺陷（实现 vs Frozen Spec）；SPEC CHANGE NOT REQUIRED
Fix policy      : STOP —— 改 prompt 属 V3 production code modification = LIMIT-AUTH §6 Forbidden Scope
```

**BLOCKER-02 — 生产 worker 入口的 live LLM 路径结构性不可达（两层独立原因）**

```text
Frozen Spec ref : 30_Task_LLM_Safety.md（LLMExecutor 唯一入口）；20 §4.1–4.5
Observed        : (a) app/ai/gateway.py::build_gateway 在 mode=="live" 只构造
                    HTTPLLMProvider(name="ollama", api_key=None,
                                   base_url=settings.ollama_base_url, model=settings.ollama_model)
                    —— settings.mimo_api_key / mimo_base_url / mimo_model 存在（config.py:47-49）
                    但未被该 factory 读取；.env 的 ollama_base_url/ollama_model 为空串
                  (b) app/worker/__main__.py:87  build_gateway(allow_live=args.allow_live)
                    —— task_context / budget_ok 走默认 None / False
                    而 LLMGateway._live（gateway.py:60-73）四前置要求：
                    allow_live + task_context is not None + budget_ok + 可解析 live provider
Expected        : --allow-live 下生产入口可发起真实 live 调用
Actual          : 实证 GatewayDeniedError: "live denied: task context missing; budget unavailable"
                  —— 即使把 MIMO provider 正确接线也必然拒绝（与 provider 无关）
Root cause      : gateway factory 未读 MIMO 配置（(a)）；worker 未传 task_context/budget_ok（(b)）
Blocking stage  : SEMANTIC ANNOTATION（生产入口）—— live 调用从未发出
Evidence        : llm_call_audit 仅 1 行 provider='ollama' model='qwen3.5-9b' status='failed'
Classification  : 实现缺陷
Fix policy      : STOP —— 改 build_gateway / app/worker 属 LIMIT-AUTH §6 Forbidden Scope
```

### MEDIUM

**MEDIUM-01 — 选项 per-label 文本 span 不可得，choice 类单元大面积 incomplete**
Observed：caseB 48 条 `role option unresolved`；全语料 producer 侧同源问题
（`OPTION_LABEL_SPAN_UNAVAILABLE`）。Expected：per-label span（`sp-<unit>.option.<label>`）。
Root cause：LLM 只输出 `{label, role, question_label}`（prompt 明令「不要转录正文」），
Resolver 无法仅凭 label 切出选项文本边界。
Classification：**PRODUCER / 证据粒度 GAP**（与 MIMO 报告一致）。
注：Q9 四个选项**成功**解析（`sp-Q9.option.A..D`），故非普适失效，属版式/启发式依赖。

**MEDIUM-02 — 同文档内题号不唯一导致 stem 大面积 unresolved**
Observed：`question N start not unique`（`ambiguous`）。Root cause：真试卷含「试题」与
「参考答案」两段，题号 1..N 重复出现，Resolver 无法消歧。
Classification：**resolver 启发式限制 + 版式**（非数据缺失）。

**MEDIUM-03 — `admission_events.created_instance_ids` 记为 `[None]`**
Observed：event `materialized_at=2026-09-25T16:29:40.214326Z`、
`created_question_ids=[a35743e0-…]`、`created_instance_ids=[None]`，
但 `question_instances` 同事务已物化 `953743dd-…`（`created_at .210316`）。
Expected：记录已物化 instance id。Actual：记 `None`。Root cause：物化事务内 instance id
回填时机缺失。Classification：**audit 完整性缺陷**（不影响物化正确性）。

**MEDIUM-04 — `.env` 的 `MIMO_MODEL` 值不是该 endpoint 支持的模型**
Observed：`MIMO_MODEL=mimo-x-pro-preview` → HTTP 400
`{"error":{"code":"400","message":"Unsupported model mimo-x-pro-preview"}}`。
`GET /v1/models` 返回 9 个模型，含 **`mimo-v2.6-pro`**（= 任务§三指定的 MIMO V2.6 PRO）。
处置：本轮以环境变量覆盖 `MIMO_MODEL=mimo-v2.6-pro` 执行，**未改 `.env`**。
Classification：**测试/配置缺陷**（非生产代码）。

**MEDIUM-05 — `fill_in` / `short_answer` 无 strict-auto grammar，auto_approve 不可达**
Observed：6/6 candidate `admission` 层 fail，`not strict-auto (grammar None)`。
Expected（可争议）：若期望这些题型可自动放行，需 grammar 定义。
Actual：`auto_approve=0`。Classification：**CANONICALIZATION / CONSUMER GAP**
（与 MIMO 报告 NEW-F3 同源）。**注：这同时是任务§10 Case B「Gate 自身阻断」的正面证明。**

### LOW

**LOW-01 — Case B `rejected` 状态迁移未执行（NOT TESTED）**
原因：host auto-mode 权限分类器拒绝 `POST /api/candidates/{id}/reject`
（不可逆 API 状态变更，未获点名授权）。**未绕过**。
已证部分：`pending_review` 态 5/6 天然观测（Gate 阻断）；
`AdmissionService.reject()`（P0-G-003 machine/human 双证据链）代码级已读，
但**未执行**。分类：**NOT TESTED（权限边界）**。

**LOW-02 — producer 数据词表噪声 `andalone_question`**
Observed：全语料 4 609 units 中 1 个 `unit_type='andalone_question'`（缺 `st`）。
与 MIMO 报告「1 unit / 1 doc 拒收」一致。分类：**PRODUCER 词表噪声**；
consumer 侧 fail-loud 拒绝是**正确行为**。

**LOW-03 — 上一轮报告行号漂移 / 个别计数不可复现（EV-11 / EV-12）**
本轮不修改上一轮报告（Reconcile, don't rewrite）；此处登记残余项，
属文档洁净度，按任务§八不阻塞工程验证。

### INFO

**INFO-01 — `AdmissionService.approve()` 是物化 Question/Instance/Material 的唯一入口**
`20 §5.4` 物化事务 + `20 §8.2` 双入口（auto 需 `gate_decision=auto_approve`；
human 需 `review_trail` 含人工确认）。自动化管线在 `pending_review` 停住是**设计行为**。

**INFO-02 — LLM 可能输出超出源文证据的结构声明**
caseA（参考答案卷）中 LLM 仍输出 22 个 unit 的题号/选项标签，Resolver 正确 fail-closed。
建议后续在 prompt 增加「源文无该结构则不得声明」的显式约束（属 prompt 改动 → 需授权）。

**INFO-03 — `run_once()` 返回值语义易误读**
返回 `True` 仅代表「认领并处理了一个 task」，**不是成功指示**；成败须以
`tasks.status` / `task_claims.outcome` 为准。本 harness 首轮即因此误报，已更正并在
artifact 中固化 `run_once_return_semantics` 字段。

**INFO-04 — `LLMGateway.complete()` 直调被 Lock-4 正确拒绝**
缺 `invocation_counter`/`task_id` 时 `GatewayDeniedError: missing invocation_counter/task_id`。
这是**正确**的 fail-closed（`LLMExecutor` 为唯一入口），非缺陷。

---

## 9b. Prior Art / Reconciliation（EV-06 处理）

对照仓内既有独立验证 `Docs/60_REPORTS/MIMO-PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION.md`
（952 行，2026-09-22，Independent auditor MiMo，X2.7 172-manifest 全量）：

| 议题 | MIMO 报告（2026-09-22） | 本次实测（2026-09-26） | 判定 |
|---|---|---|---|
| options 无 per-label span → choice `incomplete` | `PRODUCER GAP`（`:442,:633`） | 生产路径复现：48 条 `role option unresolved`（§7.2） | **一致（CONFIRMED）** |
| Gate `grammar None` → `auto_approve=0` | `CANONICALIZATION/CONSUMER GAP`（NEW-F3） | 6/6 `pending_review`，同 reason（§7.3） | **一致（CONFIRMED）** |
| B2 入口不调用 `AdmissionService` | **「NOT REACHED on B2 entry (by design; lives on runner.py / API)」**（`:410,:625`） | 本次经 **API** `POST /api/candidates/{id}/approve` 成功物化 Question（§5.2/§7.1） | **一致**——上一轮 DEFECT-003 判为「B 类 integration failure」属**定性错误**，应为 **by design** |
| `materials` 178 / leaves 533（71 ADMITTED 上） | `:412-418,:610-613` | 单 manifest 下游 8 materials（§7.5）；生产路径 0（BLOCKER-01） | **规模 + 路径差异**：MIMO 数字来自 preprocessing-consumer 分支 × 71 manifests；本次生产路径受 prompt 限制。**非系统性不可达** |
| 「正式生产链 = TaskExecutor 的 LLM Annotation 路径」 | `:422-423` | **已用真实 live MIMO 执行证实**（task `succeeded`） | **一致并升级为已执行证据** |
| 两个 harness 入口边界深度不一致（NEW-F1） | `:424` | 本次未复评（不同 artifact） | **本次未验证** |
| sub-question 不分解（PRODUCER decomposition GAP） | `:634,:657` | 本次 fixture 无 multi-q composite | **本次未验证** |
| `andalone_question` 词表噪声 | `:633`（1 unit） | 全语料独立复现 1 unit（§4.2） | **一致（CONFIRMED）** |
| 85 v1 manifests 缺 `source_content_sha256` | `:411` | 本次未复评 | **本次未验证** |

**上一轮报告与本报告的关系**：`E2E-VERIFICATION-REPORT.md`（2026-09-25）的执行证据经
DSH 独立复算**基本成立**；其数值口径（EV-01/EV-02）与治理定位（EV-03/EV-04）
不达标。本报告**不改写**该报告，而是：(a) 用本轮实测重算数字并标注 scope；
(b) 补治理定位自检；(c) 在此节做 Prior Art 调和。

---

## 10. Integration Ready — 事实判断

```text
Integration Ready  =  NO
```

逐维事实：

| 维度 | 判定 | 依据 |
|---|---|---|
| 链路可执行性（真实输入→最终对象） | **PASS** | caseB 真试卷 → task `succeeded` → `questions=1` / `question_instances=1`（§7.1/§6.3） |
| 真实 LLM 语义标注 | **PASS** | `mimo-v2.6-pro` 真实 HTTP，`llm_call_audit status=completed`（§5.1） |
| LLM 权威边界 | **PASS** | prompt 明禁转录正文；`FORBIDDEN_FIELDS` 校验通过（`status=valid`）；LLM 不决定 admission |
| Provenance | **PASS** | `source_span`(span_id+line_refs) / `text_hash` / `evidence[]` / `logical_execution_hash`（§6.3/§6.4） |
| Replay / 幂等 | **PASS** | 无非法重复，4 层唯一约束生效（§7.6） |
| DB FK / unique / audit | **PASS**（1 项 audit 缺陷） | 0 orphan；MEDIUM-03 |
| API verification | **PASS** | 真实 HTTP 200（§5.2） |
| Failure / rejection path | **PARTIAL** | Gate 阻断已证；`rejected` 迁移 NOT TESTED（LOW-01） |
| **生产入口可运行性** | **FAIL** | **BLOCKER-02**：live 路径结构性不可达 |
| **Material / composite 覆盖** | **FAIL** | **BLOCKER-01**：生产标注层不可达；仅下游证实可用 |
| Fixture 覆盖度 | **PARTIAL** | 0.016%（L-02） |

**Integration Ready 不成立的决定性原因**（二者任一即阻断）：

1. **BLOCKER-02** —— `app/worker` 生产入口无法发起 live LLM 调用
   （`build_gateway` 不读 MIMO 配置 **且** 未传 `task_context`/`budget_ok`）。
   本次 E2E 依赖验证工具的依赖注入，**不能**等同于「生产入口已可跑」。
2. **BLOCKER-01** —— 生产标注 prompt 表达不了 `composite_unit`/`shared_material`，
   `materials` 在生产路径恒为 0。任务§7「Material 必须进入 E2E」在生产路径**未达成**。

二者均需修改 V3 生产代码，属 `LIMIT-AUTH §6 Forbidden Scope`，故**一律 STOP 报告**，
不自行实施。

---

## 11. 与上一轮的差异摘要

| 项 | 上一轮（2026-09-25） | 本轮（2026-09-26） |
|---|---|---|
| 真实 live LLM | **未跑**（`--allow-live` 被拒） | **已跑**（`mimo-v2.6-pro`，3 次调用，2 completed） |
| 最终 Question 对象 | `questions=0` | **`questions=1` / `question_instances=1`** |
| 生产链 vs harness | 仅 preprocessing-consumer 分支 | **真实 `TaskExecutor` 全链路** |
| Material | 0（结论外推为系统状态） | 下游 **8**（能力证实）；生产 0（精确定位到 prompt） |
| DEFECT-002/003 | 判「B 类 integration failure」 | **更正为 by design**（EV-06 调和） |
| 语料数字 | 「全语料 472+58」（实为 22-manifest 子集） | 全语料 **4 609**（scope 明示） |
| 输入规模 | 88 074 挂 `maintainess\PDF\` | 12 707 已索引 / 88 074 全仓（分列） |
| 治理定位 | 零引用 LIMIT-AUTH | §0 逐条自检 |

---

## 12. 残余问题登记（集中，不另开任务）

按任务§六，LOW 级合并处理，不新建治理体系、不重启 OD-R-01、不扩审计发现：

- LOW-01 `rejected` 迁移 NOT TESTED（权限边界）
- LOW-02 producer `andalone_question` 词表噪声（1 unit）
- LOW-03 上一轮报告行号漂移 / 个别计数不可复现（EV-11 / EV-12）
- L-06 migration 测试未执行（治理边界）
- L-07 历史语料 pipeline 未重跑（治理边界）
- MEDIUM-03 audit event 未记 instance id
- MEDIUM-04 `.env` MIMO 模型名失效
- MEDIUM-05 `fill_in`/`short_answer` 无 strict-auto grammar

---

## 13. 最终结论

```text
E2E STATUS              : PARTIAL
FIRST BLOCKING POINT    : SEMANTIC ANNOTATION — 生产 annotation prompt
                          （app/domains/task/executor.py::_ANNOTATION_PROMPT_PREFIX）
                          表达不了 composite_unit / shared_material
                          → 生产路径 materials 恒为 0（任务§7 未达成）

SECOND BLOCKING POINT   : SEMANTIC ANNOTATION（生产入口）— app/worker/__main__.py:87
                          build_gateway(allow_live=…) 未传 task_context/budget_ok，
                          且 build_gateway 不读 MIMO 配置
                          → live 调用结构性不可达（实证 GatewayDeniedError）

INTEGRATION READY       : NO
```

**一句话**：链路**能真跑通到最终 Question 对象**（已用真实试卷 + 真实 MIMO + 真实
PostgreSQL + 真实 HTTP 证明），但**生产入口**与 **Material 覆盖**两处结构性缺口未补，
且两者都落在 `LIMIT-AUTH §6` Forbidden Scope 内，须由 Owner 裁决后方可实施。

```text
SPEC CHANGE REQUIRED    : NO   （两项 BLOCKER 均为实现 vs Frozen Spec 的实现缺陷）
STOP RAISED             : YES  （BLOCKER-01 / BLOCKER-02 修改均属 Forbidden Scope）
```
