# 地理结构修正 + 四卷同版本 E2E — 执行报告

**代码**：`2ab57e5` → **`d45cc9d`**（composite 不造假单题 + IR 拒空子题）  
**输入**：四卷 md/pdf 哈希与前次一致（见 `e2e-4paper.json`）  
**库**：`aitutors_e2e_4paper`（`SELECT current_database()` 已断言；未清任何旧库）

---

## 1. 地理缺陷修正（Phase 1）

| 问题 | 修正 |
|---|---|
| `U1-2` 两道题被合成 1 个 standalone 子题，stem 盖住材料+Q1+Q2 | **多题且无子题边界 → sub_questions=[]**，写入 `group_evidence`（材料/题组/答案行） |
| IR 可能把「无子题 composite」判 ready | IR 增加 `composite has no sub_questions` → **incomplete** |

- 不合并两题、不猜子题区间、不改 Gate/Admission 门槛  
- 回归：`test_composite_no_fake_single.py`（3）— 多题无假子题、IR 非 ready、单题仍 1:1  
- 相关测试 **44 passed**

## 2. 四卷 E2E（同版本，Phase 2–3）

| 卷 | 单元 | Accepted | Pending | Skipped | 完整性(stem+ans+opt) |
|---|---|---|---|---|---|
| 化学 | 40 | **21** | 3 | 16 | 21/21 |
| 数学 | 30 | **25** | 5 | 0 | 25/25 |
| 物理 | 22 | **10** | 8 | 4 | 10/10 |
| 地理 | 25 | **0** | 0 | 25 | —（安全拒绝） |
| **合计** | **117** | **56** | 16 | 45 | **56/56** |

**产出率 56/117 ≈ 47.9%**（此前批次 31/117≈26.5%；差异来自数学 +25 与本轮代码，非拼接历史数字）。

地理 0 入库 = **正确**（结构未确定，不造单题）；拒绝原因已入 funnel（run_id/database/input_hashes）。

## 3. 与历史对比

| 卷 | 历史 | 本轮 | 差异原因 |
|---|---|---|---|
| 化学 | 21 | 21 | 无代码影响 |
| 数学 | 0（30 pending） | **25** | 唯一 `故选` 标记抽取（上轮已入 `2ab57e5`） |
| 物理 | 10 | 10 | 无代码影响 |
| 地理 | 0（曾误造单题仍 0） | 0 | **结构更正确**：不再假单题 |

## 4. 数据库安全

`aitutors_test`：**21 Q / 21 I / 126 RC / 3 FB** 未变 · `aitutors` 0 Q · 未 TRUNCATE

## 5. 下一项最高收益

1. **地理子题边界的 Producer 局部识别**（评估，不扩框架）— 25 单元  
2. **数学 5 条短答**确定性答案  
3. 人工消化 pending（化学 3 + 数学 5 + 物理 8）

---

附件：`e2e_run/e2e-4paper.json`
