# OD-01V4R R3（四阻断项闭合轮）— DSH 独立对抗性审查

```text
Document ID:            OD-01-V4R-R3-DSH-ADVERSARIAL-REVIEW
Document Type:          Gate Report
Status:                 PENDING
Authority Level:        L3
审查对象:               OD-01 FINAL CONVERGENCE REMEDIATION（Claude 交付说明）
被审仓:                 AITutors-v3 @ 6d8a3bd71f3b3977875b3040773ce23b02db19f9（工作区 = HEAD，无未提交改动）
被审基线:               81b2080（parent）
DSH 前轮:               04ccba2（OD-01-V4R-FINAL-REMEDIATION-R2-DSH-ADVERSARIAL-REVIEW.md）
审查性质:               独立对抗性验证（不采信交付说明；以仓内可机检证据为准）
DSH 修改被审仓:         0 文件（只读审查；未触碰 Frozen Spec / Schema / Code / 被审任何文件）
```

---

## 0. 审查方法

### 0.1 证据等级

| 等级 | 含义 |
|------|------|
| **DIRECTLY VERIFIED** | DSH 直接执行命令 / 读取字节后成立 |
| **VERIFIED BY INSPECTION** | 逐行读取仓内文件后成立 |
| **DOCUMENT CLAIM** | 仅见于交付说明或仓内散文，无独立证据 |
| **UNKNOWN** | 无法从两个仓的任何可达状态验证 |

### 0.2 本轮实际执行

```text
git -C AITutors-v3 rev-parse HEAD / origin/main / rev-list --left-right --count
git -C AITutors-v3 cat-file -t 6d8a3bd…
git -C AITutors-v3 show --numstat/--shortstat/--name-only/--format=… 6d8a3bd…
git -C AITutors-v3 diff 81b2080 6d8a3bd -- <5 files>          （完整 diff，逐 hunk 读取）
git -C AITutors-v3 diff --check 81b2080 6d8a3bd / --check     （空白告警）
git -C AITutors-v3 rev-parse '81b2080:Docs/V3_SPEC' '6d8a3bd:Docs/V3_SPEC' 'HEAD:Docs/V3_SPEC'
git -C AITutors-v3 rev-parse '81b2080:Docs/DECISIONS' '6d8a3bd:Docs/DECISIONS'
git -C AITutors-v3 grep -n/-c -- <关键词>                     （table_id / NOT RELEASED / L2-proposed / 未决依赖 / …）
git -C AITutors-v3 show <rev>:<file> + PowerShell 行级读取（UTF-8 显式解码）
SHA-256 比对：OD-01-A…J 十行 / OD-01-H 行 在 81b2080 与 6d8a3bd 之间
mtime 取证：5 个变更文件 + 13 个未跟踪文件 + 84_CONFLICT_LEDGER.md
两个仓全文检索：授权依据 / BLOCKER-2 / BLOCKER-3 / 只允许处理 / FILE SCOPE / 允许集
```

---

## 1. 结论速览

```text
判定 = VERIFIED WITH FINDINGS（本轮修复动作实质性成立）
Closure Blocking = YES（尚待 Owner 处置 5 项；均为 Owner 权限内事项，非修复失败）

主张属实度：4 / 4 主张的**事实基础**成立
           3 项可无条件采信（F-53 / L0-META / F-50 于所列落点）
           2 项结论口径须加限定（F-50 未覆盖同文件同类残留；OD-01-H 依赖自撰字段名）
本轮动作闭合度：前轮 3 项 Closure Blocking 中的 2 项实质解除，1 项（F-53）解除
交付说明不实项：1（未跟踪文件计数 10 → 实测 13）
交付说明未披露项：3（D1:301-308 同类残留 / 授权依据无仓内记录 / 仓内登记与本轮结论不一致）
```

| 主张 | 判定 | 依据等级 |
|------|------|----------|
| `F-53: RESOLVED` | **属实**（判据分支达成；台账义务仍开放，已被如实列为 Remaining#1） | DIRECTLY VERIFIED |
| `F-50: RESOLVED` | **属实（限于所列落点）**；同文件同类残留 D1:301-308 未处置未登记 | DIRECTLY VERIFIED |
| `L0-META: PRESERVED AS BASELINE CONFLICT` | **属实**（事实基础 + 落点全部实测成立） | DIRECTLY VERIFIED |
| `OD-01-H: RESOLVED WITHOUT NEW STATUS` | **属实**（未新增 Status；五词归属表与主张逐字一致）；但依赖 agent 自撰非冻结字段名 | DIRECTLY VERIFIED |

---

## 2. Git 与隔离事实（DIRECTLY VERIFIED）

| 项 | 交付说明 | 实测 | 判定 |
|---|---|---|---|
| Base | `81b2080` | `6d8a3bd` 的 parent = `81b20803a2e032254e7082450d7846e7b8b850c0` | ✓ |
| DSH reference | `04ccba2` | AITutorX `HEAD = origin/main = 04ccba200847cc03bc9d111a07c542fb3d0b042d` | ✓ |
| Commit | `6d8a3bd71f3b3977875b3040773ce23b02db19f9` | `git cat-file -t` = commit；对象存在 | ✓ |
| 规模 | 5 files, 218 insertions, 126 deletions | `--shortstat` = `5 files changed, 218 insertions(+), 126 deletions(-)` | ✓ 精确 |
| Push | NO | `rev-list --left-right --count origin/main...HEAD` = `0  12`；`origin/main = 7934844` | ✓ |
| 工作区 | — | `git status --porcelain --untracked-files=no` **空**（无未提交改动） | ✓ |

**逐文件 diff 归属（按 numstat + mtime 双证据）**

| 文件 | 81b2080..6d8a3bd | 前轮（R2）测得 | mtime | 轮次归属 |
|---|---|---|---|---|
| FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md | 105 / 57 | 92 / 55 | 2026-09-24 09:59:37 | 本轮 |
| CONTRACT-CHANGE-RECORD-CR-002-OD-01.md | 6 / 4 | 6 / 4 | 2026-09-24 10:01:12 | 本轮（见注） |
| OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md | 65 / 50 | 62 / 47 | 2026-09-24 10:05:12 | 本轮 |
| Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md | 6 / 8 | 6 / 8 | 2026-09-24 08:39:56 | 前轮（未提交，本轮入库） |
| Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md | 36 / 7 | 36 / 7 | 2026-09-24 08:45:58 | 前轮（未提交，本轮入库） |

> **注（CR-002 归属）**：CR-002 的 numstat 与前轮相同（6/4），但其 `:99` 内容已由「`table_id` 生产来源 = 未决依赖」改写为「真实存在的 Preprocessing source identity…当前不存在…」，且 mtime（10:01:12）晚于前轮文件（08:39/08:45）、早于 D1（10:05:12）。numstat 不变的机制 = 该行仍是「删 1 行 / 增 1 行」。⇒ 交付说明「本轮 3 个文件」**成立**。

---

## 3. 边界声明核对（DIRECTLY VERIFIED）

| 声明 | 实测 | 判定 |
|---|---|---|
| Frozen Spec changed: **NO** | `git diff 81b2080 6d8a3bd -- Docs/V3_SPEC` **0 行**；`81b2080:Docs/V3_SPEC` = `6d8a3bd:Docs/V3_SPEC` = `HEAD:Docs/V3_SPEC` = `b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` | ✓ |
| Code changed: **NO** | 提交文件清单内 `backend/` `preprocessing/` `scripts/` 命中 **0**；工作区无其他改动 | ✓ |
| Schema changed: **NO** | 提交清单内无 schema 文件；无新增文件 | ✓ |
| Migration: **NOT AUTHORIZED** | 无 migration 产物；属负向声明 | ✓（一致） |
| X3: **NOT ENTERED** | 仓内无 X3 产物 | ✓（一致） |
| 新建文件: **0** | 未跟踪文件全部 mtime ≤ 2026-09-17 21:01（见 §6.8） | ✓ 结论成立 |
| `Docs/DECISIONS/` 未触碰 | `81b2080:Docs/DECISIONS` = `6d8a3bd:Docs/DECISIONS` = `f21a5d32e900f04735632f05c258b8bf75dccbad`；`84_CONFLICT_LEDGER.md` mtime = **2026-09-13 22:38:31** | ✓ 台账零写入 |

---

## 4. 四项主张逐项验证

### 4.1 `F-53: RESOLVED` → **属实（DIRECTLY VERIFIED）**

DSH 前轮必要修正第 3 条为**择一**：

```text
「并为 table_id 给出可核验判据，或明确「table_cell 条款暂缓写入」并登记 84 台账义务」
```

前轮判定「均未满足」，理由是判据被写成**不可核对**（Proposal 旧「四字段逐一可核对」表中 `table_id` 一行明写「当前是否可核对 = 否」）。本轮**改写了判据本身的性质**：

| 交付说明 | 实测坐标 | 判定 |
|---|---|---|
| 判据 = 五条同时成立（Proposal §5 `:294-302`） | §5 起点 `:281`；`**可核验判据（逐条可判定，F-OD01V4R-53）：**` 在 `:294`；五条件表 `:296-302`，列为 `# / 条件 / 核对方式 / 实测核对结果` | ✓ **坐标精确** |
| 同判据写入 CI-2 Proposed Frozen Text | CI-2 = `10_Data_Model.md §4`（`:341`）；其 **Proposed Frozen Text** = `:354-381`，内含 `可核验判据：` + 五条（`:370-376`）+ 来源要求（`:377-378`）+ fail-closed（`:379-380`） | ✓ **主张的 CI-2 正确** |
| canonical identity 未改（Option B） | `:284` / `:361` = `(source_version_id, table_id, row_index, column_index)`，与 81b2080 相同 | ✓ |
| table_id 来源 = 真实存在的 Preprocessing source identity；V3 只 validate/verify/normalize/preserve | `:304`；`:377-378`「table_id 只取生产来源给出的值；V3 不识别 table、不为 table 编号、不按 HTML/Markdown 顺序或视觉内容推断、不由 LLM 生成」 | ✓ 逐字符合 |
| 实测 `CONTRACTS/` · `GOVERNANCE/` · `V3_SPEC/` 各 0 命中 | `git grep -c table_id`：`Docs/COORDINATION/CONTRACTS/` **0**、`Docs/GOVERNANCE/` **0**、`Docs/V3_SPEC/` **0** | ✓ **精确** |
| 仅 `docs_archive/` V2 遗留草稿 14 命中 | `docs_archive/2026-09-03/01_ImmutableSource…v0.3.md`=6、`…/03_SourceResolver…v0.3.md`=1、`docs_archive/2026-09-05_v2_legacy/DSD.md`=7 ⇒ **14** | ✓ **精确** |
| `10 §4` M1 裁剪不建 | `10_Data_Model.md:107-108`：「**M1 裁剪**：`document_source_tables / _cells / _fragments` 不建」 | ✓ 逐字存在 |
| fail closed → `unresolved` / `incomplete` 进 review | `:306`、`:379-380` | ✓ |
| 四元组 / 状态值域 / schema 均未新增 | 四元组与 81b2080 相同；`unresolved`/`incomplete` 属既有 `option_evidence_status` 值域（`:191`）；无 schema 产物 | ✓ |

**判定理由（对前轮结论的更正）**：判据已从「宣告不可核对」改为**带核对方式的五条合取谓词**，其当前取值为**假**（条件 2、5 实测「不成立」）—— 即「可核验、且现时为假」，而非「不可核验」。这正是 DSH 前轮要求的「可核验判据」分支。⇒ **F-53 的前轮闭塞条件解除，主张属实。**

**仍未闭合（不作为 F-53 修复失败，属 Owner 权限）**：`90 §5 Rule 4`（`90:430`「指不出唯一生产者的字段 = 治理缺口，进台账」）的履行 —— `84_CONFLICT_LEDGER.md` 零写入、无任何可机检落点（交付说明 Remaining#1 已如实登记）。另见 §5.2（仓内登记与本轮结论不一致）。

### 4.2 `F-50: RESOLVED` → **属实（限于所列落点）；同文件同类残留未处置（DIRECTLY VERIFIED）**

DSH 前轮指定的 4 个落点 + 前轮残留 N-5 落点（D1 `:392`）逐项实测：

| 落点 | 前轮要求 | 实测（6d8a3bd） | 判定 |
|---|---|---|---|
| D1 文件级 Header | `STATUS: RECORDED` / `AUTHORITY: OWNER DECISION RECORD` → 合法字段 | `:7 Status: ACTIVE`（六值表内）；`:8 Authority Level: L2`；`:17 Record State: RECORDED（非 Status 字段值…）` | ✓ |
| D1 OD-01R 附录 `Status` 列（9×`VERIFIED`） | 列名改 | `:313` = `\| ID \| Finding（DSH） \| Owner Decision \| Required Action \| Verification Result \|` | ✓ |
| D1 V4R-15…29 附录 `Status` 列（15×`VERIFIED`） | 列名改 | `:469` = `… \| Applied Fix \| Verification Result \|`；更正注 `:487` | ✓ |
| D1 Document control `\| Status \| RECORDED \|` | 改 | `:545 \| Status \| ACTIVE \|` + `:546 \| Record State \| RECORDED \|` | ✓ |
| **D1 `:392` 段（前轮 N-5）** | STATUS: / AUTHORITY: 落位 | `:391 RECORD-TYPE: …（非 MIMO 建议 / 非 DSH 建议 / 非 Proposal 自述）`（原括注并入）✓；`:392 Record State: OWNER APPROVED RECORD / PENDING EFFECTIVE FREEZE` ✓；`:393 Authority Level: L2` ✓；`:394 DATE` / `:395 BINDING FOR EXECUTION: YES` / `:396 EFFECT ON L0: NOT EFFECTIVE（PENDING EFFECTIVE FREEZE）` **逐字保留** ✓ | ✓ |

补充实测：

- 交付说明称「OD-01-A…J 十行 Decision / Required Action / Verification Result 一字未改」→ **SHA-256 比对 81b2080 与 6d8a3bd 的 10 行：完全相同**（`F7D2B4CD…DD90`）✓
- 交付说明称「零新字段名」→ `Record State` 系 D1 `:17` 既有字段名 ✓；`:392` 使用处未新造字段名 ✓
- 交付说明称「零新 Status 取值」→ `ACTIVE` 同时属 `90 §4:376` 六值表与 `91 §3.1` 十值表 ✓
- D1 diff 的 8 个 hunk 中，A…J 表**仅表头 1 行**变更，10 行数据行全部为上下文 ⇒ 与 SHA-256 结果互证 ✓

**残留（本轮未处置、未登记，见 §5.1）**：D1 `:299-308`（OD-01R 段）仍为**旧式块头**：

```text
:302  RECORD-TYPE: OWNER DECISION / FINDING DISPOSITION
:303  AUTHORITY: OWNER DECISION（非 MIMO 建议 / 非 DSH 建议 / 非 Proposal 自述）   ← 自述 AUTHORITY 字段仍在
:304  SOURCE: DSH targeted review F-OD01R-01…F-OD01R-10
:305  DATE: 2026-09-23
:306  BINDING: YES
:307  EFFECT: 指导 OD-01 Proposal v3 + CR-002 治理化；不修改 Frozen Spec / Contract / 代码
```

`F-OD01V4R-50`（= `OD-01F-83`）的 Problem 原文（Proposal §0 `:129`）为「条件 3/4 以缩小口径达成；D1 仍含列名为 `Status` 的非枚举值与**旧式文件级 Header**」。`:301-308` 恰属「旧式（块）Header」，且含自述 `AUTHORITY:` —— 同一缺陷类在同一文件仍有 1 处。⇒ 主张**限于所列落点属实**；作为 `F-OD01V4R-50` 的整体结论，「RESOLVED」未覆盖该处，交付说明亦未披露（Remaining 表未列）。

> **编号歧义提示（LOW）**：D1 `:473` 另有一行 `F-OD01V4R-17 | **OD-01F-50** | Header 含 Purpose；字段名 Derives From` —— 与 `F-OD01V4R-50` 分属不同 Finding，Fix 内容无关。交付说明与 DSH 前轮均以「F-50」简称 `F-OD01V4R-50`；在 D1 中按「F-50」检索会命中另一项，属引用歧义（见 R3-10）。

### 4.3 `L0-META: PRESERVED AS BASELINE CONFLICT` → **属实（DIRECTLY VERIFIED）**

| 交付说明 | 实测 | 判定 |
|---|---|---|
| `90 §4:375` / `90 §4:376` / `91 §5:167` / `91 §3.1` 零改动 | `Docs/V3_SPEC` tree 三处相同 = `b3eeb3e9…`；四处原文逐行读取 | ✓ |
| 冲突记于 Proposal §2.1、§2.3、CR-002 §1 | Proposal `:178`（§2.1 归因分列，含「two L0-META…pre-existing Frozen/L0 governance baseline conflict」）、`:230`（§2.3 既存基线冲突）；CR-002 `:67`（§1，CR-002 的 §1 = `:60-73`） | ✓ 坐标正确 |
| 全文无「`90 §4` 已定义 `L2-proposed` / `PENDING`」类错误引用 | 全 `90 §4` 引用逐条审阅：`:25` / `:178` / CR-002 `:67` 均**正确**记述「`90 §4:375` 不含 `L2-proposed`」；`§2.3:203` 正确记六值表 | ✓（窄口径成立） |
| Remaining#3 附带事实：`90:81` 目录层表列有 `L2-proposed`，而 `90 §4:375` 枚举无 | `90_DOCUMENT_GOVERNANCE.md:81` = `\| Docs/REPORTS/ \| L3 / L4 / L2-proposed \| …` | ✓ **精确** |

**冲突事实本体（独立复核）**：

```text
90:375  Authority Level: <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>            ← 无 L2-proposed
91:167  Authority Level: <L0 | L0-META | L1 | L2 | L2-proposed | L3 | …>   ← 有 L2-proposed
90:376  Status: <ACTIVE | SUPERSEDED | HISTORICAL | DRAFT | CLOSED | NOT RELEASED>   ← 无 PENDING
91:168  Status: <ACTIVE | SUPERSEDED | HISTORICAL | DRAFT | CLOSED | NOT RELEASED>   ← 无 PENDING
91:113-122 §3.1 允许的状态值（十值，适用层「全部」）：OPEN / PENDING / CONDITIONAL PASS /
           CLOSED / NOT STARTED / DEFERRED / SUPERSEDED / RETRACTED / ACTIVE / HISTORICAL  ← 含 PENDING，无 NOT RELEASED
```

⇒ 声明为「既存 L0-META 基线冲突、非 OD-01 规范缺陷」与事实一致。**但须记录其副作用**：该声明使 Proposal `:7`/`:801`、Remediation Report `:7`/`:128`、D1 `:449`/`:497` 的 `Status: PENDING`（不受六值 Header 模板覆盖）获得追溯豁免 —— 即「规则被自己的例外吸收」，这是**声明性**处理，非冻结依据（见 §5.6）。

### 4.4 `OD-01-H: RESOLVED WITHOUT NEW STATUS` → **属实（含限定）（DIRECTLY VERIFIED）**

| 交付说明 | 实测 | 判定 |
|---|---|---|
| 五词按字段归属分类，记于 Proposal §2.3 | `:220-228` 表：`APPROVED`→`Decision`、`PENDING`→`Status`（十值内）、`VERIFIED`→`Verification Result`、`NOT EFFECTIVE`→`EFFECT ON L0`、`NOT REGISTERED`→`Registration Level` | ✓ **逐词一致** |
| 未新增任何 Status | 本轮未新增 Status 取值；`:217` 明列被移出 `Status` 字段的旧值 | ✓ |
| OD-01-H 原文未改写 | D1 `:412` 行 SHA-256 比对 81b2080 vs 6d8a3bd = **相同**（`\| **OD-01-H** \| APPROVED \| 删除模糊完成类状态词（91 §3.2）；仅用 APPROVED / PENDING / VERIFIED / NOT EFFECTIVE / NOT REGISTERED \| VERIFIED \|`） | ✓ |

**限定**：本项成立的前提是「`Verification Result` / `Decision` / `EFFECT ON L0` / `Registration Level` 均非 `Status` 字段」这一**agent 自撰**口径（Proposal `:207-215`，L2-proposed，非冻结）。实测 `Record State` / `Verification Result` / `Finding Disposition` / `Registration Level` 在 `Docs/V3_SPEC` **全部 0 命中** ⇒ 归属模型无 L0/L0-META 词表依据，仅靠 L2 自撰规则支撑。同时 Remediation Report `:113`（本轮未更新）仍写「请 Owner 裁定二者关系」⇒ **Owner 裁定请求在仓内仍未关闭**。

---

## 5. 本轮新发现（R3-01 … R3-10）

### R3-01（MED）— D1 OD-01R 段旧式块头 + 自述 `AUTHORITY` 未处置、未登记

- 位置：D1 `:301-308`（`## OD-01R — …` 段的活动记录块）。
- 事实：`:303 AUTHORITY: OWNER DECISION（非 MIMO 建议 / 非 DSH 建议 / 非 Proposal 自述）`；块内无 `Status` / `Authority Level` / `Normative` / `Derives From` 等出生证明字段，仍为 `RECORD-TYPE / SOURCE / DATE / BINDING / EFFECT` 旧式。
- 与主张关系：F-50 的 Problem 明含「旧式文件级 Header」⇒ 同类缺陷在同文件、授权范围内仍有 1 处；交付说明 Remaining 表未列。
- 与 DSH 关系：**DSH 前轮亦遗漏该处**（前轮报告 `:148` 以 `:302-313` 为 OD-01R 范围、只核了列名）——见 §8 L-2，属 DSH 自陈更正。
- 处置：属 §3「只允许处理 4 项」范围外 ⇒ 不修正是合规的；**但必须登记或豁免**，否则「F-50 RESOLVED」的文件级结论不成立。

### R3-02（MED）— 「D1:392 授权依据」无仓内落点（Remaining#4 的「特此登记」不可核验）

- 交付说明 Remaining#4 称：授权依据 = 「本 Owner Order（§1.1『本次只允许处理以下 4 项』含 BLOCKER-2 + §5.1）」，并称「仓内无更早的独立授权记录（§5.3 检查结果），**特此登记**」。
- 实测（两仓全文检索）：`授权依据` **0 命中**；`BLOCKER-2` / `BLOCKER-3` **0 命中**；`只允许处理` **0 命中**；`FILE SCOPE` / `允许集` 仅命中 Remediation Report `:111` 的范围括注（「限 `Docs/COORDINATION/**`、`Docs/REPORTS/**`」）—— 那是**范围声明**，不是授权记录。
- 结论：「Owner Order §1.1/§5.1/§5.3/§8」**在两仓任何可达状态中不存在** ⇒ 该授权依据为 DOCUMENT CLAIM（UNKNOWN）。
- 后果：D1 `:13` 自述 `Must Not Change: … · 历史决策语义`，而 `:392` 记录的是 Owner 决策元数据；前轮 DSH 明确要求「只能由 Owner 改写、**或书面记录豁免，并同步进 D1 报告 Remaining Risk**」。改写已发生，但（a）授权依据无仓内记录，（b）报告 Remaining Risk（`:107-118`，本轮未更新）**仍未登记**该事项 ⇒ 前轮 N-5 的后半部分**未闭合**。

### R3-03（MED）— 仓内登记与本轮「RESOLVED」结论不一致（OD-01F-97 类复发）

| 仓内位置（6d8a3bd） | 原文要点 | 与本轮交付说明的冲突 |
|---|---|---|
| Remediation Report `:75` | F-53：「**构造性残留**…消解须发明生产者（禁止）或暂缓条款（超授权）⇒ **未决风险**」 | 交付说明：`F-53: RESOLVED` |
| Remediation Report `:109-110` | 「…可识别前 `table_cell` 不得 `resolved`」/「条款**恒不可满足**。消解途径均超本轮授权…⇒ STOP + 未决风险」 | 同上（且「恒」已不准确：条件 2 成立时判据可满足） |
| Proposal §0 `:132`（F-OD01V4R-53 行 Finding Disposition 列） | 「元陈述移出 Proposed Text；`table_id` 记**未决依赖**；构造性残留与 `84` 台账义务记**未决风险**」 | 同上 |
| Remediation Report `:96` | 完成条件 3 = 「Header 仅冻结枚举」 | 与 D1 `:303 AUTHORITY:`、Self Review `:43/:124` 并存 |

- 性质：报告 `:75/:109-110` 与 D1 `:132` 是**上一轮的登记**，本轮未更新（若 §8 授权仅 3 文件，则「不更新」合规）；但**未更新**导致仓内出现两套结论（报告：未决风险 + STOP；交付说明：RESOLVED）。交付说明未声明「仓内报告已过时」。
- 归类：即 OD-01F-97（交付说明与仓内证据不一致）同类复发。

### R3-04（MED-LOW）— `未决依赖` 为未定义词，且本轮**新增 2 处占用**（含替换冻结词汇标签）

- 实测：`未决依赖` 在 `Docs/` 共 6 处（Proposal `:25`、`:132`；CR-002 `:71`；Report `:72`、`:75`、`:109`），`Docs/V3_SPEC` **0 命中**，无任何定义句。
- 本轮新增：Proposal `:25`（新增句「两表值域不一致属**未决依赖**，见 §5」）与 CR-002 `:71`（新增行 `**未决依赖：** 冻结枚举无法表达「决策/提案/变更记录」三分角色…`）。
- 加重情节：CR-002 `:71` 系由冻结词汇标签 `**Planning Category: Future Required Change** — …` **替换**而来（diff `-`/`+` 可证），而 Proposal `:30` 与 §10（`:764-780`）仍将 `Future Required Change` 作为唯一合法规划分类，且 `:777` 仍以该标签登记 `table_id 生产来源`。⇒ 与 OD-01F-62「Future 词 = Planning Category only」的收口方向相反，且同一事项在两文件获得两种分类标签。
- 交付说明称「N-4 中『未决依赖』措辞随 F-53/3 改写自然变化——不可避免的机械副产物」⇒ **低估**：本轮是**扩张**该未定义词的占用面并**替换**了既有冻结标签。

### R3-05（LOW-MED）— Proposal `:25` 新增交叉引用指向错误

- 原文：`…两表值域不一致属未决依赖，见 §5。`
- 实测：Proposal §5 = `:281-313`（table_cell identity），全文**不含** Authority Level / 值域内容；值域冲突实际记于 `:178`（§2.1）与 `:230`（§2.3）。
- 若「§5」本意指 Remediation Report 的 §5（`## Remaining Risk` 段位于 `:105`），则属**跨文件坐标未标注**；无论何种解释，该引用在本文件内不成立。

### R3-06（MED-LOW）— N-1「表列 Status 一律十值表」规则被同一 change set 多点证伪（实例扩展）

规则原文：Proposal `:212`「表列状态 \| `Status` \| 取值来自十值表；适用于含历史表、附录表、Document control 表在内的一切同名列」；`:211`「Header 状态 \| `Status` \| 取值来自六值表」。

| 反例 | 实测 | 是否被本轮 `:230` 声明覆盖 |
|---|---|---|
| CR-002 `:149` `\| Status \| NOT RELEASED \|`（§7 Document control） | `NOT RELEASED` ∉ 十值表（属六值表） | **否** |
| Self Review `:124` `\| Status \| HISTORICAL — SELF REVIEW \|`（历史区 Document control） | 该复合值 ∉ 六值表亦 ∉ 十值表 | **否** |
| Proposal `:7`/`:801`、Report `:7`/`:128`、D1 `:449`/`:497` `Status: PENDING` | `PENDING` ∉ 六值表（Header 模板），∈ 十值表 | **是**（`:230` 既存基线冲突声明） |

⇒ 本轮 `:230` 的声明**仅**消解 `PENDING` 子集；N-1 另两类反例仍成立（且 `:212` 是 agent 自撰规则，非冻结条款）。交付说明已把 N-1 列为「未处理（§3 禁止）」✓，但未提示该规则的证伪面已扩大。

### R3-07（LOW-MED）— D1 `:340` 假引用 `91 §3.1` 含 `NOT RELEASED`（本轮未列、DSH 前轮亦未列）

- 原文（D1 只读核对表）：`\| `91 §3.1` \| 合法 Status 含 `NOT RELEASED`（先例：`67`） \|`
- 实测：`91 §3.1`（`:113-122`）十值**不含** `NOT RELEASED`；该值属 `90 §4:376` / `91 §5:168` 六值表。
- 加重情节：该行是 OD-01R-01「正式 L1 登记」判定依据链的一环（`:331-358`）；且与同一 change set 新写的 `§2.3:203`/`:230` **自相矛盾**。与 Proposal `:745`（N-2，前轮已记）属同一缺陷类，但位置与文件不同。
- 该行在 81b2080 中已存在（不在本轮 diff 内）⇒ 非本轮引入，但**未登记**于报告 N-1…N-8 清单。

### R3-08（LOW）— 「10 个 untracked」计数不实（实测 13）

- 交付说明：`新建文件: 0（10 个 untracked 全为 2026-09-15…17 历史遗留，未触碰）`
- 实测：`--untracked-files=all` = **13** 个文件（`Docs/COORDINATION/CONTRACTS/` 9 + `Docs/GOVERNANCE/` 4）；`git status --porcelain`（默认）显示 10 行 = 9 文件 + 1 目录行 `Docs/GOVERNANCE/` ⇒ 计数源自**目录行未展开**。
- 结论修正：**「新建文件 = 0」成立**（13 个文件 mtime 全部落在 2026-09-15 23:59 … 2026-09-17 21:01，无一为本轮新建/触碰）；计数「10」不实。

### R3-09（LOW）— `Record State` 同名字段承载两个不相容值域；`F-50` 落点未就地声明「非 Status」

- D1 `:17` `Record State: RECORDED（**非** Status 字段值…）` vs D1 `:392` `Record State: OWNER APPROVED RECORD / PENDING EFFECTIVE FREEZE`。
- `:392` 使用处**未**就地声明「非 Status 字段」，仅在 `:17` 声明（且该括注针对 `RECORDED` 值）；同名字段两个值域 = 与 OD-01F-27（同名字段命名冲突）同类，但量级远低。
- 另：`Record State` / `Verification Result` / `Finding Disposition` / `Registration Level` 在 `Docs/V3_SPEC` 全检索 **0 命中** ⇒ 这些落位字段名均为非冻结词汇，F-50/OD-01-H 的合规性建立在 L2 自撰规则上（见 §5.6 L-5）。

### R3-10（MED-LOW）— `F-OD01V4R-49…64` 无 D1 登记面；本轮修订后的 F-50/F-53 处置缺 L2 登记

- D1 全部 `## ` 段：`OD-01`/`OD-02`/`OD-03`/`OD-04`/`OD-05`/`G-01`/`G-02`/`Terminology`/`Effective Scope`/`OD-01R-01…10`（`:299`）/`OD-01-A…J`（`:388`）/`OD-01V4R-15…29`（`:443`）/`OD-01V4R-30…48`（`:491`）—— **无 `F-OD01V4R-49…64` 段**。
- 实测：D1 内 `F-OD01V4R-49…64` 仅出现在两条更正值（`:487`、`:535`）的括注中（2 命中），**无登记行**。
- 后果：前轮 16 项（F-49…64）及其本轮修订后的 F-50 / F-53 处置，仅登记在 **Proposal §0 自撰表**（`:128-143`）与 **L3 Remediation Report**（`:71-86`；其 `:9` Purpose 末句自述「本报告 `Normative: NO`，**不作裁决、不作 Owner 授权主张**」，`:20` 自述「不是 DSH Verification」）；按 D1 `:535` 自设标准（「证据指向自写 `Docs/REPORTS/…`（L3，不满足 `91:171` 向上闭包至 L0/L1/L2）」），这些处置**无 L2 登记面**。
- 说明：若 §8 授权仅限 4 个阻断项，则未增设该附录属合规；但交付说明 Remaining 表未列此项，且「F-50 / F-53 RESOLVED」的登记效力因此仅及于 L2-proposed 自撰文本。

---

## 6. Remaining 6 项逐项核对

| # | 交付说明 | 实测 | 判定 |
|---|---|---|---|
| 1 | `84_CONFLICT_LEDGER.md` 台账义务未登记；落点在 `Docs/DECISIONS/`，在 §8 FILE SCOPE 之外 | `84_CONFLICT_LEDGER.md` mtime `2026-09-13 22:38:31`；`Docs/DECISIONS` tree 两 revs 相同；`90:430` 义务原文存在 | ✓ 事实成立（「§8 FILE SCOPE」本身无仓内落点，见 R3-02） |
| 2 | `table_id` 生产来源不存在；判据已成立且 fail-closed；须 Preprocessing 侧建立 | 同 §4.1（0/0/0 命中；14 命中在 `docs_archive`；`:306` fail-closed） | ✓ 精确 |
| 3 | L0-META 冲突按 BLOCKER-3 保留；`90:81` 目录层表列有 `L2-proposed` 而 `§4:375` 枚举无 | `90:81` 实测一致 | ✓ 精确 |
| 4 | `D1:392` 授权依据 = 本 Owner Order；仓内无更早独立授权记录；**特此登记** | 两仓检索：授权依据 / BLOCKER-2/3 / 只允许处理 = **0 命中**；报告 Remaining Risk 未含此项 | **部分成立**：结论（仓内无授权记录）属实；「特此登记」无仓内落点（R3-02） |
| 5 | `git diff --check` 1 处告警 = CR-002 `:70` 行尾空白；系前轮 N-3 所在行，本轮未触碰 | `git diff --check 81b2080 6d8a3bd` ⇒ **恰 1 处**：`CR-002-OD-01.md:70: trailing whitespace`；`:70` 文本与前轮记录一致（描述性快照句） | ✓ 精确 |
| 6 | N-1…N-8 未处理（§3 禁止）；N-5 已随 F-50 机械消除；N-4 措辞随改写自然变化 | N-1（`:212` 证伪，反例已扩展）/N-2（Proposal `:745` 假引用仍在）/N-3（CR-002 `:70` 描述性降级仍在）/N-6（D1 `:487`「移除前缀」与「逐字未改」并存）/N-7（§0 Problem 标题后缀仍在）/N-8 均**仍存在**；**N-5 仅在 `:392` 落点消除**（同文件 `:303` 同类仍在）；N-4 措辞**扩张**而非「自然变化」 | **部分成立**（见 R3-01 / R3-04） |

---

## 7. 对 STOP / 边界的评价

```text
交付说明末行：「If any new issue was discovered outside the four blockers: STOPPED, NOT FIXED.」
```

- **程序正确**：本轮仅改 3 个文件（Proposal / CR-002 / D1），全部落在 `Docs/COORDINATION/**`；`Docs/V3_SPEC`、`Docs/DECISIONS`、Schema、Code、Migration 全未触碰；`N-1…N-8` 明确不修 ✓。
- **边界执行严格**：`git diff -- Docs/V3_SPEC` = 0 行且 tree 三处一致；`Docs/DECISIONS` tree 不变；无新建文件；无 push（`HEAD` 领先 `origin/main` 12、落后 0）✓。
- **但 STOP ≠ 结案**：R3-01（同文件同类残留）、R3-02（授权依据无仓内记录）、R3-03（仓内登记与本轮结论冲突）、R3-10（F-49…64 无 L2 登记面）四项均属「本轮已发现但未处置/未登记」，按交付说明自设规则应为 `STOPPED, NOT FIXED` —— 交付说明事实上正是如此处理的（N-1…N-8 未修），**但 Remaining 表未把 R3-01/R3-02/R3-10 列入**，故「STOP 已覆盖全部新发现」在台账层面不完整。

---

## 8. 正面证实（P1–P10）

```text
P1  Commit 规模精确：5 files / 218 insertions / 126 deletions；parent = 81b2080；push = NO。
P2  Frozen Spec 三重一致：81b2080 == 6d8a3bd == 工作区 == b3eeb3e9…；diff 0 行。
P3  隔离成立：Docs/DECISIONS tree 不变；84 台账 mtime 2026-09-13；工作区无其他改动。
P4  F-53 判据坐标精确：§5 :294-302；且 CI-2（= 10 §4）Proposed Frozen Text :354-381 内含同一五条判据
    —— 主张的「+ CI-2」命名正确（CI-2 段 :341-384）。
P5  来源缺失判定精确：table_id 在 CONTRACTS/、GOVERNANCE/、V3_SPEC/ 各 0 命中；
    docs_archive 14 命中（6+1+7）；10:107-108 M1 裁剪原文逐字存在。
P6  F-50 落点逐字正确：:391-396 五字段值的原文（含「非 MIMO 建议 / 非 DSH 建议 / 非 Proposal 自述」、
    DATE、BINDING FOR EXECUTION、EFFECT ON L0）逐字保留。
P7  A…J 十行 SHA-256 字节级未改（与交付说明「一字未改」互证）。
P8  OD-01-H 五词归属表与主张逐词一致；D1 :412 原文 SHA-256 未改 ⇒「原文未改写」成立。
P9  L0-META 事实基础全项复核一致（90:375/376、91:167/168、91:113-122、90:81）；窄口径错误引用检索为空。
P10 诚实自认：Remaining#1（台账未登记）、#2（构造性事实 + fail-closed）、#3（冲突本体）、#5（空白告警）
    —— 四项均与实测一致，无粉饰。
```

**局限（L-1 … L-5）**

```text
L-1  「Owner Order（§1.1/§5.1/§5.3/§8）」与「Validation E 七问」在两仓均无落点 ⇒ 无法验证，
     按 DOCUMENT CLAIM / UNKNOWN 处理。本轮对该依据的**存在性**不作裁定，只记录「仓内不可核验」。
L-2  DSH 自陈更正：前轮报告以 D1 :302-313 为 OD-01R 范围却只核了 Status 列名，
     遗漏 :303 AUTHORITY: —— 本轮补记（R3-01）。此为 DSH 前轮漏检，非被审方本轮引入。
L-3  同一提交内 3 个文件的 diff 是前轮 + 本轮**累积** diff，无法从 diff 单独切分轮次；
     轮次归属依据 = mtime（09:59/10:01/10:05 vs 08:39/08:45）+ 前轮报告文本。涉归属处已注明机制。
L-4  「Migration NOT AUTHORIZED / Phase 1 NOT ENTERED / X3 NOT ENTERED / Re-freeze NOT PERFORMED」
     为负向声明，本报告只验证「两仓无相反产物或提交」，不构成对未来的保证。
L-5  F-50 与 OD-01-H 的落位依赖非冻结字段名（Record State / Verification Result / Finding Disposition /
     Registration Level，V3_SPEC 命中均 0）与 L2 自撰规则（Proposal §2.3）。
     这使「合规」= 符合 agent 自撰规则，而非符合 L0/L0-META 词表；须 Owner 明示接受该口径或改由 L1 流程确立。
```

---

## 9. 判定与 Owner 待决项

```text
OD-01V4R R3（四阻断项闭合轮）
  判定            = VERIFIED WITH FINDINGS
  主张属实度      = 4 / 4（F-50 限于所列落点；OD-01-H 附口径限定）
  本轮修复动作    = 成立（F-53 判据分支达成、F-50 所列落点达成、L0-META 声明属实、OD-01-H 未新增 Status）
  新发现          = R3-01 … R3-10（0 项主张不实；1 项计数不实：R3-08；4 项未披露：R3-01/R3-02/R3-03/R3-10）
  Closure Blocking = YES（待 Owner 处置下列 5 项；非修复失败，属权限/裁定事项）
```

### 闭合前必须由 Owner 处置（5 项）

```text
1. [L0 义务·未闭合] 84_CONFLICT_LEDGER 登记
   `90 §5 Rule 4`（90:430）义务未履行；`Docs/DECISIONS/` 不在本轮授权范围。
   处置：授权登记，或书面裁定该义务另行处置（并给出可机检落点）。
   [前轮闭合项 F-53 的台账分支至今未消解]

2. [F-50 同文件同类残留] D1 :301-308（OD-01R 段）
   `:303 AUTHORITY: OWNER DECISION（…）` + 缺出生证明字段的旧式块头。
   F-50 Problem 明含「旧式文件级 Header」⇒ 需授权改写、或书面豁免并登记。   [R3-01]

3. [D1:392 改写授权依据] 交付说明所引 Owner Order（§1.1/§5.1/§5.3/§8）两仓无落点；
   D1 :13 自述 Must Not Change 含「历史决策语义」。
   处置：以仓内可核验文件登记授权（或豁免），并同步进报告 Remaining Risk。 [R3-02 / 前轮 N-5 后半]

4. [L0-META 值域 + 词汇裁定] 90 §4:375 vs 91 §5:167；90 §4:376 / 91 §5:168 vs 91 §3.1；
   并裁定 OD-01-H 五词与 `91 §3.1` 的关系（报告 :113 请求仍未关闭），
   以及是否接受「以非冻结字段名承载 VERIFIED 等结论」这一口径。      [F-59/F-64 残留 + L-5]

5. [仓内自相矛盾项·非阻断但须记账] N-1 反例（CR-002:149 / Self Review:124）、
   N-2（Proposal:745）、R3-07（D1:340 假引用 91 §3.1）、N-3（CR-002:70）、N-6（D1:487）、
   N-7（§0 Problem 标题后缀）、R3-03（报告 :75/:96/:109-110 与 Proposal §0 :132 已过时）、
   R3-04/R3-05（未定义词 `未决依赖` + 错误交叉引用）、R3-10（F-49…64 无 D1 登记面）。
   处置建议：纳入下一轮统一收口，或在 Owner 决定中显式承认为已知项。
```

---

```text
DSH STOP。
  未修改被审仓任何文件（AITutors-v3 HEAD 仍 6d8a3bd，工作区仍无未提交改动）
  未修改 Frozen Spec / Schema / Code / MySQL / Migration
  未进入 Phase 1 / Re-freeze / X3
  等待 Owner 对上述 5 项裁定
```

**Security**：Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.
