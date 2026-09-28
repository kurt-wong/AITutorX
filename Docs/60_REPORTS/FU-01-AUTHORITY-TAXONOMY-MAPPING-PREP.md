# FU-01 — Authority Taxonomy Mapping Preparation Record

```text
Document Type : Decision Preparation Record（非 Authority Decision）
Status        : OPEN
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 1 (2026-09-28)
Date          : 2026-09-28
Authority     : —（本文不构成任何 Authority）
Parent        : Docs/40_DECISIONS/OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01.md §6 FU-01
Temporal Scope: Current-state facts verified as of 2026-09-28.
readers       : Owner（裁决方）；后续 Authority Taxonomy Mapping Decision 作者
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 非授权声明

```text
本文不是 Authority Decision。
本文不选择方案、不预填 Owner Verdict。
本文不含映射表正文（映射结果属 FU-01 实质裁决）。
本文不修改 Frozen Spec / GF-000～006 / V3 90、91。
本文不修改任何历史报告结论。
本文不触发 Migration / GF-007 / Gate 批准。
```

---

## 1. Scope

```text
本文范围（唯一）：

  Authority Level 的映射规则 ——
  「什么东西拥有定义 Authority Level 的权力，
    以及历史 L* 标签如何表达为映射。」

明确不属于本文范围：

  Governance Framework 重新设计
  新增治理原则 / 新增 OQ·BL·OD 编号体系
  文档物理迁移 / 目录重构
  状态词表修订
```

**范围风险提示**：`REPORT-I` 的 F3 行、`GF-005 OQ-GF-015`、`REPORT-H:30` 均把此问题表述为
「AITutor-X 采用哪一套层级」。若不加限定，该表述容易被扩张为「重新设计治理层级体系」。
本文按 FU-01 的限定范围回答映射问题，**不回答层级体系应如何设计**。

---

## 2. Frozen Facts

### 2.1 System A — V3 `90` / `91`（L0–L5 + L0-META）

```text
载体 : AITutors-v3/Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md（自标 L0-META）
       AITutors-v3/Docs/V3_SPEC/91_PROJECT_TERMINOLOGY.md（自标 L0-META）
```

| Level | 文档类型 | 例子（原文） |
|---|---|---|
| **L0** | Frozen Spec | `00` `10` `20` `30` `40` `50` |
| **L1** | Contract Change Record | `CR-003` · `CR-004` |
| **L2** | Architecture Decision Record | `69` `70` `75` `80` `81` `82` `90`、Closure 记录 |
| **L3** | Gate Report | `74` `80` §状态块 `81` §9 `83` §4 |
| **L4** | Experiment Report | `60`–`66` `68` `71`–`73` `76`–`79`、I-5-1 |
| **L5** | Status / log / restart | `Status.md` `log.md` `restart-prompt.md` `bugs.md` |
| **L0-META** | 治理元规范 | `90`（谁说了算）· `91`（词是什么意思） |

**关键性质**：

```text
· 90 §1.1 提供旧 A–E 五层 → 新 L0–L5 的对应表（体系自身已迁移过一次）
· 90 §1:51「未归层 = 不得引用为权威」
· 91 §5.1 出生证明四门槛；门槛 3 = Authority Level 必须 ∈ 90 §1 / 91 §1，【不得自创层级】
· 机器可读全表：AITutors-v3/docs_audit/authority_matrix.yaml（存在）
· 91 §5.1 额外约束：「DG 期间冻结新建治理文档」；再建治理文档须先证明 90/91/82/84 承载不了
```

### 2.2 System B — AITutor-X `README`（L0–L7）

```text
载体 : AITutor-X/README.md §权威层级
同层序声明 : AITutor-X/AGENTS.md「L0 > L1 > L2 > L3 > L4 > L5 > L6 > L7」
```

| Level | 含义 |
|---|---|
| L0 | Owner / System Decision |
| L1 | Frozen Specification |
| L2 | Cross-System Contract |
| L3 | Approved Architecture / Design |
| L4 | Implementation |
| L5 | Tests / Verification |
| L6 | Audit / Review |
| L7 | Working Notes |

### 2.3 System C — `DOC-GOV §9`（V3→X 名称映射表）

```text
载体 : AITutor-X/Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md §9「V3 Governance 对照表」
```

| V3 概念 | AITutorX 适配 |
|---|---|
| L0 Frozen Spec | Frozen Spec（V3_SPEC）—— Normative |
| L0-META | 本文档 |
| L1 Contract Change | Owner Decision |
| L2 / L3 / L4 / L5 | Informative / Historical Evidence |

**性质**：名称映射，**不是编号阶梯**（未给出 X L0–L7 编号）。
**效力**：已裁为**非唯一映射权威**、保留为输入证据之一（`OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §3`）。

### 2.4 同符号异义轴 — `GF-002` L1–L6（数据血缘层）

```text
载体 : AITutor-X/Docs/00_GOVERNANCE/GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md §1

L1 Source PDF → L2 OCR output → L3 Semantic annotation
→ L4 Question IR → L5 Admission Candidate → L6 AITutor-X Entity
```

```text
· 语义 = 数据血缘层深度，不是文档权威层级
· 与 README L0–L7 共用 `L<n>` 记号 → 引用时可歧义
· 实例：GF-002:235「L1–L6 层链」
        GF-003:51  `lineage_layer  # GF-002 层（L1–L6 / N/A for docs）`
        REVIEW/GF-003/02:36「不推翻 L1–L6 层链」← 指血缘层，非权威层
· CURRENT LEDGER 状态：`X2.5-05-CONFLICT-LEDGER` **未登记此轴**
```

### 2.5 Existing Conflicts

| ID | 冲突 | 两侧原文 | 状态 |
|---|---|---|---|
| **C-01** | **V3 内部：`90` ↔ `91` Authority Level 值域不一致** | `91:167` = `<L0 \| L0-META \| L1 \| L2 \| L2-proposed \| L3 \| L4 \| L5>`；`90 §4`（亲验 `:593`）= `<L0 \| L1 \| L2 \| L3 \| L4 \| L5 \| L0-META>`。两份**同为 L0-META** | **UNRESOLVED**（已登记 `F-OD01V4R-59`） |
| **C-02** | `§9` ↔ `README`：编号/命名错位 | §9 将 V3 `L1 Contract Change` 映射到「Owner Decision」（X 的 L0 名）；README 中 Contract = **L2** | 已裁：§9 非唯一映射权威 |
| **C-03** | `§9` ↔ `DOC-GOV R4`：归属冲突 | §9 将 V3 `L2（Docs/DECISIONS/）` 归为 Informative / Historical Evidence；R4 将结论归 `40_DECISIONS/`、证据归 `60_REPORTS/` | 已裁：同上 |
| **C-04** | V3 内部：目录层冲突 | `Docs/COORDINATION/` 未归层 vs `L2-proposed` 归 `Docs/REPORTS/` | **UNRESOLVED**（同 `F-OD01V4R-59`） |
| **C-05** | `REPORT-B §1` 断言「Frozen Specification（L1 — **权威最高**）」 | README：L0 = Owner/System Decision 才是最高；L1 ≠ 最高 | 未登记 |
| **C-06** | `REPORT-B §3` 在标题「（L2–L7）」的节内给 V3 文档标 **`L0-META`** | 同表混用 System A 与 System B 记号 | 未登记 |
| **C-07** | `REPORT-B §6` 给 Producer `governance/*.md` 标 `L2` | System A 的 L2 = Architecture Decision Record；System B 的 L2 = Cross-System Contract。**两者都不解释 Producer 治理文件** | 未登记 |
| **C-08** | 同符号异义：`GF-002` L1–L6（血缘层）与 README L0–L7（权威层）共用 `L<n>` | 见 §2.4 | 未登记 |

**C-01 / C-04 补充事实（`[FACT]`）**：

```text
· 定性：CR-002:67 称其为「既存的 Frozen / L0 治理基线冲突
        （pre-existing Frozen/L0 governance baseline conflict）」
· V3 侧明确处理方式：「非 OD-01 规范缺陷；【不修改 90/91，不消解】」
· 台账义务：落 AITutors-v3/Docs/DECISIONS/84_CONFLICT_LEDGER.md
            —— 该文件声明此项「超出本轮授权范围」⇒【未登记】
```

### 2.6 已登记载体的时效性

| 载体 | 内容 | 时效性 |
|---|---|---|
| `X2.5-05-CONFLICT-LEDGER.md:30` **CL-03** | 登记三套（README L0–L7 / V3 90 L0–L5 / REPORT-B 自用）；**未含 `DOC-GOV §9`**；"Current authoritative interpretation" 列写「**OD-03** 为 AITutorX 叙事基准」 | **STALE** — OD-03 射程已裁为**不覆盖 L***（`OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §2`），该列读法已被推翻 |
| `X2-03-CONCEPT-TERMINOLOGY-MAP.md:154` | `\| L0–L7 \| 多套层级体系 \| OD-03 分层模型为准；执行状态仍 OPEN \|` | **STALE** — 同上 |
| `X2-01-UNIFIED-SYSTEM-BASELINE.md:150` **C-X2-03** | 登记三套 | 仍成立（但同样未含 §9） |
| `GF-005 OQ-GF-015` | 「AITutor-X 采用哪套层级（多套 L* 叙述 vs V3 90/91 vs AGENTS.md）？」 | **OPEN-BLOCKING**（仍准确） |
| `REPORT-H:30` | 已提出三问：「采用哪一套层级为唯一标准？」「历史文档中的 L* 标签如何重映射？」「是否禁止新文档混用未声明的层级体系？」 | 与 §3 的 DQ-01 / DQ-02 / DQ-03 **同构**（未被裁定） |
| `REPORT-B §1/§3/§5/§6` | 混用实例（tracked） | 历史报告，**不修改**；作为 C-05/06/07 的证据 |

> **注**：CL-03 与 X2-03:154 的更新**不在本文范围**（属历史表体/结论），
> 但 FU-01 完成后必须处理 —— 否则仓内会同时存在「已裁旧读法」与「已裁新裁决」。

---

## 3. Decision Questions

### DQ-01 — Mapping authority source？

```text
问：AITutor-X 最终采用哪一个 Authority Level 定义源？
```

**候选（Frozen Facts §2.1–2.3）**：

| 候选 | 性质 | 已知问题 |
|---|---|---|
| A. `README` L0–L7 | X 当前描述 | 与 V3 体系无映射规则；REPORT-B 已证明被误用 |
| B. V3 `90` / `91` | 历史 Frozen 规范 | **C-01 内部值域冲突未消解**；且为 V3 仓规范，X 无采纳记录 |
| C. `DOC-GOV §9` | 迁移映射尝试 | 已裁非权威（C-02 / C-03 两处硬冲突） |
| D. 新建 Mapping Decision | 未来唯一规则 | 尚无载体 |

`[OWNER POSITION 2026-09-28 — NOT YET RULED]`

```text
倾向：新建 Mapping Decision 成为唯一 Authority Mapping Source。
理由（Owner 记录）：README 与 DOC-GOV §9 都已证明存在冲突。
```

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C   ☐ D
其他/限定: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-02 — Historical label preservation？

```text
问：历史文档中既有的 L* 标签如何处理？
```

| Option | 含义 | 后果 |
|---|---|---|
| A | **保留原标 + 映射追注**（add-only） | 历史不漂移；须建立映射记录字段 |
| B | 重写历史标签 | 与 `AGENTS.md`「不重编号历史 Decision」同类禁令冲突 |
| C | 保留原标，不建立映射表 | 歧义持续；Gate 2 / Gate 10 仍无依据 |

`[OWNER POSITION 2026-09-28 — NOT YET RULED]`

```text
倾向：A —— Original Label Preservation + Mapped Target Annotation。
记录形态（Owner 拟）：
  source_authority_level : V3-L0
  mapped_authority_level : X-L1
  mapping_record         : FU-01

明确禁止：把历史文档中的 `V3 L0` 直接改为 `X L1`（属篡改历史）。
```

> **注**：Owner 在表述中给出的 `V3-L0 → X-L1` 与 `REPORT-I §6:119`（`L0 Frozen Spec（V3）`
> 迁移至 `Docs/10_SPEC/`）一致。**本文不预填具体映射值**，仅记录该示例为 Owner 陈述。

**Owner Verdict**

```text
☐ A   ☐ B   ☐ C

If A, mapping record fields: _______________

Signed: _______________
Date:   _______________
```

---

### DQ-03 — Canonical mapping representation？（含多套历史体系共存规则）

```text
问（a）：映射表由什么载体承载？
问（b）：多套历史体系如何共存？
```

**现有候选容器**：

```text
· DOC-GOV §9                          — 人读表；已裁非权威（C-02 / C-03）
· AITutors-v3/docs_audit/authority_matrix.yaml — 机器可读全表（V3 侧）
· README §权威层级                     — X 侧层定义
· 新建 Decision Document               — 尚无
```

**（a）载体的已知约束**：

```text
· AITutor-X  R1（每任务最多 1 份文档）/ §8B（60_REPORTS 膨胀为已登记问题）
· AITutors-v3 91 §5.1（DG 期间冻结新建治理文档；
              再建治理文档须先证明 90/91/82/84 承载不了）
⇒ 两仓均有「不得以治理复制治理」的约束
```

| Option | 含义 | 约束评价 |
|---|---|---|
| A | 新建独立 Decision Document 承载映射表 | 符合「须另立 Mapping Decision」；须避免与 §9 形成第三张表 |
| B | 复用 `DOC-GOV §9`（先修 C-02 / C-03） | 不新增文档；但 §9 已被裁非权威，复用需先恢复其效力 |
| C | 复用 V3 `docs_audit/authority_matrix.yaml` | 机器可读；但受 V3 91 §5.1 冻结约束，且为 V3 仓资产 |
| D | A + 机器可读副本（人读 / 机读双载体） | 精度最高；载体数最多 |

**（b）共存规则**

`[OWNER POSITION 2026-09-28 — NOT YET RULED]`

```text
倾向：不立即删除任何一个历史体系。
裁决形式：
  Historical Authority Labels  = Evidence
  Canonical Authority Mapping  = Decision
```

**Owner Verdict**

```text
(a) 载体: ☐ A   ☐ B   ☐ C   ☐ D

(b) 共存: ☐ 历史标签 = Evidence，规范映射 = Decision
          ☐ 其他: _______________

Signed: _______________
Date:   _______________
```

---

## 4. Non-goals

```text
FU-01 不做（明确排除）：

- Migration（任何资产迁入 active tree）
- GF-007 Charter 落盘
- Gate 批准 / Gate 激活
- F5 / F10 裁决
- 修改 Frozen Spec / GF-000～006
- 修改 V3 `90` / `91`（V3 侧已明确「不修改 90/91，不消解」）
- 修改历史报告结论（CL-03 表体、REPORT-B 正文、REPORT-G/H/I/K 结论）
- 新增治理原则 / 新增 OQ·BL·OD 编号体系
- 目录重构 / 文档物理迁移
- 状态词表修订
```

---

## 5. 影响面（若 FU-01 不裁）

```text
· REPORT-I §6 Gate 2（Authority identified）无法填写
· REPORT-I §6 Gate 10（`authority_level`）无权威依据
· F4 子项 2/3/4（Charter schema）无法定稿 → GF-007 无法落盘
· F5 Gate 批准记录中的 `authority_level` 字段只能留悬空占位符
· CL-03 / X2-03:154 的已过时读法持续在库
```

---

## 6. 依赖关系

```text
FU-01（本材料）
   │
   ▼
Authority Taxonomy Mapping Decision（Owner 裁决）
   │
   ├──► F4 子项 2 / 3 / 4  ──► GF-007 Charter 落盘
   ├──► F5 Gate 版本批准（`authority_level` 有实指）
   └──► CL-03 / X2-03:154 时效性更新
```

**约束**：FU-01 必须先于 F5 完成（`OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 §5`）。

---

## 7. Owner Signature

```text
Decision:
☐ Accepted（接受本材料作为 FU-01 裁决输入）
☐ Rejected
☐ Revise

Signed: _______________
Date:   _______________
```

---

*FU-01 preparation record · 2026-09-28 · Not an Authority Decision. 映射结果属 FU-01 实质裁决，本文不预填。*
