# GF-000 — Governance Foundation Baseline（总述草案）

**Document ID**: GF-000
**Status**: `DRAFT / PROPOSED` — **不是** Frozen Authority；不授权迁移
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17
**Scope**: AITutor-X 迁移治理基线（文档 foundation，非实现、非迁移、非改码）
**Child documents**:
- `GF-001-SOURCE-AUTHORITY-MODEL.md`
- `GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md`
- `GF-003-MIGRATION-EVIDENCE-CONTRACT.md`
- `GF-004-MIGRATION-BOUNDARY-DEFINITION.md`
- `GF-005-OPEN-QUESTIONS-REGISTRY.md`

**Evidence classification**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**Hard rules observed**: 未改代码；未改既有报告；未改目录名；未迁移数据；未改 DB schema；未假设 maintainess 权威；未假设 original 权威。

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
| Migration Authority | Charter 未设立 | `[DECISION REQUIRED]` F4 |

### 2.2 Open blocking clusters（继承 REPORT-H/I，不在本轮关闭）

| Cluster | 阻塞内容 | 关联 OQ-GF |
|---------|----------|------------|
| A | Migration Authority / Gate 批准 / Taxonomy / Set B | 014, 015, 013 |
| B | Design v1.1 / untracked / D2-D4 / Contract 状态叙事 | 017 |
| C | DEC/BUG/OQ 命名空间 | 016 |
| D | 数据权威模式 / scripts·ocr_service 范围 / 绝对路径 | 002, 001 |
| E | 测试基线 / r67 / frontend 范围 | 018 |
| Lineage | 双树权威、lineage 补全、文档口径 | 001, 004, 007, 011 |

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

### 3.2 Directory roles（观测，非权威）

| Path | 角色 | 权威主张 |
|------|------|----------|
| `original/` | RSD 候选库 A | `[UNKNOWN]` |
| `maintainess/PDF` | PIS 操作输入根 `[FACT]` | 是否兼 RSD `[UNKNOWN]` |
| `maintainess/` 整目录 | Case C mixed asset `[FACT]` | 不得单一定性 |
| `Ocr-markdown/` | OCRA 产出区 `[FACT]` | n/a |

**提案硬规则**: Path ≠ Role；Role ≠ Authority；双树显式并列直至 Owner 裁决；引用优先 hash。

**明确不假设**（任务书 Forbidden）:
- ❌ maintainess = authoritative
- ❌ original = authoritative

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

共 **18** 条 `OQ-GF-001`～`018`；**9** 条 OPEN-BLOCKING。本角色 **零关闭**。

| 优先级 | ID | 问题 |
|--------|-----|------|
| P0 | OQ-GF-001 | 权威原始来源（maintainess / original / 双层） |
| P0 | OQ-GF-002 | 数据权威引用/交付模式 |
| P0 | OQ-GF-004 | 双树重叠副本策略 |
| P0 | OQ-GF-014 | Migration Authority / Gate 批准 |
| P0 | OQ-GF-015 | 唯一 Authority Taxonomy |
| P0 | OQ-GF-016 | DEC/BUG/OQ 命名空间 |
| P0 | OQ-GF-017 | Design/untracked authority + D2-D4 |
| P0 | OQ-GF-018 | 测试基线 / r67 / frontend |
| P1 | OQ-GF-007 | lineage 补全责任 |
| P1 | OQ-GF-003 | identity 词义 vs 目录双标注 |
| P1 | OQ-GF-005/008/009/011/012/013 | 恢复标准 / hash 台账 / re-index / 文档口径 / 首跑效力 / Set B |

关闭协议：仅 Owner 书面裁决或可复现新证据；禁止以进度压力将 OPEN 默认化。

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

**本文件不执行下列动作**；仅向 Owner / Evidence Reconciler 提供排序建议。

### Phase 0.5 — Owner 决策批（阻塞一切迁移）

1. 裁决 **OQ-GF-001** 权威原始来源模型（含是否接受「双层」表述）。
2. 裁决 **OQ-GF-002** 数据权威模式（建议默认：hash 清单 + 只读 locator，数据本体不迁）。
3. 设立 **Migration Authority Charter（F4）** 并批准 Gate 版本（F5）。
4. 指定 **唯一 Authority Taxonomy（F3）**。
5. 裁决 **OQ-GF-003** 是否强制 identity/目录双标注。

### Phase 0.6 — Evidence hardening（可与决策并行，仍不迁数据）

6. Owner 决定 **OQ-GF-008** 是否立项全量 source hash inventory（范围/存放）。
7. Owner 决定 **OQ-GF-007/009** lineage 补账或 re-index 的 Producer 任务书。
8. 处置 untracked Design/Contract 族（commit 或书面降级）。
9. 导入 Set B 或书面豁免（F10）。
10. 受控环境重跑测试，固化 baseline（F9）。

### Phase 1 — Governance freeze of GF docs（仅文档）

11. Owner 评审 GF-000～005；批准后将 Status 从 `DRAFT` 升为治理基线（版本化，不覆盖）。
12. 若 F3/F6 已裁，为 REPORT 与 GF 建立 taxonomy/namespace 映射（新文件，不改旧报告）。

### Phase 2 — Migration start（前置全绿后）

13. 仅对 **Class A / YES 类资产** 按 Gate 1–10 建 EvidencePackage。
14. Frozen Contract 副本 → `30_CONTRACTS/`（字节一致）。
15. V3 Frozen Spec → `10_SPEC/`。
16. Lineage manifests → 证据区（只读）。
17. 每步写 migration record；UNKNOWN 保留。

**明确非目标（下一阶段仍禁止）**: 数据树整体拷贝；改 Frozen 文档；无 Gate 的代码迁入；以目录名证明 provenance；Agent 自封 Frozen/Authority。

---

## 10. Deliverable Index

| File | 内容 |
|------|------|
| `GF-000-FOUNDATION-BASELINE.md` | 本文件：九节总述 |
| `GF-001-SOURCE-AUTHORITY-MODEL.md` | RSD/PIS/OCRA/SEM/MIG + 目录角色 |
| `GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md` | L1–L6 身份/hash/归属/校验 + 词义分辨 |
| `GF-003-MIGRATION-EVIDENCE-CONTRACT.md` | EvidencePackage + 失败处置 |
| `GF-004-MIGRATION-BOUNDARY-DEFINITION.md` | YES/NO/CONDITIONAL |
| `GF-005-OPEN-QUESTIONS-REGISTRY.md` | OQ-GF-001～018 |

**Upstream evidence (unchanged)**: REPORT-A～I、REPORT-K；V3_SPEC；Contract v0.2 四元组；Papers 账本/log。

---

## 11. Success Criterion Check

> 未来工程师应能理解：**Which data can enter AITutor-X, why it is trusted, and what evidence proves its origin**，而不知道历史 preprocessing 实现细节。

| 问题 | 本基线的落点 |
|------|----------------|
| Which data can enter? | GF-004 YES/NO/CONDITIONAL + Gate 停止线 |
| Why is it trusted? | GF-001 角色权威 + GF-003 证据原则 + Contract/V3 frozen 锚 |
| What evidence proves origin? | GF-002 分层 hash + EvidencePackage + Completeness Class |

---

*GF-000 · DRAFT · TASK-GF-001 · Independent System Governance Architect · 2026-09-17*
*仅新建 Docs/00_GOVERNANCE/GF-*.md；未修改代码、既有报告、目录名、数据；未迁移；未假设 maintainess/original 权威。*
