# MIMO CODE TASK — Phase 1 Implementation Authorization + Minimal Real E2E Loop

```text
Task ID        : MIMO-TASK-PHASE1-MINIMAL-E2E-01
Task Type      : LEVEL 1（实现 + 真实运行验证）；本指令本身即 Owner Decision 记录
Owner Authority: 本文件由 Owner 于 2026-10-01 下达；其 commit hash 即该授权的记录载体
                 commit = git log -1 --format=%H -- MIMO-TASK-PHASE1-MINIMAL-E2E-01.md
Scope of this  : 让 Primary Path 在真实源文件与真实数据库上跑通一次，并留下真实记录
Explicitly NOT : 修改 Frozen Spec / 修改 A8 / 开启 Migration / 全量迁移代码入本仓库 / 新增治理机制
Security       : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## PART 0 — 第一原则（本任务的方向改变）

从 2026-09-27 的 `MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01` 起，项目已进入治理收敛；此后
`E2E-01`、`A8`、`ARTIFACT-READINESS-ASSESSMENT-01` 继续以文档方式推进。

**本任务起，方向改变：**

```text
旧重心：Governance Hardening Phase
        —— 继续证明"每一步都符合治理"

新重心：Controlled Implementation Validation Phase
        —— 证明"设计可以承载真实数据"
```

判据（Owner 陈述，本任务以此为准）：

| 结果 | 判定 |
|---|---|
| 500 页 Frozen Spec + 100 份 Decision Record + **0 道真实试题入库** | 项目失败 |
| 约 80% 解析准确率 + 少数人工修正 + **1000 道题入库并可查询** | 项目成功 |

因此：

- 治理文档**不再**是本轮工作对象，而是**约束条件**；
- 本轮的产出必须是**真实数据库记录**，不是报告；
- 允许业务级缺陷（OCR 不准、少量切分失败、知识点关联不准、UI 缺功能）；
- **不允许**架构腐烂（数据不可追踪、重跑污染、Question/Instance 混淆、LLM 覆盖事实）。

**默认停止**（除非真实运行暴露架构问题）：Artifact Readiness 后续讨论、新 Decision Record、
新 Errata、Frozen Spec 微调、文档一致性扫描。

### 0.1 随本指令一并下达的两项 Owner 决定（2026-10-01）

```text
OD-P1-A  LEVEL 2 不预授权。
         若执行中发现"必须引入新的持久化机制"或"必须新建统一入口"才能落库，
         不是"先做再报"，而是**停下、保留现状、上报 Owner**。
         本条把 PART 2.1 / PART 2.3 / PART 6 B 类从"边界描述"升级为"明确裁定"。

OD-P1-B  数据库僵尸状态 = 标记，不删除。
         7 个 running / 3 个 queued / 15 条 task_claims（停在 2026-09-30）一律标记为
         interrupted / expired，保留全部行与 1213 条 llm_call_audit 现场。
         禁止清库重来（会抹掉现场，且属不可逆操作 = LEVEL 3）。
```

---

## PART 1 — 当前事实基线（Step 0 必须自行复核，不得引用本表代替复核）

### 1.1 仓库 HEAD（2026-10-01 观测）

| 角色 | 路径 | 分支 | HEAD |
|---|---|---|---|
| 治理 / 交付目标 | `D:\Project\AITutor-X` | `main` | `7bce066` |
| Consumer（V3） | `D:\Project\AITutors-v3` | `od01-r3-convergence` | `39840ff`（**已与 origin 同步**） |
| Producer（preprocessing） | `D:\Project\Papers` | `main` | `969d39a` |

> `D:\Project\Aitutors-preprocessing`（无 `.git`）是 `Papers` 的非版本化副本，**不是权威树**，
> 不得提交、不得 `git init`、不得作为运行入口。
>
> `CURRENT_STATE.md`（2026-09-27）§4 记 V3 为 `3bf7a09`「origin 落后 4 个 commit」，
> 该记录**已过期**：现 HEAD `39840ff` 与其上游 `origin/od01-r3-convergence` 一致。
> 该更正以本指令为准登记；**本轮不改写 `CURRENT_STATE.md`**（避免又一轮文档维护）。

### 1.2 Primary Path 能力状态

| 能力 | 状态 | 证据 |
|---|---|---|
| Producer identity 输出 | DONE | `b2266d2`：`source_content_sha256` + `identity_version: 2` |
| Option span 展开 | DONE | `969d39a`：`_expand_option_spans()` → `options: [{label,start_line,end_line}]` |
| Consumer per-option 消费 | DONE | `3bf7a09`：`manifest_reader` / `annotation_adapter` / `resolved_span_adapter` |
| Persistence（最小开启） | DONE（代码） | `runner.py:314,:335` 成功路径 `commit()`；异常路径 `rollback()` 保留 |
| **真实数据库落库** | **PENDING** | 需要一次带真实 DB 的运行（本任务） |
| Gate → Candidate → IR → Admission | PENDING | 待落库后推进 |
| Frontend | NOT IMPLEMENTED | 无 Question / Material / Instance API |

### 1.3 真实数据库状态（`DATABASE_URL` 指向 `localhost:5432/aitutors`，2026-10-01 只读探测）

```text
alembic_version              0011（26 张表齐全）
documents                    0
document_source_versions     0
document_active_sources      0
admission_candidates         0
questions                    0
question_instances           0
knowledge_nodes              0
validation_events            0
admission_events             0
tasks                        16（running 7 / queued 3 / interrupted 3 / succeeded 3，全部停在 2026-09-30）
task_claims                  15
llm_call_audit               1213（历史）
```

**由该探测得出的两条硬结论：**

1. **系统至今没有任何一道题进入数据库。** 这是本任务存在的唯一理由。
2. **数据库里留有上一轮的僵尸状态**（7 个 `running`、3 个 `queued`、15 条 `task_claims`）。
   新运行前必须显式处置（见 PART 3 Step 0），处置方式必须记录——**不得静默忽略**。

### 1.3.1 上一轮 PART 4.2 四条阻塞项的当前去向（**勿沿用旧状态，否则会重复劳动**）

| 旧编号 | 旧描述 | 现状态 |
|---|---|---|
| B1 | `.md`/`.manifest.json` 无法进入正式 import（`import_service.py:26`） | **仍 OPEN** |
| B2 | consumer 永不持久化（只校验后 rollback） | **已解除** —— `3bf7a09` 改为成功路径 `commit()`（`runner.py:314,:335`）；**但真实落库仍未验证** |
| B3 | identity 缺失 → consumer fail-closed | **已解除** —— Papers `b2266d2` 输出 `source_content_sha256` + `identity_version: 2` |
| B4 | 即使补上 identity，下游仍停在 IR（candidates_created=0, skipped 53/53） | **部分推进** —— `969d39a`+`3bf7a09` 后 IR 达 17/17 ready（`PRIMARY-PATH-MINIMAL-LOOP-01.md`）；candidate 落库未验证 |

### 1.4 真实试卷输入（已存在，无需 Owner 提供）

| 位置 | 内容 |
|---|---|
| `D:\Project\Papers\original\BaiduSyncdisk\{高一,高二,高三}\<year>\<考试类型>\<学科>\` | **真实北京试卷主库**。高一子树实测 17,164 文件 = 9,663 `.pdf` + 7,441 `.docx` + 60 `.doc`，覆盖 2018–2026 / 期中期末 / 月考 / 分班考 / 合格考 / 汇编 |
| `D:\Project\Papers\original\{高一,高二,高三}\` | **空目录**（勿当作输入源；真实数据在上一行的 `BaiduSyncdisk\` 下） |
| `D:\Project\Papers\Ocr-markdown\高一\数学\` 等 | 已有 OCR/预处理产物的分级语料 |
| `D:\Project\Papers\Ocr-markdown\reslice-p2-b1\` | 现有 consumer 默认语料（`runner.py:366`） |
| `e2e_run\inputs\caseA_real.pdf` `caseB_real_exam.pdf` | 既有 E2E 用 PDF（provenance 需标注，非北京主库来源） |

**首轮输入选择规则**：选**一份**真实北京试卷，例如
`Papers\original\BaiduSyncdisk\高一\<年>\月考\<学科>\*.pdf`（同目录下常有 `.docx` 孪生件，
**优先选 `.pdf`**，因为 `import_service.py` 的白名单是 `{.pdf, .docx}`）。

报告中必须写明其**确切路径 + 字节数 + sha256**。若该文件无法进入当前管线，
可改用同卷的 `.docx`，或改用 `Ocr-markdown` 下已有产物，并说明原因
——**不得为了跑通而伪造源**。

### 1.5 环境

```text
PostgreSQL        127.0.0.1:5432 可达；service 运行中
Python            3.12.9（系统解释器已有 asyncpg / sqlalchemy / pydantic / fastapi / alembic）
V3 .env           APP_ENV=development, LLM_GATEWAY_MODE=live, OCR_GATEWAY_MODE=disabled
                  DATABASE_MODE=fresh_test（含义待确认——见 PART 3 Step 0）
                  MIMO_MODEL=mimo-v2.6-pro
                  .env 已被 .gitignore 忽略，未被跟踪（已核实）→ 不得提交、不得粘贴进任何产出物
Consumer 入口     backend/scripts/preprocessing_consumer/runner.py（CLI: --corpus / --output）
```

> **凭据纪律（硬约束）**：`.env` 中为 live 凭据。报告中只能写键名，**不得写值**；
> 不得复制到 `AITutor-X`，不得出现在 evidence / 日志摘录 / commit message。

---

## PART 2 — 授权边界

### 2.1 分级（继承 `MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01` PART 5）

| 级别 | 内容 | 本轮 |
|---|---|---|
| **LEVEL 1** | bug fix / 测试补充 / 已定义字段实现 / integration 修复 / **真实运行并落库** | **✅ 授权（不必再申请）** |
| **LEVEL 2** | 修改 Frozen Spec / 架构边界 / Primary-Fallback 定义 / **引入新的持久化机制** | 需 Owner Decision；**本轮不授予** |
| **LEVEL 3** | Migration / 数据迁移 / 不可逆操作 | 保持严格治理；**本轮不授权** |

### 2.2 本任务明确授权

```text
1. 在 AITutors-v3 与 Papers 中做 LEVEL 1 代码修改并提交到各自权威树；
2. 在真实 PostgreSQL 上执行 Primary Path（可为新运行建立新 document/task，不修改既有行）；
3. 处置 PART 1.3 的僵尸 task 状态（方式须记录；推荐标记，不删除）；
4. 对真实试卷运行 preprocessing → V3 consumer，消耗真实 LLM 预算（额度充足：limit 100）；
5. 产出代码 + 测试 + ≤2 页说明（见 PART 7）。
```

### 2.3 本任务明确**不**授权（误判风险最高的一条）

```text
❌ 修改 A8（OWNER-DECISION-A8-ENTRYPOINT-AUTHORIZATION-01）
   A8 当前 Status=OPEN / PENDING-OWNER-SIGNATURE / 取向 B1（不授权统一入口）。
   本任务不签 A8、不改 A8、不把 A8 当作已裁决，也不为 A8 补写任何内容。

   术语边界（本条最易误伤，执行前必须读懂）：
     · 消费侧 Track A 调用生产 GateService，是**既存代码**（`runner.py:277` 注释明载），
       不是"接线"动作，因而不受 A8 约束，本任务可正常运行它。
     · A8 禁止的是去**新建**统一入口（M1–M5 ↔ GateService/AdmissionService 的正式语义前接线）。
       本任务**不新建任何入口**，不新增语义前，不扩 GateService 接口。
     · 若真实运行表明落库**只能**通过新建统一入口实现，则停止并上报 Owner
       —— 那属 LEVEL 2，不属本轮范围。
```

```text
❌ 修改 Frozen Spec（AITutors-v3/Docs/V3_SPEC/**，6 份）
❌ 修改 PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md 或任何 Contract 文本
❌ 修改 GF-005 / GF-006（FROZEN GOVERNANCE BASELINE, OD-14）
❌ 开启 Migration Gate / 把 V3 或 Papers 代码拷入 AITutor-X
❌ 新建 Registry / Gate / Contract / 状态机 / 编号体系 / 审批流程
❌ 新增 Decision Record / Errata / 文档一致性扫描（除非 PART 6 触发）
❌ 修改测试断言使测试通过；伪造 budget/task_context；绕过 enforce_interface_scope
❌ 静默跳过 UNKNOWN；用目录名或路径充当 identity
❌ 在 D:\Project\Aitutors-preprocessing（非版本化副本）上运行或提交
```

---

## PART 3 — 执行序列

> 每一步都必须有**可观测输出**。步骤失败时**不得静默降级**：记录 per-item 证据后进入下一缺陷项。

### Step 0 — 基线快照（先做，且必须先于此后的任何写入）

```text
0.1 记录三个仓库 HEAD 与 git status --porcelain（Papers 现有 2 个未跟踪 data/logs 文件，须先判断归属）
0.2 运行现有测试并记录原始输出：
      Papers  : pytest（基线 339 passed, 1 xfailed）
      V3      : pytest（基线 2034 passed, 1 skipped, 1 xfailed）
0.3 只读探测数据库计数（本任务 PART 1.3 的九个表 + budget）
0.4 处置 7 running / 3 queued / 15 task_claims 的僵尸状态（**方式已由 OD-P1-B 裁定**）：
      标记为 interrupted / expired 并记录 ID 列表；**不删除、不清库**
      并确认 DATABASE_MODE=fresh_test 的真实语义（读代码确认，不要猜）
0.5 记录所选真实试卷路径 + sha256 + 字节数
```

**Step 0 产出即"改动前事实"，不得事后回填。**

### Step 1 — Producer：真实试卷 → manifest

```text
入口：Papers（权威树 D:\Project\Papers，main）
动作：对所选真实试卷运行 preprocessing，产出 manifest + annotated markdown
必须验证（逐项给数值，不给结论词）：
  · manifest 顶层含 source_content_sha256 与 identity_version == 2
  · units 数量
  · 每 unit 的 options 是否为 per-label span（不是 options_lines 整段区间）
  · 页码 / 图片引用是否保留
  · 题号是否稳定（与源文件人工抽样对照 ≥5 题）
契约：不得修改 Contract；如 producer 输出与 Contract 不符，记录差异，不改 Contract
```

### Step 2 — 落库入口（这是当前唯一真正的堵点）

```text
现状：B2 = consumer 曾只做事务内校验后 rollback（已在 3bf7a09 改为成功路径 commit）
      B1 = import_service.py:26 _ALLOWED_EXTENSIONS = {".pdf", ".docx"} 不允许 .md/.manifest.json
要求：把 manifest 走通到**真实持久化**，并回答：
      · 本次落库走的是哪条入口（consumer runner？import API？）
      · documents / document_source_versions / document_active_sources 是否出现真实行
      · 重跑同一输入是否产生重复行（idempotency 实证，不是断言）
若 B1 必须改：属 LEVEL 1（放宽已定义入口的扩展名白名单）**或** LEVEL 2（若引入新持久化机制）。
     执行前先判定并写明判定理由；判为 LEVEL 2 则按 OD-P1-A **停下上报，不先做后报**。
```

### Step 3 — Semantic Annotation（LLM 首次介入）

```text
原则（Owner 定，不得越界）：
  LLM 负责：语义解释、标签建议、知识关系建议
  LLM 不负责：最终切题边界、唯一身份、相似性判定
验证：真实 LLM 调用次数、llm_call_audit 新增行数、budget used 增量、失败与重试次数
边界：OCR_GATEWAY_MODE=disabled 时不得假装有 OCR 结果；缺 OCR 就如实标注
```

### Step 4 — Compiler → Question IR

```text
期望形状（Owner 明确接受非 100%）：
  100 units → 80 IR → 70 question candidates；其余 pending_review
必须给出：ready / incomplete / unknown 三态计数，以及每个 incomplete 的 reason
禁止：把 incomplete 当 ready；把 skipped 计数写成"通过"
```

### Step 5 — Admission / Candidate 落库

```text
必须验证：admission_candidates 出现真实行（status 可为 pending_review）
边界：Gate auto_approve 仅覆盖 {single_choice, multiple_choice, true_false}（Owner 裁决 2026-09-06）；
      short_answer / essay 走 pending_review 属 BY DESIGN，不算失败
禁止：为了得到 candidate 而放宽 auto_approve 范围
```

### Step 6 — 最小知识关联

```text
只要求：knowledge_nodes + question_knowledge_links 出现真实行，
        且能从"学科 → 章 → 节 → 题目 ID 列表"查询出结果
不要求：图谱算法、embedding 质量、覆盖率指标
```

### Step 7 — 固化与报告

```text
· 代码提交到各自权威树（Papers main / V3 od01-r3-convergence），测试输出附上
· ≤2 页说明（PART 7）
· 不改 Frozen Spec、不改 A8、不动 Docs 目录结构
```

---

## PART 4 — 验收标准（机械可查）

**必须为真（缺一即未完成）**

```text
[ ] 至少一份**真实**试卷走完全链（Step 1 → Step 6）
[ ] documents                              ≥ 1 行真实记录
[ ] document_source_versions               ≥ 1 行，且与源文件 sha256 对应
[ ] admission_candidates                   ≥ 1 行（pending_review 亦计入）
[ ] questions 或 question_instances        ≥ 1 行
[ ] 全链 provenance 可追：每行可回溯到 source_content_sha256
[ ] 未完成项以 per-item reason 记录（不得静默丢弃）
[ ] 重跑同一输入的 idempotency 结论（有实证，非断言）
[ ] Papers / V3 测试基线不退化；Frozen Spec 6 份 hash 未变；Contract hash 未变
[ ] A8 文件 hash 未变；Docs 目录未增删
```

**明确不要求（不得作为未完成理由）**

```text
· 100% 解析准确率
· 全部题型都进 auto_approve
· 前端展示
· 知识图谱质量指标
· 任何新增治理文档
```

**四问验收（与上一轮同形）**

```text
1. 真实试卷从哪来、sha256 是多少？      → 具体路径 + hash
2. 数据库里现在有什么？                → 九个表的真实计数
3. 卡在哪、为什么、下一步是什么？       → per-item 证据
4. 架构边界有没有被真实运行推翻？       → 有/无 + 证据
```

---

## PART 5 — 硬约束（违反任一条即本轮失败）

```text
1. 不得静默跳过 UNKNOWN / 不得 fallback 掩盖失败（AGENTS.md 核心原则 2）
2. 不得修改测试断言使其通过
3. 不得伪造授权（hardcode budget_ok / dummy task_context）；authorization 必须来自真实 Task + budget
4. 不得用目录名或 path 充当 identity
5. 不得绕过 enforce_interface_scope / consumer gate
6. 不得在 D:\Project\Aitutors-preprocessing（副本）上运行或提交
7. 不得把 .env 的值写进任何产出物；不得把 .env 复制出 AITutors-v3/backend
8. 不得为跑通而放宽 gate / auto_approve / identity 校验
9. 不得删除历史文件、不得移动 Docs 目录、不得整仓拷贝
10. 不得在本轮开启 Migration 相关任何 Gate
```

---

## PART 6 — 必须记录的发现（超出实现范围的两类触发）

```text
A 类（正常）：业务缺陷（切分错、OCR 错、关联错）→ 记入报告"发现的问题"表，不在本轮修
B 类（触发上报）：架构级问题 —— 例如
   · 真实运行表明落库**必须**依赖 M1–M5 ↔ GateService/AdmissionService 统一入口（与 A8 B1 冲突）
   · 必须引入新的持久化机制才能落库（LEVEL 2）
   · 重跑污染数据库（违反 PART 0 不可接受项）
   → 触发即停：不自行决定，不新开 Decision Record，**上报 Owner 并保持现状**。
```

---

## PART 7 — 输出形状（本轮唯一交付形状）

```text
代码提交（Papers / V3，各自权威树）
  + 测试原始输出
  + ≤2 页说明（建议 Docs/60_REPORTS/，Historical Evidence，不新增治理层）

说明只需含 6 节：
  1. Input Provenance     所选试卷路径 + sha256 + 字节数；producer commit
  2. Run Record           执行命令、时间、环境（键名不含值）
  3. DB Delta             改动前 / 改动后 九表计数对照（真实查询结果）
  4. Funnel                units → IR(ready/incomplete/unknown) → candidates → questions
  5. Discoveries          A 类问题表 + B 类触发（如有）
  6. Verification         测试结果 + Frozen Spec 6 hash + Contract hash + A8 hash

禁止：报告 + 证据包 + Closure + Verification + Registry 的"五件套"。
```

**DSH 独立对抗评审：默认不执行**，仅 Owner 明确要求时执行。执行方不得自行发起。
（此条继承上一轮 PART 9，继续有效。）

---

## PART 8 — 下一轮（不在本任务内，仅为定位）

```text
本轮完成后，下一轮大概率是其中之一（由真实运行结果决定，现在不预设）：
  · 解析准确率提升（针对本轮记录的业务缺陷）
  · 规模化：从 1 份试卷 → 10 份 → 目标 1000 题入库
  · Frontend：Question / Material / Instance API
  · OCR 接入（当前 OCR_GATEWAY_MODE=disabled）
Migration 仍然不在视野内：迁移阻塞的是"把两个仓库搬入 AITutor-X"，
不阻塞在来源仓库中继续实现 Primary Path（已由 969d39a + 3bf7a09 实证）。
```

---

## 完成后

**不要再审文档。** 本轮的完成定义是：数据库里出现了真实可追溯的试题记录，
以及一份说清"卡在哪、为什么、下一步"的短说明。

```text
若真实运行证明架构能承载真实试卷 → 项目进入规模化阶段
若真实运行推翻架构假设      → 按 PART 6 B 类上报，由 Owner 裁决
两种结果都是有效结果；唯一无效的结果是"又写了一份文档"。
```
