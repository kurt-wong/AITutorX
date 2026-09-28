# REPORT-I P0 Decision Preparation Record

```text
Document Type : Decision Preparation Record（非 Authority Decision）
Status        : OPEN
supersedes    : —
superseded_by : —
disposition   : RETAIN
Revision      : 3 (2026-09-28) — 合并 ERRATA-01（E-01～E-08）+ rev.3 自洽性修补，见 §10 Amendment Record
readers       : Owner（裁决方）；MIMO CODE（准备方）；Migration Authority（待设立）
Authority     : —（本文不构成任何 Authority）
Temporal Scope: Current-state facts verified as of 2026-09-28.
                REPORT-I is as-of 2026-09-17. This record maps the delta.
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. Document Purpose

```text
本文不是 Authority Decision。
本文不是 Migration Authorization。
本文不改变 REPORT-I as-of 状态。
本文仅提供 Owner Decision 输入。
本文不修改 Frozen Spec / Authority 文档。
本文不触发 Migration / Phase B。
本文不选择方案、不预填 Owner Verdict。
本文不含 Taxonomy 正文、不含 Charter 正文、不含映射表。
```

---

## 0A. 命名空间声明

本文中的 `OD-*` 编号必须按以下规则区分：

| 编号模式 | 命名空间 | 来源 |
|---|---|---|
| `OD-01`, `OD-03`, `OD-14`（两位数） | GF-006 Owner Decision Record | `GF-006-OWNER-DECISION-RECORD.md` |
| `OD-001`, `OD-002`, `OD-003`（三位数） | REPORT-E Owner Decision Queue | `REPORT-E-OWNER-DECISION-QUEUE.md` |

**禁止混读。** 依据：`X2.5-05-CONFLICT-LEDGER` CL-05「GF-006 OD-01~20 与 REPORT-E OD-001~010 混读 → 假授权」。

此声明同时构成 **F3 必须裁决的经验证据**：一份 P0 裁决输入文档自身曾复现标签歧义缺陷（见 §10 A-01）。

---

## 1. Current State Delta

REPORT-I（as-of 2026-09-17）→ 当前（2026-09-28）的差异映射：

| 项目 | REPORT-I 原状态 | 后续变化 | 当前状态 |
|---|---|---|---|
| F7 DESIGN-v1.1 availability | untracked / authority unknown | `a4cf6a6` 恢复入库（5 份） | availability resolved |
| F7 DESIGN-v1.1 authority | unknown | 无 Owner 裁决 | **OPEN** |
| Repository Hygiene | pending（大量 untracked） | `40e0816` `02a2a77` `53082b7` `341e9f1` `a4cf6a6` `2e16b1a` | resolved（已知项） |
| Migration readiness | blocked（Cluster A 全未关闭） | 无授权变化 | **blocked** |
| F4 Migration Authority | 未设立 | 无变化 | **OPEN** |
| F5 Gate version | 草案 | 无变化 | **OPEN** |
| F3 Authority Taxonomy | 三套 L* 并存 | OD-03（GF-006）增补 GOV/EVD/EXT 分层；DOC-GOV §9 发现第四套映射 | **OPEN** |
| F10 Set B | 未导入 | 无变化 | **OPEN** |
| OD-007 git init | pending | 已完成（`659db9b`） | **可 CLOSED** |
| OD-003 D2/D3/D4 状态 | "UNKNOWN / NOT STARTED" | DEC-049 Brief 已交付（2026-09-17），裁决仍暂停 | **OPEN**（追注：Brief delivered / ruling pending） |

---

## 2. F4 — Migration Authority Decision Sheet

### Current Facts

```text
- 当前没有 Migration Authority 任命记录
- 当前没有 Migration Gate 批准人（Gate 9 无签署主体）
- 当前没有批准记录格式（migration_id / approver / approved_at 字段在 REPORT-I §6.1
  仅为合成示例，未获批准）
- 当前没有批准记录存放路径
- Charter 全文尚未落盘
```

**已有治理事实（供参考，非裁决）：**

| 来源 | 内容 | 性质 |
|---|---|---|
| GF-006 OD-01 §2.2 | "Migration Authorization remains unavailable until Charter requirements are satisfied" | Charter 条件来源（**非 OD-14**） |
| GF-006 OD-01 §2.2 | "Charter 目的（已裁，Charter 全文另立）" | 已授权另立 Charter 文件 |
| GF-006 OD-14 | Freeze boundary：Migration Authorization / Gate pass / Migration Ready 不可用 | 冻结≠授权声明 |
| OQ-GF-014 | OPEN-BLOCKING（Migration Authority / Charter） | 多轮审计一致 |
| REPORT-G §3.5 | 「当前没有已生效的、写入治理仓的 Migration Authority」 | 事实确认 |
| REPORT-I §6 Gate 9 | 「当前不可满足」 | 事实确认 |

**含义**：OD-01 已裁「要设立」且已授权「Charter 全文另立」，但 Charter 本体、授权人、记录格式、存放路径均未落盘。F4 需要决定的是**如何落地**，不是**要不要设立**。

**OD-14 射程限定**：OD-14 的冻结范围是 GF v0.2 文档体系（GF-000～006）。新建 Charter（如 `GF-007-*`）**不自动落入该冻结基线**。但依 `AGENTS.md`，Agent 自写的 "Frozen" 不自动获得权威——Charter 自身不得标为 Frozen。

### Decision Options

| Option | 含义 | 后果 |
|---|---|---|
| A | 指定 Migration Authority（Owner 本人 / 指定 Agent / 双人复核），并批准 Charter 基本要素落盘 | Gate 9 可满足；后续 F5 Gate 批准可执行 |
| B | 保持未指定 | Migration 保持全面冻结；REPORT-I §0.7 停止线持续生效 |
| C | 设计替代治理模型（如 Gate 自动化 / 去中心化批准），需额外机制定义 | 进入设计流程；Gate 9 语义需重定义 |

**Option A 产出物**（不是一行裁决）：

```text
1. Owner 裁决记录（Migration Authority 任命）
2. Migration Authority Charter 正文（另立新文件）
   - 载体：Docs/00_GOVERNANCE/GF-007-MIGRATION-AUTHORITY-CHARTER.md
   - 依据：OD-01 §2.2 已裁「Charter 全文另立」
   - 不触碰 GF-000~006 冻结文本
   - Charter 自身不得标为 Frozen（AGENTS.md）
```

**需明确的子问题（如选 A）：**

```text
1. Migration Authority 是谁？（Owner 本人 / 指定 Agent / 双人复核）
2. Gate 执行者与批准者是否分离？
3. 批准记录格式？（REPORT-I §6.1 合成示例可作为起点）
4. 批准记录存放路径？
```

### Owner Decision

```text
☐ Option A   ☐ Option B   ☐ Option C

Sub-decisions (if A):
  1. Migration Authority: _______________
  2. Executor / Approver 分离: _______________
  3. Approval record format: _______________
  4. Storage path: _______________

Signed: _______________
Date:   _______________
```

---

## 3. F5 — Migration Gate Version Decision Sheet

### Current Facts

```text
- 当前存在 Gate 概念（REPORT-D 10 步草案、REPORT-I §6 检查表）
- REPORT-I 自陈「本 REPORT-I 为草案」（§1 F5 行）
- 没有 Owner 批准的 Gate 版本
- Gate 9 依赖 F4（Migration Authority），当前不可满足
- Migration 未授权
```

**已有 Gate 草案资产：**

| 资产 | 位置 | 状态 |
|---|---|---|
| 10 步 Gate 检查表 | REPORT-D §草案 | 草案 |
| 10 步 Gate 检查表（补证据字段） | REPORT-I §6 | 草案 |
| Migration Record 最小字段 | REPORT-I §6.1 | 合成示例，未批准 |

### Decision Options

| Option | 含义 | 后果 |
|---|---|---|
| A | 批准现有 Gate 版本（REPORT-I §6 十步表作为正式 Gate） | 建立 Migration 判断基线；但 Gate 9 仍需 F4 落盘后才可满足 |
| B | 延后 Gate 定义 | 保持 NOT AUTHORIZED；迁移全面冻结持续 |
| C | 修订 Gate（指定修改点后另出版本） | 进入 Gate 设计流程；需新一轮批准 |

**F5 批准记录必须带状态头**（防「Gate 已批 = 迁移已解锁」误读）：

```text
Gate Version:     APPROVED（如选 A）
Migration:        NOT AUTHORIZED
Gate 9:           UNSATISFIABLE（待 F4 Charter 落盘后方可满足）
```

`Gate definition approved ≠ Migration authorized`。

### Owner Decision

```text
☐ Option A   ☐ Option B   ☐ Option C

If C, revision points: _______________

Signed: _______________
Date:   _______________
```

---

## 4. F3 — Authority Taxonomy Decision Sheet

### Current Facts

当前至少**四套** L* 层级体系 / 映射并存：

| # | 来源 | 体系 | 示例 |
|---|---|---|---|
| 1 | AITutorX README | L0=Owner/System Decision, L1=Frozen Spec, L2=Contract… | L0–L7 |
| 2 | V3 `90_DOCUMENT_GOVERNANCE` | L0=Frozen Spec, L0-META, L1=Contract Change… | L0–L(n) |
| 3 | REPORT-B | L1–L7 且与前两者不完全同构 | L1–L7 |
| 4 | **DOC-GOVERNANCE §9** | V3→X 对照表（V3 L0→Frozen Spec; L1→Owner Decision…） | 映射声明 |

**已有的正交分类层（OD-03 / GF-001 v0.2）：**

```text
第一层 Authority Domain:  GOV / EVD / EXT
第二层 Artifact Role:     RSD / PIS / OCRA / SEM / MIG

两类分类解决不同问题，禁止互相替代。
```

**关键区分：**

```text
OD-03 答的是「分类模型」（GOV/EVD/EXT + Role）；
OQ-GF-015 问的是「哪套 L*」；
OD-03 未回答该问。

OD-03「不废弃现有分类」的射程 = 角色分类（data lineage roles），
并未保护四套 L* 层级体系 / 映射。
```

**DOC-GOV §9 的两处硬冲突：**

| 冲突 | 内容 |
|---|---|
| §9 ↔ README | §9 将 V3 L1 Contract Change 映射到「Owner Decision」（X 的 L0 名）；README 中 Contract = L2。同一仓内相差 2 级 |
| §9 ↔ R4 | §9 将 V3 L2（Docs/DECISIONS/）归为 Informative/Historical Evidence；R4 将结论归入 `40_DECISIONS/`、证据归入 `60_REPORTS/`。同一 GAP 走哪条规则无解 |

### Decision Options — F3-A（OD-03 射程）

| Option | 含义 | 后果 |
|---|---|---|
| A | 建立单一 Authority Taxonomy（指定一套 L* 为唯一标准），并规定历史文档 L* 重映射规则 | L* 标签恢复有效；需一次性映射历史标签 |
| B | 保持分层 Authority（四套并存，按来源域区分适用范围），但规定「跨域引用必须声明体系」 | 无需映射；但标签仍有歧义风险 |
| C | 废除 L* 标签，全面转用 OD-03 的 GOV/EVD/EXT + Role 二维分类 | 消除 L* 歧义；需大规模文档改标 |

**F3-A 前置一问：**

```text
OD-03「不废弃现有分类」的射程是否覆盖 L* 层级体系？
  ☐ 是 — Option C 需先改 OD-03，A/B/C 合法性重审
  ☐ 否 — Option C 不被 OD-03 禁止，A/B/C 合法性均成立

Signed: _______________
Date:   _______________
```

### Decision Options — F3-B（DOC-GOV §9 效力）

| Option | 含义 | 后果 |
|---|---|---|
| A | DOC-GOV §9 即 F3 所要求的映射规则 | §9 为唯一映射权威；须先修其与 README 编号、R4 归属的两处冲突 |
| B | §9 仅为叙事对照，F3 须另立映射表 | 另立映射表；须声明 §9 的效力边界（降级为 informational） |
| C | 部分采纳（§9 部分行有效，部分行需修订） | 逐行裁决；工作量大但精度高 |

**F3-B 具体冲突裁决（如选 A 或 C）：**

```text
冲突 1（§9 ↔ README）：
  V3 L1 Contract Change 应映射到 X 的哪个层级？
  ☐ L0（Owner Decision）  ☐ L2（Contract）  ☐ 其他: _____

冲突 2（§9 ↔ R4）：
  V3 Docs/DECISIONS/ 应归入 40_DECISIONS/ 还是 60_REPORTS/？
  ☐ 40_DECISIONS/（结论）  ☐ 60_REPORTS/（证据）  ☐ 其他: _____
```

**F3-A 与 F3-B 为关联裁决项，不应孤立解释。** 组合有效性提示（**不构成新 Option**，仅提示解释边界）：

| F3-A（OD-03 射程） | F3-B（DOC-GOV §9 效力） | 组合 |
|---|---|---|
| 不覆盖 L* | §9 为唯一映射权威 | 可成立 |
| 不覆盖 L* | §9 非权威 | 可成立（须另立映射表） |
| 覆盖 L* | §9 为唯一映射权威 | 需解释冲突 |
| 覆盖 L* | §9 非权威 | 高风险（须受 OD-03 约束另立映射） |

**F3 实现约束**（如选 A）：

```text
✅ 保留原标 + 映射表追注
   例：REPORT-B L1 → mapped-to X __
       V3 L0      → mapped-to X __
❌ 禁止重写历史标签（AGENTS.md「不重编号历史 Decision」同类禁令）
```

注：上列映射目标留空，属 F3 实质裁决，本文不预填。

### Owner Decision

```text
F3-A:
  前置一问: ☐ 射程覆盖 L*   ☐ 射程不覆盖 L*
  ☐ Option A   ☐ Option B   ☐ Option C

F3-B:
  ☐ Option A   ☐ Option B   ☐ Option C
  冲突 1: _______________
  冲突 2: _______________

Signed: _______________
Date:   _______________
```

---

## 5. F10 — Set B Reconciliation Decision Sheet

### Current Facts

```text
- Set B（DSH Independent Audit）未以独立审计包形式导入 AITutorX
- 没有 Owner 提供的 Set B 路径/commit
- 没有 Owner 书面豁免
- OQ-GF-013 OPEN（Set B / REPORT-J）
```

**已存在的相关材料（不等于 Set B）：**

| 材料 | 位置 | 与 Set B 的关系 |
|---|---|---|
| DSH 自审（DEC-045） | Papers `INTEGRATION/` | 自审，非独立审计包 |
| Guardian 系列 | Papers `INTEGRATION/` | 监护记录，非审计包 |
| DEC-049 Decision Brief | Papers | 决策简报，非审计包 |

**REPORT-G §2.5–2.6 结论**：上述材料「不是与 REPORT-A~F 同构的独立治理审计包」。完整三方对照目前只能做到 Claude vs 仓库现实 + DSH 关键主张抽查。

### Decision Options

| Option | 含义 | 后果 |
|---|---|---|
| A | 提供 Set B（指定路径/commit，导入 AITutorX 供对账） | 对账完整性升级为三方对照；需补做 Set B 导入后二次对照 |
| B | 要求补充（先补齐 Set B 形式要求再导入） | 进入 Set B 准备流程；迁移继续冻结 |
| C | 豁免（书面豁免「本轮仅以 Set A + 仓库现实对账」） | 对账声明限定为二方对照；REPORT-G/H/I/K 可引用性恢复（附限定条件） |

**Option C 边界限定**（如选 C）：

```text
豁免声明应限定为：
  - 当前迁移范围内，不以不存在的 Set B 阻塞
  - 不追认 Papers DSH 系列为「受限 Set B」
  - 不豁免对账完整性要求本身，仅豁免 Set B 作为前置条件

REPORT-G/H/I/K 的引用声明应追加「Set B 豁免」限定语。
```

### Owner Decision

```text
☐ Option A   ☐ Option B   ☐ Option C

Sub-decisions: _______________

Signed: _______________
Date:   _______________
```

---

## 6. Dependency Graph & Ruling Order

### Gate 依赖映射（依据 REPORT-I §6）

```text
Gate 2  Authority identified  → 证据 = F3 层级 + 依据文件   ← F3
Gate 7  Evidence attached     → 对账报告引用（G/H/I）       ← F10
Gate 9  Governance approval   → Migration Authority 签字    ← F4
Gate 10 Migration record      → authority_level per F3      ← F3
Gate 本文版本                  → 批准后可作 Gate 依据         ← F5
```

### 依赖图（F3 平行）

```text
F4 ──► F5 ──┐
            ├──► Gate 可满足
F3 ─────────┘   （F3 平行，阻塞 Gate 2 与 Gate 10）
F10 ───────────► Gate 7
```

### 建议裁决顺序

```text
1. F4  — 没 Authority，没人批准
2. F3  — 没 Taxonomy，Gate 2/10 无法填；Migration Record 的
          authority_level 字段会留悬空占位符
3. F5  — Gate 明确后才能判断 Evidence 要求
4. F10 — 输入完整性问题
```

**关键约束**：若先批 F5 而不裁 F3，会出现「Gate 已批准但第 2 步永远填不出来」的状态。F3 必须在首次迁移前完成。

---

## 7. Historical Stale Registration

### OD-007 — AITutorX Git 仓库初始化

```text
Original (REPORT-E, as-of 2026-09-17):
  AITutorX git 仓库初始化，pending。

Current (2026-09-28):
  仓库已初始化（659db9b），已有多轮 commit，
  remote 已配置（github.com/kurt-wong/AITutorX）。

Classification:
  STALE historical observation.

Proposed disposition:
  Status: CLOSED
  追注: git init 已完成（659db9b）
```

### OD-003 — D2/D3/D4 状态表述

```text
Original (REPORT-E, as-of 2026-09-17):
  D2 / D3 / D4 状态标为 "UNKNOWN / NOT STARTED"。

Current (2026-09-28):
  DEC-049 Decision Brief 已交付（2026-09-17），裁决仍暂停。
  F7 DESIGN-v1.1 已入库（a4cf6a6）但 authority 仍 pending。

Classification:
  STALE wording. 实质裁决未决。

Proposed disposition:
  Status: OPEN
  追注: DEC-049 Brief delivered（2026-09-17）；ruling pending
  不关闭 OD-003（实质未决）。
```

**执行方式**：在 REPORT-E 的 OD-007 / OD-003 条目内追加 `状态:` 行（最小侵入，不动汇总表结构）。

---

## 8. Explicit Non-Authorization Boundary

```text
This record does not authorize:

- Migration
- Producer Metadata implementation
- Schema migration
- Gate activation
- Authority reassignment
- Phase B entry
- 修改 REPORT-I 原始历史报告
- 修改 Frozen Spec / Authority 文档
```

---

## 9. Owner Signature

```text
Decision:
☐ Approved（批准本准备材料作为 P0 裁决输入）
☐ Rejected
☐ Revise

Signed: _______________
Date:   _______________
```

---

## 10. Amendment Record

### A-01 (2026-09-28) — 合并 ERRATA-01 修正（E-01～E-08）

| 编号 | 修正内容 | 原文位置 |
|---|---|---|
| E-01 | §2 引用载体：OD-14 → OD-01 §2.2（Charter 条件来源） | 原 §2 Current Facts |
| E-02 | §2 补 Charter 本体产出物 + OD-14 射程限定（GF-007 不自动 Frozen） | 原 §2 |
| E-03 | §4 补 OD-03 射程一问（是否覆盖 L*） | 原 §4 |
| E-04 | §6 依赖图改 F3 平行 + 裁决顺序 F4→F3→F5→F10 | 原无 §6 |
| E-05 | §3 补 F5 状态头（Gate 9: UNSATISFIABLE） | 原 §3 |
| E-06 | §5 补 Option C 边界限定 | 原 §5 |
| E-07 | §7 OD 条目改用词表状态词（CLOSED / OPEN）+ 追注格式 | 原 §6 |
| E-08 | §4 保留映射示例行结构、清空映射目标值（映射结果属 F3 实质裁决，越界不预填）；DOC-GOV §9 引于 §4 事实栏与 F3-B | 原 §4 |

ERRATA-01 独立文件已并入本文，不再单独存在（R1：每任务最多 1 份文档）。

### A-02 (2026-09-28) — 文件治理合规

- Status 词改为词表合法值 `OPEN`（原 "DRAFT INPUT — AWAITING OWNER RULING" 非词表词）
- 补 R3 字段：`supersedes` / `superseded_by`
- 补 R5 字段：`disposition: RETAIN`
- 补命名空间声明（§0A）

### A-03 (2026-09-28) — F3 补充决策问题

- 补 F3-B（DOC-GOV §9 效力边界），含两处具体冲突裁决项
- §1 Current State Delta 的 F3 行：原状态列保留 REPORT-I as-of 值「三套 L* 并存」，变化列记入 DOC-GOV §9 第四套映射
- 补 DOC-GOV §9 两处硬冲突事实（§9↔README / §9↔R4）

### A-04 (2026-09-28) — rev.3 自洽性修补（不改变任何裁决内容）

- §4「三套」→「四套」：事实栏与 F3-A Option B 正文
- §4 新增「F3-A 与 F3-B 为关联裁决项」提示与组合有效性矩阵（不新增 Option）
- A-01 的 E-08 行改述：实际处置为「保留示例行结构 + 清空映射目标值」，非「删除示例」
- A-03 的 §1 行改述：原状态列保留 REPORT-I as-of「三套」，变化列记第四套映射

**工作稿 provenance 补记（`[OWNER RULING 2026-09-28]`）**：

```text
ERRATA-01 was working artifact only; not tracked;
merged into revision 2 before governance adoption.

revision 1 亦为工作稿，从未入库；其内容不构成治理资产，不可从 git 还原。
正式治理资产自 5205208（revision 2）起算；本 revision 3 为其自洽性修补。
不为此补建 ARCHIVE / HISTORY / ATTACHMENT 附件（不以治理复制治理）。
```

---

*Revision 3 prepared 2026-09-28. Not an Authority Decision. Owner ruling required for F3-A/F3-B/F4/F5/F10.*
