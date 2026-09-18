# GF-004 — Migration Boundary Definition（草案）

**Document ID**: GF-004
**Status**: `DRAFT / PROPOSED` — 未经 Owner 批准，不构成冻结权威
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Upstream**: REPORT-I（Gate/停止线）、REPORT-D（候选分类）、V3_SPEC `50 §5`、`AGENTS.md`
**Evidence discipline**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`

---

## 1. Purpose

定义 **什么属于 AITutor-X 迁移范围**，什么明确不属于。

边界判断基于角色与证据，**不**基于「源仓里有这个文件夹」。

---

## 2. Boundary Principles

| # | Principle | 分类 |
|---|-----------|------|
| B1 | Migration ≠ Copy：进入治理树必须逐项过 Gate | `[FACT]` REPORT-I §0.5 禁止整仓 copy |
| B2 | Untracked 默认不可进 active tree | `[FACT]` REPORT-I §0.3 |
| B3 | 数据本体默认不迁；优先 hash 清单与账本 | `[INFERENCE]` 推自 OD-009 未决 + 数据 ignored；**模式待 Owner** |
| B4 | 实验/临时/过时预处理产物默认 NO | `[FACT]` 任务书 GF-004；V3 50 §5 |
| B5 | 历史证据可归档只读，不自动获得现行权威 | `[FACT]` REPORT-I Class C / `AGENTS.md` |
| B6 | UNKNOWN 资产保留记录，不静默丢弃也不静默迁入 | `[FACT]` `AGENTS.md` 原则 2 |
| B7 | 代码可适配后迁；架构违规模式不可迁 | `[FACT]` V3 50 §5；REPORT-D Class B |

---

## 3. YES — 属于迁移范围（仍须 Gate）

> 「YES」= **原则上属于迁移对象类别**，不是「现在就可以拷入」。Cluster A 未关闭前仍受停止线约束。

### 3.1 Verified / frozen governance artifacts

| Asset 类别 | 观测实例 `[FACT]` | 目标落点（提案） | 前置 |
|------------|-------------------|------------------|------|
| Frozen Contract v0.2 副本 | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ `f4941ff`，sha256 `9c6b9063…7528` | `Docs/30_CONTRACTS/` | 字节一致 + F2 状态叙事 |
| V3 Frozen Spec | `Docs/V3_SPEC/00,10,20,30,40,50,90,91,README` | `Docs/10_SPEC/` | tracked + taxonomy 映射（F3） |
| Producer governance 三件套 | `governance/rule_registry.md` 等 | `Docs/00_GOVERNANCE/` 附录 | tracked + 层级重标注 |
| Review / completion 协议 | `review_protocol.md`；`COMPLETION_PROTOCOL.md` | `Docs/00_GOVERNANCE/` | ID 无冲突 |
| 已 tracked 决策/协调账本（镜像） | V3/Papers `COORDINATION` 账本 | `Docs/50_OPERATIONS/` 或 archive | 标明 mirror vs canonical |

### 3.2 Lineage manifests 与证据账本

| Asset 类别 | 观测实例 `[FACT]` | 说明 |
|------------|-------------------|------|
| OCR 输出清单 | `data/ocr_output_manifest.jsonl`（1,801；部分 data tracked） | L1 锚；迁清单不迁 PDF 本体（待 OQ-GF-002） |
| 接口 manifest / snapshot | reslice `*.manifest.json`；`interface_scope_snapshot_step1.json` | L2 锚；含 hash 者 Class A |
| DQ / 审计 JSON | `dq_figure_pdf_availability.json` 等 | 证据只读；冲突须保留 |
| REPORT-K 类 lineage 审计 | AITutorX `REPORT-K` | 治理仓内已存在；引用即可 |

### 3.3 Semantic annotations 与 admitted question data（目标态）

| Asset 类别 | 状态 | 说明 |
|------------|------|------|
| V3 `semantic_annotations` / `admission_candidates` 契约与实现代码 | Spec frozen；运行数据尚未作为迁移包交付 | 迁 **schema/代码/测试** 可走 Gate；迁 **业务数据** 须 L5/L6 证据链 |
| 已 ADMITTED 的 IR/question 记录（Producer 历史） | `[FACT]` 存在 71 ADMITTED 对账记录 | 仅当 lineage Class A + Owner 裁决数据模式后，以证据包形式评估 |
| Golden Corpus 计划与样本引用 | V3 50 §4 | 评测资产；版本化；非运行库表 |

### 3.4 可适配代码与测试（CONDITIONAL→YES after transform）

| Asset | 条件 |
|-------|------|
| V3 `backend/tests/**` | 文件迁入；结论基线须 F9 重跑 |
| Producer `tests/**` | 同上；r67 known-issue 须挂账（OD-006） |
| Identity modules M1–M5 + runner | 代码可迁 + **authority pending（D2/D3/D4）** 标签 |
| Producer `scripts/**` / `ocr_service/**` | 仅当完成路径抽象、Docker/env 文档化、安全审查后 |

---

## 4. NO — 不属于迁移范围

| 类别 | 规则 | 依据 |
|------|------|------|
| **Experimental scripts** | 以 experiment/probe 为分类且无 Gate 6 适配证明的脚本 | `AGENTS.md` 代码分类；REPORT-D |
| **Temporary directories** | `maintainess/test_output`（空）、临时导出、会话中间态 | 任务书 GF-004；REPORT-K 过程态（6 文件）不得入库 |
| **Obsolete preprocessing experiments** | 已废止 pipeline 分支、V2 `simple_pipeline`/fallback 模式 | V3 50 §2/§5 `[FACT]` |
| **Historical conversion artifacts** | `_archive/**` 清理产物、旧转换输出副本 | 可归档 `90_ARCHIVE/`，不进 active tree |
| **V2 数据库表/列/索引/镜像** | 禁止 | V3 10 §11 / 50 §5 `[FACT]` |
| **V2 生产 pipeline 及 legacy 兼容逻辑** | 禁止整体迁入 | 50 §5 |
| **特判规则 / Anchor Corrector / content_slicer 语义** | 禁止 | 50 §5；00 P5 |
| **API 内启动 worker / recover stale→queued** | 禁止 | 50 §5；30 §2/§8 |
| **整仓 `backend/` `frontend/` `preprocessing/` 拷贝** | 禁止 | REPORT-I §0.5 |
| **Untracked 文档（无 Owner 处置）** | 默认 NO | REPORT-I §0.3；REPORT-D Class E |
| **伪文件名 / 无法在仓定位的 REPORT-B 条目** | NO | REPORT-I §3 |
| **大体量原始语料本体**（`original/` `maintainess/` `Ocr-markdown/`） | **默认 NO**（直至 OQ-GF-002 模式裁决） | `[INFERENCE]`+`[DECISION REQUIRED]` |
| **前端** | 本轮默认 NO，除非 OD-010 明确纳入 | REPORT-I Cluster E |

---

## 5. CONDITIONAL — 转换/裁决后才可能 YES

| Asset | 条件 | 开放决策 |
|-------|------|----------|
| DESIGN-v1.1.md 及 untracked CONRACT 族 | Owner commit 或明确 authority 处置 | OD-001/002/008 |
| M1–M5 identity 实现 | D2/D3/D4 + Design authority | OD-003 |
| DEC/BUG/OQ 文档 | namespace policy（F6） | OD-004 |
| SEMANTIC_STATUS=unknown 相关 | 词表与实现一致性披露 | OD-005 |
| Producer 数据/IR 本体 | 数据权威模式 | OD-009 / OQ-GF-002 |
| 双树之一作为「唯一源」叙事 | 权威原始来源裁决 | OD-K-01 / OQ-GF-001 |
| lineage Class B/C 工件 | 补账或冲突关闭 | OQ-GF-007 / OD-K-06/07 |
| frontend | Owner 纳入范围 | OD-010 |
| r67 测试资产结论 | 修复 / known-issue / expected failure | OD-006 |
| DOCX / 待转换DOC | 是否正式输入 | OQ-GF-010 / OD-K-09 |

---

## 6. Boundary Map（逻辑视图）

```text
┌─────────────────────────────────────────────────────────────┐
│ AITutor-X Governance Repository                             │
│                                                             │
│  00_GOVERNANCE ← 治理协议、GF 草案、（迁移后）rule registry │
│  10_SPEC       ← V3 Frozen Spec 副本（经 Gate）             │
│  20_ARCHITECTURE ← 架构说明（非 V2 实现）                   │
│  30_CONTRACTS  ← Frozen Contract 副本（字节一致）           │
│  40_DECISIONS  ← 迁移后决策（须 F6 命名政策）               │
│  50_OPERATIONS ← 账本/mirror/迁移记录                       │
│  60_REPORTS    ← 审计/对账报告（既有 A–K 不改写）           │
│  90_ARCHIVE    ← 历史证据只读归档                          │
│  backend/frontend/preprocessing/tools ← 仅 Gate 后的代码资产│
└─────────────────────────────────────────────────────────────┘
          ▲
          │ Migration Gate 1–10 + EvidencePackage
          │
┌─────────┴───────────────────────────────────────────────────┐
│ Sources (not wholesale-copied)                              │
│  AITutors-v3        — specs, contract, code, tests          │
│  Papers (preprocess)— manifests, governance docs, some code │
│  Papers data trees  — DEFAULT OUT (hash/manifest only)      │
└─────────────────────────────────────────────────────────────┘
```

- `[FACT]` AITutor-X Docs 目录骨架已存在（`00_GOVERNANCE`…`90_ARCHIVE`）；当前 `00_GOVERNANCE` 本轮新建 GF 草案前仅 `.gitkeep`。
- `[FACT]` 本文件为 GF 草案落入 `00_GOVERNANCE/`，**不是** Migration Gate 通过记录。

---

## 7. Explicit Non-Goals of This Boundary Doc

本文件 **不**:

- 授权任何文件复制/迁移
- 裁决数据权威模式或双树去留
- 修改 V3 50 或 REPORT-D/I 的分类结论
- 创建 DEC/BUG ID
- 假设 maintainess 或 original 任一权威

---

## 8. Success Criterion

未来工程师应能对任意源仓资产回答：

> 「它属于 YES / NO / CONDITIONAL 哪一类？卡在哪个 Gate 或哪个 Owner 决策？」

---

*GF-004 · DRAFT · TASK-GF-001 · 2026-09-17 · 仅新建治理草案，未执行迁移*
