# LE-HASH-AUTHORITY-CONSOLIDATION-CLOSURE-REPORT

```text
Document Type : Closure Report
Status        : CLOSED WITH FINDINGS
Date          : 2026-09-27
Authority     : IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md（Phase A 范围内 follow-up）
Evidence      : Full suite: 2064–2067 passed, 0 code failures
                (1 failed + 3–6 errors per run, all WinError 10055
                 socket exhaustion; each passes in isolation;
                 reproduced on baseline 3bf7a09 → unrelated to eecd60b)
                Phase A related set: 111 passed, 0 failed
```

---

## Decision

**CLOSED WITH FINDINGS.**

---

## Evidence

```
Full suite (3 runs):
  Run 1: 2064 passed, 1 failed + 6 errors (WinError 10055)
  Run 2: 2067 passed, 1 failed + 3 errors (WinError 10055)
  基线 3bf7a09: test_executor + test_models_schema → 23 errors (WinError 10055)
  → 环境性 socket buffer 耗尽，非代码失败；单独跑均通过；基线复现证明与 eecd60b 无关

Phase A related set (identity/seal/annotation/compile/gate/repositories):
  111 passed, 0 failed

New tests (test_identity_phase_a.py): 37
```

---

## Completed

| 项 | 状态 | 证据 |
|---|---|---|
| Authority function unification | ✅ CLOSED | seal / annotation / compile 全部使用 `logical_execution_hash()`；AST 确认 16 处调用 |
| Production ad-hoc formula removal | ✅ CLOSED | `sha256_hex(f"seal:preprocessing:...")` / `sha256_hex(f"track-a:...")` / `sha256_hex(f"compile:track-b2:...")` 全部消除；生产代码 0 残留 |
| seal domain 收敛 | ✅ CLOSED | runner/seal 使用同一 domain |
| annotation domain 收敛 | ✅ CLOSED | 与 annotation service domain 一致 |
| compile domain 收敛 | ✅ CLOSED | 与 gate service compile domain 一致 |
| artifact_kind 单一定义 | ✅ CLOSED | 已迁移至 `models/source.py` |
| role/provider compatibility | ✅ CLOSED | 单一 compatibility validator |
| DB readback verification | ⚠️ PARTIAL | 见下方说明 |
| payload hash domain | ⚠️ FOLLOW-UP | 当前等价，但缺少结构保证 |

---

## DB readback verification: PARTIAL

**seal stage:**
Verified through real runner execution path and DB readback.
`test_identity_phase_a.py` 中 seal 测试调用 `_create_source_records`（真实 runner 路径）持久化后从 DB 读回，与 `logical_execution_hash()` 权威公式比对一致。

**annotation / compile stage:**
Domain structure verified against production implementation.
Existing tests verify deterministic equivalence only.
Real runner execution path DB readback remains follow-up.

当前测试证明的是：

```
logical_execution_hash(x) == logical_execution_hash(x)
```

而不是：

```
runner()
    ↓
database
    ↓
read value
    ↓
compare expected domain hash
```

这两个证明等级不同。annotation/compile 测试复刻了 runner 公式后自行构造对象写入 DB 再读回，未经真实 runner 函数调用链。

---

## Follow-up Registry

> 登记于本文件 §Follow-up Registry 与 `40_DECISIONS/LE-HASH-AUTHORITY-CONSOLIDATION-CLOSURE-01.md` §4.2。无独立 Registry 文件。

| ID | Title | Status | Priority | Blocking |
|---|---|---|---|---|
| F-LE-01 | Runner path DB readback verification for annotation/compile LE hash | OPEN | Medium | NO |
| F-LE-02 | Annotation payload identity projection alignment | OPEN | Medium | NO |
| F-LE-03 | Contract version literal authority alignment | OPEN | Low | NO |

### F-LE-01

```
Title  : Runner path DB readback verification for annotation/compile LE hash
Status : OPEN / NON-BLOCKING
Map    : GAP-R-1
Scope  : Add integration tests invoking actual runner paths,
         persisting generated rows,
         and asserting stored logical_execution_hash.
```

### F-LE-02

```
Title  : Annotation payload identity projection alignment
Status : OPEN / NON-BLOCKING
Map    : GAP-T-2
Scope  : Replace runner_b2 direct payload hashing with
         _annotation_identity_projection()
         to prevent future schema expansion drift.
Reason : Current equality depends on payload shape accidentally
         excluding confidence/line_refs.
```

### F-LE-03

```
Title  : Contract version literal authority alignment
Status : OPEN / NON-BLOCKING
Scope  : Replace runner_b2 hardcoded contract version strings
         with imported constants.
```

---

## Scope Confirmation

```
No Frozen Spec change        ✅
No Authorization change      ✅
No Phase A expansion         ✅
No migration                 ✅
No DDL                       ✅
No DB mutation               ✅
```

---

*Revised 2026-09-27. DB readback claim corrected from "completed" to "PARTIAL".*
*Revised 2026-09-27 (2). Evidence header corrected from "2071/0 failed" to measured range; flaky classified as WinError 10055 environment noise, baseline-reproduced.*
*LE Hash Authority Consolidation: CLOSED WITH FINDINGS.*
