# GF-001 — Source Authority Model（草案）

**Document ID**: GF-001
**Status**: `DRAFT / PROPOSED` — 未经 Owner 批准，不构成冻结权威
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Evidence discipline**: 每条陈述标注 `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**Forbidden honored**: 不假设 `maintainess` 权威；不假设 `original` 权威；不以物理路径充当身份；不改代码/数据/既有报告

---

## 1. Purpose

定义 AITutor-X 迁移所用的**基于角色的来源权威模型**：谁是 Raw Source、谁是 Processing Input、谁是产物、谁可迁入治理树。

本模型回答的是 **“该数据在治理上扮演什么角色”**，而不是 **“它存放在哪个目录”**。

---

## 2. Role Definitions（角色定义，非路径定义）

### 2.1 RSD — Raw Source Document

| Field | Definition |
|-------|------------|
| **Definition** | 某文档**最初被任一系统接收时的物理字节集合**（试卷 PDF/DOCX 等原件字节） |
| **Identity anchor** | `sha256(those raw bytes)` — 算法层身份，**与存放目录无关** |
| **Ownership** | 采集/持有方（当前观测到的持有树在 Producer 工作区，见 §3） |
| **Authority meaning** | 「原件身份」成立的充分条件是 **bytes 可复算且 hash 可登记**，不是路径名含 `original` |
| **Not assumed** | ❌ 不假设某目录名 = RSD 唯一库 ❌ 不假设双树中任一侧为上游 |

- `[FACT]` Producer 工作区存在两棵大体量语料树：`original/`（PDF 38,893 等，115G）与 `maintainess/PDF`（12,707 PDF，21G）；均 `git ls-files = 0`。（REPORT-K §2.1；`Papers/.gitignore:7-10`）
- `[FACT]` 抽样 6 组同名 PDF 在两树 **sha256 一致**。（REPORT-K §1.8）
- `[UNKNOWN]` 两树数据血缘方向、是否同一采集批次、哪一侧是 RSD 权威库。

### 2.2 PIS — Processing Input Snapshot

| Field | Definition |
|-------|------------|
| **Definition** | **某一次流水线执行实际消费的文件集合 + 各文件 hash**，执行后不可变 |
| **Identity key** | `snapshot_id` + 每条目 `file_role + content_sha256` |
| **Ownership** | Producer（生成侧）；Consumer 只读引用 |
| **Validation** | 执行日志输入计数 / 清单条目 / 复算 hash 三者可对账 |
| **Not assumed** | ❌ 不假设「当前目录内容」= 历史某次 PIS |

- `[FACT]` 现行 OCR 生产代码 `PDF_ROOT = r"D:\Project\Papers\maintainess\PDF"`（`ocr_service/batch_convert_pdf.py:55`）及多脚本同类硬编码。
- `[FACT]` OCR 日志首跑 `2026-09-06 10:42:46` 扫「根目录 12528 / 合计 12703」；git 首 commit `85784a9` 为 `2026-09-12`（晚于首跑）。
- `[FACT]` 因此：**当前可观测的 operational input path = `maintainess/PDF`**；**首跑字节级代码 Input path = `[UNKNOWN]`**（无 pre-git 快照）。
- `[INFERENCE]` 首跑输入 ≈ 现行 `maintainess/PDF`（数量结构 + 现行代码 + `prd.md:77` 规格支持）— Confidence **PARTIAL**，不得升格为 FACT。

### 2.3 OCRA — OCR Artifact

| Field | Definition |
|-------|------------|
| **Definition** | 对某 PIS 执行 OCR 后的产出（当前观测形态：Markdown + 图片资源 + 运行清单） |
| **Identity key** | `output_rel` + `sha256(ocr_output_bytes)`；上游锚 = 清单中的源 PDF `source_sha256` |
| **Ownership** | Producer |
| **Validation** | `data/ocr_output_manifest.jsonl` 条目 ↔ 磁盘 md 可复算 hash |
| **Not assumed** | ❌ 不假设所有 md 均在清单内 ❌ 不假设正文自带 lineage |

- `[FACT]` OCR 产出区 = `Ocr-markdown/`（自述「PDF → OCR Markdown 转换产出区」）。
- `[FACT]` `ocr_output_manifest.jsonl`：1,801 条，全部含 `source_sha256`（**PDF 字节**）与 `output_rel`；`provenance`：`r63-audit-bootstrap` 698 + 空 1,103。
- `[FACT]` 源树 md 抽样 40/40 **正文无** lineage token；覆盖相对源树 ≈4,224 不完整。
- `[UNKNOWN]` 清单外 md 的 PDF 字节级归属。

### 2.4 SEM — Semantic Artifact

| Field | Definition |
|-------|------------|
| **Definition** | 在 OCR 产物之上产生的语义/接口层工件：reslice manifest、批注、IR、接口快照 |
| **Identity key** | 接口面 `source_content_sha256` = **sha256(声明的 source bytes)**；对现有 manifest/IR 面而言即 **OCR md 字节** |
| **Ownership** | Producer 生成；身份契约权威见 Frozen Contract v0.2 |
| **Validation** | manifest `source_content_sha256` ↔ 对 md 现算；`interface_scope_snapshot_step1.json` 对账 |
| **Not assumed** | ❌ 不假设 SEM 的 source hash = PDF hash ❌ 不把 identity 词面 `original` 读成目录名 |

- `[FACT]` 样本闭环：PDF sha `8d3f9dad…f3a23`（两树一致 = OCR 清单）；md sha `0443945f…ad1ffb`（manifest = snapshot = 现算）。
- `[FACT]` 接口快照 `identity_definition` 字面 = `SHA256(original source bytes), 64 lowercase hex`，但行内 `source_file` 指向 Ocr-markdown md。
- `[FACT]` Contract v0.2 冻结要点（Producer `CURRENT.md` / log 核验）：`source_content_sha256` = Identity Authority；**path 仅 locator，禁止 path 作唯一身份**；冻结四元组 = `kurt-wong/AITutors-v3` @ `f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1` / `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` / sha256 `9c6b9063…7528`。
- `[DECISION REQUIRED]` 见 GF-005 `OQ-GF-003`（identity 词面 vs 目录 `original/` 的治理标注）。

### 2.5 MIG — Migration Artifact

| Field | Definition |
|-------|------------|
| **Definition** | **已通过 Migration Gate**、以指定身份进入 AITutor-X 治理树的资产 |
| **Identity key** | `source_repo + source_commit + source_path + (适用时) sha256 + migration_record_id` |
| **Ownership** | AITutor-X 治理仓（迁移后）；来源事实仍属源仓 commit |
| **Validation** | Gate 1–10 记录完整；REPORT-I 停止线与 F1–F10 状态满足 |
| **Not assumed** | ❌ 源仓存在 ≠ 可迁 ❌ git tracked ≠ Authority（`AGENTS.md` 原则 4） |

- `[FACT]` `AGENTS.md`：Provenance ≠ Quality Authority；UNKNOWN is retained data；未经 Migration Gate 不得进入 active tree。
- `[FACT]` REPORT-I §0：默认在 Cluster A 未由 Owner 关闭前 **全面禁止迁移**（例外仅限 Owner 书面批准的只读证据副本）。

---

## 3. Directory Role Map（观测角色，**非**权威裁决）

| Physical path（Producer `D:\Project\Papers\…`） | 观测内容 `[FACT]` | 治理角色（本模型） | 权威主张 |
|--------------------------------------------------|-------------------|--------------------|----------|
| `original/` | 69,535 文件 / 115G；PDF 38,893；DOCX 30,254；DOC 207；PPTX 164；含 `五三资料/` 等 | **RSD 候选库 A**（较大原件树） | `[UNKNOWN]` 是否 canonical RSD |
| `maintainess/PDF` | 12,707 PDF / 21G；根层扁平 12,528 | **PIS 操作输入根**（现行 OCR 代码/日志所钉） | `[FACT]` = operational OCR input；`[UNKNOWN]` 是否同时为/唯一 RSD |
| `maintainess/DOCX` | 12,142 | 范围外候选（现行 OCR 代码不读） | `[UNKNOWN]` 是否正式输入（OQ-GF-010） |
| `maintainess/待转换DOC` 等 | 38 / 5 / 0 | mixed asset 子区 | `[UNKNOWN]` |
| `maintainess/`（整目录） | 24,892 / 46G | **Case C mixed asset** | 不得整目录单一定性 |
| `Ocr-markdown/` | md 全树 6,114；manifest 166 | **OCRA 产出区** | n/a（产物，非源权威） |
| `data/`（部分 tracked） | 清单/快照/审计 JSON | **SEM/账本工件区** | 部分 git 可证 |
| `docs/…EVIDENCE`、`_archive/` | 历史证据/归档 | 历史证据（只读） | 非现行权威 |

**硬规则（本模型提案，待 Owner 批准后生效）**:

1. **Path ≠ Role**：目录名不自动授予 RSD/PIS/权威身份。
2. **Role ≠ Authority**：认定某路径为 PIS，不等于认定其为唯一/上游原始来源。
3. **双树关系显式建模**：在 Owner 裁决 `OQ-GF-001` 前，治理文档必须同时登记两树，禁止静默取其一。
4. **引用优先 hash**：下游/迁移引用数据时，优先「角色 + content_sha256 + 登记载体」，其次才是绝对路径。

---

## 4. Authority Questions This Model Explicitly Leaves Open

| ID | Open question | 本模型处理 |
|----|---------------|------------|
| OD-K-01 / OQ-GF-001 | 权威原始来源：maintainess/PDF、original/、还是双层？ | 双角色并列登记，不裁决 |
| OD-K-02 / OQ-GF-002 | 数据权威引用方式：path-ref / hash 清单 / copy / NAS | 提案偏向 hash 清单；模式待 Owner |
| OD-K-04 / OQ-GF-004 | 高重叠双树是否保留双份 | 不假设合并或删除 |
| OD-K-05 / OQ-GF-005 | maintainess 恢复完整性证据标准 | 数量+抽样 vs 全量 hash，待 Owner |
| UNKNOWN-002 / OQ-GF-006 | 双树流动方向 | 保持 UNKNOWN |

---

## 5. Relationship to V3 / Contract（服从，不重定义）

| 上游权威 | 本模型关系 |
|----------|------------|
| V3_SPEC `10_Data_Model.md` `documents.original_sha256` | V3 源域已要求「原始文件 SHA256」；本模型提供 **migration 前** 的角色解释，不修改 V3 schema |
| Contract v0.2 `source_content_sha256` + path non-identity | 本模型 **服从**该身份原则；§2.4 仅转述 |
| V3_SPEC `50_Migration_Assets.md` §5「绝不迁」 | 迁移边界见 GF-004，与 50 §5 对齐 |
| REPORT-I Gate / F1–F10 | MIG 角色的进入条件以 Gate 为准 |

---

## 6. Success Criterion（本文件）

未来工程师应能回答：

> 「这份 PDF/这份 md/这份 manifest 在治理上是什么角色？信任依据是什么？」

而**不需要**知道 preprocessing 历史实现细节，也**不会**被误导为「目录名 = 权威来源」。

---

*GF-001 · DRAFT · TASK-GF-001 · 2026-09-17 · 仅新建治理草案，未改源仓*
