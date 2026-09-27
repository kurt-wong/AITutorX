# PRIMARY-PATH-IDENTITY-CLOSURE-SUMMARY-01

```text
Document Type : Closure Summary（治理收口摘要；实现方入口文档）
supersedes    : —
superseded_by : —
readers       : MIMO CODE（实现方入口）；Owner；Implementation Authorization 作者
Status        : OPEN
Decision State: READY FOR FINAL APPROVAL（Blocking 全部 RESOLVED）
Blocking      : NONE
Revision      : rev.2 — Blocking-2 实测 RESOLVED；F-1 路径裁决记录
Date          : 2026-09-27
Authority     : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md（唯一权威源）
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

> **F-1 路径裁决（`[OWNER DECISION]`，2026-09-27）**
>
> CLOSURE-SUMMARY 属**结论载体**（Decision Summary / Implementation Entry），置于 `40_DECISIONS`。
> 其内验收状态属于**裁决元数据**，不属于独立 audit report。
> ⇒ 保持 `Docs/40_DECISIONS/PRIMARY-PATH-IDENTITY-CLOSURE-SUMMARY-01.md`，**不移动**。

**本文件用途**：把 Primary Path Identity / Provenance 的**最终裁决、剩余阻塞、实现前置条件**
收敛到一页，供实现方**直接引用**，无需重新解释。

**权威顺序**（冲突时以此为准）：

```text
1. OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md      ← 唯一 Owner Decision Authority
2. FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md           ← Spec 变更（**未生效**，待批准）
3. 本文件                                           ← 摘要（不含新裁决）
4. IDENTITY-PROVENANCE-REVISION-02.md              ← 撤回记录 / 审计轨迹
```

---

## 1. Final Decisions

### D-1 Primary Path provenance identity

```text
role     = preprocessing
provider = preprocessing
```

`Decision Type: Frozen Spec Amendment` / `Impact: LEVEL 2` ⇒ **走 errata，不强行映射到错误身份**。

```text
✗ 已撤回：role 复用 native / ocr_ppsv3
✗ 已撤回：「复用 ocr_ppsv3 ⟺ ppsv3 是唯一诚实映射」
```

### D-2 `original_sha256` identity domain — **2-B Scoped Byte-Domain Identity**

```text
original_sha256 represents raw artifact byte identity
within its defined artifact boundary.

It does not represent universal semantic content identity.
```

```text
same content means same byte sequence inside the same byte domain.
Cross-domain artifacts (PDF, Markdown, canonical L1)
do not require identical original_sha256.
```

**替换对照**：

| 旧表述（rev.1） | 新表述（rev.2，**按此实现**） |
|---|---|
| `same content = same identity` | **`same artifact bytes = same artifact identity`** |

**落地算法（唯一确定，无歧义）**：

```text
original_sha256 = SHA256(该 pipeline 实际接收到的 artifact 原始字节)
```

```text
Native         : sha256(pdf bytes)
Preprocessing  : sha256(md bytes)
Future Producer: sha256(其 artifact bytes)
```

```text
✗ 已拒绝：2-A canonicalization（不定义跨域规范表示，不要求跨域 hash 相等）
```

### D-3 Identity Model — 三种身份**分离**

```text
Artifact Identity  ≠  Semantic Identity  ≠  Execution Identity
```

| 身份 | 承载 | 域 |
|---|---|---|
| Artifact Identity | `documents.original_sha256` | 域内 raw artifact bytes |
| Semantic Identity | Question / IR layer | 由该层单独处理 |
| Execution Identity | `logical_execution_hash` | stage + contract_domain + input_domain |

**禁止**跨域要求 `original_sha256` 相等；**禁止**跨域强制 dedup。

### D-4 Producer metadata storage

producer metadata **不进入** `source_meta` JSONB、**不进入** `document_source_versions` 作为长期扩展字段。

**建立独立表**（`producer_metadata` 或 `source_producer_metadata`，待 schema review）：

```text
id / source_version_id / producer_name / producer_version
/ artifact_hash / manifest_hash / created_at / metadata_json
```

```text
Producer provenance ≠ Source identity
```

### D-5 Artifact Compatibility Rule

| role | provider | artifact_kind |
|---|---|---|
| `native` | `native` | `original_binary` / `raw_l1` |
| **`preprocessing`** | **`preprocessing`** | **`canonical_l1`** |
| `ocr_ppsv3` | `ppsv3` | `raw_l1` |
| `ocr_ppsvl` | `paddleocr-vl` | `raw_l1` |
| `docx` | `docx` | `original_binary` / `raw_l1` |
| `canonical` | **none** | `canonical_l1` |

```text
canonical_l1 describes artifact maturity, not producer identity.
✗ 禁止推断：「canonical_l1 requires canonical role」
✗ 禁止以 markdown 作为 artifact_kind
```

### D-6 Seal 定位（误解已彻底删除）

```text
✗ 已撤回：Primary Path must pass Seal ingestion boundary
✓ 保留  ：Primary Path requires valid identity creation,
          not mandatory Seal pipeline.
```

三者独立：`Producer Identity` + `V3 Identity Layer` + `Semantic Consumer`。

### D-7 Owner Decision 原文入仓

```text
Docs/40_DECISIONS/ = Owner Decision Authority
任何 “Owner said / approved / direction” 必须引用 OWNER-DECISION-*.md。
禁止只存在聊天记录。
```

---

## 2. Remaining Blockers

| # | Blocker | 状态 |
|---|---|---|
| Blocking-1 | `original_sha256` identity domain 未定义 | ✅ **RESOLVED**（2-B） |
| Blocking-3 | `artifact_kind=canonical_l1` × `preprocessing` role 合法性 | ✅ **RESOLVED**（D-5） |
| **Blocking-2** | 已 sealed / 已写入数据的处置 | ✅ **RESOLVED**（2026-09-27T09:13:28Z 实测） |

### Blocking-2 实测结果（`[FACT]`）

```text
query      : SELECT count(*) FROM documents
             WHERE original_object_key LIKE 'preprocessing/%';
result     : 0
             （交叉核对）
             Primary Path source_versions = 0
             全库 documents               = 0
             全库 document_source_versions= 0
             provider 分布                = []（空集）
timestamp  : 2026-09-27T09:13:28Z
environment: localhost:5432/aitutors（APP_ENV=test）
```

**判定**：数据库**完全为空**（全部业务表零行）⇒ **不存在 Primary Path persistence data**，
**不需要数据修复 / migration 数据处置**。

```text
Blocking-2: RESOLVED
Reason: No Primary Path persistence data exists.
        No migration data remediation required.
```

> `[FACT]` 本次为**只读查询**：未执行 DDL / DML，未修改 schema，未写入任何行。
> 可复现 SQL 原文见 `FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md` §5 Blocking-2。

---

## 3. Implementation Prerequisites

> **实现方在下列条件全部满足前不得开工。**

```text
P-1  Errata FINAL APPROVED（Blocking-2 已 RESOLVED，仅待 Owner 签署）
P-2  Implementation Authorization 另立签发
P-3  接受 §4 的 Derived Hash Impact 为强制同批范围
```

### 3.1 实现范围（MIMO CODE）

> **本表不编号。** 能力名称即授权边界的标识 —— 编号属执行计划，
> **不得**成为授权边界（同一能力在不同文档曾出现 `I-6` / `I-7` 两种编号，已消除）。

| 能力 | 内容 | 位置 |
|---|---|---|
| `role-provider enforcement` | Primary Path 写入 `role`/`provider` = `preprocessing` | `runner.py:90-91`；`runner_b2.py:338-339` |
| `artifact-kind compatibility enforcement` | `artifact_kind` 由 `"markdown"` 改为 `canonical_l1` | `runner.py:89`；`runner_b2.py:337` |
| `original_sha256 identity-domain correction` | `original_sha256` 改为 **接收字节** 的 SHA256（2-B） | `runner.py:74,78`；`runner_b2.py:322,326` |
| `identity byte-domain correction` | 复用已核对的 raw-bytes identity（现被丢弃） | `runner_b2.py:118-121` |
| `artifact-kind validation` | **新增闭集校验器**（当前不存在）并接入两条写入路径 | 现仅 `seal.py:39-44` 校验 role/provider |
| `seal role-provider enum extension` | `_SEAL_ROLE_PROVIDERS` 纳入 `preprocessing ⟺ preprocessing` | `seal.py:39-44` |
| `producer_metadata schema introduction` | 新建 producer metadata 表 + **写入后禁 UPDATE** 守卫 | 新表；参照 `source_repository.py:148-151` |
| `source repository predicate alignment` | `_version_by_le` 与 `ON CONFLICT` 目标索引**同步**修改 | `source_repository.py:110-113` vs `:128-138` |
| `model schema test alignment` | 更新 `tests/test_models_schema.py`（含 `assert len(seen) == 11`） | `tests/test_models_schema.py:39,103-107,124,126` |
| `api compatibility review` | `role` 是**排序键**且经 API 暴露 | `api/schemas.py:22-32`；`api/routers/documents.py:224-232`、`:129-133` |
| `identity invariant tests` | 见 §3.3 | — |

### 3.2 Derived Hash Impact（**强制同批，不得只改赋值**）

`[FACT]` `le_hash = f(original_sha256)`（`runner.py:86`；`seal.py:98-106`）
⇒ `original_sha256 identity-domain correction`（由 `sha256_hex(body_text)` 改为接收字节的 SHA256）
**必然改变** Primary Path 的 `le_hash`。必须同步重新验证：

```text
· le_hash
· source version identity
· replay behavior
· uniqueness assumptions
```

| 项 | 影响 | 依据 |
|---|---|---|
| `le_hash` | 输入域变化 ⇒ 无法幂等命中历史行 | `runner.py:86` |
| version identity | `UNIQUE(stage, le_hash)` 键值变化 | `models/source.py:52-57` |
| replay | 已 sealed 文档重跑 ⇒ 新建 version | `source_repository.py:148-151` |
| uniqueness | `documents.UNIQUE(original_sha256)` 语义随域变化 | `models/source.py:32-34` |
| `ON CONFLICT` 目标 | 约束与 re-read 谓词不同步 ⇒ Postgres **Binder error**（响亮失败） | `source_repository.py:110-113` / `:128-138` |

### 3.3 必须新增的测试（identity invariant）

```text
tests green  ≠  identity correctness proven
```

`[FACT]` 现有测试对 `_create_source_records` 多为 `patch` + `call_count` 断言，
**无任何测试断言** consumer 的 `role`/`provider`/`original_sha256`/`le_hash`。

最低要求：

```text
T-1  original_sha256 == SHA256(接收字节)，且 ≠ sha256_hex(body_text)
T-2  同文档同输入 ⇒ 幂等命中既有 version
T-3  role/provider/artifact_kind ∈ 闭集，非法值 fail-fast
T-4  producer metadata 写入后禁 UPDATE
T-5  跨域（PDF vs md）不要求 original_sha256 相等（2-B 不变量）
```

---

## 4. Acceptance Criteria 状态（诚实核对）

| # | 条件 | 状态 |
|---|---|---|
| 1 | 2-B Identity Domain 固化 | ✅ |
| 2 | `original_sha256` 定义无歧义 | ✅ |
| 3 | `canonical_l1` × `preprocessing` 合法 | ✅ |
| 4 | Seal boundary 误解彻底删除 | ✅ |
| 5 | Decision 状态准确 | ✅（见 §5） |
| 6 | Blocking-2 已实测确认（RESOLVED） | ✅ |
| 7 | 无代码修改 | ✅ |
| 8 | 无 migration | ✅ |
| 9 | **MIMO CODE 可根据文档直接实施，无需重新解释** | ⚠️ **NO — 见下** |

### 4.1 第 9 项为何不是 YES

**文档层面已无歧义**：identity domain、role/provider/artifact_kind、producer metadata 归属
均已固化，实现方**无需重新解释语义**。

**但实施在治理上被两处显式前置所阻断**（这是设计意图，不是文档缺陷）：

```text
P-1  Errata FINAL APPROVED  ← Blocking-2 已 RESOLVED，现已无事实前置
P-2  Implementation Authorization 另立签发
```

⇒ 准确表述为：

```text
MIMO CODE can implement from these documents WITHOUT semantic reinterpretation.
MIMO CODE must NOT start until P-1 and P-2 complete.
```

**另有一项实现层前置**（非语义歧义）：`producer_metadata schema introduction` = schema 变更 ⇒
**需要 migration**；本治理轮次与授权签发前均禁止 migration（须另立授权）。
⇒ 实施分阶段：**Phase A**（无 migration）可先做；`producer_metadata schema introduction`
须归 **Phase B**，待独立 migration 授权。

---

## 5. Decision 状态准确性说明（含一处词表冲突）

Owner 指令要求：禁止在仍有 Blocking 时使用 `CLOSED`，改用
`CLOSED WITH OPEN BLOCKING` 或 `APPROVED WITH CONDITIONS`。

**执行结果**：

```text
Status 字段        : 保持合法词表内取值（OPEN / CLOSED / DEFERRED / ARCHIVED）
Decision State 字段: OWNER-DECISION = APPROVED WITH CONDITIONS（Blocking 已全清）
                    本文件与 Errata   = READY FOR FINAL APPROVAL
Blocking 字段      : NONE（Blocking-2 实测 RESOLVED）
```

> 历史记录：Blocking-2 关闭**之前**，本文档的 `Blocking` 字段为
> `BLOCKED_PENDING_DB_CONFIRMATION`、`Status` 为 `OPEN`。
> 2026-09-27T09:13:28Z 实测确认数据库为空后，Blocking 清零，
> `OWNER-DECISION-…-01.md` 的 `Status` 转为 `CLOSED`（其 `Decision State` 仍为
> `APPROVED WITH CONDITIONS` —— 该组合表达「裁决已下 + 附约束条件」，二者不矛盾）。

**原因（必须记录）**：`AITUTORX-DOC-GOVERNANCE.md:211-216` 限定状态词表为
`OPEN / CLOSED / DEFERRED / ARCHIVED`，且 `:225-229` 禁止自创状态词。
`CLOSED WITH OPEN BLOCKING` 与 `APPROVED WITH CONDITIONS` **不在该词表内**。

⇒ 为**同时**满足「状态准确」与「不自创状态词」，本批次采用：

```text
Status = OPEN / CLOSED（合法词表内；随 Blocking 状态变化）
Decision State = APPROVED WITH CONDITIONS（作为独立字段，不占用 Status 词表）
```

三份文档（Owner Decision / Revision-02 / Errata）均已按此统一。

> `[OPEN]` 若 Owner 希望将 `APPROVED WITH CONDITIONS` 纳入正式词表，
> 须修改 `DOC-GOV` §8 —— 本批次**不自行**修改治理文档。

---

## 6. 下一动作

```text
Completed:

✅ Blocking-2 DB confirmation
   （2026-09-27T09:13:28Z 实测：数据库为空，无 Primary Path 数据）

Remaining:

1. Owner：Errata FINAL APPROVED
2. Owner：签发 Implementation Authorization（Phase A only）
```

> `MIMO CODE` 实施在下列条件全部满足前不得开始：
> `Errata FINAL APPROVED` **AND** `Implementation Authorization issued`。

---

## 7. Non-Actions（本批次确认未做）

```text
✅ 未修改 AITutors-v3 任何文件
✅ 未修改 Papers 任何文件
✅ 未创建或修改 migration
✅ 未修改数据库 schema
✅ 未执行 persistence test
✅ 未签发 Implementation Authorization
✅ 未修改 Frozen Spec / Frozen Contract 正文
✅ 未自行修改 DOC-GOV
```

---

*Recorded 2026-09-27. 本文件为治理收口摘要（实现方入口文档），不含新裁决；所有裁决引用 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md`。*
