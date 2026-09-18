# REPORT-X2.5.1 — Fact Base Correction

**Document ID**: REPORT-X2.5.1
**Task**: TASK-X2.5.1
**Document Type**: Report / Correction Completion
**Status**: `X2.5.1 DOCUMENTS WRITTEN — AWAITING DSH DELTA AUDIT`
**Date**: 2026-09-18
**Role**: Evidence Corrector / Fact-Base Maintainer
**Non-role**: Migration Authority；Migration Gate；Independent Auditor

---

## 0. Evidence Anchor（纠正后）

```text
X2.5 pre-change baseline snapshot
  = 2151998c650efb8e7325f6251acc71bc9bc39521
X2.5 result commit (before X2.5.1)
  = 96053a83eff5b327be6fdb34c69aea9b73bcdfd5
Current AITutorX HEAD at X2.5.1 task start
  = 96053a8…（= origin/main）
V3 baseline = cc12d79e9a22f6274100ea0bb61f92493ba88509
Preprocessing baseline = 2b92898f05f6541a5fc65c8300cb8a59a06c4928
Frozen Contract = f4941ff… / sha256 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528 / 92197 bytes
```

Anchor ≠ Migration Authorization ≠ Gate Passed.

---

## 1. Correction deliverables

| Item | Required by task §10 | Where |
|------|----------------------|-------|
| 1. corrected baseline anchors | YES | X2.5.1-00/01；X2.5-00/01/REPORT-X2.5 纠正 |
| 2. corrected identity semantics | YES | X2.5.1-01 C2；X2.5-01/03/02 纠正 |
| 3. corrected CL-08 | YES | X2.5.1-03 §1；X2.5-05 纠正 |
| 4. new composite_question conflict | YES | **CL-21** |
| 5. corrupted manifest data-integrity finding | YES | **DI-01** |
| 6. Material implementation conflict | YES | **CL-22** |
| 7. evidence classification audit | YES | X2.5.1-02 |
| 8. X2.5 remains CONDITIONAL PASS pending DSH re-audit | YES | 本报告 + X2.5.1-00/03 |

---

## 2. Mandatory corrections summary

### C1 Baseline drift

```text
baseline snapshot (historical X2.5 evidence) = 2151998
resulting / current HEAD after X2.5         = 96053a8
Do NOT globally replace historical anchors.
```

### C2 V3 identity（refuted overstatement）

```text
V3 M2 identity implementation:
  hashlib.sha256(file_bytes).hexdigest()
  path: backend/app/core/raw_bytes_identity.py

NOT (for identity verification path):
  canonical_json as the source-identity hash

Governance definition retained:
  cross-system source identity = specified raw/original source identity

Producer: source_content_sha256 = SHA256(OCR markdown bytes)
V3:       original_sha256        = SHA256(original uploaded source bytes)
Do NOT imply these hashes must be equal.
```

### C3 CL-08 / mapping（refuted）

```text
An explicit mapping table exists.
Some mappings are implemented.
composite_question has no explicit mapping identified.

DO NOT invent: composite_question -> composite_unit
without Frozen Spec / Contract / implementation evidence.
```

New conflict: **CL-21**.

### C4 Corrupted manifest — DI-01

```text
Observed: unit_type = "andalone_question"
Expected: standalone_question | composite_question
Artifact: Ocr-markdown\reslice-batch-C\合格考\化学\2020北京高中合格考化学（第一次）（教师版）(1).manifest.json Q1
Population: exactly 1 (manifest face + IR face); v2 consumable face; R50 member
Corpus modified: NO
Disposition: OPEN / GATE IMPACT TO BE DETERMINED
```

### C5 Material — CL-22

```text
Domain: single Question may have Material (text/figure/image/chart/diagram/table/other).
Observed: V3 gate policy standalone units → empty material payload.
Classification: OPEN IMPLEMENTATION / SEMANTIC CONFLICT
Not called a confirmed bug in this task.
Production code unchanged.
```

### C6 Evidence labels

| Group | Labels |
|-------|--------|
| DSH major numbers 166/87/79/71/16/88/1664/4609/unique shas/Contract sha+size | `DSH-RECOMPUTED` / `DIRECTLY VERIFIED` |
| 177 / 356 | `ARTIFACT-BACKED` / `CLAIM-DOC`（非 DSH 本节清单） |
| 1801 / 12707 / 38893 | `CLAIM-DOC`（未独立复跑） |
| 86 lineage wording | `UNKNOWN` |
| Claude 自己先前报告 | **不是** independent verification |

---

## 3. X2.5 status after correction

```text
X2.5 = CONDITIONAL PASS
Pending: independent DSH X2.5.1 Delta Audit
X2.5 fully PASS = NOT DECLARED
X2.5.1 PASS = NOT DECLARED
```

---

## 4. Migration / Gate state（未改变）

```text
Migration Authorization     = UNAVAILABLE
approval_block.status       = invalid_without_charter
Migration Gate              = NOT PASSED / BLOCKED / NOT RUN
GATE_PASSED                 = 0
MIGRATED                    = 0
admitted=true               = NONE
OQ-GF                       = 18; zero CLOSED
BL-09/10/11                 = OPEN
D-048                       = pending_owner_decision
D2/D3/D4                    = OPEN
X2.5.1-Q-01..05             = OPEN（新增登记）
CL-21 / CL-22 / CL-23 / DI-01 = OPEN / TBD
```

---

## 5. Prohibitions honored

- production code / schema / corpus / manifests / V3 / preprocessing / Frozen Spec / Contract：**未修改**
- migration：**未执行**
- admitted / GATE_PASSED / MIGRATED：**未设置**
- OQ / BL / D-048：**未关闭**
- UNKNOWN / `composite_question` 映射 / DI-01 终局处置：**未强行裁决**
- X2.5 / X2.5.1 PASS：**未宣布**

---

## 6. Independent auditor path

1. Read X2.5.1-00/01/02/03 + 既有 X2.5 矩阵
2. Recompute anchors via `git rev-parse` / Contract sha256
3. Re-open V3 `raw_bytes_identity.py` / `gate/service.py` `_IR_TO_CANDIDATE_UNIT_TYPE` / `gate/policy.py`
4. Re-open Papers DQE / CLOSURE-PLAN / FACT-RECONCILIATION for DI-01
5. Confirm corpus untouched
6. Produce **DSH X2.5.1 Delta Audit**（Claude 不得代跑）

---

## 7. Git registration block

```text
X2.5 baseline commit     : 96053a83eff5b327be6fdb34c69aea9b73bcdfd5
X2.5.1 commit SHA        : <filled after commit>
parent SHA               : <filled after commit>
origin/main              : <filled after push>
changed files            : <filled after git status/diff>
insertions/deletions     : <filled after commit>
git status               : <filled after push>
```

---

## 8. End state

```text
X2.5 Fact Base after correction: DOCUMENTED / CONDITIONAL PASS
X2.5.1 Correction: DOCUMENTS WRITTEN — PUSHED (see §7)
Next independent step: DSH X2.5.1 Delta Audit
Migration Authorization: UNAVAILABLE
Migration Gate: NOT PASSED
Next actor after Delta Audit: Owner / DSH — NOT Claude self-authorization
```

**STOP condition**: correction push complete → STOP. Claude does not perform the DSH audit and does not declare X2.5.1 PASS.

*Fact base correction registered. Nothing migrated.*
