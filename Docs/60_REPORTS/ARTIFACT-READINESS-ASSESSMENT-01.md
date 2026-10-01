# ARTIFACT-READINESS-ASSESSMENT-01

```text
Document Type : Assessment / Analysis Report（C — Informative；非 Decision Record）
Status        : OPEN
Stage         : DRAFT FOR DSH REVIEW
Date          : 2026-10-01
Authorization : Owner 2026-10-01 批准「Artifact Readiness Assessment-01」分析范围（10 条约束）
Parent        : E2E-01 v1.1（已封存事实输入）；A8 OD（仅引用、不修改）
Readers       : Owner；DSH；Domain modeling 评估者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
supersedes    : —   superseded_by : —   disposition   : RETAIN
```

> **本件只做事实边界补全与 ontology 缺口分析。** 不创建 Decision Record；不推荐选项排序；不改 A8 / E2E-01 / Frozen Spec / Contract / Schema / Code；不 Migration。
> **A8 Decision Record remains unchanged; Artifact Readiness is treated as an independent analysis topic.**
> **本件不定义任何正式 domain axis，不写入 canonical terminology。**

---

## 0. 词表异指称（先消歧）

| 记号 | 出处 | 指称 | 本件用法 |
|---|---|---|---|
| **E**（E2E 归因字母） | E2E-01 分类体系 | Artifact readiness 一类（`Identity VERIFIED` + IR artifact absent） | 仅作 E2E 归因标签 |
| **E**（层号） | Frozen Spec `20_Document_Pipeline.md:395-397` | `ResolvedStatus`（段 E 解析状态） | 仅作三层隔离中的层名 |
| **F**（层号） | 同上 | IR `semantic_status` | 值域见 §2 |
| **G**（层号） | 同上 | `gate_decision` | 本件不展开 |

二者 **异指称、不得互换**。下文凡写 `E2E-E` 指归因字母，凡写 `层E` 指 `ResolvedStatus`。

---

## 1. 问题陈述（中性，不预设落点）

E2E-01 已证：87 件为 `Identity VERIFIED` + **IR artifact 不存在**（见 §3）。

本评估回答的中性问题是：

> **`IR artifact absent` 这一观察事实，目前应由哪一层表达，或者是否根本不进入正式 domain model？**

**候选问题空间**（仅列落点可能性，不比较、不排序、不推荐、不预填 Owner 选择）：

```text
a. domain model
b. observation / harness
c. authorization boundary
d. 不进入正式 domain model
```

**不是**实现缺口，**不是**授权缺口，**不是** A8 尾巴。

---

## 2. 三层事实边界（Spec / Code / Harness）

三层词表 **各自独立、不得互相解释、不得互相替代**。

### 2.1 Frozen Spec historical baseline text

| 文件 | 路径 | sha256 | bytes |
|---|---|---|---|
| 20_Document_Pipeline.md | `AITutors-v3/Docs/V3_SPEC/20_Document_Pipeline.md` | `0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c` | 51875 |
| 10_Data_Model.md | `AITutors-v3/Docs/V3_SPEC/10_Data_Model.md` | `529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1` | 47009 |
| 00_Master_Spec.md | `AITutors-v3/Docs/V3_SPEC/00_Master_Spec.md` | `c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4` | 19316 |

Consumer pin: AITutors-v3 `39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4`

| 锚点 | 内容 |
|---|---|
| `20:374-382` | IR 字段示例含 `semantic_status` |
| `20:394` | **值域冻结**：`semantic_status ∈ {ready, incomplete}`（**仅此二值**）——此句身份 = **Frozen Spec historical baseline text**（BUG-V3-018 终裁） |
| `20:395-397` | 三层状态严格隔离：层E `ResolvedStatus` ≠ 层F `semantic_status` ≠ 层G `gate_decision` |
| `20:398-399` | E 的解析状态**不得搬运进 F**（`ambiguous/missing/fuzzy/contextual` 一律坍缩为 `incomplete`） |
| `20:554+` / `20:586` | `semantic_status == ready` 方可进 Compiler/Candidate |
| `10_Data_Model.md` | Identity 侧为 source/input identity（非 IR 存在性） |

**引文边界（防伪引）**：Spec `20:398-399` 的「坍缩为 `incomplete`」**仅**覆盖层E 状态搬入层F，**不是**「禁止第三值」的措辞，也**不覆盖**「IR 产物不存在」。全文**不得**写「不引入第三值」作为 Spec 原文。

**身份声明**：`{ready, incomplete}` 是 **Frozen Spec historical baseline text**，**不得**表述为当前 production Code 的唯一实际值域（见 §2.2）。

Spec 侧有「已有 IR 的质量」轴；**未定义**「IR 产物是否存在」轴。

### 2.2 Production Code 三值（implementation fact）

当前 production implementation 的值域为：

```text
semantic_status ∈ {ready, incomplete, unknown}
```

| 证据 | 位置 |
|---|---|
| 值域定义 | `AITutors-v3/backend/app/domains/compile/__init__.py:37` |
| `unknown` 保留路径 | `AITutors-v3/backend/app/domains/compile/ir.py:223-225` |
| `unknown` 解析来源 | `AITutors-v3/backend/app/domains/compile/mapping_registry.py:19 / 42 / 55 / 106` |
| 三值实现 commit | `13fdce08d2d2fb7f504c9938f1a129753b20f9e9`（M.2） |

**身份声明**：Code 三值仅是 **当前 production implementation fact**。本报告**不**将其升级为新的 Frozen Spec authority，**不**据此改写 §2.1 的历史冻结文。

### 2.3 既有 divergence：`Docs/50_OPERATIONS/X2.6-00-STATE.md §4.14`（不得裸写 F-05）

仓内另有其他 F-05 标识（如 F-05-A/B），**禁止只写裸 `F-05`**。本件所指为：

> `Docs/50_OPERATIONS/X2.6-00-STATE.md` **§4.14**  
> “Frozen Spec Divergence Registration” 中的 **F-05 — semantic_status domain divergence**

| 项 | 值 |
|---|---|
| 分歧 | Frozen Spec §6.2 值域 `{ready, incomplete}` ↔ production Code 三值 `{ready, incomplete, unknown}` |
| 状态 | **`REGISTERED — NOT CLOSED`** |
| 闭合路径 | 独立 **Spec Change**（`Docs/50_OPERATIONS/X2.6-00-STATE.md:980-999`）；无「顺手更新 Frozen Spec」路径 |
| 授权链 | OD-D9-01；OD-UNKNOWN-01；X2.6-IMPL-AUTH-01；Plan M.2（`Docs/50_OPERATIONS/X2.6-00-STATE.md:957-965`） |

**权威关系（原样沿用 `Docs/50_OPERATIONS/X2.6-00-STATE.md:968-972`，不改写、不评价谁落后/谁正确）**：

```text
Frozen Spec text                    = historical / frozen baseline text
production three-value domain       = Owner-authorized X2.6 evolution
implementation authorization       ≠ authorization to modify Frozen Spec text
```

本件**不**创造新的权威表述，**不**判定 Spec 或 Code 谁「落后 / 正确」。

### 2.4 `unknown` 的真实语义

> **`unknown` = semantic state expression**

引用：

- `ir.py:223-225`：`unknown` 已声明则保留，不触发常规校验；= semantic state expression
- `mapping_registry.py:19`：`missing/null/invalid/conflicting -> unknown（never default standalone）`
- `mapping_registry.py:55`：`canonical_target=None` = must resolve to unknown
- `mapping_registry.py:106`：value missing/unknown → caller must resolve to `semantic_status=unknown`
- 三值实现 commit `13fdce08d2d2fb7f504c9938f1a129753b20f9e9`

**`unknown` 不是**：

- IR artifact absent
- artifact readiness
- UNKNOWN migration（`compile/__init__.py:35` 明示：≠ UNKNOWN migration）

因此：**不得用 `unknown` 承载或解释「IR 产物不存在」**。

### 2.5 Harness 词表（observation 层，非 Spec、非 Code）

E2E harness 使用 `semantic_state` 字段，值域与 Spec / Code **均不对齐**：

| 值 | 出现条件 | Spec 值域？ | Code 三值成员？ |
|---|---|---|---|
| `"PENDING"` | `Identity VERIFIED` + IR artifact absent | ❌ 不是 | ❌ 不是 |
| `null` | `Identity FAILED` / `manifest_sha_missing` | ❌ 不是 | ❌ 不是 |

原始证据（均在 `E2E-01-BOUNDARY-REALITY-artifacts/`）：

| 文件 | 记录 | 归属 |
|---|---|---|
| `10-raw-b2-Ocr-markdown.json` | 79×`FAILED`+`null`；87×`VERIFIED`+`"PENDING"` | 85 分片 / 87 全量 |
| `10-raw-b2-data.json` | 4×`FAILED`+`null` | 85 分片 |
| `10-raw-b2-tests.json` | 2×`FAILED`+`null` | 85 分片 |
| `20-raw-b2-identity-ok.json` | 受控样例（`VERIFIED`+`"PENDING"`） | 非 172 分母 |
| `_write_report_v11.py` | 分片表述对照（非独立计数源） | 仅交叉核对 |

**三套词表不得互相解释**：Spec `semantic_status`（层F）≠ Code `SEMANTIC_STATUS`（三值）≠ harness `semantic_state`（`PENDING` / `null`）。

---

## 3. 事实输入（引用 E2E-01，归属当场复算）

| 事实 | 值 | harness `semantic_state` | 来源 |
|---|---|---|---|
| eligible | 172（Ocr-markdown 166 + data 4 + tests 2） | — | E2E-01 v1.1 |
| **85** = B：`Identity FAILED` / `manifest_sha_missing`（MISSING_IDENTITY） | data 4 + tests 2 + Ocr-markdown 79 | **`null`** | raw JSON 复算：`FAILED`+`null` = 4+2+79 = 85 |
| **87** = A+E2E-E：`Identity VERIFIED` + IR artifact absent | Ocr-markdown 87 | **`"PENDING"`** | raw JSON 复算：`VERIFIED`+`PENDING` = 87 |
| downstream_executed | 0/172 | — | E2E-01 |
| 统一入口 | 不存在（A8 范围） | — | E2E-01 / A8 OD |

**归属铁律**：

- 87 件 ⇔ `semantic_state="PENDING"`（`reason=semantic_pending`）
- 85 件 ⇔ `semantic_state=null`（`reason=identity_verification_failed`）
- **不得**把 85 件的 `null` 归入 87 件，亦不得反向合并。

---

## 4. 分析透镜：存在性 vs 质量（非建模推荐）

以下仅为**分析透镜**，用于说明两类事实不可混同；**不是** schema 建议，**不是** domain axis 提案。

```text
透镜一：在「已有 IR」上谈质量
  semantic_status（Spec historical baseline）∈ {ready, incomplete}

透镜二：在「IR 产物是否存在」上谈存在性
  此透镜在 Spec / Code 中均无正式字段（空位待评估）

错误压缩示例（本件不采纳，仅标冲突）：
  把「产物不存在」塞进 semantic_status
    → 违反 20:395-397 三层隔离（存在性 ≠ 层F 质量轴）
    → 20:398-399 的「坍缩为 incomplete」仅针对层E→层F 搬运，对 IR 缺席无 Spec 依据
    → 与 Docs/50_OPERATIONS/X2.6-00-STATE.md §4.14（F-05）已登记分歧叠加
```

E2E 的 87 件卡在 **产物存在性**（harness 记为 `PENDING`），**不是** `semantic_status` 语义质量失败。

---

## 5. Decision Space（自设标记；不穷尽；不推荐；不排序）

> **编号声明**：`AR-1 / AR-2 / AR-3` 为 **本 Assessment 自设分析标记**，**不是**既有 Registry 编号，**不是**穷尽集合。  
> **不推荐、不排序、不投票、不指定默认项。** 取舍属 Owner Decision（另案 OD，本件不建）。

### 5.1 候选形态（中性命名，无优先级）

| 形态 | 名称 | 若采纳则含义（描述，非推荐） |
|---|---|---|
| **形态 A** | 状态值扩展 | 在既有状态枚举上增/并值；须先裁定与 `20:394`/`20:395-397` 及 `Docs/50_OPERATIONS/X2.6-00-STATE.md §4.14` 的关系 |
| **形态 B** | 独立概念/维度 | 另立与 `semantic_status` 正交的存在性概念（**分析用占位名**，非 canonical terminology） |
| **形态 C** | 生命周期/事件 | 以生命周期状态或事件流表达，而非单一状态字段 |
| **形态 D** | 不建模于 domain | 事实留在 observation / harness 或 authorization boundary；domain 不增概念 |

### 5.2 分析标记（非穷尽）

| ID | 选项 | 若采纳则含义（描述，非推荐） |
|---|---|---|
| **AR-1** | 维持现状：IR 缺席仅在 harness/边界阻断 | Spec 不增概念；87 不进语义链；`PENDING` 保持 harness 非 Spec 状态 |
| **AR-2** | 采纳形态 B（独立概念/维度） | 须 Spec Change；不得把「不存在」塞进 `semantic_status`；命名与值域属后续 Owner/Spec 范围 |
| **AR-3** | 将 IR 缺席坍缩为 `incomplete` | 与 `20:395-397` 三层隔离及「层F 只谈已有 IR」冲突；`20:398-399` 的坍缩条款不及于产物缺席；并与 `Docs/50_OPERATIONS/X2.6-00-STATE.md §4.14` 已登记分歧叠加（风险标注，非否决） |

**本件不对 AR-1/2/3 或形态 A/B/C/D 给出推荐、排序、投票或默认值。**

---

## 6. 禁止项（本件及后续引用均受约束）

```text
禁止 1  不得定义 artifact_readiness（或任何占位名）为正式 V3 domain axis
禁止 2  不得写入 canonical terminology
禁止 3  不得把 unknown / PENDING / null 解释为 artifact absent
禁止 4  不得建立新的 Owner Decision
禁止 5  不得给 AR-1/AR-2/AR-3（或形态 A–D）推荐、排序或默认值
禁止 6  不得进入 Spec Change
禁止 7  不得进入 Migration / implementation / wiring
```

---

## 7. OPEN 项（不得推断）

```text
OPEN-AR-01  IR artifact creation ownership unresolved.
            事实仅为 Identity VERIFIED + artifact absent。
            不得推断：Producer 必须补 IR / Resolver 必须自动生成 / V3 必须接受无 IR。
```

责任归属、生成路径、超时策略均 **不在本评估裁定**。

---

## 8. 与 A8 的硬隔离

| | A8 | Artifact Readiness |
|---|---|---|
| 类型 | Execution / Authorization | Domain Modeling 评估（本件只评估，不建模） |
| 问题 | 是否授权 `M1–M5` ↔ Gate/Admission 统一入口 | 产物存在性事实应落在哪一层，或不建模 |
| 当前 | OD `40_DECISIONS/…A8-ENTRYPOINT…` = OPEN / PENDING-OWNER-SIGNATURE / **未生效** | 本 Assessment，**无 OD** |

关系 = **Related Topic**。  
不是 A8 子问题 / Amendment / Implementation。  
**不修改 A8 文件**；亦不写入「A8 Frozen」等新状态语义。

A8 当前状态保持：`Status = OPEN`；`Decision State = PENDING-OWNER-SIGNATURE`；`Authorization = 未生效`。

---

## 9. 范围声明（10 条约束符合性）

| # | 约束 | 本件 |
|---|---|---|
| 1 | 仅 1 份 60_REPORTS 分析文档 | ✅ 本文件 |
| 2 | 不创建 Decision Record | ✅ |
| 3 | 不修改 A8 | ✅ 仅引用 |
| 4 | 不修改 E2E-01 | ✅ 仅引用 |
| 5 | 不修改 Frozen Spec | ✅ 只 hash pin + 引用 historical baseline |
| 6 | 不改 Schema/Contract/Code | ✅ |
| 7 | 不 Migration | ✅ |
| 8 | Decision Space 无推荐排序 | ✅ §5 |
| 9 | IR ownership = OPEN | ✅ §7 |
| 10 | 完成后 DSH 核验再 commit | ✅ 本版未 commit |

---

## 10. 后续路径（本件不执行）

```text
本 Assessment（事实边界 + 对照 + 候选空间）
    ↓ DSH 核验
    ↓ commit / push（本件之后）
    ↓ 停止
（若 Owner 要开模）
OWNER-DECISION-ARTIFACT-READINESS-…（另案，编号另定）
    ↓
Frozen Spec Change Proposal（仅当采纳须改 Spec 的形态）
    ↓
Implementation
```

禁止倒序；禁止并入 A8。

**停止条件满足后不得自行开启 A8-R5、Errata、Correction、Sync 或第二轮 Artifact Readiness Assessment。** 下一步是否建立 Owner Decision，另由 Owner 决定。

---

*Artifact Readiness Assessment-01. Fact-boundary only. No decision, no ranking, no wiring, no canonical terminology.*
