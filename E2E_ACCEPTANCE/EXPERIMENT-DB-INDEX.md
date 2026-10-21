# 实验库索引（用途与运行归属）

| 数据库 | 用途 | 内容摘要 | 保护 |
|---|---|---|---|
| `aitutors` | 共享业务库 | 13 docs / 0 questions | **只读** |
| `aitutors_test` | 人工验收库 | **21 题 + 3 反馈**（chem 基线） | **禁止写入/清库** |
| `aitutors_testsuite` | 自动化测试专用 | 测试夹具（业务表可被清理） | 仅 pytest |
| `aitutors_phasec_exp` | 首批试跑（含错误切片 md 轮） | 混有 2 轮，**勿汇总** | 可弃 |
| `aitutors_prod_batch` | 第一批生产计量（正确原源 md） | 4 卷：31 批 / 41 待审 / 45 拒 | 只读计量 |
| `aitutors_repro_r1` / `_r2` | 数学+物理双跑 | 两轮结果一致 | 可弃 |
| `aitutors_repro_cg` | 化学+地理固定条件重跑 | chem 21 题稳定；geo 0 稳定拒 | 可弃 |

**代码基线**：AITutors-v3 `27f462a` · Papers `a4a0a8c`  
**漏斗**：`backend/data/funnels/{ann_id}_{run_id}.json`，含 `run_id` / `database` / `input_hashes`；**勿跨文件汇总**。
