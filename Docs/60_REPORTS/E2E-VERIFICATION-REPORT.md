# E2E-VERIFICATION-REPORT

**任务**：AITutors-v3 + AITutors-preprocessing 全流程 End-to-End Validation
**执行日期**：2026-09-25
**执行环境**：Windows 11 Pro / Git Bash / Python 3.12.9 / Node v24.13.0 / Docker 29.7.2
**证据目录**：`D:\Project\AITutor-X\e2e_run\`

> **证据标准声明**：本报告所有结论均附 `command` / `commit` / `input fixture` / `execution timestamp` / `result` / `database evidence`。凡无法以运行结果证明的，一律标 `NOT TESTED` 或 `NOT IMPLEMENTED`，不使用 "looks good / basically works / ready / complete" 一类不可复核措辞。

---

## §1 Repository Baseline

### 1.1 AITutor-X（治理工作区）

| 项 | 值 |
|---|---|
| HEAD | `e238dcb7552235854bc294b24d91b27987f9f676` |
| branch | `main` |
| origin/main | `e238dcb7552235854bc294b24d91b27987f9f676`（与 HEAD 一致） |
| working tree | 18 个 untracked 报告文件 + `contract_check.bin` + `index.html`；无 modified |
| 代码状态 | `backend/`、`preprocessing/`、`tools/` **均为空目录（仅 `.gitkeep`）** |

### 1.2 AITutors-v3

| 项 | 值 |
|---|---|
| 路径 | `D:\Project\AITutors-v3` |
| HEAD | `d2b9a26f1a1c0297b4536b273b8999a071433079` |
| branch | **`od01-r3-convergence`**（⚠ 非 `main`） |
| origin/main | `79348441dae0efce6855017b2b5c0491b08d6bb8`（⚠ 与 HEAD **不同**） |
| working tree | 11 个 untracked（`Docs/COORDINATION/CONTRACTS/*`、`Docs/GOVERNANCE/`）；无 modified |
| Docs/V3_SPEC tree hash | `14a7450809d4932036f415d765ab29c53671843c` |
| 实现规模 | `app/` 87 个 `.py`；`tests/` 96 个 `.py`；`scripts/` 9792 行 |

**Frozen Spec SHA256（未修改，本任务全程只读）**：

| 文件 | SHA256 |
|---|---|
| `00_Master_Spec.md` | `c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4` |
| `10_Data_Model.md` | `529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1` |
| `20_Document_Pipeline.md` | `0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c` |
| `30_Task_LLM_Safety.md` | `db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89` |
| `40_Development_Rules.md` | `8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db` |
| `50_Migration_Assets.md` | `8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7` |

**本任务未修改 Frozen Spec 中任何文件、hash、authority、数据模型、阶段定义或 STOP 条件。**

### 1.3 AITutors-preprocessing

```
PREPROCESSING ACCESS = OK   （非 BLOCKED）
```

| 项 | 值 |
|---|---|
| GitHub | `kurt-wong/Aitutors-preprocessing`（private，default branch `main`） |
| 本地工作副本 | `D:\Project\Papers`（remote = 该仓库） |
| HEAD | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` |
| HEAD commit | `2026-09-17T12:16:20Z` "DEC-049: D2/D3/D4 Decision Brief (Evidence First, No Self-Fix)" |
| branch | `main` |
| working tree | **clean**（与 remote 同 SHA） |
| 真实产物根 | `D:\Project\Papers\Ocr-markdown\`（15 个 reslice-* 语料目录 + 学科目录） |

> **基线勘误**：`AITutor-X/preprocessing/` 为空占位目录，**不是** preprocessing 仓库。真实仓库为 `D:\Project\Papers`。另：git HTTPS clone 被代理阻断（`CONNECT tunnel failed, response 404`），已改用 `gh api` tarball 校验远程 HEAD 与本地一致。

### 1.4 依赖与数据库配置

| 项 | 值 |
|---|---|
| Python | 3.12.9 |
| 依赖清单 | `backend/pyproject.toml`（fastapi / sqlalchemy[asyncio] / asyncpg / alembic / pydantic-settings / uvicorn / pymupdf） |
| DATABASE_URL | `postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors` |
| DB 容器 | `aitutor-postgres`（`pgvector/pgvector:pg16`），经 `docker compose up -d postgres` 启动，healthcheck `healthy` |
| 表数量 | **26**（`alembic upgrade head` 已应用） |
| LLM 配置 | `LLM_GATEWAY_MODE=live`，`MIMO_API_KEY`（`<REDACTED>`）/ `MIMO_BASE_URL=https://api.xiaomimimo.com/v1` / `MIMO_MODEL=mimo-x-pro-preview` |

> **环境阻断记录**：任务开始时 Docker Desktop service 为 `STOPPED`（`com.docker.service` STATE=1），PG 5432 连接被拒（WinError 10061）。`net start com.docker.service` 返回 `拒绝访问`（error 5，需管理员）。已通过启动 `Docker Desktop.exe`（GUI）恢复 daemon（29.7.2）后拉起 PG 容器。**这是环境故障（分类 C），不是实现缺陷；已排除后继续执行。**

---

## §2 Implementation Call Graph

**只登记实际存在的代码与调用关系，不按 Frozen Spec 推测。**

### 2.1 Branch P — Preprocessing 侧（真实，独立仓库）

| Stage | Actual module | Actual entry point | Input | Output |
|---|---|---|---|---|
| OCR 转换 | `ocr_service/batch_convert_pdf.py` | CLI | PDF | OCR Markdown |
| OCR 守护 | `ocr_service/ocr_watchdog.py` | 守护进程（需用户手动启动） | watch dir | 批处理 |
| LLM 重切批注 | `scripts/reslice_pipeline.py` | `--pilot/--file/--resume/--recompile` | OCR `.md` | `*.annotated.md` + `*.manifest.json` |
| 重切质检 | `scripts/reslice_qc.py` | CLI | 重切产出 | C1–C10 质检 |
| 图片恢复 | `scripts/recover_images.py` | CLI | PDF | `_imgs/` 配图 |
| 产物清单 | `ocr_service/output_manifest.py` | CLI | 输出目录 | manifest |

### 2.2 Branch C — Preprocessing Consumer（V3 侧集成点）

| Stage | Actual module | Actual entry point | Input | Output |
|---|---|---|---|---|
| manifest 读取 | `scripts/preprocessing_consumer/manifest_reader.py` | `load_manifest` / `find_manifests` | `*.manifest.json` | `Manifest` dataclass（verbatim 保留 identity/provenance） |
| 源行读取 | `scripts/preprocessing_consumer/source_loader.py` | `load_source_lines` | source `.md` | `list[SourceLine]` |
| **Identity 边界** | `runner_b2._verify_identity_boundary` | M1→M5 + Interface Scope | manifest + source + resolver IR | `{gate, identity_state, semantic_state, reason, interface_scope}` |
| 词表归一化 | `scripts/preprocessing_consumer/boundary.py` | `normalize_unit_type` / `enforce_interface_scope` | producer 词表 | canonical Unit Type |
| **Semantic Annotation** | `scripts/preprocessing_consumer/annotation_adapter.py` | `manifest_to_annotation_payload` | `Manifest` | V3 annotation payload（含 `producer_boundary.known_gaps`） |
| **Resolved Span** | `runner_b2._build_resolved_run` | `_make_resolved_span` | manifest + source_lines | `ResolvedRun`（spans + unresolved） |
| **Question IR** | `app/domains/compile/ir.py` | `IRBuilder.build` + `validate_ir` | ResolvedRun + payload | `IR`（含 `semantic_status`） |
| **Compiler** | `app/domains/compile/compiler.py` | `Compiler.compile` | IR + span_map + line_map | `CompiledSnapshot`（leaves + materials） |
| **Gate** | `app/domains/gate/policy.py` | `evaluate` / `build_payload` | root + ir + compiled + resolved_run | `gate_decision` |
| **Candidate** | `app/repositories/snapshot_repository.py` | `create_admission_candidate` | 以上全部 | `AdmissionCandidate` 行 |
| 编排 | `scripts/preprocessing_consumer/runner_b2.py` | `run_corpus` | `--corpus` / `--resolver-ir` | JSON report |
| **Admission** | — | **NOT CALLED** | — | — |
| **Persistence** | — | **`finally: await session.rollback()`** | — | **无** |

### 2.3 Branch W — 生产持久化路径（Worker / TaskExecutor）

| Stage | Actual module | Actual entry point | Input | Output |
|---|---|---|---|---|
| Ingestion | `app/domains/source/import_service.py` | `DocumentImportService.import_file` | file bytes (`.pdf`/`.docx`) | `Document` + `Task(queued)` |
| HTTP Import | `app/api/routers/documents.py:31` | `POST /api/documents/import` | multipart file | `ImportResponse` |
| Worker | `app/worker/__main__.py` | `python -m app.worker run` | queued tasks | — |
| 编排 | `app/domains/task/executor.py` | `TaskExecutor.run_once` | task | 逐 stage |
| **Seal** | `app/domains/source/seal.py` | `SealService.seal_document` | file bytes | `DocumentSourceVersion` + lines + spans + figures |
| **Quality** | `app/domains/source/quality.py` | `SourceQualityGate.evaluate_text` | `body_text` | quality report（invalid / ocr_required / valid） |
| **Annotation** | `app/domains/annotation/service.py` | `AnnotationService.annotate` | prompt + LLM | `SemanticAnnotation` |
| **Compile+Gate+Admission** | `app/domains/gate/service.py` | `GateService.run` | source_version + annotation | Candidate + **AdmissionService.approve/reject** |
| Admission | `app/domains/gate/admission.py` | `AdmissionService.approve/reject` | candidate_id + provenance | **Question / QuestionInstance / Material / UnitGroup** |
| HTTP Admission | `app/api/routers/candidates.py` | `POST /api/candidates/{id}/approve\|reject` | review body | `CandidateDetail` |

### 2.4 关键结构事实：两条分支互不衔接

```
preprocessing (P)  ──产出──▶  *.annotated.md + *.manifest.json
                                   │
                                   ▼
                    runner_b2 (C)  ──读取──▶  IR → Compiler → Gate → Candidate
                                   │
                                   └── finally: session.rollback()   ❌ 永不持久化
                                   └── AdmissionService 从未调用      ❌

PDF/DOCX ──▶ import (W) ──▶ Task ──▶ seal ──▶ quality ──▶ LLM annotate ──▶ GateService ──▶ Admission
                                                                          （自带 LLM 标注，不消费 P 的 manifest）
```

**实证**：`grep -rniE "preprocess|reslice|annotated\.md" app/` 仅在 `app/core/identity_*.py` 的**文档注释**中命中（引用 CONTRACT 设计文档），**无任何运行时 import 或调用** preprocessing 代码。V3 生产路径的 `_annotation_stage` 用 `build_annotation_prompt(version.body_text)` 自行调 LLM，**不读取 preprocessing manifest**。

---

## §3 Existing Test Baseline

**命令**：
```bash
cd D:\Project\AITutors-v3\backend
python -m pytest -q --no-header -p no:cacheprovider
```

**执行时间**：2026-09-25 约 15:00（duration 69.40s）
**commit**：`d2b9a26f1a1c0297b4536b273b8999a071433079`

| 指标 | 值 |
|---|---|
| collected | 2032 |
| **passed** | **2030** |
| **failed** | **0** |
| **skipped** | **1** |
| **xfail** | **1** |
| warnings | 8（alembic `path_separator` DeprecationWarning） |
| duration | 69.40s |

**失败分类**：**无失败**。基线 100% 绿。

**但基线绿 ≠ 系统可跑通** —— 见 §14 DEFECT-001：测试套件会**破坏性清空共享真实数据库**。测试绿与 E2E 可行性是两个独立事实。

---

## §4 Golden Fixture

### 4.1 选型

扫描语料 `D:\Project\Papers\Ocr-markdown\`（166 份 manifest）：

| 语料 | manifest 数 | 说明 |
|---|---|---|
| `reslice-pac-annotated/` | 22 | **identity_version=2**（Interface Scope 成员）✅ |
| `reslice-batch-C/` | 多 | identity_version=2 ✅ |
| `reslice-p2-*` / `resliced-pilot` / `reslice-stress10` 等 | 其余 | identity_version=**None**（会被拒：`MISSING_IDENTITY_VERSION`） |

**选定**：`reslice-pac-annotated\reslice-pac\ocr\pac-c02-01`（单文件同时含 3 组 composite+shared material + 17 个独立单题，规模适中）。

### 4.2 Golden Fixture 身份校验

```bash
cp "D:\Project\Papers\Ocr-markdown\reslice-pac-annotated\reslice-pac\ocr\pac-c02-01.manifest.json" \
   D:\Project\AITutor-X\e2e_run\golden\
```

| 字段 | 值 | 判定 |
|---|---|---|
| manifest | `pac-c02-01.manifest.json` | — |
| source_file | `D:\Project\Papers\Ocr-markdown\reslice-pac\ocr\pac-c02-01.md` | 真实文件存在 |
| `identity_version` | `2` | Interface Scope 内 |
| `source_content_sha256`（声明） | `31086f124389c375f8892505712b839f8a6e02a16bf9bd044998246bb1cd51a7` | — |
| computed SHA256（实算） | `31086f124389c375f8892505712b839f8a6e02a16bf9bd044998246bb1cd51a7` | **MATCH** ✅ |
| source bytes / lines | 22 959 / 508 | — |
| model / prompt_version | `mimo-x-pro-preview` / `reslice-pilot-v2.3` | — |
| units | 20 | — |
| validation_issues / warnings | `[]` / `[]` | 干净 |

### 4.3 单元构成

| unit_id | unit_type | question_numbers | material_lines | questions_lines |
|---|---|---|---|---|
| U1-3 | composite_question | [1,2,3] | **[9,18]** | [9,29] |
| U4-6 | composite_question | [4,5,6] | **[31,33]** | [31,59] |
| U7-9 | composite_question | [7,8,9] | **[61,63]** | [61,99] |
| Q10–Q20 | standalone_question | [10]…[20] | None | None |
| Q21–Q26 | standalone_question | [21]…[26] | None | None |

**语料级决定性结构事实**（全语料 472 个 standalone + 58 个 composite 统计）：

```
('composite_question', 'mat' , 'qspan') -> 55
('composite_question', '-'   , 'qspan') ->  3
('standalone_question', '-'  , '-'    ) -> 472
('standalone_question', 'mat', ...)    ->   0     ← 从未出现
```

> **`standalone_question + material` 在 producer 语料中不存在（472/472 均无 material）。** 因此 §6 中该项无法以真实输入端到端验证，只能验证实现侧支持状态（见 §6.2）。

### 4.4 Resolver IR 产物

`D:\Project\Papers\data\resolver_ref_r52\resolver_ir.json`（11 458 122 bytes，`ir_version: resolver-ir-0.1`，88 个文件条目）

其中 golden fixture 条目：

| 字段 | 值 |
|---|---|
| `disposition` | `ADMITTED` |
| `qc_verdict` | `PASS` |
| `reasons` | `[]` |
| `ir.source_sha256` | `31086f12…cd51a7`（与 source 实算一致 ✅） |
| `ir.materials` | **`['L9-18', 'L31-33', 'L61-63']`** — 3 个共享 material |
| `ir.units` | 20（含 `material_ref` 字段） |

---

## §5 Single Question E2E

### 5.1 E2E-001 — 命令与时间戳

```bash
cd D:\Project\AITutors-v3\backend
python -m scripts.preprocessing_consumer.runner_b2 \
  --corpus "D:/Project/AITutor-X/e2e_run/golden" \
  --output "D:/Project/AITutor-X/e2e_run/golden-report-b2-withIR.json" \
  --resolver-ir "D:/Project/Papers/data/resolver_ref_r52/resolver_ir.json"
```

| 项 | 值 |
|---|---|
| Input | `pac-c02-01.manifest.json` + `pac-c02-01.md` |
| commit | `d2b9a26f1a1c0297b4536b273b8999a071433079` |
| START | `2026-09-25T15:05:35+08:00` |
| END | `2026-09-25T15:05:36+08:00` |
| Pipeline | preprocessing → V3 ingestion → identity → annotation adapter → resolved span → IR → compiler → gate → candidate |
| Expected | 20 Question + 20 QuestionInstance |
| **Actual** | **0 Question + 0 QuestionInstance** |

### 5.2 逐阶段执行证据（中间语义链无跳步证明）

| # | Stage | STATUS | INPUT | OUTPUT | PERSISTENCE |
|---|---|---|---|---|---|
| 1 | Source file | **PASS** | 22 959 bytes / 508 lines | — | — |
| 2 | Preprocessing | **PASS** | source `.md` | annotated + manifest + resolver IR | 磁盘文件 |
| 3 | V3 ingestion (manifest read) | **PASS** | manifest | `Manifest` (20 units) | 无（rollback） |
| 4 | **Identity boundary M1–M5** | **PASS** | manifest + source + IR | `gate=PASS, identity=VERIFIED, semantic=AVAILABLE` | 无 |
| 5 | Interface Scope | **PASS** | `identity_version=2` | `accepted: true` | 无 |
| 6 | Semantic annotation (adapter) | **PASS** | `Manifest` | payload（20 units + 14 known_gaps） | 无 |
| 7 | Resolved span | **PASS** | manifest line ranges | **54 spans, 0 unresolved** | 无 |
| 8 | **Question IR** | **PARTIAL** | ResolvedRun + payload | 20 top units：**ready=6 / incomplete=14 / unknown=0** | 无 |
| 9 | Compiler | **PARTIAL** | IR | **leaves=6, materials=0** | 无 |
| 10 | Gate | **PARTIAL** | 6 ready roots | **auto_approve=0, rejected=0, pending_review=6** | 无 |
| 11 | Candidate | **PASS**（in-session） | gate_decision | `AdmissionCandidate`（in-session） | **rollback** |
| 12 | **Admission** | **NOT EXECUTED** | — | — | — |
| 13 | **Question / QuestionInstance** | **NOT REACHED** | — | — | — |

### 5.3 Identity Gate 原始输出

```json
{
  "gate": "PASS",
  "identity_state": "VERIFIED",
  "semantic_state": "AVAILABLE",
  "reason": "identity_verified_semantic_available",
  "mismatches": [],
  "interface_scope": {
    "accepted": true, "code": null,
    "declared_identity_version": 2,
    "reason": "interface_scope_accepted: identity_version==2"
  }
}
```

### 5.4 逐单元 IR 判定（真实模块取证，`e2e_run/diag_ir.py`）

```
IR: 20 top-level units, 54 spans, 0 unresolved

U1-3  composite_unit  orig='single_choice'  status=incomplete
      shared=['material']  subs=['U1-3.sub']
      PROBLEM: sub[U1-3.sub]: options missing for choice type
      PROBLEM: composite sub_question not ready
U4-6  composite_unit  orig='single_choice'  status=incomplete
      PROBLEM: sub[U4-6.sub]: options missing for choice type
      PROBLEM: composite sub_question not ready
U7-9  composite_unit  orig='single_choice'  status=incomplete
      PROBLEM: sub[U7-9.sub]: options missing for choice type
      PROBLEM: composite sub_question not ready
Q10…Q20  standalone_unit  orig='single_choice'  status=incomplete
      PROBLEM: options missing for choice type          ← 11 个，同一根因
Q21  standalone_unit  orig='fill_in'      status=ready
Q22…Q26  standalone_unit  orig='short_answer'  status=ready

IR TALLY: ready=6 incomplete=14 unknown=0
COMPILED: leaves=6 materials=0
```

### 5.5 Gate 决策（真实 `evaluate` 输出）

| unit | decision | reason |
|---|---|---|
| Q21 | `pending_review` | `leaf 'Q21' type 'fill_in' not strict-auto (grammar None)` |
| Q22–Q26 | `pending_review` | `leaf 'Q2x' type 'short_answer' not strict-auto (grammar None)` |
| U1-3 / U4-6 / U7-9 / Q10–Q20 | **skipped** | `not_ready`（semantic_status=incomplete） |

### 5.6 单题结论

| 验证项 | 结果 |
|---|---|
| Question 是否正确生成 | **NOT REACHED**（0 行） |
| QuestionInstance 是否正确生成 | **NOT REACHED**（0 行） |
| canonical identity 是否稳定 | **PARTIAL** — IR 层 stable；未落库故无 DB identity 可验 |
| source provenance 是否保留 | **PARTIAL** — manifest_reader verbatim 保留 `section_ref`/`printed_provenance`/`basis`/`basis_evidence`；未落库 |
| material 是否正确关联 | **PARTIAL** — IR 层 `shared_components=['material']` span 已解析；compiled=0 |
| 是否产生不允许的重复对象 | **PASS** — 无任何重复（DB 全 0） |

---

## §6 Material E2E

### 6.1 composite + shared material — **PARTIAL**

| 阶段 | 证据 | 状态 |
|---|---|---|
| Producer 声明 | `ir.materials = ['L9-18','L31-33','L61-63']`，3 个 composite 各带 `material_lines` | **PASS** |
| Shared material 唯一性 | 3 个 material **各归属一个 composite**，IR 中 `shared_components={'material'}`，**未被复制为多个独立 material** | **PASS** |
| IR shared component 解析 | `shared=['material']`，**无 `shared component material unresolved` 问题** → span 解析成功 | **PASS** |
| material_dependency 关系 | `relations=[]`（producer 未声明子题级 material_dependency） | **N/A** |
| Compiler 产出 material | `compiled_materials = 0` | **FAIL** |
| 持久化到 `materials` | `materials = 0` 行 | **FAIL** |
| `unit_groups.shared_material_id` 关联 | 0 行 | **NOT REACHED** |

**`compiled_materials=0` 的根因**：`app/domains/compile/compiler.py:59` 注释明确 ——「只编译 ready node；incomplete/composite-not-ready 一律不产 leaves」。3 个 composite 因子题 `options missing for choice type` 而 `incomplete` → Compiler 不编译 → material 不产出。**这是 composite 子题 options 问题的次生结果，不是 material 模块缺陷。**

### 6.2 single question + material — **IMPLEMENTATION GAP**

| 项 | 内容 |
|---|---|
| **Frozen Spec reference** | UQ-06 §1.4（领域事实：standalone **可以**有 material）；CL-22（OPEN）；OD-BLOCK-02（未裁） |
| **actual implementation state** | `scripts/preprocessing_consumer/annotation_adapter.py:46` 登记 `GAP_STANDALONE_MATERIAL_NOT_CONSUMED`，原文明载：「当前 Gate 对 standalone 产 materials=()（CL-22 OPEN，OD-BLOCK-02 未裁，**implementation authorized = NONE**）」 |
| **blocking stage** | Compiler / Gate（standalone materials 未被消费） |
| **语料侧事实** | producer 语料 472 个 standalone **无一带 material**，故无法以真实输入驱动此路径 |

> 依据 §7 规则：**不修改规范制造「支持」**。此处登记为 `IMPLEMENTATION GAP`，且代码注释已显式承认实现授权为 NONE。

### 6.3 图片 / 图表类 material — **PARTIAL**

| 项 | 证据 | 状态 |
|---|---|---|
| `source_figures` 表 | 生产分支 seal 后 **17 行**（真实 PDF 图片提取成功） | **PASS** |
| `document_source_spans` | 生产分支 seal 后 **545 行** | **PASS** |
| `InstanceFigureLink` 关联到 QuestionInstance | 0 行 | **NOT REACHED** |
| 表格 / 公式图 material | 未构造针对性 fixture | **NOT TESTED** |

---

## §7 Composite Question E2E

### 7.1 共享 material 未被复制 — **PASS**

IR 层结构取证（真实 `IRBuilder.build` 输出）：

```
U1-3  composite_unit  shared=['material']  subs=['U1-3.sub']
U4-6  composite_unit  shared=['material']  subs=['U4-6.sub']
U7-9  composite_unit  shared=['material']  subs=['U7-9.sub']
```

- 每个 composite 持有 **恰好 1 个** `shared_components['material']`，span 解析成功。
- 无「material 被复制成多个独立 material」现象（`compiled_materials=0`，且 IR 层 material 是 `shared_components` 内的单一角色对象，非独立实体）。
- DB `materials` 表 0 行，故**不存在重复 material 对象**。

### 7.2 parent/child relationship — **PARTIAL**

| 项 | 证据 | 状态 |
|---|---|---|
| 子题结构 | `subs=['U1-3.sub']` —— 1:1 结构翻译（`_SUB_DECOMPOSITION = "producer_region_as_single_sub"`） | **PARTIAL** |
| 真实子题拆分 | Producer 不提供子题边界；adapter **不猜测拆分**，登记 `SUB_QUESTION_DECOMPOSITION_UNAVAILABLE`（3 处：U1-3/U4-6/U7-9） | **IMPLEMENTATION GAP（证据粒度）** |
| `question_number_range` | `U1-3 → "1-3"` 等已正确生成 | **PASS** |
| 子题 ready 传染 | `composite sub_question not ready` → composite 整体 incomplete（invariant 7） | **PASS**（行为正确） |

### 7.3 span / provenance / identity / admission / persistence

| 项 | 结果 |
|---|---|
| span | **PASS** — 54 spans / 0 unresolved |
| provenance | **PARTIAL** — manifest 层 verbatim 保留；未落库 |
| identity | **PASS**（IR 层）— `question_number_range` + `original_question_type` + content roles |
| admission | **NOT EXECUTED** |
| persistence | **FAIL** — 0 行 |

---

## §8 Negative / Rejection E2E

> **核心验证目标**：Gate / Admission 真正阻止非法对象，而非测试代码自行过滤。以下全部经**真实 runner / 真实 HTTP API** 执行，非单测。

### Case A — 合法输入 → 应 ADMITTED

| 项 | 值 |
|---|---|
| Command | `curl -X POST http://127.0.0.1:8000/api/documents/import -F "file=@caseA_real.pdf"` |
| Input | `2021北京通州高一（下）期中数学参考答案(1).pdf`（182 605 bytes，真实试题 PDF） |
| sha256 | `a136e47bf01ed4420a935f799a0d807182a10758ad0cf3cc1d0d280a9377350e` |
| Expected | `ADMITTED`（ingest 层） |
| **Actual** | **HTTP 200**，`document_id=3a64909b-7bc9-4f33-a067-8c95c5a36c85`, `task_id=284486c2-…`, `is_new=true` |
| DB 证据 | `documents=1`, `tasks=1` |
| **判定** | **PASS**（ingest 层） |

> **注**：Pipeline 终点（Question）的 ADMITTED **未达成** —— 因 Gate 全部 `pending_review` 且 Admission 未调用。见 §5/§17。

### Case B — 语义歧义 / 身份篡改 → 应 BLOCK

| 项 | 值 |
|---|---|
| Command | `runner_b2 --corpus e2e_run/negB --resolver-ir …` |
| Input | golden manifest，`source_content_sha256` 篡改为 `"0"*64` |
| Expected | `BLOCK` |
| **Actual** | `gate=BLOCK`, `identity_state=FAILED`, `mismatches=["computed_manifest_mismatch"]`, `semantic_state=null` |
| **下游执行** | **`downstream_executed: False`** —— IR/Compiler/Gate/Admission **完全未执行** |
| **判定** | **PASS** |

### Case C1 — 非法文件（空）→ 应 NOT_ADMITTED

| 项 | 值 |
|---|---|
| Input | `caseC_empty.pdf`（0 bytes） |
| **Actual** | **HTTP 400** `{"detail":"empty file"}` |
| DB 证据 | `documents` 未增加 |
| **判定** | **PASS** |

### Case C2 — 非法类型 → 应 NOT_ADMITTED

| 项 | 值 |
|---|---|
| Input | `caseC_wrongext.txt`（17 bytes） |
| **Actual** | **HTTP 400** `{"detail":"unsupported file type: '.txt'; allowed: ['.docx', '.pdf']"}` |
| **判定** | **PASS** |

### Case C3 — Interface Scope 越界（identity 完全有效）→ 应 BLOCK

| 项 | 值 |
|---|---|
| Input | golden manifest，`identity_version = 3` |
| **Actual** | `identity_state=VERIFIED`, `semantic_state=AVAILABLE`, 但 `gate=BLOCK` |
| reason | `interface_scope_rejected: OUT_OF_SCOPE_IDENTITY_VERSION: identity_version 3 is outside the Interface Scope field criterion (identity_version == 2). v1 legacy assets are not part of the interface (Frozen Contract §1.7) and are not silently consumed.` |
| **下游执行** | **`downstream_executed: False`** |
| **判定** | **PASS（本任务最强负向证据）** |

> **Case C3 的证明力**：identity 与 semantic 双轴**均通过**，仅 Interface Scope 轴拒绝，仍全链阻断。这证明两轴确实正交、且边界强制在一切 semantic consumption **之前**生效，不存在「version != 2 → 当成 v2 继续跑」的 fallback。

### Case C4 — 生产分支 LLM 越权调用 → 应被护栏阻断

| 项 | 值 |
|---|---|
| Command | `python -m app.worker run`（**安全默认**，无 `--allow-live`） |
| **Actual** | task `status=failed`，`task_claims.lease_snapshot.error_detail = "live denied: --allow-live not granted; task context missing; budget unavailable"`，`error_type=conflict` |
| **`llm_invocations`** | **0** —— 确认未发起任何 LLM 调用 |
| **判定** | **PASS** —— 护栏真实生效，未产生不受控外部副作用 |

### Case D — Gate 真实拒绝非法对象（非测试过滤）

| 项 | 证据 |
|---|---|
| Gate 决策产生位置 | `app/domains/gate/policy.py::evaluate`（真实模块，非测试代码） |
| 观测结果 | 6 个 ready 单元全部 `pending_review`，0 `auto_approve` |
| 拦截原因 | `leaf 'Q2x' type 'short_answer' not strict-auto (grammar None)` |
| 非 ready 拦截 | 14 单元在 **IR 校验层**即被标 `incomplete`，不进 Candidate |
| **判定** | **PASS** —— 拦截发生在真实 Gate / IR 校验层，非测试过滤 |

### Case E — Admission 拒绝路径

| 项 | 值 |
|---|---|
| 状态 | **NOT TESTED** |
| 原因 | preprocessing 分支**从不调用** `AdmissionService`；生产分支在 annotation 阶段即失败。无真实 candidate 可供 approve/reject |
| 代码层存在性 | `AdmissionService.approve/reject` 存在且接入 `app/api/routers/candidates.py`，但**无真实驱动路径可达** |

---

## §9 Provenance Verification

### 9.1 追踪链现状

```
source file                       ✅ 真实文件 + SHA256 = 31086f12…
  → source version                ✅ 生产分支：document_source_versions=1（sealed）
  → semantic annotation           ⚠ preprocessing: in-session 生成后 rollback；生产分支: 未生成
  → resolved span                 ✅ 54 spans / 0 unresolved（含 span_id 与 line_ref）
  → question IR                   ✅ 20 units（含 question_number / section_ref）
  → compiled candidate            ✅ in-session（含 input_identity / logical_execution_hash）
  → admission                     ❌ NOT EXECUTED
  → persisted object              ❌ NOT REACHED
```

### 9.2 回答「这个数据库中的 Question 是从输入文件中的哪里来的？」

> **当前无法回答 —— 因为数据库中没有 Question（`questions=0`）。**

标记：**`PROVENANCE GAP`（在 persistence 边界断裂）**

### 9.3 已具备的 provenance 字段（未落库但已构造）

| 层 | 字段 | 状态 |
|---|---|---|
| manifest_reader | `source_file`, `source_content_sha256`, `identity_version`, `sections[]`, unit 级 `section_ref` / `printed_provenance` / `basis` / `basis_evidence` | **verbatim 保留** ✅ |
| ResolvedRun | `span_id` → `line_ref` 区间 | ✅ |
| IR | `unit_id`, `question_number`, `question_number_range`, `section_ref` | ✅ |
| Candidate | `source_version_id`, `annotation_id`, `input_identity`, `logical_execution_stage`, `logical_execution_hash`, `build_versions` | ✅（in-session） |
| Admission 之后 | Question / QuestionInstance / Material FK 链 | **NOT REACHED** |

### 9.4 数据库 FK 关系（schema 已就绪，行数 0）

```
question_instances.question_id        → questions(id)
question_instances.source_version_id  → document_source_versions(id)
question_instances.document_id        → documents(id)
question_instances.unit_group_id      → unit_groups(id)
unit_groups.shared_material_id        → materials(id)
unit_groups.source_version_id         → document_source_versions(id)
material_links.material_id            → materials(id)
material_links.instance_id            → question_instances(id)
materials.source_version_id           → document_source_versions(id)
```

> **schema 层 composite + shared material 的建模是存在的**（`unit_groups.shared_material_id`），故 §7 的持久化缺口是**调用链未接通**，不是数据模型缺失。

---

## §10 Replay / Idempotency

### 10.1 Ingestion 幂等（HTTP，真实）

| | Run #1 | Run #2 |
|---|---|---|
| HTTP status | 200 | 200 |
| `document_id` | `3a64909b-7bc9-4f33-a067-8c95c5a36c85` | **相同** |
| `sha256` | `a136e47b…7350e` | **相同** |
| `is_new` | `true` | **`false`** |
| `task_id` | `284486c2-…` | **`null`** |
| DB `documents` | +1 | **+0** |
| DB `tasks` | +1 | **+0** |

**判定：PASS** —— 同 SHA256 再导入返回既有 Document，**不重复创建 Task**，无非法重复对象。

### 10.2 Pipeline 幂等 / 确定性（真实，两次执行对比）

```
Run #1: golden-report-b2-withIR.json   (2026-09-25T15:05:35+08:00)
Run #2: replay-run2.json               (2026-09-25T15:2x)
```

| 字段 | Run #1 | Run #2 | 一致 |
|---|---|---|---|
| total_manifests | 1 | 1 | ✅ |
| total_units | 20 | 20 | ✅ |
| status | completed | completed | ✅ |
| ready | 6 | 6 | ✅ |
| skipped | 14 | 14 | ✅ |
| spans_in_run | 54 | 54 | ✅ |
| unresolved_in_run | 0 | 0 | ✅ |
| compiled_leaves | 6 | 6 | ✅ |
| compiled_materials | 0 | 0 | ✅ |
| gate_auto_approve | 0 | 0 | ✅ |
| gate_rejected | 0 | 0 | ✅ |
| gate_pending_review | 6 | 6 | ✅ |
| `gate_results` 全文 | — | — | **identical ✅** |
| `identity_gate` 全文 | — | — | **identical ✅** |

**判定：PASS** —— 重放完全确定性，**未产生任何非法重复对象**（`questions=0`, `materials=0`）。

### 10.3 Pipeline 层 DB 幂等

**NOT TESTED** —— preprocessing 分支无 DB 写入（rollback），生产分支未到 compile 阶段，故 `logical_execution_hash` 幂等（`find_candidate_by_le_hash`）**无真实运行证据**。代码层 `AnnotationService.annotate` 文档声明幂等，但**未以真实运行验证**。

---

## §11 Database Verification

**验证时间**：2026-09-25，E2E 全部执行完成后

### 11.1 行数（实际 schema 表名，未自创）

| 表 | expected rows | **actual rows** |
|---|---|---|
| `documents` | 1 | **1** |
| `document_source_versions` | 1 | **1** |
| `document_source_lines` | ≥1 | **338** |
| `document_source_spans` | ≥1 | **545** |
| `source_figures` | ≥0 | **17** |
| `semantic_annotations` | 1 | **0** ❌ |
| `admission_candidates` | ≥1 | **0** ❌ |
| `admission_events` | ≥0 | **0** |
| `questions` | 6–20 | **0** ❌ |
| `question_instances` | 6–20 | **0** ❌ |
| `materials` | 3 | **0** ❌ |
| `material_links` | ≥0 | **0** |
| `unit_groups` | 3 | **0** |
| `unit_group_members` | ≥0 | **0** |
| `instance_role_contents` | ≥0 | **0** |
| `tasks` | 1 | **1** |
| `task_claims` | 1 | **1** |
| `llm_call_audit` | — | **956**（含历史测试污染，见 DEFECT-001） |

### 11.2 identity / FK / provenance 关系

| 验证 | 结果 |
|---|---|
| identity | `documents.original_sha256` UNIQUE —— `a136e47b…7350e`，单行 ✅ |
| FK relationships | schema 层 10 条 FK 全部存在（§9.4）✅；**行级关系无从验证（0 行）** |
| provenance relationships | `documents → document_source_versions → document_source_lines/document_source_spans/source_figures` **已实连** ✅；`→ semantic_annotations → admission_candidates → questions` **断裂** ❌ |

### 11.3 生产分支 seal 阶段真实产物（正面证据）

```sql
document_source_versions: role=native, provider=native, status=sealed,
                          body_text length=1198, source_meta.quality.status=valid
```

**真实 PDF → 文本抽取 → 质量门 `valid` 全链通过。**

---

## §12 API Verification

**服务启动**：`python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`

| # | Endpoint | Method | Status | Response schema | DB effect | Error handling |
|---|---|---|---|---|---|---|
| 1 | `/health` | GET | **200** | `{"status":"ok"}` ✅ | 无 | — |
| 2 | `/api/documents/import` | POST | **200** | `ImportResponse{document_id,task_id,sha256,file_name,is_new}` ✅ | `documents+1, tasks+1` ✅ | 见 3/4 |
| 3 | 同上（空文件） | POST | **400** | `{"detail":"empty file"}` ✅ | **0** ✅ | fail-loud ✅ |
| 4 | 同上（.txt） | POST | **400** | `{"detail":"unsupported file type…allowed: ['.docx','.pdf']"}` ✅ | **0** ✅ | fail-loud ✅ |
| 5 | `/api/documents` | GET | 200 | `DocumentListResponse` | 只读 | — |
| 6 | `/api/documents/{id}` | GET | 200 | `DocumentDetail` | 只读 | 404 on missing |
| 7 | `/api/documents/{id}/source-quality` | GET | 200 | `SourceQualityReport` | 只读 | — |
| 8 | `/api/documents/{id}/source-lines` | GET | 200 | `SourceLinesResponse` | 只读 | — |
| 9 | `/api/tasks` | GET | **200** | `TaskListResponse{tasks[],total}` ✅ | 只读 | — |
| 10 | `/api/admin/stats` | GET | **200** | `{pending_review,running_tasks,failed_tasks,approved_today}` ✅ | 只读 | — |
| 11 | `/api/candidates/{id}` | GET | **NOT TESTED** | — | — | 无真实 candidate |
| 12 | `/api/candidates/{id}/approve` | POST | **NOT TESTED** | — | — | 无真实 candidate |
| 13 | `/api/candidates/{id}/reject` | POST | **NOT TESTED** | — | — | 无真实 candidate |
| 14 | **pipeline trigger**（独立端点） | — | **NOT IMPLEMENTED** | 无专用端点 | — | pipeline 由 worker 消费 Task 触发 |
| 15 | **result retrieval**（pipeline 结果） | — | **NOT IMPLEMENTED** | 无 Question/QuestionInstance 查询端点 | — | — |

> 未伪造任何 HTTP E2E。§12 的 11/12/13 标 `NOT TESTED`，14/15 标 `NOT IMPLEMENTED`。

---

## §13 LLM Authority Verification

### 13.1 LLM semantic annotation ≠ LLM 决定确定性 identity — **PASS**

| 检查点 | 证据 | 判定 |
|---|---|---|
| Prompt 约束 | `app/domains/task/executor.py:100-104`：「1.不要用 Markdown 代码栅栏包裹 JSON 2.不要输出 JSON 之外的任何文字 3.不要新增上述字段之外的字段 **4.不要转录题干/选项/答案/详解正文——只输出结构标签（question_label/option_label/role/zone），正文由系统从原文切片**」 | ✅ |
| Structured output 校验 | `FORBIDDEN_FIELDS = {line_refs, corrected_line_ids, resolved_span, final_line_ids, canonical_question_type, answer_text, stem_text, material_text, options_text, explanation_text}`（`app/domains/annotation/__init__.py:7-20`），递归任意深度检查 | ✅ |
| Validation 失败后果 | `AnnotationService`：「executor / JSON parse / forbidden-field 失败**一律不创建 artifact**，原始异常直接传播」 | ✅ fail-closed |
| Resolver 独立性 | `app/core/identity_verifier.py`：「Identity State: computed vs manifest。**IR 禁止参与**。」纯函数、零 IO | ✅ |
| Identity hash 输入 | `sha256_hex(canonical_json(...))` / `logical_execution_hash(task_type, stage, contract_domain, input_domain)` —— 结构输入，**不含 LLM 生成文本** | ✅ |
| Canonical type 决定 | `map_canonical_type(original_question_type)` 由 **producer 声明的 type** 映射，非 LLM 推断；adapter 注释：「本模块**从不**由 `original_question_type` 推导 `unit_type`」 | ✅ |

### 13.2 LLM output ≠ uncontrolled database write — **PASS**

| 检查点 | 证据 |
|---|---|
| 唯一写入点 | `AnnotationService.annotate`（经 `SnapshotRepository`）；`AdmissionService`（经 repository） |
| 前置校验 | `validate_annotation_payload` → 失败即不落 artifact |
| 外部副作用收敛 | `app/ai/gateway.py`：「external 副作用唯一收敛链」，三态 disabled/mock/live，live 需 `require_allow_live` |
| 护栏实证 | §8 Case C4：无 `--allow-live` 时 `llm_invocations=0`，task failed，**零外部调用** |

### 13.3 AUTHORITY VIOLATION

**未发现。** LLM 权限边界在 prompt、schema 校验、hash 输入、gateway 护栏四层均正确实施。

> **但存在一处不对称值得登记（非 authority violation，属证据粒度）**：
> `app/worker/__main__.py:24-57` 的 `AnnotationMockProvider` **硬编码 17 个 `standalone_unit`，每个带 `options: [A,B,C,D]` per-label 声明** —— 这正是真实 producer **不提供**的粒度。因此 mock 路径可产出 `ready` 单元，而真实 preprocessing 路径不可。**本报告未以 mock 路径宣称任何 E2E PASS。**

---

## §14 Defects Found

### DEFECT-001 — 测试套件破坏性清空共享真实数据库

| 项 | 内容 |
|---|---|
| **分类** | **D — test defect**（但具真实运维风险） |
| **位置** | `tests/test_task_executor.py:38-44`（`_CLEANUP_TABLES`）+ `:132-146`（`_purge_all` / autouse `_cleanup` fixture） |
| **Observed behavior** | `python -m pytest -k executor` 后 `documents` 从 1 → **0**；我经 HTTP 导入的真实 Document 被删除。二分定位：`test_task_executor.py` 单独运行即复现（before=1, after=0），其余 3 个 executor 相关文件不复现 |
| **Mechanism** | `for table in _CLEANUP_TABLES: await s.execute(text(f"DELETE FROM {table}"))` —— **无 WHERE 的全表 DELETE**，覆盖 16 张表：`admission_events, instance_role_contents, material_links, unit_group_members, question_instances, unit_groups, materials, validation_events, admission_candidates, semantic_annotations, document_source_lines, task_claims, document_source_versions, documents, questions, tasks`。autouse fixture 在**每个测试前 + 后**各执行一次 |
| **Expected behavior** | 测试只清理自己创建的数据（按 PK/FK 定向删除，如 `test_admission.py:379-405` 的正确做法） |
| **Root cause** | 用 `DELETE FROM <table>`（全表）代替定向清理，且作用于**共享开发数据库**而非隔离库 |
| **风险** | 指向生产/共享库运行测试即造成不可逆数据丢失；亦会销毁 E2E 取证 |
| **回归证据** | 二分矩阵：`test_adversarial_retry_compounding` 1→1；`test_executor` 1→1；`test_m3_boundary_canonical_vocabulary` 1→1；**`test_task_executor` 1→0** |
| **是否修复** | **否**（见 §15 修复策略说明） |

### DEFECT-002 — preprocessing consumer 永不持久化

| 项 | 内容 |
|---|---|
| **分类** | **B — integration failure** |
| **位置** | `scripts/preprocessing_consumer/runner_b2.py:548`（`finally: await session.rollback()`） |
| **Observed behavior** | 全链（annotation / ResolvedRun / IR / Compiler / Gate / Candidate）执行完毕，DB 无任何行 |
| **Expected behavior** | 若 preprocessing 分支为生产路径，应 commit 并进入 Admission |
| **Root cause** | `run_corpus` 设计为**验证型 harness**（`phase0.2-r2-evidence-faithful`），非生产 ingestion 路径；`finally` 无条件 rollback |
| **Frozen Spec reference** | 20 §8.2（Candidate → Admission 收口） |
| **是否修复** | **否** —— 需 Owner 裁决该分支的定位（验证 harness vs 生产路径），属架构决策非局部 bug |

### DEFECT-003 — preprocessing consumer 不调用 AdmissionService

| 项 | 内容 |
|---|---|
| **分类** | **B — integration failure** |
| **位置** | `runner_b2._run_full_chain` 止于 `create_admission_candidate` |
| **Observed behavior** | `AdmissionService`（`app/domains/gate/admission.py`）在该路径**零调用** |
| **Expected behavior** | `20 §8.2`：Candidate 经 Admission 收口物化 Question / QuestionInstance / Material |
| **是否修复** | **否**（同 DEFECT-002，属架构定位问题） |

### DEFECT-004 — options 证据粒度不匹配（首个语义断点）

| 项 | 内容 |
|---|---|
| **分类** | **B — integration failure**（证据粒度契约不匹配） |
| **位置** | `scripts/preprocessing_consumer/annotation_adapter.py:58-66`（`_leaf_content` 不声明 options）↔ `app/domains/compile/ir.py:245-248`（`options missing for choice type`） |
| **Observed behavior** | 14/20 单元 `incomplete`：11 个 standalone `single_choice` + 3 个 composite 子题 |
| **Expected behavior** | choice 类型单元产 options role → ready |
| **Root cause** | preprocessing 只提供 `options_lines`（**单一行区间**），V3 IRBuilder 要求 per-label span（`sp-<unit>.option.<label>`）。adapter **明确拒绝伪造**：「不声明 options → choice-type 单元会因 "options missing" 变 incomplete，**这是诚实结果**」 |
| **Frozen Spec reference** | GAP 已由 adapter 显式登记为 `OPTION_LABEL_SPAN_UNAVAILABLE`（11 处） |
| **是否修复** | **否** —— 需要 producer 侧提供 per-label span 证据，或 Owner 授权消费策略变更。伪造 span 违反 §18「不得为了让测试通过而改规范」 |
| **证据** | `producer_boundary.known_gaps` 中 11 条 `OPTION_LABEL_SPAN_UNAVAILABLE` |

### DEFECT-005 — V3 live LLM gateway 不支持 MIMO

| 项 | 内容 |
|---|---|
| **分类** | **B — integration failure** |
| **位置** | `app/ai/gateway.py:101-129`（`build_gateway`） |
| **Observed behavior** | `build_gateway` 仅构造 `HTTPLLMProvider(name="ollama", api_key=None, base_url=settings.ollama_base_url, ...)`；`.env` 中 `MIMO_API_KEY` / `MIMO_BASE_URL` / `MIMO_MODEL` **不被读取** |
| **配置面** | `app/core/config.py:47-50` **已定义** `mimo_api_key/mimo_base_url/mimo_model/mimo_vl_model`，但 `build_gateway` 未使用 → **死配置** |
| **后果** | 生产分支 annotation 阶段无法接线真实 LLM（preprocessing 用 MIMO，V3 只认 Ollama） |
| **是否修复** | **否** —— 新增 provider 接线属架构变更，超出 §18「明确、局部、可证明的 implementation bug」授权 |

### DEFECT-006 — composite 子题 options gap 未登记

| 项 | 内容 |
|---|---|
| **分类** | **D — observability defect**（provenance 观测缺口） |
| **位置** | `annotation_adapter._unit_gaps` 的条件 `unit.original_question_type in _CHOICE_TYPES and unit.options_lines` |
| **Observed behavior** | `known_gaps` 中 `OPTION_LABEL_SPAN_UNAVAILABLE` 仅 11 条（Q10–Q20），**U1-3/U4-6/U7-9 的子题未登记**，但这 3 个子题同样因 `options missing` 失败 |
| **Root cause** | composite 单元无 `options_lines`（options 内嵌于 `questions_lines` 区间），故 gap 条件不触发；而 1:1 翻译出的子题被标为 `single_choice`，仍要求 options |
| **是否修复** | **否** |

### DEFECT-007 — 测试 / mock 路径伪造真实 producer 不提供的粒度

| 项 | 内容 |
|---|---|
| **分类** | **D — test defect**（风险：以 mock 结果冒充 E2E） |
| **位置** | `app/worker/__main__.py:24-57`（`_MOCK_ANNOTATION`） |
| **Observed behavior** | mock 硬编码 17 个 `standalone_unit`，每个含 `options:[A,B,C,D]` per-label 声明 —— 恰为 DEFECT-004 缺失的粒度 |
| **风险** | mock 模式可产 `ready` → `auto_approve` → Question，从而**制造「全流程已通」的假象** |
| **本报告处置** | **未以 mock 路径宣称任何 PASS**（§16 明确标注） |

### 分类汇总

| 分类 | 数量 | 编号 |
|---|---|---|
| A — implementation failure（违反 Frozen Spec） | **0** | — |
| B — integration failure | **4** | DEFECT-002, 003, 004, 005 |
| C — environment failure | **1**（已排除） | Docker Desktop 停止（§1.4） |
| D — test defect | **3** | DEFECT-001, 006, 007 |
| E — specification ambiguity | **0** | — |

---

## §15 Fixes Applied

### 本次任务代码修改：**0 处生产代码**

**未修改**：`app/**`、`scripts/preprocessing_consumer/**`、`Docs/V3_SPEC/**`、OD-R-01 相关文件、preprocessing 仓库任何文件。

### 新增文件（仅 E2E 取证脚本与产物，非生产代码）

| 文件 | 用途 | 影响面 |
|---|---|---|
| `AITutor-X/e2e_run/golden/pac-c02-01.manifest.json` | Golden fixture 拷贝 | 只读副本 |
| `AITutor-X/e2e_run/diag_ir.py` | 只读诊断：输出逐单元 IR 不变量违规原因 | 不被任何生产/test 代码 import |
| `AITutor-X/e2e_run/negB/` `negC/` | 负向 fixture | 只读 |
| `AITutor-X/e2e_run/*.json` | runner 输出报告 | 只读产物 |
| `AITutor-X/e2e_run/inputs/*` | HTTP import 测试输入 | 只读 |
| `D:\Project\Aitutors-preprocessing\` | tarball 解压的冗余副本（真实工作副本为 `D:\Project\Papers`） | 未使用，可删除 |

### 为何未修复 DEFECT-001~007

依 §18 BUG FIX POLICY：「允许修复明确、局部、可证明的 implementation bug」。

| DEFECT | 是否属「明确、局部、可证明」 | 处置 |
|---|---|---|
| 001（测试全表 DELETE） | 是，但**修复即改变测试隔离语义**，且当前无法判断全表清理是否为刻意设计（注释自称「可重入性…cleanup 按 FK 序删净（串行安全）」，但实现是全表 DELETE） | **STOP** —— 报告缺陷，待 Owner 裁决 |
| 002/003（rollback / 无 Admission） | **否** —— 需先裁决该分支是验证 harness 还是生产路径 | **STOP** —— `SPEC/ARCHITECTURE CHANGE REQUIRED` |
| 004（options 粒度） | **否** —— 修复需 producer 侧改证据粒度，或授权消费策略变更 | **STOP** —— `SPEC CHANGE REQUIRED` |
| 005（MIMO 接线） | **否** —— 新增 provider 属架构变更 | **STOP** |
| 006（gap 未登记） | 是、局部，但属观测增强非功能缺陷 | 未修（避免顺手优化，§18） |
| 007（mock 伪造粒度） | 是，但删除/修改 mock 会破坏 2030 个既有测试 | **STOP** |

**未做**：大规模重构、顺手优化、改 schema 绕过问题、改 Frozen Spec、新增未经批准的架构组件。

---

## §16 Remaining Gaps

### 16.1 阻断性缺口（阻断 Question 物化）

| # | Gap | Frozen Spec ref | 阻断阶段 | 类型 |
|---|---|---|---|---|
| G-1 | options 证据粒度（line-range vs per-label span） | UQ-06 / adapter `OPTION_LABEL_SPAN_UNAVAILABLE` | IR validation | **IMPLEMENTATION GAP** |
| G-2 | preprocessing consumer 无条件 rollback | 20 §8.2 | Persistence | **IMPLEMENTATION GAP** |
| G-3 | preprocessing consumer 不调用 Admission | 20 §8.2 | Admission | **IMPLEMENTATION GAP** |
| G-4 | 生产分支 LLM annotation 不可达（MIMO 未接线 + live 未授权） | 30 §2/§6 | Annotation | **IMPLEMENTATION GAP** |
| G-5 | standalone + material 不消费 | UQ-06 §1.4 / CL-22 OPEN / OD-BLOCK-02（`implementation authorized = NONE`） | Compiler/Gate | **IMPLEMENTATION GAP** |
| G-6 | composite 子题不拆分（producer 无边界证据） | adapter `SUB_QUESTION_DECOMPOSITION_UNAVAILABLE` | IR 结构 | **IMPLEMENTATION GAP（证据粒度）** |

### 16.2 未测试项

| # | 项 | 状态 | 原因 |
|---|---|---|---|
| U-1 | Admission approve/reject 真实路径 | **NOT TESTED** | 无真实 candidate 可驱动 |
| U-2 | `logical_execution_hash` DB 幂等 | **NOT TESTED** | 未到 compile 阶段 |
| U-3 | 表格 / 公式图 material | **NOT TESTED** | 未构造针对性 fixture |
| U-4 | composite 的 parent/child `UnitGroup`/`UnitGroupMember` 落库 | **NOT TESTED** | 未达 admission |
| U-5 | `/api/candidates/*` 三个端点 | **NOT TESTED** | 同 U-1 |
| U-6 | 生产分支 live LLM annotation | **NOT TESTED** | 需 `--allow-live`（未获授权）+ provider 接线（G-4） |
| U-7 | Markdown 输入的 ingestion | **NOT TESTED** | `_ALLOWED_EXTENSIONS = {".pdf", ".docx"}`，preprocessing 产物为 `.md` —— **两条分支输入类型不相交** |

### 16.3 结构性事实（非缺陷，但约束 E2E 可达性）

| 事实 | 影响 |
|---|---|
| producer 语料 472/472 standalone 无 material | §6.1 的「single + material」无法以真实输入驱动 |
| preprocessing 产物为 `.md`；V3 import 只收 `.pdf`/`.docx` | 两条分支**输入类型不相交**，无法在 ingestion 层汇合 |
| `runner_b2` 显式跳过 `SourceResolver`（「preprocessing 已提供精确行号」） | Resolver 的真实解析路径**未在 preprocessing 分支验证** |
| AITutors-v3 当前在 `od01-r3-convergence` 分支，非 `main` | 本报告结论绑定该 commit |

---

## §17 Final E2E Status

### 17.1 分阶段终态

| # | 阶段 | STATUS | 证据 |
|---|---|---|---|
| 1 | 真实输入进入 preprocessing | **PASS** | 88 074 PDF；`Ocr-markdown/` 166 份 manifest + annotated md |
| 2 | preprocessing 产出真实产物 | **PASS** | manifest + annotated.md + resolver IR（88 files，`disposition=ADMITTED`） |
| 3 | preprocessing 进入 V3（读取） | **PASS** | `runner_b2` 真实读取，20 units |
| 4 | Identity Verification（M1–M5） | **PASS** | `VERIFIED`，SHA 一致 |
| 5 | Interface Scope Enforcement | **PASS** | `identity_version=2` accepted；=3 被拒 |
| 6 | Semantic Annotation（adapter） | **PASS** | payload + 14 known_gaps |
| 7 | Resolved Span | **PASS** | 54 spans / 0 unresolved |
| 8 | **Question IR** | **PARTIAL** | 20 units：ready=6 / incomplete=14 |
| 9 | Compiler | **PARTIAL** | leaves=6 / materials=0 |
| 10 | Gate | **PARTIAL** | 0 auto_approve / 6 pending_review |
| 11 | Candidate | **PASS**（in-session） | 已构造，含完整 input_identity |
| 12 | **Admission** | **NOT EXECUTED** | DEFECT-003 |
| 13 | **Persistence** | **FAIL** | DEFECT-002（rollback） |
| 14 | **Question** | **NOT REACHED** | 0 行 |
| 15 | **QuestionInstance** | **NOT REACHED** | 0 行 |
| 16 | **Material** | **NOT REACHED** | 0 行 |
| 17 | Negative / Rejection | **PASS** | Case A/B/C1/C2/C3/C4/D 全部符合预期 |
| 18 | Provenance | **PARTIAL** | 链在 persistence 断裂 |
| 19 | Replay / Idempotency | **PASS** | ingestion 幂等 + pipeline 完全确定性 |
| 20 | Database Verification | **PARTIAL** | seal 链实连；annotation 后断裂 |
| 21 | API Verification | **PARTIAL** | 10 端点 PASS；3 NOT TESTED；2 NOT IMPLEMENTED |
| 22 | LLM Authority | **PASS** | 无 AUTHORITY VIOLATION |

### 17.2 Owner 10 问直答

| # | 问题 | 答案 |
|---|---|---|
| **1** | **真实输入是否进入 preprocessing？** | **是（PASS）**。88 074 份真实 PDF 存在于 `D:\Project\Papers\maintainess\PDF\`；`Ocr-markdown\` 下 166 份 manifest + annotated.md + `_imgs/` 为真实产物。**但 preprocessing 与 V3 是两条独立链**：V3 生产 ingestion 只收 `.pdf`/`.docx`，preprocessing 产物是 `.md`，二者输入类型不相交。 |
| **2** | **preprocessing 是否真实进入 V3？** | **部分（PARTIAL）**。真实读取链存在且运行成功（`runner_b2` 读 manifest + source + resolver IR，20 units）。**但从不落库** —— `finally: await session.rollback()`（DEFECT-002），且不调用 Admission（DEFECT-003）。V3 生产路径的 `TaskExecutor._annotation_stage` **完全不消费 preprocessing 产物**，自行调 LLM。 |
| **3** | **Semantic Annotation 是否真实执行？** | **分支分裂**。(a) preprocessing 侧：**是** —— 真实 LLM（`mimo-x-pro-preview`）产出 166 份 manifest，validation_issues/warnings 为空。(b) V3 侧 `_annotation_stage`：**否** —— `semantic_annotations=0`，task failed（`live denied: --allow-live not granted`），`llm_invocations=0`。(c) V3 侧 adapter 层：**是** —— 真实构造 payload + 14 known_gaps。 |
| **4** | **Resolver 是否真实执行？** | **部分（PARTIAL）**。Span 构造真实执行（`_build_resolved_run` → 54 spans / 0 unresolved）。但 `SourceResolver`（`app/domains/resolver/resolver.py`，675 行）**被 `runner_b2` 显式跳过**（docstring：「跳过 SourceResolver（preprocessing 已提供精确行号）」）；生产分支在 annotation 前即失败。**故 SourceResolver 的真实解析路径本次未验证。** |
| **5** | **Question IR 是否真实产生？** | **是（PASS）**。真实 `IRBuilder.build` + `validate_ir` 产出 20 个 top-level IR unit，含 `question_number` / `question_number_range` / `content` / `shared_components` / `sub_questions` / `semantic_status`。ready=6 / incomplete=14 / unknown=0。 |
| **6** | **Compiler / Gate / Admission 是否真实执行？** | **Compiler 是（PARTIAL）**：leaves=6 / materials=0。**Gate 是（PARTIAL）**：6 evaluated，0 auto_approve / 6 pending_review。**Admission 否（NOT EXECUTED）**：`AdmissionService` 在 preprocessing 分支零调用；生产分支未达 compile 阶段。 |
| **7** | **Question / QuestionInstance 是否真实持久化？** | **否（FAIL）**。`questions=0`、`question_instances=0`、`materials=0`。schema 层 FK 齐备（`question_instances.question_id → questions`、`unit_groups.shared_material_id → materials`），但**无任何行**。 |
| **8** | **Material / Composite 是否真实跑通？** | **否（PARTIAL → FAIL）**。IR 层 composite+shared material **识别与 span 解析成功**（3 个 `shared_components=['material']`，无 unresolved，未被复制为多个独立 material）✅；但因 3 个 composite 子题 `options missing` 而 incomplete → Compiler 不产 material（0）→ 持久化 0。**`single question + material` 为 IMPLEMENTATION GAP**（CL-22 OPEN / OD-BLOCK-02，`implementation authorized = NONE`），且语料 472/472 standalone 无 material，无真实输入可驱动。 |
| **9** | **Replay 是否产生非法重复？** | **否（PASS）**。Ingestion 重放：`is_new=false`、同 `document_id`、同 `sha256`、`task_id=null`、DB +0。Pipeline 重放：11 项指标 + `gate_results` 全文 + `identity_gate` 全文 **完全一致**。无非法重复对象。 |
| **10** | **当前到底在哪一层还有缺口？** | **缺口在两处，且互相独立**：**(a) 语义层** —— IR validation，options 证据粒度不匹配（DEFECT-004），导致 14/20 单元 incomplete、0 auto_approve；**(b) 架构层** —— Admission 未接线 + 无条件 rollback（DEFECT-002/003），即使 gate 全过也不会物化 Question。生产分支另有第三处：LLM annotation 不可达（DEFECT-005）。 |

### 17.3 终态

```
E2E STATUS:
PARTIAL
```

```
FIRST BLOCKING POINT:
IR VALIDATION (app/domains/compile/ir.py::validate_ir) — "options missing for choice type"
  契约不匹配：preprocessing 提供 options_lines(单一行区间)
            V3 IRBuilder 要求 per-label span (sp-<unit>.option.<label>)
  后果：14/20 units incomplete → 0 auto_approve → 无 candidate 可 admit

FIRST ARCHITECTURAL BLOCKING POINT (即使上述修通仍会阻断):
ADMISSION + PERSISTENCE — runner_b2 不调用 AdmissionService 且 finally 无条件 rollback
  后果：无论如何 gate 结果如何，Question / QuestionInstance / Material 永不落库
```

### 17.4 真实跑到哪里 / 第一次断裂 / 为什么 / 修复后到哪 / 还有什么阻断

```
真实跑到哪里
  ├─ preprocessing 侧：完整跑通（166 份 manifest + resolver IR，含 ADMITTED 条目）
  ├─ V3 preprocessing-consumer 侧：跑到 Candidate（含 IR/Compiler/Gate 全部真实执行）
  └─ V3 生产侧：跑到 Seal + Quality（1 source_version / 338 lines / 545 spans / 17 figures / quality=valid）

哪里第一次断裂
  └─ 语义断点：IR validation 的 "options missing for choice type"
     （11 standalone single_choice + 3 composite 子题，共 14/20 单元）

为什么断裂
  └─ 证据粒度契约不匹配：producer 只给 options_lines 行区间，V3 要求 per-label span。
     adapter 选择「不伪造证据」→ 诚实产出 incomplete，已显式登记为 known_gap。

修复后跑到哪里（若 G-1 修通）
  └─ 14 个单元 → ready → Gate 评估
     但 Gate 现行策略对 fill_in / short_answer 一律 pending_review（grammar None），
     对 single_choice 需 strict-auto 条件。故仍可能 0 auto_approve → 全部待人工 approve。

还有什么阻断
  ├─ G-2  rollback：永不持久化
  ├─ G-3  Admission 未接线
  ├─ G-4  生产分支 LLM 不可达（MIMO 未接线 + --allow-live 未授权）
  ├─ G-5  standalone+material 不消费（implementation authorized = NONE）
  ├─ G-6  composite 子题不拆分
  └─ U-7  两分支输入类型不相交（.md vs .pdf/.docx），无法在 ingestion 层汇合
```

---

## 附录 A — 证据文件索引

| 文件 | 内容 |
|---|---|
| `e2e_run/golden/pac-c02-01.manifest.json` | Golden fixture |
| `e2e_run/golden-report-b2.json` | 无 IR 的身份阻断报告（`semantic_pending`） |
| `e2e_run/golden-report-b2-withIR.json` | **E2E-001 主报告** |
| `e2e_run/replay-run2.json` | 重放对照 |
| `e2e_run/negB-report.json` / `negC-report.json` | 负向路径报告 |
| `e2e_run/diag_ir.py` | 逐单元 IR 诊断脚本（只读） |
| `e2e_run/inputs/` | HTTP import 测试输入（real / empty / wrongext） |
| `e2e_run/api.log` | uvicorn 运行日志 |

## 附录 B — 未执行项声明

依 §22「不要为了全流程测试假装已经具备全流程」，以下为**明确未做**：

1. 未修改 Frozen Spec 任何文件、hash、authority、数据模型、阶段定义、STOP 条件。
2. 未触碰 `Docs/60_REPORTS/OD-R-01*`，未修 H-23/H-24，未重开 OD-R-01，未新增治理审计循环。
3. 未以 mock 路径宣称任何 E2E PASS（DEFECT-007 风险已显式登记）。
4. 未用「pipeline works / looks good / ready / production ready / complete」等不可复核措辞。
5. 未执行 `--allow-live` 真实 LLM 调用（权限未获授权，且 `build_gateway` 尚未接线 MIMO）。
6. 未对 `questions` / `question_instances` / `materials` 作任何声称 —— 实测 0 行。
