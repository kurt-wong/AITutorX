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
Revision      : 4 (2026-09-28) — Owner 签发（§2–§5 的 PROPOSED 转为裁决）
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

映射表正文（rows）：本文不含；见 §7 后续 REQUIRED 步骤。
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
⇒ 本 Proposed 不含任何映射表正文。映射结果属 DQ-03 实质裁决，本文不预填。
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

不预填映射表正文：映射行（source_level → target_level）属后续实质裁决，本文不含。
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

*OWNER-DECISION-AUTHORITY-TAXONOMY-MAPPING-01 · SIGNED revision 4 · 2026-09-28 · Signed by kurt。
三层防护见 §0（非 Frozen / 非新层级 Authority Source / 非替代现有 Spec）。*
