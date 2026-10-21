# PADDING=0 COUNTERFACTUAL — Q9-11 / Q12-14 / Q21-25

**Date**: 2026-10-02  
**Scope**: 零生产代码 / 零 DB / 零 Producer 修改  
**对象**: 仅 3 条听力附录 unit

---

## 四问四答

| # | 问题 | 答案 |
|---|---|---|
| **Q1** | padding=0 后是否仍 overlap？ | **否**（overlap 消失） |
| **Q2** | 问题是否完全消失？ | **否** — 三条全部变成 **UNRESOLVED**（不是正确解析） |
| **Q3** | 是否因此应进 unresolved？ | **在严格 padding=0 下：是**（exact s-1/e+1 无 unique 文本） |
| **Q4** | N=4/19/25 去掉 padding 后能否经现有 marker 机制正确解析？ | **否**（res_n=0） |

---

## 逐 unit

| unit | N | current | padding=0 |
|---|---:|---|---|
| Q9-11 | 4 | res=6 infl=1.5 **OVERLAP** Q7-8/Q12-14 material | **UNRESOLVED** |
| Q12-14 | 19 | res=21 infl=1.11 **OVERLAP** Q9-11 material | **UNRESOLVED** |
| Q21-25 | 25 | res=27 infl=1.08 **OVERLAP** answer@593 + Q18-20 | **UNRESOLVED** |

原因：恰好落在 `s-1` / `e+1` 的行文本 **非 unique**（听力稿重复头）或空行 → padding=0 规则拒发 marker。

---

## 证伪结论

```text
overlap 由 padding 引入     = 成立（去 padding 后不再 overlap）
padding=0 是正确修复        = 不成立（三条直接 unresolved）
全局取消 padding            = 禁止（第二刀 ±1 解决了其它真实边界问题）
```

**与 Owner 预判一致**：应做 **padding collision guard**（禁止 padding 侵入相邻 unit 的 declared material），而不是 padding=0。

```text
正常 → ±1 padding
若某侧 padding 进入相邻 declared material → 该侧禁 padding
若失去安全 marker → unresolved / single-marker
```

---

## 对「是否授权第四刀」的含义

Owner 条件是「padding=0 后 3 个 overlap 全部消失 **且** 问题解决」。  
实际是：**overlap 消失，但三条变 unresolved，问题未按正确解析关闭。**

⇒ **不构成「直接授权第四刀」的充分条件**；  
⇒ 但支持第四刀 **A 分支 = collision-aware padding**（而非 padding=0）。  
是否开刀等 Owner 裁决。

---

## Evidence

```text
e2e_run/phase1_3r/padding_zero_counterfactual.json
production_code_modified = false
```
