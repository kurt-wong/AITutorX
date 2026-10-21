# ENV BLOCKER — Alembic 0008 NotNullViolation（STOP）

**Date**: 2026-10-02  
**阶段**: 环境修复 Phase 2  
**裁决**: 命中停止条件 — **未改 migration、未改数据、未继续回归**

---

## 1. B3b 已撤销

`qn-entry density-max` 已从 `resolver.py::_answer_span` **删除**。  
多行 answer 命中恢复为 **`ambiguous`（spans multiple lines）**。  
**B3a = OPEN**（Producer `1\.` 转义依赖）；未改 Producer。

---

## 2. Migration 实测（与预告一致）

### 迁移序列

```text
0003 → 0004  ok
0004 → 0005  ok
0005 → 0006  ok
0006 → 0007  ok
0007 → 0008  FAILED
```

### 失败原文

```sql
UPDATE questions SET subject = NULL WHERE subject = ''
```

```text
NotNullViolationError: null value in column "subject" of relation "questions"
Failing row: (null, , single_choice, c806c1b7…, f2e306d9…, 2026-10-02…)
```

### 0008 `up()` 语句顺序（`20260908_0008_subject_grade_nullable.py`）

```python
op.execute(f"UPDATE {table} SET {col} = NULL WHERE {col} = ''")  # :22  ← 先 UPDATE
op.alter_column(table, col, existing_type=sa.String(), nullable=True)  # :23  ← 后 DROP NOT NULL
```

**缺陷**：先 `UPDATE → NULL`，后 `nullable=True`。在 `subject NOT NULL` 下 UPDATE 必失败。

### questions 那 1 行

```text
id         = f2e306d9-c3e5-4d13-a410-b4cce6b0d182
subject    = ''          (empty string, not NULL)
grade      = ''          (empty string, not NULL)
type       = single_choice
```

### 迁移前统计（已预检）

```text
questions rows     = 1
subject_null       = 0
subject_empty      = 1
grade_null         = 0
grade_empty        = 1
alembic_version    = 0003
questions.subject  is_nullable = NO
questions.grade    is_nullable = NO
candidates         = 49（旧 schema 上 reseed）
```

失败后状态不变：`alembic_version=0003`（transactional DDL 回滚 0004–0007）。

---

## 3. 需要 Owner 裁决（二选一，性质不同）

| 选项 | 内容 | 性质 |
|---|---|---|
| **A. 改 migration** | 0008 交换顺序：先 `alter_column nullable=True`，再 `UPDATE … = NULL` | 修迁移实现 |
| **B. 先清/改那一行** | 删除或改写 `f2e306d9…` 的 `subject/grade`（`''`→占位非空或删行）后再 `upgrade` | 动数据 |

两者都不由 MIMO 自行决定。

---

## 4. 当前状态

```text
A       PASS
B1      PASS
B2      PASS
B3a     OPEN — Producer dependency
B3b     REMOVED

Migration environment   BLOCKING @ 0008
Full regression         PENDING
E2E reseed baseline     PENDING

Frozen Spec / Producer / overlap invariant / AnswerTokenContract  unchanged
```

工程信号（A/B1/B2）仍在，但 **before/after 审计基线** 须在 0008 裁决 + `alembic upgrade head` 成功后重建。
