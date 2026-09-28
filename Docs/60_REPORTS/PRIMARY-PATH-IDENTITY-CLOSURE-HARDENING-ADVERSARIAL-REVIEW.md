# CLOSURE-HARDENING ADVERSARIAL REVIEW

```text
Document Type : Adversarial Review（对 Closure Hardening 结论的对抗性复审）
readers       : Owner；实现者
Status        : CLOSED
Date          : 2026-09-27
Method        : 每条结论附探测/测试证据。无推测。
```

---

## VERDICT

```text
GAP-1 fix (单一权威校验器):  PARTIAL — 单一定义 ✅，但 seal_document 绕过 canonical 拒绝
GAP-2 fix (runner 输出锁定): PASS — 真实调用 _create_source_records，断言完整
2061 passed claim:           PASS — 重跑确认
canonical handling:          PARTIAL — 行为正确，但缺专门测试；provider="" 是发明约定
```

**发现 1 个新 GAP（seal_document canonical bypass），2 个证据不足项。**

---

## 一、CONFIRMED GAPS

### NEW-GAP-1 [SEVERE] `seal_document` 绕过 `canonical` 拒绝

**声明 vs 事实**：

| 声明 | 事实 |
|---|---|
| seal 路径拒绝 `canonical`（`validate_seal_role_provider:50-51`） | `seal_document` 不调 `validate_seal_role_provider`，直接调 `validate_artifact_compatibility` |

**实证**：

```python
# seal.py:78 — seal_document 的校验调用
validate_artifact_compatibility(role, provider, _ARTIFACT_KIND)
# NOT: validate_seal_role_provider(role, provider)

# 后果：
validate_artifact_compatibility('canonical', '', 'raw_l1')  # → ACCEPTED
validate_seal_role_provider('canonical', '')                 # → REJECTED

# seal_document 用的是前者 → canonical 可通过 seal 入口
```

**根因**：`validate_seal_role_provider` 里的 `canonical` 拒绝是**死代码**（就 `seal_document` 调用链而言）。上一轮 GAP-3 的「恒真式」问题修了一半——把 `validate_artifact_kind(_ARTIFACT_KIND)` 换成了 `validate_artifact_compatibility(...)`，但没有改调 `validate_seal_role_provider`。

**需修**：`seal_document` 应调 `validate_seal_role_provider(role, provider)` 而非直接调 `validate_artifact_compatibility`。

---

### NEW-GAP-2 [MODERATE] `canonical` role 无专门测试

**事实**：`test_identity_phase_a.py` 中 `canonical` 仅作为 `artifact_kind` 出现（`canonical_l1`），**无任何测试断言 `role="canonical"` 的行为**。

`canonical` role 的正确行为（`provider=""` 接受、`provider="native"` 拒绝）仅被 2 个 fixture 改动间接覆盖（`test_repositories.py` / `test_repositories_dbflow.py`），无正面断言。

**需补**：至少 2 条测试——`canonical/""` accepted、`canonical/"native"` rejected。

---

### NEW-GAP-3 [LOW] `provider=""` 是发明约定，非 Spec 声明

**Spec 事实**（`10_Data_Model.md:151`）：

> `canonical` role **无 provider**。

**事实**：
- DB 列 `provider` 是 `String, nullable=False` — 不能存 NULL
- Spec 未指定「无 provider」在 NOT NULL 列中存什么
- 我选了 `provider=""` — **这是实现约定，不是 Spec 声明**
- 原 fixture 用 `provider="native"` — 同样不是 Spec 声明（且违反配对规则）

**影响**：不阻塞，但应显式登记为实现约定，避免被误读为 Spec 要求。

---

## 二、VERIFIED CLAIMS（确认无误的声明）

| # | 声明 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | `_ARTIFACT_KINDS` 单一定义 | 全仓 grep：仅 `models/source.py` 3 处（定义+使用） | ✅ PASS |
| 2 | GAP-2 测试调用真实 `_create_source_records` | AST 分析：import + call，无 mock | ✅ PASS |
| 3 | 2061 passed | 重跑全量：`2061 passed, 1 skipped, 1 xfailed` | ✅ PASS |
| 4 | `canonical/native` 被共享校验器拒绝 | 探测：`ValueError: mismatch` | ✅ PASS |
| 5 | `canonical/""` 被共享校验器接受 | 探测：accepted | ✅ PASS |
| 6 | runner 输出值锁定（role/provider/artifact_kind） | 3 条 `TestRunnerOutputValues` 测试，直接调用 | ✅ PASS |
| 7 | `validate_artifact_compatibility` 覆盖 repo 路径 | `source_repository.py:92` 调用 | ✅ PASS |

---

## 三、修正后的真实状态

```text
GAP-1 (单一权威校验器):       PARTIAL（NEW-GAP-1: seal_document bypass）
GAP-2 (runner 输出锁定):      PASS
canonical handling:           PARTIAL（NEW-GAP-2/3: 缺测试 + 发明约定）
Full suite:                   2061 passed, 0 failed（重跑确认）
```

**建议**：修 NEW-GAP-1（1 行改动：`seal_document` 调 `validate_seal_role_provider`）+ 补 NEW-GAP-2 测试（2 条），再关 Phase A。

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。*
