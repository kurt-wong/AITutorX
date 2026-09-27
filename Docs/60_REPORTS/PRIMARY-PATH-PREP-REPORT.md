# Primary Path Prep — Governance Boundary Adjustment

**Task**: MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01
**Type**: LEVEL 2（治理边界调整；本指令即 Owner Decision 记录）
**Date**: 2026-09-27
**Deliverable**: 2 / 2（Deliverable 1 = `Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md`）
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

---

## 1. Current Authority Model

| 档位 | 约束力 | 包含 |
|------|--------|------|
| **Normative** | 实现约束——必须遵守 | Frozen Spec（V3_SPEC）+ 冻结后的 Contract |
| **Informative** | 用于理解，不自动产生约束 | Architecture / Design / Implementation 说明 |
| **Historical Evidence** | 仅历史记录，不得阻塞 Level 1 | DSH Review / Verification / Closure / Audit 报告 |

**Historical Evidence 不得阻塞任何 Level 1 实现。**

变更分级：
- **LEVEL 1**：bug fix / 测试 / 已定义字段实现 / integration 修复 → 直接做，测试证明
- **LEVEL 2**：改 Frozen Spec / 架构边界 / Primary-Fallback 定义 → 需 Owner Decision
- **LEVEL 3**：Migration / 不可逆操作 → 保持现有严格治理

---

## 2. Primary Path Definition

**Primary Path（Spec Path B）**

```text
PDF/DOC/DOCX/IMAGE
  → Aitutors-preprocessing（Source Producer）
  → manifest + annotated markdown + semantic metadata
  → V3 ingestion → Resolver → ResolvedRun → IR → Admission
```

等价于 Frozen Spec 90 §H-C 的 Path B。本任务统一称 Primary Path。

---

## 3. Fallback Path Definition

**Fallback Path（Spec Native Path）**

```text
Source → Resolver → ResolvedRun
```

保留路径（备用 / 调试 / 特殊输入）。不作为当前生产链推进；不得因 Fallback Path 现在能跑就继续扩展它。

现有全部下游证据（13 个 admission_candidates，全部 pending_review）来自 Fallback Path（`POST /api/documents/import` + worker CLI）。**不得当作 Primary Path 的证据。**

---

## 4. Deprecated Governance Practices

下列机制**不再作为 LEVEL 1 的开发阻塞条件**：

1. 每个 M-step 独立 Owner Authorization
2. 每次代码修改必须产出 Closure + Verification + Registry + Evidence Package 完整链
3. DSH Review 作为每步实现前置
4. Implementation Queue 必须清零才能继续

**效力顺序**：上述机制的出处文档（X2.6-01 / X2.6-03 / GF-005 §5 等）属 Informative；与 DOC-GOV 冲突时以 DOC-GOV 为准；Frozen Spec 与冻结 Contract 除外。

**今后输出形状**：
- LEVEL 1 一轮 = 代码提交 + 测试输出 + ≤2 页说明
- 不再产出五件套（报告 + 证据包 + Closure + Verification + Registry）
- DSH 独立对抗评审：默认不执行；仅 Owner 明确要求时执行

---

## 5. Remaining Business Blockers

**B1** — preprocessing 产物 `.md`/`manifest` 无法进入正式 import
- `AITutors-v3/backend/app/domains/source/import_service.py:26`
- `_ALLOWED_EXTENSIONS = {".pdf", ".docx"}`

**B2** — consumer 永不持久化（事务内校验后 rollback）
- `AITutors-v3/backend/scripts/preprocessing_consumer/runner.py:296, :317`
- `finally: await session.rollback()`

**B3** — identity 缺失 → consumer fail-closed
- fresh manifest 顶层键仅 `source_file` / `model` / `annotation_meta` / `units`
- 无 `source_content_sha256` / `identity_version`
- consumer 返回 `MISSING_IDENTITY`，`downstream_executed = false`

**B4** — 即使补上 identity，下游仍停在 IR
- identity-complete 样本 Track A：`candidates_created=0`，`skipped = 53/53`
- 成因目前只有断言、无 per-unit 证据；唯一通过过 gate 的样本 model tag 为 `mimo-x-pro-preview`（迁移前历史产物）

### 三个事实边界

1. **identity 字段已存在**：定义于 `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` §0.1 ①（键名 `source_content_sha256`，64 位小写 hex）。该 Contract 标注为 DRAFT / NOT FROZEN。缺的是 producer 侧实现，不是契约文本。本任务不写、不改任何 Contract。

2. **命名澄清**（Owner, 2026-09-27）：Papers 就是 preprocessing 项目文件夹（remote: `github.com/kurt-wong/Aitutors-preprocessing.git`）。`D:\Project\Aitutors-preprocessing` = 同一代码的非版本化副本（无 .git），不是权威树。两棵树都不写 `source_content_sha256`；`_redact()` 与非 429-4xx 立即失败分支仅副本有。此前 ENABLEMENT-04/05 的 preprocessing 运行是从副本目录执行的。

3. **现有下游证据来自 Fallback Path**，不是 Primary Path（见 §3）。

---

## 6. Next-Task Prerequisites

下一轮为 **Primary Path Identity Enablement**。开工前提：

| # | 事项 | 状态 |
|---|------|------|
| 1 | 生产者权威树裁决 | **已澄清**：Papers 是项目文件夹，producer 变更提交到 Papers |
| 2 | 是否引入持久化 ingestion 入口？（B2） | **需 Owner 决定**（LEVEL 2） |

下一轮 LEVEL 1 工作项（不需 Owner Decision）：
- identity 字段实现（`source_content_sha256` / `identity_version` 输出）
- `_redact()` / 4xx 加固移植进 Papers
- `Papers/tests/test_no_config_import.py` 断言与代码对齐
- 测试补充

---

## 7. Verification

### 机械检查结果

| 检查项 | 结果 |
|--------|------|
| AITutors-v3 工作树 0 改动 | ✅ |
| Papers 工作树 0 改动 | ✅ |
| AITutorX/Docs 仅 DOC-GOV 修改 + Deliverable 2 新增 | ✅ |
| Frozen Spec 6/6 hash 未变 | ✅（见下表） |
| Contract hash 未变 | ✅ `9c6b9063…7528` |
| 无新增 Registry / Gate / Contract / 状态机 / 目录 | ✅ |
| 历史报告仍全部保留 | ✅ |

### Frozen Spec SHA256（未变）

```
c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4  00_Master_Spec.md
529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1  10_Data_Model.md
0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c  20_Document_Pipeline.md
db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89  30_Task_LLM_Safety.md
8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db  40_Development_Rules.md
8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7  50_Migration_Assets.md
```

### Contract SHA256（未变）

```
9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528  PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
```

### 四问回答

1. **当前生产路径是什么？** → Primary Path（= Frozen Spec Path B）
2. **Native Path 如何定位？** → Fallback Path（保留，不阻塞主链）
3. **哪些文档约束实现？** → Frozen Spec + 冻结后的 Contract
4. **哪些文档只是历史？** → DSH / Verification / Closure / Audit 报告

### Evidence

```
commit hash: （本次提交）
input: Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md（改写）
       Docs/60_REPORTS/PRIMARY-PATH-PREP-REPORT.md（新增）
output: 上述两文件
test result: no code change
```
