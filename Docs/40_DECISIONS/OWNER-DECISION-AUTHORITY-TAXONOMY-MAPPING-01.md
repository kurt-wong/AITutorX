# OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01

```text
Document Type : Owner Decision Record（本仓 Owner Decision Authority）— **已签发 / SIGNED**
Status        : CLOSED
Decision State: APPROVED
Signature     : kurt
Signed Date   : 2026-09-28
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 6 (2026-09-28) — rev.4 = `b329f5a`（签发）+ `09f41cd`（令牌转换，已签发）；rev.5 追加附录 A；rev.6 附录 A 裁决完成（**APPROVED**）
Date          : 2026-09-28
Authority     : 本文件（Owner Decision Authority — Authority Mapping Rule）
Parent        : Docs/40_DECISIONS/OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md §6 FU-01
Input         : Docs/60_REPORTS/FU-01-AUTHORITY-TAXONOMY-MAPPING-PREP.md @ ed35248
Scope         : AITutor-X Authority Mapping Rule（映射解释规则层）
readers       : Owner（裁决方）；F4 Charter 子项作者；Migration Record 作者；CL-03 / X2-03 更新执行者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 签发状态声明（先读）

```text
本文已于 2026-09-28 由 Owner 签发（§8）。
§2 / §3 / §4 / §5 的 PROPOSED 已转为裁决。

· 本文不创建 Registry。
· §5 授权已生效（更新 CL-03 / X2-03 的 Current interpretation；边界见 §5）。
· 本文不创建 GF-007。
· 本文不修改 Frozen Spec / GF-000～006 / V3 90、91。
· 本文不修改任何历史报告正文。

三层防护（签发后仍适用）：
  ① 非 Frozen —— 本 Decision Record 不构成 Frozen Specification，
     不创建新的 Frozen Authority Layer，不得被引作 Frozen 依据。
  ② 非新层级 Authority Source —— 本 Decision 不产生新的 Authority Level、
     不定义层级划分；它只在既有体系【之上】提供映射解释规则。
     其效力来源 = Owner 裁决（GF-000:461），非自我声证。
  ③ 非替代现有 Spec —— 不取代 README L0–L7 / V3 90·91 / DOC-GOV §9；
     三者按 §2.3 各自保留，不被本 Decision 废除。

生效范围限定：
  本 Decision 生效 = Authority Mapping Rule 已批准。
  不意味着 Migration Ready / Gate Passed / Phase B Started（见 §6）。

映射表正文（rows）：rev.4 时点本文不含 Mapping Values；FU-05 rev.6 附录 A 纳入 Mapping Rule 与 Mapping Table。
```

---

## 1. Basis

```text
上游裁决 : OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md
           §2 F3-A（OD-03 射程不覆盖 L*）
           §3 F3-B（DOC-GOV §9 非唯一映射权威，保留为输入证据）
           §6 FU-01（本 Decision 为 REQUIRED follow-up）
输入材料 : FU-01-AUTHORITY-TAXONOMY-MAPPING-PREP.md @ ed35248
           §2.1 System A（V3 90/91）· §2.2 System B（README L0–L7）
           §2.3 System C（DOC-GOV §9）· §2.4 同符号异义轴（GF-002 L1–L6）
           §2.5 Existing Conflicts C-01～C-08
```

**计数口径声明**：

```text
本 Decision 将「定义体系」与「冲突证据」分离，不沿用 Prep 的来源计数。
· 定义体系（本 Decision 的处理对象）= 3 个：README L0–L7 / V3 90·91 / DOC-GOV §9
· 同符号异义轴（需限定记号，非独立体系）= GF-002 L1–L6（数据血缘层）
· 冲突证据（不构成体系）= REPORT-B §1/§3/§5/§6 的混用实例
```

**编号边界**：本文件不新增 GF-006 `OD-*` 编号，亦不新增 REPORT-E `OD-00*` 队列项
（依据 `GF-006 §9`：Agent 不得自行新增/关闭 Owner Decision）。

---

## 2. DQ-01 — Mapping Rule Authority

### 2.1 Facts

| 候选源 | 性质 | 已知问题 |
|---|---|---|
| `README` L0–L7 | AITutor-X 现行层级定义 | 与 V3 体系无映射规则；已被 REPORT-B 误用（C-05/C-06/C-07） |
| V3 `90` / `91` | 历史 Frozen 规范 | **C-01 内部值域冲突未消解**（`F-OD01V4R-59`；V3 侧明确「不修改 90/91，不消解」） |
| `DOC-GOV §9` | 迁移映射尝试 | 已裁非权威（C-02 / C-03 两处硬冲突） |
| 新建 Owner Decision | — | 尚无载体 |

```text
[FACT] 三个现有来源均已各自被证明不足以单独承载 Authority Level 映射。
[FACT] V3 91 §5.1 门槛 3：Authority Level 必须 ∈ 90 §1 / 91 §1，不得自创层级。
[FACT] V3 91 §5.1：DG 期间冻结新建治理文档。
```

### 2.2 Options

| Option | 含义 | 后果 |
|---|---|---|
| A | 以 `README` L0–L7 为唯一映射权威 | 须补建 V3 → README 映射规则；REPORT-B 误用无解 |
| B | 以 V3 `90` / `91` 为唯一映射权威 | **继承 C-01（值域冲突）**；且需 X 侧采纳 V3 仓规范 |
| C | 以 `DOC-GOV §9` 为唯一映射权威 | 与已裁 F3-B 冲突；须先修 C-02 / C-03 |
| D | 以**新建 Owner Decision** 承载 Authority Mapping Rule | 须防「新体系」与循环论证（见 §2.3） |

### 2.3 Proposed Decision

```text
[RULED — OWNER DECISION 2026-09-28]

D = AITutor-X Authority Mapping Rule 的承载权威为【新建 Owner Decision】。
    该 Decision 即本文件（签发后）。
```

**明确不是什么**（防新体系）：

```text
✗ 不是新建一个 Authority Taxonomy
✗ 不引入 X-L0 / X-L1 / X-L2 … 等新层级记号
✗ 不取代 README L0–L7 作为 X 现有层级的定义
✗ 不与 README / V3 90·91 / DOC-GOV §9 并列成为第 4 个体系

✓ 本 Decision 是【解释规则层（Mapping Rule Layer）】，
  位于现有体系之上，回答「历史 L* 如何被规范解释」，不回答「层级应如何划分」。
```

**防循环论证说明**：

```text
本 Proposed 的依据【不是】「因为它是唯一权威，所以要建立它」。

依据链：
  ① 三个现有来源各自不足以承载映射（§2.1 Facts）
  ② 迁移需要 Authority Level 的规范解释（REPORT-I §6 Gate 2 / Gate 10）
  ③ 故需要一个解释规则载体
  ④ 该载体的权威来源 = Owner 裁决本身（GF-000:461「决策 actor = Owner」）

⇒ 权威来自 Owner，不来自「唯一性」自证。
```

**三个来源的处置（Proposed）**：

```text
README L0–L7    = 保留为 X 现行体系定义（不废、不改）
V3 90 / 91      = 保留为历史 Frozen 规范 + 映射输入（不修改；C-01 不消解）
DOC-GOV §9      = 保留为 informational 输入（已裁非权威）
```

### 2.4 Owner Verdict

```text
☐ A   ☐ B   ☐ C   ☑ D
其他/限定: 无

Signed: kurt
Date:   2026-09-28
```

---

## 3. DQ-02 — Historical Label Preservation

### 3.1 Facts

```text
[FACT] AGENTS.md：不重编号历史 Decision（用映射表）。
[FACT] REPORT-B / X2.5-05 / CL-03 均为 tracked 历史证据，改写其标签 = 历史漂移。
[FACT] E-08 已确立：保留原标 + 映射追注。
```

### 3.2 Options

| Option | 含义 | 后果 |
|---|---|---|
| A | **保留原标 + 映射解释**（add-only） | 历史不漂移；须建立映射记录字段 |
| B | 重写历史标签 | 破坏 git history / migration evidence / provenance |
| C | 保留原标，不建立映射 | 歧义持续；Gate 2 / Gate 10 仍无依据 |

### 3.3 Proposed Decision

```text
[RULED — OWNER DECISION 2026-09-28]

A = Preserve Original Label + Mapping Annotation。

原则：
  source label          = immutable（原始事实）
  canonical interpretation = derived（决策结果）
```

**映射记录字段（三件）**：

| 字段 | 性质 | 说明 |
|---|---|---|
| `source_authority_level` | 原始事实（immutable） | 历史文档中实际书写的标签 |
| `mapped_authority_level` | 决策结果（derived） | 依本 Decision 得到的规范解释 |
| `mapping_decision_id` | 解释来源 | 指向本 Decision（`OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01`） |

**禁止**：

```text
✗ 以 mapped 值替换 source 值
✗ 在历史文档内就地改写标签（例：把 `V3 L0` 直接改为 `X L1`）
✗ 删除原标后仅留映射值
```

### 3.4 Owner Verdict

```text
☑ A   ☐ B   ☐ C

If A, mapping record fields:
  source_authority_level / mapped_authority_level / mapping_decision_id（见 §3.3）

Signed: kurt
Date:   2026-09-28
```

---

## 4. DQ-03 — Canonical Mapping Representation

### 4.1 DQ-03-A — 表示方式（Axis-qualified）

`[RULED — OWNER DECISION 2026-09-28]`

```text
映射以 axis-qualified 六字段表达：

  source_system : _______________
  source_axis   : _______________
  source_level  : _______________

  target_system : _______________
  target_axis   : _______________
  target_level  : _______________
```

**格式示例**（`[示例 — 非映射裁决]`，仅示范字段用法；映射值须另行裁决）：

```text
source_system = V3
source_axis   = authority
source_level  = L0

target_system = AITutor-X
target_axis   = authority
target_level  = L1
```

```text
⇒ 本 Proposed 不含映射表正文；映射结果见 FU-05 rev.6 附录 A。
```

### 4.2 DQ-03-B — 禁止裸 `L<n>`（硬规则）

`[RULED — OWNER DECISION 2026-09-28]`

**理由（Facts）**：

```text
[FACT] GF-002 §1 的 L1–L6 是【数据血缘层】：
       L1 Source PDF → L2 OCR output → L3 Semantic annotation
       → L4 Question IR → L5 Admission Candidate → L6 AITutor-X Entity
[FACT] README L0–L7 是【文档权威层】。
[FACT] 两者共用 `L<n>` 记号（FU-01 §2.4 / C-08）；X2.5-05-CONFLICT-LEDGER 未登记此轴。
```

**规则**：

```text
禁止：裸 `L<n>`
      ✗ L3

允许：axis-qualified
      ✓ Authority-L3
      ✓ Lineage-L3
      ✓ Evidence-L3
```

**适用范围**：

```text
· 新文档
· 迁移记录 / Migration Record 的 `authority_level` 字段
· 跨仓 / 跨体系引用
```

### 4.3 载体（Proposed）

**Facts**

现有候选容器：

```text
· DOC-GOV §9                                    — 人读表；已裁非权威（C-02 / C-03）
· AITutors-v3 docs_audit/authority_matrix.yaml  — 机器可读全表（V3 仓资产）
· README §权威层级                               — X 侧层级定义
· 本 Decision Record                            — 映射规则承载权威（DQ-01 = D）
```

**Options**

| Option | 含义 | 约束评价 |
|---|---|---|
| A | 新建独立 Decision 承载映射表（人读） | 符合「须另立 Mapping Decision」；须避免与 §9 形成第三张表 |
| B | 复用 `DOC-GOV §9`（先修 C-02 / C-03） | 不新增文档；但 §9 效力已降级为 informational |
| C | 复用 V3 `docs_audit/authority_matrix.yaml` | 机器可读；受 V3 `91 §5.1` 冻结约束，且为 V3 仓资产 |
| D | A + 机器可读副本（人读 / 机读双载体） | 精度最高；载体数最多 |

**Facts — 载体约束**：

```text
[FACT] AITutor-X   R1（每任务最多 1 份文档）/ §8B（60_REPORTS 膨胀已登记问题）
[FACT] AITutors-v3 91 §5.1（DG 期间冻结新建治理文档；
              再建治理文档须先证明 90/91/82/84 承载不了）
⇒ 两仓均有「不得以治理复制治理」约束。
```

**Proposed Decision**

```text
[RULED — OWNER DECISION 2026-09-28]

A（附载体限定）= 映射表置于【本 Decision Record 内】的映射表条款，
                 不另行新建第二份 Decision 文件。

理由：
  ① DQ-01 = D 已使本 Decision 成为 Mapping Rule 的承载权威；
     表随权威走，避免「权威在一处、表在另一处」的分裂。
  ② R1 / §8B 与 V3 91 §5.1 构成双重「不得以治理复制治理」约束。
  ③ B 不可用：§9 效力已由 F3-B 裁为 informational。
     C 不可用：V3 yaml 为 V3 仓资产，且受 V3 文档冻结约束，
                X 不应以他仓资产为自身权威载体。
  ④ D 暂不建立机器可读副本 —— 待出现实际消费者时另行评估，
     届时该副本按新治理资产单独处理。

映射表正文：rev.4 时点本文不含；FU-05 rev.6 附录 A 纳入 Mapping Rule 与 Mapping Table（10 行，全部取值已裁）。
```

### 4.4 多套历史体系共存规则（Proposed）

```text
[RULED — OWNER DECISION 2026-09-28]

· 不立即删除任何一个历史体系。
· Historical Authority Labels = Evidence
· Canonical Authority Mapping = Decision
```

### 4.5 Owner Verdict

```text
DQ-03-A 表示方式:
  ☑ 采用 axis-qualified 六字段
  ☐ 其他: —

DQ-03-B 禁止裸 L<n>:
  ☑ 采纳为硬规则
  ☐ 限定范围: —

DQ-03 载体:
  ☑ A   ☐ B   ☐ C   ☐ D
  （§4.3 Proposed = A 附「本 Decision 内」载体限定 —— Owner 接受该限定）

DQ-03 共存:
  ☑ 历史标签 = Evidence，规范映射 = Decision
  ☐ 其他: —

Signed: kurt
Date:   2026-09-28
```

---

## 5. CL-03 / X2-03 后续修正授权边界

`[RULED — OWNER DECISION 2026-09-28]`

**背景（Facts）**：

```text
[FACT] X2.5-05-CONFLICT-LEDGER.md:30 CL-03
       "Current authoritative interpretation" 列：「OD-03 为 AITutorX 叙事基准」
       → 已被 OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §2（OD-03 射程不覆盖 L*）推翻
       → 且 CL-03 只登记三套，未含 DOC-GOV §9

[FACT] X2-03-CONCEPT-TERMINOLOGY-MAP.md:154
       「OD-03 分层模型为准；执行状态仍 OPEN（OQ-GF-015）」
       → 同上失效
```

**授权范围（本 Decision 签发后）**：

```text
允许：
  ✓ 更新 CL-03 的 "Current authoritative interpretation" 列
  ✓ 更新 X2-03:154 的术语解释条目
  ✓ 在两者追加指向本 Decision 的 mapping_decision_id 追注

禁止：
  ✗ 修改 Conflict Ledger 的历史事实列 / 表体
  ✗ 重写 X2-03 的历史条目
  ✗ 关闭 CL-03（该冲突不因本 Decision 而消失）
```

**总规则**：

```text
Current interpretation : 可更新
Historical record      : 不可重写
```

**执行时点**：本 Decision **签发后**方可执行；未签发前不得改动 CL-03 / X2-03。

### Owner Verdict

```text
☑ 授权上述范围   ☐ 限定: —

Signed: kurt
Date:   2026-09-28
```

---

## 6. Non-Authorization Boundary

```text
本文（含签发后）不授权 / 不执行：

- 创建 Registry
- 修改 CL-03 / X2-03（授权边界见 §5；执行须待签发）
- 创建 GF-007
- Migration / Gate 批准 / F5 / F10 裁决
- 修改 Frozen Spec / GF-000～006 / V3 90、91
- 使本文件成为 Frozen 层 / 引本文件为 Frozen 依据
- 以本 Decision 取代 README L0–L7 / V3 90、91 / DOC-GOV §9
- 修改任何历史报告正文（REPORT-B / REPORT-G/H/I/K / REPORT-E 队列结论）
- 新增治理原则 / 新增 OQ·BL·OD 编号体系
```

---

## 7. Follow-up（本 Decision 签发后）

```text
本 Decision 已签发（2026-09-28）
   │
   ├──► CL-03 / X2-03:154 时效性更新（范围见 §5）
   ├──► F4 子项 2 / 3 / 4（Charter schema 依赖 Authority Level 语义）
   │        └──► GF-007 Charter 落盘
   ├──► 【REQUIRED】Authority Taxonomy Mapping Table（映射表正文 rows）裁决
   │        · 本 Decision 已定映射的【表达规则】与【载体】，但【不含任何映射行】
   │        · 未完成此步前，Gate 2 / Gate 10 对带 V3 标签的资产仍不可填
   │        · 不得以逐资产即席判定代替
   │          （否则违反 F3-B：映射须来自 Owner 授权的规则，非填写者判定）
   ├──► F5 Gate 版本批准（`authority_level` 的【表达规则】已定；具体映射值见上一步）
   └──► F10 Set B
```

> `[追注 2026-09-28 · rev.6]` 上列 **【REQUIRED】Authority Taxonomy Mapping Table** 步骤
> **已完成** —— 映射表已纳入本文件 **附录 A**（rev.5 形成 / rev.6 裁决 · APPROVED）。
>
> ```text
> 附录 A §A.1  = Mapping Rule（Row Identity / level-state 分离 / 字段名约束 / 值域 / 行扩展规则）
> 附录 A §A.2  = Authority Mapping Table（10 行，全部取值已裁）
> 附录 A §A.3  = Exceptions（EX-1～EX-6）
> 附录 A §A.4  = History Handling（H-1～H-7）
> ```
>
> 本追注**不改上列流程图文本**；该图保留为签发时快照。
> Gate 2 / Gate 10 的 `authority_level` 现已有可填依据。

---

## 8. Owner Signature

```text
Decision:
☑ Approved（本 Decision 生效，§2–§5 的 PROPOSED 转为裁决）
☐ Rejected
☐ Revise

Signed: kurt
Date:   2026-09-28

生效范围：Authority Mapping Rule 已批准。
          不意味着 Migration Ready / Gate Passed / Phase B Started。
```

```text
注：本 Decision 已于 2026-09-28 由 Owner 签发；§2–§5 的 PROPOSED 已转为裁决。
```

---

*OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 · revision 5 · 2026-09-28。
§1–§8 已签发（rev.4 · Signed by kurt）；附录 A 已裁决（rev.6 · **APPROVED**）。
三层防护见 §0（非 Frozen / 非新层级 Authority Source / 非替代现有 Spec）。*

---

## 附录 A — FU-05 Authority Mapping Table（rev.6）

```text
Section Status : APPROVED（`[OWNER DECISION 2026-09-28]` · 同 §8 签发人 kurt）
Revision       : rev.6（2026-09-28）
Authority      : 本附录（Owner Decision Authority — Authority Mapping Table）
授权依据       : Owner 2026-09-28 FU-05 授权（DQ-05-01～DQ-05-06）
                + Owner 2026-09-28 Mapping Table Draft 逐行裁决
Input          : Docs/60_REPORTS/FU-05-AUTHORITY-TAXONOMY-MAPPING-TABLE-PREP.md @ b8dce53
                 Docs/60_REPORTS/FU-05-SOURCE-AUTHORITY-STATE-DOMAIN-INPUT.md @ 9ce763a
```

> **不影响已签发部分**：§2–§5 与 §8 的签发效力（rev.4 · APPROVED · `Signed by kurt`）
> **不因本附录而改变**。本附录已于 rev.6 裁决（APPROVED）。
>
> `§0` 所述「映射表正文（rows）：本文不含」**在 rev.4 时点为准确表述**，
> 已于 rev.6 依 Owner 裁决校正为：
> 「rev.4 时点本文不含 Mapping Values；FU-05 rev.6 附录 A 纳入 Mapping Rule 与 Mapping Table。」
>
> **rev.5 → rev.6 变更**：附录状态 `PROPOSED — NOT FINAL` → `APPROVED`；
> §A.2 全部 `[DRAFT]` 提案经 Owner 逐行接受后移除前缀；`§0` 表述校正；`EX-5` 修正。

---

### A.1 Mapping Rule

#### A.1.1 Row Identity（DQ-05-03 = C）

```text
Row Identity =
  ( source_system, source_axis, source_level,
    source_authority_state, Registration Level )
```

| # | 字段 | 来源 | 性质 |
|---|---|---|---|
| 1 | `source_system` | DQ-03-A | Mapping Core |
| 2 | `source_axis` | DQ-03-A | Mapping Core |
| 3 | `source_level` | DQ-03-A | Mapping Core（ontology position） |
| 4 | `source_authority_state` | **FU-05 追加** | Row Identity Governance Metadata |
| 5 | `Registration Level` | **FU-05 追加** | Row Identity Governance Metadata |

**Mapping Core —— DQ-03-A 原六字段，保持不变**：

```text
source_system / source_axis / source_level
target_system / target_axis / target_level
```

**DQ-03-A Extension 登记（F-3）**：

```text
Original axis-qualified six-field template remains valid.

FU-05 introduces Row Identity supplementary governance fields:
  - source_authority_state
  - Registration Level

性质：Row Identity Governance Metadata
不改变 core mapping schema。
```

#### A.1.2 `level` / `state` 分离原则（DQ-05-02 = B · 读法 B = 归一化）

```text
level = ontology position       （是什么层级）
state = governance lifecycle    （该层级的治理状态）

二者【不可混用】。level 不携带 state。
```

**归一化后果**：

```text
`L2-proposed`  【不再】作为 source_level 取值
                 → source_level            = `L2`
                 → source_authority_state  = `proposed`
                 → Registration Level      = `NOT REGISTERED`
```

**理由（记录）**：

```text
若采读法 A（source_level = `L2-proposed` + state = proposed）：
  · level 自身携带 state
  · state 字段退化为重复信息
  · 后续 Resolver / Mapping Rule 无法稳定分离 ontology 与 lifecycle
```

#### A.1.3 字段名约束（F-1 / F-2）

**允许**：

```text
source_authority_level
source_authority_state
Registration Level
```

**禁止**：

```text
✗ semantic_status        —— 与 Frozen Spec 字段同名：
                             `20_Document_Pipeline.md:394`「值域冻结（BUG-V3-018 终裁）：
                             `semantic_status ∈ {ready, incomplete}`（仅此二值）」；
                             `AITUTORX-DOC-GOVERNANCE.md:220` 列为
                             「明确排除（**不得改动、不得重命名**）」
✗ registration_state     —— 改用 V3 既有术语 `Registration Level`
✗ registered_state       —— 同上
✗ status of registration —— 同上
✗ `L2-proposed` 作为 source_level 取值
```

#### A.1.4 State 字段值域（`source_authority_state` / `Registration Level`）

**`Registration Level` 值域**：

```text
仅沿用既有实例，不新增值域：
  NOT REGISTERED
  REGISTERED AS L1
```

**`source_authority_state` 值域**（`[OWNER DECISION 2026-09-28]`）：

```text
Definition:
  Lifecycle state of a source authority taxonomy label.
  It MUST NOT represent registration status, workflow status,
  decision status, semantic processing status, or gate status.

Allowed values:
  - proposed
  - established
  - deprecated
```

| 值 | 定义 |
|---|---|
| `proposed` | authority taxonomy label 已提出，但尚未成为稳定生效定义 |
| `established` | authority taxonomy label 已被治理确认，作为当前有效定义使用 |
| `deprecated` | authority taxonomy label 已不推荐继续使用，但历史记录仍保留 |

**语义域（Q1 = A）**：

```text
source_authority_state = 【taxonomy label 的生命周期状态】

不表示：
  · 来源对象治理生命周期（Q1 Option B）
  · Mapping 参与状态（Q1 Option C）
  · 文档流程状态
  · 注册状态（由 Registration Level 负责）
```

**与 `Registration Level` 正交（Q2 = 独立）**：

```text
二者【不可互推】。反例（Owner 2026-09-28 记录）：

Case A
  source_authority_state = `established`
  Registration Level     = `NOT REGISTERED`
  语义：taxonomy label 已被治理确认，但尚未进入正式 Registration

Case B
  source_authority_state = `proposed`
  Registration Level     = `REGISTERED AS L1`
  语义：新的 taxonomy 提案仍在提出阶段，但注册体系中已有对应旧版本 L1

⇒ source_authority_state ≠ Registration Level
```

> **注（转录说明）**：Owner 原文 Case A 使用 `accepted`；`accepted` 已在同一裁决中撤回
> （见下方「撤回的候选集」），故按同义改记为域内的 `established`。
> **替换不改变反例结构**（仍为「已被治理确认」对「未注册」）。

**撤回的候选集**（`[OWNER DECISION 2026-09-28]`）：

```text
撤回：{ proposed, accepted, superseded, retired }

  proposed    → 保留（进入批准值域）
  accepted    → 不采用
  superseded  → 不采用
  retired     → 不采用
```

**`source_authority_state` 明确排除**：

| 排除值 | 原因 |
|---|---|
| `ACTIVE` | V3 / X 双规则冲突（本附录 §A.1.3 / FU-05 输入 §2.8 M-1），不进入新字段 |
| `APPROVED` | decision / governance 语义 |
| `ACCEPTED` | 与既有 `ACCEPTED` / `EFFECTIVE` 组合冲突（`90:374`） |
| `EFFECTIVE` | 生效语义 |
| `PENDING` | workflow 状态（且为 `91 §3.1` 冻结值） |
| `VERIFIED` | verification 状态 |
| `SUPERSEDED` | 已冻结状态值（`91 §3.1:119`） |
| `RETIRED` | 非当前 taxonomy 术语体系 |
| `NOT REGISTERED` | `Registration Level` |
| `REGISTERED AS L1` | `Registration Level` |
| `READY` | `semantic_status` |
| `CLOSED` | decision / status |
| `semantic_status` 取值 | 该域值域已冻结（`20_Document_Pipeline.md:394`） |
| `gate_decision` 取值 | 独立域（`20_Document_Pipeline.md:397`） |

**相关风险（记录，不因本裁决消失）**：

```text
V3 侧另有未消解的 Status 值域冲突 ——
  `OD-01V4R-FINAL-REMEDIATION-REPORT.md:50`
    「`90 §4:376` 与 `91 §3.1` 值域不一致（`PENDING` 归属）→ 未决依赖」
  `:120`「OD-01-H 词汇 vs `91 §3.1` … 请 Owner 裁定二者关系」
本裁决的排除清单已避开该冲突；该冲突本身仍 OPEN。
```

#### A.1.5 UNKNOWN 兜底（DQ-05-01 = B）

```text
无法确认【来源体系】的标签
        ↓
UNKNOWN / UNMAPPED 行
        ↓
进入人工裁决

禁止：未知 → 自动归类

依据：AGENTS.md 原则 2「UNKNOWN is retained data」—— 不得 silent skip / fallback
```

#### A.1.6 Row expansion rule（`[OWNER DECISION 2026-09-28]`）

```text
Rows are split by authority state when the same source_level
contains multiple lifecycle states.

Row expansion does not introduce new taxonomy levels.
```

**中文含义**：行扩展只表达同一 `source_level` 下的不同 `source_authority_state`，
**不代表新增 authority level**。

```text
✗ `L1` → 两个 L1（新增层级）
✓ `L1` + `proposed`
  `L1` + `established`
```

**性质（记录）**：

```text
本规则【不是】新的 authority mapping rule，
而是【既有 normalization rule 的适用】（existing normalization rule application）。

依据：
  · source_level ≠ source_authority_state ≠ Registration Level（§A.1.2 / §A.1.4）
  · `L2-proposed` 已归一化为 `L2` + `proposed`（§A.1.2）
⇒ 同一原则必须适用于 `L1`。
```

**本轮适用结果**：`L1` 拆为两行（`established` / `proposed`），行集由 9 行增至 **10 行**。

---

### A.2 Authority Mapping Table

```text
[APPROVED — OWNER DECISION 2026-09-28]
source_authority_state 值域：{ proposed, established, deprecated }（§A.1.4）
本表 = 【结构 + 行集 + 映射值】。行集 = 10 行（`L1` 已按 §A.1.6 拆行）。
全表取值已裁，无待审提案。

provenance：rev.5 以 `[DRAFT]` 提出逐行 target 提案；
            rev.6 经 Owner 逐行接受，`[DRAFT]` 前缀已移除。
```

| # | source_system | source_axis | source_level | source_authority_state | Registration Level | target_system | target_axis | target_level |
|---|---|---|---|---|---|---|---|---|
| 1 | V3 | authority | `L0` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | authority | `Authority-L1` |
| 2 | V3 | **meta** | `L0` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | **meta** | **`NULL`** |
| 3 | V3 | authority | `L1` | `established` | `REGISTERED AS L1` | AITutor-X | authority | `Authority-L0` |
| 4 | V3 | authority | `L1` | **`proposed`** | **`TBD`** | AITutor-X | authority | `NULL` |
| 5 | V3 | authority | `L2` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | authority | `Authority-L3` |
| 6 | V3 | authority | `L2` | **`proposed`** | **`NOT REGISTERED`** | AITutor-X | authority | `NULL` |
| 7 | V3 | authority | `L3` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | authority | `Authority-L6` |
| 8 | V3 | authority | `L4` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | authority | `Authority-L5` |
| 9 | V3 | authority | `L5` | `established` | `—` ⁽ᵃ⁾ | AITutor-X | authority | `Authority-L7` |
| 10 | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | AITutor-X | `UNKNOWN` | `NULL` |

**注 (a)**：Registration Level 列的 `—` = 该概念**不适用**于该 level（该 level 非 Contract Change Record）。
此为**【适用性判断】，非既有事实**；如 Owner 认为应改为 `NOT REGISTERED`，请指出。

**已裁来源（rev.5 前即已确定）**：

```text
行 2   target_level = `NULL`（DQ-05-04）
行 4   source_authority_state = `proposed`（L1 拆行裁决，§A.1.6）
行 6   source_authority_state = `proposed` / Registration Level = `NOT REGISTERED`
       （DQ-05-02 = B / 读法 B）
```

**rev.6 逐行接受（原 `[DRAFT]` 提案 → 已裁 · `[OWNER DECISION 2026-09-28]`）**：

```text
行 1  V3 L0 Frozen Spec → `Authority-L1`
      README：L1 = Frozen Specification；
      REPORT-I §6:119 已把 V3 L0 Frozen Spec 送 `Docs/10_SPEC/`
      替代：`Authority-L0`（否决：L0 = Owner/System Decision，非 spec）

行 3  V3 L1 Contract Change（established）→ `Authority-L0`
      90 §1：L1 = 「修改 L0 的唯一入口」—— 其权限高于 L0 本体，
      对应 README L0 = Owner/System Decision
      【语义解释（Owner 2026-09-28 修正）】
        该映射表示：`L1 Contract Change` —— modifies —— `Authority-L0`
        【不是】`L1 < L0`
        【也不是】authority hierarchy ranking
      `§9-3` 原写「→ Owner Decision」，语义方向一致；
      差异属【标识符未编号化】，非冲突（见 §A.3 EX-5）

行 4  V3 L1（proposed，`67` 候选）→ `NULL`
      提案态未成立；防 `proposed` → canonical 自动升格（DQ-05-02 理由）

行 5  V3 L2 Architecture Decision Record → `Authority-L3`
      90 §1：L2 = Architecture Decision Record；
      README L3 = Approved Architecture / Design

行 6  V3 L2（proposed）→ `NULL`（同行 4）

行 7  V3 L3 Gate Report → `Authority-L6`
      90 §1：L3 = Gate Report「证明状态」→ README L6 = Audit / Review
      替代：`Authority-L5`（Tests / Verification）

行 8  V3 L4 Experiment Report → `Authority-L5`
      90 §1：L4 = Experiment Report「提供证据」→ README L5 = Tests / Verification
      替代：`Authority-L6`（Audit / Review）
      [注] 行 7 / 行 8 为全表**次不确定对**，Owner 可互换

行 9  V3 L5 Status / log / restart → `Authority-L7`
      90 §1：L5 = 项目管理与索引 → README L7 = Working Notes

行 10 UNKNOWN → `NULL` + 人工裁决（§A.1.5）
```

**未使用的域值**：

```text
`deprecated` —— 当前 10 行中无实例。
保留于值域中以备 taxonomy label 退役时使用（前向定义，非冗余）。
```

**行 2 说明**（DQ-05-04 = B）：

```text
`L0-META` 归一化 → source_axis = meta / source_level = L0
target_axis   = meta
target_level  = NULL
target 对象   = AITUTORX-DOC-GOVERNANCE.md（本文档级 meta authority 对象）

不创建 target_meta_object / target_reference / target_document 等额外字段。
```

**行注**：

```text
行 3 / 行 4 —— 同一 source_level = `L1`，按 §A.1.6 拆行
行 5 / 行 6 —— 同一 source_level = `L2`，由 source_authority_state 与
               Registration Level 区分（DQ-05-02 = B）
行 4       —— Registration Level = `TBD`：Owner 明示【不得】由
               `NOT RELEASED` 推得 `NOT REGISTERED`（发布状态 ≠ 注册状态）
行 10      —— 不自动归类（§A.1.5）
```

---

### A.3 Exceptions

| ID | 项 | 例外内容 | 依据 |
|---|---|---|---|
| **EX-1** | `L0-META` | 不在 90 §1 的 L0–L5 阶梯内 → 由 `source_axis = meta` 承载；`target_level = NULL`；**不扩展字段** | DQ-05-04 = B |
| **EX-2** | `L2-proposed` | 不是独立 level → 归一化为 `L2` + `proposed`；`proposed` **不得自动升格**为 canonical | DQ-05-02 = B / 读法 B |
| **EX-3** | `L1` 的注册态依赖 | 同一类文档：未注册时写 `L2-proposed`，已注册时写 `L1`；故 `L1` 行以 `Registration Level = REGISTERED AS L1` 为条件 | DQ-05-03 = C |
| **EX-4** | UNKNOWN / UNMAPPED | 不进自动映射；进人工裁决 | DQ-05-01 = B |
| **EX-5** | `DOC-GOV §9` | 保留，降为 **informational mapping reference**；不替换、不废止 | DQ-05-05 = A |
| **EX-6** | GF-002 `L1`–`L6` | 血缘轴，不进本表；引用时写 `Lineage-L<n>` | DQ-03-B（已裁） |

**EX-5 细节**

```text
§9 四行（全部【保留】）：
  §9-1  L0 Frozen Spec     → Frozen Spec（V3_SPEC）— Normative
  §9-2  L0-META            → 本文档
  §9-3  L1 Contract Change → Owner Decision
  §9-4  L2 / L3 / L4 / L5  → Informative / Historical Evidence

§9 效力 = informational mapping reference，【非】 mapping authority。

不替换：§9 不是权威，无可替换对象
不废止：不删除旧文档（AGENTS.md）
```

**EX-5 修正（`[OWNER DECISION 2026-09-28]`，rev.6）**：

```text
§9-3 的定性由「与 README 冲突」修正为：

  Contract Change → Owner Decision
  semantic direction consistent.
  Future normalization should use: Authority-L0 identifier.

⇒ §9-3【不是冲突】（原 C-02 定性过严）。
  其语义方向与本附录 §A.2 行 3 一致（`Authority-L0`）；
  差异属【标识符未编号化】（写名称而非编号），不是层级错位。

§9 表体仍未改动。
```

---

### A.4 History Handling

```text
[APPROVED — OWNER DECISION 2026-09-28]
```

| 规则 | 内容 |
|---|---|
| **H-1** | 历史标签 **immutable**（`source_authority_level` / 原标） |
| **H-2** | 规范解释 **derived**（`mapped_authority_level` / 本附录） |
| **H-3** | 禁止重写历史文档标签；禁止以 mapped 值替换 source 值 |
| **H-4** | `L2-proposed` 在**历史文档中保持原样**；仅【行】做归一化（EX-2） |
| **H-5** | `mapping_decision_id` = `OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01` |
| **H-6** | CL-03 / X2-03 的 `Current interpretation` 已于 `aca02e3` 更新；历史事实列未改 |
| **H-7** | 本附录**不关闭 CL-03**；多套体系仍并存 |

**rev.6 后状态**：

```text
FU-05 Mapping Table Draft  ——  已完成并经 Owner 逐行接受（rev.6）
rev.6 附录 A               ——  已裁决（APPROVED）
        ↓
后续：F4 子项 2 / 3 / 4 → GF-007 → F5 → F10
```

*附录 A 形成于 2026-09-28（rev.5）· 裁决于 2026-09-28（rev.6）· APPROVED · `[OWNER DECISION 2026-09-28]`。*
