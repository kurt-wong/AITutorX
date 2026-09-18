# GF-005 — Open Questions Registry

**Document ID**: GF-005
**Status**: `FROZEN GOVERNANCE BASELINE`（OD-14）— 登记册文本已冻结；**不**在此文件内关闭未裁决 UNKNOWN
**Version**: **v0.2 Frozen**（TASK-GF-005 patch + **TASK-GF-008** Owner Decision Resolution 注记）
**Role**: Independent System Governance Architect（TASK-GF-001）；决策 actor = Owner
**Date**: 2026-09-17（v0.1） / 2026-09-18（v0.2 patch） / **2026-09-18**（v0.2 freeze + decisions）
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Decision record**: `GF-006-OWNER-DECISION-RECORD.md`（**正典**；本册 §7 为交叉索引）
**Naming note**: 本登记册使用 **`OQ-GF-###`** 前缀，以免与 Papers/历史文档中的 OQ 编号冲突。每条映射既有 OD-* / REPORT-K UNKNOWN-* / REPORT-H Cluster，**不替代**源仓原始编号。

**Discipline**: 不把 UNKNOWN 写成 FACT；不以假设关闭问题；关闭仅能由 Owner 书面裁决或可复现新证据。
**v0.2 labels**: `[FACT]` / `[OBSERVED]` / `[PROPOSAL]` / `[OWNER DECISION REQUIRED]` / `[UNKNOWN]`
**v0.2 freeze labels**: `[OWNER DECISION]`
**v0.2 non-action**: TASK-GF-005 零关闭；**TASK-GF-008 亦未将任何 OQ-GF Status 改为 CLOSED**；未关闭 BL-*；未关闭 D-048。

**Importers / cross-refs**: GF-000 §7；GF-001 §4；GF-002 §7/§8/§9 Open Items；GF-003 §3.2.3；REVIEW/GF-003/06 BL-09/10/11；GF-006 §9/§11；无代码 import。

---

## 1. Registry Summary

| 状态 | 含义 |
|------|------|
| `OPEN` | 无足够证据，待 Owner 或后续取证 |
| `OPEN-BLOCKING` | 阻塞迁移/数据引用/身份声明 |
| `MAPPED` | 已有对应 OD/REPORT 条目，本册只做治理索引 |
| `STALE-CANDIDATE` | 外部状态可能已变，需 Owner 确认关闭或重开 |

**统计（TASK-GF-008 后）**: 登记仍为 **18** 条 OQ-GF；**零 CLOSED** `[FACT: 本批未改任何 Status 为 CLOSED]`。其中 **OPEN-BLOCKING 仍为 9**（001/002/004/007/014/015/016/017/018）— 决策已注记 ≠ 执行状态完成。OQ-GF-003/005/006/008–013 保持 OPEN。

`[FACT]` **Decision ≠ Status CLOSED**: Owner 决策写入 §7 / GF-006；各 OQ Status 仅在执行/实施要求满足且 Owner 确认关闭协议后方可改。

### 1.1 blocking_scope 分层（v0.2 增补；决策后注记）

`[FACT]` 为每条 OPEN-BLOCKING 项标注 **blocking_scope**，说明「阻塞哪一类动作」。**分层不降低停止线**；`any-migration` 项仍由 REPORT-I §0.7 默认全禁迁移管辖。

| Scope | Meaning |
|-------|---------|
| `doc` | 阻塞治理文档冻结 / 权威叙事成文 |
| `data` | 阻塞数据本体引用/交付/迁入 |
| `code` | 阻塞代码模块迁入或「迁移后测试等价」声明 |
| `claim` | 阻塞 lineage verified / 来源已验证 等主张 |
| `authority` | 阻塞 Migration Authority / Gate 9 / taxonomy 生效 |

`[FACT]` 当前 OPEN-BLOCKING 分层（**Status 不变**）+ Owner Decision 注记:

| OQ-GF | Status（不变） | blocking_scope `[FACT]` | Owner Decision（TASK-GF-008） | 仍阻塞的原因 |
|-------|----------------|------------------------------|-------------------------------|--------------|
| 001 权威原始来源 | OPEN-BLOCKING | `data` + `claim` + `authority` | **OD-04** Hash-based Source Identity | 交付/实施与 claim 细节未完成；BL-10 OPEN |
| 002 数据权威模式 | OPEN-BLOCKING | `data` | **OD-05** NAS-backed read-only | 具体实施细节未完成；BL-10 OPEN |
| 004 双树保留策略 | OPEN-BLOCKING | `data` + `authority` | **本批未裁** | 无 Owner 令不得删/合任一树 |
| 007 Lineage 补全 | OPEN-BLOCKING | `claim` + `data`（大规模 verified） | **OD-18** Difference Ledger；**明示不关闭** | 差值 disposition / 补账未完成 |
| 013 Set B / REPORT-J | OPEN | `claim` + `doc` | **OD-06** REPORT-G~K 整理后收编；Set B/J 本批未裁 | admission 未完成；REPORT-J 仍不存在；BL-11 OPEN |
| 014 Migration Authority | OPEN-BLOCKING | `authority`（+ 阻塞 Gate 9） | **OD-01** 建立 Charter；Authorization unavailable | Charter requirements 未满足；BL-09 OPEN |
| 015 Authority Taxonomy | OPEN-BLOCKING | `authority` + `doc` | **OD-03** 分层模型（禁止互替） | 完整执行状态未完成；BL-09 OPEN |
| 016 DEC/BUG/OQ namespace | OPEN-BLOCKING | `doc` + `authority` | **本批未裁** | 阻塞 40_DECISIONS 填充 |
| 017 Design/untracked + D2-D4 | OPEN-BLOCKING | `code` + `authority` + `doc` | **本批未裁** | M1–M5 / DESIGN-v1.1 |
| 018 测试基线 / r67 | OPEN-BLOCKING | `code` + `claim` | **本批未裁** | 阻塞「迁移后测试等价」声明 |

`[FACT]` v0.1 事实保持: OQ-GF-013 在 v0.1 标 `OPEN`（非 OPEN-BLOCKING）；上表分层为治理提示。

`[OWNER DECISION REQUIRED]` blocking_scope 词表是否正式采纳；是否新增 OQ-GF-019（rollback / 迁移后验证标准）— **本批未裁，不新建 OQ**。

---

## 2. Source Lineage & Data Authority

### OQ-GF-001 — 权威原始来源未定义

| Field | Value |
|-------|-------|
| **Question** | preprocessing 的 canonical source corpus 是 `maintainess/PDF`、`original/`，还是「双层：original=原件库 / maintainess=OCR 队列」？ |
| **Classification** | `[UNKNOWN]` → 方向仍 `[UNKNOWN]`；身份模型已裁 |
| **Status** | `OPEN-BLOCKING` |
| **Owner Decision** | `[OWNER DECISION]` **OD-04**（2026-09-18）: Hash-based Source Identity；**不**建立永久排序；双树均为输入来源；content hash 一致 ⇒ 同一 Source Identity |
| **Evidence** | REPORT-K §2/§5：operational input = maintainess/PDF `[FACT]`；original 更大且高重叠 `[FACT]`；抽样 sha 一致 `[FACT]` |
| **Maps to** | OD-K-01；GF-006 §5 |
| **Must not** | 把 OD-04 读成「maintainess = canonical」或「original = canonical」 |
| **Still open because** | 交付/实施与 claim 细节未完成；BL-10 OPEN；本 Status 非自动 CLOSED |

### OQ-GF-002 — 数据权威与引用/交付模式

| Field | Value |
|-------|-------|
| **Question** | AITutorX/下游引用数据采用 path-ref / NAS / copy / 仅 hash 清单 / 其他？ |
| **Classification** | 模式已裁；实施细节 `[UNKNOWN]`/OPEN |
| **Status** | `OPEN-BLOCKING` |
| **Owner Decision** | `[OWNER DECISION]` **OD-05**（2026-09-18）: NAS-backed Read-only Data Model（NAS=语料；Docker=read-only mount；DB=结构化对象；Repo=测试资产） |
| **Evidence** | REPORT-I F8 / OD-009 / GAP-007；数据 ignored `[FACT]` |
| **Maps to** | OD-K-02；OD-009；GF-006 §6；GF-004 §2.0 |
| **Must not** | 将全部数据复制进代码仓；将 NAS 数据视为 Docker 生命周期数据 |
| **Still open because** | **具体实施细节**（mount 路径、schema、权限、备份）未完成；BL-10 OPEN |

### OQ-GF-003 — `SHA256(original source bytes)` 词义 vs 目录

| Field | Value |
|-------|-------|
| **Question** | 是否强制在治理/Contract 文档中显式区分 identity 词面与物理目录 `D:\Project\Papers\original`？ |
| **Classification** | `[FACT]` 二者概念不同；是否强制双标注 = `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Owner Decision** | **本批未裁** |
| **Evidence** | REPORT-K §4.1；snapshot 行 source 指向 md `[FACT]`；GF-002 §4 |
| **Maps to** | OD-K-03 |
| **Note** | OD-04 Hash-based Identity **不**自动关闭本条 |

### OQ-GF-004 — 双树重叠副本的保留策略

| Field | Value |
|-------|-------|
| **Question** | `maintainess/PDF` 与 `original/` 高重叠（basename 交集 12,626；抽样 6/6 sha 一致）是否保留双份？若否，保留哪侧、谁执行校验/合并？ |
| **Classification** | `[UNKNOWN]` 关系方向；策略 = `[DECISION REQUIRED]` |
| **Status** | `OPEN-BLOCKING` |
| **Owner Decision** | **本批未裁** |
| **Evidence** | REPORT-K §1.7–1.8、§8 OD-K-04 |
| **Maps to** | OD-K-04；GF-006 §5.5 Non-authorizations |
| **Must not** | 在无 Owner 令下删除/合并任一树 |

### OQ-GF-005 — maintainess 恢复完整性证据标准

| Field | Value |
|-------|-------|
| **Question** | Owner 是否接受「数量 12,707 + 抽样 hash」作为误删恢复完成的充分证据，还是要求恢复前后全量 hash 台账？ |
| **Classification** | `[DECISION REQUIRED]`；恢复前全量 hash = `[UNKNOWN]`（可能不存在） |
| **Status** | `OPEN` |
| **Owner Decision** | **本批未裁** |
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
| **Owner Decision** | `[OWNER DECISION]` **OD-18**（2026-09-18）: 建立 Difference Ledger；`87`/`71`/`166` 引用必须关联 difference disposition；**本决定不关闭本条** |
| **Evidence** | REPORT-K §4.2、UNKNOWN-003、OD-K-07；任务书 OQ-003；GF-002 §9.3 |
| **Maps to** | OD-K-07；UNKNOWN-003；GF-006 §7 |
| **Still open because** | Owner 明示 OD-18 不关本条；Difference Ledger 实例未创建；lineage 补账/Producer 任务书未完成 |

### OQ-GF-008 — 是否需要全量 source hash inventory

| Field | Value |
|-------|-------|
| **Question** | 是否要求对 RSD/PIS 候选树建立全量 `path → sha256` 台账？成本与存放位置？ |
| **Classification** | `[DECISION REQUIRED]` |
| **Status** | `OPEN` |
| **Owner Decision** | **本批未裁** |
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

### OQ-GF-013 — Observation Set B / REPORT-J / REPORT-G~K

| Field | Value |
|-------|-------|
| **Question** | 外部 DSH Observation Set B 是否导入？`REPORT-J` 是否曾存在/将交付？REPORT-G/H/I/K 如何处置？ |
| **Classification** | `[FACT]` AITutorX 无 REPORT-J；Set B 未导入；REPORT-G~K untracked；其余 `[UNKNOWN]` |
| **Status** | `OPEN`（F10） |
| **Owner Decision** | `[OWNER DECISION]` **OD-06**（2026-09-18）: REPORT-G/H/I/K = **整理后收编**（Evidence Package → identity → Registry → admission）；当前 **不得** `admitted=true`。Set B / REPORT-J **本批未裁** |
| **Evidence** | REPORT-K §1.10、§6；REPORT-I F10；GF-000 §3.3.2；GF-004 §2.2 |
| **Maps to** | OD-K-08；F10；GF-006 §8 |
| **Still open because** | admission 实际未完成；Registry 实例未创建；Set B/J 未决；BL-11 OPEN |

### OQ-GF-014 — Migration Authority / Gate 批准链

| Field | Value |
|-------|-------|
| **Question** | Migration Authority 由谁担任？Gate 版本（REPORT-I）谁批准？批准记录格式与存放路径？ |
| **Classification** | Charter 建立已裁；执行/requirements `[UNKNOWN]` |
| **Status** | `OPEN-BLOCKING`（Cluster A） |
| **Owner Decision** | `[OWNER DECISION]` **OD-01**（2026-09-18）: **建立** Migration Authority Charter；Charter 目的=明确审批资格/记录格式/保存位置；**当前不授予任何迁移执行权限**；`Migration Authorization remains unavailable until Charter requirements are satisfied.` Gate 版本（F5）**本批未裁** |
| **Evidence** | REPORT-I F4/F5、§2.1 P0；GF-003 §3.2.2 |
| **Maps to** | REPORT-H Migration authority；F4/F5；GF-006 §2 |
| **Still open because** | Charter 全文与 requirements satisfied 判定未落盘；approval_block 仍 = `invalid_without_charter`；BL-09 OPEN |

### OQ-GF-015 — 唯一 Authority Taxonomy

| Field | Value |
|-------|-------|
| **Question** | AITutor-X 采用哪套层级（报告中存在多套 L* 叙述 vs V3 90/91 vs AGENTS.md）？ |
| **Classification** | 分层模型已裁；完整执行 `[UNKNOWN]`/OPEN |
| **Status** | `OPEN-BLOCKING` |
| **Owner Decision** | `[OWNER DECISION]` **OD-03**（2026-09-18）: **分层模型**；第一层 Authority Domain（GOV/EVD/EXT）+ 第二层 Artifact Role（RSD/PIS/OCRA/SEM/MIG）；**不废弃现有分类**；**禁止互相替代** |
| **Evidence** | REPORT-I F3；V3 `90/91`；`AGENTS.md` L0–L7；GF-001 §2.6 |
| **Maps to** | F3；REPORT-H；GF-006 §4 |
| **Still open because** | 「Taxonomy **完整执行状态**」属 BL-09；本批未宣布执行落地完成 |

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

`[FACT]` **TASK-GF-008**: D-048 **保持** `pending_owner_decision`；不关闭；不写成 resolved。

### 4.2 Freeze-Readiness Blockers — 交叉引用（TASK-GF-008 后）

`[FACT]` 来源 `REVIEW/GF-003/06_FREEZE_READINESS_ASSESSMENT.md`（assessed @ `5010c16`；GF blob 至 `e1beba3` 未变；v0.2 patch 后文本有增补）。

`[OWNER DECISION]` **OD-14**: GF v0.2 文本 **已冻结**（FROZEN GOVERNANCE BASELINE）。冻结 **≠** 下列 blocker 关闭。

`[FACT]` 下列 blocker **不因** TASK-GF-005 / TASK-GF-008 关闭:

| Blocker | 摘要 | Current Status | TASK-GF-008 触及？ |
|---------|------|----------------|-------------------|
| **BL-09** | Migration Authority / Gate / Taxonomy **完整执行状态** | **OPEN** `[OWNER DECISION REQUIRED]` | OD-01/OD-03 **记录决策**；**不**关闭 — Charter requirements 未满足；Gate F5 未裁；taxonomy 执行状态未完成 |
| **BL-10** | 数据交付 **具体实施细节** | **OPEN** `[OWNER DECISION REQUIRED]` | OD-04/OD-05 **记录决策**；**不**关闭 — mount/schema/权限等实施未完成 |
| **BL-11** | REPORT-G~K Registry admission **实际完成** / Set B / REPORT-J | **OPEN** `[OWNER DECISION REQUIRED]` | OD-06/OD-10 **记录决策**；**不**关闭 — 整理后收编未执行；admitted≠true |
| **D-048** | Papers known-issue | `pending_owner_decision` | **保持** pending；binding-only |

`[FACT]` 其它 BL（01–08 文档缺口类）: v0.2 文本字段已落盘 + OD-14 已冻结治理文本；**不**自动等于迁移授权；执行类前置仍以 BL-09/10/11 与 Cluster 停止线为准。

---

## 5. Closure Protocol（关闭协议）

1. 仅 **Owner 书面裁决** 或 **可复现新证据** 可将状态改为 `CLOSED`。
2. 关闭时必须记录：决策摘要、证据引用、生效日期、对 GF 文档的影响。
3. 禁止以「迁移赶进度」为由把 `OPEN` 降级为默认假设。
4. 与源仓 OD-* 冲突时，**双轨保留**直至 Owner 指定唯一 mapping authority。
5. `[FACT]` **TASK-GF-008 纪律**: 本批已记录的 `[OWNER DECISION]`（OD-01/03/04/05/06/10/14/18）**本身不等于**对应 OQ/BL 的 Status=CLOSED。执行/实施要求满足后，Owner 方可按本协议另行确认关闭。

---

## 6. What This Registry Does Not Do

- 不解决任何未在 §7 注记的条目
- 不创建源仓 DEC/BUG ID
- 不修改 REPORT-A~K 或 Papers 台账
- 不批准迁移
- **TASK-GF-008**: 不将 D-048-* 写成 closed/resolved；不关闭 BL-09/10/11；不宣布 Migration Ready；不创建 Registry 实例；不将任何 OQ-GF Status 改为 CLOSED

---

## 7. Owner Decision Resolution（TASK-GF-008 交叉索引）

**正典**: `GF-006-OWNER-DECISION-RECORD.md`。本节为登记册侧索引，**不**新增决策。

| Decision ID | Status | Date | Scope（摘要） | Non-authorizations（摘要） | 关联 OQ / BL |
|-------------|--------|------|---------------|---------------------------|--------------|
| **OD-14** | `[OWNER DECISION]` | 2026-09-18 | GF v0.2 → Frozen Governance Baseline；必须写入 freeze≠auth 声明 | NOT Migration Authorization / Ready / Gate pass / OQ·BL close | OQ-GF-014 交叉；全部 BL |
| **OD-01** | `[OWNER DECISION]` | 2026-09-18 | 建立 Migration Authority Charter（资格/格式/保存位置） | NOT 迁移执行权限；NOT requirements 已满足；NOT approval_block=valid | OQ-GF-014；BL-09；F4 |
| **OD-10** | `[OWNER DECISION]` | 2026-09-18 | 建立 Artifact Registry（解决 citation state 混淆） | NOT 实例创建；NOT 导入 Artifact；NOT 改 admitted | OQ-GF-013 交叉；BL-04/11 |
| **OD-03** | `[OWNER DECISION]` | 2026-09-18 | 分层 Taxonomy：Domain（GOV/EVD/EXT）+ Artifact Role（RSD/PIS/…）；禁止互替 | NOT 废弃任一层；NOT OQ-GF-015/BL-09 关闭；NOT 执行完成 | OQ-GF-015；BL-09；F3 |
| **OD-04** | `[OWNER DECISION]` | 2026-09-18 | Hash-based Source Identity；双树均为输入来源；hash 一致=同一 Identity | NOT 指定 canonical 目录；NOT 删/合树；NOT BL-10 关闭 | OQ-GF-001/004；BL-10 |
| **OD-05** | `[OWNER DECISION]` | 2026-09-18 | NAS-backed Read-only Data Model（NAS/Docker mount/DB/Repo 四层） | NOT 数据已迁入；NOT schema/mount 已实施；NOT OQ-GF-002/BL-10 关闭 | OQ-GF-002；BL-10；F8 |
| **OD-18** | `[OWNER DECISION]` | 2026-09-18 | 建立 Difference Ledger；87/71/166 引用须关联 disposition | NOT OQ-GF-007 关闭；NOT ledger 实例已创建；NOT verified 大规模声明 | OQ-GF-007（明示不关） |
| **OD-06** | `[OWNER DECISION]` | 2026-09-18 | REPORT-G/H/I/K 整理后收编（四步流程） | NOT admitted=true；NOT 收编完成；NOT BL-11/OQ-GF-013 关闭 | OQ-GF-013；F10；BL-11 |

**本批未裁（保持 `[OWNER DECISION REQUIRED]` / OPEN）**: OQ-GF-003/004/005/008/009/010/011/012/016/017/018；Set B / REPORT-J；Gate 版本 F5；blocking_scope 词表采纳 / OQ-GF-019；D-048 disposition；TASK-GF-007 Matrix 中未出现在 brief 的 OD-02/07/08/09/11/12/13/15/16/17/19/20。

**边界（不变）**:

```text
Frozen Governance Baseline does not imply Migration Authorization.
Migration Authority ≠ Migration Execution
Decision ≠ Migration Approval
Decision recorded ≠ OQ/BL Status CLOSED
```

---

*GF-005 · **v0.2 FROZEN GOVERNANCE BASELINE** · TASK-GF-001（v0.1） + TASK-GF-005（v0.2 patch） + **TASK-GF-008（Owner Decision Resolution）** · 2026-09-18*
***Frozen Governance Baseline does not imply Migration Authorization.***
*18 条 OQ-GF **零 CLOSED**；OPEN-BLOCKING 仍为 9；BL-09/10/11 OPEN；D-048 pending_owner_decision。*
*决策正典 = GF-006；本册 §7 仅为交叉索引；未授权迁移。*
