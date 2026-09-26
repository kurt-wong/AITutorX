# FORMAL-E2E-ENABLEMENT-02 · DSH Independent Adversarial Review

**Subject**: `Docs/60_REPORTS/FORMAL-E2E-ENABLEMENT-02-REPORT.md` (280 lines)
**Subject commits**: AITutors-v3 `7702de9c36927a30907d23791d8ab64b09bc8c5a` · Papers `e7c79b6` · AITutor-X `ce3c149`, `e038abf`
**Reviewer**: DSH, independent adversarial reviewer. Read-only on `AITutors-v3` and `Papers`; no code,
Frozen Spec, governance document or producer data modified; the V3 test suite was **not** executed
(it is destructive — see F2-05).
**Date**: 2026-09-26
**Scope**: factual claims, evidence base, and completeness of decision inputs. Business semantics are
not adjudicated.

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
VERDICT  : ACCEPTED WITH FINDINGS
FINDINGS : F2-01 … F2-10   (1 P1, 3 MEDIUM, 3 LOW, 3 INFO)

This round is a genuine, substantial improvement on ENABLEMENT-01.
Of the previous review's findings, FIVE are now substantively closed:
  FE-03 actual provider/model now really comes from the API response body      → CLOSED
  FE-04 the formal entries really are the API + the worker CLI (subprocess)    → CLOSED
  FE-06 both evidence artifacts exist and are committed                        → CLOSED
  FE-10 usage is parsed from the response; audit token columns are populated   → CLOSED (tokens)
  FE-01's disclosure half: the DB reset is now recorded in the evidence        → CLOSED (disclosure)
  (plus REPORT-L RL-09: the step0_blind_test.py legacy default)                → CLOSED

ONE is not closed in substance, and this round makes the reason provable:
  FE-02 budget fail-open → the literal True is gone, the default is False,
        check() can fail in isolation … and the authorization decision is STILL a constant,
        because ensure() mints the account (limit 100) one line before check() reads it,
        and the probe inspects only that dimension (F2-01).
```

Everything the report states as FACT in §1 reproduced exactly against the database and the
committed artifacts. The weaknesses are in what the mechanism *cannot* do (F2-01, F2-02, F2-03) and
in a reproducibility claim that is asserted rather than effected (F2-04).

---

## 1. Verification tiers

| Tier | Meaning | Applied to |
|---|---|---|
| **DV** | Reproduced this session from the system itself | DB rows (task, claim, audit, budget, counts), evidence JSON, worker log, commit contents, code paths, Frozen Spec hashes, file existence |
| **VI** | Code read, contract deduced | budget check composition, reality stickiness, provider parsing, reset guard |
| **DC** | Inherited/asserted, not re-tested | that the E2E run and the test run were ordered as implied |
| **UNKNOWN** | Not establishable from artifacts | whether the annotation JSON failure was truncation or malformed output |

Reproduction log: `review_f2_evidence/f2-verification-log.txt`.

---

## 2. Verified correct — credited (this is not a formality)

1. **Formal entry discipline is now real (FE-04 closed).** `e2e_run/formal_e2e_v2.py:39-70` starts
   `uvicorn app.main:app` as a subprocess and imports over HTTP (`httpx.post` to
   `/api/documents/import`, line 183-187), then runs the worker as
   `subprocess.run([PYTHON, "-m", "app.worker", "run", "--allow-live"])` (line 55-62), capturing exit
   code, stdout and stderr into a committed log. The log
   (`e2e_run/formal-e2e-v2-worker-E2E2-20260926T121829.log`) shows the CLI-only flush line
   `provider reality evidence: provider_reality.json` followed by `processed 1 task(s)` — a line that
   only the CLI can emit. There is no in-process `TaskExecutor` construction anywhere. This closes
   FE-04 and the corresponding claim in §0. (DV)
2. **Actual provider/model really comes from the response (FE-03 closed).** `http.py` now sets
   `last_response_model = data.get("model")` and `last_response_usage = data.get("usage")`, and
   `gateway._live()` reads them **after** `await live.complete(prompt)` and only then from the
   provider object. The recorded reality record carries
   `"actual_model": "mimo-v2.6-pro"` with
   `completion_tokens_details.reasoning_tokens: 1323` and `prompt_tokens_details.cached_tokens: 8576`
   — values no configuration file contains and which could only have come from the provider body.
   `llm_call_audit` token columns, NULL in the previous round, are now
   `8607 / 4510 / 13117`. (DV)
3. **`authorize()` default is now fail-closed** (`budget_ok: bool = False`) with tests asserting both
   that default and the `task_context=None` rejection. (DV)
4. **The step0 blind-test legacy default is fixed** — `scripts/step0_blind_test.py:29` now defaults to
   `mimo-v2.6-pro`, closing REPORT-L's RL-09. (DV)
5. **The DB reset is disclosed and structurally recorded.** `db_reset.truncated_tables` lists the 25
   public tables (excluding `alembic_version`) and `reset_at`. The previous review's central complaint
   — that a reset happened silently — is addressed; the reset is now a declared, inspectable step. (DV)
6. **Every §1 FACT reproduced exactly.** Import HTTP 200 with the stated document/task ids and
   `is_new=true`; `exit_code=0`; claim `5646f2f8-…` `outcome=failed` / `error_type=validation_error`
   with `error_detail` byte-identical to §1.2; audit row `mimo / mimo-v2.6-pro / completed` at
   `2026-09-26 04:18:33.783624+00` with `8607 / 4510 / 13117`; counts `documents 1,
   semantic_annotations 0, questions 0, admission_candidates 0, source_figures 16,
   document_source_spans 855`; budget rows for request/task/le/document/daily, all `used=1`. (DV)
7. **Frozen Spec 6/6 unchanged** — I verified all six hashes against the values recorded in the two
   preceding rounds (the report prints two of them; see F2-09). `backend/app/core/config.py` and
   `Docs/V3_SPEC` are untouched. (DV)
8. **Both evidence artifacts are delivered and committed** (`ce3c149` + `e038abf`), and the run JSON
   embeds the provider-reality record rather than merely pointing at it — which is what makes the
   reality evidence durable. (DV)

---

## 3. Findings

### F2-01 — P1 · The budget authorization decision is still a constant, and the probe watches the wrong account

**Report claims**: §0/§4.1 PASS-3 *"No hardcoded budget approval — `check()` 决定 `budget_ok`；默认 False"*;
§2.4 *"budget 不再 fail-open"*; Issue-03 on the delivery summary: *"`authorize(budget_ok=False)` 默认；
`BudgetService.check()` 可失败；4 条单测全绿"*.

**VI — the composition, in order (`app/domains/task/executor.py`):**

```python
task_ref = AccountRef("task", str(task_id))
await budget.ensure(task_ref)      # get-or-create: INSERT ... ON CONFLICT DO NOTHING
await s.commit()                   # limit = DEFAULT_LIMITS["task"] = 100, used = 0, reserved = 0
budget_ok = await budget.check([task_ref])   # remaining = 100 - 0 - 0 = 100  >=  probe = 1  →  True
self._gateway.authorize(task_context=real_context, budget_ok=budget_ok)
```

`check()` returns `False` only when `remaining is None` (no account) or `remaining < 1`. The account
is created, with a 100-unit default limit, on the line immediately above the check. **`budget_ok` is
therefore `True` for every task, unconditionally, on the formal worker path.**

**DV — the implementer's own test encodes exactly this composition as expected behaviour:**

```python
# tests/test_budget_check.py:18-24
async def test_budget_check_after_ensure_available(session):
    ref = AccountRef("task", "task-check-1")
    await svc.ensure(ref)
    await session.commit()
    ok = await svc.check([ref])
    assert ok is True        # a brand-new task id → available
```

**DV — and the probe inspects a dimension that cannot bind, while the binding dimension is right
there in this run's own data:**

```text
budget rows after the run (limit | used | reserved):
  request  | 1    | 1 | 0      ← the real per-request cap; remaining = 0
  task     | 100  | 1 | 0      ← the only dimension check() looks at
  le       | 50   | 1 | 0
  document | 500  | 1 | 0
  daily    | 2000 | 1 | 0
```

`five_account_refs()` constrains a call with `DEFAULT_LIMITS["request"] = 1`. Had the availability
probe been aimed at the **request** account, `remaining` would be `0 < 1` and `check()` would return
`False`. Aimed at the **task** account — the one with a 100-unit limit — it can never fail. So the
probe is not merely weak; it is dimensionally mismatched to the constraint that actually governs LLM
calls.

The literal `True` is gone, the default is `False`, and `check()` is a real function with real unit
tests — all improvements in form. But the *authorization decision* is unchanged: this is the third
consecutive round (EE-01 → FE-02 → F2-01) in which the budget leg is the weak leg, and this round
supplies the proof that it is structural, not incidental.

For the leg to become falsifiable at least one of these must hold: the check must run **before** the
account is minted; the account must carry an independently authorized limit/quota (a task-scoped
grant) rather than `DEFAULT_LIMITS`; or the probe must cover the five accounts that
`five_account_refs` actually consumes.

---

### F2-02 — MEDIUM · The declared FIRST BLOCKING POINT is under-determined: V3 cannot distinguish a truncated response from malformed output, and preserves neither

**Report claims**: §4.2 — stage *"Semantic Annotation (JSON parse)"*, error *"LLM response not valid
JSON: Expecting ',' delimiter: line 1 column 9898 (char 9897)"*, with the note *"Provider 调用本身成功
（audit=completed，tokens 齐全）；失败发生在响应 JSON 结构校验"*.

**DV/VI:**

- `git grep -n "finish_reason\|max_tokens" -- backend/app` → **no hits anywhere in the V3 backend.**
  The request body is `json={"model": self._model, "messages": [{"role": "user", "content": prompt}]}`
  (`providers/http.py:63`) — no `max_tokens` — and `choices[0].finish_reason` is never inspected.
- The producer's own `call_llm` treats `finish_reason == "length"` as a hard error; V3's adapter does
  not, so a truncated body reaches `json.loads` and surfaces as a syntax error.
- `Expecting ',' delimiter … char 9897` is the canonical symptom of a body cut short inside a
  structure. "The model emitted syntactically invalid JSON deep inside a ~9.9 KB single-line document"
  and "the response was truncated" are **indistinguishable** with the delivered evidence.
- The raw response is preserved **nowhere**: `llm_call_audit` stores no content, and the only trace is
  the one-line `error_detail` in `task_claims.lease_snapshot`.

The report is scrupulous about not speculating *downstream* (§4.2 "不推测后续"), and LIMITATION 5
concedes the failure is stochastic — but the *cause category* it assigns (JSON structure) is itself a
hypothesis, and the competing one is not mentioned. Recording `finish_reason` (and a response length
or hash) alongside the failure would settle it; that is a one-line addition in `http.py`, and it is
the difference between a blocking point that can be acted on and one that must be re-guessed.

Note also that V3's adapter contains a "reverse" case of the same blind spot: HTTP 200 with a body
violating the adapter contract is carefully translated to `LLMProviderError(retryable=False)`, while
HTTP 200 with a *truncated* body is passed through as valid content.

---

### F2-03 — MEDIUM · `actual_model` / `actual_usage` are sticky: a failed invocation inherits the previous call's values, and the code writes them into the failed audit row

**VI — the assignment sites:**

```python
# gateway._live(): assigned ONLY on the success path
self._last_actual_provider = getattr(live, "name", ...)     # before the call (unchanged from EN-01)
result = await live.complete(prompt)                        # raises here → the next two lines never run
self._last_actual_model = getattr(live, "last_response_model", None)
self._last_actual_usage = getattr(live, "last_response_usage", None)

# ai/executor.py: read unconditionally, then used for BOTH terminal branches
_in_toks = _usage.get("prompt_tokens"); _out_toks = ...; _tot_toks = ...
await repo.finalize_audit(request_id, status="completed", input_tokens=..., ...)
await repo.finalize_audit(request_id, status="failed",    input_tokens=..., ..., error_type=...)
```

The `_last_actual_*` attributes are never reset per invocation, and `HTTPLLMProvider.last_response_*`
are only written on a successful parse. So for the second and later calls on the same gateway/provider
object, a **failed** call is recorded with the **previous** call's model and token counts, and those
tokens are then written into the failed row of `llm_call_audit` — the table this chain treats as
runtime truth and accounting.

This run made exactly one call, so its own record is self-consistent; the defect is latent and
becomes material the moment retry/fallback (`LLMExecutor` retry, `fallback` provider routing) or a
multi-document worker pass occurs. Correcting it is small: reset `last_response_*` before each call
(or read them only when `outcome is not None`).

---

### F2-04 — MEDIUM · `E2E_RUN_ID` / `DATABASE_MODE` are inert labels, and `DATABASE_MODE` does not guard the destructive reset

**Report claims**: §0/§4.1 PASS-6 *"E2E evidence reproducible = YES (`E2E_RUN_ID` + `DATABASE_MODE`)"*;
Issue-05 *"运行身份 … 证据可复现"*.

**DV/VI:**

- `git grep DATABASE_MODE` across the **entire** V3 repository → **no hits** outside the e2e script and
  `.env`. No application or test code reads it; neither value is persisted into any row.
- `reset_db()` (`formal_e2e_v2.py:113-127`) is invoked unconditionally at line 157, **before** any
  inspection of `DATABASE_MODE`, and executes
  `TRUNCATE <all 25 public tables> CASCADE`. Setting `DATABASE_MODE=production` would still wipe the
  database.
- A stamped identifier is not a reproducibility mechanism. Reproducing this run requires the
  ambient `.env` (`MIMO_*`), the exact PDF, *and* the willingness to destroy the database — the two
  variables change none of that.

There is a practical hazard here: this script is now the documented E2E entry, and it is a
destructive tool with no guard, no dry-run, and no refusal path.

---

### F2-05 — MEDIUM · The evidence database is destroyed by the E2E itself, and the destructive test suite is part of the same workflow with no recorded ordering

**DV:** the run JSON's `db_reset.truncated_tables` shows the E2E wiping 25 tables at
`04:18:30Z` before importing; the previous round's rows (its document, task, claim, annotations, and
the 42 audit rows reviewed one hour ago) are gone — the current database holds exactly 1 document,
1 task, 1 claim, 1 audit row, 5 budget rows. The reset is disclosed, which is the right behaviour;
the consequence is that **each round's evidence destroys the previous round's**, so ENABLEMENT-01's
bundle is no longer resolvable against the system.

**VI/DC:** §6 lists a test command that includes `tests/test_task_executor.py` — the suite previously
identified in this chain as destructive (autouse fixture truncating tables). The report does not state
whether those tests ran before or after the E2E; the evidence JSON shows a single reset, at
`04:18:30Z`, which implies the tests ran earlier — but the DB's lineage cannot be reconstructed from
artifacts alone, only from a report line.

Consequently I did **not** reproduce the reported *"61 passed"*. Re-running
`tests/test_task_executor.py` would destroy the evidence under review. This is the same class as the
previous round's unreconciled test figure: a test number offered as evidence that cannot be checked
without damaging the very evidence plane it belongs to. A separate test database (or a
`DATABASE_MODE` that actually gates destructive fixtures — see F2-04) would fix both.

---

### F2-06 — LOW · A no-op "guard" that reads like enforcement inside the reality tracker

```python
# app/ai/provider_reality.py:63-66
# Issue-02: actual_model MUST come from API response; never echo config
if actual_model is not None and actual_model == configured_model:
    pass  # equality is allowed ONLY if response actually returned that model
```

The branch does nothing. The *substance* of Issue-02 is genuinely fixed in `http.py` (credit, §2.2),
so this is dead code — but a comment-shaped pseudo-check inside a module whose whole purpose is
provenance invites a future reader to believe a constraint is enforced where none exists. Recording
provenance (e.g. `actual_model_source: "response"`) would be honest; an empty `if` is not.

---

### F2-07 — LOW · The reality evidence file is written into the consumer repo's worktree and left untracked

`git status` in `AITutors-v3` now reports `?? backend/provider_reality.json` (not gitignored, not
committed). The report §6 lists it among the artifacts. The consumer repository's working tree is
therefore no longer clean, and the file's durability depends entirely on the copy embedded in the
AITutor-X run JSON — which, credit where due, the script does produce. Either commit it under the
evidence repo or write it outside the V3 tree.

---

### F2-08 — LOW · The Papers side is only half-unified, and its own test suite still cannot pass

**Report claim**: §1.5 Issue-04 — *"`Papers/tests/test_no_config_import.py` assert | expects legacy
tag | expects `mimo-v2.6-pro`"*, and PASS-5 *"preprocessing model config unified"*.

**DV:** `e7c79b6` changes exactly one line (the metadata-tag assertion at the end of
`test_write_outputs_offline_without_config`). But:

- `tests/test_no_config_import.py:47` **still** reads `"except FileNotFoundError as e:"`, while the
  new `load_cfg()` delegates to `llm_provider.resolve()` and raises `ProviderConfigError`. The
  subprocess in that test therefore dies, `r.returncode != 0`, and `assert r.returncode == 0` fails:
  Papers' own H-01 regression test still cannot pass against Papers' own code.
- `_redact` is still **absent** from `Papers/scripts/reslice_pipeline.py` (untouched by this commit),
  so Papers remains the reduced port identified in the previous review.

"Active default model strings are unified" is true and worth having; "preprocessing model config
unified" as a PASS statement is broader than what was done.

---

### F2-09 — INFO · §1.6 evidences two of six Frozen Spec hashes

The report prints `00_Master_Spec.md` and `20_Document_Pipeline.md` only, where ENABLEMENT-01 printed
all six. I verified all six independently and all are unchanged, so the claim is true — but the
evidence presented is narrower than a "Frozen Spec integrity" section implies, and narrowing it
between rounds makes the two reports non-comparable at a glance.

---

### F2-10 — INFO · Headline "完成 / VERIFIED" versus `outcome=failed` and 0 questions

The execution summary says **"FORMAL-E2E-ENABLEMENT-02 完成"** and the report §0 says
**"FORMAL PIPELINE E2E PATH VERIFIED"**, while the run's task ended `failed` with
`questions = 0`. The report itself is careful (§4.3 "未声称 FULL PRODUCT COMPLETE"; §4.2 records the
blocking point; LIMITATION 4-5 bound the claims), and all six PASS conditions are *process* conditions
that a failed pipeline can satisfy. So this is optics, not a false claim — but the Owner should read
§4.1 as "the entry points and evidence plumbing are verified", not "the pipeline works". A headline
that says VERIFIED next to `outcome=failed` will eventually be quoted out of context; labelling it
"PATH VERIFIED (pipeline outcome: FAILED at annotation)" would cost nothing.

---

### Observation (not a report finding) — the delivery commit is unpushed

`AITutor-X` HEAD is `e038abf` while `origin/main` is `3a14d92`; the branch is two commits ahead. The
same situation was recorded in the previous round (FE-08). My push of this review will fast-forward
both unless the Owner instructs otherwise; I did not author or amend them.

---

## 4. Owner decision list

| # | Decision | Inputs | Blocking? |
|---|---|---|---|
| **D-1** | **Is `budget_ok` allowed to remain structurally unfalsifiable?** The literal is gone and the default is False, but `ensure()` mints a 100-unit account one line before `check()` reads it, and the probe ignores the `request` account (limit 1) that actually constrains calls. | F2-01 | **Yes** — it decides whether PASS-3 means anything |
| **D-2** | **Must failures record `finish_reason` (and response length/hash) so the blocking point is diagnosable?** Today truncation and malformed output are indistinguishable, and no raw response is kept. | F2-02 | **Yes** for the next round's usefulness |
| **D-3** | **Reset `last_response_*` per invocation, and stop writing tokens into failed audit rows from a previous call?** | F2-03 | No, but it corrupts `llm_call_audit` once retries occur |
| **D-4** | **Accept `E2E_RUN_ID`/`DATABASE_MODE` as documentary labels, or make them functional (gate the destructive reset, stamp rows, or refuse to run when `DATABASE_MODE != fresh_test`)?** | F2-04 | No |
| **D-5** | **Adopt a non-destructive evidence DB** (separate database or a gated destructive fixture), so each round stops destroying the previous round's evidence and test figures become reproducible. | F2-05 | Recommended |
| **D-6** | **Finish the Papers unification** (`except FileNotFoundError`, `_redact`, 4xx branch) or restate PASS-5 narrowly. | F2-08 | No |
| **D-7** | **Keep the no-op guard in `provider_reality.py`?** Replace it with recorded provenance or delete it. | F2-06 | No |
| **D-8** | **Where should `provider_reality.json` live** — committed evidence, or outside the consumer worktree? | F2-07 | No |
| **D-9** | **Authorize the proxy-bypass push, or accept a local-only branch?** | §3 observation | No |

---

## 5. Findings summary

```text
F2-01  P1       budget_ok still a constant: ensure() mints the account (limit 100) immediately
                before check() reads it; the probe ignores the binding request account (limit 1);
                their own test asserts this composition returns True                          [DV/VI]
F2-02  MEDIUM   FIRST BLOCKING POINT under-determined: no finish_reason/max_tokens handling anywhere
                in the V3 backend; raw response preserved nowhere; truncation vs malformed JSON
                indistinguishable                                                                  [DV]
F2-03  MEDIUM   actual_model/actual_usage sticky across invocations; failed calls inherit the previous
                call's model+tokens and those tokens are written into the failed audit row          [VI]
F2-04  MEDIUM   E2E_RUN_ID/DATABASE_MODE read by nothing; reset_db() unconditional and destructive;
                "reproducible = YES" unsupported                                                     [DV/VI]
F2-05  MEDIUM   The E2E truncates 25 tables, so each round destroys the previous round's evidence;
                the destructive test suite is in the same workflow with no recorded ordering; the
                "61 passed" figure is therefore unreproducible without destroying this evidence      [DV/VI]
F2-06  LOW      No-op `if …: pass` "guard" in provider_reality.record                            [VI]
F2-07  LOW      backend/provider_reality.json left untracked inside the consumer repo              [DV]
F2-08  LOW      Papers unified one assertion line only; `except FileNotFoundError` and missing
                `_redact` remain, so Papers' own regression test still cannot pass                  [DV]
F2-09  INFO     §1.6 evidences 2 of 6 Frozen Spec hashes (all six verified unchanged)              [DV]
F2-10  INFO     Headline "完成 / E2E PATH VERIFIED" alongside outcome=failed, questions=0            [DV]
```

---

## 6. Reviewer side-effects

1. No file under `AITutors-v3` or `Papers` was written. V3 remains at `7702de9` with the same 10
   pre-existing untracked paths plus `backend/provider_reality.json` (created by the subject run, not
   by me); `Papers` remains at `e7c79b6` with its 2 untracked run-accounting files.
2. The V3 test suite was **not** executed — F2-05. No destructive command was run against the database.
3. Database inspection was `SELECT`-only via `docker exec aitutor-postgres psql -U aitutors -d aitutors`.
4. No key material was printed; the `MIMO_API_KEY` line was inspected by length only.
