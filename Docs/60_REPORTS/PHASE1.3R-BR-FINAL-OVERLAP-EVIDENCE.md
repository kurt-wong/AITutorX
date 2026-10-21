# PHASE 1.3R-BR — Final Overlap Evidence Reconciliation

**Level**: LEVEL 1（证据补全，非新 RCA / 非修复）
**Date**: 2026-10-02
**Baseline**: `39840ff` · `match-norm/v1.1` dirty `015cdfa`（与 1.3R-B 相同）
**禁止项已遵守**：未改 production code / Spec / schema / resolver / adapter / Producer / bridge / overlap invariant。

---

## P0 — Exact 20 units（与 1.3R-B 一致）

```text
overlap_units_count = 20
```

`U52 U53 Q37 | Q1 Q2 Q3 Q4 Q5-6 Q7-8 Q9-11 Q12-14 Q15-17 Q18-20 Q21-25 | U49-52 U53-56 U57-60 | U10-13 U14 U15`

**未重新分类。**

---

## P1 — Resolved material span（pre-demotion）

方法：在 `_enforce_material_overlap` 入口对 `out.resolved` 做 **runtime spy**（不改生产文件），捕获 demote 前的 `ResolvedSpan.line_refs`。

代码原因（若拿不到）：demote 后 span 移出 `resolved`，仅存 UnresolvedReference（证据串是**冲突对方**行号，不是 material 自身）。

| 现象 | 证据 |
|---|---|
| 英语附录 material declared ≈ L500 | resolved count **470–492 行**（marker 文本被定位到全文） |
| 历史/语文嵌套 material | resolved 与 declared 接近（22/32/13/19 行） |

---

## P2 — 4 vs 10 消歧

| Measurement | Definition | Count | 来源 |
|---|---|---:|---|
| **declared material ∩ own stem** | Producer `material_lines` inclusive ∩ own stem `line_numbers_1b` | **4** | DSH |
| **resolved material ∩ own stem** | pre-demotion `ResolvedSpan.line_refs` ∩ own stem | **10** | 本轮 spy |
| **evidence mentions own stem** | demotion 证据含 `sp-<uid>[.sub].stem` | **10** | MIMO 1.3R-B |

```text
verdict = NOT A CONTRADICTION
```

**口径不同**：
- DSH 的 4 = **声明区间**（inclusive）∩ 自家 stem；
- MIMO 的 10 = **证据串/解析后 span** ∩ 自家 stem；
- **resolved ∩ stem 也 = 10**，与 evidence 一致。

英语 Q1/Q2/Q4/Q5-6/Q7-8/Q18-20：declared∩stem=0，但 resolved span 因 **marker 重定位**扩成数百行后与自家 stem 相交 → 计入 10。

---

## P3 — 地理关系（仅 material_lines vs questions_lines）

| material_question_relation | n |
|---|---:|
| **SAME_REGION** | **2** |
| **PARTIAL_REGION_OVERLAP** | **7** |
| **DIFFERENT_REGION** | **11** |
| UNKNOWN | 0 |

---

## P4 — Overlap target（非互斥 presence / 互斥机制）

**非互斥**（可叠加）：

| kind | units |
|---|---:|
| OWN_STEM | 10 |
| OTHER_UNIT_STEM | 8 |
| MATERIAL | 13 |
| ANSWER | 8 |

**互斥 mechanism**（每 unit 一条）：

| Mechanism | n |
|---|---:|
| A_SAME_REGION_OWN_STEM | 2 |
| A_PARTIAL_REGION_OWN_STEM | 2 |
| A_PARTIAL_REGION_OTHER | 5 |
| B_MARKER_RELOCATION_DRIFT | 6 |
| B_CROSS_REGION_MATERIAL_MATERIAL | 4 |
| B_CROSS_REGION_ANSWER | 1 |

---

## P5 — Two-mechanism test

| | n | 形态 |
|---|---:|---|
| **Mechanism A** 同区/半同区结构碰撞 | **9** | material 嵌在 questions 内 → sub.stem 进 material → overlap |
| **Mechanism B** 异区 / marker 重定位 | **11** | declared 与 questions 分离（附录）→ marker 文本重定位 → 与 stem/answer/他 material 碰撞 |
| other | 0 | |

**稳定可拆：9 + 11 = 20。**

---

## P6 — OBSERVED vs CAUSAL

### OBSERVED
- 20 unit 全部区间、resolved span、target kinds、rejection 证据（JSON）。
- declared∩stem=4；resolved∩stem=10；evidence own=10。
- 英语 resolved count 达 470–492 行。

### SUPPORTED CAUSAL
1. **`_enforce_material_overlap` 直接导致拒绝**（控制流，resolver.py:628-658）。
2. **4 vs 10 不是矛盾**（declared vs resolved/evidence）。
3. **B 型与 marker 文本重定位 structurally consistent**（resolved 远大于 declared 且撞 stem）。

### NOT CLAIMED
- decomposition 导致全部拒绝；
- LEVEL 2 可解这 20 条。

---

## P7 — LEVEL 2

| # | 答案 |
|---|---|
| Q1 是否 positional-interface 问题？ | **NO** |
| Q2 哪些属 decomposition/stem boundary？ | **A 型 9**（同/半同区 + stem 进 material） |
| Q3 哪些属 region semantics / 跨区？ | **B 型 11**（含 marker 重定位） |
| Q4 answer 161 是否仍无 read-point？ | **YES**（INTERFACE_BLOCKER） |
| **Q5 LEVEL 2** | **NOT YET DETERMINED** |

不得用 material RCA 推导 LEVEL 2 REQUIRED。answer 反事实仍阻塞。

---

## COMPLETE

```text
[x] exact 20 units preserved
[x] resolved material evidence (pre-demotion spy) or NOT AVAILABLE noted
[x] 4 vs 10 resolved — NOT A CONTRADICTION
[x] same/different region complete
[x] overlap target kinds complete (exclusive + non-exclusive)
[x] A/B mechanism split evidence-based (9 / 11)
[x] observed vs causal separated
[x] LEVEL 2 reassessed
[x] no production code changed
```

## Evidence

```text
e2e_run/phase1_3r/overlap_final_evidence.json      # 逐 unit 全字段
e2e_run/phase1_3r/phase13rb_overlap_final.py
e2e_run/phase1_3r/phase13rb_overlap_confirm.py     # 1.3R-B
```
