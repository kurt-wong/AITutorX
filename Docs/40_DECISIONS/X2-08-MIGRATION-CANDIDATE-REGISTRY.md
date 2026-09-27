# X2-08 — Migration Candidate Registry

> **[CLOSED 2026-09-27]** 本文件的生命周期已结束（阶段完成）。**正文保持原样不改写**（DOC-GOV §7）。
> 保留在主视野：其内容仍具参考价值。当前状态见 [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../50_OPERATIONS/CURRENT_STATE.md)。


**Document ID**: X2-08
**Task**: TASK-X2-CLAUDE
**Document Type**: Decisions / Migration Candidate Registry（审计登记）
**Status**: `CLOSED`（原状态：`ACTIVE — CANDIDATES ONLY`）
**Date**: 2026-09-18
**Hard rule**:
```text
Migration Candidate ≠ Migrated
Candidate registration ≠ Gate Passed ≠ Migration Authorized
Git presence ≠ Authority
Untracked default = not eligible for active tree
```

---

## 0. Registry schema（每个资产）

`Asset ID` | `Source` | `Path` | `Type` | `Authority` | `Status(citation)` | `Evidence` | `Dependencies` | `Conflict` | `Target AITutorX location` | `Migration classification` | `Migration readiness`

**Readiness vocabulary**:
`NOT_READY` | `CANDIDATE_UNGATED` | `GATE_BLOCKED` | ~~GATE_PASSED~~ | ~~MIGRATED~~
（后两者当前 **无任何资产**）

**Source commits（X2/X2.1 evidence anchor）**:
- AITutorX current HEAD `7002f38`
- V3 baseline `cc12d79`
- Papers baseline `2b92898`
- Contract freeze object `f4941ff`
- Contract SHA256 `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528`
- `[HISTORICAL]` X2 audit parent `331cbea`（非 current HEAD）

`[RULE]` Anchor 仅 evidence anchoring；**不授权 Migration；不把任何 candidate 标为 migrated。**

---

## 1. Specs

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness | Conflict/Dep |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|--------------|
| MC-SPEC-001 | V3 | `Docs/V3_SPEC/00_Master_Spec.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | Charter/Gate 未开 |
| MC-SPEC-002 | V3 | `Docs/V3_SPEC/10_Data_Model.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | 同上 |
| MC-SPEC-003 | V3 | `Docs/V3_SPEC/20_Document_Pipeline.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | 同上 |
| MC-SPEC-004 | V3 | `Docs/V3_SPEC/30_Task_LLM_Safety.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | 同上 |
| MC-SPEC-005 | V3 | `Docs/V3_SPEC/40_Development_Rules.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | 同上 |
| MC-SPEC-006 | V3 | `Docs/V3_SPEC/50_Migration_Assets.md` | Frozen Spec | L0 | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | 与本 registry 对照 |
| MC-SPEC-007 | V3 | `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` | L0-META | L0-META | tracked | governance merge | MERGE | GATE_BLOCKED | 与 OD-03 张力 |
| MC-SPEC-008 | V3 | `Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md` | L0-META | L0-META | tracked | merge → X2-03 源 | MERGE | CANDIDATE_UNGATED | — |
| MC-SPEC-010 | Papers | `prd.md` | Producer frozen spec | Producer | tracked | `Docs/10_SPEC/` | MIGRATE | GATE_BLOCKED | — |
| MC-SPEC-011 | Papers | `governance/phase_p2_charter.md` | Internal charter | Producer | tracked | `00_GOVERNANCE`/`10_SPEC` | MIGRATE | GATE_BLOCKED | — |
| MC-SPEC-012 | Papers | `governance/rule_registry.md` | Rule registry | Producer | tracked | `00_GOVERNANCE` | MIGRATE | GATE_BLOCKED | — |

---

## 2. Contracts

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness | Conflict/Dep |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|--------------|
| MC-CON-001 | V3 | `.../PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ **f4941ff** | Frozen Contract object | Cross-system | tracked@f4941ff | `Docs/30_CONTRACTS/` | MIGRATE (byte-identical) | GATE_BLOCKED | 状态叙事 C-X2-01；sha 必须 `9c6b9063…7528` |
| MC-CON-002 | V3 | `.../CONTRACT-v0.2-FREEZE-CANDIDATE-REVIEW.md` | Supporting | evidence | tracked | `30_CONTRACTS` | MERGE | CANDIDATE_UNGATED | — |
| MC-CON-003 | V3 | `.../CONSUMER-DECISION-ALIGNMENT-v1/v2/v3.md` | Coordination | supporting | tracked | `30_CONTRACTS` | MERGE | CANDIDATE_UNGATED | DEC 双标 |
| MC-CON-004 | V3 | GAP-MAP / BLOCKER-ANALYSIS / DECISION-ALIGNMENT-REPORT / REVIEW-v0.2 | Coordination | supporting | tracked | `30_CONTRACTS`/`60_REPORTS` | MERGE/RETAIN | CANDIDATE_UNGATED | — |
| MC-CON-005 | Papers | `Docs/COORDINATION/INTEGRATION/PREPROCESSING-INTEGRATION-CONTRACT.md` | Producer contract draft v0.1 | DRAFT | tracked | `30_CONTRACTS` | RETAIN-AS-HISTORICAL | CANDIDATE_UNGATED | 与 v0.2 关系待确认 |
| MC-CON-006 | V3 untracked | `.../IDENTITY-VERIFICATION-DESIGN-v1.1.md` 等 9 文件 | Design family | **UNKNOWN** | untracked | 未定 | UNKNOWN | NOT_READY | OQ-GF-017；D2/D3/D4 |
| MC-CON-007 | V3 untracked | `Docs/GOVERNANCE/00/02/03/04.md` | G0 governance drafts | UNKNOWN | untracked | 未定 | UNKNOWN | NOT_READY | commit 前不作依据 |
| MC-CON-008 | Papers | `question_identity_design.md` / `resolver_contract_design.md` | Design docs | UNKNOWN/working | tracked | 待审 | UNKNOWN/MERGE | CANDIDATE_UNGATED | 与 V3 设计对照 |

---

## 3. Architecture docs

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|
| MC-ARC-001 | V3 | `Docs/reference/DICTIONARY.md` | Dictionary | project | tracked | `10_SPEC` merge | MERGE | CANDIDATE_UNGATED |
| MC-ARC-002 | V3 | `Docs/reference/DISPLAY_CONTRACT.md` | Product display | accepted product | tracked | `20_ARCHITECTURE`/`10_SPEC` | MIGRATE/MERGE | CANDIDATE_UNGATED |
| MC-ARC-003 | V3 | `Docs/reference/QUESTION_TYPE_TREE.md` | Domain ref | supporting | tracked | `10_SPEC` | MIGRATE | CANDIDATE_UNGATED |
| MC-ARC-004 | V3 | `Docs/reference/REQUIREMENTS_AND_SOLUTION.md` | Requirements | inherited business | tracked | `10_SPEC`/`20_ARCHITECTURE` | MIGRATE | CANDIDATE_UNGATED |
| MC-ARC-005 | V3 | `OCR_PROVIDER_POLICY.md` / `PADDLEOCR_API.md` | EXT capability refs | EXT | tracked | `20_ARCHITECTURE` | RETAIN/MERGE | CANDIDATE_UNGATED |
| MC-ARC-006 | V3 | `Docs/reference/UI.md` | UI ref | supporting | tracked | `20_ARCHITECTURE` | RETAIN | CANDIDATE_UNGATED |
| MC-ARC-007 | V3 | `Docs/reference/V1_LESSONS.md` | Lessons | historical | tracked | `90_ARCHIVE` | RETAIN-AS-HISTORICAL | CANDIDATE_UNGATED |
| MC-ARC-008 | X2 | `Docs/20_ARCHITECTURE/X2-01/02` | AITutorX native | ACTIVE | tracked after commit | native | RETAIN | n/a native |

---

## 4. Decisions / Reports / Evidence

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness | Conflict |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|----------|
| MC-DEC-001 | V3 | `Docs/DECISIONS/*.md` (16) | L2 decisions | V3 L2 | tracked | `40_DECISIONS` via mapping | MERGE | GATE_BLOCKED | OQ-GF-016；撞号 |
| MC-REP-001 | V3 | `Docs/REPORTS/*.md` | L3/L4 | evidence | tracked | `60_REPORTS`/`90_ARCHIVE` | RETAIN-AS-HISTORICAL | CANDIDATE_UNGATED | 不单独支撑 PASS |
| MC-REP-002 | AITutorX | `REPORT-A~F` | Stage-1 audit | Set A | tracked | native | RETAIN | n/a native | 部分错误见 DL-11 |
| MC-REP-003 | AITutorX | `REPORT-G/H/I/K` | Audit | UNKNOWN until OD-06 | **untracked** | 待整理收编 | UNKNOWN | NOT_READY | admitted unknown |
| MC-EVD-001 | Papers | `Docs/COORDINATION/INTEGRATION/*` | Evidence | EVD | tracked | `60_REPORTS` evidence | MERGE | CANDIDATE_UNGATED | 不重编号 |
| MC-EVD-002 | Papers | `data/freeze_evidence_*.json` / interface_scope_* | Evidence artifacts | EVD | mixed | NAS/registry | UNKNOWN | NOT_READY | OD-05 |
| MC-EVD-003 | V3 | `backend/scripts/preprocessing_consumer/*.json` | Consumer reports | EVD | tracked | `60_REPORTS` | RETAIN/MERGE | CANDIDATE_UNGATED | — |

---

## 5. Tests

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness | Conflict |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|----------|
| MC-TST-001 | Papers | `tests/**` | Producer tests | code-adjacent | tracked | `preprocessing/tests` | Gate-gated code | GATE_BLOCKED | OQ-GF-018 baseline |
| MC-TST-002 | Papers | `attacks/**` | Adversarial suite | code-adjacent | tracked | `tools`/`preprocessing` | Gate-gated | GATE_BLOCKED | S-1/S-2 复跑纪律 |
| MC-TST-003 | V3 | `backend/tests/**` | Consumer tests | code-adjacent | tracked | `backend/tests` | Gate-gated | GATE_BLOCKED | baseline 冲突 |
| MC-TST-004 | V3 | `backend/Docs/V3_SPEC/*frozen_testset.json` | Frozen test corpora | L0 exception | tracked | 随 tests | Gate-gated | GATE_BLOCKED | 路径读取依赖 |

---

## 6. Production code（**本阶段全部 GATE_BLOCKED — 禁止迁移**）

| Asset ID | Source | Path | Type | Authority | Citation | Target | Classification | Readiness |
|----------|--------|------|------|-----------|----------|--------|----------------|-----------|
| MC-CODE-001 | V3 | `backend/app/**` | Consumer production | implementation | tracked | `backend/` | MIGRATE-candidate | **GATE_BLOCKED** |
| MC-CODE-002 | V3 | `backend/app/core/*identity*` M1–M5 | Identity modules | Design authority disputed | tracked | `backend/app/core` | MIGRATE-candidate | **GATE_BLOCKED** + OQ-GF-017 |
| MC-CODE-003 | V3 | `backend/scripts/preprocessing_consumer/**` | Consumer adapters | implementation | tracked | `backend` or `tools` | MIGRATE-candidate | **GATE_BLOCKED** |
| MC-CODE-004 | V3 | `backend/alembic/**` | DB migrations | implementation | tracked | `backend/alembic` | Gate-gated | **GATE_BLOCKED** |
| MC-CODE-005 | V3 | `frontend/**` | Consumer UI | implementation | tracked | `frontend/` | Gate-gated | **GATE_BLOCKED** |
| MC-CODE-006 | Papers | `ocr_service/**` | OCR producer service | implementation | tracked | `preprocessing/ocr_service` | Gate-gated | **GATE_BLOCKED** |
| MC-CODE-007 | Papers | `scripts/**` | Producer scripts | implementation | tracked | `preprocessing/scripts` or `tools/` | Gate-gated | **GATE_BLOCKED** |

---

## 7. CLI / migration / audit scripts / probes

| Asset ID | Source | Path | Target | Readiness | Notes |
|----------|--------|------|--------|-----------|-------|
| MC-TOOL-001 | Papers | `scripts/interface_scope_step1_snapshot.py` / `step2_backfill.py` | `tools/` | GATE_BLOCKED | Freeze evidence producers |
| MC-TOOL-002 | Papers | `scripts/freeze_evidence_final_check.py` | `tools/` | GATE_BLOCKED | — |
| MC-TOOL-003 | Papers | `scripts/audit_integrity.py` / `r50_audit_governance.py` | `tools/` | GATE_BLOCKED | Identity/QC audits |
| MC-TOOL-004 | Papers | `scripts/r64_data_inventory.py` / `r67_*` | `tools/` | GATE_BLOCKED | Absolute path hardcode |
| MC-TOOL-005 | Papers | `scripts/recover_images.py` | `preprocessing/scripts` | GATE_BLOCKED | Material/image path |
| MC-TOOL-006 | Papers | `scripts/r*_*.py` / `phase*_*.py` probes | `tools/audit` | GATE_BLOCKED | Probe class |

---

## 8. Data manifests / corpus metadata / evidence packs

| Asset ID | Source | Path | Type | Target | Readiness | Notes |
|----------|--------|------|------|--------|-----------|-------|
| MC-DAT-001 | Papers | `data/ocr_output_manifest.jsonl` | OCR manifest | NAS / hash registry | NOT_READY | OD-05；OQ-GF-002 |
| MC-DAT-002 | Papers | `Ocr-markdown/**/*.manifest.json` | Evidence manifests | NAS read-only | NOT_READY | 166/87 面 |
| MC-DAT-003 | Papers | `data/resolver_ref_r52/resolver_ir.json` | Producer IR | NAS / evidence | NOT_READY | 71 ADMITTED 叙事 |
| MC-DAT-004 | Papers | `data/interface_scope_*.json` | Interface snapshots | evidence registry | NOT_READY | Freeze evidence |
| MC-DAT-005 | Papers | `Ocr-markdown/` corpus trees | OCR corpus body | NAS | NOT_READY | **禁 copy 进 repo** |
| MC-DAT-006 | Papers | `maintainess/PDF` + `original/` | Source trees | NAS | NOT_READY | 双树；OD-04 |
| MC-DAT-007 | Papers | `data/*qc*.json` / migration reports | QC evidence | evidence registry | NOT_READY | 过程态 |
| MC-DAT-008 | Both | freeze evidence six artifacts | Freeze pack | `30_CONTRACTS` evidence annex | NOT_READY | sha 登记已有 |

---

## 9. Registry summary

| Bucket | Count (approx) | Readiness peak |
|--------|----------------|----------------|
| Specs | 11 | GATE_BLOCKED |
| Contracts | 8 families | GATE_BLOCKED / NOT_READY (untracked) |
| Architecture refs | 8 | CANDIDATE_UNGATED |
| Decisions/Reports/Evidence | 多族 | native / GATE_BLOCKED / NOT_READY |
| Tests | 4 families | GATE_BLOCKED |
| Production code | 7 families | **GATE_BLOCKED** |
| Tools/scripts | 6+ families | GATE_BLOCKED |
| Data/corpus | 8 families | **NOT_READY** |
| **GATE_PASSED / MIGRATED** | **0** | — |

---

## 10. Global blockers for all candidates

1. Migration Authority Charter requirements 未满足（OD-01；`approval_block=invalid_without_charter`）
2. REPORT-I Cluster A 未关闭 → 默认禁止迁移
3. Authority Taxonomy 完整执行未完成（OD-03 / OQ-GF-015）
4. Namespace policy 未裁（OQ-GF-016）
5. Untracked authority 未处置（OQ-GF-017）
6. Data authority 实施细节未完成（OD-05 / OQ-GF-002 / BL-10）
7. Test baseline 未固化（OQ-GF-018）
8. REPORT-G/H/I/K 未完成 OD-06 admission 流程
9. D2/D3/D4 / D-048 未裁

---

*Migration Candidate Registry registered. Nothing migrated.*
