# M3b-R1 报告：测试库隔离 · 验收库恢复 · FunnelRecorder 正式接入

## 1. 本轮目标

1. **测试隔离**：自动化测试改用专用库 `aitutors_testsuite`，禁止写共享库 `aitutors` 与人工验收库 `aitutors_test`。
2. **验收库恢复**：清除 4 个测试夹具 Question，恢复 `total=21`、唯一 Q8，保留真实反馈。
3. **复验反馈闭环**：真实 Q8 反馈链路有效，且反馈不改题。
4. **FunnelRecorder 正式路径接入**：Gate/IR 失败与跳过产生可复核记录。

## 2. 实际成果

### 2.1 测试隔离（方案 1）

| 项 | 实现 |
|---|---|
| 专用库 | `aitutors_testsuite`（已创建并迁移） |
| `conftest.py` | 强制 `DATABASE_URL` → testsuite；`_assert_testsuite_db()` fail-closed |
| 禁止目标 | `aitutors`（共享业务库）、`aitutors_test`（人工验收库） |
| 建表/迁移 | `alembic upgrade` 仅作用于 testsuite |
| 行为覆盖 | 反馈持久化、9 类校验、目标关联、题目不被改写 — **未 mock DB 写入** |
| 隔离测试 | `test_m3b_r1_isolation.py`（5 项）：拒绝共享/验收库、env 锁定 testsuite |

### 2.2 验收库恢复（`aitutors_test`）

夹具特征（从库内重新确认）：`occurrence_key='occ-q8'`、`question_number=8`、创建于 14:41–14:42。

| 角色 | 主键 | 处置 |
|---|---|---|
| **保留** 真实 Q8 | `5f461ef4…` / `5ce35672…` | 不动 |
| **保留** 真实反馈 | `50a38c8b…` | 不动 |
| 夹具 Q1 | `9afd98ff…` | 删除（含 instance/contents/doc/sv） |
| 夹具 Q2 | `c0be44b0…` | 删除 |
| 夹具 Q3 | `4279b747…` | 删除 |
| 夹具 Q4 | `9646f1e2…` | 删除 |
| 夹具反馈 | 12 条（指向上述 Q） | 删除 |

清理前后（`e2e_run/m3b_r1_fixture_cleanup.json`）：

| 表 | 前 | 后 |
|---|---|---|
| questions | 25 | **21** |
| question_instances | 25 | **21** |
| instance_role_contents | 130 | **126** |
| question_feedbacks | 13 | **1** |
| documents | 20 | **16** |
| 题号=8 | 5 | **1** |

### 2.3 反馈闭环复验

- `GET /api/questions` → **total=21**，`question_number=8` **恰好 1 条**（`5f461ef4`）。
- 真实反馈仍在：`50a38c8b` → Q8/Instance，category=`latex_render_error`，描述与 M3b E2E 一致。
- Q8 题干/选项/答案与 M3a 快照一致（` $CO_{2}$` 等原文保留）。
- 反馈仍不改题（testsuite 内自动化断言 text_hash 不变）。

### 2.4 FunnelRecorder 正式接入

| 位置 | 行为 |
|---|---|
| `funnel_recorder.skip_unit` | 记录 unit_id/stage/reason/evidence |
| `funnel_recorder.ir_skip_reasons` | 从 IR 推导 skip 原因（stem/option/answer span） |
| `GateService.run(..., funnel=)` | 对每个非 ready unit 调用 `skip_unit`；统计 input/ir_ready/candidates/pending |
| `TaskExecutor._compile_stage` | **正式路径**创建 FunnelRecorder → GateService → `data/funnels/{annotation_id}.json` |

不改变 Gate/Admission 决策；不把补跑冒充历史。

## 3. 验收证据

### 环境

- 分支 `od01-r3-convergence`，基线 `601400d`（M3b，**未推送**）
- 本轮固定提交 **`9a4bfb7`**（**未推送**，ahead 20）
- 测试目标库：**`aitutors_testsuite`**
- 人工验收库：`aitutors_test`（已恢复）
- 共享业务库：`aitutors`（只读对照，零变化）

### 隔离证明（`m3b_r1_acceptance_state.json`）

| 库 | questions | qn8 | feedbacks |
|---|---|---|---|
| 共享 aitutors | 0 | 0 | 无表 |
| **验收 aitutors_test** | **21** | **1** | **1**（真实） |
| 测试 aitutors_testsuite | 3 | 3 | 11（测试写入） |

跑完测试后验收库仍为 21 — **测试未污染验收库**。

### API

`GET /api/questions?limit=100` → `total=21`；`question_number=8` 计数=1。

### 测试

`test_m3b_r1_isolation` + `test_m3b_r1_funnel` + `test_m3b_feedback` + `test_m3a_questions_api` = **15 passed**（testsuite）。

### Funnel

- `test_m3b_r1_funnel`：skip 单元写入 `funnel.failures`（stage=`resolver_ir`，含 problems）。
- 源码确认：`executor._compile_stage` 传 `funnel=` 并 `funnel.write(...)`。

## 4. 未完成事项

1. **DSH 同 SHA 只读核验**。
2. 历史 10 单元的原始 funnel 仍缺失（本轮只保证**未来**正式路径有记录）。
3. U-cl1–3 pending；incomplete 单元回炉未做。
4. Funnel 落盘路径 `data/funnels/` 为文件观测，未进 Frozen 表结构（契约无 funnel 表；若需 DB 持久化另提最小差异）。

## 5. 整体进度

| 里程碑 | 状态 |
|---|---|
| M1 / M2-R2 / M3a / M3b | ✅ |
| M3b-R1 测试隔离 | ✅ |
| M3b-R1 验收库恢复 | ✅ 21 题 / 唯一 Q8 |
| M3b-R1 Funnel 正式接入 | ✅ |
| DSH 独立核验 | ⬜ |

## 6. 下一步

1. DSH 核验：隔离是否真实、验收库 21/Q8 唯一、真实反馈完整、Funnel 在正式路径、共享库零变化。
2. Owner 裁定 incomplete 单元回炉范围。

---

### 附件

- 夹具清理：`e2e_run/m3b_r1_fixture_cleanup.json`
- 三库状态：`e2e_run/m3b_r1_acceptance_state.json`
- 真实 Q8：`5f461ef4-1362-417a-bd11-06723bbe0dc9` / Instance `5ce35672-f285-4cb1-ac9a-75ff7e097a4e` / Feedback `50a38c8b-72d8-4a4e-9b87-79ed0a177775`
