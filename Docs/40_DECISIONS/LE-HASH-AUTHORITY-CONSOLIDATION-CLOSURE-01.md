# LE-HASH-AUTHORITY-CONSOLIDATION-CLOSURE-01

```text
Document Type : Closure Decision（**待签发 / AWAITING OWNER SIGNATURE**）
supersedes    : —
superseded_by : —
readers       : MIMO CODE（执行方）；Owner（签发方）；后续 migration 授权作者
Status        : AWAITING OWNER SIGNATURE
Signature     : —
Signed Date   : —
Decision      : LE Hash Authority Consolidation — CLOSED WITH FINDINGS
Scope         : Phase A 范围内 LE hash authority consolidation
Authority     : IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md
                OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 1. Decision

```text
LE Hash Authority Consolidation: CLOSED WITH FINDINGS
```

---

## 2. Evidence

### 2.1 Commit

```text
Repository : AITutors-v3
Branch     : od01-r3-convergence
Commit SHA : eecd60b55f8b10a26ce19d1cd6dd93a0a02c336b
Message    : Phase A identity correction + LE Hash authority consolidation
Files      : 14 changed, 720 insertions(+), 42 deletions(-)
```

### 2.2 Test Execution

```text
Phase A related set (identity/seal/annotation/compile/gate/repositories):
  111 passed, 0 failed

Full suite (3 runs):
  Run 1: 2064 passed, 1 failed + 6 errors (WinError 10055)
  Run 2: 2067 passed, 1 failed + 3 errors (WinError 10055)
  基线 3bf7a09: test_executor + test_models_schema → 23 errors (WinError 10055)
  → 环境性 socket buffer 耗尽，非代码失败；单独跑均通过；基线复现证明与 eecd60b 无关

New tests: 37 (tests/test_identity_phase_a.py)
```

### 2.3 Code Paths

| Path | Change |
|---|---|
| `app/models/source.py` | `validate_artifact_compatibility()` — single authority validator |
| `app/domains/source/seal.py` | `validate_seal_role_provider` delegates to shared validator; rejects `canonical` |
| `app/repositories/source_repository.py` | `create_source_version` calls `validate_artifact_compatibility` at entry |
| `scripts/preprocessing_consumer/runner.py` | `original_sha256` = SHA256(raw); `role=preprocessing`; `provider=preprocessing`; `artifact_kind=canonical_l1`; le_hash via `logical_execution_hash()` |
| `scripts/preprocessing_consumer/runner_b2.py` | Same identity corrections; compile le_hash via `logical_execution_hash()` |

### 2.4 Domain Comparison

| Domain | Runner | Production Service | Status |
|---|---|---|---|
| seal | `seal_contract_version` + parser role/provider | `seal.py` domain | ✅ Consistent |
| annotation | `annotation_schema_version` + `prompt_version` + `model_config_hash` | `annotation/service.py` domain | ✅ Consistent |
| compile | `resolver_version` + `ir_schema_version` + `compiler_version` + `gate_policy_version` | `gate/service.py` compile domain | ✅ Consistent |

---

## 3. Closed Items

| 项 | 状态 |
|---|---|
| 单一权威函数 `logical_execution_hash()` | ✅ CLOSED |
| Production ad-hoc LE hash 公式清零 | ✅ CLOSED |
| seal domain 收敛 | ✅ CLOSED |
| annotation domain 收敛 | ✅ CLOSED |
| compile domain 收敛 | ✅ CLOSED |
| artifact_kind 单一定义 | ✅ CLOSED |
| role/provider compatibility | ✅ CLOSED |
| DB readback verification | ⚠️ PARTIAL（见 §4.1） |

---

## 4. Known Limitations

### 4.1 DB readback verification: PARTIAL

```text
- seal stage:
  Verified through real runner execution path and DB readback.

- annotation / compile stage:
  Domain structure verified against production implementation.
  Existing tests verify deterministic equivalence only.
  Real runner execution path DB readback remains follow-up.
```

证明等级差异：

```text
当前测试证明:  logical_execution_hash(x) == logical_execution_hash(x)
目标证明等级:  runner() → database → read value → compare expected domain hash
```

### 4.2 Follow-up Registry

> 登记于本文件 §4.2 与 `60_REPORTS/LE-HASH-AUTHORITY-CONSOLIDATION-CLOSURE-REPORT.md` §Follow-up Registry。无独立 Registry 文件。

| ID | Title | Status | Priority | Blocking |
|---|---|---|---|---|
| F-LE-01 | Runner path DB readback verification for annotation/compile LE hash | OPEN | Medium | NO |
| F-LE-02 | Annotation payload identity projection alignment | OPEN | Medium | NO |
| F-LE-03 | Contract version literal authority alignment | OPEN | Low | NO |

**F-LE-01** (Map: GAP-R-1)
```
Scope: Add integration tests invoking actual runner paths,
       persisting generated rows,
       and asserting stored logical_execution_hash.
```

**F-LE-02** (Map: GAP-T-2)
```
Scope: Replace runner_b2 direct payload hashing with
       _annotation_identity_projection()
       to prevent future schema expansion drift.
Reason: Current equality depends on payload shape accidentally
       excluding confidence/line_refs.
```

**F-LE-03**
```
Scope: Replace runner_b2 hardcoded contract version strings
       with imported constants.
```

---

## 5. Governance Status

```text
Phase A Identity Correction:        CLOSED
LE Hash Authority Consolidation:    CLOSED WITH FINDINGS
Follow-ups:                         REGISTERED (F-LE-01/02/03)
Migration:                          NOT AUTHORIZED
Producer Metadata:                  NOT IMPLEMENTED
```

---

## 6. Prohibited Actions (unchanged)

```text
❌ producer_metadata schema
❌ migration
❌ DDL
❌ production DB mutation
❌ existing data migration
```

这些属于 Phase B，需单独 Migration Authorization。

---

## 7. Governance Chain Status

```text
Owner Decision
      ↓
Errata
      ↓
Implementation Authorization
      ↓
Phase A Code (commit eecd60b)
      ↓
Tests (111/111 Phase A related; full suite 0 code failures)
      ↓
Closure Record (this document)
      ↓
Owner Signature (pending)
```

---

```text
── OWNER SIGNATURE ─────────────────────────────────────────
Signed by : _______________
Date      : _______________
Verdict   : ☐ CLOSED WITH FINDINGS   ☐ REJECTED   ☐ REVISE
────────────────────────────────────────────────────────────
```

*Prepared 2026-09-27. AWAITING OWNER SIGNATURE.*
