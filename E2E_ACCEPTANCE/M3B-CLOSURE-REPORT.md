# M3b 报告：Q8 身份处置 · 10 单元证据收尾 · Human Verification 反馈闭环

## 1. 本轮目标

1. 安全识别并处置修复前遗留的 Q8 候选，消除审核/反馈歧义。
2. 补齐 40 units 中 **10 个**缺少可核验历史失败记录单元的证据状态。
3. 实现最小可用 **结构化反馈闭环**（绑定真实题目/源证据/类别；与修复分离）。

## 2. 实际成果

### 2.1 Q8 身份歧义处置

| 角色 | 主键 | 状态 | 依据 |
|---|---|---|---|
| **修前遗留 Candidate** | `563c3839-c0c5-405d-a7c1-2971c3038729` | `pending_review` → **`rejected`** | sv=`53814898`（旧 273 行）ann=`11f981c9`（旧 LLM 41 unit）；gate 失败 answer grammar；**无 admission_event / 无 Question / 无 Instance / 无引用** |
| **修后有效 Candidate** | `cc32656c-f834-4ddc-aa89-e4660be8cdfa` | `approved` | sv=`0df40d7b` ann=`c38ee1ab`，auto_approve |
| **正式 Question** | `5f461ef4-1362-417a-bd11-06723bbe0dc9` | 唯一 | 由 cc32656c 物化 |
| **正式 Instance** | `5ce35672-f285-4cb1-ac9a-75ff7e097a4e` | 唯一 | occurrence=`13e7a136…` |
| **当前 Console/API 展示** | 同上 Q/I | — | `GET /api/questions/{5f461ef4}` 与页面一致 |

处置方式：**不删行**，走既有 `AdmissionService.reject()` 唯一入口（审计保留、不动冻结模型）。

`review_trail` 记录：`pre_fix_identity_ambiguity` / `superseded_by_formal_candidate_cc32656c` / `source_version_53814898_legacy_line_mode` / `gate_answer_grammar_fail`。

清理前后：`questions/instances/admission_events` 计数不变；有效 Q8 未动；`pending_review` 4→3（仅 U-cl1–3）。

### 2.2 10 单元证据收尾

见 `M3B-10-UNIT-EVIDENCE-TABLE.md`。

**口径**：原跑 `funnel.failures=[]`，Gate `skipped` 未持久化 → 10 单元历史记录**缺失**，标记 `execution_evidence_missing`。

| unit_id | 补跑观测（非历史） | 标记 |
|---|---|---|
| Q9, Q24 | option A–D span 未解析 | execution_evidence_missing + supplemental_ok |
| Q19, Q25 | option B–D span 未解析 | 同上 |
| U-req1–6 | stem 未解析 | 同上 |

- 不得写成「原跑已确认解析失败」。
- 补跑 ready=24 与原跑 Candidate 集合一致 → 补跑可信，但**不冒充历史**。
- U-org/U-cp 有 manifest `validation_issues`（无 answer_lines），不列入本 10。

### 2.3 反馈闭环（与修复分离）

**持久化**：新表 `question_feedbacks`（Alembic `0012`，`CREATE IF NOT EXISTS`，兼容 0001 create_all）。

字段：`id, question_id, instance_id, source_version_id, producer_unit_id, source_evidence(JSONB), content_snapshot(JSONB), category, description, status, created_by, created_at, review_note`。

**API**：
- `POST /api/feedbacks`（校验 category/描述/归属；写快照+源证据）
- `GET /api/feedbacks` / `GET /api/feedbacks/{id}` / `GET /api/feedbacks/categories`

**类别（9）**：题干/选项/答案/解析/材料/LaTeX/身份题号/学科年级/其他。

**UI**：Question 详情页反馈表单（显示关联题目+instance）；`/admin/feedbacks` 列表。

**分离保证**：反馈不改 Markdown / Question / Answer / Source / Gate / Admission（测试断言 text_hash 不变）。

## 3. 验收证据

### 环境

- 分支 `od01-r3-convergence`，本轮固定提交 **`601400d`**（M3b；基线 `fefa7a1`；**未推送**，ahead 19）
- Papers `b141bfd`（**未推送**，ahead 4）
- 库：`aitutors_test` 写入；`aitutors` 只读对照
- FastAPI :8000 + Vite :5173 + Playwright

### Q8 处置

`e2e_run/m3b_q8_dispose.json`：before/after 主键、计数、review_trail；Q8 仅 `5f461ef4` 一行。

### 10 单元

`M3B-10-UNIT-EVIDENCE-TABLE.md` + `e2e_run/m3a_skip_reasons.json`（补跑）+ 原跑 funnel 为空的对照。

### 反馈 API / 页面

自动化：`tests/test_m3b_feedback.py` 4 项 + M3a 4 项 = **8 passed**。

真实页面 E2E（`e2e_run/m3b_page_evidence.json` + 截图）：

1. 打开 `/admin/questions/5f461ef4…`（Q8，含 KaTeX 选项）
2. 选择「LaTeX/公式渲染异常」，填写说明
3. 提交 → 「已保存反馈 50a38c8b… status=open」
4. 刷新页面表单仍在
5. `/admin/feedbacks` 列表可见该条，指向 `Question 5f461ef4` / `instance 5ce35672` / `sv 0df40d7b` + 真实 span（P1L042… / P1L513）

### 不变式

- Q8 正文 text_hash 与 M3a 时一致（未被反馈改写）
- 共享库：`questions=0`，无 `question_feedbacks` 表

### 隔离计数（`m3b_db_isolation.json`）

| 表 | 共享 aitutors | aitutors_test |
|---|---|---|
| questions | 0 | 25（21 真题 + 4 测试夹具） |
| question_feedbacks | 无表 | 13（1 条 E2E + 12 条测试） |
| admission_candidates | 0 | 25 |

## 4. 未完成事项

1. **DSH 同 SHA 只读核验**（待本轮固定提交）。
2. 真人签字式点验（E2E 已由 Playwright 走真实页面）。
3. U-cl1–3 仍 pending_review；16 incomplete 单元未回炉。
4. 测试夹具反馈/题目混在验收库（未影响 21 真题；如需可另做清理）。
5. 反馈处理工作流（in_review→resolved）仅有状态字段，无 UI 工作流。

## 5. 整体进度

| 里程碑 | 状态 |
|---|---|
| M1 / M2-R2 / M3a | ✅ |
| M3b Q8 歧义处置 | ✅ |
| M3b 10 单元证据透明 | ✅ |
| M3b 反馈闭环 | ✅ 最小可用 |
| 修复回炉 / 自动闭环 | ⬜ 后续 |

## 6. 下一步

1. DSH 在本轮 SHA / `aitutors_test` / 同一输入包上只读核验。
2. Owner 裁定 U-cl 与 incomplete 单元是否回炉。
3. 反馈列表增加处理状态操作（仍不自动修题）。

---

### 附件

- Q8 映射与处置：`e2e_run/m3b_q8_dispose.json`
- 10 单元表：`M3B-10-UNIT-EVIDENCE-TABLE.md`
- 页面 E2E：`e2e_run/m3b_page_evidence.json`、`m3b_page_q8_after_submit.png`、`m3b_page_feedback_list.png`
- 隔离：`e2e_run/m3b_db_isolation.json`
