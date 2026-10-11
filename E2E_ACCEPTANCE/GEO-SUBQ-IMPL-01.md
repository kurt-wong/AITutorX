# GEO-SUBQ 实现 + E2E 实测 — 执行报告

**日期**：2026-10-11 · **实验库**：`aitutors_geo_subq_v2`（全新隔离库，未触碰 aitutors_test / aitutors_e2e_4paper）· **短答不计入产能目标**

---

## 1. 实现范围

| 模块 | 变更 | 说明 |
|---|---|---|
| `backend/app/domains/source/subq_expand.py` | **新增** | 确定性子题展开器：题号→题干→A–D→答案表；仅已证明结构；歧义即跳过 |
| `backend/app/domains/source/manifest_annotation.py` | 修改 | multi-q composite 绑定 `sub_questions[]`；shared material 声明 marker 文本（resolver 可定位） |
| `backend/app/domains/resolver/match_normalization.py` | 修改 | `is_question_start` 认 OCR 分隔符变体 `·`/`,`（实测 `15·`/`20，`），非地理特例 |
| `backend/app/domains/resolver/resolver.py` | 修改 | `_ENTRY_RE`/`_LABEL_RE` 同步：圈号紧贴选项标签（`A.①②B.①④`）不再被 `(?<![\w])` 误挡 |
| `backend/tests/test_geo_subq_expand.py` | **新增** | 10 例：正常展开 Q1-Q2/Q3-Q5、Q43 拒绝、不造假结构、短答不纳入 |

**未改**：Gate / Admission / 门限。数据不足仍 reject，不猜测。

---

## 2. 测试

```
137 passed（test_geo_subq_expand 10 + manifest_binding + ir + compiler + resolver
             + gate_service + funnel + sibling_unit_id + composite_no_fake
             + answer_marker + option_fullwidth_comma）
```

关键断言：Q43 `option boundary unresolved` 必须拒绝；multi-q 不得合成假单题；`sub_questions=[]` 或真实确定数量。

---

## 3. E2E 实测对比表

数据库 `aitutors_geo_subq_v2`，四卷同版本（输入哈希与基线一致）：

| 卷 | Before | After | 备注 |
|---|---|---|---|
| 数学 | 25 | **25** | 不变 |
| 化学 | 21 | **21** | 不变 |
| 物理 | 10 | **19** | **见 §4 溢出效应** |
| 地理 | 0 | **37** | 确定性子题展开 |
| **合计** | **56** | **102** | |

**地理 37 题**：qn = 1–15, 21–25, 30–42, 47–50；全部 `stem=1, options=4, answer=1`。
**Q43 = 0**（选项 OCR 截断 `A.①②③B.①②④C`，正确拒绝）。

**缺口 13 题**（50−37）：Q16–20 / Q26–29 / Q44–46 因 composite 原子性——同组任一子题选项未解析则整组不产叶（Q43 为 1 题安全拒）。这些是 OCR 选项粘连/截断，非映射歧义。

---

## 4. 物理 10→19 溢出说明

为支持地理 OCR 变体（`15·`/`20，`、圈号紧贴选项标签 `A.①②B.`），`is_question_start` / `_LABEL_RE` 做了**全局** OCR 分隔符容忍修正（非地理特例）。物理卷同样存在这些 OCR 形态，此前 9 道真题因题号/选项识别失败被拒；修正后正常解析入库（stem/options/answer 完整，无造题）。

这是**识别正确性提升的溢出效应**，不是门槛放宽。若 Owner 要求物理严格锁 10，需另裁决是否回退该正则（会同时打回地理部分子题）。

---

## 5. 内容完整性

| 卷 | Questions | stem+answer+option | ≥4 options |
|---|---|---|---|
| 化学 | 21 | 21 | 21 |
| 数学 | 25 | 25 | 25 |
| 物理 | 19 | 19 | 19 |
| 地理 | 37 | 37 | 37 |

---

## 6. 数据库

- 新建 `aitutors_geo_subq_v2`（实验隔离库）；`SELECT current_database()` 断言通过（DB_IDENTITY 日志）。
- **未写入** aitutors / aitutors_test / aitutors_testsuite / aitutors_e2e_4paper。
- 历史 56 题未重算为本轮产出。

---

## 7. Git 状态

- V3 `od01-r3-convergence` = **`b8ea7cf`** = origin（已同步）。
- AITutorX `main` = **`fb5bdef`** = origin（已同步）。工作区 `MIMO-TASK` 与 untracked 现场原样保留。
- 未提交保留：V3 `_p14b_*` 脚本、Papers `data/`/`logs/`/`_p14b_patch_producer.py`。
