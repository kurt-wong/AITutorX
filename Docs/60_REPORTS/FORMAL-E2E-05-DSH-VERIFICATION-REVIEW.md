# FORMAL-E2E-05 · DSH Independent Verification Review

**Subject**: `Docs/60_REPORTS/FORMAL-E2E-05-PATH-B-VERIFICATION-REPORT.md` (291 lines)
**Subject commit**: AITutor-X `787e1fa2ff2f2ff86341056ef9fabd840eb749ff` (on top of the F4-04 review commit `fa3a01c`)
**Evidence**: `D:\Project\AITutor-X\evidence\` (git_and_spec_snapshot + preprocessing/{logs, report, out/*})
**Unchanged this round**: AITutors-v3 `5f097f6` (0 modified tracked) · Papers `e7c79b6` · `Aitutors-preprocessing` (no git)
**Reviewer**: DSH, independent. Read-only; no destructive command; DB access `SELECT`-only.
**Date**: 2026-09-27

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verification result

```text
REPORTED RESULT : FAIL at CONSUMER (MISSING_IDENTITY)
INDEPENDENT VERIFICATION : CONFIRMED
FINDINGS : F5-01 … F5-06   (2 MEDIUM · 3 LOW · 1 INFO)

Every falsifiable number in the report reproduced exactly.
The FAIL verdict is well-founded and correctly located.
This is the strongest of the five MIMO CODE reports on discipline.
```

| # | Claim | Independent check |
|---|---|---|
| 1 | Blocked at CONSUMER, `MISSING_IDENTITY` | `consumer_report.json` verbatim: `accepted:false`, `code:MISSING_IDENTITY`, `declared_identity_version:null`, `downstream_executed:false` **(DV)** |
| 2 | Track A `0/1`, Track B `0/1`, gaps 0, units 30 | report JSON **and** the runner's own stdout in `consumer_execution.log` **(DV)** |
| 3 | Three artifact hashes | reproduced on disk: manifest `44622cf8…` 20 579 B · `.md` `df907f5e…` 61 036 B · `.annotated.md` `16a5a65a…` 80 127 B **(DV)** |
| 4 | units 30 = 26 `standalone_question` + 4 `composite_question`, 4 with `material_lines` | parsed from the manifest itself **(DV)** |
| 5 | Contract hash `9c6b9063…b17528` = task book's value | reproduced on `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` **(DV)** |
| 6 | PREPROCESSING PASS via the formal entry | `reslice_execution.log` is the pipeline's own output: `929 行, prompt 46223 字`, `units=30 覆盖题号=30 校验问题=0 警告=0`, `完成：1/1 无校验问题` **(DV)** |
| 7 | Code modifications = 0 | v3 `5f097f6` with 0 modified tracked files; Papers `e7c79b6`; producer tree mtimes unchanged **(DV)** |
| 8 | No new candidates, no new DB rows | DB unchanged from ENABLEMENT-03: documents 2 · annotations 2 · candidates 13 · questions 0 · unit_groups 0 · tasks 2 · audits 2 · figures 8 · spans 3501 **(DV — verified externally, see F5-03)** |
| 9 | Native Path not used | no `/api/documents/import` call in the logs; DB holds no new document **(DV)** |

**Substantive addition worth stating:** this round is a **genuine re-run**, not a re-labelling of
ENABLEMENT-04. All three produced artifacts differ from E2E-04's (`same=False`; manifest 20 579 B vs
16 993 B, `.md` 61 036 vs 61 038 B), yet the unit structure reproduced identically
(30 = 26 + 4, 4 with material). That is the first independent repeat of a producer run in this chain,
and it is real reproducibility evidence rather than a duplicate claim.

---

## 1. Credited — including three items that close my own earlier findings

1. **Raw logs, not authored prose.** `reslice_execution.log` carries the producer's own per-file
   banner and counters; `consumer_execution.log` is the runner's stdout. My **F4-05** finding (an
   "execution log" that was generated prose containing a leaked Python builtin) does not recur. (DV)
2. **`markdown_sliced` is now recorded correctly.** `output_summary.json` lists the `.md` with its own
   size and hash (`df907f5e…`, 61 036 B) instead of duplicating `annotated.md` — my **F4-06** is fixed. (DV)
3. **The Spec-vs-Contract tier claim is now correct.** §3.1 states that "Spec/Contract 存在 Path B 与
   identity 字段" and sharply separates them. That is right on both counts: Path B is defined in the
   **frozen** `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:681-692`, while the identity key is defined in
   the **contract** — `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md:18,22` (§0.1 six binding items;
   "① Identity … 键名 = `source_content_sha256`"). This is a direct adoption of my **F4-01**
   correction, and the report's §3 "不能写「Frozen Spec 不支持 preprocessing」" is exactly the
   discipline that was missing in E2E-04. (DV)
4. **Honest provenance on all four repositories** — `git_and_spec_snapshot.json` records
   `Aitutors-preprocessing: "NO_GIT"` rather than implying a commit, and
   `code_modifications_this_task: 0`. (DV)
5. **"HEAD（验证前）`fa3a01c`" is accurate** — it names the repository state that existed before this
   round's own commit, fixing the EN-03/EN-04 problem where a recorded commit did not identify the
   state the run started from. (DV)
6. **FACT / INTERPRETATION are separated and the INTERPRETATION section is disciplined**: it forbids
   the two over-readings ("Frozen Spec 不支持 preprocessing", "Path B 不存在") and refuses to extend
   the distinction between in-transaction validation and a persistent ingest entry. (DV)

---

## 2. Findings

### F5-01 — MEDIUM · The gate's authority is a contract that declares itself NOT FROZEN, and the report titles it "Frozen Spec Path B"

`PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md:3`:

```text
> **状态**：**DRAFT（Freeze Candidate Finalized）。READY FOR FREEZE。NOT FROZEN。**
```

while `:18` declares "冻结内容（六项，binding；接口键名 = `source_content_sha256`，DEC-030 已裁 +
DEC-031 终局确认）".

So the document that supplies the blocking condition is **explicitly not frozen** while calling its own
contents binding. The report's title ("Frozen Spec Path B Production Pipeline Verification"), §1.1's
labelling of the hash as a frozen object, and §6's "未修改 Frozen Spec YES" all present the gate as
frozen authority. The precise picture is:

```text
Path B (the path)        → Frozen Spec        90_DOCUMENT_GOVERNANCE.md §H-C   (frozen)
identity key (the gate)  → Contract v0.2 DRAFT §0.1/①  ("NOT FROZEN" per its own header)
enforcement              → backend/scripts/preprocessing_consumer/boundary.py  (code)
```

A FAIL verdict whose single cause is a not-yet-frozen draft should say so in one line; otherwise the
Owner reads "Frozen Spec" as authority that has in fact not been frozen yet. Relatedly, the same
contract records at `:66` — "**V3 侧义务现状（`OBSERVED`，全部未实现）**：验证 Manifest（无校验）·
重算 hash（不读 producer sha，自算为 canonical…）" — i.e. the contract's obligations are asymmetric and
the V3 side is unimplemented. That context is relevant to whether `MISSING_IDENTITY` is the *first*
blocking point or one of several un-met contract clauses.

---

### F5-02 — MEDIUM · ENABLEMENT-04's strongest finding has been demoted out of the GAP list

ENABLEMENT-04 registered **F04-02 — "Consumer runner 永不持久化"** as a numbered finding with the
evidence that the before/after DB snapshots are byte-identical, and (per my F4-08) it is the gap that
blocks Path B **independently of identity**: even if `source_content_sha256` were emitted tomorrow,
`runner.py` still rolls back and Path B would still have no persistent ingest entry — against the
Spec's requirement (`90 §H-C`) that both paths feed one `ResolvedRun`.

In this round that finding survives only as a parenthetical in §3.4 ("为已知实现事实 … 需 Owner 确认，
本报告不扩展裁决") and is **absent from GAP-PB-01..03**, all three of which are producer-side identity
issues. The Owner's decision list therefore under-counts: the identity fix (PB-01/02) and the
persistence gap are two independent decisions, and only one is now on the list.

Recommendation: register it as **GAP-PB-04 — Path B 无持久化入口**, citing `90 §H-C` and
`runner.py:295-296/:316-317`. (`GAP-PB-03`, "本任务无法在不改代码/不改产物前提下继续下游", is not a
system defect but a statement of task constraints; it is fine to keep, but it should not occupy the
slot that the persistence gap vacated.)

---

### F5-03 — LOW — Evidence metadata shrank relative to the two preceding rounds

§1.5 asserts "无候选、无 DB 新行". I verified it is **true** — the database is exactly at
ENABLEMENT-03's end state (`documents 2, semantic_annotations 2, admission_candidates 13, questions 0,
unit_groups 0, tasks 2, llm_call_audit 2, source_figures 8, document_source_spans 3501`) — but this
round ships **no DB snapshot**, whereas ENABLEMENT-04 proved the same class of claim with
byte-identical before/after snapshots. Two further reductions:

- `frozen_spec_sha256` records **3 of 6** spec files (`00`, `10`, `20`); EN-03 and EN-04 recorded all six.
  I verified all six are unchanged, so the claim holds — the *evidence* narrowed.
- No run identifier and no `DATABASE_MODE` this round; run identity rests on `generated_at`
  timestamps plus file mtimes. EN-03 had `E2E_RUN_ID` + mode, EN-04 had a full metadata block.

None of this affects the verdict; it makes the rounds harder to compare and the "no new rows" claim
unverifiable from the bundle alone. All three are cheap to restore.

---

### F5-04 — LOW — The bundle is an un-namespaced repo-root directory

ENABLEMENT-04 used `FORMAL-E2E-04-evidence/`; this round writes to `D:\Project\AITutor-X\evidence\`
and the report's header points at it. A generic root-level `evidence/` will collide with the next
round (and with any other task that wants an evidence directory), and it makes the report's
"Evidence index" ambiguous about which round a file belongs to. Suggest `FORMAL-E2E-05-evidence/`.

---

### F5-05 — LOW — "null" is not "absent", and the difference is contract-relevant

§1.3 records:

```text
source_content_sha256 = null
identity_version      = null
```

But the manifest has **no such keys at all** — its top-level key set is exactly
`source_file, model, annotation_meta, units`. `output_summary.json` renders the absence as `null`
(that is the extractor's choice), and the consumer's own message is the accurate one:
*"Manifest **does not declare** `source_content_sha256`"*. The contract requires the key to be
**declared** with a 64-character lowercase hex value, so "absent" and "declared null" are different
contract states; the report should use the consumer's phrasing. Harmless here, but the same
flattening elsewhere would hide a genuine contract violation.

---

### F5-06 — INFO — Scope of what this round adds

The *stage* conclusion is unchanged from ENABLEMENT-04 (CONSUMER / `MISSING_IDENTITY`). What is new is
(a) an independent re-run that reproduces the same unit structure from a different LLM output,
(b) raw logs instead of authored prose, and (c) corrected authority tiers. The Owner should read this
as **reproducibility evidence for a known blocker**, not as a second independent blocker — and the
Change Proposal in §5 is the same one EN-04 raised (identity generation into the formal preprocessing
step, or a defined post-step), still unimplemented by design.

---

## 3. Owner decision list

| # | Decision | Inputs | Blocking? |
|---|---|---|---|
| **D-1** | **Authority: freeze the contract, or re-derive the identity gate from frozen material?** The gate that produced this FAIL lives in a document whose own header says "NOT FROZEN"; the frozen Spec defines Path B but not the identity key. | F5-01 | **Yes** — it determines what authority a FAIL verdict carries |
| **D-2** | **Re-register "Path B has no persistent ingest entry" as its own gap**, since it blocks Path B even after identity is fixed (`90 §H-C` + `runner.py` rollback). | F5-02 | **Yes** |
| **D-3** | **Authorize producer-side identity** (formal `reslice_pipeline.py` step) **or** define a legal post-step; both remain unimplemented. | §5 Change Proposal | **Yes** — it is the only route to Path B downstream |
| **D-4** | **Restore comparison-grade evidence metadata** (DB before/after snapshots, 6/6 spec hashes, run id). | F5-03 | No |
| **D-5** | **Namespace the evidence bundle** (`FORMAL-E2E-05-evidence/`). | F5-04 | No |
| **D-6** | **Should the V3-side contract obligations** ("验证 Manifest / 重算 hash", contract `:66`, recorded as unimplemented) **enter the same decision batch** as the producer-side identity gap? | F5-01 | No |

---

## 4. Findings summary

```text
F5-01  MEDIUM   The blocking gate is defined by a contract that declares itself DRAFT / NOT FROZEN,
                while the report titles the round "Frozen Spec Path B"; the frozen Spec defines the
                path, not the identity key; contract :66 records V3-side duties unimplemented      [DV]
F5-02  MEDIUM   EN-04's F04-02 ("consumer never persists") dropped from the GAP list to a §3.4
                parenthetical → the decision list under-counts a gap that blocks Path B even after
                identity is fixed                                                                    [DV]
F5-03  LOW      Evidence metadata shrank: no DB snapshot (yet "no new rows" is asserted), 3/6 spec
                hashes, no run id / DATABASE_MODE                                                     [DV]
F5-04  LOW      Bundle written to un-namespaced repo-root evidence/ (EN-04 used a round-namespaced dir) [DV]
F5-05  LOW      "source_content_sha256 = null" — the key is absent, not declared-null; the consumer's
                "does not declare" is the accurate phrasing                                          [DV]
F5-06  INFO     The round adds reproducibility evidence for a known blocker, not a new blocker       [DV]
```

**Credited (verified):** genuine re-run with different LLM output and identical unit structure; raw
pipeline/runner logs; `markdown_sliced` hash corrected; Spec-vs-Contract tier claim now accurate
(my F4-01 adopted); contract hash and its identity clause verified; four-repo snapshot with
`NO_GIT` recorded honestly; "HEAD（验证前）" correctly named; code modifications 0 in both git repos;
all artifact/input hashes reproduced byte-exactly; no manual manifest patching, no gate bypass, no
Native Path use.

---

## 5. Reviewer side-effects

1. Nothing written under `AITutors-v3`, `Papers` or `Aitutors-preprocessing`; no state-mutating command
   executed; database access was `SELECT`-only.
2. Verification was hashes + file reads + one code/doc read pass.
3. The push of `fa3a01c` and `787e1fa` to `origin/main` (which had been failing on network errors)
   succeeded during this review: `5de14d1..787e1fa  main -> main`.
