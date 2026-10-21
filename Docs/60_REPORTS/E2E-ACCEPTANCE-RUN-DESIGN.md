# 9 科正式 E2E Acceptance Run — 设计 + 第 0 轮取证结果

> DSH 记录 + 只读取证。**未改动任何代码 / 数据 / Schema / Gate / DB。**
> Owner 方案：把「重新跑一遍」正式定义为 **E2E Acceptance Run**（三个 Gate：
> Preprocessing / V3 / Attribution），语料固定为 9 科各 1 份原始 PDF，产物封存。
> 本文件先交付**可行性 + 语料定义 + 第 0 轮（PDF→Preprocessing）真实结果**。

---

## 0. 本轮最重要的发现：**原始 PDF 有文本层，真值可直接取得**

`fitz`（PyMuPDF）可用，三份焦点卷 PDF **均有可提取文本层**：

| 卷 | 页数 | 文本层字符数 |
|----|------|-------------|
| 数学（春季会考） | 15 | 9,962 |
| 化学（春季会考） | 12 | 8,402 |
| 历史（夏季会考） | 23 | 18,279 |

⇒ **不需要人工逐页比对**：Owner 只需对**已被机器定位到具体行**的少数位置做判定。
这把第一验收点的成本降低了一个数量级。

---

## 1. 语料来源已闭合：正式 preprocessing 产物 = 已验收产物，且 V3 消费的就是它

### 1.1 正式链路径（从代码读出，非推测）

```text
ocr_service/batch_convert_pdf.py
   PDF_ROOT    = D:\Project\Papers\maintainess\PDF        ← 原始 PDF（12,707 份）
   OUTPUT_ROOT = D:\Project\Papers\Ocr-markdown           ← 正式 OCR 产物
   MODEL       = "PaddleOCR-VL-1.6"    (外部 API: paddleocr.aistudio-app.com)
   MANIFEST    = D:\Project\Papers\data\ocr_output_manifest.jsonl   ← 输出清单
```

清单每条含：`source_rel / source_size / source_sha256 / output_rel / written_at / pages`。
且其语义被 governance 明确限定为 **execution ledger（已执行过一次）**，
**不是 output availability index**；且**禁止 runner 自动重跑**（R-OHM-1，防"跑步机"回流）。

### 1.2 9 科语料独立核验：**9 / 9 通过**

`_e2e_acceptance_provenance.py`：原始 PDF 的 `sha256` 与 ledger 记录**逐份相符**，
输出 `.md` 全部存在，且**全部不带行号前缀**（`line_numbered = 0 / 9`）。

| 科目 | 原始 PDF | 源 PDF sha256（ledger == 实际 ✅） | 页 | 输出 .md sha256 |
|------|----------|-----------------------------------|----|----------------|
| 语文 | 2018北京春季高中会考语文（教师版）(1).pdf | — | — | — |
| 数学 | 2018北京春季高中会考数学（教师版）(1).pdf | `3b87f19f…` ✅ | 15 | `934dec78…` |
| 英语 | 2018北京春季高中会考英语（教师版）(1).pdf | — | — | `8dc9afbc…` |
| 物理 | 2018北京春季高中会考物理（教师版）(1).pdf | `98bcc618…` ✅ | 9 | `81ea9b74…` |
| 化学 | 2018北京春季高中会考化学（教师版）(1).pdf | `8d3f9dad…` ✅ | 12 | `0443945f…` |
| 生物 | 2018北京春季高中会考生物（教师版）(1).pdf | `a8242fd3…` ✅ | 14 | `35e928c2…` |
| 政治 | 2018北京春季高中会考政治（教师版）(1).pdf | `a08604c3…` ✅ | 14 | `a7341fd0…` |
| 历史 | 2018北京春季高中会考历史（教师版）(1).pdf | `49bbd8ac…` ✅ | 23 | `0982ae9c…` |
| 地理 | 2018北京春季高中会考地理（教师版）(1).pdf | `96344286…` ✅ | 12 | `3f4a7a82…` |

（完整 10 位 sha 见 `_e2e_acceptance_provenance.json`。语文/英语 PDF 的 ledger 行亦在，
`schema` 相同；上表空格仅为省略显示。）

### 1.3 关键澄清：**V3 Phase 1 消费的 `.md` 就是正式 preprocessing 产物本身**

| 路径 | 首行 | 行号 | sha256 | 大小 |
|------|------|------|--------|------|
| `Ocr-markdown/会考/化学/…md`（**正式**） | `# 2018 北京春季高中会考…` | 无 | `0443945f…` | 31,777 |
| `Ocr-markdown/reslice-batch-C/会考/化学/…md` | `<!-- resliced by mimo-x-pro-preview … -->` | 有 `[Lnnnn]` | `22c8638b…` | 133,512 |
| `AITutor-X/e2e_run/…/reslice-batch-C/会考/化学/…md`（**V3 消费**） | `# 2018 北京春季高中会考…` | 无 | `0443945f…` | 31,777 |

⇒ **V3 Phase 1 的 `.md` 与"正式 preprocessing 产物"逐字节相同**（`0443945f…`）。
**此前称之为"实验变体语料"是不准确的**——`.md` 侧就是正式产物；
`reslice-batch-C` 那一份才是带行号的 reslice 中间形态，且**未被 V3 消费**。

（`reslice-pac-annotated/reslice-pac/ocr/pac-c01-01.md` 与 V3 语料同为 `L23`，
是另一条变体路径，同样保留。）

---

## 2. 第 0 轮取证：PDF → Preprocessing 真值对照（四题）

这是全链**从未被检查过**的一层。结果**逐题不同**，且**推翻了我此前的部分归因**。

| 题 | 原始 PDF 文本层（真值） | 正式 preprocessing `.md` | 判定 |
|----|----------------------|------------------------|------|
| **化学 Q23** | `…C．稀盐酸与碳酸钙：…` / `D．稀硫酸与氢氧化钡溶液：H⁺＋SO₄²⁻＋Ba²⁺＋OH⁻ === H₂O＋BaSO₄↓` | L192 `C．稀盐酸与碳酸钙：…` / **L194 `$ \mathrm{H}^{+} + \mathrm{SO}_{4}^{2-} + … $`（无 `D．`）** | ❌ **Preprocessing 丢了 `D．` 标签**（PDF 有，md 无） |
| **化学 Q20** | `D．硫在自然界的循环过程中，涉及了氧化 \n 还原反应` | L157 `D. …涉及了氧` / L159 `还原反应` | ✅ **Preprocessing 忠实**（PDF 此处本就换行；md 亦断行） |
| **数学 Q4** | `…C．关于直线y=x 对称2 D．关于直线y=﹣x 对称`（`对称` 与 `D．` 之间**确实有一个 `2`**） | L23 `C. 关于直线 y=x 对称 2D. 关于直线 y= -x 对称` | ⚠️ **Preprocessing 忠实**；**源 PDF 本身就含 `2`** |
| **历史 Q29** | `A. 迪亚士 / B. 达，伽马 / C. 哥伦布 / D 麦哲伦`（**README 印刷即无句点**） | L307 `D 麦哲伦` | ✅ **Preprocessing 忠实**（印刷即如此） |

### 2.1 本题最重要的两个归因修正

**(a) 化学 Q23：真正的首变点 = Preprocessing，且**不是**「label 与内容分离」而是「label 被剥离」**

PDF 里 `D．稀硫酸与氢氧化钡溶液：` 是**完整的带标签选项**；
md 里只剩**方程式正文**，标签与"稀硫酸与氢氧化钡溶液："这半句一并消失。
⇒ 这是 **preprocessing 的选项标签剥离缺陷**，V3 无过错。
**我此前称"L194 是源中裸内容行、label 从不存在"——以 PDF 为真值，该表述错误。**

**(b) 数学 Q4：源 PDF 本身就带 `2`，因此「确定性恢复 D」不可能成立**

PDF 文本层为 `C．关于直线y=x 对称2 D．关于直线y=﹣x 对称`：
`2` 位于 C 的内容与 D 的标签之间，**PDF 不提供任何信息判定 `2` 属于谁**。
⇒ 任何"正确取出 D"的实现都**必须依赖判断**，不是确定性解析。
**这从原始真值层面证实了我此前的质疑**，也说明 P1.4-B 的 Rule B 属于**歧义消解**而非兼容性修复。

### 2.2 责任矩阵（更新版，含 L0 真值）

| 题 | PDF 真值 | Preproc 输出 | V3 输入 | 首次变化层 | 最终表现 | 责任层 |
|----|---------|-------------|---------|-----------|---------|--------|
| **Q23** | 四选项完整，`D．` 在 | **丢 `D．` 标签** | 同 md | **Preprocessing** | 漏 D（P1.4-B 补 D 后 auto） | **Preprocessing** |
| **Q20** | `涉及了氧化` ⏎ `还原反应` | 忠实断行 | 同 md | **manifest/Rule A** | P1.4-B 造出假 option **E** | **P1.4-B（Rule A）** |
| **Q4** | 含 `2`，歧义 | 忠实 | 同 md | **manifest 漏 D → P1.4-B Rule B 补** | label-only D + C 被污染 | **源歧义 + P1.4-B 判断** |
| **Q29** | 印刷无句点 | 忠实 | 同 md | **manifest 漏 D → P1.4-B Rule C 补** | 仅完整性（本就 auto） | **Preprocessing 格式 + 恢复** |

**结论：四道题里有两道（Q23、Q29）的首变点在 Preprocessing，一道（Q20）在 P1.4-B，
一道（Q4）源本身歧义。没有任何一道的根因在 V3 的 Resolver/Compiler/Gate。**

---

## 3. E2E Acceptance Run — 设计（采纳 Owner 方案 + 三项增补）

### 3.1 目录与封存（采纳 Owner 第 4 节）

```text
E2E_ACCEPTANCE/
├── 01_INPUT_PDF/           原始 PDF（9 份）+ sha256
├── 02_PREPROC_OUTPUT/      机器产出（只读副本）
├── 03_OWNER_ACCEPTED/      Owner 判定为 PASS 的产物（**封存，逐字节冻结**）
├── 04_V3_INPUT/            从 03 复制而来的 V3 输入
├── 05_V3_OUTPUT/           Question / QuestionInstance / 前端快照
├── 06_ATTRIBUTION/         逐题首变点判定
└── MANIFEST.json           见 §3.2
```

**增补 1 — 封存用 SHA 清单而非"同一份文件"**：
`03_OWNER_ACCEPTED/` 必须落一份 `ACCEPTED.json`，记录每份产物的 sha256 +
Owner 判定 + 时间。V3 只读 `03`，并在入口校验 sha（不符即 fail-closed）。

**增补 2 — 必须记录"本次未重跑 OCR"**（见 §4 阻塞项 R3）：
本 Run 复用 ledger 中已存在的产物，因此 `MANIFEST.json` 要写明
`ocr_rerun = false` 与 ledger 的 `written_at`，避免下次再问"这份 MD 哪来的"。

**增补 3 — 第一验收点改为"定位式验收"**：
既然 PDF 有文本层，先跑一个**只读差分器**（PDF 文本层 vs 02 产物），
输出所有**不一致行**，Owner 只审这些行 + §3.3 的 C 类检查项。
不要把 9 份卷子整篇给 Owner 看。

### 3.2 `MANIFEST.json` 必录字段（采纳 Owner 第 2 节，落到实现）

```json
{
  "run_id": "...", "started_at": "...",
  "corpus": [{
    "subject": "化学",
    "source_pdf": "maintainess/PDF/2018北京春季高中会考化学（教师版）(1).pdf",
    "source_sha256": "8d3f9dad...", "source_size": 649356, "pages": 12,
    "preproc_commit": "<Papers SHA>", "preproc_model": "PaddleOCR-VL-1.6",
    "preproc_config": {...},
    "ocr_rerun": false,
    "ledger_written_at": "2026-09-13 21:40:50",
    "output_md": "Ocr-markdown/会考/化学/....md",
    "output_sha256": "0443945f...",
    "owner_decision": "pending | pass | fail",
    "owner_notes": []
  }],
  "v3": {"commit": "<AITutors-v3 SHA>", "entry": "document_ingest", "task_types": [...]}
}
```

### 3.3 第一验收点检查项（采纳 Owner 第 3 节 A–E，逐项可机器预筛）

| 组 | 检查项 | 可否机器预筛 |
|----|--------|-------------|
| A 题目边界 | 题号正确 / 一题被拆两题 / 两题粘一题 / 材料题完整 | 部分（题号序列连续性、跳号可机器查） |
| B 题干 | 缺字 / 乱序 / 跨页丢失 / 图片公式 / LaTeX | 部分（PDF↔md 文本差分可查缺字乱序） |
| **C 选项** | 完整 / 串题 / **跨行被误拆为新选项** / **`2D.` 粘连** / **label 与正文分离** | **可**（本轮已实现的原型即可） |
| D 答案 | 存在 / 与 PDF 一致 / 错位 | 可（答案表解析 vs PDF） |
| E 材料题 | 材料边界与子题归属 | 部分（子题号覆盖 + 材料区间） |

⇒ 建议把 C 组做成**常驻只读检查器**（即 Human Console 的机器前置层）。

---

## 4. 可行性评估：**部分可执行**，有 3 个阻塞项（交 Owner 裁决）

| # | 阻塞项 | 现状 | 影响 |
|---|--------|------|------|
| **R1** | **正式 V3 入口是否能吃"Owner 已验收的预处理产物"** | 正式链是 `TaskExecutor` / `document_ingest`（`Seal → Annotation → Compile`）。但 `preprocessing_consumer` 在 `scripts/`、`app/` 零引用；未找到「把 Papers 的 md/manifest 灌进正式 document_ingest」的入口 | **若无此入口，则 owner-accepted 产物无法进入正式链**，Gate 2 无法按正式语义执行 |
| **R2** | 数据库 / 前端 | `backend/.env` 有 `DATABASE_URL / MIMO_API_KEY / MIMO_BASE_URL / MIMO_MODEL / OCR_GATEWAY_MODE`；`AITutors-v3/frontend` 存在。但**本轮未连接 DB、未启动前端、未验证** | Gate 2 的"最终用户看到什么"未验证 |
| **R3** | OCR 重跑 | 正式 OCR 走**外部付费 API**（PaddleOCR-VL-1.6，日限 20,000 页）；且 governance（R-OHM-1）**禁止 runner 自动重跑**，重跑需人工删 ledger 记录 | 本 Run **不应重跑 OCR**；应复用 ledger 产物（已完成，§1.2 9/9） |

### 4.1 因此建议把 Run 拆成两个 Fork

```text
Fork 1 — 已完成（本轮，无需额外授权）
  PDF ──(已有 OCR 产物 + ledger sha 校验)──> 02_PREPROC_OUTPUT
        │
        └──> Owner 定位式验收 ──> 03_OWNER_ACCEPTED（封存）
   产出：语料定义 + 真值 + 首变点归因（本文档 §1、§2）

Fork 2 — 需要 R1/R2 裁决后才能跑
  03_OWNER_ACCEPTED ──> 【正式 V3 入口？】 ──> DB/QI ──> 前端 ──> Owner 验收
   缺口：入口未确认（R1）、DB/前端未验证（R2）
```

**给 Owner 的最小裁决问题**：
> `03_OWNER_ACCEPTED` 应该通过**哪个入口**进入 V3？
> (a) 正式 `TaskExecutor`/`document_ingest`（需要"外部 manifest 注入"能力——目前未见）
> (b) 现有的 `scripts/preprocessing_consumer/runner*`（但它是 `phase0` 实验路径，
>     且按上轮结论**不读 Papers manifest**，语义不同）
> (c) 新增一个正式的 "preprocessing artifact ingest" 入口（需立项）

---

## 5. 保持不变（已遵守）

- `ec62d29` / `d42cde6` **继续冻结**，未回滚、未继续修 Rule A/B/C、未修 Q20/Q4
- 未修改任何生产代码 / manifest / 语料 / Schema / Gate / Decomposition / DB
- 未重跑 OCR（R3）

---

## 6. 本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `_e2e_acceptance_provenance.py` / `.json` | 9 科语料 provenance 核验（源 PDF sha 与 ledger 逐份相符，9/9） |
| `_e2e_pdf_ground_truth.py` / `.json` | 原始 PDF 文本层提取与焦点模式命中 |
| `Docs/60_REPORTS/P1.4-E2E-TRACE-MIMO-REPORT-REVIEW.md` | 上轮 MIMO 报告审查 |
| `Docs/60_REPORTS/P1.4-E2E-TRACE-INDEPENDENT-VERIFICATION.md` | 上轮独立追踪 |
