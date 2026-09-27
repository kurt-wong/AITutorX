# AITutorX

**交付仓库**：将 `AITutors-v3`（Consumer）与 `Aitutors-preprocessing`（Producer）经集成治理后合并为完整项目。

> **当前状态请看 → [`Docs/50_OPERATIONS/CURRENT_STATE.md`](Docs/50_OPERATIONS/CURRENT_STATE.md)**
> 本 README 只负责：你是谁 / 怎么开始 / 状态在哪里。**不要把状态写进 README。**

---

## 快速定位

| 我想知道 | 去哪里 |
|---|---|
| **项目现在在哪一步** | `Docs/50_OPERATIONS/CURRENT_STATE.md` |
| 文档该怎么写、该放哪 | `Docs/00_GOVERNANCE/AITUTORX-DOC-GOVERNANCE.md` |
| Agent 行为约束 | `AGENTS.md` |
| 系统应当长什么样 | Frozen Spec（在 `AITutors-v3/Docs/V3_SPEC/`，**不在本仓库**） |
| 跨系统接口边界 | 冻结 Contract（`AITutors-v3/Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md`） |
| 为什么做了某个决定 | `Docs/40_DECISIONS/` |
| 历史过程与审计 | `Docs/60_REPORTS/`（**历史证据，不是现行依据**） |
| 已退出主视野的历史 | `Docs/90_ARCHIVE/` |

---

## 目录结构

```text
AITutorX/
├── README.md                  # 本文件（入口）
├── AGENTS.md                  # Agent 协作规则
├── Docs/
│   ├── 00_GOVERNANCE/         # 治理规则（GF-000~006 + DOC-GOV）
│   ├── 10_SPEC/               # 规格
│   ├── 20_ARCHITECTURE/       # 架构说明
│   ├── 30_CONTRACTS/          # 跨系统契约
│   ├── 40_DECISIONS/          # 已生效决策（含决策输入）
│   ├── 50_OPERATIONS/         # 当前状态（CURRENT_STATE.md）
│   ├── 60_REPORTS/            # 历史审计报告（Historical Evidence）
│   └── 90_ARCHIVE/            # 历史归档（只读，不得作现行权威）
├── preprocessing/             # Producer 代码（待迁移，当前为空骨架）
├── backend/                   # Consumer 后端（待迁移，当前为空骨架）
├── frontend/                  # Consumer 前端（待迁移，当前为空骨架）
├── tools/                     # 工具链
└── archive/                   # 历史资产
```

---

## 来源仓库

| 角色 | 本地路径 | Remote |
|------|---------|--------|
| Consumer (V3) | `D:\Project\AITutors-v3` | `kurt-wong/AITutors-v3` |
| Producer (preprocessing) | `D:\Project\Papers` | `kurt-wong/Aitutors-preprocessing` |

> `D:\Project\Aitutors-preprocessing`（无 `.git`）是 `Papers` 的**非版本化副本**，不是权威树。

---

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

---

## 变更分级（来自 DOC-GOV）

```text
LEVEL 1  bug fix / 测试 / 已定义字段实现 / integration 修复 → 直接做，测试证明
LEVEL 2  改 Frozen Spec / 架构边界 / Primary-Fallback 定义   → 需 Owner Decision
LEVEL 3  Migration / 不可逆操作                             → 完整迁移治理（GF-003/004）
```

---

## Security

```text
Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.
```
