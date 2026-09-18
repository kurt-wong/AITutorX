# GF-000 — Governance Foundation Baseline

**Document ID**: GF-000
**Status**: `FROZEN GOVERNANCE BASELINE` — 文本版本已冻结（OD-14）；**不**授权迁移；**不**代表 Gate Passed
**Version**: **v0.2 Frozen**（TASK-GF-005 document patch + **TASK-GF-008 Owner Decision Resolution & Freeze Text Solidification**；v0.1 @ `5010c16` 内容保留）
**Role**: Independent System Governance Architect（TASK-GF-001）；**Freeze decision actor = Owner（OD-14）**
**Date**: 2026-09-17（v0.1） / 2026-09-18（v0.2 patch） / **2026-09-18**（v0.2 freeze + owner decisions）
**Scope**: AITutor-X 迁移治理基线（文档 foundation，非实现、非迁移、非改码）
**Child documents**:
- `GF-001-SOURCE-AUTHORITY-MODEL.md`
- `GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md`
- `GF-003-MIGRATION-EVIDENCE-CONTRACT.md`
- `GF-004-MIGRATION-BOUNDARY-DEFINITION.md`
- `GF-005-OPEN-QUESTIONS-REGISTRY.md`
- `GF-006-OWNER-DECISION-RECORD.md`（**决策正典**；TASK-GF-008）

**Evidence classification**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**v0.2 addition labels**: `[FACT]` / `[OBSERVED]` / `[PROPOSAL]` / `[OWNER DECISION REQUIRED]` / `[UNKNOWN]`
**v0.2 freeze labels**: `[OWNER DECISION]`（Owner 已裁决，见 GF-006）；`[OWNER DECISION REQUIRED]` 仅用于 **未裁决** 事项
**Hard rules observed**: 未改代码；未改既有报告；未改目录名；未迁移数据；未改 DB schema；未假设 maintainess 权威；未假设 original 权威；**TASK-GF-008 未关闭任何 OQ/BL/D-048**；未创建 Registry 实例。

**Repositories inspected (read-only)**:

| Repo | Path | Observed HEAD / remote |
|------|------|------------------------|
| Governance | `D:\Project\AITutor-X` | `659db9b47e82123d8698ff6b9ab9615adf0f59ad`；remote `kurt-wong/AITutorX` |
| Consumer | `D:\Project\AITutors-v3` | remote main 观测 `cc12d79…`（Papers CURRENT 记载）；V3_SPEC frozen |
| Producer | `D:\Project\Papers` | `2b92898f…` == origin/main；remote `kurt-wong/Aitutors-preprocessing` |

---

## 1. Executive Summary

AITutor-X 正从历史实验流水线迁入受治理架构。本轮交付 **治理文档基线**（GF-000～005），使未来工程师能回答：

> **哪些数据可以进入 AITutor-X、为何被信任、什么证据证明其来源**——而无需掌握 preprocessing 历史实现细节。

### 1.1 Confirmed facts（本轮采信的仓库现实）

1. `[FACT]` 三仓角色：AITutor-X = 治理/迁移目标；AITutors-v3 = 目标架构与 Frozen V3_SPEC；Papers = Producer（OCR/preprocessing）。
2. `[FACT]` 现行 OCR **operational input path** = `D:\Project\Papers\maintainess\PDF`（代码 `batch_convert_pdf.py:55` + 日志 + 恢复后 12,707 PDF）。
3. `[FACT]` `original/` 为更大原件树（PDF 38,893 / 115G）；与 maintainess/PDF basename 交集 12,626；抽样 6/6 sha256 一致。
4. `[FACT]` 两树与 `Ocr-markdown/` 均 **不在 git**（`.gitignore`）；baseline 无法仅从 git 重建。
5. `[FACT]` 存在 **双层 sha 语义**：OCR 清单 `source_sha256`=PDF 字节；manifest/IR `source_content_sha256`=OCR md 字节。
6. `[FACT]` identity 词面 `SHA256(original source bytes)` ≠ 目录 `D:\Project\Papers\original` 的证明。
7. `[FACT]` Contract v0.2 已冻结：`kurt-wong/AITutors-v3 @ f4941ff…` / `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` / sha256 `9c6b9063…7528`；`source_content_sha256`=Identity Authority；path 仅 locator。
8. `[FACT]` lineage 覆盖 **PARTIAL**：接口面 87/71 可 hash 闭合；大量源 md 无正文 lineage、无清单条目。
9. `[FACT]` `AGENTS.md` 五原则：Provenance≠Quality；UNKNOWN retained；Producer/Consumer 边界；Git≠Authority；Gate 前禁入 active tree。
10. `[FACT]` REPORT-I：Cluster A 未关闭前 **默认全面禁止迁移**；F1–F10 多项仍 open。
11. `[FACT]` AITutor-X 无 REPORT-J；Observation Set B 未导入。

### 1.2 What this foundation does NOT do

- 不裁决权威原始来源（OQ-GF-001）
- 不批准任何迁移
- 不修改 Frozen Contract / V3_SPEC / REPORT-A～K
- 不把 UNKNOWN 升格为 FACT
- 不引入新数据库 schema

### 1.3 Hard Rule — Frozen Governance Baseline ≠ Migration Authorization

`[OWNER DECISION]` **OD-14（2026-09-18，GF-006 §1）**: Owner 批准 GF v0.2 升格为 **Frozen Governance Baseline**。冻结范围 = GF v0.2 文档体系（GF-000～006）。冻结 **仅**表示规则版本固定、后续引用有明确基线、变更走受控 patch 不覆盖历史版本。

**冻结声明（Owner 要求必须写入）**:

```text
Frozen Governance Baseline does not imply Migration Authorization.

Frozen Governance Baseline（治理文档冻结状态）
    ≠
Migration Authorization（迁移执行授权）

「Frozen」明确不代表：
  - 数据已经迁移
  - Migration approval
  - Migration Gate 执行力 / Gate Passed
  - Gate 9 通过
  - Migration Ready
  - 数据/代码可以进入 AITutor-X active tree

Migration Authority ≠ Migration Execution
Decision ≠ Migration Approval
```

`[FACT]` 依据: REPORT-I F4「Migration Authority Charter 未设立」；F5「REPORT-I 为草案」；GF-003 §3.2.2 `approval_block`；REPORT-I §0.7 Cluster A 未关前默认禁止迁移。

`[OWNER DECISION]` **OD-01（GF-006 §2）**: 建立 Migration Authority Charter；**当前不授予任何迁移执行权限**。

```text
Migration Authorization remains unavailable until Charter requirements are satisfied.
```

`[FACT]` Charter 全文与 requirements satisfied 判定条件尚未落盘为独立 Charter 文件。

`[FACT]` 在 Charter requirements 满足且 OQ-GF-014/015、F4/F5 相关执行状态完成前，任何「Gate 9 passed」声明 **无效**。

`[FACT]` 本文件 Status 已由 Owner（OD-14）升格为 Frozen；**TASK-GF-008 未关闭任何 OQ/BL/D-048**。

---

## 2. Current Governance State

### 2.1 Asset & authority snapshot

| 域 | 现状 | 分类 |
|----|------|------|
| Governance repo skeleton | `Docs/00_GOVERNANCE…90_ARCHIVE` 已建；本轮写入 GF 草案 | `[FACT]` |
| Audit reports | REPORT-A～I + REPORT-K 存在；J 不存在 | `[FACT]` |
| Frozen Contract | v0.2 四元组已钉；状态叙事规则未成文于治理仓 | `[FACT]` + F2 open `[DECISION REQUIRED]` |
| V3 Frozen Spec | 00/10/20/30/40/50/90/91/README 冻结可引用 | `[FACT]` |
| Identity modules M1–M5 | V3 内存在；D2/D3/D4 未裁 | `[FACT]` 代码存在；authority `[UNKNOWN]` |
| Untracked design/contract 族 | DESIGN-v1.1 等无 git history | `[FACT]` untracked；authority `[UNKNOWN]` |
| Producer data trees | 大体量、ignored、双树高重叠 | `[FACT]` |
| Lineage manifests | OCR 清单 1801；manifest 166（sha 87）；snapshot 87 | `[FACT]` |
| Test baseline | 两仓结论冲突；r67 本轮未重跑 | `[FACT]` 冲突记录；现行有效性 `[UNKNOWN]` |
| Migration Authority | Charter 建立已裁（OD-01）；requirements **未**满足；迁移执行权限未授予 | `[OWNER DECISION]` 建立 Charter；`[FACT]` Authorization unavailable；OQ-GF-014 / BL-09 仍 OPEN |

### 2.2 Open blocking clusters（继承 REPORT-H/I，不在本轮关闭）

| Cluster | 阻塞内容 | 关联 OQ-GF |
|---------|----------|------------|
| A | Migration Authority / Gate 批准 / Taxonomy / Set B | 014, 015, 013 |
| B | Design v1.1 / untracked / D2-D4 / Contract 状态叙事 | 017 |
| C | DEC/BUG/OQ 命名空间 | 016 |
| D | 数据权威模式 / scripts·ocr_service 范围 / 绝对路径 | 002, 001 |
| E | 测试基线 / r67 / frontend 范围 | 018 |
| Lineage | 双树权威、lineage 补全、文档口径 | 001, 004, 007, 011 |

### 2.3 FACT Measurement Metadata Discipline（v0.2 增补）

`[PROPOSAL]` v0.2 起，治理文档中出现的**数字类 FACT**（计数、hash 前缀、覆盖率、match 率等）应支持下列三项元数据，避免「裸数字」被误读为当前仍有效的 verified 结论：

| Field | Meaning | 填写要求 |
|-------|---------|----------|
| `measurement_method` | 该数字如何被测得 | 如 `full_inventory` / `sample_recompute` / `manifest_crosscheck` / `git_ls_files` / `owner_attested` / `log_parse`；不可考 = `UNKNOWN` + 原因 |
| `measurement_timestamp` | 该数字对应的观测时点 | 显式时区；绑定恢复/变更前后 observation；不可考 = `UNKNOWN` + 原因 |
| `source_reference` | 该数字的登记载体 | 如 `REPORT-K §x` / `Papers CURRENT.md` / `interface_scope_snapshot_step1.json` / `git ls-files@e1beba3` |

`[FACT]` 依据（数字确存在于源账本；**本节不改变这些 FACT 的既有含义**）:

| 数字 | source_reference | measurement_method / timestamp（源侧可得部分） |
|------|------------------|-----------------------------------------------|
| maintainess/PDF 恢复后 12,707 | REPORT-K §1.11；Papers 恢复后复测 | 恢复后盘点 `[OBSERVED]`；恢复前全量 hash = `[UNKNOWN]`（UNKNOWN-004） |
| original/ PDF 38,893 | REPORT-K §2.1 | 体量盘点 `[OBSERVED]` |
| OCR 清单 1,801 | `data/ocr_output_manifest.jsonl` | 清单条目计数 `[FACT]` |
| manifest 166 / sha 键 87 | `Ocr-markdown/**/*.manifest.json`；REPORT-K | 清单交叉 `[OBSERVED]` |
| snapshot n_rows=87 / match 87 | `interface_scope_snapshot_step1.json` | manifest/snapshot 对账 `[FACT]` |
| IR ADMITTED match 71 | 同上 / Papers log | 对账 `[FACT]` |
| AITutorX REPORT-G/H/I/K untracked | `git status` / `git ls-files` @ HEAD `e1beba34857c5332a910901b8f4a409cb4119235` | git 跟踪面检查 `[FACT]` |

`[PROPOSAL]` 后续治理文档引用上述数字时，应尽量附 `measurement_method` + `measurement_timestamp` + `source_reference`；无法附全时必须显式写缺口，**禁止**把历史观测裸数字写成「当前全量 verified」。

`[UNKNOWN]` 部分历史数字的精确测量时点不可考（如部分 REPORT 叙述中的计数未单列 timestamp）；不因本节自动升格或改写。

---

## 3. Proposed Authority Model（详见 GF-001）

### 3.1 Role-based（非 path-based）角色

| Role | 含义 | 关键点 |
|------|------|--------|
| **RSD** Raw Source Document | 最初接收的原件字节 | 身份=sha256(bytes)，≠目录名 |
| **PIS** Processing Input Snapshot | 某次执行实际消费的文件+hash 集合 | 当前操作观测=maintainess/PDF；历史字节级 `[UNKNOWN]` |
| **OCRA** OCR Artifact | OCR 产出 md 等 | 清单覆盖不全 |
| **SEM** Semantic Artifact | manifest/IR/批注/快照 | `source_content_sha256` 钉 md 字节 |
| **MIG** Migration Artifact | 过 Gate 后进入 AITutor-X 的资产 | Git presence ≠ Authority |

### 3.2 Directory roles（观测，非权威；OD-04 Hash-based Source Identity）

| Path | 角色 | 权威主张 |
|------|------|----------|
| `original/` | RSD 候选库 A / 输入来源 | `[UNKNOWN]` 是否 canonical；**不**永久排序（OD-04） |
| `maintainess/PDF` | PIS 操作输入根 `[FACT]`；亦为输入来源 | 是否兼 RSD `[UNKNOWN]`；**不**永久排序（OD-04） |
| `maintainess/` 整目录 | Case C mixed asset `[FACT]` | 不得单一定性 |
| `Ocr-markdown/` | OCRA 产出区 `[FACT]` | n/a |

`[OWNER DECISION]` **OD-04（GF-006 §5）**: 采用 **Hash-based Source Identity Model**。数据身份由 **content hash** 决定；`original/` 与 `maintainess/PDF` **均作为输入来源**；content hash 一致 ⇒ 同一 Source Identity。是否可进入 AITutor-X 由 validation / test corpus / processing result 决定，**不**由目录名或永久 Source Authority 排序决定。

`[FACT]` 硬规则: Path ≠ Role；Role ≠ Authority；引用优先 hash。

`[OWNER DECISION]` **不指定**（OD-04 Important Correction）:
- ❌ maintainess = canonical
- ❌ original = canonical

### 3.3 Artifact Registry 总则（v0.2 增补；OD-10 已裁建立）

`[OWNER DECISION]` **OD-10（2026-09-18，GF-006 §3）**: **建立 Artifact Registry**，用于记录治理认可的 Artifact，解决 `exists` / `tracked` / `referenced` / `admitted` 状态混淆。

`[FACT]` **本任务只固化 Registry 建立决策。禁止**: 创建 Registry 数据实例；导入 Artifact；修改 `admitted` 状态。当前仍无 Registry 实例落盘；`admitted` 保持 `[UNKNOWN]`。

`[PROPOSAL]`（Registry 总则文本，在 Registry 实例运营前作为引用纪律）: 治理侧引入 **Artifact Registry** 概念：对进入治理引用面的工件做**分类登记**，区分「存在于磁盘」与「被治理引用/准入」，避免 untracked / 未处置工件被静默当作权威。

#### 3.3.1 Registry Classes `[PROPOSAL]`

| Class | Meaning | 当前示例 `[OBSERVED]` |
|-------|---------|------------------------|
| **GOV** — Governance Authority Artifact | 治理协议、GF 文档、Frozen Spec/Contract 副本 | GF-000~006（tracked；Status=FROZEN GOVERNANCE BASELINE @ TASK-GF-008）；V3_SPEC 冻结分册 |
| **EVD** — Evidence Artifact | 审计报告、manifest、快照、DQ/ledger | REPORT-A~F（tracked）；`ocr_output_manifest.jsonl`；`interface_scope_snapshot_step1.json` |
| **EXT** — External Capability Artifact | 外部引擎/模型/契约（非本仓字节权威） | PaddleOCR / PP-StructureV3；本地 embedding；DISPLAY_CONTRACT 等 `[OBSERVED: V3 50 §3]` |
| **Working** — Working Artifact | 过程性工件，非治理权威 | 会话中间态；临时导出 |
| **Temporary** — Temporary Artifact | 默认禁入治理引用面 | REPORT-K 过程态 6 文件 `[FACT: 已禁作语料结论]` |

详细角色定义见 GF-001（GOV/EVD/EXT）。本节为 Registry 总则。

#### 3.3.2 Citation State — untracked / in-repo 工件引用效力 `[PROPOSAL]`

任何被 GF/REPORT/Gate 引用的工件，引用时必须区分四个状态，**禁止**把「磁盘存在」直接写成「治理已登记/已准入」:

| State | Meaning | 当前观测示例 `[FACT: git + 磁盘]` |
|-------|---------|-------------------------------------|
| `exists` | 文件在磁盘上可读取 | REPORT-G/H/I/K 均 exists |
| `tracked` | 在 git 跟踪面内（有 blob 历史） | REPORT-A~F tracked；G/H/I/K **untracked** |
| `referenced` | 被 GF/REPORT 正文引用 | GF-000~005 多处引用 REPORT-I/K；REPORT-G/H 亦被 REVIEW 引用 |
| `admitted` | 经治理登记 + Owner/Charter 处置后进入 registry | `[UNKNOWN]` — Registry **建立**已裁（OD-10）；**实例未创建**；无 admission 记录 |

`[FACT]` AITutor-X untracked governance reports（TASK-GF-004-A 核实 @ `e1beba3`；TASK-GF-008 时点 untracked 状态未变）:

| Artifact | exists | tracked | referenced | admitted |
|----------|--------|---------|------------|----------|
| `REPORT-G-*` | YES | NO | YES（REVIEW/GF） | `[UNKNOWN]` |
| `REPORT-H-*` | YES | NO | YES（REVIEW/GF） | `[UNKNOWN]` |
| `REPORT-I-*` | YES | NO | YES（GF-000~005、REPORT-K） | `[UNKNOWN]` |
| `REPORT-K-*` | YES | NO | YES（GF-000~005） | `[UNKNOWN]` |
| `REPORT-J` | **NO** | n/a | OQ-GF-013 记录「不存在」 | n/a |

`[OWNER DECISION]` **OD-06（GF-006 §8）**: REPORT-G/H/I/K 采用 **整理后收编**；流程 = Evidence Package → identity information → Artifact Registry → 再改变 admission 状态。**当前不得直接认为 `admitted=true`。** BL-11 / OQ-GF-013 仍 OPEN。

`[FACT]` 引用规则（Registry 实例运营前有效）:
1. `exists`/`referenced` **不等于** `admitted`。
2. untracked 且未 Owner 处置 ⇒ `authority_status` 不得写 `verified`（与 GF-003 §6 一致）。
3. 冻结/迁移/「已证实」类主张引用 untracked 工件时，必须同时标注 citation state + 缺口。
4. Registry 实例文件（清单/ledger）的落盘路径与格式 = 仍待运营层落盘（OD-10 仅裁「建立」）。

`[OWNER DECISION REQUIRED]` Registry 实例路径/格式/admission 流程运营细节；Set B / REPORT-J（OQ-GF-013 未在本批裁决部分）。

---

## 4. Proposed Lineage Model（详见 GF-002）

### 4.1 强制链与身份

```text
L1 Source PDF          source_pdf_sha256 = sha256(pdf bytes)
        ↓
L2 OCR output          ocr_md_sha256 = sha256(ocr md bytes)
        ↓
L3 Semantic annotation stage identity (stage + logical_execution_hash)
        ↓
L4 Question IR         历史 ir.source_sha256 = md bytes（非 PDF）；V3 中 IR transient
        ↓
L5 Admission Candidate input_identity + build_versions + Gate 证据
        ↓
L6 AITutor-X Entity    source_repo@commit + path + sha256 + migration_record
```

### 4.2 `SHA256(original source bytes)` 受控释义

| 维度 | 裁决性表述 |
|------|------------|
| **语义** `[FACT]` | 对该工件声明的上游 **source 字节** 做 SHA-256（64 小写 hex）；“original” 修饰 bytes 关系 |
| **分层** `[FACT]` | OCR 清单层=PDF 字节；manifest/IR/接口层=OCR md 字节 |
| **目录** `[FACT]` | `D:\Project\Papers\original` 是路径；词面 **不** 证明目录级来源 |
| **禁令** | 词面含 original ⇒ 断言源目录=original/ ❌；目录名 original ⇒ 自动权威 ❌ |
| **待裁** | 是否强制文档双标注 = OQ-GF-003 / OD-K-03 `[DECISION REQUIRED]` |

### 4.3 Completeness classes

| Class | 含义 | 迁移含义（提案） |
|-------|------|------------------|
| A Hash-closed | 双层 hash 可对账 | 可作证据输入（仍须 Gate） |
| B Locator-only | 仅 path | 禁止称 verified |
| C Conflicted | 载体互相矛盾 | 进冲突登记，等 Owner |
| D Missing | 无登记 | 禁止候选 |

---

## 5. Migration Boundary（详见 GF-004）

### 5.1 YES 类别（仍须 Gate，非立即放行）

- Frozen Contract 副本（字节一致）
- V3 Frozen Spec 副本
- 已 tracked 的治理协议 / 协调账本（标 mirror vs canonical）
- Lineage manifests 与证据账本（清单/快照/DQ）
- Semantic/Candidate **契约与代码**（数据本体另议）
- 经适配后的测试文件与合规代码模块

### 5.2 NO 类别

- 实验脚本、临时目录、会话过程态
- 过时预处理实验 / V2 pipeline·表·镜像·特判模式
- 历史转换工件本体（可只读归档）
- 未处置 untracked 文档
- **大体量原始语料本体**（默认，直至数据模式裁决）
- 整仓 directory copy

### 5.3 CONDITIONAL

- untracked Design/Contract 族 → Owner 处置
- M1–M5 → D2/D3/D4
- DEC/BUG 文档 → F6 namespace
- 数据/IR 本体 → OD-009 / OQ-GF-002
- Class B/C lineage → 补账或冲突关闭

---

## 6. Required Evidence Gates（详见 GF-003；Gate 编号沿用 REPORT-D/I）

| Gate | 要求摘要 |
|------|----------|
| 1 Source identified | repo + commit + path + role |
| 2 Authority identified | authority_status + frozen_ref + OD 引用 |
| 3 Validity verified | hash 复算 fail-closed；测试基线（适用时） |
| 4 Historical status | 代码/资产分类；归档判定 |
| 5 Duplicate check | 对 AITutor-X 既有资产比对 |
| 6 Arch compatibility | 路径抽象 / Docker·env / import（代码） |
| 7 Evidence attached | EvidencePackage 完整（含 gaps） |
| 8 Migration class | YES/NO/CONDITIONAL（GF-004） |
| 9 Governance approval | Migration Authority + Owner（F4/F5） |
| 10 Migration record | 账本条目；UNKNOWN 保留 |

**EvidencePackage 必填核心**: `source_repo/commit/path` · `bytes_kind` · `content_sha256` + `hash_meaning` · `verification.method/result` · `producer_version`（可考）· `authority_status` · `gaps[]` · `owner_decision_refs[]`。

**失败处置**: mismatch ⇒ BLOCK；not_verified ⇒ 不得称 verified；冲突 ⇒ 并列保留不改旧报告。

**停止线**: Cluster A 未关 ⇒ 默认禁迁；例外仅 Owner 书面只读证据副本。

---

## 7. Open Questions（详见 GF-005）

共 **18** 条 `OQ-GF-001`～`018`。TASK-GF-008 后 Status 摘要:

- **零 OQ 标记 CLOSED**（关闭协议未以本批决策自动触发；OD-18 **明示**不关闭 OQ-GF-007）
- 部分条目已有 `[OWNER DECISION]` 注记（见 GF-005 §7 / GF-006）: 001←OD-04；002←OD-05；007←OD-18（不关）；013←OD-06；014←OD-01；015←OD-03
- **仍 OPEN-BLOCKING（执行状态未完成）**: 001、002、004、007、014、015、016、017、018
- BL-09 / BL-10 / BL-11 保持 OPEN（GF-005 §4.2 / GF-006 §9）
- D-048 保持 `pending_owner_decision`

| 优先级 | ID | 问题 | Owner Decision（本批） |
|--------|-----|------|------------------------|
| P0 | OQ-GF-001 | 权威原始来源（maintainess / original / 双层） | OD-04 Hash-based Source Identity；**不**关闭 |
| P0 | OQ-GF-002 | 数据权威引用/交付模式 | OD-05 NAS-backed read-only；实施细节 OPEN |
| P0 | OQ-GF-004 | 双树重叠副本策略 | 本批未裁；仍 OPEN-BLOCKING |
| P0 | OQ-GF-014 | Migration Authority / Gate 批准 | OD-01 建立 Charter；Authorization unavailable；执行状态 OPEN |
| P0 | OQ-GF-015 | 唯一 Authority Taxonomy | OD-03 分层模型（Domain + Artifact Role）；完整执行 OPEN |
| P0 | OQ-GF-016 | DEC/BUG/OQ 命名空间 | 本批未裁 |
| P0 | OQ-GF-017 | Design/untracked authority + D2-D4 | 本批未裁 |
| P0 | OQ-GF-018 | 测试基线 / r67 / frontend | 本批未裁 |
| P1 | OQ-GF-007 | lineage 补全责任 | OD-18 Difference Ledger；**明示不关闭** |
| P1 | OQ-GF-003 | identity 词义 vs 目录双标注 | 本批未裁 |
| P1 | OQ-GF-013 | Set B / REPORT-J / REPORT-G~K | OD-06 整理后收编；admission 未完成 |
| P1 | OQ-GF-005/008/009/011/012 | 恢复标准 / hash 台账 / re-index / 文档口径 / 首跑效力 | 本批未裁 |

关闭协议：仅 Owner 书面裁决或可复现新证据；禁止以进度压力将 OPEN 默认化。**记录 Decision ≠ Status 自动 CLOSED**（见 GF-005 §5 / GF-006 §9）。

---

## 8. Risks

| Risk | Level | 说明 | 缓解（提案，非执行） |
|------|-------|------|----------------------|
| 双树权威未裁却按单一目录引用 | **HIGH** | 可能固化错误 provenance | GF-001 强制双列；hash 优先 |
| identity 词面被读成目录 | **HIGH** | 错误把 original/ 当唯一源 | GF-002 §4 禁令；OQ-GF-003 |
| lineage 覆盖不足却宣称 verified 迁移 | **HIGH** | 不可审计数据入 active tree | Class A/B/C/D；Gate 7 |
| 无 Migration Authority 的“Gate 9 通过” | **HIGH** | 伪授权 | F4 前任何批准无效 |
| Untracked 文档丢失 | **HIGH** | Design v1.1 等无 git history | Owner 先处置（REPORT-D） |
| 文档口径漂移（12,707 归属等） | **MED** | 继续误导后续工程师 | OQ-GF-011；不改冻结文档，另建更正载体 |
| 测试基线冲突 | **MED** | “迁移后等价”不可证 | OQ-GF-018；受控重跑 |
| 绝对路径 `D:\Project\Papers\...` | **MED** | 迁入代码固化脆弱 locator | Gate 6 路径抽象 |
| 误把 REPORT-K 过程态（6 文件）当语料 | **MED** | 错误 corpus 结论 | REPORT-K §1.11 已禁入治理结论 |
| 把 GF 草案误认为已冻结权威 | **MED** | 越权引用 | 各文件 Status=`DRAFT/PROPOSED` |
| Set B 缺失下的对账空洞 | **LOW-MED** | 外部主张无法核验 | OQ-GF-013 |
| 硬编码 secret / 无 .env 迁入 | **MED**（安全） | 违反全局安全规则 | 迁移代码审查触发 security-reviewer |

---

## 9. Recommended Next Phase

**本文件不执行下列动作**；仅向 Owner / Evidence Reconciler 提供排序建议。状态基于 TASK-GF-008 之后。

### Phase 0.5 — Owner 决策批（已完成部分）

1. ~~裁决 OQ-GF-001 权威原始来源模型~~ → **OD-04** Hash-based Source Identity（**不**关闭 OQ；执行/交付细节仍 OPEN）
2. ~~裁决 OQ-GF-002 数据权威模式~~ → **OD-05** NAS-backed Read-only（**不**关闭 OQ；BL-10 实施细节 OPEN）
3. ~~设立 Migration Authority Charter（F4）~~ → **OD-01** 决定建立 Charter；**requirements 未满足**；迁移执行权限未授予；Gate 版本（F5）本批未裁
4. ~~指定唯一 Authority Taxonomy（F3）~~ → **OD-03** 分层模型（GOV/EVD/EXT + RSD/PIS/OCRA/SEM/MIG）；完整执行状态仍属 BL-09
5. 裁决 **OQ-GF-003** 是否强制 identity/目录双标注 — **仍待 Owner**
6. ~~REPORT-G/H/I/K 处置~~ → **OD-06** 整理后收编；admission 未完成（BL-11 OPEN）
7. ~~Artifact Registry~~ → **OD-10** 决定建立；**实例未创建**
8. ~~71/87/166~~ → **OD-18** Difference Ledger；**OQ-GF-007 不关闭**
9. ~~GF v0.2 Freeze~~ → **OD-14** Frozen Governance Baseline；**不** imply Migration Authorization

### Phase 0.6 — Evidence hardening（仍待 Owner）

10. Owner 决定 **OQ-GF-008** 是否立项全量 source hash inventory（范围/存放）。
11. Owner 决定 **OQ-GF-007/009** lineage 补账或 re-index 的 Producer 任务书（OD-18 已建 ledger 决策，任务书另立）。
12. 处置 untracked Design/Contract 族（commit 或书面降级）— OQ-GF-017。
13. 导入 Set B 或书面豁免（F10）— OQ-GF-013 残余。
14. 受控环境重跑测试，固化 baseline（F9）— OQ-GF-018。
15. **Registry 实例落盘** + REPORT-G/H/I/K 走 OD-06 四步流程 → 才能改 `admitted`。
16. **Charter 正文落盘** + requirements satisfied 判定 → 才能评估 Migration Authorization 可用性。
17. **Difference Ledger 实例落盘** + 71/87/166 disposition 登记。
18. 裁决 **OQ-GF-004** 双树保留/合并；**OQ-GF-016** namespace；**OQ-GF-018** 测试基线。
19. BL-09/10/11 执行状态完成前，**保持 OPEN**。

### Phase 1 — Governance freeze of GF docs

20. ~~Owner 评审 GF-000～005；批准后将 Status 从 DRAFT 升为治理基线~~ → **已执行（OD-14，2026-09-18）**: GF-000～006 Status = `FROZEN GOVERNANCE BASELINE`。后续变更走受控 patch，版本化，不覆盖。
21. 若 F3/F6 执行完成，为 REPORT 与 GF 建立 taxonomy/namespace 映射（新文件，不改旧报告）。

### Phase 2 — Migration start（**仍不开放**）

**停止线（不变）**: Cluster A 未关 ⇒ 默认禁迁；Charter requirements 未满足 ⇒ Migration Authorization unavailable；**Frozen ≠ Migration Authorization**。

22. 仅对 **Class A / YES 类资产** 按 Gate 1–10 建 EvidencePackage（前置全绿后）。
23. Frozen Contract 副本 → `30_CONTRACTS/`（字节一致）。
24. V3 Frozen Spec → `10_SPEC/`。
25. Lineage manifests → 证据区（只读）。
26. 每步写 migration record；UNKNOWN 保留。

**明确非目标（下一阶段仍禁止）**: 数据树整体拷贝；改 Frozen 文档的**含义**（变更须版本化 patch）；无 Gate 的代码迁入；以目录名证明 provenance；Agent 自封 Migration Authority；将 NAS 数据视为 Docker 生命周期数据；将全部数据复制进代码仓。

---

## 10. Deliverable Index

| File | 内容 |
|------|------|
| `GF-000-FOUNDATION-BASELINE.md` | 本文件：总述 + v0.2 增补（§1.3 / §2.3 / §3.3）+ freeze（OD-14） |
| `GF-001-SOURCE-AUTHORITY-MODEL.md` | RSD/PIS/OCRA/SEM/MIG + GOV/EVD/EXT + 目录角色 + OD-03/04/06 |
| `GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md` | L1–L6 + Carrier/Restoration/Integrity（v0.2）+ OD-04/18 对齐 |
| `GF-003-MIGRATION-EVIDENCE-CONTRACT.md` | EvidencePackage v0.1 + v0.2 proposal 字段 + 失败处置 + OD-01 Charter 状态 |
| `GF-004-MIGRATION-BOUNDARY-DEFINITION.md` | YES/NO/CONDITIONAL + V3 50 §3 对齐 + untracked 状态 + OD-05/06 |
| `GF-005-OPEN-QUESTIONS-REGISTRY.md` | OQ-GF-001～018 + blocking_scope + D-048 binding-only + §7 Owner Decision Resolution |
| `GF-006-OWNER-DECISION-RECORD.md` | **决策正典**（TASK-GF-008）: OD-14/01/10/03/04/05/18/06 |
| `REVIEW/GF-003/01–06` | TASK-GF-003-B 设计输入（tracked @ e1beba3） |
| `REVIEW/GF-005/01_GF_V0.2_PATCH_CHANGELOG.md` | TASK-GF-005 补丁变更记录 |
| `REVIEW/GF-006/01_OWNER_DECISION_FREEZE_CHANGELOG.md` | TASK-GF-008 freeze + decision resolution 变更记录 |

**Upstream evidence (unchanged)**: REPORT-A～I、REPORT-K；V3_SPEC；Contract v0.2 四元组；Papers 账本/log。

---

## 11. Success Criterion Check

> 未来工程师应能理解：**Which data can enter AITutor-X, why it is trusted, and what evidence proves its origin**，而不知道历史 preprocessing 实现细节。

| 问题 | 本基线的落点 |
|------|----------------|
| Which data can enter? | GF-004 YES/NO/CONDITIONAL + Gate 停止线 + OD-05 NAS read-only 模型 |
| Why is it trusted? | GF-001 角色权威 + OD-03 分层 taxonomy + OD-04 hash identity + GF-003 证据原则 + Contract/V3 frozen 锚 |
| What evidence proves origin? | GF-002 分层 hash + EvidencePackage + Completeness Class + OD-18 Difference Ledger 引用义务 |

---

*GF-000 · **v0.2 FROZEN GOVERNANCE BASELINE** · TASK-GF-001（v0.1） + TASK-GF-005（v0.2 patch） + **TASK-GF-008（Owner Decision Resolution & Freeze）** · 2026-09-18*
***Frozen Governance Baseline does not imply Migration Authorization.***
*NOT Migration Authorized · NOT Migration Ready · NOT Gate Passed · NOT OQ/BL/D-048 Closed.*
*决策 actor = Owner（OD-14/01/10/03/04/05/18/06，见 GF-006）；文档 actor = document verification only。*
*未修改代码、既有报告、目录名、数据；未迁移；未创建 Registry 实例；未假设 maintainess/original canonical。*
