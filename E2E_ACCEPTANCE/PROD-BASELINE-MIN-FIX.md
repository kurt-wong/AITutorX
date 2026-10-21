# 最小修复 + 可复现基线（非治理阶段）

## 1. P0：同卷两轮差异 — 已解释

| 轮次 | 数学 ready | 物理 ready | 输入 md |
|---|---|---|---|
| 早先 phasec_exp | **0** | **0** | reslice **切片** md（含「答案区/题干区」标记） |
| 之后 prod_batch | **30** | **18** | **原始 OCR** md |

**结论**：实验条件不一致（输入 md 不同），**不是**代码不稳定。化学对照卷 md 哈希与已验收包一致，21 题基线仍可信。

### 同条件双跑（新建库，同包、同代码、同入口）

| 库 | 数学 (pdf `3b87f19f…`) | 物理 (pdf `98bcc618…`) |
|---|---|---|
| `aitutors_repro_r1` | 30 pending / **0 Q** | 10 批 + 8 待审 / **10 Q** |
| `aitutors_repro_r2` | 30 pending / **0 Q** | 10 批 + 8 待审 / **10 Q** |

**`reproducible: true`** — 同输入哈希、同 V3 `9a4bfb7`、同 Papers `a4a0a8c`。

## 2. 已做最小修复

| 项 | 状态 |
|---|---|
| `unexplained_loss` 不再双扣 pending_review | ✅ `unexplained_loss = input − ir_ready − failures` |
| 漏斗记录 `run_id` + `input_hashes` | ✅ |
| 每次运行独立漏斗文件 `{ann_id}_{run_id}.json` | ✅ |
| 入库数以 DB 为准 | ✅ 报告口径注明 |
| 测试 | 3 passed（`test_funnel_unexplained_loss.py`） |

## 3. 产出口径（三态）

| 结局 | 定义 | 第一批实测 |
|---|---|---|
| **Accepted** | 证据足，自动入库 | **31**（stem/answer/option 全） |
| **Pending review** | 未达自动标准，待人工 | **41**（≠合格、≠拒绝） |
| **Rejected / skipped** | incomplete，有原因可溯 | **45** |

单元 117 = 31 + 41 + 45。**26.5% 为单批样本，不是稳定产能承诺**；双跑证明在固定条件下可复现。

## 4. 保护

- `aitutors_test` 21 题 + 3 反馈：**未写入**。
- 实验仅在 `aitutors_repro_r1/r2`、`aitutors_prod_batch`、`aitutors_phasec_exp`。
- 未改 Gate/Admission、未批 41 条 pending、未做 Q9 通用结构。

## 5. 下一步（待你点头）

在相同输入/代码/初态下扩到 3–5 卷，用三态口径出稳定基线；再按失败分布决定是否做地理 composite。

---

附件：`repro-db-compare.json`、`rerun-compare.json`、`PROD-METRICS.json`
