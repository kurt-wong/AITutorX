# FORMAL-E2E-ENABLEMENT-01 · DSH Independent Adversarial Review

**Subject**: `Docs/60_REPORTS/FORMAL-E2E-ENABLEMENT-REPORT.md` (377 lines)
**Subject commits**: AITutors-v3 `d0a67da77448973a245e9ceda83651a7f2968e8d` · Papers `1662121` · AITutor-X `0dc3d90a3ffff28f6c931a344e18cb0a56ea39bf`
**Reviewer**: DSH, independent adversarial reviewer. Read-only on `AITutors-v3` and `Papers`; no code,
Frozen Spec, governance document or producer data was modified; no tests were re-executed in the V3
tree (reason below, FE-09).
**Date**: 2026-09-26
**Scope**: the factual claims of the report, its evidence base, and the completeness of the decision
inputs given to the Owner. Business semantics are **not** adjudicated.

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
VERDICT   : ACCEPTED WITH FINDINGS
FINDINGS  : FE-01 … FE-14   (1 P0-candidate, 4 P1/MEDIUM-high, 4 MEDIUM, 4 LOW/INFO)

SUPPORTED claims
  · provider blocker removed      — build_gateway() really builds mimo/mimo-v2.6-pro; .env switched;
                                    2 real MIMO calls, both completed (DB-verified)
  · adapter blocker removed       — preprocessing_consumer/ mapping is decision-backed normalization,
                                    not a silent rewrite; composite shared material preserved
  · task_context is real          — loaded from the claimed Task row, raises if absent
  · Frozen Spec unchanged         — 6/6 sha256 reproduced exactly; V3_SPEC tree identical

NOT SUPPORTED as written
  · "无 hardcode / bypass"        — budget_ok is a literal True; the one authority that could
                                    contradict it (BudgetService.ensure) is a get-or-create that
                                    cannot fail, and authorize() itself defaults budget_ok=True  (FE-02)
  · "Provider Reality Tracking"   — actual_provider is the local provider object's name, assigned
                                    BEFORE the call; it cannot distinguish executed from attempted (FE-03)
  · "Formal path ... as driven by python -m app.worker run --allow-live"
                                  — the Level-1 runs called TaskExecutor.run_once in-process with
                                    hardcoded provider/model literals; the CLI was not the driver (FE-04)
  · "全链路 evidence 可复核 = YES"— Run A's evidence and provider-reality artifacts do not exist (FE-06);
                                    the resolver/IR blocking-point detail is persisted nowhere (FE-08);
                                    and every global count is read from a database whose entire
                                    content is 10 minutes old, with no reset disclosed            (FE-01)
```

The three blockers named in the report **were** materially addressed. The problem is that the
*evidence plane* around them does not support the strength of the completion claims: the database the
evidence was read from is not the baseline database, two of the five indexed artifacts were never
delivered, and the two claims the task cared most about — no bypass, and declared-vs-actual
separation — are, on inspection, satisfied in form rather than in substance.

---

## 1. Verification method and evidence tiers

| Tier | Meaning | Applied to |
|---|---|---|
| **DV** | Reproduced this session from the artifact/system itself | Frozen Spec hashes, git refs, working-tree state, DB row counts and audit rows, annotation unit counts, commit contents, file existence, pytest collection count, source inspection of the changed code paths |
| **VI** | Read the cited code/line; contract deduced, not executed | budget ensure/create contract, gateway reality assignment, adapter mapping registry |
| **DC** | Inherited claim, not re-tested | that the 31 DeepSeek audit rows were fixture-only |
| **UNKNOWN** | Cannot be established from available artifacts | whether the DB clear was authorized; per-run resolver statistics; which revision produced the reported V3 test totals; provenance of the sandbox "Access denied" line in the delivery message |

Reproduction commands and outputs: `review_fe_evidence/fe-verification-log.txt`.

---

## 2. Verified correct (credited)

1. **Frozen Spec integrity — exact.** All six files under `D:\Project\AITutors-v3\Docs\V3_SPEC` hash
   to the values printed in §1.3 (`c83a5f96…`, `529d133c…`, `0b7aecee…`, `db9f9aad…`, `8b2c10a9…`,
   `8689e741…`) and are identical to the values recorded in the two preceding review rounds. The
   `Docs/V3_SPEC` tree object is `14a7450808…`; `git status` shows **0 modified tracked files** in
   V3, so the working tree equals `d0a67da`. (DV)
2. **The provider switch is real and it ran.** `build_gateway()` (`gateway.py:136-176`) constructs
   `HTTPLLMProvider(name="mimo", api_key=settings.mimo_api_key, base_url=settings.mimo_base_url or
   default, model=settings.mimo_model or MIMO_V26_PRO_MODEL)` with a fail-closed legacy-ID guard;
   `.env` now carries `MIMO_MODEL=mimo-v2.6-pro`; and `llm_call_audit` holds exactly two
   `mimo / mimo-v2.6-pro / completed` rows at `2026-09-26 02:59:54Z` and `03:06:50Z`. (DV)
3. **DeepSeek is genuinely retained-but-inert.** `.env` keeps the `DEEPSEEK_*` lines commented;
   `_build_deepseek_provider()` returns `None` without key+model; `_build_mimo_provider()` is never
   gated on Ollama. This matches §2.2's wording precisely. (DV/VI)
4. **Adapter reuse is substantive, not cosmetic.** `boundary.py:55-56` maps
   `standalone_question→standalone_unit`, `composite_question→composite_unit` with registered
   decision events (`X2.6-OD-2-MAP-STANDALONE-01` / `-COMPOSITE-01`); `annotation_adapter.py:19`
   records that the old hardcoded `standalone_question` rewrite was eliminated; the three gap codes
   §3.2 names exist at `annotation_adapter.py:38-40`. This is a real improvement over the behaviour
   cited in the previous review, and the report is right to reuse rather than re-create. (VI)
5. **Pipeline stages really ran on real PDFs.** Annotation payloads contain **7** and **20**
   semantic units (matching §6.3), sealed line counts are **90** and **609** (matching), payloads use
   canonical `unit_type: "standalone_unit"`, and `admission_candidates = 0`, `questions = 0`,
   `question_instances = 0`, `materials = 0` are exactly as reported. (DV)
6. **Authorization's `task_context` leg is honest.** `_authorize_live_from_real_context()` loads the
   claimed `Task` row from the DB and raises `RepositoryError` if it is missing; `--allow-live` is
   unchanged as the human gate. The dummy-context sin of the baseline round is genuinely gone. (VI)
7. **Ingest used the documented service entry.** Both scripts call
   `DocumentImportService.import_file(...)`, the service behind `POST /api/documents/import`. (VI)

---

## 3. Findings

### FE-01 — P0-candidate · The evidence database is not the baseline database, and no reset is disclosed

**DV — current `aitutors` database:**

```text
documents 2 | source_versions 2 | semantic_annotations 2 | questions 0
question_instances 0 | admission_candidates 0 | materials 0
tasks 18 | llm_call_audit 42 | budget 159 | alembic_version 0011
```

**DV — the entire audit history spans ten minutes:**

```text
select min(start), max(start), count(*) from llm_call_audit
→ 2026-09-26 02:56:46.474509+00 | 2026-09-26 03:06:50.41337+00 | 42
select id, status, created_at from tasks order by created_at desc
→ all 18 rows between 2026-09-26 02:57:56Z and 03:06:49Z
```

**DV — the previous round's entities are gone**, although the baseline round read them from this same
database (`-U aitutors -d aitutors`):

```text
r13_document a7fbeb3a-f3c0-464d-86b5-2d8e5197f0ed        → 0
prior_question a35743e0-2e00-4b11-89af-138861b24c29      → 0
prior_instance 953743dd-15bb-4656-b801-3ae0206e625f      → 0
prior_candidate 54f869a3-ea87-41ab-9591-ff31f2a455b9     → 0
```

versus the baseline round's readings: `documents 4`, `source_versions 3`, `questions 1`,
`question_instances 1`, `admission_candidates 6`, `tasks 11`, `llm_call_audit 961`, `budget 3421`.

**The report never mentions this.** §1.2 "Explicitly NOT done" states "Database migration — **NONE**"
(which is true — the schema version is still `0011` and the 26-table set is unchanged), but says
nothing about **data**. Consequences the report does not draw:

- Every count it reports from `SELECT count(*)` is a reading on an emptied database. §6.3's
  "Question / Instance 0 / 0" is therefore not, by itself, diagnostic of this run's behaviour — it is
  equally consistent with a database in which nothing had ever been inserted (the *mechanism* claim
  rests on FE-08's unpersisted resolver statistics).
- `formal_e2e_level1b.py:109` sets `"semantic_annotations": len(anns)` over the whole table, and
  `:104-106` count the whole `questions`/`question_instances`/`materials` tables. On a cleared DB
  these global readings happen to equal the per-run values; that coincidence is not stated.
- The prior round's evidence bundle is now dangling: the IDs it cites no longer resolve, which means
  the previous "current state" record cannot be re-checked against the system any more.

This is the single most consequential item in this review, because it changes how every other
number in the report may be read. Whether the clear was authorized is an Owner question, not mine.

---

### FE-02 — P1 · `budget_ok` is a hardcoded literal; the budget precondition is unfalsifiable, and `authorize()` defaults it to `True`

**Report claim**: §5.2 — *"3. `gateway.authorize(task_context=real_task_dict, budget_ok=True)`"*,
with §5.2/§10/§12 asserting "no hardcode", "no bypass authorization", "real task/budget
authorization".

**DV/VI — three facts:**

```python
# app/domains/task/executor.py (new in d0a67da)
budget = BudgetService(s)
await budget.ensure(AccountRef("task", str(task_id)))   # return value discarded (it is None)
await s.commit()                                        # authorization COMMITS a budget write
...
self._gateway.authorize(task_context=real_context, budget_ok=True)   # literal True

# app/ai/budget.py:35-41
async def ensure(self, refs, *, limit=None) -> None:
    for ref in refs:
        lim = limit if limit is not None else DEFAULT_LIMITS[ref.account_dim]
        await self._repo.ensure_account(..., limit=lim)     # no raise path for "unavailable"

# app/repositories/runtime_repository.py:144
pg_insert(Budget).values(..., limit=limit, used=0, reserved=0) \
    .on_conflict_do_nothing(constraint="uq_budget_account_scope")   # get-or-create

# app/ai/gateway.py (new in d0a67da)
def authorize(self, *, task_context: object, budget_ok: bool = True) -> None:
```

`ensure()` is a get-or-create that **mints the account with `DEFAULT_LIMITS["task"] = 100`**, returns
`None`, and has no failure branch for "budget unavailable". The `_live()` precondition
`if not self._budget_ok: reasons.append("budget unavailable")` can therefore never fire on the formal
worker path, and `authorize()`'s own signature supplies `True` if a caller omits the argument.

So all three of the forms the task forbade in letter — `hardcode=True`, `object()`, test bypass — are
avoided, while the **budget leg is a constant**. This is the residual of the previous round's finding
`EE-01` (harness self-granted `budget_ok=True`), now promoted from the harness into production code.
The `task_context` leg, by contrast, is genuinely real (credit, §2.6).

Two secondary observations in the same code path:

- The gate is not side-effect-free: authorization **creates and commits** a `budget` row. A read-only
  "may I call live?" check that mutates budget state is a design smell worth an explicit Owner note.
- `DEFAULT_LIMITS` are per-dimension constants; nothing in this path evaluates *remaining* headroom.

---

### FE-03 — P1 · "Provider Reality Tracking" cannot distinguish declared from actually executed

**Report claim**: §4 — *"Requirement: distinguish declared vs actually executed"*, with
`actual_provider — gateway.last_actual_provider after live complete()`; §6.4 presents an `actual`
column reading `mimo` for both calls; §1.1 lists "Provider Reality Tracking" as a delivered mechanism.

**DV/VI:**

```python
# app/ai/gateway.py _live(), immediately before the call:
await invocation_counter.consume(task_id)
self._last_actual_provider = getattr(live, "name", type(live).__name__)   # assigned BEFORE the call
self._last_configured_model = getattr(live, "_model", None) or getattr(live, "model", None)
return await live.complete(prompt)

# app/ai/executor.py:208-226
actual_provider = getattr(self._gateway, "last_actual_provider", None)
_reality_tracker.record(..., actual_provider=actual_provider,
                        execution_status="completed" if outcome is not None else "failed", ...)
```

`actual_provider` is the **name attribute of the local provider object**, known before any network
I/O, and equal to the configured name by construction (`_build_mimo_provider` hardcodes
`name="mimo"`). It is not derived from the response, and it is set *before* `complete()` — so a
request that never reached the provider (built MIMO shell with `api_key=None`; connection failure;
401/403) still leaves `last_actual_provider = "mimo"`.

That the response *does* carry a reality signal is directly established: the previous round's smoke
evidence recorded a real MIMO call returning `"response_model": "mimo-v2.6-pro"` alongside `usage`.
`HTTPLLMProvider.complete()` (`providers/http.py:82-98`) reads only `choices[0].message.content` and
never touches `data["model"]` or `data["usage"]`.

Net: §6.4's `actual` column restates the configured value; the requirement it is presented as
satisfying is not met by this mechanism. A per-invocation read of the response's `model` field (and
the invocation's own provider identity rather than a gateway-level attribute) would meet it. Note
also that `_last_actual_provider` is gateway-level, so it is not per-invocation — under concurrency a
record can carry a previous call's value.

---

### FE-04 — P1/MEDIUM · The Level-1 runs were not driven by the documented worker entry, and "configured" comes from script literals

**Report claim**: §0 — *"Formal production path was entered only through its documented entries
(`DocumentImportService.import_file` == `POST /api/documents/import`, and `TaskExecutor.run_once` as
driven by `python -m app.worker run --allow-live`)"*; §6.1 shows the CLI text as a comment above the
two script commands.

**DV — what the delivered scripts actually do** (`formal_e2e_level1.py:88-104`,
`formal_e2e_level1b.py:60-69`):

```python
gateway = build_gateway(allow_live=True)
executor = TaskExecutor(async_session_maker, llm_gateway=gateway,
                        ocr_extractor=NativeTextProvider().extract,
                        default_provider="mimo", default_model="mimo-v2.6-pro")
while await executor.run_once(worker_id=worker_id): ...
```

No subprocess anywhere; `python -m app.worker` is never invoked. The scripts' own comment says
"Worker CLI equivalent", which is candid, but the report body asserts the CLI *drove* the run.

Consequences:

1. The run's `configured_provider` / `configured_model` (the left half of §6.4's reality pair) are
   **script constants**, not the runtime configuration — while the gateway's own model comes from
   `settings.mimo_model`. The CLI, by contrast, passes neither argument and uses the class defaults.
2. The CLI-only code added in this commit (`worker/__main__.py:102-111`, the reality flush to
   `provider_reality.json`) was not exercised: no `provider_reality.json` exists anywhere under the
   V3 tree.
3. The "formal entry" discipline the task set is thus satisfied for ingest and *approximated* for the
   worker: the same `TaskExecutor.run_once` code is driven, but by an in-process harness rather than
   the documented entry point. Given how central entry-point discipline has been in this chain, the
   report should state this plainly rather than describe the CLI as the driver.

---

### FE-05 — MEDIUM · Papers' provider change is not the proven version and its own test suite was left inconsistent

**Report claim**: §2.3 — Papers' provider switch, with `scripts/llm_provider.py` "added (ported from
Aitutors-preprocessing proven module)"; §11 lists two Papers files.

**DV:**

- `scripts/llm_provider.py` in Papers is **content-identical** to the private copy's proven module
  (git-normalized diff is empty) — the port claim holds for that file.
- `scripts/reslice_pipeline.py` is **not** identical: diffing Papers' committed version against the
  proven private-copy version yields **42 insertions / 15 deletions**, and the Papers version is
  missing both of the hardening changes introduced previously:
  `_redact()` → **absent**; the non-429-4xx immediate-failure branch → **absent**.
- Papers' `tests/` were not touched by `1662121`. Papers' `tests/test_no_config_import.py` therefore
  still asserts `except FileNotFoundError as e:` and `assert "mimo-x-pro-preview" in r.stdout` —
  both of which the new `load_cfg()` / `model_tag()` falsify (the raise is now `ProviderConfigError`;
  the tag is now `mimo-v2.6-pro`). **Papers' own regression suite is inconsistent with Papers' code.**

The report presents the Papers change as the formal provider switch without noting either the reduced
port or the un-updated tests. Compounding this, the two preprocessing trees have now diverged in both
directions — Papers: reduced pipeline, no provider tests, no anchor comments; private copy: full
pipeline, 18 provider tests, `pac_*` anchor comments — while the authority question raised as **D-1**
in the previous review remains open. (Verification by execution was not performed: running Papers'
suite requires writes outside this review's workspace; the mismatch is deterministic from both sides
of the code and the missing symbol was checked directly.)

---

### FE-06 — MEDIUM · Run A's evidence artifacts do not exist, but §8 indexes them and §10 claims reviewability

**Report claim**: §8 lists `e2e_run/formal-e2e-level1.json` and `e2e_run/provider-reality-level1.json`
(run A) among the evidence; §10 asserts "全链路 evidence 可复核 = **YES**".

**DV:**

```text
e2e_run/formal-e2e-level1.json            exists=False  tracked=False
e2e_run/provider-reality-level1.json      exists=False  tracked=False
e2e_run/formal-e2e-level1b.json           exists=True   tracked=True
e2e_run/formal-e2e-evidence-summary.json  exists=True   tracked=True
e2e_run/provider-reality-level1b.json     exists=True   tracked=True
```

Commit `0dc3d90` adds exactly six files: the report, the summary, `formal-e2e-level1b.json`,
`provider-reality-level1b.json`, and the two scripts. Run A's raw evidence and its provider-reality
file were never delivered. Run A's data survives only inside the aggregate summary (its document /
task / source-version / annotation IDs and its audit row are present there), so the loss is partial —
but the two artifacts §8 names do not exist, and §10's claim is not met for run A.

Circumstantial note: `formal_e2e_level1.py` has mtime `2026-09-26 10:59:53` Beijing — the same moment
run A's task was created (`02:59:53Z`) — so the script was being written at run time and its declared
output file was never produced or was removed. Worth resolving before this evidence bundle is relied
upon.

---

### FE-07 — MEDIUM · §2.5's dismissal of the DeepSeek audit rows is factually wrong; the policy claim is unevidenced; and the test suite writes into the evidence database

**Report claim**: §2.5 — *"Older `llm_call_audit` rows from unit-test fixtures mention
deepseek/primary/fallback with test model tags — those are test artifacts, not formal production
calls"*, supporting "Observed policy held".

**DV — audit composition and window:**

```text
deepseek | deepseek-chat | completed | 14
deepseek | deepseek-chat | failed    | 14
deepseek | deepseek-chat | started   |  2
deepseek | deepseek-chat | unknown   |  1
primary  | p-m           | failed    |  5
primary  | p-m           | started   |  1
fallback | f-m           | failed    |  2
fallback | f-m           | completed |  1
mimo     | mimo-v2.6-pro | completed |  2

min(start) 2026-09-26 02:56:46Z     max(start) 2026-09-26 03:06:50Z     count 42
```

There are **no older rows**: the table's entire content lies inside `02:56:46Z–03:06:50Z`
(10:56:46–11:06:50 Beijing), i.e. inside the declared execution window and inside the
DeepSeek-forbidden weekday window the report itself defines. 31 of the 42 rows carry
`deepseek/deepseek-chat`.

Whether they were real HTTP calls cannot be established from the audit row — and that is precisely
the problem: an audit table that cannot distinguish a fixture invocation from a production invocation
cannot support the claim "Observed policy held". Treating them as fixtures is a **DOCUMENT CLAIM** in
this review, not a verified fact.

**Corroborating the fixture hypothesis — and exposing a second defect:** all 18 `tasks` rows were
created between `02:57:56Z` and `03:06:49Z`, and 14 of them (created `02:57:56–02:58:03Z`, immediately
before run A) are in states `running` / `interrupted` / `failed` with `llm_invocations = 0`. That is
the signature of the V3 test suite, which therefore **writes into the same production database that
holds this round's E2E evidence**. The report neither discloses nor registers this; it matters both
for the policy claim above and for any future "the tests are clean" statement.

---

### FE-08 — MEDIUM · The resolver/IR blocking point has no persisted evidence

**Report claim**: §7 — "every top-level unit `semantic_status = "incomplete"`", with
representative counts (run A `32 resolved / 17 unresolved`; run B `46 resolved / 70 unresolved`;
`option.* incomplete (40 refs)`, `answer missing (19 refs)`, …), and "closest near-miss Q11–Q14".

**DV:**

```text
validation_events 0 | admission_events 0 | unit_groups 0
```

No table stores resolver role-resolution status or IR node validation; the delivered scripts do not
capture resolver statistics (they query documents, source versions, annotations, candidate/question
counts, audit and budget — nothing else); and no runner stdout/log file was committed. The numbers
quoted in §7 are therefore narrative. What *is* verifiable, and matches the report, is the input
side: 7 and 20 semantic units, 90 and 609 sealed lines, 922 and 855 spans, and
`admission_candidates = 0` / `questions = 0`.

Because FE-01 shows the counts are global readings on a cleared database, §7's *conclusion* (the
chain stops at IR; no Question objects are produced) is plausible and consistent, but neither its
magnitudes nor the "every unit" quantification can be checked by a third party from the delivered
artifacts. For a task whose deliverable is an evidence bundle, the first blocking point should be
captured as data, not prose.

---

### FE-09 — MEDIUM · The four new behaviours ship untested; and the reported V3 test totals cannot be reconciled

**Report claim**: §6.1 — `python -m pytest tests/ -q` → *"2012 passed, 1 skipped, 1 xfailed"*.

**DV:**

- The only test change in `d0a67da` is `tests/test_gateway.py` swapping the ollama expectations for
  mimo ones (`11 ++--`). **No test was added** for `authorize()`, for
  `_authorize_live_from_real_context()`, for `_build_deepseek_provider()`, or for
  `ProviderRealityTracker` — the four behaviours this task introduces.
- `python -m pytest tests/ -q --collect-only` on the committed tree (working tree == `d0a67da`)
  collects **2032 tests**. `pyproject.toml` sets only `asyncio_mode = "auto"` and
  `testpaths = ["tests"]` — no `addopts`, no marker deselection that could hide 18 tests — and the
  commit adds no test file. The reported total (2012 + 1 + 1 = **2014**) is **18 short** of the
  collected count and is not explainable from the repository.

I deliberately **did not** re-run the suite to settle it: FE-07 shows the suite's fixtures write into
the same database that holds this round's evidence (18 tasks, 31 DeepSeek rows), so a re-run would
mutate the evidence plane this review is examining. The reported totals are therefore unverifiable as
delivered — a situation that a hermetic test database would have avoided.

---

### FE-10 — LOW · GAP-E2E-05 mischaracterises a known adapter defect as an unknown

§6.4 / §9 state: *"Token usage / cost: not returned by provider body in this adapter path"*, and
GAP-E2E-05 asks "whether to parse usage from response body". MIMO **does** return `usage`: the
previous round's smoke evidence recorded, from a real call,
`{"prompt_tokens": 15, "completion_tokens": 8, "total_tokens": 23,
"completion_tokens_details": {"reasoning_tokens": 9}}`. `providers/http.py` contains no reference to
`usage` at all. The accurate statement is therefore "the V3 HTTP adapter discards the provider's
`usage` block" — a concrete, fixable defect, not an open question. (A separate genuine gap is
`estimated_cost`, which requires a pricing table.)

---

### FE-11 — LOW · The run's effective provider configuration is not reviewable from the repository

`TaskExecutor.__init__` was changed to default to `mimo` / `mimo-v2.6-pro`; the CLI passes neither, the
e2e scripts pass both explicitly; `_build_mimo_provider` reads `settings.mimo_model` with a constant
fallback. The source of truth for the model that actually ran is therefore partly a Python default and
partly `.env` — and `backend/.env` is **gitignored** (`.gitignore:14`). So the configuration behind
the recorded run cannot be inspected or reproduced from version control. This is the same concern that
round L raised as D-2/D-3 and is still open; it now affects concrete E2E evidence rather than a
baseline claim.

---

### FE-12 — LOW · Dead branch and a non-existent fallback advertised in `build_gateway`

```python
if not settings.mimo_api_key and not (settings.ollama_base_url and settings.ollama_model):
    # 无 MIMO key 且无 Ollama → 仍构建 MIMO shell …
    pass
```

This branch has no effect (the MIMO provider is constructed unconditionally, including with
`api_key=None`), and the docstring's "Ollama 仅在未配置 MIMO 时作为本地开发回退" describes a fallback
that is never constructed. Harmless functionally; misleading as documentation of the live wiring.

---

### FE-13 — LOW/INFO · With a single configured provider, any requested provider name resolves to MIMO

`build_gateway` passes `live_providers=live_providers if len(live_providers) > 1 else {}`. With
DeepSeek inert, `_live_providers` is empty, so `_resolve_live_provider(name)` returns the single
default for **any** name — the very "audit 记 fallback 名、实际调 primary 对象，identity 漂移"
scenario the adjoining comment warns about. The guard only activates with ≥2 providers. In the current
configuration a request naming `deepseek` or `ollama` would execute MIMO while the caller (and any
audit recorded from the requested name) believes otherwise. This interacts with FE-07: it is one more
reason the provider field in an audit row is not, by itself, proof of who served the request.

---

### FE-14 — INFO · The delivery message carries a sandbox access-denied line

The message as delivered ends with:

```text
Access denied - path outside allowed directories: D:\Project\AITutors-v3 not in D:\Project\AITutor-X
```

Provenance is **UNKNOWN** (it may be the tail of a failed tool call in the executor's session). It is
worth clarifying, because the report's V3-side evidence — Frozen Spec hashes, the V3 test totals, and
the DB readings — presumes the ability to read `D:\Project\AITutors-v3`. Independently, I verified that
V3's working tree is clean and equals `d0a67da`, so the claims themselves stand or fall on FE-09, not
on this line.

---

## 4. Owner decision list

| # | Decision | Inputs | Blocking? |
|---|---|---|---|
| **D-1** | **Was the database clear authorized, and is the prior corpus restorable?** Every global count in the report is a reading on a database whose content is 10 minutes old; the baseline round's evidence is no longer resolvable. | FE-01 | **Yes** — it determines how §6.3's counts may be read |
| **D-2** | **Accept `budget_ok=True` as a literal, or require a real availability check?** `ensure()` can never fail and `authorize()` defaults to `True`. | FE-02 | **Yes** — it is the difference between removing and relocating the bypass |
| **D-3** | **Must `actual_provider` come from the response (`model` echo) rather than the local object's name?** | FE-03 | **Yes** — the task's §6 requirement is otherwise unmet |
| **D-4** | **Is in-process `TaskExecutor.run_once` an acceptable Level-1 driver, or must the CLI be used?** If acceptable, §0 must be corrected; if not, the runs must be repeated. | FE-04 | No |
| **D-5** | **Which preprocessing tree is authoritative (open from round L), and must the Papers port include `_redact`, the 4xx fail-fast branch, and the provider tests?** Papers' own suite is currently inconsistent with Papers' code. | FE-05 | **Yes** for the port's completeness |
| **D-6** | **Re-issue run A's evidence artifacts, or amend §8 and §10?** | FE-06 | No |
| **D-7** | **Adopt a policy for the V3 test suite writing into the evidence database; and settle whether the 31 DeepSeek audit rows were fixture-only.** | FE-07 | No, but it gates future trust in `llm_call_audit` |
| **D-8** | **Require the first blocking point to be captured as persisted data (resolver/IR status), not prose.** | FE-08 | No |
| **D-9** | **Require tests for the four new behaviours, and reconcile 2014 vs 2032.** | FE-09 | No |
| **D-10** | **Decide where the run's provider configuration is reviewable, given `.env` is gitignored.** | FE-11 | No |

---

## 5. Findings summary

```text
FE-01  P0-cand  Evidence DB is not the baseline DB; reset undisclosed (audit table spans 10 minutes;
                all prior documents/questions/candidates/961 audit rows gone)                    [DV]
FE-02  P1       budget_ok is a literal True; ensure() is get-or-create that cannot fail;
                authorize() defaults budget_ok=True; authorization commits a budget write        [DV/VI]
FE-03  P1       ProviderRealityTracker.actual_provider = local object name, assigned BEFORE the
                call; not from the response echo; gateway-level (not per-invocation)             [DV/VI]
FE-04  P1/MED  Level-1 runs used in-process TaskExecutor.run_once with hardcoded provider/model
                literals; §0 claims they were driven by `python -m app.worker run --allow-live`   [DV]
FE-05  MEDIUM   Papers' reslice_pipeline.py is not the proven version (no _redact, no 4xx branch);
                Papers' tests untouched → its own suite now contradicts its code                   [DV]
FE-06  MEDIUM   Run A's formal-e2e-level1.json and provider-reality-level1.json do not exist;
                §8 indexes them, §10 claims reviewability                                        [DV]
FE-07  MEDIUM   "Older deepseek/primary/fallback test rows" is false — the whole audit table is
                10 minutes old and inside the forbidden window; the test suite writes into the
                evidence DB (18 tasks, 31 deepseek rows)                                        [DV]
FE-08  MEDIUM   Resolver/IR blocking point persisted nowhere (validation_events 0, admission_events 0);
                §7's counts and "every unit" quantification unverifiable from artifacts          [DV]
FE-09  MEDIUM   No tests for authorize()/_authorize_live_from_real_context/_build_deepseek_provider/
                tracker; 2032 collected vs 2014 reported, unexplainable, and not safely re-runnable [DV]
FE-10  LOW      GAP-E2E-05 frames a known adapter defect (usage discarded by http.py) as an unknown [DV]
FE-11  LOW      Effective provider config partly a Python default + gitignored .env → not reviewable [DV]
FE-12  LOW      Dead `if ... : pass` branch; docstring advertises an Ollama fallback never built    [VI]
FE-13  LOW/INFO Single-provider mode resolves ANY requested provider name to MIMO                    [VI]
FE-14  INFO      Delivery message ends with a sandbox "Access denied: D:\Project\AITutors-v3" line  [UNKNOWN]
```

---

## 6. Reviewer side-effects

1. No file under `AITutors-v3` or `Papers` was written. V3 remains at
   `d0a67da77448973a245e9ceda83651a7f2968e8d` with **0 modified tracked files**, `Docs/V3_SPEC` tree
   `14a7450809d4932036f415d765ab29c53671843c`, and the same 10 untracked paths; Papers remains at
   `1662121` with the same 2 untracked run-accounting files.
2. `pytest --collect-only` was run in `AITutors-v3/backend` with `-p no:cacheprovider` and
   `PYTHONDONTWRITEBYTECODE=1`; it executes no fixtures. The suite itself was **not** run — see FE-09.
3. Database inspection was read-only (`SELECT` only), through
   `docker exec aitutor-postgres psql -U aitutors -d aitutors`.
4. No API key material was printed or written; the two `KEY=` lines inspected were reported by length
   only.
