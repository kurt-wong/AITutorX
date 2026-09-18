# X2-00 — Unified Governance Stage State

**Document ID**: X2-00
**Task**: TASK-X2-CLAUDE
**Document Type**: Operations / Stage State
**Status**: `ACTIVE — X2 DOCUMENT GOVERNANCE`
**Authority**: AITutorX 目标系统文档治理（**非** Migration Authorization）
**Date**: 2026-09-18
**Parent Governance**: GF v0.2 Frozen（`Docs/00_GOVERNANCE/GF-000` … `GF-006`）
**Decision actor**: Owner；Claude 仅 document verification / audit registration
**Referenced by**: `README.md`；`Docs/60_REPORTS/REPORT-X2-UNIFIED-GOVERNANCE.md`；X2-01~X2-10 文首字段

---

## 0. Hard Boundaries（本阶段不可突破）

```text
AITutorX Unified Documentation Governance ≠ Migration Authorization
X2 Audit Registration ≠ Gate Passed
Migration Candidate ≠ Migrated
Document commit/push ≠ Migration Authorized
Freeze ≠ Implementation
Contract Freeze ≠ V3 Implementation Capability
```

**禁止（本阶段逐字保留）**:
- 直接迁移 V3 / preprocessing 生产代码
- 删除旧仓库内容
- 修改 V3 Frozen Spec / Frozen Contract v0.2
- 擅自重新定义 Owner Decision
- 创建新治理体系取代 GF v0.2
- 通过复制文件假装完成迁移
- 把 proposal 写成 fact
- 把 migration candidate 写成 migrated
- 宣布 Migration Ready / Gate Passed
- 关闭未裁决 OQ / BL / D-048
- 将任何资产标为 `admitted=true`

---

## 1. Git FACT（本阶段审计时点 2026-09-18）

`[FACT]` 三仓 remote HEAD（`git rev-parse` + `git status -sb` + `gh api` 亲验）:

| Role | Repo | Local path | HEAD = origin/main | Sync |
|------|------|------------|--------------------|------|
| **Governance / Target** | `kurt-wong/AITutorX` | `D:\Project\AITutor-X` | `331cbea1e4018b6929e1f876bea22a528817f3d3` | IN SYNC |
| **Consumer (V3 domain)** | `kurt-wong/AITutors-v3` | `D:\Project\AITutors-v3` | `cc12d79e9a22f6274100ea0bb61f92493ba88509` | IN SYNC |
| **Producer (preprocessing domain)** | `kurt-wong/Aitutors-preprocessing` | `D:\Project\Papers` | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` | IN SYNC |

`[FACT]` Contract Freeze Object（唯一冻结对象，双仓账本一致）:

```text
repository = kurt-wong/AITutors-v3
commit     = f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1
document   = Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
sha256     = 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
```

`[FACT]` Freeze Registration commit ≠ Freeze Artifact；`c6e771c` 已排除，不得引用为冻结对象。

`[FACT]` Local path 与 GitHub name 不一致（以 git 实测为准）:
- Governance local = `D:\Project\AITutor-X`（含连字符）；GitHub = `AITutorX`
- Producer local = `D:\Project\Papers`；GitHub = `Aitutors-preprocessing`
- `[OBSERVED]` REPORT-G 登记：`D:\Project\AITutors-X` 为空目录、无 `.git`，易混淆

---

## 2. GitHub baseline vs local working tree（citation state）

`[FACT]` V3 GitHub `main` Docs 子目录仅含: `ARCHIVE` / `COORDINATION` / `DECISIONS` / `REPORTS` / `V3_SPEC` / `reference`。

`[FACT]` **GitHub main 上不存在** `Docs/GOVERNANCE/`。本地 `D:\Project\AITutors-v3\Docs\GOVERNANCE\` 为 **untracked**：

| File | exists | tracked(GitHub) | authority |
|------|--------|-----------------|-----------|
| `00-SYSTEM-BASELINE.md` | YES | NO | `[UNKNOWN]` |
| `02-AUTHORITY-MATRIX.md` | YES | NO | `[UNKNOWN]` |
| `03-DECISION-REGISTRY.md` | YES | NO | `[UNKNOWN]` |
| `04-CLAIM-REGISTRY.md` | YES | NO | `[UNKNOWN]` |

`[FACT]` V3 untracked `Docs/COORDINATION/CONTRACTS/` 共 9 文件（DESIGN v1/v1.1、IMPLEMENTATION-PLAN/READINESS/REPORT-PHASE1/2、CONSUMER-REVIEW 早期版、SKELETON、`PREPROCESSING-V3-CONTRACT.md` v0.1）；GitHub `contents/Docs/COORDINATION/CONTRACTS` 仅返回 9 个 **tracked** 文件名，与 untracked 清单无交集。

`[FACT]` AITutorX untracked: `REPORT-G` / `REPORT-H` / `REPORT-I` / `REPORT-K`（exists=YES；tracked=NO；admitted=`[UNKNOWN]`；OD-06 整理后收编）。

`[FACT]` 本阶段审计以 **GitHub remote main + 本地 tracked 对账** 为基础；untracked 文件仅登记 citation state，**不升格为权威**。

---

## 3. Input Repositories（本阶段输入面）

| Input | Path / Remote | Scope used |
|-------|---------------|------------|
| AITutorX | `D:\Project\AITutor-X` / GitHub | GF v0.2、REPORT-A~K、AGENTS.md、README、空骨架目录 |
| AITutors-v3 | `D:\Project\AITutors-v3` / GitHub | V3_SPEC frozen、DECISIONS、REPORTS、COORDINATION、backend/frontend 结构、DICTIONARY |
| Aitutors-preprocessing | `D:\Project\Papers` / GitHub | prd.md、governance/、Docs/COORDINATION、scripts/ocr_service/tests、数据树（只读观测） |
| V1/V2 (provenance only) | `D:\Project\AITutors-v1` / `AITutors-v2` / GitHub `AITutor-V2` | 仅作 provenance 标注；**非**本阶段治理对象 |

`[FACT]` AITutorX README 已将 Producer/Consumer 登记为来源仓；目标结构为统一 AITutorX，而非并列两项目 Docs。

---

## 4. Completed in TASK-X2-CLAUDE

1. 三仓 GitHub/本地 HEAD 与 citation state 重核对（不依赖旧报告结论）
2. 建立 AITutorX Unified System Lifecycle 基线（阶段 × 来源 × 文档 × 代码 × Contract × 证据）
3. 统一文档治理地图（族级 classification：MIGRATE/MERGE/SUPERSEDE/ARCHIVE/REJECT/RETAIN-AS-HISTORICAL/UNKNOWN）
4. 统一概念/术语表（含 Material 非纯文字、双状态词表、identity 键）
5. 统一架构模型（preprocessing = Producer 能力域；V3 = Semantic/Question Consumer 能力域；边界为内部边界）
6. Cross-System Contract Audit（Identity/Manifest/OCR/IR/Material/Question/QuestionInstance/Knowledge/State）
7. Decision Mapping / Difference Ledger / Migration Candidate Registry（**登记，不重编号历史 ID**）
8. Open Issues / Owner Decision Queue 更新
9. Migration Readiness Assessment（**当前全部未授权迁移**）
10. REPORT-X2 汇总 + 本 STATE 文档持久化

---

## 5. Not Completed / Out of Scope this stage

- 生产代码迁移 / 数据迁移 / NAS 配置 / DB schema 变更
- Migration Authority Charter 正文（OD-01 已裁建立；requirements 未满足）
- Artifact Registry **admission 实例**（OD-10 建立决策已裁；X2 仅建审计登记文档）
- OQ-GF / BL / D-048 关闭
- D2/D3/D4 Owner 裁决（Papers DEC-049 Brief 等待 Owner）
- Observation Set B 导入
- REPORT-G/H/I/K 的 `admitted=true`
- File-level 100% 逐文件 documentation map（本阶段为族级 + 代表路径；缺口显式标 UNKNOWN）

---

## 6. Current Governance Snapshot

| Item | State |
|------|-------|
| GF v0.2 | FROZEN（OD-14）；freeze ≠ auth |
| Migration Authorization | **UNAVAILABLE**（OD-01；Charter requirements 未满足） |
| `approval_block.status` | `invalid_without_charter` `[FACT]` |
| OQ-GF | 18 条；**零 CLOSED**；OPEN-BLOCKING 仍 9（001/002/004/007/014/015/016/017/018） |
| BL-09 / BL-10 / BL-11 | OPEN |
| D-048 | `pending_owner_decision`（binding ≠ closed） |
| Contract v0.2 | FROZEN content object；**五项 V3 capability NOT IMPLEMENTED** |
| AITutorX code tree | `preprocessing/` `backend/` `frontend/` `tools/` `archive/` 均为 `.gitkeep` 空骨架 |
| admitted=true | 无任何资产 |

---

## 7. Next Phase（本阶段完成后）

**下一 actor = Owner。**

建议 Owner 处置序列（`[PROPOSAL]`，非 Owner 令）:
1. Migration Authority Charter 全文 + requirements satisfied 判定
2. Authority Taxonomy 完整执行（OD-03 分层模型落地）
3. DEC/BUG/OQ namespace 政策（OQ-GF-016）
4. Design v1.1 / untracked 契约族 authority（OQ-GF-017；D2/D3/D4 Brief）
5. Data authority mode 实施细节（OD-05 / OQ-GF-002）
6. REPORT-G/H/I/K OD-06 四步收编
7. Difference Ledger 对 71/87/166 disposition（OD-18）

**本阶段完成后停止。** 不自行进入 Migration Gate。不自行迁移生产代码。

---

## 8. Allowed / Not Allowed after X2 commit

**允许**:
- 以 X2 文档为审计基线继续 Owner 决策
- 在受控 patch 下修订 X2 文档（不覆盖历史）

**不允许**:
- 把 X2 报告当作 Gate Passed
- 把 Migration Candidate Registry 当作已迁移清单
- 跳过 Charter/Gate 直接 copy 代码进 AITutorX active tree

---

*End State: AITutorX X2 Unified Documentation Governance Registered.*
*Migration remains UNAUTHORIZED.*
