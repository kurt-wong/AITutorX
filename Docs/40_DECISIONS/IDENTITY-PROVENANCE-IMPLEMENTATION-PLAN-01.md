# IDENTITY-PROVENANCE-IMPLEMENTATION-PLAN-01

**Document Type**: Implementation Plan（**非授权**；不产生代码、不产生 migration）
**Status**: `OPEN`
**Date**: 2026-09-27
**Owner Directive**: 输出 IMPLEMENTATION-PLAN-01，内容仅限 6 项（见 §2）
**Gate**: **D-ID-6 / D-PP-6 未最终裁决前，本计划不得开工**
**Explicitly NOT**: 修改 V3 / 修改 Papers / 跑 DB / 创建 migration / 进入代码实现

---

## 0. 前置更正（必须先读，否则 §4/§5 会基于错误前提）

Owner 指令中有 **2 处**需更正。本轮**只读**核实，逐条附证据。

### 0.1 更正 A — D-ID-6 的验证查询将无法执行

**Owner 指令中的查询**：

```sql
select count(*) from source_versions
where provider='native' and metadata->>'producer'='preprocessing';
```

**三处不成立**（`[FACT]`，逐条可核对）：

| # | 指令写法 | 实际 | 证据 |
|---|---|---|---|
| A1 | 表 `source_versions` | 表名为 **`document_source_versions`** | `app/models/source.py:47`；`alembic/versions/20260907_0006_seal_idempotency.py:44` |
| A2 | 列 `metadata` | 列名为 **`source_meta`**（JSONB） | `app/models/source.py:72` |
| A3 | `provider='native'` 且 `producer='preprocessing'` | **Primary Path 行不含任何 `producer` 键**，且其 `source_meta` 为 **NULL** | `runner.py:87-100` `create_source_version(...)` **未传 `source_meta`**；`runner_b2.py:335-348` 同 |

⇒ 该查询**恒返回 0**，会把「有数据」误判为「无数据」，从而错误解除 D-ID-6 的 BLOCKED。
**这正是 D-ID-6 要防的那类错误**（用未核实的假设解除阻塞），故在此显式拦下。

#### 0.1.1 唯一可靠的判别式（`[FACT]`）

Primary Path 与 seal 路径在**两个字段**上可区分：

| 判别字段 | seal 路径（生产/Native） | Primary Path（runner / runner_b2） |
|---|---|---|
| `source_meta` | **总是非 NULL**：`{"engine": <name>, "method": "text-layer"}`（`providers.py:100`）→ `seal.py:150` `source_meta=dict(result.source_meta)` | **NULL**（未传参数，默认 `None`，`source_repository.py:79`） |
| `original_object_key` | `raw:<sha256>`（`seal.py:88`） | `preprocessing/<file name>`（`runner.py:77`；`runner_b2.py:325`） |

`[ANALYSIS]` 其中 `original_object_key` 更可靠：它是**字面前缀**，不依赖 `source_meta` 的填充行为；
`source_meta IS NULL` 依赖「seal 必填、runner 必不填」这一当前事实，正确但对未来改动更敏感。

#### 0.1.2 建议执行的查询集（**供 Owner 决定是否授权运行**）

```sql
-- Q1  最高置信：Primary Path 落库行（对象键前缀）
select count(*) from documents
where original_object_key like 'preprocessing/%';

-- Q2  Primary Path 产生的 SourceVersion（cross-check Q1）
select count(*) from document_source_versions v
join documents d on d.id = v.document_id
where d.original_object_key like 'preprocessing/%';

-- Q3  风险上限：所有 (stage,le_hash) 冲突可能波及的文档数（D-ID-2 塌缩暴露面）
select count(*) from (
  select logical_execution_stage, logical_execution_hash
  from document_source_versions
  where logical_execution_stage is not null
  group by 1,2 having count(*) > 1
) t;

-- Q4  是否已存在跨文档同 (stage,hash) 的实例（塌缩是否已发生）
select v1.document_id, v2.document_id, v1.logical_execution_hash
from document_source_versions v1
join document_source_versions v2
  on  v1.logical_execution_stage = v2.logical_execution_stage
  and v1.logical_execution_hash  = v2.logical_execution_hash
  and v1.document_id <> v2.document_id;

-- Q5  总量基线
select count(*) from documents;
select count(*) from document_source_versions;
select provider, count(*) from document_source_versions group by 1;
```

`[ANALYSIS]` **Q4 是信息量最大的一条**：若返回非空，则 D-ID-2 的塌缩**已经发生**，
其严重度从「潜在缺陷」升级为「已污染数据」；D-ID-6 与 D-ID-5 必须合并处置。

> **注**：`provider` 当前只会出现 `native`（seal 路径与 runner 都用它），
> 故 Q5 的 `group by provider` **不能**区分两条路径——再次说明不能用 provider 做判别。

### 0.2 更正 B — D-PP-6 的裁决文本与其示例**互相矛盾**

**Owner 裁决文本**：

```text
role = 产生该 L1 的解析/转换引擎          ← 保持 Frozen Spec 原语义
不建议立即新增 role=preprocessing          ← NOT APPROVED
```

**Owner 示例**：

```json
{ "role": "preprocessing", "provider": "papers",
  "ingestion": { "service": "AITutors-v3", "version": "..." } }
```

**`[ANALYSIS]` 矛盾点**：示例中的 `role="preprocessing"` 与 `provider="papers"`
**正是裁决文本明令不批准的「新增 role」**。且：

- `provider="papers"` **不在** Frozen Spec 闭集内（闭集 = `native / ppsv3 / paddleocr-vl / docx`，
  `10_Data_Model.md:137`）；
- `role="preprocessing"` **不在** role 闭集内（`10_Data_Model.md:136`）。

**`[FACT]` 更关键的逻辑后果**（必须让 Owner 看到，否则 D-PP-6 无法收敛）：

```text
设定  role := 产生该 L1 的解析/转换引擎      （Owner 裁决，保持 Spec 原语义）
事实  Primary Path 的 L1 由 preprocessing 产生
--------------------------------------------
推出  Primary Path 的 role 【不能】是 productive 的 native
```

⇒ 即：**「保持 Spec 原语义」与「不新增 role」在当前枚举下不可同时满足**。
要么 Spec 语义让步，要么新增 role，要么把 Primary Path 映射到**枚举中已有的「外部 L1 生产引擎」**。

#### 0.2.1 枚举内唯一自洽的映射（`[ANALYSIS]`，供裁决）

Spec 闭集中已存在一个**外部 L1 生产引擎**配对：

```text
ocr_ppsv3 ⟺ ppsv3          （10_Data_Model.md:150-151）
```

`[ANALYSIS]` 若 Owner 意图是「不新增 role」，则**唯一不需要改 Spec 的诚实取值**是复用该配对：

| 理由 | 说明 |
|---|---|
| 语义 | `ppsv3` 是 Papers 侧的 L1 生产引擎；`role` 描述「产出 L1 的引擎」→ 语义成立 |
| 与 Owner 裁决文本一致 | ✅ 保持 Spec 原语义 |
| 无需 Spec 修订 | ✅ 不触发 D-PP-1 的 LEVEL 2 |
| 保留的能力 | 与 seal 的 `native`（V3 本地解析）**天然区分** → provenance 不再失真 |
| 代价 | `source_meta.producer` 需如实记录「该 L1 由 preprocessing 而非 OCR-only 阶段产出」以保留差异 |

⇒ 这是 §7 决策表中 **D-PP-1（PP-B）** 的重新激活，且**与 D-PP-7（producer metadata）互补**：
`role/provider` 回答「哪类引擎」，`producer` metadata 回答「哪个具体 producer 与版本」。

> **不预判**：本文件只登记。D-PP-6 的最终取值仍为 `[OWNER DECISION]`。

---

## 1. 当前 Frozen Contract 影响面

### 1.1 判据（`[FACT]`）

`role`/`provider`/`artifact_kind` 三者的闭集定义在 **Frozen Spec**（`AITutors-v3/Docs/V3_SPEC/10_Data_Model.md`），
不在 Frozen Contract。Frozen Contract（`PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ `f4941ff`）管的是
Producer → Consumer 接口面（`source_content_sha256` / `identity_version` / manifest 形状）。

| 拟改动 | 触及对象 | 是否需要 Frozen Spec / Contract 修订 |
|---|---|---|
| `original_sha256` 改为 V3 ingestion raw bytes（D-ID-1，**已 APPROVED**） | V3 代码实现选择 | ❌ **不需要**。`10 §4.1:117` 原文即「原始文件 SHA256」，本改动是**服从**而非改写 |
| `source_content_sha256` 独立保存（D-ID-1，已 APPROVED） | `source_meta`（JSONB，已存在） | ❌ 不需要（见 §3） |
| `execution_key` / `content_identity` 分层（D-ID-2，APPROVED WITH REFINEMENT） | `document_source_versions` 唯一约束 | ⚠️ **可能需要**（§3 详述） |
| Primary Path 的 `role` 取值（D-PP-6，**未决**） | `10 §4.2:136,150-153` role 闭集 | ⚠️ **取决于裁决**：复用 `ocr_ppsv3` ⇒ ❌ 不需要；新增 role ⇒ ✅ **需要 Spec 修订** |
| `producer` metadata（D-PP-7，APPROVED WITH SCOPE） | `source_meta` 语义 | ❌ 字段已存在；⚠️ 但 `10 §4.2:143` 对 `source_meta` 的内容有列举，**扩展其语义应留痕** |
| `artifact_kind="markdown"`（现状违规） | `10 §4.2:135` 闭集 | ❌ 不需要（改回闭集内的值即是服从） |

### 1.2 `[ANALYSIS]` 结论

**若 D-PP-6 取「复用 `ocr_ppsv3 ⟺ ppsv3`」**（§0.2.1），则本计划
**不需要任何 Frozen Spec / Frozen Contract 正文修订** —— 全部改动落在 V3 代码与既有字段语义内。
这是**唯一**能让 Step 2 不触发 LEVEL 2 的路径。

**若 D-PP-6 取「新增 `preprocessing` role」**，则需独立 Owner authorization 改 `10 §4.2`，
并同步 `seal.py:39-44` 闭集、`test_seal.py` 断言、以及 `document_active_sources.role` 的语义说明。

> **`[FACT]` 降低风险的一点**：`DocumentActiveSource`（`models/source.py:155`，复合 PK `(document_id, role)`）
> **在全后端零使用**（`grep` 仅命中定义与 `__init__` 导出）。
> ⇒ 改动 `role` 取值**不会**破坏 active-source 选择逻辑。这是风险面收窄的实证。

---

## 2. 交付范围（Owner 指定 6 项）

| # | 章节 | 状态 |
|---|---|---|
| 1 | 当前 Frozen Contract 影响面 | ✅ §1 |
| 2 | 需要修改的文件列表 | ✅ §4 |
| 3 | schema 是否变化 | ✅ §3 |
| 4 | migration 是否需要 | ✅ §5 |
| 5 | backward compatibility 策略 | ✅ §6 |
| 6 | 测试矩阵 | ✅ §7 |

---

## 3. Schema 是否变化

### 3.1 逐项判定（`[FACT]` + `[ANALYSIS]`）

| 改动 | 是否需 schema 变化 | 说明 |
|---|---|---|
| `original_sha256` 来源改为 raw bytes | ❌ **否** | 列类型 `String(64)` 不变；只改写入值（代码层） |
| `source_content_sha256` 独立保存 | ❌ **否** | `source_meta` 已是自由 `JSONB`（`models/source.py:72`），可承载 `producer{...}`；**零 DDL** |
| `producer{name,version,artifact_hash,manifest_hash}` | ❌ **否** | 同上，JSONB 内嵌套 |
| `artifact_kind` 改回闭集值 | ❌ **否** | 列不变，取值变 |
| `role`/`provider` 取值修正 | ❌ **否** | 列不变，取值变 |
| **`execution_key` / `content_identity` 分层（D-ID-2）** | ⚠️ **可能是** | 见 §3.2 |
| `parent_version_id` 承载 lineage（D-ID-3） | ❌ **否** | 列已存在（`models/source.py:65`），当前零写入（死字段） |

### 3.2 D-ID-2 的唯一 schema 风险点（**必须由 Owner 明确**）

当前唯一约束（`models/source.py:52-57`；`alembic/versions/20260907_0006:42-46`）：

```sql
UNIQUE (logical_execution_stage, logical_execution_hash)
```

D-ID-2 裁决要求「保留 content hash 能力 + 修复 conflict re-read document scope +
execution identity 与 artifact identity 分层」。三种实现路径的 schema 后果不同：

| 路径 | 做法 | schema 变化 | 是否满足「保留 content hash 幂等」 |
|---|---|---|---|
| **D-ID-2-a** | `logical_execution_hash` 的**输入域**加入 document identity | ❌ **无 DDL**（仅改计算输入） | ⚠️ **不满足**——同内容跨文档不再命中，这正是 Owner 要保留的能力 |
| **D-ID-2-b** | 唯一约束改为 `UNIQUE(document_id, logical_execution_stage, logical_execution_hash)`；hash 输入域不变 | ✅ **需 DDL**（drop + add constraint） | ✅ 满足：同文档同输入幂等；跨文档不再塌缩 |
| **D-ID-2-c** | 新增独立列 `content_identity`（artifact identity），`le_hash` 保持 execution identity | ✅ **需 DDL**（add column + index） | ✅ 满足，且**显式分列**两个 identity，最贴合 Owner 的「拆两个概念」 |

**`[ANALYSIS]` 取向**：

- D-ID-2-a **被 Owner 明确排除**（会损失幂等能力）；
- D-ID-2-b 是**最小充分修复**：它把「唯一性」限定到 document scope，
  而 `_version_by_le` 的 re-read 也随之变为 document-scoped（两处**必须同步改**，§4）；
- D-ID-2-c 显式性最好，但引入新列，需 migration 且需定义 `content_identity` 的域归属
  （很可能是 I-0 / I-1 的别名 → 可能与 `original_sha256` / `body_hash` **语义重叠**，须先裁决避免第三份重复身份）。

> **🟡 D-PP-6 之外的第二处未决点**：D-ID-2 具体取 a/b/c **尚未裁决**。
> 本计划**假设 D-ID-2-b**（最小充分、无新列）用于 §4/§5/§6 的展开，并**显式标注该假设**。
> 若 Owner 选 D-ID-2-c，§5 的 migration 规模与 §6 的兼容策略需重做。

---

## 4. 需要修改的文件列表（**清单，非实施**）

> 全部路径相对 `D:\Project\AITutors-v3\backend`。**本计划不修改任何文件。**

### 4.1 V3 应用代码（Identity Flow）

| # | 文件 | 拟改动 | 依赖裁决 |
|---|---|---|---|
| F1 | `scripts/preprocessing_consumer/runner.py` | ① `file_sha = sha256_hex(body_text)` → 复用已核对的 raw-bytes identity；② `role`/`provider`/`artifact_kind` 改为裁决值；③ `le_hash` 改用统一权威函数；④ 传 `source_meta={"producer": {...}}` | D-ID-1 ✅ / D-ID-2 / D-PP-6 / D-PP-7 |
| F2 | `scripts/preprocessing_consumer/runner_b2.py` | 同 F1（`_create_source_records` `:313-348`；`le_hash` `:334`） | 同上 |
| F3 | `scripts/preprocessing_consumer/source_loader.py` | 可能新增「raw bytes 读取」入口（或改调 `app/core/raw_bytes_identity.py`） | D-ID-1 ✅ |
| F4 | `app/repositories/source_repository.py` | ① `_version_by_le`（`:128-138`）改 document-scoped；② `create_source_version`（`:110-121`）`ON CONFLICT` 目标索引与 re-read 谓词**同步**改；③ `find_sealed_version_by_le`（`:211-220`）核对一致性 | D-ID-2 |
| F5 | `app/models/source.py` | 若取 D-ID-2-b/c：`__table_args__` 唯一约束变更 | D-ID-2 |
| F6 | `app/core/hashing.py` 或新建 `app/core/identity.py` | `le_hash` 单一权威构造函数（消除 seal 与 runner 双公式） | D-PP-4 |
| F7 | `app/domains/source/seal.py` | ① 若 D-PP-6 新增 role：`_SEAL_ROLE_PROVIDERS`（`:39-44`）扩集；② `le_hash` 改调统一权威函数；③ 保留 `original_sha256 = sha256(file_bytes)`（`:83`）不变 | D-PP-6 / D-PP-4 |

### 4.2 明确**不**修改（边界声明）

| 文件/目录 | 原因 |
|---|---|
| `app/domains/compile/**`、`app/domains/gate/**` | Semantic Flow；本次不触碰（`F-M3-04 / M.3` 已 CLOSED） |
| `AITutors-v3/Docs/V3_SPEC/**` | Frozen Spec；除 D-PP-6 裁定需修订外**不动** |
| `Papers/**` | Producer 工作树；本轮**零改动**。producer 自述字段若需新增，属独立任务（D-PP-5） |
| `runner.py:9-13` 记录的 85 号 §5 边界 | **保持**（Seal 不入 semantic 路径） |

### 4.3 Papers 侧的牵连（**登记但不实施**）

若 D-PP-7 要求 Producer 自述 `producer{name, version, artifact_hash, manifest_hash}`，
则 Papers 需在 manifest 增加该段 → 触及 **Frozen Contract**（接口形状）。
`[ANALYSIS]` 但 `manifest_hash` / `artifact_hash` **可由 Consumer 自行计算**，
故**可能无需改 Papers**（Consumer 知道 manifest 路径与 artifact 路径）。
⇒ 该点建议单列为 **D-PP-8**（producer 是否必须自述，还是 Consumer 计算），本计划不预判。

---

## 5. Migration 是否需要

### 5.1 结论（依 §3 假设 D-ID-2-b）

| 场景 | 是否需要 migration |
|---|---|
| `original_sha256` 来源修正 / `source_content_sha256` 入 `source_meta` / `role`/`provider`/`artifact_kind` 取值修正 | ❌ **不需要**（纯代码层；JSONB 与既有列复用） |
| D-ID-2-b（唯一约束加 `document_id`） | ✅ **需要 1 个 new migration**（drop `uq_source_versions_le` + add `uq_source_versions_le_doc`） |
| D-ID-2-c（新增 `content_identity` 列） | ✅ 需要（add column + index） |
| D-ID-3（复用 `parent_version_id`） | ❌ 不需要（列已存在） |
| D-ID-6（已 sealed 行处置） | ⛔ **BLOCKED**——不得设计（Owner 明令） |

### 5.2 现有 migration 链（`[FACT]`）

```text
0001 initial_abc
0002 tighten_nullable
0003 runtime
0004 tasks
0005 task_llm_invocations
0006 seal_idempotency        ← 建立了 uq_source_versions_le
0007 question_dedup_unique
0008 subject_grade_nullable
0009 source_figures_unique
0010 source_spans
0011 validation_events        ← 当前 head
```

⇒ 新 migration 编号应为 **`0012`**，`down_revision = "0011"`。

### 5.3 ⛔ 停止条件

```text
在 D-ID-6 / D-PP-6 最终裁决完成前：
  ❌ 不得创建 migration 文件
  ❌ 不得在 DB 上执行任何 DDL/DML
  ❌ 不得运行 alembic upgrade/downgrade
```

**`[ANALYSIS]` 新增风险提示**：D-ID-2-b 的约束变更与 D-ID-6 是**同一枚硬币**。
若 DB 中已有重复 `(stage,hash)` 行（§0.1.2 Q4 非空），
则 `ADD CONSTRAINT ... UNIQUE(document_id, stage, hash)` 可能**因既有数据而失败**。
⇒ **Q4 必须先于任何 migration 设计执行**（且需 Owner 授权才可运行）。

---

## 6. Backward compatibility 策略

### 6.1 兼容性矩阵

| 既有资产 | 影响 | 策略 |
|---|---|---|
| 已 sealed 的 `document_source_versions`（seal 路径） | `original_sha256` 语义不变（seal 已是 raw bytes）；`le_hash` **会变**（若 role/provider/公式改） | ⛔ 处置 = D-ID-6（BLOCKED） |
| 已 sealed 行的 `source_meta` | 追加 `producer` 键不破坏既有读取（`documents.py:237` 读 `source_meta.quality`；`task/executor.py:267` 合并写） | ✅ 加法式扩展，向后兼容 |
| 既有 sealed 行的 `body_hash` / `integrity_hash` | 不受本计划影响 | ✅ 不变 |
| `_version_by_le` 的调用方 | 若签名加 `document_id`，调用点需同步（仅 `create_source_version` `:118`） | ⚠️ 单点，低风险 |
| API 响应字段（`api/schemas.py:113-114`） | 若 `le_hash` 语义变，响应值变 | ⚠️ 需确认是否有外部消费者 |
| Frozen Spec 文本 | 若 D-PP-6 复用 `ocr_ppsv3` ⇒ 零改动 | ✅ |

### 6.2 `[ANALYSIS]` 关键兼容结论

> **`le_hash` 是唯一「改则不可逆」的字段。**
> 一旦某行 sealed，其 `le_hash` 永久冻结且禁 UPDATE（`source_repository.py:143-147`）。
> 因此本计划的所有 identity 语义修正**必须在第一批生产写入之前完成**
> —— 这正是 Step 0/1 先于 Step 4/5 的原因。

### 6.3 双读/双写过渡（**仅在 D-ID-6 裁定后适用**）

若 D-ID-6 裁定「保留历史行」：

```text
读路径：按 (document_id, stage, new_hash) 查；未命中则以 (stage, old_hash) 兼容查（标记 legacy）
写路径：只写 new_hash
```

`[ANALYSIS]` 该过渡**需要 `source_meta.legacy` 标记**（`10 §4.2:143` 已列 `legacy` 为合法内容）
⇒ 与 D-PP-7 的 `source_meta` 语义扩展**同源**，建议合并设计。

---

## 7. 测试矩阵

### 7.1 必须**新增**的测试（Identity correctness）

| # | 测试目标 | 断言要点 | 依赖 |
|---|---|---|---|
| T1 | `original_sha256` 来源正确 | 写入值 == `SHA256(raw bytes)`，**且 ≠** `sha256_hex(body_text)` | D-ID-1 ✅ |
| T2 | Producer hash 独立保存 | `source_meta.producer.artifact_hash == manifest.source_content_sha256`（或按 D-PP-8 裁定） | D-PP-7 |
| T3 | **跨文档不塌缩**（D-ID-2 核心） | 两个 document 写入**相同正文** → 各自获得**独立** SourceVersion，`document_id` 正确 | D-ID-2 |
| T4 | 同文档同输入幂等 | 同一 document 重复写入 → **命中既有** version（不新增） | D-ID-2 |
| T5 | re-read scope 一致 | `ON CONFLICT` 目标索引与 `_version_by_le` 谓词**同域**（可做静态断言） | D-ID-2 |
| T6 | `le_hash` 全路径一致 | seal 与 runner 对**同一执行**产生**相同** hash（消除双公式） | D-PP-4 |
| T7 | `role`/`provider`/`artifact_kind` 闭集 | 取值 ∈ Frozen Spec 闭集；非法值 fail-fast | D-PP-6 |
| T8 | `sealed` 不可变 | 改 identity 相关列 → 抛 `SealedVersionError` | 既有行为回归 |
| T9 | replay identity | 对已 sealed 文档重跑 → 幂等命中（若 D-ID-6 选「无数据」则此测试为新增基线） | D-ID-6 |

### 7.2 已有回归护栏（**不得以改断言方式绕过**）

`[FACT]` 来源-文本 / AST 断言（详见 `PRODUCER-PROVENANCE-DECISION-01.md` §8）：

| 测试 | 位置 | 约束 |
|---|---|---|
| `test_both_runtime_runners_call_the_single_entry_point` | `test_x26_fint08:461-467` | 两 runner 必须含 `enforce_interface_scope` |
| `test_interface_scope_gate_runs_before_gate_service_in_runner` | 同上 `:488-491` | 边界闸门索引 < `_track_a` |
| `test_normalize_interface_identity_has_one_production_call_site` | 同上 `:469-479` | 全 `scripts/` 仅 1 处调用 |
| `test_runners_contain_no_identity_version_comparison` | `test_x26_frb01:534-551` | AST：两 runner 零 `identity_version` 比较 |
| `test_membership_rule_constant_lives_only_in_boundary` | 同上 `:553-561` | 常量不越界 |
| `test_malformed_form_is_judged_only_inside_normalize` | 同上 `:563-575` | 错误码不越界 |

### 7.3 `[FACT]` 护栏覆盖缺口（必须补）

`[FACT]`（独立只读复核）：现有测试对 `_create_source_records` 全 4 处引用均为 `patch` +
断言 `call_count == 0`（`fint08:348-350,394-398`；`frb01:400-402,450-454`），
且真实 `_run_full_chain` 调用都以 `gate="BLOCK"` 在 `runner_b2.py:383-387` 提前返回。
⇒ **函数体从未被执行**，且无任何测试断言 `role`/`provider`/`original_sha256`/`le_hash`。

> ⚠️ **含意**：本次修改的行为面**完全不在现有测试覆盖内**。
> 「测试全绿」**不能**证明 identity 已修好。T1–T9 **必须新增**。

### 7.4 测试分层建议

```text
单元（无 DB）      T5 / T6 / T7 / T8
DB flow（隔离库）  T1 / T3 / T4 / T9          ← 需 Step 4 Isolated Test Database
静态/AST          T5 的 re-read 谓词一致性断言
```

**`[ANALYSIS]`** T3/T4 需真实 DB 事务语义（`ON CONFLICT`）⇒ 归入 **Step 4/5**，不得在 Step 2/3 提前。

---

## 8. 开工门禁（Gate）

```text
Step 0  Identity Domain Decision
          ✅ D-ID-1  APPROVED
          🟡 D-ID-2  APPROVED WITH REFINEMENT（a/b/c 未定 → §3.2）
          ✅ D-ID-3  （建议复用 parent_version_id）
          ✅ D-ID-4  APPROVED
          🟡 D-ID-5  OPEN（需 DB 事实）
          ⛔ D-ID-6  BLOCKED BY FACT（§0.1）
        ⇒ Step 0 未完成：D-ID-2(a/b/c) 与 D-ID-6 未收口

Step 1  Producer Provenance Decision
          ✅ D-PP-1  APPROVED（PP-E 独立 metadata）
          ✅ D-PP-2  闭集取值
          —  D-PP-3  撤回
          ✅ D-PP-4  APPROVED
          🟡 D-PP-5  （producer 是否自述，牵连 Papers）
          🟡 D-PP-6  未决（§0.2 矛盾待解）
          ✅ D-PP-7  APPROVED WITH SCOPE
          🆕 D-PP-8  （producer 自述 vs Consumer 计算；建议单列）
        ⇒ Step 1 未完成：D-PP-6 未收口

Step 2  Implement Identity Creation Path        ⛔ 禁止开工
Step 3  Regenerate Primary Path Evidence        ⛔ 禁止开工
Step 4  Isolated Test Database                  ⛔ 禁止开工
Step 5  Candidate Persistence Verification      ⛔ 禁止开工
Step 6  Primary Path Reference Run Freeze       ⛔ 禁止开工
```

### 8.1 本文件未做的事（Non-Actions）

```text
✅ 未修改 AITutors-v3 任何文件
✅ 未修改 Papers 任何文件
✅ 未执行任何 DB 查询 / DDL / DML
✅ 未创建任何 migration
✅ 未创建任何新治理机制 / Registry / Gate
✅ 未产生任何 [OWNER DECISION]
```

---

## 9. 需要 Owner 收口的最小问题集（按优先级）

| # | 问题 | 为何阻塞 |
|---|---|---|
| **1** | **§0.2**：`role` 裁决与示例矛盾；是否取「复用 `ocr_ppsv3 ⟺ ppsv3`」？ | 阻塞 D-PP-6 → 阻塞 F1/F2/F7 → 阻塞 Step 2 |
| **2** | **§0.1**：是否授权运行 Q1–Q5？（修正后的查询集） | 阻塞 D-ID-6 / D-ID-5；且 Q4 决定塌缩是否已发生 |
| **3** | **§3.2**：D-ID-2 取 a / b / c？ | 决定是否需要 migration；阻塞 §5/§6 定稿 |
| **4** | **§4.3**：`producer` 由 Producer 自述，还是 Consumer 计算？（建议 D-PP-8） | 决定是否需改 Papers + Frozen Contract |

> **`[ANALYSIS]` 最小可行收口顺序**：1 → 3 → 2 → 4。
> 第 1 项不收口，其余三项的设计都可能要重做。

---

*Recorded 2026-09-27. 本文件为 Implementation Plan（非授权），不含 `[OWNER DECISION]`，不产生代码/migration。*
