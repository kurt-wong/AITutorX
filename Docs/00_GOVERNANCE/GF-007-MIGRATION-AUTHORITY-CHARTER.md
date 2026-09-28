# GF-007 — Migration Authority Charter

```text
Document Type : Migration Authority Charter（Governance Charter）
Status        : OPEN
disposition   : RETAIN
supersedes    : —
superseded_by : —
Revision      : 1 (2026-09-28)
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
Review      ：待 Owner review（见 §7）

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
[FACT] GF-003 §3.2.2：Charter requirements 未满足时
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

  条件 ②（实质）GF-006 OD-01 §2.2：
    Migration Authorization remains unavailable until
    Charter requirements are satisfied.

────────────────────────────────────────────────
本 Charter 落盘只触及条件 ① 的前提；【不】满足条件 ②。
```

```text
[FACT] GF-006 §2.2：Charter requirements 的「satisfied 判定条件」尚未落盘。
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

## 4. Reference Relationship

| 引用对象 | 关系 |
|---|---|
| `GF-006` OD-01 §2.2 | 本 Charter 的设立依据（三项目的：资格 / 格式 / 位置） |
| `GF-003 §3.2.1` | Approval Record Core 的字段来源 |
| `GF-003 §3.2.2` | `invalid_without_charter` 硬规则与条件 ① |
| `GF-004 §2.2` | 四状态（exists / tracked / referenced / admitted）与 Registry 边界 |
| `REPORT-I §6` Gate 9 | 批准在 Gate 中的位置（当前不可满足） |
| `REPORT-I §6.1` | Migration Record 最小字段（Migration 扩展载体） |
| `OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01` | F4 裁决；Migration Authority = Owner |
| `OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 §A` | Authority Level 与 state 语义（rev.6 APPROVED） |
| `FU-02-F4-CHARTER-SCHEMA-INPUT.md` | 本 Charter 的裁决输入（含 §5.2 缺口事实） |
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
Charter 落盘              = DONE（本文件 · Status OPEN · 待 review）
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

---

## 7. Owner Review

```text
Decision:
☐ Accepted（本 Charter 作为 Migration Authority Charter 生效）
☐ Rejected
☐ Revise

Signed: _______________
Date:   _______________
```

---

*GF-007 — Migration Authority Charter · 2026-09-28 · revision 1 · Status OPEN · 非 Frozen · 待 Owner review。*
