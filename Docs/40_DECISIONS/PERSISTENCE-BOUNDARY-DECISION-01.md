# PERSISTENCE-BOUNDARY-DECISION-01

**Task**: MIMO-TASK-PERSISTENCE-BOUNDARY-DECISION-01
**Type**: LEVEL 2 — Architecture Boundary Decision Preparation
**Date**: 2026-09-27
**Purpose**: Owner Decision Preparation（不是 Verification / Closure / Audit）
**Constraint**: 零代码修改。零 Spec 修改。零新增治理机制。
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

---

## Current State

### FACT — 已完成

| 能力 | 状态 | 证据 |
|------|------|------|
| Producer identity 输出 | DONE | Papers `b2266d2`: `write_outputs()` 输出 `source_content_sha256` + `identity_version: 2` |
| Consumer identity validation | DONE | `boundary.py` `enforce_interface_scope`: sha 64 hex + version == 2 → accepted |
| Consumer manifest 读取 | DONE | `manifest_reader.py:63-64`: `source_content_sha256: str \| None` + `identity_version: int \| str \| None` |

### FACT — NOT STARTED

| 能力 | 证据 |
|------|------|
| Persistence consumption | `runner.py:296,317`: `finally: await session.rollback()` — 事务内校验后回滚 |
| ResolvedRun persistence | 同上 |
| IR / Admission / Question materialization | 无代码入口 |

### FACT — Primary Path / Fallback Path（Frozen Spec 90 §H-C:682-692）

```
Native Path : Source → Resolver → ResolvedRun
Path B      : Source → preprocessing → Adapter → ResolvedRun
```

`ResolvedRun` **必须是唯一消费入口**。下游 IRBuilder / Compiler / Gate / Admission 对两条路径完全一致。

---

## Decision 1 — Identity Domain

### Facts

**FACT 1.1** — 三个不同 hash 并存：

| hash 名 | 输入对象 | 位置 | 证据 |
|---------|---------|------|------|
| `source_content_sha256` | **OCR md raw bytes** | preprocessing manifest | Contract §1.2: "SHA-256(original source bytes) = 源 OCR markdown 文件原始字节的 SHA-256" |
| `original_sha256`（V3 `documents`） | **body_text**（joined lines，非 raw bytes） | V3 `documents` 表 | `10_Data_Model.md:117`: "原始文件 SHA256"；但 `runner.py:74`: `file_sha = sha256_hex(body_text)` |
| OCR 清单 `source_sha256` | **PDF bytes** | Papers OCR 清单 | Contract §1.2: "OCR 清单的 `source_sha256` 钉的是 PDF 字节" |

**FACT 1.2** — Contract 已明确 `source_content_sha256` = md raw bytes hash：

> "源 OCR markdown 文件**原始字节**的 SHA-256。格式 = 64 字符小写 hex 字符串。"
> — Contract §1.2

**FACT 1.3** — V3 `original_sha256` 当前与 `source_content_sha256` **不等价**：

Contract §1.3 OBSERVED:

> "consumer 路径写入 `documents.original_sha256` 的值是 canonical_json 包裹 joined-text（`runner.py:71-73` `file_sha = sha256_hex(body_text)`），**不是** raw bytes sha——该绑定当前不成立。"

**FACT 1.4** — `source_content_sha256` 的 hash 输入是 md raw bytes；`original_sha256` 的 hash 输入是 `"\n".join(line.text for line in source_lines)`。两者即使对同一文件也不会产生相同值（raw bytes 可能含 BOM / 不同换行符 / 原始空白；`body_text` 是从 `SourceLine.text` 重组）。

**FACT 1.5** — OCR 清单 `source_sha256`（PDF bytes）与 `source_content_sha256`（md bytes）语义不同，Contract §1.2 明文："两者语义不同，**不可混用**"。

### Options

**Option A — 统一 identity（`original_sha256` == `source_content_sha256`）**

| 维度 | 内容 |
|------|------|
| 做法 | V3 `documents.original_sha256` 改存 md raw bytes SHA-256，与 `source_content_sha256` 同值 |
| Native Path 影响 | **ANALYSIS**: Native Path 输入是 PDF（非 md），其 `original_sha256` 语义为 PDF hash。统一后 Native Path 的 PDF identity 无处安放——需要新字段或新语义 |
| provenance 影响 | **ANALYSIS**: 需新增字段区分「原始上传文件 hash」与「md content hash」，否则 PDF→OCR→md 链的上游身份丢失 |
| 对齐 Contract | **ANALYSIS**: 与 §1.2 一致；但改变 V3 `documents` 语义（原定义为"原始文件 SHA256"） |

**Option B — 双 identity domain（`source_content_sha256` + `original_sha256` 并存）**

| 维度 | 内容 |
|------|------|
| 做法 | 两字段独立存储，各自记录不同 hash 输入 |
| dedup | **ANALYSIS**: `documents` 表 `UNIQUE(original_sha256)` 当前约束的是 body_text hash。若 Primary Path 与 Native Path 的 `original_sha256` 算法不同，同一源文件走两条路径会产生两个 Document——dedup 逻辑需区分 domain |
| replay | **ANALYSIS**: 回放时需知道该 Document 用的是哪个 identity domain，否则无法验证 |
| Document ownership | **ANALYSIS**: 同一内容（md）经 Native Path（PDF→OCR→md）和 Primary Path（直接 md）产生不同 `original_sha256` → 两个 Document 指向同一内容 |

**Option C — identity + lineage（source identity → derived artifact relationship）**

| 维度 | 内容 |
|------|------|
| 做法 | `source_content_sha256` 作为 source identity；`original_sha256` 作为 derived artifact hash；两者通过显式 lineage 关联（非 hash 相等） |
| 与 Contract 关系 | **ANALYSIS**: Contract §1.1 已有双层概念（Manifest = identity authority，IR = semantic carrier），Option C 延伸此模式 |
| 数据模型影响 | **ANALYSIS**: 需要显式 lineage 表或字段（如 `parent_identity_sha256`），不是 hash 相等关联 |

### Implications

- **ANALYSIS**: 无论选哪个选项，当前 `runner.py:74` 的 `file_sha = sha256_hex(body_text)` 与 Contract 的 `SHA256(raw bytes)` 语义不符，需修正。
- **ANALYSIS**: 三层 hash（PDF / md / body_text）同时存在，如果不对 domain 做显式区分，跨机器迁移或 dedup 时会出现同一内容被判定为不同 identity 的问题。

---

## Decision 2 — Bytes Transport Boundary

### Facts

**FACT 2.1** — `source_file` 是本机绝对路径：

Contract §2.3:

> "当前 `source_file` 为本机绝对路径、跨机不可解析"

**FACT 2.2** — Consumer 通过本地文件系统读取 source：

`runner.py:243-249`:
```python
source_path = Path(manifest.source_file)
if not source_path.exists():
    ...
source_lines = load_source_lines(source_path)
```

要求 `source_path.exists()` 为真 → 本地文件系统可达。

**FACT 2.3** — Contract 冻结了 bytes 能力，但**不冻结传输方式**：

Contract §0.1 ⑥:

> "V3 **必须能获得 raw bytes 并重算身份键验证**（fail-closed）；**不冻结传输方案**"

> "传输 HOW（共享 FS/对象存储/IR 内嵌/相对路径）= 暂缓"

**FACT 2.4** — 跨机器场景（preprocessing machine → V3 machine）当前不成立，因为 `Path(manifest.source_file).exists()` 在目标机器上返回 False。

### Options

| 方案 | 描述 | FACT 基础 | ANALYSIS |
|------|------|-----------|----------|
| A — 共享文件系统 | preprocessing 与 V3 挂载同一 NAS/共享目录 | 当前 `source_file` 路径可达性依赖本地 FS | **ANALYSIS**: 最低成本，但跨机器部署受限；路径仍为 locator 不可作 identity |
| B — artifact upload | preprocessing 产物通过 API 上传到 V3 | 无现有 upload 入口 | **ANALYSIS**: 需新增 upload API + 存储；改变现有只读消费模式 |
| C — object storage | 共享 S3/OSS bucket | 无现有 object storage 集成 | **ANALYSIS**: 解耦路径，但需引入存储依赖 |
| D — manifest 相对路径解析 | `source_file` 改为仓库相对路径，consumer 在已知 base 下解析 | Contract §1.3 提到此选项但未裁 | **ANALYSIS**: 仍在同一文件系统，但跨仓库可移植；与 `source_content_sha256` 互补（path → 找文件，sha → 证明身份） |

### Implications

- **ANALYSIS**: 无论选哪个方案，Contract 的能力要求（可获得 raw bytes + 重算验证 + fail-closed）是 binding 的，传输方式是实现选择。
- **ANALYSIS**: 当前 `runner.py:243-244` 的 `source_path.exists()` 硬依赖本地 FS。跨机器部署前需要决定传输机制。

---

## Decision 3 — Persistence Boundary

### Facts

**FACT 3.1** — Consumer 已承担 Adapter 角色：

`runner.py:64-119` `_create_source_records()`:
- 创建 `Document`（`src_repo.create_document`）
- 创建 `DocumentSourceVersion`（`src_repo.create_source_version`，sealed）
- 创建 `DocumentSourceLine[]`（`src_repo.append_line`）
- seal version（`src_repo.seal_version`）

`_track_a()`: manifest → `manifest_to_annotation_payload` → `GateService.run` → candidates

`_track_b()`: manifest → ResolvedSpan

**FACT 3.2** — 但一切被 rollback：

`runner.py:296`: `finally: await session.rollback()`（Track A）
`runner.py:317`: `finally: await session.rollback()`（Track B）

**FACT 3.3** — Frozen Spec 90 §H-C 要求 ResolvedRun 是唯一消费入口：

> "ResolvedRun **必须是唯一消费入口**。不得出现 Native 下游消费 ResolvedRun / Adapter 下游消费 annotation_payload 两个世界。"

**FACT 3.4** — 当前 consumer 的 record creation 已经过 GateService（Track A）产生 candidates。如果去掉 rollback，Track A 的输出即为 admission_candidates。

**FACT 3.5** — Native Path 的持久化入口是 worker/task pipeline（`POST /api/documents/import` + `python -m app.worker run`），已有 task/audit 机制。

### Options

**Option A — Consumer 成为 Primary Path ingestion adapter**

| 维度 | 内容 |
|------|------|
| 做法 | 去掉 `rollback()`，consumer 的 record creation 直接持久化 |
| rollback removal | **ANALYSIS**: 需处理部分失败场景（Track A 成功 Track B 失败）；当前 rollback 是全量回滚 |
| provenance | **ANALYSIS**: `upload_meta: {"source": "preprocessing_phase0"}` + `role: "native"` + `provider: "native"`（`runner.py:81,93-94`）——需确认这是否正确表达 Primary Path 来源 |
| dedup | **ANALYSIS**: `UNIQUE(original_sha256)` 约束下，重复 ingests 会冲突——需决定 dedup 策略 |
| task/audit | **ANALYSIS**: 当前 consumer 无 task/audit 记录（不同于 Native Path 的 worker pipeline） |

**Option B — Consumer 只负责 validation，另建 ingestion layer**

| 维度 | 内容 |
|------|------|
| 做法 | consumer 保持 validation-only；另建独立的 ingestion 模块 |
| 重复入口风险 | **ANALYSIS**: Frozen Spec 90 §H-C 要求 ResolvedRun 唯一消费入口。如果 Primary Path 有独立 ingestion + Native Path 有 worker pipeline，两套代码可能产生不一致的 record 格式 |
| 与 §H-C 关系 | **ANALYSIS**: 两个入口产出的都是 ResolvedRun，只要消费格式一致，§H-C 不禁止两个生产入口 |

**Option C — 复用 Native worker/task/audit pipeline**

| 维度 | 内容 |
|------|------|
| 做法 | consumer 产出标准化中间格式，喂入现有 worker pipeline 持久化 |
| 双轨维护风险 | **ANALYSIS**: 降低——同一套 task/audit/rollback 机制 |
| Adapter 角色 | **ANALYSIS**: consumer 保持 Adapter 职位（manifest → annotation payload），不直接写 DB |

### Implications

- **ANALYSIS**: 无论选哪个选项，`runner.py:78` 的 `original_sha256=file_sha`（body_text hash）需与 Decision 1 对齐。
- **ANALYSIS**: Option A 最少改动（去 rollback），但缺少 task/audit。Option C 复用现有机制但需要中间格式。Option B 的独立入口与 §H-C 的一致性要求有张力。
- **ANALYSIS**: `role: "native"` / `provider: "native"`（`runner.py:93-94`）的 provenance 表达可能需要修正——当前 primary Path 来源的 record 被标记为 `native`，不符合真实来源。

---

## Recommendation Inputs

**ANALYSIS**（不是 Recommendation）：

1. **Identity Domain** 的选择影响 `documents` 表的 `UNIQUE(original_sha256)` 语义——如果 Primary Path 和 Native Path 的 `original_sha256` 算法不同，同一内容会产生两个 Document。Option B/C 需额外 dedup 逻辑。

2. **Bytes Transport** 在当前单机环境下不阻塞（`source_file` 本地可达）。跨机器部署是 Transport 决策的触发点。Option D（相对路径）改动最小。

3. **Persistence Boundary** 的选择影响是否需要 task/audit。Option A 最少改动但缺 audit trail。Option C 复用 worker pipeline 但需设计中间格式。

4. **三个 Decision 有依赖关系**：Identity Domain（D1）决定 `original_sha256` 语义 → 影响 Persistence（D3）的 dedup 逻辑。Bytes Transport（D2）独立于 D1/D3。

---

## Required Owner Decisions

| # | 问题 | 候选 | 影响范围 |
|---|------|------|---------|
| D1 | Identity Domain：`original_sha256` 与 `source_content_sha256` 如何共存？ | A: 统一 / B: 双 domain / C: identity + lineage | `documents` 表语义、dedup、Native Path PDF identity |
| D2 | Bytes Transport：source bytes 如何跨机器到达 V3？ | A: 共享 FS / B: upload / C: object storage / D: 相对路径 | 跨机器部署可行性 |
| D3 | Persistence Boundary：consumer 是否直接持久化？ | A: consumer = adapter / B: validation-only + 独立 ingestion / C: 复用 worker pipeline | task/audit、rollback removal、provenance |
