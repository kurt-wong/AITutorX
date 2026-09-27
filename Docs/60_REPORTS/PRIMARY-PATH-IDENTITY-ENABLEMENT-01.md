# PRIMARY-PATH-IDENTITY-ENABLEMENT-01 — Implementation Note

**Task Level**: LEVEL 1
**Commit**: `b2266d2`（Papers）
**Date**: 2026-09-27
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

---

## Implemented

### 1. Identity output（`scripts/reslice_pipeline.py`）

- `write_outputs()` 计算 `source_content_sha256 = SHA256(source md raw bytes)` 并写入 manifest
- `process_file()` 对新产物设置 `identity_version = 2`（已有值不覆盖）
- `write_outputs()` 保留从 `man` 拷贝 `identity_version`/`sections`/`source_content_sha256` 的既有逻辑

### 2. `_redact()`（`scripts/reslice_pipeline.py`）

- 新增 `_redact()` 函数：剥离 `Bearer` token / `sk-` key / `api_key` 值
- `call_llm()` 错误消息经 `_redact()` 处理后才抛出

### 3. HTTP 4xx fail-fast（`scripts/reslice_pipeline.py`）

- 非 429 的 4xx 错误（400/401/403/404 等）→ 立即抛 `RuntimeError`，不再重试
- 429/5xx 仍走指数退避重试（原行为保留）

### 4. Test fixes（`tests/`）

- `test_no_config_import.py`：`test_call_llm_fails_loudly_without_config` 断言从 `FileNotFoundError` 扩展为 `(FileNotFoundError, RuntimeError)`——代码现抛 `ProviderConfigError`（继承 `RuntimeError`）
- `test_no_config_import.py`：新增 `test_write_outputs_emits_identity`——验证 `source_content_sha256` 存在、与源字节 SHA256 一致、`identity_version = 2`
- `conftest.py`：`SYNTH_MAN` 显式标 `identity_version: 1`（合成测试数据为 v1 语义，不被 v2 严格检查干扰）

---

## Validated

| 检查 | 结果 |
|------|------|
| 全量测试 | **339 passed, 1 xfailed** |
| `test_write_outputs_emits_identity` | `source_content_sha256` 存在且与源字节一致 |
| `test_call_llm_fails_loudly_without_config` | 缺配置显式失败 |
| Consumer 侧字段兼容 | `manifest_reader.py:63-64` 已声明 `source_content_sha256`/`identity_version`；`boundary.py` `enforce_interface_scope` 可校验 |

### Consumer acceptance 事实

- producer manifest 现含 `source_content_sha256`（64 hex）+ `identity_version: 2`
- consumer `manifest_reader.py` 可读取这两字段
- `enforce_interface_scope(sha, version)` 判定条件：sha 64 hex + version == 2 → accepted
- **identity validation 不再因缺失 identity FAIL**

---

## Known Remaining Boundary

| 项 | 状态 | 说明 |
|----|------|------|
| **B2 — consumer persistence** | **NOT IMPLEMENTED**（LEVEL 2，不在本任务） | `runner.py:296,317` 仍然 `session.rollback()`；identity 可被验证但不持久化 |
| **B1 — import extension** | **NOT IMPLEMENTED** | `import_service.py:26` 仅允许 `.pdf`/`.docx`，preprocessing 产物 `.md`/`.manifest.json` 无法走正式 import |
| **B4 — downstream IR** | **NOT IMPLEMENTED** | 即使 identity 通过，下游 IR/admission 链未接入 |
| **Papers `_redact()`/4xx 加固 → 副本** | **待移植** | 副本 `D:\Project\Aitutors-preprocessing` 有 `_redact()`/4xx 加固但 Papers 原先缺；本轮已补进 Papers，两树分叉消除 |
| **Persistence Boundary Decision** | **待 Owner 决定** | Option A/B/C（consumer 入口形态）|

### 三个事实边界（供后续 Owner Decision）

1. **identity 字段已实现**：producer 输出 `source_content_sha256` + `identity_version: 2`，与 Contract 定义一致。缺的不再是契约文本或 producer 实现。
2. **Papers = preprocessing 项目文件夹**（`github.com/kurt-wong/Aitutors-preprocessing.git`）。`D:\Project\Aitutors-preprocessing` 是非版本化副本，不是权威树。本轮改动已提交到 Papers。
3. **现有全部下游证据来自 Fallback Path**（Native Path）。本次 identity 输出为 Primary Path 打下基础，但尚无 Primary Path 端到端证据。

---

## Evidence

```
commit hash:  b2266d2 (Papers)
input:        scripts/reslice_pipeline.py, tests/test_no_config_import.py, tests/conftest.py
output:       identity output + 4xx fail-fast + _redact + test fixes
test result:  339 passed, 1 xfailed
```
