# FU-05 — `source_authority_state` 值域裁决输入

```text
Document Type : Decision Preparation Record（非 Authority Decision）
Status        : OPEN
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 1 (2026-09-28)
Date          : 2026-09-28
Authority     : —（本文不构成任何 Authority；**不批准任何值域**）
Parent        : Docs/40_DECISIONS/OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01.md §A.1.4
                （`[OWNER DECISION REQUIRED]` 项）
Input         : Docs/60_REPORTS/FU-05-AUTHORITY-TAXONOMY-MAPPING-TABLE-PREP.md @ b8dce53
Temporal Scope: Current-state facts verified as of 2026-09-28.
readers       : Owner（裁决方）；FU-05 Mapping Table Draft 作者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 非授权声明

```text
本文不是 Authority Decision。
本文【不批准任何值域】。
本文不修改 §A.1.4 / §A.2 / 任何已签发或已形成的 Decision 内容。
本文不修改 V3 `90` / `91` / `20` / 任何 Frozen Spec。
本文不修改 AITutor-X DOC-GOV §8 状态词表。
本文不触发 Migration / GF-007 / Gate 批准。
本文只做两件事：
  ① 把【在两仓实际出现过的状态词】逐值归属到其 namespace；
  ② 把 `source_authority_state` 的语义域边界问题摆清。
```

---

## 1. Scope

```text
范围（唯一）：`source_authority_state` 的【语义域边界】与【候选值归属】。

不做：
  · 不选 Option（Q1 由 Owner 裁）
  · 不定值域（值域由 Owner 批准后才回填 §A.1.4）
  · 不进入 §A.2 Mapping Table Draft
```

**为什么不能直接给值域**（本文的存在理由）：

```text
当前问题不是「缺少一个枚举」，而是【namespace 未分离】。
两仓在用的状态词至少来自 9 个不同语义域（见 §2）。
直接定义 {proposed, approved, pending, …} 会立即与既有域混淆。
```

---

## 2. Facts — 两仓在用的状态词表（逐源列举）

### 2.1 V3 `91 §3.1` 允许的状态值 —— **冻结集合，10 值**

```text
载体：AITutors-v3/Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md:107-122
标题：「## 3. 状态词（冻结集合）」
```

| 值 | 含义（原文） | 适用层 |
|---|---|---|
| `OPEN` | 已登记，未解决 | 全部 |
| `PENDING` | 等待外部条件 | 全部 |
| `CONDITIONAL PASS` | 部分满足，残留项显式列出 | L3 Gate |
| `CLOSED` | **满足其声明的定义条件**（须带范围限定） | L3 Gate |
| `NOT STARTED` | 未开工 | 全部 |
| `DEFERRED` | 显式延期，不视为失败也不视为完成 | 全部 |
| `SUPERSEDED` | 已被他文废止（正文保留） | 全部 |
| `RETRACTED` | 本文件自己撤回的结论 | L4 |
| `ACTIVE` | 现行有效 | 全部 |
| `HISTORICAL` | 历史记录，非现行 | 全部 |

**`91 §3.3`**：`CLOSED` 不得单独出现，须写 `CLOSED — <范围限定>（依据 82 §3，日期）`。

### 2.2 V3 `91 §3.2` 禁止的状态词（新文档）

```text
COMPLETE（现存量 6 份）· DONE（1 份）· FINISHED（0 份）· NEXT（不是状态）· REVIEWED（3 份）
```

### 2.3 V3 `90:594` Status 模板值域 —— **6 值**

```text
载体：AITutors-v3/Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:594
  Status: <ACTIVE | SUPERSEDED | HISTORICAL | DRAFT | CLOSED | NOT RELEASED>
```

### 2.4 V3 OD-01-H 治理状态词 —— **5 值**

```text
载体：AITutors-v3/Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md:421
  「删除模糊完成类状态词（91 §3.2）；仅用
    APPROVED / PENDING / VERIFIED / NOT EFFECTIVE / NOT REGISTERED」
```

### 2.5 V3 在用但**未登记**于任何冻结集合的值

| 值 | 出现位置 | 备注 |
|---|---|---|
| `ACCEPTED` | `90:374`「Review（2026-09-24，Owner）：**ACCEPTED / EFFECTIVE**」 | **不在 91 §3.1 十值内** |
| `EFFECTIVE` | `90:41`「`CR-003` · `CR-004`（2026-09-24 起 EFFECTIVE）」 | 不在 91 §3.1 十值内 |
| `NOT RELEASED` | `90:594` 模板；`90:579`；`CR-003:45` | 在 90 模板内、**不在** 91 §3.1 |
| `DRAFT` | `90:594` 模板 | 在 90 模板内、**不在** 91 §3.1 |
| `Candidate` | OD-01-C「CR-002 保持 COORDINATION；NOT EFFECTIVE / Candidate」 | 未登记 |
| `PENDING RATIFICATION` | `90:275`（标为"未采纳"） | 未采纳 |
| `OWNER APPROVED RECORD` / `PENDING EFFECTIVE FREEZE` | OD-01-I:422 | 未登记 |

### 2.6 V3 其他**已冻结的独立状态域**

| 域 | 值域 | 载体 |
|---|---|---|
| `semantic_status` | `{ready, incomplete}`（**值域冻结 · BUG-V3-018 终裁**） | `20_Document_Pipeline.md:394` |
| `gate_decision` | `auto_approve / pending_review / …` | `20_Document_Pipeline.md:397` |
| `Registration Level` | `NOT REGISTERED` / `REGISTERED AS L1` | `CR-002:18/65`；`CR-003:322`；`CR-004:303` |
| Contract 冻结叙事 | `DRAFT / READY FOR FREEZE / NOT FROZEN` | Contract 文首（CL-01） |

### 2.7 AITutor-X 侧状态词表

| 域 | 值域 | 载体 |
|---|---|---|
| 文档生命周期 Status | `OPEN` / `CLOSED` / `DEFERRED` / `ARCHIVED` | `AITUTORX-DOC-GOVERNANCE.md §8` |
| **禁用** | `ACTIVE` / `COMPLETE` / `FINAL` / `FINAL-FINAL` / `DONE` / `IN-PROGRESS` / `进行中` | 同上 §8.1 |
| Decision 语义状态 | `pending_review` / `approved` / `rejected` | `AGENTS.md` |
| OQ 状态 | `OPEN` / `OPEN-BLOCKING` | `GF-005` |
| OQ 状态（排除项） | `semantic_status ∈ {ready, incomplete, unknown}`（**不得改动、不得重命名**） | 同上 §8 |
| 产品状态（排除项） | `admission_candidates.decision_status`（如 `pending_review`） | 同上 §8 |

### 2.8 跨仓矛盾 —— **本轮关键事实**

#### M-1：`ACTIVE` 在两仓**一允一禁**

```text
[FACT] V3 `91 §3.1:121`：`ACTIVE` = 现行有效 → 【允许】
[FACT] AITutor-X `DOC-GOV §8.1:225`：
       「`ACTIVE` 不在词表内，不得再用于新文档。」
```

⇒ 同一份文档写 `Status: ACTIVE`：**在 V3 合法、在 X 违规**。
这是**跨仓矛盾**，不只是 namespace 差异。

#### M-2：V3 内部 `90:594` ↔ `91 §3.1` 值域不一致（**已登记，未消解**）

```text
90:594  6 值：ACTIVE | SUPERSEDED | HISTORICAL | DRAFT | CLOSED | NOT RELEASED
91 §3.1 10 值：OPEN | PENDING | CONDITIONAL PASS | CLOSED | NOT STARTED | DEFERRED
               | SUPERSEDED | RETRACTED | ACTIVE | HISTORICAL

仅 90 有：DRAFT · NOT RELEASED
仅 91 有：OPEN · PENDING · CONDITIONAL PASS · NOT STARTED · DEFERRED · RETRACTED
两者共有：ACTIVE · SUPERSEDED · HISTORICAL · CLOSED
```

```text
已登记：F-OD01V4R-50
  「`90 §4:376` 与 `91 §3.1` 值域不一致（`PENDING` 归属）→ 未决依赖」
  `OD-01V4R-FINAL-REMEDIATION-REPORT.md:50`
`:120`「OD-01-H 词汇 vs `91 §3.1` … 请 Owner 裁定二者关系」
```

#### M-3：`SUPERSEDED` 已是冻结状态值

```text
[FACT] `SUPERSEDED` 同时出现在 90:594 模板与 91 §3.1 十值内
```

⇒ 该词**已被 V3 状态域占用**（见 §5 对候选值 `superseded` 的判定）。

---

## 3. Q1 — `source_authority_state` 描述什么？

```text
必须先选一个语义域。三种候选互不兼容。
```

### Option A — 来源 **taxonomy label** 的生命周期

```text
描述：某个 source authority level 标签是否正式成立
例  ：L2 + proposed = 「该来源权威层级目前只是提出中的 taxonomy label」
```

**优点**：`source_level` 已表达 ontology position；`Registration Level` 已表达注册事实；
新字段唯一剩余空间即「该 taxonomy level 是否正式成立」。

### Option B — 来源**对象**的治理生命周期

```text
描述：文档本身的治理流程状态
例  ：draft / review / approved / deprecated
```

**后果**：`approved` / `pending` / `verified` 等**可能进入** ——
而这会与 **OD-01-H 状态体系强重叠**（§2.4），并与 91 §3.1 十值碰撞（§2.1）。

### Option C — **mapping 参与状态**

```text
描述：该来源是否参与本次映射
例  ：included / excluded / unknown
```

**后果**：语义上**不应命名为** `authority_state`（命名与语义不符）。

### 边界问题

```text
[OPEN] Q1 未定 ⇒ §2.8 的 M-1 / M-2 / M-3 三处矛盾落在哪个域，无法回答。
```

---

## 4. Q2 — `source_authority_state` 与 `Registration Level` 是否独立？（本文新增）

```text
[FACT] 目前唯一的在库实例（CR-002 型）中：
         source_authority_state = proposed
         Registration Level     = NOT REGISTERED
       两者【同向共变】。
```

```text
若二者在所有情形下同向共变 ⇒ §A.1.1 的 Row Identity 含冗余字段
若二者可独立           ⇒ 须给出至少一个「一真一假」的实例反证
```

**待裁**：

```text
☐ 独立（须附反例）
☐ 不独立（则 §A.1.1 第 4 字段应移除或改为派生）
```

**本文不预判。** 若不独立，DQ-05-03 = C 的 Row Identity 需回修。

---

## 5. 候选值逐个归属（核心产出）

```text
归属 = 该词【当前已被哪个语义域占用】。
「可入 source_authority_state？」列为判定，**不是批准**。
```

| 候选值 | 出现位置 | 当前含义 | 所属 namespace | 可入 `source_authority_state`？ |
|---|---|---|---|---|
| `proposed` | FU-05 §A.1.2（Owner 2026-09-28 裁） | taxonomy label 提案态 | **待 Q1** | ⏳ 待裁 |
| `accepted` | `90:374`/`:375`「ACCEPTED / EFFECTIVE」 | CR 审查通过 | V3 审查结果域（**未登记值**） | ⚠️ 已占用 |
| `superseded` | **`91 §3.1:119`**；`90:594` | 已被他文废止 | **V3 冻结状态词** | ❌ **直接碰撞** |
| `retired` | 未见于两仓 | — | 未见占用 | ✅ 无碰撞 |
| `approved` | OD-01-H:421；`90:370` | 批准态 | V3 治理决定域 | ⚠️ 见他域 |
| `pending` | OD-01-H:421；**`91 §3.1:114`**；`90:222/580/645/677` | 等待外部条件 | **V3 冻结状态词** + 治理决定域 | ❌ **直接碰撞** |
| `verified` | OD-01-H:421 | 验证态 | V3 验证结果域 | ⚠️ 见他域 |
| `NOT EFFECTIVE` | OD-01-H:421；OD-01-C | 非有效态 | V3 治理决定域 | ⚠️ 见他域 |
| `NOT REGISTERED` | `Registration Level`（CR-002:18 等） | 未注册 | **Registration Level** | ❌ 已归他域 |
| `REGISTERED AS L1` | `Registration Level`（CR-003:322 / CR-004:303） | 已注册为 L1 | **Registration Level** | ❌ 已归他域 |
| `ready` / `incomplete` | `20_Document_Pipeline.md:394` | 语义处理状态 | **`semantic_status`（值域冻结）** | ❌ 已归他域 |
| `auto_approve` / `pending_review` | `20_Document_Pipeline.md:397` | Gate 判定 | **`gate_decision`** | ❌ 已归他域 |
| `ACTIVE` | `91 §3.1:121`；`90:594` | 现行有效 | V3 冻结状态词；**X 侧禁用** | ❌ **两仓矛盾（M-1）** |
| `DRAFT` / `NOT RELEASED` | `90:594` | 文档发布态 | 90 Status 模板 | ⚠️ 见他域 |
| `EFFECTIVE` | `90:41` | 生效 | V3 在用未登记 | ⚠️ 见他域 |
| `HISTORICAL` | `91 §3.1:122`；`90:594` | 历史记录 | V3 冻结状态词 | ⚠️ 见他域 |
| `CLOSED` | `91 §3.1:116`；`90:594`；X §8 | 满足定义条件 | 两仓共有 | ⚠️ 见他域 |
| `OPEN` | `91 §3.1:113`；X §8 | 进行中 | 两仓共有 | ⚠️ 见他域 |
| `DEFERRED` | `91 §3.1:118`；X §8 | 显式延期 | 两仓共有 | ⚠️ 见他域 |
| `ARCHIVED` | X §8 | 已归档 | X 专有 | ⚠️ 见他域 |
| `pending_review` / `approved` / `rejected` | `AGENTS.md` Decision 语义状态 | 决策状态 | X Decision 状态域 | ⚠️ 见他域 |
| `OPEN-BLOCKING` | `GF-005` | OQ 状态 | X OQ 状态域 | ⚠️ 见他域 |
| `DRAFT` / `READY FOR FREEZE` / `NOT FROZEN` | Contract 文首 | 冻结叙事 | Contract 冻结叙事域（CL-01） | ⚠️ 见他域 |

**汇总（仅针对 Owner 拟的 4 个候选）**：

```text
proposed    ✅ 未见占用（但 Q1 未定）
accepted    ⚠️ `90:374` 已在用，且未登记于 91 §3.1
superseded  ❌ 与 `91 §3.1:119` 冻结状态值同名
retired     ✅ 未见占用
```

---

## 6. 候选值空间（**输入，非批准**）

Owner 于 2026-09-28 提出（作为输入）：

```text
source_authority_state ∈ { proposed, accepted, superseded, retired }

proposed   —— 已提出但未成为正式 authority label
accepted   —— 已被治理接受
superseded —— 曾有效，但被新定义替代
retired    —— 停止使用
```

Owner 明确排除：

```text
pending · approved · verified · NOT REGISTERED · REGISTERED AS L1 · ready · incomplete
理由：分属 workflow / governance decision / verification / registration /
      semantic processing 不同 namespace
```

**本文对该候选集的碰撞检查结果**：见 §5 汇总 —— **4 值中 1 值直接碰撞**（`superseded`）。
候选集本身仍待 Owner 批准；本文不批准。

---

## 7. `L2-proposed` 的三元分解（已裁，供值域对齐）

```text
source_level            = `L2`
source_authority_state  = `proposed`
Registration Level      = `NOT REGISTERED`
```

```text
不得存在组合值：
✗ `L2-proposed` 作为 source_level 取值
✗ level 携带 state 语义
```

依据：`OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01` §A.1.2（读法 B）。
三个字段分属三个 namespace，**不得互推**。

---

## 8. 影响面

```text
若 Q1 不裁：
  · §A.1.4 的 `[OWNER DECISION REQUIRED]` 持续
  · §A.2 九行中 6 行（1 / 3 / 4 / 6 / 7 / 8）无 state 可写
  · FU-05 Mapping Table Draft 无法启动
  · Gate 2 / Gate 10 继续不可填

若 Q2 不裁：
  · §A.1.1 Row Identity 是否含冗余字段未定
  · 若判定不独立，DQ-05-03 = C 的裁决需回修
```

---

## 9. 下一步裁决顺序

```text
① Owner 输入 `source_authority_state` 语义域（Q1）      ← 本文提供输入
② Owner 批准候选值域（含 Q2 独立性）
③ 回填 §A.1.4
④ 生成 §A.2 Mapping Table Draft
⑤ 逐行审查 mapping rows
⑥ rev.6 签发附录
```

**当前状态**：

```text
FU-05 Appendix A         : PROPOSED — NOT FINAL
Mapping Table            : Structure complete
Mapping Values           : Blocked by source_authority_state domain decision
```

---

## 10. Owner Verdict

```text
Q1 语义域:
  ☐ A（taxonomy label 生命周期）  ☐ B（来源对象治理生命周期）  ☐ C（mapping 参与状态）
  其他: _______________

Q2 与 Registration Level 是否独立:
  ☐ 独立   ☐ 不独立（Row Identity 需回修）
  反例（如选独立）: _______________

候选值集:
  ☐ 批准 Owner 拟 4 值（含 `superseded` 碰撞的处理）
  ☐ 修订为: _______________

Signed: _______________
Date:   _______________
```

---

*FU-05 `source_authority_state` 值域裁决输入 · 2026-09-28 · Not an Authority Decision. 不批准任何值域。*
