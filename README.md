# AITutorX

统一最终工程骨架。由 `AITutors-v3`（Consumer）和 `Aitutors-preprocessing`（Producer）经治理验证后合并。

## 当前状态

**TASK-X2-CLAUDE — Unified Documentation Governance（文档治理已登记）**

`[FACT]` GF v0.2 = Frozen Governance Baseline（OD-14）；**freeze ≠ Migration Authorization**。

`[FACT]` X2 统一治理文档集已写入 Docs（X2-00~10 + REPORT-X2）。三仓审计锚点:
- AITutorX `331cbea`
- AITutors-v3 `cc12d79`
- Aitutors-preprocessing（本地 `D:\Project\Papers`）`2b92898`
- Contract freeze object `f4941ff` / sha256 `9c6b9063…7528`

`[FACT]` 代码迁移尚未开始；AITutorX `preprocessing/` `backend/` `frontend/` `tools/` `archive/` 仍为空骨架。

```text
Migration Authorization: UNAVAILABLE
Migration Gate: NOT PASSED
OQ-GF: 18 条零 CLOSED（OPEN-BLOCKING = 9）
BL-09/10/11: OPEN
D-048: pending_owner_decision
admitted=true: 无
Next actor: Owner
```

X2 文档入口:
- `Docs/50_OPERATIONS/X2-00-STATE.md`
- `Docs/60_REPORTS/REPORT-X2-UNIFIED-GOVERNANCE.md`
- `Docs/40_DECISIONS/X2-08-MIGRATION-CANDIDATE-REGISTRY.md`

## 目录结构

```
AITutorX/
├── Docs/
│   ├── 00_GOVERNANCE/     # 治理基线、Authority 矩阵
│   ├── 10_SPEC/           # 冻结规格
│   ├── 20_ARCHITECTURE/   # 架构设计
│   ├── 30_CONTRACTS/      # 跨系统契约
│   ├── 40_DECISIONS/      # 决策记录
│   ├── 50_OPERATIONS/     # 运维与状态
│   ├── 60_REPORTS/        # 审计报告（Report A–F）
│   └── 90_ARCHIVE/        # 历史归档
├── preprocessing/         # Producer 代码（待迁移）
├── backend/               # Consumer 后端（待迁移）
├── frontend/              # Consumer 前端（待迁移）
├── tools/                 # 工具链
└── archive/               # 历史资产
```

## 来源仓库

| 角色 | 路径 | Remote |
|------|------|--------|
| Consumer (V3) | `D:\Project\AITutors-v3` | `kurt-wong/AITutors-v3` |
| Producer (Preprocessing) | `D:\Project\Papers` | `kurt-wong/Aitutors-preprocessing` |

## 权威层级

| Level | 含义 |
|-------|------|
| L0 | Owner / System Decision |
| L1 | Frozen Specification |
| L2 | Cross-System Contract |
| L3 | Approved Architecture / Design |
| L4 | Implementation |
| L5 | Tests / Verification |
| L6 | Audit / Review |
| L7 | Working Notes |
