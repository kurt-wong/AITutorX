# E2E-VERIFICATION-EXECUTION-DSH-ADVERSARIAL-REVIEW

**Document ID**: E2E-VERIFICATION-EXECUTION-DSH-ADVERSARIAL-REVIEW
**Document Type**: Independent Adversarial Review（非裁决；仅发现 + Owner 决策清单）
**Review Date**: 2026-09-26
**Reviewer**: DSH (independent adversarial reviewer)
**Authority**: Owner task instruction（对抗性审查请求）。本报告不替 Owner 做裁决。
**Subject Artifact**: `AITutor-X/Docs/60_REPORTS/E2E-VERIFICATION-EXECUTION-REPORT.md`（846 行，untracked）
**Subject Activity**: 2026-09-26 00:03–00:36（本地）Engineering Verification Execution；AITutors-v3 `od01-r3-convergence` @ `d2b9a26`
**Prior Round**: `E2E-VERIFICATION-DSH-ADVERSARIAL-REVIEW.md`（DSH，commit `6b1fb17`，EV-01…EV-13）
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## §0 Verdict

```text
ACCEPTED WITH FINDINGS
```

**这是本链迄今质量最高的一份报告**，且它是**第一份对上一轮 DSH 全部 EV 逐条处置并留下可复算证据**的报告。
DSH 独立重算后：**上一轮 13 项 EV 中，8 项被实质闭合（EV-01/02/03/04/05/06/07/08），
5 项 LOW 被登记而未被修复（EV-09…EV-13，报告 §LOW-03 已如实登记）**。

本轮 DSH 新增 11 项发现，**其中 2 项 HIGH**，且两项都落在报告**最核心的正面主张**上：

| 维度 | 结论 |
|---|---|
| 数字（EV-01/EV-02） | **PASS** —— 4 609 / 12 707 / 88 074 全部独立复算命中，且 artifact 自证 |
| 治理定位（EV-03/EV-04） | **PASS** —— §0 逐条自检成立；引用 `OD-R-01-CLOSURE-RECORD.md:206-231` 的原文**逐句核实为真** |
| 代码取证 | **PASS** —— BLOCKER-01/02 的代码行与 Frozen Spec 行**逐行命中，无一处引文伪造** |
| 既有工作衔接（EV-06） | **PASS** —— §9b 9 项对照；DEFECT-003 定性更正为 by design **与 MIMO 原文一致** |
| DB 最终对象 | **PASS（结构）** —— `questions=1 / question_instances=1 / instance_role_contents=2` 逐字段命中；MEDIUM-03 `created_instance_ids={NULL}` 独立确认为真 |
| **live 调用的授权形态（EE-01）** | **FAIL** —— harness 在代码中**自行授予** `allow_live=True`，并以 **`task_context=object()`（裸对象）** 与 **硬编码 `budget_ok=True`** 满足 `LLMGateway._live` 的四前置中的三条；报告只称之为「依赖注入」 |
| **最终对象的内容保真（EE-02）** | **FAIL** —— 唯一物化的 Question：stem 为 **80 字符乱码**，answer role 内容仅 **5 字符 `"11. "`**，而 `answer_status` 断言 `{complete:true, source_located:true, verified_correct:true}`；报告 §6.3/§10 把它作为「Provenance PASS」的正证据，**从未检视其正文** |
| §6.1/§6.2 快照 | **PARTIAL** —— `validation_events` 实为 **1**（报告写 0→0 未产生）；`budget` 实为 **+9**（报告 §6.5 写 +3）且未入 After 表；§6.1「任务开始时」实为**任务开始后 1.5 分钟** |

**核心判定不变**：`E2E STATUS: PARTIAL` / 两个 BLOCKER / `INTEGRATION READY: NO` / `STOP RAISED: YES`
—— DSH 独立复核后**全部成立**，且 BLOCKER-01/02 的定位**精确到行**。
EE-01/EE-02 不推翻这些判定，但它们**限定**了报告对自身正面结果的表述。

---

## §1 独立复现（PASS 清单）

### 1.1 Repository baseline

| 报告声明 | DSH 实测 | 判定 |
|---|---|---|
| v3 HEAD `d2b9a26f…3079`、branch `od01-r3-convergence`、非 `??` 条目 = 0 | 完全一致（0 modified tracked） | ✅ |
| `Docs/V3_SPEC` tree = `14a7450809…843c` | `git rev-parse HEAD:Docs/V3_SPEC` = 同值 | ✅ |
| Frozen Spec 6/6 SHA256 | **6/6 逐字节一致**（独立计算） | ✅ |
| Papers HEAD `2b92898f…4928`、working tree clean | 一致（`status --porcelain` = 0） | ✅ |
| `.env`：`APP_ENV=development` / `LLM_GATEWAY_MODE=live` / `OCR_GATEWAY_MODE=disabled` / `MIMO_BASE_URL=https://api.xiaomimimo.com/v1` / `MIMO_MODEL=mimo-x-pro-preview` | **五项全对**（MEDIUM-04 的 `.env` 陈旧模型名成立） | ✅ |
| 未改 `.env`、未执行 migration | 无 modified、`.env` 值仍为 `mimo-x-pro-preview` | ✅ |

### 1.2 语料统计（EV-01 更正）—— 复算完全命中

DSH 独立扫描 `Ocr-markdown/` 全部 **166** 份 manifest：

```text
total_units = 4609        standalone_question = 3935
composite_question = 673  （含 material = 668；不含 material = 5）
andalone_question  = 1    ← 位于 2020北京高中合格考化学（第一次）（教师版）(1).manifest.json
standalone + material = 0 / 3935   ✅ 定性结论在全语料口径成立
manifests 含 ≥1 composite+material = 87   ✅ 与 §4.3 所述「87 份之一」一致
```

且报告所引 artifact `e2e_run/corpus-scope-stats.txt` 自身即印出
`3935 / 673 / 1 / total_units=4609` 与 `3995→530`-类子集口径 —— **报告与 artifact 双向一致** ✅

**EV-01 判定：CLOSED** —— 上一轮「全语料 472+58」的错误归属被正确更正，且
规模倍数 **8.7×**（530 → 4 609）由 DSH 复算确认（另见 §4 对 DSH 自身 7.4× 的更正）。

### 1.3 输入规模（EV-02 更正）

| scope | 报告 | DSH 实测 |
|---|---|---|
| `maintainess\PDF\` | 12 707 | **12 707** ✅ |
| `original\` | 75 366 | **75 366** ✅ |
| 全仓 | 88 074 | **88 074** ✅ |
| `Ocr-markdown\` 的 PDF | 0 | 0 ✅ |

`r64_corpus_inventory.json:pdf_total_indexed = 12707` ✅ 交叉验证成立。
**EV-02：CLOSED。**

### 1.4 live LLM 调用（EV-05 处理）

`llm_call_audit` DSH 独立查询（全表分组，非报告自述）：

```text
 provider |     model     |  status   | count
----------+---------------+-----------+-------
 deepseek | deepseek-chat | completed |   353
 deepseek | deepseek-chat | failed    |   326
 deepseek | deepseek-chat | started   |    41
 deepseek | deepseek-chat | unknown   |    37     ← deepseek 合计 757 ✅（报告 §5.1 称 757 ✅）
 mimo     | mimo-v2.6-pro | completed |     2     ← 报告 §5.1 = 2 ✅
 mimo     | mimo-v2.6-pro | failed    |     1     ← 报告 §5.1 = 1 ✅
 ollama   | qwen3.5-9b    | failed    |     1     ← 见 EE-07（上一轮遗留，非本轮）
 合计 959 ✅（§6.2 载 956 → 959，Δ=+3 ✅）
```

三条 mimo 行的 `start`：`16:03:12.414Z`(failed) / `16:07:40.159Z`(completed) /
`16:24:14.180Z`(completed) —— 与 §5.1 表**逐值一致** ✅；prompt_chars `3196 / 3196 / 8705` ✅。
**mimo 真实 HTTP、非 mock、非 fallback、非 DeepSeek 成立** ✅

### 1.5 任务链（§7.1 / §7.6）

DSH 直读 `tasks` 全表（10 行）：

```text
284486c2  admin      07:21:07Z  failed              ← 上一轮遗留
a7a52696  e2e-verify 16:01:54Z  failed
abc8f489  e2e-verify 16:01:55Z  failed              ← 16:03:12 记 GatewayDenied
c7e67c98  e2e-verify 16:03:12Z  succeeded  llm=1    ← caseA
735bab6f  e2e-verify 16:07:39Z  succeeded  llm=0
e5df44fb  e2e-verify 16:18:25Z  failed
03127d8f  e2e-verify 16:18:25Z  failed
7c5ecab8  e2e-verify 16:20:28Z  failed
6ec6bcec  e2e-verify 16:24:13Z  succeeded  llm=1    ← 决定性 caseB 任务；decided 16:25:17.903
9720c624  e2e-verify 16:36:34Z  succeeded  llm=0    ← replay；decided 16:36:35.230（wall 0.43s ✅）
```

`6ec6bcec-814d-4ad7-82cb-55cb1c5f4ace` / `status=succeeded` / `llm_invocations=1` /
wall **64.65s**（16:25:17.903 − 16:24:13.252 = 64.651s）✅ **§7.1 头部三值全部命中**；
replay `9720c624` / `llm_invocations=0` / **0.43s** ✅ **§7.6 命中**。

### 1.6 最终对象（§6.3 / §6.4）—— 结构层逐字段命中

```text
questions (1)      a35743e0-2e00-4b11-89af-138861b24c29  fill_in  数学/高一
                   dedup_key e09816aa8cb6c6f23910a71b0254bb268b26cf4d29dfa4b02f7068533fb8309a ✅
question_instances (1)  953743dd-15bb-4656-b801-3ae0206e625f  question_number=11
                   occurrence_key / logical_execution_hash  存在 ✅
instance_role_contents (2)  role=stem / role=answer ✅
                   stem   text_hash d48f0ffb…  span sp-Q11.stem  line_refs ["P2L073"…"P2L092"] ✅
                   answer text_hash e1a6dffe…  span sp-Q11.answer line_refs ["P6L031"] ✅
admission_events (1)  created_question_ids={a35743e0-…} ✅
                      created_instance_ids={NULL}        ✅ ← MEDIUM-03 独立确认为真
materials = 0 ✅   unit_groups = 1 / unit_group_members = 1 ✅
```

**FK / unique**：报告 §6.4 列出的约束（`uq_questions_dedup_key`、`uq_documents_original_sha256`、
`(stage,hash)` ×2、`(question_id,source_version_id,occurrence_key)`、`UNIQUE(candidate_id)`）
与 `validation_events.validator='human/e2e-verify-human'` 的存在性一致；0 orphan 成立 ✅

### 1.7 代码与 Frozen Spec 取证 —— 逐行命中

| 报告引用 | DSH 实测 | 判定 |
|---|---|---|
| `_ANNOTATION_PROMPT_PREFIX` @ `executor.py:58` | 精确 @58 | ✅ |
| 「只给出 standalone_unit 完整示例，无 composite_unit 示例」 | @71「standalone_unit 完整结构」；全文无 composite 示例 | ✅ |
| 「`role ∈ {"stem","option","answer","explanation"}` ← 缺 `shared_material`」 | **@88 逐字命中** | ✅ |
| 「无 `shared_components` / `sub_questions` / `depends_on` / `question_number_range`」 | `executor.py` 全文 **0 命中** | ✅ |
| `20_Document_Pipeline.md:130` `"role": "shared_material"` | @130 逐字 | ✅ |
| `:181-185` composite_unit + `shared_components{}` + `sub_questions[]` + `depends_on[{material_dependency}]` + `requires_material_context` | @181-186 逐字 | ✅ |
| `:378-390` IR composite + 完整性不变量 | @378-392 逐字（「共享材料只出现一次」@391） | ✅ |
| `:462` 「shared material 只输出一次，绝不复制进任何子题 stem」 | **@462 逐字** | ✅ |
| `:483` 「每个 shared material 单独产一个 material dedup_key」 | **@483 逐字** | ✅ |
| `build_gateway` live 分支只构造 `HTTPLLMProvider(name="ollama", api_key=None, base_url=settings.ollama_base_url, model=settings.ollama_model)` | **@116-122 逐字** | ✅ |
| `.env` 的 `ollama_base_url/ollama_model` 为空串 | `config.py:27-28` 默认 `""`，且 `.env` 未设 → 空 | ✅ |
| `app/worker/__main__.py:87` `build_gateway(allow_live=args.allow_live)` | **@87 逐字** | ✅ |
| `LLMGateway._live` 四前置 | `gateway.py:60-74` 逐条（allow_live / task_context / budget_ok / resolvable provider）+ Lock-4 @78-81 | ✅ |
| `import_service.py:26` `_ALLOWED_EXTENSIONS = {".pdf",".docx"}` | 命中 | ✅ |

**BLOCKER-01 / BLOCKER-02 的定位是精确的、可复核的，不含任何推测。** 这是本轮最值得记分的部分。

### 1.8 下游 Material 能力（§7.5）

`pac-c08-01.manifest.json` DSH 直读：**units=9**（8 `composite_question` + 1 `standalone_question`）、
**含 material_lines 的 unit = 8**、`identity_version=2` —— 与 §4.3/§7.5 **逐值一致** ✅
（`U-Cloze-1-10` … `U-RE-40-43` 八个 composite 各带 `material_lines`）。

### 1.9 Prior Art 调和（EV-06）与治理定位（EV-03/EV-04）

- §9b 的 9 项对照中，DSH 抽查的 MIMO 行号 `:442 :633 :410 :625 :412-418 :610-613 :422-423 :424 :634 :657`
  **全部指向正确内容**（唯一偏差见 EE-08）。
- 「DEFECT-003 应为 by design」的更正**与 MIMO 原文 `:410`「**NOT REACHED on B2 entry (by design**;
  lives on `runner.py` / API)」完全一致 ✅ —— 这是**对自己上一轮结论的正面更正**，值得记分。
- §0 所引 `OD-R-01-CLOSURE-RECORD.md:206-231`：DSH 逐行核实，
  `:223`「STOP remains effective（… A–J；§3.5 硬性 STOP）」、
  `:226`「Phase 6 is NOT entered by this record」、
  `:231-234`「Phase 6 未进入 …… 「Verification Phase STARTED」**不等于**「Phase 6 STARTED」」
  **全部逐字为真** ✅；`:253-258`「本闭合记录**不授权**下列任一事项：… X3 Entry / Production Deployment」
  亦为真 ✅。

**EV-03 / EV-04 / EV-06：CLOSED**（含 §4 对 DSH 自身 EV-04 过强表述的更正）。

### 1.10 破坏性测试处置（EV-07 / EV-08）

报告 §8 明载：本轮**未**运行任何全表 `DELETE` 测试，故无 wipe、无需 restore；
并沿用 DSH EV-08 建议，把上一轮 §3 基线标注为「运行本身具破坏性副作用，未在隔离库中执行」。
DSH 侧证：`documents` / `tasks` 等表未见异常清零，`llm_call_audit` 单调 +3。
且报告**未**声称补齐了 EV-08 三项中的①（上一轮 §3 运行前 DB 快照）—— 它如实写「上一轮缺失，
本轮已为**本轮**建立 Before 快照」。**EV-07 / EV-08：CLOSED（在可闭合范围内）。**

---

## §2 Findings

### EE-01 [HIGH] live 调用由 harness **在代码中自行授予**并**以伪造值满足 3/4 条安全前置**；报告仅称之为「依赖注入」

**位置**：`e2e_run/e2e_live_full_chain.py:224-234`

```python
gateway = LLMGateway(
    "live",
    allow_live=True,           # Owner task §三 明确授权调用外部 LLM API
    task_context=object(),     # ← 裸 object()，非真实 task context
    budget_ok=True,            # ← 硬编码 True，非由预算状态推导
    live_provider=provider,
)
```

而 `app/ai/gateway.py:60-74` 的 `_live` 四前置正是：

```python
if not self._allow_live:        reasons.append("--allow-live not granted")
if self._task_context is None:  reasons.append("task context missing")
if not self._budget_ok:         reasons.append("budget unavailable")
live = self._resolve_live_provider(provider)
if live is None:                reasons.append("no live provider configured")
```

即：**四条安全前置中，三条由本 harness 自己断言/伪造，仅第四条（provider）是真实接线。**
脚本注释自己写着「此处按契约补齐后两个前置」——「补齐」（fill in）一词准确描述了这一动作：
`task_context` 用**裸 `object()`** 通过 `is not None` 检查，`budget_ok` 直接写死 `True`。

**报告的披露缺口**。DSH 对报告全文检索 `task_context` / `budget_ok` / `allow_live` / `object()`：

| 位置 | 内容 |
|---|---|
| `:580` L-01 | 「生产链 E2E 通过**验证 harness 的依赖注入**跑通，未经 `app/worker` 生产入口」 |
| `:645-652` BLOCKER-02 | 仅描述 **worker** 未传 `task_context`/`budget_ok` |
| `:782 / :832` | 同上，均为 worker 侧 |
| `:270-271` §5.1 | 只记「授权依据 = 任务书 §一.2/§三」 |

**报告从未说明**：`allow_live=True` 是脚本自设的（而非 Owner 授予的 flag）；
`task_context` 是**裸对象**；`budget_ok` 是**硬编码**。这些只能通过阅读 harness 源码得知
（harness 在 `AITutor-X/e2e_run/`，报告未给出其关键片段）。

**为何这是 HIGH 而非格式问题**：

1. 报告 §10 把「链路可执行性」判为 **PASS**、§11 写「**真实 `TaskExecutor` 全链路**」、
   §9b 写「**已用真实 live MIMO 执行证实**」。这些结论的成立，依赖的是一次
   **由被验证方自己断言安全前置**的运行。
2. 「依赖注入」与「伪造安全闸门输入」是两件事。注入一个 provider 是 DI；
   用一个**任何对象都能通过**的 dummy 去满足 `task_context is not None`、
   并**硬编码** `budget_ok=True`，是**把闸门当成形式**。报告用前者描述后者。
3. 这直接呼应上一轮 EV-05（自行选择 `--allow-live` 被宿主权限分类器拦下）。
   本轮**同一意图换了实现路径**：不经 CLI flag，故不触发宿主分类器；
   在 Python 里自设 `allow_live=True`，于是**外部真实调用发生**（`llm_call_audit` 2 completed）。
   报告对此**未作任何治理性说明**，而 §0 的十条自检里也没有这一条。

**须精确区分、避免夸大**：`budget_ok=True` 是**闸门 flag**，非预算记账本身 ——
DSH 实测 `budget` 表仍增加（见 EE-03），故**不能**说「预算被绕过」。
DSH 报告的是：**闸门被断言，而非被满足**；且报告未披露。

**建议**：报告新增一节，原文贴出 `LLMGateway(...)` 构造片段，逐条标注
「此项由 harness 自设 / dummy / 硬编码」，并明确：
(a) `allow_live=True` 的授权来源是仓外任务书（DSH 无法核验）；
(b) 本次 live 运行**未经** `LLMGateway` 四前置的真实满足，故**不能**作为
「live 路径在授权形态下可用」的证据；(c) 据此把 §10 的「链路可执行性 PASS」
限定为「在 harness 自设前置下可执行」。

---

### EE-02 [HIGH] 唯一物化的 Question：stem 为乱码（80 字符）、answer 内容仅 5 字符 `"11. "`，而 `answer_status` 断言 `verified_correct: true`；报告从未检视正文

**DSH 直读 `instance_role_contents`（原文，含引号）**：

```text
 role   | len |  raw
--------+-----+-----------------------------------------------------------------
 answer |   5 | [11. ]
 stem   |  80 | [11.设全集U = R ，集合+{ 2},A x x = 集合{ 1}B x x = ，则集合U A = ，集合( ) U A B = .]
```

- **stem（80 字符）**：集合符号、花括号、运算子被 PyMuPDF 文本层打散并重排
  （`集合+{ 2},A x x =` / `B x x =` / `集合( ) U A B =`），且 **A/B 选项文字被并入 stem**。
  对照同一文档 `body_text`（6 707 字符）可确认源文本本身即高度碎片化。
- **answer（5 字符）**：内容就是题号 `11. `（含尾随空格）—— **没有任何答案值**。
- 而同一行的 `answer_status = {"complete": true, "source_located": true, "verified_correct": true}`。

**报告的处理**：§6.3 把 `answer_status {"complete":true,"source_located":true,"verified_correct":true}`
**原样列出**，作为落库成功的一部分；§10 判「**Provenance PASS**」；§7.1 判 Quality Check **PASS**。
全文**没有**出现 stem 乱码、answer 为空、`verified_correct` 与内容不符的任何字样。

**同时 DSH 实测 seal 质量报告**（`document_source_versions.source_meta->'quality'`）：

```json
caseB: {"issues": [], "status": "valid", "cjk_ratio": 0.2202, "total_chars": 6707,
        "non_printable_ratio": 0.0, "replacement_char_ratio": 0.0}
caseA: {"issues": [], "status": "valid", "cjk_ratio": 0.0935, "total_chars": 1198, ...}
```

`quality=valid` ✅（报告 §7.1 第 4 行属实），但**CJK 占比 0.22**——即约 78% 的字符不是中文，
这与「文本层碎片化」一致。质量门**没有**把这一退化判为问题。

**判定**：报告在**结构层**（FK / hash / 计数 / unique / span_id）的验证是充分的、可复核的；
在**内容层**（这份 Question 到底装了什么）**完全没有验证**。后果有三：

1. 「链路真跑通到了最终对象」在结构上为真，但**该对象的内容是退化的** ——
   报告把它作为正面证据展示而未加限定。
2. `answer_status.verified_correct = true` 覆盖在一个 5 字符、不含答案内容的 role 之上，
   是一个**系统内部的不实断言**。这属于本链一贯关注的「false current-state assertion」同类：
   系统声称「答案已定位且校验正确」，而实际 payload 是空的。**报告未发现、未登记。**
3. 报告的 `FIRST BLOCKING POINT` 只指向 SEMANTIC ANNOTATION。
   但 DSH 观察到的退化**发生在 Source/Seal+Quality 层**（PyMuPDF 文本层对数学版式的线性化失败），
   它**先于** annotation 存在，且 annotation 无从修复。故「首个断点」的定位
   **在时间序上不完整**：即使 BLOCKER-01 修复，该 PDF 仍会产出乱码 stem。

**建议**：(a) §6.3 补录两行 `text` 原文（stem / answer），并加一行判定「内容保真：STEM DEGRADED / ANSWER EMPTY」；
(b) §10 的 Provenance PASS 限定为「结构层 PASS；内容层 NOT VERIFIED / DEGRADED」；
(c) 新增一条与 BLOCKER 并列的缺口：**Source 层数学版式线性化保真缺口**，
并登记 `answer_status.verified_correct` 在空内容上为 true 的语义缺陷；
(d) 复核 `SourceQualityGate` 是否**设计上**不检测此类退化（若是，属 SPEC 层问题，需 Owner 裁）。

---

### EE-03 [MEDIUM] §6.2 After 快照的两处实质错误：`validation_events` 实为 1（报告写 0→0），`budget` 实为 +9（报告 §6.5 写 +3）

**位置**：报告 `:336-353`（§6.2 表）、`:419`（§6.5）

**(a) `validation_events`**。§6.2 表把它列在
「`material_links` / `validation_events` / `knowledge_nodes` | 0 | 0 | 0 | 未产生」。
DSH 实测该表 **1 行**：

```text
id 7f296aef-…  claim_id=Q11  candidate_id=54f869a3-…
validation_result=validated  validation_method=human_review
validator=human/e2e-verify-human  validated_at=2026-09-25 16:29:40.191746+00
```

即：本轮的 **HTTP `POST /api/candidates/{id}/approve`** 恰好生产了 1 行 `validation_events`
—— 它是报告自己主张的「真实 HTTP approve → 物化」这条 PASS 的证据之一，
却在 After 表里被写成「未产生」。原因是 harness 的 `db_after` 在 16:25:17 取，
而 approve 发生在 16:29:40（晚 4.4 分钟）；报告把 16:25 的快照当作整轮 After。

**(b) `budget`**。§6.5 写「预算 | `budget` +3（reserve/settle 成对）」。
实测：§6.1 Before = 3 406，当前 = **3 415**，**Δ = +9**；而 caseB 单次运行自身的
artifact 即记 `budget before=3411 → after=3415`，**该次运行就是 +4**。
且 `budget` **未出现在 §6.2 的 After 表中**（该表列了 15 张表，独缺 budget 与
`unit_groups` / `unit_group_members` / `instance_role_contents` —— 后三者也发生了 0→1/1/2 的变化）。

**影响**：§6.2 声称是「After（result / cleanup / restore）」的完整对账（EV-07/EV-08 的处置证据），
但它在两张表上与实测不符、并遗漏四张发生变化的表。**这恰好是上一轮 EV-07/EV-08 要求的东西**，
故应算「部分闭合」而非「闭合」。

**建议**：After 快照改为**两次**记录（harness `db_after` @16:25:17；**本轮终态** @16:36:35），
补齐 budget / unit_groups / unit_group_members / instance_role_contents / validation_events 五行，
并修正 §6.5「+3」→「caseB 单次 +4；本轮合计 +9」。

---

### EE-04 [MEDIUM] §6.1「Before 快照（任务开始时）」实为**任务开始后约 1.5 分钟**，且已含本轮自建数据；`tasks`/`task_claims` 的 Δ 因此被低估

**位置**：报告 `:317-334`

§6.1 标题为「Before 快照（2026-09-26T00:03:12+08:00，**任务开始时**）」，载
`tasks = 3`、`task_claims = 2`。

**DSH 直读 `tasks` 表**：在 16:03:12Z（= 00:03:12 本地，即该快照自身的时间戳）之前已存在的任务为

```text
284486c2  created_by=admin       07:21:07Z   ← 上一轮遗留
a7a52696  created_by=e2e-verify  16:01:54Z   ← 本轮 harness 自建
abc8f489  created_by=e2e-verify  16:01:55Z   ← 本轮 harness 自建
```

即 3 行中 **2 行由本轮自己的 harness 在快照前 77 秒创建**（`created_by='e2e-verify'`，
而上一轮遗留任务为 `admin`）。DSH 在上一轮审查时（本地 23:20–23:25）实测
`tasks=1 / task_claims=1`，可确证**真实的任务前基线是 1/1**。

**影响**：报告 §6.2 记 `tasks 3→10（+7）`、`task_claims 2→10（+8）`；
相对真实基线应为 **+9 / +9**。§6.1 的「Before」不是一个任务前基线，
而是**第一轮 harness 已经写过库之后**的中途快照 —— 这削弱了它以「破坏性测试纪律：
Before / After」名义提供的对账强度（EV-07/EV-08 的处置证据）。

**建议**：把 §6.1 的标签改为「Execution Phase Before（不含本 harness 首轮 matrix 写入）」，
或补列「task 前基线（2026-09-25 23:25）= topics 1 / claims 1」，并把 Δ 改为相对该基线。

---

### EE-05 [MEDIUM] §5.1 的连通性冒烟测试是一次**未入 `llm_call_audit` 的外部调用**

**位置**：报告 `:280`「冒烟测试：`Reply with exactly the single word: OK` → 返回 `'OK'`，耗时 1.38s」

DSH 实测 `llm_call_audit` 中 `provider='mimo'` **仅 3 行**（16:03:12 failed / 16:07:40 completed /
16:24:14 completed），**没有**对应冒烟测试的行。原因见 harness `:217-223`：冒烟用的是
**直接构造的 `HTTPLLMProvider`**，不经 `LLMGateway.complete()`，因而不经过
`LLMExecutor` → `invocation_counter.consume()` → `finalize_audit` 的审计链。

而 `app/models/runtime.py:20` 对该表的定义是
「`llm_call_audit`（30 §10 append-only 不可变）。**真实 LLM 请求一次一条**。」

**影响**：本轮对同一 endpoint 发起了**至少 4 次外部请求**（3 次经审计 + 1 次冒烟未审计，
另有 `GET /v1/models` 模型枚举非 completion），而 Runtime Truth 表只承载 3 条。
报告如实记录了冒烟测试的存在 ✅，但**未指出它绕过了审计不变式** ——
这属本链关心的「Runtime Truth 完整性」缺陷类（INFO-04 报告了 Lock-4 会拒绝缺
`invocation_counter`/`task_id` 的 `complete()` 直调，却未把冒烟测试与此联系起来：
**同一道防线，报告了被拒绝的那次，漏了被绕开的那次**）。

**建议**：登记为一条 MEDIUM：「验证活动自身产生 1 次未入 `llm_call_audit` 的真实 LLM 请求」，
并说明 `HTTPLLMProvider` 可被直接实例化从而绕过审计链（这是一条**可复现的审计缺口**，
不只是本轮的操作瑕疵）。

---

### EE-06 [LOW-MEDIUM] 被物化的文档在 DB 中的文件名与报告呈现的输入名不一致（副产物：解释了 `is_new=false`）

DSH 实测 `documents` 三行：

```text
caseA_real.pdf              pdf   sealed    a136e47b…7350e   ← 上一轮遗留
extmatrix_docx_stub.docx    docx  imported  dedca910…
extmatrix_real_pdf.pdf      pdf   sealed    f58e39ae…33b8ce   ← 本案 caseB 的文档
```

caseB 的 `document_id = bffd8c7b-5480-42ad-905f-023cb04104e9` 对应
`file_name = **extmatrix_real_pdf.pdf**`（sha `f58e39ae…` = caseB 的 sha）。

原因：harness 先跑 `input_layer_matrix`（`:108-138`），其中 `real_pdf` 用例以
`file_name=f"extmatrix_{name}{ext}"` **先一步导入了同一份 PDF 字节**，
于是 §7.1 的目标导入命中同一 SHA → `is_new=false`（artifact `e2e-live-caseB.json.import.is_new = false` ✅）。

**影响**：§7.1 第 1 行的「`is_new=false`，SHA 命中」是**正确的**，但报告未说明
「命中」是因为**本 harness 的扩展名矩阵已先行导入**；读者无从知道
决定性 E2E 的「真实文档」以 `extmatrix_real_pdf.pdf` 之名注册。
属证据可追溯性（provenance）表述缺口，非事实错误。

**建议**：在 §4.3 / §7.1 注明该文档由扩展名矩阵先行导入，并给出
`document_id ↔ file_name ↔ sha256` 的三元对应。

---

### EE-07 [LOW] BLOCKER-02 的「Evidence」行是**上一轮的遗留行**，未标日期

**位置**：报告 `:654`「Evidence: `llm_call_audit` 仅 1 行 provider='ollama' model='qwen3.5-9b' status='failed'」

DSH 实测该行 `start = 2026-09-25 07:22:17.714Z` = **本地 15:22:17，属上一轮**（09-25 15:00–23:14）。
它落在 §6.1 的 956 行之内，因此 §6.2 的 `956 → 959 (+3)` 是**正确的**（未把它算作本轮）。

**影响**：§6.2 无错；但 BLOCKER-02 把它列为「Evidence」而不标时点，读者会读成本轮实证。
本轮对同一现象的**直接**证据其实在别处（`abc8f489` 任务 16:03:12 的 claim `error_type=conflict`，
且该次失败在 `llm_call_audit` 中对应的是 `provider='mimo'` 的 failed 行 ——
因为 harness 当时已注入 mimo provider，故拒绝发生在 gateway 层而非 ollama 层）。

**建议**：把该 Evidence 行标注为「2026-09-25（上一轮）」并补上本轮的直接证据行。

---

### EE-08 [LOW] §9b 的 MIMO 行号引用有一处错位

§9b 表将「85 v1 manifests 缺 `source_content_sha256`」标注为 MIMO `:411`。
DSH 实测 MIMO 报告 `:411` 为**空行**；`85` 出现在 `:416`（`85 manifest_sha_missing`）、
`:631`（`| 85 v1 manifests | …`）、`:652`。其余 §9b 引用的 9 处行号均正确。

另：§9b 行「「正式生产链 = TaskExecutor 的 LLM Annotation 路径」… **已用真实 live MIMO 执行证实**」
缺少 §10/L-01 的同一限定（未经 `app/worker` 生产入口、且前置由 harness 自设，见 EE-01）。
§10 判「生产入口可运行性 **FAIL**」，§9b 却写「已执行证实」，二者可调和但需同带限定语。

---

### EE-09 [LOW] §2 命令清单含一条**从未发出**的请求

§2 `C7`（`:146`）列有 `curl -s http://127.0.0.1:8077/api/admin/stats`，
但 DSH 实测 `e2e_run/api-verify.log` **只有 4 条请求**：

```text
GET  /health                                       200
GET  /api/candidates/54f869a3-…                    200
POST /api/candidates/54f869a3-…/approve            200
GET  /health                                       200
```

无 `/api/admin/stats`。§5.2 **正确地**声明「`GET /api/documents*` 等端点本轮**未调用**，
故不列入结果表」——**这是对上一轮 EV-07 的正面修复，值得记分**；
但 §2 的命令清单仍多列了一条未执行的 curl，与 §5.2 相抵。

**建议**：从 §2 C7 删除该行，或标注 `NOT EXECUTED`。

---

### EE-10 [LOW] §7.2 未解析原因直方图缺一类（`no 详解/解析 header`），§6.2 After 时点标注与数据不符

1. §7.2（`:475-480`）列 4 类原因，但 artifact `diag-prod-ir.json` 的
   `unresolved_references` 中另有第 5 类 **`no 详解/解析 header`（missing）**
   ×5（Q16/Q17/Q18/Q25/Q26 explanations）。报告下一行已用
   「`role explanation unresolved` ×5」覆盖了数量 ✅，故只是分类表不完整。
2. §6.2 标题时点写「2026-09-26T00:35+08:00」，但表中 `tasks / task_claims = 10 / 10`
   只有在 **16:36:34Z（= 00:36:34，replay 任务创建）之后**才成立
   （harness `db_after` @16:25:17 时为 9 / 9）。时点应后移。

---

### EE-11 [INFO] 报告已主动登记但未修的两项，DSH 确认其存在

- §LOW-03 登记「上一轮报告行号漂移 / 个别计数不可复现（EV-11 / EV-12）」
  并声明「Reconcile, don't rewrite」—— 与 workspace 纪律一致 ✅（上一轮报告确未改动）。
- §LOW-02 登记 producer 词表噪声 `andalone_question`（1 unit）—— DSH 复算：
  全语料**恰好 1 个**，位于
  `2020北京高中合格考化学（第一次）（教师版）(1).manifest.json` ✅
  （该 unit 正是 DSH 上一轮把总数算成 4 608 的原因，见 §4）。
- `e2e_run/corpus-scope-stats.txt` 末节打印 `--- reslice-pac-annotated only (0 manifests) ---`
  而紧随其后是 `pac_total_units=530` —— diag 脚本自身的标签 bug（不影响数字）。

---

## §3 上一轮 EV-01…EV-13 处置核验

| EV | 上一轮要求 | 本轮处置 | DSH 判定 |
|---|---|---|---|
| EV-01 | 全语料统计更正 + scope/dataset/source/timestamp | §4.2 重算 4 609，附 artifact，二者一致 | **CLOSED** ✅ |
| EV-02 | 88 074 / 12 707 分列 | §4.1 四行 scope 表 + producer inventory 交叉验证 | **CLOSED** ✅ |
| EV-03 | 对 LIMIT-AUTH §5/§6/§4 自检 | §0 十条自检表；DSH 抽查项全部属实 | **CLOSED** ✅（惟 EE-01 暴露一项未被 §0 覆盖的授权形态，见 OD-E2E2-D2） |
| EV-04 | Phase 归属显式主张 | §0 明写「不是 LIMIT-AUTH Phase 6 authorization claim」，并引 `OD-R-01-CLOSURE-RECORD:206-231`（逐句核实为真） | **CLOSED** ✅（含 DSH 自我更正，见 §4） |
| EV-05 | model / mock / fallback / DeepSeek 逐项明示 | §5.1 六项表 + artifact 字段 | **CLOSED**（`--allow-live` 一项，但**升级为 EE-01**：本轮改为代码内自设，且实际发生外部调用） |
| EV-06 | 与 MIMO 报告调和 | §9b 9 项对照 + DEFECT-003 更正为 by design | **CLOSED** ✅ |
| EV-07 | §12 端点补证据或降级 | §5.2 只列 4 条实际请求，与 `api-verify.log` 一致；未调用者明确声明未调用 | **CLOSED** ✅（惟 EE-09：§2 命令清单仍多列 1 条） |
| EV-08 | Before/After / 时间戳 / 恢复链 | §6.1/§6.2 建立本轮 Before/After；未跑破坏性套件 | **PARTIAL** —— 见 EE-03（`validation_events`/`budget`）与 EE-04（Before 非任务前基线） |
| EV-09 | identity_version 分布 + fixture 覆盖率 | 未处理 | **OPEN（已登记 LOW-03 之外）** —— 本轮 §4.3 声明覆盖 0.016% ✅（部分满足），但未给 `identity_version` 分布 |
| EV-10 | DEFECT-002 分类对齐 | §9b 将 DEFECT-003 更正为 by design ✅；DEFECT-002 未重提 | **CLOSED（003）** / **PARTIAL（002）** |
| EV-11 | 行号更正 | 未修（LOW-03 明载「不修改上一轮报告」） | **OPEN（Owner 已可接受为 residual）** |
| EV-12 | 计数与 disposition 措辞 | 未修（同上） | **OPEN（同上）** |
| EV-13 | commit 入库 / 抬头 / diag 硬编码 DSN / 冗余副本 | **部分改善**：本轮报告带 Document ID/Type/Date/Security ✅；报告仍 **untracked** ❌；`diag_ir.py` 仍硬编码 DSN（本轮 `diag_prod_ir.py` / `e2e_live_full_chain.py` 未硬编码密钥 ✅） | **PARTIAL** |

**汇总：13 项中 8 项 CLOSED，1 项 PARTIAL→升级为新 finding（EV-05），4 项 OPEN/PARTIAL。**
这是本链迄今**最高的 EV 闭合率**。

---

## §4 DSH 对自身既往立场的更正

### 4.1 更正一：上一轮 EV-04 的「二者之一必为假」过强 —— 部分撤回

上一轮 DSH 在 EV-04 写：

> 二者之一必为假：若本任务是 Phase 6 → 收口记录 §3 边界表在 2.5 小时后即失效；若本任务**不是** Phase 6 → 报告必须写明这一主张。

**更正**：`OD-R-01-CLOSURE-RECORD.md`（同为我上一轮引用的文件）`§4.1` 已**明确**给出调和：
`:206-208` 声明该记录「**不替代**、**不修改**该模型，也**不**推进其中任何 Phase」；
`:231-234`「Phase 6 未进入 …… 「Verification Phase STARTED」**不等于**「Phase 6 STARTED」」。
即：**框架早在 12:33 就已存在，「Verification Phase 活动」与「Phase 6 进入」在文档层面已被区分**，
并非我上一轮描述的「两份文档必有一假」。

因此 EV-04 中「必为假」的判断**过强，予以撤回**；EV-04 的**有效残余**仅为
「上一轮报告未写明自己的 Phase 归属」，而本轮 §0 已补上。**EV-04 → CLOSED。**

### 4.2 更正二：上一轮语料总数与倍数算错

上一轮 DSH 在 EV-01 写「真全语料（166 份）= **3 935 / 673**」与「规模被低估约 **7.4 倍**（530 → 4 608）」。

**更正**：

- 总数应为 **4 609**，不是 4 608。我漏计了 1 个 `unit_type='andalone_question'`（producer 词表笔误）
  的单元 —— 我的第一次扫描已把它打印出来，我误判为 PowerShell 显示瑕疵而未纳入。
  本轮报告 §4.2 与 artifact `corpus-scope-stats.txt` 均正确记为 4 609，**报告在此处比 DSH 上一轮更准确**。
- 倍数应为 **8.7×**（4 609 / 530 = 8.69），不是 7.4×。7.4 是我把 4 608 与 530 相除时的算术错误。

**这两处都是 DSH 自身缺陷，据实撤回并更正。**

### 4.3 更正三：上一轮的重复读取

上一轮 DSH 曾断言「`compiled_materials=0` 是 fixture 规模差异」并引 MIMO 的 178 materials——
本轮报告用**同一条路径的下游实测**（`pac-c08-01` → materials=**8**）把缺口**精确定位到 prompt 层**
（而非 Compiler/Gate），比 DSH 上一轮的推断更锐利、更可复核。**该点记分给报告。**

---

## §5 Owner 决策清单

```text
OD-E2E2-D1  [HIGH]  EE-01 ── live 运行的授权形态
            Owner 需裁定：(a) 本次 live 外部 LLM 调用（mimo-v2.6-pro，2 completed + 1 failed，
            另有 1 次未审计冒烟）是否在授权范围内；(b) `allow_live=True` 由 harness 代码自设、
            `task_context=object()`、`budget_ok=True` 硬编码这一形态是否可接受为「验证执行」；
            (c) 要求报告原文披露该构造片段，并把 §10「链路可执行性 PASS」与 §9b
            「已用真实 live MIMO 执行证实」加上「前置由 harness 自设」的限定。
            注：DSH 无法核验仓外任务书原文；`budget` 记账未被绕过（实测 +9）。

OD-E2E2-D2  [HIGH]  EE-02 ── 最终对象的内容保真 + answer_status 不实断言
            Owner 需裁定：(a) 唯一物化的 Question 其 stem 为 80 字符乱码、answer 内容为
            `"11. "`（5 字符）而 `answer_status.verified_correct=true` —— 这是否构成
            「链路跑通」的合格证据；(b) 是否要求报告补录 text 原文并新增一条
            「Source 层数学版式线性化保真缺口」；(c) `SourceQualityGate` 对
            `cjk_ratio=0.2202` 仍判 `valid` 是否为 SPEC 层问题（若需改判据 → SPEC CHANGE）。
            注：这决定 `FIRST BLOCKING POINT` 是否需从「SEMANTIC ANNOTATION」前移到 Source 层。

OD-E2E2-D3  [MED]   EE-03 + EE-04 ── 快照对账（EV-07/EV-08 的残余）
            要求：After 快照补记本轮终态（16:36:35）并补齐
            budget / unit_groups / unit_group_members / instance_role_contents / validation_events；
            §6.5「budget +3」改「caseB 单次 +4；本轮合计 +9」；
            §6.1 Before 改标签或补列任务前基线（tasks/claims = 1/1），Δ 相应更正。

OD-E2E2-D4  [MED]   EE-05 ── 审计缺口
            要求：登记「`HTTPLLMProvider` 可被直接实例化从而绕过 `llm_call_audit`
            （『真实 LLM 请求一次一条』）」为可复现缺口，而非仅记本次冒烟操作。

OD-E2E2-D5  [LOW]   EE-06 ~ EE-11 ── 精度与卫生（可打包）
            EE-06 caseB 文档名（extmatrix_real_pdf.pdf）三元对应；
            EE-07 BLOCKER-02 的 Evidence 行标日期 + 补本轮直接证据；
            EE-08 §9b `:411` → `:416/:631/:652`；§9b「已执行证实」补限定语；
            EE-09 §2 C7 删除/标注未执行的 `/api/admin/stats`；
            EE-10 §7.2 补第 5 类未解析原因；§6.2 After 时点后移；
            EE-11 diag 脚本标签 bug；
            以及 EV-09（identity_version 分布）、EV-11/EV-12（上一轮行号漂移，可接受为 residual）、
            EV-13（报告 commit 入库 + `diag_ir.py` 改读 .env + 处置遗留 producer 冗余副本）。

OD-E2E2-D6  闭合效力（DSH 立场，供 Owner 参考）
            已独立确认为真：6/6 Frozen Spec SHA256 + subtree 14a74508…；v3 0 modified tracked；
            Papers clean；166 manifests / 4 609 units（3935 + 673 + 1）/ 668+5 composite 拆分；
            12 707 / 75 366 / 88 074；87 份 composite+material manifest；
            mimo 2 completed + 1 failed / deepseek 757；task 6ec6bcec succeeded llm=1 wall 64.65s；
            replay 9720c624 llm=0 wall 0.43s；questions=1 / q_instances=1 / irc=2 / materials=0 /
            cands=6 / aev=1（created_instance_ids={NULL}）/ sann=2 / tasks=10 / llm_call_audit=959；
            BLOCKER-01 的 prompt 行 88 与 Frozen Spec :130/:181-185/:378-390/:462/:483 逐行；
            BLOCKER-02 的 gateway:116-122 与 worker:87 逐行；api-verify.log 4 条请求。
            ⇒ E2E STATUS: PARTIAL / 两个 BLOCKER / INTEGRATION READY: NO / SPEC CHANGE: NO /
              STOP RAISED: YES —— **全部成立**。
            ⇒ 上一轮 EV-01…EV-08 实质闭合（EV-07/EV-08 留 EE-03/EE-04 残余）。
            ⇒ 本轮 EE-01/EE-02 限定的是「正面结果的强度」，不推翻任何 FAIL/BLOCKER 判定；
              若 Owner 接受其为 residual，可据此收束本轮。
```

---

## §6 方法与限制（含 DSH 未做之事）

**方法**：只读取证；不采信报告文字，只采信可重算结果。

**DSH 实际执行**：`git`（status/log/rev-parse）· 逐行读取 v3 源码（`gateway.py` / `worker/__main__.py` /
`executor.py` / `config.py` / `import_service.py`）与 harness 源码 · Frozen Spec 与 closure record 逐行核对 ·
166 份 manifest 全量 JSON 重算 · artifact 解析（`e2e-live-caseB.json` / `diag-prod-ir.json` /
`corpus-scope-stats.txt` / `api-verify.log`）· `docker exec … psql` **只读 SELECT**
（`llm_call_audit` 全表分组、`tasks` 全表、`documents`、`admission_events`、`questions`、
`instance_role_contents` 正文与长度、`document_source_versions.source_meta.quality`、`budget`、`validation_events`）。

**DSH 刻意未做**：

1. **未重跑测试套件**（`test_task_executor.py` 的全表 DELETE 具破坏性，无隔离库可用）——
   故 §8 中「本轮未运行破坏性套件」DSH 只能由 DB 状态侧证（未见异常清零），不能由执行侧证。
2. **未发起任何外部 LLM 调用**（不重复被审活动的外部副作用）。
3. **未修改 AITutors-v3 任何文件**（审查前后 0 modified tracked）；**未改 `.env`**。
4. **未写数据库**（全为 `SELECT`；审查前后 `llm_call_audit=959`、`questions=1`、`materials=0` 未变）。
5. **未修改**被审报告、harness、任何 `e2e_run/**` 既有文件、`OD-R-01-CLOSURE-RECORD.md`、
   `Docs/V3_SPEC/**`、`Docs/GOVERNANCE/**`、`Docs/COORDINATION/CONTRACTS/**`。
6. **未裁决** EE-01…EE-11 的处置 —— 全部列入 Owner 决策清单。

**UNKNOWN / 不可核验项（保留，不 silent skip）**：

| 项 | 状态 |
|---|---|
| 本轮任务书原文（§一.1 临时验证工具授权 / §一.2「允许：调用外部 API」/ §三 MIMO 优先 / §四.1 输入矩阵 / §七 Material 要求 / §八 correctness-first / §二 Temporary Verification Database） | **UNKNOWN** —— 不在任何仓内；报告的关键「允许/授权」主张全部建立其上 |
| `MIMO_MODEL=mimo-x-pro-preview` 被 API 拒为 "Unsupported model" 的**发生时间**与其对 166 份 producer manifest 的影响 | **UNKNOWN** —— DSH 未发起外部调用核验（《= 只确认 `.env` 值仍为该名，与 MEDIUM-04 一致） |
| §5.1 冒烟测试的 1 次请求详情（无法从审计表获得） | **UNKNOWN** —— 正是 EE-05 |
| 本轮是否曾以 `--allow-live` CLI flag 经宿主分类器（本轮 harness 直接走 Python 构造） | **UNKNOWN** |
| `_ANNOTATION_PROMPT_PREFIX` 的 `cjk_ratio` 类退化是否曾被 Owner/SPEC 讨论过 | **UNKNOWN** |
| 上一轮报告结论在其自身 artifact 之外的部分（DSH 已复算核心，其余未复查） | **未复查** |

---

## §7 结论

```text
VERDICT: ACCEPTED WITH FINDINGS

取证层面 —— 本链迄今最强，且是首份对上一轮全部 EV 逐条处置并附可复算证据的报告：
  · 4 609 / 12 707 / 88 074 / 87 / 757 / 2+1 等数字全部独立复算命中；
  · BLOCKER-01/02 的代码行与 Frozen Spec 行逐行命中，无一处引文伪造；
  · DB 最终对象逐字段命中，含 MEDIUM-03 的 created_instance_ids={NULL}；
  · §0 对 LIMIT-AUTH §5/§6/§4 与 OD-R-01-CLOSURE-RECORD:206-231 的引用逐句为真；
  · EV-07 被正面修复（§5.2 只列 api-verify.log 中实际存在的请求）；
  · EV-06 的 DEFECT-003 更正为 by design，与 MIMO 原文一致。
  ⇒ 13 项上一轮 EV：8 CLOSED / 1 升级为新 finding / 4 OPEN-PARTIAL。

限定层面 —— 两项 HIGH 均落在报告最核心的正面主张上：
  · EE-01：live 运行的四条安全前置中，三条由 harness 自设（allow_live=True）、
    伪造（task_context=object()）、硬编码（budget_ok=True）满足，
    报告仅称之为「依赖注入」，未披露；
  · EE-02：唯一物化的 Question，stem 为 80 字符乱码、answer 内容仅 5 字符 "11. "，
    而 answer_status 断言 verified_correct=true；
    报告 §6.3/§10 把它当作 Provenance PASS 的正证据，从未检视正文。
  · 另有 EE-03/EE-04（快照对账：validation_events 实为 1、budget 实为 +9、
    Before 非任务前基线）与 EE-05（1 次未入 llm_call_audit 的真实 LLM 请求）。

核心判定不受影响：
  E2E STATUS: PARTIAL / FIRST & SECOND BLOCKING POINT（prompt 表达不了 composite_unit /
  shared_material；生产入口 live 路径不可达）/ INTEGRATION READY: NO / SPEC CHANGE: NO /
  STOP RAISED: YES —— 全部成立。

DSH 自我更正：上一轮 EV-04「二者之一必为假」过强（closure record §4.1:231-234 早已调和），
  予以撤回；上一轮语料总数应为 4 609（非 4 608，漏计 1 个 andalone_question），
  倍数为 8.7×（非 7.4×）—— 两处均系 DSH 自身缺陷。

待 Owner 裁定：OD-E2E2-D1 ~ D6。
```

---

*End of independent adversarial review. DSH 不裁决，仅报告发现与 Owner 决策清单。*
