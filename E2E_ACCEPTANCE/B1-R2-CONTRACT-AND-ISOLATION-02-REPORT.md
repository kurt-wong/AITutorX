# TASK B1-R2-CONTRACT-AND-ISOLATION-02 · 最终报告

## A. 三仓基线与工作区

| 仓 | 分支 | HEAD | 工作区 |
|---|---|---|---|
| AITutors-v3 | `od01-r3-convergence` | `667fb32`（本任务） | 仅他人未跟踪 `backend/scripts/_p14b_*.py` |
| AITutor-X | `main` | `7bce066` | 大量未跟踪报告 / `MIMO-TASK-…` 有修改 |
| Papers | `main` | `d42cde6` | 未跟踪 `scripts/_p14b_patch_producer.py` 等 |

修复前 V3 HEAD：`545c76c`（B1-R2-FIX-01）。  
数据库计数以 DSH 收口快照为准，不作为永久基线。

---

## B. 自包含包：Producer/Consumer 最小改动方案（方案 a）

### 事实

- `E2E_ACCEPTANCE/04_V3_INPUT` 9/9 manifest 均为**绝对路径** `source_file`，目录内 md=0 pdf=0 → 不是包，是 manifest 暂存区。
- Producer 每 stem 产出 `<stem>.md` 与 `<stem>.annotated.md`。

### Consumer（V3 loader）——**零改动**

现有 `_resolve_source_markdown` 在方案 a 下已满足：

| 条件 | 行为 |
|---|---|
| manifest 声明包内相对 `.md` | `_safe_package_path` 接受相对名 ✅ |
| 声明优先，不误取 `.annotated.md` | 未声明时多候选 → 明确失败（安全失败）✅ |
| PDF 无 manifest 字段 | `_ALLOWED_ORIGINAL_EXTENSIONS` 兜底唯一一个，多于一个报错 ✅ |

### Producer / 打包侧——**需新增打包步骤**（未改代码，仅方案）

1. 每包目录自包含：`manifest.json` + 源 `.md` + 原始 PDF。
2. manifest `source_file` 改为**包内相对名**（如 `paper.md`，禁绝对路径）。
3. 命名约定显式化 PDF↔MD 来源关系（如同 stem：`paper.pdf` + `paper.md`），弥补「包内 PDF 只按唯一选取」的残留风险。
4. 不写 `*.annotated.md` 进正式包，或 manifest 必须显式声明源 md。

### DA-38 / Round 2 §2 冲突裁决（**Owner**）

| 方 | 要求 |
|---|---|
| 契约 DA-38 / B1-G4 | 把跨系统 sha（md raw bytes）写入 `documents.original_sha256` |
| Round 2 指令 §2 | `original_sha256` **仅**原始上传字节（PDF/DOCX） |

**裁定：Round 2 §2 为准。DA-38 需 Errata。**

理由：

1. `documents.original_sha256` 有 UNIQUE，语义是 BUG-V3-007「一个原始文件 = 一个 Document」。若写入 MD hash，同一 PDF 的不同 MD 版本会裂成多 Document，破坏父档唯一性。
2. 身份分层必须清晰：原件身份（PDF）≠ 源文本身份（MD）≠ Seal 版本身份。
3. 跨系统绑定意图由 **source version 层**满足：`DocumentSourceVersion.source_meta.source_content_sha256` + `Document.upload_meta.source_content_sha256`，血统经 `document_id` + `parent_version_id` 表达。
4. 契约状态 **NOT FROZEN**，冻结令未下，Errata 合法且必要。

**Errata 建议（待正式下达）**：

> DA-38 / B1-G4 改为：V3 将 `source_content_sha256` 绑定在 **source version 身份层**（`source_meta` / `input_identity`），`documents.original_sha256` 保持原始文档字节身份。禁止两层共用一列。

### OQ-12 说明

选 (a) 相对路径 = 关闭传输形态延期项 OQ-12″，与契约「传输维度暂缓、不在 v0.2 承诺」一致，**不构成违约**。

### manifest 无 PDF 字段

契约 §1.1 双哈希层设计使然（`source_content_sha256` 钚 md 面；PDF 身份由 V3 `original_sha256` 承载）。**非缺陷**。

---

## C. identity_version 校验

### 调用链（已接入）

```
PreprocessingImportService._verify_package_identity
  → hash 校验 source_content_sha256（独立，不跳过）
  → _verify_interface_scope(claimed_src, manifest)
       → scripts.preprocessing_consumer.boundary.enforce_interface_scope
            → normalize_interface_identity   # 唯一权威
```

### 合法值（契约 + boundary.py 实测）

| 值 | 结果 | 错误码 |
|---|---|---|
| `2`（int） | accepted | — |
| `"2"`（str） | accepted | — |
| `"v1"` | rejected | `OUT_OF_SCOPE_IDENTITY_VERSION` |
| 缺失 / null | rejected | `MISSING_IDENTITY_VERSION` |
| `3` / 其他标量 | rejected | `OUT_OF_SCOPE_IDENTITY_VERSION` |
| `["2"]` / list / dict | rejected | `MALFORMED_IDENTITY_VERSION` |

**不要求必须是整数 2**；`2` 与 `"2"` 同义。

### 为何原先未校验

新入口只做了 hash 比对，未接入 Interface Scope——属实现缺口，本轮已补。

### `"v1"` 测试夹具来源

`test_preprocessing_identity_split.py` 早期夹具误用 `"identity_version": "v1"` 作占位符，本轮已改为 `2`。

### 是否可能写入越界身份版本

修复前：**可能**（只校验 hash，不看 identity_version）。  
修复后：**否**——越界 / 缺失 / 畸形均在写库前 `PreprocessingImportError`。

### 测试（19 passed）

覆盖 int 2 / str "2" / "v1" / 缺失 / int 3 / list / hash 独立校验仍生效。

### 契约冲突

无。校验器输入（sha + identity_version）与正式入口兼容，无需放宽允许值。

---

## D. artifact_kind 语义矩阵

| 维度 | 证据 | 归类 |
|---|---|---|
| 允许闭集 | Spec 10 §4.2：`original_binary / raw_l1 / canonical_l1` | OBSERVED |
| role 绑定 | Spec **未**绑定 role ↔ artifact_kind | OBSERVED（缺口） |
| SealService | 硬编码 `_ARTIFACT_KIND = "raw_l1"`（全部 seal 路径） | OBSERVED |
| 正式入口经 Seal | 写入 `raw_l1` | OBSERVED |
| `test_identity_phase_a` | **断言** `preprocessing/preprocessing/canonical_l1` 合法且可持久化；GAP-2 锁 runner_b2 输出 `canonical_l1` | OBSERVED |
| runner_b2 | `artifact_kind="canonical_l1"` | OBSERVED（实验约定） |
| 下游消费 | integrity_hash provenance 含 artifact_kind；无按值分支逻辑 | INFERRED |
| `role=preprocessing` | Spec 10 role 列表含 `preprocessing`（`models._ROLE_PROVIDER_PAIRS` 亦有） | OBSERVED |

### 冲突

**Seal 路径写 `raw_l1`，测试套件期望 preprocessing → `canonical_l1`。**  
正式入口目前与 GAP-2 锁不一致。

### 裁决建议（**待 Owner**，本任务未改 Seal）

**建议统一为 `canonical_l1`**，依据：

1. `test_identity_phase_a` 已把 preprocessing/canonical_l1 视为合法并做持久化断言。
2. preprocessing 产物是「已验收第一层」，语义上非 OCR 原始层。
3. Owner 目标方向即 `canonical_l1`。

**最小变更**（若批准）：`seal.py` 将 `_ARTIFACT_KIND` 由常量改为按 `role` 选择——`preprocessing` → `canonical_l1`，其余 → `raw_l1`。  
对既有 `native/ocr_*/docx` 影响：无（仍 `raw_l1`）。  
**本任务未实施**（授权边界）。

---

## E. test_seal_dbflow 隔离修复

### 缺陷

三处全表计数断言 `count(*) == 1`，库中存在预先 document 时失败：

| 测试 | 修前 | 原因 |
|---|---|---|
| `test_b1_seal_idempotent_…` | `assert 6 == 1` | 全表 `documents` / `document_source_versions` |
| `test_cloud_path_…` | `assert 6 == 1` | 全表 `documents` |
| `test_b1_cross_transaction_…` | `assert 2 == 1` | 全表 `document_source_versions` |

### 修复

改为**只断言本测试创建的行**（按 `original_sha256` / `document_id` / `version.id` 过滤）：

```diff
- n_docs = select(func.count()).select_from(Document)
+ n_docs = select(func.count()).select_from(Document).where(Document.original_sha256 == sha)
```

未删任何既有数据，未改生产语义。

### 验证

| 项 | 结果 |
|---|---|
| 存在 5 条无关 document 时通过 | ✅（修前 3 failed → 修后 13 passed） |
| 不删除/覆盖既有数据 | ✅（断言只读；仅 `cross_transaction` 清理**本测试** sha 的行） |
| 连续两次一致 | ✅ 45 passed × 2 |
| `test_document_import_e2e` 回归 | ✅ |
| DB 状态 | 未 TRUNCATE；仅测试事务写入后 rollback 或本测试自清理 |

---

## F. 执行命令与结果

| 命令 | 退出码 | 结果 |
|---|---|---|
| `pytest tests/test_preprocessing_import_negative.py` | 0 | 19 passed |
| `pytest tests/test_seal_dbflow.py` | 0 | 13 passed |
| `pytest tests/test_seal_dbflow.py test_document_import_e2e.py test_preprocessing_import_negative.py test_preprocessing_identity_split.py test_load_package_source_selection.py` | 0 | **45 passed**（重复 2 次一致） |

修前 `test_seal_dbflow`：3 failed, 10 passed。

---

## G. 变更文件

| 文件 | 变更 |
|---|---|
| `app/domains/source/preprocessing_import.py` | `_verify_interface_scope` 调用 `enforce_interface_scope` |
| `tests/test_preprocessing_import_negative.py` | +7 Interface Scope 用例；夹具默认 `identity_version=2` |
| `tests/test_preprocessing_identity_split.py` | 夹具 `"v1"` → `2` |
| `tests/test_seal_dbflow.py` | 三处全表计数 → 本测试行计数 |

未改 Frozen Spec、Seal `artifact_kind`、Producer、其他业务逻辑。

---

## H. 提交状态

```
commit 667fb32
fix(tests+identity): Interface Scope validation and seal_dbflow isolation (B1-R2-CONTRACT-AND-ISOLATION-02)
```

未提交他人文件：`backend/scripts/_p14b_*.py`、AITutor-X / Papers 侧未跟踪物。

---

## 停止点（按授权）

- 未运行真实 Papers 包。
- 未宣称 Phase B 通过。
- **待 Owner**：① DA-38 Errata 正式下达 ② `artifact_kind` 统一为 `canonical_l1` 的 Seal 最小变更 ③ Producer 打包步骤授权。
