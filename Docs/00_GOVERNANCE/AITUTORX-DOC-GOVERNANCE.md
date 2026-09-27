# AITutorX Document Governance Baseline

**Document ID**: AITUTORX-DOC-GOVERNANCE
**Document Type**: Governance Meta-Spec
**Authority Level**: **L0-META**（文档治理元规范；**不定义业务语义**）
**Status**: `ACTIVE — REVISED 2026-09-27 (MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01)`
**Normative**: YES（对**文档治理流程**规范）
**Supersedes**: —
**Superseded By**: —
**Date**: 2026-09-21 / **Revised 2026-09-27**
**Upstream**: V3 `90_DOCUMENT_GOVERNANCE.md`；V3 `91_PROJECT_TERMINOLOGY.md`；AITutorX `GF-000`；AITutorX `AGENTS.md`
**Adaptation principle**: V3 Governance 为规则来源与成熟模板；AITutorX 目录结构为适配对象。最小适配，不机械复制。
**Owner Ratification**: Owner hereby accepts and ratifies this document as the current governance baseline for AITutorX (X2.6-BASELINE-CLOSURE-RECORD.md DSH-X26-03). Authority hierarchy: Owner Decision > Frozen Contract/Spec > Architecture/Governance documents. This ratification does NOT create a new Frozen Spec/Contract.
**Revision Authority**: MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01（Owner Decision，2026-09-27）。本次修订为治理边界收敛，不新增治理层。

---

## 0. 为什么需要 Document Governance

Architecture 结论如果没有 authoritative document 支撑，就没有真正固化。Document Governance 如果不知道哪些文档拥有 architecture authority，也无法真正执行。

本文档建立 AITutorX 自己的文档治理基线，解决：

1. 哪些文档拥有 normative authority
2. 新文档应该放在哪里
3. Root 目录允许出现什么
4. 文档创建前需要回答什么
5. Evidence 与 Conclusion 的边界

---

## 1. Document Authority Order（三档权威顺序）

| 档位 | 文档类型 | 实际约束力 |
|------|---------|-----------|
| **Normative** | Frozen Spec（`AITutors-v3/Docs/V3_SPEC/`）+ 冻结后的 Contract | **实现约束**——必须遵守 |
| **Informative** | Architecture / Design / Implementation 说明 | 用于理解，**不自动产生约束** |
| **Historical Evidence** | DSH Review / Verification / Closure / Audit 报告 | **仅历史记录**——不得阻塞任何 Level 1 实现 |

**Historical Evidence 不得阻塞任何 Level 1 实现。**

Normative 层变更需 Owner Decision + explicit amendment。Informative / Historical 层不改变 Normative。

---

## 2. Directory Layering（目录层级语义）

| 目录 | 档位 | 允许 | 禁止 |
|------|------|------|------|
| `Docs/00_GOVERNANCE/` | Normative（治理元规范） | Governance baseline、authority model | 业务 spec；临时报告 |
| `Docs/10_SPEC/` | Informative | Concepts、terminology map | Owner decisions；stage reports |
| `Docs/20_ARCHITECTURE/` | Informative | Architecture design、pipeline design | Runtime evidence reports |
| `Docs/30_CONTRACTS/` | Informative | Contract references、boundary definitions | 直接修改 Frozen Contract |
| `Docs/40_DECISIONS/` | Informative | Owner decisions、decision records | Operations state；audit reports |
| `Docs/50_OPERATIONS/` | Informative | Stage state、tracking matrix | Normative rules；owner decisions |
| `Docs/60_REPORTS/` | **Historical Evidence** | Audit / verification / evidence reports | Normative specs；owner decisions |
| `Docs/90_ARCHIVE/` | Historical | SUPERSEDED / historical documents | 作为现行引用来源 |
| **Root** | 入口 | README / AGENTS / 配置 / 授权 canonical docs | 报告、审计、临时分析 |

> **`Docs/60_REPORTS/` 全目录为 Historical Evidence，不构成实现约束。**

---

## 3. Root Directory Rule

> **Root 不是阶段报告堆放区。**

Root 允许：README.md / AGENTS.md / .gitignore / LICENSE / build metadata / 授权的 project-level canonical docs。

Root 禁止：报告、审计、临时分析、Closure records 等属于 `Docs/*` 的文档。

---

## 4. Document Creation Gate（简化为 3 项）

任何新增文档只需回答以下 3 项：

```text
1. 是否修改 Frozen Spec / 核心 Contract？
   → YES: 升级到 LEVEL 2（Owner Decision）
   → NO: 继续

2. 是否包含 secrets？
   → YES: 移除，改用 .env
   → NO: 继续

3. 放在哪个目录？
   → 按 §2 Directory Layering（不确定就放 60_REPORTS/）
```

**已删除的旧门槛（不再要求）**：authority level 判定、architecture fact 检查、重复 authority 检查、生命周期状态验证、引用闭包验证、同类文档 Glob 检查。

---

## 5. Evidence vs Conclusion 分离

```text
Evidence ≠ Conclusion ≠ Authority
```

Report 可以记录 observed facts、test results、findings、recommendations。Report 不得自动成为 architecture authority 或修改 Normative 层。

---

## 6. Terminology Governance

### 6.1 Path 命名映射（自 2026-09-27 起）

| 文档层名称 | Frozen Spec 原名 | 定义 |
|-----------|-----------------|------|
| **Primary Path** | Path B | Source → preprocessing → Adapter → ResolvedRun —— 当前目标生产路径 |
| **Fallback Path** | Native Path | Source → Resolver → ResolvedRun —— 保留路径（备用 / 调试 / 特殊输入） |

引用规则：首次出现时并列写出 Spec 原名，如「Primary Path（Spec Path B）」。不得修改 Frozen Spec 中的 Native Path / Path B 定义。

**Fallback Path 不作为当前生产链推进；不得因为 Fallback Path 现在能跑就继续扩展它。**

### 6.2 Canonical Terms（保留）

| Term | Canonical? | 说明 |
|------|:----------:|------|
| Question / Question Type | YES | 闭集 = 12 exam types |
| Unit / Unit Type | YES | 闭集 = `{standalone_unit, composite_unit}` |
| standalone_question / composite_question | **NO** | Legacy Producer 词汇，禁止作 canonical |

### 6.3 Terminology Boundary Rules

```text
T-2: Legacy vocabulary MUST NOT be used as canonical Question Type
T-3: Legacy vocabulary MUST NOT be used as canonical Unit Type
T-4: Question Type ⟂ Unit Type（正交，无映射）
T-5: Current normative documents MUST NOT declare legacy terms as canonical
```

---

## 7. Document Migration/Disposition

历史报告保留为 Historical Evidence，不做物理移动。Rule M-2（不得为"看起来干净"大规模移动）继续有效。

---

## 8. Document Lifecycle Status（受限词表）

适用范围：**仅任务/追踪类文档**。

| Status | Meaning |
|--------|---------|
| `OPEN` | 进行中 |
| `CLOSED` | 已完成 |
| `DEFERRED` | 推迟 |
| `ARCHIVED` | 归档 |

**明确排除（不得改动、不得重命名）**：
- 产品状态：`admission_candidates.decision_status`（如 `pending_review`）
- Frozen Spec 定义状态：`semantic_status ∈ {ready, incomplete, unknown}`
- GF-005 的 OQ 状态（该文件为 FROZEN GOVERNANCE BASELINE，OD-14，本任务不修改）

---

## 9. V3 Governance 对照表

| V3 概念 | AITutorX 适配 |
|---------|--------------|
| L0 Frozen Spec | Frozen Spec（V3_SPEC）—— Normative |
| L0-META | 本文档 |
| L1 Contract Change | Owner Decision |
| L2/L3/L4/L5 | Informative / Historical Evidence |

---

## 10. Agent 读取顺序（建议）

实现任何任务只需读：

```text
AITutors-v3/Docs/V3_SPEC/20_Document_Pipeline.md
AITutors-v3/Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
相关代码
```

其余文档一律 Informative / Historical。

---

## 11. Deprecated Governance Mechanisms

下列机制**不再作为 LEVEL 1 的开发阻塞条件**：

```text
1. 每个 M-step 独立 Owner Authorization
2. 每次代码修改必须产出 Closure + Verification + Registry + Evidence Package 完整链
3. DSH Review 作为每步实现前置
4. Implementation Queue 必须清零才能继续
```

**效力顺序**：上述机制的出处文档（X2.6-01 / X2.6-03 / GF-005 §5 Closure Protocol 等）属 Informative；与本文冲突时以本文为准；Frozen Spec 与冻结 Contract 除外。

本指令（MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01，2026-09-27）即为本次治理边界调整的 Owner Decision。

---

## 12. Security

```text
Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.
```

---

*Revised 2026-09-27 under MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01. Authority order simplified to 3 tiers. Creation gate reduced to 3 items. Historical Evidence declared non-blocking for Level 1.*
