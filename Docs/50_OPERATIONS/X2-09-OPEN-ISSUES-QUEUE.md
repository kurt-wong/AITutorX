# X2-09 — Open Issues / Owner Decision Queue

> **[ARCHIVED 2026-09-27]** 本文件是**历史阶段快照**，记录产生时点的状态，**不构成现行依据**。
> **Superseded By**: [`Docs/50_OPERATIONS/CURRENT_STATE.md`](CURRENT_STATE.md) — 当前状态的唯一权威来源。
> 正文保持原样不改写（DOC-GOV §7）。档案基线：tag `AITutor-X-before-cleanup` @ `43f46e8`。


**Document ID**: X2-09
**Task**: TASK-X2-CLAUDE
**Document Type**: Operations / Open Issues Queue
**Status**: `ACTIVE — NOTHING CLOSED BY X2`
**Date**: 2026-09-18
**Upstream**: GF-005 OQ-GF；REPORT-E/H/I；Papers DEC-049；X2-01/07/08
**Hard rule**: X2 不关闭任何 OQ/BL/D-048；不代 Owner 决策

---

## 1. Inherited open set（状态不变）

### 1.1 OQ-GF（18 条，零 CLOSED）

OPEN-BLOCKING（仍 9）: **001, 002, 004, 007, 014, 015, 016, 017, 018**
OPEN: 003, 005, 006, 008–013

| OQ-GF | Topic | Owner decision already noted | Still open because |
|-------|-------|------------------------------|--------------------|
| 001 | 权威原始来源 | OD-04 Hash-based Identity | 实施/claim 细节；BL-10 |
| 002 | 数据权威模式 | OD-05 NAS read-only | mount/schema/权限/备份细节 |
| 004 | 双树保留策略 | 本批未裁 | 无 Owner 令不得删/合 |
| 007 | Lineage 补全 | OD-18 Difference Ledger；**明示不关** | disposition/补账未完成 |
| 014 | Migration Authority | OD-01 Charter 建立 | Charter requirements 未满足；BL-09 |
| 015 | Authority Taxonomy | OD-03 分层模型 | 完整执行状态未完成；BL-09 |
| 016 | DEC/BUG/OQ namespace | 未裁 | 阻塞 40_DECISIONS 填充 |
| 017 | Design/untracked + D2–D4 | 未裁 | authority unknown |
| 018 | 测试基线 / r67 | 未裁 | 阻塞「迁移后测试等价」 |

### 1.2 BL / D-048

| ID | Status | Note |
|----|--------|------|
| BL-09 | OPEN | Migration Authority / Taxonomy 执行 |
| BL-10 | OPEN | 数据模式实施 |
| BL-11 | OPEN | REPORT admission / Registry 实例 |
| D-048 | `pending_owner_decision` | binding ≠ closed |
| D-048-1 | WARNING-hardening | M5 subclass 绕过；建议 `type(val) is not str`；登记不代改 |
| D-048-2 | NOTE | M3 positional fallback |
| D-048-3 | UNKNOWN root cause | Papers tracked 文件未知删除后恢复 |

---

## 2. X2-audited additions to queue（**新登记，非关闭既有**）

| X2-Q ID | Issue | Class | Blocks | Related |
|---------|-------|-------|--------|---------|
| X2-Q-01 | Contract 状态叙事双文件规则 | authority | Contract 迁入 30_CONTRACTS 身份标签 | C-X2-01；REPORT-H |
| X2-Q-02 | REPORT-B 不存在文件名导致的错误 Class A 叙事 | evidence integrity | 资产登记可信度 | DL-11 |
| X2-Q-03 | 唯一 Mapping Authority 指定 | authority | 40_DECISIONS | OQ-GF-016 |
| X2-Q-04 | Ledger canonical 归属（Papers vs AITutorX） | operations | 50_OPERATIONS | C-X2-10 |
| X2-Q-05 | Observation Set B 提供或豁免 | evidence | 对账完整性 | OQ-GF-013；F10 |
| X2-Q-06 | D2/D3/D4 Owner must decide（Brief 三处填空） | implementation authority | Identity 迁移定性 | Papers DEC-049 |
| X2-Q-07 | Design v1.1 处置（commit/降级/working/v1.2） | authority | M1–M5 迁移身份 | OQ-GF-017 |
| X2-Q-08 | bytes 传输方式 | implementation | V3 重算验证 | OQ-12″ |
| X2-Q-09 | Semantic `unknown` 解冻 + reviewable record 载体 | implementation/architecture | C-X2-09 | BUG-V3-018 |
| X2-Q-10 | 图片恢复 Step5 / figure interoperability | data/material | Material pipeline | FACT-034 |
| X2-Q-11 | 12,707 口径更正载体 | documentation policy | 既有报告不可改写纪律 | OQ-GF-011 |
| X2-Q-12 | options_region 是否进生产 Resolver | architecture | EB-002 等 | FACT-005 |
| X2-Q-13 | EB-008 外部验证补证或降级主张 | evidence | Admission authority 叙事 | EB-008 |
| X2-Q-14 | REPORT-G/H/I/K OD-06 四步执行 | registry/admission | BL-11 | OD-06 |
| X2-Q-15 | Artifact Registry 实例路径/格式/admission 流程 | operations | OD-10 运营层 | OD-10 |
| X2-Q-16 | TEST canonical 基线受控重跑 | code/evidence | OQ-GF-018 | DL-07/08/09 |
| X2-Q-17 | V1/V2 provenance 范围是否需 formal registry | scope | archive 策略 | 任务书 3.4 |
| X2-Q-18 | AITutorX 是否引入协调账本文件（state.yaml 等） | operations | 统一状态 | 任务书 §11 |

---

## 3. Recommended Owner priority（`[PROPOSAL]`）

**P0（阻塞一切迁移）**
1. Charter 全文 + requirements（OQ-GF-014 / OD-01 / BL-09）
2. Gate 版本批准（REPORT-I F5）
3. Taxonomy 完整执行（OQ-GF-015 / OD-03）
4. Set B 提供或豁免（X2-Q-05）

**P1（阻塞设计/身份类迁移）**
5. Design v1.1 + untracked family（OQ-GF-017 / X2-Q-07）
6. D2/D3/D4（X2-Q-06）
7. Contract 状态叙事规则（X2-Q-01）
8. Namespace policy（OQ-GF-016 / X2-Q-03）

**P2（阻塞数据/测试主张）**
9. Data mode 实施（OQ-GF-002 / OD-05 / BL-10）
10. Test baseline（OQ-GF-018 / X2-Q-16）
11. Lineage/双树（OQ-GF-004/007）

**P3（治理运营）**
12. OD-06 四步；Registry 实例运营；Ledger 归属

---

## 4. Explicit non-actions

- X2 未改任何 OQ Status 为 CLOSED
- X2 未关 BL-09/10/11
- X2 未关 D-048
- X2 未裁 D2/D3/D4
- X2 未设立 Charter 正文
- X2 未宣布 Migration Ready / Gate Passed

---

*Open issues queue updated. Next actor = Owner.*
