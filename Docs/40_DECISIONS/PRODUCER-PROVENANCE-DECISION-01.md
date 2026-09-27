# PRODUCER-PROVENANCE-DECISION-01

> ## ⚠️ 已修正 — 阅读本文件前必须先读 `IDENTITY-PROVENANCE-REVISION-01.md`
>
> **本文件的两处结论已被 Owner 判定修正：**
>
> 1. **§3 的 PP-A（新增 `preprocessing ⟺ ppsv3`）降为末位。**
>    Owner 判定：`role`/`provider` 属于 **V3 Source Identity Contract**，
>    **Producer provenance 不应污染 V3 ingestion identity**。
>    首选方向改为 **PP-E**：新增**独立 provenance metadata**
>    （`producer{name, version, artifact_hash, manifest_hash}`）。
> 2. **§4（与 `SealService` 的冲突 / PP-INT-1..3）框架已撤回。**
>    正确架构：**Seal 属于 Identity Flow，不属于 Semantic Flow**；两 Flow 并行，
>    Primary Path **不新增 Seal Pipeline**，85 号 §5 边界**无需放宽**。
>
> **本文件仍然有效的部分**：§1 事实基、**§2「为何 `native` 是事实错误」**、
> §1.3 `role` 为 Frozen Spec 冻结枚举、§3 的 PP-B/C/D 分析、
> **§5 Execution Identity（LE hash 分叉 + 跨 runner 碰撞）**、§7 工单骨架、§8 回归护栏。
>
> **新增裁决项**：D-PP-6（`role` 语义取 PP-E-1 还是 PP-E-2）、D-PP-7（producer metadata 承载位置）见 REVISION-01 §8。

**Document Type**: Decision Record（Owner Decision Preparation）
**Status**: `OPEN` — 本文件**不含** `[OWNER DECISION]`，Owner 尚未裁决
**Date**: 2026-09-27
**Corrected by**: `IDENTITY-PROVENANCE-REVISION-01.md`
**Related**: `IDENTITY-DOMAIN-DECISION-02.md`（同批，Identity 面，**优先**）；`PERSISTENCE-BOUNDARY-DECISION-01.md` §Decision 3
**Label convention**: `[FACT]` / `[ANALYSIS]` / `[OPEN]` / `[OWNER DECISION]`

---

## 0. Purpose & Boundary

本文件冻结 **Producer Provenance 模型**的候选：即「一个 Source Version 是**谁**产生的」。

三个正交问题必须分开回答，混在一起是当前一切混乱的根源：

```text
Identity Domain   (IDENTITY-DOMAIN-DECISION-02)  ≙「它是不是同一个东西？」
Producer Provenance (本文件)                      ≙「它是谁产生的？」
Execution Identity (本文件 §5)                    ≙「哪一次执行产生了它？」
```

**本文件不做**：修改 Frozen Spec / Contract 正文；修改任何仓的工作树；授权 DB 运行；产生 `[OWNER DECISION]`。

---

## 1. 事实基础

### 1.1 Primary Path 的真实生产链（`[FACT]`，Owner 已澄清）

```text
PDF/DOC/DOCX/IMAGE
  → Papers（preprocessing，Source Producer）
  → manifest + annotated markdown + semantic metadata
  → V3 ingestion → Resolver → ResolvedRun → IR → Admission
```

`Papers` = preprocessing 项目文件夹（`kurt-wong/Aitutors-preprocessing`，本地 `D:\Project\Papers`，HEAD `969d39a`）。
`D:\Project\Aitutors-preprocessing`（无 `.git`）是**非版本化副本，不是权威树**。
→ `MIMO-TASK-GOV-BOUNDARY-PRIMARY-PREP-01.md:208-217`；`CURRENT_STATE.md:21,26`

**关键性质**：Papers 不只是「换个格式的 OCR」。它执行的是
**OCR + 结构恢复（section / unit / line range）+ 语义标注（prompt_version / unit_type）**。

### 1.2 代码现状（`[FACT]`）

| 观察 | 位置 |
|---|---|
| Primary Path 持久化时硬编码 `role="native"` / `provider="native"` | `runner.py:90-91`；`runner_b2.py:338-339` |
| 同一处 `artifact_kind="markdown"` | `runner.py:89`；`runner_b2.py:337` |
| `upload_meta={"source": "preprocessing_phase0"}`（**这是唯一如实记录了来源的字段**） | `runner.py:81`；`runner_b2.py:329` |
| Seal 路径的 provenance 通过 `contract_domain.parser={provider, role}` 进入 LE hash | `seal.py:98-106,128` |
| Consumer 不经 `SealService`，直接调 `create_source_version` | `runner.py:87-100`；`runner_b2.py:335-348` |
| **两个 runner 的事务语义不同**：`runner.py` 成功路径 `commit()`（`:293,:314`）、仅异常 `rollback()`（`:295,:316`）；**`runner_b2.py` 只有 `rollback()`（`:572`），成功路径不提交** | 见左列行号 |
| **但 `runner_b2` 确实做了真身份核对**（M1 声明值 → M2 raw bytes 实算 → M4 `verify_identity` → M5 gate） | `runner_b2.py:79-151` |

> **精确表述**：`runner_b2` **已经**证明「这份 .md 就是 manifest 声明的那份」。
> 本决策的问题**不是**「系统不知道身份」，而是：
> **系统已经算出了正确的身份，却仍把 `role/provider` 写成 `native`，并把另一个 hash 写入身份列。**
> 这使 §2 的错误更严重——它不是信息缺失，而是**已知事实被不一致地表达**。

### 1.3 `role` 是**冻结枚举**（`[FACT]` — 这是本决策的硬约束）

`AITutors-v3/Docs/V3_SPEC/10_Data_Model.md:136-137`：

```text
| role     | VARCHAR | native / ocr_ppsv3 / ocr_ppsvl / docx / canonical |
| provider | VARCHAR | native / ppsv3 / paddleocr-vl / docx             |
```

同文件 `:150-153`：

> **role/provider 封闭配对（BUG-V3-008 errata）**：`ocr_ppsv3 ⟺ ppsv3`、`ocr_ppsvl ⟺ paddleocr-vl`、
> `native ⟺ native`、`docx ⟺ docx`；`canonical` role 无 provider。禁止任意组合。
> `provider`/`role` 均进入 seal LE hash（contract_domain.parser），独立引擎必须独立身份，防 identity 漂移。

代码侧闭集实现在 `seal.py:39-44`：

```python
_SEAL_ROLE_PROVIDERS = {
    "native": {"native"},
    "ocr_ppsv3": {"ppsv3"},
    "ocr_ppsvl": {"paddleocr-vl"},
    "docx": {"docx"},
}
```

**`[ANALYSIS]` 由此得到一个不可回避的结论：**

> 「加一个 `preprocessing ⟺ ppsv3`」**不是**三行修改。
> 它要么**修改 Frozen Spec 的冻结枚举**，要么把 Primary Path 映射到枚举中**已有**的某个 role。
> 二者都是 LEVEL 2 架构边界动作，**必须 Owner 授权**。

这正是「不要直接选 A」的硬依据，而不是风格偏好。

### 1.4 `artifact_kind` 也被冻结（附带的同类违规）

`10_Data_Model.md:135`：`artifact_kind` = `original_binary / raw_l1 / canonical_l1`。

- 代码常量 `seal.py:36`：`_ARTIFACT_KIND = "raw_l1"` ✅ 合规。
- Consumer 传入：`runner.py:89` / `runner_b2.py:337`：`artifact_kind="markdown"` ❌ **不在闭集内**。

⇒ 与 `role` 同批裁决，避免二次返工。

---

## 2. 核心判定：为何 `native` 是**事实错误**而非**命名偏好**

`native` 在 Spec 中的语义（`10 §4.2` + `40_Development_Rules.md:55`「默认本地确定性 seal」）
= **V3 自身对 admitted artifact 的本地确定性解析**。

Primary Path 的实际语义 = **Papers 这一外部 producer 已经完成了 OCR 与结构恢复，V3 只是消费其产物**。

两者**不是同一个生产者**。因此：

```text
role="native"  ⇒ 声称：这份 raw_l1 由 V3 本地解析产生
实际情况        ⇒ 这份 raw_l1 由 Papers（preprocessing）产生
```

**`[ANALYSIS]` 后果**：

1. **provenance 失真**：DB 无法区分「V3 自己解析」与「preprocessing 生产」——违反 lineage 基本原则。
2. **LE identity 落错命名空间**：`role/provider` 进入 `contract_domain.parser`（`seal.py:103`），
   故身份**同时**标错。这不是「标签不影响功能」——它直接决定该 version 的 canonical identity。
3. **审计不可逆**：一旦 `3bf7a09` 路径写入 DB，事后无法从数据本身判断某行来自哪条路径。

> 用 Owner 的话：这不是普通 bug，而是「系统第一次进入真实数据生命周期后必然暴露的架构边界问题」。

---

## 3. `role` 维度：四个候选（待裁决）

| 候选 | 内容 | Spec 变更 | provenance 正确性 | 代价 |
|---|---|---|---|---|
| **PP-A** | 新增 `preprocessing` role ⟺ `ppsv3` provider | ❌ **需改 Frozen Spec 冻结枚举** | ✅ 如实 | 需 Owner 授权 + Spec errata + 闭集/测试同步 |
| **PP-B** | 复用 `ocr_ppsv3 ⟺ ppsv3` | ✅ 无需改 Spec | ⚠️ 部分正确：同 provider，但丢失「semantic preprocessing ≠ raw OCR」区分 | 最低；语义有损 |
| **PP-C** | 复用 `canonical` role（无 provider） | ✅ 枚举内已存在 | ⚠️ 需同时裁定 `artifact_kind=canonical_l1`；且该 role 不允许带 provider，与「Papers 是 provider」冲突 | 中；语义冲突待裁 |
| **PP-D** | 保持 `native` | ✅ | ❌ **事实错误** | 0（但不可接受） |

### `[ANALYSIS]` 倾向与理由

**倾向 PP-A**，理由：

- PP-B 会把两个语义上不同的生产阶段压成一个 role，未来无法区分
  「ppsv3 直接 OCR 出的 L1」与「ppsv3 结构恢复后的 L2」；
- PP-C 的 `canonical` 无 provider 规则与「需要记录 Papers 身份」直接冲突；
- PP-D 已被 §2 排除；
- 唯一诚实解是新增 role，**代价必须由 Owner 显式承担**，不能由执行 agent 静默完成。

**但 PP-A 有一个必须先解决的边界冲突**，见 §4。

> **不预判**：本文件只登记 `[ANALYSIS]`。PP-A/B/C 的最终选择为 `[OWNER DECISION]`，见 §7 `D-PP-1`。

---

## 4. ~~与 `SealService` 及 85 号边界的冲突~~ ❌ 框架已撤回

> **Owner 判定：本节的问题框架不准确，已由 `IDENTITY-PROVENANCE-REVISION-01.md` §1-§3 撤回。**
>
> - **正确架构**：`Seal` 属于 **Identity Flow**，不属于 Semantic Flow。两条 Flow **并行**。
> - **Primary Path 不新增 Seal Pipeline**，**不改变 Producer → Consumer 边界设计**。
> - 因此 §4.1 的「所有 SourceVersion 必须经 `SealService`」是**过度推断**；
>   85 号 §5「不改 `backend/app/`」边界**无需放宽**。
> - **问题不在「缺少 Seal stage」，而在**：Primary Path 进入 persistence、需要创建
>   `SourceVersion` 时，`runner.py` **自行构造 Source Identity**，
>   绕过了 V3 已定义的 Identity 约束 —— 即 **Identity 创建权归属错误**。
>
> **本节保留的内容仍然有效**（作为事实记录）：
> `validate_seal_role_provider`（`seal.py:47-56`）是封闭配对闸门，
> 且 Primary Path 绕过它 ⇒ `role="native"` 能静默写入。
> 但**修法**不是「把 SealService 接进 semantic 路径」，
> 而是**让 Identity 创建回到 V3 Identity Layer**（见 REVISION-01 §1.2）。

### 4.1 事实（保留）

- `seal.py:47-56` 的 `validate_seal_role_provider()` 是封闭配对闸门；
  `test_seal.py:106` 断言「seal 阶段不产 canonical」——说明该闸门**只服务于 seal 路径**。
- **现状**：Primary Path 绕过它，直接调 `create_source_version`
  （`runner.py:87-100`；`runner_b2.py:335-348`），**因此绕过了 `validate_seal_role_provider`**——
  这正是 `native` 这个非法语义值能静默写入的原因。
- `runner.py:9-13` 记录 85 号 §5 边界要求「**不改 backend/app/ 生产代码**」。
  ⇒ 该边界**保持有效**（无需放宽）。

### 4.2 ~~三条备选路径~~ ❌ 已撤回

| # | 原路径 | 处置 |
|---|---|---|
| **PP-INT-1** | Primary Path 调用 `SealService.seal_document()` | ❌ **撤回**——会把 Seal 错误地串入 semantic 路径 |
| **PP-INT-2** | 仅补调 `validate_seal_role_provider()` | ⚠️ 降为残余手段——治标（仍有两处 identity 构造实现） |
| **PP-INT-3** | 把 `le_hash` 计算与 role/provider 校验抽到共享权威函数 | ✅ **仍有效**——但定位改为「Identity Flow 内部收敛」，不是「跨 Flow 接线」 |

> **`[ANALYSIS]`** 撤回后 Implementation 成本**下降**：无需放宽边界、无需把 `SealService`
> 接入 semantic 路径；只需修正 **Identity Flow 内部** 的身份构造与 provenance 承载。

---

## 5. Execution Identity（LE hash）：一个独立且必须同批修的缺陷

### 5.1 `[FACT]`：同一执行却有两个不同身份

| 路径 | le_hash 公式 | 位置 |
|---|---|---|
| Native seal | `logical_execution_hash(task_type="document_ingest", stage="seal", contract_domain={seal_contract_version, parser:{provider,role}}, input_domain={original_sha256})` | `seal.py:98-106` |
| Primary consumer | `sha256_hex(f"seal:preprocessing:{file_sha}")` | `runner.py:86` |

⇒ **两者公式不同**。对同一份内容，两条路径产生不同 `logical_execution_hash`。

### 5.2 `[FACT]`：两个 runner 之间**完全相同** → 命名空间碰撞

`runner.py:86` 与 `runner_b2.py:334` 是**逐字相同**的表达式：

```python
le_hash = sha256_hex(f"seal:preprocessing:{file_sha}")
```

且两者 `logical_execution_stage="seal"`（`runner.py:98`；`runner_b2.py:346`）。

⇒ `document_source_versions` 的 `UNIQUE(logical_execution_stage, logical_execution_hash)`
（`app/models/source.py:52-57`）在 Track A 与 Track B2 之间**无法区分**，
`create_source_version` 的 `ON CONFLICT` 幂等路径（`source_repository.py:36-60`）会**把第二次静默收敛为既有行**。

### 5.3 与 Frozen Spec 的直接冲突

`10_Data_Model.md:152-153` 要求：

> **独立引擎必须独立身份，防 identity 漂移。**

而 §5.1 的同内容双公式、§5.2 的跨 runner 碰撞，**都是 identity 漂移的现实形态**。

⇒ **`[ANALYSIS]` 只改 role/provider 字符串不足以修复身份问题**：
`le_hash` 必须由**单一权威函数**产生，否则「改对了 role 但公式仍分叉」会在下一轮重现。

---

## 6. 必须由 Owner 裁决的事项

| # | 问题 | 候选 | 影响 |
|---|---|---|---|
| **D-PP-1** | Primary Path 的 `role`/`provider` 取什么？ | ~~PP-A 新增 `preprocessing`⟺`ppsv3`（已降为末位）~~ / **PP-E 独立 producer metadata＝Owner 已给方向** / PP-B 复用 `ocr_ppsv3` / PP-C 复用 `canonical` / PP-D 保持 native（排除） | **Owner 判定：role/provider 属 V3 Source Identity Contract，不被 Producer provenance 污染** |
| **D-PP-2** | `artifact_kind` 取什么？ | `raw_l1` / **`canonical_l1`（若选 PP-C 则须此值）** | 与 `10 §4.2` 闭集一致 |
| ~~**D-PP-3**~~ | ~~Primary Path 是否强制经 `SealService`？~~ | ~~PP-INT-1/2/3~~ | ❌ **框架已撤回**（Seal 属 Identity Flow，非 semantic 路径）——见 REVISION-01 §3 |
| **D-PP-4** | `le_hash` 是否收敛为唯一权威公式？ | **是（推荐，前置）** / 否（接受两条公式长期并存） | 防 identity 漂移；**且 §7 replay 分析显示：改动 `role`/`provider` 会使已 sealed 行无法重现** |
| **D-PP-5** | Papers 侧是否需要声明 `producer` 身份（让 producer 自述，而非 consumer 猜） | **是（Owner 方向：独立 metadata）** / 否 | 影响 Contract v0.2 是否需 errata；影响是否改动 Papers 工作树 |
| **D-PP-6（新增）** | `role` 语义取 **PP-E-1**（产出 L1 的引擎）还是 **PP-E-2**（V3 ingestion 能力）？ | 见 REVISION-01 §5.2 | **LEVEL 2**，涉及 Frozen Spec `10 §4.2` 语义解释 |
| **D-PP-7（新增）** | Producer provenance（`producer{name,version,artifact_hash,manifest_hash}`）承载在何处？ | `source_meta` JSONB（可能零 schema 变更，但属语义扩展）/ 新列 / 新表 | 决定是否需 migration |

> **`D-PP-1` 与 `D-ID-1` 的依赖**：Identity 域决定 `original_sha256` 写什么字节；
> Provenance 决定 `role/provider` 写什么值。**二者共同决定 `le_hash` 的 `input_domain` 与 `contract_domain`**，
> 故必须**同批**冻结，不可先后分叉实施。
>
> **`le_hash` 的第三重依赖（本轮新增）**：因 `le_hash` 含 `contract_domain.parser`，
> 一旦 `role`/`provider` 定案，**已 sealed 行的 `le_hash` 即不可再变**（`sealed` 后禁 UPDATE）。
> ⇒ 这使 D-PP-1 / D-PP-4 从「命名选择」升级为**不可逆的持久化决策**。见 REVISION-01 §7、D-ID-6。

---

## 7. 执行工单（**非授权**，仅登记范围）

> ⚠️ 本工单在 `D-ID-1..6` 与 `D-PP-1..7` 全部裁决之前**不得开工**。
> 开工需要独立 Owner 授权（Gate 2），本文件不构成授权。
> **执行顺序以 `IDENTITY-PROVENANCE-REVISION-01.md` §9 为准（Step 0 → Step 6）。
> Step 0/1 未完成前，DB persistence 保持暂停（Owner 明令）。**

```text
BUG / DESIGN ISSUE
  Primary Path persistence opened before provenance closure

EVIDENCE
  AITutors-v3/backend/scripts/preprocessing_consumer/runner.py:74,78,86,89-91,98
  AITutors-v3/backend/scripts/preprocessing_consumer/runner_b2.py:322,326,334,337-339,346
  AITutors-v3/backend/app/domains/source/seal.py:39-44,83,98-106
  AITutors-v3/backend/app/models/source.py:52-57,65
  AITutors-v3/Docs/V3_SPEC/10_Data_Model.md:135,136,137,150-153
  AITutor-X/Docs/50_OPERATIONS/CURRENT_STATE.md:39,63

FORBIDDEN
  - 不得只把 "native" 字符串改成 "preprocessing"/"ppsv3" 即收工
  - 不得继续在持久化路径重算 hash 而丢弃 runner_b2 M2 已核对的值
  - 不得修改 Frozen Spec / Contract 正文（Spec 修订须独立 Owner 授权）
  - 不得修改测试断言以使其通过
  - 不得运行 DB 落库 / Primary Path Reference Run / candidate persistence
    （Owner 明令暂停；见 REVISION-01 §9.1）
  - 不得放宽 runner.py:9-13 记录的 85 号 §5 边界
  - 不得在 Primary Path 的 semantic 路径上新增 Seal stage
    （Seal 属 Identity Flow；两 Flow 并行 —— REVISION-01 §1-§3）
  - 不得把 Producer provenance 塞进 role / provider
    （role/provider 属 V3 Source Identity Contract —— REVISION-01 §5）

REQUIRED (order)
  EXEC-0（可立即做，零语义风险）
    变量名纠错：runner.py / runner_b2.py 内 file_sha → body_text_sha256
    （当前名与 10 §4.1 原始文件 sha 语义冲突，是 M2/M3 的直接诱因）
    ⚠️ 该改名会使 test_x26_frb01 / test_x26_fint08 的**源码文本断言**需同步核对
       （见 §8 约束），必须与测试同批提交

  EXEC-1  Owner Decision 应用（D-ID-1 已定方向 / D-ID-2 / D-PP-1 已定方向 / D-PP-2 / D-PP-6 / D-PP-7）

  EXEC-2  【关键】消除「正确身份已算出却被丢弃」：
    runner_b2 的 M2 已经算出 `computed_sha = SHA256(raw source bytes)`
    （runner_b2.py:118-121，经 load_raw_bytes_identity），M4 已证明它 == manifest 声明值。
    持久化路径必须**复用这个已核对的值**，而不是在 _create_source_records 内
    用 `sha256_hex(body_text)` 重算另一个值。
    ⇒ 这是 I-β（D-ID-1，Owner 已给方向）的最低成本实现：
      不需要新算法，只需要不再丢弃已有结果。

  EXEC-3  le_hash 收敛为单一权威函数（D-PP-4）
          ⚠️ 并须处理 D-ID-2 的塌缩：LE hash domain 是否含 document identity，
             以及 ON CONFLICT 目标索引与 _version_by_le re-read 谓词必须【同步】修改
             （source_repository.py:110-113 与 :128-138；当前 re-read 无 document 过滤）
  EXEC-4  Identity Flow 内的身份创建收敛（原 D-PP-3，框架已修正）
  EXEC-5  Producer provenance 独立 metadata 承载（D-PP-7；owner 建议字段集
          producer{name, version, artifact_hash, manifest_hash}）
  EXEC-6  provenance 回归测试（新增，不得只改旧断言）
  EXEC-7  历史数据与已 sealed 行处置（D-ID-5 + **D-ID-6**，仅在确认 DB 有行时；
          注意 sealed 后禁 UPDATE ⇒ le_hash 不可就地修正，见 REVISION-01 §7）
```

---

## 8. 实施期硬约束（回归护栏，`[FACT]`）

以下测试对 runner **源码文本 / AST** 做断言，重构必须保持其不变量，不得以改断言方式绕过：

| 测试 | 断言 | 位置 |
|---|---|---|
| `test_both_runtime_runners_call_the_single_entry_point` | 两个 runner 源码中必须出现 `enforce_interface_scope` | `test_x26_fint08_interface_scope.py:461-467` |
| `test_interface_scope_gate_runs_before_gate_service_in_runner` | runner.py 中 `scope = enforce_interface_scope(` 的索引 **<** `ta = await _track_a(` | 同上 `:488-491` |
| `test_interface_scope_gate_runs_before_semantic_consumption_in_runner_b2` | runner_b2.py 中边界闸门先于 `_run_full_chain` | 同上 `:481-486` |
| `test_normalize_interface_identity_has_one_production_call_site` | 全 `scripts/` 中 `normalize_interface_identity(` 仅 **1** 处调用，且在 `boundary.py` | 同上 `:469-479` |
| `test_runners_contain_no_identity_version_comparison` | AST：两个 runner 内**零**处对 `identity_version` 的比较 | `test_x26_frb01_identity_version_types.py:534-551` |
| `test_membership_rule_constant_lives_only_in_boundary` | `_INTERFACE_IDENTITY_VERSIONS` 不得出现在 boundary.py 之外 | 同上 `:553-561` |
| `test_malformed_form_is_judged_only_inside_normalize` | `MALFORMED_IDENTITY_VERSION` 不得出现在两个 runner 内 | 同上 `:563-575` |

**`[ANALYSIS]` 含义**：

1. 重构**不得**移除或移动 `enforce_interface_scope` 调用（否则 §8 第 1/2/3 条失败）；
2. 若 EXEC-2/EXEC-3 需要比较身份值，**不得**在 runner 内新增 `identity_version` 比较（第 5 条失败）；
3. **「对字节现算 SHA-256」不构成 identity 判定**，不违反第 4/5 条——
   但这必须在实现说明中显式写明，避免被误判为平行权威。

**`[FACT]` 对抗核验补充（2026-09-27，独立只读复核）**：

- **现有测试不会因 EXEC-4 而失败**：两个测试文件中 `_create_source_records` 全 4 处引用均为
  `patch` 且断言 `call_count == 0`（`fint08:348-350,394-398`；`frb01:400-402,450-454`）；
  且所有真实 `_run_full_chain` 调用都以 `gate="BLOCK"` 在 `runner_b2.py:383-387` 提前返回，
  故函数体从未执行；两文件均**不**断言 `artifact_kind`/`role`/`provider`/`original_sha256`/`le_hash`。
  ⇒ **唯一破坏模式是 import-time failure**（两测试模块在 module scope 导入 runner：`fint08:72-76`；`frb01:54-55`）。
  ⇒ **含意**：现有护栏**不覆盖**本次修改的行为面。EXEC-6 必须**新增**断言，
  **不得**以「测试全绿」证明 provenance 已修好。
- **第 5 条是纯语法断言，可被绕过**：AST 测试只检查 `ast.Compare` 的源码片段是否含
  `identity_version` 字样，故 `v = manifest.identity_version` 后再比较即可规避。
  ⇒ 不得以「测试通过」替代 §7 FORBIDDEN 的实质约束。

---

## 9. 与 Identity 决策的合并视图

| 层 | 状态 | 依据 |
|---|---|---|
| 文档治理 | ✅ 完成 | `AITUTORX-DOC-GOVERNANCE.md` |
| Producer option spans | ✅ 完成 | `CURRENT_STATE.md:37`（Papers `969d39a`） |
| Semantic IR / Gate 逻辑 | ✅ 基本完成 | `CURRENT_STATE.md:38` |
| **Semantic Flow 定位** | ✅ 已澄清（与 Identity Flow 并行） | `IDENTITY-PROVENANCE-REVISION-01.md` §1-§3 |
| Persistence 代码 | ⚠️ **已打开，身份模型未冻结** | `CURRENT_STATE.md:39` + 本文件 §1.2 |
| Identity Domain | 🟡 **方向已给**（D-ID-1 = I-β）；D-ID-2 已核实塌缩；D-ID-6 新增待裁 | `IDENTITY-DOMAIN-DECISION-02.md` §7 |
| Producer Provenance | 🟡 **方向已给**（PP-E 独立 metadata）；D-PP-6/7 待裁 | 本文件 §6 |
| DB 闭环 | ⛔ **暂停**（Owner 明令） | REVISION-01 §9.1 + Identity §8 |

```text
当前最重要的一句话：

  不要急着证明 Primary Path 能落库，
  先确保落库后的数据未来十年还能解释「它从哪里来」。
```

---

*Recorded 2026-09-27. 本文件为 Decision Preparation，非 Verification / Closure / Audit，不含 `[OWNER DECISION]`。*
