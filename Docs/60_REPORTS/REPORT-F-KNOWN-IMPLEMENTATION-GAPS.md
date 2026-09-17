# Report F — AITutorX Known Implementation Gaps

**日期**: 2026-09-16
**分类**: OBSERVED / INFERRED / CLAIM / DECISION REQUIRED / IMPLEMENTATION GAP

---

## 1. V3 Consumer Implementation Gaps

### GAP-001: D2 identity_version Gate — IMPLEMENTATION GAP + DECISION REQUIRED

**状态**: V3 identity modules 中零 `identity_version` 检查。
**证据**: 读取全部 5 个 identity 模块（M1-M5），无任何 `identity_version` 引用。
**分类**: IMPLEMENTATION GAP + DECISION REQUIRED

### GAP-002: D3 Semantic Boundary 四状态机 — NOT STARTED + DECISION REQUIRED

**状态**: SEMANTIC_STATUS 冻结为 `{ready, incomplete}`，无 `unknown`。
**证据**: `backend/app/domains/compile/__init__.py` line 29。
**分类**: IMPLEMENTATION GAP + DECISION REQUIRED

### GAP-003: D4 Execution Ordering — UNKNOWN + DECISION REQUIRED

**状态**: V3 scheduling 无实现。
**分类**: UNKNOWN + DECISION REQUIRED

### GAP-004: Non-ready Units Silent Skip — OBSERVED

**状态**: `runner_b2.py` lines 322-329: `semantic_status != "ready"` → skip。
**违反原则**: "UNKNOWN is retained data — 不得 silent skip"。
**分类**: OBSERVED

### GAP-005: SEMANTIC_STATUS `unknown` Not Materialized — IMPLEMENTATION GAP

**状态**: 代码中无 `unknown` 状态处理路径。
**分类**: IMPLEMENTATION GAP

---

## 2. Producer Implementation Gaps

### GAP-006: Producer Test Failure — OBSERVED

**状态**: `test_r67_t13_real_corpus_smoke` FAIL (768 AUDIT_FROM_UNMATCHED)。
**分类**: OBSERVED

### GAP-007: Producer Data Not in Git — OBSERVED

**状态**: raw_data / ir_data / Ocr-markdown 在 .gitignore 中。
**影响**: 数据 baseline 无法从 repo 独立重建。
**分类**: OBSERVED (by design)

### GAP-008: Producer Absolute Path Dependency — OBSERVED

**状态**: runner 和 scripts 使用绝对路径。
**分类**: OBSERVED

---

## 3. Cross-System Gaps

### GAP-009: 9 Untracked Docs — DECISION REQUIRED

**状态**: 9 个 V3 文档从未进入 git，Authority UNKNOWN。
**分类**: DECISION REQUIRED

### GAP-010: DEC Numbering Collision — OBSERVED

**状态**: DEC-012~036 两 repo 编号冲突。
**分类**: OBSERVED (documented, mapping in Report C)

### GAP-011: Contract §1.6 Pending Carrier / OQ-21 — CLAIM

**状态**: Contract §1.6 pending carrier 机制，OQ-21 未关闭。
**分类**: CLAIM

### GAP-012: UNKNOWN Actor on Producer Apply — OBSERVED

**状态**: DEC-048 D-048-3 记录 unknown actor working-tree deletions。
**分类**: OBSERVED

---

## 4. 汇总

| Gap ID | 分类 | 优先级 | 阻塞迁移？ |
|--------|------|--------|-----------|
| GAP-001 | IMP GAP + DECISION | P0 | 是 (D2) |
| GAP-002 | IMP GAP + DECISION | P0 | 是 (D3) |
| GAP-003 | UNKNOWN + DECISION | P0 | 是 (D4) |
| GAP-004 | OBSERVED | P1 | 否 |
| GAP-005 | IMP GAP | P1 | 否 |
| GAP-006 | OBSERVED | P1 | 否 |
| GAP-007 | OBSERVED | P2 | 否 (by design) |
| GAP-008 | OBSERVED | P2 | 否 |
| GAP-009 | DECISION REQUIRED | P0 | 是 |
| GAP-010 | OBSERVED | P2 | 否 |
| GAP-011 | CLAIM | P2 | 否 |
| GAP-012 | OBSERVED | P1 | 否 |

---

## 5. What Is Proven vs Claimed vs Stale vs Unknown

### Proven (verified this audit)
- Contract v0.2 freeze integrity (SHA256 双点一致)
- V3 test baseline: 1780 passed
- Both repos in sync with remote
- 9 untracked docs have zero git history
- Identity modules M1-M5 committed at `6c4e3ff`
- Producer test: 1 pre-existing failure

### Claimed (not independently verified this round)
- DEC-028 Part 5 `unknown` requirement content
- OQ-21 current status
- Producer data baseline completeness

### Stale
- DESIGN-v1.md (superseded by v1.1?)
- CONTRACT.md early version (superseded by v0.2?)
- CONTRACT-v0.2-DRAFT-SKELETON.md (superseded?)

### Unknown
- D2/D3/D4 resolution path
- Design v1.1 authority level
- Producer data reconstruction method for AITutorX
