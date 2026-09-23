# OD-01 v4R Remediation — DSH 独立对抗性审查报告

```text
Report ID:        DSH-OD-01-V4R-REMEDIATION-ADVERSARIAL-REVIEW
Report Type:      L3/L4 独立对抗性审查（DSH）
Report Repo:      kurt-wong/AITutorX  →  Docs/60_REPORTS/
Reviewed Repo:    kurt-wong/AITutors-v3（只读）
Reviewed Scope:   commit b6cb762（parent 9bd6eca）— 3 改 + 1 改（Self Review）
Reviewed HEAD:    b6cb762d453bbbd32a1459b2af7aa6860661fcfd
Independence:     本报告作者未参与 OD-01 v4/v4R 任何产出；本报告即 OD-01-J 所要求的
                  「DSH 外部验证」，被审方不得以其 Self Review 替代本报告
Date:             2026-09-23
Verdict:          VERIFIED WITH FINDINGS
Closure Blocking: YES
Recommendation:   OWNER ACTION REQUIRED BEFORE CLOSURE
```

> **本报告是审查证据，不是规则来源。** 不修改 `Docs/V3_SPEC/**`、不修改 Frozen Contract、
> 不修改被审四件交付物、不 re-freeze、不标记 OD-01 生效、不执行 Migration、不进入 Phase 1/X3。
> 发现只登记，不修复（AGENTS.md：**Provenance ≠ Quality Authority**；
> **Agent 自写的 "Frozen / Final / Authority" 不自动获得权威**）。

> **编号约定（本轮起）**：本报告沿用上一轮的 `F-OD01V4R-xx` 序列并**继续递增**（`-15` 起），
> 不新开命名空间。按被审方 §0 `:65` 的规则「新问题自 **OD-01F-44** 起递增」，
> 本报告 `F-OD01V4R-15…29` ⇔ `OD-01F-44…58`。

---

## 0. 审查边界与方法

**审查对象（只读）**

| # | 文件 | 角色 | 本轮变化（`9bd6eca..b6cb762`） |
|---|------|------|------------------------------|
| 1 | `Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md` | Proposal **v4R**（511 行） | 747 行变更 |
| 2 | `Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md` | CR-002 candidate（160 行） | 204 行变更 |
| 3 | `Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md` | D1（467 行，+OD-01V4R 附录） | 75 行变更 |
| 4 | `Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md` | **Self Review**（108 行） | 33 行变更 |

```text
2dc7a5e..HEAD 累计（供参照）：
  9bd6eca..b6cb762 = 4 files changed, 444 insertions(+), 615 deletions(-)   ← 净删除 171 行
  Proposal 行数轨迹：v3 530 → v4 692 → v4R 511
```

**证据分级**：本报告结论均为 `DIRECTLY VERIFIED`（除 §10 所列局限）。

**方法**：① 独立重放 Git/哈希事实；② 逐条质询 10 项 `VERIFIED` 声明，并**把自述的
Finding→Fix 映射反向核对**（finding 主题 vs fix 内容）；③ 对每处 `Current Rule` /
`Proposed Frozen Text` 做逐字与一致性核对；④ 把 change set 当作待写入 L0 的正式文本做
**可满足性推演**（是否引用 L0 中不存在或被明令禁止创建的实体）；⑤ 机械扫描禁用词、
强制字段、未定义命名空间、破引用；⑥ 核验跨仓副本是否真正清除。

**未做的事**：未重跑测试基线、未执行四道门、未做 corpus 对比、未修改任何被审文件、未修复发现、
未推送 AITutors-v3。

---

## 1. 对抗性盘问集（15 问）

| # | 盘问 | 判定 |
|---|------|------|
| Q1 | 自述 10 项 `VERIFIED` 是否都有证据？ | **否** — 3 项 VERIFIED / 4 项 PARTIALLY / 3 项 NOT VERIFIED（§5） |
| Q2 | Finding→Fix 映射是否「一问一号」？ | **否** — 3 行错配 + 4 项完全缺失 + 2 个空号（F-OD01V4R-15） |
| Q3 | 上一轮 HIGH（跨仓副本，F-OD01V4R-14）是否真清除？ | **已清除** ✅ 且无记录丢失（P2） |
| Q4 | 上一轮 F-OD01V4R-09（Gap 两版并存）是否修复？ | **未修复** — 且未映射、被判 VERIFIED（F-OD01V4R-16） |
| Q5 | 声明「全量 Header」是否成立？ | **否** — `Purpose` 字段在 Proposal 与 CR-002 中消失（F-OD01V4R-17） |
| Q6 | `Authority Level` 字段恢复后取值合规吗？ | **否** — 值域被自创（F-OD01V4R-18） |
| Q7 | 状态词问题解决了吗？ | **换词未归位** — 5 个允许词中 4 个非冻结值（F-OD01V4R-19） |
| Q8 | 禁用词 CLEAN 声明为真吗？ | **为真** ✅（唯一 `COMPLETE` 子串在 L0 引语 `INCOMPLETE` 内）（P4） |
| Q9 | change set 在 L0 中是否可满足？ | **table_cell 不可满足** — 依赖不存在且被禁建的 `table_id`（F-OD01V4R-20） |
| Q10 | 12 项 CI 是否仍逐条给 Current → Proposed？ | **否** — 5 项丢失 Current Rule（F-OD01V4R-21） |
| Q11 | 「逐字」标注可信吗？ | **否** — CI-4 的「逐字」块含自加行并删去 L0 第二 bullet（F-OD01V4R-22） |
| Q12 | form 用语与 OD-01 绑定用语一致吗？ | **否** — `char_span_in_line` 0 命中，无对照表（F-OD01V4R-23） |
| Q13 | Self Review 的头块合规吗？ | **否** — 围栏损坏（`` `<TAB>ext ``）+ 缺 5 字段（F-OD01V4R-24） |
| Q14 | Frozen Spec / 代码 / Schema / corpus 被改了吗？ | **未改** — tree 未变，delta 仅 4 文档（P1/P11） |
| Q15 | 本轮是否存在被误关闭的发现？ | **是** — 至少 OD-01F-40/42/43 三项无证据即标 VERIFIED（§5、§11） |

---

## 2. Git / 隔离事实（DIRECTLY VERIFIED）

```text
AITutors-v3
  HEAD          = b6cb762d453bbbd32a1459b2af7aa6860661fcfd       ✓ 与自述一致
  b6cb762^      = 9bd6ecac69465edcbb1f2bbcb5c57c31a2bfe8f5       ✓ 与自述一致
  log -3        = b6cb762 → 9bd6eca → 86da69c
  HEAD:Docs/V3_SPEC = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f   ✓ 未变
  9bd6eca..HEAD = 4 files（M×4，全为 COORDINATION / REPORTS 文档；无 A / 无 D）
  non-doc delta = 空（无 backend / schema / corpus / alembic 变更）
  branch -vv    = * main b6cb762 [origin/main: ahead 9]           ✓ 未 push
  untracked     = 9 × CONTRACTS/* + Docs/GOVERNANCE/（未动）

AITutor-X（报告仓 / 跨仓副本核验）
  HEAD = origin/main = d9173ab69358f0fdae12002d1c00d2ee6ff8bb1d
  Docs/COORDINATION/                → 目录**不存在**                        ✓ 副本已清除
  Docs/60_REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md → **ABSENT** ✓
  untracked 计数 20 → 18（减少的 2 项即上述副本所在路径）
  AITutors-v3 全仓仍无 OD-01-A-J 附录文件；其内容完整保留于 v3 D1 `:374-455`  ✓ 无记录丢失
```

**自述 Frozen Boundary Verification 逐条复核**：`git diff -- Docs/V3_SPEC` 空 ✅；
Frozen hash 未变 ✅；`Docs/V3_SPEC / backend / preprocessing` 无改动 ✅；
`AITutorX COORDINATION 副本 → 无` ✅；禁词 CLEAN ✅（见 P4 的精确口径）；
CHANGE-3/4/5 ACKNOWLEDGED ✅。

---

## 3. 自述主张逐条核验

| # | 自述 | 判定 | 依据 |
|---|------|------|------|
| 1 | F-OD01V4R-01 → OD-01F-34 VERIFIED（Self Review 改 HISTORICAL + 声明非 DSH；OD-01-J 改「DSH 外部验证」） | **VERIFIED** | Self Review `:5` `Status: HISTORICAL`；`:14-16` 显式非 DSH；Proposal `:29-35` + CR `:124-128` + D1 `:452-453` 三处同向；历史正文保留 |
| 2 | F-OD01V4R-02 → OD-01F-35 VERIFIED（全量 Header） | **PARTIALLY VERIFIED** | `Purpose` 在 Proposal/CR **缺失**；Self Review 头块围栏损坏且缺 5 字段（F-OD01V4R-17/24） |
| 3 | F-OD01V4R-03 → OD-01F-36 VERIFIED（状态列仅 5 词；禁词 CLEAN） | **PARTIALLY VERIFIED** | CLEAN ✅；但 5 词中 4 词非冻结允许值，§2.3「仅用冻结体系已有词」不实（F-OD01V4R-19） |
| 4 | F-OD01V4R-04 → OD-01F-37 VERIFIED（分型 locator；CI-4/CI-10） | **VERIFIED** | §3 `:126-136` 五类分型 + CI-4 `:288-296` 明文「禁止要求一切 form 具备 line_ref／禁止 table_cell 无任何定位」→ 上一轮矛盾消除 |
| 5 | F-OD01V4R-05 → OD-01F-38 VERIFIED（唯一 `span_resolution`） | **VERIFIED** | §2.2 `:101-110`、CI-4 `:295`、CI-6 `:331`、CI-9 `:381` 四处一致；`resolution_status` 全文 0 命中；`20 §5.5` 已入 Affected（`:300`） |
| 6 | F-OD01V4R-06 → OD-01F-39 VERIFIED（Authority Level 四类定义；Registration Level 分离） | **PARTIALLY VERIFIED** | 字段名恢复 ✅；值域自创、`Registration Level` 仍为非规范字段（F-OD01V4R-18） |
| 7 | F-OD01V4R-07 → OD-01F-40 VERIFIED（ID Mapping；一问一 Final ID） | **NOT VERIFIED** | 3 行错配 + 4 项缺失 + 2 空号 + 2 项历史遗漏（F-OD01V4R-15） |
| 8 | F-OD01V4R-08 → OD-01F-41 VERIFIED（降级态 → Future Consideration） | **NOT VERIFIED** | 该 Fix 与 finding 主题（命名空间增殖）无关；命名空间实增至第 8 套（F-OD01V4R-15/29） |
| 9 | F-OD01V4R-09 → OD-01F-42 VERIFIED（table_cell identity） | **NOT VERIFIED** | 同上错配，**且原 finding 主题未修**：Gap 记录仍两版并存（F-OD01V4R-16）；另 `table_id` 本身不可满足（F-OD01V4R-20） |
| 10 | F-OD01V4R-10 → OD-01F-43 VERIFIED（Unicode code point） | **NOT VERIFIED** | 同上错配（该 Fix 对应自审 F-OD01V4-01）；原 finding（`90 §5 Rule 2`）**未见修复**：Self Review `:67` 仍含 `不得` 且全文无 L0/L1 与 `82 §3` 引用 |
| 11 | Frozen Spec hash `b3eeb3e9…` 未变 | **VERIFIED** | 树哈希一致 |
| 12 | `Docs/V3_SPEC / backend / preprocessing` 无改动 | **VERIFIED** | name-status 仅 4 文档 |
| 13 | AITutorX COORDINATION 副本 → 无 | **VERIFIED** | 目录不存在；REPORTS 副本不存在；untracked 20→18 |
| 14 | 禁词 `DONE/COMPLETE/COMPLETED/NEXT/FINISHED/ADDRESSED/resolution_status` → CLEAN | **VERIFIED** | 四文件大小写敏感实测：全部 0 命中；D1 唯一 `COMPLETE` 命中位于 L0 引语 `INCOMPLETE`（`:57`），非状态词用法 |
| 15 | CHANGE-3/4/5 → ACKNOWLEDGED（4/5 保留四道门） | **VERIFIED** | Proposal `:452-465`、CR `:88-100`/`:111-120`；Gate A–D 全 PENDING |
| 16 | Commit `b6cb762` / Parent `9bd6eca` / ahead 9 | **VERIFIED** | 全 40 位与父链、`branch -vv` 精确一致 |
| 17 | Production / Preprocessing / Schema / Corpus / Migration / Phase 1 / Re-freeze 未变 | **VERIFIED** | name-status + `ahead 9` |
| 18 | OD-01 Proposal: READY FOR OWNER REVIEW | **PARTIALLY VERIFIED** | 形式可进入 Owner 视野；但存在 3 项 false VERIFIED、change-set 不可满足项与未修的 HIGH，不宜按「已闭环」呈报 |

---

## 4. 发现（F-OD01V4R-15 … F-OD01V4R-29）

> 全部只登记，不修复。严重度：HIGH / MED-HIGH / MED / LOW-MED / LOW。

### F-OD01V4R-15（HIGH）— Finding→Fix 映射错配 3 行、缺失 4 项、空号 2 个：「一问一号」不成立

**证据（自述表与本报告上一轮 14 项发现逐行对照）**

```text
上一轮本报告登记 14 项：F-OD01V4R-01 … F-OD01V4R-14
本轮 Finding→Fix 表仅列 -01 … -10

错配（fix 内容与 finding 主题无关）：
  F-OD01V4R-08（=「引入第 7 套命名空间，R-xx 仓库内无定义」）
     → Fix「降级态 → Future Consideration only」            ← 主题不符
  F-OD01V4R-09（=「Gap 结论两版并存；90:47 未归层后果未登记」）
     → Fix「Proposal §5：(source_version_id, table_id, row_index, col_index)」 ← 主题不符（且原问题未修，见 F-OD01V4R-16）
  F-OD01V4R-10（=「新文档违反 90 §5 Rule 2」）
     → Fix「Proposal §6：Unicode code point；0-based；start inclusive；end exclusive」 ← 主题不符（该 Fix 对应 Self Review 的 F-OD01V4-01）

完全缺失（未出现在任何映射表）：
  F-OD01V4R-11（Path 字段指向另一仓库）
  F-OD01V4R-12（Current Rule 块逐字/改写混用）
  F-OD01V4R-13（CI-12 与 CI-4 声明同文实则不同文）
  F-OD01V4R-14（HIGH：治理产物跨仓逐字节复制）

映射表内部空号与历史遗漏（Proposal `:41-63`）：
  F-OD01-01…08      → OD-01F-01…08
  F-OD01R-01…10     → OD-01F-11…20      ← **OD-01F-09 / OD-01F-10 为空号**
  F-OD01V3-01…10    → OD-01F-21…30      ← 该系列实为 **12** 项，-11/-12 未纳入
  F-OD01V4R-01…10   → OD-01F-34…43      ← 该系列实为 **14** 项，-11…-14 未纳入
  Proposal `:65`「历史编号保留于 Original 列；**不得重编号**。新问题自 OD-01F-44 起递增。」
```

**质询**：`OD-01F-40`（=F-OD01V4R-07 的 Fix）在 D1 `:447` 被判 `VERIFIED`，其 Required Action 写
「ID Mapping；一问一 Final ID；不重编历史」。但客观结果是：**14 项中 7 项（50%）未被正确登记**
（3 错配 + 4 缺失），另有 2 个 ID 空号与 2 项历史遗漏。这与我方上一轮 F-OD01V4R-07
（映射不完备且错配）是**同一缺陷在更大规模上的重演**，而本次被判 `VERIFIED`。

---

### F-OD01V4R-16（HIGH）— F-OD01V4R-09（Gap 两版并存）未修复，却被映射到无关 Fix 并标 VERIFIED

**证据（D1 与 Proposal/CR 仍互相矛盾）**

```text
D1 `:304`  OD-01R-01 Required Action：「…若无法合法登记 → **记 Governance Gap**，不得声称已为正式 L1」
D1 `:315`  ### OD-01R-01 — 正式 L1 落位判定（Owner 接受的 **Gap 路径**）
D1 `:334`  4. 既有目录模型内**没有**第二处正式 L1 registry。
D1 `:342`  CR-002 = L1 candidate / NOT RELEASED（对齐 67 先例）
D1 `:343`  REGISTRATION PATH = 有效未来路径；当前 Candidate only；intentionally deferred

Proposal v4R：`Governance Gap` = **0 命中**；`:481` 「Valid future registration path（非无落点）。」
CR-002   ：`Governance Gap` = **0 命中**；`:52` 同义句（`Valid future registration path.`）。

全四文件检索：
  `未归层` = **0 命中**   ← 90 `:47`「未归层 = 不得引用为权威」的后果**第三轮仍未登记**
  Self Review `:51` 仍保留旧结论「Q6 | Governance Gap 是否改为 deferred registration path？| **是**」
```

**影响**：同一事实在同一治理记录族内**两版并存**（D1 的 Gap 路径 vs Proposal/CR 的
「非无落点」）；且 `Docs/COORDINATION/**` 未归层的后果（`90:47`）对本轮全部交付物——
包括 D1 中自称 `BINDING FOR EXECUTION: YES` 的两节——依旧零登记。
本轮不仅未修，还**移除了反向文本**（Proposal/CR 不再出现 Gap 字样），使矛盾由「显式冲突」
变为「单向陈述」，更难被发现。

---

### F-OD01V4R-17（MED-HIGH）— `Purpose` 字段从 Proposal v4R 与 CR-002 头块中消失（较 v4 为回退）

**证据**

```text
91 `:170`  出生证明含 `Purpose: <一句话：本文档解决什么问题>`
91 `:182`  「存量文档不强制回填；**下次实质修订时补**」
91 `:195`  门槛 2：出生证明齐备——「`91 §5` 全部字段，**缺字段即不得创建**」

v4  Proposal `:11`  Purpose: 承载 OD-01 option provenance 的条款级 explicit diff 与语义边界…
v4  CR-002  `:10`  Purpose: OD-01 修改 L0 的 Change Record 候选；承载 CHANGE 分类、Gate、影响面与授权边界
v4R Proposal `:4-18` 无 `Purpose`
v4R CR-002   `:4-20` 无 `Purpose`
实测：四份交付物 `^Purpose:` = **0 命中**（含 Self Review）
```

**影响**：本轮自述「Proposal / CR-002 / Disposition **全量 Header**」与事实不符；
`91 §5` 的强制字段在**本轮实质修订后**反而不齐（v4 曾有）。同时 `Purpose` 缺失使
`91 §5.1` 门槛 1（说明与最近似现有文档的不可合并差异）失去落点。

---

### F-OD01V4R-18（MED-HIGH）— `Authority Level` 值域被自创，触碰「不得自创层级」

**证据**

```text
冻结枚举：
  90 `:375`  Authority Level: <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>
  91 `:167`  Authority Level: <L0 | L0-META | L1 | L2 | L2-proposed | L3 | L4 | L5>
禁止自创层级的强制门槛：
  91 `:196`  门槛 3：`Authority Level` ∈ `91 §1` / `90 §1` 已定义的层级；**不得自创层级**

本轮实际取值：
  Proposal `:8`   Authority Level: **Proposal — change proposal authority**
  CR-002   `:8`   Authority Level: **CR — registration / change tracking authority**
  D1 `:432`       Authority Level: **Owner Decision — decision authority**
  Proposal `:94-99` §2.1 另行给出四类「Authority Level」表（含 `registration / change tracking authority`）
```

**质询**：字段**名**已从 v4 的 `Authority:` 恢复为 `Authority Level` ✅（这是实质改进），
但**值域**被替换为一套自创的「权威种类」术语。`Proposal` / `CR` / `Owner Decision` 既非
`91:167` 中的层级，也不是层级的一种——其中 CR-002 本身就是变更记录，把「注册与变更跟踪」
称作一种 Authority Level 属范畴错误。上一轮 F-OD01V4R-06 的问题是「以移除字段规避矛盾」，
本轮是「恢复字段名但自造值域」，`91 §5.1:196` 仍未满足。

---

### F-OD01V4R-19（MED-HIGH）— 状态词「换词未归位」：允许集 5 词中 4 词非冻结值；OD-01-H 引错章节

**证据**

```text
91 `:109-122` §3.1 允许的状态值（10 值）=
  OPEN / PENDING / CONDITIONAL PASS / CLOSED / NOT STARTED / DEFERRED /
  SUPERSEDED / RETRACTED / ACTIVE / HISTORICAL
90 `:376` Status Header 枚举 = ACTIVE / SUPERSEDED / HISTORICAL / DRAFT / CLOSED / NOT RELEASED

v4R 自定允许集（Proposal `:114`）：
  APPROVED · PENDING · VERIFIED · NOT EFFECTIVE · NOT REGISTERED（+ DRAFT / NOT RELEASED）
  → PENDING / DRAFT / NOT RELEASED 合法；**APPROVED / VERIFIED / NOT EFFECTIVE / NOT REGISTERED 四项均不在上述任一冻结集合内**
Proposal `:115`「**不发明新状态词**」与 `:114` 的实际允许集自相矛盾
Proposal `:112`（§2.3 标题行）「仅用冻结体系已有词」← 实测不成立

D1 `:398` OD-01-H Required Action：
  「删除模糊完成类状态词（**91 §3.2**）；仅用 APPROVED / PENDING / VERIFIED / NOT EFFECTIVE / NOT REGISTERED」
  → 引用的是**禁用词表**（§3.2），而非**允许值表**（§3.1）；并把该指示写入 OWNER APPROVED RECORD
D1 `:431` 新附录 Status = **PENDING EFFECTIVE FREEZE**（亦非 90 `:376` 枚举值）

实测计数（大小写敏感）：VERIFIED = 21 / 1 / 32 / 3（Proposal / CR / D1 / Self Review）；
APPROVED = 2 / 1 / 36 / 0；NOT EFFECTIVE 与 NOT REGISTERED 均非枚举值
```

**公平记录**：自述的 **CLEAN 声明本身成立**——`DONE / COMPLETE / COMPLETED / NEXT /
FINISHED / ADDRESSED / resolution_status` 在四文件中确为 0 命中；D1 `:57` 的 `COMPLETE`
子串位于 L0 引语 `INCOMPLETE` 内，非状态词用法（见 P4）。问题不在「禁词是否清除」，
而在「替换目标是否仍是冻结词表内的词」。

---

### F-OD01V4R-20（MED-HIGH）— change set 要求 `table_id`，但 L0 无该实体且同一 change set 明令不授权创建

**证据**

```text
Proposal §5 `:159-171`
  table_cell identity = (source_version_id, table_id, row_index, col_index)
  table_id = 该 source_version 内 **sealed 表结构节点**的稳定标识
Proposal §3 `:130`      table_cell → **table identity 必需**
Proposal CI-4 `:291`    table_cell → table identity（table_id, row_index, col_index）必需
Proposal CI-2 `:230-234` Proposed Frozen Text：
  「M1 裁剪：document_source_tables / _cells / _fragments 不建完整文档级索引…option provenance 的
    table_cell 定位使用 table identity…**该允许不构成创建 document_source_tables / _cells /
    _fragments 或修改数据库 schema 的授权**。」
L0 现状：
  Docs/V3_SPEC/** 全树检索 `table_id` = **0 命中**
  `10_Data_Model.md:107`  「M1 裁剪：`document_source_tables / _cells / _fragments` **不建**」
  `10_Data_Model.md:729`  「M1 裁剪 table_cells/fragments」
冻结规则：
  90 `:420-430` §5 Rule 4 Ownership Matrix ——「**指不出唯一生产者的字段 = 治理缺口**，进台账」
```

**推演**：CI-2 与 CI-1/CI-4 的 Proposed 文本若按 CR `:66` 指定的权威文本逐条写入 L0，
结果是一组**无法满足**的规范：`table_cell` provenance 被要求携带 `table_id`，
而 L0 中不存在产生 `table_id` 的表结构（`document_source_tables` 被明确「不建」），
且同一 change set 明文声明「不构成创建 … 的授权」。
同时 `table_id` 无唯一生产者 → 按 `90 §5 Rule 4` 应进治理台账（`84_CONFLICT_LEDGER`）而本轮未登记。

**这是本轮最实质的设计缺陷**：上一轮的 CI-4「line_ref 矛盾」被消除后，同类矛盾
以 `table_id` 的形式重新出现在同一 change set 内。

---

### F-OD01V4R-21（MED）— 5 个 CI 条目丢失 `Current Rule`（v4 13 处 → v4R 8 处）：primary artifact 回退

**证据（实测计数）**

```text
'Current Rule' 出现次数：v4 = 13  →  v4R = 8
v4R 的 8 处：`:190`（§7 结构说明）、CI-1 `:195`、CI-2 `:218`、CI-3 `:244`、CI-4 `:271`、
             CI-5 `:306`、CI-6 `:325`、CI-7 `:346`
→ **CI-8 / CI-9 / CI-10 / CI-11 / CI-12 无 Current Rule**（v4 中这 5 项均有）

自相矛盾：
  Proposal §7 `:190` 自述结构 =「Current Rule → Problem/Limitation → Proposed Rule →
    Reason → Impact → Affected Frozen Sections」
  D1 `:391` OD-01-A Required Action =「恢复逐条 Frozen Text 级 **Current → Proposed** diff」（判 VERIFIED）
  v4R CI-11 `:406-414` / CI-12 `:418-430` 亦**无 Problem / Reason**（仅 Proposed + Impact + Affected）
```

**影响**：`90 §11` 的 Change Audit 以「Current → Proposed」为审计对；缺 Current 的 5 项
无法核验「改了什么」。这与上一轮 F-OD01V3-01（拟议文本缺失）属同类，方向相反但机制相同：
**以精简代替补全**（本轮 615 行删除 vs 444 行新增）。

---

### F-OD01V4R-22（MED）— CI-4 的「逐字」Current Rule 并**非逐字**；L0 字段名证据被移出块外

**证据**

```text
v4R CI-4 `:271-276`
  **Current Rule**（逐字，含历史字段名，仅对照）
  ```text
  - `granularity` ∈ {line, line_character}（M1；table_cell/fragment 延后，见 00 §5）。
    （示例 JSON 历史解析字段名见 L0 本节原文；Change Set 统一为 span_resolution）   ← **非 L0 文本**
  ```
L0 原文 `20_Document_Pipeline.md:322-324`（两 bullet）：
  - `granularity` ∈ {line, line_character}（M1；table_cell/fragment 延后，见 00 §5）。
  - line_ref 必须存在于该 source_version；line_character 的 start/end_offset 必须能唯
    一定位"同行多题答案/单行多选项"场景。
L0 实际的字段名出现处 `20:317`：  "text_hash": "<sha256>", "resolution_status": "exact",
```

**两点问题**：(a) 标注「逐字」的块内**含自加行**，且删去了 L0 第二个 bullet；
(b) L0 中字段名 `resolution_status` 的**唯一出现处**（`20:317` 的 JSON 示例）被改为
「见 L0 本节原文」的指示语——即把「Current 是什么」的证据移出 diff。
CI-4 的 Proposed 亦未重写该 JSON 示例（仅新增一句「解析字段唯一命名为 span_resolution」）。
→ 上一轮 F-OD01V4R-12（引文保真）**未修复**，且本轮新增一处自加文本。

---

### F-OD01V4R-23（MED）— form 用语与 OD-01 绑定用语脱钩且无对照表

**证据**

```text
D1 `:38-48`（OD-01 Owner Decision，本轮未改）
  「必须支持至少：line_range / char_span_in_line / table_cell / multiple_source_spans /
    other verifiable source provenance」
  「字段命名可提出实现建议，**不得改变上述语义**。」
v4R Proposal §1 `:73-74`：`granularity: line` → 「吸收为 **line** form」；
                          `line_character` + offsets → 「正式化为 **line_character** form」
v4R Proposal §3 `:128-129`：`line`（= line_range）/ `line_character`
实测：Proposal v4R 中 `char_span_in_line` = **0 命中**；`line_range` = **1 命中**（仅作 `line` 的括号注释）
```

**影响**：change set 采用的 form 名（`line` / `line_character`）与 OD-01 绑定用语
（`line_range` / `char_span_in_line`）不一致，且**无 OD-01 form ↔ v4R form 对照表**。
`D1 :48` 只授权「字段命名建议」，未授权更换用语体系；P04 的术语 `char_span_in_line`
在采纳后的 L0 中将不复存在。→ 追溯断点：从任何引用 `char_span_in_line` 的上游文档
（含 P04 / 既有 DSH 报告）无法机械定位到对应条款。

---

### F-OD01V4R-24（MED）— Self Review 头块围栏损坏且缺 5 个强制字段

**证据（`Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md`）**

```text
`:3`  实际内容 = 反引号 + **TAB** + `ext`        ← 应为 ```text
`:4-11` Document Type / Status / Authority Level / Derived From / May Change /
        Must Not Change / Related Records / Gate State Authority
`:12`  单个反引号                                  ← 围栏未闭合
→ 头块**未构成代码围栏**，渲染为正文段落，机器不可解析

缺失的 91 §5 强制字段：Document ID · Purpose · Normative · Supersedes · Superseded By（5 项）
`Derived From: Proposal v4 自查` —— 是描述，不是「本档结论向上闭包到哪些 L0/L1/L2 条目」（91 `:171`）
`Authority Level: L3 — evidence only` —— L3 后附加非枚举描述（与前两处同类模式）
```

**影响**：本轮该文件属**实质修订**（+33 行）→ `91:182` 要求补全出生证明；`90 §4:368-370`
「每份新文档必须以如下块开头」为强制。F-OD01V4R-02 的修复未覆盖该文件。

---

### F-OD01V4R-25（LOW-MED）— 破引用与跨仓路径残留：F-OD01V4R-11 未修复且未映射

**证据**

```text
Proposal v4R `:14` Related Records：
  「… · **OD-01-PROPOSAL-V4-SELF-REVIEW.md**（Self Review only）」
实测 Docs/REPORTS/ 下 OD-01* 仅 1 个文件：
  OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md  →  **SELF-REVIEW.md 不存在**（破引用）

Self Review `:105` Document control：| Path | `Docs/60_REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md` |
  实际落点 = AITutors-v3 `Docs/REPORTS/…`；`Docs/60_REPORTS/` 是 **AITutor-X** 的目录约定
  → 上一轮 F-OD01V4R-11 的具体缺陷**原样保留**，且未出现在任何映射表
```

---

### F-OD01V4R-26（LOW-MED）— 机械替换痕迹：`PENDING = Owner Review`

**证据**

```text
Self Review `:96`（历史正文内）：  PENDING                  = Owner Review（OD-01-J：DSH 复核若 Owner 另令则先 DSH）
v4 对应行（上一版本）：            Next                  = Owner Review（…）
```

**影响**：为清除 `91 §3.2` 禁用词 `NEXT`，把「顺序」位置直接替换为状态词 `PENDING`，
产生语义不成立的 `PENDING = Owner Review`（`PENDING` 是状态，`Owner Review` 是动作）。
这是「禁词 CLEAN」以 find/replace 达成而非语义修正的直接证据；
`91 §3.2:131` 的原意是「用 `Step n` 表达顺序」，本轮未采用该建议。

---

### F-OD01V4R-27（LOW）— 头块字段名仍不规范；新增多个非规范字段

**证据**

```text
91 `:171`  规范字段名 = **`Derives From`**（91 `:179`：该字段是 R7 引用闭包的**可机检落点**）
本轮实际：
  Proposal `:11` / CR `:11` / D1 `:433` / Self Review `:7` 均写 **`Derived From`**（缺 s）
新增非规范字段：`Related Records`（4 文件）· `Registration Level`（Proposal/CR）·
                `Effective`（Proposal/CR）· `Change Record ID` / `Audit ID (planned)`（CR）·
                `Record-TYPE` / `Authority` / `Binding for Execution`（D1）
```

**影响**：低——但 `Derives From` 是设计上供扫描器校验引用闭包的字段，
本轮四份文件同时写错，将使该机检落点失效。

---

### F-OD01V4R-28（LOW）— OWNER APPROVED RECORD 内的拼写错误与同文件流程不一致

**证据**

```text
D1 `:445`  | F-OD01V4R-05 | OD-01F-38 | **APPROED** | 解析字段唯一 = span_resolution | VERIFIED |
                                  ↑ 应为 APPROVED
D1 `:400`  OD-01-J Required Action：「…v4R → DSH 外部验证 → Owner 批准 → re-freeze」  ✓
D1 `:405-409` OD-01-J 流程块：「Proposal **v4** → DSH **复核** → Owner 批准 → 正式 re-freeze」 ✗ 旧版
D1 `:452`  修订块：「Proposal **v4R** → **DSH 外部验证** → Owner 批准 → re-freeze」 ✓
D1 `:386`  「指导 Proposal **v4** / CR-002」← 旧版本号
D1 `:355`  「见 Proposal **v3** diff」← 更早版本号（存量）
```

**影响**：低——但同一份 `BINDING FOR EXECUTION: YES` 记录内并存两版流程与三个版本号，
且附录表出现拼写错误。

---

### F-OD01V4R-29（LOW）— 新引入非冻结分类词 `Future Required Change` / `Future Consideration`

**证据**

```text
Proposal `:85` / `:117-120`（§2.4）/ `:427` / `:485-491`（§11）
CR-002 `:147`
D1 `:448`
出现的分类词：`Future Required Change` · `Future Consideration`
冻结约束：
  91 `:109-122` §3.1 未含这两个词；`90 §3` CHANGE-0…5 未含
  91 `:131` §3.2 以 `NEXT` 为例：「**不是状态，是顺序**。用 `Step n` 表达」
```

**影响**：低——两者实际承担的是「未做/待做的顺序」语义，与 `91 §3.2:131` 禁止的
「用顺序代替状态」同类；若确需分类，宜用冻结的 `DEFERRED` / `PENDING` + `Step n` 表达。

---

## 5. OD-01F-34…43 处置再审计

| Fix ID | 对应上一轮发现 | 自述 | 本轮实际 | 复核判定 |
|--------|----------------|------|----------|----------|
| OD-01F-34 | F-OD01V4R-01 自审冒充独立审查 | VERIFIED | Self Review 降 HISTORICAL + 显式非 DSH + OD-01-J 只收 DSH 外部验证（三处同向） | **已处置** |
| OD-01F-35 | F-OD01V4R-02 缺 `90 §4` 头块 | VERIFIED | 覆盖 Proposal/CR；但 `Purpose` 缺失、Self Review 头块损坏且缺 5 字段 | **PARTIALLY** |
| OD-01F-36 | F-OD01V4R-03 禁用状态词 | VERIFIED | 禁词 CLEAN ✅；允许集 4/5 非冻结值；OD-01-H 引 §3.2 而非 §3.1 | **PARTIALLY** |
| OD-01F-37 | F-OD01V4R-04 CI-4 line_ref 矛盾 | VERIFIED | §3 分型 + CI-4 明文禁止一刀切；矛盾消除 | **已处置** |
| OD-01F-38 | F-OD01V4R-05 字段重命名未入 change set | VERIFIED | `span_resolution` 四处一致；`resolution_status` 0 命中；`20 §5.5` 入 Affected | **已处置** |
| OD-01F-39 | F-OD01V4R-06 规范字段被删 | VERIFIED | 字段名恢复 ✅；值域自创；`Registration Level` 仍非规范 | **PARTIALLY** |
| OD-01F-40 | F-OD01V4R-07 ID Mapping | VERIFIED | 3 错配 + 4 缺失 + 2 空号 + 2 历史遗漏 | **未达标** |
| OD-01F-41 | F-OD01V4R-08 命名空间增殖 | VERIFIED | 错配（Fix 主题为降级态）；命名空间实增至第 8 套 | **未达标（错配）** |
| OD-01F-42 | F-OD01V4R-09 Gap 两版并存 | VERIFIED | 错配（Fix 主题为 table_cell identity）；**原问题未修**且新引入 `table_id` 不可满足 | **未达标（错配）** |
| OD-01F-43 | F-OD01V4R-10 `90 §5 Rule 2` | VERIFIED | 错配（Fix 主题为字符偏移单位）；Self Review `:67` 仍含 `不得` 且无 L0/L1 引用 | **未达标（错配）** |
| — | F-OD01V4R-11 / -12 / -13 / -14 | 未映射 | -11 未修；-12 未修且新增一处；-13 已静默修复；-14 **已实质修复** | **未登记** |

```text
OD-01F-34…43 复核汇总：已处置 3 / 部分已处置 3 / 未达标 4（自述 VERIFIED 10/10 不成立）
映射覆盖：上一轮 14 项 → 正确登记 7 / 错配 3 / 缺失 4
```

---

## 6. change set 可满足性推演（若按 CR `:66` 指定的权威文本逐条写入 L0）

| 推演项 | 结果 |
|--------|------|
| `table_cell` 定位 | **不可满足**：要求 `table_id`，而 L0 无表结构实体、且同 change set 明文不授权创建（F-OD01V4R-20） |
| `line` / `line_character` vs OD-01 用语 | **术语断链**：OD-01 绑定 `line_range` / `char_span_in_line`，v4R 使用 `line` / `line_character`，无对照（F-OD01V4R-23） |
| `span_resolution` | **自洽** ✅：`20 §5.5` 已入 Affected，`20 §6.2` 新文本一致，`10 §6.3` CI-9 同步列出 |
| 字符偏移单位 | **自洽** ✅：§6 定义与 CI-4 `:283-285` 文本一致；与 `20:515` `text.encode("utf-8")`、`20:532` UTF-8 字节序不冲突（不同轴向） |
| `10 §8` 2b/2c vs `20 §5.5` form 规则 | **双处规定**：CI-4 form 表与 CI-10 `2b` 各自复述分型规则，未声明单一权威处（较 v4 未改善，属 LOW） |
| `50` bbox 行 | 自洽 ✅（CI-11 与 CI-4/CI-12 的 table identity / image_region 表述一致） |
| 5 个缺 Current 的 CI | **无法审计**：CI-8…CI-12 无「Current」对照物（F-OD01V4R-21） |

---

## 7. 载体合规性矩阵（90 / 91）

| 规则 | 要求 | Proposal v4R | CR-002 | D1（含新附录） | Self Review |
|------|------|--------------|--------|----------------|-------------|
| `90 §4:373-380` 强制头块字段 | 7 字段 | ⚠️ 齐备但 `Derived From` 拼写错 | ⚠️ 同左 | ⚠️ 新附录用自有字段集 | ❌ 围栏损坏；缺 5 字段 |
| `91 §5:170-173` 出生证明扩展 | +4 字段 | ❌ 缺 `Purpose` | ❌ 缺 `Purpose` | ⚠️ 缺 `Purpose` | ❌ 缺 `Purpose` 等 |
| `91 §5.1:195` 门槛 2 缺字段即不得创建 | — | ❌ | ❌ | ❌ | ❌ |
| `90 §4:375` / `91 §5:167` Authority Level 枚举 | 8 值 | ❌ 自创值域 | ❌ 自创值域 | ❌ 自创值域 | ⚠️ `L3 — evidence only` |
| `91 §5.1:196` 不得自创层级 | — | ❌ | ❌ | ❌ | — |
| `90 §4:376` / `91 §5:168` Status 枚举 | 6 值 | ⚠️ `DRAFT` ✅；§2.3 允许 4 个非枚举值 | ⚠️ `NOT RELEASED` ✅；`NOT EFFECTIVE`/`NOT REGISTERED` 非枚举 | ❌ `PENDING EFFECTIVE FREEZE` / `RECORDED` | ✅ `HISTORICAL` |
| `91 §3.1:109-122` 允许状态值 | 10 值 | ❌ `APPROVED`/`VERIFIED` 等 | ❌ | ❌ | ⚠️ |
| `91 §3.2:124-132` 禁用状态词 | — | ✅ CLEAN | ✅ CLEAN | ✅ CLEAN（`INCOMPLETE` 子串除外） | ✅ CLEAN |
| `90 §5 Rule 2:397-404` L3/L4 禁用词须引 L0/L1 | — | n/a（未归层） | n/a | n/a | ❌ `:67` `不得` 无 L0/L1 引用（且未引 `82 §3`） |
| `90 §5 Rule 4:420-430` 唯一生产者 | 指不出即缺口进台账 | ❌ `table_id` 无生产者，未进台账 | ❌ | — | — |
| `90 §1.2:79-81` 目录落位 | V3_SPEC=新增 L1；REPORTS=证据 | ❌ 未归层 | ❌ 未归层 | ❌ 未归层 | ⚠️ 位于 REPORTS 但自称他仓路径 |
| `90:47` 未归层 = 不得引用为权威 | — | ❌ 未登记 | ❌ 未登记 | ❌ 未登记 | n/a |
| `90 §11:328-329` 登记义务 | L0 修改后强制 | 未触发 ✅ | CR `:19` 绑定未来 commit ✅ | — | — |

---

## 8. 本轮是否构成违规

**判定：仍构成对 L0-META 格式/词汇规则的违规（程序性），未构成对 Frozen Spec 内容的修改。**

| # | 违规 | 依据 | 涉及文件 |
|---|------|------|----------|
| V1 | 实质修订后出生证明仍缺 `Purpose`（且较 v4 为**回退**） | `91:170`、`91:182`、`91:195` | Proposal `:4-18`、CR `:4-20`、Self Review |
| V2 | `Authority Level` 值域自创（层级之外的「权威种类」） | `90:375`、`91:167`、`91:196` | Proposal `:8`、CR `:8`、D1 `:432` |
| V3 | 作为状态值使用非冻结词（`APPROVED`/`VERIFIED`/`NOT EFFECTIVE`/`NOT REGISTERED`/`PENDING EFFECTIVE FREEZE`） | `91:109-122` §3.1、`90:376` | 四文件（计数见 F-OD01V4R-19） |
| V4 | OWNER APPROVED RECORD 指示状态词时引用禁用表（§3.2）而非允许表（§3.1） | `91:107-122` | D1 `:398` |
| V5 | L3/L4 文档使用 `不得` 而未引用 L0/L1（亦未引 `82 §3`）——**上一轮 V4 未修复** | `90:397-404` Rule 2 | Self Review `:67` |
| V6 | change set 引入无唯一生产者的字段 `table_id`，未进治理台账 | `90:420-430` Rule 4 | Proposal §5 / CI-2 / CI-4 |

**已消除（上一轮违规）**：跨仓逐字节复制（V5 of 上一轮）✅ 已清除；
新文档无强制头块（V1 of 上一轮）⚑ 部分消除（Proposal/CR 补齐，Self Review 仍不完整）；
`COMPLETE`/`NEXT` 状态词（V2 of 上一轮）✅ 已清除；
L2 指示扩充状态词表（V3 of 上一轮）⚑ 部分消除（不再用 `ADDRESSED`/`COMPLETED`，但仍指示 4 个非冻结词）。

**未构成**：Frozen Spec 未被修改（`b3eeb3e9…` 一致）；未 re-freeze；未声称 Gate PASS；
未声称 CR-002 已注册或生效；未修改 `90`/`91`/`82`/`84`；未新建治理文档；未删除历史正文
（Self Review 原文与 D1 OD-01R 原节保留）；未 Migration / Phase 1 / X3 / push。

---

## 9. 正面证实（P1–P14）

| # | 正面事实 |
|---|----------|
| P1 | **Frozen Spec 未变**：`b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` 未变；delta 仅 4 篇文档；无 backend/schema/corpus/migration 变更 |
| P2 | **跨仓副本已彻底清除（上一轮 HIGH 已实质修复）**：AITutor-X `Docs/COORDINATION/` 目录不存在；`Docs/60_REPORTS/OD-01-PROPOSAL-V4-…md` 不存在；untracked 20→18；被删除的 `OD-01-A-J-OWNER-DECISION-APPENDIX.md` 内容在 v3 D1 `:374-455` 完整保留 → **无记录丢失** |
| P3 | **Self Review 已正确降级**：`Status: HISTORICAL`（`91 §3.1:122` 合法值）+ `:14-16` 显式「本文件不是 DSH Review；OD-01-J 不得引用本文件作为 DSH 证据」；Proposal `:29-35`、CR `:124-128`、D1 `:452-453` 三处同向；历史正文保留未删（符合「不删除旧文档」） |
| P4 | **禁用词 CLEAN 声明成立**：大小写敏感实测 `DONE` / `COMPLETE` / `COMPLETED` / `NEXT` / `FINISHED` / `ADDRESSED` / `resolution_status` 在四文件中 **0 命中**；D1 唯一 `COMPLETE` 命中位于 L0 引语 `INCOMPLETE`（`:57`）内，非状态词用法 |
| P5 | **`span_resolution` 唯一命名已落到文本**：§2.2 `:101-110` + CI-4 `:295` + CI-6 `:331` + CI-9 `:381`；`resolution_status` 0 命中；四层命名（`span_resolution` / `option_evidence_status` / `answer_status` / `semantic_status`）与 L0 既有词汇一致（`answer_status` 三字段见 `10:463`、`20:370`） |
| P6 | **CI-4 的 line_ref 对立已实质消除**：§3 `:126-136` 五类分型 + CI-4 `:288-296` 明文「line → line_ref 必需；line_character → line_ref + offset；table_cell → table identity，line_ref 可选…禁止要求一切 form 具备 line_ref；禁止 table_cell 无任何定位」 |
| P7 | **字符偏移单位已钉死并写入 Proposed 文本**：Unicode code point / 0-based / start inclusive / end exclusive（§6 + CI-4 `:283-285`），并声明「不留待决」「不得改用 code unit 而不另行走 Change」——自审 F-OD01V4-01 的未决项已闭合 |
| P8 | **`table_cell` identity 已给出唯一方案**（`(source_version_id, table_id, row_index, col_index)`，1-based）并明确「不涉及代码实现或 Schema DDL」——不再留候选列表（矛盾另见 F-OD01V4R-20） |
| P9 | **ID 体系建立了历史号保留 + 单一前进 ID 的结构**：`OD-01F-xx`，并规定「新问题自 OD-01F-44 起递增」；`F-OD01V4-01…03`（自审发现）诚实标 `PENDING` 而非 VERIFIED |
| P10 | **CHANGE-4/5 保留四道门**：Proposal `:452-465`、CR `:88-100`；Gate A–D 全 `PENDING`；未以「Proposal 完成 / Owner 同意 / 设计合理」替代 PASS |
| P11 | **边界守持且与 git 事实一致**：Frozen Spec / Contract / Production / Preprocessing / Schema / Corpus / Migration / Phase 1 / Re-freeze 全部 UNCHANGED 或 NOT EXECUTED；`ahead 9` 未推送 |
| P12 | **历史正文未被删除**：Self Review 原文完整保留于 `:20-108`；D1 保留 OD-01R 原节（`:288-367`）并**追加**新附录（`:427-455`），未重编号历史 Decision |
| P13 | **CR-002 定位表述保持正确**：`NOT EFFECTIVE` / `NOT REGISTERED` / 四条正式注册条件 / 「Valid future registration path（非无落点）」（`:48-53`、`:479-481`） |
| P14 | **`Authority Level` 字段名已恢复**（v4 曾以非规范字段 `Authority:` 取代），`Proposal` / `CR` / `D1 附录` 三处字段名一致（值域问题另计，见 F-OD01V4R-18） |

---

## 10. 局限（L-1 … L-7）

- **L-1** 未重跑任何测试基线、未执行四道门、未做 corpus 对比；本报告不对 Gate A–D 的最终结论
  作预判，仅确认其「PENDING + 未冒充 PASS」这一状态陈述为真。
- **L-2** 审查范围限于 OD-01 v4R / CR-002 / D1（含新附录）/ Self Review；对其他 OD-02…G-02
  只做「是否被改动」的一致性核对，不构成背书。
- **L-3** `git fetch` 在本环境不可用，`origin/main` 比较基于本地引用；AITutors-v3 依指令未推送，
  其远端状态未核验（本地 `ahead 9`）。
- **L-4** 本会话 `pwsh` 沙箱无法初始化（`SetNamedSecurityInfoW failed (Win32 5)`），所有命令在
  `danger-full-access` 下执行且**全部为只读命令**；未对 AITutors-v3 写入任何字节。
- **L-5** F-OD01V4R-15 的「错配」判定基于**任务书文本中的 R/Fix 描述**与 finding 主题的对照；
  若被审方内部另有 R-xx 与「降级态/table_cell identity/字符偏移」的对应定义而未随本轮提交，
  该项严重度可下调——但**提交在案的映射表本身**仍缺 4 项且含 2 个空号，这一事实独立成立。
- **L-6** F-OD01V4R-20 的「`table_id` 不可满足」结论基于 `Docs/V3_SPEC/**` 全树检索
  （`table_id` 0 命中）与 `10:107`/`10:729` 的裁剪表述；未核验 `backend/Docs/V3_SPEC/` 下的
  JSON 测试语料与 `docs_audit/authority_matrix.yaml`，如其中已定义表结构实体可影响该判定。
- **L-7** 跨仓副本的**删除**无法由 git 证实（这些文件从未被跟踪）；本报告依据「路径不存在 +
  untracked 计数 20→18 + 删除前已确认该目录仅含 3 个文件」推断其被清除且无附带损失。

---

## 11. 最终判定

```text
OD-01 Proposal v4R + CR-002 + D1（含 OD-01V4R 附录）+ Self Review（HISTORICAL）
  = VERIFIED WITH FINDINGS

Closure Blocking = YES
  理由：
   (1) 存在被误关闭的发现：10 项自述 VERIFIED 中，OD-01F-40（ID Mapping）、
       OD-01F-41/-42/-43（映射错配）经核验未达标，其中 OD-01F-42 对应的原问题
       （Gap 记录两版并存 / 90:47 未归层）**第三轮仍未修复**；
   (2) change set 存在**不可满足**项：table_cell 要求 `table_id`，而 L0 无该实体、
       同一 change set 又明文不授权创建（90 §5 Rule 4 应入台账而未入）；
   (3) 对 L0-META 的现行违规仍在：`Purpose` 缺失（91 §5.1 门槛 2）、
       Authority Level 值域自创（91 §5.1 门槛 3）、状态值非冻结词、
       Self Review 违反 90 §5 Rule 2；
   (4) 自审冒充独立审查的问题**已正确修复**（P3）——本轮 YES 的理由与前一轮不同，
       但结论一致：**尚不具备进入 Owner 批准/闭环的条件**。

Recommendation = OWNER ACTION REQUIRED BEFORE CLOSURE

Findings = F-OD01V4R-15 … F-OD01V4R-29（15 项；已登记，未修复）
  HIGH      : F-OD01V4R-15, F-OD01V4R-16
  MED-HIGH  : F-OD01V4R-17, F-OD01V4R-18, F-OD01V4R-19, F-OD01V4R-20
  MED       : F-OD01V4R-21, F-OD01V4R-22, F-OD01V4R-23, F-OD01V4R-24
  LOW-MED   : F-OD01V4R-25, F-OD01V4R-26
  LOW       : F-OD01V4R-27, F-OD01V4R-28, F-OD01V4R-29
  （按被审方 §0 `:65` 规则 ⇔ OD-01F-44 … OD-01F-58）

OD-01F-34…43 复核 = 已处置 3 / 部分已处置 3 / 未达标 4（自述 10/10 VERIFIED 不成立）
上一轮 14 项映射覆盖 = 正确登记 7 / 错配 3 / 完全缺失 4

Frozen Spec  = UNCHANGED（确认，tree b3eeb3e9…）
CR-002       = Change Proposal Record / NOT EFFECTIVE / NOT REGISTERED（确认）
Gate A/B/C/D = PENDING（确认）
Re-freeze / Phase 1 / Migration / Push(v3) = NOT EXECUTED / NOT ENTERED / NOT AUTHORIZED / 未推送（确认）
AITutorX 跨仓副本 = 已清除（确认；上一轮 HIGH 已实质修复）
Self Review  = HISTORICAL / 非 DSH（确认；不得作为 OD-01-J 证据）
```

### Re-freeze 前置条件（6 项，缺一不可）

1. **修复映射并在仓库内定义前进 ID**：补齐 F-OD01V4R-11…14 的登记；纠正 -08/-09/-10 三行错配；
   填补 OD-01F-09/10 空号；把 F-OD01V3-11/12 纳入。映射表须与 finding 主题一一对应，否则
   `VERIFIED` 不可采信。（F-OD01V4R-15）
2. **修复 Gap 记录的单向化**：D1 `:304`/`:315`/`:334` 与 Proposal/CR 的「非无落点」结论二选一；
   并登记 `90:47`（未归层 = 不得引用为权威）对 `Docs/COORDINATION/**` 全部交付物的后果。
   （F-OD01V4R-16）
3. **补齐出生证明并归位字段**：Proposal / CR-002 / Self Review 补 `Purpose`（并修复 Self Review
   头块围栏与缺失字段）；`Derived From` → `Derives From`；`Authority Level` 取值回到
   `91:167` 枚举（如需表达「提案态」用 `L2-proposed` 等既有值）。（F-OD01V4R-17/18/24/27）
4. **状态词归位**：把 `APPROVED`/`VERIFIED`/`NOT EFFECTIVE`/`NOT REGISTERED`/
   `PENDING EFFECTIVE FREEZE` 映射到 `91 §3.1` / `90 §4:376` 的冻结值（例如
   `NOT REGISTERED` → `NOT RELEASED`、`VERIFIED` → `CLOSED — <范围>` 或 `ACTIVE`+引用证据）；
   修正 D1 `:398` 的章节引用（§3.2 → §3.1）。（F-OD01V4R-19）
5. **解决 `table_id` 的可满足性**：或定义其唯一生产者与 L0 载体（并同步 `10 §4`/`10 §8`），
   或把 `table_cell` 的 identity 改为可由既有 L0 实体表达的形式；任一选择都须进
   `90 §5 Rule 4` 的 Ownership Matrix（否则进 `84` 台账）。（F-OD01V4R-20）
6. **恢复 change set 的审计性**：CI-8…CI-12 补回 `Current Rule`（并补 CI-11/CI-12 的
   Problem/Reason）；CI-4 的 Current 块去除自加行、恢复 L0 第二 bullet 与字段名原文；
   建立 OD-01 form ↔ v4R form 对照表。（F-OD01V4R-21/22/23）

**非阻断跟进**：F-OD01V4R-25（破引用 + Self Review Path 更正）、F-OD01V4R-26
（`PENDING = Owner Review` 改为 `Step n`）、F-OD01V4R-28（`APPROED` 拼写与版本号统一）、
F-OD01V4R-29（`Future *` 分类词改用 `DEFERRED`/`PENDING` + `Step n`）。

---

## 附录 A — 逐字引用核对表

| 被审引文位置 | 引用 L0 坐标 | 核对结果 |
|--------------|--------------|----------|
| CI-1 `:198-199` | `00_Master_Spec.md:274-275` | ✅ 逐字一致 |
| CI-2 `:221-223` | `10_Data_Model.md:107-109` | ⚠️ 仍省略「依据 01 v0.3 收敛。」（延续上一轮 F-OD01V4R-12） |
| CI-3 `:247-248` | `20_Document_Pipeline.md:280-281` | ✅ 逐字一致 |
| CI-4 `:274-275` | `20_Document_Pipeline.md:322-324` | ❌ 标注「逐字」但含自加行、且删去第 2 bullet（F-OD01V4R-22） |
| CI-5 `:306` | `20_Document_Pipeline.md:368` | ✅ 逐字一致 |
| CI-6 `:325` | `20_Document_Pipeline.md:394-398` | ⚠️ 摘要式（丢 E 层 7 值枚举） |
| CI-7 `:346` | `20_Document_Pipeline.md:454` | ✅ 一致 |
| CI-8 / CI-9 / CI-10 / CI-11 / CI-12 | 各自 L0 坐标 | ❌ **无 Current Rule 可核**（F-OD01V4R-21） |
| §1 `:73-86` 缺口基线 | `20 §5.5` / `10 §6.3` / `00 §5` / `10 §4` | ✅ 与 L0 状态相符 |
| §2.2 `:107` `answer_status` 三字段「既有」 | `10:463` / `20:370` / `20 §8.3` | ✅ 主张为真 |
| §5 `:163-165` `table_id` 定义 | `Docs/V3_SPEC/**` 全树 | ❌ 无对应实体（F-OD01V4R-20） |
| §6 `:178-181` 字符偏移单位 | `20:515` / `20:532`（UTF-8 轴向） | ✅ 不冲突（不同轴向） |
| §10 `:479` 四条注册条件 | `90:79`（V3_SPEC 允许「新增 L1」） | ✅ 一致 |

## 附录 B — 文件 / 坐标索引

```text
被审对象（AITutors-v3 @ b6cb762，只读）
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md   511 行（v4R）
  Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md                   160 行
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md                  467 行（含 OD-01V4R 附录 `:427-455`）
  Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md               108 行（Self Review / HISTORICAL）

被引用冻结原文（AITutors-v3，只读）
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md  548 行  （§1 :36-47；§1.2 :60-90；R1/R2 :107-115；
                                                    §3 :342-364；§4 :368-383；§5 Rule 1-4 :387-430；
                                                    §11 :271-329）
  Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md  276 行  （§3.1 :109-122；§3.2 :124-132；§5 :157-177 含
                                                    Purpose :170 / Derives From :171 / Authority Level :167；
                                                    §5.1 :184-203 含门槛 2 :195 / 门槛 3 :196）
  Docs/V3_SPEC/00_Master_Spec.md          406 行  （§5 非目标 :264-278）
  Docs/V3_SPEC/10_Data_Model.md           793 行  （§4 M1 裁剪 :105-109；§6.3 :451-471 / answer_status :463；
                                                    §8 :625-649；table_cells 裁剪 :729）
  Docs/V3_SPEC/20_Document_Pipeline.md    794 行  （§5.3 :275-294；§5.5 :308-341，resolution_status :317；
                                                    §6.1 :355-375；§6.2 :383-399；§7.2 :452-455；
                                                    §7.3 :519-536；§8.3 :642-655）
  Docs/V3_SPEC/50_Migration_Assets.md             （:51 表格定位行）
  Docs/DECISIONS/69_ARCHITECTURE_REVIEW_ADJUDICATION.md  （§5 四道门 :399-431）
  Docs/DECISIONS/82_CONTRACT_AUTHORITY_RECONCILIATION.md （:3 / :153 Gate State Authority）

在先 DSH 独立审查（AITutorX，只读）
  Docs/60_REPORTS/OD-01-FROZEN-SPEC-PROPOSAL-DSH-ADVERSARIAL-REVIEW.md   （4b419bf；F-OD01-01…08）
  Docs/60_REPORTS/OD-01-V2-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md           （8c2dca3；F-OD01R-01…10）
  Docs/60_REPORTS/OD-01-V3-L1-CR-002-CANDIDATE-DSH-ADVERSARIAL-REVIEW.md （1e44017；F-OD01V3-01…12）
  Docs/60_REPORTS/OD-01-V4-L1-CR-002-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md（d13e70d+d9173ab；F-OD01V4R-01…14）

本报告
  Docs/60_REPORTS/OD-01-V4R-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md
```

```text
— END OF REPORT —
审查者：DSH（独立外部验证；未参与 OD-01 v4/v4R 任何产出）
本报告即 OD-01-J 所述「DSH 外部验证」；被审方的 Self Review 不得替代或代表本报告。
```
