# OD-R-01 闭合记录语义边界补丁（H-18～H-21，`81dc221`）— DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Closure Record 语义边界补丁 — H-18 ~ H-21 完成报告」（STATUS: COMPLETE）及其产物 `Docs/60_REPORTS/OD-R-01-CLOSURE-RECORD.md`（补丁后 301 行） |
| 被审 commit | `81dc22192559fc0338b72b21d90e2353fb33bb10`（parent `7d4147b` = DSH 第 8 轮报告；1 file changed, +114/−17） |
| 所在仓 | `D:\Project\AITutor-X` @ `main`（DSH 报告仓）——审查期间**未修改**该产物；未修改 `AITutors-v3` 任何文件 |
| 被审仓（治理主体） | `D:\Project\AITutors-v3` @ `od01-r3-convergence`：本轮 **0 改动** ✓（本地/远程 HEAD 均 `d2b9a26`，tracked 干净） |
| 证据分级 | DIRECTLY VERIFIED > VERIFIED BY INSPECTION > DOCUMENT CLAIM > UNKNOWN |
| 关联 | 被修对象 = DSH 第 8 轮 findings H-18（MED）/ H-19 / H-20 / H-21（LOW） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（H-18 / H-19 / H-20 / H-21(a) / H-21(b) 五项**全部实质修复**，逐条实测可证；
 本轮新增 1 项 LOW（补丁自身的内部引文失配）；另：DSH 更正自身第 8 轮的一处判据错误）
```

**一句话结论**：H-18 的修法**超出了 DSH 的要求**——不仅加了命名边界，还新建 §4.1 把「六项不因本记录而发生」逐条落到可核验的仓内条款（Phase 6 未进入 / STOP 未解除 / P1 Segment A 仍 STOP / OD-01 re-freeze 未满足 / §8 不豁免 / §9–§6 未放宽），并在 Document control 增设 `V3 Authorized Phase = UNCHANGED`、`STOP / P1 Segment A / OD-01 re-freeze = 均未解除` 两行。这是把一处"缺一句话"补成了**结构化的边界对账**。

本轮唯一新 finding 是补丁自身的一处**内部引文失配**（LOW）：§3.3 仍引用 §1 里已被 H-21(b) 改写掉的旧措辞——而该补丁的自我要求恰恰是"闭合记录不能留下不可解析/不实的引用"。

**另须记明**：被审报告对我方第 8 轮判据做了三处**引用更正**，经 DSH 逐条回仓复核，**全部正确**——其中一处是 DSH 自己的错误（STOP Conditions 实为 **A–J**，第 8 轮误写 A–G）。见 §2。

---

## 2. DSH 自我更正（第 2 次）：STOP 条目计数与载体归属

被审方在「引用更正」段提出三处更正。DSH 回仓复核结果如下：

| 被审方主张 | DSH 实测 | 判定 |
|---|---|---|
| STOP 条件实为 **A–J（10 条）**，非 A–G | `LIMIT-AUTH:264-273` 逐条为 A…J（A Frozen Spec 冲突 … J 需要自行解释 Contract 未定义的语义）✓ | **被审方正确，DSH 第 8 轮「A–G」有误** —— 第 8 轮 DSH 只读到 `:270`（G）即截止，未读全 |
| `§3.5`/`§5`/`§8` 的载体是 **LIMIT-AUTH**（`:176`/`:262`/`:310`），不是 CR-003（CR-003 的 §3.5 = Change Classification、§5 = Scope、§8 = Procedural Remediation，均不含 STOP） | 实测：`LIMIT-AUTH:176` = Schema Change Boundary — OD-05（硬性 STOP）· `:262` = §5 STOP Conditions · `:310` = §8 Phase Evidence Requirement；CR-003 对应小节确不含 STOP ✓ | **被审方正确**。DSH 第 8 轮报告**证据块**已写对载体（`LIMIT-AUTH §3.5（:176）` 等），但**裁决清单 D1** 写作「CR-003 §7 P1 Segment A STOP 与 `§3.5` 硬性 STOP、`§5` STOP Conditions…」，`§3.5`/`§5` 未重复前缀 ⇒ **DSH 的简写歧义很可能是该误归属的来源**，DSH 认领 |
| 「P1 Segment A STOP」在 `CR-003 §7:228` | 实测 `CR-003:228`：「为什么不跑：P1 Segment A 实施仍处 STOP」✓ | **被审方正确**（DSH 第 8 轮报告此处写对） |

**DSH 结论**：三处更正**全部接受**；第 8 轮关于 H-18 的**实质判断**（缺阶段对账与 STOP 边界）不受影响——它依据的是 `LIMIT-AUTH §4` Phase 0–6、`§3.5` 硬性 STOP、`CR-003:228`，这些均经复核成立 ✓。**被审方"按仓内实测写引用、不照抄裁决文本"的做法应予肯定**：这是第 6 轮 H-11「核验以精确 identity 为准」精神在**引用**层面的延伸。

---

## 3. 已独立复核的关键事实（DIRECTLY VERIFIED）

```text
commit 81dc221… ✓  parent = 7d4147b… ✓  parent-is-ancestor = yes ⇒ fast-forward（无 amend / 无改写）✓
1 file changed, +114/−17 ✓  name-only = Docs/60_REPORTS/OD-R-01-CLOSURE-RECORD.md（唯一）✓
HEAD = origin/main = 81dc221… ✓（git ls-remote 核验）
AITutor-X tracked 改动 0（工作区干净）✓
AITutors-v3：本地 HEAD = 远程 od01-r3-convergence = d2b9a26… ✓  origin/main = 7934844…（未动）✓

补丁自述的机械自检，逐条复现：
  FROZEN 出现处（case-sensitive）→ 仅 :43（同词异义限定中的正确否定）与 :73（E2 文件名）✓ 与其所载一致
  `71f51f97e5674cf04ab12d4c449e3796a160bb27` 计数 = 1（C0 行）✓
  markdown 表格：8 张表、列数不一致行 = 0 ✓（DSH 独立重算一致）
  命名边界实测：`git grep -E 'Verification Phase|Audit Phase' -- Docs/` = 0 命中 ✓（见 H-22(b) 的口径说明）
Document control 新增 `Revisions` 行 ✓（:301，声明向前追加、E1–E7/C0–C8 与历史 hash 未动）

补丁正文所引仓内条款，逐条回仓核验（全部成立）：
  LIMIT-AUTH §4:242-258（Phase 0–6，Phase 6 = End-to-End Verification；Phase 0 [COMPLETE]）✓
  LIMIT-AUTH §5:264-273（STOP A–J）✓   §3.5:176（硬性 STOP）✓   §6:279-298（Forbidden Scope，含
  「Phase 1 preprocessing implementation（在 OD-01 re-freeze 前）」:281）✓   §8:310-325（10 项必报）✓
  §9:329-340（AUTHORIZED — LIMITED SCOPE）✓
  CR-003 §7:228（P1 Segment A 实施仍处 STOP）✓
  OWNER-DECISIONS…md:423 OD-01-J = **PENDING** ✓
  §4.1 第 6 条列举的 Forbidden Scope 子集（V3 production code / Gate·Admission / DB migration /
  Frozen Schema / historical corpus rerun / X3 entry）逐条见于 §6 ✓（其措辞为"含"，列子集成立）
```

---

## 4. H-18～H-21 闭合核验（逐条实测）

| 上轮 finding | 补丁落位（实测） | 判定 |
|---|---|---|
| **H-18 [MED]** 阶段声明未与已授权阶段模型 / STOP 对账 | ① §4 标题改「Phase Transition（**治理进程阶段**）」，正文改述为 `Governance process phase`，表头改「Governance process phase」（:167-180）；② :182-185 命名边界面（治理进程命名 ≠ `LIMIT-AUTH §4` Phase 0–6；不得混用、不得互相换算；附实测依据）；③ **新增 §4.1（:196-239）**：阶段关系图 + **六条「不因本记录而发生」**（① Phase 6 未进入且 Phase 1/2/3/5 亦未启动、Phase 0 的 `[COMPLETE]` 系既有标注非本记录判定；② STOP 未解除（**A–J 共 10 条** + §3.5 硬性 STOP + 「STOP 后不得『先实现再说』」）；③ P1 Segment A 仍 STOP（引 `CR-003 §7:228` 原文）；④ OD-01 re-freeze 未满足；⑤ §8 Phase Evidence Requirement 不豁免（10 项必报 + 禁四类软措辞）；⑥ §9/§6 授权面未放宽）；④ §3.1 第 4 点（:145-148）补限定并指向 §4 命名边界；⑤ Document control 增两行（`V3 Authorized Phase = UNCHANGED — Phase 6 NOT entered`、`STOP / P1 Segment A / OD-01 re-freeze = 均未解除`） | **FIXED**（超出要求的完成度） |
| **H-19 [LOW]** `§3.8` 条件未澄清 | 新增 §5.1「**OD-01 ≠ OD-R-01**」（:256-273）：引 `§3.8:216`/`:218` 原文 + Owner 给定英文句 + 明写两条 change 不同、OD-01 Proposal 仍未 re-freeze（引 `G-02 §6` 对该半句的判定 + `OWNER-DECISIONS:423` OD-01-J = PENDING）+ 「不得因 OD-R-01 CLOSED 推定 §3.8 条件已满足」+ 引 `§4` 末句与 `§6` 的 Phase 1 限制继续有效 | **FIXED** |
| **H-20 [LOW]** 索引缺 `71f51f9` | 证据索引新增 **C0** = `71f51f97e5674cf04ab12d4c449e3796a160bb27`，标注「OD-R-01 L0 源改动」（含 subject 与日期）+ 权威登记字段 = `CR-003 §1 Source Commit`；并注明登记事实早已存在于 `CR-003 §1` / `90 §11 CA-003` / `84:134` / `G-02 §6.2`、本次仅补索引完整性、**不**新增登记义务；「跨仓边界」句的 `C1–C8` 同步为 `C0–C8`（:114） | **FIXED** |
| **H-21(a) [LOW]** 局部标签 vs「不建映射表」声明 | :94-103 新增「局部引用标签声明」：写入 Owner 给定英文句 + 说明 `E1–E7`/`C0–C8` 仅为**本记录内部**局部引用标签、**不是**治理编号、**不**承载权威、**不**构成 registry 或跨仓编号映射表；每个标签均附完整 SHA；权威编号仍以 `CR-00x`/`CA-00x`/`OD-*` 为准 | **FIXED** |
| **H-21(b) [LOW]** `FROZEN` 同词异义 | §1 表项改为「历史审计证据基线 **immutable / append-only**（描述性措辞，**非** governance state）」（:29）+ 英文正文（:34-35）+ :42-44 同词异义限定（**不是** `LIMIT-AUTH §9` 的 `Contract v0.3: FROZEN`、**不是** Frozen Spec 冻结状态、**不**构成 governance state 值、**不**新增状态体系）；实测全文已**无**任何 `FROZEN` 状态词误用（case-sensitive 仅 :43 否定句 + :73 文件名）✓ | **FIXED** |

**任务书/Patch 未覆盖项（按裁决保持不动，实测确认未被动过）**：H-14～H-17 仍为 accepted residual（§3.1 原样）✓；H-02/H-03/H-04 处置未变（§3.2 原样）✓；INFO-1/INFO-2/INFO-3/INFO-4 未处理 ✓（其中 INFO-2「不在 AITutors-v3 留 closure pointer」的理由——避免反向制造 AITutorX ↔ AITutors-v3 coupling——**与 DSH 第 8 轮的判断方向一致**，DSH 认可该取舍）。

---

## 5. Findings

### H-22 [LOW] 补丁自身的两处引用/检索精确性残留

**(a) 内部引文失配（§3.3 引用了已被本补丁改写掉的 §1 旧措辞）**

`OD-R-01-CLOSURE-RECORD.md:162`：

> 适用面同 §1「**审计证据基线已冻结**」。

但 H-21(b) 已把 §1 的措辞改为「**历史审计证据基线不可改写**」（`:32`）与「**immutable / append-only**（描述性措辞，非 governance state）」（`:29`）。实测全文 `已冻结` **仅命中 `:162` 一处** ⇒ 这处**带引号的内部回指已指向一个不存在的短语**。

**为何值得记**：本补丁的**自我要求**正是「闭合记录本身不能留下不可解析/不实的引用」（被审报告「引用更正」段原话）——它修正了三处**外部**引用，却在**内部**引入了一处失配。**修法（1 行）**：把 `:162` 改为「适用面同 §1「历史审计证据基线不可改写 / immutable / append-only」的声明」。

**(b) 命名边界的「0 命中」未限定检索范围**

`:185` 写「实测：`Audit Phase` / `Verification Phase` 两个标签在 `AITutors-v3` 内 **0 命中**（`git grep` 于 `Docs/`）」。括注已限定 `Docs/`，但主句的「在 AITutors-v3 内」是**全仓**表述；实测全仓检索会命中三处**无关**历史标题：

```text
Status.md:3065 · log.md:2567 · restart-prompt.md:263 —— 「Residual Audit Phase-2（A-11）」2026-09-13 DG 条目
```

（该标题指 2026-09-13 的 DG 残余审计轮次，与本记录所指阶段命名无关——故**不**影响 §4 结论。）**建议**：把主句收紧为「在 `AITutors-v3/Docs/` 内 0 命中」，或补一句「仓库根 `Status.md`/`log.md`/`restart-prompt.md` 另有 2026-09-13「Residual Audit Phase-2」历史标题，与阶段模型无关」。

**严重度**：LOW。二者均为一行级措辞修正，不触及授权、边界结论或任何治理效力。

---

### 观察（非缺陷）

```text
OBS-1  被审报告末句「后续不再接受『再发现一个 LOW 就再审一轮』的循环」属**实施代理对审查节奏的意向声明**。
       审查范围与节奏由 Owner 决定，DSH 不作争辩；就本次而言，DSH **没有**任何 outstanding 阻断项，
       故该意向与「重心转入集成与端到端验证准备」并不冲突。
OBS-2  记录正文写的是阶段关系图「Governance verification / integration preparation ← **本记录所在处**」
       （:209），**未**写「可以开始」——即**记录本身**没有作出许可声明，符合其 §5「记录，不是授权」✓。
       （被审**报告**的文字用了「可以开始」，未进入记录 ✓ 建议保持此纪律：若该措辞日后进入记录正文，
       须同样附 §5 的 record ≠ authorization 限定。）
OBS-3  「integration preparation」的**准备 / 执行**边界未在记录内定义。已由 §4.1 第 5 条兜住
       （「Verification Phase 的任何**执行**须遵守 §8 并另获相应授权」）⇒ 不构成缺陷；若 Owner 认为必要，
       可加半句「准备性活动（计划 / 环境 / 用例设计）不构成 §4 任何 Phase 的启动」。
OBS-4  INFO-1（F/R/M 三条早期 finding 链未在 §2 闭合表内映射）与 INFO-2（不在 AITutors-v3 留 closure
       pointer）按裁决不处理 ✓；DSH 对该两处取舍无异议。
```

---

## 6. 记分

1. **H-18 修法超出要求**：从"补一句话"做成 §4.1 六条**可核验**的边界对账 + Document control 两行阶段/STOP 状态，且每条都指向仓内条款（含行号）——这是把 DSH 的缺失项补成了结构性防线。
2. **引用以仓内实测为准，不照抄裁决文本**：被审方发现裁决文本把 `§3.5`/`§5`/`§8` 归到 CR-003、把 STOP 写成 A–G、把 P1 STOP 的落点搞混，**逐条回仓核验后改写**，并显式披露三处差异及理由。**这纠正了 DSH 自身的一处判据错误**（A–G → A–J）。
3. **记录自身未越权**：正文用「本记录所在处」而非「可以开始」；§5「记录，不是授权」保持不变 ✓。
4. **H-21(b) 选择"不造新状态词"**：改用描述性 `immutable / append-only` 并加同词异义限定，未新增 governance state ✓——与 `91 §3.1` 状态集合无冲突。
5. **机械自检可信**：其自述的四项检查（FROZEN 出现处 / C0 计数 / 8 张表列数 / 命名 0 命中）DSH 独立复现，**结果一致**（唯 (b) 的范围口径见 H-22(b)）。
6. **边界与历史纪律**：唯一改动文件；AITutors-v3 本地与远程均 0 改动；fast-forward、无 amend / force push；新增 `Revisions` 行声明"向前追加修订、历史证据未动"——与其 §1/§3.3 的不可改写条款自洽 ✓。

---

## 7. Owner 裁决清单

```text
OD-R-01-PATCH-D1  【LOW】H-22(a)：修正 §3.3:162 的内部引文（「审计证据基线已冻结」→ §1 现行
                 「历史审计证据基线不可改写 / immutable / append-only」）
OD-R-01-PATCH-D2  【LOW】H-22(b)：把 §4 命名边界的「0 命中」限定为 `AITutors-v3/Docs/`，或补一句说明
                 Status.md / log.md / restart-prompt.md 的「Residual Audit Phase-2」历史标题无关
OD-R-01-PATCH-D3  【OBS】OBS-1~OBS-4：审查节奏、preparation 边界、INFO 取舍 —— 由 Owner 定；
                 DSH 无阻断项，亦无新增 MED/HIGH
OD-R-01-PATCH-D4  【闭合效力】DSH 立场：H-18 / H-19 / H-20 / H-21(a) / H-21(b) **五项全部 FIXED**（逐条实测）；
                 §4.1 六条边界与 Document control 两行状态与仓内条款**逐条一致**；
                 OD-R-01 = CLOSED 未被重开 ✓（E1–E7 / C0–C8、历史 hash、tree 取值均未改动 ✓）；
                 H-22 为一行级内部引文/检索口径残留，**不阻断**任何结论
```

**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 8. 未验证 / UNKNOWN

```text
UNKNOWN  仓外任务书 / 裁决文本原文（含 Owner 给定的三句英文与「裁决文本所引 CR-003 §3.5…」的原始措辞）
         —— 不在仓内；DSH 只核验被审方**按仓内实测改写后**的引用是否与仓内事实一致（结论：一致）
UNKNOWN  「不再接受再审循环」「重心转入集成准备」是否为 Owner 已下达的指令
         —— 属仓外指令面；DSH 只记录为 OBS-1
INFO     AITutor-X untracked 18 项为本任务前既存（未纳入）✓；AITutors-v3 本地 main 仍领先 origin/main 12 commit（既存）
```

---

**Document control**

| Field | Value |
|---|---|
| Path | `Docs/60_REPORTS/OD-R-01-CLOSURE-RECORD-PATCH-H18-H21-DSH-ADVERSARIAL-REVIEW.md` |
| Status | FINAL |
| Reviewed commit | `81dc22192559fc0338b72b21d90e2353fb33bb10`（`kurt-wong/AITutorX` @ `main`） |
| Round | OD-R-01 对抗性审查第 9 轮 |
| Verdict | ACCEPTED WITH FINDINGS（H-18～H-21 全部 FIXED；H-22 LOW ×2 + 4 OBS；DSH 自我更正 1 处） |
| Repo of subject | `kurt-wong/AITutorX`（治理主体 `AITutors-v3` 本轮 0 改动） |
| This report repo | `D:\Project\AITutor-X`（DSH 侧；未修改被审记录，未修改 `AITutors-v3` 任何文件） |
