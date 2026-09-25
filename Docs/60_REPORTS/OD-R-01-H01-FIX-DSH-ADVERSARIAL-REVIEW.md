# OD-R-01 H-01 修正（CR-003 §0.1 时点限定）— DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Hygiene Closure — 最终报告」（STATUS: COMPLETE），即对 DSH 第 4 轮 finding **H-01 / Owner 决策项 HYG-D1** 的修正 |
| 仓库 | `D:\Project\AITutors-v3`（报告自述其任务书标注 `REPOSITORY: AITutorX`，见 §5 路径披露核验） |
| 分支 | `od01-r3-convergence` |
| 被审 commit | `1ee84cdf3ad22127b95bb510b89af85cea906b10`（parent `5a46d33`） |
| 审查基线 | HEAD = `1ee84cd`（tracked 改动 0） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间未修改 `AITutors-v3` 任何文件、未 commit、未 push |
| 证据分级 | DIRECTLY VERIFIED（由 git 对象 / 逐字节文本实测） > VERIFIED BY INSPECTION > DOCUMENT CLAIM > UNKNOWN |
| 关联 | 上一轮：`OD-R-01-HYGIENE-CLOSURE-DSH-ADVERSARIAL-REVIEW.md`（AITutor-X `d7d0ecc`，其中 H-01 = 本轮被修对象） |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（H-01 本身**已被正确治愈**：修法命中实质、语义保真、未改写历史；
 但本 commit 同时产生 2 项 MED 须闭合项 —— 一项治理声明缺口、一项跨文件当前态断言失效）
```

**一句话结论**：修法**取对了取舍**——不是删掉 `CR-003 §0.1` 的旧文或改数字，而是加时点限定语并明写「**不表示** Contract Change Record 从未存在」，完全符合 `90 §4`「存量文档不强制回填（Reconcile, don't rewrite）」。`CR-003 §10` 的"字面值不入本文件"自指防火墙设计也经受住了本次编辑（§10 无需改动，re-freeze identity 仍成立）。

但对抗性核验发现：**本 commit 一边修掉一处当前态假断言，一边制造了两处同类缺陷**——
① `Docs/V3_SPEC` tree hash 由 `63810f55…` 变为 `47a59e50…`，按 `90 §11 (c)`（上一 commit 自己新增的**强制**要求）**必须**在 §11 补一行声明，实测**未补**；
② 该 tree 变化使 `G-02 §6` 登记的 **CURRENT Frozen Spec tree = `63810f55…`** 与 `§6.2` 阶段行的 **current** 标签**当场失效**——而 G-02 §6 正是 `90:493-494` 指定的「L0 tree hash change → audit required」闭环一环、也是 `CR-003 §10:298` 指定的 re-freeze 字面值**可读副本**。
因此报告 §4 结论「除 `84:176` 外，仓内不存在其余错误描述当前状态的历史陈述」**被证伪**。

以上均**不触及授权、分类、re-freeze 语义**，故不构成 REJECTED。

---

## 2. 已独立复核的关键事实（DIRECTLY VERIFIED）

```text
HEAD = 1ee84cd… ✓   branch = od01-r3-convergence ✓   parent = 5a46d33… ✓
origin/od01-r3-convergence = 1ee84cd… ✓（以 git ls-remote 直接核验远程 ref，非仅本地 tracking ref）
main = 6d8a3bd（未动）✓   origin/main = 7934844（未动）✓
1 file changed, 7 insertions(+), 2 deletions(-)，单一 hunk @@ -46,9 +46,14 @@（§0.1 段）
file = Docs/V3_SPEC/CR-003_CONTRACT_CHANGE_RECORD_OD-R-01.md
非 .md = 0 ✓   L0 00–50 = 0 ✓   `90`/`91` = 0 ✓   backend / code / schema / migration = 0 ✓

blob：CR-003  c8870b8… → 37e7d9e…
tree：Docs/V3_SPEC  5a46d33 = 63810f55c88cee983004136f288f1b6ff3527a8d
                    1ee84cd = 47a59e50126f0f7e98f44d281f8d388236240735   ← 变化，且未登记（H-05）
tree：repo root     5a46d33 = 36824a80…  →  1ee84cd = 0449b4c4…

AITutorX：tracked 改动 = 0 ✓   本轮新建 .md = 0 ✓   全仓无 `CR-00*` 文件 ✓（路径披露前提成立）
untracked（AITutors-v3）：与上一轮一致，无新增
```

**`90 §11 (c)` 现状（实测全文）**：规则在 `:489-491`；声明登记表 `:508-514` **仅 1 行数据行**（`:512`，对应上一 commit `5a46d33`）；`git grep '1ee84cd' Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md` = **0 命中**（exit 1）。

**`G-02 §6` 现状（实测）**：`:148` 阶段行仍标 **current**；`:160` **CURRENT Frozen Spec tree** = `63810f55…`；`:151-154` 链式图终点仍为 `→ CURRENT`（即 `2edd2010… →(最终卫生收口 M-01~M-05)→ CURRENT`）。

---

## 3. 报告自述逐条核对

### 3.1 Validation 表（8 条命令）

| # | 报告所载命令 | 报告结果 | DSH 实测判定 |
|---|---|---|---|
| 1 | `grep -rn "§1:41" Docs/ Status.md` | 3 处，均在 CR-003 且已限定 | **TRUE** —— 全仓（含 `Status.md`）恰 3 处：`CR-003:52/:54/:55`，无第 4 处 ✓ |
| 2 | `grep -rn "暂无" Docs/ Status.md` | 4 处，归类无误报 | **TRUE**（在其声明范围内）—— 4 处 = `90_EB008:601` / `Status.md:3593` / `90:47` / `CR-003:52`；DSH 全仓另有 `bugs.md:1022`「（暂无。）」，在声明范围外且与 L1/CCR 无关，不构成误报 |
| 3 | `grep -rn "无 Contract Change Record\|不存在…\|无一份 L1"` | 剩余 1 处 = `84:176`，NON-AUTHORIZED 保留 | 事实 **TRUE**（加 `-E` 后唯一命中 `84:176` ✓）；但**所载命令不可复现**（BRE：`\|` 为字面量，实测 0 命中 / exit 1）→ **H-08(a)** |
| 4 | `grep -rn "现存仅\|当前无 Contract\|尚未有.*Contract Change"` | 仅 `CR-003:50`，已限定 | 事实 **TRUE**（`-E` 后唯一命中 `CR-003:50` ✓）；命令同样 BRE 失效 → **H-08(a)** |
| 5 | `git diff --name-only \| grep -v '\.md$'` | OK：全部 .md | 结论 **TRUE**，但该命令**空验证**（commit 后工作区干净 ⇒ 输入为空）；正确命令 `git show --name-only --format= 1ee84cd` 实测仅 1 个 `.md` ✓ → **H-08(b)** |
| 6 | `git diff --name-only \| grep -E 'V3_SPEC/(00\|10\|20\|30\|40\|50)_'` | OK：未触碰 L0 00–50 | 结论 **TRUE**，同样是**空验证**；`git show` 实测 L0 命中 0 ✓ → **H-08(b)** |
| 7 | `git show --stat` | 1 file, +7/−2 | **TRUE** ✓（逐字一致） |
| 8 | `git rev-parse HEAD` vs `origin/od01-r3-convergence` | 均 = `1ee84cdf…` | **TRUE** ✓，且 DSH 以 `git ls-remote` 直接核验远程 ref = `1ee84cd`（强于本地 tracking ref） |

**§4 结论**：「除 `84:176` 外，仓内不存在其余错误描述当前状态的历史陈述」→ **FALSE**（被 `G-02:160` / `:148` 证伪，见 H-06）。原因是 4 条 pattern 均无法覆盖 **tree hash 字面值 / current 标签**类当前态断言 → **H-08(c)**。

### 3.2 其余自述

| 项 | 判定 |
|---|---|
| 路径披露（任务书标 AITutorX，实际落 AITutors-v3） | **前提成立** ✓：AITutorX 内确无 `CR-003` 实体，tracked/新建改动 = 0，故修正只能落在 AITutors-v3；「任务书确曾标注 `REPOSITORY: AITutorX`」属**仓外**文本 → **UNKNOWN** |
| 语义保真：保留 "at CR-003 time"，未变成 "never existed" | **TRUE** ✓（`:54-55` 逐字核对：「**仅**描述 CR-003 编制时点的历史状态」「**不表示**『Contract Change Record 从未存在』」） |
| 最小范围：未增删表行 / `§0` 四问门槛未动 / `May Change`·`Must Not Change` 未动 / `§1–§12` 结论未动 / 未新增字段·状态·registry | **TRUE** ✓（单 hunk `@@ -46` 为硬证据；`:16-17` 头块、`:33-38` 四问表、`:58` 起 `§1` 之后全文均未被本 commit 触碰） |
| 治理 6 项（No Frozen Spec files / No authority model / No migration / No X3 / 仅历史措辞 / 未处理可选项） | 6 项均 **TRUE** ✓（DSH 独立复核文件清单与 hunk 范围）——但**清单本身缺一项**：tree hash 变化 → `90 §11 (c)` 声明行 → **H-05** |
| Commit 信息（message / branch / 已 push / HEAD==origin） | **TRUE** ✓（含远程 ref 独立核验） |
| 「不受影响」暗示：re-freeze 链 | **TRUE** ✓：`CR-003 §10` 采用 commit 锚定公式且**刻意不写字面值**（`:294-295` 自指防火墙），故 L1 本体编辑不破坏 §10；但**副本**在 G-02 失效 → **H-06** |

---

## 4. Findings

### H-05 [MED] 治理声明缺口：`90 §11 (c)` 强制要求未执行（本 commit 本身未登记）

**规则原文（`90:489-491`，上一 commit 自己新增，含「**必须**」）**

> `Docs/V3_SPEC` tree hash 发生变化时，必须能在本节找到对应 CA 条目；若该变化**不触及** L0 `00–50`（例如仅改 `90` / `91` / `README`，或**新增 / 修改 L1 文件**），则在本节补一行声明其为「L0-META / L1 面改动，非 L0 修改」。

**实测**：本 commit **修改 L1 文件**（`CR-003`，属规则逐字枚举的情形）⇒ `Docs/V3_SPEC` tree `63810f55…` → `47a59e50…`；而 `:508-514` 声明登记表仍只有 `5a46d33` 一行，`90` 内 `1ee84cd` 0 命中。

**严重度理由**：定 **MED**，不定 HIGH —— 本 commit **未触及 L0 `00`–`50`**、未改授权/分类/re-freeze 语义，故不是 R-01 型（未登记的真实 L0 修改）；也不定 LOW —— 该规则文本为「必须」，机械可复核，且是上一 commit 为建立「闭环」而自设的验收条件，本 commit 恰是其**第一次适用对象**却未执行。

**反方最强辩解（诚实列出）**：(c) 表标题自述「本规则自身的执行记录」，可读作**只**登记规则创建 commit；且本任务范围可能明令不得触碰 `90`（L0-META）。**但**：① 规则正文的动作是"此后每当变化就补一行"，非一次性；② 前一 commit 为**自身**补了该行，说明可行性已确立；③ 若确因范围限制无法补行，则该**限制本身必须被声明**（登记豁免/延后 + 授权依据），否则 `90 §11 (c)` 的「必须」与实际状态**公开不一致**。

**建议修法（一行）**：在 `:508-514` 表追加一行 —— 改动所在 commit = `1ee84cd`（2026-09-25）；改动面 = `CR-003 §0.1` 时点限定 / 历史口径注记（H-01 修正）；声明 = **L0-META / L1 面改动，非 L0 修改**（未触及 L0 `00`–`50`）。或显式登记延后及依据。

---

### H-06 [MED] 跨文件当前态断言失效：`G-02 §6` 的 CURRENT 指针与 current 阶段行已成假

**事实链（全部 git 实测）**

1. `5a46d33:Docs/V3_SPEC` = `63810f55…` —— 与 `G-02:160` 登记值**一致**（上一轮 DSH 已确认）；
2. 本 commit 后 `1ee84cd:Docs/V3_SPEC` = `47a59e50…` ⇒ **登记值不再等于事实**；
3. `G-02:148` 阶段行仍标「= **current**」，`:151-154` 链式图终点仍为「→ CURRENT」；
4. `90:493-494` 明写「既有 `90 §11`（登记义务）+ **G-02 §6（tree hash 记录）** + `CR-003 §10` / `CR-004 §8`（re-freeze identity）已足以形成『L0 tree hash change → audit required』闭环」；
5. `CR-003 §10:298` 明写 G-02 §6 = 该 re-freeze identity 的**字面值可读副本**（副本非权威，但读者据以核对时会当场矛盾）。

**性质**：按 `G-02 §6.3` **自身**的判定标准（`“只修『当前断言与当前事实直接冲突』处”`，`:184`），`G-02:160` 现属 **false current-state assertion**——即本 commit 正在消除的缺陷类别，被**原样复制**到定义该标准的那份文件里。上一轮 DSH 记分的「`(c)` 规则被自觉执行 ⇒ 治理规则自洽闭环」，在本 commit 后**断裂**。

**反方最强辩解**：`:161-162` 括注「= `git rev-parse <本行登记所在 commit>:Docs/V3_SPEC`」提供了**commit 锚定**读法，可辩称该值是"登记时点的值"。**但**粗体标签是 **CURRENT**，`:148` 亦标 **current**——标签而非括注才是读者据以判断"当前"的依据；且 G-02 §6.2 定位为随每次 `Docs/V3_SPEC` 变化更新的**链**（其最后一行自称覆盖"最终卫生收口"，即当时最新变化）。

**连带影响**：报告 §4 结论被证伪（见 §3.1）。

**建议修法（三处）**：① `:160` 字面值更新为 `47a59e50126f0f7e98f44d281f8d388236240735`（由 `git rev-parse 1ee84cd:Docs/V3_SPEC` 计算，非手填）；② `:148` 表新增一行「`CR-003 §0.1` 时点限定（H-01 修正 / DSH 第 5 轮）」；③ `:151-154` 链式图追加该阶段。若 Owner 选择不再更新 G-02，则至少把 `:160` 标签改为「截至 `5a46d33` 的 CURRENT」，并把 `:148` 的 current 标签注明"其后另有 `1ee84cd` 改动（未登记）"。

---

### H-07 [LOW] 本次替换 / 新增文本自身的措辞缺陷（4 子项）

**(a) 递归创建同类断言（最重要）**：新增注记 `:55-56`「其后 `90 §1:41` 已按事实同步（见 `90:47` 注），`Docs/V3_SPEC/` 亦已新增 `CR-003` / `CR-004` **两条** `Contract Change Record`。」——这是**无时点限定的当前态 + 数量重复计数**：一旦新增 CR-005，本行即在 **ACTIVE L1** 内变为假，与 H-01 同型。
根因不是"写错字"，而是**修法策略仍在复制状态而非指向唯一权威**。建议改为「L1 现状以 `90 §1:41` 为准（本行不作重复计数）」，或退一步写成「截至本行所在 commit，其后已新增 `CR-003` / `CR-004`」。**否则固定点问题会持续复现。**

**(b) 「当期」歧义**：`:52`「`90 §1:41` **当期**自述「L1 … 暂无」」——中文「当期」常义为"**当前**期间"（会计 / 保险语境），可能被读成"现在仍自述暂无"，**恰为本轮要消除的假当前态**。建议改「**当时**」/「编制时」。

**(c) 「上述文件清单」指代不清**：`:54`「**上述文件清单**与 `90 §1:41` 引文**仅**描述 CR-003 编制时点的历史状态」——紧邻上文既有 `§0.1` 四行"最近似文档"表（其中 `CR-002` 未归层 / `67` 候选 `NOT RELEASED` 等判定**至今有效**），又有"搜索结论"内的 `Docs/V3_SPEC/` 文件清单。限定语若被读作涵盖前者，会**反向削弱至今有效的判定**。建议写明「上述**『搜索结论』中的** `Docs/V3_SPEC/` 文件清单」。

**(d) 缺日期化修订标记**：ACTIVE L1 正文（`§0.1`）被修改，但文件内**无**"何日 / 因何 / 经何审查"的修订记录（对照 `CR-004 §2.4` 把 M-01 标注在新增小节里的既有做法）。建议注记首句加「（2026-09-25 · H-01 修正，经 DSH 第 4 轮审查提出）」。

---

### H-08 [LOW] 验证表的可复现性 / 有效性

| 子项 | 内容 |
|---|---|
| **(a) BRE 失效** | 命令 3、4 写作 `grep -rn "a\|b\|c"`：**BRE 下 `\|` 为字面量**，实测 0 命中 / exit 1 ⇒ **不可能产出**报告所载「剩余 1 处 = `84:176`」「仅 `CR-003:50`」。事实本身经 DSH 以 `-E` 独立复现为**真**，但**所载命令不构成证据**——而 `§4` 结论正依赖这两条。 |
| **(b) 空验证** | 命令 5、6 在 commit **之后**执行 `git diff --name-only`：工作区干净 ⇒ 输入为空 ⇒ 无论改动多离谱都会 **PASS**。「全部 `.md`」「未触碰 L0 `00`–`50`」为真，但**未由该命令验证**。正确命令：`git show --name-only --format= 1ee84cd`（DSH 实测：1 个 `.md`、L0 命中 0、非 `.md` 0 ✓）。 |
| **(c) 扫描口径缺口** | 4 条 pattern 均**无法**发现本 commit 实际制造的当前态断言（`G-02:160` 的 tree hash 字面值、`:148` 的 current 标签）⇒ `§4` 结论为假。建议补与 `90 §11 (c)` 对齐的机械检查：`git rev-parse HEAD:Docs/V3_SPEC` 是否等于 G-02 §6 登记值；该 tree 变化是否在 `§11 (c)` 有声明行（即 H-05 / H-06 的检查本身）。 |

---

## 5. 记分：本轮做对的地方（避免只列缺陷）

1. **取舍正确**：没有删旧文 / 没有改历史值 / 没有把"当时"偷换成"从未"，而是加限定语并显式否认全称读法 —— 与 `90 §4`「Reconcile, don't rewrite」一致。这是本题**最容易做错**的一处（另一条错路是直接删掉 `§0.1` 那段）。
2. **指针正确**：新注记引用的「`90:47` 注」实测确实存在且内容相符（`:47-49` 为 `90 §1` L1 例子列事实同步注）✓。
3. **上上轮设计的红利被验证**：`CR-003 §10` 因**刻意不写** tree 字面值（`:294-295` 自指防火墙）而在本次 L1 本体编辑中**无需改动**，commit 锚定的 re-freeze identity 依然成立——说明"自指不动点"这条设计是真的有用，而非文字装饰。
4. **文件级最小化**：单文件、单 hunk、+7/−2，未顺手触碰 `90`/`91`、未新建机制/状态/registry ✓。
5. **边界纪律**：把 H-02（`84:176`）明确列为 NON-AUTHORIZED 保留、未借"顺手"扩大范围 ✓；路径披露主动给出且前提可核验 ✓。

---

## 6. Owner 裁决清单（DSH 只列项与证据，不作裁决）

```text
OD-R-01-H01-D1  【MED·唯一治理合规项】补 `90 §11 (c)` 声明行（H-05）
                 —— 否则 §11 (c) 的「必须」与实际状态公开不一致；或显式登记豁免/延后及依据
OD-R-01-H01-D2  【MED】更新 `G-02 §6`：`:160` 字面值 → 47a59e50… + `:148` 新增阶段行 + `:151-154` 链（H-06）
                 —— 该文件是 `90:493-494` 指定闭环的一环、`CR-003 §10:298` 指定的 re-freeze 副本
OD-R-01-H01-D3  【LOW】`:55-56` 改为"指向 `90 §1:41`"而非复制"两条"计数（H-07a，防同类复发）
OD-R-01-H01-D4  【LOW】措辞三项：「当期」→「当时/编制时」·「上述文件清单」限定指代 · 加 2026-09-25 修订标记（H-07b/c/d）
OD-R-01-H01-D5  【LOW】验证表改为 `grep -E` / `git show --name-only` / 增 tree-hash→§11(c) 检查（H-08）
OD-R-01-H01-D6  【HYG-D5 承接】OD-R-01 是否正式记为 CLOSED：
                 DSH 立场 = 授权链 / 分类 / provenance 链**在本 commit 后仍闭合**；
                 但 (c) 登记链在补上 D1 那一行之前**不完整**。故：先补 D1（或显式登记豁免），再判 CLOSED。
                 H-07 / H-08 属文档精确性与取证方法残留，不构成闭合阻断。
```

**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 7. 未验证 / UNKNOWN（不得当作已核验）

```text
UNKNOWN  仓外任务书原文（含 `REPOSITORY: AITutorX` 标注、NON-AUTHORIZED 清单、H-01 授权措辞）
         —— 不在仓内，DSH 无法核验其存在与逐字一致性；本报告只核验其**可核验后果**
UNKNOWN  远程服务端 push 审计日志 / 是否有其他 ref 被改动
         —— 已核验 ref 值（od01-r3-convergence = 1ee84cd、main = 7934844），其余不可见
INFO     本地 `main` = 6d8a3bd… 领先 `origin/main` = 7934844… **12 个 commit**（均不触及 `Docs/V3_SPEC`）
         —— 上一轮已存在的状态，本 commit 未改变；是否属预期推送策略 = Owner 事由，非本 commit 缺陷
INFO     `Docs/V3_SPEC` 之外仓内仍有 2 处与 L1 / CCR 无关的「暂无」文本（`90_EB008:601`、`Status.md:3593`）
         —— 语境为 IR Authority，未受影响、无需改写
```

---

**Document control**

| Field | Value |
|---|---|
| Path | `Docs/60_REPORTS/OD-R-01-H01-FIX-DSH-ADVERSARIAL-REVIEW.md` |
| Status | FINAL |
| Reviewed commit | `1ee84cdf3ad22127b95bb510b89af85cea906b10` |
| Round | OD-R-01 对抗性审查第 5 轮 |
| Verdict | ACCEPTED WITH FINDINGS（H-05 MED · H-06 MED · H-07 LOW · H-08 LOW） |
| Repo of subject | `kurt-wong/AITutors-v3` @ `od01-r3-convergence` |
| This report repo | `D:\Project\AITutor-X`（DSH 侧，未修改被审仓任何文件） |
