# LE HASH CONSOLIDATION ADVERSARIAL REVIEW 2

```text
Document Type : Adversarial Review（对 annotation/compile le_hash 收敛的对抗性复审）
readers       : Owner；实现者
Status        : CLOSED
Date          : 2026-09-27
Method        : 每条结论附探测/测试证据。无推测。
```

---

## VERDICT

```text
Seal-stage le_hash consolidation:           PASS
Annotation-stage le_hash FORMULA:           PASS（已切换到 logical_execution_hash）
Compile-stage le_hash FORMULA:              PASS（已切换到 logical_execution_hash）
Annotation/compile TEST COVERAGE:           FAIL — 测试恒真式，不锁定 runner 输出
Full suite:                                 2071 passed（重跑确认）
```

**代码收敛完成，但测试未锁定 runner 实际输出的 annotation/compile le_hash。**

---

## 一、CONFIRMED GAPS

### GAP-T-1 [MODERATE] annotation/compile 测试是恒真式

**声明 vs 事实**：

| 声明 | 事实 |
|---|---|
| 新增 annotation/compile le_hash 测试 | 测试断言 `expected == logical_execution_hash(同参数)`，即 `formula(x) == formula(x)` |

**实证**：

```python
# test_compile_le_hash_uses_unified_formula 实际做的事：
expected = logical_execution_hash(task_type=..., stage=..., ...)
assert expected == logical_execution_hash(task_type=..., stage=..., ...)
# ↑ 永真，即使 runner 用完全不同的公式也通过
```

**对比**：seal-stage 测试 `test_runner_le_hash_uses_unified_formula` 是正确的——它调用 `_create_source_records`，从 DB 读 `v.logical_execution_hash`，与权威公式比对。annotation/compile 测试缺少这一步。

**需补**：至少 2 条测试从 DB 读 runner 实际写入的 annotation/compile le_hash 并与权威公式比对。

---

### GAP-T-2 [LOW] annotation_payload_hash 计算方式不同

**事实**：
- 生产：`sha256_hex(_annotation_identity_projection(payload))` — 剥离 `confidence`/`line_refs`
- runner：`sha256_hex(payload)` — 直接 hash

**当前影响**：无。preprocessing payload 不含 `confidence`/`line_refs`（`annotation_adapter.py` 零命中），projection 是 no-op。

**潜在风险**：若未来 preprocessing payload 含这些字段，hash 会静默变化。

---

## 二、VERIFIED CLAIMS

| # | 声明 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | annotation domain 结构与生产一致 | 逐字段比对 keys | ✅ MATCH |
| 2 | compile domain 结构与生产一致 | 逐字段比对 keys | ✅ MATCH |
| 3 | runner 生产代码 ad-hoc le_hash = 0 | 全仓 grep（排除 p32） | ✅ 0 处 |
| 4 | runner.py 调用 logical_execution_hash 2 次 | AST call analysis | ✅ |
| 5 | runner_b2.py 调用 logical_execution_hash 3 次 | AST call analysis | ✅ |
| 6 | 2071 passed | 重跑全量 | ✅ |
| 7 | 剩余 sha256_hex 是合法用途（model_config_hash 等） | 逐行检查 | ✅ 非 le_hash |

---

## 三、修正后的真实状态

```text
LE-HASH-AUTHORITY-CONVERGENCE:  PARTIAL
  formula consolidation:  COMPLETE ✅（0 ad-hoc 残留）
  test coverage:          PARTIAL ❌（GAP-T-1: annotation/compile 测试恒真式）
  payload hash consistency: LATENT ⚠️（GAP-T-2: projection 差异，当前无影响）
```

**建议**：补 2 条测试从 DB 读 annotation/compile le_hash 并锁定，再关闭 LE hash 收敛。

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。*
