# OWNER-DECISION-PRIMARY-PATH-IDENTITY-01

```text
Document Type : Owner Decision Record（本仓 Owner Decision Authority）
supersedes    : —
superseded_by : —
readers       : 实现方（MIMO CODE / 任何 V3 / Papers 实现者）；DSH；Errata 与 Implementation Authorization 作者
Status        : CLOSED
Decision State: APPROVED WITH CONDITIONS（具有约束条件的裁决）
Blocking      : NONE（Blocking-1 / 2 / 3 均已 RESOLVED）
Revision      : rev.3 — Blocking-2 实测 RESOLVED（2026-09-27T09:13:28Z）
Date          : 2026-09-27
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

**Authority**: 本文件是 **Primary Path Identity & Provenance** 的唯一权威来源。
自本文件生效起：

```text
任何 “Owner said” / “Owner approved” / “Owner direction” 必须引用本文件（或后续 OWNER-DECISION-*.md）。
禁止以聊天记录作为唯一权威来源。
```

**Hard rule**：

```text
本文件下裁决 ≠ Frozen Spec 修订已执行
本文件下裁决 ≠ 实现授权
Frozen Spec 修订须另经 Owner 批准（见 FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md）
实现须另立 Implementation Authorization
```

---

## 0. 输入事实（不再争论）

### 0.1 Primary Path 架构

```text
Papers preprocessing pipeline
        │  producer artifacts
        ▼
AITutors-v3 consumer
        │
        ▼
Semantic processing
        │
        ▼
Candidate
```

`[OWNER DECISION]` Primary Path **不是** V3 OCR ingestion path。

### 0.2 已撤回的旧主张

```text
✗ “Primary Path 必须经过 SealService / Seal ingestion boundary”
```

`[OWNER DECISION]` **已撤回**。保留并取代为：

```text
Primary Path requires valid identity creation,
not mandatory Seal pipeline.
```

三者独立：

```text
Producer Identity  +  V3 Identity Layer  +  Semantic Consumer
```

### 0.3 确认的既有系统事实（经三份对抗性审查 + MIMO CODE 独立复核）

| # | 事实 | 证据 |
|---|---|---|
| F-1 | `le_hash` 是 `original_sha256` 的函数；`create_document` 以 `original_sha256` 幂等 | `runner.py:74,78,86`；`source_repository.py:41-62` |
| F-2 | 「两份内容相同的**不同**文档共享 SourceVersion」**在当前约束下不可实例化** | 同上；`models/source.py:32-34` |
| F-3 | `_version_by_le` 的 re-read **不做 document 过滤** | `source_repository.py:128-138` |
| F-4 | `source_meta` **无 sealed 不可变性** | `task/executor.py:258-270`（绕过 `source_repository.py:148-151`） |
| F-5 | `role` 是**活的选择器**（`ORDER BY role LIMIT 1`），且经 API 暴露 | `api/routers/documents.py:224-232`；`api/schemas.py:22-32` |
| F-6 | Producer 的 `source_content_sha256` = SHA256(source **md** 原始字节) | `Papers/scripts/reslice_pipeline.py:737-740` |
| F-7 | Native Path 接收 **PDF** 字节 | `app/domains/source/import_service.py:69-77` |

---

## Decision 1 — Primary Path provenance identity

`[OWNER DECISION]`

```text
role     = preprocessing
provider = preprocessing
```

**理由**：Primary Path 的 L1 artifact 由 **preprocessing pipeline** 产生，不属于
`native / ocr_ppsv3 / ocr_ppsvl / docx`。

**结论**：Frozen Spec 当前 `role`/`provider` enum **不覆盖真实架构**。

```text
Decision Type : Frozen Spec Amendment
Impact        : LEVEL 2
```

> **推进方式**：**errata 修改**，**不是**强行映射到错误身份。

### 1.1 本 Decision 推翻了本批次的哪一条前置建议（留痕）

`IDENTITY-PROVENANCE-REVISION-01.md` §5.2 曾把「复用 `ocr_ppsv3 ⟺ ppsv3`」列为**首选方向**。
该建议 **作废**：

1. `ocr_ppsv3` 字面断言「L1 来自 ppsv3 的 **OCR** 引擎」，而 Primary Path 的 artifact
   是结构恢复＋语义标注产物 —— **provenance 失真**；
2. `10_Data_Model.md:150-153` 明写「**独立引擎必须独立身份，防 identity 漂移**」，
   复用该配对**正是断言两者共享身份**；
3. 复用后 Primary Path 行与 cloud-OCR seal 行在 `role`/`provider` 上**不可区分**。

### 1.2 `provider` 取值口径

```text
provider = preprocessing        （即字符串 "preprocessing"，**不是** "papers"）
```

> 此前草案中曾出现 `provider = "papers"`。该值**不是**本 Decision 的裁决值。
> 如后续改判，须以新的 `OWNER-DECISION-*.md` 覆盖本节。

---

## Decision 2 — `original_sha256` identity domain

### 2.1 原文（rev.1，**其中的 universal 表述已被 Amendment 取代**）

`[OWNER DECISION]`（rev.1）原判定 `original_sha256` 为「系统统一内容身份 hash」，
原则为 `same content = same identity`。

> ⚠️ **该 universal 表述已被 §2.2 的 Amendment 取代。** 见 §2.3 的替换对照。

### 2.2 Decision 2 Amendment（`[OWNER DECISION]` — 固化 Blocking-1 裁决）

**裁决：采用 2-B — Scoped Byte-Domain Identity。拒绝 2-A canonicalization。**

正式文本：

```text
original_sha256 represents raw artifact byte identity
within its defined artifact boundary.

It does not represent universal semantic content identity.
```

补充：

```text
same content means same byte sequence
inside the same byte domain.

Cross-domain artifacts
(PDF, Markdown, canonical L1)
do not require identical original_sha256.
```

### 2.3 表述替换对照（**必须按此执行，避免歧义**）

| rev.1 表述 | rev.2 替换 |
|---|---|
| `same content = same identity` | **`same artifact bytes = same artifact identity`** |

⇒ 「system-wide content identity hash」的 **universal 含义作废**；
`original_sha256` 是**域内**的 raw artifact byte identity。

### 2.4 落地算法（由 Amendment 唯一确定，**无剩余歧义**）

```text
original_sha256 = SHA256(该 producer/consumer 实际接收到的 artifact 原始字节)
```

所有 pipeline 遵循**同一条规则**（hash 自己接收的原始字节）：

```text
Native        : 接收 PDF 字节      → sha256(pdf bytes)
Preprocessing : 接收 md 字节       → sha256(md bytes)
Future Producer: 接收其 artifact   → sha256(其 artifact bytes)
```

> **`[FACT]` 与现行实现的关系**：Native 路径**已符合**本规则（`seal.py:83`
> `hashlib.sha256(file_bytes)`）。**违反**本规则的是 Primary Path ——
> `runner.py:74` 使用 `sha256_hex(body_text)`（对 joined line text 的 canonical_json 取 hash），
> 既非接收字节、亦非同一 hash 族。该违反属实现 backlog（见 §6 F-03）。

### 2.5 Identity Model（`[OWNER DECISION]` — 一并固化）

**Artifact Identity**（域内字节身份）：

```text
PDF bytes            ── sha256(pdf)
Markdown bytes       ── sha256(md)
Canonical L1 bytes   ── sha256(canonical artifact)
```

它们：

```text
· 可以来源相同业务内容；
· 不共享 hash；
· 不强制 dedup。
```

**Semantic Identity**：

```text
is handled separately by Question / IR layer.
```

**Execution Identity**：

```text
由 logical_execution_hash 承载（stage + contract_domain + input_domain）。
```

⇒ 三者关系（F-02）：

```text
Artifact Identity  ≠  Semantic Identity  ≠  Execution Identity
```

**禁止**跨域要求 `original_sha256` 相等（PDF ↔ Markdown ↔ canonical L1 不要求相同）。

### 2.6 Derived Hash Impact（`[OWNER DECISION]` 登记的要求）

`[FACT]`（F-1）：

```text
le_hash = f(original_sha256)
```

⇒ **任何 `original_sha256` domain 修订，必须同步重新验证**：

```text
· le_hash
· source version identity
· replay behavior
· uniqueness assumptions
```

（详细影响面见 `FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md` §"Derived Hash Impact"。）

---

## Decision 3 — Producer metadata storage

`[OWNER DECISION]`

producer metadata **不进入**：

```text
✗ source_meta JSONB（作为长期扩展字段）
✗ document_source_versions（作为长期扩展字段）
```

**建立独立 metadata 表。**

命名（待 schema review）：`producer_metadata` 或 `source_producer_metadata`。

最少字段：

```text
id
source_version_id
producer_name
producer_version
artifact_hash
manifest_hash
created_at
metadata_json
```

**原则**：

```text
Producer provenance ≠ Source identity
必须分离。
```

### 3.1 独立技术依据（为何必须离开 `source_meta`）

`[FACT]`（F-4）`source_meta` **无 sealed 不可变性**：

```python
# app/domains/task/executor.py:258-270
# docstring: “quality report 落 source_meta（sealed version 可写 source_meta，status 字段不变）”
sv = await s.get(DocumentSourceVersion, version.id)
meta = dict(sv.source_meta or {}); meta["quality"] = report.to_dict()
sv.source_meta = meta
await s.commit()          # 直接 ORM 赋值，绕过 update_version 的 sealed 守卫
```

⇒ 把身份级 provenance 放进 `source_meta` ＝ 放进**唯一被证明可在 sealed 后被改写**的载体。

### 3.2 伴随要求（待裁项，不属本 Decision 裁决）

| # | 要求 | 状态 |
|---|---|---|
| R-1 | `producer_metadata` 行一经写入**禁 UPDATE**（须 repository 守卫 + 测试） | 实现轮 |
| R-2 | 是否**同时**给 `source_meta` 补 sealed 守卫 | `OPEN`（独立缺口，见 REVISION-02 R-4b） |
| R-3 | 新表 = **schema 变更** ⇒ 需要 migration | 属实现轮；**本轮禁止** |
| R-4 | `tests/test_models_schema.py` 的表/UNIQUE 断言须同批更新 | 不得以改断言绕过 |

---

## Decision 4 — Owner Decision 原文入仓

`[OWNER DECISION]`

正式建立：

```text
Docs/40_DECISIONS/  =  Owner Decision Authority
```

以后任何 `“Owner said” / “Owner approved” / “Owner direction”` **必须引用**
`OWNER-DECISION-xxx.md`。**禁止只存在聊天记录。**

### 4.1 立此 Decision 的直接动因

`[FACT]` 本批次对抗性审查中，审查方**无法在仓库内定位**所引用的 Owner 原文，
因而**合理怀疑其存在**，作者亦无法自证 —— 即「权威来源不在权威载体上」。
本文件为第一份落盘实例。

---

## 5. 本文件的效力范围（Explicit Non-Authorizations）

```text
✗ 授权修改 AITutors-v3 任何代码
✗ 授权修改 Papers 任何代码
✗ 授权创建或修改 migration
✗ 授权修改数据库 / schema
✗ 授权执行 persistence test
✗ 授权修改 Frozen Spec 正文（须另经 Errata 批准）
✗ 授权开始实现 / 签发 Implementation Authorization
```

---

## 6. Implementation Backlog（登记，非授权）

| # | 项 | 依据 |
|---|---|---|
| F-02 | Artifact / Semantic / Execution Identity 三者分离须在实现中体现 | §2.5 |
| F-03 | `runner.py` 的 identity construction 问题：`sha256_hex(body_text)` 不符合 raw byte identity 原则 | `runner.py:74`；`raw_bytes_identity.py:14,42` |
| F-04 | 消除「正确身份已算出却被丢弃」：复用 `runner_b2.py:120` 已核对的 raw-bytes identity | — |
| F-05 | 新建 producer metadata 表 + 禁 UPDATE 守卫 | Decision 3 |
| F-06 | `_version_by_le` 与 `ON CONFLICT` 目标索引**同步**修改 | `source_repository.py:110-113` vs `:128-138` |

---

## 7. Remaining Blockers

### Blocking-1 — `original_sha256` identity domain

```text
状态：RESOLVED（本文件 §2.2–§2.4）
裁决：2-B Scoped Byte-Domain Identity
```

### Blocking-2 — 已 sealed / 已写入数据的处置

```text
状态：RESOLVED（2026-09-27T09:13:28Z 实测确认）
```

实测结果：**Primary Path documents = 0**；**Primary Path source_versions = 0**；
全库 `documents` = 0、`document_source_versions` = 0（**数据库完全为空**）。

⇒ 不存在 Primary Path persistence data；不需要数据修复。（执行记录见
`FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md` §5 Blocking-2。）

仓库证据只能证明：

```text
no known committed execution evidence
```

**不能**证明：

```text
database definitely empty
```

⇒ 本项**保持 OPEN，不自行关闭**。（证据见 REVISION-02 R-5。）

### Blocking-3 — `artifact_kind` 与 role 的兼容规则

```text
状态：RESOLVED（见 FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md §"Artifact Compatibility Rule"）
裁决：role=preprocessing / provider=preprocessing / artifact_kind=canonical_l1 合法
```

---

## 8. 后续路径

```text
本文件（Decision 落盘，含 Decision 2 Amendment）
        ↓
FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md（提案 + Artifact Compatibility Rule）
        ↓
Blocking-2 DB confirmation          ✅ 已完成（2026-09-27T09:13:28Z，结果 = 0）
        ↓
Errata FINAL APPROVED   +   Implementation Authorization（另立）
        ↓
MIMO CODE 实现 + identity invariant tests
```

---

*Recorded 2026-09-27（rev.3）. 本文件为 Owner Decision Record。Decisions 1–4 及 Decision 2 Amendment 依 Owner 任务指令记录；Blocking-1/2/3 均已 RESOLVED。本文件不含已生效的 Spec 修订。*
