# OD-R-01 Final Governance Closure + f708370 Provenance Remediation — DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Final Governance Closure + f708370 Provenance Remediation — 最终验证」 |
| 仓库 | `D:\Project\AITutors-v3` |
| 分支 | `od01-r3-convergence` |
| 被审 commit | `12493cab2aed8df914f54a938bf6797663e11234`（WS-A）· `fbec14e9d4c79e78f3c459d5a361ca6d40ed9cc1`（WS-B，HEAD） |
| 审查基线 | HEAD = `fbec14e`（工作区干净、tracked 改动 0） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间未修改任何文件、未 push |
| 关联 | 上一轮：`AITutor-X/Docs/60_REPORTS/OD-R-01-GOVERNANCE-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md`（`23000ef`） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED
（OD-R-01 与 f708370 两条链均已闭合；5 项 findings 均为非阻断的精确性 / 落点事项）
```

**一句话结论**：本轮把上一轮唯一的 HIGH（R-01 审计完整性）**实质修好**——我独立复算的 L0 提交全集与其枚举**逐笔吻合**（20 = 15 historical-exempt + 5 registered）；CR-004 的权威论证**逐条引文实测成立**（这是上一轮 F-07 型"过度推论"的**反面**）；四件套分列（L0 change / implementation / test evidence / provenance）严格不混；无 production code 改动、无 rewrite、无重复记录。

5 项 findings 全部为**精确性与落点**问题，不改变任何业务语义或授权结论。

---

## 2. 已独立复核的关键事实

### 2.1 Git / tree（全部实测）

```text
HEAD = fbec14e…   branch = od01-r3-convergence   origin/od01-r3-convergence = fbec14e… ✓
main = 6d8a3bd（未动）   origin/main = 7934844（未动）
71f51f9 可达 ✓   f708370 可达 ✓（无 rewrite history / force push）

Doc/V3_SPEC tree 链（全部可复算）：
  fa1e953e…（pre-f708370，= f708370^）→ b3eeb3e9…（f708370 incorporation）
  → 442172f4…（71f51f9 / OD-R-01）→ 8659e2fa…（60fa9ff re-freeze）
  → a704cd8f…（12493ca / WS-A）→ 2edd2010…（fbec14e / WS-B = current）
  ⇒ CR-004 §8 声称的 fa1e953e→b3eeb3e9：实测 f708370^:Docs/V3_SPEC = fa1e953e7c4638236b298cf1c137aa2a107d5ea5 ✓
                              f708370:Docs/V3_SPEC  = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f ✓
  ⇒ 「同值说明（非笔误）」成立：f708370 是 OD-R-01 之前最后一次 L0 内容变更 ✓

红线检查：60fa9ff..HEAD 的改动文件中，backend/* 或非 .md = 0 ✓（无 production code / schema / migration）
```

### 2.2 L0 审计全集：**枚举与实测逐笔吻合**（上一轮 R-01 的实质修复）

```text
独立复算：git log -- Docs/V3_SPEC/{00,10,20,30,40,50}*.md  →  全历史 20 笔
  0dd954d 及其后（含 0dd954d 本身）= 5 笔：0dd954d · f708370 · 71f51f9 · 60fa9ff · fbec14e
  0dd954d 之前                     = 15 笔：88e7a29 b02c16c 60bc497 95c1700 5ae9853 ff64352
                                          a105bf8 c6014f7 3cca050 9c1d43f b24b5a7 19d236b
                                          5f0d3d0 0b0a4d3 5c9ecc9
  5 + 15 = 20 ✓ 与总数一致

90 §11 (a) 表：5 笔 L0 + 1 行非 L0（12493ca，行内自注「非 L0 00–50」）✓
90 §11 (b) 表：15 笔 historical-exempt，**ID 与实测逐笔一致** ✓，日期（09-05 / 09-08 / 09-09）
              全部早于 90 建立（c5a899f = 2026-09-13 17:12）✓
撤回声明：90 §11:445 逐字撤回原「已审计 0dd954d 之后所有触及 L0 的提交」，
          并声明不再使用该完备性断言 ✓；「已审计…所有」命中 3 处（:445 原文引用撤回 / :447 禁止 /
          :481 仍不使用）**全部为撤回或禁止语句**，与报告自述一致 ✓
```

### 2.3 CR-004 的权威论证：**引文逐条实测成立**

| CR-004 引用 | 实测 | 判定 |
|---|---|---|
| L0 `README.md §2.2`（`README:68` =「术语裁决（权威）」）内含 `\| standalone_unit \| 可独立解答的题 \| standalone_question / independent \|` | `README:68` = `## 2. 术语裁决（权威）`；`:88-90` 逐字一致 | **TRUE** |
| `00:10` / `10:14` / `20:13` 三分册均写「术语裁决以 `README.md` §2 为准」 | 三处逐字命中 ✓ | **TRUE** |
| L0 `10 §5.2:290` / `§6.5:516` = `unit_type` 闭集 `standalone_unit / composite_unit` | 两行逐字一致，且不含 `standalone_question` ✓ | **TRUE** |
| `IMPLEMENTATION-PLAN-v0.3.md:83` 位于 `## 0b. Owner Decisions OD-01 ~ OD-05` 块内 | 该块起于 `:71`，`:83` 逐字为 Terminology（mandatory）✓ | **TRUE** |
| `OD-P09` / `OD-P11` | `V3-CONTRACT-v0.3-OWNER-DECISION-PACKAGE.md:80/:82` 逐字一致 ✓ | **TRUE** |
| `OD-2`（Legacy Unit Type 归一裁决） | 存在于预处理契约文档（`PREPROCESSING-V3-CONTRACT-v0.3-DRAFT.md` 等）✓ | **TRUE** |

⇒ 与上一轮 F-07（`20 §6.3` role requirement 被过度推论为对象数量证明）形成对照：**本轮论证方式正确**（引用 L0 权威术语表 + L0 闭集，而非引用不相干的表）。

### 2.4 四件套分列 + 诚实标注（**报告正确**）

| 项 | 内容 | 报告定性 | 判定 |
|---|---|---|---|
| 4.A | `20 §4.5` / `§6.1` 文字与 JSON 规定值变化 | Frozen Spec change → 计入分类 | **TRUE** |
| 4.B | `backend/app/domains/compile/ir.py` :112 / :146（+2/−2，**f708370 时点**） | implementation consequence → 不计入分类 | **TRUE**（本轮未改任何 backend 文件 ✓） |
| 4.C | 两个测试文件（+150 / +17−4，**f708370 时点**） | verification evidence → 非架构事实 | **TRUE** |
| 4.D | 本 Change Record | provenance | **TRUE** |
| 回归 | 实现层回归 **NOT VERIFIED**；f708370 自述 137/197 passed 记为 **DOCUMENT CLAIM**，未伪造 | 如实记录 | **TRUE（`CR-004 §6` + `CR-003 §7` 双处记录，含「不得误读」注）** |

---

## 3. Findings（5 项，全部非阻断）

### M-01 [MED] L1 记录的判定依据引用了**仓内不可解析**的 task-book 坐标

```text
CR-004 规范性推理中使用的坐标（全部指向任务书，非仓内文档）：
  :69  「## 2. Owner authority（§11 / §14 判定）」
  :86  「不属于 §14 情况 C，未触发 STOP。归 §14 情况 B」
  :105 「若 Owner 认为…应触发 §22 STOP-1」
  :131 「§10A 要求：不因『修正词汇』自动归 CI-1」
  :171 「verification evidence（任务书 §10C）」
  :187 「不做（§22 STOP-8）」
检索：仓内定义「§14 情况 B/C」「§22 STOP-1/STOP-8」的文档 = 0（唯一命中即 CR-004 自身）
```

**影响（含对本次审查的直接后果）**：CR-004 的**关键处置**（"未触发 STOP"、分类不降级）以这些坐标为判据，但 L1 是**永久治理产物**，未来的实施者 / 审查者 / Owner 无法从仓库解析 `§14 情况 B` 与 `§22 STOP-1` 的原文。**本次审查即因此无法独立核验 STOP-1 的判据**（见 §5 U-1）——只能退回到"命题是否有 L0 支撑"来间接判断。

**建议（供 Owner；DSH 不自行补写）**：在 CR-004 增一行「任务书坐标对照」（如 `§14 情况 B = <一句话判据>`），或把判据摘要写入本记录，使其可自证。同型问题在上上轮（R3-05「见 §5」悬空引用）已出现过一次。

### M-02 [LOW-MED] `90 §11 (c)` 是 L0-META 中的**新增规范性要求**，超出"登记"性质

- `90 §11 (c):475-481` 新增：「`Docs/V3_SPEC` tree hash 发生变化时，**必须**能在本节找到对应 CA 条目；若不触及 L0 00–50，**则**在本节补一行声明」。
- 报告定性为「R-02 —— 只记录最小治理要求，**不建机制**」；就"未新建 CI / 数据库 / 服务 / 脚本"而言**成立** ✓（实测无非 .md 改动 ✓）。
- 但该条本身是一条**新的强制要求**（"必须…则…"），写入了 L0-META `90`。而项目对 90 的修改有既有硬规则语境（`OWNER-DECISIONS:351`「不得修改 90/91 规则迁就…」；上一轮 CR-003 亦自述"不改变 90/91 治理原则"）。
- 判定：**不阻断**（内容与我的 R-02 建议方向一致，且 Owner 已在 WS-A 授权该修正）；但"登记动作"与"新增要求"的界限应写明，并明确其 Owner 授权落点——与本轮其他 Owner 断言同源（见 M-03）。

### M-03 [LOW] `LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md`（`STATUS: OWNER APPROVED`）被代理编辑

- `12493ca` 修改该文件 `:320` 附近（+4/−1）：`UNCHANGED (OD-01 change is PROPOSAL only until re-freeze)` → `UNCHANGED w.r.t. OD-01 Option Provenance (…)` + 【scope clarification】说明 + 指向 G-02 §6。
- 该改动**只缩窄读法、未改变任何授权范围** ✓，且正是上一轮 R-06 的建议方向 ✓。
- 但该文件头部为 `STATUS: OWNER APPROVED` / `OWNER-APPROVED: YES` / `ENTERED-INTO-GIT: YES (G-01)`，其正文现已**不同于 Owner 批准时的文本**。文件属 `Docs/COORDINATION/`（未归层，不触 L0/L1）⇒ 不构成 L0 违规 ✓。
- **建议**：一行 ratification 注记（或并入 `OWNER-DECISIONS` 的 provenance 块），使"Owner 批准文本 = 现行文本"这一等式在仓内成立。

### M-04 [LOW] `90 §11 (a)` 的计数与表体不一致

- 标题：`#### (a) 0dd954d 及其后触及 L0 的提交 —— 完整枚举，5 笔`；表体 **6 行**（第 5 行 `12493ca` 行内自注「L1，**非** L0 00–50」）。
- 口径行（`:449`）为 `git log -- Docs/V3_SPEC/{00,10,20,30,40,50}*.md`，按此口径 `12493ca` **不在**结果内。
- ⇒ 标题的"5 笔"按 L0 口径**正确** ✓，但表体多出的一行与标题口径不符；该行内容已如实标注，属**标签/放置**问题。
- **建议**：把该行移出 (a)（或标题写"5 笔 L0 + 1 笔非 L0（列示见下）"）。

### M-05 [LOW] 口径与残留累积（第 4 次同型）

- 报告 §「Git」称「untracked 10 个既有条目原样未动 ✓」：默认 `porcelain` = 10 条目 ✓；`--untracked-files=all` = **13 文件**（CONTRACTS 9 + GOVERNANCE 4）。方向性结论成立 ✓。
- 残留累积：`90 §1:41`「L1 … 暂无（`67` 是候选，NOT RELEASED）」与 `Status.md:2624`「（当前为空）」——现已对 **2 条正式 L1**（CR-003 / CR-004）stale。该残留已在上一轮 §13.a 披露并以 `OWNER-DECISIONS:351` 为不改理由 ✓；此处仅记录**累积**（若继续新增 L1，`90 §1` 与 `Status.md` 的可读性缺口会扩大）。

---

## 4. 报告自述 vs 实测（逐条）

| # | 报告自述 | 实测 | 判定 |
|---|---|---|---|
| 1 | CR-003 / CA-003 / 10·20 §12 / re-freeze 链（`b3eeb3e9`→`442172f4`→`8659e2fa`） | 三值全部可复算一致；`current = 2edd2010` = `fbec14e:Docs/V3_SPEC` ✓ | **TRUE** |
| 2 | 「语义句相对 71f51f9 删除行 = 0」 | `71f51f9..HEAD` 对 `10`/`20` 全为 insertions（0 deletion）✓ | **TRUE** |
| 3 | 「未创建 CR-004 之外的任何 OD-R-01 重复记录」 | `CR-003bis` / `OD-R-01-v2` / `final-final` / `CR-005` = **0 命中** ✓ | **TRUE** |
| 4 | f708370 命题「可证」+ 4 类既有记录引用 | 逐条实测成立（见 §2.3）✓ | **TRUE** |
| 5 | 「具名 instrument 在 Docs/ 内无同名正式记录 = UNKNOWN」 | CR-004 §2.3 如实登记，且**未升格、未追认** ✓ | **TRUE** |
| 6 | CR-004 = §14 情况 B；classification 主导 CHANGE-3 | 分类论证与 `90 §3` 一致（规定值改变 = 行为改变；含新增禁令 ⇒ 非 CHANGE-1；未放宽/删除 ⇒ 非 4/5；四道门不适用 = `90 §3:414`）✓ | **TRUE**（判据坐标本身不可解析 → M-01） |
| 7 | 「implementation files = ir.py（+2/−2）」 | 属 **f708370 时点**的既有改动；本轮两个 commit **未触碰任何 backend 文件** ✓ | **TRUE** |
| 8 | 「test evidence = …；137/197 passed 为 DOCUMENT CLAIM，未重跑」 | CR-004 §6 明确标注证据等级与"不得误读" ✓ | **TRUE** |
| 9 | 20 §12 有补记条目（补记 f708370 · 事件 2026-09-21） | `:810-833` 存在；登记日/事件日分列 ✓；依据 `README:138`「变更记录统一追加到分册尾部，禁止覆盖历史」逐字命中 ✓ | **TRUE** |
| 10 | CA-004 = 90 §11 表行 + 详情（含独立 re-freeze reference） | `:231` 表行 + `:389-442` 详情 ✓ | **TRUE** |
| 11 | R-01 修正：撤回完备性断言，改为逐笔枚举 + 逐笔处置 | `:443-484` 结构完整；枚举与实测吻合 ✓ | **TRUE**（标签小瑕 → M-04） |
| 12 | R-02：未新建机制，仅记录静态检查要求 | 无 CI/脚本/代码改动 ✓；但该条本身是新增强制要求 → 见 M-02 | **PARTIAL** |
| 13 | R-03：复用既有 ratification 机制落最小仓内 provenance | `OWNER-DECISIONS:671-691` 新增块 ✓；**如实标注原始载体为仓外 Owner 指令** ✓；未修改 R3 ratification 的 5 项范围 ✓ | **TRUE** |
| 14 | R-04：CR-003 §7 明记 NOT VERIFIED | `CR-003:210-224` 新增子块 + 「不得误读」注 ✓ | **TRUE** |
| 15 | R-05：`90 §2 R8` → `90 §4` 引文更正 | CR-003 `:295-298` 与 G-02 `:132-135` 均已更正，且加注"两条规则不同，不得互相代引" ✓（`git grep Reconcile` 仍仅 `90 §4:440` ✓） | **TRUE** |
| 16 | R-06：LIMITED-AUTH 加最小 scope clarification | `:317-323` 已改 ✓ 未改授权范围 ✓ | **TRUE**（instrument 正文变更 → M-03） |
| 17 | `§23`：无未登记 L0 修改 / 无虚假"全部已审计" / 无新业务 Decision / 未扩大 OD-R-01 / 无 schema·migration·production redesign | 五项逐条实测成立 ✓（第 5 项：无 schema/migration 文件改动 ✓） | **TRUE** |
| 18 | push 成功；untracked 10 原样未动 | 本地 remote-tracking = `fbec14e` ✓；远端独立复核受凭据阻断（§5 U-2）；untracked 口径 → M-05 | **PARTIAL** |

---

## 5. 无法核验项（UNKNOWN）

```text
U-1  任务书 §11 / §14 / §22 / §10A / §10C / §15 / §23 的**原文**（不在仓库内）。
     ⇒ 本次审查**无法独立核验**「§14 情况 B/C 的判据」「§22 STOP-1 是否命中」
        —— 这是 M-01 的直接后果，而非笔误。（参考：仓库内含 §1–§12 的 90/91 是 L0-META，
        与任务书 §x 编号体系无关，不可互相解析。）
U-2  远端独立复核：git ls-remote 受凭据策略阻断（schannel SEC_E_NO_CREDENTIALS）；
     本地 remote-tracking ref = fbec14e，与报告一致，未从远端独立证实。
U-3  「Owner D1」/「2026-09-20 Concept Correction」的**原始载体**是否存在于仓外治理面
     （AITutorX / 会话记录）—— 仓内确认为 0 命中，与 CR-004 §2.3 的 UNKNOWN 判定一致 ✓。
```

---

## 6. 对报告末尾"安全阀"问题的 DSH 意见（供 Owner 裁决，非 DSH 决定）

**问**：具名 instrument（「Owner D1」/「2026-09-20 Concept Correction」）缺失，是否应触发 §22 STOP-1？

**DSH 可验证的事实**（不涉及 STOP-1 原文）：

```text
命题 = 「standalone_question / composite_question 不得作为 canonical V3 Unit Type」
支撑 = L0 自身：
        · README §2.2「术语裁决（权威）」⟶ standalone_unit 是裁决术语，standalone_question 是 V2 曾用
        · 00:10 / 10:14 / 20:13 三分册均声明「术语裁决以 README §2 为准」
        · 10 §5.2:290 / §6.5:516 的 unit_type 为闭集，不含 standalone_question
⇒ 该命题的**权威在 L0**，不在某个具名 Owner instrument。
⇒ f708370 的 L0 文本修改，在**内容**上是把 20 对齐到 L0 既有 canonical 术语；
  其缺的是**流程**（L1），而 CR-004 正是补该 L1。
⇒ 「Owner D1 / 2026-09-20」是**归属标签**问题（label），非权威缺失；
   CR-004 §2.3 已如实记为 UNKNOWN、且明确未升格、未追认 ✓ —— 处理方式正确。
```

**DSH 意见**：就仓内可得证据而言，**不构成"权威不可确定"**；若 STOP-1 的判据是"授权/权威无法确定"，则该条件**不成立**（因此不必撤回 CR-004）。若 STOP-1 的判据严于"任何具名 instrument 无法解析即 STOP"，则属 Owner 的判断范围——此时 CR-004 可整体撤回且不回滚 f708370 ✓（该安全阀设计合理）。

> 无论哪种读法，**M-01 都建议先补**：把任务书坐标的判据摘要写入 CR-004，否则该判断在未来不可复核。

---

## 7. 应予记分之处

```text
+ 上一轮唯一 HIGH（R-01）实质修好：撤回完备性断言 + 逐笔枚举；DSH 独立复算的 20 笔全集与其枚举**逐笔吻合**
+ 15 笔 historical-exempt 的 ID 与日期**全部准确**（含"均早于 90 建立 c5a899f"这一可证条件）
+ CR-004 权威论证逐条引文实测成立 —— 与上一轮"过度推论"形成鲜明对照（同一 agent，方法已纠正）
+ 四者严格分列（4.A/4.B/4.C/4.D）+ 明确"不得混为一个架构事实"
+ 证据等级诚实标注：implementation consequence / verification evidence / DOCUMENT CLAIM /
  实现层回归 NOT VERIFIED（含「不得误读」注，防止 G 项被读成 pass）
+ 具名 instrument 缺口如实记为 UNKNOWN，**不升格、不追认**，并给出可撤回安全阀
+ 两条 change 独立 provenance、独立 re-freeze 链，**未并入** CR-003（与任务书 §15 一致）
+ `b3eeb3e9…` 同值现象主动解释为「非笔误」并给出一致性依据（= §5 last content commit）
+ 未触碰 production code / schema / migration；无 rewrite / force push；无重复记录；无机制新建
+ R-03 的 provenance 落点**如实披露原始载体在仓外**，未伪装成仓内历史授权（未重犯 D1:392 型错误）
```

---

## 8. 附：机械验证命令（可复现）

```powershell
$repo='D:\Project\AITutors-v3'

# L0 全集与枚举（R-01 核验）
git -C $repo log --format='%h|%ad|%s' --date=short -- Docs/V3_SPEC/00_Master_Spec.md `
  Docs/V3_SPEC/10_Data_Model.md Docs/V3_SPEC/20_Document_Pipeline.md `
  Docs/V3_SPEC/30_Task_LLM_Safety.md Docs/V3_SPEC/40_Development_Rules.md Docs/V3_SPEC/50_Migration_Assets.md
git -C $repo log --format='%h' '0dd954d..HEAD' -- <同上>
git -C $repo log --format='%h' '0dd954d^'    -- <同上>     # 应 = 15

# tree 链（CR-004 §8 / G-02 §6.2 核验）
git -C $repo rev-parse 'f708370^:Docs/V3_SPEC' 'f708370:Docs/V3_SPEC' '71f51f9:Docs/V3_SPEC' `
  '60fa9ff:Docs/V3_SPEC' '12493ca:Docs/V3_SPEC' 'fbec14e:Docs/V3_SPEC'

# 红线：本轮是否触碰生产代码
git -C $repo diff --name-only 60fa9ff HEAD | Where-Object { $_ -like 'backend/*' -or $_ -notlike '*.md' }

# M-01：task-book 坐标是否可解析
git -C $repo grep -l -I -e '情况 B' -e 'STOP-1' -- Docs/          # 应仅 CR-004 自身
git -C $repo grep -n -I 'Reconcile' -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md   # 应仅 :440

git -C $repo ls-remote origin od01-r3-convergence                  # U-2：需凭据，本环境受阻
```

---

*DSH 独立对抗性审查（第三轮）· 对 git 对象与仓内文本取证 · 审查期间未修改任何文件、未 push · 全部结论均可由 §8 命令复现。*
