# M3a + M2-R2 验收收尾报告

## 1. 本轮目标

1. **M3a**：Review Console 能查询并展示已 Admission 物化的真实 Question（正文/选项/答案/学科年级/身份溯源），并用真实 Q8 样本验证 LaTeX 公式渲染与失败降级。
2. **M2-R2 收尾**：补齐 40 个 Producer units 逐单元结局表，重点解释未进入 Candidate 的单元。
3. **subject/grade**：按 Owner 定稿映射（Producer 路径规则）落真实值或保留 NULL；knowledge_links / materials 本轮不扩范围。

## 2. 实际成果

### A. M3a Review Console

| 项 | 结果 |
|---|---|
| 只读查询 API | `GET /api/questions`、`GET /api/questions/{id}`（新 `backend/app/api/routers/questions.py`） |
| 列表页 | `/admin/questions`：题号/类型/学科/年级/来源/identity，21 行真实数据 |
| 详情页 | `/admin/questions/{id}`：题干/选项/答案 + 源文档 + Source role/artifact_kind + dedup |
| 公式 | `MathText`（KaTeX）渲染 `$...$`；失败降级为原始片段（琥珀高亮 + title 提示），不整页崩溃 |
| 学科/年级 | 真实存储值 `化学` / `高一`；NULL 时显示「未设置」 |
| 依赖 | `katex@0.18`（约 280KB min JS + CSS/字体，经 Vite 分包）；理由：题干含 `\mathrm`/下标/混排，字符串替换无法正确渲染 |

### B. subject / grade 映射（Owner 定稿）

- **Producer**：`Papers/scripts/reslice_pipeline.py` 新增 `grade_subject_from_rel_path()`，在 `write_outputs()` 写入 manifest 的 `grade` / `subject` / `grade_source`。`五年级` 按真值输出、不进 `高三` 兜底，便于导入层过滤。
- **本包**：台账 `会考/化学/2018北京春季高中会考化学（教师版）(1).md` → **grade=高一, subject=化学**, `grade_source=path_keyword:会考/合格考/学业水平考试`。已写入包 `manifest.json`（manifest 不进身份 hash，不重开 M1）。
- **消费端**：`manifest_annotation.py` 不再硬编码 None，从 manifest 读取；`executor` 透传。
- **存量收敛**：21 题 `subject/grade` NULL→`化学`/`高一`（fail-loud 收敛语义，无冲突）；annotation `c38ee1ab` claims 同步。
- **materials / knowledge_links**：仍为 0。属「本轮未实现 + 无可用来源」（Producer manifest 无材料共享声明 / 无知识树），**不伪造**。不影响 M3a 展示。

### C. M2-R2 逐单元结局表

见 `AITutor-X/E2E_ACCEPTANCE/M2-R2-UNIT-OUTCOME-TABLE.md`。

| 桶 | 数量 | unit_id |
|---|---|---|
| Question+Instance | 21 | Q1–Q8, Q10–Q18, Q20–Q23 |
| Candidate pending_review | 3 | U-cl1, U-cl2, U-cl3 |
| 无 Candidate（Gate skip） | 16 | Q9, Q19, Q24, Q25, U-req1–6, U-org1–3, U-cp1–3 |

**未进入 Question 共 19** = 3 pending + 16 无 Candidate（与裁决「19」口径对齐）。

16 个无 Candidate 单元的可追溯原因（有界补跑：同一 annotation + 同一 sealed 584 行，复现 ready 集合与 M2-R2 Candidate 集合完全一致）：

| 原因 | 单元 |
|---|---|
| option span 未解析（选择项行证据不足） | Q9 (A–D), Q19 (B–D), Q24 (A–D), Q25 (B–D) |
| stem 未解析（如 question number '26' not found） | U-req1–6 |
| answer 未解析 / manifest 无 answer_lines | U-org1–3, U-cp1–3 |

证据：`e2e_run/m3a_unit_outcome.json`、`e2e_run/m3a_skip_reasons.json`。

## 3. 验收证据

### 环境

- 分支 `od01-r3-convergence`，固定提交 **`fefa7a1`**（feat(m3a): Review Console real Questions API/UI + KaTeX；本地领先 origin，**未推送**）
- Producer 映射提交：`Papers`@**`b141bfd`**（grade/subject path mapping）
- M2-R2 前序 HEAD：`336453b`（仍是祖先）
- 库：`aitutors_test`（验收）/ `aitutors`（共享，只读对照）
- 运行：FastAPI :8000 + Vite :5173，Playwright 无头 Chromium 走真实页面

### API（`e2e_run/m3a_api_evidence.json`）

```
GET /api/questions?limit=100  → 200, total=21
GET /api/questions/{q8}       → 200
  subject=化学 grade=高一
  OPT A ' HCl'
  OPT B ' $CO_{2}$'
  OPT C ' $MgCl_{2}$'
  OPT D ' $CH_{4}$'
GET /api/questions/{missing}  → 404
```

原始 LaTeX **完整保留**（API 不改写正文）。

### 页面（`e2e_run/m3a_page_*.png` + `m3a_page_evidence.json`）

1. `/admin/questions`：表格 21 行，学科/年级均为化学/高一，与 DB 一致。
2. `/admin/questions/5f461ef4-…`（Q8）：
   - 题干「8．下列物质中，含有离子键的是」
   - 选项 B/C/D 渲染为 CO₂ / MgCl₂ / CH₄（`.katex` 节点数 **3**，失败降级 **0**）
   - 答案「C」；identity/dedup/来源文档可见。

### 公式与降级

- KaTeX 对 `$CO_{2}$` / `$MgCl_{2}$` / `$CH_{4}$` / `$\mathrm{H_{2}S(g)+CO_{2}(g)}$` 渲染成功（含下标）。
- 坏公式（`\\bad{`）→ 组件 catch → 原始片段 + 「公式渲染失败，已显示原始内容」；混排普通文本不受影响；整页不崩。

### 测试

`tests/test_m3a_questions_api.py` 4 项 + 既有 manifest/artifact_kind 套件 = **20 passed**（`aitutors_test`，conftest 强制隔离）。

### 数据库前后对照（`e2e_run`）

| 表 | 共享 aitutors | aitutors_test（后） |
|---|---|---|
| documents | 13 | 16 |
| questions | **0** | **21** |
| question_instances | 0 | 21 |
| admission_candidates | 0 | 25 |
| materials / knowledge_* | 0 | 0 |

共享库 **零业务表变化**（questions 仍为 0）。

### subject/grade

21/21 = `化学`/`高一`；annotation claims 与 `grade_source` 已记录。

## 4. 未完成事项

1. **DSH 独立验收**（E）：待本报告固定提交 SHA 后，由 DSH 在同一 SHA / 同一 `aitutors_test` / 同一输入包只读复核。
2. **人工点验**：已用 Playwright 走真实页面（API+DB），若要求真人操作记录，请在 Console 再点一次 Questions → Q8 签字确认。
3. **4 个 pending Candidate**（U-cl1–3）未人工 Approve/Reject — 等 Owner 阅卷规则，不在 M3a 范围。
4. **16 个 incomplete 单元**未回炉重解析 — 属 Producer/Resolver 证据缺口，登记后续最小任务，不扩本轮。
5. **knowledge_links / materials** 空 — 无来源，待知识树与材料契约。
6. 本地提交 **`fefa7a1`**（AITutors-v3）/ **`b141bfd`**（Papers）**未推送** origin。

## 5. 整体进度

| 里程碑 | 状态 |
|---|---|
| M1 输入就绪 | ✅（不重开） |
| M2-R2 真实主链 | ✅ 21 Question / 21 Instance |
| M2-R2 证据收尾 | ✅ 逐单元结局表 + subject/grade 落值 |
| M3a Console 真题展示 | ✅ API + 页面 + Q8 LaTeX |
| M3b 反馈闭环 | ⬜ 未开始 |

## 6. 下一步

1. DSH 同 SHA 只读验收（题目真实性 / Q8 渲染 / 19 单元结局 / subject-grade / 共享库零变化）。
2. Owner 裁定 U-cl1–3 与 16 个 incomplete 单元是否回炉（另开任务）。
3. M3b：结构化问题分类（题干不完整/选项缺失/答案错误/公式渲染失败）+ 反馈持久化。

---

### 附件索引

- 逐单元结局表：`AITutor-X/E2E_ACCEPTANCE/M2-R2-UNIT-OUTCOME-TABLE.md`
- API 证据：`e2e_run/m3a_api_evidence.json`
- 页面证据：`e2e_run/m3a_page_evidence.json`、`m3a_page_questions_list.png`、`m3a_page_q8_detail.png`
- 跳过原因：`e2e_run/m3a_skip_reasons.json`
- 单元映射：`e2e_run/m3a_unit_outcome.json`
- 包 manifest（grade/subject）：`06_M1_PACKAGES/chem-2018-spring-huikao-teacher/manifest.json`
