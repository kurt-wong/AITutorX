# B3 FINAL EVIDENCE — 集合对账 + Producer→Resolver（零代码）

**Date**: 2026-10-02  
**对象**: 43 unique `candidate_id`  
**禁止**: 改代码 / Producer / Spec / migration / 测试

---

## 1. 集合数学一致性（已解）

| | HAS_VALUE | BARE_QUESTION_NUMBER | EMPTY | **sum** |
|---|---:|---:|---:|---:|
| **IN_DECLARED_ZONE** | **16** | **22** | 0 | 38 |
| **OUTSIDE** | **4** | **1** | 0 | 5 |
| NO_ANSWER / AMBIGUOUS | 0 | 0 | 0 | 0 |
| **sum** | **20** | **23** | 0 | **43** |

```text
unique_candidate_ids = 43
cross_sum            = 43   ✓
```

DSH 的 `20+23+5=48` 是交叉表误加总；**OUTSIDE(5) ⊂ 23 BARE 或 20 VALUE**，不是并列第三类。

---

## 2. 数学卷 23 个 candidate

```text
math n = 23
IN_ZONE  × BARE = 22
OUTSIDE  × BARE = 1
HAS_VALUE = 0
```

**整卷级**：23/23 answer_text 皆为裸题号（`27.` `3.` `30.`…）。

---

## 3. Q27（关键样本）

| 项 | 值 |
|---|---|
| Producer `answer_lines` | **[593, 623]** |
| Resolver answer span | **[593]** |
| answer_text | **`27.`** |
| declared 593–623 实际内容 | `27.` + `【考点】…` + `【分析】…` + `【解答】…` |
| position | IN_DECLARED_ZONE |
| content | BARE_QUESTION_NUMBER |
| **root cause** | **A** |

`27.` 是 **Producer 答案块的起始题号行**，不是 Resolver 凭空造的；Resolver **只消费了首行**，未展开到 declared 多行 answer range。

---

## 4. 5 条 OUTSIDE（重算后）

| unit | file | declared | got | text | class |
|---|---|---|---|---|---|
| Q8 | 化学 | [513,513] | 578 | 有值 | **C** |
| Q1 | 数学 | [200,206] | 747 | `1.` | **C** |
| Q2 | 物理 | [356,356] | 368 | 表格 | **C** |
| Q6 | 物理 | [356,356] | 368 | 表格 | **C** |
| Q8 | 物理 | [356,356] | 373 | 表格 | **C** |

（与先前 5 条一致，非重复计数。）

---

## 5. Producer→Resolver 对照（BARE 22 条 class A）

模式（数学 Q3/Q27/Q30…）：

```text
Producer answer_lines = [s, e]     e ≫ s   （整段解答块）
  L_s   = "27."                     ← 题号行
  L_s+2 = 【考点】…
  L_s+4 = 【分析】…
  L_s+6 = 【解答】…（含最终结论）

Resolver answer span = [s] only
answer_text          = "27."
```

**Producer 已提供完整 answer evidence；Resolver 只取 qn 入口行。**

---

## 6. B3c 根因分类

| class | n | 含义 |
|---|---:|---|
| **A** | **22** | Producer 有正确答案证据，Resolver 未消费完整 range |
| **B** | **0** | Producer 本身无可用答案 |
| **C** | **5** | Producer 有证据，Resolver 选到错误 entry（OUTSIDE） |
| **D** | 0 | — |

```text
A+C = 27  → 同属 answer-entry / answer-span resolution（B3c）
B   = 0   → 不是 Producer 缺证据
```

**结论（OBSERVED）**：B3c 主体是 **V3 Resolver 对多行 declared answer range 的消费缺陷**（只取 qn 行），外加 **共享答案表误选**（C）。  
**B3a**（`\.` 转义）仍在，但不是 23 条 BARE 的主因——即便 451 可读，数学逐题块仍是 A 型。

---

## 7. OBSERVED / INFERRED / NOT PROVEN

```text
OBSERVED
  43 unique；交叉表和 = 43
  20 HAS_VALUE / 23 BARE
  math 23 全 BARE
  Q27 declared [593,623] 含【解答】，resolver 仅 593="27."
  class A=22, C=5, B=0

INFERRED
  A 与 C 共享 answer-entry resolution 机制
  「27.」是 declared 块首行，非幻觉 token

NOT PROVEN
  canonical answer 应取解答块哪一段（结论/全文/结构化字段）← 语义，非本轮
  单一 regex/zone 规则可同时修 A+C
```

**B3c = OBSERVED DEFECT（Resolver 未消费完整 declared answer range + entry 误选）**  
下一步若授权，属 **V3 Resolver implementation defect（A 型）**；**C 型**需另核 entry 选择。  
**本轮不提实现方案。**

---

## Evidence

```text
e2e_run/phase1_3r/b3_final_evidence.json   # 43 rows + cross + anomalies
```
