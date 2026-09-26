# FORMAL-E2E-ENABLEMENT-03 · DSH Independent Adversarial Review

**Subject**: `Docs/60_REPORTS/FORMAL-E2E-ENABLEMENT-03-REPORT.md` (249 lines)
**Subject commits**: AITutors-v3 `5f097f627de79a8f3c45f1c0bd22f49247f29cb9` · AITutor-X `871ccfcc95631f85903be93250a43af5304aff2c` · Papers unchanged (`e7c79b6`)
**Reviewer**: DSH, independent adversarial reviewer. Read-only on `AITutors-v3` / `Papers`; no code,
Frozen Spec, governance document or producer data modified; no destructive command executed.
**Date**: 2026-09-26
**Scope**: factual claims, evidence base and decision inputs. Business semantics not adjudicated.

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
VERDICT  : ACCEPTED WITH FINDINGS
FINDINGS : F3-01 … F3-10   (3 P1 · 4 MEDIUM · 2 LOW · 1 INFO)

Progress since ENABLEMENT-02, verified:
  F2-02 response diagnosability → ADDRESSED (finish_reason / response_chars / response_bytes now recorded)
  F2-03 sticky actual_*         → FIXED (reset before every call, both layers)
  F2-04 run metadata            → LARGELY ADDRESSED (three repos + 6 spec hashes + doc hashes recorded)
  first gate artifact ever produced by this chain: 13 persisted admission candidates

Still weak / newly found:
  F3-01 the Resolver/IR tables are an out-of-band in-process replay, not captured pipeline output
  F3-02 §5.1 prints stale figures (16 / 855) that contradict the run's own artifact (8 / 3501)
  F3-03 the new isolation guard is default-ALLOW for the empty/unset case the report says it refuses
  F3-04 the recorded GIT_COMMIT block does not identify the code that actually ran
  F3-05 the "no inheritance" fix is unproven (the cited evidence cannot distinguish reset from
        no-reset) and, as in the last two rounds, zero tests were added
  F3-08 the authorization/budget leg (F2-01 / D-1) is untouched and is not mentioned anywhere
```

The business outcome is the most substantive of the three rounds: the chain now reaches
Compiler/Admission and leaves a persisted gate artifact. The findings are about evidence tier and
about a FACT-table number that is simply wrong.

---

## 1. Verified correct (credited)

1. **The pipeline really ran and really produced gate artifacts.** DB: `documents 2`,
   `semantic_annotations 2` (both `status=valid`), `admission_candidates 13` (all
   `decision_status=pending_review`), `questions 0`, `question_instances 0`, `materials 0`,
   `unit_groups 0`, `admission_events 0`; both tasks and both claims `succeeded`. This matches §0/§5.5
   exactly and is the first persisted Admission output in this chain. (DV)
2. **Both LLM calls are real, distinct and completed.** `llm_call_audit`:
   `mimo / mimo-v2.6-pro / completed / 2407-1558-3965` and `… / 16341-5685-22026`, matching §5.2 and
   the artifact. (DV)
3. **Response diagnosability (my F2-02) is addressed.** `http.py` now records
   `last_finish_reason` from `choices[0].finish_reason`, plus `response_chars` and `response_bytes`;
   both records show `"finish_reason": "stop"` — so the EN-02 "JSON parse failure" class is no longer
   indistinguishable from truncation. This is a real, targeted fix. (DV)
4. **Reality anti-pollution (my F2-03) is fixed in code.** `HTTPLLMProvider.complete()` and
   `gateway._live()` both reset the `last_*` reality state *before* each call, so a failed call can no
   longer inherit the previous call's model/usage. (VI)
5. **No raw content and no secret in the new parse evidence.** The annotation-service change records
   only `type(exc).__name__`, `len(response)` and `len(response.encode("utf-8"))` — verified in the
   diff; no content, no key material. (DV)
6. **Run metadata capture (my F2-04) is largely addressed.** The artifact now carries `E2E_RUN_ID`,
   `DATABASE_MODE`, start/end times, the HEAD of all three repositories, all six `V3_SPEC` hashes, and
   per-document sha256/bytes. (DV)
7. **§5.6's API-existence table is accurate.** The app's routers expose exactly admin/stats,
   candidates get/approve/reject, documents import/list/get/source-quality/source-lines and tasks —
   and no question/material/instance route. The report's YES/NO lists match. (DV)
8. **Frozen Spec unchanged** — I re-verified all six hashes; they equal the values recorded in the two
   preceding rounds and the values in the artifact. (DV)
9. **Posture discipline is correct.** 13 candidates `pending_review`, no call to
   `/api/candidates/{id}/approve`, outcome declared `PARTIAL` with the blocker recorded and classified
   `BLOCKED_BY_SEMANTIC_DECISION`. Not self-adjudicating business semantics is exactly right.

---

## 2. Findings

### F3-01 — P1 · The Resolver / IR results in §5.3–§5.4 are an out-of-band in-process replay, not output captured from the formal run

`e2e_run/formal_e2e_v3.py:175-237` (`annotation_stage_summary`) imports pipeline internals directly
and re-executes the logic inside the orchestration process:

```python
from app.domains.compile.ir import IRBuilder
from app.domains.gate.service import _annotation_identity_projection
from app.domains.resolver.resolver import SourceResolver
from app.domains.resolver.span import SourceLineView
...
views = tuple(SourceLineView(line_ref=L["line_ref"], seq=L["seq"], text=L["text"]) for L in lines)
resolver = SourceResolver(source_version_id=sv_id, lines=views)
run = resolver.resolve(_annotation_identity_projection(payload))
ir = IRBuilder.build(run, _annotation_identity_projection(payload), sv_id, uuid.UUID(...))
```

The result is written into the artifact's `annotation_resolver_ir` block, from which §5.3
("standalone 32 resolved / 17 unresolved", "material 55 resolved / 8 unresolved") and §5.4
("standalone 0 ready / 7 incomplete", "material 13 ready / 8 incomplete") are taken. No resolver or
IR output is persisted by the pipeline itself (there is no such table), so this replay is the **only**
evidence for those two tables.

Why this matters:
- §5.3/§5.4 present the numbers as the pipeline's stage results. They are a *second execution* of the
  resolver/IR code, driven by a hand-built `SourceLineView` sequence and a private gate helper
  (`_annotation_identity_projection`). If the replay diverged from what the worker computed, nothing
  in the delivered evidence would show it.
- Directly constructing/importing internals to generate evidence is the pattern earlier task books in
  this chain explicitly forbade for E2E evidence.

Mitigating, and worth stating: the persisted `admission_candidates = 13` independently corroborates
"13 ready" for the material document, and both annotation payloads are real. So this is an
**evidence-tier** finding, not an allegation that the numbers are false. The script's own docstring
calls the block a "read-only diagnostic", which is honest at the code level but not carried into the
report.

Fix shape: capture the resolver/IR outcome from the worker's own execution (log line or a persisted
diagnostic row keyed by `E2E_RUN_ID`), and label the in-process replay as a *reproduction check*
rather than the source of the pipeline tables.

---

### F3-02 — P1 · §5.1's figures contradict the run's own artifact

| Source | `source_figures` | `document_source_spans` | `document_source_lines` |
|---|---|---|---|
| Report §5.1 | **16** | **855** | "(see artifact import_counts)" |
| Artifact `staged.import_counts` | **8** | **3501** | **820** |
| Database (verified) | **8** | **3501** (922 for the 90-line doc + 2579 for the 730-line doc) | **820** |

`16` and `855` are exactly ENABLEMENT-02's single-physics-document counts — carried over from the
previous report. This is a wrong number inside a section labelled **FACT**, and the discrepancy is
against the implementer's own committed evidence file, not against my reconstruction. (DV)

---

### F3-03 — P1 · The new isolation guard is default-ALLOW for the case the report says it refuses

**Report §1.2**:

```text
ALLOWED_RESET_MODES = {test, fresh_test}
DATABASE_MODE=production / dev / ""  →  REFUSE
```

**Code** (`formal_e2e_v3.py`):

```python
:242   database_mode = os.environ.get("DATABASE_MODE") or "fresh_test"     # unset/"" -> fresh_test
:244   os.environ["DATABASE_MODE"] = database_mode
:298   evidence["db_reset"] = await reset_db_guarded(database_mode)        # -> whitelisted -> ALLOW
:73    if database_mode not in ALLOWED_RESET_MODES: raise RuntimeError(...)
```

An **unset or empty** `DATABASE_MODE` is normalised to `fresh_test` *before* the guard sees it, so the
guard allows the 25-table `TRUNCATE … CASCADE`. Only the two explicitly spelled values (`production`,
`dev`) refuse. The one case the guard exists to catch — an operator who forgets to set the variable —
is the case it does not cover.

The guard itself is a genuine improvement over EN-02 (where the truncate was unconditional), it is
explicit, and it is recorded in the artifact (`allowed_modes`). It is simply not fail-closed. Making
the default a non-whitelisted sentinel (and refusing unless the value is explicitly listed) would
close it in one line.

---

### F3-04 — MEDIUM · The recorded `GIT_COMMIT` block does not identify the code that ran

Artifact:

```json
"GIT_COMMIT": {
  "AITutors-v3": "7702de9c36927a30907d23791d8ab64b09bc8c5a",
  "Papers":      "e7c79b6ce9c61e1ee5f301170d0649d4f50d1b90",
  "AITutor-X":   "0e4747d90308de227a8504f411de39c7915e59e7"
}
```

- The v3 value is the **previous task's** commit. The run's evidence contains `finish_reason`,
  `response_chars`, `response_bytes` and `parse_error_type`, which exist only in `5f097f6` —
  committed at **13:06:33**, i.e. *after* the run started (13:02:48). The E2E therefore executed
  **uncommitted working-tree code** while recording the base commit.
- The AITutor-X value is `0e4747d`, my review commit from the previous round — not the revision that
  produced this evidence (which by construction cannot name itself, but the field should say so).

So "GIT_COMMIT" as recorded identifies the *starting* state, not the executed revision — for the very
commit whose diff introduced the fields the evidence contains. The delivery summary's phrase
"三仓 GIT_COMMIT" also overstates §1.1, which prints only the v3 line.

Recommendation: record `HEAD` **plus** a dirty-tree indicator (or commit the measured code before
measuring it), and label the AITutor-X entry as the base revision. Credit remains: capturing three
repos + six spec hashes + per-document hashes is a real advance over EN-02.

---

### F3-05 — MEDIUM · The "no inheritance" fix is verified only by construction, and its cited evidence cannot distinguish reset from no-reset

`HTTPLLMProvider.complete()` and `gateway._live()` now clear the reality fields before each call —
this is a correct fix for the stickiness I raised (F2-03). But §1.4 offers as *proof*:

> 证据：两条 reality 记录各自绑定 request_id，usage 不同（2407/1558 vs 16341/5685），无继承。

Two calls with different responses produce different usage **with or without any reset**. The
discriminating case is: call 1 succeeds, call 2 **fails** → call 2's record must show
`actual_model = null` and `actual_usage = null`. Nothing in the artifact covers that, and no test does
either: `5f097f6` touches five application files and **zero test files**, and the orchestration script
has no test.

That makes three consecutive rounds in which new behaviour ships untested (FE-09, F2-05, F3-05) —
isolation gate, response evidence, reality reset, and parse evidence all rest on code reading alone.

---

### F3-06 — MEDIUM · The reality record's `parse_error_type` cannot represent the failure it was introduced for

`last_parse_error_type` is set only by `HTTPLLMProvider` inside the adapter-contract handler
(`KeyError / IndexError / TypeError / JSONDecodeError` on the **HTTP body**, plus `ContentNull`). The
ENABLEMENT-02 blocking point was a different parse — `json.loads` in
`app/domains/annotation/service.py` — and its new evidence goes into the **exception message**
(`[parse_error_type=… response_chars=… response_bytes=…]`), which lands in
`task_claims.lease_snapshot.error_detail`.

Both parses succeeded this run, so `parse_error_type: null` is trivially correct and the new reality
field has never been exercised against its motivating failure. Report §1.3's note does distinguish
the two paths, so this is a field-semantics gap rather than a false claim — but a reader of
`provider_reality.json` alone still cannot see an EN-02-class annotation parse failure.

Minor robustness note in the same block: the `has_shared_material` probe
(`(u.get("shared_components") or {}).get("material")`) would raise `AttributeError` if a payload
carried `shared_components` as a **list** — which is the shape V3's own IR uses. It returned `false`
here only because the key is absent/dict-shaped.

---

### F3-07 — MEDIUM · OBS-03-01 is the recurrence of a registered finding, and its premise about the adapter is wrong

The round-13 baseline registered **E2E-BL-04**: the annotation prompt's `role` vocabulary is
`{stem, option, answer, explanation}` with no `shared_material` role, so composite / shared-material
semantics **cannot** be expressed; the consumer adapter carries the matching gap code
`STANDALONE_MATERIAL_NOT_CONSUMED` (`backend/scripts/preprocessing_consumer/annotation_adapter.py:38-40`).
This round's evidence — 21/21 `standalone_unit`, `has_shared_material: false`, every
`shared_components: []` — is precisely the predicted consequence. It is expected by construction, not
a new observation, and the report records it as OBS-03-01 / Owner decision #2 without citing
E2E-BL-04 or the adapter's gap code.

More consequential for Owner decision #2: **the adapter is not on the formal path at all.** The formal
chain imports the PDF and has V3's own LLM annotate it; `backend/scripts/preprocessing_consumer/`
consumes producer *manifests* and is never invoked by `formal_e2e_v3.py` or by the worker, and the
producer's `.md`/manifest output still cannot enter `POST /api/documents/import`
(`_ALLOWED_EXTENSIONS = {".pdf", ".docx"}`, round-13 E2E-BL-07). So:
- the "Adapter" blocker listed as removed in ENABLEMENT-01 has no bearing on formal-path composite
  semantics;
- the lever for composite/shared-material is the **annotation prompt vocabulary** (or a resolver-side
  inference), not the adapter.

That is constructive input the Owner does not currently have. The question "who should declare
composite semantics" should be asked against the prompt, with the adapter's role clarified as
out-of-band.

---

### F3-08 — LOW · The authorization/budget leg is untouched and is not mentioned

The report's §2 ("未修改列表") and §9 checklist do not refer to authorization or budget at all, yet the
composition is unchanged since ENABLEMENT-02 and this run exercised it again. DB confirms the same
shape: two `task` accounts `limit=100, used=1` and two `request` accounts `limit=1, used=1` — i.e. the
authorization probe still reads only the `task` dimension (`remaining = 100` at check time, always
available) while the binding constraint is the `request` account. My previous finding **F2-01 / D-1**
therefore remains open and unaddressed, and an Owner reading ENABLEMENT-03 could reasonably conclude
the authorization story is settled.

---

### F3-09 — LOW · Untracked evidence file still sits in the consumer repo

`git status` in `AITutors-v3` still reports `?? backend/provider_reality.json` (repeat of F2-07). The
durable copy inside the AITutor-X artifact is what makes this acceptable; the consumer worktree is
still not clean.

---

### F3-10 — INFO · One carried-forward claim narrowed without notice

Papers was not touched this round (`e7c79b6` unchanged), so the half-unified state I reported as F2-08
(`except FileNotFoundError` still in `Papers/tests/test_no_config_import.py:47`; `_redact` still absent
from `Papers/scripts/reslice_pipeline.py`) persists. §2 says "Papers preprocessing 历史断言 / redact —
NOT TOUCHED（任务排除）", which is a fair statement of scope; I record it only so the Owner does not
read the ENABLEMENT-02 "PASS-5 preprocessing model config unified" line as covering it.

---

## 3. Owner decision list

| # | Decision | Inputs | Blocking? |
|---|---|---|---|
| **D-1** | **Must the Resolver/IR tables be captured from the worker's own execution** rather than re-derived in-process by the orchestration script? | F3-01 | **Yes** — it decides the evidence tier for two pipeline stages |
| **D-2** | **Accept §5.1 as corrected (8 / 3501 / 820)** and require FACT numbers to be generated from the artifact rather than retyped? | F3-02 | No, but it is a wrong number in a FACT block |
| **D-3** | **Make the reset guard fail-closed** (unset/empty ⇒ refuse)? | F3-03 | **Yes** — the destructive path is currently default-allow |
| **D-4** | **Record the executed revision** (HEAD + dirty marker, or commit before measuring) and label the base commits as base? | F3-04 | No |
| **D-5** | **Require a test for the reset semantics** (success-then-failure must show null actual_*), plus tests for the gate and the response-evidence fields? | F3-05 | Recommended |
| **D-6** | **Should the reality record carry annotation-parse evidence**, or is `task_claims.lease_snapshot.error_detail` the agreed home? | F3-06 | No |
| **D-7** | **Composite semantics: change the annotation prompt vocabulary (or infer structurally), and record that the consumer adapter is not on the formal path?** | F3-07 | **Yes** for decision #2 of the report |
| **D-8** | **Close F2-01/D-1 (budget authorization) or restate it as open** — it is currently invisible in this report. | F3-08 | **Yes** |
| **D-9** | **Where should `provider_reality.json` live** (commit it, or write outside the consumer worktree)? | F3-09 | No |

---

## 4. Findings summary

```text
F3-01  P1       Resolver/IR tables are an out-of-band in-process replay (direct SourceResolver /
                IRBuilder / _annotation_identity_projection imports), not captured pipeline output  [DV/VI]
F3-02  P1       §5.1 prints source_figures=16 / spans=855; artifact and DB say 8 / 3501 / 820     [DV]
F3-03  P1       Isolation guard default-ALLOW: unset/"" -> normalised to fresh_test before the
                guard runs, so TRUNCATE proceeds in exactly the accidental case                [DV]
F3-04  MEDIUM   GIT_COMMIT block records the base commit, not the executed (uncommitted) code;
                AITutor-X entry names a reviewer commit                                           [DV]
F3-05  MEDIUM   Reset/un-inheritance proven only by construction (differing usages prove nothing);
                zero tests added for any of the four new behaviours                            [DV/VI]
F3-06  MEDIUM   reality.parse_error_type covers HTTP-body parse errors only, not the annotation
                JSON parse failure it was introduced for                                      [VI]
F3-07  MEDIUM   OBS-03-01 recurs a registered finding (E2E-BL-04) and mis-frames the lever: the
                consumer adapter is not on the formal path                                      [DV/VI]
F3-08  LOW      Authorization/budget leg (F2-01 / D-1) untouched and unmentioned in this report    [DV]
F3-09  LOW      backend/provider_reality.json still untracked inside the consumer repo             [DV]
F3-10  INFO     Papers half-unification (F2-08) persists; scope statement is fair but easy to
                over-read                                                                          [DV]
```

---

## 5. Reviewer side-effects

1. No file under `AITutors-v3` or `Papers` was written; V3 remains at `5f097f6` with the same
   untracked set (`backend/provider_reality.json` was created by the subject run, not by me).
2. No test suite executed; no destructive command run; database access was `SELECT`-only via
   `docker exec aitutor-postgres psql -U aitutors -d aitutors`.
3. No key material printed.
