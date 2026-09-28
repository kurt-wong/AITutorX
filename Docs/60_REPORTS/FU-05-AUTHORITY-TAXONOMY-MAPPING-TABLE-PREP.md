# FU-05 — Authority Taxonomy Mapping Table Preparation Record

```text
Document Type : Decision Preparation Record（非 Authority Decision）
Status        : OPEN
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 1 (2026-09-28)
Date          : 2026-09-28
Authority     : —（本文不构成任何 Authority）
Parent        : Docs/40_DECISIONS/OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md §6 追注 FU-05
Upstream      : Docs/40_DECISIONS/OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01.md（已签发 · 09f41cd）
                Docs/60_REPORTS/FU-01-AUTHORITY-TAXONOMY-MAPPING-PREP.md（@ ed35248）
Temporal Scope: Current-state facts verified as of 2026-09-28.
readers       : Owner（裁决方）；Migration Record 作者；Gate 2 / Gate 10 执行者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 非授权声明

```text
本文不是 Authority Decision。
本文不预填任何映射值 —— 所有 target_level 留空。
本文不重开 FU-01（表达规则 axis-qualified 与载体已裁，见 OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01）。
本文不重新设计 taxonomy。
本文不修改 V3 `90` / `91`。
本文不修改任何历史报告正文。
本文不关闭 CL-03 / 不修改冲突账本表体。
本文不触发 Migration / GF-007 / Gate 批准。
```

---

## 1. Scope

```text
本文范围（唯一）：

  Authority Taxonomy 映射表【正文（rows）】的决策输入。
  即为每一个【来源体系 + 来源轴 + 来源层级】确定规范解释。
```

**闭集边界（Owner 2026-09-28 确认，不做全仓盘点）**：

```text
· V3 权威层            8 行：L0 / L0-META / L1 / L2 / L2-proposed / L3 / L4 / L5
· DOC-GOV §9 已有行     4 行：L0 Frozen Spec / L0-META / L1 Contract Change / L2–L5
                              → 须裁决【保留 / 替换 / 废止】
```

**明确排除**：

```text
· README L0–L7          — X 侧自身层级，已定，无需映射
· GF-002 L1–L6          — 数据血缘轴；DQ-03-B 已要求 axis-qualified 记号，
                          不需要映射到 X 权威层
· V3 docs_audit/authority_matrix.yaml — V3 仓资产；受 V3 91 §5.1 冻结约束
· AITutors-v3 Docs/GOVERNANCE/ G0 四文件 — untracked / Class E；处置属 OD-008
· 状态词表 / 命名空间政策 / 目录重构 — 均不在本文范围
```

---

## 2. Frozen Facts

### 2.1 来源侧（V3）层级定义

```text
载体 : AITutors-v3/Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md §1（自标 L0-META）
       AITutors-v3/Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md（自标 L0-META）
```

| Level | 文档类型（90 §1 原文） | 例子（原文） |
|---|---|---|
| **L0** | Frozen Spec | `00` `10` `20` `30` `40` `50` |
| **L1** | Contract Change Record | `CR-003` · `CR-004`（2026-09-24 起 EFFECTIVE）；`67` 候选 NOT RELEASED |
| **L2** | Architecture Decision Record | `69` `70` `75` `80` `81` `82` `90`、Closure 记录 |
| **L2-proposed** | **仅见于 91 值域，90 §1 无此层** | `CR-002`；`FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE` |
| **L3** | Gate Report | `74` `80` §状态块 `81` §9 `83` §4 |
| **L4** | Experiment Report | `60`–`66` `68` `71`–`73` `76`–`79`、I-5-1 |
| **L5** | Status / log / restart | `Status.md` `log.md` `restart-prompt.md` `bugs.md` |
| **L0-META** | 治理元规范（**不在 90 §1 的 L0–L5 表内**） | `90`（谁说了算）· `91`（词是什么意思） |

**关键性质**：

```text
[FACT] 90 §1:51「未归层 = 不得引用为权威」
[FACT] 90 §1.1 提供旧 A–E 五层 → 新 L0–L5 的对应表（该体系自身已迁移过一次）
[FACT] 91 §5.1 出生证明四门槛；门槛 3 = Authority Level 必须 ∈ 90 §1 / 91 §1，
       【不得自创层级】
[FACT] 91 §5.1 额外约束：「DG 期间冻结新建治理文档」
```

### 2.2 目标侧（X）

```text
AITutor-X README §权威层级
  L0 Owner/System Decision · L1 Frozen Specification · L2 Cross-System Contract
  L3 Approved Architecture/Design · L4 Implementation · L5 Tests/Verification
  L6 Audit/Review · L7 Working Notes

同层序声明：AITutor-X/AGENTS.md「L0 > L1 > … > L7」
```

**本表不修改 README L0–L7**；它是映射的目标体系（DQ-01 = D 已裁）。
映射须以 **axis-qualified** 表达（DQ-03-A / DQ-03-B）。

### 2.3 `DOC-GOV §9` 已有 4 行（须裁决留废）

```text
载体 : AITutor-X/Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md §9「V3 Governance 对照表」
```

| # | V3 概念 | §9 现写目标 |
|---|---|---|
| §9-1 | L0 Frozen Spec | Frozen Spec（V3_SPEC）— Normative |
| §9-2 | L0-META | 本文档 |
| §9-3 | L1 Contract Change | Owner Decision |
| §9-4 | L2 / L3 / L4 / L5 | Informative / Historical Evidence |

**已裁事实**：

```text
[FACT] §9 已被裁【非】唯一映射权威，保留为 informational 输入（F3-B）
[FACT] §9 与 README 冲突：§9-3 把 V3 L1 Contract Change 映射到「Owner Decision」
       （X 的 L0 名）；而 README 中 Contract = L2 —— 同一仓内相差 2 级
[FACT] §9 与 R4 冲突：§9-4 把 V3 L2（Docs/DECISIONS/）归为 Informative /
       Historical Evidence；R4 将结论归 40_DECISIONS/、证据归 60_REPORTS/
```

### 2.4 血缘轴（不需映射，需限定记号）

```text
[FACT] GF-002 §1 的 L1–L6 是【数据血缘层】：
       L1 Source PDF → L2 OCR output → L3 Semantic annotation
       → L4 Question IR → L5 Admission Candidate → L6 AITutor-X Entity
[FACT] 与 README L0–L7 权威层共用 `L<n>` 记号（FU-01 §2.4 / C-08）
[FACT] 已裁：禁止裸 `L<n>`；须 `Authority-L3` / `Lineage-L3` / `Evidence-L3`（DQ-03-B）
⇒ 血缘轴【不进入】本映射表；只需在引用时使用 axis 限定记号。
```

### 2.5 C-01 — V3 内部 Authority Level 值域冲突【本轮关键】

#### 2.5.1 冲突本体

两个 L0-META 文档给出**不同的** Authority Level 值域：

```text
90_DOCUMENT_GOVERNANCE.md §4   （亲验 :593）
  <L0 | L1 | L2 | L3 | L4 | L5 | L0-META>

91_PROJECT_TERMINOLOGY.md:167
  <L0 | L0-META | L1 | L2 | L2-proposed | L3 | L4 | L5>
```

**差集 = `L2-proposed`（仅 91 有）。**

```text
· 已登记为 F-OD01V4R-59
    Docs/REPORTS/OD-01V4R-FINAL-REMEDIATION-REPORT.md:88
    Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md:26 / :139 / :179
· V3 定性：「既存的 Frozen / L0 治理基线冲突」（CR-002:67）
· V3 处置：【不修改 90/91，不消解】
· 台账义务落 AITutors-v3/Docs/DECISIONS/84_CONFLICT_LEDGER.md
  —— 该文件声明此项「超出本轮授权范围」⇒ 【未登记】
```

#### 2.5.2 对 `L2` 行的影响

```text
[FACT] 90 §1：L2 = Architecture Decision Record
       例 69 70 75 80 81 82 90、Closure 记录
       禁止「不得产生新的架构事实；超出裁决范围即失效」

[FACT] 91 在 L2 之外另设 L2-proposed
       ⇒ 同一「L2 家族」文档：按 90 无合法标签可写，按 91 可写 L2-proposed
```

**后果**：单一 `V3-L2 → X-L?` 行**不足以**覆盖实际出现的标签。

```text
若 L2 与 L2-proposed 视为【同一行】
    → 提案会被映射为与已裁 Decision 同层，等价于把「提案」升格为「裁决」

若视为【两行】
    → 须为 L2-proposed 单独决定目标层级，或其「未裁不得引用」规则
```

本文不预判。见 **DQ-05-02**。

#### 2.5.3 对 `L2-proposed` 行的影响 —— 在库实例

```text
实写该标签的 V3 文档（亲验）：
  Docs/COORDINATION/CONTRACT-CHANGE-RECORD-CR-002-OD-01.md:8
  Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md:8

CR-002:64 明写：
  「Authority Level | **L2-proposed** | 冻结枚举值 ——
    依据**仅为** `91 §5:167`（F-OD01V4R-59 归因分列）」

FROZEN-SPEC-CHANGE-PROPOSAL…:26 明写：
  「本文件 `L2-proposed` 的依据**仅为** `91 §5:167`。……
    两表值域不一致属未决依赖。不得自创层级。」
```

⇒ 这两个标签**只有 91 支撑**。若 X 侧映射只承认 90 的值域，则这两个标签**在映射上无源**。

#### 2.5.4 对 `L1` 行的影响 —— 注册态依赖

```text
[FACT] 90 §1：L1 = Contract Change Record，例 CR-003 / CR-004（2026-09-24 起 EFFECTIVE）
[FACT] CR-002:70 / :185 与 91 §5 门槛 3：
       禁止 Authority Level = L1，【除非已正式注册】
[FACT] 90:582：「63 若升 L0 → 待裁决（自称 Frozen Constraint ≠ 已是 L0）」
```

⇒ **V3 的层级标签带「注册态」依赖**：

```text
同一类文档（契约变更提案）
  未注册时 → 写 L2-proposed
  已注册时 → 写 L1
```

**后果**：建表口径不同，结果不同。

```text
按【标签】建行 → 须额外说明注册态差异
按【文档类型】建行 → 会漏掉「同一类型两种标签」
```

本文不预判。见 **DQ-05-03**。

#### 2.5.5 对 `L0-META` 行的影响 —— 不在阶梯内

```text
[FACT] 90 §1 的表只列 L0–L5；L0-META 仅出现在 90 / 91 的文件头与模板
       （90:593 · 91:167）
[FACT] 90 与 91 均自标 L0-META
[FACT] 语义 = 「治理元规范」（谁说了算 / 词是什么意思），
       【不是】「比 L0 更高的一层」
```

⇒ `L0-META` 需要的是「阶梯外 / 元层」的表达，而非 `target_level` 取 L0 之上。
DQ-03-A 的六字段是否足以表达，属 **DQ-05-04**。

#### 2.5.6 路径维度冲突（附带事实）

```text
[FACT] 90 §1.2 目录模型（DG-2 归位，2026-09-13 冻结）
[FACT] F-OD01V4R-59 另记：`Docs/COORDINATION/` 未归层
       vs `L2-proposed` 归 `Docs/REPORTS/`  ⇒ 目录层冲突
```

⇒ 携带 `V3-L2-proposed` 的文档**在 90 的目录模型中无家**。
这影响 `REPORT-I §6` Gate Step 1（source repo + commit + **path**）的可填写性。

### 2.6 来源标签实例清单（供建行时对照）

| # | 来源标签 | 实例（V3 仓内） | 90 §1 是否定义 | 91 值域是否含 |
|---|---|---|---|---|
| 1 | `L0` | `00` `10` `20` `30` `40` `50` | ✅ | ✅ |
| 2 | `L0-META` | `90` `91` | ❌（表内无） | ✅ |
| 3 | `L1` | `CR-003` `CR-004`；`67`（候选，NOT RELEASED） | ✅ | ✅ |
| 4 | `L2` | `69` `70` `75` `80` `81` `82` `90`、Closure 记录 | ✅ | ✅ |
| 5 | `L2-proposed` | `CR-002`；`FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE` | ❌ | ✅ |
| 6 | `L3` | `74` `80 §状态块` `81 §9` `83 §4` | ✅ | ✅ |
| 7 | `L4` | `60`–`66` `68` `71`–`73` `76`–`79`、I-5-1 | ✅ | ✅ |
| 8 | `L5` | `Status.md` `log.md` `restart-prompt.md` `bugs.md` | ✅ | ✅ |

> 第 2 / 5 行是**唯二在两个值域中不同源**的标签 —— 见 §2.5.1 / §2.5.5。

---

## 3. Decision Questions

### DQ-05-01 — 行集边界与兜底

**Facts**

```text
[FACT] 闭集 = V3 8 行 + §9 4 行（Owner 2026-09-28 确认）
[FACT] 90 §1:51「未归层 = 不得引用为权威」
[FACT] AGENTS.md 原则 2「UNKNOWN is retained data」—— 不得 silent skip / fallback
[FACT] 存在未归层实例：`Docs/COORDINATION/`（F-OD01V4R-59）；G0 四文件（OD-008 未裁）
```

| Option | 含义 |
|---|---|
| A | 8 行即为完整行集；未归层 / 未知标签**停止**（Gate Step 1 / 2 FAIL） |
| B | 8 行 + 一条显式 **UNKNOWN / 未归层兜底行**（不映射，标 `UNKNOWN`，不得 silent skip） |
| C | 8 行 + 未归层单独裁决（另立 follow-up） |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-05-02 — `L2` 与 `L2-proposed`

**Facts**：见 §2.5.2 / §2.5.3。

```text
· `L2-proposed` 只存在于 91 值域，90 §1 无此层
· 在库实写实例 2 份，且均声明「依据仅为 91 §5:167」
· 提案 ≠ 已裁 Decision（若同层映射，等于升格）
```

| Option | 含义 | 后果 |
|---|---|---|
| A | **同一行**：`L2` 与 `L2-proposed` 映射到同一 X 层级 | 提案与裁决同层 |
| B | **两行**：`L2-proposed` 单独一行，可映射到较低层级或标「未裁不得引用」 | 保留提案/裁决区分 |
| C | 两行，且 `L2-proposed` 行由 V3 侧先注册（本表暂留空） | 依赖 V3 动作 |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-05-03 — 建表口径：标签 vs 文档类型（注册态依赖）

**Facts**：见 §2.5.4。

```text
· 同一类文档（契约变更提案）：未注册 → `L2-proposed`；已注册 → `L1`
· CR-003 / CR-004 为已注册 L1 的唯一成员
· `63` 升 L0 待裁 ⇒ L0 行成员亦非封闭
```

| Option | 含义 | 后果 |
|---|---|---|
| A | 按**标签**建行（8 行），注册态写各行说明 | 行集稳定；须说明同一文档可能跨两行 |
| B | 按**文档类型 + 注册态**建行 | 覆盖完整；行集不对称，且成员随 V3 注册变动 |
| C | 按标签建行 + 另设「注册态」附加字段 | 行集稳定且可表达注册态；字段数增加 |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-05-04 — `L0-META` 的表达方式

**Facts**：见 §2.5.5。

```text
· `L0-META` 不在 90 §1 的 L0–L5 表内
· 它是「治理元规范」，不是 L0 之上的一层
· DQ-03-A 六字段为 source/target × system/axis/level
```

| Option | 含义 |
|---|---|
| A | 用 `target_level` 表达（需指定一个 X 层级值） |
| B | 用 `target_axis = meta`（或以 axis 区分），`target_level` 为空 |
| C | 六字段不足 → 需扩展字段（应避免，DQ-03-A 已裁六字段） |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-05-05 — `DOC-GOV §9` 已有 4 行的处置

**Facts**：见 §2.3。

```text
· §9 已裁【非】唯一映射权威（保留为 informational 输入，F3-B）
· §9-3 与 README 相差 2 级（V3 L1 Contract Change → 「Owner Decision」vs Contract = L2）
· §9-4 与 R4 冲突（V3 L2 → Informative/Historical Evidence vs 结论 → 40_DECISIONS/）
```

| Option | 含义 | 后果 |
|---|---|---|
| A | **保留** §9 原样（informational，不修） | 仓内并存第三张表；须声明效力边界 |
| B | **替换**：§9 各行由 FU-05 映射表取代，§9 降为历史记录 | 单一表；须 add-only 标注 §9 |
| C | **逐行裁决**（部分保留、部分替换） | 精度高；工作量大 |
| D | **废止** §9 表体 | 与「不删除旧文档」张力最大 |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C   ☐ D
逐行说明（如选 C）: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-05-06 — 映射表载体落地位置

**Facts**

```text
[FACT] DQ-03 = A 附限定：映射表置于 OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 【内】
[FACT] 该 Decision 已签发（09f41cd），当前【无】映射表节
[FACT] 该 Decision 当前【无】Follow-up Registry 节
```

| Option | 含义 |
|---|---|
| A | 在已签发 Decision 内**新增映射表节**（append-only，不动既有内容） |
| B | FU-05 裁决落为新 `OWNER-DECISION-*.md`，映射表置于其中（须先修订 DQ-03 的载体限定） |
| C | 映射表节 + 该 Decision 内同时补 Follow-up Registry |

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

## 4. 映射表骨架（逐行留空，不预填）

> **所有 `target_level` 留空待裁。** 本文不含任何映射结论。
> 字段依 DQ-03-A（axis-qualified 六字段）+ DQ-02（`mapping_decision_id`）。

### 4.1 V3 权威层 8 行

| # | source_system | source_axis | source_level | target_system | target_axis | target_level | mapping_decision_id |
|---|---|---|---|---|---|---|---|
| 1 | V3 | authority | `L0` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 2 | V3 | authority | `L0-META` | AITutor-X | `（待裁，见 DQ-05-04）` | `（待裁）` | 本 Decision |
| 3 | V3 | authority | `L1` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 4 | V3 | authority | `L2` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 5 | V3 | authority | `L2-proposed` | AITutor-X | `（待裁，见 DQ-05-02）` | `（待裁）` | 本 Decision |
| 6 | V3 | authority | `L3` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 7 | V3 | authority | `L4` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 8 | V3 | authority | `L5` | AITutor-X | authority | `（待裁）` | 本 Decision |
| 9 | `（未归层 / UNKNOWN）` | `（待裁，见 DQ-05-01）` | `UNKNOWN` | AITutor-X | `（待裁）` | `（待裁）` | 本 Decision |

### 4.2 `DOC-GOV §9` 4 行处置

| # | §9 行 | §9 现写目标 | 处置 |
|---|---|---|---|
| §9-1 | L0 Frozen Spec | Frozen Spec（V3_SPEC）— Normative | ☐ 保留 ☐ 替换 ☐ 废止 |
| §9-2 | L0-META | 本文档 | ☐ 保留 ☐ 替换 ☐ 废止 |
| §9-3 | L1 Contract Change | Owner Decision | ☐ 保留 ☐ 替换 ☐ 废止 |
| §9-4 | L2 / L3 / L4 / L5 | Informative / Historical Evidence | ☐ 保留 ☐ 替换 ☐ 废止 |

### 4.3 不进本表的轴（仅记号限定）

| 来源 | 轴 | 处置 |
|---|---|---|
| GF-002 `L1`–`L6` | `lineage` | **不映射**；引用时写 `Lineage-L<n>`（DQ-03-B 已裁） |
| README `L0`–`L7` | `authority` | **不映射**（X 侧自身） |

---

## 5. Non-goals

```text
FU-05 不做：

- Migration（任何资产迁入 active tree）
- GF-007 Charter 落盘
- Gate 批准 / Gate 激活 / F5 / F10 裁决
- 修改 Frozen Spec / GF-000～006 / V3 90、91
- 修改 README L0–L7 / DOC-GOV §9 正文（§9 处置须裁后方可执行）
- 关闭 CL-03 / 修改冲突账本表体
- 修改任何历史报告正文
- 重新盘点全仓 L* 用法
- 新增 OQ·BL·OD 编号体系
```

---

## 6. 影响面（若 FU-05 不裁）

```text
· REPORT-I §6 Gate 2（Authority identified）无法填写
· REPORT-I §6 Gate 10（`authority_level`）无值可填
· F4 子项 2 / 3 / 4 的 Charter schema 无法定稿 → GF-007 无法落盘
· F5 Gate 批准记录中的 `authority_level` 只能留悬空占位符

⇒ 若以「逐资产即席判定」代替，即违反 F3-B
  （映射须来自 Owner 授权的规则，非填写者判定）
```

---

## 7. 依赖关系

```text
FU-01（已裁 · 09f41cd）—— 表达规则 + 载体
   │
   ▼
FU-05（本文）—— 映射表正文 rows
   │
   ├──► DQ-05-06 决定载体落地（已签发 Decision 内 / 新 Decision）
   ├──► F4 子项 2 / 3 / 4  ──► GF-007 Charter 落盘
   ├──► F5 Gate 版本批准（`authority_level` 有实指）
   └──► F10 Set B
```

---

## 8. Owner Signature

```text
Decision:
☐ Accepted（接受本材料作为 FU-05 裁决输入）
☐ Rejected
☐ Revise

Signed: _______________
Date:   _______________
```

---

*FU-05 preparation record · 2026-09-28 · Not an Authority Decision. 映射值全部留空，属 FU-05 实质裁决。*
