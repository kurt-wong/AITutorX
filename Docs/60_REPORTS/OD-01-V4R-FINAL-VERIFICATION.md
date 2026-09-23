# OD-01V4R Final Remediation — DSH Final Verification

```text
Report ID:        DSH-OD-01-V4R-FINAL-VERIFICATION
Report Type:      L3/L4 DSH 最终独立验证（外部）
Report Repo:      kurt-wong/AITutorX  →  Docs/60_REPORTS/
Reviewed Repo:    kurt-wong/AITutors-v3（只读）
Reviewed Commit:  e611a4deb09e21f50278d98dd545e4541c93b19d
Parent:           b6cb762d453bbbd32a1459b2af7aa6860661fcfd
Scope:            (1) F-OD01V4R-15…29 及全链路 Finding 映射真实性
                  (2) Docs/V3_SPEC 未被修改
                  (3) Governance 头块合规（Header/Status/Authority Level/Registration Level/Derives From/Purpose）
                  (4) Proposed Frozen Text 的完整性 / 无矛盾性 / 可直接迁移性
Independence:     本报告作者未参与 OD-01 任何轮次产出；本报告即 OD-01-J 所称「DSH 外部验证」
Date:             2026-09-23
Verdict:          VERIFIED WITH FINDINGS
Closure Blocking: YES
Recommendation:   OWNER ACTION REQUIRED BEFORE CLOSURE
```

> **本报告是审查证据，不是规则来源。** 不修改 `Docs/V3_SPEC/**`、不修改 Frozen Contract、
> 不修改被审四件交付物、不 re-freeze、不标记 OD-01 生效、不执行 Migration、不进入 Phase 1/X3。
> 发现只登记，不修复（AGENTS.md：**Provenance ≠ Quality Authority**）。

> **编号约定**：本报告延续 `F-OD01V4R-xx` 序列（`-30` 起），不新开命名空间。
> 按被审方 §0 `:36` 规则「新问题自 **OD-01F-63** 起递增」，本报告
> `F-OD01V4R-30…48` ⇔ `OD-01F-63…81`。

---

## 0. 审查边界与方法

**审查对象（只读，AITutors-v3 @ `e611a4d`）**

| # | 文件 | 行数 | 本轮变化 |
|---|------|------|----------|
| 1 | `Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md` | 571 | 554 行变更 |
| 2 | `Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md` | 146 | 138 行变更 |
| 3 | `Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md` | 473 | 54 行变更 |
| 4 | `Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md` | 45 | 111 行变更（净删） |

**基准（ground truth）**：本会话先前已提交并推送的四份 DSH 报告（AITutorX）
—— `4b419bf`（F-OD01-01…08）· `8c2dca3`（F-OD01R-01…10）· `1e44017`（F-OD01V3-01…12）·
`d13e70d+d9173ab`（F-OD01V4R-01…14）· `5adb1b3`（F-OD01V4R-15…29）。
**映射真实性只能以这些基线为对照来判定**——本轮检查的第一要务。

**方法**：① 从 AITutorX 报告中机械提取发现标题，与被审方 §0 `Problem` 列**逐行对照**；
② 独立重放 Git/哈希；③ 对四份文件做强制字段与状态词机械扫描；
④ 把 CI-1…CI-12 的 `Proposed Frozen Text` 当作待写入 L0 的正式文本，做**可满足性 / 自洽性 /
可合并性 / 术语登记**四维验算；⑤ 反向检索被删除内容与遗留旧表述。

**未做的事**：未重跑测试基线、未执行四道门、未做 corpus 对比、未修改任何被审文件、未修复发现、
未推送 AITutors-v3。

---

## 1. 四问直答

| # | 问题 | 结论 | 关键依据 |
|---|------|------|----------|
| **Q1** | Finding 映射是否**真实**？有无偷换概念/漏项？ | **否 — 不真实** | 29 行中 **7 行** `Problem` 与 DSH 基准不符（3 行上轮已指出且**原样保留**、4 行**新增偷换**）；`OD-01F-09`/`OD-01F-10` 为**空号**；`F-OD01V3-11`/`F-OD01V3-12` **零命中**；**HIGH 级跨仓复制发现在 60 行表中彻底消失**（§3） |
| **Q2** | `Docs/V3_SPEC` 是否被偷偷修改？ | **否 — 未修改** | `HEAD:Docs/V3_SPEC` = `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f`（与 `b743c5d`/`506ffa8`/`f68aa09`/`2dc7a5e`/`3fa3b73`/`9bd6eca`/`b6cb762` 全链一致）；delta 仅 4 篇文档（§4） |
| **Q3** | Governance 是否合规？（Header/Status/Authority Level/Registration Level/Derives From/Purpose） | **部分合规 — 仍不合规** | 正面：Proposal 与 CR 的 `Purpose`/`Derives From`/`Document ID`/`Normative`/`Supersedes`/`Superseded By` 已齐备。负面：`Authority Level` 值域仍自创；CR `Status` 由合法 `NOT RELEASED` **退化为非枚举值** `NOT REGISTERED`；D1 新附录缺 5 字段；Self Review 缺 4 字段且 Status 退化为 `PENDING`；**Self Review 历史正文被删除**（§5） |
| **Q4** | Proposed Frozen Text 能否**直接进入 Frozen Spec**？ | **部分可以 — 11 个 target 中 3 个不可直接迁移，且遗漏 1 个必需 target** | CI-2 / CI-4 / CI-12 存在自相矛盾、不可判定条款与合并归属缺失；change set **未含 `README.md §2` 术语登记**，而 `10:100-101` 要求「新增术语必须先登记 README §2」（§6） |

```text
四问总评：
  Q1 不通过（治理记录的溯源真实性受损）
  Q2 通过
  Q3 不通过（含一处由合法值→非法值的退化）
  Q4 有条件通过（CI-1/3/5/6/7/8/9/10/11 可迁移；CI-2/4/12 须先修正；缺 README §2 target）
```

---

## 2. Git / 隔离事实（DIRECTLY VERIFIED）

```text
AITutors-v3
  HEAD              = e611a4deb09e21f50278d98dd545e4541c93b19d
  e611a4d^          = b6cb762d453bbbd32a1459b2af7aa6860661fcfd      ✓ 与自述一致
  log -8            = e611a4d → b6cb762 → 9bd6eca → 86da69c → 2dc7a5e → 3fa3b73 → f68aa09 → 506ffa8
  b6cb762..HEAD     = 4 files changed, 423 insertions(+), 434 deletions(-)   ← 净删除 11 行
  name-status       = M × 4（3 × COORDINATION + 1 × REPORTS），无 A / 无 D
  non-doc delta     = 空（无 backend / schema / corpus / alembic 变更）
  HEAD:Docs/V3_SPEC = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f      ✓ 未变
  branch -vv        = * main e611a4d [origin/main: ahead 10]          ✓ 未 push
  untracked         = 9 × Docs/COORDINATION/CONTRACTS/* + Docs/GOVERNANCE/（未动）

AITutor-X（报告仓）
  HEAD = origin/main = 5adb1b3c73c9a6c15a05b61ef82ad8b4e0e7bcbb（上一轮 DSH 报告）
  Docs/COORDINATION/                    → 目录不存在                    ✓ 跨仓副本仍为清除状态
  Docs/60_REPORTS/OD-01-PROPOSAL-V4-…md → 不存在                        ✓
  untracked = 18（与上一轮一致）
```

**Frozen Spec 全链路树哈希（Q2 的直接证据）**

| commit | `Docs/V3_SPEC` tree |
|--------|---------------------|
| `f68aa09` / `2dc7a5e` / `3fa3b73` | `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` |
| `9bd6eca` / `b6cb762` | `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` |
| **`e611a4d`（本轮）** | **`b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f`** ✓ |

---

## 3. Q1 — Finding 映射真实性审计

### 3.1 方法

被审方 §0（`Proposal :34-99`）自称「**唯一完整表**」「含 F-OD01V4R-01 … F-OD01V4R-29」
「历史 Finding 不删除、不重编号、**无空号**」。本报告以 AITutorX 中已提交的四份 DSH 报告
的发现标题为基准，逐行核对 `Problem` 列是否忠实描述该编号原本指向的问题。

### 3.2 V4R 系列（29 行）逐行对照

| ID | DSH 基准（原文标题摘要） | 被审方 `Problem` 列 | 判定 |
|----|--------------------------|---------------------|------|
| -01 | 自审文件被当作独立对抗审查结论使用 | Self Review 冒充 DSH | ✅ 对应 |
| -02 | 本轮唯一新增文档缺 `90 §4` 强制 Status Header | Header 字段不全 | ✅ 对应 |
| -03 | 禁用状态词修复不成立（`COMPLETE`/`NEXT`） | 状态词 | ✅ 对应 |
| -04 | CI-4 的 Proposed Text 内部自相矛盾 | locator 冲突 | ✅ 对应 |
| -05 | 字段重命名未进入 change set | resolution 双名 | ✅ 对应 |
| -06 | 规范字段 `Authority Level` 被改名/替换 | Authority Level | ✅ 对应 |
| -07 | ID Mapping 表不完备且存在错配 | ID Mapping | ✅ 对应 |
| -08 | **引入第 7 套命名空间，`R-xx` 语义无定义** | **降级态夹带** | ❌ **不符（上轮已指出，本轮原样保留）** |
| -09 | **Gap 结论两版并存；`90:47` 未归层后果未登记** | **table_cell identity 草率** | ❌ **不符（同上）** |
| -10 | **新文档违反 `90 §5 Rule 2`（禁止词升级）** | **char offset 未定** | ❌ **不符（同上）** |
| -11 | **新增文档的 `Path` 字段指向另一个仓库** | DSH 外部登记：治理映射/表述收口不足 | ❌ **不符（本轮新偷换）** |
| -12 | **「Current Rule」块保真度参差且未标注逐字/改写** | DSH 外部登记：注册条件与 Gap 用语冲突 | ❌ **不符（本轮新偷换）** |
| -13 | **CI-12 与 CI-4 声明「同文」但实际不同文** | DSH 外部登记：Header 字段名/缺 Purpose | ❌ **不符（本轮新偷换）** |
| -14 | **（HIGH）治理产物被逐字节复制进 AITutor-X 且从未 commit** | DSH 外部登记：Authority 值域自定义 | ❌ **不符（本轮新偷换，最严重）** |
| -15 | 映射错配 3 行、缺失 4 项、空号 2 个 | Finding→Fix 映射错配/缺失 | ✅ 对应 |
| -16 | Gap 未修复却被映射到无关 Fix | Governance Gap 双向表述 | ✅ 对应（覆盖面见 F-OD01V4R-45） |
| -17 | `Purpose` 从 Proposal/CR 头块消失 | Header 缺 Purpose；来源字段名错误 | ✅ 对应 |
| -18 | `Authority Level` 值域被自创 | Authority Level 混用 | ✅ 对应 |
| -19 | 状态词换词未归位；OD-01-H 引错章节 | 状态词 / 引用 §3.2 | ✅ 对应 |
| -20 | change set 要求 `table_id` 而 L0 无该实体且明令不授权 | table_id 写成已有事实 | ◐ 相关但**不等价**（漏「无生产者/不可满足」的一面） |
| -21 | 5 个 CI 丢失 `Current Rule` | CI 缺 Current Rule | ✅ 对应 |
| -22 | CI-4 的「逐字」并非逐字；字段名证据被移出 | CI-4 verbatim/summary 混用 | ✅ 对应 |
| -23 | form 用语与 OD-01 绑定用语脱钩且无对照表 | form 双体系无解释 | ✅ 对应 |
| -24 | Self Review 头块围栏损坏且缺 5 个强制字段 | Self Review 格式 | ✅ 对应 |
| -25 | 破引用 + 跨仓路径残留 | 外仓路径引用 | ◐ 只覆盖 Path，**未覆盖破引用**（破引用本轮已修，见 P8） |
| -26 | 机械替换痕迹 `PENDING = Owner Review` | 机械替换痕迹 | ✅ 对应 |
| -27 | `Derived From` 应为 `Derives From` | 来源字段名不统一 | ✅ 对应 |
| -28 | `APPROED` 拼写错误 + 多版本号并存 | 拼写/多 Current | ✅ 对应 |
| -29 | 新引入非冻结分类词 `Future *` | Future 词当 Status | ✅ 对应 |

```text
V4R 系列统计（29 行）：
  完全对应       22
  部分对应        2（-20、-25）
  明确不符        7（-08、-09、-10 沿用上轮错配；-11、-12、-13、-14 本轮新增偷换）
```

### 3.3 关键后果：HIGH 级发现在治理记录中消失

```text
F-OD01V4R-14 =（HIGH）治理产物被逐字节复制进 AITutor-X，违反 AGENTS.md 明列禁止项
  —— 该问题在 60 行映射表（`:40-99`）中**没有任何一行**描述它：
      含 AITutorX / AITutor-X / 跨仓 / 副本 / 复制 语义的行 = 0
      「外仓路径引用」（-25 / OD-01F-58）只描述 Path 字段，不是内容复制
  —— 而其实际修复（AITutor-X 副本已清除）也**未被登记**为任何 Final ID 的 Fix
```

同时产生 **4 组重复描述**（同一问题被记在两个 Final ID 下）：

| 描述 | 出现在 | 也出现在 |
|------|--------|----------|
| 治理映射/表述收口 | -11 → OD-01F-44 | -15 → OD-01F-48 |
| Gap / 注册用语 | -12 → OD-01F-45 | -16 → OD-01F-49 |
| Header 缺 Purpose | -13 → OD-01F-46 | -17 → OD-01F-50 |
| Authority 值域 | -14 → OD-01F-47 | -18 → OD-01F-51 |

**后果**：`§0` 被判 VERIFIED（OD-01F-48，「重建唯一 Mapping Table」），但其 `Problem` 列
对 7 个编号失真、对 1 个 HIGH 问题零登记、并制造 4 组重复。
一份不能忠实重建历史的映射表，不能充当治理溯源的权威载体
（AGENTS.md：**Provenance ≠ Quality Authority**；**UNKNOWN is retained data**）。

### 3.4 空号与漏项

```text
空号（§0 `:36` 明确宣称「无空号」，实测为假）：
  Final ID 列覆盖 OD-01F-01…08、**11**…20、21…30、31…33、34…62
  → OD-01F-09 = 0 命中；OD-01F-10 = 0 命中      （上一轮 F-OD01V4R-15 已指出，本轮未修）

漏项（表头称「唯一完整表」+「历史 Finding 不删除」，实测为假）：
  F-OD01V3-11 = 0 命中；F-OD01V3-12 = 0 命中
  → v3 系列（DSH `1e44017`）实际登记 **12** 项，本表仅纳入 10 项（F-OD01V3-01…10 → OD-01F-21…30）
  → F-OD01V3-11（`10 §4` 引文保真）与 F-OD01V3-12（UTF-8 BOM 字节改动）**连续第三轮未登记**
```

### 3.5 V3 系列 `Problem` 列抽样核对

| ID | DSH 基准 | 被审方 `Problem` | 判定 |
|----|----------|------------------|------|
| F-OD01V3-01 | 条款级 Proposed Frozen Text 全数消失 | v3 缺完整基线/diff | ◐ 与 -02 混同 |
| F-OD01V3-02 | v2 完整现状基线表被删除 | 缺 Proposed Frozen Text | ◐ 与 -01 互换 |
| F-OD01V3-03 | `DONE` 作为状态值大面积使用 | CR-002 定位误解 | ❌ 不符 |
| F-OD01V3-04 | Governance Gap 混淆候选落位与正式注册 | 状态词不合规 | ❌ 不符（那是 -03） |
| F-OD01V3-07 | 字段命名冲突以「删除该字段」规避 | 只写 Artifact 路径 | ❌ 不符 |
| F-OD01V3-08 | 新引入 `91 §3.1` 误引 ×3 | fail-closed 多字段 | ❌ 不符 |
| F-OD01V3-06 / -09 / -10 | degraded 无槽位 / ID 空间三分 / `Authority Level: L1` 矛盾 | 对应描述 | ✅ |

```text
V3 系列 10 行中：明确不符 4 行（-03/-04/-07/-08），互换/混同 2 行（-01/-02）
```

### 3.6 Q1 结论

**映射不真实。** 具体为：V4R 系列 7/29 行 `Problem` 失真（含 3 行上轮已指出未修 + 4 行新增偷换）、
1 个 HIGH 发现在表内消失、4 组重复描述、2 个 ID 空号、2 项历史发现漏登；
V3 系列另有 4 行不符。**「VERIFIED」在映射层不可采信。**

---

## 4. Q2 — `Docs/V3_SPEC` 未被修改（通过）

```text
HEAD:Docs/V3_SPEC = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
  与 f68aa09 / 2dc7a5e / 3fa3b73 / 9bd6eca / b6cb762 完全一致
b6cb762..HEAD name-status = 4 files（M），无一在 Docs/V3_SPEC/
全仓无 backend / frontend / alembic / migrations / corpus 变更
ahead 10（未 push）
```

**判定：通过。** 本轮及此前全部轮次均未改动 Frozen Spec；
`OD-01 as Frozen Spec = NOT EFFECTIVE` 与实际状态一致。

---

## 5. Q3 — Governance 合规审计

### 5.1 强制字段矩阵（`90 §4:373-380` + `91 §5:162-177`）

| 字段 | Proposal v4R | CR-002 | D1 新附录 `:431-441` | Self Review |
|------|--------------|--------|----------------------|-------------|
| `Document ID` | ✅ `:4` | ✅ `:4` | ❌ | ❌ |
| `Title` | ✅ | ✅ | — | — |
| `Document Type` | ✅ Decision Record（枚举内） | ✅ Contract Change Record（枚举内） | ✅ Decision Record | ✅ Report |
| `Status` | ✅ `PENDING`（`91 §3.1` 枚举内） | ❌ **`NOT REGISTERED`**（枚举外，且替换掉合法的 `NOT RELEASED`） | ❌ `PENDING EFFECTIVE FREEZE`（枚举外） | ❌ `PENDING`（历史文档应为 `HISTORICAL`） |
| `Normative` | ✅ `NO` | ✅ `NO` | ❌ | ❌ |
| `Purpose` | ✅ `:8`（本轮已补） | ✅ `:8`（本轮已补） | ✅ `:434` | ✅ `:6` |
| `Derives From` | ✅ `:12`（拼写已修） | ✅ `:12` | ✅ `:437` | ⚠️ `:9` 值为「Proposal v4（Previous Revision）自查」——描述而非文档闭包 |
| `May Change` | ✅ | ✅ | ✅ | ✅ |
| `Must Not Change` | ✅（含 L0） | ✅（含 L0） | ✅（含 L0） | ✅（含 L0） |
| `Supersedes` | ⚠️ 值写成「Previous Revision: Proposal v4」（应为文档清单或 `—`） | ⚠️ 同左 | ❌ | ❌ |
| `Superseded By` | ✅ `—` | ✅ `—` | ❌ | ❌ |
| `Gate State Authority` | ✅ `NO` | ✅ `NO` | ❌ | ✅ `NO` |
| `Authority Level` | ❌ `Proposal Authority`（枚举外） | ❌ `Change Record Authority`（枚举外） | ❌ `Decision Authority`（枚举外） | ❌ `Proposal Authority`（且层级错误） |
| `Registration Level`（非规范字段） | ⚠️ `NOT REGISTERED` | ⚠️ `NOT REGISTERED` | ⚠️ `NOT REGISTERED` | ⚠️ `NOT REGISTERED` |

**枚举依据（冻结）**

```text
90 `:375` / 91 `:167`  Authority Level: <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>（91 另含 L2-proposed）
90 `:376` / 91 `:168`  Status: <ACTIVE | SUPERSEDED | HISTORICAL | DRAFT | CLOSED | NOT RELEASED>
91 `:109-122` §3.1     允许状态值 = OPEN / PENDING / CONDITIONAL PASS / CLOSED / NOT STARTED /
                       DEFERRED / SUPERSEDED / RETRACTED / ACTIVE / HISTORICAL
91 `:196`              门槛 3：Authority Level ∈ 已定义层级；**不得自创层级**
91 `:195`              门槛 2：出生证明齐备——缺字段即不得创建
90 `:81`               `Docs/REPORTS/` = L3 / L4 / L2-proposed
```

### 5.2 关键退化：CR-002 的 `Status`

```text
上一版本（b6cb762）  CR-002 `Status: NOT RELEASED`   ← `90 §4:376` / `91 §5:168` 枚举内 ✅
本版本  （e611a4d）  CR-002 `Status: NOT REGISTERED` ← **不在任何冻结枚举内** ❌
                   （文件同时保留正文短语 "NOT REGISTERED AS L1" `:41`，该短语本身可用；
                     但把它填进 `Status` 字段即越出枚举）
```

**这是在以治理合规为目标的轮次中，用一个合法值替换为非法值。** 上一轮本报告
（F-OD01V4R-19）已指出同族的「换词未归位」，本轮不但未收敛，反而在 CR 的
`Status` 字段上新增一处枚举外取值。

### 5.3 状态词宣称与实测

```text
Proposal `:23`：「状态词仅用 91 §3.1 Allowed Status 词汇（本记录族实用集：
                APPROVED / PENDING / VERIFIED / NOT EFFECTIVE / NOT REGISTERED）」
Proposal `:147`：同一声称
实测（大小写敏感，四文件）：
  PENDING        在 91 §3.1 ✅
  APPROVED       不在 91 §3.1、不在 90 §4:376     → 实测 2 / 1 / 40 / 0
  VERIFIED       不在 91 §3.1、不在 90 §4:376     → 实测 62 / 1 / 37 / 0
  NOT EFFECTIVE  不在 91 §3.1、不在 90 §4:376     → 实测 5 / 4 / 3 / 0
  NOT REGISTERED 不在 91 §3.1、不在 90 §4:376     → 实测 8 / 8 / 2 / 1
```

**「仅用 `91 §3.1` 词汇」为假陈述**：实用集 5 词中仅 1 词合法。
`OD-01F-52`（`Status 仅用 91 §3.1 允许词`）标 VERIFIED 无据。

### 5.4 Self Review 文档

```text
正面：Title `:1` 与 `:16-19` 明确「Historical Self Review = 内部检查；不是 DSH Review；
      禁止引用本文档作为外部证据」；`Kind | Historical Self Review`；`DSH Review | NOT THIS DOCUMENT`
负面 1：`Status: PENDING`（`:5`、`:45`）—— 上一版本为 `HISTORICAL`（`91 §3.1:122`「历史记录，非现行」），
        本轮改为 `PENDING`（`91 §3.1:118`「等待外部条件」）。该文档显然是历史记录，不是等待条件者。
        这是把一个**正确且合法的枚举值**换成了一个语义错位的值。
负面 2：头块仍缺 `Document ID` / `Normative` / `Supersedes` / `Superseded By`（4 项，`90 §4` 强制）
负面 3：`Authority Level: Proposal Authority` —— 该文档位于 `Docs/REPORTS/`（`90:81` = L3/L4），
        填「Proposal Authority」既非层级也非其所在层
负面 4：**历史正文被删除**（见下）
```

**历史正文删除（逐字节实测）**

```text
b6cb762 版本：108 行，含完整历史正文（原 v4 自审全文，`:20-108`）
e611a4d 版本： 45 行，历史正文压缩为 6 行摘要块（`:25-30`）+ 1 行检查项摘要（`:32`）

原始结论字符串存活情况：
                        b6cb762   e611a4d
  CLOSURE BLOCKING         1         0
  READY FOR OWNER REVIEW   1         0
  VERIFIED WITH FINDINGS   3         0
  F-OD01V4-01              2         1

同一文件 `:19` 仍声明：「（历史正文保留（不删除）」
AGENTS.md 禁止行为：「不删除旧文档」；`90 §2 R8`：「废止必须可传播…1. **保留正文**
（历史审计证据，不得改写或删除）」
```

内容尚可由 git 历史（`9bd6eca` / `b6cb762`）恢复，但**当前树内已不含该历史正文**，
而文件自称保留之。这直接削弱 F-OD01V4R-01（自审边界）的原始证据留痕。

### 5.5 Q3 结论

**部分合规。** 正面：`Purpose`、`Derives From`、`Document ID`、`Normative`、
`Supersedes`、`Superseded By` 在 Proposal 与 CR 中已齐备（上一轮 F-OD01V4R-17/-27 的主体已修）。
负面：`Authority Level` 值域仍自创（3 处 + 自审档层级错误）、CR `Status` 退化为枚举外值、
状态词合法率 1/5、D1 新附录缺 5 字段、Self Review 缺 4 字段且 Status 语义错位、
历史正文被删除。**判定：不合规，须修。**

---

## 6. Q4 — Proposed Frozen Text 能否进入 Frozen Spec

> 这是本轮最关键的问题。判定标准三项：**完整性**（是否覆盖全部必改点）、
> **无矛盾性**（写入后 L0 是否自洽）、**可直接迁移**（逐字复制即可，无需再设计）。

### 6.1 完整性

| 检查项 | 结论 |
|--------|------|
| 11 个既定 target 是否都在 | ✅ `00 §5` / `10 §4` / `10 §6.3` / `10 §8` / `20 §5.3` / `20 §5.5` / `20 §6.1` / `20 §6.2` / `20 §7.2` / `20 §7.3` / `50` bbox 行 |
| 每个 CI 是否六段结构 | ✅ CI-1…CI-12 全部含 `Current Rule`（并标 verbatim/summary）→ 上一轮 F-OD01V4R-21/-22 主体已修 |
| **术语登记 target** | ❌ **缺失**：`10:100-101` 明文「枚举值与 JSON 内字段名以 `README.md` §2 与 20/30 schema 为准；**新增术语必须先登记 README §2 再在本 schema 使用**」；`README.md:68` §2 标题为「**术语裁决（权威）**」。本轮引入 `span_resolution` / `option_evidence_status` / `form` 等新术语，而 README 中 `span_resolution`=0、`option_evidence_status`=0、`form`=0、`line_range`=0、`char_span_in_line`=0 命中 → **change set 未把 `README.md §2` 列为 Target/Affected** |
| `20:317` JSON 示例改写 | ❌ 未提供（见 6.2-D） |

**判定（完整性）：不完整。** 至少缺 `README.md §2` 一个必需 target；
且采纳后触发 `90 §2 R6`「被 ≥2 份文档使用的架构术语必须有冻结定义…**使用未定义术语立规 = 违规**」。

### 6.2 无矛盾性（逐项验算）

**A. CI-4：`form` 与 `granularity` 声称「正交」，却共用值名 → 自相矛盾**

```text
CI-4 Proposed（`:295-300`）：
  - `granularity` ∈ {line, line_character}（M1；fragment 延后，见 00 §5）。
  - Resolved Span 增加 provenance form 维度（与 granularity 正交）：
    form ∈ {line, line_character, table_cell, multiple_source_spans, other}。
```

「正交」意味着两维取值互不相关；但 form 的取值 `line` / `line_character` **与被声明正交的
granularity 值域完全同名**。采纳后，L0 将同时存在 `granularity=line_character` 与
`form=line_character` 两个同名不同层的概念，而文本未给出二者的区分规则（例如是否允许
`granularity=line` 搭配 `form=table_cell`）。**这正是上一轮 F-OD01V4R-23 的修复
（把 form 名改为 `line`/`line_character` 以对齐 L0 用语）所引入的新矛盾。**
→ 不满足「可直接迁移」。

**B. CI-4：无条件 `line_ref` 与 `table_cell → line_ref 可选` 并存**

```text
`:296`  - line_ref 必须存在于该 source_version；line_character 的 start/end_offset 为 …
`:305`      table_cell → 可验证 table cell 定位必需（identity 形状另案对齐），line_ref 可选；
`:308`    禁止要求一切 form 具备 line_ref；…
```

`:296` 是无条件规范句，`:305` 对其作了例外，`:308` 提供一般性软化——三者未声明优先级，
且 `:296` 保留 L0 原文措辞未加限定词。逐字写入后，L0 §5.5 内将并存两条互相覆盖的规范。
→ 不满足「可直接迁移」（须把 `:296` 限定为 `line / line_character：…`）。

**C. CI-2 / CI-4 / §5：`table_cell` 强制要求无判定标准 + 含元陈述**

```text
CI-2 `:249-250`：option provenance 的 table_cell 必须具备可验证定位；identity 形状与 Frozen Spec
                 对齐前不得声称具体表标识已存在。本条不授权数据库 schema 变更。
CI-4 `:305`：    table_cell → 可验证 table cell 定位必需（identity 形状另案对齐）
§5   `:200-206`：Planning Category: Future Required Change
                 table_cell identity requires future Frozen Spec alignment
                 不得声称 table_id 已存在 … 具体 identity 形状待与 Frozen Spec 对齐后另案写入 Change Set
```

三点问题：
1. **不可判定**：`table_cell` 定位被设为强制（且 `resolved` 依赖它），但「可验证」的判定
   标准（identity 形状）被推迟到未来变更 → L0 将含一条**无法判定是否满足**的强制条款。
2. **元陈述进入 L0**：Frozen Spec 定义系统事实，不应承载「identity 形状与 Frozen Spec 对齐前
   不得声称…」这类**关于自身未来修订的流程条件**。
3. **`90 §5 Rule 4`（Ownership Matrix）**：「指不出唯一生产者的字段 **= 治理缺口**，进台账」。
   `table_id` 仍无生产者，而本轮既未登记进 `84_CONFLICT_LEDGER`，也未把它列为
   change set 的 Target（只列为 Future Required Change）。
   → 上一轮 F-OD01V4R-20 由「断言 table_id 存在」改为「推迟 identity 形状」，
   但**「不可满足」的实质未消除**，只是从 L0 内部矛盾转为 L0 内不可判定条款。

**D. `20:317` 的字段名未同步改写**

```text
L0 现状 `20_Document_Pipeline.md:317`：  "text_hash": "<sha256>", "resolution_status": "exact",
CI-4 仅有一句：`解析字段唯一命名：span_resolution。`（`:309`），**未给出改写后的示例**
→ 若迁移者逐字复制 CI-4 文本而不额外编辑示例 JSON，L0 将同时含 `resolution_status`（§5.5 示例）
  与 `span_resolution`（§6.2 新文本）→ **「两名一义」**，即上一轮 F-OD01V4R-05 想消除的形态。
```

**E. CI-4 与 CI-12 同时修改 `20 §5.5`，无合并文本与插入位置**

```text
CI-4  `:279-313`：Affected = `20 §5.5`；`10 §8`（新增 form / locator / 命名段落）
CI-12 `:457-476`：Affected = `20 §5.5`（新增 image_region 段落）
两者均只给增量拟制文本，未声明合并后的 §5.5 全文、插入顺序或相互引用关系
→ 迁移者必须自行设计合并结果 → 不满足「可直接迁移」（上一轮 -13「同文」表述虽已删除，问题实质保留）
```

**F. 术语双体系（已修复，供对照）**

```text
§3.1 `:156-164` 给出 Producer/P04 用语 → L0 form 名 的对照表（line_range→line 等）✅
但该对照表本身未被列入 change set 的任何 Target（它位于 Proposal 正文，不是拟制 L0 文本）；
CI-4 内虽含一行「Producer 用语映射：line_range → line；char_span_in_line → line_character。」
→ 若该行进入 L0，等于把 Producer 别名写入 L0（可接受但需 Owner 明示）；
   若不进入 L0，则对照关系只存在于 Proposal，L0 中不再有 `char_span_in_line` 的落点。
```

### 6.3 可直接迁移性逐项判定

| CI | Target | 判定 | 阻碍 |
|----|--------|------|------|
| CI-1 | `00 §5` | ✅ 可迁移 | — |
| **CI-2** | `10 §4` | ⚠️ **须先修正** | 不可判定条款 + 元陈述（6.2-C） |
| CI-3 | `20 §5.3` | ✅ 可迁移 | — |
| **CI-4** | `20 §5.5` | ❌ **不可直接迁移** | 正交声明与同名值（6.2-A）+ 无条件 `line_ref`（6.2-B）+ 示例未改写（6.2-D）+ 合并归属（6.2-E） |
| CI-5 | `20 §6.1` | ✅ 可迁移（附加段） | — |
| CI-6 | `20 §6.2` | ✅ 可迁移 | — |
| CI-7 | `20 §7.2` | ✅ 可迁移 | — |
| CI-8 | `20 §7.3` | ✅ 可迁移 | — |
| CI-9 | `10 §6.3` | ✅ 可迁移 | — |
| CI-10 | `10 §8` | ✅ 可迁移 | — |
| CI-11 | `50` bbox 行 | ✅ 可迁移（整行替换） | — |
| **CI-12** | `20 §5.5` | ⚠️ **须先修正** | 与 CI-4 的合并归属（6.2-E） |
| **（缺）** | `README.md §2` | ❌ **须补 target** | `10:100-101` 术语登记前置要求（6.1） |

### 6.4 Q4 结论

**部分可以。** 11 个 target 中 **9 个可直接迁移**（CI-1/3/5/6/7/8/9/10/11），
**3 个须先修正**（CI-2、CI-4、CI-12），**1 个 target 缺失**（`README.md §2`）。
其中 CI-4 的问题最重：它同时含一处**自相矛盾**（正交 vs 同名值）、一处**双规范并存**、
一处**未同步改写的示例**，并且与 CI-12 存在**未定义的合并关系**。
**结论：现在不能安全进入 Frozen Spec；修正上述 4 点后可。**

---

## 7. 发现（F-OD01V4R-30 … F-OD01V4R-48）

> 全部只登记，不修复。⇔ `OD-01F-63 … OD-01F-81`（按被审方 §0 `:36` 递增规则）。

| ID | 级别 | 内容 | 对应 Final ID |
|----|------|------|---------------|
| **F-OD01V4R-30** | **HIGH** | 映射表偷换概念：`-11…-14` 四行 `Problem` 与 DSH 基准不符（-11 实为 Path 错仓、-12 实为 Current Rule 保真、-13 实为 CI-12/-4 同文、-14 实为 **HIGH 级跨仓逐字节复制**），造成 4 行失真 + 4 组重复描述，且 **HIGH 级跨仓复制发现在 60 行表中零登记** → 治理记录溯源擦除 | OD-01F-63 |
| **F-OD01V4R-31** | **HIGH** | 上一轮已指明的 3 行错配（`-08/-09/-10`）**原样保留**，却同轮宣告 `OD-01F-48`（「重建唯一 Mapping Table」）VERIFIED | OD-01F-64 |
| **F-OD01V4R-32** | **MED-HIGH** | 映射表仍不完整：`OD-01F-09`/`OD-01F-10` **空号**（`§0 :36` 称「无空号」为假）；`F-OD01V3-11`/`F-OD01V3-12` **零命中**（v3 系列实为 12 项，表内仅 10 行）；表头称「唯一完整表」「历史 Finding 不删除」为假 | OD-01F-65 |
| **F-OD01V4R-33** | **MED-HIGH** | change set 遗漏 `README.md §2` target：`10:100-101` 要求「新增术语必须先登记 `README §2` 再在本 schema 使用」，`README:68` §2 自称「术语裁决（权威）」；新术语 `span_resolution`/`option_evidence_status`/`form` 在 README 中 0 命中 → 采纳即违反 L0 自身规则与 `90 §2 R6`（使用未定义术语立规 = 违规） | OD-01F-66 |
| **F-OD01V4R-34** | **MED-HIGH** | CI-4 拟制文本自称 `form` 与 `granularity` **正交**，却令 `form ∈ {line, line_character, …}` 与 granularity 值域**同名**，且未给区分规则 → 写入后 L0 出现自相矛盾的二维模型 | OD-01F-67 |
| **F-OD01V4R-35** | MED | CI-4 内并存两条互相覆盖的规范（无条件 `line_ref 必须存在于该 source_version` vs `table_cell → line_ref 可选`），无优先级声明 | OD-01F-68 |
| **F-OD01V4R-36** | **MED-HIGH** | `table_cell` 强制条款**无判定标准**且含元陈述（identity 形状推迟到 Future Required Change）；`90 §5 Rule 4` 要求无生产者的字段进台账，本轮未登记进 `84` | OD-01F-69 |
| **F-OD01V4R-37** | MED | CI-4 与 CI-12 同时修改 `20 §5.5`，均只给增量文本，未给合并后文本/插入位置 → 迁移者须自行设计合并 | OD-01F-70 |
| **F-OD01V4R-38** | MED | `20:317` 的 JSON 示例未同步改写，CI-4 仅以一句「解析字段唯一命名：span_resolution」指示 → 逐字复制后 `resolution_status` 与 `span_resolution` 仍并存 | OD-01F-71 |
| **F-OD01V4R-39** | **MED-HIGH** | CR-002 `Status` 由合法 `NOT RELEASED`（`90 §4:376` 枚举内）改为**枚举外值** `NOT REGISTERED` → 本轮在治理合规目标下移除合法值并引入非法值；`Effective: NOT EFFECTIVE` 亦为非规范字段+枚举外值 | OD-01F-72 |
| **F-OD01V4R-40** | **MED-HIGH** | `Authority Level` 值域仍自创（`Proposal Authority` / `Change Record Authority` / `Decision Authority`），`91 §5.1:196`「不得自创层级」未满足；Self Review（`Docs/REPORTS/` = L3/L4）填 `Proposal Authority`，与其所在层级不符 | OD-01F-73 |
| **F-OD01V4R-41** | MED | 「状态词仅用 `91 §3.1`」为假陈述：实用集 5 词中仅 `PENDING` 合法；实测 `VERIFIED` 62/1/37/0、`APPROVED` 2/1/40/0、`NOT REGISTERED` 8/8/2/1、`NOT EFFECTIVE` 5/4/3/0 | OD-01F-74 |
| **F-OD01V4R-42** | MED | D1 新附录 `:431-441` 缺 `Document ID`/`Normative`/`Supersedes`/`Superseded By`/`Gate State Authority`（5 项）；`Status: PENDING EFFECTIVE FREEZE` 与 `Authority Level: Decision Authority` 均非枚举值 | OD-01F-75 |
| **F-OD01V4R-43** | MED | Self Review 头块缺 `Document ID`/`Normative`/`Supersedes`/`Superseded By`（4 项）；`Status` 由合法的 `HISTORICAL` 改为语义错位的 `PENDING`；`Derives From` 值为描述而非文档闭包 | OD-01F-76 |
| **F-OD01V4R-44** | MED | Self Review **历史正文被删除**（108 → 45 行；`CLOSURE BLOCKING` 1→0、`READY FOR OWNER REVIEW` 1→0、`VERIFIED WITH FINDINGS` 3→0），而同一文件 `:19` 仍声明「历史正文保留（不删除）」→ 文档陈述与事实不符；与 AGENTS.md「不删除旧文档」及 `90 §2 R8`「保留正文（历史审计证据，不得改写或删除）」冲突（内容仅存于 git 历史） | OD-01F-77 |
| **F-OD01V4R-45** | LOW-MED | F-OD01V4R-16 仅完成一半：D1 `:315` 仍保留「（Owner 接受的 **Gap 路径**）」标题，与 Proposal §9 `:526`／CR §0 `:57` 的「不是没有 L1 落点」并存；`未归层`（`90:47`）在四文件中**第四轮仍 0 命中** | OD-01F-78 |
| **F-OD01V4R-46** | LOW | 非规范头字段持续增列：`Registration Level` / `Effective` / `Current Version` / `Related Records` / `Change Record ID` / `Audit ID`；`Supersedes` 值写成「Previous Revision: X」（`90 §4:378` 期望文档清单或 `—`） | OD-01F-79 |
| **F-OD01V4R-47** | LOW | 映射表 `Problem` 列对 v3 系列亦有 4 行不符（`-03/-04/-07/-08`）与 2 行互换（`-01/-02`） | OD-01F-80 |
| **F-OD01V4R-48** | LOW | D1 `:405-409` 的 OD-01-J 流程块仍写「Proposal v4 → DSH 复核」，与 `:400`／`:452` 的「v4R → DSH 外部验证」不一致（同文件两版流程） | OD-01F-81 |

---

## 8. 正面证实（P1–P16）

| # | 正面事实 |
|---|----------|
| P1 | **Frozen Spec 未被修改**（Q2 通过）：`b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` 在七个提交上完全一致 |
| P2 | **隔离干净**：`b6cb762..HEAD` = 4 files（3 × COORDINATION + 1 × REPORTS），全仓零 backend/schema/corpus 变更；`ahead 10` 未 push |
| P3 | **Proposal 与 CR 的出生证明已齐备**：`Document ID` / `Title` / `Document Type` / `Status` / `Purpose` / `Authority Level` / `Registration Level` / `Normative` / `Derives From` / `May Change` / `Must Not Change` / `Related Records` / `Supersedes` / `Superseded By` / `Gate State Authority` 全部存在（上一轮 F-OD01V4R-17 主体已修） |
| P4 | **`Purpose` 字段已恢复**（Proposal `:8`、CR `:8`、D1 `:434`、Self Review `:6`），且 `Derived From` 拼写已统一为 `Derives From`（四文件 `Derived From` = 0） |
| P5 | **禁用状态词已清除且保持**：`DONE` / `COMPLETE` / `COMPLETED` / `NEXT` / `FINISHED` / `ADDRESSED` / `resolution_status` 四文件 0 命中（D1 唯一 `COMPLETE` 为 L0 引语 `INCOMPLETE` 的子串） |
| P6 | **外仓路径与破引用已清除**：`Docs/60_REPORTS` = 0、`SELF-REVIEW.md` = 0、`APPROED` = 0；Proposal `:15` 的 `Related Records` 指向真实存在的 `Docs/REPORTS/…` |
| P7 | **Self Review 边界声明到位且强化**：`Kind = Historical Self Review`、`DSH Review = NOT THIS DOCUMENT`、`:16-19` 显式「不是 DSH Review／外部验证／禁止引用为外部证据」；Proposal `:28`、CR `:112-115`、D1 `:452-453` 四处同向 |
| P8 | **上一轮 HIGH（跨仓副本）的实质修复保持**：AITutor-X `Docs/COORDINATION/` 目录不存在、REPORTS 副本不存在、untracked 仍为 18 |
| P9 | **CI-1…CI-12 六段结构恢复**（上一轮 F-OD01V4R-21/-22 主体已修）：每项均含 `Current Rule`，并逐项标注 **verbatim** / **summary**；CI-4 的 verbatim 块已去掉自加行并恢复 L0 第二 bullet |
| P10 | **form 术语对照表建立**（上一轮 F-OD01V4R-23 主体已修）：§3.1 给出 `line_range→line`、`char_span_in_line→line_character` 等映射，并声明「Change Set 统一采用 L0 form 名」 |
| P11 | **`table_id` 不再被声称为已存在事实**（上一轮 F-OD01V4R-20 的表述面已修）：改为 `Planning Category: Future Required Change`，明文「不得声称 `table_id` 已存在」「不授权 schema 变更」 |
| P12 | **`span_resolution` 唯一命名保持**：Proposal §2.2 · CI-4 · CI-6 · CI-9 四处一致；`resolution_status` 全文 0 命中 |
| P13 | **字符偏移单位保持已选定**：Unicode code point / 行内 0-based / start inclusive / end exclusive（§3.3 + CI-4 `:296-298`），且「不留待决」 |
| P14 | **Planning Category 与 Status 分离**：§10 明确 `Future Required Change` / `Future Consideration` 「**不是 Status**。不得填入 Status 字段」→ 上一轮 F-OD01V4R-29 的方向已被采纳 |
| P15 | **CHANGE-4/5 保留四道门**：Proposal `:500-511`、CR `:97`、Gate A–D 全 `PENDING`；未以文档完成替代 Gate PASS |
| P16 | **历史决策与历史正文（除 Self Review 正文外）未被改写**：D1 保留 OD-01R 原节并**追加**新附录；未重编号历史 Decision；`84`/`Frozen Contract`/P01–P25 未触碰 |

---

## 9. 局限（L-1 … L-7）

- **L-1** 未重跑测试基线、未执行四道门、未做 corpus 对比；本报告不对 Gate A–D 的最终结论作预判。
- **L-2** Q1 的判定以**本会话已提交的 DSH 报告**为基准（AITutorX `4b419bf`/`8c2dca3`/`1e44017`/
  `d13e70d`+`d9173ab`/`5adb1b3`）。若被审方主张其 `Problem` 列使用的是另一套编号定义，
  该定义**未随本轮提交**，故本报告按已提交基线判定。
- **L-3** `git fetch` 不可用，`origin/main` 比较基于本地引用；AITutors-v3 依令未推送
  （本地 `ahead 10`），其远端状态未核验。
- **L-4** 本会话 `pwsh` 沙箱无法初始化（`SetNamedSecurityInfoW failed (Win32 5)`），所有命令在
  `danger-full-access` 下执行且**全部为只读命令**；未对 AITutors-v3 写入任何字节。
- **L-5** §6 的验算是**文本层可满足性推演**（把 CI-1…CI-12 当作已采纳的 L0 文本检查自洽性），
  不是实现/schema 验证；未核验 `backend/Docs/V3_SPEC/` 下 JSON 语料与
  `docs_audit/authority_matrix.yaml`。
- **L-6** `README.md` 位于 `Docs/V3_SPEC/`，本报告依据 `10:100-101` 与 `README:68` 认定其为
  术语登记权威点；若 Owner 认定 README 不属于 L0 冻结面，F-OD01V4R-33 的定性应从
  「违反 L0 规则」下调为「change set 不完整」，但**须补 target** 的结论不变。
- **L-7** F-OD01V4R-44 中「历史正文被删除」的结论基于 b6cb762 与 e611a4d 两版逐行对比与关键字
  计数；未逐一 diff 全部 108 行以确认无其他搬运位置（`Docs/ARCHIVE/` 未检索）。

---

## 10. 最终判定

```text
OD-01V4R Final Remediation（e611a4d）
  = VERIFIED WITH FINDINGS

四问结论：
  Q1 Finding 映射真实性        → 不通过（7/29 行失真；1 个 HIGH 零登记；2 空号；2 项漏登）
  Q2 Docs/V3_SPEC 未改         → 通过（b3eeb3e9… 全链路一致）
  Q3 Governance 合规           → 不通过（Authority 值域自创；CR Status 合法值→非法值；
                                  D1/Self Review 头块缺字段；Self Review 历史正文被删）
  Q4 Proposed Text 可直接迁移  → 有条件通过（9/11 可迁移；CI-2/4/12 须修正；缺 README §2 target）

Closure Blocking = YES
  理由：
   (1) 本轮的核心交付（Finding 映射表）**不真实**：4 行偷换 + 3 行上轮错配未修 +
       1 个 HIGH 级发现在记录中消失 + 2 个 ID 空号 + 2 项历史发现漏登，
       却整表判定 VERIFIED —— 治理溯源不可信，发现不得关闭；
   (2) change set 无法安全写入 L0：CI-4 自相矛盾（正交 vs 同名值）、CI-2/CI-4 不可判定条款、
       CI-4/CI-12 合并归属缺失、`20:317` 示例未改写，且遗漏 L0 自身要求的
       `README.md §2` 术语登记 target；
   (3) 存在合法值→非法值的治理退化：CR-002 `Status` 由 `NOT RELEASED`（枚举内）改为
       `NOT REGISTERED`（枚举外）。AGENTS.md：**Provenance ≠ Quality Authority**；
       未经 Migration Gate 不得进入 active tree。

Recommendation = OWNER ACTION REQUIRED BEFORE CLOSURE

Findings = F-OD01V4R-30 … F-OD01V4R-48（19 项；已登记，未修复）⇔ OD-01F-63 … OD-01F-81
  HIGH      : F-OD01V4R-30, F-OD01V4R-31
  MED-HIGH  : F-OD01V4R-32, F-OD01V4R-33, F-OD01V4R-34, F-OD01V4R-36,
              F-OD01V4R-39, F-OD01V4R-40
  MED       : F-OD01V4R-35, F-OD01V4R-37, F-OD01V4R-38, F-OD01V4R-41,
              F-OD01V4R-42, F-OD01V4R-43, F-OD01V4R-44
  LOW-MED   : F-OD01V4R-45
  LOW       : F-OD01V4R-46, F-OD01V4R-47, F-OD01V4R-48

OD-01F-34…62 复核（本轮自查）：上一轮 29 项中，映射层 7 项失真；change set 层 3 项未真正闭合
Frozen Spec  = UNCHANGED（确认，tree b3eeb3e9…）
CR-002       = Change Proposal Record / NOT EFFECTIVE / NOT REGISTERED（确认；Status 字段取值须修正）
Gate A/B/C/D = PENDING（确认）
Re-freeze / Phase 1 / Migration / Push(v3) = NOT EXECUTED / NOT ENTERED / NOT AUTHORIZED / 未推送（确认）
```

### 进入 Frozen Spec 前的必要修正（4 项，缺一不可）

1. **重建映射表使其忠实于 DSH 基线**：修正 `-08/-09/-10/-11/-12/-13/-14` 七行 `Problem`；
   补回 F-OD01V4R-14（跨仓复制，HIGH）的登记行与修复证据；填补 `OD-01F-09`/`OD-01F-10`；
   纳入 `F-OD01V3-11`/`F-OD01V3-12`。（F-OD01V4R-30/31/32/47）
2. **补 `README.md §2` 术语登记 target**：把 `span_resolution` / `option_evidence_status` /
   `form` / L0 form 名（`line`、`line_character`、`table_cell`、`multiple_source_spans`、`other`）
   写入 §2，并列为 change set 的 Target（顺序：先 README §2，后 20/10）。
   （F-OD01V4R-33；`90 §2 R6`）
3. **修正 CI-2 / CI-4 / CI-12 的拟制文本**：
   ① 删除「正交」表述或恢复 `line_range`/`char_span_in_line` 为 form 值（F-34）；
   ② 把无条件 `line_ref` 限定为 `line / line_character：…`（F-35）；
   ③ 为 `table_cell` 给出可判定的定位判定标准，或明确其在本轮**不是** `resolved` 的必要条件
   （F-36）；
   ④ 给出 CI-4+CI-12 合并后的 `20 §5.5` 全文（含改写后的 JSON 示例，字段名 `span_resolution`）
   （F-37/38）。
4. **治理字段归位**：
   ① CR-002 `Status` 回到 `NOT RELEASED`（`NOT REGISTERED` 仅作正文短语）；
   ② `Authority Level` 取值回到 `91:167` 枚举（如 `L2-proposed`），或先经 L1 流程确立新值域
   （F-39/40/46）；
   ③ D1 新附录与 Self Review 补齐 `Document ID`/`Normative`/`Supersedes`/`Superseded By`
   （附录另加 `Gate State Authority`）；Self Review `Status` 回到 `HISTORICAL`
   （F-42/43）；
   ④ 恢复 Self Review 的历史正文，或撤回「历史正文保留（不删除）」的自述
   （F-44）。

**非阻断跟进**：`未归层`/`90:47` 后果登记与 D1 `:315` Gap 措辞统一（F-45）、
D1 `:405` 流程块版本号统一（F-48）、状态词宣称与实测对齐（F-41）。

---

## 附录 A — DSH 基线（ground truth）编号与标题

```text
AITutorX @ 5adb1b3  Docs/60_REPORTS/OD-01-V4R-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md
  F-OD01V4R-15  Finding→Fix 映射错配 3 行、缺失 4 项、空号 2 个：「一问一号」不成立
  F-OD01V4R-16  F-OD01V4R-09（Gap 两版并存）未修复，却被映射到无关 Fix 并标 VERIFIED
  F-OD01V4R-17  `Purpose` 字段从 Proposal v4R 与 CR-002 头块中消失（较 v4 为回退）
  F-OD01V4R-18  `Authority Level` 值域被自创，触碰「不得自创层级」
  F-OD01V4R-19  状态词「换词未归位」：允许集 5 词中 4 词非冻结值；OD-01-H 引错章节
  F-OD01V4R-20  change set 要求 `table_id`，但 L0 无该实体且同一 change set 明令不授权创建
  F-OD01V4R-21  5 个 CI 条目丢失 `Current Rule`：primary artifact 回退
  F-OD01V4R-22  CI-4 的「逐字」Current Rule 并非逐字；L0 字段名证据被移出块外
  F-OD01V4R-23  form 用语与 OD-01 绑定用语脱钩且无对照表
  F-OD01V4R-24  Self Review 头块围栏损坏且缺 5 个强制字段
  F-OD01V4R-25  破引用与跨仓路径残留
  F-OD01V4R-26  机械替换痕迹：`PENDING = Owner Review`
  F-OD01V4R-27  头块字段名仍不规范；新增多个非规范字段
  F-OD01V4R-28  OWNER APPROVED RECORD 内的拼写错误与同文件流程不一致
  F-OD01V4R-29  新引入非冻结分类词 `Future Required Change` / `Future Consideration`

AITutorX @ d13e70d + d9173ab  Docs/60_REPORTS/OD-01-V4-L1-CR-002-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md
  F-OD01V4R-01…10（自审冒充/头块/状态词/CI-4 矛盾/重命名/Authority 字段/ID Mapping/
                   命名空间/Gap 两版/Rule 2）
  F-OD01V4R-11 新增文档的 `Path` 字段指向另一个仓库
  F-OD01V4R-12 「Current Rule」块保真度参差且未标注逐字/改写
  F-OD01V4R-13 CI-12 与 CI-4 声明「同文」但实际不同文
  F-OD01V4R-14（HIGH）治理产物被逐字节复制进 AITutor-X 且从未 commit

AITutorX @ 1e44017  Docs/60_REPORTS/OD-01-V3-L1-CR-002-CANDIDATE-DSH-ADVERSARIAL-REVIEW.md
  F-OD01V3-01…12（Proposed Text 全删/基线表删/DONE 状态词/Gap 混淆/Owner 自写/
                  degraded 无槽位/删除字段规避/§3.1 误引/ID 空间三分/Authority: L1 矛盾/
                  引文保真/BOM）
```

## 附录 B — 文件 / 坐标索引

```text
被审对象（AITutors-v3 @ e611a4d，只读）
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md   571 行
  Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md                   146 行
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md                  473 行
  Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md               45 行

被引用冻结原文（AITutors-v3，只读）
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md   548 行（§1 :36-47；§1.2 :60-90；R1–R8 :107-…；
                                                    §3 :342-364；§4 :368-383；§5 Rule 1-4 :387-430；
                                                    §11 :271-329）
  Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md   276 行（§3.1 :109-122；§3.2 :124-132；
                                                    §5 :157-177；§5.1 :184-203）
  Docs/V3_SPEC/00_Master_Spec.md           406 行（§5 非目标 :264-278）
  Docs/V3_SPEC/10_Data_Model.md            793 行（§4 :105-109；§6.3 :451-471；
                                                    **术语登记规则 :100-101**；§8 :625-649）
  Docs/V3_SPEC/20_Document_Pipeline.md     794 行（§5.3 :275-294；§5.5 :308-341，
                                                    **resolution_status :317**；§6.1 :355-375；
                                                    §6.2 :383-399；§7.2 :452-455；§7.3 :519-536）
  Docs/V3_SPEC/README.md                          （**§2 术语裁决（权威）:68**；answer_status :94）
  Docs/V3_SPEC/50_Migration_Assets.md             （:51 表格定位行）
  Docs/DECISIONS/69_ARCHITECTURE_REVIEW_ADJUDICATION.md（§5 四道门 :399-431）
  Docs/DECISIONS/82_CONTRACT_AUTHORITY_RECONCILIATION.md（:3/:153 Gate State Authority）
  Docs/DECISIONS/67_ANNOTATION_RESOLVER_BOUNDARY_ADJUSTMENT.md（L1 候选先例）

本报告
  Docs/60_REPORTS/OD-01-V4R-FINAL-VERIFICATION.md
```

```text
— END OF FINAL VERIFICATION —
审查者：DSH（外部独立验证；未参与 OD-01 任何轮次产出）
本报告即 OD-01-J 所述「DSH 外部验证」。被审方的 Self Review 不得替代或代表本报告。
```
