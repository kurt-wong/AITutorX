# FIRST CUT — INTERIOR_EMPTY inclusive/exclusive bridge

**Level**: LEVEL 1 production fix（第一刀，按 Owner 授权）
**Date**: 2026-10-02
**Scope lock**: 仅修 material 边界 marker 映射；**不碰** overlap invariant / Answer positional / LEVEL 2 / Frozen Spec

---

## 问题

Producer `material_lines=[s,e]` = **inclusive 内容区间**。  
Resolver `multi_line_pair` interior = marker **之间排他**。  
旧映射（端点当 marker）→ N=1 时 interior 空 → **INTERIOR_EMPTY 20**。

## 修复

`annotation_adapter.material_boundary_markers` + `attach_material_boundary_markers`：

- marker 落在内容区间**外侧**分隔行（`s-1` / `e+1`）
- 分隔行为空则向外找最近非空行（仍须在区间外）
- 不发明文本，只用真实 source line
- `runner.py` Track A 在 `manifest_to_annotation_payload` 后调用

未改 resolver / overlap invariant / answer 通道。

---

## 回归（284 units / 9 会考卷）

### Compute（同 DB sealed annotation）

| 指标 | 旧 bridge | 新 bridge | Δ |
|---|---:|---:|---:|
| IR Ready | 35 | **41** | **+6** |
| INTERIOR_EMPTY | 20 | **4** | −16 |
| material resolved | 11 | **32** | +21 |
| material unresolved | 43 | **22** | −21 |
| 丢失原 ready | — | **0** | — |

### 真实 E2E（GateService → DB）

| 指标 | Phase1.1 基线 | 第一刀后 |
|---|---:|---:|
| **admission_candidates** | 35 | **41** |
| skipped units | 249 | 243 |
| auto_approve | 1 | 1 |
| 数学 cand | 23 | 23（守住） |
| 英语 cand | 0 | **6** |

新增 6 条均为英语 `U26-40 … U57-60`。

### 测试

清库后：`test_gate_service` + annotation/compiler/ir/identity 等 **136 passed**。  
（此前失败为 DB 残留 E2E 数据，非本改动。）

---

## 残留

- INTERIOR_EMPTY 仍 4：边界分隔行不可用（文档首尾/空行 walk 用尽）
- overlap / answer 线 **未动**（按裁决）

## Evidence

```text
e2e_run/phase1_3r/first_cut_regression.json
e2e_run/phase1_3r/first_cut_e2e_report.json
code: scripts/preprocessing_consumer/annotation_adapter.py
      scripts/preprocessing_consumer/runner.py
```
