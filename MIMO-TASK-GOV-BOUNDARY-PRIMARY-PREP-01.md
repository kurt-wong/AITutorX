# MIMO CODE TASK — Governance Boundary Adjustment + Primary Path Preparation

```text
Task ID        : MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01
Task Type      : LEVEL 2（治理边界调整；本指令本身即 Owner Decision 记录）
                 + 交付物为文档层变更；本任务不包含业务代码实现
Owner Authority: 本文件由 Owner 于 2026-09-27 下达并 commit；其 commit hash 即该边界变更的记录载体
Scope of this  : 文档层边界收敛 + 主链定义与阻塞记录
Explicitly NOT : 业务代码实现 / Contract 或 Frozen Spec 修改 / 新治理机制
Security       : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## PART 0 — 第一原则

当前最大风险不是架构失控，而是**治理复杂度超过个人项目实际需要**，并已构成执行噪音。

本任务允许：

- 降级非关键规则；
- 合并重复说明；
- 明确权威来源；
- 停用已经造成阻塞的治理机制；
- 让历史报告退出执行路径。

本任务禁止（详见 PART 8 NO-GO LIST）：

- 新建治理层 / Registry / Gate / 审批流程 / 状态机 / 编号体系；
- 移动或重排 `Docs/` 目录结构；
- 修改 `AITutors-v3` 的 Frozen Spec 或 Contract 文本；
- 在本轮写业务代码。

**目标**：把项目从"每一步都要证明自己符合治理"调整为"架构边界需要证明，普通实现靠测试证明"。

---

## PART 0.5 — 第 0 步（必须先做，再动任何东西）

`Docs/60_REPORTS/` 下有两份**未提交**（untracked）的上轮交付物：

```text
Docs/60_REPORTS/GOVERNANCE-SIMPLIFICATION-REVIEW.md
Docs/60_REPORTS/RECOMMENDED-MINIMAL-GOVERNANCE-MODEL.md
```

先单独提交它们（内容不得修改），再做本任务的任何编辑。否则本轮的文档改动会与它们一起悬空、无法追溯。

---

## PART 1 — Path 命名统一（仅文档层）

### 1.1 Frozen Spec 原文一律不动

不得修改 `AITutors-v3/Docs/V3_SPEC/**`（尤其 `90_DOCUMENT_GOVERNANCE.md` 中的 `Native Path` / `Path B` / `ResolvedRun` 定义）。

### 1.2 文档层统一映射

自本任务起，**AITutor-X 文档层**使用下列名称；首次出现时并列写出 Spec 原名：

| 文档层名称 | 对应 Frozen Spec 原名 | 定义 |
|---|---|---|
| **Primary Path** | `Path B` | `Source → preprocessing → Adapter → ResolvedRun` —— 当前目标生产路径 |
| **Fallback Path** | `Native Path` | `Source → Resolver → ResolvedRun` —— 保留路径（备用 / 调试 / 特殊输入） |

### 1.3 约束

- 该映射必须写入 `DOC-GOV`（见 PART 2），使它可以被引用，而不是只存在于本份临时指令中；
- 引用 `AITutors-v3` 或 `PREPROCESSING-V3-CONTRACT` 时，写成 `Primary Path（Spec Path B）` 形式，避免与 Spec 原文冲突；
- 不得把 Fallback Path 当作当前生产链推进；不得因为 Fallback Path 现在能跑就继续扩展它。

---

## PART 2 — 文档治理降级（唯一允许修改的文件）

### 2.1 修改范围

**只允许修改一个文件**：

```text
Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md
```

（该文件 329 行，已含 §1 Authority Levels、§2 Directory Layering、§4 Creation Gate、§6 Terminology、§8 Lifecycle、§10 读取顺序——本任务**改写既有章节**，不追加平行新体系。）

### 2.2 该文件需要的改动（逐项，均为"改写/降级"，非新增机制）

1. **§1 → Document Authority Order（三档）**

   ```text
   Normative          : Frozen Spec（V3_SPEC/）+ 冻结后的 Contract      → 实现约束
   Informative        : Architecture / Design / Implementation 说明      → 用于理解，不自动产生约束
   Historical Evidence: DSH Review / Verification / Closure / Audit 报告  → 仅历史记录
   ```

   并写明：Historical Evidence **不得阻塞**任何 Level 1 实现。

2. **§2 Directory Layering** —— 保持现有目录不动，仅加一句全目录声明：
   **`Docs/60_REPORTS/` 全目录为 Historical Evidence，不构成实现约束。**

3. **§4 Creation Gate** —— 9 项降级为 3 项（与治理审查 §4.1 一致）：

   ```text
   1. 是否修改 Frozen Spec / 核心 Contract？ → YES 则升级 LEVEL 2
   2. 是否包含 secrets？                    → YES 则移除，改用 .env
   3. 放在哪个目录？                        → 按现有层级（不确定就放 60_REPORTS/）
   ```

   删除：authority level 判定、architecture fact 检查、重复 authority 检查、生命周期状态、引用闭包验证。

4. **§6 Terminology** —— 写入 PART 1.2 的映射与并列写法规则。

5. **§8 Document Lifecycle Status** —— 替换为**受限状态词表**：
   - 适用范围仅限**任务/追踪类文档**；
   - 词表：`OPEN` / `CLOSED` / `DEFERRED` / `ARCHIVED`（优先复用既有词，不新增近义状态）；
   - **明确排除**（不得改动、不得重命名）：
     - 产品状态：`admission_candidates.decision_status`（例如 `pending_review`）；
     - Frozen Spec 定义的状态：`semantic_status ∈ {ready, incomplete, unknown}`；
     - `GF-005` 的 OQ 状态（该文件为 `FROZEN GOVERNANCE BASELINE（OD-14）`，本任务不修改它）。

6. **§10 Agent 读取顺序（强制）** —— 降级为**建议**，并给出权威集：

   ```text
   实现任何任务只需读：
     AITutors-v3/Docs/V3_SPEC/20_Document_Pipeline.md
     AITutors-v3/Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
     相关代码
   其余文档一律 Informative / Historical。
   ```

7. **新增一节（不超过 20 行）—— Deprecated Governance Mechanisms**

   声明下列机制**不再作为 LEVEL 1 的开发阻塞条件**：

   ```text
   1. 每个 M-step 独立 Owner Authorization
   2. 每次代码修改必须产出 Closure + Verification + Registry + Evidence Package 完整链
   3. DSH Review 作为每步实现前置
   4. Implementation Queue 必须清零才能继续
   ```

   并写明**效力顺序**（关键）：

   ```text
   上述机制的出处文档（X2.6-01 / X2.6-03 / GF-005 §5 Closure Protocol 等）属 Informative；
   与本文冲突时以本文为准；Frozen Spec 与冻结 Contract 除外。
   本指令（MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01，2026-09-27，
   commit = 以 git 解析为准：
   git log -1 --format=%H -- MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01.md
   注：执行时该值约为 2d934bc…（首次提交），后续若有 amend 以 git 输出为准）
   即为本次治理边界调整的 Owner Decision。
   ```

---

## PART 3 — 历史报告处理

- 允许：把 `60_REPORTS/` 声明为 `Historical Evidence Only`（**通过 PART 2.2 第 2 项的那一句话完成，不逐份加头部**）；
- 禁止：大规模移动目录、重排 `Docs/` 结构、创建 `00_PROJECT` / `30_DEVELOPMENT` / `40_OPERATION` 等新体系；
- 禁止：删除任何历史报告或 evidence。

**理由**：避免把"简化"变成新的治理项目。

（背景数据，供理解，不需执行：`Docs/` md ≈ 175 份，其中 `60_REPORTS` ≈ 104 份；文档间存在 ~96 处 `60_REPORTS` 路径引用——因此本轮不做物理移动。）

---

## PART 4 — Primary Path：定义与阻塞（本任务只记录，不实现）

### 4.1 主链定义（写入 Deliverable 2）

```text
PDF/DOC/DOCX/IMAGE
  → Aitutors-preprocessing（Source Producer）
  → manifest + annotated markdown + semantic metadata
  → V3 ingestion → Resolver → ResolvedRun → IR → Admission
```

等价于 Frozen Spec `90 §H-C` 的 `Path B`；本任务统一称 **Primary Path**。

### 4.2 已核实的阻塞（必须原样记录，并标注文件/行号）

```text
B1  preprocessing 产物 .md/manifest 无法进入正式 import
    AITutors-v3/backend/app/domains/source/import_service.py:26
    _ALLOWED_EXTENSIONS = {".pdf", ".docx"}

B2  consumer 永不持久化（只做事务内校验后 rollback）
    AITutors-v3/backend/scripts/preprocessing_consumer/runner.py:296, :317
    finally: await session.rollback()

B3  identity 缺失 → consumer fail-closed
    fresh manifest 顶层键仅 source_file / model / annotation_meta / units
    无 source_content_sha256 / identity_version
    consumer 返回 MISSING_IDENTITY，downstream_executed = false

B4  即使补上 identity，下游仍停在 IR
    identity-complete 样本 Track A：candidates_created=0，skipped = 53/53
    （成因目前只有断言、无 per-unit 证据；且唯一通过过 gate 的样本 model tag 为
     mimo-x-pro-preview，属迁移前历史产物）
```

### 4.3 必须写进报告的三个事实边界

1. **identity 字段已存在**：定义于 `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` §0.1 ①（键名 `source_content_sha256`，64 位小写 hex）。该 Contract 文本自身标注为 **DRAFT / NOT FROZEN**。缺的是 **producer 侧实现**，不是契约文本 → 本任务**不写、不改任何 Contract**。
2. **生产者有两棵代码树且已分叉**：
   ```text
   D:\Project\Papers                 = git 仓（remote: github.com/kurt-wong/Aitutors-preprocessing.git）
   D:\Project\Aitutors-preprocessing = 无 .git 工作树副本
   两棵都不写 source_content_sha256；_redact() 与非 429-4xx 立即失败分支仅副本有
   ```
   → **权威树尚未裁决**，因此本任务**不提交任何 producer 代码**。
3. **现有全部下游证据来自 Fallback Path**：ENABLEMENT-03 的 13 个 `admission_candidates`（全部 `pending_review`）由 `POST /api/documents/import` + worker CLI 产生，即 **Fallback（Native）Path**。**不得**把它们当作 Primary Path 的证据。

---

## PART 5 — 代码授权边界（本轮 = 不写代码）

| 级别 | 内容 | 本轮 |
|---|---|---|
| **LEVEL 1** | bug fix / 测试补充 / provider 修改 / 已定义字段实现 / integration 修复 | **本轮不做**（下一轮） |
| **LEVEL 2** | 修改 Frozen Spec、修改架构边界、修改 Primary/Fallback 定义、**引入新的持久化机制** | 需 Owner Decision |
| **LEVEL 3** | Migration、数据迁移、不可逆操作 | 保持现有严格治理 |

**下一轮（Primary Path Identity Enablement）开工前必须先取两个 Owner 决定**：

1. 生产者权威树 = `Papers` 还是 `Aitutors-preprocessing`？（影响 commit 归属与 PART 6 的 evidence 可行性）
2. 是否引入**持久化** ingestion 入口？（B2；属 LEVEL 2。不决定则 Primary Path 只能停在 gate accepted，无法持久到达 `ResolvedRun`。）

---

## PART 6 — 禁止事项（NO-GO LIST）

```text
Architecture
  ❌ 修改 Frozen Spec / Contract 文本
  ❌ 新建架构层 / Gate / Registry / Contract / 生命周期状态机 / 编号体系

Governance
  ❌ 新增 Owner Decision 流程、Closure 流程、审批流程
  ❌ 修改 GF-005（FROZEN GOVERNANCE BASELINE, OD-14）的任何 Status 或正文

Primary Path（本轮）
  ❌ 人工修改 manifest 以补齐 identity
  ❌ 使用目录名 / path 作为 identity
  ❌ 绕过 enforce_interface_scope / consumer gate
  ❌ 修改测试断言使测试通过
  ❌ 伪造授权（hardcode budget_ok / dummy task_context）；authorization 必须来自真实 Task + budget 检查
  ❌ 为验证 Fallback Path 而阻塞 Primary Path 工作

Repository
  ❌ 修改 AITutors-v3 工作树（本任务对 v3 应 0 改动）
  ❌ 修改 Papers 工作树（同上）
  ❌ 自动删除历史文件 / 自动迁移仓库 / 自动 git init / 自动合并两棵 producer 树
  ❌ 移动 Docs 目录或重排目录结构

Output
  ❌ 新 Registry / Gate / Closure 文件 / 审批流程
  ❌ 为本轮工作自行发起 DSH 审查（评审由 Owner 决定）
```

---

## PART 7 — 交付物（恰好两份）

### Deliverable 1 — 修改后的 `Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md`

按 PART 2.2 的 7 项执行。**不新建平行文件、不追加新治理层。**

### Deliverable 2 — 一份简短说明（≤2 页，建议放 `Docs/60_REPORTS/`）

必须包含且只需包含以下小节：

```text
1. Current Authority Model            （三档权威顺序，引自 Deliverable 1）
2. Primary Path Definition            （含 Spec 原名 Path B 的并列写法）
3. Fallback Path Definition           （含 Spec 原名 Native Path 的并列写法）
4. Deprecated Governance Practices    （PART 2.2 第 7 项的 4 条 + 效力顺序）
5. Remaining Business Blockers        （PART 4.2 的 B1–B4，含文件:行号）
6. Next-Task Prerequisites            （PART 5 的两个 Owner 决定）
7. Verification                       （见 PART 8 的机械检查结果 + commit hash）
```

---

## PART 8 — 验收标准（机械可查）

**文档层**

```text
[ ] AITutors-v3 工作树 0 改动（git status --porcelain 无 modified tracked）
[ ] Papers 工作树 0 改动
[ ] AITutorX/Docs 仅 DOC-GOV 一个文件被修改 + Deliverable 2 一个新文件
[ ] Frozen Spec 6/6 hash 未变，并在 Deliverable 2 中列出这六个文件的值：
    AITutors-v3/Docs/V3_SPEC/00_Master_Spec.md
    AITutors-v3/Docs/V3_SPEC/10_Data_Model.md
    AITutors-v3/Docs/V3_SPEC/20_Document_Pipeline.md
    AITutors-v3/Docs/V3_SPEC/30_Task_LLM_Safety.md
    AITutors-v3/Docs/V3_SPEC/40_Development_Rules.md
    AITutors-v3/Docs/V3_SPEC/50_Migration_Assets.md
[ ] Contract 文件 hash 未变
[ ] 无新增 Registry / Gate / Contract / 状态机 / 目录
[ ] 历史报告仍全部保留（60_REPORTS 文件数不减）
```

**执行层** —— 执行者必须能直接回答这四问（答案即为验收）：

```text
1. 当前生产路径是什么？        → Primary Path（= Frozen Spec Path B）
2. Native Path 如何定位？      → Fallback Path（保留，不阻塞主链）
3. 哪些文档约束实现？          → Frozen Spec + 冻结后的 Contract
4. 哪些文档只是历史？          → DSH / Verification / Closure / Audit 报告
```

---

## PART 9 — Evidence 与输出形状（本轮的最低要求）

```text
Implementation → Test（如有）→ Evidence

Evidence 最低要求（仅此四项）：
  commit hash
  input（改了哪些文件）
  output（Deliverable 1 / 2 的路径）
  test result（本任务无代码改动时写 "no code change"）
```

**禁止**新增 Evidence Registry / Evidence Gate / Evidence Lifecycle。

**并且，本任务同时确立今后 LEVEL 1 轮次的输出形状**（写入 Deliverable 2 的第 4 节即可，不必另立文档）：

```text
LEVEL 1 一轮 = 代码提交 + 测试输出 + ≤2 页说明
不再产出：报告 + 证据包 + Closure + Verification + Registry 的"五件套"
不再默认配 DSH 独立对抗评审（评审仅在 LEVEL 2 / LEVEL 3 轮次进行）
```

---

## 完成后

下一轮为 **Primary Path Identity Enablement**，其开工前提见 PART 5 的两个 Owner 决定。

不要提前扩展 Fallback Path；不要重新设计治理体系；不要因为历史冗余代码而恢复 Frozen Spec 中不存在的业务链。
