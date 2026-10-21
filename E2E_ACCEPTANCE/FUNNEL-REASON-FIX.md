# Funnel 拒绝原因漂移修复 — 执行报告

**基线**：`d45cc9d` → **`5689ef1`**

## 1. 代码变更

| 文件 | 差异 |
|---|---|
| `compile/ir.py` | 抽出 `collect_validation_problems()`（与 `_validate_node` **同一问题列表**） |
| `source/funnel_recorder.py` | `ir_skip_reasons()` **只调用**该函数，删除手写 leaf 分支 |
| `tests/test_funnel_reasons_match_ir.py` | 新增 3 项：多题 composite / standalone / 单题 composite |

**优先复用真实校验器**，无双份规则。

## 2. 测试

**50 passed**（含 compiler/gate/manifest/composite/funnel 全回归）。

## 3. 真实管线（地理，新 run_id）

- 库：`aitutors_e2e_4paper`（`current_database()` 已断言）
- run_id：`baae0135-650d-4a29-ad66-3021e8246dfc-030d54f3`
- 结果：**25 单元全拒，0 候选**（安全，无假单题）

**本轮漏斗原因（真实校验器）**：
```
shared component material unresolved; composite has no sub_questions
```
**已无** leaf 式 `stem not declared; options missing…` 漂移。

（历史同名漏斗文件仍保留旧原因，不清理、不冒充本轮。）

## 4. 验收库

`aitutors_test`：21 Q / 21 I / **3 FB** 未变。

## 5. 停止

等待下一项裁决。
