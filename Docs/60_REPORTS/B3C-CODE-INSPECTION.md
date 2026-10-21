# B3C READ-ONLY CODE INSPECTION

**Date**: 2026-10-02  
**性质**: 只读勘察 · 零代码修改

---

## A. `_answer_span` 调用链

```text
SourceResolver.resolve
  → extract_targets / _answer_target          reference.py:202-218
       kind=answer_zone, zone, question_number
  → _resolve_unit                             resolver.py:~360
  → _span_other → kind=="answer_zone"         resolver.py:493-494
  → _answer_span                              resolver.py:602-634
  → _ENTRY_RE / _entry_offsets                resolver.py:47-52
  → add_char_span (single line_character)     resolver.py:160+
```

---

## B. A 型（Q27）：为何只取首行

```text
Producer manifest
  answer_lines = [593, 623]     # 完整解答块  manifest_reader.py:49,105
        ↓
annotation_adapter._leaf_content   annotation_adapter.py:175-179
  content["answer"] = {
    role: "answer",
    question_label: "27",
    answer_zone: "answer_table"
  }                                # ← answer_lines 未写入 payload
        ↓
reference._answer_target           reference.py:202-218
  ResolveTarget(kind=answer_zone, zone=…, question_number="27")
  # 无 start/end / line range 字段
        ↓
resolver._answer_span              resolver.py:602-634
  扫 answer header → explanation header 之间所有行
  _entry_offsets(l.text, "27") 匹配 "27."
  切片 = entry 起点 → 同行下一 entry / 行尾
  add_char_span  → 仅 P1L593 = "27."
```

**丢失点**：`annotation_adapter._leaf_content` 不发射 `answer_lines`；  
`_answer_target` / `ResolveTarget` **无多行 range 通道**；  
`_answer_span` **从不读取** Producer `answer_lines`。

---

## C. C 型（物理 Q2 → 368）：错 entry

同一 `_answer_span` + `_entry_offsets`：

```text
物理 Q2  question_label="2"  answer_zone="answer_table"
  _answer_span 在 answer 区扫描
  _ENTRY_RE / _entry_offsets 匹配 "2."
  命中共享答案表/他 unit 答案块上的 "2." 行 368
  （declared [356,356] 未参与定位）
```

**同一入口**：`_entry_offsets` / `_ENTRY_RE` / `_answer_span`。

---

## D. A/C 是否同源

```text
YES
```

| | 机制 | 代码 |
|---|---|---|
| A | 同一 entry 扫描只切 **单行 char span**，不扩 declared 多行 range | `resolver.py:618-634` |
| C | 同一 entry 扫描在 zone 内命中 **错误 unit 的 qn token** | 同上 |

差异仅在「命中哪一行 / 切多长」，**匹配入口同一**。

---

## E. Producer `answer_lines` 是否被消费

```text
NO
```

| 层 | 事实 |
|---|---|
| `manifest_reader.py:49,105` | **解析**进 `ManifestUnit.answer_lines` |
| `annotation_adapter.py:175-179` | **丢弃**；只写 `role/question_label/answer_zone` |
| `reference._answer_target` | 只读 `answer_zone` + `question_label` |
| `_answer_span` | 只用 qn token + zone 扫描 |

信息在 **adapter 发射点** 丢失；resolver 从未见过 `answer_lines`。

---

## F. AnswerTokenContract 现有语义

```text
NOT SPECIFIED  （多行 range 作为 answer evidence）
```

- `grammar.py:174-184`：要求 `ResolvedSpan` 文本切片，**`granularity` = 字符切片**（line_character）
- 明确写「不是裸 source/OCR 文本」；对 **多行 declared range** 无定义
- 不禁止上游给出更宽 evidence 再抽 token，但 **span 形态按 char-slice 契约**
- 未规定「解答块取哪一段为 canonical answer」→ **NOT SPECIFIED**

现有可表达多行的机制：`add_span`（material `multi_line_pair` → `line_refs` 多行）。  
**answer 路径未使用**；无现成 answer 多行 API 需新增即可——`ResolvedSpan.line_refs` 已存在。

---

## G. 最终结论

```text
OBSERVED
  A 与 C 共用 _answer_span + _ENTRY_RE + _entry_offsets
  Producer answer_lines 在 adapter 发射点丢失，resolver 从未消费
  _answer_span 输出 = 单行 char_span（qn entry 切片）
  material 有 multi_line_pair；answer 无对等通道
  AnswerTokenContract 对多行 answer evidence = NOT SPECIFIED

INFERRED
  A = declared 多行 range 未进入 resolution，只匹配入口行
  C = 同一 qn-token 扫描在共享 answer zone 内错配
  A+C 可作为同一 implementation defect 的两面处理

NOT PROVEN
  canonical answer 应取解答块哪一段（需 Owner / Spec）
  单一改动是否同时消灭 A 与 C
```

**STOP 条件**：若要定义「解答块内何为 canonical answer」→ 需 Owner/Spec（`NOT SPECIFIED`）；  
**若仅要求 Resolver 消费已有 `answer_lines` 整段作为 answer evidence span**，则属 V3 implementation（A/C 同源）。

未改任何代码。
