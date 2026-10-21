# PHASE 1.2 — Real E2E Funnel & Replayability Verification

**Level**: LEVEL 1（诊断/测量，非功能开发）
**Date**: 2026-10-02（落盘校正；证据采集含 2026-09-30/10-02 运行）
**Scope**: 现有 DB 基线上的因果漏斗 + sealed 只读重放
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

**NOT-GO 已遵守**：未改 Frozen Spec / AnswerTokenContract / Authority；未修 Track B；
未扩 Admission 白名单；未引入 LLM；未清库；未改 preprocessing；未把未测数字写成已测。

---

## 0. 归因前提（必须先于漏斗读数）

### 0.1 分母：以 DB 9 个 source_version 为准

| 层级 | 计数 | 证据 |
|---|---:|---|
| E2E 语料文件 | 9 manifest + 9 md = 18 | `e2e_run/phase1_1_corpus_optspans/reslice-batch-C/会考/` |
| runner report papers | 9 | `phase1_1-huikao-report.json` `total_manifests=9` |
| **documents** | **9** | DB `documents` |
| **document_source_versions** | **9**（全部 `status=sealed`） | DB |
| semantic_annotations | 9（1:1） | DB |
| annotation `semantic_units` | **284** | 逐 payload 点算 |

**漏斗分母 = 284 annotation units（不是 35，不是 9）。**

### 0.2 「report 11 条」vs「document 9 行」差异解释

| 口径 | 值 | 含义 |
|---|---:|---|
| Ocr-markdown `reslice*` 目录**含 manifest** | **11** | **语料库盘点**（历史口径，见 `E2E-VERIFICATION-DSH-ADVERSARIAL-REVIEW`：「有 manifest 的 11 个」）。`reslice-pac` 无 manifest；故 12 个 reslice 目录 → 11 个有产出 |
| 本 E2E 运行 documents / source_versions | **9** | **本次运行**只消费 `会考/` 9 份试卷 |

**二者不是同一总体。** 11 = 全库可消费语料目录数；9 = 本次 E2E 落库文档数。
任何把 11 当作 funnel 分母的表述都是**口径混用**，本轮废止。

### 0.3 Resolver 工作树状态（漏斗数字的代码绑定）

```text
repo     : D:\Project\AITutors-v3
branch   : od01-r3-convergence
HEAD     : 39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4
worktree : M  backend/app/domains/resolver/match_normalization.py   (仅此 1 文件)

blob (worktree) : 015cdfa515ce23661ac1d9f02fb861869e111363
blob (HEAD)     : 73badc31fe94d4066f9e53469cb704b11ba8844b

MATCH_NORMALIZATION_VERSION = "match-norm/v1.1"   # 工作树，未提交
```

**变更内容（已读 diff）**：`normalize_text()` 剥离行首 Markdown `#`/`##` 标题记号。

> ⚠️ **本报告全部 funnel 数字绑定在上述 dirty worktree 上。**
> 在 HEAD（match-norm/v1）上重跑会得到不同 IR Ready（Phase1 实测：answer region 恒 missing → 接近 0 ready）。
> **不可**把 v1.1 数字表述为「39840ff 提交态」的可回归结果。

---

## 1. P0-A Sealed Source Read-Only Replay

### OBSERVED FACTS

对 DB 中 **9 个 sealed source_version + 9 个 annotation** 执行只读计算链：

```text
sealed source_version
  → SourceRepository.get_lines_by_version / get_figures_by_version   (SELECT)
  → semantic_annotations.payload                                     (SELECT)
  → SourceResolver.resolve                                           (纯函数)
  → IRBuilder.build                                                  (纯函数)
  → Compiler.compile                                                 (纯函数)
  → gate.policy.evaluate                                             (纯函数，仅对 ready units)
```

| 检查 | 结果 |
|---|---|
| 运行前 snapshot（13 表 count） | 见脚本输出 |
| 运行后 snapshot | **与运行前完全一致** |
| DIFF | **NONE** |
| append to sealed | **未尝试、未需要** |

读到的写路径边界（代码阅读，未执行）：

| 调用点 | 写？ | 说明 |
|---|---|---|
| `SourceResolver` / `IRBuilder` / `Compiler` / `evaluate` | 否 | 纯函数 |
| `GateService.run` | **是** | 内部 `create_admission_candidate` / `admission.approve` |
| `AdmissionService._materialize` | **是** | Question/Instance/Group |
| Track B `_create_source_records` | **是** | append → sealed **拒绝**（immutability） |

### RESULT-A

```text
READ_ONLY_REPLAY_SUPPORTED
```

**范围限定**：Resolver / Compiler / Gate-evaluate **计算重放**支持只读。
**GateService.run 整链不是只读**（会写 Candidate）。
Track B 的 sealed append 是**写路径**问题，与本结果**独立**。

证据：前后 13 表 count DIFF=NONE；9/9 pairs 可重算 IR。

---

## 2. P0-B Funnel Census

### 2.1 完整漏斗（实测）

```text
284  Input Units          annotation.semantic_units
 ↓
 35  IR ready             semantic_status == "ready"
249  IR incomplete        ≠ ready（不得计入 Candidate 失败）
 ↓
 35  Candidates           与 IR ready 1:1（损失 0）
 ↓
  1  Admission approved   auto_approve × 1
 34  pending_review       （Authority 边界，非 crash）
 ↓
  1  Questions            created
 ↓
  1  QuestionInstances    行存在
      admission_events.created_instance_ids = [null]  ← 记账缺陷，见 §2.6
```

| 箭头 | count | loss | loss categories |
|---|---:|---:|---|
| Units → IR Ready | 35 / 284 | **249** | 见 §2.2 |
| IR Ready → Candidate | 35 / 35 | **0** | — |
| Candidate → Admission | 1 / 35 | **34** | answer_grammar_fail 23；short_answer 9；fill_in 2 |
| Admission → Question | 1 / 1 | **0** | — |
| Question → Instance | 1 / 1 | **0** | 记账 [null] 为 audit 缺陷 |

**结论（事实）**：第一处大额损失在 **Units → IR**，不在 Admission，不在 Materialization。

---

### 2.2 P0-B.1 Input / Group Census

**OBSERVED**（annotation payload，非推断）：

```text
standalone_unit : 230
composite_unit  :  54
---------------------
total           : 284
```

composite 结构抽样：

```text
unit_type          = composite_unit
shared_components  = { material: ... }     # 54/54 有 material
sub_questions      = [1 个]                # 54/54 恰 1 子题
```

IR 侧：

```text
composite_unit  incomplete = 54 / 54
composite_unit  ready      =  0 / 54
```

DB `unit_groups` = **1**（standalone 那条 approved 物化产物），**0 条 composite group**。

**归因（阶段准确）**：

| 层 | composite 是否存在 | 证据 |
|---|---|---|
| annotation / adapter payload | **存在 54** | payload 点算 |
| IR | 54 全 incomplete | 只读重放 |
| Candidate / unit_groups | **0** | DB |

⇒ **不是 preprocessing 丢 group**（Producer/adapter 已声明 composite + material）。
⇒ **丢失点在 Unit → IR（Resolver material incomplete / IR incomplete）**。
⇒ 禁止归因到「preprocessing 没产生 group」。

未修任何层（NOT-GO）。

---

### 2.3 P0-B.2 IR Ready Census（实测，非沿用 35）

| IR status | standalone | composite | total |
|---|---:|---:|---:|
| ready | **35** | 0 | **35** |
| incomplete | 195 | 54 | **249** |
| **input** | **230** | **54** | **284** |

Unresolved reference 归因（Resolver 输出，Top）：

| role × status | count | 阶段 |
|---|---:|---|
| answer missing | 200 | Unit→IR |
| option incomplete | 197 | Unit→IR |
| stem missing | 69 | Unit→IR |
| material incomplete | 54 | Unit→IR（= 全部 composite） |
| option ambiguous | 40 | Unit→IR |
| stem ambiguous | 21 | Unit→IR |
| answer ambiguous | 15 | Unit→IR |

`semantic_status != ready` **已归入 Unit→IR**，未计入 Candidate 失败（纪律 §7）。

---

### 2.4 P0-B.3 IR → Candidate

```text
IR ready = 35
Candidate = 35
loss = 0
```

无 Gate reject / structural reject / duplicate 损失。

---

### 2.5 P0-B.4 Candidate → Admission

| category | n | 说明 |
|---|---:|---|
| auto_pass (approved) | **1** | `strict-auto: all answers verified_correct=true` |
| answer_grammar_fail | **23** | `answer not expressible as canonical value` |
| type_not_strict_auto:short_answer | **9** | grammar None by design（非 strict-auto 集合） |
| type_not_strict_auto:fill_in | **2** | 同上 |
| **pending total** | **34** | |

**子类标注（仅分类，不改契约）**：

| 子类 | 判定 | 本轮处理 |
|---|---|---|
| A Canonical | 1（已 approved） | — |
| B Deterministically extractable | **未测出 answer 正文**（payload 无 `text` 字段；仅 span 引用）→ **measurement_gap**，不得写成 YES/NO | 只登记 gap |
| C Ambiguous | 0（无该 reason） | — |
| D Missing | 0（无该 reason） | — |
| E Unsupported grammar / type | 11（short_answer+fill_in） | BY DESIGN pending |
| answer grammar（选择题非 token 形） | 23 | AnswerTokenContract **拒绝**；**未**扩白名单 |

---

### 2.6 P0-B.5–B.6 Admission → Materialization + `[null]`

**OBSERVED**：

```text
approved candidate 74390915-…  →  questions.id 2d0bf2f6-…
                                →  question_instances.id 818cb485-…  (行存在)
admission_events.created_question_ids  = [2d0bf2f6-…]     # 正确
admission_events.created_instance_ids  = [null]           # 错误
```

**Admission approved → Materialization = 100%（1/1）**
**Materialization → Instance 对象 = 100%（1/1 行存在）**

**`created_instance_ids=[null]` root_cause（代码路径，已定位，未改）**：

```text
content_repository.create_instance()
  = session.add(instance) + return instance     # 无 INSERT..RETURNING
                                               # 无 flush；id 仍 None

admission._materialize()
  instance = await create_instance(...)
  created_instances.append(instance.id)        # ← 取值时 id == None
  await flush()                                # id 此后才回填
```

对比 `create_question`：`pg_insert().returning(Question)` → id 立即有值 → `created_question_ids` 正确。

| 项 | 结论 |
|---|---|
| root_cause | **在 flush 前按值捕获 `instance.id`**；Instance 用 add() 而非 returning |
| impact | 审计账本 `[null]`；**不**表示 Instance 未创建 |
| repair_scope | `admission.py` 顺序（先 flush 再 append）或 `create_instance` 改 returning——**本轮不修** |

---

### 2.7 P0-B.7 LLM Audit Boundary

```text
llm_call_audit before = 1213
llm_call_audit after  = 1213
delta                 = 0
manifest.model        = mimo-x-pro-preview   # 历史 artifact metadata，未改
```

**已验证**：`existing preprocessing artifact → V3`（确定性链）。
**未验证、不得宣称**：`raw PDF → MIMO V2.6 PRO → preprocessing → V3`。

---

## 3. P1 登记（不修）

### 3.1 unit_group 结构断点

已在 §2.2 阶段归因：**annotation 有 54 composite，IR 全灭** → interface/V3 Resolver-IR，非 preprocessing。

### 3.2 Track B（独立）

```text
Track B: 9/9 failed
document_source_spans = 0
cause: sealed source append rejected (10 §4.2 immutability)
```

与 P0-A **独立**：只读重放已 SUPPORTED；Track B 走的是写路径。保持 OPEN。

### 3.3 OD-P1-B zombie tasks

```text
tasks: running 7 / queued 3 / interrupted 3 / succeeded 3
task_claims: 15
```

对本 E2E 漏斗计数**无直接污染**（runner Track A 自建 document/annotation/candidate，不经 TaskExecutor）。
**impact**：后续若走正式 TaskExecutor 会撞 stale lease。**recommended action**：Owner 单独裁决是否清理。本轮不清理。

### 3.4 Producer option span

保持事实：1356 units 中 753 标签在不同行 / 603 同行。**不**推进 span hint implementation。

---

## 4. ANALYSIS / INTERPRETATION（与 FACTS 分离）

1. **最大实证断点 = Unit → IR（284→35，loss 249）**。其中 composite **54/54 全灭**是干净子断点。
2. **Admission 不是第一断点**：34 pending 是 Authority/grammar 设计行为，不是物化失败。35→1 的产量损失在「IR ready 的答案/token 形态」与「题型不在 strict-auto 集合」。
3. **Materialization 在 approved 路径上是通的**（1/1）；`[null]` 是记账缺陷，不是业务断点。
4. **可回归性当前是部分的**：数字绑定 dirty `match-norm/v1.1`；未提交前不能称「HEAD 可回归」。

---

## 5. Q1–Q10

| # | 问题 | 答案 |
|---|---|---|
| **Q1** | 284 → IR Ready？ | **35**（standalone 35 / composite 0）；incomplete 249 |
| **Q2** | IR Ready → Candidate 损失？ | **0**（35→35） |
| **Q3** | Candidate → Admission 损失？ | **34 pending**：23 answer_grammar + 9 short_answer + 2 fill_in；**非 crash** |
| **Q4** | approved → Materialization 100%？ | **是（1/1）** |
| **Q5** | Materialization → Instance 100%？ | **对象 1/1 是**；**audit `[null]` 否**（记账缺陷） |
| **Q6** | 284 中多少应属 unit_group？丢在哪层？ | **54 composite**（payload 已有）；**丢在 Unit→IR**（material incomplete 54），非 preprocessing |
| **Q7** | sealed 是否 read-only replay？ | **SUPPORTED**（E/F/G 计算重放）；`GateService.run` 整链会写 |
| **Q8** | Track B sealed append 与 read-only replay 是否独立？ | **是**。只读已通；Track B 走写路径被 immutability 拒 |
| **Q9** | `created_instance_ids=[null]` 真因？ | **flush 前捕获 `instance.id`**（`create_instance`=add 无 returning）；Instance 行**存在** |
| **Q10** | 第一生产断点？ | **Unit → IR Ready**（284→35）。优先子项：**composite material 解析**（54/54）与 standalone 的 answer/option resolve。**不是** Admission，**不是** Materialization |

---

## 6. 根因列表（P0/P1/P2）

| 级 | 项 | 事实依据 |
|---|---|---|
| **P0** | Unit→IR：249/284 incomplete | 只读重放 |
| **P0** | composite 54/54 material incomplete | 同上 |
| **P0** | 漏斗可回归性：数字绑 dirty v1.1 | git blob 对 |
| **P1** | `created_instance_ids=[null]` | admission.py:393 vs create_instance |
| **P1** | Track B sealed append | 9/9 error |
| **P1** | zombie tasks 7/3/3 | tasks 表 |
| **P1** | pending answer 正文不可见 → B 类「确定可抽取」无法证 | payload 无 text |
| **P2** | option span 603/1356 无行内区分 | corpus 事实 |
| **P2** | 11 vs 9 口径 | §0.2 |

---

## 7. 唯一最高优先级建议（不执行）

> **下一步唯一 P0：在可回归代码基线（先提交或回退 `match-norm/v1.1` 并二选一固定）上，攻 Unit→IR 的 composite material 解析（54/54 全灭子断点）。**

理由：这是漏斗第一处大额且**结构干净**的损失；不触碰 AnswerTokenContract / Authority；
修成后才谈「Candidate 覆盖率」与「确定性答案抽取」。

**本任务结束。未开始任何修复。**

---

## Evidence

```text
DB snapshot     : documents=9 sv=9 lines=5741 anns=9 cand=35 q=1 inst=1
replay          : 9/9 pairs, DIFF=NONE, IR ready=35 incomplete=249
funnel          : 284 → 35 → 35 → 1 → 1 → 1
worktree        : 39840ff + M match_normalization.py (015cdfa vs 73badc3)
llm_call_audit  : 1213 → 1213
```
