# 10 单元失败/跳过证据状态表（M3b）

## 口径

- **historical_run_record**：M2-R2 原跑是否留下可核验的失败/跳过记录。
- 原跑 `m2-real-chem-*.json` 的 `funnel.failures` 为 **[]**；GateService 的 `skipped` 列表**未持久化**。
- 因此下列 10 单元 **`execution_evidence_missing`（历史）**。
- 表中 `supplemental_*` 来自 M3b 有界补跑（同一 annotation `c38ee1ab` + 同一 sealed 584 行）；
  **不是**原始运行记录，仅证明当前代码路径下的确定性结局。

## 为何是这 10 个

16 个无 Candidate 单元中：

- U-org1–3 / U-cp1–3（6）：Producer `annotation_meta.validation_issues` 已记载「无 answer_lines」→ 有导入前证据。
- Q9/Q19/Q24/Q25 + U-req1–6（**10**）：原跑无任何 per-unit 失败记录 → 本轮点名收尾。

## 逐单元

| unit_id | 分类 | 历史执行记录 | 最后成功阶段 | 首个失败/跳过 | 补跑观测（非历史） | 证据是否足够 | 标记 |
|---|---|---|---|---|---|---|---|
| Q9 | option_span_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(option) / IR incomplete | role option unresolved; role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['A', 'B', 'C', 'D'] | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| Q19 | option_span_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(option) / IR incomplete | role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['B', 'C', 'D'] | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| Q24 | option_span_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(option) / IR incomplete | role option unresolved; role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['A', 'B', 'C', 'D'] | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| Q25 | option_span_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(option) / IR incomplete | role option unresolved; role option unresolved; role option unresolved; option spans unresolved: ['B', 'C', 'D'] | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req1 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req2 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req3 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req4 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req5 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |
| U-req6 | stem_unresolved | **缺失**（funnel.failures 空） | Annotation（40 unit 绑定成功） | Resolver(stem) / IR incomplete | role stem unresolved; stem unresolved | 历史不足 / 补跑可复现 | execution_evidence_missing + supplemental_ok |

## 结论

1. 10 单元**均未**生成 Candidate（与库内一致：无 admission_candidates.ir_units 命中）。
2. **不得**写成「原跑已确认解析失败」；只能写「原跑无记录 + 补跑显示 incomplete」。
3. 补跑 ready 集合（24）与原跑 Candidate 集合完全一致 → 补跑可信，但不冒充历史。
4. 全部单元无需强行生成 Candidate；本表目标是**结局与证据缺口透明**。

## 证据文件

- `e2e_run/m2-real-chem-20261010T132409Z.json`（funnel.failures=[]）
- `e2e_run/m3a_skip_reasons.json`（补跑 IR 状态）
- `e2e_run/m3a_unit_outcome.json`（40 单元映射）
- `06_M1_PACKAGES/.../manifest.json` annotation_meta.validation_issues
