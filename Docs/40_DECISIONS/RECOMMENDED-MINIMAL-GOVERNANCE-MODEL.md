# Recommended Minimal Governance Model

**Document Type**: Report / Recommendation（L3，非 normative）
**Status**: `COMPLETE — FOR OWNER REVIEW`
**Date**: 2026-09-23
**Purpose**: 让 Owner 看完后直接回答：什么事需要停下来问我？什么事可以直接做？什么事需要严格 Migration Governance？
**Constraint**: 不新增 Governance Framework。本文件本身不是新的治理体系，只是对现有规则的收敛建议。

---

## 0. 一页总览

```
┌─────────────────────────────────────────────────────────────┐
│                    AITutor-X 变更分级                         │
│                  （最多三档，不设第四级）                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LEVEL 1 — NORMAL IMPLEMENTATION                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 明确需求 → 检查 Frozen Spec → 实现 → 测试 → 提交      │    │
│  │                                                     │    │
│  │ 不需要 Owner Authorization                          │    │
│  │ 不需要 DSH Verification                             │    │
│  │ 不需要 Closure Record                               │    │
│  │ Evidence = 测试通过 + commit message                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                         ▲                                   │
│            只有当变更涉及 ↓ 时才升级                           │
│                                                             │
│  LEVEL 2 — ARCHITECTURAL CHANGE                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 提出变更 → Owner Decision → 修改 Spec/Decision        │    │
│  │ → 实现 → 测试 / Evidence                            │    │
│  │                                                     │    │
│  │ 需要 Owner Decision（一次）                          │    │
│  │ 不需要多轮 DSH + Closure 仪式                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                         ▲                                   │
│            只有当变更涉及 ↓ 时才升级                           │
│                                                             │
│  LEVEL 3 — MIGRATION / IRREVERSIBLE CHANGE                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Decision → Plan → Implementation → Verification     │    │
│  │ → Closure                                           │    │
│  │                                                     │    │
│  │ 保留现有 Migration Governance（GF-003/004）          │    │
│  │ 仅在此级别生效                                       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. LEVEL 1 — NORMAL IMPLEMENTATION

### 1.1 定义

**凡是不改变 Frozen Architecture 和关键不变量的工程工作，全部属于 LEVEL 1。**

### 1.2 包含

| 工作类型 | 示例 |
|----------|------|
| Bug Fix | 修复 `ir.py` 默认值、修 wash path |
| Test Fix / 增加测试 | 补 P-path 回归测试 |
| Parser Fix | 修 annotation JSON parse |
| Preprocessing Integration | `reslice_pipeline.py` 输出 `source_content_sha256` |
| Adapter Implementation | `annotation_adapter.py` 边界归一化 |
| 普通 API 实现 | Question/Material/Instance 读 API |
| 普通数据转换 | manifest 格式调整 |
| 非破坏性内部重构 | 提取公共函数 |
| 性能优化 | 缓存、索引 |
| 修复已知实现缺陷 | P3/P4/P5/P9/P10/P11/P12 wash path |
| **完成已明确的 Frozen Spec 实现** | Contract v0.2 已定义但未实现的字段 |
| 普通 UI | 前端展示 |
| 文档 bug fix | 修正文档中的事实错误 |

### 1.3 流程

```
明确需求
  ↓
检查 Frozen Spec（确认不冲突）
  ↓
实现
  ↓
测试（pytest / 集成测试）
  ↓
提交（commit message 写清做了什么）
```

### 1.4 不需要

- ❌ Owner Authorization
- ❌ Owner Decision
- ❌ DSH Adversarial Review
- ❌ DSH Verification
- ❌ Closure Record
- ❌ Evidence Plan / Evidence Approval
- ❌ Registry 登记
- ❌ Document Creation Gate 9 项（见 §4 简化版）
- ❌ 追踪矩阵更新（除非是大 feature）

### 1.5 Evidence 位置

```
Implement → Test → Evidence（测试结果 + commit）

而不是：

Evidence Plan → Evidence Approval → Implementation
```

**Evidence 是证明实现正确的手段，不是阻止普通实现开始的理由。**

### 1.6 唯一约束

即使在 LEVEL 1，以下 A 类硬规则**始终有效**：

| 规则 | 说明 |
|------|------|
| 不修改 Frozen Spec / Frozen Contract 正文 | 如需修改 → 升级到 LEVEL 2 |
| 不 hardcode secrets | 安全 |
| Hash-based Identity（Path ≠ Identity） | 数据完整性 |
| Fail-closed（hash 不一致 ⇒ 拒绝） | 数据完整性 |
| UNKNOWN 不 silent skip / fallback | 数据完整性 |
| Legacy 术语不得作 canonical | 语义完整性 |
| Evidence append-only | 审计 |
| 不为测试通过改断言 | 测试可信度 |
| 禁 destructive replacement（双字段策略） | 历史保护 |

---

## 2. LEVEL 2 — ARCHITECTURAL CHANGE

### 2.1 定义

**当变更涉及以下任一项时，升级到 LEVEL 2：**

| 触发条件 | 示例 |
|----------|------|
| 改变 Frozen Spec | 修改 V3 pipeline 顺序、改数据模型 |
| 改变核心 Contract | 修改 PREPROCESSING-V3-CONTRACT |
| 改变核心 Authority | 改变谁有权决定 Unit-Type |
| 改变跨模块公共 Contract | 改变 preprocessing↔V3 接口语义 |
| 架构存在两个合理解释 | 选择不同解释会改变系统架构或长期数据结构 |
| 改变核心数据模型 | 增删持久化字段（非内部临时结构） |
| 改变 Pipeline 核心语义 | 改变 Admission 规则语义 |

### 2.2 流程

```
提出变更（简要说明：改什么、为什么、影响面）
  ↓
Owner Decision（一次裁决）
  ↓
修改 Spec / Decision（如有需要）
  ↓
实现
  ↓
测试 / Evidence（测试通过即可，不强制 DSH）
```

### 2.3 不需要

- ❌ 多轮 DSH Adversarial Review
- ❌ 独立 Closure Record
- ❌ Registry 登记前置
- ❌ Evidence Plan 审批
- ❌ 6 步 Spec Change 流程（简化为：Owner Decision + 修改 + 测试）

### 2.4 Spec Change 简化流程

**现有**：proposal → Owner → Change Record → impact analysis → verification → new baseline（6 步）

**建议**：
```
Owner Decision（批准修改）
  ↓
修改 Spec（版本化，不覆盖历史）
  ↓
测试验证
  ↓
记录（commit message + 简短 Decision note）
```

**3 步替代 6 步。** 历史版本通过 git 保留，不需要独立 Change Record 文档。

### 2.5 何时必须停下来问 Owner

**只有以下情况必须阻塞等待 Owner Decision：**

| # | 情况 | 示例 |
|---|------|------|
| ① | 实现方案与 Frozen Spec 明确冲突 | 想改 pipeline 顺序 |
| ② | 架构存在两个合理解释，选择不同会改变长期数据结构 | composite_unit 判定条件 |
| ③ | 需要修改 Frozen Spec | 修 SPEC ERROR |
| ④ | 不可逆操作 | 数据删除、大规模 Migration |
| ⑤ | 项目目标变化 | 产品边界改变、核心业务模型改变 |

**除此之外：默认允许继续实现，通过测试和 Evidence 证明实现正确。**

---

## 3. LEVEL 3 — MIGRATION / IRREVERSIBLE CHANGE

### 3.1 定义

**只有以下工作属于 LEVEL 3：**

| 类型 | 示例 |
|------|------|
| 数据 Migration | 从 Papers 迁移语料到 AITutor-X |
| 不可逆 Schema Change | 删除持久化字段、改数据库 schema |
| 大规模数据转换 | 全量 re-indexing、批量数据格式迁移 |
| 破坏性 Contract Change | 不兼容的接口变更 |
| 删除/合并数据树 | OQ-004 涉及的操作 |

### 3.2 流程（保留现有 Migration Governance）

```
Decision（Owner 裁决）
  ↓
Plan / Registry（迁移计划 + 候选登记）
  ↓
Implementation（执行迁移）
  ↓
Verification（hash 对账 + 测试）
  ↓
Closure（迁移记录 + UNKNOWN 保留）
```

### 3.3 此级别保留的规则

| 规则 | 来源 | 说明 |
|------|------|------|
| Migration Authority Charter | GF-003 / OD-01 | 迁移授权机制 |
| Gate 1–10 | GF-003 | 迁移证据链 |
| EvidencePackage schema | GF-003 §3 | 迁移证据格式 |
| Hash 对账 fail-closed | GF-003 P5 | 迁移数据完整性 |
| UNKNOWN retained | GF-003 P3 | 迁移缺口保留 |
| Migration ≠ Copy | GF-004 B1 | 逐项过 Gate |
| Untracked 不进 active tree | GF-004 B2 | 来源控制 |
| NAS read-only | OD-05 | 数据模式 |
| Difference Ledger | OD-18 | 迁移 lineage |

### 3.4 关键原则

> **Migration Governance 不得自动成为普通 Integration Governance。**

`preprocessing → V3` 的普通 Integration 不是 Migration。它不需要 Gate 1–10、不需要 EvidencePackage、不需要 Charter。

---

## 4. 简化后的日常规则

### 4.1 Document Creation（简化）

**现有**：9 项 Creation Gate，任一答不出 → 不得创建。

**建议**：3 项检查

```
1. 是否修改 Frozen Spec / 核心 Contract？
   → YES: 升级到 LEVEL 2
   → NO: 继续

2. 是否包含 secrets？
   → YES: 移除，用 .env
   → NO: 继续

3. 放在哪个目录？
   → 按现有目录层级放（不确定就放 60_REPORTS/）
```

**不需要**：authority level 判定、architecture fact 检查、重复 authority 检查、生命周期状态、引用闭包验证。

### 4.2 报告写作（简化）

**现有**：Evidence Classification Labels、Status Header 9 字段、数字三元元数据、Citation state 四态。

**建议**：
- 报告写清**做了什么、结果如何、有什么发现**即可
- 数字附来源（"来自 XX 文件"一行）
- 不需要 Evidence Classification Label
- 不需要 Status Header 9 字段
- 不需要 Citation state 四态

### 4.3 Closure（简化）

**现有**：每 Closure 附带"不等于"清单；Findings 独立挂账；"blocker 不自动 CLOSED"。

**建议**：
- **实现完成 + 测试通过 = 可以继续下一步**
- Findings 如果是真实 bug → 创建 issue / TODO，修的时候修
- Findings 如果是记录性 → 写在报告里即可
- **不再要求 "Closure ≠ Findings Closure" 的独立仪式**

### 4.4 DSH Adversarial Review（降级）

**现有**：每个 M-step 一次 DSH verification + Owner Closure（6 事件/bug fix）。

**建议**：
- DSH Review **仅用于 LEVEL 2/3 的重大变更**
- LEVEL 1 的 bug fix / feature 不需要 DSH
- 测试通过 = 足够的 evidence

### 4.5 Open Questions 管理（简化）

**现有**：18 条 OQ 零关闭；Closure Protocol 要求 Owner 书面裁决才可关闭；"禁止以赶进度把 OPEN 降级"。

**建议**：
- OQ 分两类：
  - **真正需要 Owner 裁决的**（架构方向、数据模式）→ 保持 OPEN，需要时问
  - **实际上已有答案的**（OD-04/05 已裁）→ 标记 RESOLVED-BY-OD-XX
  - **不重要的**（命名规范、文档口径）→ 标记 WONT-FIX 或降为 NOTE
- 允许在实现过程中自然关闭已解决的 OQ
- **不需要"零关闭"纪律**

---

## 5. 对现有文档的执行建议

### 5.1 立即可做（不需要 Owner Decision）

| 动作 | 说明 |
|------|------|
| 把 60_REPORTS 中的历史报告标记为 `HISTORICAL` | 头部加一行 Status 即可 |
| 在 X2.6-01/03 中清理陈旧记录 | P3/P9 等已 CORRECTED 的行 |
| 把「Implementation Queue = 0」的口径改为「按 LEVEL 1 可直接做的项」 | 语义修正 |

### 5.2 需要 Owner Decision

| 动作 | 说明 |
|------|------|
| 批准本 Minimal Governance Model | 作为新的工作方式 |
| 批准 60_REPORTS ARCHIVE 计划 | 移动 ~130 份历史报告到 90_ARCHIVE |
| 批准 GF-006 并入 GF-000 | 减少重复 |
| 批准 Creation Gate 9→3 | 降低文档创建门槛 |
| 裁决 OQ-016 namespace | 解除 40_DECISIONS 填充阻塞 |
| 裁决是否需要 Migration Charter | 如短期不迁移，可以推迟 |

### 5.3 关于 Migration 的建议

**短期建议：暂停 Migration Governance 的完善。**

理由：
1. 当前业务主线是 `preprocessing → V3 → Admission → Question`
2. 这是**普通 Integration**，不是 Migration
3. Migration Governance（Charter、Gate 1-10、Registry、Difference Ledger）完善本身就是一个巨大的治理工程
4. 在 Migration 真正需要之前，完善 Migration Governance 是「为了证明项目是严谨的，而建立一套比项目本身更复杂的系统」

**Migration Governance 保留为 LEVEL 3 规则文本（已 FROZEN 的 GF-003/004），但不主动推进其执行载体（Charter/Registry/Ledger）落盘。**

---

## 6. Owner 决策清单

Owner 看完后可以直接回答：

### Q: 以后什么事情需要停下来问我？

**A: 只有这 5 种：**
1. 实现方案与 Frozen Spec 明确冲突
2. 架构存在两个合理解释，选择不同会改变长期数据结构
3. 需要修改 Frozen Spec / Frozen Contract
4. 不可逆操作（数据删除、大规模 Migration、破坏性 Schema Change）
5. 项目目标变化（产品边界、核心业务模型）

### Q: 什么事情开发者可以直接做？

**A: 其他一切。** 包括但不限于：
- Bug fix、test fix、parser fix
- Preprocessing integration（输出 Contract 已定义的字段）
- Adapter implementation
- 普通 API / UI
- 非破坏性重构
- 增加测试
- 修复已知实现缺陷
- **完成已经明确的 Frozen Spec 实现**

### Q: 什么事情需要严格 Migration Governance？

**A: 只有这些：**
- 数据 Migration（Papers → AITutor-X 资产迁移）
- 不可逆 Schema Change
- 大规模数据转换
- 破坏性 Contract Change
- 删除/合并数据树

**普通 Integration（preprocessing → V3）不是 Migration。**

### Q: 哪些现有规则已经不应该再阻塞业务？

| 规则 | 理由 | 建议 |
|------|------|------|
| OQ 零关闭纪律 | 制造永久 OPEN 状态 | 允许自然关闭 |
| 每 M-step 独立 Owner 授权 | LEVEL 1 不需要授权 | 取消 |
| Decision ≠ Closure ≠ Authorization 三层解耦 | 单人项目过重 | 合并为一个事件 |
| DSH Review 作为每步前置 | 单人项目过重 | 仅 LEVEL 2/3 |
| Creation Gate 9 项 | 文档形式 | 简化为 3 项 |
| 矩阵记账不越权清理 | 制作文档-现实漂移 | 允许清理 |
| Findings 永久挂账 | 永远有 OPEN finding | 修完就关 |
| 87/71/166 引用纪律 | 过度引用治理 | 降为建议 |
| Freeze≠Auth 重复 ≥10 次 | 冗余 | 合并为单点声明 |
| 「Implementation Queue = 0」口径 | 自我阻塞 | 改为 LEVEL 1 口径 |

---

## 7. 最终目标

> **严谨，但不官僚。**
> **有边界，但不僵化。**
> **保护架构，但不保护文档本身。**
> **重大变化必须严格控制；普通开发应该能够直接推进。**
> **Governance 是安全护栏，不是业务流水线。**

---

*本文件为 RECOMMENDATION。不新增 Governance Framework。不修改 Frozen Spec。不关闭任何 OQ/BL/CL/X3P。批准后可作为工作方式参考，但不强制生成额外的 Registry/Gate/Contract。*
