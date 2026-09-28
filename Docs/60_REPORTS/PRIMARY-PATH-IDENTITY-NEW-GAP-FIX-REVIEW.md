# NEW-GAP FIX ADVERSARIAL REVIEW

```text
Document Type : Adversarial Review（对 NEW-GAP-1/2/3 修复的对抗性复审）
readers       : Owner；实现者
Status        : CLOSED
Date          : 2026-09-27
Method        : 每条结论附探测/测试证据。无推测。
```

---

## VERDICT

```text
NEW-GAP-1 (seal_document canonical bypass):  FIXED ✅
NEW-GAP-2 (canonical 无专门测试):             FIXED ✅
NEW-GAP-3 (provider="" 未登记):               FIXED ✅
Full suite:                                   2066 passed, 0 failed
New gaps found:                               0
```

---

## 一、修复验证（逐条探测）

### NEW-GAP-1 FIXED — seal_document 现在走 `validate_seal_role_provider`

**探测 1**：函数调用链

```python
inspect.getsource(SealService.seal_document)
→ 'validate_seal_role_provider(role, provider)'     # 不再直接调 validate_artifact_compatibility
```

**探测 2**：行为验证

```python
validate_seal_role_provider('canonical', '')
→ ValueError: seal does not produce canonical role    # 被拒绝 ✅
```

**探测 3**：无残留直接调用

```
seal_document calls validate_artifact_compatibility directly: False
seal_document calls validate_seal_role_provider: True
```

---

### NEW-GAP-2 FIXED — canonical 有专门测试

新增 5 条测试，AST 确认调用真实函数：

```
test_canonical_empty_provider_accepted:      validate_artifact_compatibility('canonical', '', ...)     → accepted
test_canonical_native_provider_rejected:     validate_artifact_compatibility('canonical', 'native', ...) → ValueError
test_canonical_preprocessing_provider_rejected: 同上反向 → ValueError
test_seal_rejects_canonical_role:            validate_seal_role_provider('canonical', '')               → ValueError
test_seal_rejects_canonical_even_with_empty_provider: 同上 → ValueError
```

---

### NEW-GAP-3 FIXED — provider="" 约定已登记

```python
# models/source.py
# [NEW-GAP-3 登记] provider="" 是实现约定（Spec 未指定 NOT NULL 列的空 provider 存储值），
# 不是 Spec 声明。如 Owner 裁定其他约定，需同步修改此处与测试 fixture。
"canonical": frozenset({""}),
```

---

## 二、对抗性探测（寻找残留问题）

| # | 探测 | 方法 | 结果 |
|---|---|---|---|
| 1 | `_ARTIFACT_KINDS` 是否单一定义 | 全仓 grep | ✅ 3 处，全在 `models/source.py` |
| 2 | `seal_document` 是否还有直接调用 | `inspect.getsource` | ✅ 无残留 |
| 3 | 所有 `create_source_version` 调用点是否过校验 | 全仓 grep call sites | ✅ 4 处，全部经 repo 层校验 |
| 4 | canonical 测试是否调用真实函数 | AST call analysis | ✅ 真实调用，无 mock |
| 5 | repo 层能否拒绝非法配对 | 直接探测 | ✅ `(preprocessing, native)` rejected |
| 6 | repo 层能否拒绝非法 artifact_kind | 直接探测 | ✅ `markdown` rejected |
| 7 | 全量测试 | 重跑 | ✅ 2066 passed, 0 failed |

---

## 三、写入路径覆盖矩阵

| 写入路径 | 校验位置 | 状态 |
|---|---|---|
| `seal.py:seal_document()` | `validate_seal_role_provider` → `validate_artifact_compatibility` | ✅ |
| `runner.py:_create_source_records()` | `create_source_version` → `validate_artifact_compatibility` | ✅ |
| `runner_b2.py:_create_source_records()` | 同上 | ✅ |
| `p32_enforcement_experiment.py` | 同上（`artifact_kind="pdf"` 会被拒） | ✅ |
| 任何直接调 `create_source_version` | repo 层入口校验 | ✅ |

---

## 四、测试计数

```
Phase A 基线:                2055
Closure Hardening GAP 修复:  +6
NEW-GAP 修复:                +5
────────────────────────────────
Total:                      2066 passed, 0 failed
```

---

## 五、结论

**三个 NEW-GAP 全部修复，对抗性探测未发现新问题。** Phase A Closure 可以关闭。

```text
Identity semantics        PASS
Authorization boundary    PASS
Implementation scope      PASS
Artifact compatibility    PASS
Persistence invariant     PASS
Consumer regression       PASS
Report accuracy           PASS
Canonical handling        PASS    ← NEW-GAP-1/2/3 关闭
```

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。*
