# GF-002 — Artifact Lineage Specification

**Document ID**: GF-002
**Status**: `FROZEN GOVERNANCE BASELINE`（OD-14）；**不**授权迁移
**Version**: **v0.2 Frozen**（TASK-GF-005 patch + **TASK-GF-008** OD-04/OD-18 对齐）
**Role**: Independent System Governance Architect（TASK-GF-001）；决策 actor = Owner
**Date**: 2026-09-17（v0.1） / 2026-09-18（v0.2 patch） / **2026-09-18**（v0.2 freeze + decisions）
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Decision record**: `GF-006-OWNER-DECISION-RECORD.md`（OD-04 / OD-18）
**Evidence discipline**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**v0.2 addition labels**: `[FACT]` / `[OBSERVED]` / `[PROPOSAL]` / `[OWNER DECISION REQUIRED]` / `[UNKNOWN]`
**v0.2 freeze labels**: `[OWNER DECISION]`
**Forbidden honored**: 不混用 identity 词义与物理目录；**不**指定 maintainess/original canonical（OD-04）；不改代码/数据

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

## 7. Carrier Model（v0.2 增补）

`[PROPOSAL]` v0.2 在 L1–L6 层链（**保留，不废除**）之外，增加 **Carrier（载体）时间维**：同一 path 在不同时点可能持有不同字节状态。hash 归属于某次 **观测（observation）**，不归属于裸路径。

### 7.1 Carrier Model 字段

| Field | Meaning | 填写要求 |
|-------|---------|----------|
| `carrier_state` | 载体在某观测时点的字节/数量状态 | 记 `inventory_claimed` / `inventory_verified` / `bytes_coverage`（full \| sample \| manifest_subset）；state 由 observation 序列推导，**禁止覆盖历史** |
| `observation_time` | 观测时点 | 显式时区 timestamp；不可考 = `UNKNOWN` + 原因；绑定 `observation_id`（若已分配） |
| `as_of_semantics` | 该状态/数字的时点语义 | 枚举 `[PROPOSAL]`: `observation_as_of`（hash/计数属某次观测）/ `inventory_as_of`（目录盘点）/ `assertion_as_of`（文档主张时点，≠ bytes 时点）/ `unknown_time` |

`[FACT]` 依据（**不改变既有 FACT 含义**）: REPORT-K §1.11 — `maintainess/PDF` 会话中途观测仅 6 文件（误删过程态）；Owner 恢复后复测 12,707 PDF。同一路径 `D:\Project\Papers\maintainess\PDF` 不同时点字节状态不同 `[FACT: REPORT-K]`。GF-0.1/§1–§6 无 time/observation 字段 `[FACT: GF-002 v0.1 正文]`。

`[PROPOSAL]` 引用规则:
1. 引用「12,707」必须绑定恢复后 observation；引用首跑日志「12,528/12,703」绑定首跑 observation。
2. **禁止**用最新观测静默覆盖历史观测。
3. 恢复事件前后必须各有 observation，或显式 `not_verified`。
4. REPORT-K「6 文件」态 = incident 观测，**不得**作语料治理结论 `[FACT: REPORT-K §1.11 已禁]`。
5. Completeness Class A/B/C/D 挂在 **Observation** 上，不挂在裸路径。

`[UNKNOWN]` 首跑字节级 Input path 仍为 `[UNKNOWN]`（无 pre-git 快照）— 与 GF-001 §2.2 / OQ-GF-012 一致，不因本节升格。

`[OWNER DECISION REQUIRED]` OQ-GF-001（双树权威）、OQ-GF-005（恢复证据标准）、OQ-GF-006（血缘方向）**不因**本模型关闭。

---

## 8. Restoration Event Model（v0.2 增补）

`[PROPOSAL]` v0.2 登记 **Restoration Event（恢复事件）** 的最小字段集，使治理文档能指向恢复事实，而**不**把恢复写成已完成的完整性证明。

### 8.1 Restoration Event 字段

| Field | Meaning | 填写要求 |
|-------|---------|----------|
| `event_id` | 治理侧恢复事件 ID | 治理分配（如 `REST-<carrier>-<date>`）；源仓已有编号则保留源编号 |
| `source_reference` | 事件记录载体 | 如 `REPORT-K §1.11` / `Papers COORDINATION/CURRENT.md` / Owner 声明载体 |
| `restored_artifact` | 被恢复的载体/集合 | `carrier_id` + locator（locator only）+ 声称数量 |
| `restoration_method` | 恢复方式 | 如 `owner_file_restore` / `git_checkout_recover` / `unknown` |
| `verification_result` | 恢复后验证结果 | `match` \| `mismatch` \| `partial` \| `not_verified`；附 method + 证据引用 |

### 8.2 已观测事件（登记，**不关闭** issue）

| event_id（治理提案） | source_reference | restored_artifact | restoration_method | verification_result |
|----------------------|------------------|-------------------|--------------------|---------------------|
| `REST-maintainess-PDF-2026-09-17` `[PROPOSAL id]` | REPORT-K §1.11；UNKNOWN-004 | `maintainess/PDF`；恢复后声称 12,707 PDF | `[OBSERVED]` Owner 声明误删后恢复；具体字节级来源路径叙事存在冲突候选 `[UNKNOWN: OQ-GF-011]` | `[OBSERVED]` 数量 12,707 + 抽样；**byte_level_equivalence = `not_verified`**（无恢复前全量 hash 台账） |
| D-048-3 关联恢复（tracked 文件）`[OBSERVED]` | Papers `CURRENT.md` / DEC-048；REPORT-F 提及 | Papers git tracked 文件 | `git checkout --` 恢复 `[FACT: Papers 记录]` | git 工作区恢复记录；与 maintainess/PDF 误删恢复 **不是同一事件** `[FACT: 文本对照]` |

`[PROPOSAL]` 硬规则:
1. 登记 Restoration Event **≠** 关闭 restoration issue。
2. **禁止**在 `verification_result=not_verified` 时写「恢复完整性已证实」。
3. `OQ-GF-005`（恢复完整性证据标准：count+sample vs 全量 hash 台账）保持 **OPEN**；本节只提供字段，不裁决标准。
4. 恢复后未复算的 hash 主张，在 EvidencePackage 中必须带 `restoration_event_ref` + gap。

`[OWNER DECISION REQUIRED]` OQ-GF-005 / OD-K-05；恢复证据充分性标准；是否立项全量 hash inventory（OQ-GF-008）。

---

## 9. Integrity Model — interface_integrity vs locator_integrity（v0.2 增补）

`[FACT]` GF-002 v0.1 §6 仅有 V-Bytes / V-Manifest / V-Snapshot / V-Gate / V-Admission / V-Stage，**未**将「接口定义层验证」与「locator→bytes 验证」分列为可独立记录的 integrity 结果。

`[PROPOSAL]` v0.2 **拆分**两类 integrity；**禁止**继续合并为单一 hash validation 结论。

### 9.1 字段定义

| Field | Object | Method | Pass condition |
|-------|--------|--------|----------------|
| `interface_integrity` | 接口/冻结定义层 | manifest/接口键的 `hash_meaning` + 语义 **==** Frozen Contract v0.2 identity 定义（`source_content_sha256` = Identity Authority；path non-identity） | 接口键可复算且与冻结定义一致 |
| `locator_integrity` | 具体 IR/清单条目/文件 | `ir.locator` → 当前 bytes → `sha256 == 登记 sha` | 逐条 match；fail-closed |

### 9.2 不可互相替代 `[PROPOSAL HARD RULE]`

```text
FORBIDDEN:
  interface_integrity PASS  ⇒  locator_integrity PASS   ❌
  locator_integrity PASS    ⇒  全树 lineage 完整         ❌
  合并写成单一 hash_validation=pass 而不分列             ❌

REQUIRED:
  interface_integrity 与 locator_integrity 分列记录
  INTERFACE_VERIFIED ∧ LOCATOR_LINEAGE_BROKEN  ⇒ 该 IR 不得迁移本体
  两者 PASS ∧ coverage_class=A  ⇒ 仅可作数据类 Gate 证据输入（仍须 Gate 9 有效）
```

### 9.3 当前观测数字（分列口径；**不改变既有 FACT**）

| 指标 | 值 | 可支持的结论 | Evidence |
|------|-----|--------------|----------|
| snapshot n_rows | 87 | interface 面规模 `[FACT]` | `interface_scope_snapshot_step1.json` |
| r50 source sha match | 87/87 | **locator** 对账子集 PASS `[FACT]` | 同上 |
| ir_admitted sha match | **71** | locator 对账更小子集 `[FACT]` | 同上 / Papers log |
| manifest 总数 | 166（sha 键 87） | 登记覆盖面 `[FACT]`；**≠** 166 条均已 locator 验证 | REPORT-K；`Ocr-markdown/**` |
| OCR 清单 | 1,801 | L1 锚覆盖面 `[FACT]` | `ocr_output_manifest.jsonl` |

`[PROPOSAL]` 易混读纠正: 「snapshot 87/87 match」**≠**「全部 166 manifest 或全部 IR locator 已验证」。71/87 差值须单独 disposition，不得用 interface 结论掩盖。

`[OWNER DECISION]` **OD-18（GF-006 §7）**: **建立 Difference Ledger**，用于解释 snapshot / manifest / IR admitted 之间差异。后续任何 `87` / `71` / `166` 数字引用 **必须能够关联 difference disposition**。**本决定不关闭 OQ-GF-007。**

`[FACT]` Difference Ledger **实例** 本任务未创建；引用义务自本 freeze 文本生效。

`[OWNER DECISION REQUIRED]` OQ-GF-003（词面/目录双标注）本批未裁；OQ-GF-007 lineage 补全责任仍 OPEN。

---

## 10. Open Items Referenced

见 `GF-005-OPEN-QUESTIONS-REGISTRY.md`：`OQ-GF-001` 双树关系（OD-04 已记 hash identity，OQ 仍 OPEN）、`OQ-GF-003` 词义冻结（未裁）、`OQ-GF-007` lineage 补全（OD-18 不关）、`OQ-GF-002` 数据权威模式（OD-05 NAS read-only，实施 OPEN）、`OQ-GF-008` 全量 hash 台账等。

---

*GF-002 · **v0.2 FROZEN GOVERNANCE BASELINE** · TASK-GF-001（v0.1） + TASK-GF-005（v0.2 patch） + **TASK-GF-008（OD-04/18）** · 2026-09-18*
***Frozen Governance Baseline does not imply Migration Authorization.***
*§7 Carrier · §8 Restoration · §9 Integrity（interface ≠ locator）；L1–L6 与双层 sha 保留。*
*OD-18 Difference Ledger 已裁建立；OQ-GF-007 不关闭；未授权迁移。*
