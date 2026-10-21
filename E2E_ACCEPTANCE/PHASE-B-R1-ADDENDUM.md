# Phase B-R1 — 对抗性审查补记与 Phase C 前置条件冻结

**性质**：只读补记。不改代码 / 不写库 / 不跑管线 / 不删反馈 / 不动分支。  
**基线**：AITutors-v3 `9a4bfb7` · Papers `b141bfd` · AITutor-X `7bce066`（执行前核实一致）。  
**证据**：`PHASE-B-R1-EVIDENCE.json`、manifest `paper.md` HTML table、`aitutors_test` 反馈只读查询。  
**O1–O3 追加证据**：`PHASE-B-R1-O1O3-EVIDENCE.json`（表格/printed NULL/U-cl2）；图像路径探测 + PDF `get_images` + `source_figures`/`instance_figure_links` 只读计数。

---

## R1. 表格结构问题拆分（Q9 / Q19 / Q24 / Q25）

**更正 Phase B 表述**：不得统一称为「表格选项切分问题」。四题结构语义不同。

### Q9 — 文本标签行 + 图像行（列对齐）

| 项 | 内容 |
|---|---|
| **原始 HTML** | L51，`<table>` 2×4：行1 `A. 青铜器皿` / `B. 陶瓷` / `C. 丝绸` / `D. 中草药`；行2 四个 `<img>`（`img_in_image_box_157…` 等） |
| **Producer manifest** | `options_lines=[51,51]` 单行；无 per-label span；无 figure 绑定 |
| **丢失结构** | ① label→文本 映射；② label→图像 的**列对齐**关系；③ 图序 = 选项序 |
| **预期输出** | `option[label].text` + `option[label].figure_ref`（列序绑定） |
| **可能波及** | 其他「文+图」选择题（Q20 有图但非本表） |
| **回归验收** | 四选项 text 与 img 一一对应；图序不乱；Q9 其余题不受影响 |

### Q19 — 列头 A/B/C/D + 实验数据矩阵

| 项 | 内容 |
|---|---|
| **原始 HTML** | L145，`<table>` 3×5：行1 空格 + `A|B|C|D`（**列头**）；行2 `t/°C` + 10/10/40/40；行3 `c(H2SO4)` + 1/3/1/3 |
| **Producer manifest** | `options_lines=[145,145]` |
| **丢失结构** | 每选项 = **一列的条件向量**（温度+浓度），不是独立文本行 |
| **预期输出** | `option[label] = {t, c(H2SO4)}` 或保留表格 + label 列索引 |
| **禁止** | **不得**把各列拍成普通「A. …」文本选项（会丢矩阵语义） |
| **可能波及** | 一切「列=选项」的数据表题 |
| **回归验收** | 列头顺序 A–D 与数据列一致；单元格公式保留 |

### Q24 — 图形/公式引用行 + 文字选项行

| 项 | 内容 |
|---|---|
| **原始 HTML** | L199，`<table>` 2×4：行1 `[F4][F3][F5][F2]`（图形/公式引用）；行2 `A. 收集氯气` … `D. 配制…NaCl` |
| **Producer manifest** | `options_lines=[199,199]` |
| **丢失结构** | **图↔选项列对应**；F 编号与 A–D 顺序绑定 |
| **预期输出** | `option[label].text` + `option[label].figure_ref`（同 Q9 列对齐） |
| **可能波及** | 装置图选择题 |
| **回归验收** | F4↔A、F3↔B、F5↔C、F2↔D 不错位 |

### Q25 — 行标识 A–D + 多列内容组合

| 项 | 内容 |
|---|---|
| **原始 HTML** | L204，`<table>` 5×3：表头 `选项|实验操作及现象|推理或结论`；行 A–D 各含 label + 操作 + 结论（含 LaTeX） |
| **Producer manifest** | `options_lines=[204,204]` |
| **丢失结构** | **行级选项**；每选项 = 操作列 + 结论列的**组合**，不能拆成两个独立选项 |
| **预期输出** | `option[label] = {operation, conclusion}` 复合结构 |
| **可能波及** | 多列表格式选择题 |
| **回归验收** | A–D 行完整；两列不被拆成 8 个假选项 |

**R1 小结**：Q9/Q24=列对齐（文本/图）；Q19=列向量矩阵；Q25=行复合。共性仅是「HTML table」，**数据结构要求互不相同**。

---

## R2. 题号锚点与分节作用域（U-req1–6 等）

### 事实（证据）

| 字段 | U-req1 | 印刷 |
|---|---|---|
| manifest `question_numbers` | **[26]** | — |
| manifest `printed_number` | **[1]** | L210 `1. （3分）…` |
| annotation `question_label` | **26** | — |
| 补跑 Resolver | `question number '26' not found` | stem 文本实际存在 |

同理 U-req2–6 → 全局 27–31 / 印刷 2–6。U-org/U-cp 印刷 1–3 与 Q1–Q3、U-req1–3 **分节重号**（manifest warnings 已载）。

### 冻结约束（Phase C 不得违反）

1. **全局题号、印刷题号、Producer unit_id 为三个不同身份字段，禁止混用。**  
2. 印刷题号解析必须带 **可验证 section 作用域**（如 `必答题/26` vs `选择题/26`）。  
3. **禁止**无作用域全局字符串搜索或 printed number 裸匹配来定答案行。  
4. 分节/题号映射歧义 → 必须停在 **ambiguous / pending**，禁止猜测绑定。  
5. U-org1–3、U-cp1–3 印刷 1–3 与 Q1–Q3 重复 → **回归碰撞用例**（改锚点后 Q1–Q3 不得错绑）。  
6. **Resolver/Gate 题号逻辑变更不得混入 Producer 首轮修复。**

**本任务不修改 Resolver。**

---

## R3. U-org / U-cp 复合根因

| 因素 | 证据 | 判断 |
|---|---|---|
| **A. 输入证据缺失** | manifest `validation_issues`：6 条「无 answer_lines」；annotation `answer.answer_lines` 为 **null** | **已证实** |
| **B. 跨节匹配歧义** | 若按印刷题号 1–3 找答案，选择题答案表、必答题、模块题均有「1.」→ 多行歧义 | **候选（结构上必然，未跑证）** |
| **C. 处置** | 见下 | 待 Owner |

**明确**：现有证据**不能**证明「只补 answer_lines」或「只修 Resolver」单一因素即可通过。二者可能叠加。

**禁止**：为消 skip 而生成答案；不得把无答案证据的题自动转为可入库。

**处置选项（Owner 裁决）**：

1. 人工补 answer_lines（精确行区间）→ 再评估；  
2. Producer 标记 `answer_zone=absent` + 保留 pending_review；  
3. 保持 skip，计入「输入缺陷」清单。

---

## R4. U-cl2 两个独立因素

源文 L570–572：

```
2.（8分，每空2分）          ← 评分表头
（1）对 （2）对 （3）对 （4）对   ← 四个独立对/错
```

| # | 因素 | 证据 | 单独修复能否通过 |
|---|---|---|---|
| 1 | **answer span 含评分表头** `2.（8分，每空2分）` | answer_lines=[570,572] 含表头行 | **不能预设** — 清表头后仍为「对 对 对 对」多值 |
| 2 | **canonical `true_false` 无法表达四空复合** | 题型=true_false；Gate：`answer not expressible as canonical value` | 清表头仍不能 canonicalize |

**只读判别法**（Phase C 前可做，不改代码）：

1. 人工检查 answer_lines 去掉 L570 后剩余是否仍多值 → 若是，因素 2 主导。  
2. 对比同卷其他 true_false 是否单值 → 若是，支持「题型误标」而非 grammar 全局缺陷。  
3. Gate reason 含 `canonical value` 而非 `grammar None` → 已排除「无 grammar」路径。

**必须保留人工审核的情形**：多空对/错、复合判断、answer 含表头且无法唯一 canonical。  
**不得**仅因清了表头就批准 auto_approve。

---

## R5. 用户反馈驱动的字号差异候选

### 反馈原文（库内 `f335fd96`）

> 「字号大小好像不太一样，A选项的HCL明显比其他选项的字号小一圈」  
> category=`latex_render_error`，指向真实 Q8 `5f461ef4`。

（任务书写「大/不一致」；**以库内原文「小一圈」为准**。）

### 已知候选机制（登记，不改代码）

| 选项 | 内容 | 渲染路径 |
|---|---|---|
| A | ` HCl` | 纯文本 → 普通 `<span>` |
| B | ` $CO_{2}$` | KaTeX `.katex` |
| C | ` $MgCl_{2}$` | KaTeX |
| D | ` $CH_{4}$` | KaTeX |

### 必须分开验证的两件事

1. **公式是否成功渲染**（B/C/D 下标正确）— 已在 M3a 验证。  
2. **纯文本 vs KaTeX 的字号、基线、行内对齐是否一致** — **未验证**；`.katex` 节点计数 **不构成验收**。

### 候选缺陷登记（不实施）

- ID 建议：`M3C-FE-001`（前端字号/基线）  
- 涉及：`MathText.tsx`、KaTeX CSS、行内 `vertical-align` / `font-size`  
- **禁止**本任务修改上述文件或公式分隔符。

### 未来验收条件

同一题同一行内 **A（纯文本）与 B/C/D（数学）并排截图**；测量 font-size / baseline；仅 `katex` 节点数不通过。

---

## 反馈记录计更正

**实时只读查询**（`aitutors_test`，本补记执行时）：

| ID | 来源 | 类别 | 描述摘要 |
|---|---|---|---|
| `50a38c8b-…` | E2E（M3b） | latex_render_error | 选项B/C/D公式下标显示异常（E2E验收） |
| `880b092a-…` | E2E 重复（Phase A 复验） | latex_render_error | **同文** |
| `f335fd96-…` | **用户真实提交** | latex_render_error | 字号…A选项的HCL…小一圈 |

**总数 = 3**（2 条同文 E2E + 1 条真实用户反馈）。  
**未删除/未更新/未重建任何记录。** 与上轮「2 条」的差异原因：Phase A 后用户又提交了 `f335fd96`。

---

## Phase C 前置条件（提出，不实施）

**最小实施顺序：**

1. **Papers Producer**：表格结构表达（R1 四型）+ 题号身份/作用域（R2）；  
2. **独立实验库**同卷回归（非 `aitutors_test`）；  
3. 核对 Producer 输出与原卷结构一致（表格语义、图选项绑定）；  
4. 再评估是否单改 **Resolver**；  
5. 最后评估 **U-cl2** 题型/Gate 语义；  
6. **MathText 字号**作为独立前端缺陷，不与 Producer 结构修复捆绑。

**成功标准（禁止唯数量论）**：

- 不以「恢复 21 题」为唯一标准；  
- 要求：结构保真、身份不串题、既有 21 题回归不破坏、skip 有据可查。

---

## Phase C 前仍需 Owner 裁决

1. R1：表格四型的**预期数据结构**是否按本补记冻结（尤其 Q19 列矩阵禁止拍成文本选项）。  
2. R2：是否批准「printed + section 身份三字段分离」为契约约束。  
3. R3：U-org/cp 走人工补答案 / absent 标记 / 保持 skip？  
4. R4：U-cl2 是改题型、扩展 grammar，还是强制人工？  
5. R5：字号问题是否立独立前端缺陷单。  
6. 重复 E2E 反馈 `880b092a` 是否标注「复验重复」。  
7. 是否授权 Phase C 仅动 Papers Producer（Resolver/Gate 另批）。

---

**补记完成，停止。等待 Owner 审阅；不宣称 Phase C 已授权。**

---
---

# Phase B-R1-O1–O3 — 最终实施前置条件补记

**追加时间**：Phase B-R1 之后（不覆盖上文 R1–R5 结论）。  
**基线核实**：AITutors-v3 `9a4bfb7c87bd5fa2e8173374b2780b3663568631` · Papers `b141bfda9a4bb5037adfe06fab8f8f75b096dc75` · AITutor-X `7bce066` — **与预期一致**。  
**新证据**：`PHASE-B-R1-O1O3-EVIDENCE.json`；图像路径只读探测；`aitutors_test` 表计数只读。

---

## O1. Q9 图像资源闭环

### 已核实事实

| # | 事实 | 证据 |
|---|---|---|
| 1 | Q9 表格第二行含 **4 个** `<img>` 引用 | `paper.md` L51 表 HTML |
| 2 | 四图 src 均指向 `../../_imgs/2018北京春季高中会考化学（教师版）(1)/img_in_image_box_*.jpg` | 同上 |
| 3 | 库内 **`source_figures = 0`**、**`instance_figure_links = 0`** | 只读 count |
| 4 | M1 配置包仅有 `paper.pdf / paper.md / manifest.json / PAIRING_EVIDENCE.json`，**无 `_imgs/`** | 包目录清单 |
| 5 | 四个 jpg **实际存在**于 `Papers/Ocr-markdown/_imgs/…` 与 `…/resliced-pilot/_imgs/…`（各 2 处） | `rglob` 命中 |
| 6 | `paper.pdf` 含 **47** 张嵌入图（p2:12, p3:7, p4:3, p5:1, p8:20, p9:1, p10:3） | PyMuPDF `get_images` |
| 7 | **Q9 四图与 PDF xref 的身份对应关系未建立** | 无 pairing 记录 |

### 模型约束（只读）

- `source_figures`：`figure_id`（version 内 UNIQUE）+ `page_no`/`bbox`/`placement`/`source`/`object_key`/`figure_hash`；**无选项/题号归属字段**。  
- `instance_figure_links`：复合 PK `(instance_id, source_figure_id, role, order)` — 可表达「选项 role」绑定，但**当前无数据**。  
- Producer artifact（manifest）**未定义**图像资源传输通道；`figure_ref` 目前 **无可证明可解析的目标资源**（包内无图）。

### 尚待 Owner 决定的方案（本任务不选定）

1. **图像随 Producer artifact 一并交付**（包内含 `_imgs/` + 身份清单）；  
2. **走已存在且可验证的图像资源通道**（如 source_figures 从 PDF 抽取 + pairing）；  
3. **契约暂不支持图像传输时**：将 Q9 标记 **资源缺失/待处理**，不产生悬空 `figure_ref`。

### Q9 后续验收条件

- 四选项标签与原始图像的**顺序与列对应**可验证；  
- 资源**实际存在且可解析**（object_key/figure_hash 可回指）；  
- 否则明确报告缺失 — **禁止**将空 `figure_ref` 当作成功。

---

## O2. printed_number = NULL 分支

### NULL 分布（manifest 实测）

| unit_id | printed_number | question_numbers | section 线索 |
|---|---|---|---|
| Q1 | **NULL** | [1] | 第一部分 选择题 |
| Q9 | **NULL** | [9] | 同上 |
| Q13 | **NULL** | [13] | 同上 |
| Q14 | **NULL** | [14] | 同上 |
| Q15 | **NULL** | [15] | 同上 |
| Q18 | **NULL** | [18] | 同上 |
| Q19 | **NULL** | [19] | 同上 |

共 **7** 个；其余 33 个 units 的 printed_number 非 NULL。  
身份字段现状：manifest 同时有 `unit_id` / `question_numbers` / `printed_number`；annotation 使用 `question_label`（多为全局号）。

### 冻结实施约束

1. **全局题号、印刷题号、`unit_id` 为不同身份字段，禁止混用。**  
2. `printed_number = NULL` 时，**禁止**对 NULL 做题号检索或推导题号。  
3. 仅当来源身份 + section 作用域 + 匹配证据**唯一**时，才允许其他证据绑定。  
4. 不能唯一确定 → 保持 **unresolved / ambiguous / pending**，禁止猜测。  
5. **Q9、Q19** 同时属表格结构问题与 printed NULL 集合 → **只记为两个待检验关联因素**，不预设共同根因。  
6. 回归必须覆盖：**有 printed / 无 printed / 跨 section 重号 / 题号冲突** 四类。

本轮 **不修改 Resolver**，不制定无来源证据的回退算法。

---

## O3. U-cl2 判别方法修订

### 修订：删除不可执行步骤

原 Phase B-R1 R4 判别法中「与本卷其他 true_false 题比较」**不可执行** — 实测 `original_question_type == "true_false"` 的 units **仅 U-cl2 一道**。该步骤应从验收步骤中**删除**。

### 事实（只读）

| 项 | 值 |
|---|---|
| U-cl2 answer_lines | **[570, 572]** |
| span 内文本 | `2.（8分，每空2分）` + 空行 + `（1）对 （2）对 （3）对 （4）对` |
| options_lines | **null** |
| 本卷 true_false 数量 | **1**（仅 U-cl2） |
| U-cl1 / U-cl3 | fill_in / short_answer，options_lines 同为 null |

### 三独立维度（事实 ≠ 因果已证）

| 维 | 描述 | 现存证据 | 可验证影响 | 仍未知 |
|---|---|---|---|---|
| **A** | 答案 span **混入评分表头** `2.（8分，每空2分）` | L570 落在 answer_lines 内 | 去表头后 span 是否仍非单值 | 去表头后 Gate 是否仍 fail |
| **B** | 四个「对/错」子项 **超出单值 `true_false` canonical** | 题型=true_false；答案四元组 | canonical 无法表达 → pending | 是否应改题型或扩展 grammar |
| **C** | **`options_lines` 缺失** 使选项/子题结构未表达 | manifest `options_lines=null` | 子问（1）–（4）无独立结构位 | 缺 options 是否导致/加重 A/B |

**禁止**：将 A/B/C 直接认定为三个已证实根因。  
**跨卷比较**：需**另一份真实样本**；获得后单独验证。本任务不构造样本、不调 LLM、不重跑管线。

### 何时必须保留人工审核

- 多空对/错、复合判断；  
- answer 含表头且无法唯一 canonical；  
- options_lines 缺失且子题结构未声明。

---

## 副作用声明（实际变化）

| 项 | 变化 |
|---|---|
| 代码 / 配置 / Frozen Spec / 测试 | **无** |
| 数据库写入 / 删除 / 迁移 / TRUNCATE | **无**（仅只读 count） |
| LLM / 题目处理管线 | **无** |
| 反馈记录 | **无**（未删/未改/未重建） |
| 分支 / 提交 / 推送 | **无** |
| 文档 | **仅追加**本补记 + 新建 `PHASE-B-R1-O1O3-EVIDENCE.json` |

---

## 需 Owner 裁决（O1–O3）

1. **O1**：Q9 图像走「artifact 附带 `_imgs/`」/「source_figures 通道」/「标记资源缺失」三者之一？  
2. **O2**：printed NULL 的 7 题是否冻结为「禁止 NULL 检索 + 必须 section 唯一」契约？  
3. **O3**：U-cl2 优先清理 A（表头）还是改 B（题型/grammar）？C 是否单列？  
4. 是否授权 Phase C **仅动 Papers Producer**（Resolver/Gate 图像与题号另批）。

**补记 O1–O3 完成，停止。不进入 Phase C。**

---
---

# O2 根因证据补记（Owner 裁决后追加）

**依据**：DSH 发现 7 个 printed_number=NULL 与 OCR 转义题号 `\.` 及 Producer provenance 吻合。

## 事实

1. **7 个 NULL 单元 stem 均为转义点形式**（实测 paper.md）：
   - Q1 `1\. 2017年…`、Q9 `9\. 丝绸之路…`、Q13 `13\. 下列营养物质…`
   - Q14 `14\. 下列属于取代反应…`、Q15 `15\. 下列方法…`、Q18 `18\. 下列事实…`、Q19 `19\. 控制变量…`
2. **非 NULL 对照**：Q2/Q8 为全角 `2．`/`8．`，Q10 为半角 `10.` → `printed_number` 非空、`basis=printed_as_is`、`printed_provenance=source_line`。
3. **抽取路径**：`question_identity.PRINTED_LINE` 覆盖 `.` `、` `．`，**不覆盖**转义 `\.`。`phase2_identity_backfill.printed_from_stem` 依赖该正则 → 匹配失败返回 `(None, "unknown")` → `basis=unverified`。
4. **7 个单元** `printed_provenance=unknown`、`basis=unverified`（manifest 实测）。
5. **section 已存在**：manifest 含 `section` / `section_ref`，本次修复**不需要另造 section 身份**。
6. **U-org1** 等为 `migration_report / keep` 路径，**不应**误归为抽取器例外。

## 首个修复点（Phase C #1）

- 修 `PRINTED_LINE`（或等价 Producer 抽取）以接受可选转义反斜杠 `\?`（与 `r55_r45_audit.NUM_PREFIX` / `_NUM_PREFIX` 已知正确写法对齐）。
- 补齐 provenance：目标单元从 `unknown/unverified` → **`source_line` / `printed_as_is`**。
- 建立 7 个 NULL 单元的回归测试。
- 验证 **section 作用域与重号不受影响**（U-req/U-cl/Q1-3 分节同号仍分离）。

## 回归验收条件

| 条件 | 要求 |
|---|---|
| 身份字段分离 | 全局题号 / 印刷题号 / unit_id / section 仍为独立字段 |
| 7 单元 provenance | `unknown`→`source_line`（有源行证据） |
| basis | `unverified`→`printed_as_is`（或保持可溯源的 keep/migration 路径） |
| 重号 | 选择题 1 与模块题 1 的 keep 豁免语义不变 |

**本补记完成即不再开独立全仓库审计。**
