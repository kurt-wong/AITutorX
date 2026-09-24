# OD-01V4R Final Verification Remediation — DSH 对抗性审查

```text
被审对象（只读，未修改）:
  AITutors-v3  HEAD = 81b20803a2e032254e7082450d7846e7b8b850c0
  Subject      = OD-01V4R Final Verification Remediation（F-OD01V4R-30…48）
  Parent       = e611a4deb09e21f50278d98dd545e4541c93b19d
  Delta        = 5 files（COORDINATION ×3 · REPORTS ×2）

审查者:
  DSH 外部独立验证（未参与 OD-01 任何轮次产出；非 Self Review）

判定 = VERIFIED WITH FINDINGS
Closure Blocking = YES
Recommendation = OWNER ACTION REQUIRED BEFORE CLOSURE
Findings = F-OD01V4R-49 … F-OD01V4R-64（16 项）⇔ OD-01F-82 … OD-01F-97

完成条件核对（被审方自述 8/8 VERIFIED）:
  #1 Mapping 一一对应          → NOT SUBSTANTIATED（F-OD01R 系列 4 行不符）
  #2 无 Finding 遗漏 / 无空号  → VERIFIED
  #3 无自定义 Status           → NOT SUBSTANTIATED（口径被缩小）
  #4 Authority Level 不扩展    → PARTIAL（值在枚举内；归因引用不实；D1 文件级 AUTHORITY 非枚举）
  #5 Self Review 不冒充 DSH    → VERIFIED（但历史区被改写，见 F-56）
  #6 table_cell identity 方案B → PARTIAL（四元组已定；table_id 无可核验判据；84 台账未登记）
  #7 Proposed Text 可迁移      → NOT SUBSTANTIATED（围栏损坏 + 无来源条款 + L0 元陈述）
  #8 不修改 Frozen Spec        → VERIFIED
```

本报告是 **OD-01-J 所述「DSH 外部验证」**。被审方的 Self Review 与 Remediation Report 均不得替代或代表本报告。

---

## 0. 审查边界与方法

```text
被审对象 = AITutors-v3 @ 81b2080（只读）
基线     = AITutorX 已提交的 6 份 DSH 报告（HEAD 9eb521b）
           OD-01-FROZEN-SPEC-PROPOSAL…(4b419bf)          F-OD01-01…08   (8)
           OD-01-V2-L1-CR-002…(8c2dca3)                   F-OD01R-01…10  (10)
           OD-01-V3-L1-CR-002-CANDIDATE…(1e44017)         F-OD01V3-01…12 (12)
           OD-01-V4-L1-CR-002-REMEDIATION…(d13e70d+d9173ab) F-OD01V4-01…03 (3)
                                                            F-OD01V4R-01…14(14)
           OD-01-V4R-L1-CR-002…(5adb1b3)                  F-OD01V4R-15…29(15)
           OD-01-V4R-FINAL-VERIFICATION…(9eb521b)         F-OD01V4R-30…48(19)
                                                    合计 = 81
```

**本轮授权范围**：只读审查 + 登记发现。**不**修复、**不** re-freeze、**不**标记 OD-01 生效、**不** push AITutors-v3、**不**修改 Frozen Spec / Contract / P01–P25 / 生产代码 / Preprocessing / Gate / Admission / DB schema / corpus / D1–D5 原件 / 被审交付物。

**验证方法**：文件级逐行对照 + git blob 对照（含历史版本 byte 级首行 diff）+ 全仓词频/坐标实测 + `Docs/V3_SPEC` 树哈希多点取样。所有结论均为**可复现的机械实测**或**规则演绎**，二者在报告中分别标注。

---

## 1. 结论速览

| # | 被审方自述完成条件 | DSH 判定 | 依据 |
|---|--------------------|----------|------|
| 1 | Mapping 与 DSH 基准一一对应 VERIFIED | **不成立** | §3；F-49 |
| 2 | 无 Finding 遗漏、无空号 VERIFIED | **成立** | §4 |
| 3 | 无自定义 Status（Header 仅冻结枚举；处置列≠Status） | **不成立** | §5；F-50 |
| 4 | Authority Level 不扩展（仅 L2 / L2-proposed / L3） | **部分成立** | §5；F-50、F-59 |
| 5 | Self Review 不冒充 DSH | **成立**（边界声明齐备） | §6 |
| 6 | table_cell identity 方案 B（四元组；生产来源必须存在） | **部分成立** | §7；F-53 |
| 7 | Proposed Text 可迁移（含 README §2 前置序 + 合并全文） | **不成立** | §8；F-51、F-52、F-53 |
| 8 | 不修改 Frozen Spec | **成立** | §9 |

```text
实质进展（本轮确实做到的）:
  ✓ F-OD01V4R-30/-31/-32 的映射失真已修复（-08…-14 与 V3 全 12 项按 DSH 标题逐字对齐）
  ✓ OD-01F-01…81 连续、无重号、无空号（81 = 8+10+12+3+14+15+19 精确闭合）
  ✓ CR-002 Status 回到合法枚举 NOT RELEASED
  ✓ Self Review 历史正文 108 行恢复、头块围栏修复、Status 回 HISTORICAL
  ✓ README.md §2 术语登记已进入 change set（含迁移序）
  ✓ §6.3 给出合并后 20 §5.5 全文，既有条款无遗漏
```

```text
但仍阻断 closure 的 4 项:
  ✗ 条件 1 的口径（「Problem 列以 DSH 基线为准，不重释、不合并不降级」）在 F-OD01R 系列不成立
  ✗ 条件 3 以「缩小声明口径」而非「消除非枚举 Status」达成；D1 仍有多处列名为 Status 的非枚举值
  ✗ §6.3 合并全文的围栏结构损坏（§7 被吞入代码块，合并全文不是一个可复制块）
  ✗ Proposed Frozen Text 仍含无来源条款与 L0 元陈述，写入后产生不可判定/流程性条款
```

---

## 2. Git / 隔离事实（DIRECTLY VERIFIED）

```text
AITutors-v3
  HEAD                    = 81b20803a2e032254e7082450d7846e7b8b850c0
  HEAD:Docs/V3_SPEC       = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f   ← UNCHANGED
  ahead of origin/main    = 11（NOT pushed）
  tracked tree            = clean
  untracked               = 10（9 × Docs/COORDINATION/CONTRACTS/* + Docs/GOVERNANCE/）

  delta e611a4d..81b2080  = 5 files changed, 692 insertions(+), 253 deletions(-)
    Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md  +376 -193
    Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md             +112  -17
    Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md                         + 99  -  0  ← 新建
    Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md                + 71  - 12
    Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md                  + 34  - 31

AITutorX（本报告仓）
  HEAD = origin/main = 9eb521b（本报告写入前）；tracked clean；untracked 18
```

**树哈希多点取样**（`git rev-parse <rev>:Docs/V3_SPEC`）：

| rev | tree |
|-----|------|
| f68aa09 | `b3eeb3e9…` |
| 3fa3b73 | `b3eeb3e9…` |
| 9bd6eca | `b3eeb3e9…` |
| b6cb762 | `b3eeb3e9…` |
| e611a4d | `b3eeb3e9…` |
| **81b2080** | **`b3eeb3e9…`** |

`Docs/V3_SPEC` 零改动 ✓，无 `backend/` / Migration / corpus / Schema / 生产代码改动 ✓，AITutors-v3 未 push ✓。

---

## 3. 条件 1 — 映射表真实性审计（**不成立**）

### 3.1 方法

`Proposal §0`（`:36-126`）本轮自述规则（`:40`）：
> 「`Problem` 列以 DSH 已提交基线报告的发现标题为准，**不重释、不合并不降级**。」

故逐行以 DSH 报告**原始 Finding 标题**为基准对照。基准来源：
V1 系列 = `4b419bf`（8 项）；R 系列 = `8c2dca3` 的 `### F-OD01R-0n — <标题>` 标题行；
V3 系列 = `1e44017` 的 `:124-389` 标题行；V4 系列 = `d13e70d` 的 `:42-46`；
V4R 系列 = `d13e70d` 的 `:140-490` 标题行 + `5adb1b3` + `9eb521b`。

### 3.2 逐系列对照结果

| 系列 | 项数 | 与基线一致 | 判定 |
|------|------|-----------|------|
| F-OD01-01…08（V1） | 8 | 8 | ✅ 全部为忠实概括 |
| F-OD01R-01…10（R） | 10 | 6 | ❌ **4 行不符**（R-02、R-04、R-06、R-09） |
| F-OD01V3-01…12（V3） | 12 | 12 | ✅ **逐字一致**（含本轮新填入的 -11/-12） |
| F-OD01V4-01…03（V4） | 3 | 3 | ✅ |
| F-OD01V4R-01…48（V4R） | 48 | 48 | ✅ **上轮 7 行失真全部修复** |

### 3.3 R 系列 4 行不符（本轮新发现问题）

| ID | DSH 基线标题（原文） | 被审方 `Problem`（`:56-65`） | 判定 |
|----|---------------------|------------------------------|------|
| R-02 | 载具违犯 `91 §5.1` 冻结的文档创建门槛（**MED-HIGH｜re-freeze 前置**） | 治理 Header 不合规（含自创 L1-proposal） | ❌ **降级重释**：基线是「四项门槛缺一不可、缺字段即不得创建」的**创建资格**问题，被收窄为字段格式问题 |
| R-04 | 新 §5.3「Producer 唯一权威」与冻结的双轨语义冲突未处置（**HIGH｜design**） | 未覆盖多路径（只写 Artifact） | ❌ 重释：基线是**与冻结语义冲突**，非「未覆盖」 |
| R-06 | 拟议 `20 §5.5` 文本自身不闭合（MED｜re-freeze 前置） | 定位方式一刀切 | ❌ 与基线标题不符（该表述取自 D1 的转述，非 DSH 标题） |
| R-09 | Owner 处置/裁决在指定的 Owner Decision 载体内**不可核验**（MED｜provenance） | 缺 Owner Decision / Finding Disposition 记录 | ❌ **方向反转**：基线=「存在但不可核验」，本行=「记录缺失」；且与 `V3-05 → OD-01F-25` 行（「OD-01R-09 正式 Owner Decision 为 agent 自写…权威来源不可核验」）**语义重叠 → 同一问题两处登记** |

**后果**：`§0:40` 的规则与完成条件 1 的标题句（「Mapping 与 DSH 基准一一对应」）在 F-OD01R 系列不成立。被审方自述把范围限定为「-08…-14 / V3 全系按基线重写」，等于承认只重写了 19 行；而 `§0` 表头仍宣称全部 81 行均以基线为准。

### 3.4 已修复项确认（对照上轮 F-OD01V4R-30/-31/-32）

| ID | 上轮 DSH 指出的失真 | 本轮 `:86-92` 实际 | 判定 |
|----|---------------------|--------------------|------|
| -08 | 实为「引入第 7 套命名空间 / `R-xx` 无定义」，旧表写作「降级态夹带」 | 引入第 7 套命名空间，且 R-xx 语义在仓库内无定义 | ✅ 已恢复 |
| -09 | 实为「Gap 两版并存；`90:47` 未归层未登记」 | Gap 结论两版并存；90:47 未归层后果仍未登记 | ✅ 已恢复 |
| -10 | 实为「违反 `90 §5 Rule 2`」 | 新文档违反 90 §5 Rule 2（禁止词升级） | ✅ 已恢复 |
| -11 | 新增文档的 `Path` 指向另一仓库 | 新增文档的 Path 字段指向另一个仓库 | ✅ 与基线标题一致 |
| -12 | 「Current Rule」块保真度参差 | Current Rule 块保真度参差且未标注逐字/改写 | ✅ |
| -13 | CI-12 与 CI-4 声明同文实则不同文 | CI-12 与 CI-4 声明「同文」但实际不同文 | ✅ |
| -14 | （HIGH）治理产物被逐字节复制进 AITutor-X 且从未 commit | （HIGH）治理产物逐字节复制进入 AITutor-X 且从未 commit：跨仓副本；独立审查边界破坏风险 | ✅ **HIGH 已单独成行** |

上轮 F-OD01V4R-30（HIGH 发现零登记 / 4 组重复描述）在 V4R 系列内**已实质修复** ✓。

---

## 4. 条件 2 — 无遗漏 / 无空号（**成立**）

机械实测（`^| F-… | OD-01F-nn |` 行提取）：

```text
匹配行数        = 81
distinct Final  = 81
min / max       = 01 / 81
重复 Final ID   = 0
缺失 Final ID   = （空）
重复 Finding ID = 0
```

闭包核对：`8 + 10 + 12 + 3 + 14 + 15 + 19 = 81` —— 与 DSH 六份报告的 Finding 计数**精确相等**。

- `OD-01F-09 / -10` 空号已由 `F-OD01V3-11 / -12` 填入，且两行 `Problem`（`:54-55`）与 `1e44017:367` / `:389` 标题**逐字一致** ✓
- V3 系列 12 项全部在表（-11/-12 位于 `:54-55`，-01…-10 位于 `:66-75`），未重编号既有 Final ID（-01…-10 仍为 21…30）✓
- V4R-30…48 对应 `OD-01F-63…81`，连续 ✓

**条件 2 = VERIFIED。**

---

## 5. 条件 3 / 4 — Status 与 Authority Level（**不成立 / 部分成立**）

### 5.1 本轮真正的修复（正面）

| 字段（行号为 81b2080） | e611a4d 值 | 81b2080 值 | 合法值 |
|------------------------|-------------|------------|--------|
| CR-002 `:7` Status | `NOT REGISTERED`（**枚举外**） | `NOT RELEASED` | ✅ `90:376` / `91:168` |
| CR-002 `:8` Authority Level | `Change Record Authority`（自创） | `L2-proposed` | ✅ `91:167` |
| Proposal `:8` Authority Level | `Proposal Authority`（自创） | `L2-proposed` | ✅ `91:167` |
| Self Review `:7` Status | `PENDING`（语义错位） | `HISTORICAL` | ✅ `91:121` |
| Self Review `:8` Authority Level | `Proposal Authority`（自创；更早版本为 `L3 — evidence only`） | `L3` | ✅ `91:167` |
| D1 V4R-15…29 附录 `:438` Status | `PENDING EFFECTIVE FREEZE` | `PENDING` | ✅ `91:114` |
| D1 V4R-15…29 附录 `:439` Authority | `Decision Authority`（自创） | `L2` | ✅ `91:167` |
| Proposal `§0` 第 6 列列名 | `Status`（旧表 60 行全 `VERIFIED`） | `Finding Disposition` | ✅ 处置词≠Status |

F-OD01V4R-39 / -40 / -41 的**主体已修复** ✓。

### 5.2 但条件 3 的达成方式是**缩小口径**，非消除非枚举 Status

`§2.3`（`:180-189`）把声明改写为「Header Status 字段仅用冻结枚举 + Finding Disposition 列≠Status + **Owner Decision 历史表 Status 列 = 历史原文保留（不重写）**」。以此豁免后，仓内仍存在**列名就是 `Status`** 且值非冻结枚举的表：

| 位置 | 列名 | 值 | `91 §3.1` 是否允许 |
|------|------|----|--------------------|
| D1 `:302-313`（OD-01R 附录） | `Status` | `VERIFIED` ×9、`PENDING` ×1 | ❌ `VERIFIED` 不在 10 值枚举内 |
| D1 `:458-474`（V4R-15…29 附录） | `Status` | `VERIFIED` ×15 | ❌ 同上 |
| D1 `:530`（Document control） | `Status` | `RECORDED` | ❌ |
| D1 `:4`（文件级 Header） | `STATUS` | `RECORDED` | ❌ |

关键点：**`:458-474` 并非「历史原文」** —— 该表是上一轮（e611a4d）由 agent 新建的自我判定表，且其 15 项 `VERIFIED` 已被本轮 19 项发现（F-30…48）证伪（例如 F-15「重建唯一 Mapping Table」→ 本轮 F-49；F-19「Status 仅用 91 §3.1 允许词」→ 本轮 F-50；F-24「Self Review 格式」→ 本轮 F-55/F-56；F-25「删除外仓路径」→ 本轮 F-57）。保留 `Status: VERIFIED` 且不加注更正，等于在治理记录中维持已被独立验证推翻的结论。

同时 D1 `:4-5` 是**旧式非规范 Header**（`STATUS: RECORDED` / `AUTHORITY: OWNER DECISION RECORD`，字段名与取值均非规范）。D1 本轮属**实质性修订**（+71/−12、新增两个带完整出生证明的附录、改写章节标题），按 `90 §4:383`「存量文档…**下次实质性修订时补上**」应回填规范 Header —— 未回填。故条件 3 的窄口径（「Header 仅冻结枚举」）在 D1 文件级同样不成立。

### 5.3 条件 4 的残留：归因引用不实 + 目录层冲突

三处均以两个 L0-META 值域**合并引用**支持 `L2-proposed`：

```text
Proposal :25   「Authority Level 取值仅限冻结枚举（`90 §4:375` / `91 §5:167`：
                 L0 | L0-META | L1 | L2 | L2-proposed | L3 | L4 | L5）」
Proposal :161  「冻结枚举（`90 §4:375` / `91 §5:167`）无法表达三分角色」
CR-002  :64    「L2-proposed | 冻结枚举值（`90 §4:375` / `91 §5:167`）」
```

实测 `90 §4:375`：

```text
Authority Level: <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>      ← 不含 L2-proposed
```

`L2-proposed` 仅见于 `91:167` 与 `90 §1.2:81`（后者把该层绑定到 `Docs/REPORTS/`）。因此：(a) 引用归因不实（把 91 独有的值同时归给 90 §4）；(b) 两个 L0-META 文档的 Authority Level 值域并不一致，该冲突未按 `90 §5` 登记进 `84`；(c) `90 §1.2:62` 明文「**物理目录强制分层**」，而 Proposal/CR 位于自认「未归层」的 `Docs/COORDINATION/`（`:32` / CR `:29`），却声明 `Authority Level: L2-proposed`（该层归属 `Docs/REPORTS/`）—— 层级主张与目录模型冲突。

**条件 3 = 不成立；条件 4 = 部分成立。**

---

## 6. 条件 5 — Self Review 不冒充 DSH（**成立**）

非 DSH 边界声明共 4 处，互相一致：

```text
Self Review :20-22   「Historical Self Review = 内部检查。Status: HISTORICAL。/ 不是 DSH Review。
                      不是外部验证。/ 禁止引用本文档作为外部证据或 DSH 证据。OD-01-J 不得引用本文件。」
Self Review :33      「本文档不是 DSH Verification；不得作为 OD-01-J 外部验证证据。」
Self Review :128     「| DSH Review | NOT THIS DOCUMENT |」（历史块内）
Self Review :138     「| DSH Review | NOT THIS DOCUMENT |」（现行块）
新报告    :20        「本报告是治理修复登记，不是 DSH Verification」
```

`OD-01-J`（D1 `:405-414`）已统一为 `Proposal v4R → DSH 外部验证 → Owner 批准 → 正式 re-freeze`，并删除上一轮残留的 `→ DSH 复核` ✓（F-OD01V4R-48 主体修复）。

**条件 5 = VERIFIED**（历史区完整性问题另计，见 F-56）。

---

## 7. 条件 6 — table_cell identity 方案 B（**部分成立**）

**已达成**：`§5:242-244` 与 CI-2 `:310-331` 给出四元组 `(source_version_id, table_id, row_index, column_index)`；字段含义 + 生产来源表（`:246-251`）；`table_id` 生产来源「**必须存在**」（`:257`）；当前未定义明示（`:258`）；生产来源确立前 `table_cell` 不得 `resolved`（`:261`/`:329`）；明确「不得假设生产来源已存在」「不得在本轮创建 schema」（`:260`）。上轮 F-OD01V4R-20/-36 的「table_id 被写成已有事实」已修复 ✓。

**未达成（F-53）**：

1. **可判定标准只覆盖 3/4 字段**：`:253` 与 `:327-328` 的可核对对象是 `source_version_id / row_index / column_index`，**不含 `table_id`** —— 而 `table_id` 恰是唯一没有 Frozen Spec 承载的字段。四元组中有一个字段无判据，「四字段均有值」不可机械判定。
2. **构造性不可满足**：`table_id` 生产来源在 Frozen Spec 内不存在且本轮不创建 → 采纳后 L0 含一条**永久无法满足**的强制条款（`table_cell` 恒不得 `resolved`），而被审方同时把 `table_cell` 写入 `form` 值域并解除 `00 §5` 非目标。
3. **`90 §5 Rule 4` 台账义务未履行**：`90:430`「**指不出唯一生产者的字段 = 治理缺口，进台账**」，`90:389` 指定扫描产物落入 `84_CONFLICT_LEDGER.md`。`Docs/V3_SPEC` 树哈希未变（正确边界），但新报告 `:49` / `:84` **自认**「未写入 `84_CONFLICT_LEDGER`」。义务既未履行也未在任何可机检台账中登记，仅以 Future Required Change 表述。
4. **元陈述仍进入 L0 文本**：见 F-53 与 §8.4 —— `§5:263` 自称「**禁止**元陈述进入 L0」，而 CI-2 的 Proposed Frozen Text 恰好是元陈述。

**条件 6 = 部分成立。**

---

## 8. 条件 7 — Proposed Text 可迁移性（**不成立**）

### 8.1 §6.3 合并全文的围栏结构损坏（F-51，规则演绎 + 机械实测）

机械实测（`Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md`）：

```text
:590  ```text          ← 开启外层
:593  ```json          ← 有 info string，按 CommonMark 不能作为闭合围栏 → 属内容
:604  ```              ← 裸围栏，提前关闭外层（本意不是关闭它）
:646  ```json          ← 开启
:648  ```              ← 关闭
:651  ```              ← 被审方本意是关闭 :590 的外层，实际开启一个新代码块
:678  ```text          ← 有 info string，不能关闭
:682  ```              ← 关闭
```

按 CommonMark「闭合围栏必须与开启围栏同字符、不短于它、且**不得带 info string**」的规则演绎：外层在 `:604` 关闭，`:651` 的裸围栏开启的新块直到 `:682` 才闭合 → **`:653-681`（含 `:657-672` 的 §7 Explicit Diff Appendix 全表、`:676-681` 的 §8 标题与正文）落入代码块**，渲染中不可见；同时 `:590` 的合并全文不再是一个完整代码块，「迁移者须整节替换/合并使用下文」（`:585`）的复制对象在渲染层被截断为 `:591-604`。

重要：全文围栏行数 = **68（偶数）**，常规「配对计数」平衡检查通过 —— 这正是该缺陷逃过自检的原因。同类缺陷曾以 F-OD01V4R-24（`Self Review` 头块围栏损坏，原 `\`\text`）登记，属**复发**。

正确写法：外层使用四反引号围栏（或改为引用块）。当前写法无法表达「含 ```json 的段落」。

### 8.2 合并全文含**无来源、不可判定**的新条款（F-52）

`§6.3:635`（CIE-4 `:396` 同文）：

```text
- option_evidence_status=resolved 时 form 为 1..n。
```

- 现行 `20 §5.5`（`:308-339`）**无**对应条款 —— CI-4 的 `Current Rule`（`:363-367`）只含两行（granularity / line_ref），不含此句；
- CI-4 的 `Problem`（`:369`）与 `Reason`（`:399`）**均未提出**需要该规则；
- 全 `Docs/V3_SPEC` 检索 `1..n` → 仅 `30_Task_LLM_Safety.md:95` 命中（语义无关）；
- 语义不可判定：`form` 是枚举值（`line / line_character / table_cell / multiple_source_spans / other`），而 `1..n` 是计数表达；「form 为 1..n」既非值域约束也非基数约束，无判定规则。

该句在 e611a4d 已存在于 CI-4 增量文本（旧 `:310`）；本轮的实质变化是把它**提升进「合并后完整目标文本」**，即从「增量片段」变成「写入 L0 的成品」。写入后 L0 将新增一条无 Current Rule 对应、无理由、不可判定的规范条款。

### 8.3 CI-11 未声明地删除 L0 引用坐标（F-60）

现行 `50_Migration_Assets.md:51`：

```text
| 图像/表格 bbox 定位能力 | 保留思想，重写 | source_figures（page/bbox/placement/source，IS-7）+ role 归属（10 §4.4/§6.6、20 §5.3/§7.2.5） |
```

CI-11 Proposed（`:528`）：

```text
| 图像/表格 bbox 定位能力 | 保留思想，重写 | source_figures（page/bbox/placement/source，IS-7）+ role 归属；option provenance 的 table_cell 使用 table_cell identity 四元组定位，other(method=image_region) 使用 figure/region 身份；line_ref 可选，不得伪造 |
```

`（10 §4.4/§6.6、20 §5.3/§7.2.5）` —— role 归属的**权威定义坐标**被删除，CI-11 的 `Problem`（`:524`）与 `Reason`（`:531`）均未声明该删除。属未声明的 L0 引用删除，削弱 `90 §2 R7` 引用闭包。

### 8.4 L0 元陈述：`§5:263` 禁止的事，同一 change set 正在做（F-53）

`§5:263`：

```text
**禁止**元陈述进入 L0（不写「identity 形状与 Frozen Spec 对齐前不得声称…」类流程句）。
```

同一 change set 的 Proposed Frozen Text 实际内容：

| 位置 | 文本 | 性质 |
|------|------|------|
| CI-2 `:321-324` | 「当前 Frozen Spec **未定义** `table_id` 生产来源」「**Future Required Change**：在 Frozen Spec 写入前确立…」「**本条不授权**数据库 schema 变更」 | 关于本文档自身变更过程的流程句 |
| CI-1 `:286` | 「例外子集（**CHANGE-4**）」 | 把 change 分类号写入 L0 条款 |
| CI-12 `:549` / §6.3 `:631` | 「不引入降级质量标记（**Planning Category: Future Consideration**）」 | 把 **Proposal 级规划词汇**写入 L0 成品文本 |
| CI-8 `:474-476` | 「…**保持不变**。Resolved Span 增加 form **不改变**既有 dedup 组合定义」 | 无规范内容的自指句 |
| CI-9 `:492-493` | 「JSONB invariant 与既有键**保持**；不引入双名」 | 同上 |

其中 CI-12/§6.3 的 `Planning Category: Future Consideration` 最严重：`§10:716-723` 明确定义「Planning Category（**非 Status**）…不是 Status。不得填入 Status 字段」—— 它属 proposal 层的分类词汇，却被写进要迁移进 Frozen Spec 的成品文本。

### 8.5 Native 路径出现规范空洞（F-61）

CI-3 删除 `20:280-281` 的 `按 A/B/C/D 顺序；每项到下一标签/下一题结束`，替换为「Native 路径：Native Resolver 确定性 role resolution 产出 option 边界（**首次解析**）」（`:352`）。被删除的那句正是使 Path A 解析「确定性」的**唯一规范定义**。CI-3 同时要求「**两路径必须产出语义等价 option 结构**」（`:353`）—— 在删除了 Path A 的边界判据后，「语义等价」不可判定。

### 8.6 CI-7/8/9/10 相对 e611a4d 的规范缩减（F-62）

逐行对照 `e611a4d` 被删文本（git diff）：

| CI | e611a4d 曾有 | 81b2080 现有 |
|----|--------------|--------------|
| CI-7 | `compiled_roles[]` + `text_hash`；「option leaf label/text 按 §5.3 路径规则确定」；「正文与 verified locator slice 一致」 | 「Compiler 从 Resolved Span 按 form 提取（…）。不得重新发现 option 边界…」 |
| CI-8 | `dedup_key = canonical question type + own stem + own options（label order；label 重复 fail-fast）；排除列表不变`；Question identity 不变 | 「dedup 组合键…保持不变」 |
| CI-9 | JSONB 允许承载键清单 + 「不得用 JSONB 隐式承载整个业务模型」 | 「增加 form 与 span_resolution 字段…」 |
| CI-10 | `2b line / line_character：…∈ document_source_lines 且 slice 存在；table_cell：…；2c resolved text_hash == …` | 「核验规则按 form 分型（见 20 §5.5 locator 表）…」 |

缩减本身可以是有意的（CHANGE-1「防误改」不必重述现行条款），但 4 条同时缩减未在 `Problem`/`Reason` 中登记；在条件 7「可迁移」口径下，新文本的规范密度**低于**它所取代的版本。

### 8.7 条件 7 中**已达成**的部分（正面）

- **README §2 目标已入 change set** ✓：CI-README（`:554-579`）、`§7` 首行（`:661`）、`§10` Future Required Change（`:730`、`:734`），并声明迁移序「先 README §2，后 20/10」。实测 `README.md` / `10` / `20` 中 `span_resolution` / `option_evidence_status` / `form` 命中 = **0**，故「先登记后使用」的序是必要且已声明的 ✓（F-OD01V4R-33 主体修复）。
- **`§6.3` 合并全文对现行 `20 §5.5` 无遗漏** ✓：逐条核对现行 `20:308-339` 的 heading / JSON / granularity / line_ref / `text_hash` / Annotation / `figure_id` / Resolved Relation / 「关系必须全部 resolved，IR 才可 ready」全部保留；`resolution_status` 已改为 `span_resolution`（F-OD01V4R-38 主体修复）。
- **CI-4「正交」表述已删除**，给出维度定义 + 绑定规则（`form=line ⇒ granularity=line` 等），并声明「禁止声明正交」（F-OD01V4R-34 主体修复）。
- **「无条件 line_ref」已删除**，`§3.2:209-217` 与 §6.3 `:617-626` 均为按 form 分型（F-OD01V4R-35 主体修复）。
- **12/12 CI 均含 `Current Rule`**，且逐条标注 verbatim / summary ✓；本轮抽样复核 `CI-1`（↔`00:274-275`）、`CI-2`（↔`10:107-109`）、`CI-3`（↔`20:280-281`）、`CI-4`（↔`20:322-324`）**逐字一致**（含 CI-2 补齐的「依据 01 v0.3 收敛。」与「（M1 必需）」）→ F-OD01V4R-21/-22 与 V3-11（OD-01F-09）主体修复 ✓。

**条件 7 = 不成立**（8.1–8.6 为阻断项）。

---

## 9. 条件 8 — 不修改 Frozen Spec（**成立**）

```text
git rev-parse 81b2080:Docs/V3_SPEC = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
delta 5 files 全部位于 Docs/COORDINATION/** 与 Docs/REPORTS/**
无 Docs/V3_SPEC/** 变更；无 backend/ / migration / corpus / schema / 生产代码变更
```

**条件 8 = VERIFIED。**

---

## 10. 发现（F-OD01V4R-49 … F-OD01V4R-64）

```text
严重度分布：
  MED-HIGH : F-49, F-50, F-51, F-53
  MED      : F-52, F-54, F-55, F-56, F-57, F-58, F-61
  LOW-MED  : F-59, F-60, F-62
  LOW      : F-63, F-64
全部 = REGISTERED, 0 REPAIRED（本报告不修复）
```

### F-OD01V4R-49（MED-HIGH）— `§0` 的「以 DSH 基线为准」在 F-OD01R 系列不成立
`Problem`：`§0:40` 宣称「`Problem` 列以 DSH 已提交基线报告的发现标题为准，不重释、不合并不降级」，条件 1 宣称「Mapping 与 DSH 基准一一对应」；实测 R-02、R-04、R-06、R-09 四行与 `8c2dca3` 标题不符，其中 R-02 把 MED-HIGH 的「违犯 `91 §5.1` 文档创建门槛」降级为字段格式问题、R-09 把「不可核验」反转为「记录缺失」并与 V3-05 行重复登记。
`Evidence`：`Proposal :56-65`；`AITutorX 8c2dca3:95 / :122 / :155 / :190`；`Proposal :70`（V3-05 行）。
`Risk`：映射表作为治理溯源的载体，仍存在 4 行失真；若据此判「无遗漏、一一对应」，历史 Finding 的级别与语义继续被静默改写（AGENTS.md：Provenance ≠ Quality Authority）。
`Closure Blocking`：YES。

### F-OD01V4R-50（MED-HIGH）— 条件 3/4 以缩小口径达成；D1 仍含列名为 `Status` 的非枚举值与旧式文件级 Header
`Problem`：`§2.3:186` 以「Owner Decision 历史表 Status 列 = 历史原文保留」豁免后，D1 `:302-313`（9×`VERIFIED` + `PENDING`）、`:458-474`（15×`VERIFIED`）、`:530`（`RECORDED`）三处 **列名仍为 `Status`** 且值非 `91 §3.1` 冻结枚举；`:458-474` 系上一轮新建表而非历史原文，其 15 项 `VERIFIED` 已被本轮 19 项发现证伪。D1 `:4-5` 文件级 Header 为 `STATUS: RECORDED` / `AUTHORITY: OWNER DECISION RECORD`（字段名与取值均非规范），而 D1 本轮属实质性修订，按 `90 §4:383` 应回填。
`Evidence`：`D1 :4-5 / :302-313 / :458-474 / :530`；`91:109-122`（无 `VERIFIED`/`RECORDED`）；`91:167`；`90:383`；`91 §5.1:196`。
`Risk`：条件 3「无自定义 Status」与条件 4「Authority Level 不扩展」在 D1 不成立；治理记录维持已被推翻的 `VERIFIED` 结论。
`Closure Blocking`：YES。

### F-OD01V4R-51（MED-HIGH）— `§6.3` 合并全文围栏结构损坏，§7 差异附录被吞入代码块
`Problem`：`:590` 的 `\`\`\`text` 被 `:604` 的裸围栏提前关闭（`:593` 的 `\`\`\`json` 带 info string 不能闭合），`:651` 的裸围栏转而开启新块并吞掉 `:653-681`（§7 全表 + §8 标题）；合并全文不是一个可复制的单体块，与 `:585`「迁移者须整节替换/合并使用下文」冲突。总围栏数 68（偶数）故配对检查通过。
`Evidence`：`Proposal :590 / :593 / :604 / :646 / :648 / :651 / :657-672 / :682`；CommonMark 闭合围栏规则；对比上轮 F-OD01V4R-24（围栏损坏）。
`Risk`：交付物结构损坏 + 迁移对象在渲染层被截断；同类缺陷第二次出现。
`Closure Blocking`：YES。

### F-OD01V4R-52（MED）— 合并 Frozen Text 含无来源、不可判定的新条款
`Problem`：`§6.3:635`（= CI-4 `:396`）`- option_evidence_status=resolved 时 form 为 1..n。` 在现行 `20 §5.5` 无对应条款，CI-4 的 `Problem`/`Reason` 未提出该规则，`form`（枚举）与 `1..n`（计数）语义不匹配，无判定规则。本轮把它从增量片段提升为「写入 L0 的成品」。
`Evidence`：`Proposal :363-367（Current Rule 仅两行）/ :369 / :396 / :399 / :635`；`20:308-339`；全 `Docs/V3_SPEC` 检索 `1..n` → 仅 `30:95`。
`Risk`：采纳后在 L0 新增一条无 Current Rule 对应、无理由、不可判定的规范条款。
`Closure Blocking`：YES（随 F-51 一并修正）。

### F-OD01V4R-53（MED-HIGH）— `§5:263` 禁止的元陈述正出现在同一 change set 的 L0 成品文本；`table_cell` 构造性不可满足且台账义务未履行
`Problem`：`§5:263` 明文「禁止元陈述进入 L0」，但 CI-2 `:321-324`（「当前 Frozen Spec 未定义…」「Future Required Change：在 Frozen Spec 写入前确立…」「本条不授权数据库 schema 变更」）、CI-1 `:286`（「（CHANGE-4）」）、CI-12 `:549`/§6.3 `:631`（「（Planning Category: Future Consideration）」）、CI-8 `:474-476`、CI-9 `:492-493` 均为流程/自指/分类句；`Planning Category` 更属 `§10:716-723` 定义的 proposal 层词汇。另：`table_cell` 可判定标准只覆盖 `source_version_id/row_index/column_index` 三字段（`:253`/`:327-328`），`table_id` 无判据；生产来源不存在且本轮不创建 → 条款构造性不可满足；`90 §5 Rule 4`（`90:430`）的「进台账」义务未履行，`84_CONFLICT_LEDGER` 未登记（新报告 `:49`/`:84` 自认）。
`Evidence`：`Proposal :253 / :261 / :263 / :286 / :321-324 / :327-328 / :474-476 / :492-493 / :549 / :631 / :716-723`；`90:389 / :420-430`；`Remediation Report :49 / :84`。
`Risk`：采纳后 L0 含不可判定条款 + proposal 级词汇；治理缺口未入账。
`Closure Blocking`：YES。

### F-OD01V4R-54（MED）— 新建报告未过 `91 §5.1` 门槛 1，且与同 commit 新增的 D1 附录内容重叠
`Problem`：`OD-01V4R-FINAL-REMEDIATION-REPORT.md:9` 的 `Purpose` 未论证「与最近似现有文档的**不可合并差异**」（`91 §5.1:194-195`：四项缺一不可，缺字段即不得创建），而其 19 项逐项登记与同一 commit 新增的 D1 `OD-01V4R-30…48` 附录（`:500-520`）实质重叠 —— 正是门槛 1 要求论证的差异。
`Evidence`：新报告 `:9`；`D1 :478-520`；`91:184-199`。
`Risk`：以「再建一份治理文档」解决治理问题，即 `91 §5.1:186-188` 明示要阻止的模式。
`Closure Blocking`：NO（但须说明或合并）。

### F-OD01V4R-55（MED）— 两份 `Docs/REPORTS/` 文档的 `Document Type` 不合规
`Problem`：Self Review `:6` = `Report`（`91:165-166` 枚举为 Frozen Spec / Contract Change Record / Decision Record / Governance Meta-Spec / Gate Report / Experiment Report / Status，**无 `Report`**；该值自 e611a4d 沿用，本轮以「字段齐备」结案但未改正）；新报告 `:6` = `Experiment Report` 而其 `:8` = `Authority Level: L3`（`90:43-44`：L3 = Gate Report，L4 = Experiment Report）→ 类型与层级不符。
`Evidence`：`Self Review :6`；`Remediation Report :6 / :8`；`91:165-168`；`90:43-44`；`90:81`。
`Risk`：条件 3/4 的「Header 冻结枚举」声明未覆盖 `Document Type` 字段；同一枚举错用在两处。
`Closure Blocking`：NO。

### F-OD01V4R-56（MED）— Self Review「全文恢复 / 不覆盖、不删除」与事实不符
`Problem`：历史正文 108 行确已恢复，但恢复的同时改写了历史区内容：(a) `## 历史正文（Self Review only）` → 追加「— 全文恢复」（`:37`）；(b) `**Document control**` → 「**Document control（历史块内；原文保留）**」（`:118`）；(c) 历史表行 `| Path |` → `| Path（历史自述） |`（`:122`）；(d) 历史表内插入 3 行 `Path（现行本仓）` / `Kind` / `DSH Review`（`:123`、`:127-128`）；(e) 移除原文件首字节 UTF-8 BOM。
`Evidence`：`git diff --no-index b6cb762:… 与 81b2080` 首行与 `:117/:122/:123/:127-128`；`Self Review :23 / :31`（「不删除、不改写」「不覆盖、不删除」）；`90 §2 R8`（「保留正文（历史审计证据，不得改写或删除）」）。
`Risk`：历史审计证据被改写而声明为「未改写」。
`Closure Blocking`：NO（但声明与事实必须一致）。

### F-OD01V4R-57（MED）— 新报告 `Derives From` 含不可解析引用（本仓不存在的 `AGENTS.md` + 跨仓路径 `Docs/60_REPORTS`）
`Problem`：`Remediation Report :11` 的 `Derives From` 含 `AGENTS.md`（AITutors-v3 全仓递归检索 **0 命中**）与 `Docs/60_REPORTS`（跨仓路径，本仓 `Docs/60_REPORTS` 不存在）。`91:171`/`:179` 规定 `Derives From` 是 R7 引用闭包的**可机检落点**。同时 `§0` 的 `OD-01F-58` 行（`:103`）把 F-OD01V4R-25 的修复证据写成「仅本仓路径；引用可解析」—— 该声明在新文件上不成立（同类残留亦见于 Self Review `:122` 的历史保留行）。
`Evidence`：`Remediation Report :11`；`Proposal :103`；`Test-Path` 实测；`91:171 / :179`；`90 §2 R7`。
`Risk`：破引用与跨仓路径在同一 commit 新建文件中复发；闭包点不可机检。
`Closure Blocking`：NO。

### F-OD01V4R-58（MED）— D1 新附录预先登记 19 项「Owner Decision: APPROVED」，无外部证据且与同 commit 报告口径矛盾
`Problem`：`D1 :502-520` 对 F-OD01V4R-30…48 逐项填 `Owner Decision: APPROVED — …`，`Derives From`（`:488`）把证据指向**自写**的 `Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md`（L3，且 `91:171` 要求向上闭包到 L0/L1/L2）。同一 commit 内 `Remediation Report :69` 写「条件 1：PENDING 自检 / 待 DSH」、`:89` 写「等待 DSH」，而任务陈述称 8/8 VERIFIED → 三处状态口径互不相同。相关：`D1 :288` 仍自称「（正式 Owner Decision）」并在 `:317` 声明本文件「不得充当 L0/L1/L2 权威来源」，同节自相矛盾；`:299` 声称证据链为 `DSH Finding → Owner Decision`，但载体为 agent 自写。此即 `F-OD01V3-05`/`OD-01F-25`（agent 自写 Owner Decision、权威来源不可核验）的**第 5 轮复现**。
`Evidence`：`D1 :288 / :299 / :317 / :488 / :502-520`；`Remediation Report :11 / :69 / :89`；`91:171 / :179`；`AITutorX 1e44017:237-259`。
`Risk`：以自写报告为据主张 Owner 授权，provenance 链不可核验。
`Closure Blocking`：YES。

### F-OD01V4R-59（LOW-MED）— `Authority Level` 归因引用不实，且与目录层模型冲突未登记
`Problem`：`Proposal :25 / :161`、`CR-002 :64` 以「`90 §4:375` / `91 §5:167`」共同支持 `L2-proposed`，但 `90 §4:375` 枚举为 `<L0|L1|L2|L3|L4|L5|L0-META>`，不含 `L2-proposed`；该值仅见于 `91:167` 与 `90 §1.2:81`（绑定 `Docs/REPORTS/`）。`90 §1.2:62` 明文「物理目录强制分层」，而两份文档位于自认未归层的 `Docs/COORDINATION/`。两个 L0-META 值域不一致的冲突未登记 `84`。
`Evidence`：`Proposal :25 / :32 / :161`；`CR-002 :29 / :64`；`90:375 / :376 / :81 / :62`；`91:167`。
`Risk`：条件 4「不扩展」在值层面成立、在归因与目录层不成立。
`Closure Blocking`：NO。

### F-OD01V4R-60（LOW-MED）— CI-11 未声明地删除 L0 引用坐标
`Problem`：CI-11 Proposed（`:528`）删除 `50:51` 现行行中的 `（10 §4.4/§6.6、20 §5.3/§7.2.5）`，`Problem`（`:524`）与 `Reason`（`:531`）未声明。
`Evidence`：`Proposal :524 / :528 / :531`；`50:51`；`90 §2 R7`。
`Closure Blocking`：NO。

### F-OD01V4R-61（MED）— CI-3 删除 Native 路径 option 边界规范，却要求两路径语义等价
`Problem`：`20:280-281` 的 `按 A/B/C/D 顺序；每项到下一标签/下一题结束` 是 Path A（Native）option 边界确定性的唯一规范定义；CI-3（`:348-354`）删除后仅以「Native Resolver 确定性 role resolution（首次解析）」替代，同时要求「两路径必须产出语义等价 option 结构」→ 等价性无可判定规则。
`Evidence`：`Proposal :340-341 / :348-354`；`20:275-294`。
`Closure Blocking`：NO（但须补 Path A 规范或撤回等价性主张）。

### F-OD01V4R-62（LOW-MED）— CI-7/8/9/10 相对 e611a4d 缩减拟制规范细节，未登记
`Problem`：`compiled_roles[]`/`text_hash`、`dedup_key` 组合定义、JSONB 允许键清单、`10 §8` 的 2b/2c 分型改写文本在本轮 Proposed Text 中消失（见 §8.6 对照表），`Problem`/`Reason` 未声明缩减。
`Evidence`：`git diff e611a4d..81b2080` 删除行；`Proposal :454-458 / :473-476 / :491-494 / :509-512`。
`Closure Blocking`：NO。

### F-OD01V4R-63（LOW）— 未声明的字节级改动：BOM 被移除
`Problem`：本轮 Proposal / CR-002 / D1（及 Self Review）的首行出现 `-﻿# …` → `+# …`，即既有 UTF-8 BOM 被移除；`OD-01F-10`（V3-12）的处置文本只声明「本轮写入不经 BOM」，未覆盖对既有 BOM 的**移除**这一相反方向的字节改动。
`Evidence`：`git diff --unified=0 e611a4d..81b2080` 三个文件的首个 hunk；`Proposal :55`。
`Closure Blocking`：NO。

### F-OD01V4R-64（LOW）— 交付说明与仓内证据不一致（三处状态口径）
`Problem`：任务陈述称 8 项完成条件全部 `VERIFIED`；仓内 `Remediation Report :69-76` 实写「条件 1：PENDING 自检 / 待 DSH」与「自检：…」；`D1 :502-520` 对同一 19 项记 `Owner Decision: APPROVED`。同一 commit 内并存「VERIFIED / 自检 PENDING / APPROVED」三种口径。
`Evidence`：`Remediation Report :65-76 / :89`；`D1 :502-520`。
`Closure Blocking`：NO。

---

## 11. 正面证实（P1–P16）

| # | 证实项 | 证据 |
|---|--------|------|
| P1 | `Docs/V3_SPEC` 树哈希在 f68aa09 / 3fa3b73 / 9bd6eca / b6cb762 / e611a4d / **81b2080** 六点完全一致 | §2 |
| P2 | delta 严格限于 5 个 COORDINATION / REPORTS 文档；无 backend / schema / corpus / 生产代码 | `diff --stat` |
| P3 | `§0` 重建为 81 行，`OD-01F-01…81` 连续、无重号、无空号；`8+10+12+3+14+15+19 = 81` 精确闭合 | §4 机械实测 |
| P4 | V3 系列 12/12 与 DSH 标题逐字一致，含本轮新填入的 `-11/-12 → OD-01F-09/-10` | `§0:54-55 / :66-75` |
| P5 | V4R 系列上轮 7 行失真全部修复（-08/-09/-10 恢复、-11…-14 对齐、-14 含 HIGH 与三要素并单独成行）；4 组重复描述消除 | `§0:86-92` |
| P6 | `§0` 第 6 列由 `Status`（旧版 60 行全 `VERIFIED`）改为 `Finding Disposition`，词汇表在 `:128` 声明为非 Status | `Proposal :44 / :128` |
| P7 | CR-002 `Status: NOT RELEASED`（`90:376`/`91:168` 枚举内）、`Authority Level: L2-proposed`（`91:167` 枚举内）；`Registration Level` 与 Authority 分离 | `CR-002 :7 / :8 / :22 / :64 / :147` |
| P8 | Self Review `Status: HISTORICAL`、13 字段出生证明齐备、原损坏围栏（`\`\text`）修复 | `Self Review :3-18` |
| P9 | Self Review 历史正文 108 行恢复（`VERIFIED WITH FINDINGS` / `CLOSURE BLOCKING` / `READY FOR OWNER REVIEW` 原文回归） | `Self Review :39-130` |
| P10 | README §2 术语登记进入 change set（CI-README + §7 首行 + §10 + 迁移序） | `Proposal :554-579 / :661 / :730 / :734` |
| P11 | CI-4 删除「与 granularity 正交」；改为维度定义 + 绑定规则 + 「禁止声明正交」 | `Proposal :374-380` |
| P12 | 「无条件 line_ref」删除；`§3.2:209-217` 与 §6.3 `:617-626` 均按 form 分型 | `Proposal :384-392 / :617-626` |
| P13 | `§6.3` 合并全文对现行 `20 §5.5` **无遗漏**（heading / JSON / text_hash / Annotation / figure_id / Resolved Relation / ready 条件全保留），`resolution_status` → `span_resolution` | `Proposal :590-651` vs `20:308-339` |
| P14 | 12/12 CI 含 `Current Rule` 且逐条标 verbatim/summary；抽样四条与 L0 逐字一致（含 CI-2 补齐「依据 01 v0.3 收敛。」与「（M1 必需）」）→ V3-11/OD-01F-09 修复 | `Proposal :273 / :294 / :337 / :361`；`00:274-275` / `10:107-109` / `20:280-281` / `20:322-324` |
| P15 | 禁用状态词扫描仍 CLEAN（命中均为禁用清单或 Problem 引述）；`APPROED` 不再作状态值 | 全 5 文件词频实测 |
| P16 | `CHANGE-4/5: ACKNOWLEDGED（four-gate required）`；Gate A–D 全 `PENDING`；`未归层`（`90:47`）已在 Proposal `:32/:705`、CR `:29`、D1 `:317/:454` 登记 | `Proposal :678-689 / :705` |

---

## 12. 局限（L-1 … L-6）

```text
L-1  未运行任何测试/回归；本报告是文档级与规则级验证，不含实现与 schema 验证。
L-2  条件 1 的基线取 AITutorX 已提交的 6 份 DSH 报告标题；若 Owner 另有 Finding 定义版本，
     受影响发现为 F-49（及 F-50 的严重度）。
L-3  git fetch 不可用：origin/main 比较基于本仓本地引用；AITutors-v3 远端未核验。
L-4  本机 pwsh 沙箱不可初始化，全部命令以 danger-full-access 只读执行；未写入被审仓库。
L-5  §8.1 的围栏结论为 CommonMark 规则演绎（闭合围栏不得带 info string），未使用具体渲染器复现；
     可机械复核的事实是围栏行序列与总数 68（偶数）。
L-6  §8.6 的「缩减」判断基于 git diff 文本对照，未评估每一项缩减是否在别处已有等价规范。
```

---

## 13. 最终判定

```text
OD-01V4R Final Verification Remediation = VERIFIED WITH FINDINGS
Closure Blocking = YES
Recommendation   = OWNER ACTION REQUIRED BEFORE CLOSURE
Findings         = F-OD01V4R-49 … F-OD01V4R-64（16 项；REGISTERED，0 REPAIRED）⇔ OD-01F-82 … OD-01F-97

新问题起始号 = OD-01F-82（符合 §0:42「新问题自 OD-01F-82 起」）
```

### 进入 Frozen Spec 前的必要修正（缺一不可）

```text
1. §0 映射表：把 F-OD01R-02 / -04 / -06 / -09 四行 Problem 恢复为 DSH 基线标题
   （R-02 = 违犯 91 §5.1 文档创建门槛；R-09 = 裁决在指定 Owner Decision 载体内不可核验），
   并消除 R-09 与 V3-05 的重复登记。                        [F-49]

2. §6.3：外层改用四反引号围栏（或引用块），使合并全文成为单一可复制块、§7 不再被吞入代码块；
   删除 `option_evidence_status=resolved 时 form 为 1..n`，或为其补 Current Rule / Problem /
   Reason 并给出可判定语义。                                [F-51, F-52]

3. Proposed Frozen Text 去元陈述：CI-1 的「（CHANGE-4）」、CI-2 的「当前 Frozen Spec 未定义…／
   Future Required Change…／本条不授权…」、CI-12 与 §6.3 的「（Planning Category: Future
   Consideration）」、CI-8/CI-9 的自指句移出 L0 文本；并为 table_id 给出可核验判据，
   或明确「table_cell 条款暂缓写入」并登记 84 台账义务。      [F-53]

4. 治理字段归位：D1 文件级 Header（`STATUS: RECORDED` / `AUTHORITY: OWNER DECISION RECORD`）
   与三处 `Status` 列（`:302-313` / `:458-474` / `:530`）改为冻结枚举或改名为非 Status 的处置列；
   两份 REPORTS 的 `Document Type` 改用枚举值并与层级一致；新报告 `Derives From` 改为可解析的
   本仓闭包；Self Review 历史区停止改写（或撤回「不改写」声明）；D1 新附录的
   「Owner Decision: APPROVED」改为不含 Owner 授权主张的处置登记，或提供外部 Owner 证据。
                                                            [F-50, F-55, F-56, F-57, F-58]
```

### 非阻断（建议顺手处置）

```text
- Authority Level 引用归因改正（90 §4:375 不含 L2-proposed）+ 登记 L0-META 值域冲突   [F-59]
- CI-11 恢复被删引用坐标 `（10 §4.4/§6.6、20 §5.3/§7.2.5）`                          [F-60]
- CI-3 为 Native 路径补 option 边界规范，或撤回「两路径语义等价」主张                   [F-61]
- CI-7/8/9/10 说明缩减理由或恢复拟制细节                                              [F-62]
- 声明 BOM 移除；统一 `VERIFIED / 自检 PENDING / APPROVED` 三处状态口径                [F-63, F-64]
- 新建报告与 D1 附录的不可合并差异须论证或合并                                         [F-54]
```

```text
边界声明（审查期间强制保持）:
  Frozen Spec: UNCHANGED     Schema: UNCHANGED        Production: UNCHANGED
  Migration: NOT AUTHORIZED  Phase 1: NOT ENTERED     Re-freeze: NOT EXECUTED
  AITutors-v3: NOT PUSHED    被审交付物: 未修改        Findings: 仅登记，未修复
```

---

## 附录 A — DSH 基线编号与标题（条件 1 的对照依据）

```text
AITutorX @ 4b419bf  OD-01-FROZEN-SPEC-PROPOSAL-DSH-ADVERSARIAL-REVIEW.md
  F-OD01-01…08（8 项）
    -01 §2.1 Current Frozen Semantics 遗漏 20 §5.5 既有 granularity/line_ref 语义
    -02 变更集不完整：至少 5 处 L0 条款需修改/废止而 D4 未列
    -03 禁 V3 rediscovery 与现行 20 §5.3 option_label 规则冲突
    -04 Producer options[].provenance 与既有 IR source_span 权威关系未定义
    -05 fail-closed 表征歧义：unresolved 与 options_unresolved 并存未定名
    -06 image_region / degraded 未纳入最小原语集
    -07 L0 修改路径未按 90 §3 分类
    -08 引用 sp-*.option.* 坐标错误

AITutorX @ 8c2dca3  OD-01-V2-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md   （:78-203 标题行）
  F-OD01R-01 L1 Change Record = CREATED 在 90 层面不成立（HIGH）
  F-OD01R-02 载具违犯 91 §5.1 冻结的文档创建门槛（MED-HIGH）
  F-OD01R-03 变更分类未评估 CHANGE-4/5，却断言「不需要四道门」（HIGH）
  F-OD01R-04 新 §5.3「Producer 唯一权威」与冻结的双轨语义冲突未处置（HIGH｜design）
  F-OD01R-05 explicit diff 未穷尽受影响条款（MED）
  F-OD01R-06 拟议 20 §5.5 文本自身不闭合（MED）
  F-OD01R-07 新增 resolution_status 与既有同名字段值域不同（MED）
  F-OD01R-08 fail-closed 模型仍有未闭合词：degraded（MED）
  F-OD01R-09 Owner 处置/裁决在指定的 Owner Decision 载体内不可核验（MED｜provenance）
  F-OD01R-10 两处精度问题（LOW）

AITutorX @ 1e44017  OD-01-V3-L1-CR-002-CANDIDATE-DSH-ADVERSARIAL-REVIEW.md（:124-389 标题行）
  F-OD01V3-01…12（12 项，标题见 §4 与 Proposal :54-55 / :66-75，逐字一致）

AITutorX @ d13e70d + d9173ab  OD-01-V4-L1-CR-002-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md
  F-OD01V4-01…03（编码单位未钉死 / 50 文件名差异 / 四道门仍 PENDING）
  F-OD01V4R-01…14（:140-490 标题行；-14 = HIGH 治理产物被逐字节复制进 AITutor-X 且从未 commit）

AITutorX @ 5adb1b3  OD-01-V4R-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md
  F-OD01V4R-15…29（15 项）
AITutorX @ 9eb521b  OD-01-V4R-FINAL-VERIFICATION.md
  F-OD01V4R-30…48（19 项）
                                                                合计 = 81
```

## 附录 B — 文件 / 坐标索引

```text
被审对象（AITutors-v3 @ 81b2080，只读）
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md   754 行
  Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md                   149 行
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md                 532 行
  Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md              140 行
  Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md                           99 行（新建）

被引用冻结原文（只读）
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md   548 行（§1 :36-47；§1.2 :60-90；§2 R7/R8；
                                                    §4 :368-383；§5 Rule 1-4 :387-430；§11）
  Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md   276 行（§3.1 :109-122；§3.2 :124-132；
                                                    §5 :157-177；§5.1 :184-203）
  Docs/V3_SPEC/00_Master_Spec.md           §5 非目标 :264-278
  Docs/V3_SPEC/10_Data_Model.md            §4 :105-109；术语登记规则 :100-101；§6.3；§8
  Docs/V3_SPEC/20_Document_Pipeline.md     §5.3 :275-294；§5.5 :308-339（resolution_status :317）；
                                           §6.1；§6.2 :383-399；§7.2 :452-455；§7.3
  Docs/V3_SPEC/50_Migration_Assets.md      :51 表格/图像定位行
  Docs/V3_SPEC/README.md                   §2 术语裁决（权威）:68
  Docs/V3_SPEC/30_Task_LLM_Safety.md       :95（1..n 唯一命中处）

本报告
  Docs/60_REPORTS/OD-01-V4R-FINAL-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md
```

```text
— END OF ADVERSARIAL REVIEW —
审查者：DSH（外部独立验证；未参与 OD-01 任何轮次产出）
本报告即 OD-01-J 所述「DSH 外部验证」。被审方的 Self Review 与 Remediation Report
不得替代或代表本报告，亦不得被引用为 DSH 证据。
```
