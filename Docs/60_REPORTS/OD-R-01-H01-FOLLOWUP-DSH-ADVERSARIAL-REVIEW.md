# OD-R-01 H-01 Follow-up 整改（H-05～H-08 闭合）— DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 H-01 Follow-up Remediation — 最终报告」（STATUS: COMPLETE） |
| 仓库 | `D:\Project\AITutors-v3`（分支 `od01-r3-convergence`） |
| 被审 commit | `615289957ecaa1562aced149a22c04bfcbfe3628`（parent `1ee84cd`；message = `docs: close OD-R-01 H01 follow-up findings`） |
| 改动面 | 3 files changed, 131 insertions(+), 13 deletions(-)：`Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` · `Docs/V3_SPEC/CR-003_CONTRACT_CHANGE_RECORD_OD-R-01.md` · `Docs/COORDINATION/G-02-FREEZE-REGISTRATION-VERIFICATION.md` |
| 审查基线 | HEAD = `6152899`（tracked 改动 0） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间未修改 `AITutors-v3` 任何文件、未 commit、未 push |
| 关联 | DSH 第 5 轮：`AITutor-X/Docs/60_REPORTS/OD-R-01-H01-FIX-DSH-ADVERSARIAL-REVIEW.md`（`294bfdb`，其中 H-05/H-06 MED、H-07/H-08 LOW = 本轮被修对象） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（H-05 / H-06 / H-07 / H-08 四项**实质闭合**，逐条实测可证；
 另：DSH 撤回自身 H-08(a) 判据；本 commit 新增 2 项 MED、3 项 LOW 文档精确性/可追溯性残留）
```

**一句话结论**：上一轮的两项 MED 与两项 LOW **全部真实闭合**，且**固定点处置是本轮最漂亮的一处**——CURRENT tree 字面值只写在 `Docs/V3_SPEC/` **之外**（实测该目录内 0 处），`90 §11 (c)` 内只写**历史** tree（`63810f55…` / `47a59e50…`），因此写入行为不改变被记录的 tree，无自指不动点；这比"更新一下字面值"高一个层次。历史 hash 一律未改写，`H-07(a)` 更采用了 DSH 指出的**根因修法**（改为指向 `90 §1:41`，不再重复计数）。

须闭合项集中在**新加的 L0-META 规范性注记自身的登记/分类完整性**与**仓外 finding-ID 坐标不可解析**两处（各 MED，都是一行级修法），不涉授权、分类、re-freeze 链。

---

## 2. DSH 自我更正：撤回第 5 轮 H-08(a)

第 5 轮 DSH 判定「命令 3、4 使用 `grep -rn "a|b|c"`（BRE）：`|` 为字面量 ⇒ 0 命中、exit 1 ⇒ 所载命令不可复现」。**本轮实测后 DSH 撤回该判据**，理由三条：

1. **实测**（`git grep`，BRE 语义与 GNU grep 一致）：转义写法确实产出报告所载结果——
   `git grep -n '无 Contract Change Record\|不存在 Contract Change Record\|无一份 L1'` → **命中 `84:176`**（`\|` = alternation）；裸 `|` 写法 → 仅命中**字面量**本身。
2. 被审报告所载结果（「剩余 1 处 = `84:176`」）**恰是转义写法才可能产出**的结果，故原命令应为可用写法。
3. 决定性证据是 **DSH 自己的报告内部不一致**：第 5 轮 §3.1 表格把命令转写为带 `\|` 的形式，§4 H-08(a) 却按**裸 `|`** 立论——这是 DSH 侧的转写错误，不是被审方的缺陷。

**Claude 的实测更正（「GNU BRE 下 `\|` = alternation，裸 `|` = 字面量」）技术上正确，DSH 接受。** 取证纪律仍以 `-E` + 裸 `|` 为准（语义唯一、可移植），该纪律本轮已落盘于 `G-02 §6.4` ✓。

**残余影响**：第 5 轮 H-08(b)（提交后 `git diff --name-only` 为空验证）与 H-08(c)（扫描口径缺 tree-hash 类断言）**不受影响、依然成立**，且本轮已完整闭合——故第 5 轮 VERDICT 不变。

*方法学边界*：本沙箱禁止 `grep.exe`（`couldn't create signal pipe, Win32 error 5`），故 GNU grep 侧未能直接复现；上表由 `git grep` 等价复现（两者 BRE 行为一致），并把结果如实记于此。

---

## 3. 已独立复核的关键事实（DIRECTLY VERIFIED）

```text
HEAD = 6152899… ✓   branch = od01-r3-convergence ✓   parent = 1ee84cd… ✓
origin/od01-r3-convergence = 6152899… ✓（git ls-remote 直接核验远程 ref）
origin/main = 7934844…（未动）✓   main = 6d8a3bd…（未动，仍领先 origin/main 12 commit，既存状态）✓
3 files changed, +131 / −13 ✓   非 .md = 0 ✓   L0 00–50 = 0 ✓   code/schema/migration = 0 ✓

tree 等式（报告 TREE IDENTITY 段）：
  1ee84cd:Docs/V3_SPEC = 47a59e50126f0f7e98f44d281f8d388236240735  ✓
  6152899:Docs/V3_SPEC = ecd12c0e9682eaed2e3ad7c2416984b9cff92bee  ✓ = HEAD:Docs/V3_SPEC
  G-02:163 CURRENT 字面值 = ecd12c0e9682eaed2e3ad7c2416984b9cff92bee  ⇒ EQUAL ✓

固定点（自指防火墙）实测：
  `ecd12c0e…` 全仓 3 处，**全部**在 G-02 之外于 Docs/V3_SPEC 的文件中：G-02:163 / :278 / :294
  在 `Docs/V3_SPEC/` 内命中 = 0（git grep exit 1）✓ ⇒ 写入 CURRENT 不改变被记 tree ✓
  `63810f55…` → 仅 G-02:148/:155（已改为历史阶段值）与 `90:513`（历史证据，缩写形式）✓ 无当前态框架
  `47a59e50…` → 仅 G-02:149/:156/:277 与 `90:513`，均为历史阶段 ✓

90 §11 (c)：规则正文 :489-491「必须」逐字**未改**（hunk 起于 :510）✓
  声明登记表 :512（5a46d33，文本未改）· :513（1ee84cd）· :514（本 commit）✓ 3 行
  全仓 `L0-META / L1 面改动，非 L0 修改` 命中 = :491 + :512 + :513 + :514 ✓（与报告一致）
  新增行锚定注实际跨度 :516-522（报告写 :516-520，引用范围略短，无实质影响）

历史 hash 未改写：fa1e953e / b3eeb3e9 / 442172f4 / 8659e2fa / a704cd8f / 2edd2010 逐条未动 ✓
AITutor-X：tracked 改动 0 ✓（HEAD = 294bfdb = DSH 上一轮报告）
```

---

## 4. H-05～H-08 闭合核验（逐条实测）

| 上轮 finding | 本轮修法（实测） | 判定 |
|---|---|---|
| **H-05** `90 §11 (c)` 声明缺口 | `:513` 实名行（`1ee84cd`，含 tree 证据 `63810f55…`→`47a59e50…` 与两条机械取值命令）+ `:514` 自指行；规则正文 `:489-491` 未改；未造豁免、未建机制。另补 `:516-522` 行锚定注，规定「本行所在 commit」= **引入该行的 commit**，并明令**不得**用 `git log -1` 解析（该命令只返回最近一次触及本文件的 commit） | **CLOSED**（分类完整性见 H-09） |
| **H-06** G-02 CURRENT 失效 | `:148` 去掉 `= **current**` 并落实历史实值 `63810f55…`（取值命令改为 `git rev-parse 5a46d33:Docs/V3_SPEC`）；新增 `:149`（1ee84cd）与 `:150`（= current）两行；`:155-156` 链式图追加两阶段；`:163` CURRENT = `ecd12c0e…`，实测 **== HEAD:Docs/V3_SPEC** ✓；新增"固定点说明"明写本节**既定义务**（今后再变须同步追加） | **CLOSED** |
| **H-07** 替换文本自身缺陷 | (a) 删除「亦已新增 … **两条**」，改为「**L1 当前状态以 `90 §1:41` 为准（本注记不作重复计数，不自建第二套 registry）**」——正面采用 DSH 指出的**根因修法**；(b) **当期 → 当时** ✓；(c) 补「上述**「搜索结论」中的**」限定 ✓；(d) 首句加「（2026-09-25，H-01 修正 / H-07 措辞精确化）」✓。实测 `git grep -E '当期\|上述文件清单\|亦已新增'`（排除 G-02）= **0 命中** ✓ | **CLOSED** |
| **H-08** 验证表可复现性 | 新增 `G-02 §6.4`（`:199-298`，既有 verification record 内小节）：A1–A4 交替检索表（一律 `-E`）、三写法实测对照、B1–B3 commit-specific 核验、C1→C2→C3→C4 三段机械链 + "任一环节断链即违规"。DSH 独立复现：A1 = 4 处（CR-003 :52/:55/:56/:57）✓ · A2 = `84:176` 唯一 ✓ · A3 = 0 ✓ · A4 = `CR-003:50` 唯一 ✓ · C3 = 4 行 ✓ · C4 等式成立 ✓ · B（`git show --name-only --format=`）= 3 `.md`、非 `.md` 0、L0 0 ✓ | **CLOSED**（H-08(a) 判据已由 DSH 撤回，见 §2；残留见 H-11/H-13） |

**报告自述其余各项**：路径说明（AITutor-X 0 tracked）✓ · TREE IDENTITY 三等式 ✓ · §11(c)「required 2 / actual 3」✓ · Validation A–H 全部可复现 ✓ · Governance safety 12 项全 TRUE（无 code/schema/migration/新机制/编号改动）✓ · Commit/push（`1ee84cd..6152899`、远程 ref = 6152899、main 未动）✓ · Residual findings 1–4 描述准确（§6.1:117-118 内容属实且现确实返回 6152899；`84:176` 仍在；H-03/H-04 未触碰；CLOSED 留给 Owner）✓ · H-08 落点说明（第 5 轮验证表不在仓内）✓。

---

## 5. Findings

### H-09 [MED] 新增的 L0-META 规范性注记：`(c)` 行「改动面」漏登，且未分类 / 未声明授权落点

**事实**：本 commit 在 `90 §11 (c)` 内**删除**了原有的机械取值指令（`> 机械取值：git log -1 --format=%H -- …`），**新增** 7 行注记（`:516-522`），其中含**强制措辞**「**不得**用 `git log -1 --format=%H` 解析自指行」。而 `:514` 行的「改动面」列写的是「`90 §11 (c)` 本表补登 `1ee84cd` 与本行 · `CR-003 §0.1` 措辞精确化（H-07）· `G-02 §6` CURRENT 同步 + 机械复核命令表（H-06 / H-08）」——**未提及该注记**，即该行对自身 commit 的改动面描述**不完整**。

**为何是问题**：① `90:530` 明写「**Errata 不应只处理「放宽」。新增强制 invariant 同样是正式变更。**」，`:536` CHANGE-2 = 新增此前未规定的强制约束 → **Change Record + 评审**；`:541`「**拿不准往高里归**」；② 本 commit 的上一棒（`5a46d33`，M-02）刚刚建立过先例：把「既有登记义务」与「**本次新增**的审计完整性措辞」**严格分列**并给出**授权落点**（`90:496-506`）。本 commit 未做同型处置；③ 该注记**改动**了既有指令（原有 `git log -1` 指令被废止并代之以禁令），按 `:537` CHANGE-3 口径亦可能成立。

**最强反方辩解（诚实列出）**：① 该注记可读作对既有「必须补一行声明」义务的**解释**（即自指行一直意指"引入该行的 commit"）＋对一个**可证伪的错误命令**的更正——按 `:535` 可归 CHANGE-1（措辞澄清，规范语义零变化）；② 按本项目 `(c)` 的既有构造，`90` 本体编辑只需 `(c)` 声明行、不需 CR（`:490-491` 把「仅改 `90`/`91`」与「新增/修改 L1 文件」并列为"非 L0 修改"）；③ 该注记内容**正确且有用**（原 `git log -1` 确实会误解析 `:512` 行）。

**但**：即使按最宽读法（CHANGE-1），`90 §3` 仍要求**至少**简式 Change Record 或等效分类记录；且在 M-02 先例后，**新增强制措辞出现在 L0-META** 而不声明其性质与落点，与上一棒自我设定的纪律不一致。修法极廉价：在 `:514` 行「改动面」补一句并标注分类（例如「＋`90 §11 (c)` 自指行解析规则澄清（判为 CHANGE-1：语义零变化；原 `git log -1` 指令可证伪）」）。

---

### H-10 [MED] 仓外不可解析坐标（H-01 / H-05～H-08 / HYG-D1）进入 L0-META 与 ACTIVE L1

**事实**：这些 finding 编号属**仓外**审查产物（DSH 报告在另一仓 `AITutor-X`），而本轮 commit 把它们写进了：
- `90 §11 (c)`：`:513`（「OD-R-01 H-01 修正 / HYG-D1」）· `:514`（「H-05~H-08 闭合」「（H-07）」「（H-06 / H-08）」）· `:516`（「（2026-09-25，H-05）」）；
- `CR-003`（ACTIVE L1）`:54`：「（2026-09-25，H-01 修正 / H-07 措辞精确化）」；
- `G-02`：`:149`（「HYG-D1 / DSH 第 4 轮 H-01」）· `:150` · `:168` · `§6.4` 标题（`:199`）。

**为何是问题**：仓内**无任何解析路径**——没有报告路径、没有 commit 锚点、没有编号规则说明。这与 DSH 第 3 轮 **M-01**（task-book 坐标仓内不可解析）**完全同类**，而项目对该类问题的既定处置正是 `CR-004 §2.4`：给坐标对照表 + 明写**可复核性边界**。更实质的是：`90 §11 (c)` 是 **Change Audit Record**，其声明行存在的意义就是可验证；写「H-05~H-08 闭合」而未来审计者无法解析 H-05 是什么，等于在**审计记录**里留了一个不可验证的断言。

**反方最强辩解**：编号对 Owner 与当前工作流是可识别的；本轮任务书本身即以 H-05～H-08 下达，属于共同语境；且 `G-02:149` 已写「DSH 第 4 轮」，提供了部分语境。**但**「当下可识别」≠「仓内可解析」——M-01 的争议点恰是后者。

**建议修法（一行级）**：给一个锚点即可，例如在 `90:513` 首次出现处补「（外部审查记录：AITutor-X `Docs/60_REPORTS/OD-R-01-H01-FIX-DSH-ADVERSARIAL-REVIEW.md` @ `294bfdb`；**仓外坐标，仓内不可解析**）」，或在 `G-02 §6.4` 内加一行坐标对照（照 `CR-004 §2.4` 体例）。

---

### H-11 [LOW] 自指行的"机械取值"仍需人工模糊匹配；`§6.4` 以永久 exclude 处置污染，使 G-02 自身成盲区

**(a) 解析规则尚不机械**：`:514` 行写「本行所在 commit（2026-09-25，OD-R-01 H01 follow-up：H-05~H-08 闭合）」，而实际 commit subject 是 `docs: close OD-R-01 H01 follow-up findings`——两者**文本不等**。`:519-521` 给出的机械程序是 `git log --format='%H %s' -- …` + 「取 subject 含「OD-R-01 H01 follow-up」的那一行」，落在 G-02 `§6.4` 的被验 commit 上恰好可匹配；但对 `90` 表的自指行，规则**没有**给出可精确匹配的检索串（`5a46d33` 行同理：「OD-R-01 最终卫生收口 M-01~M-05」vs `docs: OD-R-01 final hygiene closure M-01~M-05`）。结论：一条自称"机械"的规则实际需要人工模糊比对。**建议**：在自指行内追加该 commit 的 subject 字面（或事后补实名 hash），使匹配精确。

**(b) 污染处置的代价未计入**：`§6.4` 把被检模式**字面量**写进 G-02，随即对所有检索加 `:(exclude)…G-02…`。DSH 独立复现确认污染真实存在（裸字面量现 **3 命中**，全部在 `§6.4` 的 `:228`/`:243`/`:249`）；但 exclude 是**永久**的——若今后 G-02 内再出现「当期」或无限定的「无 Contract Change Record」，该验证表**永远不会报警**。**建议**：在 `§6.4` 内明记这一盲区代价，或改用不写裸字面量的写法（例如以模式类或分词描述代替原样串），从而无需 exclude。

---

### H-12 [LOW] G-02 §6.1:117-118 的活指令与新增 `90` 禁令直接冲突，未标注 superseded

`G-02:117-118` 至今仍写「Re-freeze commit : 本记录所在 commit（机械取值：`git log -1 --format=%H -- …G-02…`）」——**正是**新注记 `:521-522` 明令**不得**使用的解析方式；且按 `§6.2` 表，OD-R-01 re-freeze 实为 `60fa9ff`，该行的表述本身也不成立。报告把它列为残留观察 #1 并援引「Do not modify unrelated historical entries」未改。**但**这是一条**活的机械指令**，不是历史条目；同一文件、同一 commit 内一处新立禁令、一处保留被禁用法，构成文件内自相矛盾。**建议**：改为 commit 锚定（`60fa9ff`）或就地标注「已被 `90 §11 (c)` 行锚定注取代（superseded）」。报告已如实披露，故定 LOW。

---

### H-13 [LOW/INFO] `§6.4`「可原样复现」的前提未注明；CURRENT 推导记录与 commit root tree 不一致

**(a)** `§6.4` 混用 `git grep`（可移植）与裸 `grep -rnE` / `grep -vE`（依赖 **GNU grep 在 PATH**）。DSH 环境实测无 `grep`（PATH 无；Git 自带 `grep.exe` 在本沙箱被拒）。表称"均可原样复现"，建议注明环境前提，或命令统一改用 `git grep`。

**(b)** 报告写 CURRENT 由 `git add` → `git write-tree` 得 `T = 45fc29da…` 再 `git rev-parse T:Docs/V3_SPEC` 算得；但本 commit 的 root tree 实测 = `471d6b27…`（`V3_SPEC` 子树等式本身已核验为真）。最可能解释是 `write-tree` 取值发生在最后一次 G-02（位于 `V3_SPEC` 之外）编辑之前——**不影响结论**，但使所载推导路径不能被逐字重放。建议记最终值或删去中间 T 值。

---

## 6. 记分：本轮做对的地方

1. **四项 findings 实质闭合**，且每项都能被 DSH 独立复现（§4 全表）。
2. **固定点处置正确且自洽**：CURRENT 字面值只在 `Docs/V3_SPEC/` **之外**；`Docs/V3_SPEC/` 内实测 **0 处**当前 tree 字面值；`90` 内只写**历史** tree ⇒ 写入不改变被记 tree。这是本题真正的设计解。
3. **历史不被改写**：六个历史 baseline hash 逐条未动；`:148` 正确地从「= current」降为历史实值。符合 `90 §4`「Reconcile, don't rewrite」。
4. **H-07(a) 采用根因修法**：不是把「两条」改成「三条」，而是改为**指向 `90 §1:41`** 并声明不自建第二套 registry —— 正面消除了复发的固定点。
5. **首次出现"自查自报"**：主动发现把被检模式写入验证表导致的自指污染，并披露处置（DSH 复现：污染命中 3 处、位置与其所载完全一致）✓ 披露准确。
6. **对 DSH 判据的实测更正技术上正确**，DSH 据此撤回自身 H-08(a)（§2）——被审方能纠正审查方，且证据成立。
7. **不越界**：3 文件、无 L0 `00`–`50`、无 code/schema/migration、无新机制/审批层/registry/新文档类型、编号未动。
8. **残留项如实登记**（§6.1 陈旧自指、H-02/H-03/H-04 未触碰、CLOSED 属 Owner），未隐去对自己不利的事实。

---

## 7. Owner 裁决清单（DSH 只列项与证据，不作裁决）

```text
OD-R-01-H01R-D1  【MED】H-09：`90:514` 行「改动面」补登本 commit 在 `90 §11 (c)` 新增的行锚定注，
                 并给出分类（CHANGE-1 / CHANGE-2 择一说明；若认定新增强制措辞，按 M-02 先例声明授权落点）
OD-R-01-H01R-D2  【MED】H-10：为 H-01 / H-05~H-08 / HYG-D1 补仓内可解析锚点（报告路径 @ commit），
                 或按 `CR-004 §2.4` 体例加「仓外坐标、仓内不可解析」的可复核性边界注
OD-R-01-H01R-D3  【LOW】H-11：自指行补 commit subject 字面使解析可机械执行；并明记 `§6.4` exclude G-02 的盲区代价
OD-R-01-H01R-D4  【LOW】H-12：`G-02 §6.1:117-118` 改为 commit 锚定，或标注已被 `90 §11 (c)` 新注取代
OD-R-01-H01R-D5  【LOW】H-13：`§6.4` 注明环境前提（GNU grep on PATH）或统一 `git grep`；修/删 `T = 45fc29da…` 推导值
OD-R-01-H01R-D6  【OD-R-01 是否 CLOSED】DSH 立场：
                 `90 §11 (c)` 登记链自 `5a46d33` → `1ee84cd` → `6152899` **完整**（实测 3 行 + 规则原文未改），
                 H-05/H-06/H-07/H-08 全部闭合，授权 / 分类 / re-freeze / provenance 链**均闭合**；
                 H-09 / H-10 属文档登记完整性与坐标可追溯性残留（各一行级修法），**不阻断 CLOSED**。
                 DSH 不代行该裁决。
```

**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 8. 未验证 / UNKNOWN

```text
UNKNOWN  仓外任务书原文（H-05~H-08 的原始措辞、授权范围、NON-AUTHORIZED 清单）
         —— 不在仓内；DSH 只核验其可核验后果
UNKNOWN  首次 push 的「Recv failure: Connection was aborted」失败事件
         —— 无法从 ref 状态反推；远程 ref 终态已核验 = 6152899 ✓
方法学边界  GNU grep 在本沙箱不可执行（signal pipe 被拒）；BRE 三写法对照由 `git grep` 等价复现
INFO     本地 `main` = 6d8a3bd 领先 `origin/main` = 7934844 共 12 commit（均不触及 `Docs/V3_SPEC`）
         —— 既存状态，本 commit 未改变
INFO     本 commit 之后，`git diff --name-only` 一类命令文本因 `§6.4` 而入仓（此前报告称"仓内 0 命中"就当时成立）
```

---

**Document control**

| Field | Value |
|---|---|
| Path | `Docs/60_REPORTS/OD-R-01-H01-FOLLOWUP-DSH-ADVERSARIAL-REVIEW.md` |
| Status | FINAL |
| Reviewed commit | `615289957ecaa1562aced149a22c04bfcbfe3628` |
| Round | OD-R-01 对抗性审查第 6 轮 |
| Verdict | ACCEPTED WITH FINDINGS（H-05~H-08 全部 CLOSED；H-09/H-10 MED · H-11/H-12/H-13 LOW；DSH 撤回 H-08(a)） |
| Repo of subject | `kurt-wong/AITutors-v3` @ `od01-r3-convergence` |
| This report repo | `D:\Project\AITutor-X`（DSH 侧，未修改被审仓任何文件） |
