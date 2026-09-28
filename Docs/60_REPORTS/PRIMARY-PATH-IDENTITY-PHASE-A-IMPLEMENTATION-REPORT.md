# PRIMARY-PATH-IDENTITY-PHASE-A-IMPLEMENTATION-REPORT

```text
Document Type : Implementation Report（修正版）
supersedes    : MIMO CODE 会话内初版实现报告（含 3 处过度声明，已修正）
superseded_by : —
readers       : Owner；实施审计；后续 Phase / follow-up 执行者
Status        : CLOSED（报告完成；含 3 项 OPEN follow-up）
Date          : 2026-09-27
Authority     : IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md（Phase A）
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

**本报告性质**：对 Phase A 代码实现的**证据记录**。初版报告有 3 处将「未完成/未验证」写成了
「已完成」，本修正版逐条收敛。代码未做任何额外修改。

---

## 0. 修正对照（初版 → 本修正版）

| # | 初版表述 | 问题 | 修正后表述 |
|---|---|---|---|
| 1 | `derived hash dependencies remain consistent` | le_hash 生成仍是双公式，非「一致」 | 影响链已处理；**收敛未完成**，列 OPEN follow-up |
| 2 | `source repository predicate alignment — Phase A 完成` | 该能力为「检查并确认一致」，未发生修改 | **NOT CHANGED** — 既有对齐确认，无需修改 |
| 3 | `api compatibility review — completed` | 无 review artifact | 补证据段：已审阅，判定不改，附理由 |

---

## 1. Changed files

| # | File | Change | 对应授权能力 |
|---|---|---|---|
| 1 | `app/domains/source/seal.py` | +`_ARTIFACT_KINDS` 闭集常量；+`validate_artifact_kind()`；`_SEAL_ROLE_PROVIDERS` 加 `preprocessing ⟺ preprocessing` | `seal role-provider enum extension` + `artifact-kind validation` |
| 2 | `app/repositories/source_repository.py` | +artifact_kind 闭集校验于 `create_source_version` 入口 | `artifact-kind validation`（repository path） |
| 3 | `scripts/preprocessing_consumer/runner.py` | `original_sha256` 改为 `load_raw_bytes_identity().sha256`；`role/provider` → `preprocessing`；`artifact_kind` → `canonical_l1` | `original_sha256 identity-domain correction` + `role-provider enforcement` + `artifact-kind compatibility enforcement` |
| 4 | `scripts/preprocessing_consumer/runner_b2.py` | 同上 | 同上 |
| 5-10 | `test_gate_service.py` / `test_admission.py` / `eb008_helpers.py` / `test_seal_dbflow.py` / `test_adversarial_evidence_boundary.py` / `test_adversarial_seal_immutability.py` | `artifact_kind="pdf"` → `"raw_l1"`（"pdf" 不在 Spec 闭集，新校验拒绝） | `model schema test alignment` |
| 11 | `tests/test_identity_phase_a.py` | **新增** 21 条 identity invariant 测试 | `identity invariant tests` |

### 1.1 `identity byte-domain correction` 细节

```
before:  file_sha = sha256_hex(body_text)        ← canonical_json 包裹，错误 hash 族
after:   raw_id = load_raw_bytes_identity(source_path)
         file_sha = raw_id.sha256                ← SHA256(raw bytes)，正确
```

`runner_b2.py` 的 `_verify_identity_boundary` 中已有 `load_raw_bytes_identity` 调用（M2 步骤），
但其结果此前被丢弃、`_create_source_records` 重新用错误算法计算。本次修正使
`_create_source_records` 使用同一正确来源。

---

## 2. 按授权能力逐项状态

| 能力 | 状态 | 说明 |
|---|---|---|
| `identity byte-domain correction` | ✅ DONE | `runner.py` / `runner_b2.py` 均改为 raw-bytes SHA256 |
| `original_sha256 identity-domain migration` | ✅ DONE | Decision 2 Amendment (2-B) 落地 |
| `role-provider enforcement` | ✅ DONE | `role=preprocessing` / `provider=preprocessing` |
| `artifact-kind compatibility enforcement` | ✅ DONE | `artifact_kind=canonical_l1` |
| `artifact-kind validation` | ✅ DONE | 闭集校验器，覆盖 seal path + repository path |
| `seal role-provider enum extension` | ✅ DONE | `_SEAL_ROLE_PROVIDERS` 加 `preprocessing` |
| `derived hash recalculation logic` | ⚠️ PARTIAL | 见 §3 |
| `source repository predicate alignment` | ➖ NOT CHANGED | 见 §4 |
| `identity invariant tests` | ✅ DONE | 21 条新增，全部通过 |
| `model schema test alignment` | ✅ DONE | 6 文件 fixture 更新 |
| `api compatibility review` | ✅ REVIEWED | 见 §5 |

---

## 3. Derived Hash Impact — 修正声明

**初版写 `derived hash dependencies remain consistent`，不准确。**

### 3.1 实际状态

```
✅ original_sha256 已切换为 raw bytes identity
✅ le_hash 是 original_sha256 的函数 —— 输入变了，le_hash 跟着变
✅ 下游 identity 影响由测试覆盖（T-5: le_hash 一致性断言）
❌ le_hash 生成路径仍是双公式：
     runner.py / runner_b2.py:  sha256_hex(f"seal:preprocessing:{file_sha}")
     seal.py:                   logical_execution_hash(task_type, stage, contract_domain, input_domain)
❌ 单一权威 le_hash 函数收敛（EXEC-3 / D-PP-4）未在 Phase A 实现
```

### 3.2 正确表述

```text
original_sha256 identity-domain correction completed.

Derived hash impact reviewed:
- le_hash dependency identified.
- downstream identity impact covered by tests.

However:
- le_hash generation remains split between preprocessing runner and seal domain.
- Single authoritative le_hash function convergence (EXEC-3 / D-PP-4)
  is NOT implemented in Phase A.

Status: OPEN FOLLOW-UP ITEM
```

### 3.3 FOLLOW-UP: LE-HASH-AUTHORITY-CONVERGENCE

```text
Status:   OPEN
Reason:   Phase A 修正了 identity domain，但 le_hash 生成仍有多条调用路径。
Required: 单一权威 logical_execution_hash 实现。
Constraint: 需同步更新当前依赖 runner-local 公式的 invariant tests。
```

---

## 4. Source Repository Predicate Alignment — 修正声明

**初版写「Phase A 完成」，不成立 —— 该能力为检查性工作，未发生修改。**

```text
Status: NOT CHANGED IN PHASE A

Reason: 当前核查确认现有 ON CONFLICT target 与 re-read 谓词对齐：
          ON CONFLICT: (logical_execution_stage, logical_execution_hash)
          _version_by_le: WHERE stage = ? AND hash = ?
        两者一致，无需修改。

Future: 建议补回归覆盖，防止约束与谓词分叉。
```

---

## 5. API Compatibility Review — 补证据

```text
Reviewed:
  - app/api/schemas.py (SourceVersionInfo: artifact_kind/role/provider 均为 str 透传)
  - app/api/routers/documents.py (:132,:230,:268 order_by(role) 字典序排序)

Finding:
  - role/provider/artifact_kind 在 API schema 中为普通 str 字段，无枚举约束。
  - 新增取值 preprocessing / canonical_l1 不触发 schema 破坏。
  - order_by(role) 为字典序；preprocessing 插入后排序位置在 ocr_ppsvl 之后，
    纯展示顺序，无功能依赖。

Assessment: 现有行为（按 role 排序）为设计意图。无需 API 层代码变更。

Status: Reviewed — no code change required.
```

---

## 6. Tech-debt 登记

```text
TECH-DEBT: Duplicate artifact_kind authority definitions

Current:
  seal.py              _ARTIFACT_KINDS = frozenset({...})
  source_repository.py _ARTIFACT_KINDS = frozenset({...})

Future:
  Extract shared domain constant (e.g. app/models/source.py or app/core/)

Not blocking Phase A.
```

---

## 7. 非 Phase A 问题登记

```text
File:   backend/provider_reality.json
Date:   2026-09-26T05:04:40Z（早于 Phase A，非本轮产物）
Status: NOT A PHASE A VIOLATION
Action: Owner classify (archive / remove / gitignore)
```

---

## 8. Tests

```text
tests/test_identity_phase_a.py          21 passed  ← 新增 identity invariant
Full suite                           2055 passed, 1 skipped, 1 xfailed
```

新增测试覆盖：
1. preprocessing/preprocessing/canonical_l1 accepted
2. preprocessing with wrong provider rejected
3. markdown / pdf / empty artifact_kind rejected
4. raw byte hash identity preserved（BOM / CRLF 敏感性）
5. le_hash 作为 original_sha256 的函数（同入同出、异入异出）
6. invalid artifact combinations cannot persist（repository 层）

---

## 9. Confirmation

```text
No migration       ✅
No DDL             ✅
No DB mutation     ✅
No Spec change     ✅
No Papers change   ✅
```

---

## 10. 最终状态（含对抗性审查 GAP 修复）

```text
Phase A Code Implementation:       PASS
Phase A Authorization Compliance:  PASS
Implementation Report:             PASS（修正版）
Invariant Coverage:                PASS（GAP-1/2 已修复）
```

### 10.1 对抗性审查 GAP 修复记录

| GAP | 级别 | 修复 | 证据 |
|---|---|---|---|
| GAP-1 | SEVERE | `validate_artifact_compatibility` 单一权威校验器（`models/source.py`），seal + repository 双入口调用 | `(preprocessing, native)` 被 repo 层拒绝（3 条新增测试） |
| GAP-2 | MODERATE | 3 条 runner 输出值锁定测试（`TestRunnerOutputValues`） | 直接调用 `_create_source_records` 断言 `role/provider/artifact_kind` |
| GAP-3 | LOW | seal 的恒真式校验改为委托共享校验器 + `canonical` 专属拒绝 | `validate_seal_role_provider` 委托 + `if role == "canonical"` |
| GAP-4 | LOW | `p32_enforcement_experiment.py` 使用 `artifact_kind="pdf"` 现被 repo 层拒绝 | 登记，不阻塞 |

### 10.2 附带修正

- `canonical` role 补入配对表（Spec「无 provider」→ `provider=""`）
- 2 个测试 fixture 从 `provider="native"` 修正为 `provider=""`（canonical 无 provider）
- 消除 `seal.py` / `source_repository.py` 双 `_ARTIFACT_KINDS` 常量（tech-debt 关闭）

```text
Full suite: 2061 passed, 1 skipped, 1 xfailed
  (Phase A 基线 2055 + GAP 修复新增 6)
```

### 10.3 Remaining Technical Follow-ups

```text
1. LE-HASH-AUTHORITY-CONVERGENCE         OPEN
2. provider_reality.json classification  OPEN
```

（artifact_kind authority extraction 已随 GAP-1 修复关闭。）

---

*Recorded 2026-09-27. 本报告为 Phase A 实现证据修正版。初版报告的 3 处过度声明已收敛，代码未做额外修改。*
