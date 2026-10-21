# TASK B1-R2-FIX-01 · 最终报告

## A. 当前基线

| 项 | 值 |
|---|---|
| 仓库 | `AITutors-v3` |
| 分支 | `od01-r3-convergence` |
| 修复前 HEAD | `512bba2` |
| 修复后 HEAD | `545c76ce3741766c31224122a9b9336c07062c9d` |
| 工作区 | 仅残留他人未跟踪脚本 `backend/scripts/_p14b_*.py`（未触碰、未提交） |

## B. 缺陷复现（修前）

探针：`_dsh_review/probe_load_package.py`

| 用例 | 修前行为 | 判定 |
|---|---|---|
| **A** 声明 `REAL.md` 缺失，存在 `aaa_other.md` | **RETURNED `# AAA_OTHER_CONTENT`** | 缺陷：静默替换 |
| **B** 未声明，`a.md` + `b.md` | **RETURNED `# A_CONTENT`**（排序任选） | 缺陷：模糊选取 |
| **C** 声明 `chosen.md` 存在 | RETURNED `# CHOSEN_CONTENT` | 正常 |
| **D** 声明缺失且无其他 md | RAISED `source markdown missing` | 正常 |

pytest 修前：A/B `DID NOT RAISE`，C/D/单文件/穿越（测试笔误后修）另记。

## C. 最小修复

**仅改** `backend/app/domains/source/preprocessing_import.py` 的源文件选择逻辑（新增 `_resolve_source_markdown` / `_safe_package_path`）。

路径选择规则：

1. manifest 声明 `source_file` / `source_markdown` → **唯一权威**。缺失 / 非文件 / 路径穿越 → 立即 `PreprocessingImportError`。**绝不**搜索其他 `.md` 替代。
2. 未声明 → 仅当 `*.md` 恰好 1 个时自动发现；0 个或 ≥2 个 → 明确失败并列出候选名。
3. 禁止绝对路径、`..` 逃逸、包目录外读取。
4. 未改身份哈希、`source_content_sha256` 定义、Annotation/Resolver/Gate 等逻辑。无 native fallback。

## D. 修后验证

探针修后：

```
A: RAISED [load] declared source markdown not found: REAL.md
B: RAISED [load] multiple candidate source markdown files, cannot choose uniquely: a.md, b.md
C: RETURNED '# CHOSEN_CONTENT\n'
D: RAISED [load] declared source markdown not found: REAL.md
```

pytest：

| 套件 | 命令 | 结果 |
|---|---|---|
| 源选择契约 | `pytest tests/test_load_package_source_selection.py` | **6 passed** |
| 负向身份 | `pytest tests/test_preprocessing_import_negative.py` | 12 passed |
| 身份切分 | `pytest tests/test_preprocessing_identity_split.py` | 3 passed |
| 导入/执行器/身份回归 | `test_document_import_e2e.py test_task_executor.py test_identity_phase_a.py` | 59 passed |
| 合计 | 同上一批 | **74 passed, 0 failed** |

**声明文件缺失不会被替换**：A/D 断言 `PreprocessingImportError` 且 reason 含声明文件名，不读取任何替代 `.md`。
**无 NativeTextProvider 回退**：`preprocessing_provider.py` / `preprocessing_import.py` 零 import；executor 预处理模式缺 MD 或 hash 不匹配直接 `RepositoryError`。

## E. 契约核验（只读，未改）

### E.1 identity_version

| 来源 | 事实 |
|---|---|
| 真实 Papers manifest | 87 处均为 `"identity_version": 2`（JSON **整数 2**） |
| `boundary.py` `_INTERFACE_IDENTITY_VERSIONS` | `{2, "2"}` — **int 2 与 str "2" 均接受** |
| `"v1"` / 其他值 | `OUT_OF_SCOPE_IDENTITY_VERSION` 显式拒绝 |

**结论**：不要求必须是整数 `2`；`2` 与 `"2"` 表达同一事实均合法。新入口目前**不校验** `identity_version`（只透传进 manifest_meta）。是否强制接入 `enforce_interface_scope` → **待 Owner 裁决**（属扩大生产改动，未做）。

### E.2 artifact_kind

| 写入方 | 值 | 依据 |
|---|---|---|
| 新正式入口（经 `SealService`） | `raw_l1` | `seal.py` 硬编码 `_ARTIFACT_KIND = "raw_l1"`（OCR/native 第一层） |
| 实验 `runner.py` / `runner_b2.py` | `canonical_l1` | 实验约定，无 Frozen Spec 条款支撑 |

Frozen Spec 10 §4.2 仅定义闭集 `original_binary / raw_l1 / canonical_l1`，**未**绑定 role。
**推荐**：preprocessing 产物语义上接近「已验收第一层」，与 `canonical_l1` 更一致；但 **契约未冻结，标注为待 Owner 裁决，不得擅自改 Spec 或把实验 Runner 约定升格为正式标准。**

### E.3 task_params

| 疑点 | 事实 |
|---|---|
| 是否被错误存成字符串 | **否**。列类型 `jsonb`；raw asyncpg 无 codec 时显示为 str，ORM 路径 `dict(task.task_params)` 正常取 dict。**非双重编码**（`double_encoded_string=False`）。 |
| 测试夹具 vs 生产序列化 | `TaskService.enqueue(task_params: dict)` → `Task(task_params=dict)` 生产路径为结构化对象。 |
| 当前 queued 任务来源 | 现库 5 个 task **全部来自本轮测试写入**（`created_by=test/admin`，15:29 UTC）；先前 16 个合成 task 已不在库中。 |
| 是否执行过 | 全部 `status=queued`，未 claim、未执行。 |
| `document_active_sources=0` | 表示尚无 document 选定 active source version。seal 只创建 source version，active 选择在后续管线；当前 1 个 SV（role=preprocessing, artifact_kind=raw_l1, sealed）未完成 active 绑定。 |

## F. 数据安全

| 项 | 状态 |
|---|---|
| 清库 / TRUNCATE / 重置 | **未执行** |
| 写入业务 DB | **有**——回归测试经 conftest 真库 session commit，留下 5 documents / 5 tasks / 1 source_version（测试夹具数据）。未删除、未修改既有业务行。 |
| 真实 Papers 包 E2E | **未运行**（按授权停止） |

## G. 提交状态

```
commit 545c76ce3741766c31224122a9b9336c07062c9d
fix(preprocessing): fail-closed source markdown selection (B1-R2-FIX-01)
```

已提交范围：`preprocessing_provider.py`、`preprocessing_import.py`、`documents.py`、`schemas.py`、`executor.py`、三份测试。
**未提交**：`backend/scripts/_p14b_*.py`（他人未跟踪改动，按授权隔离保留）。

## H. 后续阻塞（真实 Papers 正式 E2E 前）

1. **artifact_kind 未裁决**：正式入口写 `raw_l1`，实验 Runner 写 `canonical_l1`，Frozen Spec 未绑定 role → 需 Owner 裁定统一值。
2. **identity_version 未接入正式入口**：新入口不调用 `enforce_interface_scope`；是否强制校验 `2/"2"` 待裁决。
3. **active source 绑定**：seal 后 `document_active_sources` 仍为 0，后续 Gate/Admission 是否依赖 active 绑定需确认。
4. **真实包端到端**：Annotation → Gate → DB → 前端，以及负向集成（API 层 400 且零 native 调用）未做。
5. **测试污染业务库**：conftest 直连真库且部分用例 commit，正式验收前需隔离或标记测试数据。
