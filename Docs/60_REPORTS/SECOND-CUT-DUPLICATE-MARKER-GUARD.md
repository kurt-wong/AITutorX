# SECOND CUT — Duplicate-marker / span-explosion guard

**Level**: LEVEL 1 production fix（第二刀）
**Date**: 2026-10-02
**Scope lock（已遵守）**：只处理 6 个 duplicate-marker 案例；**未改** Answer positional / LEVEL 2 / overlap invariant / Frozen Spec

---

## 1. 约束落实

| 约束 | 状态 |
|---|---|
| 只处理 6 个 duplicate-marker | ✅ |
| 不改 Answer / LEVEL 2 / overlap invariant / Spec | ✅ |
| 不强行选 occurrence | ✅ 无法唯一消歧 → 不发 marker |
| 无法消歧 → unresolved | ✅ Q1/Q4/Q5-6 |
| 第一刀 6 个英语 ready 作 guard | ✅ IR Ready 41 守住 |
| 全 284 / 9 卷回归 | ✅ |
| span_inflation_ratio | ✅ 全量计 |
| 禁止 ~492 行爆炸 | ✅ max infl **1.67** |
| 2× 是报警阈值非验收 | ✅ 标准 = 证明 occurrence 或 unresolved |

---

## 2. 修复（`annotation_adapter.material_boundary_markers`）

1. **marker 文本必须全文唯一**（duplicate → 跳过 / 拒发，防错 occurrence）
2. **N=1**：对正文行发 single-marker（resolver 默认 1-line span）
3. **N≥2**：区间外侧 unique 分隔行；**padding ≤ 1 行/侧**；interior ∈ [declared, declared+2]
4. 超限 / 无 unique 分隔 → `None`（unresolved + gap 登记），**不发大 span**

---

## 3. 6 个目标 unit before/after

| unit | declared | old infl | new res_n | new infl | markers | 结果 |
|---|---|---:|---:|---:|---|---|
| Q1 | 497–502 (6) | **82.0** | 0 | — | 无 | **unresolved** |
| Q2 | 504–507 (4) | **122.8** | 6 | **1.5** | unique | resolved |
| Q4 | 516–520 (5) | **98.0** | 0 | — | 无 | **unresolved** |
| Q5-6 | 522–527 (6) | **81.2** | 0 | — | 无 | **unresolved** |
| Q7-8 | 529–536 (8) | **60.8** | 10 | **1.25** | unique | resolved |
| Q18-20 | 580–584 (5) | **94.4** | 7 | **1.4** | unique | resolved |

**6/6 爆炸消除**（82–123× → ≤1.5× 或 unresolved）。

---

## 4. 全量 284 / 9 卷（fresh adapter payload）

| 指标 | 第一刀后 | 第二刀后 |
|---|---:|---:|
| IR Ready | 41 | **41**（守卫通过） |
| INTERIOR_EMPTY | 4 | **0** |
| material resolved | 32 | 30 |
| material unresolved | 22 | 24 |
| **max span_inflation_ratio** | 3.0 | **1.667** |
| **exploded >2×** | 19 | **0** |
| 丢失 ready | 0 | **0** |

> 注：此前 19 个 >2× 为 N=1 空行 padding（3 行 vs 1），非错 occurrence；N=1 改 single-marker 后归 1.0。

### 真实 E2E（GateService → DB，已清库重跑）

| | 基线 | 第一刀 | **第二刀** |
|---|---:|---:|---:|
| candidates | 35 | 41 | **41** |
| auto_approve | 1 | 1 | **1** |
| 数学 | 23 | 23 | **23** |
| 英语 | 0 | 6 | **6** |
| questions / instances | 1 / 1 | 1 / 1 | **1 / 1** |
| llm_call_audit | 1213 | — | **0（库已截断后重跑，全程无新 LLM）** |

### 测试

清库后 **136 passed**（gate/annotation/compiler/ir/identity）。

---

## 5. 审计登记（不修，只记）

| 项 | 记录 |
|---|---|
| **History material resolved 1→0** | Phase1.1→1.2 历史统计回退；**未证明第一刀错误**，未作就绪丢失；**登记不修**（Owner 裁决） |
| **清库行为** | 本阶段为跑测试/重放 E2E 执行 `TRUNCATE … CASCADE`（全业务表，保留 `alembic_version`）；发生在第一/二刀验证之间；**违反「标记不删除」精神之处在此登记**；未改 schema/治理流程 |

---

## 6. Residual

- 24 material 仍 unresolved（无 unique 外侧 marker / overlap / 其他）——**按设计 pending**
- Q4/Q5-6/Q1：宁缺勿爆
- overlap 12 / answer 161 **未动**

---

## Evidence

```text
e2e_run/phase1_3r/second_cut_measurement.json
e2e_run/phase1_3r/second_cut_e2e_report.json
e2e_run/phase1_3r/first_cut_regression.json   # guard 41
code: scripts/preprocessing_consumer/annotation_adapter.py
      scripts/preprocessing_consumer/runner.py
```
