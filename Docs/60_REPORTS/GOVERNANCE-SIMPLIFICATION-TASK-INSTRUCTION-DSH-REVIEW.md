# MIMO CODE TASK BOOK · DSH Pre-Execution Instruction Review

**Subject**: the Owner's draft instruction `Governance Simplification Alignment & Main Pipeline Unblocking` (PART 0 – PART 9 + FINAL INSTRUCTION)
**Review type**: review of the **instruction**, before execution. No code, document or repository was changed.
**Verifier**: DSH, independent. Read-only.
**Date**: 2026-09-27

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
DIRECTION        : SOUND — this is the right next task (stop修治理, start 推进主线)
EXECUTABILITY    : PARTIALLY — 4 internal contradictions must be fixed before handing it over,
                   or the executor will be forced to choose between failing and violating the no-go list
FINDINGS         : T-01 … T-11   (4 BLOCKING · 4 MEDIUM/HIGH · 3 INFO)

Nothing in the instruction violates its own principles. The problems are:
  · the "primary path" and "Path B" are declared to be the same pipeline under two names with
    opposite statuses (T-01);
  · implementing identity (PART 4) needs the tree decision that PART 3 defers to the Owner, and
    PART 7's "commit hash" is unsatisfiable in the tree with no .git (T-02);
  · PART 6's required chain cannot pass in one round, for reasons unrelated to identity (T-03);
  · the no-go list is missing the three prohibitions this specific pipeline invites (T-04);
  · PART 9 demands four documents while PART 2 forbids new documents (T-05);
  · the PART 9 priority order is inverted (T-06).
```

All findings below are grounded in artifacts I verified in this session; each cites the file and line.

---

## 1. PART 0 fact audit (what is verified, what is not)

Verified at the stated tier — these are safe to hand over as "必须遵守":

| PART 0 statement | Verification |
|---|---|
| Three repositories; no production migration completed | AITutor-X `b4889f7`, AITutors-v3 `5f097f6`, Papers `e7c79b6`; no migration artifact; `90_ARCHIVE` empty **(DV)** |
| Two producer code trees exist | `D:\Project\Papers` = git repo (remote `…/Aitutors-preprocessing.git`); `D:\Project\Aitutors-preprocessing` = no `.git`; the two `reslice_pipeline.py` differ **(DV)** |
| Native Path runs | ENABLEMENT-03 ran `POST /api/documents/import` → worker CLI → 13 persisted `admission_candidates` **(DV)** |
| Path B identity not implemented | fresh manifest keys are only `source_file, model, annotation_meta, units`; consumer returns `MISSING_IDENTITY`, `downstream_executed=false` **(DV)** |
| Path B consumer persistence not implemented | `runner.py:296` and `:317` `await session.rollback()`; E2E-04 before/after DB snapshots byte-identical **(DV)** |
| `mimo-x-pro-preview` retired except historical data | `.env MIMO_MODEL=mimo-v2.6-pro`; `step0_blind_test.py` fixed; producer writes no legacy ID; legacy survives only in historical artifacts (e.g. `FORMAL-E2E-04-evidence/consumer_input_identity_ok/…manifest.json`) **(DV)** |

**Not verified / needs rewording (T-07):** three statements sit under "以下事实已经通过 DSH 独立验证" without qualifying their tier — see T-07. The heading should be split into "已独立验证的事实" / "本任务的方向性判断".

---

## 2. Blocking findings

### T-01 — BLOCKING · The "Primary Production Path" and "Path B" are the same pipeline, declared with opposite statuses in one document

PART 0 states as the future primary chain:

```text
preprocessing → manifest + annotated markdown + semantic metadata → AITutors-v3 ingestion
              → Resolver → ResolvedRun → IR → Admission          「该路径是当前开发重点」
```

and separately declares:

```text
Path B: preprocessing → adapter → ResolvedRun
  · identity contract 尚未完成
  · consumer persistence 尚未完成
  · 当前不能作为生产路径          →  「只记录为 Future integration gap」
```

The Frozen Spec defines exactly two consumption paths and requires one shared entry
(`Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:682-686`):

```text
Native Path : Source → Resolver → ResolvedRun
Path B      : Source → preprocessing → Adapter → ResolvedRun
`ResolvedRun` 必须是唯一消费入口。
```

So **"V3 ingestion" in the primary chain *is* Path B's Adapter leg.** The instruction therefore:

- designates Path B as the primary production path (PART 4 "重点", PART 6 required target, PART 9 P1/P3), and
- simultaneously forbids treating Path B as a production path and forbids any Path-B-specific governance.

An executor reading PART 0 literally cannot tell whether to build Path B or to leave it alone. This is
also the exact ambiguity the previous round's task (§17) and the governance review warned about — the
new instruction re-imports the Path B vocabulary without collapsing it.

**Minimal amendment:** one sentence in PART 0: *"Primary Production Path ≡ Frozen Spec 的 Path B
（`90 §H-C`）。本任务统一使用「Primary Production Path」一个名称；Path B 仅为 Spec 侧同义词。"*
and delete the "Future integration gap" framing for the main line (keep that label for the
**unimplemented identity/persistence legs**, not for the path).

### T-02 — BLOCKING · PART 4 depends on the tree decision PART 3 defers to the Owner; PART 7's evidence requirement is unsatisfiable in the non-git tree

- PART 3 correctly restricts itself to fact-finding and forbids auto-merge / auto-migration / auto-`git init`.
- PART 4 then asks for an **implementation** ("如果这是业务必要字段：直接实现") in `Aitutors-preprocessing`.
- Verified: `D:\Project\Aitutors-preprocessing` has **no `.git`**; the git repository for that codebase is
  `Papers`. Neither tree writes `source_content_sha256` (`writes_identity = False` in both).
- PART 7 requires the evidence to record a **`commit hash`**.

Consequence: implementing identity in the tree named by the instruction produces either
(a) a change with **no commit hash** → PART 7 unsatisfiable, or (b) a commit into `Papers` →
an authority decision PART 3 explicitly reserves for the Owner.

**Minimal amendment (PART 4):** *"identity 变更的落盘仓库由 PART 3 的 Owner 裁决决定；裁决前允许产出
补丁 + 测试证据，不得提交、不得 `git init`、不得移动文件。"* — this keeps PART 3's promise and keeps
PART 7 satisfiable.

### T-03 — BLOCKING · PART 6's required chain cannot pass this round, and its failure would not be the executor's fault

Verified blockers on `preprocessing output → V3 ingestion → ResolvedRun`, in order:

```text
1  .md/manifest cannot enter the formal import at all
   app/domains/source/import_service.py:26   _ALLOWED_EXTENSIONS = {".pdf", ".docx"}
   (baseline round registered this as E2E-BL-07)

2  the consumer never persists
   scripts/preprocessing_consumer/runner.py:296, :317   finally: await session.rollback()
   (registered as F04-02; proven by byte-identical before/after DB snapshots)

3  the identity gate fails closed
   fresh manifest has no source_content_sha256 → MISSING_IDENTITY, downstream_executed=false
   (F04-01 / GAP-PB-01 — the one blocker PART 4 addresses)

4  even with identity, the chain still stalls
   consumer-report-identity-ok.json: Track A completed, candidates_created=0, skipped = ALL 53 units
   cause asserted but NOT evidenced (my F4-04); and the only artifact that ever passed the gate
   carries the legacy model tag mimo-x-pro-preview (my F4-02)
```

So "PART 6 Required: 验证 preprocessing output → V3 ingestion → ResolvedRun" is **not achievable in one
task**, and PART 7's evidence requirement would then be met only by a failing test or by a shortcut.

**Minimal amendment (PART 6):** stage the target.

```text
REQUIRED   : preprocessing 产出含 identity → consumer gate accepted → 存在一条持久化 ingestion 记录
BEST-EFFORT: ResolvedRun / IR 完整度；未达成时按数据记录（per-unit semantic_status + unresolved 原因），
             不视为本任务失败
```

### T-04 — BLOCKING · The no-go list omits the three prohibitions this pipeline invites

The previous task stated them explicitly; this one does not:

```text
❌ 人工修改 manifest 以补齐 identity
❌ 用 path / 目录名冒充 identity
❌ 绕过 enforce_interface_scope / consumer gate
```

With T-03's target unachievable as written, these are precisely the shortcuts an executor under
delivery pressure would reach for — and they are the three things the last five rounds spent their
effort proving must not happen (E2E-05 §5; `boundary.py`'s own message: *"path must never be used as
identity"*).

Two further omissions from verified history worth adding to PART 8:

```text
❌ 伪造授权：hardcode budget_ok / dummy task_context —— authorization 必须来自真实 Task + budget 检查
   (my F2-01 is still open; this task authorizes "provider 修改", which is adjacent to that path)
❌ 为让测试通过而放宽/删除断言 —— 已知 Papers/tests/test_no_config_import.py:47 目前无法通过，
   修法是把断言改成与代码一致，不是删掉断言 (my F2-08)
```

---

## 3. Non-blocking findings

### T-05 — HIGH · PART 9 requires four documents while PART 2 forbids new documents

PART 2: *"新增文档：默认禁止。如果现有文档可以表达：不要创建新文档。"*
PART 9: *"提交：1. Current State Assessment 2. Simplification Proposal 3. Implementation Plan 4. Code Changes"*

Read literally, the executor satisfies PART 9 by creating four new files → straight PART 2 violation.
**Amendment:** *"PART 9 的四项作为**同一份**任务报告的四节；可并入既有治理简化交付物的部分优先并入，不新建。"*
(The previous instruction used the same discipline: "只需要两个结果".)

### T-06 — HIGH · PART 9's priority order is inverted

```text
declared   P1 preprocessing → V3 integration
           P2 identity completion
           P3 Path B future support
           P4 Native fallback preservation
```

- **P2 is a prerequisite of P1**, not a lower priority: both E2E-04 and E2E-05 stop at the identity gate
  with `downstream_executed=false`. Integration acceptance cannot be reached before identity lands.
- **P3 is the same pipeline as P1** (T-01), so as written the task asks for the same work twice, once as
  priority 1 and once as priority 3.

**Amendment:**

```text
P1 identity completion（producer 侧；唯一能解除 gate 的变更）
P2 ingestion / persistence + integration acceptance（consumer 接受 + 一条持久化记录）
P3 IR/ResolvedRun 完整度（record-only，数据化未达成原因）
P4 Native Path preservation（不做事，只保证不破坏、且不得当作主链证据）
```

### T-07 — MEDIUM · Three PART 0 statements are presented as verified facts but are not

| Statement | Problem | Correction |
|---|---|---|
| "Primary Production Path … 该路径是当前开发重点" | a direction, not a verified fact; and its V3-ingestion leg does not exist (T-03) | move under "方向性判断" |
| "Native Path 已经可以运行" | true only to Admission, with **0 Questions** — the 13 candidates are all `pending_review` | "可运行至 Admission（13 candidates / 0 Question）" |
| "identity contract 尚未完成" | imprecise and **dangerous**: the identity key is already defined in `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md:18,22` (§0.1 ①, 64-hex). What is missing is the producer-side *implementation* — and the contract itself is marked **NOT FROZEN** (my F5-01) | "identity 契约文本已存在（v0.2 DRAFT，未冻结）；缺的是 producer 侧实现" |

As written, "identity contract 尚未完成" invites the executor to **write a contract** — a CREATE,
forbidden by PART 2 and PART 8. (See also T-09.)

### T-08 — MEDIUM · "Which repo is Aitutors-preprocessing" is ambiguous

PART 0 lists three repositories including `Aitutors-preprocessing`; PART 3 calls that name one of two
code trees, the other being `Papers`. But the git repository **whose remote is named
`Aitutors-preprocessing.git`** is `Papers`. **Amendment:** one mapping line —

```text
Papers                  = git 仓（remote: github.com/kurt-wong/Aitutors-preprocessing.git）
Aitutors-preprocessing   = 无 .git 的工作树副本
两棵树代码不一致（`_redact` / 4xx 分支仅副本有；identity 两棵都没有）
```

### T-09 — MEDIUM · PART 4's "直接实现，不需要 Contract approval" is correct only if the target is stated

`source_content_sha256` is **already defined** in the Contract (`v0.2 DRAFT §0.1 ①`, "64 字符小写 hex"),
so implementing it is "完成已明确的实现" and correctly LEVEL 1 — the governance review's own §1.2 list
names *"`reslice_pipeline.py` 输出 `source_content_sha256`"* as a LEVEL 1 example. But combined with
T-07's wording, PART 4 could be read as license to draft a contract. **Amendment (PART 4):**
*"字段已定义于 Contract v0.2 §0.1；本任务只实现，不修改契约文本、不新建契约。"*

### T-10 — MEDIUM · Objective #4 ("修复已确认但未实施的实际业务缺口") has no list

The verified, already-confirmed-and-unimplemented producer-side items are:

```text
(a) Papers/scripts/reslice_pipeline.py 缺 _redact() 与 non-429-4xx 立即失败分支
    （同一代码的无 .git 副本两者都有 → 两棵树已在加固程度上分叉）      my F2-08 / F4
(b) Papers/tests/test_no_config_import.py:47 仍 catch FileNotFoundError，
    而 load_cfg() 抛 ProviderConfigError → 该测试对自家代码无法通过       my F2-08
(c) authorization：ensure() 先铸造账户、check() 再读它（limit=100 → remaining=100）
    → budget_ok 在正式 worker 路径上不可证伪                            my F2-01（仍未关闭）
```

Naming (a)(b) as LEVEL 1 and (c) as *record-only unless the Owner authorizes* prevents both scope drift
and duplicate discovery.

### T-11 — INFO · PART 1's "provider 修改" is consistent with the verified state

`.env MIMO_MODEL=mimo-v2.6-pro`; `step0_blind_test.py` no longer defaults to the legacy ID; the producer
writes no legacy model; the only surviving `mimo-x-pro-preview` occurrences are in historical artifacts —
covered by the instruction's "旧测试数据除外" ✓.

---

## 4. What MIMO CODE can actually deliver under these constraints

| PART | Achievable this round? | Note |
|---|---|---|
| PART 3 producer fact-finding (candidates / differences / recommended authority) | **YES, fully** | read-only; the deliverable is exactly what PART 0/3 describe |
| PART 4 identity implementation in the producer + tests | **YES as a patch**, subject to T-02's tree question | this is the single change that can move the gate from `MISSING_IDENTITY` to `accepted` |
| PART 6 acceptance at the identity gate | **YES** once PART 4 lands (reuse the E2E-04/05 corpus) | |
| PART 6 persistence + ResolvedRun completeness | **NO** (T-03) | must be pre-declared as best-effort/record-only, or the round looks like a failure |
| PART 2 simplification proposal | **already delivered** by the governance review | per PART 2's own rule, merge rather than recreate |
| PART 1 three-level model | **already delivered** | same |
| PART 9 #1 Current State Assessment | **YES** | but must not present Native-Path results as primary-chain evidence — see below |

**One evidence-integrity point the instruction should state explicitly:** all downstream evidence that
exists today (13 admission candidates, all `pending_review`) came from the **Native Path**
(`POST /api/documents/import` + `python -m app.worker run --allow-live`), i.e. from the path this task
deprioritises. There is currently **no evidence of the primary chain beyond the consumer identity gate**.
The Current State Assessment should say so, otherwise a reader will attribute the 13 candidates to the
main line.

---

## 5. Recommended amendments (wording only — no new artifact)

1. **PART 0**: split "已独立验证的事实" from "方向性判断"; state once that *Primary Production Path ≡ Spec Path B*; sharpen the three T-07 wordings.
2. **PART 0 / PART 3**: add the repo↔tree mapping line (T-08).
3. **PART 4**: state that the identity field is already contract-defined (implement only, never draft a contract); state that the target tree waits on PART 3's Owner decision (T-02, T-09).
4. **PART 6**: stage the required target — gate acceptance + one persisted ingestion record are REQUIRED; ResolvedRun/IR completeness is best-effort with data-recorded causes (T-03).
5. **PART 8**: add the five prohibitions — hand-edited manifest / path-as-identity / gate bypass / fabricated authorization / relaxed test assertions (T-04).
6. **PART 9**: four sections **of one report**; and reorder the priorities as P1 identity → P2 ingestion+integration → P3 IR completeness → P4 Native preservation (T-05, T-06).

None of these adds a governance mechanism; they remove ambiguity and close the loopholes the current
wording leaves open. With them applied, the instruction is executable end-to-end without violating its
own constraints — which is the FINAL INSTRUCTION's stated success criterion.

---

## 6. Reviewer side-effects

1. Nothing written outside this review document and its log; no repository state changed; no test run.
2. Verification was read-only: `git rev-parse`/`status`, targeted greps in `AITutors-v3/backend/app` and
   `scripts/preprocessing_consumer`, `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md`, the two producer
   `reslice_pipeline.py` trees, `Papers/tests/test_no_config_import.py`, and the E2E-04/05 evidence files.
3. No key material printed.
