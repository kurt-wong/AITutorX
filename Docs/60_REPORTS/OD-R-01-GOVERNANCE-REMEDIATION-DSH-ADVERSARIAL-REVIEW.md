# OD-R-01 Governance Remediation — DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Governance Remediation — 完成报告」 |
| 仓库 | `D:\Project\AITutors-v3` |
| 分支 | `od01-r3-convergence` |
| 被审 commit | `60fa9ff30f70037e1990db7dd5bc255310073432`（parent `71f51f9`） |
| 审查基线 | HEAD = `60fa9ff`（工作区干净、无 tracked 改动） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间**未修改任何文件、未 push** |
| 证据等级 | DIRECTLY VERIFIED · VERIFIED BY INSPECTION · DOCUMENT CLAIM · UNKNOWN |
| 关联 | 上一轮 DSH 审查：`AITutor-X/Docs/60_REPORTS/OD-R-01-FROZEN-SPEC-CLOSURE-DSH-ADVERSARIAL-REVIEW.md`（commit `f22af28`） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（授权链与审计链已实质闭合；1 项 HIGH 完整性断言需修正，另有 1 项既存未登记 L0 修改待 Owner 处置）
```

**一句话结论**：本轮是**高质量补救**——L1 / CA / §12 / re-freeze 四件套齐备且互相锚定，分类判定与 `90 §3` 逐字吻合，历史 hash **未做机械替换**（只加注），我上一轮的 F-01～F-08 **全部被正确处置**，且无任何 code / schema / DDL / migration 改动。

但审查发现一件**必须修正的事实性断言**：本 commit 在 `84_CONFLICT_LEDGER` 新写「`0dd954d` 之后触及 L0 的提交**共两处，均已登记**」，而机械检验显示存在**第三个**触及业务 L0 的提交 `f708370`（2026-09-21，`20_Document_Pipeline.md` 9+/4−），它**既未登记于 `90 §11`，也未追加 `20 §12` 条目**——即 `90 §11:395`「90 生效后，任何 L0 修改若不在本节登记，即为违规」所指的那类违规，被新的完整性断言排除在视野之外。

---

## 2. 已独立复核的关键事实

### 2.1 Git / tree（全部实测）

```text
HEAD = 60fa9ff…   branch = od01-r3-convergence   parent = 71f51f9…
origin/od01-r3-convergence = 60fa9ff…   main = 6d8a3bd（未动）   origin/main = 7934844（未动）
10 files changed, 487 insertions(+), 2 deletions(-)   —— 全部 .md；backend/ 或非 .md 改动 = 0

Docs/V3_SPEC tree:
  9f1763e (pre-OD-R-01)  = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
  71f51f9 (incorporation)= 442172f40942368a4856231a742bf4d273242034
  60fa9ff (re-freeze)    = 8659e2fab715d1d2164f9bc559a04ceb05fd7fc0   ← 与报告 §7 一致
```

### 2.2 分类判定：与 `90 §3` 逐字吻合（**报告正确**）

| `90 §3` 原文 | 报告/CR-003 主张 | 判定 |
|---|---|---|
| `:407` CHANGE-2 = 新增此前未规定的强制约束 → **Change Record + 评审**；不必走四道门 | `10 §6.3` = CHANGE-2 | **TRUE** |
| `:408` CHANGE-3 = 改变既有规定的行为 → Change Record + 受影响层回归 | `20 §5.3` = CHANGE-3 | **TRUE** |
| `:412` 判定规则「拿不准往高里归」 | 主导分类取 CHANGE-3 | **TRUE** |
| `:414` 四道门（69 §5）**仅**适用 CHANGE-4/5 | 「本记录不需要四道门」 | **TRUE（逐字）** |

### 2.3 出生证明与创建门槛（**合规**）

- `90 §4:427-438`「每份新文档必须以如下块开头」：CR-003 头块 `:3-23` 含 Document Type / Authority Level / Status / Normative / Supersedes / Superseded By / Gate State Authority ✓
- `91 §5:163-176`（= `90 §4` 扩展为出生证明）共 **13** 字段：CR-003 头块 `:4-22` **13 项齐全** ✓（报告「头块 13 项字段齐全」**TRUE**）
- `91 §5.1:190-197` 创建门槛四问：CR-003 §0 `:31-38` 逐条回答 ✓，并在 §0.1 给出「与最近似文档的不可合并差异」（含 `90 §11` / CR-002 / `67` / D1 四个对照）✓
- 值域合法性：`Contract Change Record` ∈ `90 §4:430-431`；`L1` ∈ `90 §4:432` / `91 §5:167`；`ACTIVE` ∈ `90 §4:433` / `91 §5:168` ✓

### 2.4 L0 规范句「逐字未变」（**报告正确**）

`git diff 71f51f9 HEAD -- Docs/V3_SPEC/10_Data_Model.md Docs/V3_SPEC/20_Document_Pipeline.md` 的 numstat = `17/0` 与 `13/0` ⇒ **deletion = 0**，全部为 §12 追加；OD-R-01 两处规范句与 `71f51f9` 字节级一致 ✓

### 2.5 历史 hash 未机械替换（**报告正确**）

`git grep 'b3eeb3e9'` 命中 7 处（6 处现行/基线 + 历史报告），本 commit 的处置为**加注而不改值** ✓；`84 §0` 汇总与 `§2` 优先级**未被刷新**（符合上一轮 Owner「不刷新历史 snapshot」裁决）✓；G-02 §6.3 给出 9 行逐项判定表（historical vs false current-state）✓

### 2.6 re-freeze 自指问题（**处理正确**）

CR-003 §10 `:274-280`：因文件位于 `Docs/V3_SPEC/` 内，tree hash 字面值写入该目录会形成**自指不动点**，故权威登记采用 **commit 锚定**（`git rev-parse <生效 commit>:Docs/V3_SPEC`），字面值副本放目录外（G-02 §6）。该论证**成立** ✓，且三个 hash 均由 git 对象计算（无手填）✓

---

## 3. Findings

### R-01 [HIGH] 审计范围完整性断言不准确 —— `f708370` 未登记、且被新断言排除

**证据链（全部 DIRECTLY VERIFIED）**

```text
机械检验：git log --oneline 0dd954d..HEAD -- Docs/V3_SPEC/{00,10,20,30,40,50}*.md
  60fa9ff  docs: ratify OD-R-01 L0 change and re-freeze Frozen Spec      ← 本 commit（已登记 CA-003）
  71f51f9  docs: register OD-R-01 and close multi-blank Answer boundary  ← 已登记 CA-003
  f708370  fix(x2.6): m.3 checkpoint b — question/unit canonical vocabulary correction   ← 未登记

f708370 元信息：2026-09-21 12:25:53
  改动：Docs/V3_SPEC/20_Document_Pipeline.md   9 insertions(+), 4 deletions(-)
        §4.5:160,164 与 §6.1:355,359  standalone_question → standalone_unit（+ 加注 legacy vocabulary）
  时序：c5a899f（建立 90）2026-09-13 17:12 → f708370 2026-09-21 ⇒ 90 生效之后
        git merge-base --is-ancestor c5a899f f708370 = 0（YES）

登记检索：
  git grep 'f708370' Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md   → 0 命中（§11 审计表内无 CA 记录）
  git grep 'f708370' Docs/DECISIONS/84_CONFLICT_LEDGER.md     → 0 命中
  f708370 是否补过 20 §12 条目                                 → 否（diff 内无 §12 变更记录行）

仓内自证（该提交确属 L0 内容提交）：
  Docs/COORDINATION/G-02-FREEZE-REGISTRATION-VERIFICATION.md:88
    last content commit = f708370065870d89ac4ba025a1d47e38c411314e
```

**与本 commit 新断言冲突**

| 位置 | 文本 | 问题 |
|---|---|---|
| `84_CONFLICT_LEDGER.md` 审计范围行（**本 commit 修改**：`仅 40 一处` → `共两处，均已登记`） | 「`0dd954d` 之后触及 L0 的提交共 **两处**，均已登记——`0dd954d`（`40 §5` → CA-001）与 `71f51f9`（`10 §6.3`/`20 §5.3` → CA-003）」 | **漏 `f708370`** ⇒ 事实不准确 |
| `90 §11` 审计范围声明 `:388-395`（**既有文本，本 commit 未改**） | 「本节**已审计** `0dd954d` 之后**所有**触及 L0 的提交。更早的 L0 修改（`10`/`20` 于 09-08/09-09，`30`/`50` 于 09-08）…不在本轮审计范围」 | `f708370`（09-21）**既不在已登记集，也不在被豁免的"更早"集合**（该豁免只列 09-08/09-09）⇒ 落在两者之间的空档 |

**严重度依据**：`90 §11:226`「**任何对 L0 的修改，无论发生在 90 生效前或后，都必须在本节登记**」；`:395`「90 生效后，任何 L0 修改若不在本节登记，**即为违规**」。本轮在更新同一审计事实时**只改了 84、未同步订正 90 §11 的声明**，并新增了一句把该违规排除在外的完整性断言。

**影响**：声明式完整性（"共两处，均已登记"）会使后续读者/审查者停止检索 ⇒ 一个真实的未登记 L0 修改被制度性遮蔽。这恰是 `90 §11` 存在的理由。

**建议（供 Owner 裁决，DSH 不自行处置）**：
```text
(a) 为 f708370 补建 CA 记录（含分类：20 §4.5/§6.1 词汇修正 → CHANGE-2 或 CHANGE-1，按 90 §3 判定）
    + 必要时补 20 §12 条目；或
(b) 把 90 §11 / 84 的审计范围声明限定为明确枚举（"已登记：CA-001 / CA-003；其余 L0 提交见附录"），
    并显式声明 f708370 的状态（已审计未登记 / 待登记）。
现状「共两处，均已登记」两种读法下均不成立。
```

### R-02 [MED] 硬边界解除后缺少 tree-hash 漂移检测 —— 与 R-01 构成组合风险

- 旧硬边界（`OWNER-DECISIONS:347`「本轮硬边界要求 Frozen Spec tree hash 保持 `b3eeb3e9…` 不变」）已被本 commit 的时点范围注**显式解除**（`:353-358`），改为「经 L1 CR-003 → re-freeze」的常规路径。
- 新机制下 re-freeze identity 采用 **commit 锚定**（CR-003 §10）⇒ **任何后续对 `Docs/V3_SPEC/` 的触碰都会静默改变该 tree hash**，唯一保护是 `90 §11` 的登记义务。
- 而 R-01 证明该义务的"审计范围"声明本身不完整（且有既有空档）。
- **组合风险**：无 pinning + 声明式完整性 ⇒ 未来 L0 漂移可能既无 hash 守卫、也无有效检索口径。
- 说明：该风险**不是**本 commit 引入的设计错误（L0 可经 L1 修改是 `90 §1` 的正确设计）；但"历史硬边界已解除"这一事实**未在报告中作为治理后果说明**，建议 Owner 明确是否需要一个机械校验点（每见 L0 提交必须有对应 CA 记录）。DSH 不设计该机制。

### R-03 [MED] Owner 授权 / 审阅的仓内 provenance 仍缺独立落点

- 本轮**四处**断言 Owner 已批准 / 已审阅：
  - CR-003 §9 `:233-244`「Review / Owner Approval」+ `:244`「Review **ACCEPTED / EFFECTIVE**」
  - CR-003 §8 `:218-222`「Owner Decision（2026-09-24）」
  - `90 §11:365-371`「Owner Decision（2026-09-24）… **Review（2026-09-24，Owner）：ACCEPTED / EFFECTIVE**」
  - `10 §12` / `20 §12` 条目 + `OWNER-DECISIONS:352-358` 注
- 唯一依据是**仓外任务书**（DSH 无法核验）。
- 该情形与两处仓内先例同型：
  - `OWNER-DECISIONS:487`（F-OD01V4R-58 更正注）：附录曾以 `Owner Decision: APPROVED` 逐项登记，被认定「**无外部 Owner 证据**」并改为不含 Owner 授权主张的 `Applied Fix`；
  - 上一轮你就 **D1:392** 明确选择「方案 A：补建 current ratification」以闭合同类 provenance 缺口。
- **正面记分**：CR-003 §8 `:225-226` 正确写出「**current ratification ≠ historical authorization**」语义，未重构、未主张历史授权 ✓；§9 也未伪造历史日期 ✓。
- **建议（Owner 裁决）**：(i) 按上一轮模式补一条仓内 Owner authorization / ratification（覆盖 OD-R-01 的 L0 修改 + re-freeze），或 (ii) 在 CR-003 §9 明记**授权 instrument = 任务书（日期 / 编号）**，使链路在仓内可锚定。二者择一即可，DSH 不自选。

### R-04 [MED-LOW] CHANGE-3 的「受影响层回归」只覆盖文档层，未覆盖实现层（且未声明该缺口）

- `90 §3:408` CHANGE-3 明文要求「Change Record + **受影响层回归**」。
- CR-003 §7 `:197-208` 的 8 项全部为**文档 / 治理层**检查（git identity、tree 前后、L1 存在性、CA 登记、§12、语义文字、forbidden scope、hash 判定）。
- **未包含**：`20 §5.3` blank 映射收窄对**实现层**（Resolver / Compiler / IR 的 blank→answer 映射与 vocabulary 映射）的影响评估。
- 该缺口未被声明：CR-003 §6 的 exclusions `:178-188` 只排除 payload / answer_status / evidence / schema / migration 面，**未排除也未免责**"实现符合性未评估"。
- 反证实现层在本项目是被显式跟踪的：`f708370` 的 commit message 记录 `ir.py:112/146` 的词汇映射改动，并注明 `gate/service.py` 两处 diff **因权限分类器阻断而未改** ⇒ 实现层与 L0 的对应关系有既有跟踪实践。
- **建议**：一句显式声明（"实现层符合性未评估，本任务禁 code/runtime；如需跟踪请登记"）或按 D-07/D-08 先例登记为 residual。属**覆盖面缺口**，非内容错误。

### R-05 [LOW] `90 §2 R8` 引用错位（引文出自 `90 §4:440`）

- CR-003 §10 `:283`：历史表述不得机械替换，标注「（`90 §2 R8`「Reconcile, don't rewrite」）」；G-02 §6.2 同写「（`90 §2 R8`：Reconcile, don't rewrite）」；commit message 亦写「(90 §2 R8)」。
- 实测：`git grep 'Reconcile' Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` → **仅 1 处命中 = `:440`**（`90 §4` Status Header 规范节尾）。`90 §2 R8:170-181` 实为「**废止传播规则**」，其第 1 项确含「保留正文（历史审计证据，不得改写或删除）」——**原则相邻，但引文非出自 R8**。
- 判定：**LOW**（实质主张站得住：R8 第 1 项确实要求保留正文；属引文坐标错误）。建议改为 `90 §4:440`（或同时引 R8 第 1 项）。

### R-06 [LOW] `LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md:320` 的 `Frozen Spec: UNCHANGED` 未处理

- G-02 §6.3 `:第 10 行附近的说明`：该文件「属 Limited Implementation Authorization（另一授权面），本轮**不改**，以免扩大修改范围」，理由是该半句指 **OD-01 Option Provenance** 那条 change 的状态。
- 对抗性意见：该窄读法**可辩护**（括号内文字支持），但——该文件是 **ACTIVE 授权文书**，其 `Frozen Spec: UNCHANGED` 的**字面**读法现在已假；而 G-02 §6.3 自定准则为「只修『当前断言与当前事实**直接冲突**』处」，同一准则下 `Proposal:24` 被修、此处不改，**准则适用不一致**（虽已披露理由）。
- 风险：实施者据"UNCHANGED"形成过时前提；且该文件正是 `LIMIT-AUTH §3.5:149`「不允许自行新增 Frozen Data Model 属性」的载体，其基线表述宜明确。
- 建议：加一句 scope 限定即可（不改变其实质）。**LOW**。

### R-07 [LOW] untracked 计数口径（**连续第三轮**同一问题）

- 报告 §10：「10 个既有 untracked 条目（未清理、未纳入提交）」。
- 实测：`git status --porcelain`（默认）10 条目 ✓；`--untracked-files=all` = **13 个文件**（CONTRACTS 9 + GOVERNANCE 4）。
- 方向性结论（未清理、未入库）**成立** ✓；仅口径不一致。建议统一 `-uall`。

### R-08 [LOW / 信息] L1 的落点与命名引入新惯例（不违规）

| 记录 | 落点 | 层 / 状态 |
|---|---|---|
| `CR-001` | **内嵌** `90 §11:272-330` | L0-META 内 |
| `CR-002` | `Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md` | **未归层**（`90:47`）/ NOT RELEASED |
| `CR-003` | `Docs/V3_SPEC/CR-003_CONTRACT_CHANGE_RECORD_OD-R-01.md` | L1 / ACTIVE |

- `90 §1.2:79` 明文允许 `Docs/V3_SPEC/`「引用；补 Change Record；**新增 L1**」⇒ CR-003 的落点**有明文依据，不违规** ✓
- CR-003 §0.1 `:44` 已论证"为何不内嵌 `90 §11`"（内嵌会让审计载具兼任授权层，违反 `90 §1` 层分离）——论证**成立** ✓
- 但 `90` 未规定 L1 的**文件命名 / 模板 / 检索方式**；`90 §1.2:89-90` 只对 L0 文件名有"永久保持现状"规则。CR-003 的命名形态（`CR-00X_....md`）因此是**新惯例**。
- 建议：若 Owner 希望正式化，需改 `90`（L0-META）⇒ 又是一次需 L1 的修改；否则记为新惯例即可。**信息性**。

---

## 4. 上一轮 Findings 的处置核验（对抗性审查的闭环记录）

| 上轮 ID | 内容 | 本轮处置 | 判定 |
|---|---|---|---|
| F-01 | L0 被直接编辑、无合法入口 | 建 **L1 CR-003**（`90 §1.2:79` 允许列）+ CA-003 + re-freeze | **CURED** |
| F-02 | 同一 commit 违反 D1 自设禁区 | `OWNER-DECISIONS:352-358` 加时点范围注，值不改，显式说明第 2/3 条已由 Owner 解除 | **CURED** |
| F-03 | 4 处现行断言变假 + 基线漂移 | 6 处加注/更正（Proposal `:24`、Report `:27`、G-02 `:87`、D1 `:347`、IMPLEMENTATION-PLAN `:31/:452/:828`）+ G-02 §6.3 九行判定表 | **CURED**（`LIMIT-AUTH:320` 除外 → R-06） |
| F-04 | 先执行后询问的顺序倒置 | CR-003 §8 / `90 §11:362` 明确登记为 **procedural gap**，对齐 CA-001 同型定性；未追认历史授权 | **CURED（如实登记）** |
| F-05 | L0 §12 变更记录缺失 | `10 §12` / `20 §12` 各追加一条（含 L1 / CA / Source Commit / 分类 / 生效状态） | **CURED** |
| F-06 | payload `answer[]` 元素粒度未定 | `84` **D-07** 只登记不裁决（沿用 D-06 归类先例） | **CURED（按指令只登记）** |
| F-07 | `20 §6.3` 理由过度推论 | CR-003 §4 `:141-149` 明确更正："`answer=required` 只规定 role requirement，**不能单独作为『只有一个 Answer 对象』的证明**；唯一依据是 OD-R-01 本身" | **CURED** |
| F-08 | `value[i]` 指称 / 行数映射 | `84` **D-08** 只登记不裁决 | **CURED（按指令只登记）** |
| F-09 | 报告内自检自相矛盾 | 本轮报告无同类表述 | N/A |
| F-10 | untracked 口径 | 复现（→ R-07） | **未 cure** |
| F-11 | 验证未覆盖授权面 | CR-003 §7 现含 L1 存在性 / CA 登记 / classification / re-freeze 检查 | **部分 CURE**（仍缺实现层回归 → R-04） |

---

## 5. 报告自述 vs 实测（逐条）

| # | 报告自述 | 实测 | 判定 |
|---|---|---|---|
| 1 | CR-003 = `Docs/V3_SPEC/CR-003_CONTRACT_CHANGE_RECORD_OD-R-01.md`，Document Type/Authority Level/Status = CCR/L1/ACTIVE | 文件存在（296 行）；头块 `:3-23` 13 字段齐全，值域均合法 | **TRUE** |
| 2 | 编号避碰：CR-002/CA-002 已被占用 | `CR-002` 文件存在；`90 §11` 表内确无 CA-002 | **TRUE** |
| 3 | 分类 20 §5.3 = CHANGE-3；10 §6.3 = CHANGE-2；主导 CHANGE-3；四道门不需要 | 与 `90 §3:405-414` 逐字吻合 | **TRUE** |
| 4 | 10/20 「逐字未变；删除行 = 0」 | numstat 17/0、13/0 ⇒ deletion 0 | **TRUE** |
| 5 | CA-003 = 审计表 1 行 + 详情小节 | `90 §11:231` 表行 + `:332-386` 详情 | **TRUE** |
| 6 | 10 §12 / 20 §12 各追加一条 | 两处 `### 2026-09-24（OD-R-01 · 经 CR-003 / CA-003 生效）` | **TRUE** |
| 7 | old tree `b3eeb3e9` 永久保留、未机械替换 | 6 处加注均保留原值；§0/§2 snapshot 未刷新 | **TRUE** |
| 8 | new tree = `8659e2fa…`（= `60fa9ff:Docs/V3_SPEC`） | 实测一致 | **TRUE** |
| 9 | 三个 hash 均由 git 对象计算，无手填 | 三值均可由 `git rev-parse <rev>:Docs/V3_SPEC` 复算一致 | **TRUE** |
| 10 | re-freeze 权威登记 = CR-003 §10（commit 锚定），字面值在 G-02 §6（非权威） | 与 CR-003 §10 `:270-280`、G-02 §6 实测一致；自指论证成立 | **TRUE** |
| 11 | 「修复了哪些当前错误 baseline」共 6 处 | 6 处均已改（Proposal/Report/G-02/D1/PLAN×3 计入一处声明/84） | **TRUE**（另见 R-06 的第 7 处未处理） |
| 12 | push 成功，HEAD == origin/od01-r3-convergence == `60fa9ff` | 本地 remote-tracking = `60fa9ff` ✓；**远端独立复核受阻**（凭据，见 §6） | **PARTIAL** |
| 13 | 「本任务范围内：无 governance blocker」 | 本轮自身无 STOP 条件命中；但 R-01 的完整性断言需修正 | **PARTIAL** |
| 14 | 13.a 90 §1:41「L1 暂无」/ Status.md:2624 stale，未改（理由：`OWNER-DECISIONS:351`） | `90 §1:41` 与 `Status.md:2624`（「（当前为空）」）实测仍 stale ✓；`OWNER-DECISIONS:351` 确为禁改 90/91 规则 | **TRUE** |
| 15 | 13.b G-02 §6 位于未归层目录（`90:47`） | `Docs/COORDINATION/` 不在 `90 §1.2:66-74` 模型内 ✓ | **TRUE** |
| 16 | 13.c Proposal change set 与 `20 §5.3` 行级重叠未裁定 | Proposal `:25` 已加该声明；Proposal `:163`/`:409` 确有 `20 §5.3` 的 CHANGE-5 条目（**真实重叠风险**） | **TRUE（且风险真实）** |
| 17 | 13.d 84 D-07 / D-08 为 OPEN | 两行均存在、均为 `OPEN`、均标注"只登记不裁决" | **TRUE** |
| 18 | 「10 个既有 untracked 条目」 | 默认口径 10 ✓；`-uall` = 13 | 口径差异（R-07） |
| 19 | 未改 `90 §1:41` 等治理原则 | 90 仅 §11 追加（57 行、0 deletion），§1/§2/§3 未动 | **TRUE** |
| 20 | CR-003 §4 称过度推论"仓内 0 命中" | 精确短语仅命中 CR-003 自身引文行（自指），无实质实例 | **TRUE** |

---

## 6. 无法核验项（UNKNOWN）

```text
U-1  任务书原文（Owner 对 OD-R-01 的授权、对「保留不回滚」的裁决）—— 不在仓库内，
     DSH 无法核验其是否构成 L0 修改授权，以及是否明确要求 re-freeze。
     ⇒ 归 Owner 裁决（R-03）。
U-2  远端独立复核：git ls-remote 受凭据策略阻断（schannel SEC_E_NO_CREDENTIALS）。
     本地 remote-tracking ref = 60fa9ff，与报告一致；未从远端独立证实。
U-3  f708370 的 L0 词汇修正是否在仓外（AITutorX / X2.6 治理面）有其自身的授权/登记。
     本仓内 90 §11 与 84 均无登记（R-01 的登记缺口成立，与其仓外授权状态无关——
     90 §11:226 的登记义务不因授权来源而免除）。
```

---

## 7. Owner 裁决清单（本审查提出的待裁项）

| ID | 待裁问题 | 为何须 Owner 裁 |
|---|---|---|
| **OD-R-01-R2-D1** | `f708370`（2026-09-21，`20 §4.5/§6.1` 词汇修正）如何处置：补 CA 登记 + §12 条目，还是限定审计范围声明的措辞？ | 涉及 L0-META `90 §11` 的登记内容（R-01，HIGH） |
| **OD-R-01-R2-D2** | 是否需要一个"每次 L0 tree hash 变化必须有对应 CA 记录"的机械校验点？（硬边界已解除） | 治理机制设计，DSH 不设计（R-02） |
| **OD-R-01-R2-D3** | Owner 授权 / 审阅是否补仓内落点（Current Ratification 模式），或在 CR-003 §9 明记 instrument = 任务书？ | 授权 provenance，同 D1:392 先例（R-03） |
| **OD-R-01-R2-D4** | CHANGE-3 的"受影响层回归"是否需扩展到实现层符合性（或声明该缺口）？ | `90 §3:408` 的流程要件（R-04） |
| **OD-R-01-R2-D5** | R-05（`90 §2 R8` → `90 §4:440`）与 R-06（`LIMIT-AUTH:320` scope 限定）是否要求更正？ | 文档精确性，涉及 L0-META 引文（R-05 只需改 CR-003/G-02 自身文本） |

---

## 8. 应予记分之处

```text
+ 四件套齐备且互相锚定：L1 CR-003 → 90 §11 CA-003 → 10/20 §12 → re-freeze（CR-003 §10 + G-02 §6 副本）
+ 分类判定与 90 §3 逐字吻合，且显式声明"不降级"（CHANGE-1 不成立的理由写清）
+ 出生证明 13 字段齐全、91 §5.1 四问逐条回答、并论证 DG 冻结不适用（未自创层级/目录/registry）
+ 历史值未机械替换：6 处加注保留原值，84 §0/§2 历史 snapshot 未刷新（符合上一轮 Owner 裁决）
+ 自指问题处理正确：tree hash 字面值不入 Docs/V3_SPEC/，权威面用 commit 锚定，副本放目录外
+ 上一轮 DSH F-01～F-08 全部处置：F-07 明确更正（并承认唯一依据是 OD-R-01 本身）；F-06/F-08 按指令只登记
+ procedural gap 定性对齐 CA-001 先例，且明确"不追认历史授权""不重构历史"
+ 无 code / schema / DDL / migration / corpus / evidence / runtime 改动（10 文件全为 .md）
+ 三处 hash 全部 git 可复算，无手填；报告 §7/§8 的数字与实测一致
+ 主动披露 4 项残余治理事项（13.a–d），未掩盖；13.a 的"未改"理由有既有硬规则支撑（OWNER-DECISIONS:351）
```

---

## 9. 附：机械验证命令（可复现）

```powershell
$r='D:\Project\AITutors-v3'
git -C $r rev-parse HEAD ; git -C $r show --numstat --format='' 60fa9ff
foreach($x in @('9f1763e','71f51f9','60fa9ff')){ git -C $r rev-parse "${x}:Docs/V3_SPEC" }

# R-01：审计范围完整性
git -C $r log --oneline '0dd954d..HEAD' -- Docs/V3_SPEC/00_Master_Spec.md Docs/V3_SPEC/10_Data_Model.md `
  Docs/V3_SPEC/20_Document_Pipeline.md Docs/V3_SPEC/30_Task_LLM_Safety.md `
  Docs/V3_SPEC/40_Development_Rules.md Docs/V3_SPEC/50_Migration_Assets.md
git -C $r show --numstat --format='' f708370 -- Docs/V3_SPEC
git -C $r merge-base --is-ancestor c5a899f f708370    # 0 = f708370 在 90 生效之后
git -C $r grep -n -I 'f708370' -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md Docs/DECISIONS/84_CONFLICT_LEDGER.md
git -C $r show 60fa9ff -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md | Select-String '^@@|^\+[^+]'

# R-05：引文坐标
git -C $r grep -n -I 'Reconcile' -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md

# 2.4 L0 逐字未变
git -C $r diff --numstat 71f51f9 HEAD -- Docs/V3_SPEC/10_Data_Model.md Docs/V3_SPEC/20_Document_Pipeline.md
git -C $r ls-remote origin od01-r3-convergence    # U-2：需凭据，本环境受阻
```

---

*DSH 独立对抗性审查 · 对 git 对象与仓内文本取证 · 审查期间未修改任何文件、未 push · 全部结论均可由 §9 命令复现。*
