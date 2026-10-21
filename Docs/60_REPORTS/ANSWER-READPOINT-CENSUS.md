# ANSWER READ-POINT CENSUS（零代码 · 43 candidates）

**Date**: 2026-10-02  
**Baseline**: Alembic **0011** · reseed 9 卷 · candidates **43**  
**禁止项已遵守**: 未改 resolver / adapter / Producer / Spec / migration / overlap invariant / 测试 / 数据

---

## 1. 汇总（来自 **candidate payload.answer**，非重推）

| answer_resolution_state | n |
|---|---:|
| **IN_DECLARED_ANSWER_ZONE** | **38** |
| **OUTSIDE_DECLARED_ANSWER_ZONE** | **5** |
| NO_ANSWER_SPAN | 0 |
| AMBIGUOUS | 0 |
| **total** | **43** |

| source_version_binding | n |
|---|---:|
| **SAME_SOURCE_VERSION** | **43** |
| **CROSS_SOURCE_VERSION** | **0** |

| outside_by_location | n |
|---|---:|
| **OTHER_UNIT_ANSWER**（落入他 unit 答案区/共享答案表） | **5** |
| OWN_STEM / OWN_MATERIAL / 其他 | 0 |

---

## 2. Q27 证据（与 DSH 口径对账）

```text
unit              = Q27
file              = 数学（不是英语）
declared answer   = [593, 623]
resolved line     = 593
resolved text     = "27."          ← 答案块起始行
state             = IN_DECLARED_ANSWER_ZONE
source_version    = SAME
```

**OBSERVED**：Q27 的 593 落在 **本卷 declared [593,623]** 内，**不是**英语听力正文。  
**DSH「Q27→P1L593→英语听力」= NOT CONFIRMED**（疑为不同 unit/不同测量口径）。

---

## 3. 5 条 OUTSIDE 明细

| unit | 卷 | declared | got | 落点 |
|---|---|---|---|---|
| Q8 | 化学 | [513,513] | 578 | **U-cl3.answer [574–584]** |
| Q1 | 数学 | [200,206] | 747 | **Q30.answer [691–749]** |
| Q2 | 物理 | [356,356] | 368 | **Q24/Q25/Q26 答案表** |
| Q6 | 物理 | [356,356] | 368 | 同上（共享表） |
| Q8 | 物理 | [356,356] | 373 | **Q26/Q27/Q28 答案** |

**机制（INFERRED）**：共享 packed answer table / 答案块上 **qn entry 误匹配** 到邻题行——不是跨 source_version。

---

## 4. 英语听力（文件内 6 candidates）

| unit | state | line |
|---|---|---|
| U26-40.sub | IN_DECLARED | 459 |
| U41-44 / U45-48 / U49-52 / U53-56.sub | IN_DECLARED | 463（共享答案表） |
| U57-60.sub | IN_DECLARED | 465 |

**Q1–Q25 听力选择题不在 43 个 candidate 中**（多因 IR not-ready / skip）。  
不存在「听力 Q1–Q25 被 593 污染」的当前证据。

---

## 5. Answer-span reuse

| line | units |
|---|---|
| 物理 368 | Q2, Q6 |
| 英语 463 | U41-44, U45-48, U49-52, U53-56 |

英语 463 = **合法共享答案表**；物理 368 = 共享表上的误匹配源。

---

## 6. 49 vs 43

| | |
|---|---|
| **49** | `fourth_cut_e2e_report.json` — **B3b density-max 仍在** 时的 run（math 28 / physics 4） |
| **43** | `fourth_cut_rerun_baseline_e2e.json` — **B3b 已撤 + 0011 reseed**（math 23 / physics 3） |
| 原因 | **代码状态不同**（有/无 B3b），非同一次 DB 漂移 |
| **当前基线** | **只认 43** |

---

## 7. 对 B3c 的事实结论

```text
OBSERVED
  38/43 answer 落在 declared zone
  5/43 OUTSIDE，全部 OTHER_UNIT_ANSWER（同 source_version）
  0 CROSS_SOURCE_VERSION
  Q27 = 合法 declared 593，非跨卷

INFERRED
  OUTSIDE = 共享答案表/答案块上的 qn 误匹配（read-point 过宽或 entry 匹配松）

NOT YET PROVEN
  存在跨 source_version 绑定错误
  英语听力 Q1–Q25 大规模污染
  单一全局 answer-zone 规则即可覆盖
```

**B3c = OBSERVED DEFECT（5/43 OTHER_UNIT_ANSWER）**  
**≠ 已授权实现**；根因更像 **共享答案表 qn 归属**，不是跨卷 binding。  
**暂不改 `_answer_span()`**。

---

## Evidence

```text
e2e_run/phase1_3r/answer_readpoint_census.json
```
