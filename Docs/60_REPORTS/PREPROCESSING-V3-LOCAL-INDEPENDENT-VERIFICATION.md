# PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION

**Document ID**: PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION  
**Name History**: file and Document ID renamed 2026-09-28 from `MIMO-PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION` per DOC-GOV §8 R2 (producer name must not appear in filename). Body findings and Date unchanged.  
**Document Type**: Independent Forensic Audit / Feasibility Verification  
**Date**: 2026-09-22  
**Authority**: Independent auditor (MiMo). Evidence-first. No architecture decision taken on behalf of Owner.  
**Evidence labels**: `OBSERVED` / `DERIVED` / `HYPOTHESIS` / `CONCLUSION`  
**Working directory**: `D:\Project\AITutor-X`  
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 1. Scope

本报告是对三个本地工作区的独立取证，不接受任务描述中的任何待验证假设作为前提。

| 项目 | 路径 | 角色 |
|---|---|---|
| Preprocessing | `D:\Project\Papers` | Producer（文档理解 / 题目抽取 / 结构事实发现） |
| V3 | `D:\Project\AITutors-v3` | Consumer（Annotation / Resolver / IR / Compiler / Gate / Admission） |
| Integration | `D:\Project\AITutor-X` | 集成治理与边界文档（当前无生产代码） |

目标问题（最终目标）：

> 现在的 Preprocessing 到底已经完成了什么，V3 到底还缺什么，以及从 Preprocessing 到 V3 的最小、正确、可治理的系统边界究竟应该在哪里。

本报告**不**替 Owner 做架构决策。

---

## 2. Local workspace state

`OBSERVED`（任务开始时 `git status --short` / `git status -sb`）：

| Repo | Branch | HEAD | tracked tree | LOCAL_ONLY | vs origin/main |
|---|---|---|---|---|---|
| Papers | `main` | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` | clean | 无 | 0 / 0 |
| AITutors-v3 | `main` | `3e2f9bbd2b3464453e1c42db4af75e315496b335` | clean (tracked) | **10 untracked**（`Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-*` 契约/设计/实施报告 + `Docs/GOVERNANCE/`） | 0 / 0 |
| AITutor-X | `main` | `5618b0075d34f5e0763682d75a9f223202a3e9cb` | clean (tracked) | **16 untracked**（`Docs/60_REPORTS/REPORT-G/H/I/K`、`X2*-DSH-*`、`contract_check.bin`） | 0 / 0 |

Remotes：

- Papers → `https://github.com/kurt-wong/Aitutors-preprocessing.git`
- AITutors-v3 → `https://github.com/kurt-wong/AITutors-v3.git`
- AITutor-X → `https://github.com/kurt-wong/AITutorX.git`

`OBSERVED`：三仓 tracked 均与 `origin/main` 同步；LOCAL_ONLY 仅存在于未跟踪文档/二进制，**不是**生产代码差异。  
`DERIVED`：后续结论可以建立在当前 HEAD 上；LOCAL_ONLY 文档仍被本报告阅读并引用，标记为 `LOCAL_ONLY`。

---

## 3. Repository / commit state

`OBSERVED` 末次提交：

| Repo | `git log -1 --oneline` |
|---|---|
| Papers | `2b92898 DEC-049: D2/D3/D4 Decision Brief (Evidence First, No Self-Fix)` |
| AITutors-v3 | `3e2f9bb fix: reject non-scalar identity_version at interface boundary` |
| AITutor-X | `5618b00 docs(x2.7): record int-full-01 full-corpus end-to-end integration run baseline` |

`OBSERVED`：AITutor-X 存在 X2.7 全量集成运行报告与 artifacts（`Docs/60_REPORTS/X2.7-INT-FULL-01-*`），该运行时 AITutorX HEAD 曾为 `a8e9319`；当前 HEAD 已推进到 `5618b00`（记录该 run）。本审计在当前 HEAD 上独立复核其结论。

---

## 4. Preprocessing architecture

### 4.1 代码形态

`OBSERVED`：`D:\Project\Papers` **不是**标准 Python package 生产服务，而是 **scripts 管线 + 语料 + QC/审计脚本 + 协调文档**。

关键目录：

| 路径 | 实际内容 |
|---|---|
| `Ocr-markdown/` | OCR→Markdown 源语料 + reslice 切分结果 + `*.manifest.json` 标注 |
| `original/` | 原始 PDF/DOC/DOCX |
| `scripts/` | 70+ 脚本：OCR runner、reslice、QC、identity backfill、resolver_reference、审计/攻击/修复 |
| `data/` | QC/审计快照、interface scope、phase3 migration、`resolver_ref_r52/resolver_ir.json` |
| `reports/` | prereview / reclassify / preview |
| `governance/` | phase charter / risk / rules |
| `Docs/COORDINATION/` | 与 V3/X 的契约、冻结、交接（含 ADMITTED 相关字段名） |

`OBSERVED` 代码级职责（以 docstring + 调用关系为准，不以 README 为准）：

| 能力 | 代表脚本 | 是否生产链路 |
|---|---|---|
| OCR 输入 | `pac_ocr_runner.py` | 实验/批处理 |
| Markdown 输入 | `Ocr-markdown/**` | 语料事实 |
| segmentation / splitting | `reslice_pipeline.py` | 批处理切分 |
| question extraction | LLM annotation → `*.manifest.json`（model=`mimo-x-pro-preview`） | **核心产出** |
| metadata annotation | 同上 + `question_identity.py` | **核心产出** |
| unit / question / material / answer / explanation region | `manifest.units[]` + `resolver_reference.py` | **核心产出** |
| evidence / provenance | `basis` / `basis_evidence` / `printed_provenance` / `provenance.source_lines` | **核心产出** |
| identity / SHA256 | `identity_version` + `source_content_sha256`（v2 face） | **核心产出** |
| IR | `resolver_reference.py` → `resolver_ir.json` | **参考实现，明确不进生产** |
| validation / QC | `reslice_qc.py`、`pac_audit_*`、`phase*_qc` | 质量闸门 |
| ADMITTED / QC_FAIL | `resolver_ir.json` disposition | **产出物事实** |
| 实验 runner / 对抗 | `r4x–r6x_*`、`phase2_adversarial_*` | 实验/对抗，非生产 |

`OBSERVED` `scripts/resolver_reference.py` 自我定位（docstring 逐字要点）：

> 三边界 Resolver 只做 structural 判定(无语义判定)  
> 定位: 参考实现 + 对抗审查对象，**不进生产链路**

`CONCLUSION`：Preprocessing 的“生产事实发现”主体是 **manifest 标注 + 源 MD 行号锚定 + identity v2 + QC disposition**；`resolver_ir.json` 是参考/审计聚合产物，不是持续生产输出。

### 4.2 实际产出物 schema（以文件为准）

`OBSERVED` live manifest（`Ocr-markdown/**/*.manifest.json`）两种 face：

**v2 face（87 份，Interface Scope）** 顶层键：

`source_file`, `model`, `annotation_meta`, `units`, `identity_version`, `sections`, `source_content_sha256`

**v1 face（79 份）** 顶层键：

`source_file`, `model`, `annotation_meta`, `units`  
→ **无** `identity_version` / `source_content_sha256`。

`OBSERVED` manifest unit 字段（实际键，非文档声明）：

- 共有：`unit_id`, `unit_type`, `question_numbers`, `original_question_type`, `answer_lines`, `explanation_lines`, `section_ref`/`section`, `printed_number`, `printed_provenance`, `basis`, `basis_evidence`
- standalone：`stem_lines`, `options_lines`, `extra_lines`
- composite：`material_lines`, `questions_lines`
- 稀有：`explanation_lines_note`

`OBSERVED` resolver IR unit 字段（`resolver_ir.json` inner `ir.units[]`）：

`unit_id`, `unit_type`, `question_numbers`, `printed_number`, `printed_provenance`, `basis`, `basis_evidence`, `section_ref`, `section_title`, `content{stem_lines,options_lines,answer_lines,explanation_lines,material_lines,questions_lines}`, `material_ref`, `answers`, `answer_text`, `flags`, `provenance{source_file,source_version,source_lines,manifest_file,qc_verdict,extraction_method,confidence_state}`

`OBSERVED` IR file record：

`file`, `ir{ir_version,source_file,source_sha256,manifest_file,qc_verdict,materials,units}`, `reasons`, `qc_verdict`, `disposition`

`CONCLUSION`：产出物远超“简单 metadata”——包含 **行区间正文、材料区、答案表结构尝试、flags、basis 证据字符串、逐 unit provenance、源 SHA、manifest 路径、QC verdict**。

---

## 5. Preprocessing actual outputs

`OBSERVED` 语料规模（live `Ocr-markdown`）：

| 指标 | 值 |
|---|---|
| manifests | 166 |
| units 合计 | 4609 |
| unit_type | `standalone_question` 3935 / `composite_question` 673 / **`andalone_question` 1** |
| Interface Scope v2 manifests | 87（`identity_version==2` + `source_content_sha256`） |
| v1 manifests（无 identity 字段） | 79 |

`OBSERVED` `original_question_type` 词表（71 ADMITTED 内）：

`single_choice` 1042, `short_answer` 346, `fill_in` 126, `reading` 48, `multiple_choice` 66, `essay` 18, `cloze` 5, `reading_expression` 5, `seven_to_five` 3, `grammar_fill` 3, `vocabulary_fill` 2

`OBSERVED` 71 ADMITTED 的 IR 层统计（1664 units）：

| 字段 | 分布 |
|---|---|
| `flags` | `[]` 1071 / `answer_table_unresolved` 502 / `answer_number_mismatch` 91 |
| `basis` | `printed_as_is` 1041 / `unverified` 596 / `shift` 18 / `answer_key` 9 |
| `printed_provenance` | `source_line` 1041 / `unknown` 596 / `migration_report` 27 |
| `answers` | `null` 1136 / dict 528（答案表解析尝试） |
| content 有 options / explanation / material | 945 / 474 / 278 |

`CONCLUSION`（回答 Q2）：产出**显著丰富于简单 metadata**；但语义完备性不均匀，且诚实保留了 `unverified` / `unknown` / `answer_table_unresolved`。

---

## 6. ADMITTED population verification

**不信任历史报告数字，从本地文件重算。**

`OBSERVED` `data/resolver_ref_r52/resolver_ir.json`（`ir_version=resolver-ir-0.1`, `files` 88）：

| disposition | n | qc_verdict |
|---|---|---|
| `ADMITTED` | **71** | PASS 71 |
| `REJECTED_QC_FAIL` | **16** | FAIL 16 |
| `REJECTED_V1` | **1** | null 1 |

`OBSERVED` `data/interface_scope_snapshot_step1.json` summary：

```json
{"n_rows": 87, "ir_records": 87, "ir_admitted": 71, "ir_rejected_qc_fail": 16, "ir_absent": 0}
```

`OBSERVED` `data/interface_scope_step2_backfill_report.json`：

`n_scope=87`, `n_ir_admitted=71`, `n_semantic_pending_qc_fail=16`, `n_ir_absent=0`

`OBSERVED` live manifest face recount：

- `identity_version==2` + `source_content_sha256`：**87**
- 无 identity 字段：**79**

**人口对账**：

```text
Interface Scope = 87 = 71 ADMITTED + 16 QC_FAIL/semantic pending
V1 Reject = 1（REJECTED_V1，在 88 条 resolver_ir 中，不在 87 Interface Scope 内）
```

| 历史数字 | 本地重算 | 结论 |
|---|---|---|
| Interface Scope 87 | 87 | **一致** |
| ADMITTED 71 | 71 | **一致** |
| QC_FAIL / Semantic Pending 16 | 16 | **一致** |
| V1 Reject 1 | 1 | **一致** |

`CONCLUSION`（回答 Q3 的 population 维度）：历史 87/71/16/1 **在本地真实文件上可独立复现**。  
**注意**：population 数字正确 ≠ 每个 ADMITTED 的语义字段都正确（见 §7–§8）。

---

## 7. Source → Artifact accuracy verification

### 7.1 Identity

`OBSERVED` 对 **全部 71 ADMITTED** 执行 `sha256(source bytes)` 对 `ir.source_sha256`：

| 结果 | n |
|---|---|
| MATCH | **71** |
| MISMATCH | 0 |
| SOURCE MISSING | 0 |

`OBSERVED` 5 份抽样再核（会考历史/地理/政治/数学/物理）：claimed == actual。  
`OBSERVED` interface_scope snapshot 对 87 份记录 `ir_admitted_sha_match=71`。

`DERIVED`：`source bytes → SHA256 → manifest.source_content_sha256（v2）→ ir.source_sha256` 在 71 ADMITTED 上闭环。

### 7.2 Question boundary / line ranges

`OBSERVED` 对 71 ADMITTED 全部 `provenance.source_lines` 角色区间做程序化校验：

| 检查 | 结果 |
|---|---|
| 区间形态合法（int, 1≤a≤b≤n） | 100%（stem 1337 / options 945 / answer 1664 / explanation 474 / material 278 / questions 278 全部 `in_bounds`） |
| 首行文本锚定（claimed[0] 出现在源切片） | 100% `text_anchor_ok` |
| `material_ref` 可解析到 `ir.materials` | 278/278 |

`OBSERVED` 结构不变量抽查发现的真实质量问题（**不是越界，而是切分/编号语义**）：

| 现象 | n | 解读 |
|---|---|---|
| `material_lines == questions_lines` 同区间 | 41 | 材料区与题区未拆开（结构折叠） |
| multi-q 的 questions 区缺少部分印刷题号 | 54 / 148 | OCR/排版导致题号不全（常为 `（1）（2）` 小问格式） |
| answer 首行数字 ≠ unit.question_numbers | 212 | 多含“1. 本题共10分…”评分说明行；与 flag `answer_number_mismatch`(91) 部分重叠，**启发式过报** |
| stem 首行数字 ≠ question_numbers（standalone） | 33 | 同类评分前缀/重编号噪声 |

`DERIVED`：**行锚定与源字节身份可靠**；**题边界切割存在可观察误差**（材料/小问/答案区编号）。  
`CONCLUSION`：不能把“identity 71/71 通过”表述成“boundary 71/71 语义正确”。

### 7.3 Unit structure

`OBSERVED` 71 ADMITTED units：

- `standalone_question` 1385 / `composite_question` 278 / `andalone_question` 1
- composite 全部 278 有 `material_ref` 且可解析
- multi-q（`len(question_numbers)>1`）148 个 unit；其中 94 个印刷题号齐全，54 个缺号

`OBSERVED` `andalone_question` 位于：

`Ocr-markdown/reslice-batch-C/合格考/化学/2020北京高中合格考化学（第一次）（教师版）(1).manifest.json` `unit_id=Q1`（全文 34 units）

`CONCLUSION`：`unit_type` 结构与源文档大体一致；composite/material 关系真实存在；multi-question 真实存在但小问分解**未做**（见 §10 PRODUCER GAP）。

---

## 8. Semantic metadata accuracy

必须拆开两类事实：

### A. Structural fact（可程序化回源）

| 事实 | 可靠度 | 证据 |
|---|---|---|
| 行号区间存在且在界内 | **高**（71/71） | §7.2 |
| 源字节 SHA | **高**（71/71） | §7.1 |
| material_ref 链接 | **高**（278/278） | §7.2 |
| 印刷题号 / section_ref | **中高** | 字段齐全；少量 `basis=shift` / `unverified` |
| question_numbers 集合 | **中** | multi-q 54/148 印刷号不全 |

### B. Semantic classification（模型/规则解释，非直接回源字节）

| 事实 | 可靠度 | 证据 |
|---|---|---|
| `original_question_type` | **中**（词表稳定，未人工全量核对） | 12 值闭集分布合理 |
| `unit_type` | **高（两值）+ 1 噪声** | 仅 `standalone/composite` + 1×`andalone` |
| answer 是否完整 | **中低** | `answer_table_unresolved` 502；`answers=null` 1136 |
| explanation 是否完整 | **中** | 仅 474/1664 有 explanation 区 |
| 题目内容理解 / 知识点 | **未提供** | 无 knowledge / skill 字段 |

`OBSERVED` evidence closure（1664 units）：

| basis | n | basis_evidence | printed_provenance | 闭环？ |
|---|---|---|---|---|
| `printed_as_is` | 1041 | 有 | `source_line` | **是** |
| `shift` | 18 | 有 | 多 `migration_report` | **是** |
| `answer_key` | 9 | 有 | 多 `source_line` | **是** |
| `unverified` | 596 | **空** | **`unknown`** | **否（诚实 UNKNOWN）** |
| 全部 | 1664 | — | — | 100% 有 `provenance.source_lines` |

`CONCLUSION`（回答 Q3 完整维度 + §7 标题）：

- **Structural reliable：是（在 71 ADMITTED 上）。**
- **Semantic reliable：部分。** 题型/结构分类可用；答案表与小问级语义不完备，且 596 unit 的印刷题号 provenance 为 `unknown`。
- 不得用单一 “accuracy” 混述。

---

## 9. Evidence / provenance verification

`OBSERVED` 闭环模型（实际字段）：

```text
fact (content.*_lines / question_numbers / basis)
  → evidence (basis_evidence 字符串, 常含 L{line})
  → provenance (printed_provenance + provenance.source_lines + source_version=sha256)
  → source (source_file bytes, SHA256 可重算)
```

`OBSERVED`：

- 1664/1664 units 有 `provenance.source_lines`
- 1068/1664 有实质 `basis_evidence`（printed_as_is+shift+answer_key）
- 596/1664 为 `basis=unverified` 且 `basis_evidence=""` 且 `printed_provenance=unknown`——**无印刷题号证据，保留 UNKNOWN，不伪造**
- IR 顶层有 `extraction_method=line_span_v1` 与 `confidence_state`（如 `structural_only+flags`）

`CONCLUSION`（回答 Q4）：

> 对 **structural facts**，证据链完整，V3 可安全消费其行锚定与身份。  
> 对 **printed_number / answer completeness / sub-question**，存在明确的无证据或 flag 缺口；V3 **不得**把它们当作已验证语义。  
> “足够安全消费”的正确表述是：**可安全消费 structural input + 显式 gap/flag；不可无条件消费全部语义字段。**

---

## 10. V3 architecture and call graph

### 10.1 模块地图

`OBSERVED` `AITutors-v3/backend`：

| 层 | 模块 | 分类 |
|---|---|---|
| Identity | `core/manifest_identity.py` (M1), `raw_bytes_identity.py` (M2), `ir_identity.py` (M3), `identity_verifier.py` (M4), `identity_gate.py` (M5) | **Production safety** |
| Annotation | `domains/annotation/service.py` | **Production**（LLM 标注） |
| Resolver | `domains/resolver/*` | **Production**（显式 marker → span；可失败不可猜） |
| Compile | `domains/compile/{ir,compiler,snapshot,identity_normalization,mapping_registry}` | **Production**（IR/Compiler）；`mapping_registry` 为 **governance scaffold, NOT wired** |
| Gate | `domains/gate/{binding,grammar,payload,policy,service,admission}` | **Production** |
| Evidence | `domains/evidence/*` | **Production**（ValidationEvent 权威） |
| Source | `domains/source/{import,seal,quality,line_index,figure_index}` | **Production** |
| Task | `domains/task/{executor,service}` | **Production orchestration** |
| API | `api/routers/*` | **Production HTTP** |
| Integration probe | `scripts/preprocessing_consumer/*` | **Experimental / integration harness（非 app 生产路径）** |
| Gate B experiments | `scripts/gate_b/*` | **Experimental harness** |
| Tests | `tests/**` | **Tests**（含 M1–M5 对抗、x26 integration） |

### 10.2 正式生产调用链（TaskExecutor）

`OBSERVED` `domains/task/executor.py` docstring + imports：

```text
Input: Document upload
  ↓ SealService (source seal / immutability)
  ↓ AnnotationService (LLM → SemanticAnnotation payload)
  ↓ GateService.run
       1. SourceResolver → ResolvedRun / ResolvedSpan
       2. IRBuilder → IR (semantic_status ready|incomplete|unknown)
       3. Compiler → CompiledSnapshot
       4. payload.build + GatePolicy.evaluate → gate_decision
       5. create AdmissionCandidate (pending_review)  [idempotent by LE hash]
       6. auto_approve → AdmissionService.approve
          rejected   → AdmissionService.reject
  ↓ AdmissionService.approve 物化 A 域
       Question / QuestionInstance / role_contents / material / unit_group
  ↓ DB
```

`OBSERVED`：`mapping_registry` 文档字符串：

> Production mapping enforcement = NOT IMPLEMENTED (P1-P13 all OPEN).  
> This module is a GOVERNANCE SCAFFOLD. No production code imports it.

### 10.3 Preprocessing 消费链（scripts/preprocessing_consumer，非生产入口）

`OBSERVED` 两个 harness 入口：

**`runner.py` (Phase 0)**：

```text
manifest → boundary.enforce_interface_scope
        → annotation_adapter / resolved_span_adapter (SKIP SourceResolver)
        → production GateService → AdmissionService
```

- **无 M1–M5**
- 产出 report，不作为正式入库产品

**`runner_b2.py` (Phase 0.2)**：

```text
manifest
  → boundary + M1→M5 Consumer Identity Verification（任一拒绝则下游 NOT REACHED）
  → annotation_adapter → ResolvedRun (SKIP SourceResolver by design)
  → IRBuilder → Compiler → GatePolicy → AdmissionCandidate
```

- `AdmissionService.approve` **不在**此入口（仅建 candidate）

`OBSERVED` X2.7 全量运行（172 manifests）三 leg 摘要：

| Leg | 结果 |
|---|---|
| B2 primary（无 `--resolver-ir`） | 172/172 **M5 BLOCK**：85 `manifest_sha_missing` + 87 `semantic_pending/ir_absent`；下游全 NOT REACHED |
| V1 primary (`runner.py`) | Interface Scope 拒 85；接受 87；annotation 86 成功 1 失败；Resolver **SKIP BY DESIGN**；spans 7029 valid 0 unresolved；Gate candidates **4**；units_skipped_not_ready **2309** |
| B2 probe secondary（+ 真实 batch `resolver_ir.json`） | **M5 PASS 71** / BLOCK 101；annotation 70 成功 1 失败；spans 4854；IR 70 docs / 1630 root units；compiler **533 leaves** / 178 materials；gate **533 candidates** 全 `pending_review`（auto_approve=0）；1097 skipped_not_ready |

`CONCLUSION`：

- **正式生产链**是 TaskExecutor 的 LLM Annotation 路径，**不是** preprocessing_consumer。
- preprocessing_consumer 是 **已实现的集成边界实验层**，证明“可接”，但未升格为 production path。
- **两个 harness 入口边界深度不一致**（NEW-F1）：`runner.py` 无 M1–M5 却进生产 GateService/AdmissionService。

---

## 11. Producer → V3 field-level mapping

以**实际字段**为准（manifest face + IR face）。V3 目标 = `ManifestUnit` / annotation payload / `ResolvedSpan` / `IRNode`。

| Preprocessing field | 实际含义 | Source evidence | V3 target | 直接兼容 | Canonicalization | 信息损失 / Gap |
|---|---|---|---|---|---|---|
| `source_file` | 源 MD 路径（locator） | path | `Manifest.source_file` / `provenance.source_file` | 是 | 无 | path ≠ identity（设计如此） |
| `source_content_sha256` | SHA256(raw source bytes) | 可重算 | M1/M2/M4 identity | 是（v2） | 无 | **v1 87/166 之外缺失 → PRODUCER GAP for 79** |
| `identity_version` | 接口身份版本 | 字段 | `enforce_interface_scope` | 仅 `==2` | 无 | v1 拒收（正确） |
| `unit_id` | Producer 单元 id | 字段 | `IRNode.unit_id` / span_id | 是 | 无 | 无 |
| `unit_type` | `standalone_question` / `composite_question` / 噪声 | 字段 | `standalone_unit` / `composite_unit` | **否（legacy 名）** | **需要**：OD-2 两条映射 | `andalone_question` → fail-loud `UNKNOWN_UNIT_TYPE` |
| `question_numbers` | 题号列表 | 印刷/迁移证据 | `question_number` / `question_number_range` | 大体是 | 范围格式化 | multi-q 小问不拆：**PRODUCER GAP**（`SUB_QUESTION_DECOMPOSITION_UNAVAILABLE`） |
| `original_question_type` | 题型（12 值） | 模型标注 | `IRNode.original_question_type` **verbatim** | 是（透传） | **无 canonical QT 闭集接入 runtime** | **CANONICALIZATION GAP**（QT 词表未治理进 runtime） |
| `stem_lines` | 题干行区间 `[a,b]` | 源 MD 行 | `content.stem` + ResolvedSpan | 是 | 无 | 无（行锚定可靠） |
| `options_lines` | 选项行区间（整块） | 源 MD 行 | V3 需要 **per-label option span** | **否** | 无 | **PRODUCER GAP**：`OPTION_LABEL_SPAN_UNAVAILABLE` → choice 题易 `incomplete` |
| `extra_lines` | 补充区 | 源 MD 行 | span role `extra` | 是 | 无 | 弱语义 |
| `answer_lines` | 答案区 | 源 MD 行 | `content.answer` + span | 是 | 无 | 答案表整块，题号映射弱 |
| `explanation_lines` | 解析区 | 源 MD 行 | `content.explanation` | 是 | 无 | 覆盖率仅 474/1664 |
| `material_lines` / `questions_lines` | 材料/子题区 | 源 MD 行 | `shared_components.material` + `sub_questions` | 结构可映射 | 无 | 41 份 material==questions 同区间；子题不拆 |
| `answer_evidence` | 答案证据 | 字段/空 | 无直接 1:1 | 部分 | — | **CONSUMER GAP**（V3 annotation 契约不直接吃此面） |
| `basis` / `basis_evidence` | 题号合法性依据 | 字符串+行号 | 保留在 ManifestUnit；**不进 IR identity** | 读取层保留 | 无 | **CONSUMER GAP**：下游 IR/Gate 不消费 |
| `printed_number` / `printed_provenance` | 印刷题号及来源 | 字段 | ManifestUnit 保留 | 读取层保留 | 无 | 596 `unknown` |
| `flags` | `answer_table_unresolved` 等 | IR 面 | 无 V3 等价强制字段 | **否** | 无 | **CONSUMER GAP**（质量旗标未进入 Gate 策略） |
| `provenance.source_lines` | 逐 role 行区间 | IR 面 | ResolvedSpan.line_refs | 是（adapter） | 无 | 无 |
| `provenance.source_version` | 源 SHA | IR 面 | identity 语义一致 | 是 | 无 | 无 |
| `materials` + `material_ref` | 材料区注册表 | IR 面 | shared material span | 是 | 无 | 无 |
| `answers` (dict cells) | 答案表尝试解析 | IR 面 | 无 | **否** | 无 | **PRODUCER GAP**（502 unresolved）+ **CONSUMER GAP** |
| `sections` / `section_ref` | 分节 | v2 face | ManifestSection | 是 | 无 | 无 |
| `model` / `prompt_version` / `validation_issues` / `warnings` | 标注运行元数据 | `annotation_meta` | 可进 audit | 部分 | 无 | 非语义身份 |

**Gap 标签汇总**：

- `PRODUCER GAP`：per-option label spans；sub-question decomposition；79 份缺 `source_content_sha256`；答案表题号→答案稳定映射；部分 material/questions 区间折叠
- `CONSUMER GAP`：`flags` / `basis` / `answer_evidence` / 答案表 dict 未进入正式 IR/Gate 策略；`mapping_registry` 未接入 production
- `CANONICALIZATION GAP`：unit_type 两条翻译**已实现且授权**；question_type **无** runtime canonical 闭集
- `IDENTITY / GOVERNANCE GAP`：v1 不得静默升 v2；`andalone_question` 必须 fail-loud；M1–M5 与 Interface Scope 必须 AND；两个 runner 深度不一致

---

## 12. Resolver assessment

存在两套“Resolver”，必须分开：

### A. Preprocessing `scripts/resolver_reference.py`

| 项 | 判定 |
|---|---|
| semantic inference / classification | **否**（docstring：无语义判定） |
| line range resolution | **是**（span 传播） |
| source reference validation | **是**（C-IN-*） |
| identity validation | 只读 manifest v2，不推断 |
| evidence binding | **是**（C-OUT-2 provenance） |
| structural normalization | **是** |
| 生产路径？ | **否**（“不进生产链路”） |

→ 归类：`STRUCTURAL / SAFETY WORK` + **reference implementation**

### B. V3 `domains/resolver/*`

| 项 | 判定 |
|---|---|
| semantic inference | **否**（“可以失败，但不能猜”；禁 fuzzy 自动接受） |
| line range resolution | **是**（显式 marker → ResolvedSpan） |
| source reference validation | **是** |
| identity validation | 本身不做 SHA；配合 M* |
| evidence binding | ResolvedSpan + EvidenceReference 提案；权威在 ValidationEvent |
| structural normalization | **是**（match_normalization） |
| 在 preprocessing 集成路径上 | **SKIPPED BY DESIGN**（`resolved_span_adapter` 直供行号） |

| 责任 | 分类 |
|---|---|
| 显式 reference → span | `STRUCTURAL / SAFETY WORK` |
| unresolved 诊断（exact/normalized/fuzzy 尝试记录） | `STRUCTURAL / SAFETY WORK`（fuzzy 只诊断不接受） |
| 在 preprocessing 已给精确行号时再跑一遍搜索 | `DUPLICATED PRODUCER/CONSUMER RESPONSIBILITY`（集成路径已跳过） |
| 无 preprocessing、纯 LLM annotation 时的定位 | `REAL CONSUMER REQUIREMENT`（生产 TaskExecutor 仍需要） |

`CONCLUSION`（回答 Q5 关于 Resolver）：

- **不能删除 V3 Resolver**：生产 LLM Annotation 路径仍依赖它做 reference→span。
- **在 preprocessing 直供行号的集成路径上，Resolver 搜索段被正确跳过**；这不是“Resolver 无意义”，而是责任上移。
- 仍需保留的是 Resolver 的 **fail-closed / 不猜** 安全语义与 unresolved 诊断，而不是其“发现题目”的能力。

---

## 13. M1–M5 assessment

`OBSERVED` 代码定位（core/*）：

| ID | 模块 | 保护什么 | 验证什么 | 输入 | 输出 | Semantic? | Identity/Integrity? | Preprocessing 已提供？ | V3 仍需要？ | 删除会失去什么 | 归类 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **M1** | `manifest_identity` | 身份声明形态 | manifest `source_content_sha256` 可读且形态正确 | manifest JSON | sha 声明 | 否 | **是** | v2 face 已写字段；v1 无 | **是**（消费侧闸门） | 无法 fail-closed 拒收无声明输入 | **RETAIN** |
| **M2** | `raw_bytes_identity` | 真实字节身份 | SHA256(raw bytes) | 源文件 bytes | computed sha | 否 | **是** | Producer 也写 sha，但消费者必须自算 | **是** | path 冒充 identity / 篡改不可测 | **RETAIN** |
| **M3** | `ir_identity` | 语义证据绑定 | IR 内 `source_sha256` 与 manifest 对齐 | resolver IR | ir sha | 否（一致性） | **是** | resolver_ir 提供 | **是**（语义轴） | IR 与身份脱钩，假语义证据可混入 | **RETAIN** |
| **M4** | `identity_verifier` | 三方一致 + 语义轴独立 | computed vs manifest（identity）；ir vs manifest（semantic） | 三 sha | `VerificationResult` 双轴 | 语义轴是“证据存在”不是“语义理解” | **是** | 不重复语义识别 | **是** | 无法区分 identity fail vs semantic pending | **RETAIN** |
| **M5** | `identity_gate` | 放行决策 | identity+semantic 真值表（VERIFIED+PENDING=BLOCK） | M4 结果 | PASS/BLOCK | 否 | **是** | 否 | **是** | 半验证数据可进语义消费 | **RETAIN** |
| 附加 | `boundary.enforce_interface_scope` | Contract Interface Scope | `identity_version==2` + 身份字段 | 声明字段 | accept/reject | 否 | **是** | v2 自声明 | **是** | v1/越界版本混入 | **RETAIN**（并统一进所有 runner） |

`OBSERVED` X2.7 真实触发：

- M1：85 × `manifest_sha_missing`（v1 face）
- M3/M4 semantic：87 × `ir_absent`（未给 batch IR）/ 16 × `semantic_pending`（QC_FAIL）
- M5：全部 BLOCK 当任一轴失败；71 PASS 当 IR 在场且 sha 对齐
- `andalone_question` 在 boundary 层 `UNKNOWN_UNIT_TYPE` fail-loud

`CONCLUSION`（回答 Q7）：

> M1–M5 **不是**重复语义处理。它们是 **identity / integrity / governance**。  
> Preprocessing 提供了身份**声明与证据**，但**不能**替代消费侧对 raw bytes 的再验证与 AND 门。  
> 全部 **RETAIN**；需要 **ADAPT** 的是把同一套 M1–M5+Scope **统一接入所有 runner**（消除 NEW-F1）。

---

## 14. Canonicalization assessment

`OBSERVED`：

| Producer | Canonical | 状态 |
|---|---|---|
| `standalone_question` | `standalone_unit` | OD-2 授权；`boundary.normalize_unit_type` **已实现**；`mapping_registry` 有表但 **NOT wired to production** |
| `composite_question` | `composite_unit` | 同上 |
| `andalone_question` | （无） | **PROHIBITED** → `UNKNOWN_UNIT_TYPE` fail-loud（正确） |
| `standalone_unit` / `composite_unit` | 自身 | 幂等直通 |
| `original_question_type`（12 值） | 无 runtime 闭集 | **verbatim 透传**；QT ⊥ UT（Owner D1） |

`OBSERVED` X2.7 vocabulary counts 与本审计 71 内分布一致；X2.7 明确：

> No canonical Question Type closed set is wired into the runtime.

`CONCLUSION`：

- unit_type：**简单字段 rename（带 Owner event id）**，不是重新理解题目。已在 consumer boundary 实现。
- question_type：**真正的语义词表治理缺口**（不是 rename）——缺闭集、缺 UNKNOWN 策略、缺进 Gate 的 grammar 映射（关联 NEW-F3 `grammar None`）。
- `mapping_registry` 与 `boundary.normalize_unit_type` **双表并存**：一个 governance scaffold、一个 runtime；需防止第二套权威（已有注释强调 UNIT_TYPES 单一真源，但映射表仍是两处）。

---

## 15. Feasibility probe

### 15.1 独立 probe（本审计）

只读脚本调用真实 `scripts/preprocessing_consumer` 适配器，对 **全部 71 ADMITTED** 执行：

```text
manifest load → enforce_interface_scope → normalize_unit_type
             → manifest_to_annotation_payload
             → load_source_lines + manifest_to_resolved_spans
```

`OBSERVED` 结果：

| 阶段 | PASS | FAIL |
|---|---|---|
| Interface Scope | **71** | 0 |
| annotation payload | **70** | 1（`andalone_question`） |
| resolved spans | **70** / 4898 spans / **0 unresolved** | 1（同上） |
| unit_type 映射 | standalone_question→standalone_unit **1385**；composite_question→composite_unit **278** | UNKNOWN 1 unit |

Case 覆盖（真实 ADMITTED，非构造）：

| Case | 样本 | payload | spans | 备注 |
|---|---|---|---|---|
| A standalone | 会考历史 | PASS | PASS | `content.stem/answer/explanation` 角色声明 |
| B composite | 会考历史 U51+ | PASS | PASS | `shared_components.material` |
| C multi-question | 会考地理 U1-2 等 | PASS | PASS | **仅 1 个 sub_question**（结构翻译） |
| D material | 会考历史/地理 | PASS | PASS | material span 生成 |
| E 不同 question type | single_choice 等 | PASS | PASS | QT 透传 |
| F 结构复杂/flagged | 会考地理 answer table | PASS | PASS | flags 保留于 IR 面 |
| 噪声 andalone | 合格考化学 | **FAIL** | **FAIL** | `UNKNOWN_UNIT_TYPE` fail-loud（预期安全行为） |

`OBSERVED` payload 形状（70）：`document_metadata_claims`, `sections`, `semantic_units`, `producer_boundary`  
`producer_boundary` 携带 OD-2 授权与 `unit_normalizations`（legacy 值保留）。

### 15.2 与 X2.7 全量 probe 的一致性

`OBSERVED` X2.7 B2 secondary（提供 batch resolver IR）与本 probe 对齐：

- M5 PASS **71**
- annotation 成功 **70** / 失败 **1**（`andalone_question`）
- 本 probe spans 4898 vs X2.7 4854（X2.7 在 DB 事务中构造 ResolvedRun，略有对象化差异；均为 0 unresolved）

`OBSERVED` 本 probe **未**跑 IRBuilder/Compiler/Gate（无 DB）。X2.7 已证明该段：

- IR produced 70 / root_units 1630
- compiler leaves **533** / materials 178
- gate candidates **533** 全 `pending_review`（`not strict-auto (grammar None)`）
- skipped_not_ready **1097**（与 options 未 per-label 声明高度相关）

### 15.3 阶段判定表（综合）

```text
Producer artifact            PASS (71 identity + line anchors)
  ↓ minimal deterministic adaptation (boundary + adapters)
Canonical representation     PASS 70 / FAIL 1 (andonline)
  ↓ V3 IR                     PASS 70 (X2.7) ; 1630 root units
  ↓ Compiler                  PASS (533 leaves) ; 1097 incomplete/skip
  ↓ Gate                      REACHED 533 ; auto_approve 0 ; pending_review 533
  ↓ Candidate                 PASS 533 AdmissionCandidate
  ↓ Admission approve/reject  NOT REACHED on B2 entry (by design; lives on runner.py / API)
```

| 失败点 | expected | actual | 缺失/错配 |
|---|---|---|---|
| andalone unit | canonical UT | `UNKNOWN_UNIT_TYPE` | Producer 词表噪声；安全拒绝正确 |
| 85 v1 manifests | `source_content_sha256` | 缺失 | **PRODUCER identity GAP** |
| 无 batch IR 时 | semantic AVAILABLE | `ir_absent` → PENDING | **artifact 分发/路径 GAP**（非代码 bug） |
| choice options | per-label spans | 仅 `options_lines` 整块 | **PRODUCER evidence granularity GAP** → incomplete |
| multi-q sub | 子题列表 | 单 sub + `producer_region_as_single_sub` | **PRODUCER decomposition GAP** |
| Gate auto_approve | question_type grammar | `grammar None` | **CONSUMER canonical QT GAP** |

`CONCLUSION`（回答 Q6 的工程面）：

> 在 **71 ADMITTED** 上，**理论上和实际代码上已经可以**被 V3 消费到 Candidate。  
> 阻断正式集成的**不是“缺一个 Adapter 文件”**，而是：  
> 1) 两个 runner 边界深度不一致；  
> 2) identity 字段覆盖（79 v1）与 batch IR 分发；  
> 3) 证据粒度（option label / sub-question）与 QT grammar；  
> 4) `mapping_registry` / flags / basis 未接入治理化生产路径。

---

## 16. Blocker classification

| Blocker | 类别 | 证据 |
|---|---|---|
| 79 manifests 无 `source_content_sha256` | `IDENTITY / GOVERNANCE` + Producer 数据 | M1 `manifest_sha_missing` ×85（含 tests/data 混入） |
| 默认路径无 batch resolver IR | `C environment / missing artifact` | X2.7 NEW-F2；唯一 IR 为 r52 实验产物 |
| 16 QC_FAIL / semantic pending | Producer 质量 | disposition `REJECTED_QC_FAIL` |
| `andalone_question` | Producer 词表噪声 + 治理 fail-loud | 1 unit / 1 doc 拒收 |
| options 无 per-label span | `PRODUCER GAP` | adapter `OPTION_LABEL_SPAN_UNAVAILABLE` |
| sub-question 不分解 | `PRODUCER GAP` | `SUB_QUESTION_DECOMPOSITION_UNAVAILABLE` |
| Gate `grammar None` | `CANONICALIZATION / CONSUMER GAP` | NEW-F3 |
| runner.py 缺 M1–M5 | `IDENTITY / GOVERNANCE` 流程缺口 | NEW-F1 |
| flags/basis 不进 Gate | `CONSUMER GAP` | 字段存在但无策略消费 |
| mapping_registry 未接线 | `CANONICALIZATION` 实施缺口 | P1–P13 OPEN |

---

## 17. Historical runner assessment

`OBSERVED`：

| 入口 | 位置 | 是否当前正式生产 | 是否被正式 API/Task 调用 | 与 B2 / M1–M5 关系 |
|---|---|---|---|---|
| `scripts/preprocessing_consumer/runner.py` | v3 scripts | **否**（Phase 0 harness） | 否 | **无 M1–M5**；却可进 production GateService → NEW-F1 风险 |
| `scripts/preprocessing_consumer/runner_b2.py` | v3 scripts | **否**（Phase 0.2 harness） | 否 | **完整 M1–M5 + Scope**；IR→Compiler→Candidate |
| `scripts/preprocessing_consumer/runner_b3.py` | v3 scripts | 否 | 否 | 同族实验 |
| `scripts/gate_b/*` | v3 scripts | 否 | 否 | Gate B 对抗/测量 |
| `app/domains/task/executor.py` + API | v3 app | **是** | Worker / API | 生产 LLM Annotation 路径 |
| Papers `resolver_reference.py` | Papers scripts | **否**（明确不进生产） | 否 | 产出 r52 IR，供审计与 secondary probe |
| Papers `r4x–r6x_*` / phase 实验 | Papers scripts | 否 | 否 | 历史审计/攻击/修复 |

`CONCLUSION`：**不得**把 Phase 0/V1 runner 或 resolver_reference 当作当前正式 V3 生产架构。它们是集成验证与历史实验层；正式架构是 TaskExecutor + GateService 链。

---

## 18. Responsibility boundary

```text
                    ┌────────────────────────────┐
                    │ Original Document          │
                    │ PDF/DOC + OCR Markdown     │
                    └─────────────┬──────────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │ Preprocessing (Papers)     │
                    │ 负责：                      │
                    │  · OCR→MD / reslice        │
                    │  · question/unit 切分事实   │
                    │  · stem/options/answer/    │
                    │    explanation/material 行号│
                    │  · printed_number+basis    │
                    │  · unit_type / QT 标签      │
                    │  · flags / QC disposition  │
                    │  · source_content_sha256   │
                    │  · (参考) resolver_ir       │
                    │ 不负责：语义权威/入库/去重   │
                    └─────────────┬──────────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │ Canonical Boundary         │
                    │ 已有雏形：                  │
                    │  · Interface Scope (v2)    │
                    │  · OD-2 unit_type 映射      │
                    │  · M1–M5 identity AND      │
                    │  · annotation_adapter /    │
                    │    resolved_span_adapter   │
                    │ 缺：                        │
                    │  · 全 runner 统一强制        │
                    │  · QT canonical 闭集        │
                    │  · option label / sub-q    │
                    │    证据粒度契约             │
                    │  · flags/basis 消费策略     │
                    │  · batch IR 分发规范        │
                    └─────────────┬──────────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │ V3                         │
                    │ 负责：                      │
                    │  · raw bytes 再验证 (M*)     │
                    │  · ResolvedSpan/IR/Compiler│
                    │  · Gate policy / binding   │
                    │  · Evidence authority      │
                    │  · Question dedup / A 域   │
                    │  · Admission 事务物化       │
                    │ 不负责：OCR/题目发现         │
                    └─────────────┬──────────────┘
                                  ↓
                    ┌────────────────────────────┐
                    │ Admission / DB             │
                    │ Question / Instance /      │
                    │ role_contents / materials  │
                    │ validation_events          │
                    └────────────────────────────┘
```

---

## 19. What is actually missing

### A. Preprocessing 已经可靠完成的能力

1. OCR/Markdown 文档事实载体（源文件 + 行）
2. question / unit 边界的行区间抽取（stem/options/answer/explanation/material/questions）
3. composite material 关联（`material_ref` → `materials`）
4. 印刷题号与 basis 证据字段（含 UNKNOWN 保留）
5. unit_type 两值分类（+ 显式拒绝非法值的潜力）
6. question type 粗分类（12 值）
7. source bytes SHA256（v2 face）
8. QC verdict / ADMITTED / QC_FAIL / V1 Reject 分层
9. flags（answer table / number mismatch）诚实登记
10. 逐 unit provenance（source_file / source_version / source_lines / extraction_method）

### B. Preprocessing 尚未完成的能力

1. 79 份 v1 manifest 的 identity 字段（`source_content_sha256` / `identity_version`）
2. options per-label span（A/B/C/D…）
3. composite 子题真分解（（1）（2）（3）→ sub_questions）
4. 答案表题号→答案稳定解析（502 unresolved）
5. 16 份 QC_FAIL 的语义修复
6. `andalone_question` 清理（或显式 UNKNOWN 隔离产物）
7. 41 处 material/questions 区间折叠的重切
8. 596 unit 的 printed_number provenance（仍为 unknown）
9. 可持续的 batch resolver IR 发布（当前仅 r52 实验快照）
10. question_type 的规范化建议集（不单是模型标签）

### C. V3 已经具备、可以直接复用的能力

1. M1–M5 + Interface Scope 消费闸门
2. `normalize_unit_type`（OD-2 两条映射，fail-loud）
3. annotation payload / ResolvedSpan 适配器（scripts 层）
4. IRBuilder（ready/incomplete/unknown）
5. Compiler（只切片不猜）
6. Gate binding/grammar/payload/policy
7. Admission 事务物化 + Question dedup
8. Evidence ValidationEvent 权威模型
9. Seal / source line index / raw bytes identity

### D. V3 当前重复实现的能力

1. 在 preprocessing 已给精确行号时，SourceResolver 搜索定位（集成路径已 SKIP；生产 LLM 路径仍需要）
2. unit_type 词表判定（`mapping_registry` scaffold vs `boundary.normalize_unit_type`）——治理表与运行时表并存
3. 若未来再对 preprocessing 的 QT 做“再分类”，将与 Producer 标签重复（当前正确地 verbatim 透传）

### E. Producer → V3 之间真正缺失的能力

1. **统一 Consumer Boundary 强制**（所有入口 AND：Scope + M1–M5）
2. **证据粒度契约**（option label spans、sub-question spans）
3. **batch IR / 语义证据的发布与路径约定**（消掉默认 `ir_absent`）
4. **flags / basis / answer_evidence 的消费策略**（进 Gate 或进 review 队列）
5. **QT grammar 映射**（打开 auto_approve 或明确永不 auto）
6. **Admission 完整闭环入口**（B2 只建 candidate；approve 路径需受同一边界保护）

### F. 只是 vocabulary / schema canonicalization 的问题

1. `standalone_question` → `standalone_unit`
2. `composite_question` → `composite_unit`
3. `original_question_type` 12 值 → 是否建立 canonical QT 闭集（含 `true_false`/`listening` 等在全量出现值）
4. line span 形态：manifest `[a,b]` → V3 `line_refs` / `P1Lxxx`（adapter 已做）

### G. 只是 identity / governance / safety 的问题

1. v1 → 必须拒绝或走 Migration Gate，不得 silent upgrade
2. `source_content_sha256` 必须与 raw bytes 一致（消费侧重算）
3. `identity_version` 非标量拒绝（已在 HEAD 提交）
4. `andalone_question` fail-loud（OD-1 migrate-as-UNKNOWN）
5. M5：VERIFIED + PENDING = BLOCK
6. runner 入口深度一致（NEW-F1）
7. mapping 事件 id 与 Owner decision 绑定

### H. 真正需要继续开发的 production code

1. 将 `preprocessing_consumer` 边界从 scripts **升格/注入**正式入口（或明确其永远为旁路并加硬阻断）
2. 统一 M1–M5 到所有 ingest 入口
3. QT grammar / Gate auto 策略实现或废止声明
4. option-label / sub-question 证据消费（依赖 Producer 增强或显式 incomplete 策略）
5. flags/basis 进入 review/policy
6. `mapping_registry` 接线或删除，消除双表
7. batch IR 作为正式 artifact 的加载协议（路径、hash、版本）

---

## 20. Evidence-backed conclusions (Q1–Q8)

### Q1 — Preprocessing 是否已承担主要 document understanding / question extraction / structural fact discovery？

`OBSERVED`：manifest + 源行号 + IR provenance 覆盖 unit/question/material/answer/explanation 全链路事实。  
`CONCLUSION`：**是（structural fact discovery 主体在 Preprocessing）。**  
语义理解（题意、知识点、答案正确性）**不在**其可靠完成范围。

### Q2 — 产出是否比“简单 metadata”丰富？

`OBSERVED`：逐 role 行区间、材料注册表、flags、basis 证据、source SHA、QC disposition、答案表尝试。  
`CONCLUSION`：**是，显著更丰富。** 但仍缺 option-label / sub-question 粒度。

### Q3 — ADMITTED population 实际准确性如何？

`OBSERVED`：87/71/16/1 本地重算与历史一致；71/71 SHA 与行锚点通过；边界质量存在 41 折叠区、54 multi-q 缺号、答案表 502 unresolved、596 unverified。  
`CONCLUSION`：

- **Population 计数：准确。**
- **Structural accuracy：高。**
- **Semantic completeness：中低（有 flag/UNKNOWN）。**
- **不得**表述为“71 个全部语义正确”。

### Q4 — 是否具备足够 source evidence / provenance 使 V3 可安全消费？

`OBSERVED`：structural 证据闭环；596 unit 无 printed provenance；flags 未进 Gate。  
`CONCLUSION`：**可以安全消费 structural input + 显式 gap；不可把全部语义字段当已验证。**  
安全条件 = M1–M5 + Scope 通过 + 显式 incomplete/flag 策略。

### Q5 — Annotation / Resolver / IRBuilder 链条哪些仍必要？

| 组件 | preprocessing 直供路径 | 生产 LLM 路径 | 结论 |
|---|---|---|---|
| Annotation（LLM） | 可被 adapter 替代其“发现” | **必要** | 保留 |
| Resolver | 搜索段可跳过 | **必要** | **保留**（fail-closed 语义） |
| ResolvedSpan | adapter 直构 | 必要 | 保留 |
| IRBuilder | **必要**（ready/incomplete/unknown） | 必要 | **保留** |
| Compiler | **必要** | 必要 | **保留** |
| Gate/Admission | **必要** | 必要 | **保留** |

### Q6 — 只缺 Adapter，还是更深缺口？

`OBSERVED`：适配器**已存在**（scripts）；71 可进 Candidate。  
`CONCLUSION`：**不是“只缺一个 Adapter 文件”。**  
存在更深缺口：入口治理不一致、身份覆盖、证据粒度、QT grammar、flags/basis 消费、mapping 接线、IR 分发。Adapter 是其中最小的一块。

### Q7 — M1–M5 是重复语义还是必要 identity/integrity/governance？

`CONCLUSION`：**必要的 identity / integrity / governance。** 全部 **RETAIN**；需 **ADAPT** 为全入口强制。  
与 Preprocessing 的关系是**声明/证据 vs 复核/门禁**，不是重复语义识别。

### Q8 — Preprocessing → Canonical Interface → V3 → Admission 是否合理系统边界？

`DERIVED`（基于 §4–§15 全部证据，而非直觉）：

1. 事实发现确已前移到 Preprocessing（Q1/Q2）。
2. 消费侧仍必须保留 identity 复核、fail-closed 装配、Gate/Admission 治理（Q4/Q7）。
3. 中间 Canonical Boundary 已有真实代码与授权映射（OD-2、Scope、M*），不是空想。
4. Feasibility probe 证明该边界在 71 上**可运行到 Candidate**。

`CONCLUSION`：**该四层划分与当前证据一致，可以作为合理系统边界候选。**  
**前提条件**（缺一不可）：

- Canonical Boundary 成为**唯一**强制入口（消 NEW-F1）；
- 证据粒度与 QT/flags 策略被显式契约化；
- 未知值走 UNKNOWN/Admission，不 silent repair；
- Owner 仍需决定是否进入正式集成设计——本报告不代做该决策。

---

## 21. Unresolved questions

1. 79 份 v1 是否走 Migration Gate 回填 identity，还是永久排除 Interface Scope？
2. 16 份 QC_FAIL 的修复责任在 Producer 重切/重标，还是 Consumer 降级消费？
3. options per-label / sub-question 分解由 Producer 升级提供，还是 Consumer 接受 incomplete + 人工补全？
4. `original_question_type` 是否建立 canonical 闭集；`true_false`/`listening` 等全量值如何处置？
5. Gate `grammar None` 是实现缺口还是有意永不 auto_approve？
6. `mapping_registry` 是接线为唯一权威，还是删除以免双表？
7. batch `resolver_ir` 是否升格为正式 versioned artifact（而非 r52 实验快照）？
8. `flags`/`basis`/`answer_evidence` 是否进入 Gate policy，还是仅进入 review UI？
9. `runner.py`（无 M1–M5）应删除、加硬阻断，还是对齐 B2？
10. AITutor-X 的 X2.x governance 文档与 V3 `mapping_registry` 事件 id 的交叉绑定（F-05-A）由谁最终裁定？

---

## 22. Recommended next engineering step

`DERIVED`（排序即建议，不代替 Owner 批准）：

1. **治理入口统一**：所有 preprocessing→V3 runner 强制 `Interface Scope ∧ M1–M5`（修 NEW-F1）。
2. **身份覆盖**：对 Interface 外 v1 明确 Migration Gate 或排除策略；禁止 silent backfill。
3. **证据契约 v0.3**：写清 option-label / sub-question / answer-table 的粒度要求与 incomplete 语义。
4. **QT grammar 决策**：实现映射并接 Gate，或书面废止 auto_approve。
5. **再跑全量 probe**（172 或收紧后的 corpus）作为进入正式集成设计的门禁证据。

---

## 23. Audit method & artifacts

- 三仓 git 只读盘点（branch/HEAD/status/remote/ahead-behind）
- Papers 全量 manifest/IR schema 解析与 population 重算
- 71 ADMITTED 全量 SHA256 与 source_lines 锚定校验
- 分层结构不变量（composite/multi-q/answer numbering/evidence closure）
- V3 call graph 以 imports/docstring/入口脚本为准
- 独立 feasibility probe（真实 adapter，无 DB，无生产代码修改）
- 交叉核对 X2.7 `30-analysis.json` / FULL-RUN 报告（作为已有 run 的 OBSERVED 对照）

临时脚本目录：`D:\Project\AITutor-X\_tmp_audit\`（任务结束前删除）。

---

## 24. Workspace hygiene

本审计：

- **未修改**任何 production code / Frozen Spec / Contract / vocabulary / DB schema
- **未执行** migration / governance 变更
- **仅**新增本报告与临时只读脚本（删除前）

结束前将再次执行 `git status --short` 确认仅剩本报告。

---

*End of independent verification report.*
