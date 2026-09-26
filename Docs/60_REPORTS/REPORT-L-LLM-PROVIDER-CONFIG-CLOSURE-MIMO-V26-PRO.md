# REPORT-L · Formal LLM Provider Configuration Closure + Preprocessing Provider Migration Preparation

**Date**: 2026-09-26
**Scope**: 三仓 LLM provider 配置事实调查 + `Aitutors-preprocessing` 正式 MIMO V2.6 PRO 切换 + 迁移配置基线建立
**Explicitly OUT of scope (未执行)**: V3 → AITutorX/backend 代码迁移、Frozen Spec 修改、preprocessing → V3 输入契约实现

> **措辞纪律**：本文中的 “configuration baseline established / smoke test passed”
> **不得**被读作 “full E2E integration complete” 或 “V3 production pipeline passed”。

---

## 1. Observed Facts

### 1.1 三仓物理位置与 git 边界

| 仓库 | 路径 | git HEAD | 备注 |
|---|---|---|---|
| AITutorX | `D:\Project\AITutor-X` | `949bfc895bec74987a942d6f98ed2c3124a76512` | 正常 git 仓库 |
| AITutors-v3 | `D:\Project\AITutors-v3` | `d2b9a26f1a1c0297b4536b273b8999a071433079` | 正常 git 仓库 |
| Aitutors-preprocessing | `D:\Project\Aitutors-preprocessing` | **N/A** | **`.git` ABSENT —— 不是 git 仓库**（仅有 `.gitattributes` / `.github/`） |

`git -C D:\Project\Aitutors-preprocessing rev-parse --show-toplevel` → `fatal: not a git repository`。
这直接决定 §9 的提交结论。

### 1.2 AITutorX/backend 实际内容

```
D:\Project\AITutor-X\backend
└── .gitkeep
```
非 `.gitkeep` 文件计数 = **0**。无 production Python source、无 config、无 provider implementation、无 migrated V3 code。

### 1.3 MIMO model ID 证据链（非猜测）

任务 §6 禁止猜测 model ID。本项目的权威值来自**实测**而非推断：

| 观察值 | 出处 | 性质 |
|---|---|---|
| `mimo-v2.6-pro` | `AITutor-X/Docs/60_REPORTS/E2E-VERIFICATION-EXECUTION-REPORT.md:684`：<br>`GET /v1/models` 返回 9 个模型，含 `mimo-v2.6-pro`（= 任务§三指定的 MIMO V2.6 PRO） | **权威目标**（provider 自身 model 列表实测返回 + 真实调用成功） |
| `mimo-v2.6-pro` | `AITutor-X/e2e_run/e2e_live_full_chain.py:43-45` 注释：实测 `api.xiaomimimo.com/v1/models` 返回 `mimo-v2.6-pro`；`.env` 的 `mimo-x-pro-preview` 被 API 拒绝 | 同上，交叉印证 |
| `mimo-x-pro-preview` | `AITutors-v3/backend/.env:9`、`preprocessing/scripts/reslice_pipeline.py`（原 DEFAULT_MODEL） | **LEGACY TEST MODEL CONFIG**（live API 返回 `400 Unsupported model`） |
| `mimo-v2.5` / `mimo-v2.5-pro` | `AITutors-v3/docs_archive/**`（2026-08 历史文档） | 历史归档，非当前配置 |

```text
Observed (legacy, rejected by API):
mimo-x-pro-preview

Observed (authoritative target, verified via GET /v1/models + real calls):
mimo-v2.6-pro

Unable to establish authoritative target:
NO  —— 目标已建立，来源为 provider model 列表实测 + 真实调用成功，非猜测。
```

### 1.4 Provider Configuration Matrix

| Repository | Provider | Model | API Key Var | Base URL | Current Status | Target |
|---|---|---|---|---|---|---|
| **AITutorX** | — (none) | — | — | — | `backend/` 仅 `.gitkeep`；migration NOT STARTED | 迁移后继承 V3 baseline（本任务不实施） |
| **AITutors-v3** (LLM Gateway, 生产路径) | `ollama`（`build_gateway()` 内 `HTTPLLMProvider(name="ollama", …)`） | `settings.ollama_model` = `""`（`.env` 未设） | 无（Ollama 本地无 key） | `settings.ollama_base_url` = `""`（`.env` 未设） | `LLM_GATEWAY_MODE=live`，但 Ollama base_url/model **均为空** | MIMO V2.6 PRO（**后续任务**） |
| **AITutors-v3** (Step 0.5 blind test 脚本，非 Gateway) | `mimo` | `mimo-x-pro-preview` | `MIMO_API_KEY`: **PRESENT** | `https://api.xiaomimimo.com/v1` | LEGACY TEST CONFIG；已知被 API 拒绝 | `mimo-v2.6-pro` |
| **Aitutors-preprocessing (BEFORE)** | `provider` 字段虽在文档契约中，但 `load_cfg()` 未使用 → 实质无 provider 抽象 | `mimo-x-pro-preview`（`DEFAULT_MODEL`） | `api_key`（`data/.llm_config` 内）：**ABSENT**（文件不在树中） | `https://api.xiaomimimo.com/v1` | LEGACY TEST MODEL CONFIG | `mimo-v2.6-pro` |
| **Aitutors-preprocessing (AFTER)** | `mimo`（显式 registry，`LLM_PROVIDER` 可选） | `mimo-v2.6-pro` | `MIMO_API_KEY`（legacy `.llm_config` 的 `api_key=` 兜底） | `https://api.xiaomimimo.com/v1` | **ACTIVE 正式配置** | 已达成 |

### 1.5 DeepSeek 现状（配置面）

| 位置 | 观察 |
|---|---|
| `Aitutors-preprocessing` 代码/配置（改动前） | **零** DeepSeek 引用（`grep -i deepseek` 在 `*.py/*.ini/*.yml/*.sh` 无命中） |
| `Aitutors-preprocessing` 改动后 | 新增 `llm_provider.PROVIDERS["deepseek"]` + `DEEPSEEK_*` 环境变量引用 + 4 项测试 |
| `AITutors-v3/backend/app/core/config.py:43-46` | `deepseek_api_key` / `deepseek_base_url="https://api.deepseek.com"` / `deepseek_model=""` / `deepseek_vl_model=""` —— **未触碰** |
| `AITutors-v3/backend/.env` | `DEEPSEEK_API_KEY`: **ABSENT**；`DEEPSEEK_BASE_URL`: **ABSENT**；`DEEPSEEK_MODEL`: **ABSENT**；`DEEPSEEK_VL_MODEL`: **ABSENT** |

### 1.6 preprocessing 原配置链（改动前实况）

```
provider   → 字段在 prd.md:390 文档契约中存在，但 load_cfg() 从未读取（实现缺口）
model ID   → data/.llm_config 的 model= ；缺失时 DEFAULT_MODEL = "mimo-x-pro-preview"
base URL   → data/.llm_config 的 base_url= （文档记 https://api.xiaomimimo.com/v1）
API key    → data/.llm_config 的 api_key= （文件在文件系统层面 gitignored: /data/.llm_config, *llm_config*）
             —— 该文件在当前树中 ABSENT
payload    → {"model","messages":[{"role":"user","content"}],"max_tokens","temperature"}
parser     → data["choices"][0]["message"]["content"]，finish_reason=="length" 抛错
error      → HTTPError 429/5xx 指数退避 30/60/120/240s；其余码同样重试（400 也重试 4 次）
```

关键发现：**`data/.llm_config` 在当前树中不存在**（`CFG_PATH` 注释称「2026-09-10 自 finetune 归档时移出」），
即 preprocessing 的 LLM 调用在本工作树上**原本不可用**。

### 1.7 范围外观察（未读取内容）

`D:\Project\Papers\data\.llm_config` 文件存在，但位于三仓**之外**，
被 host 的 credential-exploration 防护拦截读取。**内容未读、未输出、未使用**。
本报告不据此推断任何凭证状态。

---

## 2. Configuration Changes

### 2.1 新增 `Aitutors-preprocessing/scripts/llm_provider.py`

正式 provider registry 与配置链解析（唯一新增生产模块）：

| Provider | `api_key_env` | `base_url_env` | `model_env` | `default_base_url` | `default_model` |
|---|---|---|---|---|---|
| `mimo` | `MIMO_API_KEY` | `MIMO_BASE_URL` | `MIMO_MODEL` | `https://api.xiaomimimo.com/v1` | `mimo-v2.6-pro` |
| `deepseek` | `DEEPSEEK_API_KEY` | `DEEPSEEK_BASE_URL` | `DEEPSEEK_MODEL` | `https://api.deepseek.com` | `""`（**不猜测**） |

解析优先级：**环境变量 → legacy `data/.llm_config` → provider 默认值**；
密钥缺失 / model 缺失 / model 为 legacy ID / provider 未知 → `ProviderConfigError`（fail-closed）。
`deepseek` 的 `default_model` 刻意为空：项目内无 DeepSeek 权威 model ID，禁止猜测（任务 §6）。

### 2.2 `scripts/reslice_pipeline.py` 配置链改造

| 位置 | Before | After |
|---|---|---|
| `DEFAULT_MODEL` | `"mimo-x-pro-preview"` | `llm_provider.MIMO_V26_PRO_MODEL` = `mimo-v2.6-pro` |
| `CFG_PATH` | `ROOT / "data/.llm_config"` | `llm_provider.legacy_config_path(ROOT)`（仅 legacy 兜底） |
| `load_cfg()` | 内联读 `k=v` 文件，缺文件抛 `FileNotFoundError` | 委托 `llm_provider.resolve(ROOT)`，配置链任一环缺失显式失败 |
| `model_tag()` | `load_cfg().get("model", DEFAULT_MODEL)` | `llm_provider.default_model_tag(ROOT)` |
| `call_llm()` | `model` 来自文件；HTTP 400 也重试 4 次；异常文本可能含 key | `model` 来自解析后的 provider 配置；4xx(除 429) 立即失败并带非敏感响应体；`_redact()` 保证 key 不进异常文本 |
| 模块 docstring | 「LLM（mimo-x-pro-preview）」 | 「正式 MIMO V2.6 PRO = mimo-v2.6-pro，见 llm_provider」 |

### 2.3 历史锚点（**保留未改**，已加注「非活跃生产配置」）

- `scripts/pac_audit_recompute.py:237-243` —— I7 不变式校验**既有 corpus 当时实际使用**的 model；改动会破坏对 87 份历史 manifest 的复证。
- `scripts/pac_assemble_tracks.py:75` —— 重建 round1 历史 track 记录。
- `tests/samples/artifact/**`、`data/**` 中的 `mimo-x-pro-preview` —— 历史产物 fixture / 审计 json。

三处均已加注释标明「历史工件锚点，非活跃生产配置」。

---

## 3. MIMO Verification

```text
Current provider (preprocessing, before):  无 provider 抽象（provider 字段未被代码消费）
Current model    (preprocessing, before):  mimo-x-pro-preview
Current provider (preprocessing, after):   mimo
Current model    (preprocessing, after):   mimo-v2.6-pro
Target provider:                           mimo
Target model:                              mimo-v2.6-pro   (= MIMO V2.6 PRO)
API credential:                            PRESENT
Configuration valid:                       YES
```

**API Key 是否沿用旧配置 —— 任务 §9 裁定：Case A**

```text
MIMO_API_KEY: PRESENT
MIMO_BASE_URL: https://api.xiaomimimo.com/v1   （与旧配置一致）
```
旧 Key 变量仍然存在，且目标 MIMO provider 使用同一变量名 `MIMO_API_KEY`、同一 `base_url`，
且以该 credential + 新 model `mimo-v2.6-pro` 发起真实调用返回 **HTTP 200**。

> **Existing MIMO credential configuration can be retained.**
> 仅 model ID 需重映射（`mimo-x-pro-preview` → `mimo-v2.6-pro`）；credential/base_url/provider 均可沿用。
> 注意：该 credential 的权威存放位置是 `AITutors-v3/backend/.env`；
> preprocessing 侧 `data/.llm_config` 在本树中 **ABSENT**，故 preprocessing 需通过 `MIMO_API_KEY`
> 环境变量注入（或补一份 gitignored 的 `data/.llm_config`）。**本任务未创建任何新密钥。**

**Key 内容**：`MIMO_API_KEY` 仅报告 PRESENT（长度 51 字符）。**值从未写入本报告、任何 commit、任何产物或任何终端输出。**

---

## 4. DeepSeek Verification

```text
Provider:                        deepseek
Model:                           （项目内无权威值 → 不设默认，需显式 DEEPSEEK_MODEL）
Credential:                      ABSENT      （DEEPSEEK_API_KEY 在 AITutors-v3/backend/.env 中不存在）
Configuration preserved:         YES
```

```text
DeepSeek configuration:
PRESERVED
```

**原因**：
1. `AITutors-v3` 的 `deepseek_api_key` / `deepseek_base_url` / `deepseek_model` / `deepseek_vl_model`
   （`config.py:43-46`）**零改动** —— 本任务未修改 V3 任何文件（`git status` 跟踪文件零变更）。
2. `Aitutors-preprocessing` 改动前**没有任何 DeepSeek 配置可被破坏**（零引用）。
3. MIMO 切换未删除/覆盖任何 DeepSeek 通路；反而新增 `llm_provider.PROVIDERS["deepseek"]`
   显式声明 `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL` 三个变量的正确引用，
   并由 4 项测试固定（`test_deepseek_provider_config_remains_valid`、
   `test_deepseek_credential_variable_still_referenced`、`test_deepseek_model_is_not_guessed`、
   `test_deepseek_missing_model_fails_loudly`）。
4. 按任务 §13，本轮**未**发起任何 DeepSeek 真实调用（纯静态验证，零 API 消耗，不涉时间窗口）。

---

## 5. Preprocessing Verification

```text
Before:  mimo-x-pro-preview
After:   mimo-v2.6-pro
Provider: mimo
Real API smoke test: PASS
```

### 5.1 冒烟链路（任务 §12 六环全覆盖）

```text
Preprocessing (reslice_pipeline.process_file)
 → 正式 MIMO V2.6 PRO (mimo-v2.6-pro @ https://api.xiaomimimo.com/v1)
 → 真实 API request
 → 正常 response
 → preprocessing parser (extract_json → validate_manifest → write_outputs)
 → 生成预期 .md + manifest
```

### 5.2 冒烟实测证据（`.smoke_mimo_v26/smoke_evidence.json`）

| 校验项 | 实测 |
|---|---|
| HTTP status | **200** |
| provider | `mimo` |
| model（请求） | `mimo-v2.6-pro` |
| model（服务端回显） | **`mimo-v2.6-pro`** ← 服务端确认该 model ID 真实存在并被接受 |
| response 是否符合 parser | **YES** —— `extract_json` 成功，`pipeline_returncode = 0` |
| 是否产生预期 `.md` | **YES** —— `smoke_min.md` + `smoke_min.annotated.md` |
| manifest 是否正常 | **YES** —— 顶层 `source_file/model/annotation_meta/units`；`model=mimo-v2.6-pro`；`annotation_meta.prompt_version=reslice-pilot-v2.7`；`validation_issues` 为空 |
| units | 2（`Q1` standalone/single_choice + `U2` composite/short_answer）← 与合成输入精确对应 |
| 不输出 API Key | **PASS**（脚本内硬断言 `api_key not in evidence_blob`） |

注：证据 JSON 中 `finish_reason: length` 属**探针**自身的 `max_tokens=8`（用于取回执），
与流水线调用无关；流水线调用返回 rc=0 且产出完整 manifest。

### 5.3 Provider + Model + API contract 完整可运行组合

已确认为成套可用，非仅改 model 字符串：

| 环 | 状态 |
|---|---|
| provider | `mimo` 显式 registry 条目 |
| model ID | `mimo-v2.6-pro`，服务端回显确认 |
| base URL | `https://api.xiaomimimo.com/v1`（实测可达） |
| API key 环境变量 | `MIMO_API_KEY` PRESENT，实测鉴权通过 |
| request payload | OpenAI 兼容 `chat.completions`，`model` 取自解析配置（非硬编码） |
| response parser | `choices[0].message.content` + `finish_reason=="length"` 截断判定，实测通过 |
| error handling | 4xx(除 429) 立即失败带非敏感响应体；429/5xx 指数退避；`_redact()` 防 key 泄漏 |

---

## 6. AITutorX Migration Status

```text
Migration started?
NO
```

**证据**：
```
D:\Project\AITutor-X\backend
└── .gitkeep          ← 唯一文件；非 .gitkeep 文件计数 = 0
```
无 production Python source、无 config、无 provider implementation、无 migrated V3 code。
`D:\Project\AITutor-X\preprocessing` 与 `D:\Project\AITutor-X\tools` 同样仅 `.gitkeep`。

**本任务未开始 V3 → AITutorX/backend 迁移**（任务 §11 明令禁止）。

### 6.1 V3 当前 provider（仅记录，未修改）

```text
V3 LLM Gateway 生产路径:
  build_gateway() @ app/ai/gateway.py:101-120
  mode = settings.llm_gateway_mode   → .env: live
  live_provider = HTTPLLMProvider(name="ollama",
                                  base_url=settings.ollama_base_url,   → "" （.env 未设）
                                  model=settings.ollama_model)         → "" （.env 未设）
```

**迁移所需修改点（后续任务清单，本轮不实施）**：
1. `build_gateway()` 需支持 `mimo` provider（`HTTPLLMProvider(name="mimo", base_url=mimo_base_url, model=mimo_model)`）或 `live_providers` 多 provider 路由。
2. `.env` 需补 `OLLAMA_*` 或改用 `MIMO_*` 作为 gateway 实际取值源（当前 `MIMO_*` 仅供 `scripts/step0_blind_test.py` 使用，**未接入 gateway**）。
3. `MIMO_MODEL` 需由 `mimo-x-pro-preview` 更新为 `mimo-v2.6-pro`（当前值已被 live API 拒绝）。
4. `deepseek_*` provider 面保留，凭证需另行配置（当前 ABSENT）。

---

## 7. Preprocessing → V3 Contract Status

```text
FORMAL CONTRACT:
DOES NOT EXIST
```

**事实依据**：

| 侧 | 事实 |
|---|---|
| preprocessing 输出 | `.md`（源/切片/annotated）+ `*.manifest.json`（`source_file`/`model`/`annotation_meta`/`units`） |
| V3 import 接受格式 | `app/domains/source/import_service.py:26` `_ALLOWED_EXTENSIONS = {".pdf", ".docx"}` —— **仅 pdf/docx** |
| 正式生产输入契约 | **NOT IMPLEMENTED** |

`.md` 与 manifest 无法经 V3 正式 import 通道进入；`PREPROCESSING-V3-CONTRACT-v0.2` 是
**Producer/Consumer 语义与身份（SHA256）边界契约**，不是文件格式 import 契约。
手工复制 `.md` **不构成**集成，本报告不以此宣称已集成。

**后续正式解决方案候选（均未实施，待 Owner 另行授权）**：
```text
A. V3 正式支持 preprocessing .md + manifest 作为 source import 输入
B. preprocessing 产生 V3 可接受的正式输入格式（pdf/docx 或等价物）
C. 建立明确的中间 artifact / import contract（专用 adapter + 契约测试）
```

---

## 8. Tests

### 8.1 新增 `tests/test_llm_provider_config.py`（18 用例）

| 任务 §17 要求 | 对应用例 | 结果 |
|---|---|---|
| `provider == target MIMO provider` | `test_mimo_provider_registry_declares_formal_model`、`test_resolves_to_mimo_v26_pro_with_env_credential` | PASS |
| `model == target MIMO V2.6 PRO model ID` | `test_resolves_to_mimo_v26_pro_with_env_credential`、`test_reslice_default_model_is_formal_mimo` | PASS |
| `credential variable exists` | `test_mimo_provider_registry_declares_formal_model`、`test_mimo_credential_absent_fails_loudly` | PASS |
| DeepSeek `provider config remains valid` | `test_deepseek_provider_config_remains_valid`、`test_deepseek_model_is_not_guessed` | PASS |
| DeepSeek `credential variable remains correctly referenced` | `test_deepseek_credential_variable_still_referenced`、`test_deepseek_missing_model_fails_loudly` | PASS |
| legacy model 不再是正式默认 | `test_default_model_is_not_legacy_test_model`、`test_legacy_test_model_rejected_when_explicitly_configured`、`test_legacy_test_model_rejected_from_legacy_config_file`、`test_assert_no_legacy_model_hook` | PASS |
| 配置链完整性 / 密钥不外泄 | `test_legacy_config_file_is_read_for_model_and_key`、`test_env_var_takes_priority_over_legacy_config_file`、`test_api_key_never_leaks_into_error_message`、`test_unknown_provider_fails_loudly` | PASS |

### 8.2 更新 `tests/test_no_config_import.py`（H-01 回归）

- `test_call_llm_fails_loudly_without_config`：`except FileNotFoundError` → `except Exception`
  （配置链异常类型变为 `ProviderConfigError`），仍断言缺配置**显式失败不吞异常**。
- `test_write_outputs_offline_without_config`：默认元数据标签断言改为 `mimo-v2.6-pro`，
  并新增负断言 `mimo-x-pro-preview not in output`。

### 8.3 全量回归

```text
$ python -m pytest tests/ -q
338 passed, 18 skipped, 1 xfailed, 0 failed
```
确定性路径（渲染/校验/QC/fix 链）零破坏；`test_e2e_pipeline.py:37`
（`mf["model"] == rp.DEFAULT_MODEL`）随常量同步，无需改动。

---

## 9. Git Evidence

### 9.1 起始 HEAD（任务 §16 要求）

```text
AITutorX                949bfc895bec74987a942d6f98ed2c3124a76512
AITutors-v3             d2b9a26f1a1c0297b4536b273b8999a071433079
Aitutors-preprocessing  N/A  ——  .git ABSENT，不是 git 仓库
```

### 9.2 Frozen Spec 一致性（任务 §15）

```text
Frozen object: AITutors-v3 @ f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1
               Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md

sha256 (登记值) : 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528  (92197 bytes)
sha256 (本轮实测): 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528  (92197 bytes)

RESULT: 字节级一致 —— Frozen Spec 未修改
```

### 9.3 变更范围

| 仓库 | 跟踪文件变更 | 说明 |
|---|---|---|
| `AITutors-v3` | **0** | 任务 §10 明令不改 V3 provider 实现 —— 已遵守 |
| `AITutor-X` | **0** | 任务 §11 明令不启动 migration —— 已遵守；本报告为新增文档 |
| `Aitutors-preprocessing` | 见下 | 主要实现对象 |

`Aitutors-preprocessing` 实际改动文件：
```text
新增  scripts/llm_provider.py
新增  tests/test_llm_provider_config.py
修改  scripts/reslice_pipeline.py          (配置链 + call_llm 错误处理)
修改  scripts/pac_audit_recompute.py       (仅注释：标注历史锚点)
修改  scripts/pac_assemble_tracks.py       (仅注释：标注历史锚点)
修改  tests/test_no_config_import.py       (断言同步新默认 model)
新增  .smoke_mimo_v26/                     (一次性冒烟证据，非生产流水线)
```

### 9.4 提交可行性 —— **BLOCKED（需 Owner 决定）**

```text
Aitutors-preprocessing: 无法 commit
原因: 该目录无 .git（git rev-parse --show-toplevel → fatal: not a git repository）
      仅有 .gitattributes / .github/
影响: 上述 provider 配置改动目前仅存在于工作树文件系统，无版本历史保护
```

未 amend、未 force push、未覆盖历史、未修改无关文件。

---

## 10. Open Items / Next Authorized Task

### 10.1 阻塞项（需 Owner 裁定）

| # | 事项 | 影响 |
|---|---|---|
| **B-1** | `Aitutors-preprocessing` 无 `.git`，改动无法版本化/提交 | §16「Commit/push」无法对该仓执行。需 Owner 确认：是重新 `git init` + 首次提交，还是该目录本就应是某仓的工作树/子模块？ |
| **B-2** | preprocessing 的 `data/.llm_config` 在树中 ABSENT | 冒烟验证通过 `MIMO_API_KEY` 环境变量注入完成；长期需 Owner 决定密钥存放方式（env-only，或补 gitignored 配置文件） |
| **B-3** | `D:\Project\Papers\data\.llm_config` 被 credential 防护拦截、**内容未读** | 若该文件是 preprocessing 的真实历史配置，需 Owner 明示是否授权读取以完成 Case A/B/C/D 的最终裁定 |

### 10.2 观察项（不阻塞）

| # | 事项 |
|---|---|
| O-1 | `AITutors-v3` gateway live 模式的 `ollama_base_url` / `ollama_model` 均为空（`.env` 未设）—— provider 配置实际不完整 |
| O-2 | `AITutors-v3/backend/.env` 的 `MIMO_MODEL=mimo-x-pro-preview` 已被 live API 拒绝（`400 Unsupported model`），属**已知失效配置** |
| O-3 | MIMO V2.6 PRO 响应含 `completion_tokens_details.reasoning_tokens`（冒烟探针观测到 9）—— reasoning token 计费/截断策略需在后续正式接入时确认 |
| O-4 | preprocessing → V3 无正式文件格式 import 契约（§7） |

### 10.3 建议的下一授权任务（**均需 Owner 另行授权，本轮不执行**）

1. **V3 provider migration**（§6.1 修改点清单）：`build_gateway()` 接入 MIMO V2.6 PRO，
   `.env` 的 `MIMO_MODEL` 更新为 `mimo-v2.6-pro`，补齐 gateway 实际取值源。
2. **preprocessing → V3 输入契约**：从 §7 的 A/B/C 三候选中择一实施。
3. **preprocessing 版本控制收口**：解决 B-1。

---

## 附录 · 任务 §19 完成标准核对

```text
[x] AITutorX/backend migration status confirmed          → NO (仅 .gitkeep)
[x] Three-repository provider matrix completed            → §1.4
[x] MIMO credential status verified without exposing      → PRESENT (值未输出)
[x] DeepSeek credential status verified without exposing  → ABSENT (值未输出)
[x] Official MIMO V2.6 PRO model ID verified              → mimo-v2.6-pro (实测 /v1/models)
[x] preprocessing old model removed from active config    → DEFAULT_MODEL 已切换 + legacy fail-closed
[x] preprocessing provider configuration updated          → llm_provider.py + reslice_pipeline.py
[x] preprocessing MIMO smoke test executed                → PASS (HTTP 200)
[x] DeepSeek configuration preserved                      → PRESERVED
[x] V3 current provider documented but not modified       → §6.1, git 零变更
[x] preprocessing → V3 contract status established        → DOES NOT EXIST
[x] Frozen Spec unchanged                                 → sha256 逐字节一致
[x] Relevant tests added/updated                          → 18 新增 + 2 更新, 338 passed
[x] Git working trees checked                             → §9.3
[!] Commit/push completed only for authorized changes     → BLOCKED: preprocessing 无 .git (B-1)
```
