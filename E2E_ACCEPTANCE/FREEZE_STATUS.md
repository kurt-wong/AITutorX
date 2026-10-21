# Viewer 冻结状态 · 本轮只读

## 已执行
1. RAW 证据冻结 → `FROZEN_EVIDENCE/`（viewer_data_raw.json + data.js + SHA，只读）
2. `05_V3_OUTPUT/*.v3.json` 只读
3. Viewer：选项完整性标记（空壳/吞并）+ 分维度反馈（题干/选项/答案/LaTeX/整体）
4. Gate1：全文未切片 + 题号锚定 + 全文检索
5. 页面记录：正式链 vs 实验路径、Resolver 二次缺陷形态、可证明上限

## 裁定采纳的三点校正
- **冻结后禁止再跑 export_raw_full.py**（会覆盖证据）→ 证据已隔离到 FROZEN_EVIDENCE/ 只读
- **正式链不消费 Papers manifest**（TaskExecutor document_ingest 自有 Annotation）→ 已写入 Viewer facts
- **inline 只定位标签区间** → 最小断言应为「标签后至下一标签前」内容，不是空壳数下降

## 分维度策略（不整题跳过）
| 维度 | 选项结构异常时 |
|------|----------------|
| 题干 | 可独立验收 |
| 选项 | 只标异常，不判内容对错 |
| 答案 | **暂不可判**（answer↔labels 依赖 options） |
| LaTeX | 独立报渲染成败 |
| 整体 | 暂缓 |

## 可证明上限
S1 = data.js ↔ viewer_data_raw.json 内部一致。
更强证据 = viewer_data_raw.json ↔ DSH 独立重放逐选项比对（待执行，不改文件）。

## 明确未做
- 未修改 Resolver / Producer / Gate / Schema / P1.4-B
- 未宣布九科 E2E 通过
- 未跳过 97 题
