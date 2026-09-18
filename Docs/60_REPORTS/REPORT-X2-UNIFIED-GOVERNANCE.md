# REPORT-X2 — AITutorX Unified Documentation Governance & Cross-System Architecture Integration

**Report ID**: REPORT-X2
**Task**: TASK-X2-CLAUDE；X2.1 = Evidence Anchor Consistency Correction
**Date**: 2026-09-18
**Role**: Document verification / audit registration（**Decision actor = Owner**）
**Method**: 三仓 GitHub + 本地 git 实测重核对 + 权威文档亲读；**不**仅依据既有 Claude/DSH 报告
**Evidence Anchor（current）**: AITutorX `7002f38` · V3 `cc12d79` · Papers `2b92898` · Contract freeze object `f4941ff` / sha256 `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528`
**Historical audit parent（非 current HEAD）**: AITutorX `331cbea`

---

## 0. Verdict（先读这个）

```text
AITutorX 已建立同时解释 V3 与 preprocessing 的统一项目级文档治理模型。
重要资产已在 registry/audit 层可追溯：来源 / 当前状态 / 权威依据 / 迁移结论（多为 GATE_BLOCKED 或 UNKNOWN）。

NOT:
  Migration Authorized
  Migration Ready
  Gate Passed（任何 Gate）
  Production code migrated
  Data migrated
  OQ/BL/D-048 Closed
  admitted=true（任何资产）
```

**Boundaries held**:
- Freeze ≠ Migration Authorization
- Migration Authority ≠ Migration Execution
- Decision ≠ Migration Approval
- Document commit ≠ Migration Authorized
- Migration Candidate ≠ Migrated
- Contract Freeze ≠ V3 Implementation Capability

---

## 1. Deliverables（本阶段输出清单）

| # | Requirement | Artifact |
|---|-------------|----------|
| 1 | X2 Claude Report | **本文件** |
| 2 | Unified System Baseline | `Docs/20_ARCHITECTURE/X2-01-UNIFIED-SYSTEM-BASELINE.md` |
| 3 | Unified Documentation Map | `Docs/10_SPEC/X2-05-UNIFIED-DOCUMENTATION-MAP.md` |
| 4 | Unified Architecture Baseline | `Docs/20_ARCHITECTURE/X2-02-UNIFIED-ARCHITECTURE-BASELINE.md` |
| 5 | Concept / Terminology Map | `Docs/10_SPEC/X2-03-CONCEPT-TERMINOLOGY-MAP.md` |
| 6 | Cross-System Contract Audit | `Docs/30_CONTRACTS/X2-04-CROSS-SYSTEM-CONTRACT-AUDIT.md` |
| 7 | Migration Candidate Registry | `Docs/40_DECISIONS/X2-08-MIGRATION-CANDIDATE-REGISTRY.md` |
| 8 | Difference Ledger 更新/实例 | `Docs/40_DECISIONS/X2-07-DIFFERENCE-LEDGER.md` |
| 9 | Decision Mapping 更新 | `Docs/40_DECISIONS/X2-06-DECISION-MAPPING.md` |
| 10 | Open Issues / Blocking Items | `Docs/50_OPERATIONS/X2-09-OPEN-ISSUES-QUEUE.md` |
| 11 | Migration Readiness Assessment | `Docs/50_OPERATIONS/X2-10-MIGRATION-READINESS.md` |
| — | Stage State 持久化 | `Docs/50_OPERATIONS/X2-00-STATE.md` |

---

## 2. Re-verification against GitHub（不依赖旧报告）

### 2.1 Git FACT（X2.1 corrected）

| Repo | HEAD = origin/main | Role |
|------|--------------------|------|
| kurt-wong/AITutorX | `7002f3807ddbd4b30f945fc417ddb7f90a79fc6c` | **current evidence anchor** |
| kurt-wong/AITutors-v3 | `cc12d79e9a22f6274100ea0bb61f92493ba88509` | V3 baseline |
| kurt-wong/Aitutors-preprocessing | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` | Preprocessing baseline |

`[HISTORICAL]` X2 撰写时 audit parent = AITutorX `331cbea`（parent of `7002f38`）。
`[FACT]` `7002f38` 已 push；local main == origin/main。**push ≠ Migration Authorized。**

### 2.2 Material corrections vs prior reports

| Prior claim | X2 re-check | Impact |
|-------------|-------------|--------|
| REPORT-B 多份 L1 Spec/Finalization **tracked** | GitHub Contracts 目录仅 **9 tracked** 文件；所列其余文件名 **0 命中** | 资产 Class A 叙事部分无效；标 CONFLICT DL-11 |
| V3 `Docs/GOVERNANCE/` 可作治理依据 | **不在 GitHub main**；本地 untracked | authority UNKNOWN；不作迁移依据 |
| 本地路径 `D:\Project\Aitutors-preprocessing` | 实际 = `D:\Project\Papers` | 与 README/REPORT-G 一致；路径纪律 |
| REPORT-C AIT-DEC 可作 canonical | 源账本未采用 | 仅 mapping 草稿 |
| 测试「全部通过/基线」单一叙事 | 至少三套数字并存 | OQ-GF-018 保持 OPEN-BLOCKING |
| Design v1.1 为接口权威 | untracked；Contract 对 Python 签名零规定；「冻结」出自 Design 自述 | OQ-GF-017 / D2–D4 仍待 Owner |

---

## 3. Unified model summary（一句话架构）

```text
AITutorX = 目标系统
  preprocessing  = Source Evidence Producer（内部能力域）
  V3 backend/frontend = Semantic / Question Consumer（内部能力域）
  Producer↔Consumer Contract = 内部系统边界（仍 binding）
  Unified Docs = 同时解释两侧的唯一治理叙事
```

**生命周期**: Source → Preprocessing → Identity/Version → Semantic Annotation → Resolver → IR → Compiler → Gate → Admission → Question → QuestionInstance/Material/Knowledge。

**关键词表**:
- Identity: `source_content_sha256` = SHA256(raw bytes)；path 仅 locator
- Semantic: `{ready,incomplete,unknown}`
- Decision: `{pending_review,approved,rejected}`
- Material: **含题图/配图/图表/图片**；single question 可有 Material
- Provenance ≠ Quality Authority
- UNKNOWN → reviewable；≠ discard

---

## 4. Contract audit headline

| Topic | Frozen semantics? | Implementation |
|-------|-------------------|----------------|
| Identity key naming | YES | Consumer verification NOT IMPLEMENTED |
| Path non-identity | YES | Code 符合 locator-only（FACT-044 叙事） |
| Manifest/IR verification requirements | YES | 五项 V3 capability NOT IMPLEMENTED |
| Semantic vs Decision separation | YES (vocab) | `unknown` 未解冻；可达性缺口 |
| Material/figures pipeline | PARTIAL | Step5 未做；dangling refs |
| Freeze object | YES (`f4941ff`+sha) | 正文状态叙事 CONFLICT（账本 vs 文首） |
| 87/71/16/166/79 | YES | 禁止混用 |

---

## 5. Registries headline

### 5.1 Migration Candidate Registry
- 覆盖 Specs / Contracts / Architecture / Decisions / Reports / Tests / Production code / CLI-tools / Data manifests
- **GATE_PASSED = 0；MIGRATED = 0**
- 代码与数据全部 `GATE_BLOCKED` 或 `NOT_READY`

### 5.2 Difference Ledger
- 数字差：166/87/71/16/79/177/356/12707/38893/1801 等
- 权威差：Contract 状态叙事、taxonomy 三套、DEC 撞号、REPORT-B 虚构文件、Set B 缺失
- Lineage gaps：双树方向、pre-git 证据、hash 台账、图片恢复、bytes 传输
- **不关闭 OQ-GF-007**

### 5.3 Decision Mapping
- 历史 ID 全部保留；碰撞表（DEC-021/022/023 等）双标
- REPORT-C 非 mapping authority
- 40_DECISIONS 大规模填充仍被 OQ-GF-016 阻塞

### 5.4 Documentation Map
- 族级 classification：MIGRATE / MERGE / SUPERSEDE / ARCHIVE / REJECT / RETAIN-AS-HISTORICAL / UNKNOWN
- untracked → UNKNOWN until Owner
- 数据本体 → NAS（OD-05），禁 copy
- 未逐审家族显式 `UNREVIEWED-FAMILY`

---

## 6. Open items unchanged + X2 additions

**继承（零关闭）**: OQ-GF ×18（OPEN-BLOCKING 仍 9）；BL-09/10/11；D-048 pending。

**X2 新登记队列**: X2-Q-01~18（Contract 状态叙事、Set B、D2/D3/D4、Design v1.1、namespace、ledger 归属、test baseline、Material Step5、Registry 运营等）。

**下一 actor = Owner。**

---

## 7. What X2 explicitly did NOT do

- 未迁移 V3/Preprocessing 生产代码
- 未删除旧仓库内容
- 未修改 V3 Frozen Spec / Frozen Contract v0.2
- 未擅自重新定义 Owner Decision
- 未创建新治理体系取代 GF v0.2
- 未复制文件假装迁移
- 未把 proposal 写成 fact
- 未把 migration candidate 写成 migrated
- 未宣布 Migration Ready / Gate Passed
- 未关闭 OQ/BL/D-048
- 未将任何资产标 admitted=true
- 未重编号历史 DEC/BUG/OQ/REPORT ID
- 未进入 Migration Gate

---

## 8. Git operations（本阶段 + X2.1）

**允许且执行（X2）**: 新增 X2 治理/审计文档至 AITutorX `Docs/`；更新 README 状态；commit（message 属 X2 governance）。

**Commit message（X2）**:
```text
docs(x2): register AITutorX unified documentation governance baseline
```

**Push（X2）**: 已执行 — `331cbea..7002f38` → `kurt-wong/AITutorX:main`。**push 后 Migration 仍为未授权。**

**X2.1（本报告后继 patch）**: 仅 evidence anchor / current-state 一致性修正；commit message:
```text
docs(x2.1): correct unified baseline evidence anchors
```
**X2.1 push 后 Migration 仍为未授权。**

**未跟踪保留**: `REPORT-G/H/I/K` 继续 untracked（OD-06 未完成；非本阶段收编对象）。`X2-DSH-*` 为历史第三方攻击报告，保持 untracked，**不作为 current-state authority**。

---

## 9. End State Declaration

```text
Final State: AITutorX X2 Unified Documentation Governance Registered
X2.1: Evidence anchors corrected (current-state only)

Registered artifacts:
  X2-00 Stage State
  X2-01 Unified System Baseline
  X2-02 Unified Architecture Baseline
  X2-03 Concept/Terminology Map
  X2-04 Cross-System Contract Audit
  X2-05 Unified Documentation Map
  X2-06 Decision Mapping
  X2-07 Difference Ledger
  X2-08 Migration Candidate Registry
  X2-09 Open Issues Queue
  X2-10 Migration Readiness Assessment
  REPORT-X2 (this file)

Evidence Anchor (X2/X2.1):
  AITutorX current HEAD = 7002f38
  V3 baseline = cc12d79
  Preprocessing baseline = 2b92898
  Frozen Contract = f4941ff
  Frozen Contract SHA256 = 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
  Historical audit parent = 331cbea (not current HEAD)

Next actor: Owner
Migration: NOT AUTHORIZED
Evidence correction ≠ Migration Authorization
```

---

## 10. Recommendation to Owner（非决策）

1. 审阅 X2-09 P0 队列并下达 Charter/Gate/Taxonomy 相关令
2. 确认 Contract 双文件状态规则（X2-Q-01）
3. 处置 Design v1.1 / untracked / D2–D4
4. 指定 mapping authority 与 ledger 归属
5. 授权后再考虑：REPORT-G/H/I/K OD-06 四步、Registry 运营细节、受控文档收编（仍须 Gate）

**完成后停止。** 不自行进入 Migration Gate。不自行迁移生产代码。

---

*REPORT-X2 end. Unified model registered. Migration remains unauthorized.*
