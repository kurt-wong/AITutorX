# GF-004 — Migration Boundary Definition

**Document ID**: GF-004
**Status**: `FROZEN GOVERNANCE BASELINE`（OD-14）；**不**授权迁移
**Version**: **v0.2 Frozen**（TASK-GF-005 patch + **TASK-GF-008** OD-05/OD-06/OD-10 固化）
**Role**: Independent System Governance Architect（TASK-GF-001）；决策 actor = Owner
**Date**: 2026-09-17（v0.1） / 2026-09-18（v0.2 patch） / **2026-09-18**（v0.2 freeze + decisions）
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Decision record**: `GF-006-OWNER-DECISION-RECORD.md`（OD-05 / OD-06 / OD-10）
**Upstream**: REPORT-I（Gate/停止线）、REPORT-D（候选分类）、V3_SPEC `50 §3/§4/§5`、`AGENTS.md`
**Evidence discipline**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`
**v0.2 addition labels**: `[FACT]` / `[OBSERVED]` / `[PROPOSAL]` / `[OWNER DECISION REQUIRED]` / `[UNKNOWN]`
**v0.2 freeze labels**: `[OWNER DECISION]`

**Importers / cross-refs**: GF-000 §5；GF-003 Gate 8 migration class；REVIEW/GF-003/02 §2.4；无代码 import。

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
| B3 | 数据本体默认不迁；采用 **NAS-backed read-only** 模型（OD-05） | `[OWNER DECISION]` **OD-05**（GF-006 §6）；仍须 Gate + Class 判定 |
| B4 | 实验/临时/过时预处理产物默认 NO | `[FACT]` 任务书 GF-004；V3 50 §5 |
| B5 | 历史证据可归档只读，不自动获得现行权威 | `[FACT]` REPORT-I Class C / `AGENTS.md` |
| B6 | UNKNOWN 资产保留记录，不静默丢弃也不静默迁入 | `[FACT]` `AGENTS.md` 原则 2 |
| B7 | 代码可适配后迁；架构违规模式不可迁 | `[FACT]` V3 50 §5；REPORT-D Class B |
| B8 | Frozen Governance Baseline ≠ Migration Authorization | `[OWNER DECISION]` **OD-14** + `[FACT]` GF-000 §1.3 |

### 2.0 Data Entry / Storage Model（OD-05 固化）

`[OWNER DECISION]` **OD-05（GF-006 §6）**: 采用 **NAS-backed Read-only Data Model**。

| 层 | 内容 |
|----|------|
| **NAS** | 原始 PDF、图片、OCR Markdown、中间处理结果 |
| **Docker AITutor-X** | 通过 **read-only volume mount** 访问 NAS 数据 |
| **Database** | 结构化对象：Question / QuestionInstance / Knowledge Node / Relation / Embedding metadata |
| **Repository** | 测试资产：golden corpus / fixtures / validation samples |

`[OWNER DECISION]` **禁止**:
- 将全部数据复制进入代码仓
- 将 NAS 数据视为 Docker 生命周期数据

`[FACT]` 非授权: OD-05 **不**表示数据本体已迁入；**不**关闭 OQ-GF-002 / BL-10（具体实施细节仍 OPEN）；**不**创建/修改 Database schema；**不**实施 NAS mount 配置。

### 2.1 V3_SPEC 50 §3 Asset Classification 对齐（v0.2 增补）

`[FACT]` V3_SPEC `50_Migration_Assets.md` §3「可复用资产清单」分**五类**：外部能力 / 数据样本 / 知识种子 / 非代码资产 / 失败教训（只读不移植）；§4 Golden Corpus；§5 绝不迁清单。

`[FACT]` v0.2 在本文件的 YES/NO/CONDITIONAL 之上，增加与 V3 50 §3 对齐的 **迁移用途分类**（不替换 YES/NO/CONDITIONAL，不修改 V3 50 原文）:

| Classification | Meaning | 对齐 V3 50 §3 | 迁移含义 |
|----------------|---------|---------------|----------|
| **identity asset** | 身份/契约类资产（Frozen Contract、identity 定义、canonical type/DISPLAY_CONTRACT 等非代码业务契约） | 非代码资产 | 字节级引用优先；**不**自动获得运行授权；M1–M5 实现另属 conditional |
| **migration candidate** | 原则上可作为迁移对象候选（仍须 Gate 1–10） | 外部能力（版本登记后）/ 数据样本（Golden）/ 知识种子 | YES 类仍须 Gate；Cluster A 未关前 DEFAULT-BLOCKED |
| **conditional migration** | 转换/补账/Owner 裁决后才可能迁 | 失败教训以外的可适配代码；Class B/C lineage | 须 known_issue binding + authority/evidence reference（适用时） |
| **prohibited migration** | 明确禁止迁入 | 失败教训（只读参考，不移植）；§5 全部 V2 库/pipeline/特判/API-worker/recover→queued | 违反 = 停；只读归档 ≠ 迁入 active tree |

`[FACT]` 映射摘要:

| V3 50 §3 / §5 类别 | GF-004 v0.2 classification | GF-004 YES/NO/CONDITIONAL |
|---------------------|----------------------------|---------------------------|
| 外部能力（PaddleOCR 等） | migration candidate（须版本/契约登记） | CONDITIONAL→YES after register |
| 数据样本 / Golden Corpus | migration candidate（评测资产，非运行库表） | CONDITIONAL（版本化；**OD-05**: Repository 保存测试资产；NAS 保存大体量语料） |
| 知识种子 | migration candidate（schema/seed 契约） | CONDITIONAL |
| 非代码资产（DISPLAY_CONTRACT、canonical type） | **identity asset** | CONDITIONAL→YES after F3/namespace 执行（OD-03 分层模型已裁；执行状态 OPEN） |
| 失败教训（BUG 清单、V2 代码作失败样本） | **prohibited migration**（只读归档） | NO（active tree）；可 `90_ARCHIVE` 只读 |
| V3 50 §5 全部绝不迁项 | **prohibited migration** | NO |
| Identity modules M1–M5 实现代码 | conditional migration | CONDITIONAL（authority pending D2/D3/D4） |
| lineage manifests（含 hash 者） | migration candidate（证据类） | YES + Gate；Class B 须降级标注 |

`[OWNER DECISION REQUIRED]` D2/D3/D4；Golden Corpus 规模/版本（V3 50 §4.3）；本分类表是否单独升格引用条款；OQ-GF-015 完整执行状态（taxonomy 分层已裁 OD-03）。

### 2.2 AITutorX Untracked Artifact 引用规则（v0.2 增补；OD-06/OD-10）

`[FACT]` 引用 AITutor-X 治理仓内工件时，**必须区分**下列四个状态（与 GF-000 §3.3 / GF-001 §2.6 一致）:

| State | Meaning | 迁移/Gate 含义 |
|-------|---------|----------------|
| `exists` | 磁盘可读 | 仅证明存在；**不**证明治理效力 |
| `tracked` | git 跟踪（有 blob 历史） | 可复现引用；仍 ≠ Authority |
| `referenced` | 被 GF/REPORT/Gate 文本引用 | 引用链存在；仍 ≠ admitted |
| `admitted` | 经 Registry 登记 + Owner/Charter 处置 | 唯一可作「治理已接受」状态；当前 `[UNKNOWN]` |

`[OWNER DECISION]` **OD-10**: 建立 Artifact Registry；**禁止**本任务创建实例/导入/改 `admitted`。

`[OWNER DECISION]` **OD-06（GF-006 §8）**: REPORT-G/H/I/K 采用 **整理后收编**：Evidence Package → identity information → Artifact Registry → 再改变 admission 状态。**当前不得直接认为 `admitted=true`。** BL-11 OPEN。

`[FACT]` 当前观测（TASK-GF-004-A @ HEAD `e1beba34857c5332a910901b8f4a409cb4119235`；TASK-GF-008 时点 untracked 状态未变）:

| Artifact | exists | tracked | referenced | admitted |
|----------|--------|---------|------------|----------|
| REPORT-A～F | YES | YES | YES | `[UNKNOWN]` |
| REPORT-G | YES | **NO** | YES | `[UNKNOWN]` |
| REPORT-H | YES | **NO** | YES | `[UNKNOWN]` |
| REPORT-I | YES | **NO** | YES（GF-000~006） | `[UNKNOWN]` |
| REPORT-K | YES | **NO** | YES（GF-000~006） | `[UNKNOWN]` |
| REPORT-J | NO | n/a | OQ-GF-013 | n/a |

`[FACT]` 规则:
1. untracked 且无 Owner 处置 ⇒ 默认 **NO**（维持 §4）；引用时必须标注 citation state + gap。
2. **禁止**把 `exists`/`referenced` 写成 `admitted` 或「治理已证实」。
3. Gate 证据引用 untracked REPORT 时，`authority_status` 不得为 `verified`（与 GF-003 §6 一致）。
4. Registry 实例与 admission 流程未完成前，**所有** REPORT 的 `admitted` 保持 `[UNKNOWN]`。

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
| **DQ / 审计 JSON**（v0.2 调整） | `dq_figure_pdf_availability.json` 等 | **v0.1 曾列 YES；v0.2 收窄为 CONDITIONAL**（见下） |
| **wrong-claim / 冲突主张账本**（v0.2 调整） | 含错误主张的 ledger/叙事（如 CLOSURE-PLAN 12,707 归属类） | **CONDITIONAL**（见下）；证据只读；冲突须保留 |
| REPORT-K 类 lineage 审计 | AITutorX `REPORT-K` | exists + **untracked** + referenced；admitted=`[UNKNOWN]`；引用规则见 §2.2 |

**v0.2 CONDITIONAL 化 — DQ / wrong-claim ledger**

`[PROPOSAL]` 对 **DQ/审计 JSON** 与 **wrong-claim ledger**（含已知错误主张的账本/报告叙事）：

```text
classification: CONDITIONAL（不再是无条件 YES）

全部满足下列三项后，方可作为迁移证据候选（仍须 Gate）:
  1. known_issue binding     — known_issue_refs[] 非 silent empty（若有源账本 issue）
  2. authority reference     — authority_status + frozen_ref/OD 引用；untracked ⇒ 不得 verified
  3. evidence reference      — content_sha256/hash_meaning/measurement 元数据可追溯

任一缺失 ⇒ 保留在候选册，不得称 verified；不进入 active tree
```

`[FACT]` 依据: TASK-GF-004-A §5A；REVIEW 02 §2.4/§3（DQ YES 收窄）；OQ-GF-011（12,707 归属口径）仍 OPEN；REPORT-H authority conflicts 未裁；GF-003 P7（冲突并列保留）。

`[PROPOSAL]` 本调整 **不删除** v0.1 对这些工件「存在、可作证据」的观察 FACT；只收窄**迁移类别**。

`[OWNER DECISION REQUIRED]` known_issue binding 流程；OQ-GF-011 更正载体；REPORT-H 冲突处置。

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
| **Untracked 文档（无 Owner 处置）** | 默认 NO | REPORT-I §0.3；REPORT-D Class E；v0.2 状态区分见 §2.2 |
| **伪文件名 / 无法在仓定位的 REPORT-B 条目** | NO | REPORT-I §3 |
| **大体量原始语料本体**（`original/` `maintainess/` `Ocr-markdown/`） | **默认 NO**（直至 OQ-GF-002 模式裁决） | `[INFERENCE]`+`[DECISION REQUIRED]` |
| **前端** | 本轮默认 NO，除非 OD-010 明确纳入 | REPORT-I Cluster E |
| **失败教训类资产**（V2 BUG 清单、作失败样本库的 V2 代码） | **prohibited migration** 进 active tree；仅 `90_ARCHIVE` 只读 | V3 50 §3 失败教训「只读参考，不移植」`[FACT]` |
| **V3 50 §5 绝不迁项**（库/表/镜像/pipeline/特判/API-worker/recover→queued 等） | NO — prohibited migration | V3 50 §5 `[FACT]`；v0.2 §2.1 分类对齐 |

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
- 将 OD-04/OD-05 决策解读为数据已可迁入或实施已完成
- 修改 V3 50 或 REPORT-D/I 的分类结论
- 创建 DEC/BUG ID
- 指定 maintainess 或 original 任一为 canonical（OD-04）
- 将 untracked REPORT 写成 `admitted=true`（OD-06）
- 关闭 OQ-GF-002/013/015 或 BL-09/10/11

---

## 8. Success Criterion

未来工程师应能对任意源仓资产回答：

> 「它属于 YES / NO / CONDITIONAL 哪一类？卡在哪个 Gate 或哪个 Owner 决策？」

---

*GF-004 · **v0.2 FROZEN GOVERNANCE BASELINE** · TASK-GF-001（v0.1） + TASK-GF-005（v0.2 patch） + **TASK-GF-008（OD-05/06/10）** · 2026-09-18*
***Frozen Governance Baseline does not imply Migration Authorization.***
*§2.0 NAS-backed read-only 数据模型（OD-05）；§2.2 untracked + OD-06 整理后收编（admitted≠true）。*
*未授权迁移；未关闭 OQ/BL；未修改 V3 50 原文。*
