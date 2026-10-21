# CUT-3R — Post-second-cut overlap remeasurement

**Level**: 零生产代码 · 只重测 8 条
**Date**: 2026-10-02
**对象**: `U49-52 U53-56 U57-60 Q3 Q9-11 Q12-14 Q15-17 Q21-25`
**原则**: 代码状态改变后必须重算指标，禁止用旧 span 证据指导下一刀

---

## 结果总览

| status | n | unit |
|---|---:|---|
| **RESOLVED**（第二刀消除 / 历史伪影） | **3** | U49-52 · U53-56 · U57-60 |
| **STILL_PRESENT**（真实残余 overlap） | **3** | Q9-11 · Q12-14 · Q21-25 |
| **AMBIGUOUS**（无 unique marker，非 overlap） | **2** | Q3 · Q15-17 |

---

## 逐 unit

| unit | current span | overlap | target | infl | status |
|---|---|---|---|---:|---|
| U49-52 | 20 行 (299–314 区域) | **no** | — | 1.11 | **RESOLVED** |
| U53-56 | 23 行 | **no** | — | 1.10 | **RESOLVED** |
| U57-60 | 9 行 | **no** | — | 1.29 | **RESOLVED** |
| Q3 | — (无 marker) | no | — | — | **AMBIGUOUS** |
| Q9-11 | 6 行 (537–542) | **yes** | Q7-8.material, Q12-14.material | 1.5 | **STILL_PRESENT** |
| Q12-14 | 21 行 (542–562) | **yes** | Q9-11.material | 1.11 | **STILL_PRESENT** |
| Q15-17 | — (无 marker) | no | — | — | **AMBIGUOUS** |
| Q21-25 | 27 行 (585–611) | **yes** | Q12-14.sub.answer@593, Q18-20.material | 1.08 | **STILL_PRESENT** |

### STILL_PRESENT 明细（真实残余）

- **Q9-11 ↔ Q12-14**：相邻听力稿 material 互相重叠（附录 script 区）
- **Q21-25**：撞 Q12-14 的 answer 行 + Q18-20 material

### AMBIGUOUS

Q3 / Q15-17：`markers_attached=false`（外侧无 unique 文本）→ unresolved  
**不是** overlap 问题。

---

## 对第三刀结论的修正

| 原第三刀（陈旧 span） | 第三刀-R（第二刀后） |
|---|---|
| U49-52/U53-56/U57-60 = Producer 段界问题 | **RESOLVED BY SECOND CUT**（历史伪影，勿碰 Producer） |
| Q3/Q9-11/Q12-14/Q15-17/Q21-25 = 全部语义裁决 | **3 条真 overlap** + **2 条仅缺 marker** |
| 14 条待处理 | **收敛** |

**收敛后真实剩余：**

```text
6 条 stem/material 边界（稳定，本轮未重测）
    U52 U53 Q37 U10-13 U14 U15

3 条听力附录相邻 material/answer
    Q9-11 Q12-14 Q21-25

2 条 marker 不可得（非 overlap）
    Q3 Q15-17

3 条 RESOLVED BY SECOND CUT
    U49-52 U53-56 U57-60
```

---

## 工程纪律（本轮起）

> **代码状态改变 → 重算受影响指标 → 再定下一刀。**  
> 禁止「上份报告说 14 个 → 就修 14 个」。

---

## Evidence

```text
e2e_run/phase1_3r/cut3r_remeasurement.json
production_code_modified = false
```
