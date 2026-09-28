# FU-02 — F4 Charter Schema 裁决输入（子项 2 / 3 / 4）

```text
Document Type : Decision Preparation Record（非 Authority Decision）
Status        : OPEN
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 1 (2026-09-28)
Date          : 2026-09-28
Authority     : —（本文不构成任何 Authority；**不预填任何 Owner choice**）
Parent        : Docs/40_DECISIONS/OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md §1（F4 子项 2/3/4）
                + §6 FU-02（GF-007 落盘）
Upstream      : Docs/40_DECISIONS/OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01.md（rev.6 · APPROVED）
                Docs/00_GOVERNANCE/GF-006-OWNER-DECISION-RECORD.md §2（OD-01）
                Docs/60_REPORTS/REPORT-I-MIGRATION-GATE-DEFINITION.md（as-of 2026-09-17）
Temporal Scope: Current-state facts verified as of 2026-09-28.
readers       : Owner（裁决方）；GF-007 Charter 作者；Gate 9 执行者；Migration Record 作者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 非授权声明

```text
本文不是 Authority Decision。
本文【不预填任何方案】，不提前倾向任何 Option。
本文不把 FU-05 的 mapping 结论扩展成 charter rule。
本文不产生 implementation implication（见 §6）。
本文不修改 GF-000～006 / V3 90、91 / DOC-GOV / 任何已签发 Decision。
本文不创建 GF-007。
本文不触发 Migration / Gate 批准 / Frozen Spec amendment。
```

**性质区分（Owner 2026-09-28 明确）**：

```text
FU-05 已解决      ：Authority Taxonomy Mapping（Level 是什么 / 如何映射 / state 与 registration 如何分离）
本文进入          ：Authority Charter Governance Schema（谁批准 / 如何记录 / 记录在哪）
⇒ 三者属治理机制，【不得由 Mapping Table 直接推导】。
```

---

## 1. Scope

```text
唯一范围：F4 子项 2 / 3 / 4 的决策输入

  子项 2 —— Gate 执行者与批准者是否分离？
  子项 3 —— 批准记录格式？
  子项 4 —— 批准记录存放路径？

形式：Facts → Options → Verdict（留空）
```

**排除**：

```text
· F4 子项 1（Migration Authority 人选）—— 已裁：Owner（本人）
· F5 Gate 版本批准 / F10 Set B —— 未裁
· Runtime enforcement / DB schema / Registry 实例 —— 未授权（§6）
```

---

## 2. Frozen Preconditions（已确定；不得推导超出）

### 2.1 Authority Mapping 已冻结

```text
L1 Contract Change
        │  modifies
        ▼
Authority-L0
```

```text
解释：Authority relation ≠ numeric hierarchy ranking
禁止推导：`L1 < L0`
依据：OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 §A.2 行 3 说明
```

### 2.2 Authority State 已冻结

```text
source_authority_state ∈ { proposed, established, deprecated }
语义 = taxonomy label lifecycle
【不是】approval status / registration status / runtime state
依据：同上 §A.1.4
```

### 2.3 Registration Level 独立

```text
source_authority_state ≠ Registration Level
```

```text
禁止自动推导（例如 proposed → NOT REGISTERED、established → REGISTERED）
依据：同上 §A.1.4「与 Registration Level 正交（Q2 = 独立）」
```

### 2.4 已裁的 Charter 三项目的

```text
GF-006 OD-01 §2.2（已裁，Charter 全文另立）：
  - 谁拥有迁移审批资格
  - 审批记录格式
  - 审批保存位置
```

**已裁的既有约束**：

```text
GF-006 §2.4 Non-authorizations：
  · NOT 迁移执行授权
  · NOT Migration Authority 个人任命（本 Decision 未点名授权人）
      → 已由 OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §1 补齐：Migration Authority = Owner（本人）
  · NOT Gate 9 有效性
  · NOT 将 `approval_block` 写为 `valid`
```

### 2.5 GF-007 落盘约束（已裁）

```text
载体       ：Docs/00_GOVERNANCE/GF-007-MIGRATION-AUTHORITY-CHARTER.md
不得标注   ：Frozen
Status     ：OPEN
disposition：RETAIN
不修改     ：GF-000～006 冻结文本
不落入     ：OD-14 冻结基线（该基线明确为 GF-000～006）
```

---

## 3. F4-2 — Gate 执行者与批准者是否分离？

### 3.1 Facts

```text
[FACT] GF-003 §3.2.1 `gate_evidence_slots`
       「Gate 1–10 证据槽（pass|fail|pending|blocked_by(ref)）；【槽 ≠ 批准权】」
       ⇒ 执行证据与批准权【已被明文分离为两个概念】

[FACT] GF-003 §3.2.1 `approval_block` 字段：
         status / migration_authority_ref / owner_decision_ref / approved_at / notes
       ⇒ 现有 schema 同时含 `migration_authority_ref`【与】`owner_decision_ref`，
         即现格式【隐含双重引用】

[FACT] GF-003:261 与 GF-000:320 的 Gate 9 行均写：
       「9 Governance approval | Migration Authority + Owner（F4/F5）」

[FACT] REPORT-I §6 Gate 9：
       「Governance approval | Migration Authority 签字/记录（格式由 F4 定）| 当前不可满足」

[FACT] REPORT-I §6.1 Migration Record 最小字段仅含单一 `approver: <Migration Authority>`

[FACT] REPORT-I §1 F4 迁移前要求：
       「必须先有：授权人/角色、【Gate 执行者】、批准记录格式、存放路径」
       ⇒ 该处【已把「授权人」与「Gate 执行者」并列为两项】

[FACT] Migration Authority = Owner（本人）（OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §1）

[FACT] 既有实践：`OWNER-DECISION-*.md` 由 Owner 签署（`Signed by / Signed: kurt`）；
       本次 session 内无「执行者与批准者分离」的既有实例可引用
```

**Facts 呈现的张力（记录，不作判断）**：

```text
· 「槽 ≠ 批准权」已明文 ⇒ 概念上已分离
· 但 `approval_block` 同时含两个 ref ⇒ 现格式未说明二者关系（并存？分工？互斥？）
· GF-003 / GF-000 写「Migration Authority + Owner」⇒ 与 REPORT-I 的单一 `approver` 不一致
```

### 3.2 Options

| Option | 含义 | 需回答的连带问题 |
|---|---|---|
| **A** | Executor 可以批准（执行者与批准者可为同一主体） | 如何防止「自执行自批准」无记录？ |
| **B** | Executor 与 Approver **必须分离** | 分离的判定标准是什么（主体 / 角色 / 记录链）？ |
| **C** | 按 **Authority Level** 定义例外（部分层级允许合并） | 以哪套层级判定（`Authority-L*`）？例外清单由谁维护？ |

```text
其他: _______________
```

### 3.3 Owner Verdict

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

若选 B，分离判定标准: _______________
若选 C，例外清单依据: _______________

Signed: _______________
Date:   _______________
```

---

## 4. F4-3 — 批准记录格式？

### 4.1 Facts — 已存在的记录载体盘点（防重复造字段）

**载体 ①：`GF-003 §3.2.1 approval_block`（已存在，属 evidence package schema）**

```text
approval_block
  ├─ status                 # valid | invalid_without_charter | pending_owner | rejected
  ├─ migration_authority_ref
  ├─ owner_decision_ref
  ├─ approved_at
  └─ notes
```

```text
[FACT] 其 status 值域已含 `invalid_without_charter`；GF-003 §3.2.2 规定
       Charter 不存在时该值【强制生效】。
[FACT] GF-006 §2.4：NOT 将 `approval_block` 写为 `valid`。
```

**载体 ②：`REPORT-I §6.1` Migration Record 最小字段（合成示例，未批准）**

```text
migration_id / asset / class / source_repo / source_commit / source_path / sha256
/ authority_level / authority_basis / gate_status / approver / approved_at / notes
```

**载体 ③：`OWNER-DECISION-*.md` 体例（本仓 Owner Decision 记录）**

```text
Document Type / supersedes / superseded_by / readers / Status / Decision State
/ Date / Authority / Parent / Scope / Security（+ Revision）
（签名块：Signed by / Signed Date / Verdict）
```

**载体 ④：V3 `CR-003` / `CR-004` Contract Change Record 体例（L1，V3 仓）**

```text
Document ID / Title / Document Type / Authority Level / Status / Normative / Purpose
/ Derives From / May Change / Must Not Change / Supersedes / Superseded By
/ Gate State Authority
```

**横切规则**：

```text
[FACT] DOC-GOV R3：新文档文件头必须回答 supersedes / superseded_by / readers
[FACT] DOC-GOV §5：Evidence vs Conclusion 分离
[FACT] DOC-GOV §4 Document Creation Gate 3 项：是否改 Frozen Spec / 是否含 secrets / 放哪个目录
       【已删除的旧门槛】含「authority level 判定」「重复 authority 检查」——
       即：新增文档不再强制做 authority 判定
[FACT] 载体 ①② 字段【重叠但不等同】（① 5 字段；② 12 字段；仅 status/refs/approved_at/notes 部分对应）
```

### 4.2 Options

| Option | 含义 | 需回答的连带问题 |
|---|---|---|
| **A** | **统一 Approval Record schema**（单一 schema 覆盖全部批准记录） | 与 ① 冲突时以谁为准？是否吸收 ②？ |
| **B** | **Artifact-specific record**（各 authority artifact 各有记录格式） | 跨 artifact 如何对账？`approval_block` 是否降为其中一种？ |
| **C** | **最小公共字段 + 扩展字段** | 最小公共集是哪几个？扩展由谁定义？ |

```text
其他: _______________
```

### 4.3 Owner Verdict

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

若选 C，最小公共字段集: _______________

Signed: _______________
Date:   _______________
```

---

## 5. F4-4 — 批准记录存放路径？

### 5.1 Facts

**目录层级语义（DOC-GOV §2）**：

| 目录 | 档位 | 允许 | 禁止 |
|---|---|---|---|
| `Docs/00_GOVERNANCE/` | Normative（治理元规范） | Governance baseline、authority model | 业务 spec；临时报告 |
| `Docs/40_DECISIONS/` | **Informative** | Owner decisions、decision records | Operations state；audit reports |
| `Docs/60_REPORTS/` | **Historical Evidence** | Audit / verification / evidence reports | Normative specs；owner decisions |

```text
[FACT] DOC-GOV §2 脚注：「`Docs/60_REPORTS/` 全目录为 Historical Evidence，不构成实现约束。」
[FACT] DOC-GOV R4：结论 → `40_DECISIONS/`；证据 → `60_REPORTS/`；规则 → `00_GOVERNANCE/`
[FACT] DOC-GOV R1：每个任务最多产出 1 份文档；例外须 Owner 显式批准
[FACT] DOC-GOV §8B：60_REPORTS 膨胀已登记为治理问题（104 → 112 份 / 4 天）；
       现值 = 150 份
[FACT] DOC-GOV §7.4：移动必须 `git mv`（保留历史）；移动后必须更新所有指向旧路径的引用
[FACT] 现有目录规模：00_GOVERNANCE 17 · 10_SPEC 5 · 20_ARCHITECTURE 11 · 30_CONTRACTS 4
       · 40_DECISIONS 38 · 50_OPERATIONS 19 · 60_REPORTS 150 · 90_ARCHIVE 1
```

**既有先例**：

```text
[FACT] 本仓 Owner Decision 记录现存于 `Docs/40_DECISIONS/`（38 份）
[FACT] V3 的 L1 Contract Change Record 存于 V3 仓 `Docs/V3_SPEC/`（跨仓）
[FACT] `approval_block` 不是独立文档，而是 evidence package 的【内嵌字段】
```

**与 Registry 的关系**：

```text
[FACT] GF-004 §2.2 四状态：`admitted` = 「经 Registry 登记 + Owner/Charter 处置」
[FACT] GF-006 OD-10：建立 Artifact Registry；【禁止】本任务创建实例/导入/改 admitted
⇒ 记录「存放位置」与 Registry「登记动作」是两个问题；本文只问前者
```

### 5.2 一项此前未登记的权威分档缺口（本文核出）

```text
[FACT] DOC-GOV §1「Document Authority Order（三档权威顺序）」：
         Normative        = Frozen Spec + 冻结后的 Contract
         Informative      = Architecture / Design / Implementation 说明
         Historical Evidence = DSH Review / Verification / Closure / Audit 报告
       ⇒ 三档中【没有「Owner Decision / Decision」档位】

[FACT] DOC-GOV §2 把 `Docs/40_DECISIONS/` 归为 **Informative**
[FACT] §1 对 Informative 的定义：「用于理解，【不自动产生约束】」

⇒ 依 §2 的目录归档，`40_DECISIONS/` 内的 Owner Decision 会被归入 Informative
   —— 而 README 层级中 `L0 = Owner / System Decision` 为最高。
```

**该缺口的后果（直接影响 F4-4）**：

```text
若批准记录落在 `40_DECISIONS/`：
  · 依 §2 获 Informative 档位
  · 而批准是 authority act，不是「说明」
⇒ F4-4 的答案会顺带决定「批准记录受哪一档约束」。
```

```text
[OPEN] 该缺口【未登记】于任何冲突账本（CL-03 / X2-03 均未含）。
本文只登记事实，不作裁决。
```

### 5.3 Options

| Option | 含义 | 需回答的连带问题 |
|---|---|---|
| **A** | **Decision documents**（批准记录作为 Decision 文档，入 `40_DECISIONS/`） | 与 §5.2 的 Informative 档位如何处理？ |
| **B** | **Dedicated governance directory**（新建专用目录，如 `Docs/00_GOVERNANCE/` 下） | 是否与 R1（1 文档/任务）及 §8B（膨胀）冲突？ |
| **C** | **Artifact adjacent storage**（记录随 artifact 存放） | 与 R4（结论 → 40_DECISIONS）如何协调？ |

```text
其他: _______________
```

### 5.4 Owner Verdict

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

§5.2 分档缺口是否一并处置: ☐ 是（另立 follow-up）  ☐ 否

Signed: _______________
Date:   _______________
```

---

## 6. 边界：Document repository location vs Runtime storage

```text
本输入只讨论【Document repository location】—— 仓库内文档路径。

【不引入】下列任何一项（未授权）：
  · database table
  · migration storage
  · runtime registry
  · runtime enforcement
  · schema / DDL
```

**明确记录**：

```text
[FACT] GF-006 §2.4：NOT 将 `approval_block` 写为 `valid`
       ⇒ 无论 F4-3 选哪个 Option，本阶段均不得使任何 approval 变为有效
[FACT] GF-003 §3.2.2：Charter 不存在时 `invalid_without_charter` 强制生效
       ⇒ 该状态在本阶段【继续适用】
```

```text
本输入不产生 implementation implication。
```

---

## 7. GF-007 限制（已裁 + 本文重申）

```text
暂不授权：
  ❌ Frozen Spec amendment
  ❌ Implementation
  ❌ Migration
  ❌ Gate activation

GF-007 只能作为：Governance Charter proposal

状态：
  Status        : OPEN
  disposition   : RETAIN
不得：
  Status        : FROZEN
不得修改：
  GF-000 ～ GF-006
```

---

## 8. 影响面

```text
若 F4 子项 2/3/4 不裁：
  · GF-007 无法落盘（Charter 三要素缺二）
  · Gate 9 保持 UNSATISFIABLE
  · `approval_block.status` 保持 `invalid_without_charter`
  · F5 Gate 版本批准记录无「格式」可依
  · Migration 仍 NOT AUTHORIZED
```

---

## 9. Owner Signature

```text
Decision:
☐ Accepted（接受本材料作为 F4 子项 2/3/4 裁决输入）
☐ Rejected
☐ Revise

Signed: _______________
Date:   _______________
```

---

*FU-02 F4 Charter Schema 裁决输入 · 2026-09-28 · Not an Authority Decision. 不预填任何方案。*
