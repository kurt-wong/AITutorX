# IDENTITY-PROVENANCE-REVISION-01

**Document Type**: Revision / Correction Record（架构表述修正 + Owner 方向登记）
**Status**: `OPEN`
**Date**: 2026-09-27
**Corrects**: `IDENTITY-DOMAIN-DECISION-02.md` §4-§5 的 Seal 定位表述；`PRODUCER-PROVENANCE-DECISION-01.md` §3 PP-A 的首选地位
**Owner Ruling Direction recorded**: D-ID-1 / D-ID-2 / D-PP-1（方向已给；最终冻结文本待 Owner 签署）
**Authorization**: **无**。本文件不授权任何实现；DB persistence 保持暂停。

---

## 0. 本文件要修什么

上一轮我（DSH）在 `IDENTITY-DOMAIN-DECISION-02.md` §6 的 **D-PP-3 / PP-INT-1..3** 中，
把问题描述为「Primary Path 是否必须经过 V3 seal ingestion boundary」，
并列出「放宽 85 号 §5 边界以调用 `SealService`」作为候选。

**Owner 判定：该表述不准确，予以修正。**

修正的要点不是措辞，而是**架构分层**：

```text
Seal 不属于 Semantic Flow；Seal 属于 Identity Flow。
两个 Flow 必须明确分离。
```

---

## 1. 修正后的架构（权威表述）

### 1.1 Primary Path 原始架构**保持不变**

```text
Preprocessing Producer
        │
        ▼
Producer Artifact
(manifest + markdown + spans)
        │
        ▼
V3 Adapter
        │
        ▼
Semantic Question IR
        │
        ▼
Gate
        │
        ▼
Candidate
```

- preprocessing / `Papers` 仍然是 **Producer**
- V3 Adapter 仍然是 **Semantic Consumer**
- **Primary Path 不新增独立 Seal Pipeline**
- **不改变 Producer → Consumer 的边界设计**

### 1.2 两个 Flow 分离

**Semantic Flow**（负责 question meaning / option spans / resolved spans / semantic_status / IR / candidate）

```text
Producer ──▶ Adapter ──▶ IR ──▶ Gate ──▶ Candidate
```

**Identity Flow**（负责 document identity / source_version / hash / provenance / seal / replay）

```text
Producer Artifact ──▶ V3 Source Identity Layer ──▶ SourceVersion
```

### 1.3 两者汇合，职责不同

```text
                     Semantic Path

Preprocessing ──▶ Adapter ──▶ IR ──▶ Candidate


                     Identity Path

Preprocessing Artifact ──▶ Canonical Source Identity Creation ──▶ SourceVersion
```

最终：

```text
Producer Artifact
        │
        ├────────────────┬
        │                │
        ▼                ▼
Semantic Consumer    V3 Identity Layer
        │                │
        ├────────────────┘
        │
        ▼
     Candidate
```

---

## 2. 被修正的错误表述（明确禁止的两种误解）

### 2.1 错误 A —— Primary Path 缺少 Seal

```text
✗ 问题不是：Primary Path 缺少 Seal。
```

### 2.2 错误 B —— 在 Producer 与 Adapter 之间插入 Seal

```text
✗ 错误：
Preprocessing ──▶ New Seal Boundary ──▶ Adapter

✓ 正确：Semantic 与 Identity 是【并行】两条 Flow，不是串行插入一个 stage。
```

### 2.3 正确的问题陈述

> 当 Primary Path 进入 **persistence 阶段**、需要创建 `SourceVersion` 时，
> `runner.py` 当前**自行构造 Source Identity**，
> **绕过了 V3 已定义的 Identity / Seal 约束**。

即：缺的不是「一个 Seal stage」，而是「**Identity 创建权归属错误**」。

---

## 3. 对上一轮文档的具体更正（逐条）

| # | 原位置 | 原表述 | 更正 |
|---|---|---|---|
| 1 | `IDENTITY-DOMAIN-DECISION-02.md` §6 D-PP-3 / `PRODUCER-PROVENANCE-DECISION-01.md` §4 | 「Primary Path 是否强制经 `SealService`」+ PP-INT-1「放宽 85 号 §5 边界」 | **撤回该框架**。Identity Flow 与 Semantic Flow 并行；Primary Path 不新增 Seal Pipeline。85 号 §5「不改 `backend/app/`」边界**不需要放宽**——因为不需要在 semantic 路径上调用 `SealService` |
| 2 | 同 §4.1 | 「所有进入系统的 SourceVersion 必须经 `SealService.seal_document()`」（我据 `validate_seal_role_provider` 推断的设计意图） | 该推断**过度**。`SealService` 是 Identity Flow 的**一种**实现，不是 semantic 路径的必经关卡。正确要求是：**SourceVersion 的创建必须经 V3 的 canonical identity creation，而非 runner 自行构造** |
| 3 | `PRODUCER-PROVENANCE-DECISION-01.md` §3 表 | **PP-A（新增 `preprocessing ⟺ ppsv3`）为首选倾向** | **降级**。见 §5 |

> **`[ANALYSIS]`** 更正 1/2 有一个重要副作用：**Implementation 成本下降**。
> 不需要放宽既有边界，也不需要把 `SealService` 接进 semantic 路径——
> 只需要修正 **Identity Flow 内部**的身份构造与 provenance 承载。

---

## 4. Owner 方向登记（D-ID-1 / D-ID-2）

### 4.1 D-ID-1 — `original_sha256` 的域

**Owner 裁决方向**：

```text
original_sha256 = V3 ingestion received raw bytes SHA256
```

即：**`original_sha256` 不应保存 Producer hash。**

| 项 | 内容 |
|---|---|
| 理由 | SourceVersion 的 identity 属于 **V3 Source Layer** |
| Producer hash | `source_content_sha256` **作为 Producer provenance 独立保存** |
| 相等性 | **二者不得强制相等** |
| 与我上轮建议的关系 | ✅ 与我推荐的 **I-β** 一致 → 该建议**转为已裁决方向** |

⇒ `IDENTITY-DOMAIN-DECISION-02.md` §6 的 **I-A 作废**；**I-β 升为已定方向**。

### 4.2 D-ID-2 — `logical_execution_hash` 的唯一域

**Owner 要求重新检查**：

```text
当前风险：
  若 logical_execution_hash = content hash only
  则两个不同 document（Document A / Document B）
  若内容一致，可能共享同一个 SourceVersion  →  身份塌缩

需要确认：LE hash domain 是否包含 document identity？
```

**`[FACT]` 本轮已核实：风险成立，且机制已定位。** 见 §6。

---

## 5. Producer Provenance 修正（D-PP-1）

**Owner 判定**：

```text
不要新增 role=preprocessing / provider=ppsv3 作为第一选择。
```

**理由**：`role`/`provider` 属于 **V3 Source Identity Contract**；
**Producer provenance 不应污染 V3 ingestion identity。**

**推荐方向** —— 新增独立 provenance metadata：

```text
producer:
    name
    version
    artifact_hash
    manifest_hash
```

而不是塞进：

```text
role / provider
```

### 5.1 对上一轮 §3 选项表的处置

| 候选 | 上轮地位 | 本轮处置 |
|---|---|---|
| **PP-A** 新增 `preprocessing ⟺ ppsv3` | 首选倾向 | **降为末位**（污染 V3 identity 域；且需改 Frozen Spec） |
| **PP-B** 复用 `ocr_ppsv3 ⟺ ppsv3` | 次要 | **保留待议**（见 §5.2） |
| **PP-C** 复用 `canonical` | 次要 | **保留待议** |
| **PP-D** 保持 `native` | 已排除 | **仍然排除**（事实错误，见 PROVENANCE §2） |
| **PP-E（新）** role/provider 描述 **V3 ingestion 能力**；Producer 身份入独立 metadata | 未列 | **升为首选方向** |

### 5.2 `[OPEN]` PP-E 与 V3 枚举的一个未决冲突（必须显式登记）

PP-E 要求 `role/provider` 描述「V3 ingestion 能力」。但对 Primary Path：

- 若认为「V3 对 Producer 的 .md 做**本地确定性解析**」⇒ `native ⟺ native` 成立；
- 但 `role` 的 Spec 语义是「**产出该 L1 的解析引擎**」（`10 §4.2`），
  而该 L1 的产出引擎是 **preprocessing**，不是 V3 本地解析器。

⇒ **两者不可能同时为真。** 必须由 Owner 在下列二者中选一：

```text
PP-E-1  role 描述【产出 L1 的引擎】      → L1 由 preprocessing 产出 → 需要新 role 或复用 ocr_ppsv3
PP-E-2  role 描述【V3 ingestion 的能力】 → native 成立；但需明示这是对 Spec 语义的澄清/改写
```

**`[ANALYSIS]` 倾向**：PP-E-2 更符合本轮架构修正（Seal/Identity 属于 V3 Source Layer，
故 `role` 描述 V3 侧能力），但它**实质上是对 Frozen Spec `10 §4.2` 语义的重新解释**，
属 LEVEL 2，必须 Owner 明示裁定，不得由执行方默认。

> **不预判**：本文件只登记冲突。PP-E-1 / PP-E-2 为 `[OWNER DECISION]`。

---

## 6. D-ID-2 核实结果：跨文档身份塌缩（`[FACT]`）

### 6.1 LE hash 的实际构成

`app/core/hashing.py:65-82`：

```python
payload = {"task_type": …, "stage": …, "contract_domain": …, "input_domain": …}
return sha256_hex(payload)
```

Seal 路径（`seal.py:98-106`）：

```python
logical_execution_hash(
    task_type="document_ingest",
    stage="seal",
    contract_domain={"seal_contract_version": "seal/v1",
                     "parser": {"provider": provider, "role": role}},
    input_domain={"original_sha256": original_sha256},   # ← 无 document_id
)
```

Primary Path（`runner.py:86`）：`sha256_hex(f"seal:preprocessing:{file_sha}")`（**无** document_id）

⇒ **`input_domain` 与 `contract_domain` 均不含 `document_id`。**
⇒ **回答 Owner 的问题：LE hash domain 当前【不】包含 document identity。**

### 6.2 塌缩的确切机制（不止是「约束太宽」）

关键在**冲突后的 re-read 不带 document 过滤**：

| 环节 | 位置 | 是否带 `document_id` |
|---|---|---|
| UNIQUE 约束 | `source.py:52-57` / `0006:42-46`：`UNIQUE(logical_execution_stage, logical_execution_hash)` | ❌ 无 |
| INSERT `ON CONFLICT DO NOTHING` | `source_repository.py:110-113` | ❌ 无 |
| **冲突 re-read `_version_by_le`** | `source_repository.py:128-138` | ❌ **无**（只过滤 stage + hash） |
| seal 前置查询 `find_sealed_version_by_le` | `source_repository.py:211-220` | ✅ **有**（`document_id == …`） |

```text
Document B 写入 → le_hash 与 Document A 相同
  → INSERT ON CONFLICT DO NOTHING（静默跳过）
  → re-read：_version_by_le(stage, hash)   ← 无 document 过滤
  → 返回【Document A 的】SourceVersion 行
  → Document B 拿到 A 的 source_version_id
```

⇒ **Document B 的 semantic 消费（annotation / resolved spans / candidates）将挂在 Document A 的 SourceVersion 上。**
这是**真实身份损坏**，不是标注问题。

**`[ANALYSIS]` 第二个发现**：`SealService`（生产/Native 路径）也走同一条 `create_source_version`，
其**冲突 re-read 同样无 document 过滤**（`:118-121` → `:128-138`）。
即：seal 的**前置检查**是 document-scoped，但**并发冲突收敛**是 global-scoped —— 两者不一致。
⇒ 该缺陷不限于 Primary Path，是 **Identity Flow 的公共缺陷**。

**`[ANALYSIS]` 结论**：D-ID-2 的答案不是「给 UNIQUE 加一列」那么简单——
`ON CONFLICT` 的目标索引与 re-read 谓词**必须同步**，否则约束与收敛逻辑继续分叉。

---

## 7. Replay identity consistency（Owner 要求的检查项，`[FACT]`）

Owner 要求检查 **replay identity consistency**。本轮核实到一个**必须先裁定的阻断项**：

`le_hash` **包含 `contract_domain.parser = {provider, role}`**（`seal.py:103`）
与 `input_domain.original_sha256`（`seal.py:105`）。

⇒ 因此二者中**任何一个**改动，都会使 `le_hash` 变化。后果：

```text
已 sealed 的 version：le_hash_old = H(role=native, provider=native, sha=sha1)
修正 role/provider 后：le_hash_new = H(role=X, provider=Y, sha=sha2)
                        le_hash_new ≠ le_hash_old
```

⇒ **对同一份已 sealed 的文档重跑，不会幂等命中，而会创建一个【新的】SourceVersion。**
即：

- **replay 不会收敛**（同文档产生多个 sealed version）；
- 历史上任何「通过 primary path 落库」的数据，其身份在本轮修正后**无法原样重现**。

**`[ANALYSIS]`** 这把 §6 的 Stop Condition 从「暂停」升级为**不可逆风险**：

> 「第一次写库会永久固化 document identity / source version identity / provenance」
> —— 若在 `role`/`provider`/`original_sha256` 域未冻结前落库，
> 这些行的 `le_hash` **永久**绑定在一个即将被判定为错误的 contract_domain 上，
> 且因 `sealed` 后禁 UPDATE（`source_repository.py:143-147`）而**不可就地修正**。

`[OPEN]` 因此需新增裁决项：**已 sealed 行的 `le_hash` 迁移策略**（见下方 D-ID-6）。

---

## 8. 新增裁决项

| # | 问题 | 候选 | 备注 |
|---|---|---|---|
| **D-ID-6** | 修正 `role`/`provider`/`original_sha256` 域后，已 sealed 行的 `le_hash` 如何处置？ | 无数据（若 DB 从未跑过）/ 标记 legacy 保留 / 清库重跑 / 重建 sealed 行（需破坏 sealed 不可变） | 依赖 D-ID-5（DB 是否有行，当前 `[UNKNOWN]`） |
| **D-PP-6** | `role` 语义取 PP-E-1（产出 L1 的引擎）还是 PP-E-2（V3 ingestion 能力）？ | 见 §5.2 | **LEVEL 2**，涉及 Frozen Spec `10 §4.2` 语义 |
| **D-PP-7** | Producer provenance 的承载位置与字段集 | 独立 metadata（`producer{name,version,artifact_hash,manifest_hash}`，Owner 建议）/ 其它 | 需确认承载载体（`source_meta` JSONB 已是自由 JSONB，`10_DataModel.md:143`） |

> **注**：`source_meta` 在 `10_Data_Model.md:143` 定义为「提取配置、page_range、OCR 证据、`legacy` 标记」。
> 把 `producer{...}` 放入 `source_meta` **可能**无需 schema 变更——但这是**语义扩展**，
> 须 Owner 确认（`[OPEN]`），不得由执行方默认塞入。

---

## 9. 执行顺序（Owner 指定，取代上一轮 §7）

```text
Step 0   Identity Domain Decision                      ← 冻结 D-ID-1..6
   ↓
Step 1   Producer Provenance Decision                   ← 冻结 D-PP-1..7
   ↓
Step 2   Implement Identity Creation Path
   ↓
Step 3   Regenerate Primary Path Evidence Manifest
   ↓
Step 4   Isolated Test Database
   ↓
Step 5   Candidate Persistence Verification
   ↓
Step 6   Primary Path Reference Run Freeze
```

**当前状态：Step 0 未完成（D-ID-6 为新增项）。**

### 9.1 暂停项（Owner 明令，D-6）

在下列问题未明确前**禁止**：

```text
❌ Primary Path Reference Run
❌ candidate persistence
❌ production database write
```

理由（Owner 原文）：

> 第一次写库会永久固化 document identity / source version identity / provenance。
> 如果模型错误，后续修复成本高于当前。

我方新增的**技术佐证**见 §7：`sealed` 后禁 UPDATE + `le_hash` 含 `contract_domain.parser`
⇒ 落库后的身份错误**不可就地修正**。

---

## 10. 下一轮审查重点（Owner 指定）

**不再继续只验证**（已证明）：`IR ready` / `option spans` / `semantic_status`。

### 10.1 Identity correctness（本轮重点）

```text
[ ] SourceVersion 创建入口
[ ] original_sha256 来源
[ ] producer hash 保存位置
[ ] seal input domain
[ ] logical_execution_hash uniqueness
[ ] replay identity consistency
```

### 10.2 Semantic correctness（继续保持，但不与 Identity Flow 混合）

```text
[ ] option spans
[ ] resolved spans
[ ] IR readiness
```

**最终目标**：不是增加新的 Pipeline，而是确保

```text
Producer Artifact
        │
        ├────────────────┬
        │                │
        ▼                ▼
Semantic Consumer    V3 Identity Layer
        │                │
        ├────────────────┘
        │
        ▼
     Candidate
```

**Primary Path 架构保持不变，只补齐 persistence 阶段缺失的 identity governance。**

---

## 11. 本文件的状态

| 层 | 状态 |
|---|---|
| 架构表述（Seal ∈ Identity Flow） | ✅ **已修正**（本文件 §1-§3） |
| D-ID-1 方向 | ✅ Owner 已给方向（= I-β） |
| D-ID-2 核实 | ✅ 已核实，风险成立，机制已定位（§6） |
| D-PP-1 方向 | ✅ Owner 已给方向（PP-E：独立 producer metadata） |
| D-ID-6 / D-PP-6 / D-PP-7 | ❌ **新增待裁** |
| Step 0 冻结 | ❌ **未完成** |
| DB persistence | ⛔ **暂停**（Owner 明令） |
| 实现授权 | ❌ 无 |

---

*Recorded 2026-09-27. 本文件为 Revision / Correction Record，不含 `[OWNER DECISION]` 冻结文本，不授权任何实现。*
