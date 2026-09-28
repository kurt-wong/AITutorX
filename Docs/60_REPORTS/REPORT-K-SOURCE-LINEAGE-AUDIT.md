# REPORT-K — SOURCE-LINEAGE-AUDIT

> **Role**: Independent Evidence Auditor（Governance Foundation Phase 0）
> **Scope**: Source Data Lineage Verification only
> **Question**: preprocessing 项目实际使用的原始试卷来源是什么？
> **Date**: 2026-09-17（取证时点；maintainess 误删文件已由 Owner 恢复后复测）
> **Repositories observed**: Governance `D:\Project\AITutor-X` · Consumer `D:\Project\AITutors-v3` · Producer `D:\Project\Papers`（remote = `kurt-wong/Aitutors-preprocessing`）
> **Hard restrictions honored**: 未修改任何既有仓库文件；未迁移；未创建 DEC/BUG/OQ；未改 Contract/Design；未提交 git。
> **Output discipline**: 每条结论标注 `OBSERVED FACT` / `INFERRED POSSIBILITY` / `UNKNOWN` / `OWNER DECISION REQUIRED`；无证据处写 `NOT VERIFIED`。
> **Temporal Scope**: This report reflects repository state as of 2026-09-17. Subsequent commits have not been re-audited. Findings are as-of that date and are retained as historical audit artifacts; they are not current-state authority.

---

## 1. Executive Summary（只列 Confirmed Facts）

1. **OBSERVED FACT** — Producer 本地路径为 `D:\Project\Papers`，remote `https://github.com/kurt-wong/Aitutors-preprocessing.git`，HEAD `2b92898f05f6541a5fc65c8300cb8a59a06c4928`，branch `main`，与 `origin/main` 一致。
   - Evidence: `git rev-parse HEAD`；`git status -sb`；`git remote -v`。

2. **OBSERVED FACT** — 存在两套大体量语料树，均 **不在 git**：
   - `original/`：69,535 文件，115G，`git ls-files original` = **0**
   - `maintainess/`：24,892 文件，46G，`git ls-files maintainess` = **0**
   - `Ocr-markdown/`：52,003 文件，1013M，`git ls-files Ocr-markdown` = **0**
   - Evidence: `find`/`du`/`git ls-files`；`.gitignore:7-10` 明确 `/original/`、`/maintainess/`、`/Ocr-markdown/`；`git check-ignore -v` 三者命中。

3. **OBSERVED FACT** — 恢复后 `maintainess/PDF` = **12,707** 个 `.pdf`（21G）；`original` 树 PDF = **38,893**。
   - Evidence: `find maintainess/PDF -type f -iname '*.pdf' | wc -l` → 12707；`find original -iname '*.pdf'` → 38893。
   - 与 Papers 历史文档数字一致：`production_adversarial_corpus_design.md:29` / `log.md:871` 记 `maintainess\PDF` = 12,707；`log.md:871` 记 `original` PDF 38,893 / DOCX 30,254 / DOC 207 / PPTX 164（本轮实测 original：PDF 38893 / DOCX 30254 / DOC 207 / PPTX 164，**与台账数字一致**）。

4. **OBSERVED FACT** — 现行 OCR/preprocessing **生产代码硬编码输入根**为 `maintainess\PDF`，不是 `original\`。
   - Evidence: `ocr_service/batch_convert_pdf.py:55` `PDF_ROOT = r"D:\Project\Papers\maintainess\PDF"`；`ocr_service/batch_convert_pdf.py:56` `OUTPUT_ROOT = ...\Ocr-markdown`。
   - 同类硬编码：`scripts/pac_select.py:28`、`scripts/pdf_fidelity.py:20`、`scripts/r64_data_inventory.py:42`、`scripts/r65_r64_review.py:36`、`scripts/r66_1_preflight.py:21`、`scripts/r67_manifest_bootstrap.py:48`、`scripts/r67_apply_gate.py:35`、`scripts/r67_apply_verify.py:21`、`scripts/recover_images.py:40`、`tests/test_r67_bootstrap.py:25,405`。

5. **OBSERVED FACT** — 现存 OCR 批处理日志记录的首次大规模执行时间为 **2026-09-06 10:42:46**，扫描「根目录PDF文件 12528 / 共发现 12703 个PDF文件」。
   - Evidence: `logs/ocr_batch_log.txt` 首段；当前 `maintainess/PDF` **根层扁平 PDF = 12,528**、全树 12,707（与日志 12528/12703 同量级，差额 +4 属后续变动，**具体增减清单 NOT VERIFIED**）。

6. **OBSERVED FACT** — git 历史**晚于**首次 OCR 日志：仓库首个 commit = `85784a9ace132d9043edf112d6bdc49ee40fa962`，`R25: 重切流水线 v2.1 全量就绪`，时间 **2026-09-12 10:11:06 +0800**；`ocr_service/batch_convert_pdf.py` 在该 commit 以 `PDF_ROOT=maintainess\PDF` **首次入库**。
   - Evidence: `git log --reverse`；`git log --diff-filter=A -- ocr_service/batch_convert_pdf.py`；`git log -S 'maintainess' -- ocr_service/batch_convert_pdf.py` 仅见 R25 初始引入。

7. **OBSERVED FACT** — 两树存在高重名重叠：`maintainess/PDF` 唯一文件名 12,707；与 `original` PDF 文件名交集 **12,626**；maintainess 独有 81；original 独有 26,187。
   - Evidence: 本轮 Python basename 集合运算（命令结果）。

8. **OBSERVED FACT** — 抽样 6 组同名 PDF 在 `maintainess/PDF` 与 `original/` 的 **sha256 完全一致**（6/6 match，0 mismatch）。其中 `2018北京春季高中会考化学（教师版）(1).pdf` 两侧 sha256 均为 `8d3f9dad0918567b3ef375a57843d5d28d1eff77dfac467ff9eddc0f3c4f3a23`，且与 `data/ocr_output_manifest.jsonl` 中该条 `source_sha256` 一致。
   - Evidence: 本轮 Python 哈希对账；`data/ocr_output_manifest.jsonl` 条目 `source_rel/source_sha256/source_size=649356/output_rel=会考/化学/...md`。

9. **OBSERVED FACT** — 接口面 manifest 的身份字段钉的是 **OCR 源 markdown 字节**，不是 PDF 字节。
   - Evidence: `Ocr-markdown/reslice-batch-C/会考/化学/2018北京春季高中会考化学（教师版）(1).manifest.json`：`source_file = D:\Project\Papers\Ocr-markdown\会考\化学\....md`，`source_content_sha256 = 0443945f4672b05da3d2d950b0a3eb20a495c1635c353c024c8c050b7fad1ffb`，`identity_version = 2`；对该 md 现算 sha256 = 同值（match True）。
   - `data/interface_scope_snapshot_step1.json` `identity_definition` 字面为 `SHA256(original source bytes), 64 lowercase hex`，但 snapshot 行的 `source_file` 指向 Ocr-markdown md，`source_content_sha256` = md sha。
   - Papers DQ 报告已写明两层 sha 语义不同：`Docs/COORDINATION/EVIDENCE/PREPROCESSING-DATA-QUALITY-REPORT.md:69-78` — OCR 清单钉 **PDF**，IR/接口面钉 **OCR md**；manifest 自身 0/166 携带 sha（本轮复核：166 份 manifest **全部**有 `source_file`，仅 **87** 份含任一 sha 键）。

10. **OBSERVED FACT** — AITutorX 现有报告中 **不存在 REPORT-J**；`Docs/60_REPORTS/` 仅 REPORT-A~I。
    - Evidence: `Glob Docs/60_REPORTS/REPORT-*.md`；目录列表。

11. **OBSERVED FACT（会话过程，非仓库终态）** — 本轮审计中途曾测得 `maintainess/PDF` 仅 6 个文件；Owner 声明为误删除并已完成恢复。恢复后复测 = 12,707 PDF。**该 6 文件观测不得当作语料现实写入治理结论。**

---

## 2. Source Corpus Reality

### 2.1 PAPERS-DIRECTORY-INVENTORY（Part 1）

取证命令：`find` 计数 + `du -sh` + `git ls-files`（时点：恢复完成后，HEAD `2b92898`）。

| Path | Type | File Count | Size | Git tracked | Role（禁止按名推断；下栏为证据类型） |
|------|------|------------|------|-------------|--------------------------------------|
| `original/` | directory | 69,535（PDF 38893 / DOCX 30254 / DOC 207 / PPTX 164） | 115G | **0** | **OBSERVED**: 大体量原始资料树；子目录含 `五三资料/高一/高二/高三`。文档称「原始资料」（`README.md:20`,`prd.md:125`）。**生产 OCR 代码未把它设为 PDF_ROOT**。 |
| `maintainess/PDF` | directory | **12,707**（全部 `.pdf`） | 21G | **0** | **OBSERVED**: 现行 OCR/多脚本硬编码输入根；结构以根层扁平为主（12,528）+ 少量子目录。 |
| `maintainess/DOCX` | directory | 12,142 | 25G | **0** | **OBSERVED**: DOCX 体量区；现行 OCR 服务不读此路径（`batch_convert_pdf.py` 只扫 PDF）。 |
| `maintainess/待转换DOC` | directory | 38 | 78M | **0** | **OBSERVED**: 小体量；用途 **UNKNOWN**（仅目录存在）。 |
| `maintainess/质量测试` | directory | 5 | 5.7M | **0** | **OBSERVED**: 5 文件；用途 **UNKNOWN**。 |
| `maintainess/test_output` | directory | 0 | 0 | **0** | **OBSERVED**: 空目录。 |
| `maintainess/`（合计） | directory | 24,892 | 46G | **0** | **OBSERVED**: 混合资产区（见 Part 5）。 |
| `Ocr-markdown/` | directory | 52,003（`.md` 全树 6,114；源树口径约 4,224；`.manifest.json` **166**） | 1013M | **0** | **OBSERVED**: OCR 与批注产物区；`Ocr-markdown/README.md` 自述「PDF → OCR Markdown 转换产出区」。 |
| `data/` | directory | 204 | 146M | **193** | **OBSERVED**: 大量审计/接口 JSON 工件入 git；含 `ocr_output_manifest.jsonl`（1,801 行）、`interface_scope_snapshot_step1.json` 等。 |
| `ocr_service/` | directory | 9 | 77K | **6** | **OBSERVED**: OCR 服务代码。 |
| `scripts/` | directory | 116 | 1.7M | **76** | **OBSERVED**: 流水线/审计脚本。 |
| `_archive/` | directory | 4,012 | 1.6G | **0** | **OBSERVED**: 归档区（含 `2026-09-10_Ocr-markdown清理/` 等）。 |
| `preprocessing outputs` | 非单一路径 | — | — | 混合 | **OBSERVED**: 主输出落在 `Ocr-markdown/`（md/manifest/`_imgs`）+ `data/`（清单与接口工件）+ `logs/`。**不是**独立名为 `preprocessing_outputs` 的目录。 |

### 2.2 原始来源回答

**问题**: preprocessing 实际使用的原始试卷来源是什么？

| 候选 | 判定 | 证据层级 |
|------|------|----------|
| `D:\Project\Papers\maintainess\PDF` | **OBSERVED FACT：现行生产 OCR 输入路径（operational input）** | 硬编码 `PDF_ROOT` + OCR 日志 12,703 扫描量 + 恢复后 12,707 在位 |
| `D:\Project\Papers\original` | **OBSERVED FACT：更大体量原始资料库；与 maintainess/PDF 高重名重叠（12,626），抽样字节一致；部分后置审计脚本改在 original/ 检索源 PDF** | basename 交集 + 6/6 sha match + `dq_data_quality_scan.py:268-270` + `PREPROCESSING-CLOSURE-PLAN.md:75,81` |
| 二者关系（谁拷到谁、是否同一采集批次） | **UNKNOWN / NOT VERIFIED** | 数据目录均不在 git；无 import commit；无全量 hash 清单证明方向 |

**官方文档表述（OBSERVED，文档层非代码层）**:
- `prd.md:77`：「原始 | `maintainess\PDF\*.pdf` | OCR 输入源」
- `prd.md:124-125`：`maintainess\` = 待转换区（PDF=OCR 源）；`original\` = 原始资料（五三资料等）
- `README.md:19-20`：同上两分法
- `production_adversarial_corpus_design.md:29`：「OCR 生产队列 | `maintainess\PDF` 12,707 份纯 PDF | 实测」
- 后置治理文档出现路径口径漂移：`PREPROCESSING-CLOSURE-PLAN.md:75` 写「stem 精确匹配 `original/` 树 **12,707** PDF 索引」——但 **12,707 是 maintainess/PDF 的实测 PDF 数**，original PDF 实测为 **38,893**。该句字面把 maintainess 的数量安到 original/ 名下。
  - Evidence: 本轮计数对照 `CLOSURE-PLAN.md:75`。
  - Status: **PARTIALLY VERIFIED / 措辞不精确（见 Part 6）**

**术语碰撞（OBSERVED）**: 契约/快照中的 `SHA256(original source bytes)` 是 **身份定义用语**（指该接口工件的 source bytes：对 IR/接口 manifest 面而言是 OCR md 字节；对 OCR 输出清单而言是 PDF 字节），**不能**仅凭字面断言来源目录 = `D:\Project\Papers\original`。
- Evidence: `interface_scope_snapshot_step1.json` 行内 `source_file`→Ocr-markdown md；`ocr_output_manifest` 条目 `source_sha256`→PDF；DQ 报告 §4 明确两层不可混用。

**结论（Source Corpus Reality）**:
- **OBSERVED FACT**: 运行时 preprocessing/OCR 的输入来源 = `maintainess\PDF`（代码 + 日志 + 数量三角互证）。
- **OBSERVED FACT**: `original/` 是并行存在的更大原始库，与 OCR 队列高度同名，抽样字节相同；后置图片恢复/质量扫描文档与脚本出现以 `original/` 为 PDF 检索树的口径。
- **UNKNOWN**: 哪一棵是「权威原始来源」；两树是否应被视为同一语料的双副本；采集上游（Papers 之外）来源。
- **OWNER DECISION REQUIRED**: 见 §8。

---

## 3. Preprocessing Input Lineage

### 3.1 第一次 preprocessing pipeline 执行

| 字段 | 值 | 分类 |
|------|----|------|
| Input path（日志层） | OCR 批处理从 PDF 根扫描；首日志报 **根目录 12,528 / 合计 12,703** 个 PDF | **OBSERVED FACT**（`logs/ocr_batch_log.txt` `[2026-09-06 10:42:46]`） |
| Input path（代码层，git 内最早） | `D:\Project\Papers\maintainess\PDF` | **OBSERVED FACT**（`85784a9` 引入 `batch_convert_pdf.py:55`） |
| 首跑时代码是否 git 可证 | **否** — 首跑 2026-09-06 **早于** git 首 commit 2026-09-12 | **OBSERVED FACT** |
| Commit（git 内首次落码） | `85784a9ace132d9043edf112d6bdc49ee40fa962`（2026-09-12 10:11:06 +0800, R25） | **OBSERVED FACT** |
| Commit（首跑对应 commit） | **NOT VERIFIED** — git 无 2026-09-06 的代码快照 | **UNKNOWN** |
| Evidence | OCR 日志首段；git reverse log；`git log --diff-filter=A` on `ocr_service/*`；当前树 `maintainess/PDF` 根层扁平计数 12,528 | — |

**Confidence**: **PARTIAL**

理由：
- 支持「首跑输入 ≈ maintainess/PDF」：日志数量结构（根扁平 12,528）与**当前** maintainess/PDF 结构同构；git 后代码唯一 PDF_ROOT；`prd.md` 事前规格写 maintainess\PDF 为 OCR 输入源。
- 不足以 **VERIFIED**：首跑当时的脚本字节不在 git；无法排除 2026-09-06 至 2026-09-12 间曾改过 `PDF_ROOT`；数据目录无 git 历史。

### 3.2 CODE_SOURCE_PATH_REFERENCE_REPORT（Part 3）

生产/审计代码中的源路径引用（硬编码或近硬编码）：

| File | Line | Reference | Meaning |
|------|------|-----------|---------|
| `ocr_service/batch_convert_pdf.py` | 55 | `D:\Project\Papers\maintainess\PDF` | **OCR 输入源 PDF_ROOT** |
| `ocr_service/batch_convert_pdf.py` | 56 | `D:\Project\Papers\Ocr-markdown` | OCR 输出根 |
| `ocr_service/batch_convert_pdf.py` | 47 | `D:\Project\Papers\data\ocr_page_usage.json` | 页额度账本 |
| `ocr_service/batch_convert_pdf.py` | 58 | `data\ocr_output_manifest.jsonl` | OCR 输出清单 |
| `scripts/recover_images.py` | 38-40 | `BASE=D:\Project\Papers`；`PDF_ROOT=...\maintainess\PDF` | 配图恢复所用源 PDF |
| `scripts/pac_select.py` | 28 | `ROOT/"maintainess"/"PDF"` | PAC 选样源 PDF |
| `scripts/pdf_fidelity.py` | 20 | `ROOT/"maintainess"/"PDF"` | PDF 文本层对照源 |
| `scripts/r64_data_inventory.py` | 41-43 | `Ocr-markdown` / `maintainess/PDF` / `data`（可用 `R64_*` 环境变量覆写，注释写明测试用） | 语料盘点武器 |
| `scripts/r64_data_inventory.py` | 50-53 | `SOURCE_DIRS = 高一/高二/高三/高考真题/未分类/合格考/会考/竞赛自招/其他汇编/学业水平考试` | **Ocr-markdown 源目录白名单**（非 original/maintainess） |
| `scripts/r65_r64_review.py` | 36,42 | `maintainess/PDF` + 同款 SOURCE_DIRS | R64 复查 |
| `scripts/r66_1_preflight.py` | 21 | `maintainess/PDF` | R66 预检 |
| `scripts/r66_1_activation_driver.py` | 28 | `maintainess/PDF/<specific>.pdf` | 受控激活样本 |
| `scripts/r67_manifest_bootstrap.py` | 48 | `maintainess/PDF` | manifest bootstrap |
| `scripts/r67_apply_gate.py` | 35 | `maintainess/PDF` | apply gate |
| `scripts/r67_apply_verify.py` | 21 | `maintainess/PDF` | apply verify |
| `scripts/r59_r58_review.py` | 26 | `maintainess/PDF` | R58/R59 复查 |
| `scripts/dq_data_quality_scan.py` | 268-270 | `ROOT/"original"` + `original.rglob(name)` | **OCR 清单 PDF sha 对账检索树 = original/** |
| `scripts/dq_data_quality_scan.py` | 253-259 | `fir["source_file"]`（IR 源路径） | IR provenance 对账对象 = 源 md/源树路径 |
| `tests/test_r67_bootstrap.py` | 25,405 | `D:\Project\Papers\maintainess\PDF` | 真实语料闸门路径 |
| `data/pac_selection.json` | 多条 `path` | `D:\Project\Papers\maintainess\PDF\...pdf` | 选样工件记录的绝对输入路径 |
| `data/r66_1_preflight.json` | 多条 `source_rel` | `maintainess/PDF/....pdf` | 预检记录的相对输入路径 |

**未发现** 生产代码使用 `INPUT_DIR=` / `SOURCE_DIR=` / `PDF_DIR=` / `CORPUS_DIR=` 这类命名的独立配置键（本轮 grep）；路径以 `PDF_ROOT`/`OCR_ROOT`/`BASE` 常量或 `R64_*` 测试覆写形式出现。

**INFERRED POSSIBILITY（非事实）**: 存在「操作队列 = maintainess/PDF，长期原件库 = original/」的双层设计；后置文档/脚本把「源 PDF 在位」检查切到 original/。
- 支持线索：README/prd 两分法；DQ/CLOSURE-PLAN 用 original/；`recover_images.py` 代码仍写 maintainess/PDF（文档与代码不一致）。
- **不得**升格为 OBSERVED FACT，除非 Owner 或全量 hash 台账确认。

### 3.3 OCR 清单与运行账本

| 工件 | 观测 | 分类 |
|------|------|------|
| `data/ocr_output_manifest.jsonl` | 1,801 条；**全部**含 `source_sha256` 与 `output_rel`；`provenance`：`r63-audit-bootstrap` 698 条 + 空/None 1,103 条 | **OBSERVED FACT** |
| 抽样 50 条 `output_rel` | 50/50 在 `Ocr-markdown/` 下存在 | **OBSERVED FACT** |
| `data/ocr_page_usage.json` | `{"date":"2026-09-16","used":16478}` | **OBSERVED FACT** |
| `logs/ocr_batch_log.txt` | 首跑 2026-09-06；文件近 8MB；后续大量 `DECIDE:NO_MANIFEST_ENTRY` 与续跑记录 | **OBSERVED FACT** |
| 首跑输入树的 git 可重建性 | **不可**（数据 ignored） | **OBSERVED FACT** |

**注意**: `provenance=r63-audit-bootstrap` 表明清单中至少 698 条来自 **审计回填/引导**而非（或不仅是）daemon 实时记账；**不能**把 1,801 条全部解释为「首跑实时写入」。
- Evidence: manifest `provenance` 计数；`git log` R63/R67 系列 commit 信息（bootstrap/apply）。
- 分类：**OBSERVED FACT（字段值）** + **UNKNOWN（每条真实产生时刻）**。

---

## 4. Artifact Traceability

### 4.1 Lineage 链（观测到的字节锚）

```
original/**.pdf  (or maintainess/PDF/**.pdf)     [数据不在 git]
        │  PDF bytes
        │  sha256 记于 data/ocr_output_manifest.jsonl :: source_sha256
        │  （代码 PDF_ROOT = maintainess/PDF；部分后置对账在 original/ 检索同名）
        ▼
Ocr-markdown/{年级|类别}/{科目}/*.md              [数据不在 git]
        │  源 md 字节
        │  接口面 source_content_sha256 / IR source_sha256 = sha256(md)
        ▼
Ocr-markdown/reslice-*/**.manifest.json (+ .annotated.md / 切片视图)
        │  166 manifests；source_file 绝对路径 → 源 md
        │  87 份含 sha；interface snapshot n=87
        ▼
data/interface_scope_snapshot_step1.json 等        [部分 tracked]
        identity_definition 字面: SHA256(original source bytes)
        行内 source_file → Ocr-markdown md；sha = md 字节
```

**OBSERVED FACT**: 链上存在 **两套 sha 语义** —— PDF 字节（OCR 清单）vs OCR md 字节（manifest/IR/接口快照）。
**OBSERVED FACT**: 词面 `original source bytes` ≠ 目录 `original/` 的自动证明。

### 4.2 OCR-LINEAGE-REPORT（Part 4）

抽样与全量键检查（本轮）：

| Artifact 类 | Has source reference | Has hash | Can trace | 说明 |
|-------------|---------------------|----------|-----------|------|
| 源树 OCR `Ocr-markdown/{学科树}/**/*.md` | **NO**（正文内） | **NO**（正文内） | **UNKNOWN→依赖外部清单** | 抽样 40 份源树 md：**0** 份正文含 `source_sha256`/`source_file` 等 lineage token |
| `data/ocr_output_manifest.jsonl` 条目 | YES（`source_rel` 文件名 + `output_rel`） | YES（`source_sha256`=PDF） | **PARTIAL / VERIFIED（有条目者）** | 1,801 条；覆盖远小于源树 md 约 4,224 |
| `*.manifest.json`（166） | YES（`source_file` 绝对路径→md） | **87/166** 含 sha 键 | **VERIFIED（有 sha 者，经快照 match）** | snapshot：87/87 r50 sha match；ir_admitted 71 sha match |
| `_imgs/**` 配图 | 经 md 引用与 `recover_images` 审计账 | 工具账目含 sha 闭环（文档层） | **PARTIAL** | 本轮未重算全量配图 hash；DQ 报告称已改写形态悬空=0 |
| `data/interface_scope_snapshot_step1.json` rows | YES | YES | **VERIFIED（87 行口径）** | `summary`: n_rows=87；r50 source sha match=87；ir_admitted_sha_match=71 |

**覆盖率事实（OBSERVED）**:
- 源树 md ≈ **4,224**（排除派生前缀后的口径）
- OCR 输出清单条目 = **1,801**
- reslice/接口 manifest = **166**（其中 sha=87）
- **存在大量源 md 无法仅凭现有 tracked 工件完成 PDF↔md 闭环**（清单未覆盖）

**Traceability 总评**: **PARTIAL**
- 有清单/快照的子集：可 hash 追溯（VERIFIED）。
- 无清单正文 lineage 的多数源 md：仅能靠文件名与目录布局 **推断**，**NOT VERIFIED** 到字节级 PDF 锚。

### 4.3 示例闭环（VERIFIED 样本）

对象：`2018北京春季高中会考化学（教师版）(1)`

| 节点 | 值 | Evidence |
|------|----|----------|
| maintainess PDF path | `maintainess/PDF/2018北京春季高中会考化学（教师版）(1).pdf` | `rglob` |
| original PDF path | `original/高三/2018/合格考试/化学/....pdf` | `rglob` |
| PDF sha256（两树） | `8d3f9dad0918567b3ef375a57843d5d28d1eff77dfac467ff9eddc0f3c4f3a23` | 现算；两侧一致 |
| OCR manifest | 同 sha；`output_rel=会考/化学/...md`；`written_at=2026-09-13 21:40:50`；`provenance=r63-audit-bootstrap` | `ocr_output_manifest.jsonl` |
| 接口 manifest | `source_content_sha256=0443945f...fad1ffb`；`identity_version=2` | `reslice-batch-C/...manifest.json` |
| 源 md sha256 | `0443945f4672b05da3d2d950b0a3eb20a495c1635c353c024c8c050b7fad1ffb` | 现算 match True |
| snapshot 行 | 同 md sha；r50 match true | `interface_scope_snapshot_step1.json` rows[0] |

该样本证明：**在清单+manifest 覆盖范围内，PDF 与 md 两层 hash 锚可闭合；且 maintainess/original 同名 PDF 可字节一致。**

---

## 5. Maintainess Project Classification（Part 5）

**禁止提前判断；以下仅列证据后的分类。**

### 5.1 观测摘要

| 证据 | 内容 |
|------|------|
| 规格定位 | `prd.md`/`README.md`：maintainess = 待转换/维护区；其 `PDF\` = OCR 源 |
| 代码消费 | 生产 OCR 与 R59/R64–R67/pac/pdf_fidelity/recover_images **只把 maintainess/PDF 当 PDF_ROOT** |
| 结构 | PDF 树以扁平根为主（12,528/12,707）；另有 DOCX 12,142、待转换DOC 38、质量测试 5、空 test_output |
| 与 original 重叠 | 文件名交集 12,626/12,707；抽样 6/6 sha 一致 |
| 文档漂移 | 部分后置治理文档把「12,707 PDF」写在 `original/` 名下，或用 original/ 做 stem 检索 |
| git | maintainess 全树 ignored，无历史 |

### 5.2 分类结论

| 可能结果 | 判定 | 依据 |
|----------|------|------|
| **Case A** maintainess = temporary conversion experiment | **对整个 maintainess 树：不充分成立**；对 `PDF/` 子树：**不支持**（生产 daemon/脚本持续读取，且数量与生产日志同构） | 代码 + 日志 + 12,707 在位 |
| **Case B** maintainess = original preprocessing source | **对 operational OCR source：成立（OBSERVED）**；对「唯一/上游原始来源」：**NOT VERIFIED** | PDF_ROOT 硬编码；但 original/ 更大且文档称原始资料 |
| **Case C** mixed asset | **对整个 `maintainess/` 目录：成立（OBSERVED）** | 同时含生产 PDF 队列 + 大体量 DOCX + 质量测试 + 空目录；各子树角色不同 |

**精确表述（审计用语）**:
- **OBSERVED FACT**: `maintainess/PDF` = 当前 preprocessing OCR 的 **operational input corpus**。
- **OBSERVED FACT**: `maintainess/` 整目录 = **mixed asset**（不能单靠目录名定性）。
- **UNKNOWN**: `maintainess/PDF` 与 `original/` 的数据血缘方向、是否双副本、哪侧为治理权威。
- **OWNER DECISION REQUIRED**: 见 §8。

---

## 6. Existing Audit Claim Verification（Part 6）

检查范围：`D:\Project\AITutor-X\Docs\60_REPORTS\REPORT-A..I`。  
**OBSERVED FACT**: `REPORT-J` **不存在**（任务书列出但仓库无此文件）→ 无 J 可对账。

### AUDIT-CLAIM-CORRECTION

| Claim | Previous status / 出处 | New evidence（本轮） | Updated status |
|-------|------------------------|----------------------|----------------|
| Producer 大体量数据不在 git，baseline 无法仅从 git 重建 | REPORT-G **VERIFIED**（GAP-007/OD-009） | `.gitignore:7-10`；`git ls-files original/maintainess/Ocr-markdown`=0 | **VERIFIED（维持）** |
| 数据物理位置在 Papers 工作树，绝对路径依赖 `D:\Project\Papers\...` | REPORT-G/H | 代码大量 `D:\Project\Papers\...`；`pac_selection.json` 绝对路径 | **VERIFIED（维持）** |
| r67 真实语料 smoke FAIL（768 AUDIT_FROM_UNMATCHED）仍存在 | REPORT-A/F/G | 与 lineage 无直接冲突；本轮**未重跑**该测试 | **UNVERIFIED（本轮未测）** — 不作 lineage 结论 |
| 「原始试卷来源」可用 `original/` 或 `maintainess/` 任一目录名直接等同 | Claude A–I **未给出**明确 lineage 裁决（多回避） | 代码 PDF_ROOT=maintainess/PDF；original 更大且高重叠 | **UNKNOWN→本轮单列**（旧报告不足以回答本问题） |
| 后置文档：源 PDF 在位率按 `original/` 树 **12,707** PDF 索引 | Papers `PREPROCESSING-CLOSURE-PLAN.md:75`（非 AITutorX REPORT，但属既有审计/治理主张） | original PDF 实测 **38,893**；**12,707 = maintainess/PDF** 实测值 | **PARTIALLY VERIFIED / 措辞错误** — 在位率数字与「12,707」可同时真，但**目录归属写错或未定义** |
| OCR 生产队列 = `maintainess\PDF` 12,707 | `production_adversarial_corpus_design.md:29` | 恢复后实测 12,707 | **VERIFIED** |
| original 树格式分布 PDF 38,893 / DOCX 30,254 / DOC 207 / PPTX 164 | `log.md:871` | 本轮实测完全一致 | **VERIFIED** |
| manifest 不钉 sha；IR/OCR 清单分层钉链 | DQ 报告 §4（Papers EVIDENCE） | 166 manifest：source_file=166，sha=87；snapshot 87 match | **PARTIALLY VERIFIED** — 「manifest 自身不钉 sha」在「0/166 携带 sha」字面下与本轮「87/166 含任一 sha 键」**不完全一致**（可能键名/批次口径不同，**细节 UNKNOWN**） |
| 「PDF only 6 files means corpus issue」类主张 | 任务书示例；**AITutorX REPORT-A~I 无此句** | 会话中途 6 文件 = Owner 确认的**误删除过程态**；恢复后 12,707 | **NOT APPLICABLE to committed reports** / 若外部 Set B 有此主张则 **STALE 或需按恢复后状态重测** |
| DSH Observation Set B 已导入 AITutorX | REPORT-G：**UNVERIFIED** | 目录仍无 Set B；无 REPORT-J | **UNVERIFIED（维持）** |
| identity 定义 `SHA256(original source bytes)` 可证明源目录=original/ | 无 Claude 报告明确这样写；风险来自词面 | snapshot/md/PDF 两层 sha 语义 + DQ 报告 | **UNVERIFIED if anyone claims directory-level proof** — 词面定义 ≠ 目录证明 |

---

## 7. UNKNOWN（不自行解决）

| ID | 陈述 | 为何无法证明 |
|----|------|----------------|
| **UNKNOWN-001** | 2026-09-06 首次 OCR 执行时的**脚本字节级 Input path** | git 首 commit 晚于首跑 6 天；无 pre-git 代码快照 |
| **UNKNOWN-002** | `maintainess/PDF` ↔ `original/` 的文件流动方向（谁拷贝谁 / 是否同一采集批次） | 双树均不在 git；无 import 记录；无全量双侧 hash 台账 |
| **UNKNOWN-003** | 源树 md（≈4,224）中有多大比例可被 `ocr_output_manifest.jsonl`（1,801）或 manifest（166）字节级覆盖 | 本轮未做全量 join 统计 |
| **UNKNOWN-004** | 恢复后的 `maintainess/PDF` 是否与误删前逐字节一致 | 仅验证数量 12,707 + 抽样 6 组与 original/清单一致；无恢复前全量 hash 快照 |
| **UNKNOWN-005** | `original/` 语料进入 Papers **之前**的上游来源 | 仓库内无采集 provenance 文档（本轮未发现） |
| **UNKNOWN-006** | 12,626 个交集文件名中，全量是否都字节一致 | 仅 6/6 抽样 |
| **UNKNOWN-007** | REPORT-J 内容与主张 | 文件不存在于 AITutorX |
| **UNKNOWN-008** | DQ/CLOSURE 文档中「original/ 12,707 PDF 索引」具体索引工件路径与生成脚本 | `dq_figure_pdf_availability.json` 只给 `pdf_in_original_by_stem` 等汇总键，未附索引文件路径；`recover_images.py` 代码仍指向 maintainess/PDF |
| **UNKNOWN-009** | `ocr_output_manifest` 中 1,103 条无 `provenance` 记录的真实产生时间与是否含 daemon 实时账 | 清单未记录逐条 runtime 时间戳（`processed_at` 多为 null） |
| **UNKNOWN-010** | 87/166 manifest 含 sha 与 DQ 报告「0/166 携带 sha」的口径差来源 | 可能键名（`source_content_sha256`）/批次/检测方法不同；未做报告级复现脚本对账 |

---

## 8. Owner Decisions Required（只列问题，不替 Owner 裁决）

| ID | 需要 Owner 决策的问题 |
|----|------------------------|
| **OD-K-01** | **权威原始来源**：preprocessing 的 canonical source corpus 定义为 `maintainess/PDF`、`original/`，还是「双层：original=原件库 / maintainess=OCR 队列」？ |
| **OD-K-02** | **数据权威与治理引用**：AITutorX/下游应引用哪条路径？是否要求 Producer 提交「路径 + sha256 清单」而非数据本体？ |
| **OD-K-03** | **词义冻结**：Contract/快照中 `SHA256(original source bytes)` 是否需要在治理文档中**显式区分**「identity 词面」vs「目录 `original/`」，避免目录级误读？ |
| **OD-K-04** | **双树策略**：`maintainess/PDF` 与 `original/` 高重叠副本是否保留双份？若只保留一份，保留哪份、迁移/校验由谁执行？（本轮不执行任何迁移） |
| **OD-K-05** | **恢复完整性**：Owner 是否接受「数量 12,707 + 抽样 hash」作为 maintainess 恢复完成的充分证据，还是要求全量 hash 重算入账？ |
| **OD-K-06** | **文档口径**：如何更正 Papers 内将「12,707」系于 `original/` 的表述，而又不违反「不得修改既有报告/账本」的冻结纪律（更正载体：新报告 / 附录 / Owner 令）？ |
| **OD-K-07** | **lineage 补全责任**：源 md 无正文 lineage、OCR 清单覆盖不全——是否立项要求 Producer 补齐可审计清单（范围、格式、是否入 git）？ |
| **OD-K-08** | **Observation Set B / REPORT-J**：外部独立审计包是否导入？若 Set B 存在与本报告冲突的 corpus 主张，以何为对账基准？ |
| **OD-K-09** | **DOCX/待转换DOC**：`maintainess/DOCX`（12,142）与 `待转换DOC`（38）是否属于 preprocessing 正式输入范围？（现行 OCR 代码不读 DOCX） |
| **OD-K-10** | **首跑证据效力**：在无 pre-git 代码快照情况下，是否接受「日志数量结构 + 现行代码 + prd 规格」作为 maintainess/PDF=历史 OCR 输入 的治理级证据？ |

---

## 9. Evidence Index（命令与文件）

| 类 | Evidence |
|----|----------|
| 仓库现实 | Papers `git rev-parse HEAD`=2b92898…；`git status -sb` main==origin/main；remote `kurt-wong/Aitutors-preprocessing` |
| 目录清点 | `find`/`du`/`git ls-files`（original 69535/115G/0；maintainess 24892/46G/0；maintainess/PDF 12707/21G；Ocr-markdown 52003/1013M/0；data 204/193 tracked） |
| 忽略规则 | `Papers/.gitignore:7-10`；`git check-ignore -v original maintainess Ocr-markdown` |
| 代码路径 | `ocr_service/batch_convert_pdf.py:25,47,55-58`；`scripts/recover_images.py:38-40`；`scripts/dq_data_quality_scan.py:261-276`；`scripts/r64_data_inventory.py:41-54`；`tests/test_r67_bootstrap.py:25,405` |
| Git 时间线 | 首 commit `85784a9` 2026-09-12 R25；OCR 日志首跑 2026-09-06；`ocr_service/batch_convert_pdf.py` 首次入库即含 maintainess PDF_ROOT |
| Hash 对账 | 6/6 maintainess↔original 同名 PDF sha256 一致；化学卷 PDF sha `8d3f9dad…` = OCR manifest；md sha `0443945f…` = manifest/snapshot |
| Lineage 工件 | `data/ocr_output_manifest.jsonl`（1801）；`data/interface_scope_snapshot_step1.json`（n=87）；`data/dq_figure_pdf_availability.json`（dangling 1396/27240；pdf_in_original_by_stem 1394）；manifest keys 166/87 |
| 文档口径 | `prd.md:77,124-125`；`README.md:19-20`；`production_adversarial_corpus_design.md:29,34`；`log.md:871`；`PREPROCESSING-CLOSURE-PLAN.md:75,81`；`PREPROCESSING-DATA-QUALITY-REPORT.md:69-78` |
| AITutorX 报告 | REPORT-A~I 存在；REPORT-J 不存在；G/H/I 关于数据不入 git 的主张维持 VERIFIED |

---

## 10. STOP

本报告为 Phase 0 唯一交付物。  
**不**开始 Governance Foundation 编写；**不** migration；**不**代码修改；**不**扩展审计；**不**创建 DEC/BUG/OQ。

等待 Owner 与 Evidence Reconciler 下一步指令。

*REPORT-K · Independent Evidence Auditor · 2026-09-17 · 仅新建本文件*
