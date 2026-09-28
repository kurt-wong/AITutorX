# GF-007 — Migration Authority Charter

```text
Document Type : Migration Authority Charter（Governance Charter）
Status        : OPEN
Decision State: approved
disposition   : RETAIN
supersedes    : —
superseded_by : —
Revision      : 5 (2026-09-28) — rev.1 → rev.2：新增 §3.7 Charter Requirements Satisfaction Criteria（rev.1 内容逐字保留）；rev.2 → rev.3：新增 `Decision State` 字段、§7 增列 RC-1～RC-4 核验证据、修正 §2.5 / §3.4 引用锚点、§4 补 `GF-005` / `FU-06` 两行；rev.3 → rev.4：Owner 签署 §7.2（☑ Accepted · Signed: kurt · 2026-09-28），`Decision State` 由 `pending_review` 记为 `approved`，记明 §3.7.2 Review authority 身份不固定（不新增 FU），§1–§6 内容未改（rev.1～rev.3 内容逐字保留）；rev.4 → rev.5：§6 禁用状态词 `DONE` → `已落盘`（DOC-GOV §8.1 与本 Charter §3.6 一致性修正；Editorial consistency correction，不影响 Owner Decision 内容、不重新签署；§3.7 / §7.2 / Status / Decision State 均未改）（rev.1～rev.4 内容逐字保留）
Date          : 2026-09-28
Authority     : 本文件（Owner Decision Authority — Migration Authority Charter）
依据           : GF-006 OD-01 §2.2（Charter 目的；「Charter 全文另立」已裁）
                Docs/40_DECISIONS/OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md §1
                  （F4 = Option A；Migration Authority = Owner）
                Docs/40_DECISIONS/OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01.md §A
                  （Authority Level 语义；rev.6 APPROVED）
Parent        : Docs/00_GOVERNANCE/GF-006-OWNER-DECISION-RECORD.md（OD-01）
readers       : Owner（批准方）；Gate 9 执行者；Migration Record 作者；F5 Gate 批准记录作者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 状态声明（先读）

```text
本文件是 Migration Authority Charter（Governance Charter），【不是】Frozen Spec。

Frozen      ：NO —— 本文件不构成 Frozen Specification，
              不得标注 FROZEN，不得被引作 Frozen 依据。
Status      ：OPEN
disposition ：RETAIN
不修改      ：GF-000～006 冻结文本
不落入      ：OD-14 冻结基线（该基线明确为 GF-000～006）
Review      ：已完成 —— Owner Accepted（2026-09-28；见 §7.2）

本文件不授权 / 不执行：
  Migration implementation · Runtime enforcement · Database schema / DDL
  Gate activation · Frozen Spec amendment · 创建 Artifact Registry 实例
```

**性质说明**：

```text
本 Charter 落盘 ≠ Charter requirements satisfied ≠ Migration Authorization
（见 §3.4 —— 这是本文件最重要的一条边界。）
```

---

## 1. Authority Role Model

> 依据：F4 子项 2 裁决 = **A**（允许同一主体）+ 强制角色区分

### 1.1 Charter 条文

```text
Migration execution authority and approval authority may belong to the same entity.
Charter SHALL preserve role distinction even when identity is identical.
```

### 1.2 三概念区分（禁止混淆）

| 概念 | 含义 | 本 Charter 下的载体 |
|---|---|---|
| **Executor** | 执行动作 / 产生结果 | Gate 1–10 的执行与证据填写 |
| **Authority** | 拥有授权范围 | Migration Authority |
| **Approver** | 承担批准责任 | 批准记录中的批准方 |

### 1.3 已裁的授权归属

```text
Migration Authority = Owner（本人）
依据：OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §1（F4 = Option A）
```

### 1.4 角色区分的强制后果（本 Charter 的核心约束）

```text
即使 Migration Authority 与 Approver 为【同一主体】，
批准记录【必须】分别记入两个引用字段 —— 不得合并、不得省略其中一个：

  `migration_authority_ref`   —— 授权范围归属
  `owner_decision_ref`        —— 批准责任归属

两个字段均沿用 GF-003 §3.2.1 `approval_block`（见 §2.1），不新造字段。
```

**理由（记录）**：

```text
单 Owner 治理模型下，强制主体拆分不提高真实性、不提高审计价值，
只增加形式流程 ⇒ 故允许同主体。
但「允许同主体」不等于「允许同概念」⇒ 故强制角色区分并显式记录。
```

### 1.5 与 Gate 证据的关系（**已存在的分离事实**，本 Charter 不改动）

```text
[FACT] GF-003 §3.2.1 `gate_evidence_slots`：
       「Gate 1–10 证据槽（pass|fail|pending|blocked_by(ref)）；【槽 ≠ 批准权】」

⇒ 执行证据与批准是【两个不同记录位】。本 Charter 沿用该划分，不合并。
```

---

## 2. Approval Record Core

> 依据：F4 子项 3 裁决 = **统一 Approval Record Core + Artifact Extension**

### 2.1 复用声明（不新建 schema）

```text
本 Charter 【不新建】Approval Record schema。
Core = GF-003 §3.2.1 `approval_block` 的既有五字段，逐字沿用：

  status                    # valid | invalid_without_charter | pending_owner | rejected
  migration_authority_ref
  owner_decision_ref
  approved_at
  notes
```

```text
依据：Owner 裁决「优先复用已有冻结结构，而不是重新发明」——
      重新设计将制造第三套体系。
```

### 2.2 模型

```text
Approval Record
      │
      ├── Core（上列五字段；跨 artifact 一致）
      │
      └── Artifact Extension（按 artifact 类型附加）
```

### 2.3 Artifact Extension（**已存在的扩展载体**，不新造）

| Artifact 类型 | 扩展载体 | 状态 |
|---|---|---|
| Migration | `REPORT-I §6.1` Migration Record 最小字段 | 合成示例，未批准 |
| Owner Decision | `OWNER-DECISION-*.md` 文件头体例 | 已签发实例 |
| Contract Change | V3 `CR-003` / `CR-004` 文件头体例（L1） | V3 仓已注册 |

```text
扩展字段的定义权属各 artifact 的既有载体；本 Charter 不重定义它们。
```

### 2.4 语义差异（记录，不消除）

```text
Owner Decision   = 决策批准
Contract Change  = 规范批准
Migration        = 执行授权

⇒ 三者语义不同，故【不采用】「单一万能 schema」。
```

### 2.5 硬规则（沿用，不放松）

```text
[FACT] GF-003 §3.2.2：Migration Authority Charter（F4）不存在时
       `approval_block.status = invalid_without_charter` 强制生效。
[FACT] GF-006 §2.4（OD-01 Non-authorizations）：NOT 将 `approval_block` 写为 `valid`。

⇒ 本 Charter 落盘【不】改变上述状态；本阶段任何 approval 均不得置为 `valid`。
```

---

## 3. Charter Governance Rules

### 3.1 批准记录存放位置

> 依据：F4 子项 4 裁决 = **A**

```text
批准记录存放于：Docs/40_DECISIONS/

依据：DOC-GOV R4「结论 → 40_DECISIONS/」
     既有先例：本仓 Owner Decision 记录现存 38 份于该目录
```

```text
边界：本 Charter 只定义【Document repository location】。
【不引入】database table / migration storage / runtime registry /
        runtime enforcement / schema / DDL。
```

### 3.2 与 Artifact Registry 的关系

```text
[FACT] GF-004 §2.2：`admitted` = 「经 Registry 登记 + Owner/Charter 处置」
[FACT] GF-006 OD-10：建立 Artifact Registry；【禁止】本任务创建实例

⇒ 记录【存放】与 Registry【登记】是两个动作。
   本 Charter 只定前者，【不】创建任何 Registry 实例。
```

### 3.3 权威分档缺口（登记，**不在本 Charter 内解决**）

```text
[FACT] DOC-GOV §1 三档权威顺序（Normative / Informative / Historical Evidence）
       【无「Owner Decision / Decision」档位】；
       §2 将 `Docs/40_DECISIONS/` 归为 Informative，
       而 §1 对 Informative 的定义为「用于理解，【不自动产生约束】」。
       与 README「L0 = Owner / System Decision」构成张力。

Owner 裁决（2026-09-28）：
  · 另立 Follow-up（FU-06），【不阻塞本 Charter】
  · 后续再决定是否修订 DOC-GOV Authority Order

⇒ 本 Charter 【不】修改 DOC-GOV。
```

### 3.4 **本 Charter 落盘 ≠ requirements satisfied ≠ Migration Authorization**

```text
两个【不同】条件必须区分：

  条件 ①（结构）GF-003 §3.2.2：
    IF Migration Authority Charter 不存在
      → approval_block.status = invalid_without_charter

  条件 ②（实质）GF-006 OD-01 §2.3：
    Migration Authorization remains unavailable until
    Charter requirements are satisfied.

────────────────────────────────────────────────
本 Charter 落盘只触及条件 ① 的前提；【不】满足条件 ②。
```

```text
[FACT] GF-006 §2.3：Charter requirements 的「satisfied 判定条件」尚未落盘。
[FACT] GF-005 OQ-GF-014：仍 OPEN-BLOCKING。
```

⇒ **本 Charter 不声明 requirements satisfied。**
⇒ `approval_block.status` 在本 Charter 落盘后**仍不得**置为 `valid`。
⇒ **Migration Authorization 仍不可用。**

### 3.5 Authority Level 引用规则（沿用已裁语义）

```text
引用 Authority Level 时一律使用 axis-qualified 记号（例：`Authority-L0`、`Authority-L3`）。
禁止裸 `L<n>`。
依据：OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 §A.1.3 / §A.2。
```

### 3.6 文书规则

```text
· 新文档文件头须含 supersedes / superseded_by / readers（DOC-GOV R3）
· 状态词限用于 DOC-GOV §8 词表：OPEN / CLOSED / DEFERRED / ARCHIVED
· 移动须用 `git mv` 并更新旧路径引用（DOC-GOV §7.4）
```

---

### 3.7 Charter Requirements Satisfaction Criteria（rev.2 新增）

> **rev.1 快照说明**：§3.4 中「Charter requirements 的『satisfied 判定条件』尚未落盘」
> 为 **rev.1 时点**的准确表述。**本 §3.7 即该判定条件**，自 rev.2 起生效。
> §3.4 的文本按 add-only 原则**逐字保留**；本节为其 supersede 记录。

#### 3.7.1 Required conditions（结构）

```text
Charter requirements satisfied SHALL require:

  RC-1  Required Charter sections exist
  RC-2  Required approval record fields are defined
  RC-3  Required references are resolved
  RC-4  Required governance conditions are recorded
```

| ID | 条件 | 机械核验口径 |
|---|---|---|
| **RC-1** | Required Charter sections exist | §1 / §2 / §3 / §4 / §5 均已落盘且非占位 |
| **RC-2** | Required approval record fields are defined | Approval Record Core 五字段已定义（§2.1）；Artifact Extension 载体已指名（§2.3） |
| **RC-3** | Required references are resolved | §4 全部引用对象可解析（不指向不存在文件） |
| **RC-4** | Required governance conditions are recorded | Migration Authority 归属已裁（§1.3）；F4-2 / F4-3 / F4-4 裁决已落盘；FU-06 状态已登记（§3.3） |

```text
四项为【合取】—— 任一不满足 ⇒ requirements 未 satisfied。
```

#### 3.7.2 Declaration authority（判定主体）

| 主体 | 权限 |
|---|---|
| **Owner** | **唯一** declaration authority —— 只有 Owner 可声明「requirements satisfied」 |
| Migration Authority | 与 Owner 为**同一主体**（§1.3）⇒ 不构成独立第二方；其角色为**授权范围归属** |
| Review authority（如 DSH / 外部审查） | 可出具 review 结论与证据，**【不】**具有 declaration 权 |

```text
⇒ 审查方提供【证据】，不提供【声明】。
（与 §1.4「角色区分即使同一身份也须显式记录」一致：Owner 与 Migration Authority
  同一身份，但二者在判定链中的角色必须分别记录。）
```

#### 3.7.3 Determination record（判定记录）

```text
Satisfied determination record SHALL contain:

  reference        —— 指向本 Charter 与判定依据
  evidence         —— 每项 RC-1 .. RC-4 的核验结果
  decision_owner   —— Owner
  timestamp        —— 判定日期
```

```text
存放位置：Docs/40_DECISIONS/（依 §3.1 / F4-4 = A）
形态    ：Decision Record（依 DOC-GOV R4「结论 → 40_DECISIONS/」）
```

#### 3.7.4 判定之后（**明确不在本 Charter 范围**）

```text
本 Charter 只定义【如何判定 satisfied】，
【不】定义【判定之后发生什么】。

不在本 Charter 范围：
  · `approval_block.status` 的取值变更
  · Gate 9 评估 / Gate 9 PASS
  · Migration execution permission / Migration Authorization
  · Migration 执行步骤
  · runtime enforcement / database / schema

⇒ requirements satisfied ≠ Migration Authorized（§3.4 继续适用）
```

#### 3.7.5 与 GF-005 `OQ-GF-014` 的关系

```text
GF-005 `OQ-GF-014`  = 历史【冻结】状态记录（OPEN-BLOCKING；2026-09-18 时点）
本 §3.7             = 现行 Charter satisfaction rule

二者层级不同：前者是冻结账本中的历史条目，后者是现行判定规则。
```

⇒ **不修改 GF-005；不改变 `OQ-GF-014`；本 Charter 提供【未来】判定规则。**

#### 3.7.6 rev.1 → rev.2 变更

```text
rev.1（commit 213a78a）：§1 / §2 / §3.1–§3.6 / §4 / §5 / §6 / §7
rev.2（本次）          ：新增 §3.7；rev.1 全部内容逐字保留

背景：GF-006 OD-01 §2.2 已要求「Charter 全文与 requirements satisfied 判定条件」
      落盘为【独立 Charter 文件】⇒ 判定条件属 Charter 的组成部分，
      不宜外置为独立 follow-up。（Owner 2026-09-28 裁决）
```

---

## 4. Reference Relationship

| 引用对象 | 关系 |
|---|---|
| `GF-006` OD-01 §2.2 | 本 Charter 的设立依据（三项目的：资格 / 格式 / 位置） |
| `GF-003 §3.2.1` | Approval Record Core 的字段来源 |
| `GF-003 §3.2.2` | `invalid_without_charter` 硬规则与条件 ① |
| `GF-004 §2.2` | 四状态（exists / tracked / referenced / admitted）与 Registry 边界 |
| `GF-005` `OQ-GF-014` | requirements satisfied 的冻结历史条目（`OPEN-BLOCKING`；不修改，见 §3.7.5） |
| `REPORT-I §6` Gate 9 | 批准在 Gate 中的位置（当前不可满足） |
| `REPORT-I §6.1` | Migration Record 最小字段（Migration 扩展载体） |
| `OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01` | F4 裁决；Migration Authority = Owner |
| `OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 §A` | Authority Level 与 state 语义（rev.6 APPROVED） |
| `FU-02-F4-CHARTER-SCHEMA-INPUT.md` | 本 Charter 的裁决输入（含 §5.2 缺口事实） |
| `FU-06` | DOC-GOV §1 权威顺序缺 Decision 档位（登记，不在本 Charter 内解决，见 §3.3） |
| `AITUTORX-DOC-GOVERNANCE.md` R3 / R4 / §2 / §7.4 / §8 | 文件头、归属、目录层级、移动、状态词 |

---

## 5. Non-Authorization Boundary

```text
本 Charter 不授权 / 不执行：

- Migration implementation
- Runtime enforcement
- Database schema / DDL
- Gate activation
- Frozen Spec amendment
- 创建 Artifact Registry 实例
- 使任何 approval 变为 `valid`
- 修改 GF-000～006 / V3 90、91 / DOC-GOV
- 修改任何历史报告正文
```

---

## 6. 当前状态

```text
Charter 落盘              = 已落盘（本文件 · Status OPEN · Decision State approved）
Migration Authority       = Owner（已裁）
角色区分（F4-2）           = 强制（§1）
Approval Record（F4-3）    = Core = GF-003 approval_block + Extension（§2）
记录位置（F4-4）           = Docs/40_DECISIONS/（§3.1）

Gate 9                    = UNSATISFIABLE        （GF-003 §3.2.2 状态继续适用）
approval_block.status     = invalid_without_charter
Migration Authorization   = NOT AUTHORIZED
Gate activation           = NOT AUTHORIZED
FU-06（§3.3 缺口）         = OPEN（不阻塞本 Charter）
```

> `[rev.2 追注]` `Requirements Satisfaction Criteria` 已于 **§3.7** 定义
> （判定条件已落盘）。**但判定尚未执行** —— requirements 未被声明为 satisfied；
> §3.4 的状态不变：`approval_block.status` 仍为 `invalid_without_charter`，
> **Migration Authorization 仍不可用**。本追注**不改上列状态块文本**。

---

## 7. Owner Review

### 7.1 Charter requirements verification（§3.7.1 机械口径）

核验方证据（§3.7.2：审查方可出具证据，**不**具 declaration 权）· 2026-09-28

| RC | 结果 | 证据 |
|---|---|---|
| **RC-1** | PASS | §1 / §2 / §3 / §4 / §5 均在位；占位词扫描（`TBD` / `TODO` / `FIXME` / `XXX` / `占位` / `待补` / `待填`）无实质占位（唯一 `占位` 命中为 §3.7.1 判据文本自身） |
| **RC-2** | PASS | §2.1 五字段与 GF-003 §3.2.1 逐字一致（`status` / `migration_authority_ref` / `owner_decision_ref` / `approved_at` / `notes`）；§2.3 Extension 载体 3 项已指名；§1.4 角色区分保留 |
| **RC-3** | PASS | §4 十二项引用可解析：涉 9 份既有文件（GF-003 / GF-004 / GF-005 / GF-006 / REPORT-I / DOC-GOV / OWNER-DECISION ×2 / FU-02）均在位；`FU-06` 为已登记 ID（无独立文件，见 §3.3） |
| **RC-4** | PASS | Migration Authority 归属已裁（§1.3）；F4-2 / F4-3 / F4-4 已落盘（§1 / §2 / §3.1）；FU-06 已登记（§3.3） |

```text
四项为合取（§3.7.1）。全部 PASS ⇒ requirements satisfied 的【判定基础具备】。

范围声明（§3.7.2 / §3.7.4）：
  · 本核验属 Charter completeness verification
  · 非 Migration Authorization 判定 · 非 Gate 9 判定
  · 不构成 requirements satisfied 声明 —— 声明权唯属 Owner
  · 本核验不改变 §3.4 / §6 的任何状态（`approval_block.status` 仍 `invalid_without_charter`）
```

### 7.2 Owner Decision

```text
Decision:
☑ Accepted（本 Charter 作为 Migration Authority Charter 生效）
☐ Rejected
☐ Revise

Signed: kurt
Date:   2026-09-28
```

---

*GF-007 — Migration Authority Charter · 2026-09-28 · revision 5 · Status OPEN · Decision State approved · 非 Frozen · Owner Accepted 2026-09-28。*
