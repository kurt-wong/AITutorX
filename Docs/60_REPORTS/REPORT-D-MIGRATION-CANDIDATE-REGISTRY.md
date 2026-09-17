# Report D — AITutorX Migration Candidate Registry

**日期**: 2026-09-16
**前提**: 迁移必须经过 Migration Gate（10 步检查）

---

## Migration Gate 检查项

1. Source identified
2. Authority identified
3. Current validity verified
4. Historical status classified
5. Duplicate check
6. Architecture compatibility check
7. Evidence attached
8. Migration class assigned
9. Governance approval
10. Migration record created

---

## 1. 立即可迁移（Class A — Gate 1-8 已满足）

### 1.1 Frozen Contract & Specs

| Asset | Source Repo | Commit | Gate Status | 阻塞项 |
|-------|------------|--------|-------------|--------|
| Contract v0.2 DRAFT | V3 | `f4941ff` | 1-8 PASS | Gate 9 (Owner approve) |
| Integration Spec v0.1 | V3 | tracked | 1-8 PASS | Gate 9 |
| Interface Finalization docs (4) | V3 | tracked | 1-8 PASS | Gate 9 |
| Owner Decision docs (2) | V3 | tracked | 1-8 PASS | Gate 9 |

### 1.2 Identity Modules (M1-M5)

| Asset | Source Repo | Commit | Gate Status | 阻塞项 |
|-------|------------|--------|-------------|--------|
| manifest_identity.py (M1) | V3 | `6c4e3ff` | 1-8 PASS | Gate 9 |
| raw_bytes_identity.py (M2) | V3 | `6c4e3ff` | 1-8 PASS | Gate 9 |
| ir_identity.py (M3) | V3 | `6c4e3ff` | 1-8 PASS | Gate 9 |
| identity_verifier.py (M4) | V3 | `6c4e3ff` | 1-8 PASS | Gate 9 |
| identity_gate.py (M5) | V3 | `6c4e3ff` | 1-8 PASS | Gate 9 |
| runner_b2.py | V3 | `cc12d79` | 1-8 PASS | Gate 9 |

### 1.3 Governance Files

| Asset | Source Repo | Gate Status | 阻塞项 |
|-------|------------|-------------|--------|
| governance/rule_registry.md | Producer | 1-8 PASS | Gate 9 |
| governance/risk_register.md | Producer | 1-8 PASS | Gate 9 |
| governance/phase_p2_charter.md | Producer | 1-8 PASS | Gate 9 |
| review_protocol.md | Producer | 1-8 PASS | Gate 9 |
| COMPLETION_PROTOCOL.md | V3 | 1-8 PASS | Gate 9 |

### 1.4 Test Suites

| Asset | Source Repo | Gate Status | 阻塞项 |
|-------|------------|-------------|--------|
| V3 backend/tests/ | V3 | 1-8 PASS | Gate 9 |
| Producer tests/ | Producer | 1-8 PASS (1 known failure) | Gate 9 |

---

## 2. 需要适配后迁移（Class B）

| Asset | Source | 适配需求 | Gate 阻塞 |
|-------|--------|---------|-----------|
| scripts/ (~40 files) | Producer | 路径适配、import 调整 | Gate 6 (arch compat) |
| ocr_service/ | Producer | Docker 配置、路径适配 | Gate 6 |
| attacks/ | Producer | 测试框架适配 | Gate 6 |
| docs_audit/authority_matrix.yaml | V3 | 合并到新 governance 结构 | Gate 5 (dup check) |
| prd.md | Producer | 与 V3 prd 合并 | Gate 5 |
| question_identity_design.md | Producer | 与 Contract v0.2 对齐 | Gate 3 |
| resolver_contract_design.md | Producer | 与 Contract v0.2 对齐 | Gate 3 |
| production_adversarial_corpus_design.md | Producer | 评估与新架构兼容性 | Gate 6 |

---

## 3. 历史归档（Class C）

| Asset | Source | 归档理由 |
|-------|--------|---------|
| HANDOFFS/ (14+14 files) | Both | 历史通信记录，仅供追溯 |
| reports/ (7 files) | Producer | 历史报告 |
| V3 HANDOFFS/ | V3 | 同上 |
| Producer EVIDENCE/ | Producer | 历史审计证据 |

---

## 4. 待治理裁决（Class E — 无法迁移）

| Asset | Source | 阻塞原因 | 需要的决策 |
|-------|--------|---------|-----------|
| DESIGN-v1.1.md | V3 (untracked) | 无 git history, UNKNOWN authority | Owner: 是否 commit + assign authority |
| DESIGN-v1.md | V3 (untracked) | 同上 | Owner: superseded by v1.1? |
| IMPLEMENTATION-PLAN-v1.md | V3 (untracked) | 同上 | Owner: 是否 commit |
| IMPLEMENTATION-READINESS-v1.md | V3 (untracked) | 同上 | Owner: 是否 commit |
| IMPLEMENTATION-REPORT-PHASE1.md | V3 (untracked) | 同上 | Owner: 是否 commit |
| IMPLEMENTATION-REPORT-PHASE2.md | V3 (untracked) | 同上 | Owner: 是否 commit |
| CONTRACT-CONSUMER-REVIEW.md | V3 (untracked) | 同上 | Owner: 是否 commit |
| CONTRACT-v0.2-DRAFT-SKELETON.md | V3 (untracked) | 同上 | Owner: 是否 superseded |
| CONTRACT.md (early version) | V3 (untracked) | 同上 | Owner: historical or active? |
| GOVERNANCE/ (G0 docs) | V3 (untracked) | 同上 | Owner: 是否 commit |

---

## 5. 依赖关系与迁移顺序

**建议顺序**: Contract → Governance → Identity Modules → Tests → Scripts → OCR Service

---

## 6. 风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| Untracked docs 丢失 | HIGH | Owner 先 commit 到 V3 或 copy to AITutorX |
| Producer test failure (r67) | MEDIUM | 记录为 known issue，迁移后修复 |
| Script path adaptation | MEDIUM | 迁移后逐一验证 |
| DEC 编号冲突 | LOW | 已有映射表（Report C） |
