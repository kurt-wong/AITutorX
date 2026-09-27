# X2-02 — Unified Architecture Baseline

> **[CLOSED 2026-09-27]** 本文件的生命周期已结束（阶段完成）。**正文保持原样不改写**（DOC-GOV §7）。
> 保留在主视野：其内容仍具参考价值。当前状态见 [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../50_OPERATIONS/CURRENT_STATE.md)。


**Document ID**: X2-02
**Task**: TASK-X2-CLAUDE
**Document Type**: Architecture Baseline
**Status**: `CLOSED`（原状态：`ACTIVE — X2 AUDIT BASELINE`）
**Date**: 2026-09-18
**Upstream**: `X2-01-UNIFIED-SYSTEM-BASELINE.md`；GF v0.2；Contract v0.2 Freeze Object
**Hard rule**: Architecture Baseline 文档 ≠ Implementation；≠ Migration Authorization

---

## 1. Unified Architecture View（AITutorX 项目级）

```text
                    ┌─────────────────────────────────────┐
                    │              AITutorX                 │
                    │   Unified Docs + Governance (GF v0.2) │
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
   ┌──────▼──────────┐      ┌─────────▼─────────┐      ┌─────────▼─────────┐
   │ preprocessing   │      │   backend (V3)    │      │    frontend       │
   │ Producer domain │      │ Consumer domain   │      │ Consumer UI       │
   │                 │      │                   │      │                   │
   │ OCR / Repair    │      │ Source seal       │      │ Admin/Student     │
   │ LLM re-slice    │─────►│ Annotation        │      │ Review queue      │
   │ Manifest / IR   │Contract│ Resolver/IR     │      │ Display contract  │
   │ Evidence QC     │      │ Compiler/Gate     │      │                   │
   │                 │      │ Admission/Domain  │      │                   │
   └─────────────────┘      └───────────────────┘      └───────────────────┘
          │                           │
          │         ┌─────────────────▼─────────────────┐
          └────────►│     tools / archive (Gate-gated)  │
                    │  audit · migration scripts · probes│
                    └───────────────────────────────────┘

Boundary: Producer ↔ Consumer = AITutorX **内部系统边界**
          （仍须 Contract；不是两个项目边界）
```

---

## 2. Capability Domain Assignment

### 2.1 Modules → preprocessing（Producer 能力域）

| Module / area | Source path（历史） | Evidence |
|---------------|---------------------|----------|
| OCR service | Papers `ocr_service/` | prd §3.3 |
| Source repair scripts | Papers `scripts/fix_*` / `recover_images` / `corpus_scan` / `pdf_fidelity` | prd 脚本索引 |
| LLM re-slice pipeline | Papers `scripts/reslice_pipeline.py` | prd §3.1 |
| QC / render lint | Papers `scripts/reslice_qc.py` / `render_*` | prd C1–C10 |
| Evidence manifests / IR artifact | Papers `Ocr-markdown/` + `data/resolver_ref_r52/` | Contract；CURRENT 关键数字 |
| Identity backfill / freeze evidence scripts | Papers `scripts/interface_scope_step1/2` / `freeze_evidence_*` | DEC-031/033 evidence |
| Producer tests | Papers `tests/` | pytest baseline（冲突见 OQ-GF-018） |
| Producer governance | Papers `governance/` + `Docs/COORDINATION/` | charter / rule_registry |

### 2.2 Modules → V3 / backend（Consumer Semantic/Question 能力域）

| Module / area | Source path（历史） | Evidence |
|---------------|---------------------|----------|
| Source domain seal | V3 `backend/app/domains/source` + `core/hashing` | V3_SPEC 10 |
| Semantic Annotation | V3 `domains/annotation` | V3_SPEC 20 §4 |
| Resolver | V3 `domains/resolver` | V3_SPEC 20 §5 |
| Compile / IR / Snapshot | V3 `domains/compile` | V3_SPEC 20 §6–7 |
| Evidence / promotion | V3 `domains/evidence` | DEC 75–92 EB-008 |
| Gate / Admission | V3 `domains/gate` | V3_SPEC 20 §8；10 §5.4 |
| Identity verification modules M1–M5 | V3 `backend/app/core/{raw_bytes,manifest,ir}_identity*` + `identity_gate/verifier` | Contract §5.6；**implementation state disputed/untracked-design-linked** |
| Consumer adapters | V3 `backend/scripts/preprocessing_consumer/` | consumer-report-* |
| API / Worker / DB | V3 `backend/app/{api,worker,db,models,repositories}` | V3_SPEC 30/10 |
| Frontend | V3 `frontend/` | DISPLAY_CONTRACT / UI reference |

### 2.3 Future merge candidates（`[PROPOSAL]`，未授权执行）

| Item | Why | Gate condition |
|------|-----|----------------|
| V3 consumer adapters ↔ producer interface docs | 同属 AITutorX 内部边界 | Contract + Identity verification 实现裁决后 |
| 两仓 COORDINATION 账本 → AITutorX `Docs/50_OPERATIONS` | 统一状态载体 | Owner ledger 归属裁决 |
| Unified Docs 目录内容 | 本任务目标结构 | 逐资产过 Migration Gate |
| Test harness 叙事统一 | 消除基线冲突 | OQ-GF-018 Owner 裁决 |

### 2.4 Boundaries that MUST remain

| Boundary | Why it remains |
|----------|----------------|
| Producer/Consumer Contract | AGENTS.md 原则 3；即使同仓也需 Contract |
| Source immutable / sealed | V3 P3；禁止反向改 Source |
| Candidate = 唯一 A-domain 通道 | V3 10 四条承载规则 |
| LLM 无 Admission Authority | V3 P2；Contract 最终原则 |
| Path ≠ Identity | Contract 冻结项 ①/④；OD-04 |
| UNKNOWN retained | AGENTS.md；Contract 三禁令 |
| Git presence ≠ Authority | AGENTS.md 原则 4 |
| Freeze ≠ Implementation | Contract / DEC-036 / OD-14 |

### 2.5 Old designs superseded by unified architecture view

| Old design | Status under AITutorX unified view |
|------------|-------------------------------------|
| V1/V2 pipeline as code base | SUPERSEDED by V3 rebuild principles（00 §1） |
| preprocessing 输出 Question IR / V3 Admission 格式（P2.3 旧表述） | SUPERSEDED by §12 Source Evidence Producer（charter） |
| 两仓并列 Docs 治理（各自完整再拼接） | SUPERSEDED by AITutorX Unified Model（任务书 §3.2） |
| monorepo / internal package migration 预设计 | **明确不做**（prd §12.7）；合并依据真实维护成本 |
| V2 Quality Gate / Admission Gate R 规则 | SUPERSEDED（legacy）by V3 Gate 分层 |
| L1 Anchor Correction 范式 | SUPERSEDED by Source Resolver |
| 四状态机跨层合并记法 | SUPERSEDED by 双层词表（DEC-028 Part 5） |

---

## 3. Identity & Data Architecture（统一口径）

```text
Cross-system identity key (binding):
  source_content_sha256 = SHA256(original source bytes)  # 64 lowercase hex
  path / source_file    = locator only

V3 internal:
  source_version_id     = uuid.UUID FK (document_source_versions)
  documents.original_sha256 = historical field; semantics ≠ raw-bytes key (OBSERVED)

Producer artifacts:
  OCR source_sha256     = SHA256(pdf bytes) in OCR manifest layer (historical dual-layer)
  manifest/IR           = source_content_sha256 (after Step2 backfill on interface scope 87)
```

`[FACT]` OD-05 Data model mode（已裁，细节 OPEN）:
- NAS = 语料本体
- Docker = read-only mount
- DB = 结构化对象
- Repo = 测试资产
- 禁止把全部数据复制进代码仓

`[FACT]` 当前数据主体在 Papers 本地且 `.gitignore`；AITutorX **不持有** corpus 本体。

---

## 4. Material Architecture（统一强调）

```text
Material ≠ 纯文字
Material 可包含:
  - 题图
  - 配图
  - 图表
  - 图片
  - 其他题目依赖的外部材料

single question 也可以拥有 Material
composite_question 共享 material 是常见形态，但不是唯一形态
```

`[FACT]` V3 `10_Data_Model`: `materials` / `material_links` / `source_figures` / `instance_figure_links`。
`[FACT]` preprocessing prd: composite `material ⊆ questions`；`extra` 卫星锚承载排版漂移的配图归属。
`[FACT]` figure_id 确定性规则已冻结（BUG-011）；`figure_hash = SHA256(raw_image_bytes)`。

`[UNKNOWN]` 图片恢复 Step5 / dangling figure recovery 未完成；不影响 Material 概念定义。

---

## 5. State Architecture（两层语义分离）

| Layer | Values | Meaning |
|-------|--------|---------|
| **Semantic layer** | `ready` / `incomplete` / `unknown` | 内容语义可解释性 |
| **Decision layer** | `pending_review` / `approved` / `rejected` | 治理/入库决策 |

规则（binding）:
- `unknown ≠ ready`
- unknown → reviewable record → `pending_review`
- 禁 silent skip / silent convert / silent fallback
- 两层禁止合并

`[OBSERVED]` V3 现状: `SEMANTIC_STATUS` 冻结于 `{ready,incomplete}`（加 `unknown` 须解冻 BUG-V3-018）；candidate 仅由 ready 产生 → unknown 单元当前在实现上难以进入 pending_review（C-X2-09）。

**其它状态词表（不得互相替代）**:

| Vocabulary | Values | Use |
|------------|--------|-----|
| Citation state | exists / tracked / referenced / admitted | 工件引用效力 |
| Migration classification | MIGRATE / MERGE / SUPERSEDE / ARCHIVE / REJECT / RETAIN-AS-HISTORICAL / UNKNOWN | 文档/资产迁移处置 |
| Migration readiness | NOT_READY / CANDIDATE_UNGATED / GATE_BLOCKED / **（未出现）GATE_PASSED / MIGRATED** | 迁移进程 |
| Processing status (V3 documents) | created / ingesting / sealed / failed | Source 生命周期摘要，≠ pipeline 完成度 |
| V3 90/91 Gate status | OPEN / PENDING / CONDITIONAL PASS / CLOSED — scope / … | V3 文档治理词表 |
| GF OQ status | OPEN / OPEN-BLOCKING / MAPPED / STALE-CANDIDATE | OQ-GF 登记册 |

---

## 6. Module Ownership Map（迁移后目标位置 — 仅登记）

| Historical asset class | Target AITutorX location | Classification default |
|------------------------|--------------------------|------------------------|
| V3 frozen spec | `Docs/10_SPEC/`（引用或受控副本；**不改 Frozen 原文**） | MIGRATE-candidate |
| Contract v0.2 freeze object copy | `Docs/30_CONTRACTS/` | MIGRATE-candidate（字节一致 + sha） |
| V3 decisions | `Docs/40_DECISIONS/` via mapping | MERGE + mapping |
| Papers contracts/integration reports | `Docs/30_CONTRACTS/` / `Docs/60_REPORTS/` | MERGE |
| Producer prd / rule registry | `Docs/10_SPEC/` / `Docs/00_GOVERNANCE/` 细则 | MIGRATE-candidate |
| V3 backend code | `backend/` | **Gate-gated code migration**（本阶段禁止执行） |
| Producer scripts/ocr_service | `preprocessing/` / `tools/` | Gate-gated |
| V3 frontend | `frontend/` | Gate-gated |
| Working notes / logs / status | `Docs/50_OPERATIONS/` or `Docs/90_ARCHIVE/` | RETAIN-AS-HISTORICAL / ARCHIVE |
| Untracked design family | 未定 | UNKNOWN until Owner |

---

## 7. Non-Claims

- 本文不授权任何代码迁移
- 本文不宣布统一架构已实现
- 本文不关闭 C-X2-01~10
- 本文不替代 V3 90/91 或 GF v0.2

---

*Unified Architecture Baseline registered. Migration remains UNAUTHORIZED.*
