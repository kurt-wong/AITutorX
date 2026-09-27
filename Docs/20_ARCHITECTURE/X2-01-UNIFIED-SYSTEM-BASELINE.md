# X2-01 — Unified System Baseline

> **[CLOSED 2026-09-27]** 本文件的生命周期已结束（阶段完成）。**正文保持原样不改写**（DOC-GOV §7）。
> 保留在主视野：其内容仍具参考价值。当前状态见 [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../50_OPERATIONS/CURRENT_STATE.md)。


**Document ID**: X2-01
**Task**: TASK-X2-CLAUDE
**Document Type**: Architecture / System Baseline
**Status**: `CLOSED`（原状态：`ACTIVE — X2 AUDIT BASELINE`）
**Date**: 2026-09-18
**Upstream**: `X2-00-STATE.md`；GF v0.2；三仓 Git FACT @ X2-00 §1
**Decision actor**: Owner；本文为审计登记，非迁移授权
**Hard rule**: Unified Baseline ≠ Migration Authorization

---

## 1. Target System（唯一目标）

```text
AITutorX（目标系统）
├── preprocessing/     ← Producer 能力域（历史来源: Aitutors-preprocessing / Papers）
├── backend/           ← Consumer Semantic/Question 能力域（历史来源: AITutors-v3）
├── frontend/          ← Consumer 展示能力域（历史来源: AITutors-v3/frontend）
├── tools/             ← 工具链（audit / migration scripts 等，待 Gate）
├── archive/           ← 历史资产（非 active tree）
└── Docs/              ← Unified Docs（00/10/20/30/40/50/60/90）
```

`[FACT]` 当前 AITutorX 代码目录均为 `.gitkeep` 空骨架；**无生产代码已迁入**。

`[FACT]` V3 与 preprocessing 从本阶段起被视为 **AITutorX 的历史来源 + 内部职责域**，不是两个最终独立项目。

---

## 2. Unified System Lifecycle（阶段模型）

`[PROPOSAL]`（统一生命周期模型；实现映射见 §3 表）:

```text
Source (raw exam PDF / DOCX / ...)
  ↓
Preprocessing (OCR / source repair / LLM re-slice / QC)
  ↓
Source Identity / Version (source_content_sha256 = SHA256(raw bytes))
  ↓
Semantic Annotation (LLM claims + Semantic Reference)
  ↓
Resolver (Semantic Reference → Resolved Span)
  ↓
IR (Semantic Question IR)
  ↓
Compiler (Deterministic Compiler → compiled roles)
  ↓
Gate (Structural / Provenance / Semantic / Admission)
  ↓
Admission (Transaction → A-domain)
  ↓
Question (canonical domain entity)
  ↓
QuestionInstance / Material / Knowledge
```

**角色裁决（与 GF / Contract / V3_SPEC 对齐）**:

| Stage | Capability domain | 责任一句话 |
|-------|-------------------|------------|
| Source intake | Producer + Storage | 原件进入；path ≠ identity |
| Preprocessing | **Producer** | 「原文有什么、在哪里」 |
| Source Identity/Version | **Boundary / Contract** | 内容 hash 决定身份；path 仅 locator |
| Semantic Annotation | **Consumer** | LLM 语义 claim；无 Admission Authority |
| Resolver | **Consumer** | 确定性解析位置 |
| IR | **Consumer**（Producer 产出 Semantic Evidence / IR artifact） | 语义中间表示；IR ≠ Question |
| Compiler | **Consumer** | 确定性编译正文 |
| Gate | **Consumer** | Admission Authority 属 Gate Policy |
| Admission | **Consumer** | 唯一物化 Question 的通道 |
| Question / Instance / Material / Knowledge | **Consumer domain model** | 业务实体 |

`[FACT]` preprocessing 自我定位（`prd.md` + `governance/phase_p2_charter.md` §12）: **Source Evidence Producer**；不负责 V3 语义/准入职责。

`[FACT]` V3 自我定位（`V3_SPEC/00_Master_Spec.md` P1–P7）: Source 唯一事实源；LLM 无 Admission Authority；Question 是可重放编译结果。

`[FACT]` 「原文有什么/在哪里 vs 意味着什么/能否入库」= Owner 已裁边界；X2 不重开该定位。

---

## 3. Lifecycle Traceability Table（阶段 × 来源 × 文档 × 代码 × Contract × 证据）

Legend: `H`=historical source repo；`C`=current authority claim；`U`=authority unknown；`X`=conflict；`T`=has test evidence

| Stage | Source repo / path | Docs（权威） | Code（现行） | Contract | Historical | Current | Authority unknown | Conflicts | Test evidence |
|-------|--------------------|--------------|--------------|----------|------------|---------|-------------------|-----------|---------------|
| **Source intake** | Papers `maintainess/PDF`（operational）+ `original/`（RSD 候选） | REPORT-K；GF-001；OD-04 | `ocr_service/batch_convert_pdf.py:55` 硬编码 `maintainess\PDF` | OD-04 Hash-based Source Identity | 双树均历史输入 | 双树均为输入来源（OD-04 不排序） | 双树血缘方向；canonical 不指定 | 文档曾将 12,707 系于 `original/`（实测=maintainess/PDF）；OQ-GF-011 | 历史日志；恢复后盘点；**非**全量 hash 台账 |
| **Preprocessing / OCR** | Papers `Ocr-markdown/`；`ocr_service/` | `prd.md` 冻结规格；`governance/rule_registry.md` | `batch_convert_pdf.py` / `ocr_watchdog.py` / `output_manifest.py`；PaddleOCR-VL | prd 数据契约 §4 | v1/v2 流水线教训 | Producer Evidence 流水线 | OCR 产物覆盖 vs 清单 1801 vs manifest 166 | lineage 覆盖 PARTIAL（OQ-GF-007） | `tests/` pytest；QC C1–C10；**测试基线冲突未消**（OQ-GF-018） |
| **Source repair** | Papers `Ocr-markdown` + scripts | prd §3.3 脚本索引 | `fix_bare_latex.py` / `recover_images.py` / `corpus_scan.py` / `pdf_fidelity.py` | prd 保真原则「去锚点==源原文」 | 历史 BUG 修复轮 | 确定性修复 + 可回滚 | 修复轮与 IR 血统关系细节 | D-048-3 数据文件删除恢复事件 vs maintainess 误删 = 非同一事件 | `test_fix_*` / integrity gate |
| **Source Identity** | 两侧 | Contract v0.2 §0.1①；DEC-030/031；OD-04 | Producer: IR/manifest 字段；V3: `core/raw_bytes_identity.py` 等 M1–M5 | **FROZEN**: `source_content_sha256` = SHA256(raw bytes) 64 hex；path 非身份 | 历史 `source_sha256` / `source_version_id` 词面 | 接口键已裁 | D3 M3 内部字段名；bytes 传输 HOW（OQ-12″） | Contract 双名域；V3 内部 `source_version_id`=UUID ≠ 跨系统 sha | Producer Step1/2 验证 PASS；V3 消费验证 **NOT IMPLEMENTED** |
| **Semantic Annotation** | V3 `domains/annotation`；Producer LLM re-slice 为 **Evidence annotation** | V3 `20_Document_Pipeline` §4；prd §3 | V3 `annotation/service.py`；Papers `reslice_pipeline.py` | V3 Annotation schema v0.3；Producer manifest v2 | V2 L2 Annotation Mirror = legacy | 两侧 annotation **职责不同**（Evidence vs Semantic claim） | Producer annotation 如何映射进 V3 Semantic Annotation = 未完整定义 | 词表/字段同名异义风险 | V3 annotation tests；Papers reslice QC |
| **Manifest (Producer)** | Papers `Ocr-markdown/**/*.manifest.json` | prd §4.2；Contract §1 | `reslice_pipeline.py` 三产出；interface_scope step1/2 | Contract: Manifest = Source Identity Authority | 166 manifests；87 接口面 | 87/87 回填 `source_content_sha256`（Step2） | 16 Semantic Pending 呈现机制（OQ-21） | REPORT-B 曾列不存在的 L1 Spec 文件名（X2 对账 CONFLICT） | Step1 snapshot + Step2 report + freeze evidence |
| **OCR Artifact** | Papers `Ocr-markdown/` | GF-001 OCRA role；REPORT-K | OCR md + `_imgs/` | OD-05 NAS-backed read-only（模式已裁） | 大体量不在 git | 操作事实层 | 全量 lineage 清单 | 覆盖缺口叙事 | manifest 部分覆盖 |
| **Resolver** | V3 `domains/resolver` | V3 `20` §5；Papers `resolver_contract_design.md` | `resolver.py` | Path A Native / Path B Adapter（V3 91 登记制） | V2 anchor correction = legacy | Production Resolver | options_region 未进生产（FACT-005/009） | options_region 设计 vs 生产零概念 | consumer-report-b2/b3；sampling |
| **IR** | Producer IR artifact + V3 transient Semantic IR | Contract；V3 `20` §6 | Producer: `data/resolver_ref_r52/resolver_ir.json`；V3: compile/ir | Contract IR = Semantic Consumption Authority；V3 IR transient → candidate payload | resolver-ir-0.1 | 71 ADMITTED units | D3 字段名；16 pending IR 再生成批次 | 「IR 71」≠「Interface 87」；禁 IR=Interface | 71/71 hash 对账；V3 IR 消费能力 NOT IMPLEMENTED |
| **Compiler** | V3 `domains/compile` | V3 `20` §7；`10` schema | `compiler.py` / `identity_normalization.py` / `snapshot.py` | Deterministic；P7 Replayability | V2 pipeline patches = forbidden pattern | 确定性编译 | 与 Producer IR 字段映射细节 | — | compile domain tests |
| **Gate** | V3 `domains/gate` | V3 `20` §8；`10` decision_status；EB-008 | `admission.py`；evidence promotion | EB-008 frozen constraints；Gate Policy = Admission Authority | V2 Quality/Admission Gate legacy | 分层 Gate | REPORT-I Gate 版本谁批准（F5） | FACT-012: 4/4 attack 曾 bypass Admission（历史 observed）；EB-008 外部验证 pending | gate tests；p32 enforcement results |
| **Admission** | V3 A-domain tables | V3 `10` §5.4 | repositories + admission transaction | Candidate = 唯一通道 | — | 架构冻结 | 迁移后 Gate/Admission 等价声明（OQ-GF-018） | silent skip for non-ready（REPORT-F GAP-004） | DB tests（环境依赖） |
| **Question** | V3 A-domain | V3 `10` §6；DICTIONARY | models/repositories | Source-derived；P3 | V1/V2 Question Aggregate 产品概念 | canonical entity after Admission | 迁移映射未执行 | provenance ≠ quality | schema tests |
| **QuestionInstance** | V3 A-domain | V3 `10` §6.2 | question_instances | occurrence in source | — | 与 Question 身份分离 | 与 Producer unit_id 关系（display alias 禁作键） | unit_id 可重复（汇编卷） | schema tests |
| **Material** | V3 materials / source_figures；Producer material/extra | V3 `10` §4.4/§6；prd §2.3 | materials / material_links / source_figures；`recover_images.py` | Material **可含题图/配图/图表/外部材料**；single question 亦可有 Material | V2 图片链路教训 | 领域模型已定义 | 图片恢复 Step5 未执行；dangling refs | FACT-034: figure dangling refs 大量存在 | figure_id 约束测试 |
| **Knowledge** | V3 knowledge_nodes | DICTIONARY Knowledge Tree | question_knowledge_links | AI 只能映射，不能随意创建节点 | — | schema 存在 | 何时/由谁建立关联 = 业务流程未在本阶段验证 | mapping_source/review_status 词表 | — |
| **Admission Evidence / Authority** | V3 validation_events | DEC 87–92 EB-008 | evidence/ domain | EB-008 Identity Model frozen | — | Implementation completed（V3 叙事） | External verification pending；NOT DSH approved | EB-008 状态跨仓表述差 | p32 results；external verification unavailable in repo |
| **Coordination / Governance** | AITutorX + 两仓账本 | GF v0.2；X2-00~10；两仓 CURRENT/state | N/A（docs） | AGENTS.md 五原则；OD-* | 两仓独立 Docs | **统一 Docs 目标** | Ledger canonical 归属（Papers vs AITutorX） | V3 CURRENT mirror 落后于 Papers DEC-049 | N/A |

---

## 4. What is Historical / Current / Unknown / Conflicting

### 4.1 Historical（保留，不删除）

- V1/V2 项目与 lessons（`V1_LESSONS.md`；`docs_archive/`）
- V3 `docs_archive/` 多日期归档
- Papers `_archive/`、旧 auto-annotated 版本、旧 QA 脚本
- legacy 状态词与 V2 pipeline 模式（V3 DICTIONARY 已标 legacy）
- untracked 过程文档（authority unknown，但**存在事实**登记）

### 4.2 Current（现行权威主张，仍可能未执行）

- GF v0.2 Frozen Governance Baseline
- Contract v0.2 Freeze Object（内容权威）
- V3_SPEC 00/10/20/30/40/50 + 90/91 L0-META
- OD-01/03/04/05/06/10/14/18（AITutorX Owner Decisions）
- preprocessing `prd.md` 冻结规格 + P2 charter §12 定位重校准
- 双状态词表：`{ready,incomplete,unknown}` + `{pending_review,approved,rejected}`

### 4.3 Authority Unknown（必须保留为 reviewable）

- 全部 untracked 文档（V3 9+4；部分 Papers 过程件）
- Observation Set B
- REPORT-G/H/I/K admitted 状态
- 双树数据血缘方向、恢复完整性证据标准
- 测试基线 canonical（冲突未裁）
- Design v1.1 接口权威
- bytes 传输方案
- V3 消费端五项能力实现状态的「可迁移完成度」

### 4.4 Conflicts（登记，不猜答案）

| ID | Conflict | Evidence |
|----|----------|----------|
| C-X2-01 | Contract 状态叙事：账本 FROZEN vs 正文 DRAFT/NOT FROZEN | V3 CURRENT vs Contract 文首 |
| C-X2-02 | REPORT-B 所列多份 “L1 Finalization/Spec tracked” 文件在 GitHub **不存在** | `gh contents` 仅 9 tracked Contracts |
| C-X2-03 | Authority Taxonomy 至少三套（AITutorX README L0–L7 / V3 90 L0–L5 / REPORT-B 自用） | README；V3 90；REPORT-B |
| C-X2-04 | DEC 双轨撞号（V3 vs DSH；021/022/023 等） | 两仓 CURRENT；REPORT-C 未被采用 |
| C-X2-05 | 测试基线叙事冲突（REPORT-A V3 1780 passed vs Papers canonical 338/1 vs REPORT-I F9 337+1failed） | 各报告；OQ-GF-018 |
| C-X2-06 | Producer IR 字段 `source_sha256` vs Contract 接口键 `source_content_sha256` | Contract 允许双名域；AITutorX 数据字典待裁 |
| C-X2-07 | 12,707 PDF 归属文档错误（写 original 实为 maintainess/PDF） | REPORT-K；OQ-GF-011 |
| C-X2-08 | options_region 设计存在 vs V3 生产 Resolver 零概念 | FACT-005/009 |
| C-X2-09 | 四状态机表达缺口：semantic 非 ready 单元无法进入 decision pending_review | FACT-039/045 |
| C-X2-10 | Papers `state.yaml` canonical vs AITutorX 尚无协调账本 | state.yaml 头注释 |

---

## 5. Provenance ≠ Quality Authority（统一原则，重申）

```text
V1 / V2 / V3 / preprocessing 来源版本
    ≠
Question 质量权威
```

Question 最终质量取决于: source facts + processing + semantic interpretation + validation + review evidence。

`[FACT]` 来源: AITutorX `AGENTS.md` 原则 1；GF 治理纪律；本阶段不修改该原则。

---

## 6. UNKNOWN Retention Rule

```text
AI / Agent 无法可靠理解 → UNKNOWN
UNKNOWN → reviewable state
UNKNOWN ≠ discard
UNKNOWN ≠ default accept
UNKNOWN ≠ silent skip / fallback / convert
```

`[FACT]` Contract 冻结项 ③: unknown → reviewable record → pending_review；三禁令仍 binding。

---

## 7. Baseline Non-Claims

本文 **不**声明:
- 任一阶段已 Migration Authorized
- 任一资产 admitted
- 任一 OQ/BL/D-048 closed
- 统一架构已实现
- 两仓代码已合并

---

*Unified System Baseline registered. Migration remains UNAUTHORIZED.*
