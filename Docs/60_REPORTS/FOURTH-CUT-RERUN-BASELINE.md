# FOURTH-CUT-RERUN BASELINE

**Date**: 2026-10-02  
**Migration commit**: `dfc0331` `fix(alembic-0008): apply nullable before normalizing empty strings`  
**前一 commit**: `39840ff`  
**修改文件**: `backend/alembic/versions/20260908_0008_subject_grade_nullable.py`（仅 `upgrade()` 顺序）

```diff
-            op.execute(f"UPDATE {table} SET {col} = NULL WHERE {col} = ''")
+            # Order matters: drop NOT NULL before writing NULL…
             op.alter_column(table, col, existing_type=sa.String(), nullable=True)
+            op.execute(f"UPDATE {table} SET {col} = NULL WHERE {col} = ''")
```

---

## 1. Migration

```text
0003→0004→0005→0006→0007→0008→0009→0010→0011  SUCCESS
alembic_version = 0011
```

| 检查 | 结果 |
|---|---|
| questions.subject nullable | **YES** |
| questions.grade nullable | **YES** |
| 原 `subject=''` / `grade=''` 行 | **→ NULL / NULL**（`f2e306d9…`） |
| materials schema | OK（0 行） |

---

## 2. 全量测试

| 类别 | 结果 |
|---|---|
| **A setup/environment** | migration 302 errors **已消失** |
| **B actual test failure** | **2**（见下） |
| passed | **2151** |
| skipped / xfailed | 1 / 1 |

**2 failed（非业务回归）**：

```text
test_adv_state_audit::test_v3_worktree_clean_at_checkpoint
test_adv_state_audit::test_x_worktree_clean
```

原因：工作树含 Fourth Cut dirty 文件（resolver/adapter/runner），属 **state-audit 断言**，非功能失败。

> 清库前另见 23 failed / 4 errors，多为 DB 残留计数；truncate 后消失。

---

## 3. FOURTH-CUT-RERUN Baseline（9 卷 / 284 units）

| 指标 | **当前值** |
|---|---:|
| documents | **9** |
| source_versions | **9** |
| source_lines | **5741** |
| semantic_units | **284** |
| IR ready | **43** |
| IR not ready | **241** |
| candidates | **43** |
| approved | **1** |
| pending_review | **42** |
| skipped units（E2E） | 241 |
| questions | **1** |
| question_instances | **1** |
| materials | **0** |
| admission_events | **1** |
| validation_events | **1** |
| llm_call_audit | **28**（测试套写入） |
| **new LLM calls（E2E）** | **NOT PROVABLE**（未与测试隔离计数；Track A 无 LLM 调用路径） |
| alembic | **0011** |

历史数字（35/41/49 candidates、1213 llm audit）**仅作历史观察**，非当前 DB。

---

## 4. Q12–14 单独验收（B3b 已撤销）

| 项 | 值 |
|---|---|
| Producer declared answer | **451** |
| Producer artifact | `1\. C2\. C3\. …`（escaped-dot） |
| Resolver answer span | **593** |
| 593 内容 | `M: 5 days, from March, 7 to 12.`（听力台词） |
| 判定 | **非 missing / 非 ambiguous** — 唯一 `_ENTRY_RE` 命中即 593 |
| 451 | **未解析**（`\.` 使 entry 不匹配） |
| 593 是否正确答案 | **否** |

**未**用 density-max 强推 451；**未**把 593 当合法答案。  
**B3a = OPEN**（Producer unescape）。

---

## 5. Fourth Cut 状态（不变）

```text
A       PASS
B1      PASS
B2      PASS
B3a     OPEN — Producer dependency
B3b     REMOVED

Migration 0008  → FIXED (dfc0331)
Migration head  → 0011

Full test       → 2151 passed / 2 worktree-audit failed / 0 setup errors
9-paper E2E     → baseline above
Q12–14          → Resolver = 593 (illegal); declared 451 not read
```

Frozen Spec / Producer / overlap invariant / AnswerTokenContract **unchanged**。
