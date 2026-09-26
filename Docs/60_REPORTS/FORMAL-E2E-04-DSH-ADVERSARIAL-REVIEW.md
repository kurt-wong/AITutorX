# FORMAL-E2E-04 · DSH Independent Adversarial Review

**Subject**: `Docs/60_REPORTS/FORMAL-E2E-04-PRODUCTION-PIPELINE-VERIFICATION-REPORT.md` (191 lines)
**Subject commits**: AITutor-X `88f0a3f`, `6c666ab` · AITutors-v3 unchanged (`5f097f6`) · Papers unchanged (`e7c79b6`)
**Evidence bundle**: `FORMAL-E2E-04-evidence/` (00–07, consumer reports, `preproc_out/`, `consumer_input_identity_ok/`)
**Reviewer**: DSH, independent adversarial reviewer. Read-only; nothing modified; no destructive command executed.
**Date**: 2026-09-27

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
VERDICT  : ACCEPTED WITH FINDINGS
FINDINGS : F4-01 … F4-09   (1 P1 · 4 MEDIUM · 3 LOW · 1 INFO)

This is the most disciplined of the four MIMO CODE rounds.
  · every falsifiable number in the report checks out byte-for-byte against the bundle
  · the report proves non-persistence instead of asserting it (byte-identical snapshots)
  · it explicitly declines to re-run resolver.resolve() as evidence — exactly the practice
    I faulted as F3-01
  · it self-discloses the producer's missing call-level record, closing my REPORT-L RL-02 concern

The findings are about framing and provenance, not about the numbers:
  F4-01 "Frozen Spec 生产链" is only half-supported — the path is in the Spec, the blocking
        condition is not; and the Spec defines TWO paths, one of which demonstrably runs
  F4-02 the only artifact that passes the consumer gate carries the LEGACY model ID
  F4-04 F04-03's stated cause is not evidenced by any delivered artifact
  F4-05 the bundle is partly executor-authored, and one "execution log" is generated prose
        containing a leaked Python builtin
```

---

## 1. Verified correct (credited — all checked, not assumed)

| # | Claim | Verification |
|---|---|---|
| 1 | Fresh manifest lacks `source_content_sha256` / `identity_version` | Manifest key set is exactly `source_file, model, annotation_meta, units`; `02….identity_fields = {null, null}` **(DV)** |
| 2 | Consumer rejects with `MISSING_IDENTITY`, `downstream_executed: false` | `consumer-report.json` verbatim; `interface_scope_blocked: 1`, Track A/B `0/0` **(DV)** |
| 3 | identity-ok run: Track A `completed=1`, Track B `completed=1`, `spans=212`, `failed=0` | `consumer-report-identity-ok.json` **(DV)** |
| 4 | 53/53 units skipped, 0 candidates | `skipped` lists Q1–Q50, U51–U53; `candidates_created=0`, `gate_pass=0`, `gate_rejected=0`, `pending_review=0` **(DV)** |
| 5 | Mechanism: "Gate 不为 incomplete 建 candidate" | Code: `gate/service.py:178-179` `if root.semantic_status != "ready": skipped.append(root.unit_id)`, consistent with `:17` (`20 §8.2/§5.2`) **(VI)** |
| 6 | Consumer never persists (`run_corpus` rollback) | `runner.py:295-296` and `:316-317` `finally: await session.rollback()` **(DV)** |
| 7 | No new DB rows | `05_…before.json` and `06_…after.json` are **byte-identical** (same SHA256); counts still ENABLEMENT-03's: `documents 2 / spans 3501 / figures 8 / candidates 13 / tasks 2`, `questions 0` **(DV)** |
| 8 | PDF Import path NOT used | `04_v3_execution.log` marks it NOT USED; snapshots show no new document/task **(DV)** |
| 9 | Input hashes | PDF `72afe586…` (791 365 B) and source md `0938b8e8…` (68 631 B) reproduced exactly **(DV)** |
| 10 | Produced artifacts | manifest `a6b8115a…` (16 993 B), `annotated.md` `41221be3…` (80 127 B) reproduced exactly **(DV)** |
| 11 | Historical backfill scope | The cited `interface_scope_step2_backfill.py` docstring itself states the 87-file frozen interface set ("Step 1 冻结的 v2 接口面(87 份)…71 份 ADMITTED / 16 份 Semantic Pending") — so 87 is **sourced**, not asserted **(DV)** |
| 12 | No code changed this round | v3 `5f097f6` and Papers `e7c79b6` unchanged; the validated tree's `reslice_pipeline.py` mtime (2026-09-26 09:42) predates the run (2026-09-27 00:41) **(DV)** |
| 13 | Frozen Spec unchanged | all six hashes reproduce the values from the three preceding rounds **(DV)** |

Two further creditable disclosures I want on record because they close earlier findings:

- `02_preprocessing_output.json.llm_call` states `"token_usage": "NOT PERSISTED by reslice_pipeline"` and
  `"note": "preprocessing has no llm_call_audit equivalent; model tag from manifest only"`. That is
  exactly the caveat I raised as **REPORT-L RL-02** (a manifest `model` tag is a fallback label, not
  proof of execution) — the report now states it instead of relying on the tag.
- The report refuses to manufacture Resolver evidence: "未另跑 `resolver.resolve()` 作证据". My previous
  review faulted precisely that practice as **F3-01**, and TRACK B's `spans_constructed=212/failed=0`
  is the tool's own number instead.

---

## 2. Findings

### F4-01 — P1 · "Frozen Spec 生产链" is half-supported: the path is in the Spec, the blocking condition is not, and the Spec defines two paths of which one runs

**The Spec does recognise Path B** (`Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:681-692`):

```text
Native Path : Source → Resolver → ResolvedRun
Path B      : Source → preprocessing → Adapter → ResolvedRun

`ResolvedRun` 必须是唯一消费入口 …… 下游 IRBuilder / Compiler / Gate / Admission
对两条路径完全一致。
```

So the report is right that a preprocessing→Adapter path has Spec standing, and its F04-02 (no
persistent Path B) is a real gap against that clause. Credit.

**But two things in the report overreach:**

1. **The blocking condition is not a Spec requirement.** `identity_version` and
   `source_content_sha256` appear **nowhere** in `Docs/V3_SPEC` (0 hits across all six spec files).
   The `MISSING_IDENTITY` gate is enforced solely by
   `backend/scripts/preprocessing_consumer/boundary.py` — the report itself attributes it to
   `F-INT-08 / F-INT-01`, i.e. a coordination-contract item. The Executive Summary's
   "Frozen Spec 生产链是否端到端可运行 → **否**" therefore equates *the Spec* with *the F-INT
   contract's* identity gate. The first blocking point is a contract-tier gate, not a Spec term.

2. **The Spec defines two co-equal paths and one of them demonstrably runs.** The Native Path ran
   end-to-end in ENABLEMENT-03 (persisted 13 admission candidates). F04-04 calls that path
   "存在但非本任务正式边界" and warns that using it yields an "E2E PASS 假象" — but per `H-C` the two
   paths are *required* to feed the same `ResolvedRun`, not to compete. Declaring the working path
   the "wrong boundary" is the **task book's** scoping choice (F04-04 cites "task instruction §2.2"),
   not a Spec-derived conclusion, and the report does not say so.

**Impact for the Owner:** the headline reads "Frozen Spec 生产链不可端到端运行", while the accurate
statement is "Path B 不可端到端运行；Native Path 可（ENABLEMENT-03 已证）". The difference decides
whether this is read as a system-level failure or as one of two Spec paths being unimplemented.
Suggested correction in the Executive Summary and in F04-04.

---

### F4-02 — MEDIUM · The only artifact that passes the consumer's interface gate carries the LEGACY model ID

`consumer_input_identity_ok/2018北京夏季高中会考历史（教师版）(1).manifest.json`:

```text
source_content_sha256 = d4917437065bfcb8eda24dd45b4e92ca4e2bb6eb8bb4342170903e4c5a62e714
identity_version      = 2
units                 = 53
model                 = mimo-x-pro-preview        ← the ID the live API rejects
```

The report describes this sample accurately as "real producer artifact… not hand-crafted", and it is
indeed from the historical `reslice-batch-C` corpus. What it does not state is that the sample's
declared model is the **legacy test model ID** that (a) the live API rejects with
`400 Unsupported model`, and (b) the V3 gateway now fail-closes on by design
(`LEGACY_TEST_MODEL_IDS` in `gateway.py`).

Combined with F04-01, the sharper conclusion is: **no artifact produced by the formal pipeline under
the migrated provider has ever been accepted by the consumer interface.** The single acceptance in
this round rests on a pre-migration, backfilled historical artifact. That is material to how
"Annotation PASS（事务内）" and the Track A/B "completed" results should be read, and it is a
provenance fact the bundle contains but the report does not surface.

---

### F4-03 — MEDIUM · The preprocessing PASS is indirect by construction, and the artifact is honest about it

Precisely *because* `02_preprocessing_output.json` discloses that no call-level record exists, the
status **"PDF→Preprocessing PASS（真实 LLM）"** rests on: exit success, `units=30`,
`validation_issues=0/warnings=0`, and a rendered `annotated.md` (80 127 B). There is no request/response
record, no token usage, no provider-side attestation — the producer has no `llm_call_audit`
equivalent.

That evidence is as good as the producer can currently produce and I do not dispute the PASS; the
finding is one of labelling. "真实 LLM" reads as a verified property, whereas what is verified is
*pipeline output whose structure only an LLM annotation can produce*. Writing "PASS（间接证据：产出 +
manifest 完整性；无 call-level 记录）" costs nothing and prevents the phrase from being quoted as
provider-level proof. (Related: GAP-E2E-05 in ENABLEMENT-01 asked for exactly this record on the V3
side; the producer side has no equivalent at all.)

---

### F4-04 — MEDIUM · F04-03's stated cause is not evidenced by any delivered artifact

The **fact** is verified (all 53 units skipped, 0 candidates) and the **mechanism** is verified in
code (`gate/service.py:178-179`). But F04-03 and
`07_pipeline_summary.second_blocking_point` assert a **cause**: *"adapter known gaps: option per-label
spans unavailable; choice units cannot be ready"* → `GAP_OPTION_LABEL_SPAN_UNAVAILABLE`.

Nothing in the bundle supports that attribution:

- `consumer-report-identity-ok.json` contains no per-unit `semantic_status` and no resolver
  unresolved-role detail for Track A — only the id list.
- Track B reports `unresolved_total: 0`, `unresolved_detail: []`, `spans_with_bad_refs: 0` — i.e. the
  only unresolved-related numbers present are all zero.
- ENABLEMENT-03's real run showed incompleteness arising from `answer`/`explanation` resolution on
  similar material, so "option granularity" is one hypothesis among several.

This is the same family as F2-02 and F3-01 in earlier rounds: a diagnosis asserted where the evidence
would need one more field. A per-unit dump (`unit_id`, `semantic_status`, resolver unresolved reasons)
into the bundle would settle it and would also let the Owner evaluate the `GAP_OPTION_LABEL_SPAN_UNAVAILABLE`
contract question on evidence rather than on inference.

---

### F4-05 — MEDIUM · The bundle is partly executor-authored, and one "execution log" is generated prose with a leaked Python builtin

`04_v3_execution.log` — listed in the report's Evidence index as an execution log — contains:

```text
Present read API : GET /api/documents/<built-in function id>, source-lines, source-quality,
                   GET /api/candidates/<built-in function id>
```

`<built-in function id>` is the Python `id` builtin interpolated into an f-string (`{id}` where
`{document_id}` was meant). So the file is a **rendered summary written by the executor's own
generator**, not captured command output. The evidence bundle also ships that generator
(`_write_evidence.py`, 11.4 KB, plus `_snap.py`, `_inspect_after.py`), and `02`, `04`, `07` are all
script-authored.

Shipping the generator is a *good* practice (it makes the bundle re-runnable) — the finding is that
the bundle does not distinguish **raw tool output** (manifest, `.md`, consumer reports, DB snapshots)
from **executor-authored renderings**. In a round whose entire subject is evidence, that distinction
should be explicit (a per-file `provenance` field, or a separate `authored/` subdirectory).

Process note: `04_v3_execution.log` is listed in the report's evidence index but was **not delivered
in the first commit** `88f0a3f`; it arrived in `6c666ab`.

---

### F4-06 — LOW · `markdown_sliced` is recorded with the wrong artifact

`02_preprocessing_output.json.artifacts` lists:

```text
markdown_sliced : …annotated.md , sha 41221be3…, 80127 bytes
annotated_md    : …annotated.md , sha 41221be3…, 80127 bytes     ← same path, same hash
```

but the directory holds three distinct files:

```text
….md             61038 B   sha 466d08cc87f0b0dcc4e1fa262c1861591a74a9f406d2639acb48ffa362c642e7
….annotated.md   80127 B   sha 41221be300076ef5d4423ca6d7646171f7a0db8b302edf2d6e97ac53927835f4
….manifest.json  16993 B   sha a6b8115a34f7478a32ff3d0a0c8ac6f1f2f13517268041434ace5e0c12a07353
```

So the "三件套" is present on disk but only two of three are recorded correctly, and the sliced
markdown is absent from the evidence record. The manifest and `annotated.md` hashes match exactly —
this is a record-precision defect, not a missing artifact.

---

### F4-07 — LOW · The validated "正式 preprocessing 入口" lives in the non-versioned tree, and the authority question is still open

The E2E command runs preprocessing from `cd D:\Project\Aitutors-preprocessing\scripts` — the
non-git copy whose authority I raised as **REPORT-L RL-03 / D-1** (still unresolved), while the git
repository for that codebase (`Papers`, remote `Aitutors-preprocessing.git`) carries a *different*
(reduced) `reslice_pipeline.py`.

In fairness I verified that F04-01's conclusion holds for **both** trees:

```text
D:\Project\Aitutors-preprocessing\scripts\reslice_pipeline.py  writes_identity = False
D:\Project\Papers\scripts\reslice_pipeline.py                  writes_identity = False
```

So the finding is not that the result is wrong — it is that a report whose subject is a
producer/consumer contract never names which producer tree is authoritative, and the tree it validated
has no version control.

---

### F4-08 — LOW · F04-02 deserves the Spec citation, and the persist/no-persist asymmetry is the report's most important result

F04-02 is verified twice over (code + byte-identical snapshots) and is, in my assessment, the most
consequential finding in the report: the Spec requires both paths to feed one `ResolvedRun`
(`90 §H-C`), and Path B has **no persistent entry at all** — `run_corpus` always rolls back. Writing
it as a **Spec-level** gap ("Path B exists in the Spec; no persistent Path B ingest exists") rather
than as a code observation would give the Owner the decision in the right frame. Right now it sits in
a Findings list next to the frontend gap.

---

### F4-09 — INFO · Additional notes

- The identity-ok sample's markdown/manifest were copied into the bundle
  (`consumer_input_identity_ok/`), which makes the Track A/B run reproducible in isolation — good.
- `03_consumer_mapping.json` presents `mapping_checks` as code-level statements
  ("PERFORMED by annotation_adapter"), which is the correct tier; note that this mapping is on the
  **consumer** path only and has no bearing on the Native Path's annotation vocabulary (see my F3-07
  for FORMAL-E2E-ENABLEMENT-03).
- The run occurred at 2026-09-26T16:41Z (2026-09-27 00:41 Beijing) — outside the weekday DeepSeek
  window, and MIMO-only, consistent with the stated policy.
- AITutor-X HEAD `6c666ab` is unpushed at review time (`origin/main` = `5de14d1`). My push of this
  review will fast-forward both unless the Owner instructs otherwise.

---

## 3. Owner decision list

| # | Decision | Inputs | Blocking? |
|---|---|---|---|
| **D-1** | **Which path is "the" production chain — Native (runs today, ENABLEMENT-03) or Path B (blocked)?** Spec `90 §H-C` requires both to feed one `ResolvedRun`; if Path B is the target, F04-02 must be treated as a Spec-level gap. | F4-01, F4-08 | **Yes** — it changes how "OUTCOME: BLOCKED" should be read |
| **D-2** | **Should `source_content_sha256` be emitted by the formal preprocessing step**, or is a defined post-step legitimate? (Neither tree writes it; 87 historical manifests were backfilled by a one-off script.) | F04-01 (the gate is F-INT, not Spec) | **Yes** for Path B |
| **D-3** | **Define a persistent Path B ingest (commit semantics)**, or declare Path B non-production. The current consumer is a rollback validator. | F4-08 | **Yes** |
| **D-4** | **Require per-unit IR/resolver evidence** before deciding the `GAP_OPTION_LABEL_SPAN_UNAVAILABLE` contract question — F04-03's cause is currently unevidenced. | F4-04 | Recommended |
| **D-5** | **Should the producer gain a call-level record** (`llm_call_audit` equivalent), so "真实 LLM" is a verified rather than indirect property? | F4-03 | No |
| **D-6** | **Require evidence bundles to mark raw vs authored files** (and fix the `04` log generator's `{id}` bug). | F4-05 | No |
| **D-7** | **Name the authoritative preprocessing tree** (RL-03 / D-1) — the validated entry has no version control, and `Papers` differs. | F4-07 | No, but it gates reproducibility |
| **D-8** | **Accept the corrected provenance statement**: no migrated (`mimo-v2.6-pro`) artifact has passed the consumer interface; the single acceptance is a pre-migration backfilled artifact. | F4-02 | No |

---

## 4. Findings summary

```text
F4-01  P1       "Frozen Spec 生产链" framing: Path B is Spec-recognised (90 §H-C), but the blocking
                condition (identity) appears nowhere in V3_SPEC (0 hits) and lives in an F-INT gate;
                the Spec's Native Path demonstrably runs end-to-end, which the summary does not say  [DV/VI]
F4-02  MEDIUM   The only artifact passing the interface gate declares model=mimo-x-pro-preview
                (legacy ID, API-rejected, gateway fail-closed) → no migrated artifact has ever
                passed the consumer interface                                                       [DV]
F4-03  MEDIUM   Preprocessing PASS is indirect (no call-level record); the artifact says so honestly,
                the status table does not                                                           [DV]
F4-04  MEDIUM   F04-03's cause (option per-label spans) is not evidenced: no per-unit semantic_status,
                and every unresolved-related number in the artifact is zero                           [DV]
F4-05  MEDIUM   Bundle mixes raw and executor-authored files; 04_v3_execution.log is generated prose
                containing "<built-in function id>"; it was also missing from commit 88f0a3f        [DV]
F4-06  LOW      markdown_sliced recorded with annotated.md's path and hash; the real .md (466d08cc…)
                is absent from the evidence record                                                  [DV]
F4-07  LOW      The validated formal preprocessing entry lives in the non-versioned tree; Papers
                carries a different revision; authority (RL-03/D-1) unnamed                              [DV]
F4-08  LOW      F04-02 (no persistent Path B) should be framed against 90 §H-C as a Spec-level gap    [VI]
F4-09  INFO     side notes incl. mapping artifact tier, run window, unpushed AITutor-X HEAD          [DV]
```

---

## 5. Reviewer side-effects

1. No file under `AITutors-v3`, `Papers` or `Aitutors-preprocessing` was written; nothing was executed
   that mutates state; database access was `SELECT`-only via
   `docker exec aitutor-postgres psql -U aitutors -d aitutors`.
2. Verification was file/hash/code-read only: hashes of the input PDF, source markdown, produced
   manifest and `annotated.md`; key lists of the fresh and identity-ok manifests; bundle file
   inventory; `runner.py` / `gate/service.py` / `90_DOCUMENT_GOVERNANCE.md` reads.
3. No key material printed; `01_preprocessing_input.json` records `MIMO_API_KEY` as
   "PRESENT(not recorded)", which I confirmed it does not violate.
