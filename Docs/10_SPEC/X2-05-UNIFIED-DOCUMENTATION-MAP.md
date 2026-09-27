# X2-05 — Unified Documentation Map

> **[ARCHIVED 2026-09-27]** 本文件已退出主读取路径，**不构成现行依据**。**正文保持原样不改写**（DOC-GOV §7）。
> **Superseded By**: [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../50_OPERATIONS/CURRENT_STATE.md) — 当前状态的唯一权威来源。
> 归档基线：tag `AITutor-X-before-cleanup` @ `43f46e8`。


**Document ID**: X2-05
**Task**: TASK-X2-CLAUDE
**Document Type**: Specification / Documentation Governance Map
**Status**: `ARCHIVED`（原状态：`ACTIVE — X2 DOC MAP`）
**Date**: 2026-09-18
**Upstream**: X2-00 Git FACT；任务书 §5 目标 Docs 结构
**Scope note**: **族级 + 代表路径** map；非 100% 逐文件全量。未逐读文件标 `UNKNOWN`/`UNREVIEWED-FAMILY`。**禁止机械复制。**

---

## 0. Target Docs Structure（AITutorX）

```text
Docs/
├── 00_GOVERNANCE/   # GF v0.2 + 治理协议
├── 10_SPEC/         # 冻结规格 / 术语
├── 20_ARCHITECTURE/ # 统一架构
├── 30_CONTRACTS/    # 跨系统契约
├── 40_DECISIONS/    # 决策映射与登记
├── 50_OPERATIONS/   # 状态 / 账本 / 队列
├── 60_REPORTS/      # 审计报告
└── 90_ARCHIVE/      # 历史归档（不得作现行权威）
```

`[FACT]` 该目录骨架已在 AITutorX tracked（`.gitkeep`）；X2 阶段开始填充。

---

## 1. Classification Vocabulary

`MIGRATE` | `MERGE` | `SUPERSEDE` | `ARCHIVE` | `REJECT` | `RETAIN-AS-HISTORICAL` | `UNKNOWN`

每个族必须登记: source repository / original path / current status / authority / effective scope / superseded by / classification / evidence / dependencies / stale refs / conflicts。

---

## 2. AITutorX 内既有文档

| Family | Path | Status | Authority | Classification | Target | Notes |
|--------|------|--------|-----------|----------------|--------|-------|
| GF v0.2 foundation | `Docs/00_GOVERNANCE/GF-000`…`GF-006` | FROZEN | AITutorX governance | **RETAIN (native)** | 原地 | 不迁移、不替换 |
| GF REVIEW | `Docs/00_GOVERNANCE/REVIEW/**` | historical review | supporting | RETAIN-AS-HISTORICAL | 原地 | 提案/变更日志 |
| REPORT-A~F | `Docs/60_REPORTS/REPORT-A`…`F` | tracked audit | Stage-1 Set A | RETAIN (native) | 原地 | 部分数字/文件名有误，见 X2-07 |
| REPORT-G/H/I/K | `Docs/60_REPORTS/REPORT-G/H/I/K` | **untracked**；exists | authority UNKNOWN until OD-06 | UNKNOWN → 整理后收编 | 待 Registry | **不得 admitted=true** |
| REPORT-J | — | **不存在** | n/a | n/a | n/a | OQ-GF-013 |
| README / AGENTS | 根目录 | ACTIVE | AITutorX operating rules | RETAIN + 更新 | 原地 | X2 后更新状态节 |
| 空骨架 | `preprocessing/ backend/ frontend/ tools/ archive/` + Docs 分册 gitkeep | skeleton | target tree | RETAIN | 原地 | 无代码已迁入 |

---

## 3. V3（AITutors-v3）文档族

Git FACT: HEAD `cc12d79` = origin/main。GitHub Docs 仅含 ARCHIVE/COORDINATION/DECISIONS/REPORTS/V3_SPEC/reference。

### 3.1 V3_SPEC（Frozen L0）

| Family | Path | Status | Authority | Classification | Target | Notes |
|--------|------|--------|-----------|----------------|--------|-------|
| Master Spec 00 | `Docs/V3_SPEC/00_Master_Spec.md` | Baseline—Frozen | L0 | **MIGRATE-candidate** | `Docs/10_SPEC/` | 不改原文；引用+受控副本 |
| Data Model 10 | `Docs/V3_SPEC/10_Data_Model.md` | Frozen | L0 | MIGRATE-candidate | `Docs/10_SPEC/` | schema 权威 |
| Pipeline 20 | `Docs/V3_SPEC/20_Document_Pipeline.md` | Frozen | L0 | MIGRATE-candidate | `Docs/10_SPEC/` | 阶段对象契约 |
| Task/LLM 30 | `Docs/V3_SPEC/30_Task_LLM_Safety.md` | Frozen | L0 | MIGRATE-candidate | `Docs/10_SPEC/` | — |
| Dev Rules 40 | `Docs/V3_SPEC/40_Development_Rules.md` | Frozen | L0 | MIGRATE-candidate | `Docs/10_SPEC/` | — |
| Migration Assets 50 | `Docs/V3_SPEC/50_Migration_Assets.md` | Frozen | L0 | MIGRATE-candidate | `Docs/10_SPEC/` | 与 X2 registry 对照 |
| Doc Governance 90 | `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` | ACTIVE L0-META | L0-META | **MERGE** into AITutorX taxonomy policy | `Docs/00_GOVERNANCE/` 或 X2 taxonomy | 不得与 OD-03 互替 |
| Terminology 91 | `Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md` | ACTIVE L0-META | L0-META | **MERGE** | X2-03 源之一 | 词表冻结 |
| V3_SPEC README | `Docs/V3_SPEC/README.md` | ACTIVE | index | MIGRATE-candidate | 随 SPEC | — |
| Frozen testset JSON | `backend/Docs/V3_SPEC/*.json` | Frozen exception | 测试按路径读取 | RETAIN-AS-HISTORICAL / Gate-gated code asset | 随测试迁移 | 90 §1.2 例外 |

### 3.2 V3 DECISIONS（L2）

| Family | Path | Status | Authority | Classification | Target | Notes |
|--------|------|--------|-----------|----------------|--------|-------|
| Decisions 67–92 | `Docs/DECISIONS/*.md`（16 tracked） | historical/current mix | L2 V3 | **MERGE + mapping** | `Docs/40_DECISIONS/` | **禁止重编号**；用 X2-06 别名 |
| EB-008 series 87–92 | 同上 | design revisions → FINAL | L2 | MERGE + mapping | 同上 | 外部验证 pending |

### 3.3 V3 REPORTS（L3/L4）

| Family | Path | Status | Authority | Classification | Target | Notes |
|--------|------|--------|-----------|----------------|--------|-------|
| Phase/closure reports 60–83 等 | `Docs/REPORTS/*.md` | historical evidence | L3/L4 | **RETAIN-AS-HISTORICAL** 或 ARCHIVE | `Docs/60_REPORTS/legacy-v3/` 或 `90_ARCHIVE` | 不单独支撑 PASS |
| gate_* reports | 同上 | Gate 证据叙事 | L3 引用 | RETAIN | 映射引用 | Gate 状态权威在 82 §3（V3） |

### 3.4 V3 COORDINATION（tracked）

| Family | Path | Status | Authority | Classification | Target | Notes |
|--------|------|--------|-----------|----------------|--------|-------|
| Contract v0.2 DRAFT（Freeze Object） | `.../PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ f4941ff | **FROZEN content** | Cross-system | **MIGRATE-candidate（字节一致）** | `Docs/30_CONTRACTS/` | sha 必须一致 |
| Contract v0.2 freeze review | `.../FREEZE-CANDIDATE-REVIEW.md` | tracked supporting | evidence | MERGE/RETAIN | `30_CONTRACTS` or `60_REPORTS` | — |
| Consumer Alignment v1–v3 | tracked | coordination | supporting | MERGE | `30_CONTRACTS` | 双向标注 DEC |
| Gap Map / Blocker Analysis / DECISION-ALIGNMENT-REPORT / REVIEW-v0.2 | tracked | supporting | L3/L4-ish | RETAIN + mapping | `30_CONTRACTS`/`60_REPORTS` | — |
| CURRENT.md / state.yaml / log.md | tracked | **mirror** in V3 | coordination | RETAIN-AS-HISTORICAL mirror；canonical = Papers | `50_OPERATIONS` 摘录 | mirror 可落后 |
| HANDOFFS 001–007 | tracked | working handoff | L5-ish | RETAIN-AS-HISTORICAL | `90_ARCHIVE` or `50_OPERATIONS` | — |
| EVIDENCE EB008-* | tracked | evidence | EVD | MERGE | `60_REPORTS` | admitted unknown |

### 3.5 V3 UNTRACKED（authority UNKNOWN — 不得当 GitHub 权威）

| Family | Path | Classification | Owner action needed |
|--------|------|----------------|---------------------|
| DESIGN-v1 / v1.1 identity verification | `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-DESIGN-*.md` | **UNKNOWN** | commit / 降级 / working ref / v1.2（OQ-GF-017） |
| IMPLEMENTATION-PLAN/READINESS/REPORT-PHASE1/2 | 同目录 | UNKNOWN | 同上 |
| CONTRACT.md v0.1 / SKELETON / CONSUMER-REVIEW 早期 | 同目录 | UNKNOWN / likely SUPERSEDED by freeze object | 处置 |
| Docs/GOVERNANCE/ 00/02/03/04 | `Docs/GOVERNANCE/*.md`（本地 untracked） | UNKNOWN | commit to V3 或收编 AITutorX；**commit 前不作迁移依据** |

`[FACT]` GitHub `contents/Docs/COORDINATION/CONTRACTS` 仅 9 tracked 文件；与 untracked 无交集。

### 3.6 V3 reference / archive / root L5

| Family | Path | Classification | Target | Notes |
|--------|------|----------------|--------|-------|
| reference/PRD, DICTIONARY, DISPLAY_CONTRACT, QUESTION_TYPE_TREE, OCR_PROVIDER_POLICY, PADDLEOCR_API, UI, V1_LESSONS, REQUIREMENTS… | `Docs/reference/*` | DICTIONARY/DISPLAY = **MERGE**；lessons = RETAIN-AS-HISTORICAL | `10_SPEC` / `20_ARCHITECTURE` / `90_ARCHIVE` | — |
| docs_audit/ | `docs_audit/*` | RETAIN-AS-HISTORICAL | `90_ARCHIVE` | authority_matrix 与 OD-03 对照 |
| docs_archive/2026-* | `docs_archive/**` | **ARCHIVE** | `90_ARCHIVE` | 不得引用为现行权威 |
| Status.md / log.md / bugs.md / restart-prompt.md | root | L5 | RETAIN-AS-HISTORICAL 或 `50_OPERATIONS` | 不改 L0 |
| frontend docs/README | `frontend/README.md` | code-adjacent | Gate-gated | 随前端资产 |

---

## 4. Preprocessing / Papers 文档族

Git FACT: HEAD `2b92898` = origin/main；local path `D:\Project\Papers`。

### 4.1 Root specs & working logs

| Family | Path | Status | Classification | Target | Notes |
|--------|------|--------|----------------|--------|-------|
| **prd.md** | `prd.md` | **冻结规格基准**（2026-09-10；校准 2026-09-15） | **MIGRATE-candidate** | `Docs/10_SPEC/` | Producer 业务权威 |
| question_identity_design.md | root | design | MERGE/UNKNOWN | `30_CONTRACTS` or `10_SPEC` 待审 | — |
| resolver_contract_design.md | root | design | MERGE/UNKNOWN | 同上 | 与 V3 resolver 对照 |
| production_adversarial_corpus_design.md | root | design | RETAIN-AS-HISTORICAL | `90_ARCHIVE` | — |
| review_protocol.md | root | protocol | MERGE | `00_GOVERNANCE`/`50_OPERATIONS` | — |
| status.md / log.md / bugs.md | root | L5 working | RETAIN-AS-HISTORICAL | `50_OPERATIONS`/`90_ARCHIVE` | append-only 叙事 |
| README.md | root | index | RETAIN | `preprocessing/` 随代码 | — |
| RS.MD | root | `[UNKNOWN]` | UNKNOWN | 待读 | 未在本阶段全文审计 |

### 4.2 governance/

| Family | Path | Classification | Target | Notes |
|--------|------|----------------|--------|-------|
| phase_p2_charter.md | `governance/phase_p2_charter.md` | **MIGRATE-candidate**（内部定位权威） | `Docs/00_GOVERNANCE/` 或 `10_SPEC` | §12 重校准 binding 叙事 |
| rule_registry.md | `governance/rule_registry.md` | MIGRATE-candidate | `00_GOVERNANCE` | — |
| risk_register.md | `governance/risk_register.md` | MERGE | `50_OPERATIONS` | — |

### 4.3 Docs/COORDINATION（Papers = canonical ledger 叙事）

| Family | Path | Classification | Target | Notes |
|--------|------|----------------|--------|-------|
| CURRENT.md | `Docs/COORDINATION/CURRENT.md` | RETAIN + **摘录进 AITutorX state** | `50_OPERATIONS` | Papers 自称 canonical |
| state.yaml | 同目录 | RETAIN + 摘录 | `50_OPERATIONS` | 机器可读 |
| PROTOCOL.md / COMPLETION_PROTOCOL.md | 同目录 | MERGE | `00_GOVERNANCE`/`50_OPERATIONS` | — |
| INTEGRATION/*（freeze/guardian/brief 等） | `Docs/COORDINATION/INTEGRATION/*` | **MERGE + mapping**；大量为 evidence | `60_REPORTS` / `40_DECISIONS` evidence | 不重编号 DEC |
| EVIDENCE/EB008-* | 同目录 | MERGE evidence | `60_REPORTS` | — |
| HANDOFFS/001–014 | 同目录 | RETAIN-AS-HISTORICAL | `90_ARCHIVE` | — |

### 4.4 Code-adjacent / data（非文档迁移，登记）

| Family | Classification | Target | Notes |
|--------|----------------|--------|-------|
| ocr_service/ scripts/ tests/ attacks/ | Gate-gated code | `preprocessing/` / `tools/` | **本阶段不迁移** |
| data/** (json/qc/migration reports) | EVD / 数据工件 | NAS / evidence registry | OD-05；.gitignore 大量 |
| Ocr-markdown/ maintainess/ original/ | **数据本体** | NAS read-only（OD-05） | **禁止 copy 进 repo** |
| _archive/ | ARCHIVE | `90_ARCHIVE` 或原地 | — |
| reports/ | EVD | `60_REPORTS` evidence | — |

---

## 5. V1 / V2（provenance only）

| Repo | Classification | Target |
|------|----------------|--------|
| AITutors-v1 / AITutors-v2 / GitHub AITutor-V2 / AITutor | **RETAIN-AS-HISTORICAL** | 不进入 active tree；lessons 已被 V3_SPEC/V1_LESSONS 引用 |

---

## 6. Stale References & Conflicts（文档地图层）

| ID | Issue | Handling |
|----|-------|----------|
| SR-01 | REPORT-B 列出不存在的 L1 Spec/Finalization 文件名 | X2 对账标 CONFLICT；迁移不得引用为源 |
| SR-02 | REPORT-C AIT-DEC 表未被账本采用且主题有误 | 仅作 **提案映射草稿**；见 X2-06 |
| SR-03 | Papers 文档将 12,707 PDF 系于 original | OQ-GF-011 更正载体未裁；X2 登记事实 |
| SR-04 | V3 Contract 正文状态 vs 账本 FROZEN | C-X2-01；待 Owner 双文件规则 |
| SR-05 | V3 CURRENT mirror 落后 Papers DEC-049 | 允许 lag 需 Owner 确认；引用回 canonical ledger |
| SR-06 | untracked GOVERNANCE/DESIGN 被当权威引用 | citation state 强制标注 |
| SR-07 | 绝对路径 `D:\Project\Papers\...` 依赖 | 数据文档迁移前需 locator 策略（OQ-GF-002） |

---

## 7. Map Completeness Statement

`[FACT]` 本 map 覆盖:
- AITutorX 全部现存 Docs
- V3 GitHub tracked Docs 族（SPEC/DECISIONS/REPORTS/COORDINATION/reference/ARCHIVE + root L5）
- V3 untracked 全清单
- Papers 根文档 / governance / COORDINATION 族
- 数据与代码邻接面（分类级）

`[UNKNOWN]` 本 map **未**对下列做逐文件正文审计:
- V3 `docs_archive/` 全部子文件
- Papers `data/**` 每个 json
- Papers `reports/**` 全部过程报告
- 两仓全部 test 文件

这些标记为 `UNREVIEWED-FAMILY` / ARCHIVE-candidate，**不得**在未审前标 MIGRATE。

---

*Unified documentation map registered. No mechanical bulk copy authorized.*
