# 任务 A 收口 · 残余风险与审计失败说明

## Q17 回退行为 — 残余风险登记（不阻塞正常样本）

| 项 | 内容 |
|----|------|
| 现象 | `Empty content falls back to whole-line ok`：当内容区间为空（如 manifest 误声明 `H` 使 `B. H: O: H` 的 B 内容被切空）时，回退为**整行** span |
| 影响面 | 仅 Q17 型「假标签把前一选项内容切空」的输入；97 题指标改善不受影响 |
| 是否阻塞 Gate2 正常样本验收 | **否** — 正常 A–D 样本走内容区间分支 |
| 处置 | **另案**，不重启大范围 Resolver 修改 |
| 验收口径 | 任务 A 验收的是「单行多选项内容区间」缺陷；**不是**「所有选项解析异常已解决」 |

## 2 个 failed 测试 — 与任务 A 无关的证据

### 1. `test_adv_state_audit.py::TestClaimedPushAndSuite::test_v3_worktree_clean_at_checkpoint`
- **断言**：`git status` porcelain 每行须匹配 allowed 模式
- **失败内容**：`?? backend/scripts/_p14b_patch_resolver.py` 等 3 个 **untracked 脚本**
- **性质**：工作区清洁度审计（要求 checkpoint 时 V3 worktree 无杂质）
- **与 Task A 关系**：无关。失败项是 **P1.4-B 时期的临时 patch 脚本**（未提交、未删除），不是 Task A 改动的 `resolver.py` / 测试
- **Task A 提交文件**：`resolver.py`, `test_task_a_option_content_span.py`, `test_resolver.py`, `test_option_fullwidth_comma.py`（均已 commit `512bba2`）

### 2. `test_adv_state_audit.py::TestClaimedPushAndSuite::test_x_worktree_clean`
- **断言**：AITutor-X `git status` 必须为空
- **失败内容**：大量 `?? Docs/60_REPORTS/*`、`?? e2e_run/*`、`?? E2E_ACCEPTANCE/` 等调查/报告产物
- **性质**：X 仓清洁度审计；本轮 E2E/Viewer/Task A 报告均落在该仓
- **与 Task A 功能关系**：**无**。不含任何生产代码断言

**结论**：2 failed = **workspace cleanliness audits**，非功能回归。功能面 2286 passed。
