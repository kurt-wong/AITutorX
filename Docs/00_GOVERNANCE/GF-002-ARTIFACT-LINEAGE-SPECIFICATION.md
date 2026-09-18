# GF-002 — Artifact Lineage Specification（草案）

**Document ID**: GF-002
**Status**: `DRAFT / PROPOSED` — 未经 Owner 批准，不构成冻结权威
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Evidence discipline**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**Forbidden honored**: 不混用 identity 词义与物理目录；不假设 maintainess/original 权威；不改代码/数据

---

## 1. Mandatory Lineage Chain（强制血缘链）

```text
L1  Source PDF
      ↓
L2  OCR output
      ↓
L3  Semantic annotation
      ↓
L4  Question IR
      ↓
L5  Admission Candidate
      ↓
L6  AITutor-X Entity
```

- `[FACT]` 任务书 GF-002 规定此六层链为治理强制模型。
- `[FACT]` V3_SPEC `20_Document_Pipeline.md` §1–§3 的阶段对象与 `10_Data_Model.md` A/B/C 三域可映射到 L2–L6（见 §3）。
- `[FACT]` Producer 现存工件主要覆盖 **L1–L4 的部分子集**；L5/L6 在 AITutor-X/V3 侧尚未以迁移后 active entity 形式落地（REPORT-I 停止线）。

每层必须能回答四问：**identity key · hash meaning · ownership · validation method**。

---

## 2. Layer Contracts

### L1 — Source PDF

| Field | Specification |
|-------|---------------|
| **Identity key** | `source_pdf_sha256` = `sha256(pdf_raw_bytes)`（64 lowercase hex） |
| **Hash meaning** | **PDF 文件字节**的 SHA-256。与 OCR md hash、IR hash **不是同一层** |
| **Ownership** | RSD/PIS 持有方（Producer 侧角色见 GF-001 §2–§3） |
| **Validation method** | (a) 对登记路径现算 sha256；(b) 与 `ocr_output_manifest.jsonl` 条目 `source_sha256` 对账；(c) 双树同名文件可选交叉复算 |
| **Observed carriers** | `[FACT]` `data/ocr_output_manifest.jsonl`（1,801 条全部含 `source_sha256`） |
| **Gaps** | `[FACT]` 数据树不在 git；`[UNKNOWN]` 交集 12,626 文件名是否全量字节一致（仅 6/6 抽样） |

**Path rule** `[FACT from Contract]`：path（如 `maintainess/PDF/....pdf` 或 `original/高三/....pdf`）仅为 **locator**，禁止作唯一身份。

### L2 — OCR output

| Field | Specification |
|-------|---------------|
| **Identity key** | `ocr_md_sha256` = `sha256(ocr_markdown_bytes)` |
| **Hash meaning** | **OCR 产出 md 字节**（当前接口面/IR 所钉的 source bytes） |
| **Ownership** | Producer |
| **Validation method** | manifest `source_content_sha256` / snapshot 行 ↔ 对 md 现算；样本已 VERIFIED |
| **Observed carriers** | `[FACT]` `Ocr-markdown/**/*.manifest.json`（166；其中 87 含 sha 键）；`data/interface_scope_snapshot_step1.json`（n_rows=87，r50 match 87） |
| **Gaps** | `[FACT]` 源树 md ≈4,224 ≫ 清单 1,801 ≫ manifest 166；正文 lineage 0/40 抽样；`[UNKNOWN]` 全量覆盖率（UNKNOWN-003） |

**双层锚关系（治理必须分列，不得折叠为一条 hash）**:

```text
L1 source_pdf_sha256  ──(OCR 转换)──►  L2 ocr_md_sha256
     ↑ 清单 source_sha256                   ↑ manifest/IR source_content_sha256
```

- `[FACT]` Papers DQ 报告已写明两层 sha 语义不同（`PREPROCESSING-DATA-QUALITY-REPORT.md:69-78` 口径）。
- `[FACT]` 样本：PDF `8d3f9dad…` ≠ md `0443945f…`；链在清单覆盖范围内可闭合。

### L3 — Semantic annotation

| Field | Specification |
|-------|---------------|
| **Identity key** | 治理提案：`(source_content_sha256, annotation_stage, logical_execution_hash)`；V3 落库形态见 `10 §3/§5.1` |
| **Hash meaning** | **对「该 annotation stage 的输入身份 + 阶段配置」的 stage hash**，不是 source bytes 本身的别名 |
| **Ownership** | Producer 生成历史工件；V3 运行期归 Consumer 管线（Gate Policy 与 LLM 边界见 00 P2） |
| **Validation method** | V3：`semantic_annotations.payload` + `logical_execution_stage/hash` + `source_version_id`；历史：reslice/annotated md 与 manifest 对账 |
| **Observed carriers** | `[FACT]` `Ocr-markdown/reslice-*/**`（manifest + annotated 视图等） |
| **Gaps** | `[UNKNOWN]` 历史 annotation 工件与 V3 `semantic_annotations` schema 的字段级等价性（未做全量映射） |

### L4 — Question IR

| Field | Specification |
|-------|---------------|
| **Identity key** | 治理提案：`ir.source_sha256`（观测到的历史字段）对齐 Contract 接口键语义 = **上游 source bytes hash** + IR 自身结构版本 |
| **Hash meaning** | 历史 IR 面 `source_sha256` = **OCR md 字节**（与 L2 同层），**不是** PDF；IR 结构完整性另需 build/version 身份（V3 P7） |
| **Ownership** | Producer 历史 IR；V3 中 IR 为 **transient**，持久化形态 = `admission_candidates.payload`（`20 §1` 第二数据模型禁令） |
| **Validation method** | `[FACT]` Papers 记录：71 ADMITTED 的 `ir.source_sha256` 与磁盘 md 字节 sha 对账零漂移（log 核验条） |
| **Gaps** | `[FACT]` IR 71 ≠ manifest 166 ≠ OCR 清单 1801；`[UNKNOWN]` 未 ADMITTED/未建 IR 的源如何补链 |

### L5 — Admission Candidate

| Field | Specification |
|-------|---------------|
| **Identity key** | V3：`admission_candidates` + `logical_execution_stage/hash`（compile stage）+ `input_identity` + `build_versions` |
| **Hash meaning** | Candidate = **冻结快照边界**（管线世界 → 业务世界的唯一通道）；hash 身份是「对何输入、用何版本构建」，不是源 PDF 目录 |
| **Ownership** | Consumer（V3/AITutor-X 目标架构）；**LLM 无 Admission Authority**（00 P2 / 10 §1.1） |
| **Validation method** | Gate 分层证据 + payload 可重放；`decision_status` 只能经确定性 Gate Policy 或人工 |
| **Observed carriers** | `[FACT]` V3_SPEC 定义完整；AITutor-X 内 **尚无** 已迁移的 active candidate 实体（REPORT-I） |
| **Gaps** | `[DECISION REQUIRED]` D2/D3/D4、Design v1.1 authority（REPORT-E/H）影响 identity 实现资产定性 |

### L6 — AITutor-X Entity

| Field | Specification |
|-------|---------------|
| **Identity key** | 迁移记录身份：`source_repo + source_commit + source_path + content_sha256 + migration_record_id`；业务实体身份服从 V3 `10 §6`（Question vs Instance 等） |
| **Hash meaning** | 实体层身份来自 **Admission 物化 + 治理迁移记录**，不来自 preprocessing 目录名 |
| **Ownership** | AITutor-X 治理仓 |
| **Validation method** | Migration Gate 1–10 + Admission 唯一入口证据 + lineage 前层完整 |
| **Gaps** | `[FACT]` Cluster A 未关闭前默认禁止迁移（REPORT-I §0.7） |

---

## 3. Mapping to Frozen V3 Spec（服从性对照）

| GF-002 层 | V3_SPEC 锚点 `[FACT]` | 备注 |
|-----------|----------------------|------|
| L1 Source PDF | `10 §4.1 documents.original_sha256` | V3 源域要求原始文件 SHA256 |
| L2 OCR / L1 extract | `10 §4.2 document_source_versions`（`artifact_kind`/`body_hash`/`integrity_hash`） | OCR 可作为 `raw_l1` 类 version；role/provider 封闭配对 |
| L3 Semantic annotation | `10 §5.1` + `20 §4` | payload + stage hash |
| L4 Question IR | `20 §6`（transient）→ 并入 candidate payload | 禁止为 IR 另建中间表（20 §1） |
| L5 Admission Candidate | `10 §5.2/§5.3` + `20 §8` | Candidate=noun；decision_status 三分 |
| L6 AITutor-X Entity | `10 §6` A 域 + AITutor-X Gate | 只经 Admission Transaction 物化 |

- `[FACT]` `50_Migration_Assets.md` §4.2：Golden Corpus 条目 = `{源 PDF 引用, seal hash, 逐层预期}`，与本血缘链分层验证一致。
- `[INFERENCE]` Golden Corpus 可作为 L1–L5 的**评测真值载体**，但 corpus 本身不是迁移权威数据源。

---

## 4. Explicit Resolution — `SHA256(original source bytes)`

任务书要求：必须区分 **语义** 与 **物理目录**，禁止混用。

### 4.1 Semantic meaning（身份语义）— 采用

**定义（治理提案用语）**:

> `SHA256(original source bytes)` = **对该工件所声明的「上游 source 原始字节」计算的 SHA-256（64 位小写 hex）**。
> 其中 “original” 修饰的是 **bytes 相对该工件的来源关系**，不是磁盘目录名。

| 工件层 | 该层的 “source bytes” 实际是什么 `[FACT]` | 对应 hash 字段 |
|--------|------------------------------------------|----------------|
| OCR 输出清单条目 | **PDF 文件字节** | `source_sha256` |
| 接口 manifest / IR / snapshot | **OCR Markdown 字节** | `source_content_sha256` / `ir.source_sha256` |
| V3 `documents` | **入库原始文件字节** | `original_sha256` |

- `[FACT]` Contract v0.2：`source_content_sha256` = Identity Authority；path non-identity；双层职责不得混用。
- `[FACT]` 样本闭环证明两层 hash 各自可复算且不相等。

### 4.2 Physical directory（物理目录）— 单独概念

| 对象 | 观测 | 与 identity 词面的关系 |
|------|------|------------------------|
| `D:\Project\Papers\original` | 存在；PDF 38,893；更大原件树 | `[FACT]` 是路径；`[UNKNOWN]` 是否为唯一/权威 RSD |
| identity_definition 词面 `original source bytes` | 出现在 `interface_scope_snapshot_step1.json` | `[FACT]` 行内 source 指向 Ocr-markdown md，**不**指向目录 `original/` |

### 4.3 混用禁令（Hard Rule）

```text
FORBIDDEN:
  source_content_sha256 的词面含 "original"
    ⇒ 因此源目录 = D:\Project\Papers\original     ❌

FORBIDDEN:
  目录名为 original/
    ⇒ 其中文件自动获得 RSD / Identity Authority   ❌

REQUIRED:
  每次书写 hash 时同时标注:
    (1) hash 作用的 bytes 类型（pdf / ocr_md / figure / stage…）
    (2) 登记载体（哪个清单/manifest/表）
    (3) locator 路径（可空、可变、非身份）
```

- `[FACT]` REPORT-K §4.1：词面 ≠ 目录自动证明。
- `[DECISION REQUIRED]` OD-K-03 / OQ-GF-003：是否强制在 Contract/治理文档加双标注。

### 4.4 建议的受控同义词（待 Owner 冻结）

| 提案用语 | 含义 | 替代的歧义用语 |
|----------|------|----------------|
| `source_bytes_sha256`（带 `bytes_kind` 标签） | 分层 source 字节 hash | 裸写 “original sha” |
| `pdf_source_sha256` | L1 | OCR 清单的 `source_sha256`（保留原字段名作 legacy 别名） |
| `ocr_md_source_sha256` | L2 | `source_content_sha256`（接口键，存量零迁移优先保留原名） |
| `archive_path_locator` | 仅路径 | 不得命名为 *identity* |

- `[FACT]` Papers log：历史裁决倾向「命名保守义 / 存量零迁移」——接口键保留 `source_content_sha256`。
- `[INFERENCE]` 治理层宜加**标签**而非重命名存量键，以免违反零迁移原则。

---

## 5. Lineage Completeness Classes

| Class | 定义 | 当前观测 |
|-------|------|----------|
| **A — Hash-closed** | L1 hash 与 L2 hash 均有登记载体且可复算对账 | `[FACT]` 样本与接口面 87/71 子集 |
| **B — Locator-only** | 仅有 path/文件名，无字节 hash 登记 | `[FACT]` 大量源 md；清单未覆盖 |
| **C — Conflicted** | 不同载体对同一对象给出不一致主张 | `[FACT]` 例如 CLOSURE-PLAN 将 12,707 系于 original/（数字实为 maintainess/PDF） |
| **D — Missing** | 无路径登记且无 hash | `[UNKNOWN]` Papers 之外上游（UNKNOWN-005） |

**Migration rule（提案）**:

- Class A：可作为迁移证据输入（仍须 Gate）。
- Class B：默认 **不得** 宣称「来源已验证」；可迁时必须降级标注 `locator-only`。
- Class C：必须进入冲突登记并等 Owner/对账关闭。
- Class D：禁止进入迁移候选。

---

## 6. Validation Methods（治理要求）

| 检查 | 方法 | 适用层 |
|------|------|--------|
| V-Bytes | 标准库独立重算 sha256，fail-closed | L1–L2 |
| V-Manifest | 清单/manifest 字段 ↔ 现算 | L1–L4 |
| V-Snapshot | 接口快照 vs 当前磁盘/IR | L2–L4 |
| V-Gate | Migration Gate 1–10 记录 | L6 |
| V-Admission | 唯一入口 + payload 可重放 | L5–L6 |
| V-Stage | `logical_execution_stage/hash` 成对校验 | L3–L5 |

- `[FACT]` Contract 要求 bytes verification：可得 raw bytes / 标准库独立重算 / fail-closed / 独立于 IR。
- `[FACT]` REPORT-I：迁移记录必须保留 UNKNOWN/冲突/known-issue，禁止静默丢弃。

---

## 7. Open Items Referenced

见 `GF-005-OPEN-QUESTIONS-REGISTRY.md`：`OQ-GF-001` 双树关系、`OQ-GF-003` 词义冻结、`OQ-GF-007` lineage 补全、`OQ-GF-002` 数据权威模式、`OQ-GF-008` 全量 hash 台账等。

---

*GF-002 · DRAFT · TASK-GF-001 · 2026-09-17 · 仅新建治理草案，未改源仓*
