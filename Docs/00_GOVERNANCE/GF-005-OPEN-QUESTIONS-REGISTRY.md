# GF-005 — Open Questions Registry（草案）

**Document ID**: GF-005
**Status**: `DRAFT / PROPOSED` — 登记未决问题；**不**在此文件内解决任何 UNKNOWN
**Version**: **v0.2 Draft**（TASK-GF-005 document patch；新增 blocking_scope / D-048 binding-only / BL 交叉引用）
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17（v0.1） / **2026-09-18**（v0.2 patch）
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Naming note**: 本登记册使用 **`OQ-GF-###`** 前缀，以免与 Papers/历史文档中的 OQ 编号冲突。每条映射既有 OD-* / REPORT-K UNKNOWN-* / REPORT-H Cluster，**不替代**源仓原始编号。

**Discipline**: 不把 UNKNOWN 写成 FACT；不以假设关闭问题；关闭仅能由 Owner 书面裁决或新证据。
**v0.2 labels**: `[FACT]` / `[OBSERVED]` / `[PROPOSAL]` / `[OWNER DECISION REQUIRED]` / `[UNKNOWN]`
**v0.2 non-action**: **零关闭** — 未将任何 OQ-GF Status 改为 CLOSED；未关闭 BL-*；未关闭 D-048。

**Importers / cross-refs**: GF-000 §7；GF-001 §4；GF-002 §7/§8/§9 Open Items；GF-003 §3.2.3；REVIEW/GF-003/06 BL-09/10/11；无代码 import。

---

## 1. Registry Summary

| 状态 | 含义 |
|------|------|
| `OPEN` | 无足够证据，待 Owner 或后续取证 |
| `OPEN-BLOCKING` | 阻塞迁移/数据引用/身份声明 |
| `MAPPED` | 已有对应 OD/REPORT 条目，本册只做治理索引 |
| `STALE-CANDIDATE` | 外部状态可能已变，需 Owner 确认关闭或重开 |

**统计（v0.2）**: 登记仍为 **18** 条 OQ-GF；其中 OPEN-BLOCKING 仍为 **9**；**零关闭** `[FACT: 本 patch 未改任何 Status 为 CLOSED]`。

### 1.1 blocking_scope 分层（v0.2 增补）

`[PROPOSAL]` 为每条 OPEN-BLOCKING 项标注 **blocking_scope**，说明「阻塞哪一类动作」。**分层不降低停止线**；`any-migration` 项仍由 REPORT-I §0.7 默认全禁迁移管辖。

| Scope | Meaning |
|-------|---------|
| `doc` | 阻塞治理文档冻结 / 权威叙事成文 |
| `data` | 阻塞数据本体引用/交付/迁入 |
| `code` | 阻塞代码模块迁入或「迁移后测试等价」声明 |
| `claim` | 阻塞 lineage verified / 来源已验证 等主张 |
| `authority` | 阻塞 Migration Authority / Gate 9 / taxonomy 生效 |

`[PROPOSAL]` 当前 OPEN-BLOCKING 分层（**Status 不变，仍 OPEN-BLOCKING**）:

| OQ-GF | Status（不变） | blocking_scope `[PROPOSAL]` | 说明 |
|-------|----------------|------------------------------|------|
| 001 权威原始来源 | OPEN-BLOCKING | `data` + `claim` + `authority` | 双树权威未裁前不得单树 data/claim |
| 002 数据权威模式 | OPEN-BLOCKING | `data` | path-ref/copy/hash-manifest 未裁 |
| 004 双树保留策略 | OPEN-BLOCKING | `data` + `authority` | 无 Owner 令不得删/合任一树 |
| 007 Lineage 补全 | OPEN-BLOCKING | `claim` + `data`（大规模 verified） | 阻塞「大规模 verified 迁移」声明 |
| 013 Set B / REPORT-J | OPEN* | `claim` + `doc` | 外部主张无法核验；v0.1 为 OPEN（F10） |
| 014 Migration Authority | OPEN-BLOCKING | `authority`（+ 阻塞 Gate 9） | Charter/F5 未设；approval_block=invalid_without_charter |
| 015 Authority Taxonomy | OPEN-BLOCKING | `authority` + `doc` | 多套层级并存 |
| 016 DEC/BUG/OQ namespace | OPEN-BLOCKING | `doc` + `authority` | 阻塞 40_DECISIONS 填充 |
| 017 Design/untracked + D2-D4 | OPEN-BLOCKING | `code` + `authority` + `doc` | M1–M5 / DESIGN-v1.1 |
| 018 测试基线 / r67 | OPEN-BLOCKING | `code` + `claim` | 阻塞「迁移后测试等价」声明 |

`[FACT]` v0.1 事实保持: OQ-GF-013 在 v0.1 标 `OPEN`（非 OPEN-BLOCKING）；上表分层为治理提示，**不**将其 Status 改为 OPEN-BLOCKING。

`[OWNER DECISION REQUIRED]` 分层命名是否采用本表取值；是否新增 OQ-GF-019（rollback / 迁移后验证标准）— **本 patch 不新建 OQ**。

---

## 2. Source Lineage & Data Authority

### OQ-GF-001 — 权威原始来源未定义

| Field | Value |
|-------|-------|
| **Question** | preprocessing 的 canonical source corpus 是 `maintainess/PDF`、`original/`，还是「双层：original=原件库 / maintainess=OCR 队列」？ |
| **Classification** | `[UNKNOWN]` → `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING` |
| **Evidence** | REPORT-K §2/§5：operational input = maintainess/PDF `[FACT]`；original 更大且高重叠 `[FACT]`；方向/权威 `[UNKNOWN]` |
| **Maps to** | OD-K-01；任务书示例 OQ-001 |
| **Must not** | 假设 maintainess 权威 **或** original 权威 |

### OQ-GF-002 — 数据权威与引用/交付模式

| Field | Value |
|-------|-------|
| **Question** | AITutorX/下游引用数据采用 path-ref / NAS / copy / 仅 hash 清单 / 其他？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING` |
| **Evidence** | REPORT-I F8 / OD-009 / GAP-007；数据 ignored `[FACT]` |
| **Maps to** | OD-K-02；OD-009；任务书 OQ-002 相关 |
| **Proposal (non-binding)** | 优先「角色 + sha256 清单 + 只读 locator」；数据本体默认不迁 |

### OQ-GF-003 — `SHA256(original source bytes)` 词义 vs 目录

| Field | Value |
|-------|-------|
| **Question** | 是否强制在治理/Contract 文档中显式区分 identity 词面与物理目录 `D:\Project\Papers\original`？ |
| **Classification** | `[FACT]` 二者概念不同；是否强制双标注 = `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K §4.1；snapshot 行 source 指向 md `[FACT]`；GF-002 §4 |
| **Maps to** | OD-K-03 |

### OQ-GF-004 — 双树重叠副本的保留策略

| Field | Value |
|-------|-------|
| **Question** | `maintainess/PDF` 与 `original/` 高重叠（basename 交集 12,626；抽样 6/6 sha 一致）是否保留双份？若否，保留哪侧、谁执行校验/合并？ |
| **Classification** | `[UNKNOWN]` 关系方向；策略 = `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING` |
| **Evidence** | REPORT-K §1.7–1.8、§8 OD-K-04 |
| **Maps to** | OD-K-04；任务书 OQ-001 |
| **Must not** | 在无 Owner 令下删除/合并任一树 |

### OQ-GF-005 — maintainess 恢复完整性证据标准

| Field | Value |
|-------|-------|
| **Question** | Owner 是否接受「数量 12,707 + 抽样 hash」作为误删恢复完成的充分证据，还是要求恢复前后全量 hash 台账？ |
| **Classification** | `[DECISION REQUIRED]`；恢复前全量 hash = `[UNKNOWN]`（可能不存在） |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K §1.11、UNKNOWN-004、OD-K-05 |
| **Maps to** | OD-K-05 |

### OQ-GF-006 — 双树数据血缘方向

| Field | Value |
|-------|-------|
| **Question** | 谁拷贝谁？是否同一采集批次？Papers 之外上游是什么？ |
| **Classification** | `[UNKNOWN]` |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K UNKNOWN-002/005/006；无 import commit；无全量双侧 hash |
| **Maps to** | UNKNOWN-002/005/006 |

### OQ-GF-007 — Lineage 补全责任与范围

| Field | Value |
|-------|-------|
| **Question** | 源 md 无正文 lineage、OCR 清单覆盖不足（≈4,224 vs 1,801 vs 166）——是否立项要求 Producer 补齐可审计清单？范围/格式/是否入 git？ |
| **Classification** | `[FACT]` 覆盖缺口；补全要求 = `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING`（阻塞「大规模 verified 迁移」声明） |
| **Evidence** | REPORT-K §4.2、UNKNOWN-003、OD-K-07；任务书 OQ-003 |
| **Maps to** | OD-K-07；UNKNOWN-003 |

### OQ-GF-008 — 是否需要全量 source hash inventory

| Field | Value |
|-------|-------|
| **Question** | 是否要求对 RSD/PIS 候选树建立全量 `path → sha256` 台账？成本与存放位置？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | 任务书 OQ-002；与 OQ-GF-002/004/005 关联 |
| **Maps to** | OD-K-02/04/05 |

### OQ-GF-009 — Preprocessing 工件是否需要 re-indexing

| Field | Value |
|-------|-------|
| **Question** | 既有 OCR/manifest/IR 工件是否在迁入前重做索引，还是只登记存量 hash？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | 任务书 OQ-003；REPORT-K 覆盖缺口 |
| **Maps to** | OD-K-07 |

### OQ-GF-010 — DOCX / 待转换DOC 是否正式输入

| Field | Value |
|-------|-------|
| **Question** | `maintainess/DOCX`（12,142）与 `待转换DOC`（38）是否属于 preprocessing/迁移输入范围？ |
| **Classification** | `[FACT]` 现行 OCR 代码不读 DOCX；范围 = `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K §2.1、OD-K-09 |
| **Maps to** | OD-K-09 |

### OQ-GF-011 — 文档口径更正载体（12,707 归属）

| Field | Value |
|-------|-------|
| **Question** | 如何更正 Papers 文档将「12,707 PDF」系于 `original/` 的表述，而不违反不得改写既有报告/账本的冻结纪律？ |
| **Classification** | `[FACT]` 数字归属错误或未定义；更正载体 = `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K §6；`PREPROCESSING-CLOSURE-PLAN.md:75` vs 实测 12,707=maintainess/PDF、original=38,893 |
| **Maps to** | OD-K-06 |

### OQ-GF-012 — 首跑证据效力（pre-git）

| Field | Value |
|-------|-------|
| **Question** | 无 pre-git 代码快照时，是否接受「日志数量结构 + 现行代码 + prd 规格」作为 maintainess/PDF=历史 OCR 输入 的治理级证据？ |
| **Classification** | Confidence PARTIAL `[INFERENCE]`；效力 = `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Evidence** | REPORT-K §3.1、UNKNOWN-001、OD-K-10 |
| **Maps to** | OD-K-10；UNKNOWN-001 |

---

## 3. Governance / Migration Authority

### OQ-GF-013 — Observation Set B / REPORT-J

| Field | Value |
|-------|-------|
| **Question** | 外部 DSH Observation Set B 是否导入？`REPORT-J` 是否曾存在/将交付？若 Set B 与仓库现实冲突，对账基准是什么？ |
| **Classification** | `[FACT]` AITutorX 无 REPORT-J；Set B 未导入；其余 `[UNKNOWN]` |
| **Status** | `OPEN`（F10） |
| **Evidence** | REPORT-K §1.10、§6；REPORT-I F10 |
| **Maps to** | OD-K-08；F10 |

### OQ-GF-014 — Migration Authority / Gate 批准链

| Field | Value |
|-------|-------|
| **Question** | Migration Authority 由谁担任？Gate 版本（REPORT-I）谁批准？批准记录格式与存放路径？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING`（Cluster A） |
| **Evidence** | REPORT-I F4/F5、§2.1 P0 |
| **Maps to** | REPORT-H Migration authority；F4/F5 |

### OQ-GF-015 — 唯一 Authority Taxonomy

| Field | Value |
|-------|-------|
| **Question** | AITutor-X 采用哪套层级（报告中存在多套 L* 叙述 vs V3 90/91 vs AGENTS.md）？ |
| **Classification** | `[FACT]` 多套并存的治理风险已被 REPORT-H/I 指出；唯一化 = `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING` |
| **Evidence** | REPORT-I F3；V3 `90/91` Authority Level 体系；`AGENTS.md` L0–L7 |
| **Maps to** | F3；REPORT-H |

### OQ-GF-016 — DEC/BUG/OQ 命名空间政策

| Field | Value |
|-------|-------|
| **Question** | 历史 DEC 编号如何映射进 AITutor-X？BUG/OQ 规则？mapping authority 载体？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING`（阻塞 40_DECISIONS 填充） |
| **Evidence** | REPORT-C 映射草案；REPORT-I F6/Cluster C；OD-004 |
| **Maps to** | OD-004；F6 |

### OQ-GF-017 — Design v1.1 / untracked 契约族 authority

| Field | Value |
|-------|-------|
| **Question** | DESIGN-v1.1 等 untracked 文档：commit / 降级 / working ref / 拒绝？D2/D3/D4 如何裁？ |
| **Classification** | `[UNKNOWN]` authority；`[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING`（Cluster B） |
| **Evidence** | REPORT-A/B/D/E；REPORT-I §2.2 |
| **Maps to** | OD-001/002/003/008 |

### OQ-GF-018 — 测试基线与 r67 处置

| Field | Value |
|-------|-------|
| **Question** | 两仓测试受控重跑基线以谁为准？r67 FAIL：修复前迁 / known-issue 挂账 / expected failure？frontend 是否在范围？ |
| **Classification** | `[DECISION REQUIRED]`；REPORT-K **本轮未重跑** r67 ⇒ 旧 FAIL 主张 `UNVERIFIED（本轮未测）` |
| **Status** | `OPEN-BLOCKING`（阻塞「迁移后测试等价」声明） |
| **Evidence** | REPORT-I F9/§2.5；REPORT-K §6 |
| **Maps to** | OD-006；OD-010；F9 |

---

## 4. Cross-Index（与既有编号映射）

| OQ-GF | 既有映射 |
|-------|----------|
| 001 | OD-K-01；示例 OQ-001 |
| 002 | OD-K-02；OD-009；F8 |
| 003 | OD-K-03 |
| 004 | OD-K-04；示例 OQ-001 |
| 005 | OD-K-05 |
| 006 | UNKNOWN-002/005/006 |
| 007 | OD-K-07；UNKNOWN-003；示例 OQ-003 |
| 008 | 示例 OQ-002；关联 OD-K-02/04/05 |
| 009 | 示例 OQ-003；OD-K-07 |
| 010 | OD-K-09 |
| 011 | OD-K-06 |
| 012 | OD-K-10；UNKNOWN-001 |
| 013 | OD-K-08；F10 |
| 014 | F4/F5；REPORT-H Migration authority |
| 015 | F3；REPORT-H |
| 016 | OD-004；F6；REPORT-C |
| 017 | OD-001/002/003/008；Cluster B |
| 018 | OD-006/010；F9；Cluster E |

**额外 REPORT-K UNKNOWN 未单列成 OQ-GF 者**（仍有效，不在本册关闭）:

| 源 ID | 摘要 |
|-------|------|
| UNKNOWN-007 | REPORT-J 内容不存在 → 并入 OQ-GF-013 |
| UNKNOWN-008 | CLOSURE/DQ original 索引工件路径未定位 → 关联 OQ-GF-011 |
| UNKNOWN-009 | OCR 清单 1,103 条无 provenance 的真实产生时刻 → 关联 OQ-GF-007/012 |
| UNKNOWN-010 | 87/166 vs 「0/166 携带 sha」口径差 → 关联 OQ-GF-003/007 |

### 4.1 D-048 Known-Issue Binding Reference（v0.2 增补）

`[FACT]` Papers 侧已登记（**本册只做 binding reference，不关闭**）:

| issue_id | 摘要 | severity（源账本） | source_ledger |
|----------|------|--------------------|---------------|
| **D-048-1** | M5 subclass 绕过 | WARNING-hardening | `PREPROCESSING-PHASE25-GUARDIAN-REVIEW-v1.md`；ODR DEC-048；`Papers/COORDINATION/CURRENT.md` |
| **D-048-2** | M3 positional fallback | NOTE | 同上 |
| D-048-3 | 审查窗口 unknown actor deletions（tracked 文件；`git checkout` 恢复） | 见 Papers/REPORT-F | Papers CURRENT / DEC-048；**与** maintainess/PDF 误删恢复 **非同一事件** `[FACT: 文本对照]` |

`[PROPOSAL]` Binding-only 规则（硬约束）:

```text
ALLOWED:
  binding reference（在 GF-005 / EvidencePackage.known_issue_refs 登记）
  映射到 Papers 源账本 locator
  disposition = pending_owner_decision（M1–M5 默认）

FORBIDDEN:
  在 AITutor-X 治理文档中把 D-048-1/2/3 写成 closed / resolved
  以 GF patch 代为关闭 Papers 源账本
  silent empty（源账本有 issue 却在证据包中省略）
  把 binding reference 写成「已修复 / 已证实 fail-closed 无影响」的迁移放行依据
```

`[FACT]` Papers Guardian Review: 登记不代改；fail-closed 主张按源账本记录 — **本 patch 不改写该记录，不将其作为迁移授权**。

`[OWNER DECISION REQUIRED]` D-048-1/2/3 处置属 Papers/Owner 范围（DEC-049 语境）；GF 侧仅保持 binding。

### 4.2 Freeze-Readiness Blockers — 交叉引用（v0.2；**均保持 OPEN**）

`[FACT]` 来源 `REVIEW/GF-003/06_FREEZE_READINESS_ASSESSMENT.md`（assessed @ `5010c16`；GF blob 至 `e1beba3` 未变；v0.2 patch 后文本有增补但仍非 Frozen）。

`[PROPOSAL + OBSERVED]` 下列 blocker **不因** TASK-GF-005 关闭：

| Blocker | 摘要 | Current Status（不变） | v0.2 patch 触及？ |
|---------|------|------------------------|-------------------|
| **BL-09** | OQ-GF-014/015 + F4/F5 未决 | **OPEN-BLOCKING** `[OWNER DECISION REQUIRED]` | 否 — 文档仅引用 |
| **BL-10** | OQ-GF-001/002 未决 | **OPEN-BLOCKING** `[OWNER DECISION REQUIRED]` | 否 |
| **BL-11** | REPORT-G~K 处置 / Set B / REPORT-J | **OPEN-BLOCKING** `[OWNER DECISION REQUIRED]` | 否 — 仅登记 citation state（exists/untracked/referenced） |

`[PROPOSAL]` 其它 BL（01–08 文档缺口类）: v0.2 已**落盘部分字段**（Carrier/Restoration/Integrity、EvidencePackage v0.2 proposal、Artifact Registry、blocking_scope、冻结≠授权硬化句、V3 50 §3 对齐、DQ CONDITIONAL）— **但** REVIEW 06 的 Freeze 判定仍须 Owner 重新评审；**本 patch 不宣布 Frozen Baseline，不关闭 BL-01~08**。

---

## 5. Closure Protocol（关闭协议）

1. 仅 **Owner 书面裁决** 或 **可复现新证据** 可将状态改为 `CLOSED`。
2. 关闭时必须记录：决策摘要、证据引用、生效日期、对 GF 文档的影响。
3. 禁止以「迁移赶进度」为由把 `OPEN` 降级为默认假设。
4. 与源仓 OD-* 冲突时，**双轨保留**直至 Owner 指定唯一 mapping authority。

---

## 6. What This Registry Does Not Do

- 不解决任何条目
- 不创建源仓 DEC/BUG ID
- 不修改 REPORT-A~K 或 Papers 台账
- 不批准迁移
- **v0.2**: 不将 D-048-* 写成 closed/resolved；不关闭 BL-09/10/11；不宣布 Migration Ready

---

*GF-005 · **v0.2 DRAFT / PROPOSED** · TASK-GF-001（v0.1） + TASK-GF-005（v0.2 document patch） · 2026-09-18*
*新增 §1.1 blocking_scope · §4.1 D-048 binding-only · §4.2 BL-09/10/11 保持 OPEN-BLOCKING。*
*18 条 OQ-GF 零关闭；未授权迁移。*
