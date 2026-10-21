# Round 2 · B1 实施纪要（2026-10-09）

## 裁定落地

| 矛盾 | 裁定 | 动作 |
|---|---|---|
| 1 库状态 | 基线作废，按 fresh_test；禁止伪造 1213 对照 | `_dsh_review/db_reset_forensic.py` + `db_reset_timeline.md` |
| 2 合成僵尸 | 禁止按真实僵尸处置 | 取证确认：16 task / 6.69s / succeeded 无 LLM |
| 3 旧任务书 | SUPERSEDED | `MIMO-TASK-PHASE1-MINIMAL-E2E-01.md` 顶部已打戳 |

执行范围指令：`E2E_ACCEPTANCE/ROUND2-OWNER-SCOPE-DIRECTIVE.md`

## 取证事实（矛盾 1/2）

- PG 启动 `2026-10-09 14:30:23 UTC`；取证 `15:01 UTC`
- 业务九表全 0；`DATABASE_MODE=fresh_test`
- `llm_call_audit` 190 行（10-04 → 10-09 12:06），ann 阶段 93 failed / 77 completed
- 16 个 `document_ingest` 全在 `12:07:15–12:07:22 UTC`（6.69s），`created_by=NULL`，3 个 succeeded 却 `llm_invocations=0` → **合成数据**

## B1 正式入口（option b 最小实现）

### 新增

| 文件 | 职责 |
|---|---|
| `app/ai/ocr/preprocessing_provider.py` | 已验收 MD → OCRResult；记录 `source_content_sha256`；空 MD 直接拒绝 |
| `app/domains/source/preprocessing_import.py` | 正式包导入：身份校验 + Seal(role=preprocessing) + 入队 |
| `tests/test_preprocessing_import_negative.py` | 负向 12 项 |
| `tests/test_preprocessing_identity_split.py` | 身份切分正向 3 项 |

### 修改

| 文件 | 变更 |
|---|---|
| `app/domains/task/executor.py` | `_seal_stage`：`source_mode=preprocessing` 时强制走预处理提取器；缺 MD / hash 不匹配 → 明确失败，**不**调用 NativeTextProvider |
| `app/api/routers/documents.py` | `POST /documents/import-preprocessing`（original + source_md + manifest） |
| `app/api/schemas.py` | `PreprocessingImportResponse` |

### 身份契约（已测）

```
documents.original_sha256       = SHA256(PDF/DOCX 原始字节)     ✅ 只写原件
source_meta.source_content_sha256 = SHA256(Markdown 原始字节)   ✅ 独立字段
两者不得相同、不得互写                                      ✅ 断言覆盖
```

## 测试结果

```
test_preprocessing_import_negative.py   12 passed
test_preprocessing_identity_split.py     3 passed
test_document_import_e2e.py
test_task_executor.py
test_identity_phase_a.py                59 passed
```

## 仍待（Phase B 端到端）

- [ ] 真实 Papers 包走 `POST /documents/import-preprocessing`
- [ ] Annotation → Gate → DB → 前端
- [ ] 负向集成（非单元）：manifest 缺失 / hash 不匹配 / md 不可读 时 API 明确 400 且零 native 调用
- [ ] 全 64 hex 哈希证据包

**禁止**：放宽原 PDF/DOCX 白名单当「已接入」；用 Phase 1 Runner 成绩顶替；静默回退。
