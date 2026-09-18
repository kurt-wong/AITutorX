# REPORT-X2.5 — Pre-Migration Documentation Baseline & Cross-System Fact Base

**Document ID**: REPORT-X2.5
**Task**: TASK-X2.5
**Document Type**: Reports / Final Fact Base
**Status**: `ACTIVE — PRE-MIGRATION FACT BASE COMPLETE / AUDITABLE`
**Date**: 2026-09-18
**Decision actor**: Owner
**Hard rule**:
```text
This report is NOT Migration Ready
This report is NOT Migration Authorized
This report is NOT Migration Executed
This report is NOT Gate Passed
```

---

## 0. Evidence Anchor（X2.5 audit，亲验）

```text
AITutorX current HEAD = 2151998c650efb8e7325f6251acc71bc9bc39521 (= origin/main)
X2/X2.1 content baseline = 7002f3807ddbd4b30f945fc417ddb7f90a79fc6c
V3 baseline = cc12d79e9a22f6274100ea0bb61f92493ba88509
Preprocessing baseline = 2b92898f05f6541a5fc65c8300cb8a59a06c4928
Frozen Contract = f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1
Frozen Contract SHA256 = 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
Frozen Contract size = 92197 bytes
Historical audit parent (X2) = 331cbea (not current HEAD)
```

`[FACT-RECOMPUTED]` 经 `git rev-parse` / `git show | sha256sum` / `wc -c` 亲验。

---

## 1. Deliverables index

| Doc | Path |
|-----|------|
| X2.5-00 STATE | `Docs/50_OPERATIONS/X2.5-00-STATE.md` |
| X2.5-01 Baseline matrices | `Docs/20_ARCHITECTURE/X2.5-01-PRE-MIGRATION-BASELINE.md` |
| X2.5-02 Concept/State/Material | `Docs/10_SPEC/X2.5-02-CONCEPT-MATRIX.md` |
| X2.5-03 Producer/Consumer audit | `Docs/30_CONTRACTS/X2.5-03-PRODUCER-CONSUMER-AUDIT.md` |
| X2.5-04 Decision + Candidate | `Docs/40_DECISIONS/X2.5-04-MIGRATION-CANDIDATE-MATRIX.md` |
| X2.5-05 Conflict ledger | `Docs/40_DECISIONS/X2.5-05-CONFLICT-LEDGER.md` |
| X2.5-06 Evidence/Lineage | `Docs/50_OPERATIONS/X2.5-06-EVIDENCE-LINEAGE.md` |
| X2.5-07 Open issues | `Docs/50_OPERATIONS/X2.5-07-OPEN-ISSUES.md` |

---

## 2. 12 个必须回答的问题

### Q1. 三个系统当前各自的真实边界是什么？

| System | True boundary @ X2.5 | Evidence |
|--------|----------------------|----------|
| **AITutorX** | 统一文档治理 + 目标系统叙事；**无生产代码迁入**；**不持有 corpus 本体** | README；X2-01；git tree |
| **preprocessing** | Source Evidence Producer：OCR/repair/reslice/QC/Manifest/IR/evidence；**不产 Question**；**无 Admission Authority** | prd；charter §12；Contract |
| **V3** | Semantic/Question Consumer：seal→Annotation→Resolver→IR/Compiler→Gate→Admission→Question/Instance/Material/Knowledge | V3_SPEC；`domains/*` |
| **Boundary** | AITutorX **内部** Producer↔Consumer；仍须 Contract | X2-02 §1 |
| **Owner** | 唯一 Migration Decision authority；Charter/Gate 未开 | GF-006 OD-01 |

### Q2. 统一架构中谁对什么负责？

完整 Authority Matrix 见 **X2.5-01 §2**。

- Manifest = **preprocessing** Source Identity Authority（「哪个文件」）
- Producer IR = preprocessing 语义证据工件（「表达什么」）；**≠ Question**
- Semantic Annotation / Resolver / Compiler / Gate / Admission / Question / Instance / Knowledge = **V3**
- Migration decision = **Owner**
- path = locator；`source_content_sha256` = 唯一跨系统身份键
- Material = 双侧模型，非纯文字
- Provenance ≠ Quality

### Q3. 哪些 authority 已经确定？

| Determined authority | Basis |
|----------------------|-------|
| `source_content_sha256 = SHA256(raw bytes)` 64 lower hex | Contract；DEC-030/031；OD-04 |
| path 非 identity | Contract 冻结项④ |
| Manifest vs IR 双层职责 | Contract §1.1；DEC-031 |
| Semantic vs Decision 双层词表禁合并 | Contract §0.3/§3.2 |
| Provenance ≠ Quality | AGENTS/X2 |
| Producer 不产 Question；LLM 无 Admission Authority | V3 P2；charter §12 |
| 87 / 71 / 16 接口语义 | Contract §1.6 |
| GF v0.2 冻结；OD-01/03/04/05/06/10/14/18 已记 | GF-006 |
| AITutorX 唯一目标系统；Producer/Consumer 内部边界 | X2 |
| Historical ID 不重编号；UNKNOWN 保留 | X2-03；Contract |

### Q4. 哪些 authority 仍空洞或冲突？

Charter 未落盘（OD-01/BL-09）；Gate 定义未批；Taxonomy 执行 OPEN 且多套 L*（CL-03）；namespace/mapping 未裁；untracked/Design unknown（OQ-GF-017）；D2/D3/D4 OPEN；Contract 账本 FROZEN vs 正文 NOT FROZEN（CL-01）；Data mode 未实施；test baseline 无 canonical（CL-06）；Ledger 归属（CL-10）；semantic unknown 无执行面（CL-09）；unit_type 词面冲突（CL-08）；Registry admitted 空。

### Q5. 跨系统 identity 是否完全明确？

**否。定义层明确；实现/映射层未完全明确。**

- Contract 定义 **明确**；Producer 87 manifest **已落地**（disk RECOMPUTED）
- IR 键名仍 `source_sha256`；OCR 另层 PDF sha
- V3 internal UUID 与 `original_sha256` 历史口径 ≠ 接口键自动成立
- Consumer 验证链：Freeze 时点 NOT IMPLEMENTED；后续 Guardian 叙事须分账
- Question/Instance/Family ↔ historical unit **未映射 = UNKNOWN**
- **定义一致 ≠ 实现一致 ≠ 已验证可迁移**（X2.5-01 §3.1）

### Q6. Producer IR 与 Semantic IR 是否明确区分？

**治理/Contract 文本层：是。迁移叙事层：仍有混淆风险。**

| | Producer IR | V3 Semantic Question IR |
|--|-------------|-------------------------|
| 产出 | preprocessing R52 | 不产出 |
| 角色 | Semantic evidence artifact | Consumer transient |
| 形态 | `resolver_ir.json` | → snapshot/candidate |
| 规模 | 88/71 ADMITTED/1664 units | n/a |
| 迁移规则 | **≠ Question** | 须完整 Consumer 链 |

把 71 读成「71 题可迁」= **错误**。

### Q7. Semantic State 与 Decision State 是否完全区分？

**否。裁决文本已区分；V3 实现层未完全区分。**

- 词表已裁禁合并
- code：`SEMANTIC_STATUS={ready,incomplete}`（无 unknown）；`DECISION_STATUS={pending_review,approved,rejected}` = FACT-RECOMPUTED
- unknown→pending_review **不可达**；静默 incomplete→skip **违反三禁令**
- **approved ≠ Migration Authorized**

### Q8. Material 模型是否足够明确？

**概念层明确（禁止收缩）；管道/迁移层不明确。**

- text/image/figure/chart/diagram/table/other；**single question 亦可有 Material**
- V3 `materials`/`source_figures`；Producer `material_lines`/IR `material_ref`+`materials`
- 图片恢复 Step5 未做；dangling CLAIM；贯穿 **NOT PROVEN**；Contract 未冻图片恢复
- **概念明确 ≠ Material 可迁移**

### Q9. 87 / 71 / 16 / 177 / 166 等分别代表什么？

详见 **X2.5-06**。禁止裸数字。

| Number | Counts | NOT |
|--------|--------|-----|
| 166 | Ocr-markdown 全树 manifest 历史面（87+79） | 题数/接口 |
| 87 | Interface Scope（identity_version==2 + 已回填 sha） | 题数/migrated |
| 71 | IR ADMITTED files（units 1664） | Question |
| 16 | Semantic Pending = 87−71 | failed |
| 79 | v1 legacy | 可自动入接口 |
| 88 | IR 目录面 71+16+1 | 接口面 |
| 177 | Guardian 锚 87md+87manifest+3工件 | 全资产/题数 |
| 356 | R50 基线 | 题数 |
| 86；「166 lineage surface」字面 | **UNKNOWN**（源 docs 无） | 不得发明 |

磁盘亲验：166 manifests，**87** 含 `source_content_sha256`；Step2 report = 87/71/16。

### Q10. 哪些历史资产可以进入 Migration Candidate 集合？

**仅 candidate，无一 migrated。** 明细 **X2.5-04**。

- MIGRATE candidate：V3_SPEC 00–50；Contract freeze object；Papers prd/charter/rule_registry（均 GATE_BLOCKED）
- MERGE/RETAIN：V3 90/91；coordination docs；GF/X2/X2.5 native；REPORT-A~F historical
- GATE_BLOCKED/UNKNOWN：全部 production code/tests/tools
- NOT_READY/UNKNOWN：corpus/IR/pending/legacy/figures/data packs

### Q11. 哪些资产必须保持 UNKNOWN / Historical？

REPORT-G/H/I/K；X2-DSH-*；Design v1.1/untracked GOVERNANCE；D2/D3/D4 面；Set B/REPORT-J/GF-007 Matrix；双树血缘与 hash inventory；16 份 IR regen；`86`/无源口径；EB-008 external；PENDING 载体/准则；Question 映射；Material recovery；以及 **「代码已有/Guardian VERIFIED=可迁移」必须保持 NOT PROVEN**。

### Q12. X3 Migration Gate 之前还缺哪些事实或决策？

| Missing | Type |
|---------|------|
| Charter 全文 + requirements 判定 | Decision+fact |
| Owner 批准 Migration Gate 定义 | Decision |
| Taxonomy 完整执行 | Decision+fact |
| Namespace/mapping authority | Decision |
| untracked/Design/D2/D3/D4 处置 | Decision |
| Data mode 实施证据 | Fact |
| Canonical test baseline 重跑 | Fact |
| Lineage dispositions 87/71/16/166/177/79/双树 | Fact+Owner |
| Contract 双文件状态规则 | Decision |
| Semantic unknown 执行面 | Decision+impl fact |
| Consumer identity 的 migration-grade verification | Fact |
| unit_type / IR 字段名映射 | Decision |
| Material recovery 与贯穿验证 | Fact |
| Set B 或豁免；Registry admission 运营 | Fact |
| bytes HOW 或等价能力证明 | Decision/fact |
| Freeze-time vs Guardian VERIFIED 如何进入 Gate 证据的分账规则 | Decision |

---

## 3. Level separation snapshot

| Layer | X2.5 state |
|-------|------------|
| SPECIFIED | Contract 六项、GF OD、V3_SPEC、prd 等大量存在 |
| IMPLEMENTED | Producer 流水线/87 回填/IR；V3 domains/tests |
| TESTED | 双侧测试资产存在；**基线 CLAIM 冲突** |
| VERIFIED | 锚点/计数/部分字段本轮 RECOMPUTED；**无 migration-grade VERIFIED** |
| MIGRATABLE | **0 assets declared** |
| MIGRATION AUTHORIZED | **UNAVAILABLE** |

---

## 4. Current status（未改变）

```text
Migration Authorization     = UNAVAILABLE
approval_block.status       = invalid_without_charter
Migration Gate              = NOT PASSED / BLOCKED / NOT RUN
GATE_PASSED                 = 0
MIGRATED                    = 0
admitted=true               = NONE
OQ-GF                       = 18; zero CLOSED; OPEN-BLOCKING = 9
BL-09/10/11                 = OPEN
D-048                       = pending_owner_decision
D2/D3/D4                    = OPEN
Next actor                  = Owner
```

---

## 5. Independent auditor path

1. 三仓 `git rev-parse` / remote 对锚点
2. `git show f4941ff:<contract path> | sha256sum` → `9c6b9063…7528`
3. Papers manifest 计数 166；含 `source_content_sha256` → 87
4. 读 Step2 backfill report summary
5. 读 `resolver_ir.json` dispositions → 71/16/1
6. 读 V3 `compile/__init__.py` / `gate/__init__.py`
7. 读 GF-006 / GF-005（OQ 零 CLOSED）
8. 对照 X2.5-01~07 矩阵逐行核 label

---

## 6. X2.5 success criterion

```text
Success = 独立审计者可仅凭矩阵+引用进入三仓与 Frozen Contract 逐条复核
          并分清：事实/实现/测试/验证/未知/历史资产/有资格进 X3 Gate 的候选

Endpoint = Pre-Migration Fact Base Complete / Auditable
       ≠ Migration Ready / Authorized / Executed / Gate Passed
```

UNKNOWN、冲突与证据缺口已显式登记，未为结果美化而隐藏。

---

## 7. End State

```text
Final State: AITutorX X2.5 Pre-Migration Documentation Baseline & Cross-System Fact Base
Status: COMPLETE / AUDITABLE (documentation only)

NOT:
  Migration Authorized / Ready
  Gate Passed（任何 Gate）
  Production code or data migrated
  OQ / BL / D-048 / D2 / D3 / D4 Closed
  admitted=true / GATE_PASSED / MIGRATED
  UNKNOWN forcibly classified
  Frozen Spec / Contract modified

Boundaries held:
  Evidence Anchor ≠ Migration Authorization
  Document commit/push ≠ Migration Authorization
  Freeze ≠ Migration Authorization
  Migration Authority ≠ Migration Execution
  Decision ≠ Migration Approval
  Migration Candidate ≠ Migrated
  IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ MIGRATABLE ≠ MIGRATION AUTHORIZED
  Provenance ≠ Quality
  Producer IR ≠ V3 Semantic IR
  Semantic State ≠ Decision State

Next actor: Owner
```

---

*REPORT-X2.5 registered. Pre-migration fact base complete / auditable. Nothing migrated.*
