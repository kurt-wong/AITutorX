# ANSWER-AWARE CONFIRMATION — Q9-11 / Q12-14 / Q21-25

**Date**: 2026-10-02  
**Scope**: 零代码 / 零 DB / 零 Producer / 未跑全量回归 / 未碰 Frozen Spec

---

## 1. Answer span（第二刀后）

| unit | Producer declared answer_lines | Resolver 当前 answer span | 源文 |
|---|---|---|---|
| Q9-11 | **[451,451]** | **无**（`answer row qn=9 not found`） | 451 = 答案表 `…A9. C10. A11. B12. A…` |
| Q12-14 | **[451,451]** | **[593]** ⚠️ | 593 = `M: 5 days, from March, 7 to 12.`（**听力原文**） |
| Q21-25 | **[455,455]** | **[455]** ✓ | 455 = `21.Grady 22.61295 … 25.airport` |

---

## 2. 相交检查

| 检查 | 结果 |
|---|---|
| Q21-25 trimmed material **[586,610]** ∩ Q12-14 answer **[593]** | **YES**（593 ∈ [586,610]） |
| Q21-25 material [586,610] ∩ Q18-20 material [580,584] | **NO**（584 &lt; 586；旧 overlap 含 585 空行 padding） |

---

## 3. Q12-14 answer 是否合法 source？

```text
593 = 对话台词 “M: 5 days, from March, 7 to 12.”
合法答案应为 451 = 答案表行（含 “B12. A”）
```

**结论：593 不是 Q12-14 的合法 answer source。**

### 偏离点（Producer → Adapter → Resolver）

| 层 | 事实 |
|---|---|
| Producer | `answer_lines=[451,451]` **正确** |
| Adapter | 只声明 `answer_zone` + question_label（无行号）— 未偏离 |
| **Resolver `_answer_span`** | **第一处偏离**：answer zone 过宽（答案区无详解表头则延至文末）+ `_ENTRY_RE` 把台词 `7 to 12.` 中的 `12.` 当成 qn=12 条目 |

⇒ **B3 候选 = Answer read-point / qn-token 误匹配**，不是 material trim 问题，也不是 Producer 缺陷。

与 Q37↔Q36.stem、U10-13↔Q9.stem 同属「read-point 过宽读到邻接 unit 内容」，但 **role=answer，机制独立**。

---

## 4. 对第四刀范围的含义

```text
A  trim blank          — 成立（Q9-11/Q12-14 material 已证）
B1 own-stem            — 待做（U52 U53 U14 U15）
B2 neighbor-stem       — 待做（Q37 U10-13）
B3 answer boundary     — 本轮确认存在（至少 Q12-14；机制 = zone 过宽 + qn 误匹配）
```

**B3 不得预先排除**；也不在本轮修 Resolver。  
B1/B2/B3 仍应分支独立。

---

## Evidence

```text
e2e_run/phase1_3r/answer_aware_confirmation.json
```
