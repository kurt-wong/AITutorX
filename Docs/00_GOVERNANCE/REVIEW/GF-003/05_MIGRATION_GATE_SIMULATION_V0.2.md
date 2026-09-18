# 05 — Migration Gate Simulation v0.2

**Document class**: REVIEW PROPOSAL（模拟推演，非放行记录）  
**Task**: TASK-GF-003-B  
**Date**: 2026-09-18  
**Base**: REPORT-I Gate 1–10 + GF-004 + 本 REVIEW `03_*.md`/`04_*.md`（原文件均不修改）

**Classification**: `[FACT]` / `[PROPOSAL]` / `[UNKNOWN]` / `[NEED OWNER DECISION]`

**Global stop line** `[FACT: REPORT-I §0.7；GF-003 §5]`:
> Cluster A 未由 Owner 关闭前，**默认全面禁止迁移**。例外仅限 Owner 书面批准的只读证据副本。

**Gate 9 状态** `[FACT: REPORT-I F4/F5]`:
- F4 Migration Authority Charter = **未设立**
- F5 Gate 文本 = **REPORT-I 自身为草案**
- ⇒ 本模拟中 **无任何资产** 可获得 `approval_block.status=valid`

**状态枚举** `[PROPOSAL]`:
- **YES** — 原则上属迁移对象类别（仍须 Gate；**不**等于现在可拷入）
- **NO** — 不属迁移范围
- **CONDITIONAL** — 须满足明示条件后才可能 YES
- **BLOCKED** — 类别上可能 YES，但当前被停止线/OQ/F* **阻塞**

---

## 总览

| ID | Asset | YES | NO | CONDITIONAL | BLOCKED（当前） |
|----|-------|-----|----|-------------|-----------------|
| A | AITutors-v3 source code | | | ✅（类别） | **✅ 默认** |
| B | AITutorX reports | A–F 类别 ✅ | | G–K 视处置 | **✅ 默认**；G–K 另需 OWNER |
| C | Papers preprocessing output | 清单/manifest 类别 ✅ | | DQ/错误口径须过滤 | **✅ 默认** |
| D | PDF corpus 本体 | | **✅ 默认 NO** | hash 清单可议 | 清单项 **✅ BLOCKED** |
| E | OCR markdown | Class A 子集类别 ✅ | Class B/D | 补账前不可称 verified | **✅ 默认** |
| F | V2 artifacts | | **✅ NO** | 失败教训=只读归档 | 绝不迁 `[FACT: V3 50 §5]` |

---

## A. AITutors-v3 source code

| 字段 | 内容 |
|------|------|
| **范围** | M1–M5 identity modules、runner、`backend/**`、`backend/tests/**`、其它 V3 实现代码 |
| **classification** | **CONDITIONAL**（类别）/ **BLOCKED**（当前）`[PROPOSAL]` |
| **authority** | 代码 bytes 在 V3 git 可考 `[FACT]`；**接口 authority = UNKNOWN**（Design v1.1 untracked；D2/D3/D4 未裁）`[FACT: REPORT-I F7；GF-005 OQ-GF-017 OPEN-BLOCKING]` |
| **evidence requirement** `[PROPOSAL]` | file sha256 + code_class + `known_issues_refs`（D-048-1/2 等，disposition 默认 `pending_owner_decision`）+ `test_baseline`（若称测试等价，依 F9）+ `rollback_ref` + Gate 6 路径抽象/Docker/env + 安全审查（安全敏感代码） |
| **migration status** | **BLOCKED** — Cluster A + F4/F5 + OQ-GF-014/015/017/018 open `[FACT: GF-005；REPORT-I]` |
| **升级为可评审条件** `[PROPOSAL]` | Owner 关闭 Cluster A 相关项；D2/D3/D4 或书面「authority pending 标签迁移」令；F9 测试基线（代码类） |
| **必须保留的标签** `[PROPOSAL]` | M1–M5 即使未来迁入也须 `authority_status=unknown` / pending，直至 D2/D3/D4 |

**测试文件** `[FACT: REPORT-I §3]`: 测试**代码文件**可自动迁（Cluster A 后）；测试**结论/基线**必须 F9 受控重跑 — 二者不可混称。

---

## B. AITutorX reports

| 字段 | 内容 |
|------|------|
| **范围** | `Docs/60_REPORTS/REPORT-A` ~ `REPORT-K` |
| **tracked 现状** `[FACT]` | `git ls-files Docs/60_REPORTS/` = **REPORT-A~F**；磁盘另有 **G/H/I/K**（**untracked**）；**REPORT-J 不存在** |
| **classification** | A–F：**YES（Evidence Artifact 类别）+ BLOCKED（当前）** `[PROPOSAL]`；G/H/I/K：**CONDITIONAL + NEED OWNER DECISION** `[PROPOSAL]` |
| **authority** | 报告 = 审计/对账证据，**不是** Frozen Authority `[FACT: 各报告自述；AGENTS.md]`；GF `[FACT]` 大量引用 REPORT-I/K |
| **evidence requirement** `[PROPOSAL]` | repo@commit + path + file sha + `role=EVD`；untracked 须登记 + `EVIDENCE_LOCAL_ONLY` + 文内声明「GitHub commit 不可核验」 |
| **migration status** | **BLOCKED**（停止线）；G–K 另 **NEED OWNER DECISION** |
| **引用效力** `[FACT + PROPOSAL]` | G–K 不在 `5010c16` 提交内 ⇒ 外部评审者无法从 GitHub 核验 GF 对 REPORT-I/K 的事实锚 |

**Owner 处置选项** `[NEED OWNER DECISION]`（不代裁）:
1. commit 入 AITutorX 并 push  
2. 打包为独立 evidence 包（含 hash）  
3. 维持 local-only + GF 引用降级  
4. 书面豁免（F10 / OQ-GF-013 语境）

---

## C. Papers preprocessing output

| 字段 | 内容 |
|------|------|
| **范围** | `data/ocr_output_manifest.jsonl`、reslice `*.manifest.json`、`interface_scope_snapshot_step1.json`、DQ/审计 JSON、接口键说明等 |
| **classification** | 清单/manifest/snapshot：**YES（证据账本类别）+ BLOCKED（当前）** `[PROPOSAL]`；DQ/含错误主张账本：**CONDITIONAL**（须 known_issue 绑定）`[PROPOSAL]` |
| **authority** | Contract v0.2 冻结四元组 `[FACT: REPORT-I F1]`；账本 mirror vs canonical **UNKNOWN/未裁** |
| **evidence requirement** `[PROPOSAL]` | 双层 hash 分列（`source_sha256`=PDF vs `source_content_sha256`=OCR md）`[FACT: REPORT-K；GF-002 §2]` + coverage_class + interface/locator 分列 + 冲突登记（如 CLOSURE-PLAN 将 12,707 系于 original/ 的口径错误 `[FACT: REPORT-K §6；OQ-GF-011]`） |
| **migration status** | **BLOCKED** — F8/OQ-GF-002 未决 `[FACT: REPORT-I F8；GF-005]`；停止线 |
| **提案默认** `[PROPOSAL]` | 模式未决前只接受 **hash 清单 + 只读 locator**，不接受数据本体/整目录 copy |
| **不自动获得** `[PROPOSAL]` | 迁入证据区 ≠ 所载主张全部为 FACT；已知错误口径必须 `known_issues_refs` |

---

## D. PDF corpus

| 字段 | 内容 |
|------|------|
| **范围** | `D:\Project\Papers\original\`；`D:\Project\Papers\maintainess\PDF` |
| **classification** | **本体 NO（默认）** `[PROPOSAL + FACT: OQ-GF-002/OD-009 未决]`；**hash 清单 = CONDITIONAL 类别 + BLOCKED（当前）** |
| **authority** | operational OCR input = `maintainess/PDF` `[FACT: REPORT-K；代码 PDF_ROOT]`；canonical RSD = **UNKNOWN**（OQ-GF-001 OPEN-BLOCKING）`[FACT: GF-005]` |
| **evidence requirement（若未来清单迁）** `[PROPOSAL]` | Carrier Observation（full_inventory 或声明 sample）+ `restoration_event_ref`（maintainess）+ 双树并列 + `byte_level_equivalence=not_verified` 显式（UNKNOWN-004）+ hash_meaning/bytes_kind |
| **migration status** | 本体 **NO**；清单 **BLOCKED**（OQ-GF-001/002/004/005 + F8 + Cluster A） |
| **禁止** `[FACT/纪律]` | 不假设 maintainess 权威；不假设 original 权威；无 Owner 令不删除/合并任一树 |
| **数字锚** `[FACT: REPORT-K]` | maintainess/PDF 恢复后 **12,707**；original PDF **38,893**；basename 交集 **12,626**；抽样 6/6 sha 一致；均 `git ls-files=0` |

---

## E. OCR markdown

| 字段 | 内容 |
|------|------|
| **范围** | `D:\Project\Papers\Ocr-markdown\**`（md + 图 + manifest） |
| **classification** | Class A（有清单且双层 hash 可对账）：**CONDITIONAL 类别 + BLOCKED（当前）** `[PROPOSAL]`；Class B/D：**NO（迁移候选拒绝直至补账）** `[PROPOSAL]` |
| **authority** | OCRA = 产物，非源权威 `[FACT: GF-001 §2.3]`；清单外 md 归属 **UNKNOWN** |
| **evidence requirement** `[PROPOSAL]` | 有清单条目：L1 PDF sha + L2 md sha + `coverage_class` + manifest entry ref；无清单：最高 Class B，**不得**写「来源已验证」 |
| **migration status** | **BLOCKED**（Cluster A + OQ-GF-002/007/009） |
| **覆盖事实** `[FACT: REPORT-K]` | 清单 1,801；manifest 166（sha 87）；源树 md ≈4,224；抽样 40/40 正文无 lineage token |
| **IR 关联** `[FACT]` | 接口/IR `source_sha256` = **OCR md 字节**（非 PDF）；IR ADMITTED sha match 71 |

---

## F. V2 artifacts

| 字段 | 内容 |
|------|------|
| **范围** | V2 库/列/索引/镜像、生产 pipeline 及 legacy 分支、特判/Anchor Corrector/content_slicer 语义、recover stale→queued、API 内启动 worker、「V2 最稳定版本」整体搬入 |
| **classification** | **NO** `[FACT: V3_SPEC 50 §5「绝不迁」；10 §11；00 §6 红线]` |
| **authority** | V3 Frozen Spec 文本约束；**不**因 V2 运行过而获得迁移权 |
| **evidence requirement** | **不要求**迁移 EvidencePackage；若归档引用则 `artifact_class=ARCHIVE-READONLY` + locator `[PROPOSAL]` |
| **migration status** | **NO**（违反 = 停）`[FACT: V3 50 §5]` |
| **例外（只读参考）** `[FACT: V3 50 §3 失败教训类]` | V2 BUG 清单、审计教训、V2 代码作**失败样本库**：**只读参考，不移植** `[PROPOSAL: role=EVD/ARCHIVE]` |
| **可复用五类（非 V2 表结构）** `[FACT: V3 50 §3]` | 外部能力 · 数据样本/Golden · knowledge seed · DISPLAY_CONTRACT 等 · 失败教训 — GF-004 v0.2 应补映射 `[PROPOSAL]`；**仍非**当前放行 |

---

## 补充资产（GF-004 v0.2 应覆盖）`[PROPOSAL 分类]`

| Asset | YES/NO/CONDITIONAL/BLOCKED | 依据 |
|-------|----------------------------|------|
| Frozen Contract 副本 | YES 类别 + **BLOCKED**（F2 状态叙事 + Gate 9） | REPORT-I F1/F2 `[FACT]` |
| V3 Frozen Spec 副本 | YES 类别 + **BLOCKED**（F3 taxonomy） | REPORT-I F3 `[FACT]` |
| knowledge seed / DISPLAY_CONTRACT / Golden Corpus | CONDITIONAL 类别 + **BLOCKED** | V3 50 §3/§4 `[FACT]`；GF-004 现行未成类 |
| attacks/**、logs/** | CONDITIONAL / 默认 NO-active + **BLOCKED** | REPORT-I；会话过程态禁入治理结论 |
| frontend | DEFAULT-NO（OD-010 未决） | REPORT-I Cluster E `[FACT]` |
| untracked Design/Contract 族 | CONDITIONAL + **NEED OWNER DECISION** | OQ-GF-017；REPORT-I F7 `[FACT]` |

---

## Gate 槽位模拟（全资产共性）`[PROPOSAL]`

| Gate | A–F 当前 | 阻塞源 `[FACT]` |
|------|----------|-----------------|
| 1 Source identified | 部分可满足 | 数据/清单路径可 locator |
| 2 Authority identified | **多数 fail/unknown** | OQ-GF-001/014/015；F3 |
| 3 Validity verified | Class A 子集 partial | 恢复后 not_verified；F9 测试基线 |
| 4 Historical status | 部分 | V2 vs V3 可依 50 §5 |
| 5 Duplicate check | 未系统执行 | — |
| 6 Arch compatibility | 代码类未完成 | 绝对路径；Docker/env |
| 7 Evidence attached | **v0.1 schema 不足** | 03_*.md PROPOSAL 字段缺口 |
| 8 Migration class | 本表可作草案 | PROPOSAL，非 Owner 批准 |
| 9 Governance approval | **当前不可满足** | F4 未设立；F5 草案 |
| 10 Migration record | 未开始 | 停止线 |

---

## 结论（模拟）

1. **A–E** 类别上均可能属 CONDITIONAL/YES，但**当前全部 BLOCKED**（Cluster A + F4/F5 + 多项 OQ）。  
2. **F** 与 V2 表结构/pipeline/特判 = **NO**（V3 50 §5）`[FACT]`。  
3. **D 本体** 默认 **NO**，待 OQ-GF-002 `[FACT: 未决]`。  
4. **B 的 G–K** 叠加 **NEED OWNER DECISION**。  
5. 本表**不是**迁移批准；`approval_block` 全局 = `invalid_without_charter` `[FACT: F4]`。

---

## Non-Actions

- 不修改 GF-004 / REPORT-I / V3_SPEC  
- 不执行任何复制/迁移/删除  
- 不关闭 OQ-GF-001/002/013/014/015/017/018  
- 不将 PROPOSAL 分类写成 Owner 已批准边界  

---

*05_MIGRATION_GATE_SIMULATION_V0.2.md · REVIEW/GF-003 · TASK-GF-003-B · 2026-09-18*
