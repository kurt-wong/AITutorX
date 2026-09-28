# GAP-T-1 DB READBACK ADVERSARIAL REVIEW

```text
Document Type : Adversarial Review（对 GAP-T-1 DB readback 测试修复的对抗性复审）
readers       : Owner；实现者
Status        : CLOSED
Date          : 2026-09-27
Method        : 每条结论附探测/测试证据。无推测。
```

---

## VERDICT

```text
DB readback 真实性:       PASS（select + session.execute + row.field）
Persistence invariant:   PASS（write formula(x) → DB → read → assert == formula(x)）
Tautological elimination: PASS（不再是 formula(x) == formula(x)）
Runner code path lock:    FAIL — 测试复刻逻辑，不调用 _track_a / _run_full_chain
Full suite:               2071 passed（重跑确认）
```

**测试质量显著提升，但有一个残余缺口：测试不锁定 runner 的实际代码路径。**

---

## 一、VERIFIED CLAIMS

| # | 声明 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | 测试从 DB 读回 | `select()` + `session.execute` + `row.logical_execution_hash` | ✅ |
| 2 | 测试非恒真式 | write → DB read → assert pattern | ✅ |
| 3 | 2071 passed | 重跑全量 | ✅ |
| 4 | annotation 测试创建 SemanticAnnotation 并写入 DB | constructor + flush | ✅ |
| 5 | compile 测试创建 AdmissionCandidate 并写入 DB | constructor + flush | ✅ |

---

## 二、RESIDUAL GAP

### GAP-R-1 [MODERATE] 测试复刻 runner 逻辑，不调用 runner track 代码

**事实**：

| 测试 | 调用 runner 代码 | 说明 |
|---|---|---|
| `test_runner_le_hash_uses_unified_formula` (seal) | ✅ `_create_source_records` | 直接调用 runner 函数 |
| `test_runner_annotation_le_hash_persisted` | ⚠️ 仅 `_create_source_records`（setup） | annotation 创建是**复刻**，不走 `_track_a` |
| `test_compile_le_hash_persisted` | ❌ 无 | compile 创建是**复刻**，不走 `_run_full_chain` |

**后果**：若 `runner.py:156` 回归到 `sha256_hex(f"track-a:...")`，annotation 测试**仍会通过**——因为它测试的是自己复刻的代码，不是 runner 的。

**对照**：seal 测试更强——若 `_create_source_records` 回归，测试会失败。

**需补**（可选，不阻塞）：至少 1 条测试调用 `_track_a` 或 `_run_full_chain` 的 annotation/compile 路径并从 DB 读回。

---

## 三、测试质量对比

```text
修复前：assert formula(x) == formula(x)     ← 恒真式，零信息量
修复后：write formula(x) → DB → read → assert  ← 证明 persistence invariant
缺失：  call runner code → DB → read → assert   ← 锁定 runner 实际代码路径
```

---

## 四、修正后的真实状态

```text
LE HASH AUTHORITY CONSOLIDATION

Code:                     PASS
Formula unification:      COMPLETE
Persistence verification: PASS（GAP-T-1 已修复）
Runner code path lock:    PARTIAL（GAP-R-1，可选补强）
Follow-up:                GAP-T-2 OPEN（annotation_payload_hash alignment）
```

**结论**：GAP-T-1 的核心目标（persistence invariant）已达成。GAP-R-1 是进一步补强，不阻塞 LE hash 收敛关闭。

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。*
