# 批量产出改进实测（地理 composite / 数学答案边界）

**基线**：V3 `9fb36ed` + 本轮最小修改 · Papers `a4a0a8c`  
**输入**：数学 `934dec78…` · 地理 `3f4a7a82…`（与前次一致）  
**库**：`aitutors_yield_v1`（新建；已 `SELECT current_database()` 断言）  
**保护**：`aitutors_test` 21 题 + 3 反馈未写入

---

## 1. 地理 25 单元（Work A）

| 证据 | 结论 |
|---|---|
| 25 单元均为 `composite_question` | → `composite_unit`（边界映射已有） |
| 字段 | `questions_lines`+`material_lines`+`answer_lines`；**无** stem/options/sub_questions |
| Producer 能否可靠拆子题？ | **否** — 无子题边界证据 |
| 已做最小改动 | `questions_lines`→stem 检索窗；composite **1:1** 译为单子题（不猜拆分） |
| V3 结果 | **仍 0 候选**：20 条 single_choice 缺 per-label 选项；composite 材料/选项 span 未解析 |

**结论：维持安全拒绝**（证据不足，不猜）。不扩通用 composite 契约。

## 2. 数学答案边界（Work B）

| 样本 | 形式 | 频率 |
|---|---|---|
| 故选：X | `故选：D.` | 23/25 单选 |
| 故选X | `故选C.` | 2/25 |
| 无标记 | — | **0/25** |
| 多标记冲突 | — | 0 |

**确定性规则**（仅全文唯一 `故选[：:]?[A-D]` / `答案：[A-D]`；缺失/冲突→不抽）已实现于 `gate/grammar.py`。  
**不改** answer span 证据（仍存全文）；**不** LLM 猜答案；短答题 5 条仍 pending。

## 3. V3 管线结果（真实入口）

| 卷 | 修改前 | 修改后 | 入库题完整性 |
|---|---|---|---|
| 数学 30 | 0 Q / 30 pending | **25 Q 自动入库** + 5 pending（短答） | 25/25 有 stem+answer+option |
| 地理 25 | 0 | **0**（稳定拒绝） | — |

**准确产出 +25**（0→25），质量门槛未降（仅唯一明确标记才抽取）。

## 4. 口径

| 结局 | 数学 | 地理 |
|---|---|---|
| Accepted | **25** | 0 |
| Pending | 5（短答） | 0 |
| Skipped | 0 | 25 |

Funnel 含 `run_id`/`database`/`input_hashes`；Accepted 以 DB 复算。

## 5. 变更文件

- `manifest_annotation.py`：questions_lines→stem；composite 1:1 子题
- `gate/grammar.py`：唯一故选/答案标记抽取
- 测试：`test_answer_marker_and_composite.py`（4）+ 既有 30 通过

## 6. 下一项最高收益

1. **数学 5 条短答**的确定性答案（非 A–D）规则 — 若有明确边界可再 +5  
2. **地理选项 per-label**（若 OCR 表格可确定性拆）— 影响 20 单元  
3. 人工消化历史 41 条 pending

---

**成功标准达成**：根因有据、产出可证明提高（+25）、不可证的仍拒、真实管线验证、验收库未破坏。
