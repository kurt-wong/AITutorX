# OD-R-01 Final Hygiene Closure (M-01～M-05) — DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Final Hygiene Closure」（RESULT: COMPLETE） |
| 仓库 | `D:\Project\AITutors-v3` |
| 分支 | `od01-r3-convergence` |
| 被审 commit | `5a46d331d2a019bcc6a2f542fdda330cdbd0c438`（parent `fbec14e`） |
| 审查基线 | HEAD = `5a46d33`（tracked 改动 0） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间未修改任何文件、未 push |
| 关联 | 上一轮：`AITutor-X/Docs/60_REPORTS/OD-R-01-FINAL-CLOSURE-F708370-DSH-ADVERSARIAL-REVIEW.md`（`12a1067`） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（M-01 ~ M-05 五项**全部正确闭合**；本轮因 M-05.2 的事实同步产生 1 项新的 MED 陈旧引用）
```

**一句话结论**：五项修法**逐条对得上上一轮 findings**，且两处最需要诚实的地方（M-01 的可复核性边界、M-03 的"合成状态"表述）写得**准确、不越界**——没有把仓外任务书升格为仓内权威，也没有伪造"当前正文 == Owner 批准原文"。

唯一实质问题：**M-05.2 改了 `90 §1:41`，却使 `CR-003 §0.1:51` 对同一行的引用变成假引用**（且 `:49-50` 的文件清单也已过期）——即本轮所要消除的"stale current-state assertion"被**自己制造了一处**。该行位于 **ACTIVE L1** 记录内，属真实缺陷但**不阻断**（不影响授权、分类、re-freeze 链）。

---

## 2. 已独立复核的关键事实

```text
HEAD = 5a46d33… ✓  branch = od01-r3-convergence ✓  origin/od01-r3-convergence = 5a46d33… ✓
parent = fbec14e… ✓   main = 6d8a3bd（未动）✓   origin/main = 7934844（未动）✓
5 files changed, 124 insertions(+), 9 deletions(-) —— 非 .md = 0 · backend/* = 0 · L0 00–50 = 0 ✓
f708370 可达 ✓   71f51f9 可达 ✓（无 rewrite / force push）
untracked：默认 porcelain = 10 · -uall = 13 ✓（与报告两口径一致）

Docs/V3_SPEC tree：
  fbec14e = 2edd20101c4abf3238d5689b3bb3cba0d5fc75fe
  5a46d33 = 63810f55c88cee983004136f288f1b6ff3527a8d   （= HEAD:Docs/V3_SPEC）
  ⇒ 与 G-02 §6.2 登记的 CURRENT 字面值一致 ✓，且由 git 计算（非手填）✓

90 本轮改动范围（hunk 头）：@@ -38（§1 表 L1 行 + 注）、@@ -450（§11 (a) 标题 + 口径注）、
  @@ -483（§11 (c) 授权落点澄清 + (c) 声明登记表）⇒ **§2–§10 逐条未动** ✓
```

---

## 3. 五项 findings 的闭合核验（逐条）

| 上轮 finding | 本轮修法（实测） | 判定 |
|---|---|---|
| **M-01** CR-004 引用仓内不可解析的 task-book 坐标 | §2 标题下 1 行指引（`:71-72`）+ 新增 §2.4（`:111-139`）：① 两类权威**严格分列**表（仓内权威 = L0 README §2.2 / `10 §5.2:290`·`§6.5:516` / L0-META 90·91「仓内可解析=是」；仓外任务授权载体「仓内可解析=否」，并明写"不是业务语义来源、不是 Frozen Spec、不得与 README/Frozen Spec 并列"）；② **7 个坐标**（`§11/§14`·`§22 STOP-1`·`§22 STOP-8`·`§10A`·`§10C`·`§15`·`§5`）逐条记「作用」+「本记录做了什么动作」；③ **可复核性边界如实**：「本表**只**使『本记录在该坐标下做了什么判断』可自证；判据原文不在仓内，本表**不承担**使其可自证」；④ 未搬入 task-book 原文、未重新定义 STOP-1、未新增权威层；⑤ 声明本属头部 `May Change`，不改 §3–§8 结论 | **CLOSED** |
| **M-02** `90 §11 (c)` 新增要求 vs「登记」性质 | `:493-514` 新增「授权落点澄清」三行表：把「既有登记义务（`90 §11` 首句，本次未改）」与「**本次新增**的审计完整性措辞（**不是**上一行的复述）」**严格分列**，并给出新增要求的授权落点 = 仓外任务授权载体；第三行明写"新增治理机制 / 审批层 / 治理状态 / registry = **无**"；附声明确认不把任务书升格为仓内权威、不改 `90` 任何治理规则文本、不重新设计 Change Audit 机制 | **CLOSED** |
| **M-03** OWNER APPROVED instrument 被代理编辑 | LIMIT-AUTH 头部后新增 Ratification / Provenance 注记（`:16-46`）：① 原始 approval = **仓外**，仓内对应登记 = G-01，且明写「**G-01 是入 Git 登记，不是内容批准的原始载体，两者不得混同**」；② 逐条列出五项未变（未扩大授权范围 / 未放宽 forbidden scope / 未改 Authority Order / 未改 STOP condition / 未改 phase order·terminology 限制）；③ 明写「**不主张『当前正文 == Owner 批准时的原始文本』**」+「现行正文 = 原始批准文本 + 后续仅收窄解释范围的修正 的**合成状态**」+ 头部 `STATUS: OWNER APPROVED` 语义不被重新签发；④ 复用既有 current-ratification 模式 + G-01，**未新建** approval 机制 / registry | **CLOSED**（小瑕见 H-03） |
| **M-04** `(a)` 标题计数与表体不一致 | 标题改为「完整枚举（**L0 = 5 笔**；表内另列 **1 笔非 L0，共 6 行**）」+ 新增口径注（逐项点名 5 笔 L0 与 1 笔非 L0 `12493ca`），并明写"两个口径**不得混用**"「今后凡非 L0 的 `Docs/V3_SPEC` 改动一律在 (c) 声明，不再计入 (a)」；未删 `12493ca`、未改 audit scope | **CLOSED** |
| **M-05.1** untracked 口径 | G-02 新增 §6.1a：两口径对照表（默认 `porcelain` = **10**（目录折叠，`Docs/GOVERNANCE/` 计 1）vs `-uall` = **13**）+ **拆分明细准确**（9 × `CONTRACTS/PREPROCESSING-V3-*.md` + 4 × `GOVERNANCE/*.md` —— DSH 独立计数一致 ✓）+ 要求"必须写明口径、不得只写裸数字"+ 历史未标口径数字按默认口径理解、按 `90 §4` 不机械改写 | **CLOSED** |
| **M-05.2** L1 stale assertion | `90 §1:41` 例子列 `暂无（67 是候选…）` → `CR-003 · CR-004（2026-09-24 起 EFFECTIVE）；67 仍为候选、NOT RELEASED`，并附 `:47-49` 事实同步注（只改例子列、权限/禁止逐字未变 —— DSH 实测 ✓）；`Status.md:2624` `（当前为空）` → `（现有 CR-003 / CR-004 两条）` + `:2633` 同型注 | **CLOSED（但产生新 stale 引用 → H-01）** |

**附带项（G-02 §6.2）**：WS-B 行由悬空 `<本登记所在 commit>` 落为实值 `fbec14e`（值不变）✓；新增「最终卫生收口 M-01~M-05 = current」行 ✓；`CURRENT Frozen Spec tree` 更新为 `63810f55…`（= HEAD ✓）并写明覆盖范围与"未触及 L0 00–50" ✓。属既有 §6.2 登记义务 ✓ **正确**。

**上一轮 (c) 规则的自执行**：`90 §11:508-514` 存在「（c）声明登记」表，登记本 commit 为「**L0-META / L1 面改动，非 L0 修改**」并给出机械取值命令 `git log -1 --format=%H -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` ✓ —— **上一轮新增的 (c) 规则被正确执行，规则自洽** ✓（这是本轮最值得记分的一处）。

---

## 4. Findings

### H-01 [MED] M-05.2 的事实同步**自伤** Active L1 内的一处现行断言

```text
事实链：
  本 commit 之前：90 §1:41 例 = 「暂无（67 是候选，NOT RELEASED）」
                  ⇒ CR-003 §0.1:51「`90 §1:41` 自述「L1 … 暂无」」**当时为真**
  本 commit 之后：90 §1:41 例 = 「CR-003 · CR-004（2026-09-24 起 EFFECTIVE）；67 仍为候选、NOT RELEASED」
                  ⇒ CR-003:51 所引文本**已不存在** ⇒ 该引用成为**假引用**

全仓检索 `§1:41`：命中 = **仅 CR-003:51**（即唯一的 stale 引用，且位于 ACTIVE L1 记录内）

同时过期：
  CR-003 §0.1:49-50「`Docs/V3_SPEC/` 现存仅 `README.md` + `00/10/20/30/40/50/90/91`，
                      `Document Type` 均为 Frozen Spec / Governance Meta-Spec，**无** `Contract Change Record`」
  ⇒ 现 `Docs/V3_SPEC/` 内实际存在 `CR-003_…md` / `CR-004_…md`，两者 `Document Type: Contract Change Record`
```

**为何是 finding（而非小瑕）**

1. 属**本轮自己制造的**同类缺陷：本 commit 的既定目标是消除 stale current-state assertion（M-05.2 与附带项均以此为理由），却在改动 `90 §1:41` 时未同步检查**引用该行的文档**。
2. 载体是 **ACTIVE L1**（CR-003）——项目最高审查级别的文档类之一；且该行正是 CR-003 的**创建门槛论证**的一部分（用它证明"此前无 L1"）。
3. 修法与项目既有惯例一致且极简：按 `90 §4`「Reconcile, don't rewrite」加**时点限定语**即可（例：`90 §1:41` 自述「L1 … 暂无」**（CR-003 编制时；其后已事实同步，见 `90:47` 注）**）。
4. **不阻断**：CR-003 的落点依据是 `90 §1.2:79` 允许列 ✓（未受影响）；授权、分类、re-freeze 链均不受影响。

**建议（Owner 裁决；DSH 不自行修改）**：在 `CR-003 §0.1:49-51` 加一行时点/范围限定语（或注明"该清单为该 L1 编制时状态"）。

### H-02 [LOW] `84_CONFLICT_LEDGER:176` 的「无一份 L1 Contract Change Record」

```text
:176 **结论**：`line_refs` 的规范载体在四个层级上有四种答案，**且无一份 L1 Contract Change Record**。
:177 在 BIND-1/2/3 裁决并走完 L1 之前，**任何一方都不得被当作事实**。
```

- 上下文（C-01 `line_refs` 载体冲突）表明原意是「**就 `line_refs` 而言**无 L1 可裁决」——按此读法**仍为真**（CR-003/CR-004 均不涉 `line_refs`）✓。
- 但字面为无限定断言，而仓内现有 2 条 L1 ⇒ 与本轮 H-01 属同型（无限定语的现行断言）。**LOW**；若 Owner 要求严格，加「（就 `line_refs` 而言）」即可。

### H-03 [LOW] M-03 注记的自指措辞不精确

- 注记称「后续仓内编辑（2026-09-24 起）= **解释性修正**（如下方 `Frozen Spec:` 行的 scope clarification）」。
- 但**该注记本身**就是一次 2026-09-25 的仓内编辑，且属 provenance 注记（非"解释范围收窄"）。⇒ 该分类句未把自己排除，严格说不够精确。
- 不影响授权语义 ✓（注记本身也未扩大/收窄任何授权）。建议改为「后续仓内编辑 = 解释性修正**与 provenance 注记**」。

### H-04 [LOW / UNKNOWN] M-02 在 L0-META `90` 内引述了仓外任务书的一句授权文本

- `90 §11 (c)`:500 引「R-02 —— 若确实缺一个简单的静态检查点，只记录最小治理要求」作为新增要求的授权落点。
- 该引文**无法在仓内核验**（任务书不在仓内），DSH 亦无独立来源；与 CR-004 §2.4 明确"**不**复制外部原文"的处理**口径不一致**（可辩护：一为授权落点、一为判据，但应明示）。
- 周边文字已把载体标注为**仓外**并要求"不升格为仓内权威" ✓ ⇒ 风险有限。建议加「（引述；未逐字核对）」或统一到 CR-004 §2.4 的口径。

---

## 5. 报告自述 vs 实测（逐条）

| # | 报告自述 | 实测 | 判定 |
|---|---|---|---|
| 1 | HEAD `5a46d33` · push 后 == origin · 5 文件 +124/−9 全 .md | 全部一致 ✓ | **TRUE** |
| 2 | tree 链至 `63810f55…`（CURRENT），`git rev-parse HEAD:Docs/V3_SPEC == G-02 §6.2 字面值` | `5a46d33 = HEAD = 63810f55` ✓ 与 G-02 §6.2 一致 ✓ | **TRUE** |
| 3 | M-01：§2.4 两类权威分列 + 7 坐标 + 可复核性边界；未搬原文、未重定义 STOP-1 | 逐项实测一致（`:111-139`）✓ | **TRUE** |
| 4 | M-02：授权落点澄清三行表；无新机制/审批层/状态/registry | `:493-505` 一致 ✓；无任何新机制文件 ✓ | **TRUE** |
| 5 | M-03：ratification/provenance 注记；不主张正文 == 原始批准；合成状态；复用既有机制 | `:16-46` 一致 ✓；`STATUS: OWNER APPROVED` 未被重新签发 ✓ | **TRUE** |
| 6 | M-04：标题 L0=5 / 表体 6 行已显式对齐；12493ca 保留；audit scope 未变 | 一致 ✓ | **TRUE** |
| 7 | M-05.1：G-02 §6.1a 双口径 10 / 13 + 明细 | 一致 ✓（9 + 4 明细经独立计数验证 ✓） | **TRUE** |
| 8 | M-05.2：90 §1 + Status.md 两处 stale 事实同步；只改事实 | 一致 ✓；两处权限/禁止列**逐字未变** ✓ | **TRUE（副作用见 H-01）** |
| 9 | 「OD-R-01 业务语义 NO CHANGE（10/20 本轮 0 改动；§6.3 与 ABD 逐字保留）」 | 本轮文件清单**不含** `10_Data_Model.md` / `20_Document_Pipeline.md` ✓ | **TRUE** |
| 10 | 「OD-R-01 语义关键词新增行 = 0」 | 新增行扫描（multi-value / QuestionInstance / ordered value / `value[i]` / partial correct / `answer[]` / `answer_status`）= **0** ✓ | **TRUE** |
| 11 | 「禁止产物扫描新增行命中 = 0」 | NULLS NOT / CREATE·ALTER TABLE / alembic / migration / CREATE INDEX / UNIQUE = **0** ✓ | **TRUE** |
| 12 | 「新 Owner Decision / OD-R-02+ 命中 = 0」 | **0** ✓ | **TRUE** |
| 13 | 「(c) 声明登记行存在（90 §11:512）」 | `:512` 逐字一致 ✓（含机械取值命令 `:514`）✓ | **TRUE** |
| 14 | 「untracked：默认 10 · -uall = 13（未混用）」 | 一致 ✓ | **TRUE** |
| 15 | 「90 §2–§10 治理原则逐条未动」 | hunk 仅 `@@ -38` / `@@ -450` / `@@ -483` ⇒ §2–§10 未触 ✓ | **TRUE** |
| 16 | 「无 force push / rewrite / rollback；两 commit 可达」 | `f708370` / `71f51f9` 均为 HEAD 祖先 ✓ | **TRUE** |
| 17 | 单 commit 说明（§12 建议两 commit，本次以声明一次覆盖为由合并） | 理由自洽且已披露 ✓（拆分确会使 L0-META 改动出现瞬时无声明窗口） | **合理** |
| 18 | 「M-03『mechanism not available』分支 NO CHANGE REQUIRED（仓内有可复用机制）」 | 仓内确有 current-ratification 模式 + G-01 ✓ | **TRUE** |
| 19 | AUDIT：「0dd954d 及其后触及 L0 00–50 = 5 笔；本次 commit 不在其中」 | 本 commit 未触 00–50 ✓；5 笔枚举与上轮 DSH 独立复算一致 ✓ | **TRUE** |
| 20 | VALIDATION「(c) 声明登记行存在」/「[✓] 无新的未登记 L0 change」 | 成立 ✓（本 commit 为 L0-META/L1 面改动，已按 (c) 声明 ✓） | **TRUE** |

---

## 6. 无法核验项（UNKNOWN）

```text
U-1  任务书 §11 / §14 / §22 / §10A / §10C / §15 / §5 的**判据原文**（不在仓内）。
     CR-004 §2.4 已**如实声明**本表不承担使其可自证 ✓ ⇒ 属已披露边界，不再是缺陷。
U-2  `90 §11 (c)` 中引述的 R-02 授权语句与任务书原文的**一致性**（不在仓内）⇒ H-04。
U-3  远端独立复核：git ls-remote 受凭据策略阻断；本地 remote-tracking = 5a46d33 ✓。
```

---

## 7. Owner 裁决清单

| ID | 待裁问题 | 说明 |
|---|---|---|
| **HYG-D1** | `CR-003 §0.1:49-51` 是否加时点/范围限定语（H-01，MED） | 唯一实质项；一行即可，属 `90 §4` Reconcile 模式 |
| **HYG-D2** | `84:176` 是否加「（就 `line_refs` 而言）」限定（H-02，LOW） | 严格性选择，不影响语义 |
| **HYG-D3** | M-03 注记措辞是否补"与 provenance 注记"（H-03，LOW） | 自指精确性 |
| **HYG-D4** | M-02 引述仓外授权文本是否加"引述/未逐字核对"标注或统一口径（H-04，LOW） | 与 CR-004 §2.4 口径一致性 |
| **HYG-D5** | OD-R-01 是否正式记为 CLOSED（报告已声明 CLOSED / Implementation = STOP / X3 NOT ENTERED） | DSH 确认：授权链、审计链、provenance 链**已闭合**；H-01 为文档精确性残留，不构成闭合阻断 |

---

## 8. 应予记分之处

```text
+ 五项 findings 逐一对应、修法精准，无一项以"扩大范围"方式解决
+ M-01 写出了**可复核性边界**（"只使判定动作可自证，不使判据原文可自证"）—— 诚实且有方法论价值
+ M-03 明确拒绝"当前正文 == Owner 批准原文"的等式，并提出"合成状态"表述 —— 未伪造 Owner approval
+ M-02 把"既有登记义务"与"本次新增要求"严格分列，并给出后者的授权落点 —— 直接回应 M-02 的实质
+ 上一轮新增的 (c) 规则被**自觉执行**（90 §11:512 声明登记 + 机械取值命令）—— 治理规则自洽闭环
+ 数字与明细全部准确（tree 三值可复算；untracked 10/13 与 9+4 明细；L0=5/表体 6 行）
+ 无 production code / schema / migration / L0 00–50 改动；无 rewrite；无重复记录
+ 报告主动列出 OUT OF SCOPE 与单 commit 理由，未掩盖决策
```

---

## 9. 附：机械验证命令（可复现）

```powershell
$repo='D:\Project\AITutors-v3'
git -C $repo rev-parse HEAD 'HEAD:Docs/V3_SPEC' 'fbec14e:Docs/V3_SPEC'
git -C $repo show --numstat --format='' 5a46d33
git -C $repo show --name-only --format='' 5a46d33 |
  Where-Object { $_ -notlike '*.md' -or $_ -like 'backend/*' -or $_ -match 'V3_SPEC/(00|10|20|30|40|50)_' }
git -C $repo show 5a46d33 -- Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md Status.md
git -C $repo grep -n -I '§1:41' -- Docs/ Status.md          # H-01：唯一命中 = CR-003:51
git -C $repo grep -n -I '暂无（' -- Docs/ Status.md          # H-01 相关
git -C $repo merge-base --is-ancestor f708370 HEAD ; git -C $repo merge-base --is-ancestor 71f51f9 HEAD
git -C $repo ls-remote origin od01-r3-convergence           # U-3：需凭据，本环境受阻
```

---

*DSH 独立对抗性审查（第四轮）· 对 git 对象与仓内文本取证 · 审查期间未修改任何文件、未 push · 全部结论均可由 §9 命令复现。*
