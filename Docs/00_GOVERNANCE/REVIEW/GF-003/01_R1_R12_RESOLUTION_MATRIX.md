# 01 — DSH R1–R12 Resolution Matrix

**Document class**: REVIEW PROPOSAL（非 Frozen Authority）  
**Task**: TASK-GF-003-B Governance Review Artifact Export  
**Date**: 2026-09-18  
**Review base**: AITutor-X `main` @ `5010c1698f92e67b9fdf8776b5f66519c6c6d3f7`  
**Scope**: `Docs/00_GOVERNANCE/GF-000` ~ `GF-005`（只读评审，不改原文件）

**Classification discipline**:
- `[FACT]` — 仓库可复验，必须带证据引用
- `[PROPOSAL]` — 本 REVIEW 建议，**不是** Owner Decision，**不是**新治理原则
- `[UNKNOWN]` — 未验证，保持未知
- `[NEED OWNER DECISION]` — 仅 Owner 可裁

**Forbidden honored**: 未改 GF-000~005 · 未改 V3_SPEC · 未迁移 · 未关 OQ · 未把 proposal 写成 fact · 未假设 maintainess/original 权威 · 未降低 Gate 标准

---

## 0. Evidence Boundary（DSH R1–R12 原文状态）

| Statement | Classification | Evidence |
|-----------|----------------|----------|
| 完整「DSH Migration Engineer Review R1–R12」**未**在 AITutorX / Papers / AITutors-v3 检索到 | `[FACT]` | Glob `**/*DSH*` in AITutorX = 0；Grep 治理主题词 in AITutorX/Docs = 0；Papers `prd.md` R1–R12 = 批注规则；V3 `Status.md`/`log.md` R1–R12 = LLMExecutor 审查编号 |
| Papers 内存在可核验 DSH 材料 | `[FACT]` | `Papers/Docs/COORDINATION/INTEGRATION/PREPROCESSING-PHASE25-GUARDIAN-REVIEW-v1.md`；`PREPROCESSING-OWNER-DECISION-RECORD-v1.md`；`PREPROCESSING-D2-D3-D4-DECISION-BRIEF-v1.md`；`CURRENT.md`（DEC-048/049） |
| 任务书指定的 DSH 主题：Evidence Lifecycle、Carrier State、Known Issue Binding、Audit Artifact Registry | `[FACT from task briefing]` | 用户 TASK-GF-003 / TASK-GF-003-B 指令正文 |
| 下表 R1–R12 为**重构映射**，非 DSH 原文 | `[FACT]` | 重构依据 = 任务书主题 + Papers DSH 材料 + 仓库取证 + 前轮审查发现 |

**纪律**: 本矩阵**不得**被引用为「已审阅 DSH R1–R12 原文」。Owner 提供原文后须二次对照。

---

## 1. Per-Item Analysis（五问 + 状态）

| ID | 重构主题 | ①问题真实？ | ②违反 GF 原则？ | ③需改 GF？ | ④应转 OQ？ | ⑤仅表达问题？ | **当前状态** |
|----|----------|-------------|------------------|------------|-------------|----------------|--------------|
| R1 | Evidence Lifecycle / hash 验证时点 | **是** `[FACT]` REPORT-K §1.11 maintainess 误删→恢复→12,707；UNKNOWN-004 无恢复前全量 hash；GF-003 §3 无 `verification_timestamp` | **否**（P2/P5 未违反；原则未规定时点） | **是** | 可并 OQ-GF-005 语境 | **否** | **ACCEPTED** |
| R2 | Carrier State（数据随时间变化） | **是** `[FACT]` REPORT-K：日志 12,703 vs 恢复后 12,707，增减清单 NOT VERIFIED；数据树 `git ls-files=0` | **否**（GF-001 PIS 已否定「当前目录=历史 PIS」，无状态模型） | **是** | 可选 | **否** | **ACCEPTED** |
| R3 | Restoration Event 未建模 | **是** `[FACT]` REPORT-K 记恢复事件；GF-000~005 无 restoration 概念 | **否** | **是** | 交叉引用 **OQ-GF-005**，不新开 | **部分** | **ACCEPTED**（完整性标准本身见 OQ-GF-005） |
| R4 | EvidencePackage 执行字段不足 | **是** `[FACT]` GF-003 §3 无 timestamp/environment/test_baseline/known_issue_refs/restoration_event_refs/post_copy_sha256/approval_block | **否** | **是** | **否** | **否** | **ACCEPTED** |
| R5 | Known Issue Binding（D-048-1/2） | **是** `[FACT]` Papers Guardian Review：D-048-1 WARNING-hardening；D-048-2 NOTE；「登记不代改」 | **否**（REPORT-I 要求 known-issue 保留；GF schema 未落地） | **是** | GF 只定义 binding；**不**关 D-048 | **否** | **ACCEPTED**（binding 设计）；D-048 关闭 = **NEED OWNER DECISION**（Papers 侧） |
| R6 | Evidence-only Artifact Registry / untracked 引用 | **是** `[FACT]` `git ls-files Docs/60_REPORTS/`=A~F；G/H/I/K 磁盘有、commit 无；GF 引用 REPORT-I/K | **否**（B2 已有；缺工件分类与引用效力） | **是** | 映射 **OQ-GF-013**/F10 | **部分** | **ACCEPTED**（设计）；REPORT-G~K 处置 = **NEED OWNER DECISION** |
| R7 | 角色模型缺口（GOV/EVD/EXT） | **是** `[FACT]` GF-001 §2 仅 RSD/PIS/OCRA/SEM/MIG；V3_SPEC 50 §3 五类资产无角色 | **否** | **是** | 可选 | **否** | **ACCEPTED** |
| R8 | Interface Integrity ≠ Locator Integrity（LG-6） | **是** `[FACT]` REPORT-K：manifest sha 键 87/166；snapshot n=87 match 87；IR ADMITTED sha match **71** | **否** | **是** | **否** | **否** | **ACCEPTED** |
| R9 | 迁移分类 vs V3 50 资产清单 | **是** `[FACT]` V3_SPEC `50_Migration_Assets.md` §3 五类、§4 Golden、§5 绝不迁；GF-004 未一一映射 | **否** | **是** | **否** | **否** | **ACCEPTED** |
| R10 | Migration Authority / Gate 批准链 | **是** `[FACT]` REPORT-I F4 Charter 未设立；F5「本 REPORT-I 为草案」 | **否**（GF 已保留 UNKNOWN；风险=冻结间接升格） | **是（硬化句）** | 已有 **OQ-GF-014/015** | **部分** | 设计句 **ACCEPTED**；F4/F5/OQ-014/015 = **NEED OWNER DECISION** |
| R11 | Rollback / 迁移后验证缺失 | **是** `[FACT]` GF-002 §6 仅有 V-Bytes…V-Gate（迁移前）；无 rollback_ref / 漂移处置 | **否** | **是** | `[PROPOSAL]` 新 OQ-GF-019 | **否** | 字段设计 **ACCEPTED**；rollback 标准 = **NEED OWNER DECISION** |
| R12 | OQ 阻塞未按资产类分层 | **是** `[FACT]` GF-005 §1 统计 9 条 OPEN-BLOCKING，未分 doc/data/code/claim | **否** | **是** | **否** | **部分** | **ACCEPTED** |

---

## 2. Resolution Matrix（裁决 · 修改位置 · blocking）

| ID | 状态 | 对应修改位置 | 修改方式 `[PROPOSAL]` | Blocking 级别 | 依据证据 |
|----|------|--------------|----------------------|---------------|----------|
| R1 | ACCEPTED | GF-003 §3 schema | 增 `verification_timestamp` mandatory；`verification_environment` conditional | **BLOCKING-FREEZE** | REPORT-K §1.11；GF-003 §3 |
| R2 | ACCEPTED | GF-001 §2.2；GF-002 新节 | Carrier / Observation / State 概念 | **BLOCKING-FREEZE** | REPORT-K 恢复后计数 |
| R3 | ACCEPTED | GF-002；GF-003 字段 | Restoration Event + `restoration_event_ref`；交叉 OQ-GF-005 | **BLOCKING-FREEZE**（模型） | REPORT-K UNKNOWN-004 |
| R4 | ACCEPTED | GF-003 → v0.2 | 见 `03_EVIDENCE_PACKAGE_V0.2_SCHEMA.md` | **BLOCKING-FREEZE** | GF-003 §3 字段对照 |
| R5 | ACCEPTED | GF-003 Known Issue Binding；GF-004 | Asset→Issue→Disposition | **BLOCKING-FREEZE**（代码类） | Papers Guardian Review D-048-1/2 |
| R6 | ACCEPTED | GF-001/004 + Registry 节 | 四类工件 + untracked 引用规则 | **BLOCKING-FREEZE**；处置决策 OWNER | `git ls-files` A–F vs 磁盘 A–K |
| R7 | ACCEPTED | GF-001 §2 | 补 GOV/EVD/EXT（扩展） | **BLOCKING-FREEZE** | V3_SPEC 50 §3 |
| R8 | ACCEPTED | GF-002 §6；GF-003 verification | 双验证分列 + 状态枚举 | **BLOCKING-FREEZE** | REPORT-K 87/166、87/87、71 |
| R9 | ACCEPTED | GF-004 §3–§5 | 对齐 V3 50；见 `05_MIGRATION_GATE_SIMULATION_V0.2.md` | **BLOCKING-FREEZE** | V3_SPEC 50 §3/§5 |
| R10 | ACCEPTED（硬化表述） | GF-000 §6；GF-003 §5/§7 | 「GF 冻结 ≠ Gate 批准」显式句 | 表述 **BLOCKING-FREEZE**；Charter/裁决 = OWNER | REPORT-I F4/F5 |
| R11 | ACCEPTED | GF-003 §6 + schema | `rollback_ref` + 迁移后 mismatch 行 | 字段 **BLOCKING-FREEZE** | GF-002 §6 对照 |
| R12 | ACCEPTED | GF-005 增列 | `blocking_scope` 分层 | **BLOCKING-FREEZE**（评估依据） | GF-005 §1–§3 |

**状态统计**: ACCEPTED **12** · REJECTED **0** · DEFERRED **0** · 叠加 NEED OWNER DECISION：R5（D-048）、R6（REPORT-G~K）、R10（F4/F5/014/015）、R11（rollback 标准）

**Blocking 级别说明** `[PROPOSAL]`:
- **BLOCKING-FREEZE**: 未写入 GF v0.2 前，不建议将 GF 标为 Frozen Governance Baseline
- **NEED OWNER DECISION**: 本 REVIEW 不可代裁；设计可先写，裁决位保持 open

---

## 3. OQ Mapping（一律不关闭）

| DSH（重构） | 既有登记 | 本矩阵动作 |
|-------------|----------|------------|
| R1 / R3 | OQ-GF-005 | 交叉引用；**不关闭** |
| R6 | OQ-GF-013；REPORT-I F10 | 交叉引用；**不关闭** |
| R10 | OQ-GF-014；OQ-GF-015；F4/F5 | 交叉引用；**不关闭** |
| R5 | Papers D-048-1/2；OD-003 | 仅 binding 设计；**不关闭** |
| R8 | 关联 OQ-GF-003/007 | 不关闭 |
| R11 | `[PROPOSAL]` OQ-GF-019 | **不**在本 REVIEW 创建正式 GF-005 条目 |

---

## 4. Non-Actions

- 不修改 GF-000~GF-005 原文件
- 不修改 V3_SPEC / Papers / Contract
- 不执行迁移、不改数据、不改代码
- 不关闭任何 OQ / OD / F* / Cluster
- 不将 DSH 或本 REVIEW 建议写成 Owner Decision 或 FACT
- 不引入新治理原则

---

*01_R1_R12_RESOLUTION_MATRIX.md · Docs/00_GOVERNANCE/REVIEW/GF-003/ · TASK-GF-003-B · 2026-09-18*
