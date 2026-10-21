# PHASE 1.3R — Evidence Reconciliation & Material Resolver RCA

**Level**: LEVEL 1（消歧 + RCA，非修复）
**Date**: 2026-10-02
**Git binding**: `od01-r3-convergence` @ `39840ff` · `match-norm/v1.1` dirty (`015cdfa` vs HEAD `73badc3`)
**禁止项已遵守**：未改 production code / Spec / Contract / Authority / DB。

---

## 1. P0 — Answer census 161/15 vs 167/13

### Q1 = `CLASSIFICATION_DRIFT` · VERDICT = **RESOLVED**

| 口径 | answer_missing | answer_ambiguous |
|---|---:|---:|
| Phase 1.2R census（strict unit 键） | **161** | **15** |
| Phase 1.3（`rid.startswith(unit_id)`） | 167 | 13 |
| **同 IR / 同 unresolved 集重算 strict** | **161** | **15** |

**根因（代码事实）**：`phase13_counterfactual.py` `_prim_from_unresolved` 使用

```python
if uid != unit_id and not rid.startswith(unit_id): continue
```

`unit_id="Q3"` 会吞并 `Q30.*` / `Q31.*`；`Q1` 吞并 `Q10.*`…
12R census 按**精确 derived uid** 分桶。IR 状态 / DB / worktree **均未变**（Case A）。

**Unit 级证据**（`answer_reason_reconciliation.json`）：

| 动作 | n | unit |
|---|---:|---|
| → answer_missing | **7** | 化学 Q1,Q2；生物 Q1–Q5 |
| answer_ambiguous → answer_missing | **2** | 化学 Q2；生物 Q2 |
| answer_missing → material_* | **1** | 政治 Q3（泄漏 material 高优先） |
| 净核对 | | 161+7−1=**167**；15−2=**13** ✅ |

非 NON_DETERMINISTIC、非 input/baseline 差异。

---

## 2. P1 — Material 43 unresolved RCA

产物：`material_counterfactual_rca.json` / `material_resolved_controls.json`。

### Q2 / Q3 — failure distribution（精确）

| taxonomy | n | 桶 |
|---|---:|---|
| **INTERIOR_EMPTY** | **20** | span boundary / interior semantics |
| **MATERIAL_OVERLAP_REJECTED** | **20** | overlap invariant（与 stem/answer/其他 material 重叠） |
| **START_MARKER_AMBIGUOUS** | **2** | marker resolution |
| **START_MARKER_NOT_FOUND** | **1** | marker resolution |
| **合计** | **43** | |

```text
marker resolution failure          =  3
span boundary / interior semantics = 20
overlap rejected (resolver invariant) = 20
other                              =  0
```

### 逐 unit 可复核字段

`unit_id · document_id · material_lines · start/end_marker_text · match_count ·
start/end_seq · material_span_status · failure_taxonomy · other_ir_blockers`

### Marker 原文自匹配

| 组 | start_match_count |
|---|---|
| 11 resolved | 全部 = 1 |
| 43 unresolved | 35×1 + 8×2（歧义） |

失败**不是**「marker 文本找不到」为主因——35/43 文本唯一仍失败。

---

## 3. Q4 / Q5 — material_lines 语义 vs Resolver

| | Producer | Resolver |
|---|---|---|
| 定义 | `material_lines: [起始行号, 结束行号]` | `multi_line_pair` marker 之间 |
| 语义 | **INCLUSIVE 内容区间**（`chk_range` 允许 start==end；QC C12 material⊆questions） | **EXCLUSIVE interior**：`between(s_seq+1, e_seq)` |
| 证据 | `reslice_pipeline.py:312,391-397,581-584` | `resolver.py:485-496`「排他」 |

**Bridge（1.3）** 把 inclusive 首尾行文本当作 start/end marker → resolver 只要中间：

- N=1（20 个）→ interior 空 → **INTERIOR_EMPTY**
- N=2 → 同样空
- N≥3 → 丢掉首尾两行内容

**Q5 = `MISALIGNED`**

---

## 4. Q6 — 为什么 11 成功、43 失败

| 特征 | 11 resolved | 43 unresolved |
|---|---|---|
| 内容行数 N | **全部 ≥3**（3–32） | **20 个 N=1**；其余 4–109 |
| start 唯一 | 11/11 match=1 | 35 match=1 + 8 match=2 |
| overlap | 无 | **20 个**被 `_enforce_material_overlap` 拒 |
| 结构 | marker 唯一 + interior 非空 + 不碰 stem/answer | 否则 |

**结构化差异成立**：成功 = (N≥3) ∧ (marker 唯一) ∧ (无 overlap)；失败三类见 §2。

---

## 5. 三层表述

### A. OBSERVED
census / RCA JSON / 代码行号 / 计数表。

### B. VERIFIED CAUSAL
1. 161/167 = **前缀碰撞分类漂移**，非 IR 变化。
2. 20/43 material 失败 = **inclusive vs exclusive 语义错位**（N=1）。
3. 20/43 = **overlap invariant**（resolver 拒 material∩stem/answer）。
4. 3/43 = marker 定位（歧义/未找到）。

### C. HYPOTHESIS
- Overlap 组：Producer `material_lines` 可能与 sub.stem_lines 在语料上本就重叠
  （完形/阅读 material⊆questions 嵌套），与 V3「material 不得与 stem 重叠」不变量冲突。
  需 Owner 裁决谁让步（**未证**为 bug 归属）。

---

## 6. Q1–Q7

| # | 答案 |
|---|---|
| **Q1** | **CLASSIFICATION_DRIFT · RESOLVED**（startswith 前缀碰撞；+7/−2/1 转 material 已对账） |
| **Q2** | INTERIOR_EMPTY 20 · OVERLAP_REJECTED 20 · START_AMBIG 2 · START_NOT_FOUND 1 |
| **Q3** | marker 3 / interior 20 / overlap 20 / other 0 |
| **Q4** | `material_lines` = **inclusive 内容行区间** |
| **Q5** | **MISALIGNED**（exclusive marker interior vs inclusive content） |
| **Q6** | 成功需 N≥3 ∧ marker 唯一 ∧ 无 overlap；见对比表 |
| **Q7** | **NOT YET DETERMINED** |

### Q7 说明

Q1 已 RESOLVED，但 Q2 已拆出的因果是：

1. 语义错位（resolver 边界语义 / bridge 映射）→ **可先在实验/文档层修 bridge 映射或裁决 range 语义**，不一定需要 LEVEL 2 positional interface；
2. overlap 不变量与 Producer 嵌套语义冲突 → **Resolver/Producer 不变量裁决**，与「是否让 Resolver 消费行号」正交；
3. answer 161 的 LEVEL 2 问题**仍无合法反事实**（INTERFACE_BLOCKER 未变）。

在 overlap 归属与 inclusive/exclusive 裁决前，**不能**说 LEVEL 2 positional interface 已具备充分批准条件。

```text
Q7 = NOT YET DETERMINED
```

**禁止推理（本轮未用）**：249→位置一定能解；answer 176→LEVEL2 一定能解；delta=0→位置无效。

---

## 7. COMPLETE 核对

```text
[x] 161/167 消解
[x] 15/13 消解
[x] 43 material 逐 unit RCA
[x] 11 resolved 逐 unit 对照
[x] material_lines 语义确认
[x] resolver marker 语义确认
[x] 一致性 = MISALIGNED
[x] 未改生产代码
[x] LEVEL 2 重判 = NOT YET DETERMINED
```

---

## Evidence

```text
e2e_run/phase1_3r/answer_reason_reconciliation.json
e2e_run/phase1_3r/phase13r_answer_reconcile.py
e2e_run/phase1_3r/material_counterfactual_rca.json
e2e_run/phase1_3r/material_resolved_controls.json
e2e_run/phase1_3r/material_lines_semantics.json
e2e_run/phase1_3r/phase13r_material_rca.py
```

**Owner 下一步二选一（本报告不实施）**：

1. 裁决 inclusive/exclusive + overlap 不变量归属（Resolver 边界）；或
2. 在语义对齐后仍不够，再审 LEVEL 2 positional reference interface。
