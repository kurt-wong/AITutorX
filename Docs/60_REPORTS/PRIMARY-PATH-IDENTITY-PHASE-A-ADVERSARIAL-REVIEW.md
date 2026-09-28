# PRIMARY-PATH-IDENTITY-PHASE-A-ADVERSARIAL-REVIEW

```text
Document Type : Adversarial Review（对抗性审查）
readers       : Owner；实现者；后续审计
Status        : CLOSED
Date          : 2026-09-27
Scope         : Phase A implementation（代码 + 测试 + 实现报告声明）
Authority     : IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md
Method        : 每条结论附真实测试/代码证据；无推测、无自我合理化
```

---

## 审查方法

1. 对实现报告的每项声明做**独立验证**（不采信报告，重新跑测试/写探测）
2. 对代码做**攻击性探测**（试图传入非法值，看是否被拒绝）
3. 对测试做**覆盖缺口分析**（声称覆盖的，测试里有没有断言）

---

## VERDICT

```text
Code implementation:     PASS（核心逻辑正确）
Authorization compliance: PASS（未越权）
Report accuracy:          PASS AFTER CORRECTION（修正版）
Test coverage:            FAIL — 2 项覆盖缺口（见下）
```

**不建议在补完 GAP-1 之前进入 Phase B 或关闭 Phase A。**

---

## 一、CONFIRMED GAPS（有实证的真实缺陷）

### GAP-1 [SEVERE] role/provider 配对校验未覆盖 consumer/repo 写入路径

**声明 vs 事实**：

| 声明 | 事实 |
|---|---|
| `role-provider enforcement` DONE | 值已改对，但**非法配对可静默持久化** |

**实证探测**：

```python
# 直接调用 create_source_version 传入非法配对 (preprocessing, native)
await repo.create_source_version(
    document_id=doc.id, artifact_kind='canonical_l1',
    role='preprocessing', provider='native',  # ← 非法配对
    ...
)
# 结果: ACCEPTED — role='preprocessing' provider='native'
```

**根因**：

```
validate_seal_role_provider()
  调用位置: seal.py:seal_document() 唯一入口
  覆盖路径: ✅ seal path
  覆盖路径: ❌ consumer path（runner.py / runner_b2.py 直接调 create_source_version）
  覆盖路径: ❌ repository path（create_source_version 不校验 role/provider 对）
```

**影响**：`role="preprocessing", provider="native"` 等非法配对可通过 runner 写入 DB，不被拒绝。

**需补**：在 `create_source_version` 中增加 role/provider 配对校验，或在 runner 调用前校验。

---

### GAP-2 [MODERATE] runner 实际输出值未被测试锁定

**声明 vs 事实**：

| 声明 | 事实 |
|---|---|
| `identity invariant tests` 21 条 DONE | 测试覆盖 validator + repository 接受正确值 |
| | **无测试验证 `_create_source_records` 实际写入 `role=preprocessing`** |

**实证**：

```bash
# 调用 _create_source_records 后检查 DB 行（探测结果）:
ROLE:     'preprocessing'     ✅ 值正确
PROVIDER: 'preprocessing'     ✅ 值正确
ARTIFACT: 'canonical_l1'      ✅ 值正确
MATCH: True

# 但搜索测试文件:
grep "role.*preprocessing|assert.*preprocessing" tests/
→ 仅 test_identity_phase_a.py 的 validator 测试
→ 4 个调用 _create_source_records 的测试文件（test_real_producer_activation.py,
  test_consumer_boundary_closure.py, test_x26_fint08, test_x26_frb01）
  均不断言 role/provider/artifact_kind 值
```

**影响**：runner 的 identity 字段若回归（如有人改回 `role="native"`），测试套件仍全绿。

**需补**：至少 1 条测试直接调用 `_create_source_records` 并断言输出的 `role`/`provider`/`artifact_kind`。

---

## 二、MINOR ISSUES

### GAP-3 [LOW] seal.py 的 artifact_kind 校验在调用点是恒真式

```python
# seal.py:validate_seal_document()
validate_artifact_kind(_ARTIFACT_KIND)  # _ARTIFACT_KIND = "raw_l1" (常量)
```

`_ARTIFACT_KIND` 是硬编码常量，对闭集校验恒通过。该调用仅在开发者把 `_ARTIFACT_KIND` 改为非法值时才有用（编译期防护），不拦截运行时非法值。

**注**：repository 层的校验是**动态的**（校验函数参数，非常量），实际运行时防护有效：

```python
# source_repository.py:91（已验证是参数级校验，非恒真）
if artifact_kind not in _ARTIFACT_KINDS:
    raise RepositoryError(...)
```

**需补**：无需紧急修复。可将 seal.py 改为传入实际使用的值（如 result-derived）以消除恒真式。

---

### GAP-4 [LOW] p32_enforcement_experiment.py 使用已被拒绝的值

```python
# p32_enforcement_experiment.py:50
artifact_kind="pdf", role="native", provider="native"
```

`artifact_kind="pdf"` 现在被 repository 校验拒绝。该脚本若运行将抛 `RepositoryError`。不在测试套件中，不影响 CI。

**需补**：Owner 决定是否更新或弃用该实验脚本。

---

## 三、VERIFIED NON-ISSUES（确认无问题的项）

| # | 声明 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | `original_sha256` 使用 raw bytes | 探测 `load_raw_bytes_identity().sha256 == hashlib.sha256(bytes).hexdigest()` | ✅ PASS |
| 2 | `artifact_kind` 闭集校验有效（repo 层） | 传入 `markdown` → `RepositoryError` | ✅ PASS |
| 3 | 双 `_ARTIFACT_KINDS` 常量一致 | `seal_kinds == repo_kinds` → `True` | ✅ 一致（tech-debt 已登记） |
| 4 | le_hash 公式不兼容 | 同一输入跑两种公式，hash 不同 | ✅ 确认不兼容（OPEN follow-up 正确登记） |
| 5 | TOCTOU 顺序 | runner_b2 中 `_verify_identity_boundary` 先于 `_create_source_records` | ✅ 顺序正确 |
| 6 | model_schema 测试 | 5/5 passed | ✅ PASS |
| 7 | 全量测试套件 | 2055 passed, 1 skipped, 1 xfailed | ✅ PASS |
| 8 | BOM/CRLF 敏感性 | 21 条新测试中已覆盖 | ✅ PASS |
| 9 | le_hash 是 original_sha256 的函数 | `test_le_hash_is_function_of_original_sha256` passed | ✅ PASS |
| 10 | API 兼容 | schemas 为 str 透传 + `order_by(role)` 字典序 | ✅ 无破坏 |

---

## 四、测试覆盖矩阵

| 授权要求的测试 | 有无测试 | 测试位置 | 锁定的断言 |
|---|---|---|---|
| preprocessing/preprocessing/canonical_l1 accepted | ✅ | `TestValidCombinations` | validator 层 |
| preprocessing with wrong provider rejected | ✅ | `TestRoleProviderEnforcement` | validator 层（**仅 seal 入口**） |
| markdown artifact_kind rejected | ✅ | `TestArtifactKindClosedSet` + `TestRepositoryEnforcement` | validator + repo 层 |
| raw byte hash identity preserved | ✅ | `TestRawByteIdentity` | `load_raw_bytes_identity` |
| le_hash 一致性 | ✅ | `TestDerivedHashDependency` | 纯函数层 |
| invalid artifact combinations cannot persist | ✅ | `TestRepositoryEnforcement` | repo 层 |
| **runner 实际写入正确值** | ❌ **缺失** | — | — |
| **非法 role/provider 组合在 repo 层被拒** | ❌ **缺失** | — | — |

---

## 五、修正后的真实状态

```text
Phase A Code Implementation:       PASS（核心逻辑正确）
Phase A Authorization Compliance:  PASS（未越权）
Implementation Report:             PASS（修正版）

Test Coverage:                     FAIL
  GAP-1  role/provider 校验未覆盖 consumer/repo 路径   [SEVERE]
  GAP-2  runner 输出值未被测试锁定                      [MODERATE]
  GAP-3  seal artifact_kind 校验恒真式                  [LOW]
  GAP-4  p32_experiment 使用已拒绝值                    [LOW]

Remaining Technical Follow-ups:
  1. LE-HASH-AUTHORITY-CONVERGENCE         OPEN
  2. artifact_kind authority extraction    OPEN
  3. provider_reality.json classification  OPEN
```

---

## 六、建议

**立即修（Phase A 内，LEVEL 1）**：
1. `create_source_version` 加 role/provider 配对校验（闭 GAP-1）
2. 加 1 条测试锁定 `_create_source_records` 输出值（闭 GAP-2）
3. 加 1 条测试锁定非法配对在 repo 层被拒（闭 GAP-1 的测试面）

**不阻塞 Phase A 关闭但应登记**：
4. seal.py 恒真式校验（GAP-3）
5. p32 脚本处置（GAP-4）

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。无推测结论。*
