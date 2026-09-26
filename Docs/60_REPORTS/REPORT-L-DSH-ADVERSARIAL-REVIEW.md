# REPORT-L · DSH Independent Adversarial Review

**Subject**: `Docs/60_REPORTS/REPORT-L-LLM-PROVIDER-CONFIG-CLOSURE-MIMO-V26-PRO.md`
(442 lines, `AITutor-X` commit `be08bb02f7ef2c6d3cb7a9c78c21a7ec3bdf80e4`, 1 file / +442)
**Reviewer role**: independent adversarial reviewer. Read-only on `AITutors-v3` and on the producer tree.
No code, configuration, Frozen Spec, governance document or producer data was modified.
**Date**: 2026-09-26
**Scope of this review**: the factual claims of REPORT-L, its evidence base, and the completeness of the
decision inputs it puts in front of the Owner. Business semantics are **not** adjudicated here.

> **Standing security line**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 0. Verdict

```text
REPORT-L CLAIMED SUBJECT : "Formal LLM Provider Configuration Closure"
VERDICT                  : ACCEPTED WITH FINDINGS
FINDINGS                 : RL-01 … RL-14   (1 P0-candidate, 3 P1, 4 MEDIUM, 6 LOW/INFO)

What is SUPPORTED        : the MIMO V2.6 PRO provider/model/credential combination is real and
                           runnable (own 200 + server model echo + pipeline rc=0 with faithful
                           manifest); the test result 338/18/1/0 reproduces EXACTLY; the Frozen
                           Spec sha256 reproduces byte-exactly and is genuinely the REGISTERED
                           value; the change set is content-complete for scripts/ + tests/;
                           secret discipline holds under an independent full-tree scan.
What is NOT CLOSED       : the changed codebase has NO version authority (RL-03), artifacts
                           produced with zero LLM calls are now stamped with the formal
                           production model ID (RL-02), and the H-01 regression test becomes
                           non-hermetic — i.e. it can fire a real paid LLM call — under the very
                           credential mechanism this report asks the Owner to adopt (RL-01).
```

"Configuration baseline established" is an accurate description of **what exists on disk in
`D:\Project\Aitutors-preprocessing` at review time**. It is not a description of a versioned,
reproducible, authoritative configuration, and the report does not claim otherwise.
The gap that matters is therefore not the wording but the **authority and provenance of the tree
that was changed** (RL-03).

---

## 1. Verification method and evidence tiers

| Tier | Meaning | Applied to |
|---|---|---|
| **DIRECTLY VERIFIED (DV)** | Reproduced by this reviewer in this session from the artifact itself | test suite result, Frozen Spec sha256, change-set diff, secret scan, key length, smoke manifest fidelity, V3 config/gateway/import lines, git refs |
| **VERIFIED BY INSPECTION (VI)** | Read the cited file/line; content matches the citation, execution not re-run | `step0_blind_test.py` MIMO wiring, producer↔consumer vocabulary, `preprocessing_consumer/` tier |
| **DOCUMENT CLAIM (DC)** | Inherited from a prior report; not re-tested here | `mimo-x-pro-preview` → `400 Unsupported model` |
| **UNKNOWN** | Cannot be established from available artifacts | provenance/attestation of the one-off smoke JSON in a non-versioned tree; whether the printed `+442` list is exhaustive of *all* filesystem writes |

Full-tree secret scan, byte-level comparisons, and the hermeticity probe are reproducible from
`review_l_evidence/` (see §5 evidence index).

---

## 2. What the report gets right (verified, credited)

These are not courtesies — each was independently reproduced, and several are sharper than the
corresponding claims in prior rounds.

1. **Test suite reproduced exactly.** `python -m pytest tests/ -q` in
   `D:\Project\Aitutors-preprocessing` → **`338 passed, 18 skipped, 1 xfailed`**, 357 collected.
   The report's `338 passed, 18 skipped, 1 xfailed, 0 failed` (§8.3) is accurate to the unit. (DV)
2. **Frozen Spec claim is true and correctly sourced.** `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md`
   at `AITutors-v3` is **tracked**, measures **92 197 bytes**, and hashes to
   `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528`. That value is genuinely a
   **registered** value, not a self-declared one: it appears in `Docs/COORDINATION/state.yaml`,
   `Docs/COORDINATION/CURRENT.md`, `Docs/COORDINATION/log.md`,
   `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-GAP-MAP.md`, and as a constant in
   `backend/scripts/preprocessing_consumer/boundary.py`. The cited base commit
   `f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1` exists in V3 history. (DV)
3. **Change set is content-complete.** A normalized (git-attribute-aware) file-by-file diff of
   `Papers/scripts|tests` vs the modified tree yields **exactly** the report's list:
   new `scripts/llm_provider.py`, new `tests/test_llm_provider_config.py`,
   modified `scripts/reslice_pipeline.py`, `scripts/pac_audit_recompute.py`,
   `scripts/pac_assemble_tracks.py`, `tests/test_no_config_import.py`. No unlisted content change
   exists in those two trees. (DV)
4. **`reslice_pipeline.py` before/after table (§2.2) matches the code line-for-line** — including
   the pre-change "HTTP 400 was also retried 4×" behaviour (§1.6), the new
   `CFG_PATH = llm_provider.legacy_config_path(ROOT)`, the immediate-failure branch for non-429 4xx,
   and `_redact()`. (DV)
5. **Secret discipline holds.** `MIMO_API_KEY` is **51 characters** as stated; an independent
   full-tree scan for that literal found it in **exactly one file — `AITutors-v3/backend/.env`**,
   its authoritative location — and in **0** files under the preprocessing tree, the AITutor-X tree,
   or the reviewed report corpus. `run_smoke.py:124` does contain the hard assertion the report
   cites. (DV)
6. **Smoke evidence is internally consistent and the manifest is faithful to the input.** The
   manifest's 2 units correspond exactly to `smoke_min.md` (`Q1` single_choice answer `A` at line 12;
   `U2` composite, `material_lines [15,16]`, `questions_lines [15,18]`, answer `要点甲；要点乙。`
   at line 20). §5.2's `finish_reason: length` explanation is correct — it is the probe's own
   `max_tokens=8` (`probe_content: ""`, `reasoning_tokens: 9`), not the pipeline call. (DV)
7. **V3-side facts check out precisely**: `_ALLOWED_EXTENSIONS = {".pdf", ".docx"}` is at
   `import_service.py:26` exactly; `.env` has `LLM_GATEWAY_MODE=live`, **no** `OLLAMA_*`, **no**
   `DEEPSEEK_*`, and `MIMO_MODEL=mimo-x-pro-preview` at line 9; `config.py:43-46` `deepseek_*` is
   untouched; `build_gateway()` is at `gateway.py:101` and constructs
   `HTTPLLMProvider(name="ollama", api_key=None, base_url=settings.ollama_base_url, model=settings.ollama_model)`
   with both empty; `AITutor-X/{backend,preprocessing,tools}` each contain exactly `.gitkeep`. (DV)
8. **§6.1's "MIMO_* is consumed only by the Step 0.5 blind-test script, never by the gateway" is
   true.** `git grep "mimo_" -- "*.py"` in V3 returns only the `config.py:47-50` declarations and
   `tests/test_config.py:35`; the only consumer sets `API_KEY/BASE_URL/MODEL` from a parsed `.env`
   in `backend/scripts/step0_blind_test.py:26-29`. (DV/VI)
9. **§1.6/§1.7 tree facts are correct**: `Papers/data/.llm_config` exists (147 B, mtime 2026-09-09);
   `Aitutors-preprocessing/data/.llm_config` is absent; `.gitignore` carries both `/data/.llm_config`
   and `*llm_config*`; the copy has only `.gitattributes` + `.github/`, no `.git`. (DV)
10. **The report's citation discipline is unusually good.** Both cited line ranges I spot-checked are
    exact: `E2E-VERIFICATION-EXECUTION-REPORT.md:684` really does state the `/v1/models` result, and
    `e2e_run/e2e_live_full_chain.py:43-45` really does carry the model-ID comment plus the
    `setdefault`. Prior rounds in this chain have had to correct citation drift; this round needs none.

---

## 3. Findings

### RL-01 — P0-candidate · The H-01 regression test becomes non-hermetic under the credential mechanism this same report recommends; it can fire a real paid LLM call from the unit-test suite

**Claim under review**: §8.3 "确定性路径（渲染/校验/QC/fix 链）零破坏" +
§10.1 **B-2** recommending "`MIMO_API_KEY` 环境变量注入" as the long-term credential mechanism.

**Fact**: `tests/test_no_config_import.py:21-31` builds the child environment as
`dict(os.environ, RESLICE_ROOT=..., PYTHONPATH=...)` — it **never scrubs** `MIMO_API_KEY`,
`MIMO_BASE_URL`, `MIMO_MODEL` or `LLM_PROVIDER`. The test at `:41-53` is titled
*fails loudly **without config*** and asserts `"EXPECTED True" in r.stdout`, where
`EXPECTED` is `'.llm_config' in str(e)` — i.e. it asserts that configuration resolution **fails**.

Those two facts are mutually exclusive once the Owner adopts B-2. On any host that exports a
credential as the report recommends, the "without config" precondition is silently false:
configuration resolves, and `call_llm()` proceeds to the transport layer — with the **live default
base URL** `https://api.xiaomimimo.com/v1` unless one is also exported.

**Reproduction** (`review_l_evidence/hermeticity_probe.py`, run this session; base URL overridden to
`http://127.0.0.1:9/v1` so that **no external provider was contacted**):

```text
case A · ambient MIMO_* scrubbed (today's CI-like environment)
    EXC_TYPE ProviderConfigError
    EXPECTED True            → test PASSES

case B · ambient MIMO_API_KEY present (the convention B-2 asks for)
    EXC_TYPE RuntimeError                 ← config resolution SUCCEEDED; transport was reached
    EXPECTED False                        ← assert "EXPECTED True" in stdout would FAIL
    MSG_HEAD LLM 调用失败: HTTP 503 <!DOCTYPE html>   (local endpoint, not MIMO)
```

**Impact**: (a) a unit-test suite that makes real, billable outbound requests, (b) the deterministic
path is only deterministic *while the recommended credential is absent* — the exact opposite of what
the credential policy intends, (c) the suite fails rather than degrades, so the first symptom of
adopting B-2 is a red test suite that the operator may "fix" by weakening the H-01 assertion —
the very assertion this chain has protected since round 1.

**Fix shape** (not applied): scrub the four variables in `_run()` (or `monkeypatch.delenv`) so the
"no config" test constructs its precondition instead of inheriting it. This is the same discipline
the H-01 change itself established.

---

### RL-02 — P1 · Artifacts produced with zero LLM calls are now stamped with the formal production model ID; `manifest.model` stops being evidence of execution

**Fact**: `llm_provider.default_model_tag()` (`llm_provider.py:165-175`) catches
`ProviderConfigError` and returns `PROVIDERS[provider]["default_model"]`, which for `mimo` is
`mimo-v2.6-pro`. Consequently `UNCONFIGURED_TAG = "unconfigured-llm-provider"` (line 35) is
**unreachable for the mimo provider** — it can only be returned when `default_model == ""`, i.e. for
`deepseek`. The behaviour is not incidental; it is **pinned by the updated test**:

```text
tests/test_no_config_import.py:79   assert "mimo-v2.6-pro" in r.stdout   # 无配置也成立
                         :80-81   assert "mimo-x-pro-preview" not in r.stdout
```

That test runs `validate_manifest` + `write_outputs` with `RESLICE_ROOT` pointed at an empty temp
directory — **no credential, no network** — and the emitted manifest carries `model: mimo-v2.6-pro`.

**Consequences**:

1. A producer manifest produced by a run that made **zero** LLM calls is now textually
   indistinguishable from one produced by a real MIMO V2.6 PRO run. Before this change the same hole
   existed but was labelled with the *legacy* test model; the change moves the mislabel onto the
   **formal production model name**, which is strictly more misleading for every downstream consumer
   that trusts `model` (V3's `manifest_reader.py` preserves `model` verbatim; the `pac_*` I7
   invariant audits read `man.get("model")`; prior-round evidence bundles quoted manifest `model`).
2. It is the same defect class as **E2E-BL-01** from the immediately preceding baseline round —
   "the assertion/metadata field is populated by construction, not by evidence" — reappearing on the
   producer side.
3. The report's own §5.2 table lists *"manifest 是否正常 → YES — `model=mimo-v2.6-pro`"* as a
   validation row. That row is a **metadata tag with a fallback**, not verification. The row that
   actually carries weight is `model（服务端回显）= mimo-v2.6-pro`, and the report does present it —
   but the two are listed side by side as if they were equivalent evidence.

The report's §2.2 change table describes `model_tag()` as neutral bookkeeping ("产物元数据里的模型名")
and does not disclose the provenance consequence.
A `model_source: env|legacy|default` field (or refusing the formal tag when unresolved) would close it.

---

### RL-03 — P1 · B-1 omits the load-bearing fact: a git repository for this exact codebase already exists

**The report asks the Owner** (§10.1 B-1): *"是重新 `git init` + 首次提交，还是该目录本就应是某仓的工作树/子模块？"*

**Missing fact** (DV): `D:\Project\Papers` **is** a git repository for this same codebase:

```text
HEAD     2b92898f05f6541a5fc65c8300cb8a59a06c4928   ("DEC-049: D2/D3/D4 Decision Brief")
remote   https://github.com/kurt-wong/Aitutors-preprocessing.git   (fetch & push)
status   clean except 2 untracked run-accounting files
```

and its `scripts/` + `tests/` are content-identical to the modified tree except for the six changes
this report lists (plus CRLF↔LF normalization, RL-14). REPORT-L's §1.1 "三仓 git 边界" table lists
only the non-git copy; §1.7 mentions `Papers` solely as "三仓之外" holding a `.llm_config`. The
Owner is therefore being asked to choose between "re-init" and "maybe it is a worktree/submodule"
**without being told that the repository — with a remote, and with history — is already there and
untouched**.

**Why this matters beyond bookkeeping**:

- Option 1 (`git init` in the copy) would create a **second, divergent history** for code whose
  canonical history already exists, and would make the provider change a change to a repository
  nobody's remote points at. `AGENTS.md` principle 4 — *Git presence ≠ Authority, Local ≠ Tracked ≠
  Authority* — does not resolve in favour of the copy; it requires the Owner to see both candidates,
  which the report does not present.
- The same fact undercuts the report's own evidence attestation: the tests, the smoke JSON and the
  provider module live only in a tree with no VCS. I could reproduce the *result* (338/18/1/0) but not
  attest that the reviewed bytes are the bytes that produced it. The report is candid that there is
  "无版本历史保护"; what it does not draw is the consequence for its own evidence.
- Conversely, and to be fair: my normalized diff **confirms the report's §9.3 change list is accurate
  and complete**, which is a real verification result that only exists because `Papers` was
  unmodified. That verification should be recorded as an input to the Owner's decision.

---

### RL-04 — MEDIUM · §2.3 claims anchor comments were added at three sites; the third site has no such comment

§2.3 is headed **"历史锚点（保留未改，已加注「非活跃生产配置」）"** and closes with
*"三处均已加注释标明「历史工件锚点，非活跃生产配置」"*, the three being
`pac_audit_recompute.py`, `pac_assemble_tracks.py`, and `tests/samples/artifact/**、data/**`.

**DV**: a content search for `历史工件锚点|非活跃生产配置` across the tree's `.py/.md/.json/.txt/.ini`
returns **exactly two files**:

```text
scripts/pac_assemble_tracks.py
scripts/pac_audit_recompute.py
```

Neither `tests/samples/artifact/**` nor `data/**` was edited at all (the three
`geo_…(教师版)` artifact files are content-identical to `Papers` once line endings are normalized).
So §2.3 simultaneously asserts *"保留未改"* and *"已加注释"* for the same entry, and the second half
is false. This is the "unsourced / mislabeled current-state assertion" defect class this chain
exists to police; it is small here, but it sits inside the section the Owner is most likely to trust
when judging whether the historical corpus was touched.

---

### RL-05 — MEDIUM · The stated resolution chain does not cover `provider`; §1.6's declared 实现缺口 is only partially closed

**Claim**: §2.1 — *"解析优先级：**环境变量 → legacy `data/.llm_config` → provider 默认值**"*,
presented as the fix for §1.6's finding that *"`provider` 字段在 prd.md 文档契约中存在，但
`load_cfg()` 从未读取（实现缺口）"*.

**Fact** (`llm_provider.py:88-94, 116-118`): the provider name comes from
`resolve_provider_name(env)` = `LLM_PROVIDER` environment variable **or** the hard-coded
`DEFAULT_PROVIDER = "mimo"`. The legacy file is read *after* the provider is already fixed
(line 118) and its `provider=` line is **never consulted**. The three-step priority holds for
`model`, `base_url` and `api_key` only.

The gap is masked by coincidence in the test suite: `test_legacy_config_file_is_read_for_model_and_key`
writes `provider=mimo` into the legacy file and passes only because `DEFAULT_PROVIDER` is also
`mimo`. A legacy file naming any other provider would be silently overridden rather than honoured or
rejected. Either the report's chain diagram should be narrowed, or `provider=` should be resolved
(and fail-closed on conflict).

---

### RL-06 — MEDIUM · The anti-leak function on the HTTP error path is untested, and the test cited for key-leak protection is vacuous

**Claim**: §5.3 lists as a verified ring of the "完整可运行组合":
*"error handling | 4xx(除 429) 立即失败带非敏感响应体；429/5xx 指数退避；`_redact()` 防 key 泄漏"*.
§8.1 lists `test_api_key_never_leaks_into_error_message` as the key-exposure case.

**DV**:

- `reslice_pipeline._redact` is defined at `:69` and called at `:112` and `:125`. A search of the
  entire `tests/` tree finds **no reference to `_redact`** — the function that this round added to
  keep the key out of exception text is executed by no test.
- `test_llm_provider_config.py:207-216` triggers the failure by setting
  `MIMO_MODEL=LEGACY_TEST_MODEL`, which raises `ProviderConfigError` from
  `llm_provider.py:132-137`. That message is built from the provider name and the model ID and
  **never interpolates the API key**. The assertion `FAKE_KEY not in str(ei.value)` therefore passes
  even if no redaction mechanism exists at all. It is an assertion that cannot fail for the reason
  its name claims.

Net: key-leak prevention on the live HTTP path rests on code reading, not on evidence — while the
report presents it as verified. (The `llm_provider` side is genuinely well-protected at
`resolve()`: the key is never placed into any raised message there. The gap is specifically the
transport path.)

---

### RL-07 — MEDIUM · §7 concludes "FORMAL CONTRACT: DOES NOT EXIST" without disclosing that a producer-manifest consumer tier already exists in V3

**Claim**: §7 — evidence is the single line `import_service.py:26` plus the producer's `.md` +
manifest output; conclusion *"FORMAL CONTRACT: DOES NOT EXIST"*; candidates A/B/C for the Owner, with
**C** = *"建立明确的中间 artifact / import contract（专用 adapter + 契约测试）"*.

**Fact (VI)**: V3 already contains a **tracked, committed** manifest-consuming tier:

```text
backend/scripts/preprocessing_consumer/
    manifest_reader.py        ← "Producer 词表: standalone_question | composite_question";
                                 preserves identity_version / source_content_sha256 / sections /
                                 section_ref / printed_provenance / basis / basis_evidence verbatim
    boundary.py               ← carries the frozen contract sha256 as a constant
    annotation_adapter.py     ← payload adaptation
    resolved_span_adapter.py  ← span construction
    runner.py / runner_b2.py / runner_b3.py
    consumer-report.json / -b2 / -b3, correctness-sampling-report.json, p32-* …
```

with registered gaps in V3's own coordination documents (e.g.
`PREPROCESSING-V3-CONSUMER-DECISION-ALIGNMENT-v2.md:156` — N-5 violated because
`annotation_adapter.py:42` hardcodes a `unit_type` rewrite; `PREPROCESSING-V3-CONSUMER-GAP-MAP.md:51-52`).

The report's *conclusion* may well survive — a script-tier adapter is not the formal import channel,
and `.md` cannot enter `POST /api/documents/import`. But the **decision input is incomplete**: the
Owner is offered "build a dedicated adapter + contract tests" as a fresh option (C) without being
told that a dedicated adapter tier already exists, already runs, and already has a documented
boundary-violation register. That materially changes the cost/benefit of A vs B vs C.

Related omission: §7 does not mention the vocabulary divergence that the report's **own smoke
artifact** displays — the producer manifest emits `unit_type ∈ {standalone_question, composite_question}`
(`smoke_min.manifest.json`, and `manifest_reader.py` documents it as the Producer vocabulary), while
the formal pipeline's annotation prompt requires
`unit_type ∈ {standalone_unit, composite_unit}` and `role ∈ {stem, option, answer, explanation}`
(`app/domains/task/executor.py` prompt prefix). That is a semantic-layer, not file-format,
incompatibility and it belongs in the same §7 decision input.

---

### RL-08 — MEDIUM · The report does not disclose that its own commit is unpushed; the appendix implies a single blocker

**DV**:

```text
AITutor-X HEAD        be08bb02f7ef2c6d3cb7a9c78c21a7ec3bdf80e4
origin/main           949bfc895bec74987a942d6f98ed2c3124a76512
rev-list --left-right --count origin/main...HEAD   →   0    1
```

The local branch is **one commit ahead** of origin. REPORT-L never states this: a full-text search of
the report for `push|origin|CONNECT|404` returns only `:392` (about preprocessing: "未 force push"),
`:402` (B-1) and `:441` (`[!] Commit/push completed only for authorized changes → BLOCKED:
preprocessing 无 .git`). The appendix's single blocker implies AITutor-X's commit/push completed.

The accompanying chat summary states *"push 失败：CONNECT tunnel failed, response 404（环境代理阻断，
非权限问题）—— main 现落后 origin 1 commit"*. The obstruction is real and reproducible — the repo
carries `http.proxy=http://127.0.0.1:55219` / `https.proxy=…`, and the default `git push` fails with
exactly that tunnel error — but the **direction is inverted** (the local branch leads origin; origin
does not lead it), and the obstruction is **bypassable**: `git -c http.proxy= -c https.proxy= push`
was the working recipe for `7715703` and `949bfc8` in the two immediately preceding rounds. Labelling
it an environment impossibility rather than an unattempted workaround is a current-state labelling
defect, and it leaves the report of record unpushed.

*Disclosure*: this review's own push will fast-forward `origin/main` to include `be08bb0` unless the
Owner instructs otherwise. I did not author, amend or alter that commit.

---

### RL-09 — LOW · V3's code-level legacy fallback is missing from §6.1's migration checklist

**Claim**: §6.1 item 3 — *"`MIMO_MODEL` 需由 `mimo-x-pro-preview` 更新为 `mimo-v2.6-pro`（当前值已被
live API 拒绝）"*, referring to `.env`.

**Fact (DV)**: `backend/scripts/step0_blind_test.py:29` —
`MODEL = _env.get("MIMO_MODEL", "mimo-x-pro-preview")` — is a **hard-coded in-code legacy default**.
Whenever `.env` lacks `MIMO_MODEL`, that script reproduces the API-rejected model with no `.env`
involvement. Not modifying V3 is correct under the task's §10; the defect is that the one site where
the legacy ID lives as **code rather than configuration** is absent from the migration checklist —
which is precisely the list the next (authorized) task will execute. (Path also appears as
`scripts/step0_blind_test.py` in §1.4/§6.1; the tracked path is `backend/scripts/step0_blind_test.py`.)

---

### RL-10 — LOW · §1.3 labels a prior report as the "权威目标" source

§1.3's table gives the authoritative-target row's provenance as
`AITutor-X/Docs/60_REPORTS/E2E-VERIFICATION-EXECUTION-REPORT.md:684` plus a comment in
`e2e_run/e2e_live_full_chain.py:43-45` — both citations are accurate (verified). But both are
**reports/scripts**, i.e. DOCUMENT CLAIM tier; the former was itself the subject of an adversarial
review (`EE-01…EE-11`). The **DIRECTLY VERIFIED** evidence for the model ID is this round's own real
call (HTTP 200 with server-side `model` echo `mimo-v2.6-pro`, plus pipeline rc=0) — that is what
should be labelled authoritative, with the report citations demoted to corroboration. Likewise the
`400 Unsupported model` rejection of the legacy ID is inherited from that prior report and was not
re-tested this round; declining to re-test is defensible (it would be a gratuitous call), but the
tier label should say so.

---

### RL-11 — LOW · Stale documentation introduced by this change

`tests/test_no_config_import.py:8` still states the contract as
*"call_llm 在缺配置时显式抛 FileNotFoundError"*. The same change replaced that exception with
`ProviderConfigError` and updated the test body at `:47` — the module docstring was not updated. The
report's §8.2 accurately describes the two assertion changes; it does not notice that the file's
self-description is now false.

---

### RL-12 — INFO · `assert_no_legacy_model` has no production caller

Defined at `llm_provider.py:178-182`; referenced only by `test_llm_provider_config.py:167-171`. It is
presented in §2.1/§8.1 as part of the legacy guard, and it does enforce something — inside its own
test. Nothing in `reslice_pipeline.py` or elsewhere calls it, so no runtime path is protected by it.

---

### RL-13 — INFO · `api_key_env` may contain a non-identifier string

When the key comes from the legacy file, `llm_provider.py:144` sets
`api_key_env = "MIMO_API_KEY 或 data/.llm_config 的 api_key="`. The field is named and typed as an
environment-variable name but carries a sentence. No consumer today (the smoke evidence reports the
constant `"MIMO_API_KEY"` from its own literal), so this is latent only.

---

### RL-14 — INFO · The two trees differ in line endings, which invalidates naive byte-level auditing

`D:\Project\Papers`' working tree is **CRLF**; the modified copy is **LF** (despite `.gitattributes`
declaring `*.py text eol=lf`). A raw SHA256 comparison flags 11 files as "modified"; only 6 are. Git's
attribute-aware diff shows the difference immediately. Two consequences for the Owner: (a) any
byte-level hash comparison between the two trees is meaningless without normalization — the report's
§9.3 list can only be confirmed after normalization (I did so, RL/correctness item 3); (b) if the
Owner ever reconciles the trees, it must be done through git, never by copying files.

---

## 4. Owner decision list

No decision below is made by this review.

| # | Decision | Inputs the Owner needs | Blocking? |
|---|---|---|---|
| **D-1** | **Which tree is authoritative for the producer codebase** — `D:\Project\Papers` (git, remote `Aitutors-preprocessing.git`, clean) or the non-git `D:\Project\Aitutors-preprocessing` copy? | RL-03. Option "`git init` the copy" creates a second divergent history for code that already has one. The copy and `Papers` also disagree on line endings (RL-14). | **Yes** — §16 commit/push is unexecutable until this is answered |
| **D-2** | **May an artifact be stamped `model: mimo-v2.6-pro` when no LLM call occurred?** | RL-02. Today: yes, by design and by test. Alternatives: emit `model_source`, or stamp `unconfigured-llm-provider` (the constant already exists), or fail. | Yes — it determines whether manifest `model` can be used as evidence downstream |
| **D-3** | **Credential mechanism** — adopt `MIMO_API_KEY` env-var injection (B-2)? If yes, the H-01 test must be made hermetic in the same change. | RL-01. The two decisions are coupled: adopting B-2 today breaks `test_call_llm_fails_loudly_without_config` and can trigger live paid calls from pytest. | Yes |
| **D-4** | **Is the legacy `.llm_config` `provider=` field honoured, or retired from the contract?** | RL-05. Currently declared as part of the chain in §2.1 but not implemented. | No |
| **D-5** | **For §7 A/B/C: does the existing `backend/scripts/preprocessing_consumer/` tier count as the "专用 adapter", and are its registered gaps (N-5 etc.) in scope?** | RL-07. Also: producer vocabulary `*_question` vs formal pipeline `*_unit`. | No |
| **D-6** | **Authorize the proxy-bypass push, or accept a local-only commit?** | RL-08. `git -c http.proxy= -c https.proxy= push` is the known working recipe; the report currently leaves `be08bb0` unpushed and mislabels the situation. | No |
| **D-7** | **Add `backend/scripts/step0_blind_test.py:29` to the V3 migration checklist** (fix still deferred) | RL-09 | No |
| **D-8** | **(pre-existing B-3) Authorize reading `D:\Project\Papers\data\.llm_config`?** | It exists — 147 bytes, mtime 2026-09-09 — verified by metadata only; **content not read** by this review either. | No |

---

## 5. Evidence index (this review)

| Artifact | Content |
|---|---|
| `review_l_evidence/rl-hermeticity-probe.json` | RL-01 two-case probe output (case A `ProviderConfigError`/EXPECTED True; case B transport-reached/EXPECTED False) |
| `review_l_evidence/hermeticity_probe.py` | The probe itself; base URL pinned to `127.0.0.1:9` so no external provider is contacted |
| `review_l_evidence/rl-verification-log.txt` | Command/result log: git refs, Frozen Spec hash, pytest result, normalized change-set diff, secret scan, V3 line checks |

Reproduction commands are recorded in the log; the pytest run is
`python -m pytest tests/ -q` from `D:\Project\Aitutors-preprocessing`
(`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`).

**Reviewer side-effects, disclosed**:

1. The pytest reproduction required the suite's own scratch directory, which lies outside my session
   workspace (`D:\Project\Aitutors-preprocessing\.pytest_work`). The fixture's best-effort cleanup
   left `.pytest_work\r67_t`. I did not delete it (the workspace rules forbid removing prior
   artifacts); it is scratch, not data.
2. No file under `AITutors-v3` or `Papers` was written. `AITutors-v3` remains at
   `d2b9a26f1a1c0297b4536b273b8999a071433079` with `Docs/V3_SPEC` tree
   `14a7450809d4932036f415d765ab29c53671843c` and the same 10 untracked paths; `Papers` remains at
   `2b92898f05f6541a5fc65c8300cb8a59a06c4928` with the same 2 untracked run-accounting files.
3. The API key value was never printed, logged or written by this review; the leak scan compared
   literals in-process and emitted counts only.

---

## 6. Findings summary

```text
RL-01  P0-cand  H-01 test non-hermetic under the report's own recommended credential mechanism
                (can fire a real paid LLM call; fails when it does)                    [reproduced]
RL-02  P1       offline artifacts stamped with the formal production model ID;
                UNCONFIGURED_TAG unreachable for mimo; manifest.model ≠ execution evidence
RL-03  P1       B-1 omits that D:\Project\Papers IS the git repo for this codebase
                (remote Aitutors-preprocessing.git, HEAD 2b92898, clean)
RL-04  MEDIUM   §2.3 "三处均已加注释" — the third site (tests/samples/artifact, data) has none
RL-05  MEDIUM   provider name not resolved through the legacy chain; §1.6 gap only partially closed
RL-06  MEDIUM   reslice_pipeline._redact untested; the cited leak test is vacuous
RL-07  MEDIUM   §7 omits V3's existing preprocessing_consumer tier and the *_question / *_unit divergence
RL-08  MEDIUM   own commit unpushed and undisclosed; "main 落后 origin" inverts the direction
RL-09  LOW      backend/scripts/step0_blind_test.py:29 legacy default missing from §6.1 checklist
RL-10  LOW      a prior report is labelled the "权威目标" source; DV evidence is this round's own probe
RL-11  LOW      stale module docstring (FileNotFoundError) in the edited test file
RL-12  INFO     assert_no_legacy_model has no production caller
RL-13  INFO     api_key_env can carry a non-identifier string
RL-14  INFO     CRLF/LF divergence makes byte-level comparison between the two trees invalid
```
