# PHASE 1.3 — Reference Evidence Counterfactual Experiment

**Level**: LEVEL 1（隔离反事实实验，非修复）
**Date**: 2026-10-02
**Scope**: Producer positional evidence → 真实 reference read-point 的因果杠杆
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

**Git binding**：

```text
branch od01-r3-convergence @ 39840ff
match-norm/v1.1 dirty (blob 015cdfa vs HEAD 73badc3)
```

**禁止项已遵守**：未改 production adapter / resolver / reference.py / IRBuilder /
Frozen Spec / Contract / AnswerTokenContract / Authority / DB。仅新增 harness + JSON + 本报告。

---

## 0. 为何 1.2R 注入实验无效（Q1）

1.2R 把 `start_line/end_line` 写进 role dict。生产消费链是：

```text
reference.py::_stem_target   → 仅 question_label
reference.py::_option_target → 仅 label / question_label
reference.py::_answer_target → 仅 answer_zone / question_label
reference.py::_material_target → start_marker / end_marker   ← 唯一位置/标记入口
```

`start_line/end_line` **从未被读取**。故 A=B=35 **不能**证明「位置证据无效」。

**Q1 = YES，1.2R 的 start_line/end_line 实验作为因果实验是 INVALID 的。**

---

## 1. 真实 read-point 契约（实验合法性前提）

| 通道 | 生产读取字段 | 消费函数 | 本实验 bridge |
|---|---|---|---|
| **material** | `shared_components.material.start_marker/end_marker`（`granularity: multi_line_pair` + `text`） | `resolver._material_span:467-510` | **有效**：`material_lines` → 源文行文本作 marker |
| stem | `content.stem.question_label` | `_locate_question_start` / `_stem_span` | **无行号入口** |
| option | `content.options[].label` | `_locate_options` | **无行号入口** |
| answer | `content.answer.answer_zone` + `question_label` | `_answer_span:533-565` | **无行号入口**（zone 不参与定位） |

注入字段 → bridge → 真实读点 → 消费函数（file:line）已写入 `validity_checks.json`。

---

## 2. 输出矩阵（Q2–Q7）

| Experiment | Evidence | IR Ready | Delta vs A | Newly Ready | Remaining |
|---|---|---:|---:|---:|---:|
| **A** | none | **35** | 0 | — | 249 |
| **B1** | stem | **INTERFACE_BLOCKER** | — | — | — |
| **B2** | option | **INTERFACE_BLOCKER** | — | — | — |
| **B3** | answer | **INTERFACE_BLOCKER** | — | — | — |
| **B4** | material markers | **35** | **0** | **0** | 249 |
| **C** | all supported | **35** | **0** | **0** | 249 |

`newly_ready_unit_ids[]` = **[]**（B4/C）。

**B4 通道级因果（非 IR 级）**：

```text
unresolved material:  54 → 43   (−11)
material spans resolved: 11
```

⇒ marker bridge **到达消费者**且**有效**（validity 通过），但 **IR Ready 不变**。

---

## 3. Validity test

| 检查 | 结果 |
|---|---|
| B 相对 A 仅差一处预期证据 | ✅ 仅 `shared_components.material` 增 marker |
| 证据到达真实读点 | ✅ `_material_target` 读 start/end_marker；`_material_span` 解析 |
| 未改无关语义 | ✅ payload deep-copy，只改 material 声明 |
| production code 修改 | ✅ **0** |
| B1/B2/B3 若只注入 line 字段 | ❌ **INVALID**（与 1.2R 同）→ 记 INTERFACE_BLOCKER，不测假 delta |

---

## 4. Answer 专项（Q5 / 161+15）

| 类别 | n | 判定 |
|---|---:|---|
| answer_missing | **161** | `position_not_consumed`（接口阻塞） |
| answer_ambiguous | **15**（census）/ 实测归类 13+… | `position_not_consumed` |

**不是**「已证明位置无效」，而是 **ResolveTarget 无 answer 位置入口**，无法做合法反事实。

分类文件：`answer_missing_classification.json`。

---

## 5. Material 专项（Q6 / 54 composite）

| 阶段 | 事实 |
|---|---|
| B4 注入 | 54/54 composite 均注入 marker |
| material 解析 | **11 resolved / 43 still unresolved** |
| composite IR | **仍 54 incomplete，0 ready** |

残差（B4 后仍 incomplete 的 composite）：

| 残余引用组合 | n |
|---|---:|
| answer_missing + material_incomplete | 20 |
| material_incomplete only | 9 |
| answer_missing + stem_missing | 7 |
| answer_missing + material_incomplete + stem_missing | 7 |
| answer_missing only | 3 |
| material_ambiguous | 3 |
| 其他 | 5 |

**结论**：material 证据有 **通道级因果**（54→43），**不足以**使 IR ready。
composite 需要 stem+answer+options+material **多通道同时满足**。

---

## 6. 三层表述

### A. OBSERVED FACTS
矩阵、unresolved 计数、composite 残差表、接口阻塞代码行号。

### B. VERIFIED CAUSAL RELATION
1. material marker bridge **被消费**（11 material spans 从无到有）。
2. material-only 证据 **不能**把 composite 推到 IR ready（Δ ready=0）。
3. stem/option/answer **无** positional read-point；line 字段注入不可达消费者。

### C. HYPOTHESIS / NEXT DECISION
- 249 中 answer_missing（161）的主因更可能是 `_answer_span` 的答案区启发式
  （`is_answer_header` + qn entry），**无法**在不改 LEVEL 2 契约下用 producer 行号验证。
- 假设：若 LEVEL 2 允许 answer/stem 使用 marker 或 span 通道，B3/B1 才可测。

---

## 7. Q1–Q8

| # | 答案 |
|---|---|
| **Q1** | **YES — 1.2R start_line/end_line 实验 INVALID as causal**（字段不被读取） |
| **Q2** | **仅 material 可以**（start_marker/end_marker）；**stem/option/answer 不可以** → INTERFACE_BLOCKER |
| **Q3** | stem：**NOT TESTABLE**（无 read-point） |
| **Q4** | option：**NOT TESTABLE**（无 read-point） |
| **Q5** | answer：**NOT TESTABLE**（无 read-point）；161 missing / 15 ambiguous = `position_not_consumed` |
| **Q6** | material：**通道级有效**（unresolved 54→43）；**IR 级 Δ=0**；composite 多通道阻塞 |
| **Q7** | 组合效应 = **0**（C≡B4；其余通道阻塞） |
| **Q8** | **REQUIRED** |

### Q8 依据（不得写成已修）

要使 Producer 行号对 stem/option/answer 产生 **可测因果杠杆**，必须 LEVEL 2：
扩大 ResolveTarget / extract_targets / resolver，使这些 role 能消费 marker 或 span。
**现有契约下**：这些通道无法做合法反事实；material 虽可测，但不足以改变 284→35。

```text
Q8 = REQUIRED
```

（不是 NOT REQUIRED：B4 证明「有 read-point 时证据会被消费」；B1–B3 证明「无 read-point 时无法归因」。）

---

## 8. 产物

```text
e2e_run/phase1_3_counterfactual/phase13_counterfactual.py
e2e_run/phase1_3_counterfactual/experiment_matrix.json
e2e_run/phase1_3_counterfactual/newly_ready_by_experiment.json
e2e_run/phase1_3_counterfactual/answer_missing_classification.json
e2e_run/phase1_3_counterfactual/material_composite_analysis.json
e2e_run/phase1_3_counterfactual/validity_checks.json
```

**未修改生产代码。** 本实验不宣称 question quality / admission quality 提升。
