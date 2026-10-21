# Phase B — 真实题目问题定位与归因（只读诊断）

## 1. 基线与证据位置

### 基线（执行前核实，与预期一致）

| 仓库 | branch | HEAD | 与预期 |
|---|---|---|---|
| AITutors-v3 | `main` / `od01-r3-convergence` | `9a4bfb7c87bd5fa2e8173374b2780b3663568631` | ✅ |
| Papers | `main` | `b141bfda9a4bb5037adfe06fab8f8f75b096dc75` | ✅ |
| AITutor-X | `main` | `7bce0664972282ee073c313910bc8390e7bbadf5` | ✅ |

工作区：AITutors-v3 仅 3 个 untracked `_p14b_*.py`（未读写）；AITutor-X 大量 untracked 报告（只读引用）。**本轮零代码/零写库/零 LLM。**

### 读取过的证据

* `06_M1_PACKAGES/chem-2018-spring-huikao-teacher/{manifest.json, paper.md, PAIRING_EVIDENCE.json}`
* `e2e_run/m2-real-chem-20261010T132409Z.json`（原跑 funnel）
* `e2e_run/m3a_unit_outcome.json`、`e2e_run/m3a_skip_reasons.json`（M3a 有界补跑，**非历史**）
* `e2e_run/m3b_page_evidence.json`
* 库 `aitutors_test`：semantic_annotations / admission_candidates / questions / question_feedbacks
* 派生：`PHASE-B-DIAGNOSIS.json`、`PHASE-B-EVIDENCE-CHAIN.md`

---

## 2. 19 个诊断对象固定清单

来源：manifest `units`（40）∩ 库内候选映射 ∩ M3a 结局表。**不用题号前缀模糊匹配。**

| # | unit_id | 分桶 | 实际状态 | 来源标识 |
|---|---|---|---|---|
| 1–3 | **U-cl1, U-cl2, U-cl3** | pending_review | IR ready + Candidate 存在 | ann=c38ee1ab, sv=0df40d7b |
| 4–7 | **Q9, Q19, Q24, Q25** | 无 Candidate | IR incomplete（补跑） | 同上 manifest unit_id |
| 8–13 | **U-req1…U-req6** | 无 Candidate | IR incomplete（补跑） | 同上 |
| 14–19 | **U-org1–3, U-cp1–3** | 无 Candidate | IR incomplete（补跑） | 同上 |

**分母核对**：40 Producer units = 21 已成 Question + **19**（本清单）。无重叠；与 M3a 表 3 pending + 16 无 Candidate 一致。

历史 funnel `failures=[]` → 16 个 skip **无原跑逐单元失败记录**；IR 问题来自 M3a 有界补跑（已标注 supplemental）。

---

## 3–4. 逐簇证据链与归因

### 簇 A：U-cl1–3（pending_review，3）

| unit | 原文证据 | Annotation | IR | Gate 实际决策 | 归因 |
|---|---|---|---|---|---|
| **U-cl1** | L291–299 重阳糕 4 小问填空；L566–568 答案 `（1）①…` | fill_in, qn=1, stem+answer 有行 | ready | `fill_in not strict-auto (grammar None)` → pending_review | **已证实：Gate 对 fill_in 无 grammar 时禁止 auto-approve（设计如此，非缺陷）** |
| **U-cl2** | L301–317 短文 + 4 个对/错判断；L570–572 答案 `（1）对（2）对…` | 标为 **true_false** | ready | `answer not expressible as canonical value` | **候选：Producer 题型 `true_false` 与内容「四小问判断」不符 + Gate grammar 不接受多空复合答案** |
| **U-cl3** | L319–350 含图综合题 4 小问；L574–584 答案区 | short_answer | ready | `short_answer not strict-auto (grammar None)` | **已证实：同 U-cl1，设计性 pending_review** |

附注（身份）：U-cl1–3 的 `question_numbers` 为 1/2/3，与 Q1–Q3、U-req1–3 **分节重号**（manifest warnings 已标）。模块卷分节编号，不是错误，但检索/展示需靠 unit_id 而非题号。

**证据充分性**：充分（源文 + gate_decision JSON 齐备）。  
**无 Candidate 不成立**——三者均有 Candidate，停在 pending_review 供人工裁定。

---

### 簇 B：Q9 / Q19 / Q24 / Q25（option span 未解析，4）

| unit | stem | manifest options | 源文实际 | IR problems（补跑） |
|---|---|---|---|---|
| Q9 | L46「…属于合金的是」 | `options_lines=[51,51]` | **L51 起是 HTML `<table>`（实为 Q10 区）**，无 A/B/C/D 文本行 | options A–D 全 unresolved |
| Q19 | L142「…反应速率最快的是」 | `[145,145]` | L145 是 `<table>` | B–D unresolved（A 或可解析） |
| Q24 | L196「…不相符合的是」 | `[199,199]` | L199 `<table>` + 公式图 | A–D unresolved |
| Q25 | L201「…不相符的一组是」 | `[204,204]` | L204 `<table>`（含「选项」表头） | B–D unresolved |

对比：Q8 选项在 **单行文本** `A. HCl B. $CO_{2}$…`（L44）→ 解析成功。

**归因（有证据支持的候选）**：

1. **原始 OCR/版面缺陷**：这 4 题选项在 PDF 中为表格/图表，OCR 落成整块 HTML table，而非 `A. … B. …` 文本行。  
2. **Producer 切分缺陷**：`options_lines` 只给了单行区间，且该行不是选项文本；未把表格拆成 label→内容 span（对比 P1.4-B 已做 Rules A/B/C 仅覆盖文本形态）。  
3. 下游 Resolver 对「option 无 content span」→ incomplete（预期 fail-closed）。

**已证实**：IR incomplete 与「option 无 span」因果链完整。  
**待验证**：表格选项是否应在 Producer 拆行，或 Resolver 应消费表格单元格。

---

### 簇 C：U-req1–6（stem 未解析，6）

| 证据 | 内容 |
|---|---|
| manifest | `question_numbers=[26]…[31]`，`printed_number=[1]…[6]` |
| 源文 L208+ | 「一、必答题」印刷题号 **1.–6.** |
| annotation | `question_label: "26"`（全局号） |
| 补跑 unresolved | `question number '26' not found` |
| manifest warnings | 已标「题号 1 与 Q1 重号（分节各自编号）」 |

**归因（有证据支持的候选）**：

1. **Producer 身份映射缺陷**：分配全局 question_numbers 26–31，却未把 `printed_number` 交给 Resolver 作检索锚。  
2. **Annotation 源位置绑定缺陷**：stem 声明 `question_search_lines=[210,210]` 存在，但 Resolver 仍以题号字符串检索且失败 → 说明题号优先或 search_lines 未覆盖。  
3. 非 OCR 空白：L210 有完整题干文本。

**已证实**：补跑显示 stem unresolved；与题号 26 检索失败一致。  
**待验证**：Resolver 优先级（printed vs global）与 `question_search_lines` 实际消费路径（需读 resolver 代码，本轮未改）。

---

### 簇 D：U-org1–3 / U-cp1–3（answer 未解析，6）

| 证据 | 内容 |
|---|---|
| manifest `annotation_meta.validation_issues` | 逐条：`无 answer_lines（题号 [1]）` 等 6 条 |
| annotation content | `answer.answer_zone=answer_table` **无 answer_lines** |
| 补跑 IR | `role answer unresolved` / `answer unresolved` |
| 源文 | 模块题干在 L354+/L444+；**参考答案区有内容**，但 manifest 未绑定 |

**归因**：

1. **已证实（导入前）**：Producer manifest **无 answer 行区间**（validation_issues 书面记载）。  
2. **下游正确 fail-closed**：无 answer → IR incomplete → 不产 Candidate。  
3. 不是 Gate 误杀，也不是反馈问题。

---

## 5. 运行证据缺口

| 缺口 | 状态 | 影响 |
|---|---|---|
| 原跑 `funnel.failures` | **空** | 16 skip 无历史 per-unit 记录 |
| Gate `skipped` 列表 | **未持久化**（M3b-R1 起 FunnelRecorder 已接入正式路径） | 历史不可追溯；未来可追 |
| Resolver 逐 span 诊断 | 仅有 M3a 补跑 `unresolved` 摘要 | 可复现，但**不能**写成「原跑已确认」 |

**明确标注**：表中 IR problems = `supplemental_ok`（同一 annotation + 同一 sealed 584 行），**不是**原始运行记录。

---

## 6. 根因总表

| 簇 | 对象数 | 已证实 | 有证据候选 | 尚不能判断 |
|---|---|---|---|---|
| U-cl1/3 pending | 2 | Gate 设计：非 strict-auto 类型 → pending_review | — | — |
| U-cl2 pending | 1 | Gate：answer 无法表达为 canonical | 题型 true_false vs 多空复合；grammar 覆盖 | 是否应改题型或 grammar |
| Q9/19/24/25 | 4 | IR：option 无 span → incomplete | **OCR 表格选项 + Producer options 切分** | 拆表 vs Resolver 吃表格 |
| U-req1–6 | 6 | IR：stem unresolved；题号 26 不可检索 | **全局题号 vs printed 题号绑定** | search_lines 是否被 Resolver 忽略 |
| U-org/cp | 6 | **Producer 无 answer_lines**（导入前 issues） | — | 答案区行号是否可确定性回填 |
| 全部 16 skip | 16 | — | — | **原跑逐单元日志缺失**（历史） |

**不归责**：反馈机制、KaTeX、Admission 物化、测试隔离——与本 19 对象无关。

---

## 7. 重复反馈专项

| ID | 创建时间 | 内容 | 关联 |
|---|---|---|---|
| `50a38c8b-72d8-4a4e-9b87-79ed0a177775` | 2026-10-10T14:43:53Z | 「选项B/C/D公式下标显示异常（E2E验收）」latex_render_error | Q=`5f461ef4` I=`5ce35672` sv=0df40d7b，spans 齐 |
| `880b092a-1be6-4c21-8717-896bc45d4cb2` | 2026-10-10T16:11:45Z | **同上描述** | 同上真实 Q8/Instance |

**来源（现存日志可证）**：均来自真实 Console Playwright E2E（M3b 首轮、Phase A 复验），`created_by=console-user`。  
**一致性**：均指向真实 Q8，source_evidence 含真实 span。  
**引用**：无其他表引用。

**建议（不执行）**：二者都是对真实题目的有效反馈，**不必当测试垃圾删除**；若 Owner 要去重，可保留 `50a38c8b`（首次）并在 `880b092a` 的 review_note 标注「E2E 复验重复」。**由 Owner 裁决。**

---

## 8. 修复方向（仅建议，不实施）

| 优先级 | 方向 | 影响面 | 风险 | 建议验证 |
|---|---|---|---|---|
| P1 | Producer：表格选项拆 label/content span（或声明 table 角色） | Q9/19/24/25 同类 | 可能影响已成功 21 题的选项解析 | 同卷复跑，对比 21 题选项 hash 不变 |
| P1 | Producer/Resolver：printed_number 作检索锚，question_numbers 仅作内部 ID | U-req 同类 | 题号歧义（分节重号） | U-req1–6 stem 可解析且 Q1–6 不变 |
| P2 | Producer：为模块题补 answer_lines（或显式 absent） | U-org/cp | 错绑答案行 | 6 单元 answer 可解析或标记 absent |
| P3 | Gate grammar：多空判断题（对/错×N）或改 Producer 题型 | U-cl2 | 可能放大 auto-approve | U-cl2 能否 canonical 或明确人工 |
| — | U-cl1/3 | **无需修**（设计性 pending_review） | — | 人工 approve 即可入库 |
| — | Funnel | M3b-R1 已接入 | 历史不可补 | 新跑应有 failures |

**最小授权（下一阶段）**：允许只改 Papers Producer 切分/题号绑定（或 V3 Resolver 检索锚），同卷只读对比 21 题回归 + 19 对象状态；**禁止**未验证前批量改 Gate/Admission。

---

## 9. 仍无法判定

1. 表格选项应在 **Producer 拆行** 还是 **Resolver 吃 HTML table**（需样例对照与契约）。  
2. U-req：`question_search_lines` 为何未阻止题号检索失败（需读 resolver 源码，本轮只读未深挖实现）。  
3. U-org/cp 答案行区间是否可从参考答案区确定性回填。  
4. 原跑 16 skip 的逐单元历史原因——**证据不存在，不可追认**。

---

## 10. 结论

* **19 对象身份固定，无重叠，分母与 40=21+19 一致。**  
* **U-cl1/3**：非缺陷，等人工 approve。**U-cl2**：题型/grammar 与多空答案不匹配。  
* **4 道选择题**：表格化选项 + Producer options 切分不足 → option 无 span。  
* **6 道 U-req**：全局题号 vs 印刷题号绑定问题 → stem 解析失败。  
* **6 道 U-org/cp**：Producer 无 answer_lines（导入前已记载）。  
* **历史 funnel 空**：16 skip 原跑不可追溯；补跑仅作补充观测。  
* **重复反馈**：两条均为真实 Q8 有效记录，建议保留并标注，由 Owner 裁决。

**本阶段到此停止，不进入修复。等待 Owner 审阅。**
