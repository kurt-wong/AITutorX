# AITutorX

统一最终工程骨架。由 `AITutors-v3`（Consumer）和 `Aitutors-preprocessing`（Producer）经治理验证后合并。

## 当前状态

**Stage 1 — Governance Audit（进行中）**

本仓库当前仅包含治理骨架和审计报告。代码迁移尚未开始。

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
