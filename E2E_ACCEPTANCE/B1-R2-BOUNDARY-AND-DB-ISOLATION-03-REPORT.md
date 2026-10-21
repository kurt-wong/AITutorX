# TASK B1-R2-BOUNDARY-AND-DB-ISOLATION-03 · 最终报告

## A. 三仓基线与工作区

| 仓 | 分支 | HEAD | 工作区 |
|---|---|---|---|
| AITutors-v3 | `od01-r3-convergence` | `667fb32`（核实为实际基线）→ 本轮新提交见 G | 仅他人未跟踪 `backend/scripts/_p14b_*.py` |
| AITutor-X | `main` | `7bce066` | 大量未跟踪报告 |
| Papers | `main` | `d42cde6` | 未跟踪 `_p14b_*` |

数据库快照（调查用，非永久基线）：documents=13、document_source_versions=1、questions=0、admission_candidates=0、question_instances=0、tasks=16。

---

## B. DA-38 Errata

**文件**：`Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md`（NOT FROZEN，授权可改）

**插入位置**：「边界声明」之前，新增 `## Errata` 节。

**修改范围对照**：

| 项 | 修改前 | 修改后 |
|---|---|---|
| DA-38 / B1-G4 绑定落点 | raw bytes **写入 `documents.original_sha256`** | 绑定在 **Source Version 层**（`source_meta` / `input_identity`）；`original_sha256` 仅原件字节 |
| §1.3 `original_sha256` | 「将来装接口键值」 | 「**仅**原始文档字节身份；接口键不入此列」 |
| 多 MD 对一 PDF | 未说明 | 允许；经 `DocumentSourceVersion.parent_version_id` 血统 |
| `input_identity` | 未说明 | P7 输入身份 JSONB；可同时记原件哈希与 `source_content_sha256`，非第二 UNIQUE 键 |
| `role=preprocessing` | 未对照 | **显式登记**：代码有、Frozen Spec 10 §4.2 role 枚举无 |
| Frozen Spec 10 结构/UNIQUE/哈希格式/path 非身份 | — | **全部不变** |

**未决**：`role=preprocessing` 是否补入 Spec role 枚举 → Owner。

---

## C. 身份校验规则迁移

### 迁移前

`app/domains/source/preprocessing_import.py` → `sys.path.insert` → `scripts.preprocessing_consumer.boundary.enforce_interface_scope`

### 迁移后

```
app/domains/source/identity_scope.py          ← 唯一规则权威（新建）
        ↑
app/domains/source/preprocessing_import.py    ← 生产入口直接依赖
        ↑
scripts/preprocessing_consumer/boundary.py    ← 兼容转发层（不再持有规则）
```

| 检查项 | 结果 |
|---|---|
| 生产入口无 `sys.path` 修改 | ✅ 已删除 |
| 生产入口无 `scripts.*` 依赖 | ✅ 仅 `app.domains.source.identity_scope` |
| boundary 为纯转发 | ✅ `enforce_interface_scope is identity_scope.enforce_interface_scope` → True |
| 合法值集合 / 错误码 / 哈希顺序 | ✅ 未改（`{2,"2"}`、5 个 CODE_*、hash 先于 scope） |
| 无第二份规则副本 | ✅ 常量与函数均 import 自生产模块 |
| unit-type 归一化保留 | ✅ `NormalizedUnitType` / `normalize_unit_type` 完整（转发重写时曾误删，已从 git 恢复） |

**测试**：`test_preprocessing_import_negative.py` **19 passed**（含 Interface Scope 7 项）。

---

## D. 测试数据库隔离

### 架构

```
conftest.py  (强制，不用 setdefault)
  DATABASE_URL = .../aitutors_test     ← 独立库
  + _assert_not_shared_db()            ← 指向 aitutors 即 RuntimeError
  + migrated_db 在 aitutors_test 上跑 alembic
  + session fixture 亦断言
```

`app.db.session.async_session_maker` 随 `settings.database_url` 建 engine；env 覆盖 `.env`，故 API/服务层自建 session、`test_b1_cross_transaction_idempotency` 的 `async_session_maker` **全部指向 aitutors_test**。

### 验证

| 项 | 结果 |
|---|---|
| `current_database()` | `aitutors_test` ✅ |
| 测试两轮 | 45 passed × 2 ✅ |
| 共享库前后 documents | 13→13，**id 集合相同** ✅ |
| 共享库前后 document_source_versions | 1→1，id 相同 ✅ |
| 共享库前后 questions / candidates / instances | 0→0 ✅ |
| 共享库前后 tasks | 16→16，id 集合相同 ✅ |
| 测试夹具落点 | `aitutors_test`：documents=5、sv=1、tasks=6 ✅ |

**结论**：测试执行路径实际使用隔离库，夹具数据**未**提交到共享业务库。非「断言免疫」。

快照证据：`_dsh_review/db_snap_before.json` / `db_snap_after.json`。

---

## E. artifact_kind 影响矩阵（本轮未改 Seal）

| 维度 | 内容 | 归类 |
|---|---|---|
| Frozen Spec 10 §4.2 允许值 | `original_binary / raw_l1 / canonical_l1`（闭集） | OBSERVED |
| Frozen Spec 10 §4.2 role 枚举 | `native / ocr_ppsv3 / ocr_ppsvl / docx / canonical`（**无 `preprocessing`**） | OBSERVED |
| `models._ARTIFACT_KINDS` | 同 Spec 闭集 | OBSERVED |
| `models._ROLE_PROVIDER_PAIRS` | 含 `preprocessing`→`{preprocessing}`（超出 Spec 枚举） | OBSERVED |
| `seal.py` 写入点 | `_ARTIFACT_KIND = "raw_l1"` 硬编码，全部 seal 路径 | OBSERVED |
| `test_identity_phase_a` | 断言 `preprocessing/preprocessing/canonical_l1` 合法可持久化 | OBSERVED |
| `runner_b2.py` | `artifact_kind="canonical_l1"` | OBSERVED（实验约定） |
| 下游消费者 | integrity_hash provenance 含 artifact_kind；无按值分支 | INFERRED |
| 既有 native SV 影响 | 若按 role 分支，native/ocr_*/docx 仍 `raw_l1`，**零影响** | INFERRED |

### 六 role 建议值

| role | 当前（经 Seal） | 建议 | 受影响消费者 | 回归 |
|---|---|---|---|---|
| `native` | `raw_l1` | `raw_l1`（不变） | 无 | seal_dbflow / identity |
| `ocr_ppsv3` | `raw_l1` | `raw_l1`（不变） | 无 | — |
| `ocr_ppsvl` | `raw_l1` | `raw_l1`（不变） | 无 | — |
| `docx` | `raw_l1` | `raw_l1` 或 `original_binary`（UNRESOLVED） | 无 | — |
| `preprocessing` | `raw_l1` | **`canonical_l1`** | integrity provenance | identity_phase_a |
| `canonical` | （非 Seal 路径） | `canonical_l1`（已有约定） | 无 | — |

### 最小变更建议（未实施）

`seal.py`：`_ARTIFACT_KIND` 由常量改为按 role 选择——`preprocessing` → `canonical_l1`，其余 → `raw_l1`。  
对既有 native Source Version：无（仍 `raw_l1`）。

**UNRESOLVED**：docx 是否 `original_binary`；Spec role 枚举是否补 `preprocessing`。

---

## F. 执行命令与结果

| 命令 | 退出码 | 结果 |
|---|---|---|
| `pytest tests/test_preprocessing_import_negative.py` | 0 | 19 passed |
| `pytest tests/test_seal_dbflow.py test_preprocessing_identity_split.py test_document_import_e2e.py test_preprocessing_import_negative.py test_load_package_source_selection.py` | 0 | **45 passed** × 2 |
| `db_snap.py before/after` + `_cmp_snap.py` | 0 | 共享库 id/count 全一致 |
| `current_database()` 探针 | 0 | `aitutors_test` |

无失败。

---

## G. 变更文件与提交

| 文件 | 变更 |
|---|---|
| `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` | +DA-38 Errata |
| `backend/app/domains/source/identity_scope.py` | 新建：唯一身份规则权威 |
| `backend/app/domains/source/preprocessing_import.py` | 去 sys.path / scripts 依赖 |
| `backend/scripts/preprocessing_consumer/boundary.py` | 身份段改为转发 |
| `backend/tests/conftest.py` | 强制 `aitutors_test` + 隔离断言 |

**Commit**：`7abff7fb7eb8b63b80165e78925bc889c75e80b7`  
未提交他人文件：`backend/scripts/_p14b_*.py` 等。

---

## H. 剩余阻塞与停止点

1. **`role=preprocessing` 未入 Frozen Spec 10 枚举** → Owner 是否补登。
2. **artifact_kind 统一**：是否批准 Seal 按 role 写 `canonical_l1`（本任务未改）。
3. **docx → `original_binary`?** UNRESOLVED。
4. **Producer 自包含打包**未实施（需 Owner 授权）。
5. **真实 Papers 包正式 E2E** 未运行（本任务禁止）。
6. **Phase B** 未通过，不宣称。

**停止**：等待 Owner 审阅 Errata 与 artifact_kind 结论。
