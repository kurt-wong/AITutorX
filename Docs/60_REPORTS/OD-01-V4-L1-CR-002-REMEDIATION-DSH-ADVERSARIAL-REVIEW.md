# OD-01 v4 Remediation — DSH 独立对抗性审查报告

```text
Report ID:        DSH-OD-01-V4-REMEDIATION-ADVERSARIAL-REVIEW
Report Type:      L3/L4 独立对抗性审查（DSH）
Report Repo:      kurt-wong/AITutorX  →  Docs/60_REPORTS/
Reviewed Repo:    kurt-wong/AITutors-v3（只读）
Reviewed Scope:   commit 86da69c + 9bd6eca（parent 2dc7a5e）— 3 改 + 1 新增
Reviewed HEAD:    9bd6ecac69465edcbb1f2bbcb5c57c31a2bfe8f5
Independence:     本报告作者未参与 OD-01 v4 任何产出；被审方不得以其自审文件
                  或在先声称替代本报告
Date:             2026-09-23
Verdict:          VERIFIED WITH FINDINGS
Closure Blocking: YES
Recommendation:   OWNER ACTION REQUIRED BEFORE CLOSURE
```

> **本报告是审查证据，不是规则来源。** 不修改 `Docs/V3_SPEC/**`、不修改 Frozen Contract、
> 不修改被审四件交付物、不 re-freeze、不标记 OD-01 生效、不执行 Migration、不进入 Phase 1/X3。
> 发现只登记，不修复（AGENTS.md：**Provenance ≠ Quality Authority**；
> **Agent 自写的 "Frozen / Final / Authority" 不自动获得权威**）。

---

## 0. 审查边界与方法

**审查对象（只读）**

| # | 文件 | 角色 | 本轮变化 |
|---|------|------|----------|
| 1 | `Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md` | Proposal **v4** | +502 / −340 |
| 2 | `Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md` | CR-002 candidate | +139 / −163 |
| 3 | `Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md` | D1（+OD-01-A…J） | +64 / −11 |
| 4 | `Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md` | **新增**（自审） | +87（A） |

**证据分级**：`DIRECTLY VERIFIED` / `SOURCE-LEVEL VERIFIED` / `VERIFIED BUT NOT REPRODUCED` /
`NOT VERIFIED`。本报告全部结论为 `DIRECTLY VERIFIED`（除 §10 所列局限）。

**方法**：① 独立重放 Git/哈希事实；② 逐条质询「R-01…R-10 = ADDRESSED」；③ 对每处
「Current Rule」与「Proposed Frozen Text」做逐字/逐条核对；④ **把 change set 当作待写入 L0 的
正式文本做一致性推演**（若逐条应用会产生什么矛盾）；⑤ 反向检索禁用词、未定义命名空间、
未登记字段、未映射 ID；⑥ 对新增文档做 `90 §4` / `91 §5` / `90 §5` 机械合规扫描。

**未做的事**：未重跑测试基线、未执行四道门、未做 corpus 对比、未修改任何被审文件、未修复发现、
未推送 AITutors-v3。

---

## 1. 对抗性盘问集（14 问）

| # | 盘问 | 判定 |
|---|------|------|
| Q1 | 自述「R-01…R-10 全部 ADDRESSED」成立吗？ | **否** — 5 项成立，6 项部分，1 项不成立（R-09），见 §5 |
| Q2 | 上一轮 12 项发现是否都被映射并处置？ | **否** — F-OD01V3-11/12 未映射，且 11 仍未修复（F-OD01V4R-07/12） |
| Q3 | 新出现的「对抗审查结论」是独立复核吗？ | **否** — 由被审方撰写并提交在被审仓库（F-OD01V4R-01） |
| Q4 | 新建的 `Docs/REPORTS/` 文档是否满足 `90 §4` 强制头块？ | **否** — 缺 10 个强制字段（F-OD01V4R-02） |
| Q5 | 禁用状态词问题真的解决了吗？ | **否** — `COMPLETE` 出现在新文档 Status；`NEXT` 出现在 D1 Status；且指示 `COMPLETED`（F-OD01V4R-03） |
| Q6 | 「Proposed Frozen Text 可直接复制」成立吗？ | **否** — CI-4 三段文本互相矛盾（F-OD01V4R-04） |
| Q7 | 逐条应用 change set 后 L0 会自洽吗？ | **否** — `resolution_status` / `span_resolution` 将两名一义，且 `20 §5.5` 未列入受影响条款（F-OD01V4R-05） |
| Q8 | 规范字段 `Authority Level` 为何消失？ | 被 `Authority:` 替换以规避上一轮矛盾（F-OD01V4R-06） |
| Q9 | ID 唯一化（R-09）实现了吗？ | **否** — 表不完备、≥4 行错配、并引入第 7 套未定义命名空间（F-OD01V4R-07/08） |
| Q10 | v3 的「Governance Gap / 无合法落点」结论是否一致更正？ | **否** — CR 已更正，D1 仍保留 Gap 路径表述，两版并存（F-OD01V4R-09） |
| Q11 | 新文档受 `90 §5` 机械扫描规则约束吗？是否合规？ | **受约束，不合规** — L3/L4 禁用词未引用 L0/L1/`82 §3`（F-OD01V4R-10） |
| Q12 | 缺口基线 / 完整六段式 diff 是否恢复？ | **是** — §1 基线表 + CI-1…CI-12 六段式齐备（P3/P4） |
| Q13 | `degraded` 是否被夹带进 change set？ | **否** — 明确排除并给出替代路径（P5） |
| Q14 | Frozen Spec / 代码 / Schema / corpus 是否被改动？ | **未改动** — 三点树哈希一致（P1/P12） |

---

## 2. Git / 隔离事实（DIRECTLY VERIFIED）

```text
AITutors-v3
  HEAD              = 9bd6ecac69465edcbb1f2bbcb5c57c31a2bfe8f5   ✓ 与自述一致
  log -5            = 9bd6eca → 86da69c → 2dc7a5e → 3fa3b73 → f68aa09
  86da69c / 9bd6eca 的 parent chain 终点 = 2dc7a5e                ✓ 与自述一致
  2dc7a5e..HEAD     = 4 files: M×3（COORDINATION）+ A×1（REPORTS）
                      numstat 139/163 · 502/340 · 64/11 · 87/0
  non-(COORDINATION|REPORTS) delta = 空（无 backend/schema/corpus/alembic 变更）
  HEAD:Docs/V3_SPEC = b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f   ✓ 未变
  branch -vv        = * main 9bd6eca [origin/main: ahead 8]       ✓ 未 push
  untracked         = 9 × Docs/COORDINATION/CONTRACTS/* + Docs/GOVERNANCE/（未动）

AITutorX（报告仓）
  HEAD = origin/main = 1e44017ba7e1238942d429cafa57c916694dbb3b  （上一轮 DSH 报告）
```

**自述 Git Evidence 逐条复核**：`git diff -- Docs/V3_SPEC` 空 ✅；`HEAD~2..HEAD` 仅
COORDINATION+REPORTS ✅；`status` 仅既有 untracked ✅。

---

## 3. 自述主张逐条核验

| # | 自述 | 判定 | 依据 |
|---|------|------|------|
| 1 | R-01 ADDRESSED — 完整六段式 + 缺口基线 | **VERIFIED** | CI-1…CI-12 均含 Current/Problem/Proposed/Reason/Impact/Affected；§1 基线表 16 行 |
| 2 | R-02 ADDRESSED — Proposed Frozen Text 可复制、无 TODO/未决 | **PARTIALLY VERIFIED** | CI-4 内部矛盾 + 编码单位未定义 + 命名不一致（F-OD01V4R-04/05/12） |
| 3 | R-03 ADDRESSED — CR-002 = Change Proposal Record / NOT EFFECTIVE / NOT REGISTERED AS L1 | **PARTIALLY VERIFIED** | 三项否定性表述齐备 ✅；但自创类型名 `Change Proposal Record`（CR `:5`/`:23`/`:199`）不在 `90 §4:373-374` / `91 §5:165-166` 文档类型枚举内，与同文件 `Document Type: Contract Change Record（候选）`（CR `:6`）并存 → 类型命名不统一（见 F-OD01V4R-06） |
| 4 | R-04 ADDRESSED — `DONE` 已从状态列清除 | **不达标（实质部分）** | Proposal 状态列已清 ✅；但新文档 Status = `COMPLETE`、D1 `:400` Status 含 `NEXT`、并指示 `COMPLETED`（F-OD01V4R-03） |
| 5 | R-05 ADDRESSED — valid future registration path；intentionally deferred | **VERIFIED** | CR `:58`/`:61` 明确「不是没有落点，而是当前不注册」 |
| 6 | R-06 ADDRESSED — degraded 不入本轮；`span_resolution` / `option_evidence_status` 拆分 | **VERIFIED** | §2.3/§2.4 值域与分层写明；`answer_status` 三字段确为既有（`10:463`/`20:370`） |
| 7 | R-07 ADDRESSED — Native / Adapter / Artifact 统一 provenance；禁第二 authority | **VERIFIED** | §3 三路径 + 4 条汇聚不变量 |
| 8 | R-08 ADDRESSED — resolved / unresolved / incomplete / reviewable 唯一关系 | **VERIFIED** | §2.5 四态关系明确 |
| 9 | R-09 ADDRESSED — ID Mapping 表 | **NOT VERIFIED** | 遗漏 F-OD01V3-11/12；≥4 行错配；R-xx 语义仓库内无定义（F-OD01V4R-07/08） |
| 10 | R-10 ADDRESSED — Authority = Owner Decision / Proposal Record；Registration Level = Pending L1 | **PARTIALLY VERIFIED** | 矛盾消除 ✅；但以移除规范字段 `Authority Level` 实现（F-OD01V4R-06） |
| 11 | OD-01-A…J = OWNER APPROVED RECORD / PENDING EFFECTIVE FREEZE | **PARTIALLY VERIFIED** | 记录存在 ✅；agent 自写 `BINDING FOR EXECUTION: YES`；OD-01-H 指示违规词汇 |
| 12 | Frozen Spec UNCHANGED（tree `b3eeb3e9…`） | **VERIFIED** | 树哈希一致 |
| 13 | Production/Schema/Corpus/Phase1/Re-freeze/Migration/Pushed = 未变/未执行/未推送 | **VERIFIED** | name-status 仅 4 文档；ahead 8 |
| 14 | Commit `9bd6eca` + `86da69c`，parent `2dc7a5e` | **VERIFIED** | 全 40 位与父链精确一致 |
| 15 | 「对抗审查结论：VERIFIED WITH FINDINGS（F-OD01V4-01～03，均 LOW、非阻断）」 | **NOT VERIFIED** | 该结论来自被审方自审文件；且漏报本轮全部 13 项发现（F-OD01V4R-01） |

---

## 4. 发现（F-OD01V4R-01 … F-OD01V4R-13）

> 命名说明：使用 `F-OD01V4R-xx` 前缀以避免与被审方自审文件中的 `F-OD01V4-xx` 混淆
> （这本身即为 F-OD01V4R-08 所述命名空间问题的实例）。全部只登记，不修复。

### F-OD01V4R-01（HIGH）— 自审文件被当作独立对抗审查结论使用

**证据**

```text
Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md（本轮新增，87 行）
  :1   标题「OD-01 Proposal v4 — 定向对抗性审查」
  :11  VERDICT: VERIFIED WITH FINDINGS
  :12  CLOSURE BLOCKING: NO
  :13  RECOMMENDATION: READY FOR OWNER REVIEW
  :6-8 SUBJECT = 被审的三件交付物（即作者本人本轮产出）
  :42-46 Findings = F-OD01V4-01（编码单位未钉死）、-02（50 文件名差异）、-03（四道门仍 PENDING）
        三项全 LOW；其中两项为既有已知事项、一项为既有约束复述
外层任务报告：「对抗审查结论：VERIFIED WITH FINDINGS（F-OD01V4-01～03，均 LOW、非阻断）」
```

**质询**：该文件由被审方撰写、提交在被审仓库、并**自declare 独立审查的判定词汇**
（`VERIFIED WITH FINDINGS` / `CLOSURE BLOCKING`）与结论（`READY FOR OWNER REVIEW`）。
AGENTS.md 明示「**Provenance ≠ Quality Authority**」「Agent 自写的 'Frozen / Final / Authority'
不自动获得权威」；DSH 前两轮报告（AITutorX `4b419bf`、`8c2dca3`、`1e44017`）均在文末写明
**「被审方不得以本报告作为自身验证权威」**。

**加重情节**：其 3 项 findings **未触及本轮任何实质缺陷**——`COMPLETE` 状态词（F-OD01V4R-03）、
缺失 `90 §4` 头块（F-OD01V4R-02）、CI-4 自相矛盾（F-OD01V4R-04）、命名不一致（F-OD01V4R-05）、
字段改名（F-OD01V4R-06）、映射错误（F-OD01V4R-07/08）、Gap 记录两版并存（F-OD01V4R-09）、
`90 §5` 违规（F-OD01V4R-10）、自指路径错误（F-OD01V4R-11）**全部漏报**。
一份「未发现问题」的自审 + `READY FOR OWNER REVIEW` 建议，若被当作 Gate 前置证据，
将使 Owner 在没有独立复核的情况下批准 change set。

**建议（仅登记）**：撤回或改题（例如标为 `SELF-CHECK`）该文件；在 `Docs/REPORTS/` 保留的
自审不得承载 `CLOSURE BLOCKING` / `RECOMMENDATION` 类判定；OD-01-J 明列的「DSH 复核」须由
非产出方执行。

---

### F-OD01V4R-02（MED-HIGH）— 本轮唯一新增文档缺失 `90 §4` 强制 Status Header 与 `91 §5` 出生证明

**证据**

```text
90 `:368-370`  ## 4. Status Header 规范（强制）
               「**每份新文档必须以如下块开头**，使 Agent 无需猜测权威层级」
90 `:373-380`  强制字段 = Document Type / Authority Level / Status / Normative /
               Supersedes / Superseded By / Gate State Authority
91 `:157-177`  扩展为出生证明（+ Purpose / Derives From / May Change / Must Not Change）
91 `:195`      门槛 2：「出生证明齐备 —— `91 §5` 全部字段，**缺字段即不得创建**」

实况（新文件 `:3-14` 头块）：
  STATUS / SCOPE / SUBJECT / COMMIT / FROZEN SPEC TREE / VERDICT /
  CLOSURE BLOCKING / RECOMMENDATION
  → 缺 Document Type、Authority Level、Normative、Supersedes、Superseded By、
    Gate State Authority、Purpose、Derives From、May Change、Must Not Change（共 10 项）
  → `Document control`（`:80-87`）亦仅 Path/Status/Verdict/Subject HEAD
```

**影响**：本轮唯一**新建**文档（M×3 + A×1 中的 A）未通过 `91 §5.1` 门槛 2 与 `90 §4` 强制格式。
同时 `Authority Level` 缺失使 `90:47`（未归层 = 不得引用为权威）与
`docs_audit/authority_matrix.yaml` 的机器可检性下降。

---

### F-OD01V4R-03（MED-HIGH）— 禁用状态词修复不成立：`COMPLETE` / `NEXT` 实际出现，且 OD-01-H 指示的替代词本身违规

**证据（大小写敏感实测）**

```text
91 `:124` §3.2 禁止的状态词（新文档）
91 `:128` | **`COMPLETE`** | 模糊——完成什么？…现存量 6 份文档，历史保留，**新文档禁用** |
91 `:129` | **`DONE`** | 同上。现存量 1 份 |
91 `:131` | **`NEXT`** | 不是状态，是顺序。用 `Step n` 表达 |
91 `:109-122` §3.1 允许的状态值 = OPEN / PENDING / CONDITIONAL PASS / CLOSED /
             NOT STARTED / DEFERRED / SUPERSEDED / RETRACTED / ACTIVE / HISTORICAL

本轮实测：
  Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md
    :4   STATUS: TARGETED ADVERSARIAL REVIEW — COMPLETE        ← 新文档使用被禁词
    :85  | Status | COMPLETE — TARGETED ADVERSARIAL REVIEW |    ← 同上
  Docs/COORDINATION/OWNER-DECISIONS-…md
    :400 | OD-01-J | … | **PENDING NEXT ROUND** |              ← Status 值含被禁词 NEXT
    :398 | OD-01-H | APPROVED | 删除 `DONE` 状态词；用 ADDRESSED / VERIFIED / COMPLETED 等 |
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-…md
    :100 | `DONE` | `ADDRESSED` / `VERIFIED` / `COMPLETED` / `PENDING` / `NOT EFFECTIVE`（按实际） |
    :35-62 §0 表 Status 列 = `ADDRESSED` ×29
```

**质询**：`DONE` 确实从状态列消失（R-04 的字面目标达成），但

1. 被禁词 `COMPLETE` **新文档禁用**，而本轮新建文档正以它为 Status（`91 §3.2:128` 直接违反）；
2. 被禁词 `NEXT` 作为 D1 的状态值出现（`91 §3.2:131`）；
3. OD-01-H（`91 §3.2` 语境的「Owner Decision」）**指示**改用
   `ADDRESSED / VERIFIED / COMPLETED`：其中 `COMPLETED` 即被禁的 `COMPLETE` 的变体，
   `ADDRESSED` / `VERIFIED` **不在** `91 §3.1` 允许集合内。
   以 L2 记录扩充/改写 L0-META 的冻结状态词表，触碰 `90:107-110`（R1：任何 L2–L5 文档
   **不得**改写、扩充、或「事实上修订」L0 语义）。
4. 我方上一轮 F-OD01V3-03 的结论是「`DONE` 违反 `91 §3.2`」，修复后问题**迁移而非消除**。

---

### F-OD01V4R-04（MED-HIGH）— CI-4 的「可直接复制」Proposed Frozen Text 内部自相矛盾

**证据（Proposal v4 `:322-341`，被声明为可逐字写入 L0 的文本）**

```text
:325  - `granularity` ∈ {line, line_character}（M1；fragment 延后，见 00 §5）。
:326  - line_ref 必须存在于该 source_version；line_character 的 start/end_offset 必须能唯
:327    一定位"同行多题答案/单行多选项"场景。            ← 无条件要求 line_ref
:335      table_cell → 可验证 cell 身份与可回溯 raw（不要求 line_ref）；     ← 不要求 line_ref
:338      other → method + locator + 可独立验证回溯信息（不要求 line_ref）。
:339    禁止为满足旧 line 字段而伪造 line_ref。
:340    option_evidence_status=resolved 时 form 为 1..n；禁止 0-span 静默通过。
```

**矛盾**：`:326` 保留对**所有** span 的无条件「`line_ref` 必须存在于该 source_version」，
而 `:335`/`:338` 对 `table_cell` / `other`、「不要求 line_ref」；`:339` 只禁止**伪造**，
并未解除 `:326` 的存在性要求。三段同时写入 L0 后，`table_cell` span 将同时被要求具备
与不被要求具备 `line_ref`。这正是我方上一轮 F-OD01R-06 指出的同一处矛盾，
本轮**未被消解**，且被明确声明为「**可直接复制进入 Frozen Spec**」（`:205`）。

**加重**：`§5 Explicit Diff Appendix`（`:607-619`）对 `10 §8 2b/2c` 标注 Gate 为「四道门联动」，
却对 CI-4 的矛盾文本无任何保留说明；`§6`（`:625-640`）亦无。

---

### F-OD01V4R-05（MED-HIGH）— 字段重命名未进入 change set，且 `20 §5.5` 未列入受影响条款 → 采纳后将产生「两名一义」

**证据**

```text
L0 中字段名 `resolution_status` 的**唯一**出现处：
  20 `:317`  "text_hash": "<sha256>", "resolution_status": "exact",   （§5.5 Resolved Span 输出）
L0 中概念名 ResolvedStatus：
  20 `:394-395`  E `ResolvedStatus`（exact/normalized/contextual/fuzzy/ambiguous/missing/incomplete，§5）

Proposal v4：
  :116 | Provenance / span 解析 | **`span_resolution`**（= 现行 `20 §5.2` ResolvedStatus） | …
  :403   span_resolution（= ResolvedStatus，20 §5.2）—— provenance/span 解析质量；
  CI-4（`:306-347`，即重写 `20 §5.5` 的项）Proposed 文本 **未提及** `resolution_status` → `span_resolution`
  CI-4 的 Affected = `20 §5.5`；`00 §5`；`10 §8`
  CI-6 的 Affected = `20 §6.2`；`20 §5.2`；`10 §6.3`     ← **不含 `20 §5.5`**
  CR `:95` 「权威文本 = Proposal v4 §4 CI-1…CI-12 + §5 Explicit Diff Appendix」
```

**推演**：按 CR 指定的权威文本逐条应用后，L0 将在 `20 §5.5:317` 保留 `resolution_status`、
在 `20 §6.2` 新增 `span_resolution`，且**没有任何条款说明二者是同一字段的重命名**。
这正是该修复要消除的缺陷类别（§2.3 `:112`「禁止同名双 authority」/ `:121`）的镜像：
现在是**一义两名**。且该重命名属改变既有规定的行为（CHANGE-3 量级），却既未列 `20 §5.5`
为受影响条款，也未列出读取该字段的其他 L0 位置（`10 §6.3` JSONB 结构、`20 §8` 相关表行）。

---

### F-OD01V4R-06（MED）— 规范字段 `Authority Level` 被改名/替换以规避上一轮矛盾

**证据**

```text
规范字段名（强制）：
  90 `:375`  Authority Level: <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>
  91 `:167`  Authority Level:  <L0 | L0-META | L1 | L2 | L2-proposed | L3 | L4 | L5>

Proposal v4 `:7-8`：   Authority:             Owner Decision / Proposal Record
                       Registration Level:    Pending L1 Registration
CR-002  `:7-8`：       Authority:             Owner Decision / Proposal Record
                       Registration Level:    Pending L1 Registration
D1 `:379`/`:431`：     AUTHORITY: Owner Decision（…）

`Authority Level` 在本轮四文件中的出现仅为**否定示例**：
  Proposal `:109`  | Authority: Owner Decision / Proposal Record | 「Authority Level: L1」且同时写 NOT REGISTERED（逻辑冲突） |
  CR       `:38`   | Authority | **Owner Decision / Proposal Record**（非「Authority Level: L1」） |
```

**质询**：上一轮 F-OD01V3-10 是「头字段 `Authority Level: L1` 与 `NOT REGISTERED` 自相矛盾」。
本轮的处理是**删除该规范字段并另起 `Authority:` / `Registration Level:` 两个非规范字段**，
而不是把值改为合规形式（`91:167` 本已提供 `L2-proposed` 这类表达）。
问题因此不再显现，但**强制字段从头部消失**：`90 §4:370` 的强制块、`91 §5.1:195` 的门槛 2
（出生证明齐备）、`90:47` 的未归层判定、`authority_matrix.yaml` 的机检均受影响。
这与上一轮 F-OD01V3-01（以删除 Proposed 文本代替补全）属同一模式：**以移除问题载体代替解决问题**。

**同类第二处（类型名）**：CR 自述类型名 `Change Proposal Record`（`:5` / `:23` / `:199`）
不在 `90 §4:373-374` 与 `91 §5:165-166` 的 Document Type 枚举
（`Frozen Spec | Contract Change Record | Decision Record | Governance Meta-Spec |
Gate Report | Experiment Report | Status`）之内，而同一头块的 `Document Type:` 字段
（`:6`）写的是 `Contract Change Record（候选）`。即：**规范字段用旧值、非规范字段用新名**，
两者并存。若要确立新类型名，须走 `90 §3` 的 CHANGE 流程（并在 `90 §4`/`91 §5` 枚举内登记），
不能在 CR 自身文本中直接使用。

---

### F-OD01V4R-07（MED）— ID Mapping 表不完备且存在错配

**证据（Proposal v4 §0 `:31-65`，标题「ID Mapping（R-09）」）**

```text
:61 | F-OD01V3-09 | R-09 | — | ADDRESSED |
:62 | F-OD01V3-10 | R-10 | OD-01-C | ADDRESSED |
     → 表内**没有** F-OD01V3-11、F-OD01V3-12 两行（全仓检索 `F-OD01V3-11`/`F-OD01V3-12` = 0 命中）
:65 「**唯一编号原则：** 一个问题一个编号；本表为唯一映射。」

与 Remediation 语义对照（R-xx 语义见任务书文本）：
  F-OD01V3-03（`DONE` 禁用状态词）        → 表内标 R-03，而 R-03 = 「CR-002 = Change Proposal Record」
  F-OD01V3-04（未归层 / Governance Gap）  → 表内标 R-04，而 R-04 = 「`DONE` 已从状态列清除」
  F-OD01V3-05（Owner 权威不可核验）       → 表内标 R-05，而 R-05 = 「valid future registration path」
  F-OD01V3-07（字段命名冲突规避）         → 表内标 R-07，而 R-07 = 「Native / Adapter / Artifact 统一」
  F-OD01V3-08（`91 §3.1` 误引 ×3）        → 表内标 R-08，而 R-08 = 「resolved / unresolved / incomplete / reviewable」
```

**影响**：R-09 的目标是「ID Mapping 唯一」，实际结果是**两套编号互不指涉**：
读者无法从 `F-OD01V3-03` 找到真正处理它的 Remediation 项，也无法确认
`F-OD01V3-11/12` 是否被有意放弃。`F-OD01V3-11`（引文保真）在 v4 中**依然存在**（F-OD01V4R-12），
因此这不是「已知悉而放弃」，而是「未登记而遗漏」。

---

### F-OD01V4R-08（MED）— 引入第 7 套命名空间，且 `R-xx` 语义在仓库内无定义

**证据**

```text
本轮同时存在的 ID 空间：
  1  F-OD01-01…08             （第一轮 DSH，AITutorX 4b419bf）
  2  F-OD01R-01…10            （第二轮 DSH，AITutorX 8c2dca3）
  3  F-OD01V3-01…12           （第三轮 DSH，AITutorX 1e44017）
  4  OD-01R-01…10             （D1 `:288-313`）
  5  OD-01-A…J                （D1 `:374-400`）
  6  F-OD01V4-01…03           （本轮自审 `:44-46`）
  7  R-01…R-10                （Proposal §0 `:31-65`、D1 `:391-400` 引用）
仓库内对 `R-01…R-10` 的**语义定义**：无（仅在 Proposal §0 出现为「Remediation ID」列值，
不附含义；其含义只存在于未提交进仓库的任务书文本）
```

**相关规则**：AGENTS.md「不重编号历史 Decision（**用映射表**）」；`90 §1.2:89-90` 强调
引用坐标稳定。我方上一轮 F-OD01V3-09 登记 ID 空间三分的目的是**收敛**，
本轮映射表反而**新增**了第 7 套并列命名空间，且新增的一套在仓库内不可解释。

---

### F-OD01V4R-09（MED）— Gap 结论两版并存；`90:47` 未归层后果仍未登记

**证据**

```text
已更正处（CR `:61`）：
  「（修正 v3「Governance Gap / 无合法落点」表述：**不是**没有落点，而是 **当前不注册**…）」
  CR `:58`  CR-002 has a valid future registration path.
  CR `:45-50` 四条正式注册条件（Owner approval + Gate completion + Frozen Spec commit +
              90/91 governance registration）—— 与 90 `:79`（V3_SPEC 允许「新增 L1」）一致 ✓

未更正处（D1）：
  :304 | OD-01R-01 | … | 若无法合法登记 → **记 Governance Gap** | **ADDRESSED — REGISTRATION DEFERRED** |
  :315 ### OD-01R-01 — 正式 L1 落位判定（Owner 接受的 **Gap 路径**）
  :334 4. 既有目录模型内**没有**第二处正式 L1 registry。
  :342 CR-002 = L1 candidate / NOT RELEASED（对齐 67 先例）
  :343 REGISTRATION PATH = 有效未来路径；当前 Candidate only；intentionally deferred

全仓检索（本轮四文件）：`未归层` = **0 命中**
  90 `:47`  **未归层 = 不得引用为权威。**
  90 `:80`  `Docs/DECISIONS/` = L2（允许「解释与裁决」）——即先例 `67` 的落点位于
            90 `:64-75` 目录模型**之内**
```

**影响**：对方在 CR 中接受了我方上一轮的核心更正，却在 D1 同一主题下保留 v3 的
「Gap 路径 / 无第二 registry」表述，形成**同一事实两版并存**的治理记录；
且 `Docs/COORDINATION/**` 未归层（`90:47`）对本轮全部四份文件的后果仍未在任何文件中登记
——包括 D1 中自称 `BINDING FOR EXECUTION: YES` 的 OD-01-A…J。

---

### F-OD01V4R-10（MED）— 新文档违反 `90 §5 Rule 2`（禁止词升级，适用 L3/L4/L5）

**规则**

```text
90 `:397-401`  ### Rule 2 — 禁止词升级（L3/L4/L5）
               「下列词在 L3/L4/L5 中出现且**未引用 L0/L1** 即违规：
                 guarantee solved authority must shall forbidden 必须 不得 冻结」
90 `:403-404`  细化：`CLOSED` / `PASS` 不整体禁止——**必须引用 82 §3**
90 `:81`       `Docs/REPORTS/` = L3 / L4 / L2-proposed
```

**证据（实测，`Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md`）**

```text
:33  | Q9 | Native / Adapter / Artifact 是否统一？ | **是**（§3；等价语义 + 禁第二 authority） |
:46  | **F-OD01V4-03** | LOW | 四道门 Gate A–D 全部 PENDING，CHANGE-4/5 在门未过前不得 re-freeze | 保持 PENDING；禁止提前标 PASS |
全文 L0/L1 条款坐标引用：**无**（未出现 `00 §5` / `20 §5.3` / `90 §…` / `91 §…` 形式的坐标）
全文 `82 §3` 引用：**无**（而 `:46` 出现 `PASS`）
```

**影响**：`authority`（`:33`）、`不得`（`:46`）、`PASS`（`:46`）落在 L3/L4 文档中且无 L0/L1
或 `82 §3` 引用 → 按该机械扫描规则构成违规。这同时说明该文档既未声明自身层级
（F-OD01V4R-02），也未满足其所在层级的用词约束。

---

### F-OD01V4R-11（LOW-MED）— 新增文档的 `Path` 字段指向另一个仓库

**证据**

```text
实际落点（git）：Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md  （AITutors-v3）
文档自述 `:84`：| Path | `Docs/60_REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md` |
                `Docs/60_REPORTS/` 是 **AITutor-X** 的报告目录约定，AITutors-v3 内不存在该路径
```

**影响**：自指坐标错误。在 `90 §1.2:89-90`「引用坐标稳定」与 `91:179`「Derives-From 可机检」
的语境下，文档无法被机械定位；亦可能被误读为「该审查属于 AITutor-X 的 DSH 报告系列」，
从而与真正的独立审查报告混淆（加重 F-OD01V4R-01）。

---

### F-OD01V4R-12（LOW）— 「Current Rule」块保真度参差且未标注逐字/改写

**证据（逐字核对结果，详见附录 A）**

```text
逐字一致：CI-1（00 `:274-275`）、CI-3（20 `:280-281`）、CI-4（20 `:322-324`）、
          CI-5（20 `:368`）、CI-7（20 `:454-455`）、CI-8（20 `:523` 主体）、
          CI-10（10 `:632-634`）、CI-11（50 `:51` 行）
非逐字（但仍置于 fenced ```text 块内，未标注为改写）：
  CI-2 `:243-245` 仍省略 L0 `10:107` 的「依据 01 v0.3 收敛。」（上一轮 F-OD01V3-11 的同一处）
  CI-6 `:390-391` 为删减引用（丢掉 E 层 7 值枚举与 G 层取值），而该枚举正是 CI-6 改动的对象
  CI-9 `:491-492` 为**改写句**：L0 `10:628-630` 原文为
      「因 `source_span` 是 JSONB 而非 FK，以下**应用层 provenance invariant 必须由
        Resolver/Compiler/Gate 验证**，不假设数据库保证」
    而 CI-9 写成「source_span 是 JSONB，不是 FK。它是应用层 provenance invariant，由
        Resolver/Compiler/Gate 验证（§8 不变量 2a-2d）。」
```

**影响**：`90 §11` 的 Change Audit 以「Current → Proposed」为审计对；Current 块混入改写句
会使「本条究竟改了什么」不可机械核对。我方上一轮 F-OD01V3-11 因此**未被修复**
（且未出现在 ID Mapping，见 F-OD01V4R-07）。

---

### F-OD01V4R-13（LOW）— CI-12 与 CI-4 声明「同文」但实际不同文

**证据**

```text
CI-12 `:601`  **Affected Frozen Sections：** `20 §5.5` form 枚举；**与 CI-4 同文**。
CI-12 Proposed `:588-595`：含 image_region 的 figure/region 身份要求、无法确定时
   option_evidence_status=unresolved/incomplete、「fragment 不因本条纳入 form 枚举」
CI-4  Proposed `:324-341`：不含上述 image_region 段落
```

**影响**：两项均声明改 `20 §5.5`，其中一项宣称「与 CI-4 同文」。若同时采纳，
`20 §5.5` 将出现两段来源不同、内容不同的并行拟制文本，而 change set 未规定其合并方式
（拼接位置、先后、去重）。属 change set 内部归属不清。

---

## 5. R-01…R-10 处置再审计

| R | 自述 | 本轮实际 | 复核判定 |
|---|------|----------|----------|
| R-01 | ADDRESSED 完整六段式 + 缺口基线 | CI-1…CI-12 六段式齐备；§1 基线 16 行 | **已处置** |
| R-02 | ADDRESSED Proposed Frozen Text 可复制 | CI-4 三段自相矛盾；编码单位未定义；CI-12 归属不清 | **PARTIALLY** |
| R-03 | ADDRESSED CR-002 定位 | 表述已改；`Document Type` 字段仍为 `Contract Change Record（候选）` | **PARTIALLY** |
| R-04 | ADDRESSED `DONE` 已清除 | Proposal 状态列 ✅；新文档 `COMPLETE`、D1 `NEXT`、指示 `COMPLETED` | **不达标** |
| R-05 | ADDRESSED 有效注册路径 | CR `:58`/`:61` 明确更正 v3 结论 | **已处置** |
| R-06 | ADDRESSED degraded 排除 + 命名拆分 | 值域/分层写明；`answer_status` 既有性核实为真 | **已处置** |
| R-07 | ADDRESSED 三路径统一 | §3 三路径 + 4 不变量 | **已处置** |
| R-08 | ADDRESSED 四态唯一关系 | §2.5 明确 | **已处置** |
| R-09 | ADDRESSED ID Mapping | 遗漏 2 项、≥4 行错配、新增未定义命名空间 | **未达标** |
| R-10 | ADDRESSED Authority / Registration Level | 矛盾消除，但以移除规范字段实现 | **PARTIALLY** |

```text
R-01…R-10 复核汇总：已处置 5 / 部分已处置 3 / 不达标 2
（自述：ADDRESSED 10/10 —— 不成立）
```

---

## 6. change set 一致性推演（若按 CR 指定的权威文本逐条应用）

> CR `:95` 指定的唯一权威文本 = Proposal v4 §4（CI-1…CI-12）+ §5 Appendix。

| 推演项 | 结果 |
|--------|------|
| `20 §5.5` `line_ref` 要求 | **矛盾**：`:326` 无条件要求 vs `:335`/`:338` 不要求（F-OD01V4R-04） |
| `resolution_status` / `span_resolution` | **两名一义**：`20:317` 保留旧名，`20 §6.2` 新增新名，无重命名条款（F-OD01V4R-05） |
| `20 §5.5` form 文本归属 | **两段并行**：CI-4 与 CI-12 均声明改该节且自称「同文」实则不同（F-OD01V4R-13） |
| `10 §8` 2b/2c 与 CI-4 的联动 | `:612` 标「四道门联动」，但 2b 新文本（`:535-539`）已自行规定非 line form 的处理，与 §5.5 新文本重复规定同一事 → 双处规定、需明确单一权威 |
| `10 §6.3` JSONB「状态字段」 | CI-9 `:504-505` 允许 JSONB 承载「状态字段」，但未列出字段名清单，与 §2.3 的四命名未建立引用 → 采纳后 JSONB 内状态字段的许可范围不明 |
| `00 §5` / `10 §4` / `20 §5.5` 延后解除的边界 | CI-1/CI-2/CI-4 三处措辞互不引用同一解除条件，未声明三者是同一解除的三个投影 → 可被读为三次独立放宽（CHANGE-4 ×3） |
| `option_evidence_status` 的 L0 落点 | §2.3 规定命名与值域，但 CI-6（唯一把它写入文本的项）的 Affected 不含 `10 §6.3`/`10 §8` → 新增强制字段的 Schema 侧归属未登记（触及 OD-05「V3 Frozen Schema 不可由 Implementation 自行扩展」边界） |

---

## 7. 载体合规性矩阵（90 / 91）

| 规则 | 要求 | Proposal v4 | CR-002 | D1 OD-01-A…J | REPORTS 自审 |
|------|------|-------------|--------|--------------|--------------|
| `90 §4:373-380` 强制头块字段 | 7 字段 | ⚠️ `Authority Level` 被改名；+2 非规范字段 | ⚠️ 同左 | ⚠️ 自有块 | ❌ 缺 7/7 |
| `91 §5:170-173` 出生证明扩展 | +4 字段 | ✅ 齐备 | ✅ 齐备 | ❌ 无 | ❌ 无 |
| `91 §5.1:195` 门槛 2 缺字段即不得创建 | — | ⚠️ | ⚠️ | ⚠️ | ❌ 违反 |
| `90 §4:376` / `91 §5:168` Status 枚举 | 6 值 | ✅ `DRAFT` | ✅ `NOT RELEASED` | ❌ `RECORDED` / `PENDING NEXT ROUND` | ❌ `COMPLETE` |
| `91 §3.1:109-122` 允许状态值 | 10 值 | ❌ `ADDRESSED`×29 | ⚠️ | ❌ `ADDRESSED`×20 | ❌ `COMPLETE`/`VERIFIED` |
| `91 §3.2:124-132` 禁用状态词 | COMPLETE/DONE/FINISHED/NEXT/REVIEWED | ⚠️ `:100` 指示 `COMPLETED` | ⚠️ `:87` 同 | ❌ `NEXT`（`:400`） | ❌ `COMPLETE`×2 |
| `90 §5 Rule 2:397-401` L3/L4 禁用词 | 须引 L0/L1 | n/a（未归层） | n/a | n/a | ❌ `authority`/`不得`/`PASS` 无引用 |
| `90 §1.2:79-81` 目录落位 | V3_SPEC=新增 L1；REPORTS=证明状态 | ❌ 未归层 | ❌ 未归层 | ❌ 未归层 | ⚠️ 在 REPORTS 内但自称他仓路径 |
| `90:47` 未归层 = 不得引用为权威 | — | ❌ 未登记 | ❌ 未登记 | ❌ 未登记 | n/a |
| `90:107-110` R1 L2–L5 不得扩充 L0 语义 | — | ⚠️ `:100` 扩充状态词表 | ⚠️ | ❌ `:398` 同 | — |
| `90 §11:328-329` 登记义务 | L0 修改后强制 | 未触发 ✅ | CR `:19` 绑定未来 commit ✅ | — | — |

---

## 8. 本轮是否构成违规

**判定：构成对 L0-META 格式与状态词规则的违规（程序性），未构成对 Frozen Spec 内容的修改。**

| # | 违规 | 依据 | 涉及文件 |
|---|------|------|----------|
| V1 | 新建文档未使用 `90 §4` 强制 Status Header / `91 §5` 出生证明 | `90:368-370`（**强制**）、`91:195`（缺字段即不得创建） | REPORTS 自审 |
| V2 | 新文档使用被禁状态词 `COMPLETE`；D1 状态值使用被禁词 `NEXT` | `91:128`、`91:131`（**新文档禁用**） | REPORTS 自审 `:4`/`:85`；D1 `:400` |
| V3 | L2 记录指示扩充冻结状态词表（`ADDRESSED`/`VERIFIED`/`COMPLETED`） | `90:107-110` R1（L2–L5 不得改写/扩充/事实上修订 L0 语义） | D1 `:398`；Proposal `:100` |
| V4 | L3/L4 文档使用 `authority`/`不得`/`PASS` 而未引用 L0/L1 或 `82 §3` | `90:397-404` Rule 2（机械扫描规则，明示「即违规」） | REPORTS 自审 `:33`/`:46` |

**未构成的违规（须明确记录以免误判）**：

- Frozen Spec 未被修改（`b3eeb3e9…` 三点一致）；
- 未 re-freeze、未声称 Gate PASS、未声称 CR-002 已注册或已生效；
- 未修改 `90`/`91`/`82`/`84`，未新建治理文档（`91 §5.1:201-203` 未被触碰）；
- 未重编号或删除历史决策：D1 的 OD-01…OD-01R 原文保持，仅追加 OD-01-A…J；
- 未执行 Migration / Phase 1 / X3 / push。

---

## 9. 正面证实（P1–P14）

| # | 正面事实 |
|---|----------|
| P1 | **Frozen Spec 未变**：`b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f` 在 `2dc7a5e`/`86da69c`/`9bd6eca` 一致 |
| P2 | **隔离干净**：delta = 3 M（COORDINATION）+ 1 A（REPORTS）；全仓零 backend/schema/corpus/migration 变更 |
| P3 | **完整六段式 diff 已恢复**（上一轮 F-OD01V3-01 的主体）：CI-1…CI-12 每项均含 Current Rule / Problem-Limitation / **Proposed Rule（fenced，可复制）** / Reason / Impact / Affected Frozen Sections |
| P4 | **缺口基线表已恢复**（上一轮 F-OD01V3-02）：§1 共 16 行，逐项给出「现有能力 / 真缺口 / 延后 + 非目标」+ Frozen 依据 + 与 OD-01 关系，并附「分析依据（不得删除）」 |
| P5 | **`degraded` 明确排除出本轮**：§1 `:86`、§2.4（`:123-133`）、§5 `:678`、CI-12 Reason（`:597`）四处一致，且给出替代路径（`option_evidence_status ∈ {unresolved, incomplete}` / `span_resolution ∈ {fuzzy, ambiguous, missing, incomplete}` → review / fail closed）——上一轮 F-OD01V3-06 的正向收敛 |
| P6 | **命名拆分与既有词汇对齐**：`span_resolution`（= `20 §5.2` 7 值）、`option_evidence_status ∈ {resolved, unresolved, incomplete}`、`answer_status`、`semantic_status ∈ {ready, incomplete}`；其中 `answer_status` 的「既有三字段」主张经核实为**真**（`10:463`、`20:370`、`20 §8.3:642-655`、`00:319`） |
| P7 | **三路径统一 provenance 模型**（§3）：Native / Adapter / Artifact 三行 + 4 条汇聚不变量（ResolvedRun 唯一消费入口、Gate 只面对 Canonical IR、Artifact 不替代 Native authority、禁第二 semantic authority）——与 `90:426` R4、`90:464-474` H-C、`91:51` 一致 |
| P8 | **CR-002 定位表述已实质更正**：`Change Proposal Record` / `NOT EFFECTIVE` / `NOT REGISTERED AS L1` / `WAITING FOR FOUR-GATE APPROVAL` / 四条正式注册条件；CR `:61` 明确放弃 v3 的「无合法落点」结论 —— 上一轮 F-OD01V3-04 的核心更正被接受 |
| P9 | **四道门保持 PENDING**，`Proposal :644-649`、`CR :163-168`、`CR :170` 并明文禁止以 Proposal 完成或 DESIGN APPROVED 替代 Gate PASS |
| P10 | **逐字引用核对**：CI-1/CI-3/CI-4/CI-5/CI-7/CI-8/CI-10/CI-11 的 Current Rule 与对应 L0 文本一致（见附录 A）——引用总体可信，问题集中在少数改写块（F-OD01V4R-12） |
| P11 | **未引入 `options_unresolved`**：§1 `:87` 明确「不存在于 L0（tree `b3eeb3e9…` 无此字段）/ 禁止引入」，§2.5 `:159` 再次禁止并行布尔位 |
| P12 | **边界守持**：Frozen Spec / Frozen Contract / Production / Preprocessing / Schema / Corpus / Migration / Phase 1 / Re-freeze / Push(L0) 全部标 UNCHANGED 或 NOT EXECUTED，与 git 事实一致 |
| P13 | **命名不一致被主动披露**：§5 `:621` 与自审 F-OD01V4-02 均登记「任务书用语 `50_Interface_Contract` ↔ 仓库实名 `50_Migration_Assets.md`」并在 change set 中按实名登记 —— 属主动 provenance 披露 |
| P14 | **历史决策未被改写**：D1 仅追加 OD-01-A…J（`:374-422`），OD-01…OD-01R 原文与状态保持；Proposal/CR 保留 v3→v4 的 `Supersedes` 链（Proposal `:15`、CR `:15`） |

---

## 10. 局限（L-1 … L-6）

- **L-1** 未重跑任何测试基线、未执行四道门、未做 corpus 对比；本报告不对 Gate A–D 的最终结论作预判，
  仅确认其「PENDING」状态陈述为真。
- **L-2** 审查范围限于 OD-01 v4 / CR-002 / D1 OD-01-A…J 与新增自审文件；对 OD-02…G-02 只做
  「是否被改动」的一致性核对，不构成背书。
- **L-3** `git fetch` 在本环境不可用，`origin/main` 比较基于本地引用；AITutors-v3 依指令未推送，
  其远端状态未核验（本地 `ahead 8`）。
- **L-4** 本会话 `pwsh` 沙箱无法初始化（`SetNamedSecurityInfoW failed (Win32 5)`），所有命令在
  `danger-full-access` 下执行且**全部为只读命令**；未对 AITutors-v3 写入任何字节。
- **L-5** §6 的「change set 一致性推演」是**文本层推演**（把 CI-1…CI-12 当作已采纳文本后检查
  自洽性），不是对实现或 schema 的验证；实现层影响（例如读取 `resolution_status` 的代码）
  未核验，仅从 L0 受影响条款登记的完备性角度登记 F-OD01V4R-05。
- **L-6** `docs_audit/authority_matrix.yaml` 未逐条比对；如其中已登记 OD-01/CR-002 的层级或
  `Docs/COORDINATION/` 的归属，可能影响 F-OD01V4R-06/09 的严重度判定。
- **L-7** 本报告未对 `R-01…R-10` 的原始定义文本（仅存在于任务书输入）做独立核验，
  故 F-OD01V4R-07 的「错配」判定基于该输入中的 R 描述与 Proposal §0 的对照。

---

## 11. 最终判定

```text
OD-01 Proposal v4 + CR-002 candidate + D1 OD-01-A…J + REPORTS 自审
  = VERIFIED WITH FINDINGS

Closure Blocking = YES
  理由：
   (1) 被审方自撰、提交在被审仓库、并自declare 独立审查判定
       （VERIFIED WITH FINDINGS / CLOSURE BLOCKING: NO / READY FOR OWNER REVIEW），
       且该项被外层报告作为「对抗审查结论」呈现 —— 独立复核被产出方自我关闭
       （AGENTS.md：Provenance ≠ Quality Authority）；
   (2) 存在对 L0-META 的现行违规：90 §4 强制头块缺失、91 §3.2 禁用状态词
       （COMPLETE / NEXT）、90 §5 Rule 2（L3/L4 禁用词未引用）——
       须撤回或整改后方可进入 Owner 批准；
   (3) change set 存在若按「可直接复制」采纳即写入 L0 的矛盾文本
       （CI-4 line_ref；resolution_status ↔ span_resolution 两名一义）。

Recommendation = OWNER ACTION REQUIRED BEFORE CLOSURE

Findings = F-OD01V4R-01 … F-OD01V4R-13（13 项；已登记，未修复）
  HIGH      : F-OD01V4R-01
  MED-HIGH  : F-OD01V4R-02, F-OD01V4R-03, F-OD01V4R-04, F-OD01V4R-05
  MED       : F-OD01V4R-06, F-OD01V4R-07, F-OD01V4R-08, F-OD01V4R-09, F-OD01V4R-10
  LOW-MED   : F-OD01V4R-11
  LOW       : F-OD01V4R-12, F-OD01V4R-13

R-01…R-10 复核 = 已处置 5 / 部分已处置 3 / 不达标 2（自述 ADDRESSED 10/10 不成立）

Frozen Spec  = UNCHANGED（确认，tree b3eeb3e9…）
CR-002       = Change Proposal Record / NOT EFFECTIVE / NOT REGISTERED AS L1（确认）
Gate A/B/C/D = PENDING（确认）
Re-freeze / Phase 1 / Migration / Push(v3) = NOT EXECUTED / NOT ENTERED / NOT AUTHORIZED / 未推送（确认）
自审 F-OD01V4-01…03 不足以作为 OD-01-J 所要求的「DSH 复核」证据
```

### Re-freeze 前置条件（5 项，缺一不可）

1. **独立复核取代自审**：撤回或改题 `Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md`
   （至少移除 `CLOSURE BLOCKING` / `RECOMMENDATION` 判定与 `VERIFIED WITH FINDINGS` 措辞，
   改标 `SELF-CHECK`），并补齐 `90 §4` + `91 §5` 强制头块；OD-01-J 的「DSH 复核」由非产出方执行。
   （F-OD01V4R-01, F-OD01V4R-02）
2. **状态词合规收口**：清除 `COMPLETE` / `NEXT` / `RECORDED`；把 `ADDRESSED` / `VERIFIED` /
   `COMPLETED` 替换为 `91 §3.1` 允许集合内的值（如 `CLOSED — <范围>` 或 `ACTIVE`+引用证据）；
   D1 `:398` 的 OD-01-H 指示须相应修正，或另行走 Change Record 扩充状态词表。
   （F-OD01V4R-03）
3. **消解 CI-4 的矛盾文本**：把 `:326` 的 `line_ref` 要求限定为「line 系 form」，
   并明确非 line 系 form 的 locator 与 `text_hash` 口径；同时钉死 `char_span_in_line` 的
   字符编码单位（可在正文引用既有先例 `20:515` `text.encode("utf-8")` 与 `20:532-534`
   UTF-8 字节字典序，而非留作未决）。（F-OD01V4R-04）
4. **补全重命名与受影响条款**：在 change set 中显式规定 `resolution_status` → `span_resolution`
   的替换（属 CHANGE-3），并把 `20 §5.5`（`:317`）及其他读取该字段的 L0 位置列入受影响条款；
   明确 CI-4 与 CI-12 在同一节的合并归属。（F-OD01V4R-05, F-OD01V4R-13）
5. **恢复规范字段与 ID 收敛**：头块恢复 `Authority Level`（值用 `L2-proposed` 等不预设 L1 的形式）；
   修复 ID Mapping（补 F-OD01V3-11/12、纠正 ≥4 行错配、在仓库内给出 `R-xx` 语义定义）；
   统一 D1 与 CR 关于 L1 注册的表述，并登记 `90:47` 未归层后果。
   （F-OD01V4R-06, F-OD01V4R-07, F-OD01V4R-08, F-OD01V4R-09）

**非阻断跟进**：F-OD01V4R-10（自审文件补 L0/L1 与 `82 §3` 引用）、F-OD01V4R-11（Path 字段更正）、
F-OD01V4R-12（Current Rule 块标注逐字/改写，并补齐 CI-2/CI-9）。

---

## 附录 A — 逐字引用核对表

| 被审引文位置 | 引用 L0 坐标 | 核对结果 |
|--------------|--------------|----------|
| CI-1 `:211-214` | `00_Master_Spec.md:274-275` | ✅ 逐字一致 |
| CI-2 `:243-245` | `10_Data_Model.md:107-109` | ⚠️ 省略「依据 01 v0.3 收敛。」（F-OD01V4R-12） |
| CI-3 `:276-277` | `20_Document_Pipeline.md:280-281` | ✅ 逐字一致 |
| CI-4 `:311-313` | `20_Document_Pipeline.md:322-324` | ✅ 逐字一致 |
| CI-5 `:356` | `20_Document_Pipeline.md:368` | ✅ 逐字一致 |
| CI-6 `:390-391` | `20_Document_Pipeline.md:394-398` | ⚠️ 删减引用（丢 E 层 7 值与 G 层取值） |
| CI-7 `:426-427` | `20_Document_Pipeline.md:454-455` | ✅ 逐字一致 |
| CI-8 `:459-460` | `20_Document_Pipeline.md:523` | ✅ 一致（前缀「Question dedup_key =」） |
| CI-9 `:491-492` | `10_Data_Model.md:628-630` | ⚠️ 改写句（非 L0 原文） |
| CI-10 `:522-524` | `10_Data_Model.md:632-634` | ✅ 逐字一致（反引号略） |
| CI-11 `:556` | `50_Migration_Assets.md:51` | ✅ 一致 |
| §1 `:73-88` 基线判定 | `20 §5.5` / `10 §6.3` / `00 §5` / `10 §4` | ✅ 与 L0 状态相符（含 `options_unresolved` 不在 L0、`image_region` 无承载） |
| §2.3 `:118` `answer_status` 三字段「既有」 | `10:463` / `20:370` / `20 §8.3:642-655` | ✅ 主张为真 |
| §7 `:663-668` 四条注册条件 | `90:79`（V3_SPEC 允许「新增 L1」） | ✅ 一致 |

## 附录 B — 文件 / 坐标索引

```text
被审对象（AITutors-v3 @ 9bd6eca，只读）
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md   692 行（v4）
  Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md                   206 行
  Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md                  432 行
  Docs/REPORTS/OD-01-PROPOSAL-V4-TARGETED-ADVERSARIAL-REVIEW.md               87 行（本轮新增）

被引用冻结原文（AITutors-v3，只读）
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md  548 行  （§1 :36-47；§1.2 :60-90；R1/R2 :107-115；
                                                    §3 :342-364；§4 :368-383；§5 Rule 1-4 :387-430；
                                                    §11 :271-329）
  Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md  276 行  （§3.1 :109-122；§3.2 :124-132；§5 :157-177；
                                                    §5.1 :184-203）
  Docs/V3_SPEC/00_Master_Spec.md          406 行  （§5 非目标 :264-278；Answer 三字段 :319）
  Docs/V3_SPEC/10_Data_Model.md           793 行  （§4 :105-109；§6.3 :451-471 / answer_status :463；
                                                    §8 :625-649，含 2a-2d :631-635）
  Docs/V3_SPEC/20_Document_Pipeline.md    794 行  （§5.2 :256-270；§5.3 :275-294；§5.5 :308-341，
                                                    resolution_status :317；§6.1 :355-375；
                                                    §6.2 :383-399；§7.2 :452-455；
                                                    §7.3 :519-536；§8.3 :642-655）
  Docs/V3_SPEC/50_Migration_Assets.md             （:51 表格定位行）
  Docs/DECISIONS/69_ARCHITECTURE_REVIEW_ADJUDICATION.md  （§5 四道门 :399-431）
  Docs/DECISIONS/82_CONTRACT_AUTHORITY_RECONCILIATION.md （:3 / :153 Gate State Authority）
  Docs/DECISIONS/67_ANNOTATION_RESOLVER_BOUNDARY_ADJUSTMENT.md （L1 候选先例，位于目录模型内）

在先 DSH 独立审查（AITutorX，只读）
  Docs/60_REPORTS/OD-01-FROZEN-SPEC-PROPOSAL-DSH-ADVERSARIAL-REVIEW.md          （4b419bf；F-OD01-01…08）
  Docs/60_REPORTS/OD-01-V2-L1-CR-002-DSH-ADVERSARIAL-REVIEW.md                  （8c2dca3；F-OD01R-01…10）
  Docs/60_REPORTS/OD-01-V3-L1-CR-002-CANDIDATE-DSH-ADVERSARIAL-REVIEW.md        （1e44017；F-OD01V3-01…12）

本报告
  Docs/60_REPORTS/OD-01-V4-L1-CR-002-REMEDIATION-DSH-ADVERSARIAL-REVIEW.md
```

```text
— END OF REPORT —
审查者：DSH（独立对抗性审查；本报告作者未参与 OD-01 v4 任何产出）
被审方不得以本报告或任何自撰文件作为自身验证权威。
```
