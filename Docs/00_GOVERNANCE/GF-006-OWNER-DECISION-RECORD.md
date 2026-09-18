# GF-006 — Owner Decision Record（v0.2 Freeze 决策正典）

**Document ID**: GF-006
**Status**: `FROZEN GOVERNANCE BASELINE`（决策记录文本已冻结；**不**授权迁移）
**Version**: **v0.2 Frozen**（TASK-GF-008 Owner Decision Resolution & Freeze Text Solidification）
**Role**: Independent System Governance Architect（记录载体）；**Decision actor = Owner**
**Date**: **2026-09-18**
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Authority**: Owner Decision Input（TASK-GF-008 brief §2）— Claude **仅**转写，**不**新增决策

**Evidence classification**: `[FACT]` / `[OWNER DECISION]` / `[PROPOSAL]` / `[UNKNOWN]` / `[OBSERVED]`

**Hard rule（本文件核心边界）**:

```text
Frozen Governance Baseline does not imply Migration Authorization.

Freeze ≠ Migration Authorization
Migration Authority ≠ Migration Execution
Decision ≠ Migration Approval
```

**Related**: TASK-GF-007 Decision Matrix（OD-01~20）；GF-000~005；REVIEW/GF-003/06；REVIEW/GF-005/01

---

## 0. Record Scope

### 0.1 What this record does

将 Owner 已批准的决策，从 TASK-GF-007 Decision Package 中的 `[OWNER DECISION REQUIRED]`，**固化**为 `[OWNER DECISION]`，并写明 Scope 与 Non-authorizations。

### 0.2 What this record does NOT do

- 不关闭 BL-09 / BL-10 / BL-11
- 不关闭 D-048（保持 `pending_owner_decision`）
- 不关闭任何未在本文件出现的 OQ-GF
- 不创建 Artifact Registry 数据实例
- 不导入 Artifact
- 不修改 `admitted` 状态
- 不授予迁移执行权限
- 不宣布 Migration Ready
- 不宣布 Gate Passed
- 不修改代码 / 数据库 / 数据文件
- 不执行 migration
- 不将 proposal 扩展为新的设计
- 不自行新增 Owner Decision

### 0.3 Label meaning

| Label | Meaning |
|-------|---------|
| `[OWNER DECISION]` | Owner 已书面裁决；本文件转写 |
| `[FACT]` | 仓库/文档可核对事实 |
| `[UNKNOWN]` | 证据缺口，保留 |
| `[PROPOSAL]` | 非 Owner 裁决的提案性文本 |

---

## 1. OD-14 — GF v0.2 Freeze Decision

| Field | Value |
|-------|-------|
| **Decision ID** | OD-14 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-014（交叉）；REVIEW/GF-003/06；GF-000 §1.3 |

### 1.1 Owner Decision

**批准 GF v0.2 升格为 Frozen Governance Baseline。**

**冻结范围**: GF v0.2 文档体系（GF-000～005 + 本 GF-006 决策记录）。

**必须增加冻结声明**（已写入本文件 §0 Hard rule 及 GF-000 §1.3）:

> Frozen Governance Baseline does not imply Migration Authorization.

### 1.2 含义

**冻结代表**:

- 规则版本固定
- 后续引用有明确基线
- 变更走受控 patch，不覆盖历史版本

**冻结不代表**:

- 数据已经迁移
- Gate 已通过
- Migration 已授权
- Migration Ready
- 数据/代码可以进入 AITutor-X active tree

### 1.3 Non-authorizations

- NOT Migration Authorization
- NOT Migration Ready
- NOT Gate Passed
- NOT 数据迁移授权
- NOT 代码迁入 active tree 授权
- NOT 关闭任何 OQ / BL / D-048

---

## 2. OD-01 — Migration Authority Charter

| Field | Value |
|-------|-------|
| **Decision ID** | OD-01 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-014；BL-09；F4；GF-003 §3.2.2 `approval_block` |

### 2.1 Owner Decision

**建立 Migration Authority Charter。**

**但：当前不授予任何迁移执行权限。**

### 2.2 Charter 目的（已裁，Charter 全文另立）

Charter 用于明确:

- 谁拥有迁移审批资格
- 审批记录格式
- 审批保存位置

### 2.3 当前状态

```text
Migration Authorization remains unavailable until Charter requirements are satisfied.
```

`[FACT]` Charter 全文与「Charter requirements satisfied」的判定条件 **尚未落盘** 为独立 Charter 文件；本任务 **不**创建 Charter 正文，**不**代为满足 requirements。

### 2.4 Non-authorizations

- NOT 迁移执行授权
- NOT Migration Authority 个人任命（本 Decision 未点名授权人）
- NOT Gate 9 有效性
- NOT 关闭 OQ-GF-014 / BL-09
- NOT 将 `approval_block` 写为 `valid`

---

## 3. OD-10 — Artifact Registry

| Field | Value |
|-------|-------|
| **Decision ID** | OD-10 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | GF-000 §3.3；GF-001 §2.6；OQ-GF-013 交叉；BL-04 / BL-11 |

### 3.1 Owner Decision

**建立 Artifact Registry。**

### 3.2 目的

解决下列状态之间的混淆:

- `exists`
- `tracked`
- `referenced`
- `admitted`

Registry 用于: **记录治理认可的 Artifact。**

### 3.3 本任务执行边界（逐字约束）

**注意：本任务只固化 Registry 建立决策。**

**禁止**:

- 创建 Registry 数据实例
- 导入 Artifact
- 修改 `admitted` 状态

`[FACT]` 当前仍无 Registry 实例文件落盘；`admitted` 对 GF/REPORT 等引用对象保持 `[UNKNOWN]`。

### 3.4 Non-authorizations

- NOT Registry 实例已创建
- NOT 任何 Artifact `admitted=true`
- NOT REPORT-G/H/I/K 已准入
- NOT 关闭 BL-04 / BL-11

---

## 4. OD-03 — Authority Taxonomy

| Field | Value |
|-------|-------|
| **Decision ID** | OD-03 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-015；BL-09；F3；GF-001 §2.1–2.6 |

### 4.1 Owner Decision

**采用分层模型。**

**不废弃现有分类。**

### 4.2 规则

**第一层：Authority Domain**

例如:

- GOV
- EVD
- EXT

**第二层：Artifact Role**

例如:

- RSD
- PIS
- OCRA
- SEM
- MIG

### 4.3 说明

两类分类解决不同问题。

**禁止互相替代。**

`[OWNER DECISION]` 与 GF-001 §2.6「GOV/EVD/EXT 与 RSD/PIS/OCRA/SEM/MIG 正交」一致；v0.2 增补角色 **不替换** data lineage roles。

### 4.4 Non-authorizations

- NOT 废弃 RSD/PIS/OCRA/SEM/MIG
- NOT 废弃 GOV/EVD/EXT
- NOT 允许以 Authority Domain 替代 Artifact Role，或反向替代
- NOT 关闭 OQ-GF-015 / BL-09（BL-09 仍含「Taxonomy 完整执行状态」）
- NOT 声明 taxonomy 已在全部文档完成执行落地

---

## 5. OD-04 — Source Authority Model

| Field | Value |
|-------|-------|
| **Decision ID** | OD-04 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-001；OQ-GF-004 交叉；BL-10；GF-001 §2–§3；REPORT-K |

### 5.1 Important Correction（Owner 明示）

**不建立** `original/` 与 `maintainess/PDF` 的永久 Source Authority 排序。

**不指定**:

- `original` = canonical
- `maintainess/PDF` = canonical

### 5.2 Owner Decision

**采用：Hash-based Source Identity Model。**

### 5.3 规则

**数据身份由 content hash 决定。**

**是否可进入 AITutor-X 由下列因素决定**:

- validation
- test corpus
- processing result

`original/` 和 `maintainess/PDF` **均作为输入来源。**

只要 **content hash 一致**，则视为 **同一 Source Identity**。

### 5.4 与既有 FACT 的关系

`[FACT]`（不变）: 抽样 6/6 basename 交集 sha256 一致（REPORT-K）；operational OCR input = `maintainess/PDF`；`original/` 更大且高重叠。

`[OWNER DECISION]` 上述 operational 观测 **不**自动升级为 permanent canonical ranking。

### 5.5 Non-authorizations

- NOT 指定 original/ 为唯一 canonical RSD
- NOT 指定 maintainess/PDF 为唯一 canonical RSD
- NOT 授权删除/合并任一树（OQ-GF-004 仍 OPEN-BLOCKING）
- NOT 关闭 OQ-GF-001 / OQ-GF-004 / BL-10
- NOT 声明双树数据交付实施细节已完成

---

## 6. OD-05 — Data Entry / Storage Model

| Field | Value |
|-------|-------|
| **Decision ID** | OD-05 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-002；BL-10；F8；GF-004 B3；Docker-first 项目约束 |

### 6.1 Owner Decision

**采用：NAS-backed Read-only Data Model。**

### 6.2 最终架构

**NAS 保存**:

- 原始 PDF
- 图片
- OCR Markdown
- 中间处理结果

**Docker AITutor-X**:

通过 **read-only volume mount** 访问 NAS 数据。

**Database 保存**（结构化对象）:

- Question
- QuestionInstance
- Knowledge Node
- Relation
- Embedding metadata

**Repository 保存**（测试资产）:

- golden corpus
- fixtures
- validation samples

### 6.3 禁止

- 将全部数据复制进入代码仓
- 将 NAS 数据视为 Docker 生命周期数据

### 6.4 Non-authorizations

- NOT 数据本体已迁入 AITutor-X
- NOT NAS 路径/mount 配置已实施
- NOT Database schema 已创建或修改
- NOT 关闭 OQ-GF-002 / BL-10
- NOT 声明数据交付「具体实施细节」已完成
- NOT 将大体量语料默认改为可迁（仍须 Gate + Class 判定）

---

## 7. OD-18 — 71 / 87 / 166 Difference Handling

| Field | Value |
|-------|-------|
| **Decision ID** | OD-18 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-007（**不关闭**）；OQ-GF-003 交叉；GF-002 §9；GF-000 §2.3 |

### 7.1 Owner Decision

**建立 Difference Ledger。**

### 7.2 目的

解释下列对象之间的差异:

- snapshot
- manifest
- IR admitted

### 7.3 要求

后续任何下列数字引用 **必须能够关联 difference disposition**:

- `87`
- `71`
- `166`

### 7.4 注意（Owner 明示）

**本决定不关闭已有 OQ-GF-007。**

`[FACT]` 当前观测（不变）: snapshot n_rows=87；manifest 相关 sha 键 87；IR ADMITTED 71；manifest 计数叙事含 166。Difference Ledger **实例** 本任务 **不**创建；仅固化建立决策与引用义务。

### 7.5 Non-authorizations

- NOT OQ-GF-007 CLOSED
- NOT 71/87/166 已解释完毕
- NOT 「大规模 verified」声明已成立
- NOT interface_integrity 与 locator_integrity 可合并
- NOT Difference Ledger 实例已落盘

---

## 8. OD-06 — REPORT-G/H/I/K Treatment

| Field | Value |
|-------|-------|
| **Decision ID** | OD-06 |
| **Status** | `[OWNER DECISION]` |
| **Date** | 2026-09-18 |
| **Related** | OQ-GF-013；F10；BL-11；GF-000 §3.3.2；GF-004 §2.2 |

### 8.1 Owner Decision

**采用：整理后收编。**

### 8.2 流程

1. 整理为 Evidence Package
2. 补充 identity information
3. 进入 Artifact Registry
4. 再改变 admission 状态

### 8.3 当前

**不得直接认为 `admitted=true`。**

`[FACT]` 当前: REPORT-G/H/I/K = exists + untracked + referenced；`admitted=[UNKNOWN]`。本任务 **不**执行上述四步流程中的整理/入库/改状态。

### 8.4 Non-authorizations

- NOT `admitted=true`
- NOT 四报告已收编完成
- NOT Registry admission 实际完成（BL-11 仍 OPEN）
- NOT 关闭 OQ-GF-013 / F10 / BL-11
- NOT 允许将 untracked 报告直接写成治理已准入权威

---

## 9. Remaining Open Items（必须保持 OPEN）

下列事项 **仍保持 OPEN**。本记录 **不**关闭:

| Item | Status | 摘要 |
|------|--------|------|
| **BL-09** | OPEN | Migration Authority / Gate / Taxonomy **完整执行状态** |
| **BL-10** | OPEN | 数据交付 **具体实施细节** |
| **BL-11** | OPEN | REPORT-G/H/I/K Registry admission **实际完成** |
| **D-048** | `pending_owner_decision` | Papers 侧 known-issue；GF 仅 binding |
| **OQ-GF-001** | OPEN-BLOCKING | 决策已记（OD-04）；实施/交付细节与执行状态未完成 |
| **OQ-GF-002** | OPEN-BLOCKING | 决策已记（OD-05）；实施细节未完成 |
| **OQ-GF-004** | OPEN-BLOCKING | 双树保留/合并策略未在本批裁决 |
| **OQ-GF-007** | OPEN-BLOCKING | OD-18 **明示不关闭** |
| **OQ-GF-013** | OPEN | 决策已记（OD-06）；admission 未完成 |
| **OQ-GF-014** | OPEN-BLOCKING | Charter 决策已记（OD-01）；Charter requirements 未满足 |
| **OQ-GF-015** | OPEN-BLOCKING | Taxonomy 分层模型已记（OD-03）；完整执行状态未完成 |
| **OQ-GF-016/017/018** | OPEN-BLOCKING | 本批未裁决 |
| **OD-02 / OD-07~09 / OD-11~13 / OD-15~17 / OD-19~20** | 未在 TASK-GF-008 brief 出现 | **不得**由 Claude 自行新增或关闭 |

---

## 10. Decision × Boundary Matrix

| Decision | 固化内容 | 明确不授予 |
|----------|----------|------------|
| OD-14 | GF v0.2 = Frozen Governance Baseline | Migration Authorization / Gate pass / Migration Ready |
| OD-01 | 建立 Charter 的决定 | 迁移执行权限；Charter requirements 已满足 |
| OD-10 | 建立 Registry 的决定 | Registry 实例；admitted 状态变更 |
| OD-03 | 分层 Taxonomy；禁止互替 | OQ-GF-015/BL-09 执行完成 |
| OD-04 | Hash-based Source Identity | 单树 canonical；删/合树；BL-10 完成 |
| OD-05 | NAS-backed read-only 数据模式 | 数据迁入；实施细节完成；schema 变更 |
| OD-18 | Difference Ledger 建立决定 + 引用义务 | OQ-GF-007 关闭；verified 大规模声明 |
| OD-06 | 整理后收编流程 | admitted=true；BL-11 完成 |

---

## 11. Importers / Citation

| Consumer | 引用方式 |
|----------|----------|
| GF-000 §1.3 / Status / §7 / §9 | Freeze 声明；决策索引 |
| GF-001 §2.6 / §3 / §4 | OD-03 分层；OD-04 hash identity；OD-06 |
| GF-002 §7–§9 / Open Items | OD-04 对齐；OD-18 difference 引用义务 |
| GF-003 §3.2.2 / Schema status | OD-01 Charter 状态；approval_block 仍非 valid |
| GF-004 B3 / §2.2 / 数据边界 | OD-05 NAS 模型；OD-06 admission |
| GF-005 §7 Owner Decision Resolution | 交叉引用本文件；OQ 状态注记 |

---

## 12. Freeze Declaration（全文）

```text
Frozen Governance Baseline does not imply Migration Authorization.

「Frozen」仅表示：
  - 治理文档版本状态被冻结（文本可被引用、变更须版本化）
  - 后续引用有明确基线
  - 变更走受控 patch，不覆盖历史版本

「Frozen」明确不代表：
  - Migration approval
  - Migration Gate 执行力 / Gate Passed
  - Migration Ready
  - 数据已经迁移
  - 数据/代码可以进入 AITutor-X active tree

Migration Authority ≠ Migration Execution
Decision ≠ Migration Approval
```

---

*GF-006 · **v0.2 FROZEN GOVERNANCE BASELINE** · TASK-GF-008（Owner Decision Resolution） · 2026-09-18*
*决策 actor = Owner；记录 actor = document verification only。*
***Frozen Governance Baseline does not imply Migration Authorization.***
*NOT Migration Authorized · NOT Migration Ready · NOT Gate Passed · NOT OQ/BL/D-048 Closed.*
