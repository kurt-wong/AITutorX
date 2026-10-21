# PHASE 1.3R-B — Overlap 20 Structural Confirmation

**Level**: LEVEL 1（定向 RCA，非修复 / 非 LEVEL 2 实验）
**Date**: 2026-10-02
**Baseline**: `od01-r3-convergence` @ `39840ff` · `match-norm/v1.1` dirty `015cdfa`
**禁止项已遵守**：未改 production code / Spec / schema / contract / DB / resolver / adapter / bridge / Producer / overlap invariant。

---

## P0 — Exact 20 units

来源：Phase 1.3R `material_counterfactual_rca.json` 中 `failure_taxonomy == MATERIAL_OVERLAP_REJECTED`（**未重新分类**）。

```text
overlap_units_count = 20
```

| # | unit_id | document |
|---|---|---|
| 1 | U52 | 会考历史 |
| 2 | U53 | 会考历史 |
| 3 | Q37 | 会考政治 |
| 4–15 | Q1,Q2,Q3,Q4,Q5-6,Q7-8,Q9-11,Q12-14,Q15-17,Q18-20,Q21-25 | 会考英语 |
| 16–18 | U49-52, U53-56, U57-60 | 会考英语 |
| 19–20 | U10-13, U14, U15 | 会考语文 |

（语文 3 条 + 历史 2 + 政治 1 + 英语 14 = 20。）

---

## P1 — Three-range evidence

机器可读：`e2e_run/phase1_3r/overlap_structural_confirmation.json`（每 unit 完整 interval）。

抽样（完整 20 条见 JSON）：

| unit | material_lines | questions_lines | mat vs q | sub.stem seq | mat∩stem |
|---|---|---|---|---|---|
| U52 | [569,592] | [569,592] | **equal** | [568,592] | **24 lines** |
| U53 | [594,627] | [594,627] | **equal** | [593,629] | **34 lines** |
| Q37 | [472,496] | — | subset | (Q36.stem) | 跨 unit |
| Q1 (英) | [497,502] | — | **disjoint** | [10,15] | 0（撞 **Q2** stem） |
| U10-13 | [80,188] | — | — | (Q9.stem) | 跨 unit |

每条含：`material_lines` / `questions_lines` / `sub_question.stem_source_span` / `material_vs_sub_stem.shared_manifest_line_numbers` / `resolver_overlap_rejection.evidence_verbatim`。

---

## P2 — Decomposition path（代码位置）

```text
annotation_adapter.py:_SUB_DECOMPOSITION = "producer_region_as_single_sub"   :45
annotation_adapter.py:_build_composite                                     :120-164
  shared["material"] = {"role": "material"}          # 无行号              :131-132
  sub = { unit_id: f"{uid}.sub", content: _leaf_content(unit) }             :134-140
  gaps += SUB_QUESTION_DECOMPOSITION_UNAVAILABLE                            :143-151
annotation_adapter.py:_leaf_content                                        :52-73
  stem = {role:stem, question_label: parent QN}     # 无 questions_lines
```

| 问题 | 答案 |
|---|---|
| Q：`questions_lines` 如何进入 `_SUB_DECOMPOSITION`？ | **不进入**。adapter **不读** `questions_lines`；仅 1:1 造一个 sub |
| material==questions 时是否整区→一个 sub？ | **是**（`producer_region_as_single_sub`） |
| sub.stem 是否覆盖整个 questions region？ | **否**。stem 由 Resolver `question_label` 启发式决定，**不是** questions_lines |
| 是否有其他 decomposition metadata？ | **无**（gap 文本明示「不猜拆分」） |
| `SUB_QUESTION_DECOMPOSITION_UNAVAILABLE` 语义 | 登记「Producer 无子题边界」；消费端只有一个 sub，**非** IR-ready 保证 |

**sub.stem 实际 span** = `resolver._locate_question_start` + `_stem_span`（题号行→下一题/答案区），常**大于** material。

---

## P3 — Resolver rejection path（控制流）

```text
resolver.py:_material_span           467-510  先按 marker 解析 material
resolver.py:_enforce_material_overlap 628-658
  for m in mats:
    if m.line_refs ∩ other_resolved.line_refs ≠ ∅:
      m demoted → UnresolvedReference(incomplete, evidence="overlaps …")
```

**因果（控制流可证）**：material 与任一非 material / 其他 material 的 `line_refs` 交集非空  
→ **直接** demote → `MATERIAL_OVERLAP_REJECTED`。

对 20/20 unit：`resolver_overlap_rejection.actual = true`，verbatim 含 `overlaps … material overlap → unresolved`。

---

## P4 — Aggregate pattern

| Pattern | Count |
|---|---:|
| material == questions | **2** |
| material ⊂ questions | **7** |
| material ⊃ questions | 0 |
| partial_overlap (mat vs q) | 0 |
| disjoint (mat vs q) | **11** |
| single sub covers whole questions region (stem⊇/== q) | **4** |
| material overlaps **own** sub.stem | **10** |
| material overlaps **other unit** stem | **8** |
| material overlaps **other material** | **13** |
| material overlaps **answer** span | **8** |
| **overlap 直接被 resolver 拒绝** | **20** |

（后四行可叠加：同一 unit 可撞多种 span。）

```text
20/20 common pattern = 部分
  全部直接被 _enforce_material_overlap 拒绝     = YES (20/20)
  全部撞自家 sub.stem                          = NO  (10/20)
```

**例外（非「自家 stem」型）**：英语 Q1/Q2/Q3/Q9-11/… 等 8 个跨 unit stem、13 个 material-material、8 个 answer——见 JSON `overlap_target_kinds`。

---

## P5 — Observed vs Causal

### Observed structural facts
- 20 unit 来自 1.3R 精确集合
- 每 unit 三区间已落盘
- adapter 单 sub、不消费 questions_lines（代码）
- 20/20 有 overlap 证据字符串
- mat vs q：equal 2 / subset 7 / **disjoint 11**

### Causal conclusions（控制流可证）
1. **`_enforce_material_overlap` 是 20 条拒绝的直接原因**（demote 分支）。
2. **adapter 单 sub + stem 启发式** 与 Producer 嵌套/跨区 material **结构一致**地导致 overlap（非每条都必现自家 stem 碰撞）。

### Not claimed
- 修 decomposition 后 IR ready 一定上升
- LEVEL 2 positional interface 能解这 20 条

---

## P6 — 未解决
无代码修改、无 bridge 修改、无 invariant 放宽。

---

## P7 — LEVEL 2 scope

| # | 问题 | 答案 |
|---|---|---|
| **Q1** | 20 条 overlap 是否为独立于 positional-interface 的结构问题？ | **YES** |
| **Q2** | 能否从 LEVEL 2 positional 因果论证中剥离？ | **YES**（属 overlap invariant + `_SUB_DECOMPOSITION` 语义，与「Resolver 是否消费行号」正交） |
| **Q3** | answer 161 是否仍缺 positional read-point？ | **YES**（INTERFACE_BLOCKER 未变） |
| **Q4** | LEVEL 2？ | **NOT YET DETERMINED** |

### Q4 说明（默认不得自动升 REQUIRED）

- 这 20 条：**剥离**后应走 **Resolver/Producer overlap·decomposition 裁决**，不是 positional interface。
- INTERIOR_EMPTY 20 条：inclusive/exclusive **语义裁决**（1.3R），也不必先上 LEVEL 2。
- answer 161：仍无合法反事实；**不足以**单独批准 LEVEL 2。

```text
Q4 = NOT YET DETERMINED
```

---

## COMPLETE

```text
[x] exact 20 units reproduced
[x] 20 units each have material/questions/sub.stem intervals
[x] decomposition path verified (code lines)
[x] resolver rejection path verified (control flow)
[x] aggregate pattern complete
[x] exceptions identified (overlap target kinds; disjoint mat vs q 11)
[x] observed vs causal separated
[x] no production code changed
[x] LEVEL 2 explicitly reassessed
```

## Evidence

```text
e2e_run/phase1_3r/overlap_structural_confirmation.json
e2e_run/phase1_3r/phase13rb_overlap_confirm.py
（输入）material_counterfactual_rca.json  taxonomy=MATERIAL_OVERLAP_REJECTED
```
