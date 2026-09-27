# CURRENT_STATE — AITutor-X 当前状态

**Document ID**: CURRENT_STATE
**Document Type**: Operations / Current State
**Status**: `OPEN`
**Date**: 2026-09-27
**Supersedes**: 本文件取代 `Docs/50_OPERATIONS/` 下全部 `*-STATE.md` 的 current-state 含义（那些文件为历史阶段快照，其正文不改写）
**Authority**: 本文件是**状态登记**，不是决策、不是规范、不授权任何迁移
**Owner Decision**: 目标定位 — AITutor-X = **交付仓库**（合并 `Papers` + `AITutors-v3` 为完整项目）

---

## 0. 这个仓库是什么

AITutor-X 是**交付仓库**：把两个来源仓库经集成后合并为完整项目。

| 角色 | 仓库 | 本地路径 | 当前 HEAD |
|---|---|---|---|
| 治理 / 交付目标 | `kurt-wong/AITutorX` | `D:\Project\AITutor-X` | `c68e100` |
| Consumer（V3） | `kurt-wong/AITutors-v3` | `D:\Project\AITutors-v3` | `3bf7a09`（分支 `od01-r3-convergence`） |
| Producer（preprocessing） | `kurt-wong/Aitutors-preprocessing` | `D:\Project\Papers` | `969d39a`（`main`） |

**代码尚未迁入本仓库**：`preprocessing/` `backend/` `frontend/` `archive/` 仍为空骨架（仅 `.gitkeep`）。
代码目前**在来源仓库中运行**，未复制到此处。

> `D:\Project\Aitutors-preprocessing`（无 `.git`）是 `Papers` 的非版本化副本，**不是权威树**。

---

## 1. Primary Path（生产路径）状态

**Primary Path（Spec Path B）** = `Source → preprocessing → Adapter → ResolvedRun`

| 能力 | 状态 | 证据 |
|---|---|---|
| Producer identity 输出 | **DONE** | Papers `b2266d2`：`source_content_sha256` + `identity_version: 2` |
| Option span 展开 | **DONE** | Papers `969d39a`：`_expand_option_spans()` 产出 `options: [{label,start_line,end_line}]` |
| Consumer 消费 per-option | **DONE** | V3 `3bf7a09`：`manifest_reader` / `annotation_adapter` / `resolved_span_adapter` |
| Persistence（最小开启） | **DONE** | V3 `3bf7a09`：`runner.py` 成功路径 `rollback()` → `commit()`；异常路径保留 `rollback()` |
| Gate → Candidate 真实落库 | **PENDING** | 需一次带 DB 的真实运行 |
| Downstream IR / Admission / Question materialization | **PENDING** | 待落库验证后推进 |
| Frontend | **NOT IMPLEMENTED** | 无 Question / Material / Instance API |

### 1.1 关键因果（为什么之前一直卡住）

```
Producer 只声明 options_lines（整段行区间）
  → V3 IRBuilder 需要 per-label span（sp-Q1.option.A）
  → adapter 拒绝伪造证据 ⇒ 不声明 options
  → IR: "options missing for choice type" ⇒ semantic_status = incomplete
  → gate/service.py:178 「!= ready ⇒ skipped」⇒ 永不产生 candidate
```

**2026-09-27 已修复**（`969d39a` + `3bf7a09`）。实测证据见
`Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-PROBE-RESULT.md` 与 `PRIMARY-PATH-MINIMAL-LOOP-01.md`。

### 1.2 尚未解决的真实边界

| # | 项 | 状态 |
|---|---|---|
| B1 | `import_service.py:26` 仅允许 `.pdf`/`.docx`；preprocessing 产物 `.md`/`.manifest.json` 无法走正式 import | OPEN |
| B4 | identity 通过后，下游 IR/admission 链的持久化闭环 | OPEN（部分已随 `3bf7a09` 推进） |
| — | `role: "native"` / `provider: "native"` 的 provenance 标记不符合 Primary Path 真实来源 | OPEN |
| — | Gate auto_approve 仅覆盖 `{single_choice, multiple_choice, true_false}`（Owner 裁决 2026-09-06）；`short_answer`/`essay` 等结构性走 `pending_review` | BY DESIGN |

---

## 2. 治理状态（区分「仍需遵守」与「已成历史」）

### 2.1 仍然有效 —— 实现必须遵守（Normative）

| 文档 | 位置 |
|---|---|
| Frozen Spec（6 份） | `AITutors-v3/Docs/V3_SPEC/`（**不在本仓库**） |
| 冻结 Contract | `AITutors-v3/Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md`（sha `9c6b9063…7528` @ `f4941ff`） |
| `AITUTORX-DOC-GOVERNANCE.md` | `Docs/00_GOVERNANCE/` — 文档治理规则 |
| `AGENTS.md` | 仓库根 — Agent 行为约束 |

### 2.2 已成历史 —— 不构成实现约束

| 文档族 | 状态 | 说明 |
|---|---|---|
| `GF-000` ~ `GF-006` | **FROZEN（OD-14），原地保留** | 迁移治理基线。迁移**未执行**，故仍在原位。冻结内容未经 Owner 授权不得变更/移动。迁移完成后转为历史 |
| `Docs/50_OPERATIONS/*-STATE.md`（17 份） | **ARCHIVED** | 均为阶段快照，最后修改 ≤ 2026-09-22 |
| `Docs/60_REPORTS/**` | **Historical Evidence** | 全目录，不构成实现约束（DOC-GOV §2） |
| 全部 "X2 / X2.5 / X2.6 / X2.7" 阶段文档 | **历史** | 阶段已结束 |

> ⚠️ `Docs/60_REPORTS/PERSISTENCE-BOUNDARY-DECISION-01.md` 等 3 份**决策载体**已于
> 2026-09-27 归入 `Docs/40_DECISIONS/`（原在 `60_REPORTS/`，属分类错误）。

### 2.3 迁移相关（未关闭，**但不阻塞 Primary Path 实现**）

```text
Migration Authorization      = UNAVAILABLE（Charter requirements 未满足）
Migration Gate               = NOT PASSED / NOT RUN
GATE_PASSED / MIGRATED       = 0 / 0
admitted=true                = NONE
OQ-GF                        = 18 条，零 CLOSED；OPEN-BLOCKING = 9
BL-09 / BL-10 / BL-11        = OPEN
D-048                        = pending_owner_decision
```

**重要边界**：上列各项阻塞的是**迁移**（把两个仓库搬入本仓库），**不阻塞**在来源仓库中继续实现 Primary Path。已实证：`969d39a` + `3bf7a09` 的修改在**未解锁任何迁移治理项**的情况下完成并通过测试。

---

## 3. 代码落位（未来合并目标）

| 来源 | 规模 | 目标位置（待迁移） |
|---|---|---|
| `AITutors-v3/backend/app` | 174 files | `backend/` |
| `AITutors-v3/frontend` | 1262 files | `frontend/` |
| `Papers/scripts` | 118 files | `preprocessing/` |
| `Papers/ocr_service` | 9 files | `preprocessing/` |

**迁移须走 GF-003/004 的 Migration Gate。** 未通过前不得整体拷贝（GF-004 §4 明确禁止整仓拷贝）。

---

## 4. Git 与推送状态

```text
AITutor-X   main              c68e100   已本地提交，未 push
Papers      main              969d39a   origin/main 已同步
AITutors-v3 od01-r3-convergence 3bf7a09  origin 落后 4 个 commit（含 Primary Path 实现）
```

> ⚠️ **V3 的 Primary Path 实现（`3bf7a09`）当前只存在于本地**，GitHub 上还没有。
> 任何人 clone 下来看到的都不是这个版本。

---

## 5. 我该信什么 / 不该信什么

| 想了解 | 读这个 |
|---|---|
| 项目整体在哪 | **本文件** |
| 文档该怎么写/放 | `Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md` |
| 系统应当是什么样 | Frozen Spec（在 V3 仓库） |
| 跨系统边界 | 冻结 Contract（在 V3 仓库） |
| 为什么这样决策 | `Docs/40_DECISIONS/` |
| 历史过程 | `Docs/60_REPORTS/`（**历史证据，勿当现行依据**） |

**不要**把 `Docs/60_REPORTS/` 或 `Docs/50_OPERATIONS/*-STATE.md` 当作当前事实来源——
它们记录的是产生时点的状态，多数已过期。

---

*Registered 2026-09-27 under the AITutor-X productionization cleanup.*
*Baseline tag before cleanup: `AITutor-X-before-cleanup` @ `43f46e8`.*
