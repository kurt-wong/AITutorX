# AITutorX Agent Guidelines

## 核心原则

1. **Provenance ≠ Quality Authority** — 来源版本不决定质量
2. **UNKNOWN is retained data** — 不得 silent skip / fallback
3. **Producer/Consumer 是子系统边界** — 即使同仓也需 Contract
4. **Git presence ≠ Authority** — Local ≠ Tracked ≠ Authority
5. **未经 Migration Gate 不得进入 active tree**

## Authority 层级

L0 > L1 > L2 > L3 > L4 > L5 > L6 > L7

Agent 自写的 "Frozen / Final / Authority" 不自动获得权威。

## 禁止行为

- 不修改 Frozen Contract
- 不重编号历史 Decision（用映射表）
- 不删除旧文档/旧代码
- 不大规模重构
- 不修改 Producer 数据
- 不将两个 repo 直接 copy 到 AITutorX

## 代码分类

Production / CLI / Tests / Migration / Audit Tool / Utility / Probe / Experiment / Legacy / Deprecated / Unknown

## 语义状态

- `ready` / `incomplete` / `unknown`
- Decision: `pending_review` / `approved` / `rejected`
- UNKNOWN → reviewable record → pending_review
