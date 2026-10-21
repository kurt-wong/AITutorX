# A-CONFIRMATION — trim blank vs declared（3 条）

**Date**: 2026-10-02  
**Scope**: 零代码 / 零 DB / 零 Producer / 未跑 284 / 未碰 B1·B2·Answer·LEVEL 2

---

## 结果（与预期完全一致）

| unit | declared | raw interior | lead/trail 空行 | **trimmed** | == declared |
|---|---|---|---|---|---|
| Q9-11 | **538–541** (4) | 537–542 (6) | 537 / 542 | **538–541** | **YES** |
| Q12-14 | **543–561** (19) | 542–562 (21) | 542 / 562 | **543–561** | **YES** |
| Q21-25 | **586–610** (25) | 585–611 (27) | 585 / 611 | **586–610** | **YES** |

**trimmed overlap（两两）**：Q9-11 ∩ Q12-14 = ∅ · Q9-11 ∩ Q21-25 = ∅ · Q12-14 ∩ Q21-25 = ∅

```text
trimmed_equals_declared_all = true
trimmed_overlap_any         = false
```

---

## 因果确认

```text
第二刀 ±1 padding
  → interior 含首尾纯空行
  → 相邻 unit 边界在 542 / 585 相撞
trim 首尾纯空白
  → 严格等于 declared
  → 三组 disjoint
```

**第四刀 A = Material Boundary Normalization（trim 首尾纯空白）** 的因果证据已齐。  
**不需要** collision-aware 禁 padding 分支（trim 已消掉本批 overlap）。

---

## 第四刀条件（Owner 标准）

```text
[✓] Q9-11   raw [537,542] → trim [538,541]
[✓] Q12-14  raw [542,562] → trim [543,561]
[✓] Q21-25  raw [585,611] → trim [586,610]
[✓] trimmed == declared 3/3
[✓] trimmed overlap = 0
```

**第四刀已具备批准条件。**

建议执行结构：

```text
Fourth Cut
├── A. trim 首尾纯空白（保留第二刀 unique-marker 外走）
└── B. stem boundary（B1 own 4 / B2 neighbor 2）独立修复
```

---

## Evidence

```text
e2e_run/phase1_3r/a_confirmation_trim_blank.json
```
