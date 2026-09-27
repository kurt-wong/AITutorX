# IDENTITY-DOMAIN-DECISION-02

> ## ⚠️ 已修正 — 阅读本文件前必须先读 `IDENTITY-PROVENANCE-REVISION-01.md`
>
> **本文件的两处表述已被 Owner 判定为不准确，由 `IDENTITY-PROVENANCE-REVISION-01.md` 修正：**
>
> 1. **§6 的 D-PP-3 / PP-INT-1..3（「Primary Path 是否强制经 `SealService`」）已撤回。**
>    正确架构：**Seal 属于 Identity Flow，不属于 Semantic Flow**；两条 Flow **并行**，
>    Primary Path **不新增 Seal Pipeline**，85 号 §5 边界**无需放宽**。
> 2. **§6 的 I-A（强制 `original_sha256 == source_content_sha256`）已作废**；
>    Owner 已给裁决方向 = **I-β**（`original_sha256` = V3 ingestion received raw bytes SHA256）。
>
> **本文件仍然有效的部分**：§1 审计背景、§2 对 PBD-01 的三处更正、§3 事实基、
> §4「PBD-01 的 A/B/C 基于错误前提」的核心判定、§5.2.1 规范违反、**§5.2.2 跨文档身份塌缩**、
> §7 裁决清单（D-ID-1 已定方向；**新增 D-ID-6**）。
>
> **新增裁决项**：D-ID-6（已 sealed 行的 `le_hash` 迁移策略）见 REVISION-01 §8。

**Document Type**: Decision Record（Owner Decision Preparation）
**Status**: `OPEN` — 本文件**不含** `[OWNER DECISION]`，Owner 尚未裁决
**Date**: 2026-09-27
**Supersedes（option framing only）**: `PERSISTENCE-BOUNDARY-DECISION-01.md` §Decision 1 的 A/B/C 选项目框架
**Corrected by**: `IDENTITY-PROVENANCE-REVISION-01.md`
**Related**: `PRODUCER-PROVENANCE-DECISION-01.md`（同批，Provenance 面）；`PERSISTENCE-BOUNDARY-DECISION-01.md`（D2/D3 仍有效）
**Label convention**: `[FACT]` / `[ANALYSIS]` / `[OPEN]` / `[OWNER DECISION]`

---

## 0. Purpose & Boundary

本文件把「Primary Path 落库身份」从**标签问题**重新定位为**架构边界问题**，并冻结 **Identity Domain**（身份域）的候选模型，供 Owner 裁决。

**本文件不做**：

- 不修改 Frozen Spec / Frozen Contract 任何正文
- 不修改 `AITutors-v3` / `Papers` 工作树（0 代码改动）
- 不授权 DB 运行
- 不自行产生 `[OWNER DECISION]`
- 不新建编号体系 / Registry / Gate / 审批流程

**诊断结论（一句话）**：

> 当前 Primary Path 的 persistence **不是**标错了 `role/provider` 字符串，
> 而是**在身份域模型冻结之前就已经打开了落库开关**（`3bf7a09`）。

---

## 1. 审计背景（本次为何重开 D1）

| 轮次 | 结论 | 性质 |
|---|---|---|
| 上一轮 | 「Primary Path 的 `role="native"` / `provider="native"` 是标签问题，改字符串即可」 | `[FACT]` 但**不充分** |
| 本轮审计 | 该字符串同时进入 **seal LE identity**（`seal.py:98-106` 的 `contract_domain.parser`），因此它不是标签，而是**身份输入** | 架构边界问题 |

`10_Data_Model.md:152-153` `[FACT]`：

> `provider`/`role` 均进入 seal LE hash（contract_domain.parser），**独立引擎必须独立身份，防 identity 漂移**。

→ 改 `native` 的动作**必然**改变该 Source Version 的 canonical identity。
→ 因此这个改动**不能**与身份域裁决分离执行。

---

## 2. 对 `PERSISTENCE-BOUNDARY-DECISION-01` 的更正（必须先读）

`PERSISTENCE-BOUNDARY-DECISION-01.md` 事实基础扎实，其 FACT 1.1–1.5 与 Implications 至今成立。
但有 **3 处**必须在裁决前更正/升级，否则会基于过期前提决策：

| # | 位置 | 原文 | 更正 | 依据 |
|---|---|---|---|---|
| 1 | §Current State「FACT — NOT STARTED」 | 「Persistence consumption … `finally: await session.rollback()` — 事务内校验后回滚」 | **已过期**。`runner.py:293/314` 成功路径为 `await session.commit()`，`rollback()` 只在 `except` 分支。落库**已开启** | `runner.py:290-297`、`:311-318`；`CURRENT_STATE.md:39` |
| 2 | §Decision 3 FACT 3.2 | 「但一切被 rollback … `runner.py:296` `finally: await session.rollback()`」 | **同上，已过期**。`296` / `317` 行现为异常分支 | 同上 |
| 3 | §Decision 1 §Implications | 「无论选哪个选项，当前 `runner.py:74` 的 `file_sha = sha256_hex(body_text)` 与 Contract 的 `SHA256(raw bytes)` 语义不符，**需修正**」 | **成立且升级**：该行的**变量名 `file_sha` 本身即错误标注**（它不是 file sha，是 body_text sha）。此点已由 `CURRENT_STATE.md:63` 登记为 OPEN，但尚未进入任何裁决 | `CURRENT_STATE.md:63` |

**`[ANALYSIS]`** 第 1/2 条更正改变的是**紧迫性**而非结论：
Persistence 已打开 ⇒ 每多跑一次 DB，就多写入一批身份未冻结的数据 ⇒ 这就是「Step 0 必须先裁」的直接理由。

**处理方式**：本文件**不修改** `PERSISTENCE-BOUNDARY-DECISION-01.md` 正文（保留其历史审计轨迹），
改为在本文件 §2 显式标注差异，并由 Owner 决定是否回改原文。

---

## 3. 外部知识基（`[FACT]`，逐条可核对）

### 3.1 权威定义

| 来源 | 定义 | 位置 |
|---|---|---|
| Frozen Contract v0.2 §1.2 | `source_content_sha256` = 源 **OCR markdown 文件原始字节**的 SHA-256，64 小写 hex | `AITutors-v3/Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ `f4941ff` |
| Frozen Contract v0.2 §1.2 | OCR 清单 `source_sha256` 钉的是 **PDF 字节**；两者语义不同，**不可混用** | 同上 |
| Frozen Spec `10 §4.1` | `documents.original_sha256` = 「原始文件 SHA256（01 v0.3 决策 4）」 | `AITutors-v3/Docs/V3_SPEC/10_Data_Model.md:117` |
| Frozen Spec `30 §…` | `[FACT]` 「同一 `original_sha256` 允许多 sealed version 跨 role/provider；**非原始文件 hash 全局唯一**」 | `AITutors-v3/Docs/V3_SPEC/30_Task_LLM_Safety.md:400` |
| 冲突台账 `CL-23` | 「Producer sha vs V3 `original_sha256`」— **不暗示必须相等**；对账 OPEN | `AITutor-X/Docs/40_DECISIONS/X2.5-05-CONFLICT-LEDGER.md:38` |

### 3.2 代码实际形态（`[FACT]`）

| 观察 | 位置 |
|---|---|
| Seal（Fallback/Native Path）持久路径：`original_sha256 = hashlib.sha256(file_bytes).hexdigest()`（**artifact 原始字节**） | `app/domains/source/seal.py:83` |
| Consumer（Primary Path）持久路径：`file_sha = sha256_hex(body_text)`（**joined line text**），随后 `original_sha256=file_sha` | `scripts/preprocessing_consumer/runner.py:74,78`；`runner_b2.py:322,326` |
| Manifest 声明的 `source_content_sha256` 被解析、被校验（`boundary.normalize_interface_identity`） | `manifest_reader.py:136`；`boundary.py:204-266` |
| **`runner_b2` 已做真身份核对**：M1 读 manifest 声明值 → M2 `load_raw_bytes_identity(source_path)` 对 raw bytes 实算 → M4 `verify_identity(computed_sha, manifest_sha, ir_sha)` → M5 gate | `runner_b2.py:79-151`（尤其 `:110,120-121,146-148`） |
| **但核对结果只决定 accept/block，该 SHA 值从未进入任何 `create_document` / `create_source_version` 调用** | `runner_b2.py:313-348` 自算 `file_sha = sha256_hex(body_text)`；`runner.py:64-100,262-280` 仅取 `scope.accepted` / `scope.code` / `scope.reason` |
| `body_hash` = `SHA256(normalized body_text)`，**已是独立列** | `10_Data_Model.md:140`；`app/models/source.py:67` |
| `parent_version_id` 已在 schema 与 repository 签名中存在 | `app/models/source.py:65`；`app/repositories/source_repository.py:77,97` |
| **`parent_version_id` 是死字段：全后端无任何调用点写入过它** | `grep parent_version_id` → 仅上列 3 处（定义/签名/透传），零写入 |

> **精确表述（勿误读为「完全没校验」）**：核对**已存在**，缺的是**核对结果与持久化身份的绑定**。
> 即：系统**知道**真正的身份是什么，却把**另一个值**写进了 `documents.original_sha256`。

**`[FACT]` 更准确的形式是「双向不核对」**（独立只读复核，2026-09-27）：

```text
声明的 digest   →  从未与【实际存储的】digest 核对
存储的 digest   →  从未与【声明的】digest 核对
```

- `runner_b2` 的 M1–M5 核对的是 `SHA256(raw bytes)` ↔ `manifest 声明值` ↔ IR 值
  （`runner_b2.py:110,120-121,136-148`；`identity_verifier.py:98-118`），
  **`file_sha`（即真正写入 `original_sha256` 的值）不在其中任何一侧**。
- 全仓范围内，manifest 声明值作为 hash 值被使用的地方只有两类：
  上述核对，以及 `enforce_interface_scope` 的**格式**校验（`boundary.py:229-236`）。
  **没有任何持久化路径使用它**。
- annotation payload 亦不含任何 sha（`annotation_adapter.py` 无 `sha256` / `source_content_sha256`）；
  `AdmissionCandidate.input_identity` 仅 `{"source": "preprocessing_manifest"}`（`runner_b2.py:461`）。

⇒ **身份事实在进入 DB 的那一刻被替换成一个从未被核对过的值**，且两个值之间无任何关联记录。

---

## 4. 核心判定：为什么 PBD-01 的 A/B/C **全部**基于一个错误前提

`PERSISTENCE-BOUNDARY-DECISION-01` §Decision 1 把问题设为：

> `original_sha256` 与 `source_content_sha256` **如何共存**？A 统一 / B 双 domain / C identity+lineage

三个选项共享同一隐含前提：

```text
source_content_sha256  与  original_sha256  是【同一个东西的两个候选写法】
```

**`[ANALYSIS]` 该前提不成立。** 它们是两个**语义上不可比**的量：

| | `source_content_sha256` | `documents.original_sha256` |
|---|---|---|
| 输入字节 | Producer 的 **.md raw bytes** | V3 **自身接收到的 artifact 字节** |
| 生产者 | Papers（preprocessing） | V3（seal / ingest） |
| 作用域 | **跨系统**绑定键 | **V3 内部** `documents` 主档键 |
| 权威 | Frozen Contract §1.2 | Frozen Spec `10 §4.1` |

两者**只有在一种特定情况下**才应相等：V3 接收到的 artifact 恰好就是 Producer 的那份 .md 字节（即 Primary Path）。
在 Fallback/Native Path 下 V3 收到的是 PDF/DOCX，**此时两者相等在物理上不可能**。

⇒ 把问题写成「如何共存 / 是否统一」，等于要求一个**在一条路径上无解**的等式。
⇒ 正确的问题不是「两者如何相等」，而是「**系统内实际存在几个身份域，各自叫什么名字、各自回答什么问题**」。

**这就是本次审计把「标签问题」升级为「架构边界问题」的准确含义。**

---

## 5. Identity Domain 模型（候选，待冻结）

### 5.1 实际存在的四个域（`[FACT]`）

```text
Papers:   PDF bytes ──sha_PDF──┐
                               │        (I-0)
          .md bytes ──sha_MD───┤──────► manifest.source_content_sha256   ← 跨系统绑定键
                               │
V3:       receive bytes ───────┘
              │
              ├──► documents.original_sha256        (I-1)  原始文件身份
              │
              └──► document_source_versions
                        ├── body_hash   = SHA256(normalized body_text)   (I-2)  规范内容身份
                        └── logical_execution_hash = f(contract_domain.input_domain) (I-3) 执行身份
```

| ID | 域名 | 公式（现状） | 回答的问题 | 现存位置 |
|---|---|---|---|---|
| **I-0** | Producer 原始字节域 | `SHA256(.md raw bytes)` | 「Producer 产物是哪一个？」 | manifest `source_content_sha256`（**未落库**） |
| **I-0'** | Producer 上游字节域 | `SHA256(PDF bytes)` | 「上游原始 PDF 是哪一个？」 | Papers OCR 清单 `source_sha256`（不跨系统） |
| **I-1** | admitted artifact 字节域 | `SHA256(artifact bytes)` | 「V3 接收的原始文件是哪一个？」 | `documents.original_sha256` |
| **I-2** | 规范内容域 | `SHA256(normalized body_text)` | 「归一化正文是否同一份？」 | `document_source_versions.body_hash` |
| **I-3** | 执行身份域 | `LE_hash(contract+input)` | 「这个 Source Version 由哪次执行产生？」 | `logical_execution_stage` + `logical_execution_hash` |

**不变量（本文件主张）**：

```text
1. 每个域必须全限定命名（I-0 / I-1 / I-2 / I-3），禁止裸用 sha / hash / file_sha。
2. 跨域【禁止】直接比较、禁止要求相等、禁止互相替代 dedup。
3. I-3 的 contract_domain 必须包含生产该 version 的 parser 身份（role/provider）。
4. I-1 必须由 V3 对【V3 自己接收到的字节】现算，不得接受外部传入值作为唯一依据。
5. path 永远只是 locator，不得充当任何域的身份（DEC-031 原则 1）。
```

### 5.1.1 为何 I-0 与 I-2 **结构上**不可能相等（`[FACT]`）

`source_loader.load_source_lines()` 的读取路径是**有损**的：

```python
text  = source_path.read_text(encoding="utf-8")   # BOM 被剥离；CRLF→LF
lines = text.splitlines()                          # 丢弃行尾换行符
# body_text = "\n".join(l.text for l in lines)     # 重新用 \n 拼接
```

⇒ `body_text` 丢失了三类原始字节信息：

| 丢失项 | 后果 |
|---|---|
| BOM | `SHA256(raw bytes)` ≠ `SHA256(body_text)` |
| CRLF / CR 行尾 | 同上 |
| 文件末尾换行符 / 尾随空行 | 同上 |

**`[ANALYSIS]`**：因此「让 `original_sha256 == source_content_sha256`」（I-A）**不是**一个
「改一行代码」的选项——它要求 consumer 停止使用 line-index 重建的 `body_text` 作为身份来源，
改为直接对 raw bytes 现算。这**再次证明** PBD-01 把 D1 描述为「两者如何共存」是错误的问题框定：

> 它们相等**不是**一个配置选择，而是一个**读取路径**选择。

**且该读取路径的选择在代码库中已有明文答案**：`raw_bytes_identity.py:7-16` 要求
「Identity 来源唯一：SHA256(raw bytes)」，并**点名禁止** `read_text()` / `splitlines()` / `sha256_hex`。
⇒ **I-β 不是新设计，而是让 persistence 服从既有规范。** 这是它「实施代价最小」的根据。

### 5.1.2 `body_text` 必然携带规范化损失（派生自 5.1.1）

即使 consumer 改为对 bytes 现算 I-1，`body_text`（I-2）与原始文件仍是**两个不同对象**。
故 I-1 与 I-2 **必须并存**，不可合并。这正是 I-β+ 建议保留 I-0 lineage 的技术理由。

### 5.2 现行三条实际混用（`[FACT]` — 缺陷，非主张）

| # | 混用 | 证据 | 后果 |
|---|---|---|---|
| **M1** | **I-0 声明后未落到身份载体**：manifest 的 `source_content_sha256` 被解析、被核对（`runner_b2` M1–M5），但核对结果**不进入任何身份列**；持久化另算一个值 | `runner_b2.py:79-151`（核对）vs `:313-348`（持久化）；`runner.py` 同构无核对绑定 | 跨系统绑定键在消费侧不生效；身份在 `documents` 处断裂 |
| **M2** | **I-1 被 I-2 顶替**：`documents.original_sha256` 写入的是 `SHA256(body_text)` | `runner.py:74,78`；`runner_b2.py:322,326` | 列名/规格（`10 §4.1`「原始文件 SHA256」）与实际语义不符 |
| **M3** | **同一 artifact 两条写路径算法不同**：seal 用 `sha256(file_bytes)`，consumer 用 `sha256_hex(body_text)` | `seal.py:83` vs `runner.py:74`；`runner_b2.py:322` | 同一份 .md 走 Native seal 与走 Primary consumer，得到**两个不同 Document** ⇒ `UNIQUE(original_sha256)` 失效 |

### 5.2.1 M2 的真实严重度：不只是「域不对」，而是**用了被明令禁止的 hash 族**（`[FACT]`）

`runner.py:74` 的 `sha256_hex` **不是**「SHA-256 of text」。它是：

```python
def sha256_hex(obj): return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()
# canonical_json = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",",":"))
```

⇒ 对 `body_text` 实际计算的是 **JSON 引号包裹并转义后**的字节的 SHA-256
（`{"..."}` 形态 → 首尾带 `"`、内部 `\n` 被转义为 `\\n`）。
它**既不是** I-0（raw bytes），**也不是** I-2（`body_hash = SHA256(plain joined text)`，`source_loader.py:43-46`）。

而代码库中对此有**明文禁止**——`app/core/raw_bytes_identity.py:7-16`：

```text
身份语义：
- Identity 来源唯一：SHA256(raw bytes)。raw bytes = file.read_bytes() 的精确字节序列。
- CRLF / BOM / trailing newline / unicode 多字节字符全部保真。
- path 是 locator，不是 identity（DEC-031 原则 1）。

禁止（防回归）：
- read_text() / splitlines() / strip() — 会丢字节信息（FACT-031）
- app.core.hashing.sha256_hex — canonical_json wrap，V3 logical identity primitive
- 任何 text normalization — 源字节不经规范化
```

**`[ANALYSIS]` 结论**：

> `runner.py` 的持久化路径**同时违反该清单的第 1、2、3 条**：
> 用 `load_source_lines()`（内部 `read_text()` + `splitlines()`）取字节、
> 用 `sha256_hex()` 算身份、并对文本做了规范化。
>
> 这不是「设计尚未决定」，而是**系统已经写下了正确答案，却在另一条路径上违反了它**。
> 因此本决策的很大一部分**不是新增设计，而是让 persistence 服从已有规范**。
> 这显著降低了 EXEC-2 的风险：**正确实现已存在**（`load_raw_bytes_identity()`，`runner_b2.py:120`）。

### 5.2.2 `[FACT]` 附带发现：跨文档身份塌缩（比 M1–M3 更危险）

`le_hash = sha256_hex(f"seal:preprocessing:{file_sha}")`（`runner.py:86`）的输入**只有正文文本**，
**不含** `document_id` / `role` / `provider` / path / file_name。

配合：

- `UNIQUE(logical_execution_stage, logical_execution_hash)`（`app/models/source.py:52-57`）
- `create_source_version` 的 `ON CONFLICT DO NOTHING` + 按 (stage, hash) 重读
  （`source_repository.py:110-112,128-138`，**不带 document 过滤**）

⇒ **两份内容相同的不同文档，第二次写入会静默复用第一份的 version 行**（跨文档 identity 塌缩）。
同一原因使 `runner.py` 自身的 Track A 与 Track B 相互碰撞（§5.2）。

**`[ANALYSIS]`** 这是 identity 设计缺陷的**可数据损坏形态**，优先级应高于 `role/provider` 标签本身。
它同时构成 `D-ID-1` 必须前置的独立理由：**在 le_hash 收敛（EXEC-3）之前不得开启 DB 落库。**

**M1 + M3 的组合后果**（这是「未来十年无法解释它从哪来」的具体形态）：

```text
同一个 PDF
  ├─ 经 Primary Path  → document(id=1).original_sha256 = SHA256(body_text)
  └─ 经 Native  seal  → document(id=2).original_sha256 = SHA256(pdf_bytes)

系统判定：两个不同 Document   ← 无法日后区分的身份歧义
```

---

## 6. 更正后的选项目（Identity Domain）

> 与 PBD-01 的区别：不再问「两者是否相等」，而是问「**I-1 定义在哪个字节域**」。

### I-A — I-1 := Producer 域（强制 `original_sha256 == source_content_sha256`）

| 维度 | 内容 |
|---|---|
| 做法 | `original_sha256` 改存 .md raw bytes SHA-256，与 manifest 声明值恒等 |
| 与 Contract | ✅ 对齐 |
| 与 `10 §4.1` | ⚠️ 需重新解释「原始文件」= Producer 声明的 source file |
| Native Path | ❌ **无解**：Native 接收 PDF，拿不到 .md bytes；该路径的 I-1 无处安放 |
| 裁决 | **`[ANALYSIS]` 不可选**——它对一条现存路径无定义 |

### I-β — I-1 := V3 admitted artifact 域（**推荐**）

| 维度 | 内容 |
|---|---|
| 做法 | `original_sha256` 恒 = V3 **对自身接收字节**现算的 SHA-256。Native 收 PDF → PDF sha；Primary 收 .md → .md sha |
| 与 `10 §4.1` | ✅ 「原始文件 SHA256」字面成立（V3 收到的就是它的原始文件） |
| 与 `30:400` | ✅「同一 `original_sha256` 允许多 version 跨 role/provider」继续成立 |
| 与 Contract §1.2 | ✅ 不要求与 `source_content_sha256` 相等（CL-23 已明确「不暗示必须相等」） |
| dedup | ✅ 自洽：同一 .md 无论走哪个 runner 都得同一 I-1 → 正确收敛为 1 个 Document |
| I-0 的保留 | ❌ 需要额外机制才能保留（见 I-β+）；否则 Primary Path 丢失 Producer 声明身份 |
| 实施代价 | **最小**：seal 路径已符合；consumer 侧只需改用**已存在**的 `load_raw_bytes_identity()`（`runner_b2.py:120`）替代 `sha256_hex(body_text)`——**无需新算法、无需新表、无需新字段** |
| 合规性 | ✅ 同时修好 §5.2.1 的规范违反（该模块正是被 `raw_bytes_identity.py:12-15` 明令要求的做法） |

### I-β+ — I-β ＋ 显式 I-0 lineage 记录（**推荐组合**）

| 维度 | 内容 |
|---|---|
| 做法 | 在 I-β 之上，把 manifest 声明的 I-0 连同「已校验」事实写入 lineage，**不要求 hash 相等** |
| 可用既有机制 | ✅ `document_source_versions.parent_version_id` **已存在且当前零使用** → 无需新表即可承载派生关系 |
| 或 | 新增一个**受约束**的 I-0 记录列（需 Owner 裁决，见 D-ID-3） |
| 与 PBD-01 Option C | 同源，但**不用新表**：优先复用 schema 中已冻结的死字段 |
| 风险 | `parent_version_id` 语义须重新裁定（原注为「修正/派生来源」，与本用途一致） |

### I-γ — 新增独立 I-0 identity 实体（PBD-01 Option C 原形）

| 维度 | 内容 |
|---|---|
| 做法 | 建 lineage/identity 表，I-0 与 I-1 通过**显式关系**关联 |
| 代价 | 新表 + migration + dedup 重写 |
| 裁决 | `[ANALYSIS]` 在「只为一个跨系统绑定键」的规模下**过度**；先做 I-β+，不足再升 |

---

## 7. 必须由 Owner 裁决的事项

| # | 问题 | 候选 | 前置关系 |
|---|---|---|---|
| **D-ID-1** | `documents.original_sha256` 定义在哪个字节域？ | ~~I-A（Producer 域）~~ **已作废** / **I-β（V3 admitted 域）＝Owner 已给裁决方向** | **全链前置**；未冻结则不得改任何持久化代码 |
| **D-ID-2** | 「同一文档」的 dedup 以哪个域为准？**且 `le_hash` domain 是否须含 document identity？** | I-1 / I-2（`body_hash`） / I-1+I-2 复合；**`input_domain` 是否加 `document_id`** | ✅ 风险已核实成立（§5.2.2 + REVISION-01 §6）；`ON CONFLICT` 目标索引与 re-read 谓词必须同步修改 |
| **D-ID-3** | Producer 声明的 I-0 是否需要独立血缘载体？ | **复用 `parent_version_id`（推荐，零新表）** / 新列 / 新表 / 不保留（接受丢失） | 与 **D-PP-7** 合并考虑（Owner 已倾向独立 producer metadata） |
| **D-ID-4** | 同一源材料经两条路径到达（PDF 经 OCR→.md vs 直接 .md）是否**应当** dedup 为同一 Document？ | **不合并**（推荐：二者 I-1 不同，本就是不同 artifact 身份） / 合并（需引入 I-0' 上游身份，成本高） | 影响 `documents` 唯一性语义 |
| **D-ID-5** | `3bf7a09` 之后若已写入 DB 的行如何处置？ | 未运行 ⇒ 无数据（推荐先确认） / 标记 `legacy` 保留 / 清库重跑 | **须先确认 DB 是否已有行**（当前 `[UNKNOWN]`） |
| **D-ID-6（新增）** | 修正 `role`/`provider`/`original_sha256` 域后，已 sealed 行的 `le_hash` 如何处置？ | 无数据（若从未跑过）/ 标记 legacy / 清库重跑 / 重建 sealed 行 | 依赖 D-ID-5；见 REVISION-01 §7-§8（`sealed` 后禁 UPDATE ⇒ 不可就地修正） |

> **`[OPEN]`** D-ID-5 的可判定前提是「DB 当前是否存在 Primary Path 行」。本轮**未连接 DB**（见 §8），
> 故该事实为 `[UNKNOWN]`，须由 Owner 或下一次授权运行为准。

**`[FACT]` 风险敞口收窄**：实际会落库的入口只有 **`runner.py`（Track A，`commit()` 于 `:293`）**。
`runner_b2.py` 成功路径**不提交**（仅 `:572` 有 `rollback()`），因此 B2 链路当前不产生持久行。
⇒ D-ID-5 的暴露面 = `runner.py` 的历史运行次数，而非两个 runner 的总和。

---

## 8. 当前禁止事项（Stop Condition）

在 Step 0（Identity Domain Decision）冻结之前：

```text
❌ 不得对 AITutors-v3 做任何 persistence / provenance 代码修改
❌ Primary Path Reference Run
❌ candidate persistence
❌ production database write
   （Owner 明令，见 REVISION-01 §9.1：第一次写库会永久固化 document identity /
     source version identity / provenance，模型错误时修复成本高于当前）
❌ 不得把 role/provider 改成 preprocessing/ppsv3 作为首选
   （role/provider 属 V3 Source Identity Contract；Producer provenance 入独立 metadata
     —— Owner 方向，见 REVISION-01 §5）
❌ 不得为「让 Primary Path 落库成功」而修改测试断言
❌ 不得在 Primary Path 的 semantic 路径上新增 Seal stage / 放宽 85 号 §5 边界
   （Seal 属 Identity Flow，两 Flow 并行 —— 见 REVISION-01 §1-§3）
```

**允许**：

```text
✅ 本批 Decision / Revision Record 的撰写与 Owner 审理
✅ 纯只读的事实核验
✅ 不改语义、不改身份的变量重命名（如 file_sha → body_text_sha256）——见工作单 EXEC-0
```

---

## 9. 与下一步的接口

- Identity 裁决（D-ID-1..6）与 Provenance 裁决（D-PP-1..7）**同批受理**，按 **Step 0 → Step 1** 顺序冻结。
- 执行顺序以 `IDENTITY-PROVENANCE-REVISION-01.md` §9 为准（Step 0..6）。
- 两者冻结后，才产生**可执行修改工单**；工单范围见 `PRODUCER-PROVENANCE-DECISION-01.md` §7（工单）与 §6（裁决项）。
- 本文件**不授权**任何实现。授权另立独立 Owner authorization（Gate 2）。

---

*Recorded 2026-09-27. 本文件为 Decision Preparation，非 Verification / Closure / Audit，不含 `[OWNER DECISION]`。*
