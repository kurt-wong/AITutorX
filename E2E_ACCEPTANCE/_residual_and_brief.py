from pathlib import Path
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
(OUT / "TASK_A_RESIDUAL_AND_AUDIT_FAILS.md").write_text("""# 任务 A 收口 · 残余风险与审计失败说明

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
""", encoding="utf-8")
print("wrote residual + audit fails note")

# Task B brief (boundaries only)
(OUT / "TASK_B_BOUNDARY_BRIEF.md").write_text("""# 任务 B — 正式产品链 E2E · 边界书

## 目标
找出正式链中**第一个尚未打通的环节**，不是证明文档完整。

## 边界（Owner 裁定）
1. **正式入口优先**：`TaskExecutor task_type=document_ingest` → Seal → Annotation → Compile → Gate → DB 持久化 → 前端读取
2. **禁止**用 Phase 1 `preprocessing_consumer_phase0` Runner 顶替；若正式入口吃不下预处理产物 → **报告接口/契约缺口**，不许切回实验路径宣布成功
3. **首轮不修生产逻辑**：只验证与定位；若必须改代码 → 先列缺口/证据/最小方案，另授权
4. **保留任务 A 基线**：不重置、不覆盖、不把 Q17 例外混入 E2E 结论
5. **逐层留证**：每层记 输入/输出、数量、ID 关联、失败原因、文件哈希  
   必须能区分：预处理输入错 | 正式入口接入错 | V3 处理错 | DB 持久化错 | 前端读取错

## 已知前置
- 2 worktree audit fails 已说明，与 Task A 功能无关
- Q17 / Q20 / OCR 边界保持另案

## 首轮交付
- 正式调用链实测轨迹（哪层通、哪层断）
- 缺口清单（接口/契约/数据）— **只报告不修**
""", encoding="utf-8")
print("wrote TASK_B_BOUNDARY_BRIEF.md")
