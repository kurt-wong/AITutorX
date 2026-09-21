# AITutorX Document Governance Baseline

**Document ID**: AITUTORX-DOC-GOVERNANCE
**Document Type**: Governance Meta-Spec
**Authority Level**: **L0-META**（文档治理元规范；**不定义业务语义**）
**Status**: `ACTIVE — OWNER RATIFIED 2026-09-21`
**Normative**: YES（对**文档治理流程**规范）
**Supersedes**: —
**Superseded By**: —
**Date**: 2026-09-21
**Upstream**: V3 `90_DOCUMENT_GOVERNANCE.md`；V3 `91_PROJECT_TERMINOLOGY.md`；AITutorX `GF-000`；AITutorX `AGENTS.md`
**Adaptation principle**: V3 Governance 为规则来源与成熟模板；AITutorX 目录结构为适配对象。最小适配，不机械复制。
**Owner Ratification**: Owner hereby accepts and ratifies this document as the current governance baseline for AITutorX (X2.6-BASELINE-CLOSURE-RECORD.md DSH-X26-03). Authority hierarchy: Owner Decision > Frozen Contract/Spec > Architecture/Governance documents. This ratification does NOT create a new Frozen Spec/Contract.

---

## 0. 为什么需要 Document Governance

Architecture 结论如果没有 authoritative document 支撑，就没有真正固化。Document Governance 如果不知道哪些文档拥有 architecture authority，也无法真正执行。

本文档建立 AITutorX 自己的文档治理基线，解决：

1. 哪些文档拥有 normative authority
2. 新文档应该放在哪里
3. Root 目录允许出现什么
4. 文档创建前需要回答什么
5. Evidence 与 Conclusion 的边界

---

## 1. Authority Levels（AITutorX 适配）

| Level | 文档类型 | 目录 | 权限 | 禁止 |
|-------|---------|------|------|------|
| **L0-GOV** | Governance Foundation | `Docs/00_GOVERNANCE/` | 定义治理基线、authority model、migration boundary | 不得被 L1–L3 隐式修改 |
| **L0-SPEC** | Normative Specification | `Docs/10_SPEC/` | 定义 canonical concepts、terminology、architecture facts | 不得被报告替代 |
| **L0-META** | Document Governance + Terminology | 本文档 + `Docs/00_GOVERNANCE/` | 定义文档放置规则、创建门槛、authority 层级 | 不含业务语义 |
| **L1** | Owner Decision | `Docs/40_DECISIONS/` | 对具体问题裁决；可产生 governance fact | 不得修改 L0 frozen text |
| **L2** | Operations / Stage State | `Docs/50_OPERATIONS/` | 记录当前状态、执行跟踪、prerequisites | 不得定义规则；不得改变 authority |
| **L3** | Report / Evidence | `Docs/60_REPORTS/` | 提供 evidence、audit findings、verification results | 不得单独支撑 PASS/CLOSED；不得成为 normative authority |

**未归层 = 不得引用为权威。**

### 1.1 Authority 关键规则

```text
R-A: L0-GOV / L0-SPEC 只能经 Owner Decision + explicit amendment 修改
R-B: L1 (Owner Decision) 可以裁决具体问题，但不得修改 L0 frozen text
R-C: L2/L3 永远不得改变 L0/L1
R-D: Report 可以记录 evidence，但 evidence ≠ conclusion ≠ authority
R-E: 被 ≥2 份文档使用的架构术语必须在 L0-SPEC 或 L0-META 中有定义
```

---

## 2. Directory Layering（目录层级语义）

| 目录 | 层级 | 允许 | 禁止 |
|------|------|------|------|
| `Docs/00_GOVERNANCE/` | L0-GOV / L0-META | Governance foundation、authority model、document governance | 业务 spec；临时报告 |
| `Docs/10_SPEC/` | L0-SPEC | Canonical concepts、terminology map、architecture facts | Owner decisions；stage reports |
| `Docs/20_ARCHITECTURE/` | L0-SPEC / L1 | Architecture design、pipeline design、modification design | Runtime evidence reports |
| `Docs/30_CONTRACTS/` | L0-GOV | Contract references、boundary definitions | 直接修改 Frozen Contract |
| `Docs/40_DECISIONS/` | L1 | Owner decisions、decision records、authorization records | Operations state；audit reports |
| `Docs/50_OPERATIONS/` | L2 | Stage state、tracking matrix、prerequisite registry | Normative rules；owner decisions |
| `Docs/60_REPORTS/` | L3 | Audit reports、verification reports、evidence reports | Normative specs；owner decisions |
| `Docs/90_ARCHIVE/` | deprecated | SUPERSEDED / historical documents（审计证据） | 作为现行引用来源 |
| **Root** | 入口 | 项目入口文件 + 授权的 project-level canonical docs | 报告、审计、临时分析 |

---

## 3. Root Directory Rule（正式建立）

> **Root 不是阶段报告堆放区。**

### 3.1 Root 允许的文件类型

```text
允许：
  README.md                    — 项目入口
  AGENTS.md                    — Agent instructions
  .gitignore / .gitattributes  — Git 配置
  LICENSE                      — 许可证
  package.json / pyproject.toml — Build/config metadata（如适用）
  其他明确由 governance 授权的 project-level canonical documents
```

### 3.2 Root 禁止的文件类型

```text
禁止在 root 新建：
  Audit report
  Verification report
  Stage report
  Temporary analysis
  Implementation report
  Migration report
  Meeting/working notes
  DSH audit/verdict reports
  Closure records
  Any document that belongs in Docs/*
```

### 3.3 现存 Root 违规文件（migration candidate）

| 文件 | 类型 | Classification | Disposition |
|------|------|---------------|-------------|
| `X2-DSH-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2-DSH-ATTACK-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2-DSH-FINAL-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2-DSH-FINAL-ATTACK-SUMMARY.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.1-DSH-AUDIT-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.1-DSH-FINAL-VERDICT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.5-DSH-AUDIT-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.5.1-DSH-AUDIT-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.5.1-DSH-FINAL-VERDICT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.5.2-DSH-AUDIT-REPORT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |
| `X2.5.2-DSH-FINAL-VERDICT.md` | Report | **MIGRATE** → `Docs/60_REPORTS/` | Duplicate risk |

**Migration execution requires Owner approval.** See §7 Document Migration Plan.

---

## 4. Document Creation Gate（文档创建门槛）

任何新增文档**必须**回答以下 9 项，缺一不可：

```text
1. 这是什么类型的文档？
   → Document Type ∈ {Governance, Specification, Decision, Operations, Report}

2. 谁拥有它的 authority？
   → Authority Level ∈ {L0-GOV, L0-SPEC, L0-META, L1, L2, L3}

3. 它应该放在哪个目录？
   → 按 §2 Directory Layering 选择

4. 是否已经存在同类文档？
   → Glob/Grep 检查；如存在同类，说明不可合并差异

5. 它是否创造新的 architecture fact？
   → YES: 需要 Owner authority 或 L0-SPEC amendment
   → NO: 通常属于 report/evidence 范畴

6. 如果创造新的 normative fact，Owner authority 在哪里？
   → 引用具体 Owner Decision ID 或 L0-SPEC location

7. 它引用哪些 authority？
   → 向上引用闭包：L0/L1 或已具备闭包的 L1 decision

8. 它的生命周期/状态是什么？
   → Status ∈ {ACTIVE, SUPERSEDED, HISTORICAL, DRAFT, CLOSED}

9. 是否会与现有文档形成重复 authority？
   → 如有重复 authority，必须解决后再创建
```

**判定**：任一答不出 → **不得创建**，应改为在现有文档中增补章节。

### 4.1 禁止用 Report 替代 Normative Spec

```text
违规：
  Report 中定义 "canonical Question Type = {…}"
  而 L0-SPEC 中无此定义

正确：
  L0-SPEC（如 X2-03）定义 canonical terms
  Report 引用 L0-SPEC 作为 authority
```

---

## 5. Evidence vs Conclusion 分离

```text
Evidence ≠ Conclusion ≠ Authority
```

### 5.1 Report 可以做

- 记录 observed facts
- 记录 test results
- 记录 independent verification
- 提出 findings
- 提出 recommendations

### 5.2 Report 不得做

- 未经 Owner Decision 自动成为 architecture authority
- 定义 normative rules
- 修改 L0 frozen text
- 单独支撑 PASS / CLOSED / MIGRATION AUTHORIZED

### 5.3 Evidence Classification Labels

| Label | Meaning |
|-------|---------|
| `DIRECTLY VERIFIED` | 本轮执行者直接验证（code read, test run, git check） |
| `INDEPENDENTLY VERIFIED` | 第三方（如 DSH）独立验证 |
| `DOCUMENTED FACT` | 从已有文档中提取的事实 |
| `OWNER DECISION` | Owner 已裁决 |
| `OWNER DECISION REQUIRED` | 需要 Owner 裁决 |
| `RECOMMENDATION` | 执行者建议（非 fact） |
| `PROPOSAL` | 提案（非 approved） |
| `UNKNOWN` | 无法确定 |

---

## 6. Terminology Governance（AITutorX canonical terms）

### 6.1 Canonical Term Authority Table

| Term | Canonical X? | Authority | Definition Location |
|------|:-----------:|-----------|-------------------|
| **Question** | YES | Canonical Domain | `X2-03` §4 + `X2.5-02` §1 |
| **Question Type** | YES | Canonical Domain | `X2-03` §4；closed set = 12 exam types |
| **Unit** | YES | Canonical Pipeline | `X2-03` §4 |
| **Unit Type** | YES | Canonical Pipeline | `X2-03` §4；closed set = `{standalone_unit, composite_unit}` |
| **standalone_unit** | YES | Canonical Unit Type | V3 `UNIT_TYPES` / `X2-03` §4 |
| **composite_unit** | YES | Canonical Unit Type | V3 `UNIT_TYPES` / `X2-03` §4 |
| **standalone_question** | **NO** | Legacy Producer/Preprocessing | `X2-03` §4；`X2.5-02` §1 |
| **composite_question** | **NO** | Legacy Producer/Preprocessing | `X2-03` §4；`X2.5-02` §1 |

### 6.2 Terminology Boundary Rules

```text
Rule T-1: Legacy vocabulary may exist in Producer/historical layers
Rule T-2: Legacy vocabulary MUST NOT be used as X canonical Question Type
Rule T-3: Legacy vocabulary MUST NOT be used as X canonical Unit Type
Rule T-4: Question Type ⟂ Unit Type (orthogonal; no QT→UT mapping)
Rule T-5: Current normative documents MUST NOT declare legacy terms as canonical
Rule T-6: Success criterion = boundary correctness, NOT grep=0
```

---

## 7. Document Migration/Disposition Plan（分类与建议）

### 7.1 Migration Rules

```text
Rule M-1: 先建立 governance baseline，再提出 migration/disposition plan
Rule M-2: 不得为了"看起来干净"而进行大规模文件移动
Rule M-3: 迁移动作如需 Owner 批准，则只生成 migration plan
Rule M-4: Duplicate 处理 = 指定 canonical location + mark other as SUPERSEDED
Rule M-5: Historical reports 可以保留历史事实，但须避免被误认为 current authority
```

### 7.2 Root File Migration Plan

**Status**: PLAN ONLY — OWNER APPROVAL REQUIRED FOR EXECUTION

| Action | File | Target | Classification |
|--------|------|--------|---------------|
| MIGRATE (git mv) | Root `X2*-DSH-*.md` (11 files, TRACKED) | `Docs/60_REPORTS/` | Root report → proper location; use `git mv` (files are TRACKED per DSH verification) |
| CHECK | Root vs `Docs/60_REPORTS/` duplicates | Dedup | Keep canonical, mark SUPERSEDED |

### 7.3 Untracked File Disposition

| File | Status | Classification | Recommendation |
|------|--------|---------------|---------------|
| `Docs/60_REPORTS/REPORT-G-*.md` | Untracked | Report | RETAIN-AS-HISTORICAL（OD-REPO-01） |
| `Docs/60_REPORTS/REPORT-H-*.md` | Untracked | Report | RETAIN-AS-HISTORICAL（OD-REPO-01） |
| `Docs/60_REPORTS/REPORT-I-*.md` | Untracked | Report | RETAIN-AS-HISTORICAL（OD-REPO-01） |
| `Docs/60_REPORTS/REPORT-K-*.md` | Untracked | Report | RETAIN-AS-HISTORICAL（OD-REPO-01） |
| `Docs/60_REPORTS/X2*-DSH-*.md` | Untracked | Report | Check if duplicate of root; dedup |

### 7.4 Docs/60_REPORTS Inventory Assessment

Tracked reports in `Docs/60_REPORTS/` (current HEAD):
```text
REPORT-A/B/C/D/E/F/X2/X2.5/X2.5.1  — tracked, admitted governance reports
X2*-CLAUDE*.md                      — Claude implementation reports
X2.6-M2/M3*.md                      — M.2/M.3 closure and verification reports
X2.6-OD-FINAL*.md                   — OD finalization reports
X2.6-ONTOLOGY*.md                   — Ontology correction report (latest)
```

Untracked reports (NOT admitted):
```text
REPORT-G/H/I/K                      — per OD-REPO-01, remain untracked
```

Root DSH reports (TRACKED per DSH verification 2026-09-21):
```text
X2*-DSH-*.md (root)                 — TRACKED; migration = git mv (PLAN ONLY)
```

---

## 8. Document Lifecycle Status

### 8.1 Allowed Status Values

| Status | Meaning |
|--------|---------|
| `ACTIVE` | 现行有效 |
| `FROZEN` | 文本已冻结（如 GF v0.2）；修改需 explicit amendment |
| `SUPERSEDED` | 已被他文废止（正文保留为审计证据） |
| `HISTORICAL` | 历史记录，非现行 |
| `DRAFT` | 草稿 |
| `CLOSED` | 已关闭（须带 scope 限定） |
| `NOT ADMITTED` | 未 admitted（untracked / governance pending） |

### 8.2 Status Header（新文档必须）

```text
Document ID:      <编号>
Document Type:    <Governance | Specification | Decision | Operations | Report>
Authority Level:  <L0-GOV | L0-SPEC | L0-META | L1 | L2 | L3>
Status:           <ACTIVE | FROZEN | SUPERSEDED | HISTORICAL | DRAFT | CLOSED>
Normative:        <YES | NO>
Purpose:          <一句话：本文档解决什么问题>
Derives From:     <向上引用闭包>
May Change:       <本文档有权影响的范围>
Must Not Change:  <本文档无权触碰的范围>
```

**存量文档不强制回填**（Reconcile, don't rewrite）；下次实质性修订时补。

---

## 9. V3 Governance 对照表

| V3 概念 | AITutorX 适配 | 说明 |
|---------|--------------|------|
| L0 Frozen Spec (`00–50`) | L0-SPEC (`10_SPEC/`, `20_ARCHITECTURE/`) | Canonical architecture + terminology |
| L0-META (`90`, `91`) | L0-META（本文档） | Document governance + terminology |
| L1 Contract Change Record | Owner Decision + explicit amendment | 修改 L0 的入口 |
| L2 Decision Record | L1 Owner Decision (`40_DECISIONS/`) | 裁决与解释 |
| L3 Gate Report | L2 Operations (`50_OPERATIONS/`) + L3 Reports | 状态跟踪 |
| L4 Experiment Report | L3 Reports (`60_REPORTS/`) | Evidence 提供 |
| L5 Status/log | L2 Operations + root README/AGENTS | 项目入口与状态 |
| `Docs/ARCHIVE/` | `Docs/90_ARCHIVE/` | SUPERSEDED / historical |

---

## 10. Agent 读取顺序（强制）

为防上下文污染与 authority 混淆，Agent 处理 AITutorX 文档时遵循：

```text
1. AGENTS.md（Agent instructions）
2. README.md（项目入口 + 当前状态）
3. Docs/00_GOVERNANCE/（L0-GOV: GF-000~006）
4. 本文档（L0-META: Document Governance）
5. Docs/10_SPEC/（L0-SPEC: canonical terms + architecture facts）
6. Docs/40_DECISIONS/（L1: Owner Decisions）
7. Docs/50_OPERATIONS/（L2: current state）
8. Docs/60_REPORTS/（L3: evidence reports）
9. Historical documents（90_ARCHIVE/ + untracked reports）
```

**禁止「grep 到什么读什么」。Report 结论不得自动提升为 authority。**

---

## 11. 显式不主张

1. **不主张**本文档可修改任何 L0-SPEC 业务语义
2. **不主张**本文档关闭任何 OQ-GF / BL / D-048 / CL / DI-01 / X3P
3. **不主张**Document Migration Plan 已获 Owner 批准执行
4. **不主张**REPORT-G/H/I/K 已 admitted（OD-REPO-01: remain untracked）
5. **不主张**本文档削弱 GF-000 governance baseline 权威
6. **不主张**Frozen Contract 冲突需要 Contract amendment（Owner Decision 2026-09-21: Clarification sufficient; amendment NOT REQUIRED）

---

## 12. Security

```text
Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.
```

---

*AITutorX Document Governance Baseline established. Minimal adaptation from V3. Root rule defined. Creation gate defined. Terminology authority registered.*
