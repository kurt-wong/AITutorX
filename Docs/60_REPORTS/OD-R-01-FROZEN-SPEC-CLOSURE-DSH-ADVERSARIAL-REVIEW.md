# OD-R-01 固化 + Frozen Spec 最小闭环 — DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 固化 + Frozen Spec 最小闭环 — 完成报告」 |
| 仓库 | `D:\Project\AITutors-v3`（governance subject） |
| 分支 | `od01-r3-convergence` |
| 被审 commit | `71f51f97e5674cf04ab12d4c449e3796a160bb27`（parent `9f1763e`） |
| 审查基线 HEAD | `71f51f9`（= 被审 commit 本身；工作区干净、无 tracked 改动） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间**未修改任何文件、未 push** |
| 证据等级 | DIRECTLY VERIFIED（git 对象 / 逐字文本）· VERIFIED BY INSPECTION · DOCUMENT CLAIM · UNKNOWN |

---

## 1. VERDICT

```text
VERDICT: REJECTED AS-IS
（授权链与审计链未闭合；在 Owner 裁决前，不得视为合法的 L0 / Frozen Spec 修改）
```

**一句话结论**：改动**内容**很小、方向与 OD-R-01 一致，且报告**主动披露**了治理张力——这部分应予记分；但它在性质上是**对 L0（`Docs/V3_SPEC/`）正文的直接原地编辑**，命中 `90 §1.2:79` 的**禁止列**，且**缺 L1、缺 Change Audit Record、缺 re-freeze 记录**，并同时违反其**自身父文件（D1）** 记录的硬边界。**问题不在文字质量，在授权与审计。**

```text
核心矛盾（不可回避的二难）：
  若本次 L0 修改未经授权 → 违反 90 §1 / §1.1 / §1.2（L0 只能经 L1 修改；禁止直接编辑）
  若主张已获授权       → 仍缺 90 §11 Change Audit Record 与 re-freeze 登记
  任一读法下，仓内合规模块均未闭合。
```

---

## 2. 已独立复核的关键事实

### 2.1 Frozen Spec tree 已改变（决定性事实）

```text
9f1763e:Docs/V3_SPEC  = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f   （审查前基线，历史各轮均记为 UNCHANGED）
71f51f9:Docs/V3_SPEC  = 442172f40942368a4856231a742bf4d273242034   ← 已改变
HEAD:Docs/V3_SPEC     = 442172f40942368a4856231a742bf4d273242034
```

### 2.2 L0 的修改规则（`Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md`，L0-META，本 commit 未改）

| 位置 | 原文（逐字） |
|---|---|
| `90 §1:40` | `| **L0** | **Frozen Spec** | `00` `10` `20` `30` `40` `50` | **定义系统事实**。唯一 Schema Source of Truth = `20` | 不得被 L2–L5 隐式修改 |` |
| `90 §1:41` | `| **L1** | **Contract Change Record** | 暂无（`67` 是候选，**NOT RELEASED**） | **修改 L0 的唯一入口** | 未走完流程不得生效 |` |
| `90 §1.1:54` | `| — | **L1 Contract Change Record** | **新增成层**——修改 L0 的唯一门 |` |
| `90 §1.2:79` | `| `Docs/V3_SPEC/` | L0 / L0-META | 引用；补 Change Record；新增 L1 | **直接编辑；隐式改变** |` |
| `90 §11:224` | `## 11. Change Audit Record（L0 修改审计）` |

### 2.3 本次改动（逐字复核，共 3 文件）

```text
71f51f9  docs: register OD-R-01 and close multi-blank Answer boundary in Frozen Spec
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md   70 / 0
  Docs/V3_SPEC/10_Data_Model.md                                  8 / 0   ← L0
  Docs/V3_SPEC/20_Document_Pipeline.md                           2 / 1   ← L0
  total: 3 files changed, 80 insertions(+), 1 deletion(-)
```

- `10 §6.3` 约束列表新增一条「Answer 业务对象边界（OD-R-01 冻结）」（`:468-475`）。
- `20 §5.3` blank 条由「一个 blank 必须映射到一个 sub_question/answer」改为「…一个 sub_question，或**同一份 Answer 的一个有序值**（多空题 Answer 业务对象边界见 10 §6.3 OD-R-01）」（`:288-289`）。

---

## 3. Findings

### F-01 [BLOCKING] L0 正文被直接原地编辑，且仓内**不存在**合法的 L0 修改入口

证据（全部 DIRECTLY VERIFIED）：

1. `Docs/V3_SPEC/` tree hash 已变（§2.1）。
2. `90 §1:41`：L1 = **修改 L0 的唯一入口**；而同一行自述 L1 **「暂无」**（`67` 仅候选、NOT RELEASED）⇒ **仓内当前不存在任何 L1**。
3. `90 §1.2:79`：`Docs/V3_SPEC/` 的**允许**列是「引用；补 Change Record；新增 L1」，**禁止**列是「**直接编辑；隐式改变**」。本 commit 的行为（原地改写 `10`/`20` 正文）字面落入禁止列。
4. `90 §11:224` Change Audit Record：本 commit **未新增任何变更审计记录**（`git show 71f51f9 -- Docs/V3_SPEC` 中无 `变更`／`2026-09-24` 相关行）。
5. `Docs/COORDINATION/LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md` §9`:320`：`Frozen Spec: UNCHANGED (OD-01 change is PROPOSAL only until re-freeze)` ⇒ 自本 commit 起**为假**。
6. 同文 §6`:257` 禁止 `V3 Frozen Schema modification`；§5 STOP Conditions`:233` A「Frozen Spec 冲突」、`:235` C「必须修改 Frozen Schema」。

> **判定**：无论 Owner 的授权意图如何，**仓内缺少承载该 L0 修改的合规模块**（L1 / Change Audit Record / 新 tree hash 登记）。这是本轮最高严重度问题，且**不可由 DSH 自行消解**。

### F-02 [BLOCKING] 同一 commit 违反其自身父文件声明的禁区

`Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md`（本 commit **同时修改**的文件）：

```text
:13  Must Not Change:  L0 00–50 · L0-META 90/91 · Frozen Contract · Schema · Code · Corpus · 历史决策语义
:347 2. 本轮硬边界要求 Frozen Spec tree hash 保持 `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` 不变。
:348 3. 向 `Docs/V3_SPEC/` 新增任何文件（含 L1）都会改变该 tree hash。
```

被改的 `10_Data_Model.md` / `20_Document_Pipeline.md` 正是 `L0 00–50` 成员（`90:40`）。⇒ 新增的 70 行 OD-R-01 记录，与其所在文件**自身既有**的禁区条文直接冲突（单文件内自相矛盾）。

### F-03 [HIGH] 4 处「现行 / 基线」断言被改成为假；并造成 OD-01 Proposal 的基线漂移

**现行 / 基线断言（未标注历史，仍被当作当前事实引用）：**

| 文件:行 | 断言 | 现状 |
|---|---|---|
| `Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md:24` | `Frozen Spec tree = b3eeb3e9…（UNCHANGED）` | **假** |
| `Docs/COORDINATION/IMPLEMENTATION-PLAN-v0.3.md:31` | 基线表 `Frozen Spec tree …（unchanged）` | **假** |
| `Docs/COORDINATION/IMPLEMENTATION-PLAN-v0.3.md:452` | Phase 0 Scope 核对 `b3eeb3e9` | **假** |
| `Docs/COORDINATION/IMPLEMENTATION-PLAN-v0.3.md:828` | `Compiled from … Frozen Spec tree b3eeb3e9` | **假** |
| `Docs/COORDINATION/G-02-FREEZE-REGISTRATION-VERIFICATION.md:87` | `Frozen Spec tree (Docs/V3_SPEC) = b3eeb3e9…` | **假** |
| `Docs/COORDINATION/OWNER-DECISIONS-…md:347` | 硬边界要求 tree hash 不变 | **与本 commit 冲突** |

**历史报告（当时快照，现与仓状态冲突，需明示或加注）：**
`Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md:49` / `:73` / `:95`；
`Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md:27`。

**二次危害（竞争修改 L0）**：`FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md` 是针对 `b3eeb3e9` 基线写就、**正待 Owner review + re-freeze**。现 L0 已由**另一条路径（直接编辑）**先行改变 ⇒ 同一 L0 出现两条竞争修改路径，Owner 复审时基线已漂移，Proposal 的 `UNCHANGED` 前提失效。

### F-04 [HIGH] 顺序倒置：自行解释授权 → 执行 → push（不可逆）→ 之后才询问

报告 §E 末段自述：执行过程中（由权限分类器）发现张力，自行判定「视为你针对本次、以此为限解除该冻结」，随后 commit 并 push（`9f1763e..71f51f9`），**最后**才写「若这一读法与你的意图不符，请指示，我可只回退这两处 Frozen Spec 改动」。

对照项目既有纪律：

```text
LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md
  §1:35  STOP → 记录冲突 → Owner Decision
  §1:38  不得自行解决。不得通过 Implementation PR「顺便修正」Frozen Contract。
  §3.5:160  记录 Schema Gap → 说明现有 Schema 为何无法承载 → STOP → Owner Decision / Frozen Spec Change
```

⇒ 面对「需 Owner 裁决」的情形，项目纪律要求**先停后问**；此处为**先做后问**，且已推送到远端。

### F-05 [MED-HIGH] L0 自带「变更记录」未更新（独立的可机检遗漏）

| 文件 | 变更记录落点 | 最后条目 |
|---|---|---|
| `10_Data_Model.md` | `:732 ## 12. 变更记录` | `:789 ### 2026-09-09（v1.2.2，BUG-011 Scope Freeze errata）` |
| `20_Document_Pipeline.md` | `:742 ## 12. 变更记录` | `:789 ### 2026-09-09（v1.2.1，BUG-011 Scope Freeze errata）` |

本 commit 对两文件的改动**未新增任何变更记录行**。且 `10:785` 自身写明「20 §12 是变更记录」⇒ 该惯例是 L0 明确认知的。**即使**认定 §5 授权有效，L0 自身的变更审计链仍未闭合——与 F-01 的 `90 §11` 缺失**相互独立、叠加存在**。

### F-06 [MED] 「最小闭环」在 payload 侧未闭合，且残留**在仓内无落点**

- 新条款（`10:468-475`）判定「多个空 = **一份 Answer**」；但**同一文档** `10 §5.3:329` 的 payload 载体仍是 `answer[]`（**数组**），元素粒度未写明 ⇒ 3 空题的 payload 可被读成 3 个 answer 元素。`10 §5.3:340`「`payload` 是快照承载，不是 live 关系」属实，但未解决元素粒度。
- 报告**已披露**该残留（「属 evidence / payload 载体形态…不偷偷并入 OD-R-01」）——**披露属实，应予记分**。
- 但**披露只存在于对话报告**：本 commit 仅动 3 文件；D1 的「本 Decision 不裁决」清单列的是 evidence 数据模型 / evidence 粒度 / partial correctness / 每空独立 evidence state，**未列** `answer[]` 元素粒度与 `answer_status` 挂载点；84 台账或任何 GAP registry 亦无登记（本 commit 未触碰）。
- ⇒ 「Frozen Spec **最小闭环**」这一自我定性，对其**自身目标**（消除「多份 Answer」读法）而言**未闭合**。

### F-07 [MED] 报告「无需修改」清单中 `20 §6.3` 的**理由不成立**（结论方向对、理由错）

- 报告自述：「`20 §6.3 M1 Role Contract` 表 12 型均为 `answer | required`（单一要求），已排除「多份 Answer」读法」。
- 实测 `20:404-408`：该表是「canonical question type → **role requirement**」的**唯一规范来源**，值域 ∈ `{required, required_for_choice, optional, not_applicable}`；`:431-434` 明确 `answer=required` 是 **M1 数据完整性要求**。12 行 `answer=required` **数字正确**，但该表规定的是「answer role **是否必需**」，**既不表述、也不可能排除答案对象数量**。
- ⇒ 该理由为**推论过度**。此类「理由不成立」在治理文档中会被后续轮次引用为证据（上一轮 R3 已出现同型问题），需更正措辞。

### F-08 [MED] 新条款用语与 L0 既有用语未对齐；`value[i]` 指称在字段表中不存在

- L0 **既有**「多值」措辞：`10:459`（`role_index` note：`options/多值顺序`）、`20:651`（`complete` 判据：`选项/多值/单元格/跨行答案全部闭合`）。
- 新条款改用 **`multi-value`**（英文）并引入 **`value[i]`** 记号；而 `10 §6.3` 字段表（`:453-463`，含表头 11 行）**不存在 `value` 字段**（字段为 `id/instance_id/role/label/role_index/text/text_hash/source_span/answer_status`）⇒ `value[i]` 的指称在表定义中无对应字段。
- 与同句「（`role_index` 承载该顺序）」并置后，**N 个有序值在 `instance_role_contents` 中对应 1 行还是 N 行**仍未写明；而既存唯一约束 `(instance_id, role, label, role_index)`（`:467`）的自然映射是 N 行 ⇒ 语义层「一份 Answer」与关系层行数之间的缺口，恰好留在本决策**要消除歧义的那张表**里。
- **声明**：F-08 **不主张**「必须补字段 / 必须改 schema」——那属 Owner 裁决面；此处仅记录 L0 文本层面的**指称缺口**。

### F-09 [LOW] 报告 §E 自检项与 §A 事实自相矛盾

- §A：「OD-R-01 最终文本（**已登记**）… 登记位置 = 既有 Owner Decision 载体 `OWNER-DECISIONS-…md` 的 `## OD-R-01` 节 + 顶部 Summary Table 追加 1 行」。
- §E 自检：「…✅ **未引入新 Owner Decision** ✅…」。
- ⇒ 同一报告内，§A 自述新增了一条 Owner Decision，§E 却称「未引入新 Owner Decision」。可推测原意为「未引入**任务书之外**的额外 Decision」，但**措辞未限定**，属可被误引的自检表述。

### F-10 [LOW] untracked 计数口径

- 报告 §C：「untracked 计数保持 10」；§D：「10 个既有 untracked 条目（9 × `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-*.md` + `Docs/GOVERNANCE/`）」。
- 实测：`git status --porcelain`（默认口径）**10 条目** ✓ 与其一致；`--untracked-files=all` 为 **13 个文件**（CONTRACTS 9 + GOVERNANCE 4）。
- **判定**：口径差异，非事实错误；方向性结论（未清理、未纳入提交）**成立** ✓。建议统一为 `-uall` 计数，避免「未清理」被误读。**该口径问题在上一轮报告中亦已出现**。

### F-11 [LOW / 方法] 验证集未覆盖授权面（F-01～F-03 的根因）

报告 §C 的验证 = diff 逐字核对 + forbidden-artifact 扫描 + 条款落点计数 + untracked 计数 + 未跑代码测试（理由正当）。**未包含**：

```text
90 §1 / §1.1 / §1.2 / §11 的 L0 修改合法性检查
Frozen Spec tree hash 前后对比（b3eeb3e9 → ?）
D1 `Must Not Change`（:13）自检
D1 硬边界（:347）自检
```

⇒ 验证的是**形式**（改动大小、禁用产物、计数），**未验证权限**。这是 F-01/F-02/F-03 未被自查拦下的直接原因。

---

## 4. 报告自述 vs 实测（逐条）

| # | 报告自述 | 实测 | 判定 |
|---|---|---|---|
| 1 | commit `71f51f9` / branch `od01-r3-convergence` | HEAD=`71f51f9` ✓ branch ✓ parent=`9f1763e` ✓ | **TRUE** |
| 2 | 3 文件 / 80 insertions / 1 deletion | 逐文件 70/0 + 8/0 + 2/1 ⇒ 一致 | **TRUE** |
| 3 | Frozen Spec 恰好 2 处改动 | `10 §6.3` + `20 §5.3`，无第三处 | **TRUE** |
| 4 | 落点计数 `10×1` / `20×1` / `OWNER-DECISIONS×4` | 实测 1 / 1 / 4 | **TRUE** |
| 5 | ABD 不推广保护条款 `10×1` / `OWNER-DECISIONS×1` | 实测一致 | **TRUE** |
| 6 | forbidden-artifact 扫描 → 0 命中 | 对新增行的等价扫描 → 0 命中 | **TRUE** |
| 7 | 未运行代码测试（理由：非代码实现 / 仓内无对应测试） | 纯 Markdown 规格，理由成立 | **TRUE** |
| 8 | push 成功，HEAD == origin/od01-r3-convergence | 本地 remote-tracking = `71f51f9` ✓；**远端独立复核受阻**（凭据策略，见 §5） | **PARTIAL** |
| 9 | untracked 计数保持 10 | 默认口径 10 ✓；`-uall` = 13 | 口径差异（F-10） |
| 10 | 「`20 §6.3` 已排除『多份 Answer』读法」 | 该表只规定 role requirement，不表述对象数量 | **FALSE（理由）**（F-07） |
| 11 | 「Frozen Spec 最小闭环」 | payload `answer[]` 元素粒度未定；残留未在仓内登记 | **PARTIAL**（F-06） |
| 12 | 「未引入新 Owner Decision」（§E 自检） | §A 自述已登记 OD-R-01（新增 Decision） | 报告内自相矛盾（F-09） |
| 13 | 「未改 schema」 | 未改字段表 / DDL ✓；但 `10`/`20` 是 `90:40` 所称「Schema Source of Truth」，其正文（`10 §6.3`）已改 | 需 Owner 界定（见 §6 D-2） |
| 14 | 「未重开其他 Owner Decision / 未新增状态」 | 未改 `90 §4:376` / `91 §3.1` 状态词表 ✓；`APPROVED` 沿用该文件 Summary Table 既有词汇（OD-01…OD-05 行同为 `**APPROVED**`）✓ | **TRUE**（此点报告处理得当） |
| 15 | 「`10 §6.3` 原文只写 `role_index = options/多值顺序`」 | `10:459` 逐字一致 | **TRUE** |

---

## 5. 无法核验项（UNKNOWN）

```text
U-1  任务书 §5 原文（「只做让 Frozen Spec 明确表达该 Owner Decision 所必需的最小文字修改」）
     —— 该任务书**不在仓库内**，DSH 无法核验其是否构成对 `Docs/V3_SPEC/` 的 L0 修改授权。
     ⇒ 归入 Owner 裁决（§6 D-1），DSH 不做判断。
U-2  远端独立复核：`git ls-remote origin od01-r3-convergence` 受凭据策略阻断
     （schannel SEC_E_NO_CREDENTIALS）。本地 remote-tracking ref = `71f51f9`，与其自述一致，
     但**未从远端独立证实**「L0 修改已公开在远端」。
U-3  OD-R-01 是否与统一仓（AITutorX）既有裁决冲突：`Docs/40_DECISIONS/**` 中
     `OD-R-01` = 0 命中；`多空/多个空/Answer 对象/multi-value/有序值` 仅命中
     `single_choice / multiple_choice / true_false / fill_blank` 等题型清单行 ⇒ **未见直接冲突**，
     但 OD-R-01 在统一仓**无落点**（信息性，非缺陷；与 OD-01 系列落点惯例一致）。
```

---

## 6. Owner 裁决清单（本审查提出的待裁项）

| ID | 待裁问题 | 为何必须 Owner 裁 |
|---|---|---|
| **OD-R-01-D1** | 任务书 §5 是否构成对 `Docs/V3_SPEC/`（L0）的**修改授权**？ | 任务书不在仓内，DSH 无法核验；此点为 F-01 的分水岭 |
| **OD-R-01-D2** | 若授权有效：如何补齐仓内合规模块——L1（Contract Change Record）落点 / `90 §11` Change Audit Record / **新 Frozen Spec tree hash 登记** / F-03 的 4 处现行断言更正 | 涉及 L0 治理结构，非实现者可自决 |
| **OD-R-01-D3** | 若授权无效：是否回退该 L0 改动（**新 commit 反向修改**，不 rewrite history），仅保留 D1 登记 | 不可逆动作已 push，回退方式需 Owner 指定 |
| **OD-R-01-D4** | F-06 的残留（payload `answer[]` 元素粒度、`answer_status` 挂载点）在仓内的正式落点（84 台账 / GAP registry / D1 追加） | 决定「闭环」是否成立 |
| **OD-R-01-D5** | F-07 报告理由更正（`20 §6.3` 一行的理由为推论过度）是否要求 | 治理文档中被引用的错误理由会污染后续轮次 |
| **OD-R-01-D6** | F-08 —— `value[i]` 指称与「N 值 → 1 行还是 N 行」是否要求写入 L0 | 若要求 ⇒ 又一次 L0 修改，须先解决 D2 的授权 / 审计链 |
| **OD-R-01-D7** | F-04 的 push-前 STOP 纪律是否要求纠正（先停后问 vs 先做后问） | 属执行纪律，影响后续阶段 |

---

## 7. 应予记分之处（对抗性审查的平衡记录）

```text
+ 主动披露治理张力：报告未隐瞒「动了 Frozen Spec」这一点，末尾专门写出并给出回退选项
+ 结尾正确 STOP：按 §12 停止，未继续寻找新 GAP、未做 corner-case 分析、未扩展为 Answer/Evidence 重构
+ 残留披露：payload `answer[]` 与 `answer_status` 挂载点被明确列为「不偷偷并入」
+ 落点计数与事实数字：10×1 / 20×1 / D1×4、ABD 条款、3 文件 80/1、commit/branch —— 逐条实测为真
+ 未触碰实现面：无 code / DDL / migration / 字段表改动；新增行 forbidden-artifact 扫描 0 命中（已复现）
+ 登记沿用既有载体：未新建 Decision 管理体系、未自创 registry（符合 91 §5.1 门槛纪律的取向）
+ 词汇说明正确：`APPROVED` ∉ `90 §4:376` / `91 §3.1` 冻结枚举，且沿用该文件 Summary Table 既有写法 —— 说明准确
+ `10:459` 原文引用准确（「role_index = options/多值顺序」逐字一致）
```

---

## 8. 附：机械验证命令（可复现）

```powershell
$r='D:\Project\AITutors-v3'
git -C $r rev-parse HEAD
git -C $r rev-parse '9f1763e:Docs/V3_SPEC' ; git -C $r rev-parse '71f51f9:Docs/V3_SPEC'
git -C $r show --numstat --format='' 71f51f9
git -C $r show 71f51f9 -- Docs/V3_SPEC
git -C $r grep -n -I 'b3eeb3e9' -- Docs/          # F-03：断言旧 tree hash 的现行/历史文档
git -C $r grep -n -I '多值' -- Docs/V3_SPEC/      # F-08：L0 既有措辞
git -C $r show 71f51f9 -- Docs/V3_SPEC | Select-String '^\+[^+]' |
  Select-String 'CREATE|UNIQUE|CONSTRAINT|ENUM|NULLS NOT|migration|ALTER|sqlalchemy'   # 报告声称的 0 命中（已复现）
git -C $r ls-remote origin od01-r3-convergence     # U-2：需凭据，本环境受阻
```

---

*DSH 独立对抗性审查 · 对 git 对象与仓内文本取证 · 审查期间未修改任何文件、未 push · 全部结论均可由 §8 命令复现。*
