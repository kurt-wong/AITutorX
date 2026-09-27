# AITutorX Document Governance Baseline

**Document ID**: AITUTORX-DOC-GOVERNANCE
**Document Type**: Governance Meta-Spec
**Authority Level**: **L0-META**（文档治理元规范；**不定义业务语义**）
**Status**: `OPEN`（本文件为长期有效规则，非任务/追踪文档）
**Revision**: REVISED 2026-09-27 (MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01)；**REVISED 2026-09-27 (Productionization Cleanup Phase 2)**
**Normative**: YES（对**文档治理流程**规范）
**Supersedes**: 本文件 §7 的 2026-09-27 版（原「一律不做物理移动」表述已细化为 §7.1/§7.2 两分）；本文件 §8 的 2026-09-27 版（原词表未禁用 `ACTIVE`）
**Superseded By**: —
**Date**: 2026-09-21 / Revised 2026-09-27 ×2
**Upstream**: V3 `90_DOCUMENT_GOVERNANCE.md`；V3 `91_PROJECT_TERMINOLOGY.md`；AITutorX `GF-000`；AITutorX `AGENTS.md`
**Adaptation principle**: V3 Governance 为规则来源与成熟模板；AITutorX 目录结构为适配对象。最小适配，不机械复制。
**Owner Ratification**: Owner hereby accepts and ratifies this document as the current governance baseline for AITutorX (X2.6-BASELINE-CLOSURE-RECORD.md DSH-X26-03). Authority hierarchy: Owner Decision > Frozen Contract/Spec > Architecture/Governance documents. This ratification does NOT create a new Frozen Spec/Contract.
**Revision Authority**: MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01（Owner Decision，2026-09-27）。本次修订为治理边界收敛，不新增治理层。
**Revision Authority (2nd)**: AITutor-X 生产化整理 Phase 2（Owner 授权，2026-09-27）。本次修订补 `ACTIVE` 禁用、拆分 §7、新增 staleness 判据与产出规则。**仅文档治理流程，不触及 Frozen Spec / 冻结 Contract。**
**Productionization baseline**: tag `AITutor-X-before-cleanup` @ `43f46e8`

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
| `Docs/90_ARCHIVE/` | Historical（只读） | SUPERSEDED / stage-ended 文档；历史证据；已退出执行路径的产物 | 作为现行引用来源；被现行文档引用为依据 |
| **Root** | 入口 | README / AGENTS / 配置 / **§3 显式授权的 canonical docs** | 报告、审计、临时分析、Closure records |

> **`Docs/60_REPORTS/` 全目录为 Historical Evidence，不构成实现约束。**

---

## 3. Root Directory Rule

> **Root 不是阶段报告堆放区。**

Root 允许：README.md / AGENTS.md / .gitignore / LICENSE / build metadata / 授权的 project-level canonical docs。

Root 禁止：报告、审计、临时分析、Closure records 等属于 `Docs/*` 的文档。

### 3.1 Canonical docs 显式授权清单

§3 所称「授权的 project-level canonical docs」**必须在此逐一点名**，不靠推断：

| 文件 | 授权依据 | 说明 |
|------|---------|------|
| `README.md` | 本规则 | 入口：项目身份 / 导航 / 目录结构。**不承载状态** |
| `AGENTS.md` | 本规则 | Agent 行为约束 |
| `MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01.md` | Owner Decision（2026-09-27） | 该 Owner Decision 的载体；其文件名与 commit hash 即授权记录 |

**未列入本表的文件不得放在 Root。** 新增需 Owner Decision 并更新本表。

> `CURRENT_STATE.md` **不在 Root**，其位置为 `Docs/50_OPERATIONS/CURRENT_STATE.md`（见 §2）。README 以链接指向它。

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

## 7. Document Migration / Disposition（两分）

> **原表述**「历史报告保留为 Historical Evidence，不做物理移动」**过于笼统**：它把「为美观乱搬」与「归档处置」混为一谈，导致 `90_ARCHIVE/` 长期空置，且与 `GF-004` §4/§6（Frozen，OD-14）明文允许归档历史工件相冲突。
> 按已确立层级（`GF-006` §8：Owner Decision > Frozen Contract/Spec > Architecture/Governance），**GF-004 优先**。本节据此细化为两类，不再一刀切。

### 7.1 禁止：装饰性重排（Rule M-2，继续有效）

**禁止**仅为「看起来干净」而大规模移动/重排 `Docs/` 目录或重新分类报告族。

判定：**若移动的收益仅是可读性、且无类型错误或违规事实，则不做。**

> 依据：`60_REPORTS` 存在大量文档间路径引用，大范围移动的成本高于收益。

### 7.2 允许：归档处置（Archival Disposition）

下列情形**允许移动**，但**必须逐项登记**：

| 情形 | 允许动作 | 要求 |
|------|---------|------|
| **类型错误**（决策载体误置于 `60_REPORTS`） | 移入 `40_DECISIONS/` | 更新所有引用路径 |
| **Root 违规文档**（报告/临时物误置于 Root） | 移入 `60_REPORTS/` 或 `90_ARCHIVE/` | 更新所有引用路径 |
| **阶段已结束的 state / tracking 文档** | 移入 `90_ARCHIVE/stages/` **或**原地加 `ARCHIVED` 状态头 | 二选一；原地标注优先（成本更低） |
| **已被取代的报告族** | 移入 `90_ARCHIVE/` | 保留唯一有效终态在主位 |
| **非作者撰写的生成物**（运行账目、临时导出） | 移入 `90_ARCHIVE/evidence/` 或删除 | 见 §7.3 |

### 7.3 删除规则（极窄）

**删除**须**同时**满足：

```text
1. 生成物，非作者撰写
2. 已被某份报告收录（存在替代载体）
3. 可低成本再生（无 LLM / OCR 调用，或产物 hash 已随报告留存）
```

不满足则**归档**，不删除。**任何作者撰写的文档一律不删除**（`AGENTS.md`：不删除旧文档）。

### 7.4 移动必守事项

```text
- 必须用 git mv（保留历史），不得用 rm + 新建
- 移动后必须更新所有指向旧路径的引用
- 移动前必须实测「哪些引用会断、分别在哪一行」（机械检查，不靠推断）
- 裸文件名引用（无目录前缀）不受移动影响，无需修改
```

> `[RESTORED]` 本条曾以「DOC-GOVERNANCE.md §3.3 / §7.2：注明 TRACKED + migration 用 `git mv`」形式存在于
> `X2.6-BASELINE-CLOSURE-RECORD.md` DSH-X26-02 的处理记录中，但该注记在 2026-09-27 的 DOC-GOV 重写中丢失。
> 现于 §7.4 恢复。**已核实事实**：原 11 份 root-level DSH 报告为 **git TRACKED**；迁移须用 `git mv`
> （已于 2026-09-27 执行，见 commit `c68e100`）。

---

## 8. Document Lifecycle Status（受限词表）

适用范围：**任务 / 追踪 / 阶段状态 / 报告类文档**。

| Status | Meaning |
|--------|---------|
| `OPEN` | 进行中 |
| `CLOSED` | 已完成 |
| `DEFERRED` | 推迟 |
| `ARCHIVED` | 已归档（历史，不构成现行依据） |

**明确排除（不得改动、不得重命名）**：
- 产品状态：`admission_candidates.decision_status`（如 `pending_review`）
- Frozen Spec 定义状态：`semantic_status ∈ {ready, incomplete, unknown}`
- GF-005 的 OQ 状态（该文件为 FROZEN GOVERNANCE BASELINE，OD-14，不修改）

### 8.1 `ACTIVE` 不再合法

**`ACTIVE` 不在词表内，不得再用于新文档。** 禁止的自然语言状态包括但不限于：

```text
ACTIVE / COMPLETE / FINAL / FINAL-FINAL / DONE / IN-PROGRESS / 进行中
```

**存量处置**：若文档为**长期有效规则**（如本文档、Frozen Spec 引用），用 `OPEN` 并在 `Revision` 字段记版本；
若为**阶段/追踪文档**，改为 `CLOSED` 或 `ARCHIVED`。

> `[FACT]` 2026-09-27 前，`Docs/50_OPERATIONS/` 全部 17 份状态文档均写 `ACTIVE`（含本文档自身）。
> 已于生产化整理 Phase 1-4 全部标记为 `ARCHIVED` 并加 `Superseded By` 指针。

---

## 8A. Staleness 判据（机械可判定）

归档决策**不靠主观判断**，用下列机械指标：

```text
指标 A（commit offset）：文档最后修改 commit 落后 HEAD 的 commit 数
指标 B（cited_by）    ：是否被较新文档引用为依据

归档候选 = (指标 A > 50) AND (指标 B = 无)
例外：装载「为什么」（决策依据）的文档 → 保留在主位，不归档
```

复核命令：

```bash
git log -1 --format=%h -- <path>          # 该文档最后修改 commit
git rev-list --count <sha>..HEAD          # 落后多少
```

> 判据理由：`AGENTS.md` 要求保留决策依据。代码只记录结论，**理由在文档里**；
> 归档「过程」但必须保留「为什么」。

---

## 8B. 文档产出规则（防止再膨胀）

> `[FACT]` 2026-09-23 → 2026-09-27 的 4 天内，`Docs/` 由 175 份增至 183 份（+8），
> `60_REPORTS/` 由 104 份增至 112 份（+8）。无产出上限是文档失控的直接原因。

```text
R1  每个任务最多产出 1 份文档。
    报告 = 证据 + 结论合一；不再拆 Report / Review / Verification / Closure 四件套。
    例外须 Owner 显式批准。

R2  文件名必须可判定归属：生产者名字不得出现在文件名中。
    禁止：CLAUDE / MIMO / DSH（那是生产者，不是文档类型）。

R3  新文档文件头必须回答三个问题：
      supersedes:     我取代了谁？（无则写 —）
      superseded_by:  我被谁取代？（无则写 —）
      readers:        谁读我？
    答不出「我取代了谁」且非新增规则的文档，不应存在。

R4  新增文档前先问：这是证据还是结论？
    结论 → 40_DECISIONS/；证据 → 60_REPORTS/；规则 → 00_GOVERNANCE/。

R5  每份新报告必须显式声明 disposition：RETAIN / SUPERSEDES-<file> / ARCHIVED。
```

> 依据：`GOVERNANCE-SIMPLIFICATION-REVIEW.md` 结论——「AITutor-X 本身是纯治理仓库，
> 其文档量已超过所治理的业务代码量，属典型的『治理系统比项目本身更复杂』」。

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

*Revised again 2026-09-27 under the AITutor-X Productionization Cleanup (Phase 2, Owner-authorized).
Changes: §3.1 Root canonical-docs allowlist made explicit; §7 split into 7.1 (forbid decorative
reshuffling) / 7.2 (permit registered archival disposition) / 7.3 (narrow deletion rule) / 7.4 (git mv
requirement + restored DSH-X26-02 note); §8.1 bans `ACTIVE`; §8A adds a mechanical staleness criterion;
§8B adds document-production rules R1–R5 to stop re-accumulation. No Frozen Spec or frozen Contract touched.*
