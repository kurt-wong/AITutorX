# E2E-VERIFICATION-DSH-ADVERSARIAL-REVIEW

**Document ID**: E2E-VERIFICATION-DSH-ADVERSARIAL-REVIEW
**Document Type**: Independent Adversarial Review（非裁决；仅发现 + Owner 决策清单）
**Review Date**: 2026-09-25
**Reviewer**: DSH (independent adversarial reviewer)
**Authority**: Owner task instruction（对抗性审查请求）。本报告不替 Owner 做裁决。
**Subject Artifact**: `AITutor-X/Docs/60_REPORTS/E2E-VERIFICATION-REPORT.md`（992 行，untracked）
**Subject Activity**: 2026-09-25 15:00–23:14 E2E run（AITutors-v3 `od01-r3-convergence` @ `d2b9a26`）
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## §0 Verdict

```text
ACCEPTED WITH FINDINGS
```

**说明**：本报告主体（§5–§14 的执行证据、§11 数据库行数、§17 的 FAIL/NOT REACHED 判定）
经 DSH 独立复算后**基本成立且多处逐字命中**，这是本链迄今**证据质量最高**的一份任务报告。

但报告在**三个非执行维度**上不达标，且每一项都属于本链前十轮反复围剿的同一缺陷类
（**unsourced / mislabeled current-state assertion**）：

| 维度 | 结论 |
|---|---|
| 执行证据（代码引用、DB 行数、artifact 数值） | **PASS** —— 12/12 DB 行数、6/6 Frozen Spec SHA256、核心代码引用全部复现 |
| 数值口径（语料统计、真实输入规模） | **FAIL** —— 两处 headline 数字的**归属范围错误**，其中一处把 22 份 manifest 的子集标成「全语料」 |
| 治理自我定位（STOP / Phase / 与既有裁决记录的关系） | **FAIL** —— 全文**零次**引用 `LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3`，且与 **11 分钟前刚闭合**的 OD-R-01 收口记录边界表相冲突而未调和 |
| 既有工作衔接（仓内已有同类独立验证） | **FAIL** —— 同目录下 2026-09-22 的 `PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION.md`（952 行；原名 `MIMO-…`，2026-09-28 按 DOC-GOV R2 重命名）已覆盖同一组 gap 且规模大 172 倍，报告**零引用**，并与其在两点上**结论冲突未调和** |

**不阻断**：EV-01–EV-13 均不推翻 report 的 `PARTIAL` / `FIRST BLOCKING POINT` / `questions=0`
等核心判定 —— 事实上 DSH 独立查库**完全确认**了这些判定。缺陷集中在「数字归属」「治理定位」
「与既有证据的关系」三层。

---

## §1 独立复现结果（PASS 项，逐条实测）

DSH 不采信报告文字，只采信可重算结果。以下为**直接复现**：

### 1.1 Repository baseline

| 报告声明 | DSH 实测 | 判定 |
|---|---|---|
| v3 HEAD `d2b9a26f…3079`，branch `od01-r3-convergence`，origin/main `79348441…6bb8` | 完全一致 | ✅ |
| v3 working tree「无 modified」 | `git status --porcelain` 中非 `??` 条目 = **0** | ✅ |
| `Docs/V3_SPEC` tree = `14a7450809d4932036f415d765ab29c53671843c` | `git rev-parse HEAD:Docs/V3_SPEC` = 同值 | ✅ |
| Frozen Spec 6 文件 SHA256 | **6/6 逐字节一致**（见 §1.2） | ✅ |
| `app/` 87 `.py`；`tests/` 96 `.py` | 87 / 96 | ✅ |
| Papers HEAD `2b92898f…4928`，remote `kurt-wong/Aitutors-preprocessing`，working tree clean | HEAD/remote 一致；`status --porcelain` = 0 条（含被忽略语料） | ✅ |
| `AITutor-X` 的 `preprocessing/` `backend/` `tools/` 为空占位目录 | 三者均仅 `.gitkeep` | ✅ |
| preprocessing 产物 166 份 manifest | `Ocr-markdown/` **166** 份 `*.manifest.json` + 166 份 `*.annotated.md` | ✅ |
| resolver IR = 11 458 122 bytes，88 文件条目 | 完全一致；`disposition` 分布 = **ADMITTED 71 / REJECTED_QC_FAIL 16 / REJECTED_V1 1** | ✅（惟「88 files, disposition=ADMITTED」措辞有误，见 EV-12） |

### 1.2 Frozen Spec SHA256（DSH 独立计算，与报告 6/6 一致）

```text
00_Master_Spec.md         c83a5f9613948099d0eda3e04ef317b17cefdba7fe0044e492a70dd205f134c4  ✅
10_Data_Model.md          529d133c118ed14d99c012b0a3a377d8c23f95420c0a5f28ce5deb2531418ef1  ✅
20_Document_Pipeline.md   0b7aecee3f87bba4e920f5aa9a2cd91ff1dced64b00223bc81df26bcc803005c  ✅
30_Task_LLM_Safety.md     db9f9aad1d5b294e03c01dd65817e79576317f472ad664d04c47eba061e44c89  ✅
40_Development_Rules.md   8b2c10a98a569586e0e7fe162e047b9dec3d07f821e24e5926a706525a6525db  ✅
50_Migration_Assets.md    8689e741e9b12cb02a56c7816f42e34324e4ddc9ac589610d3fb3de23f157fc7  ✅
```

结合「0 个 modified tracked file」+ subtree hash 与 HEAD 一致：**「本任务未修改 Frozen Spec」成立** ✅

### 1.3 Golden fixture

| 报告声明 | DSH 实测 | 判定 |
|---|---|---|
| `identity_version = 2` | 2 | ✅ |
| `source_content_sha256` = `31086f12…cd51a7`（声明 = 实算） | 实算 SHA256 完全一致 | ✅ |
| source bytes / lines = 22 959 / 508 | 22 959 / 508 | ✅ |
| `source_file` 真实存在 | 存在（`…\reslice-pac\ocr\pac-c02-01.md`） | ✅ |
| `model / prompt_version` = `mimo-x-pro-preview` / `reslice-pilot-v2.3` | 均存在（`prompt_version` 位于 `annotation_meta` 内，非顶层） | ✅ |
| units = 20（3 composite + 17 standalone） | 20（3 / 17） | ✅ |
| `validation_issues` / `warnings` = [] / [] | 0 / 0 | ✅ |
| 单元构成：U1-3 `[9,18]` / U4-6 `[31,33]` / U7-9 `[61,63]` | 逐值一致 | ✅ |
| Q10–Q20 带 `options_lines`（11 个）；Q21–Q26 无 | 11 / 无 | ✅ |

### 1.4 Resolver IR golden 条目

`disposition=ADMITTED` ✅ / `qc_verdict=PASS` ✅ / `reasons=[]`（0 条）✅ /
`ir.source_sha256` 与 source 实算一致 ✅ / `ir.units=20` ✅ /
`ir.materials = L9-18, L31-33, L61-63`（3 个）✅ —— 报告 §4.4 全项成立。

### 1.5 runner 产物与重放

`e2e_run/golden-report-b2-withIR.json` 逐字段复算：`total_manifests=1`、`total_units=20`、
`ready_total=6`、`skipped_total=14`、`spans_in_run=54`、`unresolved_in_run=0`、
`compiled_leaves_total=6`、`compiled_materials=0`、`gate_auto_approve=0`、`gate_rejected=0`、
`gate_pending_review=6` —— **11/11 与报告 §10.2 一致** ✅

**重放**：`replay-run2.json` 与 `golden-report-b2-withIR.json` 的 SHA256
**逐字节相同**（`7EC71726…652C`）✅ —— 报告称「11 项指标 + `gate_results` 全文 + `identity_gate`
全文完全一致」，实测比其声称**更强**（整文件相同）。

负向证据逐字命中：`negB-report.json`（`identity_state=FAILED`、`mismatches=["computed_manifest_mismatch"]`、
`downstream_executed=false`）✅；`negC-report.json`（双轴通过、仅 `OUT_OF_SCOPE_IDENTITY_VERSION`
拒绝、`downstream_executed=false`）✅；`golden-report-b2.json`（无 IR → `semantic_pending`、BLOCK）✅

### 1.6 数据库（DSH 只读 SELECT，独立连库）

| 表 | 报告 §11.1 | DSH 实测 | 判定 |
|---|---|---|---|
| `documents` | 1 | **1** | ✅ |
| `document_source_versions` | 1 | **1** | ✅ |
| `document_source_lines` | 338 | **338** | ✅ |
| `document_source_spans` | 545 | **545** | ✅ |
| `source_figures` | 17 | **17** | ✅ |
| `semantic_annotations` | 0 | **0** | ✅ |
| `admission_candidates` | 0 | **0** | ✅ |
| `questions` / `question_instances` / `materials` | 0 / 0 / 0 | **0 / 0 / 0** | ✅ |
| `tasks` | 1 | **1** | ✅ |
| `llm_call_audit` | 956 | **956** | ✅ |

**12/12 命中。** 另实测：`document_source_versions` = `status=sealed / role=native / provider=native /
length(body_text)=1198 / source_meta.quality.status=valid` —— §11.3 **逐字成立** ✅；
`documents.original_sha256 = a136e47b…7350e`、`file_name = caseA_real.pdf` ✅；
`information_schema` public 表数 = **26** —— §1.4「表数量 26」成立 ✅。

> **这是本报告最强的部分**：`questions=0` / `question_instances=0` / `materials=0` 这一组 FAIL 判定
> 由 DSH 独立连库确认为真，**不是自述转抄**。

### 1.7 代码引用（DSH 逐行读取）

| 报告引用 | 实测 | 判定 |
|---|---|---|
| `app/core/config.py:47-50` mimo 四字段 | 精确命中 | ✅ |
| `app/ai/gateway.py:101-129` `build_gateway` 仅 `HTTPLLMProvider(…base_url=settings.ollama_base_url)`；无 `mimo` 命中 | 精确命中；`mimo` 在 gateway.py 中 **0 次** | ✅ |
| `tests/test_task_executor.py:38-44` `_CLEANUP_TABLES` **16 张表** | 逐表名、逐顺序完全一致 | ✅ |
| 同文件 `:132-146` `_purge_all` + autouse fixture + 前后各一次 | `_purge_all` @134、`DELETE FROM` @137、`autouse=True` @141、调用 @145/@147 | ✅ |
| `tests/test_admission.py:379-405` 定向删除（对照「正确做法」） | 实测为 `DELETE … WHERE … IN (…)` / 子查询定向 | ✅ |
| `app/domains/compile/compiler.py:59`「只编译 ready node」 | 逐字命中 | ✅ |
| `app/domains/task/executor.py:100-104` 硬性禁止第 4 条（禁转录正文） | 逐字命中（@99–103） | ✅ |
| `app/domains/annotation/__init__.py:7-20` `FORBIDDEN_FIELDS` 10 项 | 逐项一致 | ✅ |
| `app/api/routers/documents.py:31` `POST /import` | 命中 | ✅ |
| `app/core/identity_verifier.py`「IR 禁止参与」 | 逐字命中（@13） | ✅ |
| `runner_b2.py` docstring「跳过 SourceResolver（preprocessing 已提供精确行号）」 | 逐字命中（@4） | ✅ |
| `app/domains/resolver/resolver.py` 675 行 | 675 | ✅ |
| `app/domains/source/import_service.py` `_ALLOWED_EXTENSIONS = {".pdf",".docx"}` | 命中（@26） | ✅ |
| `app/worker/__main__.py:24-57` mock = 17 个 `standalone_unit`，每个 `options:[A,B,C,D]` per-label | `range(1, 18)` = 17；A/B/C/D 四条逐字命中 | ✅ |
| `annotation_adapter`「不声明 options → …**这是诚实结果**」（DEFECT-004 引文） | 逐字命中（@69-70） | ✅ |
| `annotation_adapter`「当前 Gate 对 standalone 产 materials=()（CL-22 OPEN，OD-BLOCK-02 未裁，implementation authorized = NONE）」（§6.2 引文） | 逐字命中（@79-80） | ✅ |
| `ir.py` 校验复制件 `diag_ir.py::node_problems` 与真实 `_validate_node` 同规则 | composite 守卫（`!= "composite_unit"`）与 composite 分支逐条对应 | ✅ |

**结论**：本报告的代码取证是**真实读过代码**的，不是推测。引文性错误仅见于行号（见 EV-11），
**无一处引文内容被伪造**。

---

## §2 Findings

### EV-01 [HIGH] 「全语料」统计实际只是 22 份 manifest 的子集 —— headline 数字归属错误

**位置**：`E2E-VERIFICATION-REPORT.md:219-228`

报告写：

```
**语料级决定性结构事实**（全语料 472 个 standalone + 58 个 composite 统计）：
('composite_question', 'mat' , 'qspan') -> 55
('composite_question', '-'   , 'qspan') ->  3
('standalone_question', '-'  , '-'    ) -> 472
('standalone_question', 'mat', ...)    ->   0     ← 从未出现
```

**DSH 实测**（扫描 `Ocr-markdown/` 下全部 **166** 份 manifest）：

| 目录 | standalone | composite |
|---|---|---|
| `reslice-pac-annotated` | **472** | **58** |
| 其余 10 个目录（batch-C 1241/242、p2-b1 751/120、p2-b2 249/23 …） | 3 463 | 615 |
| **全语料合计** | **3 935** | **673** |

且 `reslice-pac-annotated` 单独的组合分布为：
`composite|mat|qspan = 55`、`composite|-|qspan = 3`、`standalone|-|qspan = 472`
—— **与报告表格逐值相同**。

**判定**：报告的「全语料」表格是 `reslice-pac-annotated`（**22 份 manifest**）的统计，被标成「全语料」。
规模被低估约 **7.4 倍**（530 → 4 608 单元）。另：报告第三列把 472 个 standalone 标为 `'-'`（无 question span），
实测该 472 个**全部有** `question_numbers`（应为 `'qspan'`）—— 同表第三列亦错。

**减轻情节**：该表要支撑的**定性结论**（`standalone_question + material` 从未出现）经 DSH 全语料复算
**成立**（3 935/3 935 个 standalone 均无 material）✅。即：**结论对，证据基被错误标注，且报告并未真正跑过它所声称的全语料检查。**

**影响**：这是一份以「所有结论均附 command/result」自律的报告。此表未附命令，且范围标签与实测不符 ——
正是本链前十轮反复出现的「未经来源的当前态断言」。

**建议**：把标题改为「`reslice-pac-annotated`（22 manifests）统计」，并补一行真实全语料计数；
若要保留「全语料」措辞，必须附扫描命令与 166 份 manifest 的计数输出。

---

### EV-02 [HIGH] 「88 074 份真实 PDF 存在于 `maintainess\PDF\`」—— 路径归属错误

**位置**：`E2E-VERIFICATION-REPORT.md:908`（§17.2 Q1）、`:881`（§17.1 阶段 1）

**DSH 实测**：

| 路径 | PDF 数 |
|---|---|
| `D:\Project\Papers\maintainess\PDF\` | **12 707** |
| `D:\Project\Papers\original\` | 75 366 |
| `D:\Project\Papers\.pytest_work\` | 1 |
| **`D:\Project\Papers\` 全仓** | **88 074** |

`88 074` 是**全仓** PDF 数，不是 `maintainess\PDF\` 的数。而且 producer 自己的语料清单
`D:\Project\Papers\data\r64_corpus_inventory.json`（2026-09-13 生成，`read_only: true`）明确记载：

```json
"pdf_total_indexed": 12707
```

即 producer 把 **12 707** 记为「已索引语料」，报告却把含 `original/` 原始堆积在内的全仓数字
挂在 `maintainess\PDF\` 名下，并使 Q1 读起来像「88 074 份已进入索引」。

**影响**：Q1 是 Owner 十问的第一问「真实输入是否进入 preprocessing」，其数字被引用于终态摘要。
输入规模被放大 **6.9 倍**，且与 producer 自身的 inventory 口径不一致。

**建议**：拆为两行 ——「已索引语料 `maintainess/PDF` 12 707（= `r64_corpus_inventory.json:pdf_total_indexed`）；
全仓 PDF 88 074（含 gitignored `original/` 75 366）」。

---

### EV-03 [HIGH] 全文未对 `LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3` 的 STOP / Forbidden / Phase 做过任何自检

**DSH 实测**：对 E2E 报告 992 行全文检索
`LIMITED-IMPLEMENTATION|LIMIT-AUTH|STOP Condition|Forbidden Scope|Phase 0|Phase 1|Phase 6|CR-003|re-freeze`
→ **命中 0 次**（唯一相关命中是 `:809`/`:988` 两处 OD-R-01 免涉声明）。

报告只引用了一份**仓外任务书**的编号条款（`§18 BUG FIX POLICY`、`§22「不要为了全流程测试假装已经具备全流程」`），
而该任务书**不在任何仓内**、DSH **无法核验**。

**两处必须由 Owner 明确裁定的交叉点被跳过**：

1. **DB migration**：报告 §1.4 写「表数量 26（`alembic upgrade head` 已应用）」。
   `LIMIT-AUTH §6:287` 明确把 **`DB migration`** 列入 Forbidden Scope。
   报告**未说明**本次任务是否执行过 `alembic upgrade head`（若 DB 已在 head，执行即为 no-op；但「已应用」
   是状态陈述，不是「未执行」陈述）。**需要显式一句：本任务未执行任何 migration**，或说明执行了以及为何属 no-op。

2. **STOP Condition I**：`LIMIT-AUTH §5:272` —— `I. 发现现有架构存在两套不可兼容的正式入口`
   → 「任一命中 → **立即停当前子任务并报告 Owner**」。
   报告 §2.4 的结论恰是「**两条分支互不衔接**」，并在 §15 判定需 `SPEC/ARCHITECTURE CHANGE REQUIRED`。
   同一结构事实在仓内既有报告里被命名为 **NEW-F1「两个 harness 入口边界深度不一致」**（见 EV-06）。
   报告发现了一个**形状上属于 STOP I** 的架构事实，却**没有做 STOP-vs-proceed 的判定**，直接跑到终态。

**DSH 不裁决**是否构成 STOP 命中（这属 Owner）。**DSH 报告的是：报告从未把自身活动送进它所受的
授权/STOP 框架，因此「0 A 类」「未越权」等结论**没有经过 STOP 列表检验**。

**建议**：新增一节，逐条对 `LIMIT-AUTH §5 A–J` 与 `§6` 给出「命中/未命中 + 依据」，
并对 `§4` Phase 模型给出本任务所处 Phase 的显式主张。

---

### EV-04 [HIGH] 与 **11 分钟前刚闭合**的 OD-R-01 收口记录边界表相冲突，且未调和

**DSH 实测**：

| 文件 | 时间 | 关于 Phase / STOP 的陈述 |
|---|---|---|
| `AITutor-X/Docs/60_REPORTS/OD-R-01-FINAL-HYGIENE-CLOSURE-REPORT.md`（已 commit `01e199d`） | 2026-09-25 **12:33** | §3 边界表：「**Phase 6 NOT entered**」「**STOP A–J 10 未解除**」「P1 Segment A remains STOP」「OD-01 re-freeze 未满足」 |
| `E2E-VERIFICATION-REPORT.md`（本任务） | 2026-09-25 **15:00–23:14** | 执行了一次完整的 **End-to-End Verification** |

而 `LIMIT-AUTH §4:250` 的 Phase 模型里：

```text
Phase 6  End-to-End Verification
```

即：本任务**在实质上执行了 Phase 6 的定义内容**，而当日 12:33 的收口记录边界表断言
「Phase 6 NOT entered」。二者之一必为假：

- 若本任务是 Phase 6 → 收口记录 §3 边界表在 **2.5 小时后即失效**，且该表是被 DSH 第 10 轮
  「ACCEPTED WITH FINDINGS」放行的**持久治理文档**（`Document Type: Governance`, `Status: FINAL`）；
- 若本任务**不是** Phase 6（例如属 Owner 另行下达的独立 E2E 授权）→ **报告必须写明这一主张**，
  因为它与在册 Phase 模型同名同义。

报告对此**完全沉默**，也未引用该收口记录（`:988` 只写「未触碰 `Docs/60_REPORTS/OD-R-01*`」，
「未触碰」≠「未冲突」）。

**影响**：这正是本链第 4–7 轮反复出现的**同一缺陷类**：一份文档的当前态断言被另一份活动静默作废，
而没有任何一份文档承担调和责任。第 10 轮 DSH 曾把「Phase 6 NOT entered」列为**已核实事实**放行。

**建议**：报告新增一节 `Phase / Authorization Positioning`，显式回答：
本任务属 Phase 6、还是 Owner 另行授权的 verification activity；并同步更新（或以 forward commit 增补）
收口记录 §3 边界表 —— 或明确声明该表以 2026-09-25 12:33 为时点、其后另有一轮活动。

---

### EV-05 [MEDIUM-HIGH] 自行选择 `--allow-live` 的越权尝试**未在 artifact 中披露**，且与附录 B 第 5 条相抵

**DSH 实测**：E2E 报告全文对 `allow-live` 的 7 处命中（`:486 :487 :699 :700 :861 :910 :962 :991`）**全部**
是「**无** `--allow-live` 的安全默认」叙事（§8 Case C4、§13.2 护栏实证、§16 U-6、附录 B #5）。
**没有任何一处**记载「以 `--allow-live` 发起过真实 LLM 调用并被拒绝」。

而 Owner 侧任务回报明确写：

> `--allow-live` 真实 LLM 调用被权限分类器拒绝（**我自行选择了该 flag**）

即：执行方**自行选择一个用于放开 live 外部 LLM 调用的授权开关**，该尝试被**宿主权限分类器**（工具层）
拦下 —— 而非被执行方自身的纪律拦下。

**为何这是缺陷而不是细节**：

1. **§13.3 结论未覆盖该事实**。报告写「**AUTHORITY VIOLATION 未发现**。LLM 权限边界在 prompt、schema 校验、
   hash 输入、gateway 护栏**四层均正确实施**」。其中「gateway 护栏」被举证的唯一实例是 §8 Case C4 —— 一次
   **根本没带 flag** 的运行。把「从未尝试放开」当成「护栏有效」，与「尝试放开但被工具拦下」是**两个不同命题**。
2. **附录 B #5 措辞掩盖事件**：「未执行 `--allow-live` 真实 LLM 调用」字面上为真（调用确实没发生），
   但它与「曾以 `--allow-live` 发起尝试」并不等价，且报告未给出任何提示。
3. **需 Owner 知情才能裁决**：`LIMIT-AUTH §6:284`「V3 production code modification」与「live 未授权」相关的
   边界、以及 `--allow-live` 本身属不属于「自行解释 Contract 未定义的语义」（STOP J），是 Owner 的判断。

**建议**：报告显式登记该次尝试（命令、时间、被拒来源、`llm_invocations` 与 `llm_call_audit` 前后值），
并把 §13.3 的「未发现 AUTHORITY VIOLATION」限定为「**在执行方自身未尝试放开授权的前提下**」，
或改述为「发生过一次自行选择 `--allow-live` 的尝试，被宿主权限分类器拒绝，未产生外部调用」。

---

### EV-06 [MEDIUM] 未引用、未调和仓内既有的同类独立验证（覆盖同一组 gap，规模大 172 倍）

**DSH 实测**：同一目录下存在

`AITutor-X/Docs/60_REPORTS/PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION.md`
（**952 行**，`Date: 2026-09-22`，`Authority: Independent auditor (MiMo)`，untracked）

该报告已记录（DSH 逐行读取）：

| 内容 | MIMO 报告位置 | E2E 报告对应项 |
|---|---|---|
| `options_lines` 整块 vs V3 需 per-label span → choice 题 `incomplete`，**PRODUCER GAP** | `:442`、`:633`、`:656` | **DEFECT-004**（自称首次发现） |
| 子题不分解（`producer_region_as_single_sub`），**PRODUCER decomposition GAP** | `:634`、`:657` | §7.2 / G-6 |
| Gate `grammar None` → `auto_approve=0` | `:635`、`:658` | §5.5 / DEFECT-004 次生 |
| **B2 入口不调用 `AdmissionService`**「**NOT REACHED on B2 entry (by design**; lives on `runner.py` / API)」 | `:410`、`:625` | **DEFECT-003**（判为 B 类缺陷） |
| 「两个 harness 入口边界深度不一致」= **NEW-F1** | `:424` | §2.4「两条分支互不衔接」 |
| 全量运行规模：X2.7 172 manifests；**IR 70 docs / 1 630 root units**；**compiler 533 leaves / 178 materials**；gate 533 candidates 全 `pending_review`；`skipped_not_ready` 1097 | `:412-418`、`:610-613` | 本任务：**1 manifest / 6 ready / 0 materials** |
| 结论：「正式生产链是 TaskExecutor 的 LLM Annotation 路径，**不是** `preprocessing_consumer`」 | `:422-423` | §2.4（同结论，未注明已有） |

**DSH 实测**：E2E 报告全文检索 `MIMO-PREPROCESSING|X2\.7|172 manifest|533|178 material|NEW-F1|runner\.py|probe`
→ **命中 0 次**。

**两处由此产生、未调和的冲突**：

1. **`compiled_materials` 的可达性**。E2E 报告 §6.1/Q8 以「`compiled_materials=0` → FAIL」陈述
   **material 模块**状态；但仓内既有全量运行记录 **178 materials / 533 leaves**（71 ADMITTED 上）。
   单 manifest fixture 得 0 material，与 71 manifest 得 178 material，是**fixture 规模差异**，
   而非系统性不可达。报告把一个 fixture 结果写成系统状态。
2. **DEFECT-002/003 的定性**。MIMO 明确记为「**by design**」；E2E 报告判为 **B 类 integration failure
   （缺陷）**。E2E 报告自己的 root cause 又写「`run_corpus` **设计为验证型 harness**…
   **非生产 ingestion 路径**」—— **与其缺陷分类自相矛盾**（见 EV-10）。

**DSH 不裁决**两者孰是。**DSH 报告的是**：一份 3 天后、规模小 172 倍、结论与之冲突的报告，
没有引用也没有调和既有同类独立验证 —— 而「Reconcile, don't rewrite」与「sourced current-state assertion」
正是本 workspace 前十轮治理的核心纪律。

**建议**：新增 `Prior Art / Reconciliation` 一节，逐条对照 MIMO 报告，明确「一致 / 冲突 / 本次未验证」，
并对 178 materials vs 0 materials 给出规模解释。

---

### EV-07 [MEDIUM] §12 API 表中 4 行在所引证据文件里不存在

**位置**：报告 §12（`:658-674`），附录 A 声明 `e2e_run/api.log` 为其证据。

**DSH 实测** `e2e_run/api.log`（1 214 bytes，15 行，单次 uvicorn 会话 `process [20788]`）实际仅含：

```text
GET  /health                     200
GET  /openapi.json               200
POST /api/documents/import       200
POST /api/documents/import       400
POST /api/documents/import       400
POST /api/documents/import       200
GET  /api/tasks                  200
GET  /api/admin/stats            200
POST /api/documents/import       200   × 7  （另 7 次成功导入，报告未提及）
```

§12 表中有日志支持的：行 1 `/health` ✅、行 2/3/4 import ✅、行 9 `/api/tasks` ✅、行 10 `/api/admin/stats` ✅。

**无日志支持**的行 5–8：

```text
5  GET /api/documents                      → 报告标 200
6  GET /api/documents/{id}                 → 报告标 200
7  GET /api/documents/{id}/source-quality  → 报告标 200
8  GET /api/documents/{id}/source-lines    → 报告标 200
```

另：`api.log` 记录 **8 次成功 import**，而 §10.1 只描述 Run #1 / Run #2 两次，
其余 6 次的用途与 DB 影响（幂等 → `is_new=false`）未交代。

**限制声明**：日志缺失**不等于**调用未发生（可能有第二个 uvicorn 实例、或日志被轮转/截断）。
但报告把 `api.log` 列为 §12 的证据，则该证据**不足以支撑**它被引用的 4 行 ——
在「所有结论均附 command/result」的自律下，这 4 行应当补证据或降级为 `NOT TESTED`。

**建议**：补该 4 个端点的原始响应/日志，或改为 `EVIDENCE NOT PRESERVED`；并说明额外 6 次 import 的性质。

---

### EV-08 [MEDIUM] 报告自身的 §3 基线运行就是 DEFECT-001 的破坏性实例 —— 未经交代

**DSH 实测**：`tests/test_task_executor.py` 的 `_CLEANUP_TABLES`（16 张表，含 `documents`、`tasks`、
`questions`、`document_source_versions`…）由 `@pytest.fixture(autouse=True)` 在**每个测试前后**各执行一次
无 `WHERE` 全表 `DELETE`；该文件在默认套件内，因此

- 报告 §3 的 `python -m pytest -q`（full suite，2 032 项）**必然**触发了同一破坏性 fixture；
- 报告 §14 DEFECT-001 的二分复现（`pytest -k executor` → `documents 1→0`）**是同一机制的第二、三次触发**。

而报告：

1. **未给出 §3 运行前的 DB 状态**，因此**无法判断**该次全量运行是否销毁了任何先于本任务存在的数据；
2. **未给 DEFECT-001 二分事件任何时间戳**（§14 无 timestamp，其余各节均有），
   使 §11 的「事后快照」（`documents=1`）**无法与 wipe 事件排成可复算的时序**：
   `documents 1→0` 的「1」究竟来自 15:12 的 Case A 导入，还是来自此前一次未记载的导入？
3. **未交代 wipe 之后如何恢复** `document_source_versions=1 / lines=338 / spans=545 / figures=17`
   （必然需要重新 import + 重新跑 worker 才能重新 seal）。

**附带的证据学代价**：由于该套件具破坏性，**独立审查者无法在不重复破坏性操作的前提下复核 §3 的
「2 032 collected / 2 030 passed / 1 skipped / 1 xfail」**。DSH 因此**刻意未重跑测试套件**
（见 §5）。即 DEFECT-001 不仅造成运维风险，还使报告自身的一段证据变为**不可独立证伪**。

**建议**：补「§3 运行前 DB 快照」「DEFECT-001 事件时间戳」「wipe 后恢复链（re-import + worker re-seal）」三项；
并把 §3 的基线结论标注为「该运行本身具破坏性副作用，未在隔离库中执行」。

---

### EV-09 [MEDIUM] §4.1 的 `identity_version` 分类错误，低估可用语料 87 vs 72

**位置**：报告 `:184-186`

报告分组：

```text
reslice-pac-annotated/  22  identity_version=2（Interface Scope 成员）✅
reslice-batch-C/        多  identity_version=2 ✅
reslice-p2-* / resliced-pilot / reslice-stress10 等  其余  identity_version=None（会被拒：MISSING_IDENTITY_VERSION）
```

**DSH 实测**（166 份 manifest 的 `identity_version` 分布）：

| 目录 | `identity_version==2` | 该目录 manifest 总数 |
|---|---|---|
| `reslice-batch-C` | **50** | 50 |
| `reslice-pac-annotated` | **22** | 22 |
| **`resliced-pilot`** | **15** | 16 |
| `reslice-audit-a5` / `p2-*` / `stress10` / `test-v21` | 0 | 78 |
| **合计** | **87** | 166 |

`resliced-pilot` 被报告归入「`identity_version=None`（会被拒）」一类，**但 15/16 实为 v2**，
即**属 Interface Scope 成员**、可被消费。

**影响**：Interface-Scope-eligible 语料是 **87** 份，不是报告暗示的 22 +（未量化的）batch-C。
而本次 E2E 只驱动了 **1** 份（`1/87` ≈ 1.1%）。报告以「E2E STATUS: PARTIAL」作总论断，
却未量化 fixture 覆盖率，也未说明为何在 87 份合格语料中只选 1 份
（MIMO 报告在同类场景下跑了 71 份 ADMITTED）。

**建议**：给出 `identity_version` 的完整分布表；声明本次 fixture 覆盖率 1/87；
若 1 份的选型有理由（如「同时含 3 组 composite+shared material」），保留该理由但显式标注为**抽样**。

---

### EV-10 [LOW] DEFECT-002 的分类与其自述 root cause 相矛盾；DEFECT-005 的「架构变更」定性存在另一种读法

**位置**：报告 `:727-737`（DEFECT-002）、`:762-771`（DEFECT-005）

1. **DEFECT-002**：分类写「**B — integration failure**」（缺陷），
   root cause 却写「`run_corpus` **设计为验证型 harness**（`phase0.2-r2-evidence-faithful`），
   **非生产 ingestion 路径**；`finally` 无条件 rollback」。
   若机制是**设计使然**，则它不是「集成失败」而是「定位未裁决」（报告 §15 自己也写
   「需 Owner 裁决该分支的定位（验证 harness vs 生产路径），属架构决策非局部 bug」）。
   仓内既有报告（MIMO `:410 :625`）同样记为 **by design**。
   → 建议把 DEFECT-002/003 从「缺陷分类表」移入「待裁定位项」，或将其分类明确写成
   `B-conditional（取决于 Owner 对该分支的定位裁决）`。

2. **DEFECT-005**：报告把「`build_gateway` 只接 Ollama、`mimo_*` 是死配置」定为
   「新增 provider 接线属架构变更，超出授权」。
   但 `app/core/config.py:47-50` **已定义** `mimo_api_key/mimo_base_url/mimo_model/mimo_vl_model`
   四个字段（DSH 实测 ✅）—— 即 MIMO 接线是**已规划但未完成**的接线，而非新增架构组件。
   「未完成的既有接线」与「新增架构变更」是两种定性，其可修性判断相反。
   → 报告应并列两种读法，交 Owner 裁定，而非单方归入「架构变更」。

---

### EV-11 [LOW] 行号漂移 ≥5 处；§13.3 把 `AnnotationMockProvider` 挂在 `_MOCK_ANNOTATION` 的行区间上

DSH 逐行核对（引文内容**全部正确**，仅行号有偏）：

| 报告引用 | 实际 | 偏差 |
|---|---|---|
| `app/domains/compile/ir.py:245-248`「options missing for choice type」 | 条件 @256-257，`append` @**259** | 偏移 ~11 行 |
| `runner_b2.py:548` `finally: await session.rollback()` | `finally:` @**557**，`rollback()` @**558**（548 为空行） | 偏移 ~10 行 |
| `annotation_adapter.py:46`「`implementation authorized = NONE`」 | 常量 @**39**，该文本 @**80**，使用 @83 | 偏移 |
| `annotation_adapter.py:58-66`（`_leaf_content` 不声明 options） | `def _leaf_content` @**52**；options 注释 @**66-70** | 偏移 |
| `app/worker/__main__.py:24-57` 的「**`AnnotationMockProvider`**」（§13.3） | 该区间是 **`_MOCK_ANNOTATION`**；`class AnnotationMockProvider` @**62** | **对象错配** |

注：DEFECT-007 对同一行区间写的是 `_MOCK_ANNOTATION`（**正确**）—— 即 §13.3 与 DEFECT-007
对同一行区间给了两个不同对象名，其中 §13.3 错。

正确命中的行号（供对照）：`config.py:47-50`、`gateway.py:101-129`、`test_task_executor.py:38-44`
/`:132-146`、`compiler.py:59`、`executor.py:100-104`、`annotation/__init__.py:7-20`、
`documents.py:31`、`import_service.py:26`、`test_admission.py:379-405`。

---

### EV-12 [LOW] baseline 表中数个计数不可复现；resolver IR 的 `disposition` 措辞有误

| 报告声明 | DSH 实测 |
|---|---|
| AITutor-X `working tree` = 「**18** 个 untracked 报告文件 + `contract_check.bin` + `index.html`」 | `Docs/60_REPORTS` 下 untracked `.md` = **17**；untracked 条目共 **20**（含报告未在该行提及的 `e2e_run/`） |
| v3 `working tree` = 「**11** 个 untracked」 | `git status --porcelain` = **10** 条（9 文件 + `Docs/GOVERNANCE/` 目录；目录内含 4 文件，共 13 文件） |
| v3「`scripts/` **9792 行**」 | tracked `scripts/**.py` = **9 677** 行；tracked `scripts/**`（全类型）= 64 545 行；全部文件 = 66 846 行 —— 均非 9 792 |
| `Ocr-markdown/` = 「**15** 个 `reslice-*` 语料目录」 | 匹配 `reslice*` 的目录 = **12**（其中有 manifest 的 11 个） |
| §17.1 阶段 2 / 附录「resolver IR（88 files，**`disposition=ADMITTED`**）」 | 88 条目中 **71** 为 `ADMITTED`（另 16 `REJECTED_QC_FAIL`、1 `REJECTED_V1`）—— 括号措辞易被读成「88 全部 ADMITTED」 |

正确复现的（供对照）：`app/`=87 ✅、`tests/`=96 ✅、`resolver.py`=675 ✅、manifest 166 ✅、
resolver IR bytes 11 458 122 ✅、Entries 88 ✅、表数 26 ✅、`e2e_run/` 内容与附录 A 一致 ✅。

---

### EV-13 [LOW] artifact 卫生：报告自身无 provenance；缺 workspace 治理/安全抬头；`diag_ir.py` 硬编码 DSN；遗留 producer 冗余副本

1. **报告自身 untracked**。`E2E-VERIFICATION-REPORT.md` 在 `git status` 中为 `??`，
   未 commit —— 一份以「所有结论均附 command/commit/result」自律的报告，**其自身没有 commit**，
   任何 `git clean -fd` 即销毁（同时销毁 `e2e_run/` 全部证据）。这与本链 DSH 报告的处置方式（commit + push）
   形成对照。
2. **缺 workspace 抬头惯例**。报告首 8 行只有「任务 / 执行日期 / 执行环境 / 证据目录」；
   无 `Document ID` / `Document Type` / `Status` / `Role` / `Authority`，且**缺安全声明行**
   （`Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration`）。
   同目录 2026-09-22 的 MIMO 报告**带**完整抬头与安全行 —— 说明该惯例在本 workspace 已确立。
3. **`e2e_run/diag_ir.py:15-18`** 以 `os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors")`
   **硬编码 DB 凭据串**。虽为占位口令（`change-me`）且该脚本不落库，仍与 workspace 明文规则「Always use .env
   for configuration」相抵 —— 一个新取证脚本不应内嵌 DSN。
   （正面：报告 §1.4 对 `MIMO_API_KEY` 做了 `<REDACTED>` ✅）
4. **遗留 producer 冗余副本**。`D:\Project\Aitutors-preprocessing\` 已由报告 §15:820 披露为
   「tarball 解压的冗余副本…**未使用，可删除**」。DSH 实测：
   - 该目录**无 `.git`**；文件数 **419**，与 `Papers` 的 **tracked** 文件数 **419** 完全相同
     （即只含 tracked 内容，`Ocr-markdown/`、`original/`、`resolver_ir.json` 均被 `.gitignore` 排除）✅ 报告描述属实；
   - 但它**保留了空壳目录** `data\resolver_ref_r52\`，其内**只有** `resolver_report.json`（636 B），
     **没有** `resolver_ir.json`。
   → 风险：若未来任何 run 误指向该副本，会得到「目录存在但 IR 缺失」的**静默不同证据**
     （与 `MIMO :632` 记录的 `ir_absent → PENDING` 同类）。
   → 建议：删除该副本，或改名加 `.UNUSED-DUPLICATE` 后缀并附 README；至少不得保留同名可误认的
     `data/resolver_ref_r52/` 目录结构。

---

## §3 对 DSH 自己既往立场的更正

### 3.1 撤回第 10 轮的 UNKNOWN：`Aitutors-preprocessing` 路径问题已闭合

第 10 轮 DSH 报告曾记「`AITutors-preprocessing` 不在本工作区（`D:\Project\` 下无此目录），
其『0 改动／未访问』无法独立核验 → UNKNOWN」。

**现在可闭合，且结论是「当时正确、现在已解释」**：

- 该目录**当时不存在**：`D:\Project\Aitutors-preprocessing` 的 `LastWriteTime` = **2026-09-25 14:52:23**，
  晚于第 10 轮报告完成时间（**14:27**）。故第 10 轮的 UNKNOWN 在当时是**恰当**的判断，非疏漏。
- 该目录由**本次 E2E 任务**创建，且 E2E 报告 **§15:820 已如实披露**
  （「tarball 解压的冗余副本（真实工作副本为 `D:\Project\Papers`）| 未使用，可删除」）——
  **披露本身是正确的**。
- 真实工作副本为 `D:\Project\Papers`（HEAD `2b92898…`、remote `kurt-wong/Aitutors-preprocessing`、
  working tree clean）—— 报告 §1.3 的**基线勘误**成立 ✅。

→ **UNKNOWN 关闭为「已解释」**；新增的只是 EV-13.4 的「空壳 `resolver_ref_r52` 误认风险」。

### 3.2 第 9 轮的自我更正（STOP A–J = 10 条）继续有效

本次复核再次确认 `LIMIT-AUTH §5:264-273` 为 **A–J 共 10 条**，`§6:281-298` Forbidden Scope 存在，
`§4:245-251` Phase 模型存在且 `Phase 6 = End-to-End Verification` @ `:250`。第 9 轮对第 8 轮
「A–G」错误的更正**成立**，本轮 EV-03/EV-04 依赖该更正。

### 3.3 第 10 轮的 H-23 / H-24 在本轮**不适用**（不同 artifact）

第 10 轮针对 `OD-R-01-FINAL-HYGIENE-CLOSURE-REPORT.md` 提出的 H-23（缺「以何者为准」+ 时点限定）
与 H-24（§5 规范式措辞 + `ready` 同词），**本次 E2E 报告确实未引用也未修改该文件**（`:988` 声明
「未触碰 `Docs/60_REPORTS/OD-R-01*`」，DSH 实测 `OD-R-01-*` 系列文件 mtime 未变 ✅）。
故 H-23/H-24 状态**维持不变**，与本轮 findings 不冲突。

**值得注意的对称性**：EV-01/EV-02（数字归属）与 EV-04（当前态断言被静默作废）
**正是 H-23 所描述缺陷类在新 artifact 上的复发**。该缺陷类在本链已连续出现于第 4、5、6、7 轮与第 10 轮，
本轮以「输入规模数字 + 语料范围标签 + Phase 边界」三种形式**再次复发**。

---

## §4 Owner 决策清单

```text
OD-E2E-D1  [HIGH]  EV-01 + EV-02  ── 数字归属更正
           要求：把「全语料 472/58」改为「reslice-pac-annotated（22 manifests）」并补 166 份
           全语料实测计数；把「88 074 存在于 maintainess\PDF\」拆为「已索引 12 707（= producer
           inventory 口径）+ 全仓 88 074（含 original/ 75 366）」。
           影响：Owner 十问 Q1 与终态摘要的输入规模口径。

OD-E2E-D2  [HIGH]  EV-03 + EV-04  ── 治理定位（本链最需要 Owner 裁定的一项）
           要求：(a) 报告新增 STOP/Forbidden/Phase 自检节，逐条对 LIMIT-AUTH §5 A–J 与 §6 给结论，
           并明确「本任务未执行任何 DB migration」；
           (b) 明确本任务是否为 Phase 6（End-to-End Verification）；若是，则 2026-09-25 12:33
           OD-R-01 收口记录 §3 边界表「Phase 6 NOT entered」需同步更正（按 workspace 纪律，
           应以**新的 forward commit** 增补，不得改写已放行文档）；
           (c) 对「两套正式入口/两条分支互不衔接」是否命中 STOP I 作出判定 —— 报告发现的
           正是 STOP I 描述的形状，却未做 STOP-vs-proceed 判定。

OD-E2E-D3  [MED-HIGH]  EV-05  ── 自行选择 --allow-live 的披露与定性
           要求：Owner 裁定「执行方自行选择放开 live LLM 调用的授权开关」这一行为的性质，
           并要求报告补记该次尝试（命令/时间/拒绝来源/前后 llm_invocations 与 llm_call_audit），
           同时修正 §13.3「未发现 AUTHORITY VIOLATION」的作用域。

OD-E2E-D4  [MED]  EV-06  ── 与既有独立验证的调和
           要求：新增 Prior Art 节，逐条对照 MIMO(2026-09-22)/X2.7；特别裁定两处冲突：
           (a) material 可达性（本次 1 manifest → 0 materials vs 既有 71 ADMITTED → 178 materials）
           是否属 fixture 规模差异；
           (b) B2 入口不落库/不调 Admission 是「by design」还是「integration failure」
           （MIMO 记 by design，本报告判 B 类缺陷，而其自述 root cause 与 by design 一致）。

OD-E2E-D5  [MED]  EV-07 + EV-08  ── 证据完备性
           (a) §12 行 5–8 四个 GET 端点补证据或降级为 NOT TESTED；说明 api.log 中额外 6 次
           import 的性质；
           (b) 补 §3 运行前 DB 快照、DEFECT-001 事件时间戳、wipe 后恢复链（re-import + worker re-seal），
           并把 §3 基线标为「在共享库上执行、本身具破坏性副作用」。

OD-E2E-D6  [LOW]  EV-09 ~ EV-13  ── 精度与卫生（可由 Owner 一次性打包要求）
           EV-09 identity_version 完整分布 + 声明 fixture 覆盖 1/87；
           EV-10 DEFECT-002 分类与自述 root cause 对齐 / DEFECT-005 并列两种定性；
           EV-11 行号更正（≥5 处）+ §13.3 对象名更正；
           EV-12 计数与 disposition 措辞更正；
           EV-13 报告 commit 入库 + 补 Document/Authority/安全抬头 + diag_ir.py 改读 .env +
           处置遗留 producer 冗余副本（至少消除空壳 resolver_ref_r52 的误认风险）。

OD-E2E-D7  闭合效力（DSH 立场，供 Owner 参考）
           已独立确认为真：Frozen Spec 6/6 SHA256 与 subtree 14a74508… 未变；v3 0 个 modified
           tracked file；Papers HEAD/remote/clean；166 manifests；golden fixture 全部字段与 SHA 命中；
           resolver IR 71 ADMITTED 结构正确；runner 11 项指标命中且重放逐字节一致；
           DB 12/12 行数命中 + seal 链（sealed/native/1198/valid）+ 26 表；
           questions=0 / question_instances=0 / materials=0 为真。
           ⇒ 报告的 PARTIAL / FIRST BLOCKING POINT / 「Question 未持久化」等核心判定
             **成立，不因 EV-01~EV-13 而改变**。
           EV-01~EV-13 均属「表述归属 / 治理定位 / 既有证据衔接」层，不阻断核心结论。
           若 Owner 愿以此收束，可将其全部记为 accepted residual 并将本轮报告作为该 E2E 活动的
           正式记录（但 D2 的 Phase/STOP 定位建议先裁，因其影响在册治理文档的有效性）。
```

---

## §5 方法与限制（含 DSH 未做之事）

**方法**：只读取证。所有结论以命令重算为准，不以报告文字为准。

**DSH 实际执行**：
`git`（status/log/rev-parse/ls-files/check-ignore/ls-remote 等价物）· 逐行读取 v3 源码 ·
`Get-ChildItem`/`Get-FileHash` 语料与 artifact 计数 · 166 份 manifest 与 88 条 resolver IR 的 JSON 解析重算 ·
JSON 报告字段复算 · `docker exec … psql` **只读 SELECT**（12 项行数 + seal 状态 + `information_schema` 表数）。

**DSH 刻意未做（及原因）**：

1. **未重跑测试套件** —— §3 的 2 032 项无法在不触发 `test_task_executor.py` 破坏性全表 `DELETE`
   的前提下复核；重跑会销毁共享库现有状态。故 §3 的「2 030 passed」在 DSH 侧为 **UNVERIFIED**
   （报告自身的证据使其不可独立证伪）。
2. **未修改 AITutors-v3 任何文件、任何未跟踪文档**（`0 modified` 由 DSH 独立复核，审查前后一致）。
3. **未写数据库** —— 全部为 `SELECT`；审查前后 12 项行数一致。
4. **未修改** `E2E-VERIFICATION-REPORT.md`、`MIMO-PREPROCESSING…md`、`e2e_run/**`、
   `Docs/GOVERNANCE/**`、`Docs/COORDINATION/CONTRACTS/**` 任何内容。
5. **未裁决** EV-01~EV-13 的性质与处置 —— 全部列入 Owner 决策清单。

**UNKNOWN / 不可核验项（保留，不 silent skip）**：

| 项 | 状态 |
|---|---|
| 仓外任务书正文（被引用的 `§18 BUG FIX POLICY`、`§22`、以及「允许修复明确、局部、可证明的 implementation bug」原句） | **UNKNOWN** —— 不在任何仓内；报告的全部「为何未修」论证建立其上 |
| 仓外任务书是否要求了 §3 全量测试、§8 Case A–E、§12 API 表 | **UNKNOWN** |
| 是否另有第二个 uvicorn 实例服务了 §12 行 5–8 | **UNKNOWN**（EV-07 的限制） |
| `--allow-live` 尝试的原始命令与拒绝来源 | **UNKNOWN** —— 仅见于 Owner 侧任务回报，artifact 中无记录（正是 EV-05） |
| MIMO 报告 `:412-418` 的 X2.7 全量运行数字（172 manifests / 533 leaves / 178 materials） | **DOCUMENT CLAIM** —— DSH 未复算该次运行 |
| server-side push / 权限分类器日志 | **UNKNOWN** |
| `AITutor-X` 其余 16 份 untracked 报告（`X2-*`、`REPORT-G/H/I/K`）与本次活动的关系 | **未审查**（不在本任务范围）；其中 `MIMO-…` 因与主体直接相关而读取 |

---

## §6 结论

```text
VERDICT: ACCEPTED WITH FINDINGS

执行证据层面：本链迄今最强 —— 12/12 DB 行数、6/6 Frozen Spec SHA256、核心代码引用、
  golden fixture 全字段、runner 11 项指标、重放逐字节一致，全部由 DSH 独立复现。
  代码引文无一处内容伪造；DB 为独立连库实测而非自述转抄。

表述与治理层面：三项不达标，均为本链反复围剿的同一缺陷类
  （unsourced / mislabeled current-state assertion）：
  · 输入规模与语料范围数字归属错误（88 074 / 472 / 58 —— EV-01, EV-02, EV-09）
  · 全文未对 LIMIT-AUTH §5 STOP / §6 Forbidden / §4 Phase 做自检，且与 2.5 小时前
    刚闭合的 OD-R-01 收口记录边界表「Phase 6 NOT entered」相冲突而未调和（EV-03, EV-04）
  · 自行选择 --allow-live 的越权尝试未在 artifact 中披露，且 §13.3 的
    「未发现 AUTHORITY VIOLATION」未覆盖该事实（EV-05）
  · 未引用仓内既有同类独立验证（MIMO 2026-09-22，952 行，同一组 gap，规模大 172 倍），
    并与其在 material 可达性与 DEFECT-002/003 定性上冲突未调和（EV-06）

核心判定不受影响：PARTIAL / FIRST BLOCKING POINT（IR validation "options missing
  for choice type"）/ FIRST ARCHITECTURAL BLOCKING POINT（Admission 未接线 + 无条件 rollback）/
  questions=0 · question_instances=0 · materials=0 —— 全部成立。

待 Owner 裁定：OD-E2E-D1 ~ D7。
```

---

*End of independent adversarial review. DSH 不裁决，仅报告发现与 Owner 决策清单。*
