# Report B — AITutorX Asset Registry

**日期**: 2026-09-16
**方法**: 两 repo git ls-files + status + log 独立枚举

---

## Migration Class 定义

| Class | 含义 |
|-------|------|
| A | Migrate（直接迁移） |
| B | Migrate + Adapt（迁移并适配） |
| C | Historical Archive（历史归档） |
| D | Reject（拒绝迁移） |
| E | Pending Governance（待治理裁决） |

---

## 1. Frozen Specification（L1 — 权威最高）

| # | Asset | Source | Commit | Status | Authority | Class |
|---|-------|--------|--------|--------|-----------|-------|
| 1 | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` | V3 | `f4941ff` | TRACKED, FROZEN | L1 (verified sha256) | **A** |
| 2 | `PREPROCESSING-V3-INTEGRATION-SPEC-v0.1.md` | V3 | tracked | TRACKED | L1 | **A** |
| 3 | `PREPROCESSING-V3-INTERFACE-FINALIZATION-REVISION-v1.md` | V3 | tracked | TRACKED | L1 | **A** |
| 4 | `PREPROCESSING-V3-INTERFACE-DECISION-FINALIZATION-v1.md` | V3 | tracked | TRACKED | L1 | **A** |
| 5 | `PREPROCESSING-V3-CONTRACT-DECISION-FINALIZATION-v1.md` | V3 | tracked | TRACKED | L1 | **A** |
| 6 | `PREPROCESSING-V3-OWNER-DECISION-FINAL-v1.md` | V3 | tracked | TRACKED | L1 | **A** |
| 7 | `PREPROCESSING-V3-OWNER-B1-B2-B3-DECISION-ALIGNMENT-v1.md` | V3 | tracked | TRACKED | L1 | **A** |

---

## 2. Consumer Implementation（L4）

| # | Asset | Source | Commit | Status | Class |
|---|-------|--------|--------|--------|-------|
| 8 | `backend/app/core/manifest_identity.py` (M1) | V3 | `6c4e3ff` | TRACKED | **A** |
| 9 | `backend/app/core/raw_bytes_identity.py` (M2) | V3 | `6c4e3ff` | TRACKED | **A** |
| 10 | `backend/app/core/ir_identity.py` (M3) | V3 | `6c4e3ff` | TRACKED | **A** |
| 11 | `backend/app/core/identity_verifier.py` (M4) | V3 | `6c4e3ff` | TRACKED | **A** |
| 12 | `backend/app/core/identity_gate.py` (M5) | V3 | `6c4e3ff` | TRACKED | **A** |
| 13 | `backend/scripts/preprocessing_consumer/runner_b2.py` | V3 | `cc12d79` | TRACKED | **A** |
| 14 | `backend/app/domains/compile/__init__.py` | V3 | tracked | TRACKED | **A** |
| 15 | `backend/app/domains/gate/__init__.py` | V3 | tracked | TRACKED | **A** |
| 16 | `backend/tests/` (all test files) | V3 | various | TRACKED | **A** |

---

## 3. Consumer Governance / Coordination（L2–L7）

| # | Asset | Source | Status | Authority | Class |
|---|-------|--------|--------|-----------|-------|
| 17 | `Docs/COORDINATION/state.yaml` | V3 | TRACKED | L5 (state) | **A** |
| 18 | `Docs/COORDINATION/CURRENT.md` | V3 | TRACKED | L5 (state) | **A** |
| 19 | `Docs/COORDINATION/COMPLETION_PROTOCOL.md` | V3 | TRACKED | L0-META | **A** |
| 20 | `Docs/COORDINATION/EVIDENCE/` (6 files) | V3 | TRACKED | L6 | **A** |
| 21 | `Docs/COORDINATION/HANDOFFS/` (14 files) | V3 | TRACKED | L7 | **C** |
| 22 | `Docs/COORDINATION/INTEGRATION/` (~30 files) | V3 | TRACKED | L2–L6 | **A** |
| 23 | `bugs.md` | V3 | TRACKED | L5 | **A** |
| 24 | `docs_audit/authority_matrix.yaml` | V3 | TRACKED | L6 | **B** |

---

## 4. V3 Untracked Documents（LOCAL ONLY — 核心风险）

| # | Asset | Status | Authority | Class |
|---|-------|--------|-----------|-------|
| 25 | `…DESIGN-v1.1.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 26 | `…DESIGN-v1.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 27 | `…IMPLEMENTATION-PLAN-v1.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 28 | `…IMPLEMENTATION-READINESS-v1.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 29 | `…IMPLEMENTATION-REPORT-PHASE1.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 30 | `…IMPLEMENTATION-REPORT-PHASE2.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 31 | `…CONTRACT-CONSUMER-REVIEW.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 32 | `…CONTRACT-v0.2-DRAFT-SKELETON.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 33 | `…CONTRACT.md` | UNTRACKED, never in git | **UNKNOWN** | **E** |
| 34 | `Docs/GOVERNANCE/` (G0 docs, 4 files) | UNTRACKED | **UNKNOWN** | **E** |

---

## 5. Producer Core（L4/L5）

| # | Asset | Source | Status | Class |
|---|-------|--------|--------|-------|
| 35 | `scripts/` (~40 Python scripts) | Producer | TRACKED | **B** |
| 36 | `tests/` (~30 test files) | Producer | TRACKED | **A** |
| 37 | `ocr_service/` | Producer | TRACKED | **B** |
| 38 | `attacks/` | Producer | TRACKED | **B** |
| 39 | `data/` (test samples) | Producer | TRACKED | **A** |

---

## 6. Producer Governance（L2–L6）

| # | Asset | Source | Status | Authority | Class |
|---|-------|--------|--------|-----------|-------|
| 40 | `governance/rule_registry.md` | Producer | TRACKED | L2 | **A** |
| 41 | `governance/risk_register.md` | Producer | TRACKED | L2 | **A** |
| 42 | `governance/phase_p2_charter.md` | Producer | TRACKED | L2 | **A** |
| 43 | `Docs/COORDINATION/state.yaml` | Producer | TRACKED | L5 | **A** |
| 44 | `Docs/COORDINATION/CURRENT.md` | Producer | TRACKED | L5 | **A** |
| 45 | `Docs/COORDINATION/EVIDENCE/` (7 files) | Producer | TRACKED | L6 | **A** |
| 46 | `Docs/COORDINATION/HANDOFFS/` (14 files) | Producer | TRACKED | L7 | **C** |
| 47 | `Docs/COORDINATION/INTEGRATION/` (~30 files) | Producer | TRACKED | L2–L6 | **A** |
| 48 | `log.md` (append-only) | Producer | TRACKED | L5 | **A** |
| 49 | `bugs.md` | Producer | TRACKED | L5 | **A** |
| 50 | `status.md` | Producer | TRACKED | L5 | **A** |
| 51 | `prd.md` | Producer | TRACKED | L2 | **B** |
| 52 | `reports/` (7 files) | Producer | TRACKED | L6 | **C** |
| 53 | `question_identity_design.md` | Producer | TRACKED | L3 | **B** |
| 54 | `resolver_contract_design.md` | Producer | TRACKED | L3 | **B** |
| 55 | `review_protocol.md` | Producer | TRACKED | L2 | **A** |
| 56 | `production_adversarial_corpus_design.md` | Producer | TRACKED | L3 | **B** |

---

## 7. 汇总

| Class | 数量 | 说明 |
|-------|------|------|
| A (Migrate) | ~35 | Frozen specs, identity modules, tests, governance files |
| B (Migrate+Adapt) | ~12 | Scripts, OCR service, design docs |
| C (Historical Archive) | ~5 | Handoffs, old reports |
| D (Reject) | 0 | 无 |
| E (Pending Governance) | 10 | All untracked docs |
