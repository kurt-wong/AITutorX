# Report E — AITutorX Owner Decision Queue

**日期**: 2026-09-16
**目的**: 需要 Owner 明确裁决的事项，按优先级排列

---

## P0 — 阻塞迁移

### OD-001: Untracked 文档 Authority 处置

**问题**: 9 个 V3 文档从未进入 git，Authority = UNKNOWN。其中 DESIGN-v1.1 被引用为 D2/D3/D4 的权威来源。

**证据**: `git log --all -- <path>` 对全部 9 个文件返回空。

**选项**:
- (A) Commit 到 V3 repo → 获得 git traceability
- (B) Copy 到 AITutorX 并标注 authority
- (C) 确认为 historical，不再引用
- (D) 组合：commit + assign authority level

**影响**: 不解决则迁移无法继续（Class E 阻塞）。

---

### OD-002: Design v1.1 Authority Anchoring

**问题**: D2/D3/D4 的裁决引用 DESIGN-v1.1.md 作为权威，但该文件无 git history、无正式 authority anchoring。

**证据**: 文件存在但 untracked；D2/D3/D4 Decision Brief (Producer AIT-DEC-138) 引用它。

**选项**:
- (A) 正式 anchoring：commit + 在 Authority Matrix 中标注 L3
- (B) 标记为 UNKNOWN AUTHORITY，D2/D3/D4 重新裁决
- (C) 确认内容正确但仅作为 working reference (L7)

**影响**: 直接影响 D2/D3/D4 是否可执行。

**状态（2026-09-29 追注）**: **Owner 裁 (C) WORKING REFERENCE (L7)**。赋权 DEFERRED 至 D2/D3/D4 closure。
登记落点: AITutors-v3 `DESIGN-v1.1` 文首批注 + `EB008-P1-IMPLEMENTATION-NOTES.md §10` + commit `6279136`。
**不**在本文件新建 Decision；正文选项历史保留。

---

### OD-003: D2 / D3 / D4 裁决

**问题**: 三个接口层开放问题等待 Owner 决定：

| Item | 描述 | 状态 |
|------|------|------|
| D2 | V3 identity_version gate | UNKNOWN — 是否实现？ |
| D3 | Semantic boundary 四状态机 | NOT STARTED — 是否实现？ |
| D4 | Execution ordering V3 scheduling | UNKNOWN — 是否实现？ |

**前提**: OD-002 需先解决（authority anchoring）。

**影响**: 阻塞 V3 Phase 3+ 实现。

**状态（2026-09-29 追注）**: OD-002 = (C) working reference。**D2 = (b)** 已裁（仅 DESIGN-v1.1 §4.2–§4.6 M1–M5 interface reference；§1/§2/§3 排除）。**D3/D4 仍 OPEN**。
建议分层裁：D2（实现依据范围）→ D3（schema/migration 边界）→ D4（LIMITED 扩面）。
多空题 representation 另见 V3 `LIMITED-…-v0.3 §D.1` **BLOCKED**（L0 冲突，未进本队列）。


---

## P1 — 影响架构决策

### OD-004: DEC 编号冲突处理

**问题**: DEC-012~036 范围内 V3 和 Producer 有独立且冲突的编号。

**证据**: 见 Report C。

**选项**:
- (A) 接受 AIT-DEC-* 映射表（Report C），未来统一使用
- (B) 重新编号历史 DEC（违反"不重写历史"原则）
- (C) 仅在文档中加 disambiguation 前缀

**建议**: (A)

---

### OD-005: SEMANTIC_STATUS `unknown` 实现

**问题**: DEC-028 Part 5 要求 SEMANTIC_STATUS 包含 `{ready, incomplete, unknown}`，但代码中冻结为 `{ready, incomplete}`（BUG-V3-018）。

**证据**: `backend/app/domains/compile/__init__.py` line 29。

**选项**:
- (A) 实现 unknown → 触发 unknown→reviewable→pending_review workflow
- (B) 维持现状，记录为 known gap
- (C) 修改 Contract（不推荐——frozen）

**影响**: UNKNOWN 数据处理路径。

---

### OD-006: Producer Test Failure (r67_t13)

**问题**: `test_r67_t13_real_corpus_smoke` FAIL — 768 条 AUDIT_FROM_UNMATCHED。

**证据**: 2026-09-16 实测，1 failed / 337 passed。

**选项**:
- (A) 接受为 known issue，迁移后修复
- (B) 迁移前修复
- (C) 标记为 expected failure

---

## P2 — 治理改进

### OD-007: AITutorX Git 仓库初始化

**问题**: AITutorX 目录已创建但未 `git init`。

**选项**:
- (A) `git init` + initial commit
- (B) 等到迁移开始时再初始化

---

### OD-008: G0 Governance Docs 处置

**问题**: `Docs/GOVERNANCE/` 下 4 个文件（00-SYSTEM-BASELINE 等）也是 untracked。

**选项**:
- (A) Commit 到 V3
- (B) Copy 到 AITutorX Docs/00_GOVERNANCE/
- (C) 两者都做

---

### OD-009: Producer 数据 Baseline 重建

**问题**: Producer 的 raw_data / ir_data / Ocr-markdown 不在 git 中（.gitignore）。如何在 AITutorX 中引用？

**选项**:
- (A) 保持 Producer repo 作为数据源，AITutorX 通过 path reference
- (B) 复制数据到 AITutorX（需要大量空间）
- (C) 使用 NAS 作为共享数据源

---

### OD-010: 前端 (frontend/) 迁移范围

**问题**: V3 frontend/ 是否需要迁移？当前审计主要关注 backend。

**选项**:
- (A) 包含在迁移范围内
- (B) 延后，先完成 backend + preprocessing

---

## 汇总

| ID | 优先级 | 标题 | 阻塞 |
|----|--------|------|------|
| OD-001 | P0 | Untracked docs authority | 迁移 |
| OD-002 | P0 | Design v1.1 anchoring | D2/D3/D4 |
| OD-003 | P0 | D2/D3/D4 裁决 | Phase 3+ |
| OD-004 | P1 | DEC 编号冲突 | 文档治理 |
| OD-005 | P1 | SEMANTIC_STATUS unknown | UNKNOWN workflow |
| OD-006 | P1 | Producer test failure | 测试基线 |
| OD-007 | P2 | AITutorX git init | 版本控制 |
| OD-008 | P2 | G0 docs 处置 | 治理连续性 |
| OD-009 | P2 | Producer data baseline | 数据访问 |
| OD-010 | P2 | Frontend migration scope | 范围定义 |
