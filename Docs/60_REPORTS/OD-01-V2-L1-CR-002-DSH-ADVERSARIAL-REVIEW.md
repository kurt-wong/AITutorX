# OD-01 修订版（v2）+ L1 CR-002 — DSH 独立对抗性复核

```text
Document Type:      DSH Independent Adversarial Review
Authority Level:    L6 (DSH review record; 非 L0/L1/L2)
Scope:              OD-01 修订版 Proposal + CONTRACT-CHANGE-RECORD-CR-002-OD-01
Reviewed Revision:  AITutors-v3 @ f68aa0963de9c64ebd5f0fe1d92954d104199077
Baseline Revision:  AITutors-v3 @ 506ffa81e5639333ba2bfae61fb8d9d09c2e9aca（v1）
Mode:               READ-ONLY — 未修改任何被审对象，未修复任何发现
```

---

## 0. 复核边界与质询集

**只审两件交付物**：`Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md`（v2）与 `Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md`（新建）。不审 OD-02/03/04/05/G-01/G-02 实体内容（引用仅作对齐检查）。

**本报告不做**：不修 L0 / L1 / CR-002 / Proposal / 代码 / Schema / corpus；不 re-freeze；不代 Owner 批准；不代 Owner 关闭；不 push AITutors-v3。

质询集（本轮 10 问，逐问在报告中给判定）：

| # | 质询 | 判定 | 位置 |
|---|------|------|------|
| Q1 | 七项自述主张（SHA / 未改 / 等授权）是否与仓库事实一致？ | **6/7 VERIFIED，1 项 NOT VERIFIED** | §2 |
| Q2 | F-OD01-01~08 是否 8/8 处置？ | **6 全处置 / 1 部分 / 1 未达标** | §8 |
| Q3 | 条款级 explicit diff 是否完整、引用是否逐字准确？ | **引用逐字准确（8/8）；条款集不完整** | §7 |
| Q4 | CR-002 是否构成 `90` 意义上的合法 L1 载具？ | **NOT VERIFIED** | §6 |
| Q5 | 变更分类 CHANGE-3 是否有依据？ | **未评估 CHANGE-4/5，分类依据不足** | §5 |
| Q6 | 新 §5.3「Producer 唯一权威」是否与双轨冻结语义相容？ | **冲突未处置** | §3 F-OD01R-04 |
| Q7 | 拟议 20 §5.5 文本自身是否闭合？ | **未闭合（granularity/line_ref 与新 form 并存矛盾）** | §3 F-OD01R-06 |
| Q8 | fail-closed 模型是否真正钉死（F-OD01-05 目标）？ | **仍有未闭合词（`degraded`）与同名不同值域** | §3 F-OD01R-07/08 |
| Q9 | 本轮是否已产生 governance 违规？ | **未产生**（CR 明确 NOT EFFECTIVE，L0 未改） | §11 |
| Q10 | 交付物是否可安全封存为「等待 Owner 授权」状态？ | **可封存，但 re-freeze 前置条件未满足** | §11 |

---

## 1. Git / 隔离事实（DIRECTLY VERIFIED）

| 事实 | 值 | 证据 |
|------|-----|------|
| v3 HEAD | `f68aa0963de9c64ebd5f0fe1d92954d104199077` | `git rev-parse HEAD` |
| HEAD `^` | `506ffa81e5639333ba2bfae61fb8d9d09c2e9aca` | `git rev-parse f68aa09^` |
| author / date | `kurt-wong <kurt-wong@users.noreply.github.com>` / `Wed Sep 23 20:21:07 2026 +0800` | `git show -s` |
| 本轮 delta | **仅 2 文件**：`CONTRACT-CHANGE-RECORD-CR-002-OD-01.md`（+282，新建）/ `FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md`（+843/−113） = `2 files changed, 1012 insertions(+), 113 deletions(-)` | `git diff --stat 506ffa8..HEAD` |
| 两文件已 tracked | 是 | `git ls-files --error-unmatch` |
| 工作树（tracked） | 干净（`status --porcelain -uno` 输出空） | `git status` |
| Frozen Spec tree | `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f`，在 `b743c5d` / `506ffa8` / `f68aa09` **三处相同** | `git rev-parse <rev>:Docs/V3_SPEC` |
| `origin/main..HEAD` | 4 提交、仅 6 个 `Docs/COORDINATION/**` 文件、**零** `backend/` 变更 | `git diff --name-only origin/main..HEAD -- backend frontend alembic migrations` 为空 |
| v3 与 origin 关系 | `ahead 4`（`branch -vv`），**未 push**（按令） | — |
| AITutor-X | HEAD = `origin/main` = `4b419bf`，tracked clean，18 项未跟踪与上轮一致 | — |
| Preprocessing / Papers | HEAD = `2b92898f05f6541a5fc65c8300cb8a59a06c4928`，porcelain = 0 | — |
| 未跟踪项 | v3：10 项（9 文件 + `Docs/GOVERNANCE/`），与上轮一致 | — |

**结论**：`Frozen Spec / Production Code / Schema / Corpus = UNCHANGED` 三项主张**成立**。本轮 delta 是纯文档。

---

## 2. 自述主张逐项判定

| # | 自述 | 判定 | 依据 |
|---|------|------|------|
| 1 | F-OD01-01~08 全部处置（8/8） | **PARTIALLY VERIFIED** | 01/03/04/05/06/08 有实质落点；02 部分（漏条款）；07 载具不合规（§6/§8） |
| 2 | 完成条款级 explicit diff（§8：00/20/10 共 8 项） | **PARTIALLY VERIFIED** | 8 项确实存在且引用逐字准确；但至少漏 2 处受影响条款 + 1 处内部不自洽（§7） |
| 3 | L1 Change Record 已建立（CR-002） | **NOT VERIFIED（作为 L1 行为）** | 文件存在且在 Git 中；但 `90` 层面 L1 仍为「暂无」，无任何登记，位置越层（§6） |
| 4 | Frozen Spec 保持未修改 | **VERIFIED** | tree `b3eeb3e9…` 不变；delta 不含 `Docs/V3_SPEC/**` |
| 5 | 代码 / Schema / Corpus 未修改 | **VERIFIED** | 全仓 delta 仅 2 个 COORDINATION 文档；Papers clean |
| 6 | 当前仍等待 Owner Authorization | **VERIFIED** | CR-002 §10 / Proposal §13 一致声明 REQUIRED / NOT GRANTED；仓库内无授权文书 |
| 7 | Commit SHA = `f68aa09…` | **VERIFIED（精确一致）** | `git rev-parse HEAD` 全 40 位相同 |

**摘要块逐行核对**：`OD-01 Proposal = REVISED` ✅（316→933 行，v1 被 supersede 声明）；`Frozen Spec = UNCHANGED` ✅；`Production Code / Schema / Corpus = UNCHANGED` ✅；`Re-freeze = NOT EXECUTED` ✅；`Phase 1 = NOT ENTERED` ✅（delta 无实现）；`Owner Authorization = REQUIRED` ✅；`F-OD01-01~08 = ADDRESSED` ⚠️ 与主张 1 同判定；`L1 Change Record = CREATED` ⚠️ 与主张 3 同判定。

---

## 3. Findings（本轮登记，未修复）

> 编号 `F-OD01R-nn`，与上一轮 `F-OD01-01…08` 不重号。

### F-OD01R-01 — `L1 Change Record = CREATED` 在 `90` 层面不成立（HIGH｜re-freeze 前置）

**证据（全部 DIRECTLY VERIFIED）**：

1. `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:41`（L0-META，Status ACTIVE，Superseded By —）：L1 = **Contract Change Record**，例子列写的是 **「暂无（`67` 是候选，**NOT RELEASED**）」**，权限列写「**修改 L0 的唯一入口**」。
2. `90:79`（目录模型）：`Docs/V3_SPEC/` 允许「引用；**补 Change Record**；**新增 L1**」——即 L1 的规范落点在 `Docs/V3_SPEC/` 内。先例 `CR-001` 正是写在 **`90 §11` 正文内**（`90:271-329`，含 `Change Record ID : CR-001` / `Audit ID : CA-001`）。
3. `90:64-75`（§1.2 目录模型）只登记 4 个目录：`Docs/V3_SPEC/`、`Docs/DECISIONS/`、`Docs/REPORTS/`、`Docs/ARCHIVE/`。**`Docs/COORDINATION/` 不在其中**；`90:47` 冻结规则：「**未归层 = 不得引用为权威。**」
4. `90:359-364`（§3 候选表）登记的是 `67`（CHANGE-5）/ `E1`（CHANGE-2）/ `E2`（CHANGE-3）/ `63`——**无 OD-01 / CR-002**。
5. `90:226` + `90:328-338`：任何 L0 修改**必须**在 §11 登记；`90:41` 的 L1 行与 §11 表**均无 CR-002 / CA-002**。
6. 本仓 `Docs/COORDINATION/CURRENT.md`（其自述 `Canonical Ledger … This is V3 mirror`）与 `log.md` 对 `OD-01`/`CR-002` **零命中**（全文检索）。

**判定**：CR-002 是一件**自我标注**为 L1 的文档；仓库内没有任何 L0/L0-META 或台账条目承认它的 L1 身份。按 AGENTS.md「Agent 自写的 Frozen/Final/Authority 不自动获得权威」与 `90:47`，**「L1 Change Record 已建立」不能从仓库事实得到支持**——它是「已起草并等待登记的 L1 候选」。

**为什么重要**：`90 R1`（`90:107-110`）「L0 只能经 L1 修改」。若载具的 L1 身份不被承认，则后续 L0 修改就**没有合法的入口**——这正是 F-OD01-07 想堵的洞，只是洞的形状从「没走 L1」变成了「走了一个不被承认的 L1」。

**要害澄清**：**尚未违规**——L0 未被修改，`90 §11` 的登记义务尚未触发（见 Q9）。

### F-OD01R-02 — 载具违犯 `91 §5.1` 冻结的文档创建门槛（MED-HIGH｜re-freeze 前置）

`91_PROJECT_TERMINOLOGY.md`（L0-META，ACTIVE）`157-177` 把 `90 §4` 头部扩展为**出生证明**，`184-199` §5.1「文档创建门槛（**冻结**）」要求四项**缺一不可**，其中：

| `91 §5.1` 要求 | CR-002 实际 | 判定 |
|---|---|---|
| #1 Purpose 说明不可合并差异 | 无 `Purpose` 字段（Proposal 有 `PURPOSE:`，CR-002 无） | **缺** |
| #2 「出生证明齐备 — `91 §5` 全部字段，**缺字段即不得创建**」 | 缺 `Derives From` / `May Change` / `Must Not Change` 三个字段（`Must Not Change` 有 §2 实质内容但未按字段声明） | **缺（违反冻结门槛）** |
| #3 「`Authority Level` ∈ `91 §1`/`90 §1` 已定义层级；**不得自创层级**」 | Proposal 自述 `Authority Level: L1-proposal（非 L0）`（Proposal `:923`）——合法枚举为 `<L0｜L0-META｜L1｜L2｜L2-proposed｜L3｜L4｜L5>`（`91:167`），**无 `L1-proposal`** | **自创层级** |
| #4 `May Change` / `Must Not Change`（后者至少含 L0） | 见 #2 | **缺** |

另：两文档 `Status` 取值 `PROPOSED / OWNER AUTHORIZATION REQUIRED / NOT EFFECTIVE` **不在** `90:376` 枚举 `{ACTIVE, SUPERSEDED, HISTORICAL, DRAFT, CLOSED, NOT RELEASED}` 内，也非 `91 §3.1`（`91:111-122`）冻结状态集；而 Proposal `:911` 却声明「本 Proposal 与 CR-002 **已按 `90 §4` 补 Status Header**」——该自述**只对"字段齐"成立，对"取值合法"不成立**。

**为什么重要**：为 cure「L0 修改路径不合规」（F-OD01-07）而新建的载具，本身违犯 L0-META 的**文档创建冻结门槛**（`91 §5.1` 是 `冻结` 级别，且 `DG` 期间「冻结新建治理文档」，`91:201-203`）。修法很轻（补字段、改层级名、改状态词），但必须在 re-freeze 前完成。

### F-OD01R-03 — 变更分类未评估 CHANGE-4/5，却断言「不需要四道门」（HIGH｜re-freeze 前置）

**证据**：

1. `90:346-357`：CHANGE-4 = 「**放宽**既有约束」→ **四道门 + Change Record**；CHANGE-5 = 「**删除**既有约束」→ **四道门 + Change Record**；`90:355`「**判定规则：拿不准往高里归。**归低了就是绕过治理」；`90:357`「**四道门（69 §5）仅适用 CHANGE-4 / CHANGE-5**」。
2. CR-002 §2 T1 动作原文 = 「**部分解除** table_cell option-provenance 子集」（CR `:53`）；§4 After 原文 = 「**废止**独立 `options_unresolved` 语义字段」（CR `:106`）；§6 分类表原文 = 「**废止/改写** `00 §5` table_cell 延后非目标」（CR `:130`）、「改 `20 §5.3` option 边界规则」（CR `:132`）；Proposal `:127` = 「OD-01 **部分解除**该非目标」。
3. CR-002 §6 结论直接写「**本变更不是 CHANGE-4/5，不需要四道门**」（CR `:143`）——**全表没有任何一行评估 CHANGE-4/5**，没有对「解除/废止」两个动词做定性。
4. `90:359-361` 先例：`67`（删 `20:117` FORBIDDEN_FIELDS 的 `line_refs`）= **CHANGE-5 / NOT RELEASED（Gate B NOT CLOSED）**——同一治理体系对「删除冻结项」的既有归类比 CR-002 高一级，且带 Gate 依赖。
5. `69 §5`（`Docs/DECISIONS/69_ARCHITECTURE_REVIEW_ADJUDICATION.md:399-431`）四道门 = Gate A Identity Closure / Gate B Legacy-PathB 对比 / **Gate C Safety Invariant（C3 invalid pointer fail-closed、C5 span integrity 可验证、C6 replay identity）** / Gate D Adapter Boundary。CR-002 §8 的回归项 1/3/7/10（span 构造解析、locator 可回溯 fail-closed、重放）**恰是 Gate C 的同类命题**——即该变更确实落在四道门所守的面上，不能仅凭断言排除。

**判定**：`CHANGE-3 overall` 可能正确，但**当前没有被论证**，且其论证方式（直接断言"不是 CHANGE-4/5"）与 `90 §3` 的强制判定规则和既有先例不一致。按「拿不准往高里归」，正确做法是给出**书面分类理由**（例如：解除的是 capability-scope 非目标而非 safety 边界，故不触发 Gate C），并说明 Gate B 的 open 状态是否构成 release 约束。**这是 re-freeze 之前必须由 Owner 裁定的首要分类问题**——因为它决定 re-freeze 是否需要先跑四道门。

### F-OD01R-04 — 新 §5.3「Producer 唯一权威」与冻结的双轨语义冲突未处置（HIGH｜design）

**证据**：

1. 拟议 20 §5.3 文本（Proposal `:505-513`）：「**Preprocessing Artifact `options[]` 是 option segmentation 的唯一权威来源**……V3 不得重新发现或猜测 option 边界……不得回退到 V3 自行推断。」
2. 冻结的 `90:426`（§5 Rule 4 Ownership Matrix）：「`ResolvedSpan` | **Resolver（Native）或 Adapter（Path B）** | IRBuilder / Compiler / Gate | L0 `20 §5.5`」。
3. 冻结的 `90:464-474`（§6 H-C 双轨一致性）：「Native Path : Source → Resolver → ResolvedRun」「Path B : Source → preprocessing → Adapter → ResolvedRun」「**`ResolvedRun` 必须是唯一消费入口**」「下游 IRBuilder / Compiler / Gate / Admission 对两条路径**完全一致**」。
4. `91:51`：「**当前已登记两条**：`Path A` = Native（Resolver search/resolve）；`Path B` = Adapter/Manifest（verify only）」。
5. Proposal 的语义链（`:66-76`、`:215-237`、`:668-686`）**只描述 Path B**（Original Source → Preprocessing → Artifact → Consumer Boundary）；CR-002 §7 受影响层表（`:149-159`）列了 Consumer Boundary / Resolved Span / IRBuilder / Compiler / Gate，**没有出现 Native / Adapter / Path / ResolvedRun**。

**判定**：把 option segmentation 的唯一权威交给 **Producer Artifact**，在 Path A（Native，无 Producer Artifact）下**没有任何合法的 segmentation 来源**——Native 要么违反新规，要么只能 rediscovery（被新规禁止）。两条路径下游必须「完全一致」的冻结要求随之被破坏。两文档**通篇未提这一冲突**，也未把 Path A 明确排除在适用范围外。

**必须处置**：给出适用范围限定（仅 Path B？）或裁决 Path A 的 option 来源，并同步列入受影响层与回归项。这是本轮**设计层面最重的未处置冲突**。

### F-OD01R-05 — explicit diff 未穷尽受影响条款（MED｜re-freeze 前置）

`10_Data_Model.md:107-108`（§4 B 域开篇）：

```text
依据 01 v0.3 收敛。**M1 裁剪**：`document_source_tables / _cells / _fragments` 不建
（00 §5 non-goal：文档级 cell/fragment 字符粒度延后）；`source_figures` 保留（M1 必需）。
```

该条的**裁剪理由直接引用被本次修改的 `00 §5` 非目标**。CR-002 §2 的 T1–T8 与 Proposal §8.9 的清单**均未包含 `10 §4`**——既没判"需改"，也没像 Proposal `:652` 对 `00 §5` JSONB 非目标那样给出"不改正文"的显式判定。

同类未列引用点（次要）：

- `50_Migration_Assets.md:51`（L0）引用 `20 §5.3`（该节被取代）与 `20 §7.2.5`；
- `20:705` / `20:708`（§8.1 表）把 §5.3 作为依据列；
- `20:392-399`（§6.2 不变量 8「**三层状态严格隔离**：E `ResolvedStatus` ≠ F `semantic_status` ≠ G `gate_decision`/`decision_status`」）——新增 option 级 `resolution_status` 是**第四条状态轴**，且与 E 层**同名**（见 F-OD01R-07），该不变量未被列入 diff 或被声明为不受影响。

**判定**：Proposal `:840`「覆盖 §8.9 清单中全部实际受影响条款」与自述 #2「完成条款级 explicit diff」** overstated**；准确表述是「已交付 8 项条款级 diff，但受影响条款集未穷尽」。

### F-OD01R-06 — 拟议 `20 §5.5` 文本自身不闭合（MED｜re-freeze 前置）

拟议文本（Proposal `:475-487`）**原样保留**了两条旧约束，同时新增非行型 form：

```text
- `granularity` ∈ {line, line_character}（M1；fragment 仍延后，见 00 §5）。
- line_ref 必须存在于该 source_version；line_character 的 start/end_offset 必须能唯一…
- 【OD-01】Resolved Span 增加 provenance form 维度（与 granularity 正交）：form ∈ {...}
```

但 §5.5 的 JSON 形态（`20:310-320`）把 `start_line_ref` / `end_line_ref` / `line_refs` / `granularity` 作为**无条件字段**。于是对 `table_cell` / `multiple_source_spans` / `other` 三种新 form：`granularity` 取什么值？`line_ref` 是否仍必须存在？——**拟议文本没有回答**。而 §8.7 对 `10 §8` 2b 的拟议新文本恰恰承认 locator 可以**不是行型**（「其他 provenance form 的 locator 必须能解析到该 source_version 下可验证 source 实体/切片」）。

**判定**：若把 §8.7 与 §8.2 的拟议文本同时写入 L0，`20 §5.5` 与 `10 §8` 2b 将**互相矛盾**（前者要求 line_ref 必存，后者允许非行型 locator）。§8.2 的 Impact 自述「与 granularity 正交」只是解释了"为什么不往枚举里加 table_cell"，并未解决非行型 span 的必填字段问题。需要一句显式限定（例如：非行型 form 时 `granularity`/`line_ref*` 不适用或为 null），否则 re-freeze 后立刻产生新的内部不一致。

### F-OD01R-07 — 新增 `resolution_status` 与既有同名字段值域不同（MED｜design/naming）

| 出现处 | 字段名 | 值域 |
|---|---|---|
| `20:317`（§5.5 Resolved Span JSON，既有 L0） | `resolution_status` | `exact / normalized / contextual / fuzzy / ambiguous / missing / incomplete`（`20:262-270`） |
| `20:368`（§6.1 IR option，既有 L0） | `status` | `resolved`（示例值） |
| Proposal `:277`（新拟） | option `resolution_status` | `{resolved, unresolved, incomplete}` |

三处**同一语义簇、两个字段名、两个值域**。`20:392-399` 冻结了「三层状态严格隔离」，而新字段与 E 层**同名**——读者将无法从名字判断"这是 span 解析状态还是 option 状态"。`90 R6/R9/R10`（术语必须有冻结定义、近义词不可互换、L2 及以下不得造词）的立法精神正指向此类命名。§8.6 对 IR 的拟议文本仍写 `"status": "resolved"`，**未与新字段名对齐**。

建议（登记层面，非本轮执行）：改名（如 `option_resolution_status`）或在拟议文本中显式声明与 E 层字段的区分与优先级。

### F-OD01R-08 — fail-closed 模型仍有未闭合词：`degraded`（MED｜F-OD01-05 未彻底）

Proposal `:272-279` 声明「**唯一 fail-closed 承载模型（消除双字段歧义）**」并把 option 状态钉死为 `{resolved, unresolved, incomplete}` + QC 层 `QC_FAIL`。但：

- `:307`（§3.5 image_region）要求：「必须显式 **`degraded`** / `unresolved` 声明，**不得伪造** option text」；
- CR-002 §8 回归项 5（`:172`）同样列出「figure identity + region + **degraded**/unresolved」。

`degraded` **不在** §3.4 钉死的状态集内，`§13` 的 12 项 Owner 批准清单（`:803-823`）也没有对应项（#11 只确认 `image_region = other(method=image_region)`）。这与 F-OD01-05 想消除的「双字段歧义」是**同类问题的再现**：一个必须有值的新状态词，没有被纳入唯一承载模型，也没有批准项。

### F-OD01R-09 — Owner 处置/裁决在指定的 Owner Decision 载体内不可核验（MED｜provenance）

**证据**：

- F-OD01-01…08 的处置（`ACCEPT` / `ACCEPT + Owner 裁决`）只出现在 Proposal §0（`:35-44`）与 CR-002 自述（`:42`、`:208`）。
- Proposal §3.2–§3.5 的四处「**Owner 最终裁决**」（Producer 权威 / 单链路与冲突规则 / fail-closed 模型 / `image_region`）同样只见于被审文档自身。
- 指定的 Owner Decision 载体 `Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md`（D1）**本轮未被修改**（delta 只有 2 个文件），全文**无 `F-OD01` 命中**。
- CR-002 自己写明来源：「F-OD01-01…08 dispositions | Owner ACCEPT（**任务书**）」（`:248`）。

**判定**：以**任务书/会话**为准据去改 L0，在仓库内**没有可核验的文书**。按 AGENTS.md「Provenance ≠ Quality Authority」与本仓惯例（OD-01~05 均落盘到 `OWNER-DECISIONS-*`），建议在任何 L0 文本替换前，先把 F-OD01-01…08 处置与四处裁决**增补进 D1**（或在 CR-002 §11 增加指向正式裁决文书的引用）。此项**不阻断**记录封存，但阻断「以 CR-002 为据改 L0」的 provenance 链。

（缓解事实：CR-002 §10 的 A–G 勾选项要求 Owner 主动确认授权、目标、diff、回归范围与分类，因此该缺口可在授权环节一次性补齐。）

### F-OD01R-10 — 两处精度问题（LOW）

1. **无目标的"变更"**：CR-002 §4「After」列入「**废止独立 `options_unresolved` 语义字段**」（`:106`）、Proposal §5 表列「`options_unresolved` 独立语义字段 | **DO NOT ADD / 明确废止**」（`:389`）。该字段**从未存在于 L0**——它是 v1 自造（CR §3 Before 行 `:86` 已如实披露）。以"废止"描述从未生效之物属范畴错误，且 §2 的 T1–T8 **没有对应目标条款**（一条变更没有可改坐标）。建议改述为「不予采用（v1 自造字段，从未进入 L0）」。
2. **引用精度回退**：Proposal §2.1 把示例 span_id 列表标注为「（`20 §6.1`）」（`:95`），含 `sp-M1`——但 `sp-M1` 实际出自 `20:336`（**§5.5** Resolved Relation 示例），§6.1 的示例是 `sp-Q1-stem` / `sp-Q1-A` / `sp-Q1-answer`（`20:367-369`）。该错位恰恰出现在修正引用精度的同一张表内（F-OD01-08 的修复节）。

---

## 4. 经证实的正面结论

| # | 结论 | 证据 |
|---|------|------|
| P1 | **Frozen Spec 逐字节未变**，且与 F-OD01 复核时的 `b3eeb3e9…` 完全一致（`b743c5d` / `506ffa8` / `f68aa09` 三点取样相同） | `git rev-parse <rev>:Docs/V3_SPEC` |
| P2 | 本轮 delta 严格限于 2 个 `Docs/COORDINATION/**` 文档；**无** `backend/` / 迁移 / corpus 变更；Papers clean | §1 |
| P3 | 声明的 commit SHA 与 HEAD **全 40 位精确一致**；父提交 = `506ffa8`（未发生 rebase/改写） | `git rev-parse` |
| P4 | 文档内**引用的 8 段 L0 原文全部逐字准确**（无编造引用）——这是对上一轮"引用错误"的系统性修正 | 附录 A |
| P5 | F-OD01-03/04/05/06 的**设计内容确有落点且互不矛盾**：Producer 唯一权威 + 禁 fallback（`:183-213`）、单链路 + conflict signal（`:215-256`）、状态/基数钉死 + 显式非法情形（`:281-289`）、`image_region = other(method=image_region)` + figure/region/degraded 三项可验证性（`:291-312`） | Proposal §3.2–§3.5 |
| P6 | `10 §6.3` / `10 §8` 2b-2c 的现状基线与拟议扩展方向正确（应用层 invariant、非 FK、非 migration） | `10:469-471`、`10:631-634`、Proposal `:598-645` |
| P7 | CR-002 对 `90 §11` 的**登记时机**处理正确：明确「L0 未改 → CA-002 行随实际 L0 commit 产生」（`:12`、`:225`、`:265`）。这与 `90:226`（"任何对 L0 的修改…必须登记"）一致，且**正是本轮未构成违规的依据** | §11 |
| P8 | 边界守得住：Gate Structural/Semantic/Admission / DB Schema / Production / Corpus 明确标 NO（CR `:155-159`）；回归项 13 负向锁定「不得新增 Gate condition / Admission 条件」（`:180`）；§12 六条「显式不主张」与 §10.2 九条「特别禁止」齐全；§16 回滚设计合理 | CR-002 |
| P9 | **未重编号、未改写历史 Decision**：D1–D5 本轮零改动；`CR-001` 只作为先例引用（`90` CR-001，CHANGE-2，`40 §5`）而未被改写 | delta + `:254` |
| P10 | `69 §5`（四道门）与 `90 §3`（分类表）的**引文与坐标本身正确**——问题在分类论证，不在引用（见 F-OD01R-03） | `69:399-431`、`90:346-357` |

---

## 5. 专项：变更分类（对齐 `90 §3`）

| 动作 | 被改对象性质 | `90 §3` 定义下的候选类别 | CR-002 归类 | 是否给出理由 |
|---|---|---|---|---|
| `00 §5`「文档级表格 cell/fragment 字符粒度索引」非目标 **部分解除** | 冻结的**范围约束**（"M1 不做"） | CHANGE-4（放宽既有约束）**或** CHANGE-3 | CHANGE-3 | **无**（未评估 CHANGE-4） |
| `20 §5.3`「按 A/B/C/D 顺序；每项到下一标签…」**被取代** | 冻结的**行为规则** | CHANGE-3（改行为）/ 亦可能 CHANGE-5 成分 | CHANGE-3 | 部分（只说明"改变既有行为"） |
| `20 §5.5` 新增 form 维度 | 新增强制约束 | CHANGE-2 | CHANGE-2 | 有 |
| `20 §7.2` 步 1 提取扩展 | 改行为 | CHANGE-3 | CHANGE-3 | 有 |
| `10 §8` 2b/2c 核验扩展 | 新增/改核验口径 | CHANGE-2 | CHANGE-2 | 有 |
| `20 §6.1` 链路语义 | 新增约束 + 澄清 | CHANGE-2 + 1 | CHANGE-2/1 | 有 |
| `20 §7.3` 输入来源注释 | 语义零变化 | CHANGE-1 | CHANGE-1 | 有 |

**结论**：`CHANGE-3 overall` 的判断**可能正确**（因为确实含多项"改变既有行为"），但**缺少对 CHANGE-4/CHANGE-5 的排除论证**，而排除它们直接决定 `69 §5` 四道门是否适用（`90:357`）。在 `90 §3` 明令「拿不准往高里归」且存在 `67` = CHANGE-5 的同类先例（`90:361`）的情况下，**断言式排除"不是 CHANGE-4/5"不满足治理要求**。⇒ 主张「F-OD01-07 已处置」在分类维度上**不成立**。

---

## 6. 专项：L1 载具合规矩阵（`90` + `91`）

| `90`/`91` 要求 | 坐标 | CR-002 状态 | 判定 |
|---|---|---|---|
| L1 = Contract Change Record = 修改 L0 唯一入口 | `90:41`、`90:107-110` | 自称 L1 | 身份**自称** |
| L1 规范落点在 `Docs/V3_SPEC/`（补 Change Record / 新增 L1） | `90:79` | 位于 `Docs/COORDINATION/` | **越层** |
| 目录模型只含 V3_SPEC / DECISIONS / REPORTS / ARCHIVE | `90:64-82` | COORDINATION 未登记 | **未归层**（`90:47`：不得引用为权威） |
| 未发布的 L0 变更候选登记于 `90 §3` 候选表 | `90:359-364` | 无 OD-01/CR-002 | **未登记** |
| L0 修改强制在 `90 §11` 登记 | `90:226`、`90:328-338` | 明确"待 re-freeze 时登记" | **合规**（尚未触发） |
| Status Header 七字段 | `90:368-381` | 七字段齐 | **合规（形式）** |
| Status 取值 ∈ 冻结枚举 | `90:376`、`91:111-122` | 自造三元组 | **越界** |
| 出生证明全字段（含 Derives From / May Change / Must Not Change） | `91:157-177`、`91:184-199` | 缺 3 字段 | **违反冻结门槛** |
| Authority Level 不得自创 | `91:184-199` #3 | `L1-proposal` | **自创层级** |
| 先例形态（CR-001 写在 `90 §11`，含 ID/Target/Class/Source Commit/Audit ID/Date） | `90:271-329` | CR-002 含 `Change Record ID` / `Target` / `Class` / `Source Proposal` / `Audit ID` / `Date` | **形态合规**（位置不合规） |

**净判定**：CR-002 在**内容形态**上明显对齐 CR-001 先例（值得肯定），但**层级归属与创建门槛**不满足 `90`/`91`。⇒ 主张 #3 → **NOT VERIFIED（作为 L1 行为）**。

---

## 7. 专项：条款级 explicit diff 质量

### 7.1 引用逐字核对（全部 DIRECTLY VERIFIED）

| diff 项 | 引用坐标 | 逐字 | 备注 |
|---|---|---|---|
| §8.1 | `00_Master_Spec.md:274-275` | ✅ | 含换行位置一致（"待样本 / 证明需要再加回"） |
| §8.2 | `20_Document_Pipeline.md:322-324` | ✅ | `granularity ∈ {line, line_character}` + offset 句完整 |
| §8.3 | `20_Document_Pipeline.md:280-281` | ✅ | `option_label` 原句完整，含 `ambiguous`/`incomplete` |
| §8.4 | `20_Document_Pipeline.md:454-455` | ✅ | 步 1「line / line_character」原文一致 |
| §8.5 | `20_Document_Pipeline.md:523` | ✅ | `dedup_key` 行 + 排除列表完整 |
| §8.6 | `20_Document_Pipeline.md:368` | ✅ | `{"options": {"A": {"source_span": {"span_id": "sp-Q1-A"}, "status": "resolved"}}}` 精确一致 |
| §8.7 | `10_Data_Model.md:632-634` | ✅ | 2b/2c 摘要与原文一致（2a 未引，不影响） |
| §8.8 | `10_Data_Model.md:469-471` | ✅ | JSONB / 非 FK / 应用层 invariant 原文一致 |

→ **无编造引用**（对比上一轮 F-OD01-08 的问题，本轮已系统性修正）。唯一精度瑕疵见 F-OD01R-10-2（`sp-M1` 归属 §5.5 而非 §6.1）。

### 7.2 条款集完整性

已覆盖：`00 §5`（cell/fragment 非目标）、`00 §5`（JSONB 非目标，显式"不改"）、`20 §5.3`、`20 §5.5`、`20 §6.1`、`20 §7.2`、`20 §7.3`、`10 §6.3`、`10 §8`、`90 §11`（流程）。

**未覆盖但受影响**：`10 §4:107-108`（裁剪理由引用被改非目标）、`20 §6.2` 不变量 8（三层状态隔离 vs 新状态轴）、`50:51`（引用被取代的 §5.3）、`20:705/708`（以 §5.3 为依据的表行）。已知不足：至少 **1 处实质**（`10 §4`）+ 3 处引用级。

### 7.3 内部自洽

`20 §5.5` 拟议文本对非行型 form 未定义 `granularity`/`line_ref` 取值（F-OD01R-06）；`degraded` 未纳入 fail-closed 模型（F-OD01R-08）；option `resolution_status` 与 E 层同名字段值域冲突（F-OD01R-07）。⇒ **不可逐字直接替换**，需先补 3 处收口句。

---

## 8. 上一轮 8 项 finding 的处置复核

| Finding | 上一轮要求 | 本轮处置 | 判定 |
|---|---|---|---|
| F-OD01-01 基线不完整 | 补完整 Resolved Span 现状（含 `line_character`+offset、`00 §5` 非目标、`fragment`、真缺口清单） | Proposal §2.1 新增 12 行现状表，逐项标"已存在/延后/真缺口"；`char_span_in_line` 与 `line_character` 关系单列 §2.2 钉死 | **已处置** |
| F-OD01-02 变更集不完整 + 缺 explicit diff | 交付条款级 diff（含 00/20/10） | §8.1–§8.9 共 8 项 diff（Current→Proposed→Reason→Impact）+ §8.9 汇总清单 | **部分处置**（漏 `10 §4` / `20 §6.2` / `50:51`；内部不自洽 3 处） |
| F-OD01-03 §5.3 rediscovery 冲突 | 显式取代，无 fallback | §8.3 给出取代文本，明写「本条取代原…规则」+ 禁 fallback + fail closed | **已处置（但引出 F-OD01R-04 双轨问题）** |
| F-OD01-04 双 provenance 权威未定义 | 定义单链路 + 冲突规则 | §3.3 三层职责表 + 4 条冲突规则 + OD-04 对齐；§8.6 写入 IR 语义 | **已处置** |
| F-OD01-05 fail-closed 未钉死 | 唯一承载模型 + 基数钉死 + 进 Owner 清单 | §3.4 状态表 + 基数表（`resolved ⇒ 1..n`，`0-span` 非法）+ §13 #8 批准项 | **基本处置**（`degraded` 未纳入 → F-OD01R-08） |
| F-OD01-06 `image_region` 缺口 | 纳入正式承载 + 可验证性 + 风险登记 | §3.5 三条可验证性要求 + `form=other/method=image_region` + §5/§6/§13#11 + §15 未单列风险行但已由 §7.3 覆盖 | **已处置** |
| F-OD01-07 L0 路径不合规 | 建立 L1 Change Record + 登记分类/受影响层/回归范围 | CR-002（7 字段头、T1–T8、Before/After、CHANGE-3、受影响层表、13 项回归、显式不主张、Owner 勾选） | **未达标**：内容齐，但 L1 身份不被 `90` 承认（F-OD01R-01）、违反 `91 §5.1`（F-OD01R-02）、分类未论证（F-OD01R-03） |
| F-OD01-08 引用错误 | 修正 `sp-<unit>.option.<label>` → 规范示例 | §2.4 更正表 + §8.6 拟议文本注明"代码构造名不得回写为 Spec"；引用实名为 `sp-Q1-A` | **已处置**（新增 1 处精度回退，LOW） |

**统计**：**6 项已处置 / 1 项部分（02）/ 1 项未达标（07）**。⇒ 自述「8/8」**偏高**，准确表述为「6 项处置完毕、2 项部分」。

---

## 9. 本轮是否产生违规（Q9）

**未产生。** 依据：`Docs/V3_SPEC/**` tree 与其他 L0 文件全部未改（§1）；CR-002 与 Proposal 全文一致声明 NOT EFFECTIVE / RE-FREEZE NOT DONE；`90 §11` 的强制登记义务针对**已发生的 L0 修改**（`90:226`），本轮无 L0 修改 → 义务未触发。因此 F-OD01R-01 描述的是**载具身份缺陷**，不是**既成违规**。

**风险边界**：若 Owner 在未解决 F-OD01R-01/02/03/04 的情况下按 CR-002 §10 勾选 A–G 并下令 re-freeze，则 `90 §3` 的分类风险（CHANGE-4/5 未评估）会转化为**实际治理绕过**，且 L0 修改将经由一个 `90` 不承认的 L1 载具完成。

---

## 10. 限制（L-1…L-7）

- **L-1**：未重跑任何测试基线（Preprocessing `338 passed, 1 xfailed` / V3 `2030 passed, 1 skipped, 1 xfailed` 未复核）。**本轮为文档治理审，不涉及基线**；相关数字属 G-02 范围。
- **L-2**：只审 OD-01 两件交付物；对 OD-02/03/04/05/G-01/G-02 与 Frozen Contract 五件套的引用仅用于**对齐检查**，不构成对其内容的背书。
- **L-3**：`git fetch` 在本环境不可用，`origin/main` 比较基于本地 ref；AITutors-v3 未 push（按令），因此其远端状态未复核。
- **L-4**：本环境 pwsh 沙箱无法初始化（`SetNamedSecurityInfoW Win32 5` on `D:\Project\AITutor-X`），所有仓库命令在 `danger-full-access` 提权下执行；**所有判定基于只读命令输出**（`git`、`Select-String`、`Get-ChildItem`），未写入被审仓库。
- **L-5**：`90`/`91` 均为 `Status: ACTIVE`、`Superseded By: —`，未发现使其失效的记录（含 `82 §1/§2/§9/§11` 被吸收的说明），故按现行 L0-META 适用。若存在未搜索到的废止文书，F-OD01R-01/02/03 的适用性需相应复核。
- **L-6**：`Docs/COORDINATION/**`（含 Frozen Contract v0.3、D1–D5、CR-002）整体**不在** `90 §1.2` 的目录/层级模型内——这是**本轮之前既存**的系统性治理缺口（该目录与 Frozen Contract 亦是本仓 OD/Contract 权威链的支柱）。本轮只就其对 CR-002 的影响登记，不扩大审计范围。
- **L-7**：被审报告的传输通道出现过一次 `spawn ENAMETOOLONG` 外层错误。**交付物完整性不受影响**（本文所有结论均已独立与仓库事实逐项核对），但无法从仓库侧排除"存在未被粘贴的输出"。

---

## 11. 最终判定

```text
OD-01 Proposal v2 + L1 CR-002  = VERIFIED WITH FINDINGS
Closure Blocking               = NO
Recommendation                 = OWNER ACTION REQUIRED BEFORE CLOSURE
Findings                       = F-OD01R-01 … F-OD01R-10（10 项，已登记未修复）
上一轮 F-OD01-01…08 处置       = 6 已处置 / 1 部分 / 1 未达标
```

**`Closure Blocking = NO` 的口径**：本轮交付物**没有违反任何被冻结的既有约定**——Frozen Spec / 代码 / Schema / corpus 全部未改，CR-002 明确 NOT EFFECTIVE，`90 §11` 的登记义务尚未触发，不存在"被误关闭的事项"。10 项发现阻断的是**下一步（re-freeze）**，不是本轮的治理记录。

**`OWNER ACTION REQUIRED BEFORE CLOSURE` 的口径**：以下四项必须在发出任何 Freeze Order 之前处置，否则 re-freeze 会经由一个 `90` 不承认的 L1 载具、在一个未论证的变更分类下完成：

1. **F-OD01R-03**（变更分类）：书面判定 `00 §5` 非目标"部分解除"与 `20 §5.3` 规则"取代"是否触发 CHANGE-4/CHANGE-5 与 `69 §5` 四道门（含 `67` 先例与 Gate B 状态）；
2. **F-OD01R-01 + F-OD01R-02**（L1 载具）：把 CR-002 落到 `90` 承认的位置/登记（`90 §3` 候选表与 §11，或 `Docs/V3_SPEC/` 内），并补 `91 §5.1` 出生证明字段、修正自创层级 `L1-proposal` 与状态词；
3. **F-OD01R-04**（双轨）：显式裁决新 segmentation-authority 规则的适用范围（Path B only？）与 Path A/Native 的 option 来源，并同步受影响层与回归项；
4. **F-OD01R-05 + F-OD01R-06**（diff 收口）：补齐 `10 §4:107-108`、`20 §6.2` 不变量 8、`50:51` 等受影响/引用点，并为非行型 form 补 `granularity`/`line_ref` 适用性一句。

**建议顺手一并处置（不阻断）**：F-OD01R-07（`resolution_status` 命名与 E 层冲突）、F-OD01R-08（`degraded` 纳入 fail-closed 模型）、F-OD01R-09（F-OD01 处置增补进 Owner Decision 记录）、F-OD01R-10（两处精度）。

**执行到此停止。** 本报告不修复任何发现，不 re-freeze，不宣布 Owner 关闭，不进入 Phase 1。

---

## 附录 A — 引用原文逐字核对记录

| 引用方 | 被引原文 | 结论 |
|---|---|---|
| Proposal §8.1 | `00:274-275`「文档级表格 cell/fragment 字符粒度索引（首版只做 line + 必要 inline，见 20；待样本 / 证明需要再加回）。」 | 逐字一致 |
| Proposal §8.2 | `20:322`「`granularity` ∈ {line, line_character}（M1；table_cell/fragment 延后，见 00 §5）。」+ `20:323-324` offset 句 | 逐字一致 |
| Proposal §8.3 | `20:280-281`「**option_label**：按 A/B/C/D 顺序；每项到下一标签/下一题结束；重复标签 → ambiguous；缺标签 → incomplete。」 | 逐字一致 |
| Proposal §8.4 | `20:454-455`「1. 逐 content role 从 resolved span（line / line_character）**确定性提取**正文 → `compiled_roles[]`，每个带 `text_hash`（= source slice hash，供 10 §8 2c 校验）。」 | 逐字一致 |
| Proposal §8.5 | `20:523` Question `dedup_key` 行 + 排除列 | 逐字一致 |
| Proposal §8.6 | `20:368` option IR 示例 | 逐字一致 |
| Proposal §8.7 | `10:632-634` 2b/2c | 逐字一致（摘要式） |
| Proposal §8.8 | `10:469-471` JSONB 约束段 | 逐字一致 |
| Proposal §3.4 | `20:262-270` §5.2 status 表（E 层值域） | 一致（"沿用 §5.2 值域"成立） |
| Proposal §3.5 | `figure_id` / `source_figures` / page-bbox-placement / `D-6 Figure Contract` | **均真实存在于 L0**（`10 §4.4:180-228`、`20 §5.3:289-294`、`20 §5.5:327-331`、`20 §7.2.5`）——无编造概念 |
| CR-002 §6/§11 | `69 §5` 四道门；`90 §3` 分类表；`90` CR-001（CHANGE-2，`40 §5`） | 引用正确（问题在论证） |
| Proposal §2.1 | 示例 keys 归属「`20 §6.1`」（含 `sp-M1`） | **不精确**（`sp-M1` 在 `20:336` §5.5）→ F-OD01R-10-2 |

## 附录 B — 文件与关键坐标索引

```text
被审对象
  AITutors-v3/Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md（933 行，v2）
  AITutors-v3/Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md（282 行，新建）
  commit f68aa0963de9c64ebd5f0fe1d92954d104199077（parent 506ffa8；2 files, +1012/−113）

规范依据（L0/L0-META）
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md   :41 :47 :64-82 :79 :107-110 :226 :271-329 :328-338 :346-357 :359-364 :368-381 :426 :464-474
  Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md   :51 :107-132 :157-177 :184-199 :201-203
  Docs/V3_SPEC/00_Master_Spec.md           :264-278（§5 非目标；含 :270 JSONB、:274-275 cell/fragment）
  Docs/V3_SPEC/20_Document_Pipeline.md     :275-294（§5.3）:308-331（§5.5）:360-375（§6.1）:383-399（§6.2）:452-492（§7.2）:519-536（§7.3）
  Docs/V3_SPEC/10_Data_Model.md            :105-109（§4）:451-471（§6.3）:625-643（§8）
  Docs/V3_SPEC/50_Migration_Assets.md      :51
  Docs/DECISIONS/69_ARCHITECTURE_REVIEW_ADJUDICATION.md :399-431（四道门）
  Docs/COORDINATION/CURRENT.md             （全文无 OD-01/CR-002 命中）
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md（全文无 F-OD01 命中）
```

**Report ends.**
