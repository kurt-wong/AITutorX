# LE HASH CONSOLIDATION ADVERSARIAL REVIEW

```text
Document Type : Adversarial Review（对 LE hash 权威收敛结论的对抗性复审）
readers       : Owner；实现者
Status        : CLOSED
Date          : 2026-09-27
Method        : 每条结论附探测/测试证据。无推测。
```

---

## VERDICT

```text
Seal-stage LE hash consolidation:        PASS
Annotation-stage LE hash consolidation:  FAIL — ad-hoc 公式残留
Compile-stage LE hash consolidation:     FAIL — ad-hoc 公式残留
Full suite:                              2069 passed（重跑确认）
```

**结论「LE-HASH-AUTHORITY-CONVERGENCE → CLOSED」不成立。** seal 阶段收敛完成，但 annotation / compile 阶段仍是 ad-hoc 公式。

---

## 一、CONFIRMED GAP

### GAP-LE-1 [SEVERE] annotation / compile 阶段 le_hash 未收敛

**声明 vs 事实**：

| 声明 | 事实 |
|---|---|
| LE hash 权威收敛完成 | 仅 seal 阶段收敛；annotation / compile 阶段仍有 5 处 ad-hoc 公式 |

**实证 — 5 处残留**：

```
runner.py:156         logical_execution_hash=sha256_hex(f"track-a:{sv_id}:{json.dumps(...)}")
runner_b2.py:415      logical_execution_hash=sha256_hex(f"track-b2:{sv_id}")
runner_b2.py:466      le_hash = sha256_hex(f"compile:track-b2:{sv_id}:{ann.id}:{root.unit_id}")
p32_enforcement_experiment.py:87   sha256_hex("ann")
p32_enforcement_experiment.py:98   sha256_hex("gate")
```

**对照 — 生产服务已用权威公式**：

```
annotation/service.py:62    le_hash = logical_execution_hash(...)   ✅
gate/service.py:197         le_hash = logical_execution_hash(...)   ✅
```

**后果**：runner 直接创建 `SemanticAnnotation`（不经 `annotation/service.py`），用 ad-hoc 公式写 `logical_execution_hash` 列。若同一语义操作经生产服务执行，会写入**不同的 le_hash**——同表身份不一致。

**探测证据**：

```python
sha = 'test-sv-id'
le_adhoc = sha256_hex(f'track-a:{sha}:{{"key":"value"}}')
le_authority = logical_execution_hash(
    task_type='semantic_annotation', stage='ann', ...)
# DIFFERENT: True
```

---

## 二、VERIFIED CLAIMS

| # | 声明 | 验证方法 | 结果 |
|---|---|---|---|
| 1 | seal 阶段旧公式 `seal:preprocessing` 彻底清除 | 全仓 grep `.py` 文件 | ✅ 0 处 |
| 2 | runner 与 seal 的 seal-stage le_hash 一致 | 同输入探测：IDENTICAL | ✅ PASS |
| 3 | `logical_execution_hash` 为权威函数 | `hashing.py:65-82` 唯一定义 | ✅ PASS |
| 4 | 2069 passed | 重跑全量 | ✅ PASS |
| 5 | 不同 role → 不同 le_hash | `test_different_roles_produce_different_le_hash` | ✅ PASS |

---

## 三、测试覆盖缺口

| 项 | 状态 | 说明 |
|---|---|---|
| seal-stage runner le_hash == 权威公式 | ✅ `test_runner_le_hash_uses_unified_formula` | 已覆盖 |
| annotation-stage runner le_hash == 权威公式 | ❌ **无测试** | GAP-LE-1 未锁定 |
| compile-stage runner le_hash == 权威公式 | ❌ **无测试** | GAP-LE-1 未锁定 |

---

## 四、修正后的真实状态

```text
LE-HASH-AUTHORITY-CONVERGENCE:  PARTIAL（非 CLOSED）
  seal stage:       CONVERGED ✅
  annotation stage: NOT CONVERGED ❌（GAP-LE-1）
  compile stage:    NOT CONVERGED ❌（GAP-LE-1）
  experiment scripts: NOT CONVERGED（p32，低优先级）
```

**建议**：将 GAP-LE-1 列为新的 OPEN follow-up，或在本轮补完后再关闭 LE hash 收敛项。

---

*Reviewed 2026-09-27. 每条结论均有探测/测试证据。*
