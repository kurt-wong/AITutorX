# FROZEN-SPEC-ERRATA-PRIMARY-PATH-01

```text
Document Type : Frozen Spec Change Proposal（**已批准 / APPROVED**）
supersedes    : —
superseded_by : —
readers       : Owner（批准方）；MIMO CODE（实现方）；后续 V3_SPEC 维护者
Status        : FINAL APPROVED
Decision State: APPROVED
Blocking      : NONE（Blocking-2 于 2026-09-27T09:13:28Z 实测关闭）
Revision      : rev.3 — Blocking-2 实测 RESOLVED；rev.2 新增 §2.6 Artifact Compatibility Rule、§4.4 Derived Hash Impact
Date          : 2026-09-27
Authority     : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md（Decision 1 / Decision 2 Amendment / Decision 3）
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
Approval:
  Approved by: <kurt>
  Date: 2026-09-27
  Scope:
    Frozen Spec amendment proposal approved.
    Implementation requires separate authorization.
```

> ## ✅ 本文件已获 Owner 批准（2026-09-27）
>
> ```text
> ✓ 本文件（Frozen Spec 变更提案）已获批准 —— 见头部 Approval 块
> ✗ 本文件不修改 AITutors-v3/Docs/V3_SPEC/**（Frozen Spec 位于 V3 仓）
> ✗ 本文件不产生任何 migration
> ✗ 本文件不授权实现
> ✓ 本文件只描述「应当改什么、为什么、影响面」
> ✓ 【已批准】将本 errata 应用于 V3 仓 Spec 正文本须另立动作，与本文件批准状态无关
> ```
>
> 本文件曾以「提案，未生效」形态存在；Owner 于 2026-09-27 批准后，
> 该状态声明已被头部 `Status: FINAL APPROVED` / `Decision State: APPROVED` 取代。

**放置位置说明**：`DOC-GOV:56` 定义 `Docs/30_CONTRACTS/` 为「Contract references、boundary definitions」。
本提案属契约引用/边界定义，故置于此，**不新建目录**（避免触发「不新建目录体系」边界）。

---

## 1. 修订依据

| 依据 | 内容 |
|---|---|
| `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 1 | Primary Path 的 L1 artifact 由 preprocessing pipeline 产生 ⇒ 现行 enum **不覆盖真实架构** ⇒ 走 **errata**，不强行映射 |
| `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 2 | `original_sha256` = 系统统一内容身份 hash |
| `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 3 | producer provenance 入**独立表** |
| 对抗性审查（三份）+ MIMO CODE 独立复核 | 现行 enum 的复用方案已被证伪（见 `IDENTITY-PROVENANCE-REVISION-02.md` W-3） |

---

## 2. 拟修订对象

### 2.1 修订 A — `role` enum 新增 `preprocessing`

**文件**：`AITutors-v3/Docs/V3_SPEC/10_Data_Model.md`
**位置**：§4.2 `document_source_versions` 字段表（现行 `:136`）

```text
现行：
| role | VARCHAR | native / ocr_ppsv3 / ocr_ppsvl / docx / canonical |

拟改为：
| role | VARCHAR | native / ocr_ppsv3 / ocr_ppsvl / docx / canonical / preprocessing |
```

### 2.2 修订 B — `provider` enum 新增 `preprocessing`

**同文件同表**（现行 `:137`）

```text
现行：
| provider | VARCHAR | native / ppsv3 / paddleocr-vl / docx |

拟改为：
| provider | VARCHAR | native / ppsv3 / paddleocr-vl / docx / preprocessing |
```

> `[OWNER DECISION]` provider 取值为字符串 `preprocessing`（**不是** `papers`）。
> 见 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` §1.2。

### 2.3 修订 C — role/provider 封闭配对新增一条

**同文件** §4.2 约束段（现行 `:150-153`）

```text
现行：
ocr_ppsv3 ⟺ ppsv3、ocr_ppsvl ⟺ paddleocr-vl、native ⟺ native、docx ⟺ docx；
canonical role 无 provider。

拟新增：
preprocessing ⟺ preprocessing
```

### 2.4 修订 D — `artifact_kind`：禁用 `markdown`，Primary Path 取 `canonical_l1`

**同文件** §4.2 `artifact_kind` 字段（现行 `:135`）

```text
现行 enum：original_binary / raw_l1 / canonical_l1

[OWNER DECISION] Primary Path 的 artifact_kind 明确取 canonical_l1。
[OWNER DECISION] 禁止以 markdown 作为 artifact_kind。
```

**`[FACT]` 现行违规**：`runner.py:89` 与 `runner_b2.py:337` 当前传入 `artifact_kind="markdown"`，
**不在闭集内**。该违规在 `PRODUCER-PROVENANCE-DECISION-01.md §1.4` 已登记。

**`[FACT]` 闭集目前无代码强制**：全 `backend/app` 内 `artifact_kind` 仅出现于
`seal.py:36,128,141`（常量与传参），**不存在闭集校验器** ⇒ 非法值可静默写入。
⇒ 见 §4.2 实现影响。

### 2.5 修订 E — `source_meta` 内容口径（**条件性**）

**同文件** §4.2 `source_meta` 字段（现行 `:143`）

现行口径：「提取配置、page_range、OCR 证据、`legacy` 标记」。

`OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 3 判定
**producer metadata 不进入 `source_meta`** 作为长期扩展字段 ⇒ **本字段口径无需为 producer 扩展**。

但 `[OPEN]`：

```text
source_meta 当前无 sealed 不可变性（task/executor.py:258-270 可在 sealed 后改写）。
是否为 source_meta 补 sealed 写入守卫，属独立缺口（REVISION-02 R-4b），
不在本 errata 的必然范围内 —— 需 Owner 另行裁定。
```

### 2.6 修订 F — Artifact Compatibility Rule（`[OWNER DECISION]`）

**同文件** §4.2 约束段新增 `role` / `provider` / `artifact_kind` 的**允许组合表**。

| role | provider | artifact_kind |
|---|---|---|
| `native` | `native` | `original_binary` / `raw_l1` |
| `preprocessing` | `preprocessing` | `canonical_l1` |
| `ocr_ppsv3` | `ppsv3` | `raw_l1` |
| `ocr_ppsvl` | `paddleocr-vl` | `raw_l1` |
| `docx` | `docx` | `original_binary` / `raw_l1` |
| `canonical` | **none** | `canonical_l1` |

**必须同时写明**：

```text
canonical_l1 describes artifact maturity,
not producer identity.
```

**明确禁止下列推断**：

```text
✗ “canonical_l1 requires canonical role”
```

⇒ `artifact_kind` 表达的是 **artifact 成熟度**，**不是** producer 身份；
因此 `preprocessing` role 配 `canonical_l1` **合法**。

> `[FACT]` 本条同时关闭 Blocking-3。

---

## 3. 修改理由

| # | 理由 | 依据 |
|---|---|---|
| 1 | 真实架构的 L1 生产者是 preprocessing pipeline，**不属于**现有五个 role 中任何一个 | Owner Decision 1 |
| 2 | 强行映射会导致 **provenance 失真**（`native` 或 `ocr_ppsv3` 均谎报 L1 来源） | `IDENTITY-PROVENANCE-REVISION-02.md` W-3 |
| 3 | `role`/`provider` **进入 seal LE hash**（`contract_domain.parser`）⇒ 错值即**身份漂移**，非纯标签问题 | `10_Data_Model.md:150-153` |
| 4 | Spec 自身要求「**独立引擎必须独立身份，防 identity 漂移**」⇒ 复用既有配对**违反 Spec 本意** | 同上 |
| 5 | `artifact_kind="markdown"` 为**现行违规**，须一并纠正，避免二次返工 | `PRODUCER-PROVENANCE-DECISION-01.md §1.4` |

---

## 4. 影响面

### 4.1 Migration impact

| 项 | 判定 |
|---|---|
| 本 errata 本身 | **不产生 migration**。`role`/`provider`/`artifact_kind` 均为 `VARCHAR`，**无 CHECK 约束、无 enum 类型** ⇒ 扩值**无需 DDL** |
| producer metadata 独立表（Decision 3） | ✅ **需要 migration**（新表）。**不在本 errata 范围**，属实现轮 |
| 已 sealed 行的 `le_hash` | ⚠️ **不可就地修正**（`body_text` 等列有 sealed 守卫）。**历史无此类行**（见下行） |
| DB 是否已有此类行 | ✅ **RESOLVED** — 2026-09-27T09:13:28Z 实测：`Primary Path documents = 0`、`Primary Path source_versions = 0`、**全库业务表为空**。确认：`No Primary Path persistence data exists.` / `No migration remediation required.`<br>历史轨迹：本项曾为 `[OPEN]`（依 `REVISION-02` R-5 高置信度推测为「无」，但**未确证**）；现已实测确证。 |

### 4.2 Implementation impact（**MIMO CODE 后续范围；本轮零改动**）

> **本表不编号。** 能力名称即授权边界的标识 —— 编号属执行计划，
> **不得**成为授权边界（同一能力在不同文档曾出现 `I-6` / `I-7` 两种编号，已消除）。

| 能力 | 内容 | 位置 |
|---|---|---|
| `role-provider enforcement` | Primary Path 写入 `role`/`provider` = `preprocessing` | `runner.py:90-91`；`runner_b2.py:338-339` |
| `artifact-kind compatibility enforcement` | `artifact_kind` 由 `"markdown"` 改为 `canonical_l1` | `runner.py:89`；`runner_b2.py:337` |
| `artifact-kind validation` | **新增闭集校验器**（当前不存在）并接入 seal 与 consumer 两条写入路径 | 现仅 `seal.py:39-44` 校验 role/provider；`artifact_kind` **无校验** |
| `original_sha256 identity-domain correction` | `original_sha256` 改为符合 Decision 2 的域（2-B） | `runner.py:74,78`；`runner_b2.py:322,326` |
| `identity byte-domain correction` | 消除「正确身份已算出却被丢弃」：复用 `runner_b2.py:120` 已核对的 raw-bytes identity | 同上 |
| `producer_metadata schema introduction` | 新建 producer metadata 表 + repository 守卫（写入后禁 UPDATE） | 新表；参照 `source_repository.py:148-151` |
| `source repository predicate alignment` | `_version_by_le` 与 `ON CONFLICT` 目标索引**同步**修改（否则 Postgres Binder error） | `source_repository.py:110-113` 与 `:128-138` |
| `seal role-provider enum extension` | `seal.py:39-44` 的 `_SEAL_ROLE_PROVIDERS` 需纳入 `preprocessing ⟺ preprocessing` | `seal.py:39-44` |
| `identity invariant tests` | 新增 identity invariant 测试（现有测试不覆盖） | 见摘要 §3.3 |
| `api compatibility review` | `role`/`provider`/`artifact_kind` 经 `GET /documents/{id}` 暴露，且 `role` 是**排序键** | `api/schemas.py:22-32`；`api/routers/documents.py:224-232`、`:129-133` |
| `model schema test alignment` | 更新 `tests/test_models_schema.py`（含 `assert len(seen) == 11`）——**不得以改断言绕过** | `tests/test_models_schema.py:39,103-107,124,126` |

### 4.3 与 Frozen Contract 的关系

`[FACT]` Frozen Contract（`PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ `f4941ff`）
**不涉及** `role` / `provider` / `artifact_kind` / `source_meta`（这些是 V3 内部 Spec 概念）。

⇒ 本 errata **只触及 Frozen Spec（`10_Data_Model.md`）**，**不触及 Frozen Contract**。

⚠️ **但**：`OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 2 的落地
**可能触及** Contract（因 Contract §1.2 把 `source_content_sha256` 定义为
`SHA256(original source bytes)`）。见 §5。

### 4.4 Derived Hash Impact（`[OWNER DECISION]` 登记）

`[FACT]`（F-1）：`le_hash = f(original_sha256)`
（`runner.py:86`；`seal.py:98-106` 的 `input_domain={"original_sha256": …}`）。

⇒ 由于 `le_hash` 是 `original_sha256` 的函数，**任何 `original_sha256` domain 修订
必须同步重新验证**：

```text
· le_hash
· source version identity
· replay behavior
· uniqueness assumptions
```

**逐项影响**：

| 项 | 影响 | 依据 |
|---|---|---|
| `le_hash` | 输入域变化 ⇒ hash 值变化 ⇒ 无法幂等命中历史行 | `runner.py:86`；`seal.py:98-106` |
| source version identity | `UNIQUE(logical_execution_stage, logical_execution_hash)` 的键值变化 | `models/source.py:52-57` |
| replay behavior | 对已 sealed 文档重跑 ⇒ **不命中**，会新建 version | `source_repository.py:148-151`（sealed 后禁 UPDATE） |
| uniqueness assumptions | `documents.UNIQUE(original_sha256)` 的语义随域定义变化 | `models/source.py:32-34` |
| `ON CONFLICT` 目标 | 若唯一约束与 re-read 谓词不同步 ⇒ Postgres **Binder error**（响亮失败） | `source_repository.py:110-113` vs `:128-138` |

> **⚠️ 本项构成实现的强制前置**：Decision 2 Amendment 采用 2-B 后，
> `original_sha256` 的算法由 `sha256_hex(body_text)` 改为 **接收字节的 SHA256**，
> 该变更**必然改变** Primary Path 的 `le_hash`。⇒ 实现轮**必须**同批处理上表五项，
> 不得只改 `original_sha256` 的赋值。

---

## 5. Blocking 项

### Blocking-1 — Decision 2 的「规范表示」未定义

```text
状态：RESOLVED
裁决：2-B — Scoped Byte-Domain Identity（拒绝 2-A canonicalization）
```

**Owner 裁决原文**（引自 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` §2.2–§2.4）：

```text
original_sha256 represents raw artifact byte identity
within its defined artifact boundary.
It does not represent universal semantic content identity.

same content means same byte sequence inside the same byte domain.
Cross-domain artifacts (PDF, Markdown, canonical L1)
do not require identical original_sha256.
```

**落地算法（无剩余歧义）**：

```text
original_sha256 = SHA256(该 pipeline 实际接收到的 artifact 原始字节)
```

⇒ 因取 2-B，本 errata **范围不变**，且**不触及 Frozen Contract**
（Contract 的 `source_content_sha256` = SHA256(original source bytes) 与本规则**同向**，
无需修订）。

### Blocking-2 — 已 sealed / 已写入数据的处置

```text
状态：RESOLVED（2026-09-27 实测确认）
```

**Required verification**（**已修正**——Owner 指令中的查询在本 schema 上不可执行）：

```sql
-- ❌ Owner 指令原查询（不可执行，且不可用）：
--    document_source_versions 无 created_at 列（仅 source_lines / spans 有 created_at）
--    且 version 行不携带 path 标记，无法按时间窗隔离 Primary Path
-- SELECT count(*) FROM document_source_versions
--  WHERE created_at >= <Primary Path test window>;

-- ✅ 已执行（version 行只能经父 Document 归属）：
SELECT count(*)
  FROM document_source_versions v
  JOIN documents d ON d.id = v.document_id
 WHERE d.original_object_key LIKE 'preprocessing/%';

-- ✅ 已执行：Primary Path 的 Document 行
SELECT count(*) FROM documents WHERE original_object_key LIKE 'preprocessing/%';
```

#### 执行记录（`[FACT]`）

```text
query      : 上列两条 SELECT（只读；无 DDL / DML）
result     : Primary Path documents       = 0
             Primary Path source_versions = 0
             全库 documents               = 0
             全库 document_source_versions= 0
             provider 分布                = []（空集）
             object_key 分布              = []（空集）
timestamp  : 2026-09-27T09:13:28Z
environment: localhost:5432/aitutors（APP_ENV=test）
```

**判定**：数据库**完全为空**——不仅是「无 Primary Path 行」，而是**全部业务表零行**。

⇒ **不存在 Primary Path persistence data**；**不需要任何数据修复 / migration 数据处置**。

```text
Blocking-2: RESOLVED
Reason: No Primary Path persistence data exists.
        No migration data remediation required.
```

> `[FACT]` 本次为**只读查询**：未执行 DDL / DML，未修改 schema，未写入任何行。
> 临时查询脚本已从工作区移除；上列 SQL 为**可复现原文**。

**说明**：`documents.original_object_key` 是唯一写入即固定的 Primary Path 路径标记
（`runner.py:77` 写 `preprocessing/<name>`；`seal.py:88` 写 `raw:<sha>`；
`import_service.py:70-76` 写 `data/imports/<sha>.<ext>`）。

**确认后才能**：

```text
Errata FINAL APPROVED
```

### Blocking-3 — `artifact_kind = canonical_l1` 与 role 配对惯例

```text
状态：RESOLVED
裁决：role=preprocessing / provider=preprocessing / artifact_kind=canonical_l1 合法
依据：本文件 §2.6 Artifact Compatibility Rule
```


---

## 6. Errata 正文（已批准；待移入 V3 仓）

> 以下为**拟写入** `10_Data_Model.md` 的文本形状。
> **本 errata 已于 2026-09-27 获 Owner 批准**（见头部 `Status: FINAL APPROVED`）；
> 该文本**尚未应用于 V3 仓 Spec 正文** —— 应用于 `AITutors-v3` 属另立动作，
> 须在该仓执行并记录 Frozen Spec 新 hash（见 §7）。

```text
§4.2 document_source_versions —— role/provider 封闭配对（amend）

role     : native / ocr_ppsv3 / ocr_ppsvl / docx / canonical / preprocessing
provider : native / ppsv3 / paddleocr-vl / docx / preprocessing

配对：
  ocr_ppsv3     ⟺ ppsv3
  ocr_ppsvl     ⟺ paddleocr-vl
  native        ⟺ native
  docx          ⟺ docx
  preprocessing ⟺ preprocessing          ← 新增
  canonical     : 无 provider

artifact_kind : original_binary / raw_l1 / canonical_l1
  · Primary Path（producer = preprocessing pipeline）取 canonical_l1。
  · markdown 不得作为 artifact_kind。
  · 闭集须由代码强制（当前无校验器）。

Artifact Compatibility Rule（role / provider / artifact_kind 允许组合）：
  native        ⟺ native          → original_binary / raw_l1
  preprocessing ⟺ preprocessing   → canonical_l1            ← 新增
  ocr_ppsv3     ⟺ ppsv3           → raw_l1
  ocr_ppsvl     ⟺ paddleocr-vl    → raw_l1
  docx          ⟺ docx            → original_binary / raw_l1
  canonical     : 无 provider     → canonical_l1

  canonical_l1 describes artifact maturity, not producer identity.
  禁止推断「canonical_l1 requires canonical role」。

说明：
  preprocessing role 表示该 L1 artifact 的产出引擎为 preprocessing pipeline；
  与 native（V3 本地确定性解析）及 ocr_ppsv3（ppsv3 OCR 引擎）为
  相互独立的生产引擎，依「独立引擎必须独立身份，防 identity 漂移」不得互相复用。
  Producer 的名称/版本/artifact hash 等 provenance 记录于独立表
  （见 producer_metadata），不写入 role/provider，亦不作为 source_meta 长期扩展字段。
```

---

## 7. 批准后动作（**本轮不执行**）

```text
1. Owner 批准本 errata
2. ~~Blocking-2 DB confirmation~~ ✅ 已于 2026-09-27T09:13:28Z 完成（§5）
3. 在 AITutors-v3 仓执行 Spec 修订（另立动作；须记录 Frozen Spec 新 hash）
4. 更新 AITutor-X 侧的 Frozen Spec 引用与 hash 记录
5. 另立 Implementation Authorization
6. MIMO CODE 按 §4.2 实现 + 补 identity invariant tests
```

> **Blocking-1 / Blocking-2 / Blocking-3 均已 RESOLVED。**
> 剩余动作仅为 Owner 批准与 Implementation Authorization 签发。

---

*Recorded 2026-09-27. 本文件为 Frozen Spec Change Proposal（未生效）。不含 `[OWNER DECISION]` 的批准动作；其中引用的 Owner 裁决见 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md`。*
