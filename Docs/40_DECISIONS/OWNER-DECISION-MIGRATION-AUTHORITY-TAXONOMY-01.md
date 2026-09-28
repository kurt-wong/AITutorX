# OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01

```text
Document Type : Owner Decision Record（本仓 Owner Decision Authority）
supersedes    : —
superseded_by : —
readers       : MIMO CODE；DSH；后续 Migration Authority 行使者；Authority Taxonomy Mapping Decision 作者
Status        : CLOSED
Decision State: APPROVED
Date          : 2026-09-28
Authority     : 本文件（Owner Decision Authority）
Parent        : Docs/60_REPORTS/REPORT-I-P0-DECISION-PREPARATION-01.md（revision 3 · 2ad1eea）
Scope         : REPORT-I §2.1 P0 Cluster A — F4 Migration Authority + F3 Authority Taxonomy
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

**Authority**：本文件是 **F4（Migration Authority）** 与 **F3（Authority Taxonomy）** 裁决的唯一权威来源。

```text
任何 "Owner said" / "Owner approved" / "Owner direction" 关于 F4 / F3 者，必须引用本文件。
禁止以聊天记录作为唯一权威来源。
```

**Hard rule**：

```text
本文件下裁决 ≠ Migration 授权
本文件下裁决 ≠ Phase B 授权
本文件下裁决 ≠ 实现授权
本文件下裁决 ≠ Frozen Spec 修订
本文件下裁决 ≠ GF-007 Charter 正文已落盘
```

**编号边界**：本文件**不新增** GF-006 `OD-*` 编号，亦不新增 REPORT-E `OD-00*` 队列项
（依据 `GF-006 §9`：Agent 不得自行新增/关闭 Owner Decision）。

---

## 0. Input Basis

```text
Decision input : Docs/60_REPORTS/REPORT-I-P0-DECISION-PREPARATION-01.md
                 Revision 3（2026-09-28），commit 2ad1eea
Upstream       : Docs/60_REPORTS/REPORT-I-MIGRATION-GATE-DEFINITION.md（as-of 2026-09-17）
Ruling order   : F4 → F3（本轮）；F5 / F10 延后（见 §5）
```

本文件仅转录 Owner 于 2026-09-28 作出的裁决；未增加、未删除、未改写任何裁决内容。

---

## 1. Decision F4 — Migration Authority

`[OWNER DECISION]`

```text
Option A — 设立 Migration Authority。
Migration Authority = Owner（本人）。
授权落盘：Docs/00_GOVERNANCE/GF-007-MIGRATION-AUTHORITY-CHARTER.md
```

**依据（既有已裁事实）**：

| 来源 | 内容 |
|---|---|
| `GF-006 OD-01 §2.2` | 「建立 Migration Authority Charter」；Charter 目的 = 审批资格 / 记录格式 / 保存位置 |
| `GF-006 OD-01 §2.2` | 「Charter 全文另立」→ 落盘新文件已获授权 |
| `GF-006 OD-01 §2.2` | 「Migration Authorization remains unavailable until Charter requirements are satisfied」 |
| `GF-006 OD-14 §1` | 冻结范围 = GF v0.2 文档体系（GF-000～006）；Freeze ≠ Migration Authorization |
| `OQ-GF-014` | OPEN-BLOCKING（Charter requirements 未满足） |

**GF-007 落盘约束**：

```text
· 载体：Docs/00_GOVERNANCE/GF-007-MIGRATION-AUTHORITY-CHARTER.md
· 不得标注 Frozen（AGENTS.md：Agent 自写的 Frozen 不自动获得权威）
· Status = OPEN；disposition = RETAIN（与其他治理文档同规）
· 不修改 GF-000～006 冻结文本
· GF-007 不自动落入 OD-14 冻结基线（该基线明确为 GF-000～006）
```

**F4 尚未裁决的子项**（Charter 正文落盘前必需）：

```text
[OWNER DECISION REQUIRED]
  2. Gate 执行者与批准者是否分离？
  3. 批准记录格式？（REPORT-I §6.1 合成示例可作为起点）
  4. 批准记录存放路径？
```

⇒ **GF-007 在本文件签发时尚未落盘**。Gate 9 保持 `UNSATISFIABLE`。

```text
F4 打开的是治理能力（谁有资格决定），不是迁移权限。
```

---

## 2. Decision F3-A — OD-03「不废弃现有分类」的射程

`[OWNER DECISION]`

```text
OD-03「不废弃现有分类」的射程【不覆盖】L* 层级体系。
```

**含义**：

```text
· OD-03 裁的是角色分类：GOV / EVD / EXT 与 RSD / PIS / OCRA / SEM / MIG
· OD-03 未定义、也未保护 Frozen Spec / Contract / Decision / Evidence 的层级关系
· 因此 OD-03 不得被解释为 L* authority taxonomy
· 推论：F3-A 的 Option C（废除 L* 标签）不因 OD-03 被禁止
```

**依据**：`GF-001 §2.6`；`GF-006 §4:233`「v0.2 增补角色**不替换** data lineage roles」；
`GF-005 OQ-GF-015`「AITutor-X 采用哪套层级（多套 L* 叙述 vs V3 90/91 vs AGENTS.md）？」（Status：OPEN-BLOCKING）。

---

## 3. Decision F3-B — DOC-GOV §9 的效力

`[OWNER DECISION]`

```text
DOC-GOV §9（V3 Governance 对照表）【不是】当前唯一映射权威。
保留 §9 作为输入证据之一。
不得让 §9 自动成为规则。
须另立明确的 Authority Taxonomy Mapping Decision。
```

**理由（记录）**：`Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md §9` 存在两处已确认硬冲突：

| 冲突 | 内容 |
|---|---|
| §9 ↔ README | §9 将 V3 `L1 Contract Change` 映射到「Owner Decision」（X 的 L0 名）；README 中 Contract = L2。同一仓内相差 2 级 |
| §9 ↔ R4 | §9 将 V3 `L2（Docs/DECISIONS/）` 归为 Informative / Historical Evidence；R4 将结论归入 `40_DECISIONS/`、证据归入 `60_REPORTS/` |

⇒ **不废弃 §9，但降级其效力**：§9 为 informational 输入，非 mapping authority。

---

## 4. F3-A 主选项状态 — DEFERRED（未被裁决）

`[NOT RULED]`

```text
本轮裁决回答了 F3-A 的射程前置问（§2），
【未选择】F3-A 的三项主选项：

  ☐ A 建立单一 Authority Taxonomy（指定唯一 L* + 历史重映射）
  ☐ B 保持分层 Authority（四套并存 + 跨域引用必须声明体系）
  ☐ C 废除 L* 标签，全面转用 GOV/EVD/EXT + Role 二维分类

状态 = DEFERRED。该问题转入 §6 FU-01 的 Authority Taxonomy Mapping Decision。
```

**理由（记录）**：`F3-A` 与 `F3-B` 为关联裁决项，不应孤立解释
（`REPORT-I-P0-DECISION-PREPARATION-01.md §4`）。F3-B 已裁「须另立 Mapping Decision」，
故 taxonomy 主选项在该 Decision 中一并裁决更为自洽。

```text
本文件不代选。
```

⇒ **后果**：`REPORT-I §6` Gate 2（Authority identified）与 Gate 10（`authority_level`）
在 FU-01 完成前**仍无权威依据可填**。

---

## 5. Deferred Decisions — F5 / F10

Owner 明确指示：本轮只裁 F4 + F3；F5 / F10 延后成立独立 Decision Record。

`[OWNER POSITION — NOT YET RULED]`（记录位置，**不构成裁决**）

```text
F5  Migration Gate Version ：倾向 Option A（批准 REPORT-I §6 十步表为正式 Gate），
                             且批准记录须带 Gate 9 = UNSATISFIABLE 状态头。
F10 Observation Set B      ：倾向 Option C（本轮限定豁免），
                             边界 = 不承认不存在的 Set B /
                                    不追认 Papers DSH 系列为「受限 Set B」/
                                    后续迁移前仍需明确 Evidence Authority。
```

```text
F5  状态 = DEFERRED（未裁决）
F10 状态 = DEFERRED（未裁决）
```

**延后理由（记录）**：F3 决定 Gate 字段语义；先完成 F3 才能在 F5 批准记录中写出实指而非悬空占位符。

---

## 6. Follow-up Registry

| ID | 项 | 依据 | 状态 | 阻塞 |
|---|---|---|---|---|
| **FU-01** | **Authority Taxonomy Mapping Decision**（另一份 `OWNER-DECISION-*.md`） | 本文件 §3 + §4 | **REQUIRED** | 阻塞 Gate 2 / Gate 10 |
| **FU-02** | `GF-007-MIGRATION-AUTHORITY-CHARTER.md` 落盘 | 本文件 §1 | **AUTHORIZED / BLOCKED** | 阻塞于 F4 子项 2 / 3 / 4 |
| **FU-03** | F5 Migration Gate Version 裁决 | 本文件 §5 | DEFERRED | — |
| **FU-04** | F10 Observation Set B 裁决 | 本文件 §5 | DEFERRED | — |

> **FU-01 说明**：若不登记此项，F5 批准后 Gate 2 的 `authority_level` 字段
> 会从「填不出来」变为「填了但无权威依据」—— 后者风险更高。

---

## 7. Non-Authorization Boundary

```text
本文件不授权：

- Migration
- Phase B 进入
- Producer Metadata 实现
- Schema migration / DDL
- Gate 激活（Gate 9 保持 UNSATISFIABLE）
- Authority reassignment（Migration Authority 之外）
- 修改 Frozen Spec / GF-000～006
- 修改 REPORT-I 原始历史报告
```

---

## 8. Post-Ruling State

```text
Migration Authority     = EXISTS（Owner）
GF-007 Charter          = NOT LANDED（阻塞于 F4 子项 2 / 3 / 4）
Authority Taxonomy (L*) = DEFERRED（转入 FU-01）
Gate Version            = NOT APPROVED（F5 DEFERRED）
Set B                   = NOT WAIVED（F10 DEFERRED）

Gate 9                  = UNSATISFIABLE
Migration Authorization = NO
Migration Ready         = NO
Phase B                 = NOT ENTERED
```

---

## 9. Owner Signature

```text
Signed by  : kurt
Signed Date: 2026-09-28
Verdict    : ☑ APPROVED（F4 = Option A；F3-A 射程 = 不覆盖 L*；F3-B = §9 非唯一映射权威）
```

**转录声明**：本文件所载裁决由 Owner 于 2026-09-28 作出。DSH 仅作转录
（依据 `GF-000:461`「决策 actor = Owner；文档 actor = document verification only」），
**未增加、未删除、未改写任何裁决**。

---

*OWNER-DECISION-MIGRATION-AUTHORITY-TAXONOMY-01 · 2026-09-28 · 本文件为 F4 / F3 的唯一权威来源。*
