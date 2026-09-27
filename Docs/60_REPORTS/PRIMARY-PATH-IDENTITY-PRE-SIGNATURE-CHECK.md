# PRIMARY-PATH-IDENTITY PRE-SIGNATURE CHECK

```text
Document Type : Verification Record（evidence；不含新裁决）
supersedes    : —
superseded_by : —
readers       : Owner（签署方）；MIMO CODE；后续授权作者
Status        : CLOSED
Date          : 2026-09-27
Scope         : 治理文档一致性核查（未改 code / Spec 正文 / DB / migration；未签署任何 Owner authority）
Authority     : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 1. Checked Files

| # | 文件 | 结论 |
|---|---|---|
| 1 | `Docs/30_CONTRACTS/FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md` | PASS |
| 2 | `Docs/40_DECISIONS/OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` | PASS |
| 3 | `Docs/40_DECISIONS/IDENTITY-PROVENANCE-REVISION-02.md` | PASS |
| 4 | `Docs/40_DECISIONS/PRIMARY-PATH-IDENTITY-CLOSURE-SUMMARY-01.md` | PASS |
| 5 | `Docs/40_DECISIONS/IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md` | PASS |

**本核查为只读**；唯一变更是任务 D 项明确要求的**能力名称重命名**（见 §3 D）。

---

## 2. A — Status Consistency

| 项 | 要求 | 实际 | 结果 | 证据 |
|---|---|---|---|---|
| Governance | `CLOSED` | `Status: CLOSED` | ✅ PASS | `OWNER-DECISION…-01.md:8` |
| Blocking | `NONE` | `Blocking: NONE（Blocking-1 / 2 / 3 均已 RESOLVED）` | ✅ PASS | `OWNER-DECISION…-01.md:10`、`:370`；`CLOSURE-SUMMARY…-01.md:162`；`FROZEN-SPEC-ERRATA…-01.md:269` |
| Specification | `READY FOR FINAL APPROVAL` | Errata `Decision State: READY FOR FINAL APPROVAL` | ✅ PASS | `FROZEN-SPEC-ERRATA…-01.md:9`；`CLOSURE-SUMMARY…-01.md:9` |
| Implementation Authorization | `PENDING OWNER SIGNATURE` | `Signature: ⛔ PENDING OWNER SIGNATURE`（`Status: OPEN`） | ✅ PASS | `IMPLEMENTATION-AUTHORIZATION…-01.md:8-9`、`:29-35` |
| Migration | `NOT AUTHORIZED` | `Scope: Phase A only（No Migration）`；Phase B `未授权` | ✅ PASS | `IMPLEMENTATION-AUTHORIZATION…-01.md:11`、`:97-104`、`:140-150` |

**A 项总判定：PASS**

---

## 3. B — Decision Consistency

| Decision | 要求 | 实际 | 结果 | 证据 |
|---|---|---|---|---|
| **Decision 1** | role/provider separation | `role = preprocessing` / `provider = preprocessing`；明示「role/provider 描述 producer identity，不描述 artifact maturity，不复用 OCR identity」 | ✅ PASS | `OWNER-DECISION…-01.md:87-125` |
| **Decision 2** | `original_sha256 = SHA256(actual pipeline received artifact raw bytes)`；Scoped byte-domain only | §2.2 Amendment 正式文本 + §2.4 落地算法 `original_sha256 = SHA256(该 pipeline 实际接收到的 artifact 原始字节)`；§2.5 明示「域内」且「跨域不要求相同」 | ✅ PASS | `OWNER-DECISION…-01.md:139-227` |
| **Decision 3** | producer metadata independent storage model | 「不进入 `source_meta` / `document_source_versions` 作为长期扩展字段」「建立独立 metadata 表」 | ✅ PASS | `OWNER-DECISION…-01.md:250-306` |
| **Decision 4** | derived hash dependency consistency | ⚠️ **编号语义不符** —— 见下 | ⚠️ **PASS（内容存在，编号不符）** | `OWNER-DECISION…-01.md:311` vs `:229` |

### 3.1 Decision 2 — `same content = same identity` 残留检查

| 出现位置 | 性质 | 结果 |
|---|---|---|
| `OWNER-DECISION…-01.md:135` | 位于 §2.1「原文（rev.1，**其中的 universal 表述已被 Amendment 取代**）」块内，紧接 `:137` 警示行 | ✅ **限定引用，非未限定残留** |
| `OWNER-DECISION…-01.md:167` | 位于 §2.3「表述替换对照」表内，作为**被替换的左列**，右列为 `same artifact bytes = same artifact identity` | ✅ **限定引用，非未限定残留** |

```text
全 5 份文档内 "same content = same identity" 共 2 处，
两处均为【显式标注已被取代】的历史引用。
⇒ 无未限定残留。
```

### 3.2 Decision 4 编号不符（如实报告，未自行改名）

任务 check B 将 **Decision 4** 描述为 `derived hash dependency consistency`。
但 `OWNER-DECISION…-01.md` 中：

```text
Decision 4 = Owner Decision 原文入仓（:311）
derived hash dependency = §2.6 Derived Hash Impact（:229），隶属 Decision 2 之下
```

派生 hash 依赖一致性**内容确实存在且完整**（`§2.6`：`le_hash = f(original_sha256)` ⇒
必须同批重新验证 `le_hash` / source version identity / replay / uniqueness），
但它在文档中的**位置**是 Decision 2 的子节，**不是** Decision 4。

**处置**：本核查**不自行重新编号**（避免制造新的编号漂移）。
如需使编号与 check B 一致，须由 Owner 明示裁定。

**B 项总判定：PASS**（Decision 1–3 完全一致；Decision 4 内容存在，仅编号归属与 check B 措辞不符）

---

## 4. C — Phase Boundary Verification

### 4.1 Phase A（allowed without migration）

| 能力 | 是否在 Phase A | 证据 |
|---|---|---|
| `role-provider enforcement` | ✅ | `IMPLEMENTATION-AUTHORIZATION…-01.md:53` |
| `artifact-kind compatibility enforcement` | ✅ | `:54` |
| `original_sha256 identity-domain correction` | ✅ | `:52` |
| `identity invariant tests` | ✅ | `:71`、§4 `:157-175` |
| `source repository predicate alignment` | ✅ **（带边界条件）** | `:69`；条件见 `:151-153` |
| `api compatibility review` | ✅ | `:73` |
| （另含）`artifact-kind validation` / `seal role-provider enum extension` / `derived hash recalculation logic` / `model schema test alignment` | ✅ | `:55-72` |

Phase A 定义：`✅ code changes / ✅ validation / ✅ tests / ✅ non-persistent model changes`（`:127-138`）。

### 4.2 Phase B（NOT AUTHORIZED）

| 项 | 是否 NOT AUTHORIZED | 证据 |
|---|---|---|
| `producer_metadata schema introduction` | ⛔ | `:103`、`:111-116`、`:145` |
| `any DDL` | ⛔ | `:149-150`「任何需要 DDL 的动作（含建表、改约束、加列）一律属 Phase B」 |
| `any migration` | ⛔ | `:22`、`:100`、`:140` |
| `any existing data migration` | ⛔ | `:101`、`:120` |

特别声明存在且措辞准确（`:111-113`）：

```text
producer_metadata schema
    =
separate migration authorization required
```

### 4.3 C 项的两处观察（如实报告，未自行裁定）

**观察 C-1**：任务 check C 的 Phase A 列表**已包含** `source repository predicate alignment`，
但 `IMPLEMENTATION-AUTHORIZATION…-01.md:151-153` 载有条件：

```text
若该项涉及【唯一约束变更】（而非仅 re-read 谓词），则该部分属 Phase B。
实施方须在开工前判定并报备。
```

⇒ **若该能力的实现涉及唯一约束变更，它与 check C 的「Phase A」归类存在张力。**
该条件由本核查在上一轮加入（依据「约束与 re-read 谓词必须同改，否则 Postgres Binder error」）。
**须 Owner 确认**：接受该条件（实施方须报备并可能拆至 Phase B），或判定该项恒属 Phase A。

**观察 C-2**：任务 check C 的 Phase A 列表**未列** `seal role-provider enum extension`
与 `model schema test alignment`，但二者实际位于 Phase A（`:67`、`:72`）。
check C 措辞为 `Includes:`（非穷举），故**不构成失败**，仅记录差异供核对。

**C 项总判定：PASS（附 C-1 待确认）**

---

## 5. D — Naming Consistency

### 5.1 重命名执行（任务明确要求）

```text
original_sha256 identity-domain migration
        ↓
original_sha256 identity-domain correction
```

| 文件 | 行 | 状态 |
|---|---|---|
| `FROZEN-SPEC-ERRATA…-01.md` | `:187` | ✅ 已改 |
| `IMPLEMENTATION-AUTHORIZATION…-01.md` | `:52` | ✅ 已改 |
| `CLOSURE-SUMMARY…-01.md` | `:212`、`:225` | ✅ 已改 |

**复核**：全仓 `grep "identity-domain migration"` = **0 命中**；
`grep "identity-domain correction"` = **4 命中**（上列四处）。✅ PASS

### 5.2 其他 capability name 中的 "migration" 用词

| 名称 | 出现位置 | 是否合规 |
|---|---|---|
| `producer_metadata schema introduction` | Authorization `:66` | ✅ 不含 "migration" |
| `existing data migration` | Authorization `:101`、`:120` | ✅ 显式指 **data migration**，属允许例外 |
| `Migration`（Phase B 标题） | Authorization `:140` | ✅ 显式指 **migration**，属允许例外 |
| §2「Authorization Boundary」其余能力名 | — | ✅ 无 "migration" 字样 |

⇒ 无 capability name 滥用 "migration"。✅ PASS

**D 项总判定：PASS**

---

## 6. E — Authority Boundary Verification

| 检查 | 结果 | 证据 |
|---|---|---|
| 是否存在 `Agent signed` | ✅ **无** | 全仓 grep = 0 命中 |
| 是否存在 `Automatically approved` | ✅ **无** | 全仓 grep = 0 命中 |
| 是否存在 `Final approved by implementation agent` | ✅ **无** | 全仓 grep = 0 命中 |
| 签署区是否保持 `PENDING OWNER SIGNATURE` | ✅ **保持** | `IMPLEMENTATION-AUTHORIZATION…-01.md:9`（`Signature: ⛔ PENDING OWNER SIGNATURE`）、`:29-35` 签署区空白 |

**签署区原文（未改动，供核对）**：

```text
── OWNER SIGNATURE ─────────────────────────────────────────
Signed by : ______________________
Date      : ______________________
Verdict   : ☐ AUTHORIZED (Phase A only)   ☐ REJECTED   ☐ REVISE
────────────────────────────────────────────────────────────
```

**其他 authority 边界确认**：

| 项 | 结果 |
|---|---|
| Errata 是否被自行标为 FINAL APPROVED | ✅ 否（`Decision State: READY FOR FINAL APPROVAL`） |
| Authorization 是否被自行生效 | ✅ 否（`Status: OPEN`，`:18-27` 显式声明「未获 Owner 签署」「不构成授权」） |
| 是否有 agent 自写「Frozen / Final / Authority」 | ✅ 无（引用权威一律指向 `OWNER-DECISION…-01.md`） |

**E 项总判定：PASS**

---

## 7. PASS / FAIL Table

| 项 | 内容 | 结果 |
|---|---|---|
| **A** | Status consistency（5 项状态） | ✅ **PASS** |
| **B** | Decision consistency（Decision 1–4） | ✅ **PASS**（Decision 4 编号不符，见 §3.2） |
| **C** | Phase boundary（A / B 边界） | ✅ **PASS**（附 C-1 待确认） |
| **D** | Naming consistency（重命名 + migration 用词） | ✅ **PASS** |
| **E** | Authority boundary（签署区 / 自授权） | ✅ **PASS** |

---

## 8. Remaining Issues

**无阻塞项。** 下列 3 项为**待 Owner 确认**，均**不阻塞签署**：

| # | 项 | 性质 | 需 Owner |
|---|---|---|---|
| **I-1** | Decision 4 编号归属：check B 称 Decision 4 = derived hash dependency；文档中 Decision 4 = Owner Decision 原文入仓，而 derived hash 隶属 Decision 2 §2.6 | 编号措辞不符（内容完整） | 确认是否需重编号，或接受现状 |
| **I-2** | C-1：`source repository predicate alignment` 若涉及唯一约束变更则属 Phase B（Authorization `:151-153`） | 归类条件 | 确认接受该条件，或判定恒属 Phase A |
| **I-3** | C-2：check C 的 Phase A 列举未含 `seal role-provider enum extension` / `model schema test alignment`，二者实际在 Phase A | 列举差异（非穷举） | 知悉即可 |

---

## 9. Exact Signature Prerequisites

**Owner 签署前，仅需下列两项动作（无其他前置）**：

### 前置 1 — Errata FINAL APPROVED

```text
文件：Docs/30_CONTRACTS/FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md
现状：Status = OPEN ；Decision State = READY FOR FINAL APPROVAL
动作：Owner 确认批准后，将 Decision State 改为 FINAL APPROVED
依据：全部 Blocking-1/2/3 已 RESOLVED；无剩余前置
```

### 前置 2 — Implementation Authorization 签署（Phase A only）

```text
文件：Docs/40_DECISIONS/IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md
现状：Status = OPEN ；Signature = ⛔ PENDING OWNER SIGNATURE
动作：Owner 在 §"OWNER SIGNATURE" 区填写 Signed by / Date，
      并在 Verdict 勾选 ☐ AUTHORIZED (Phase A only)，
      同时将文件顶部 Status 由 OPEN 改为 CLOSED
```

### 签署后仍**不**授权的事项（须另行签发）

```text
⛔ producer_metadata schema introduction
⛔ 任何 DDL / schema migration
⛔ production DB mutation
⛔ existing data migration
```

---

## 10. Verdict

```text
A. Status consistency        : PASS
B. Decision consistency      : PASS
C. Phase boundary            : PASS
D. Naming consistency        : PASS
E. Authority boundary        : PASS

Remaining blockers           : NONE
Pending Owner confirmations  : 3（均不阻塞签署）

VERDICT: READY FOR OWNER SIGNATURE
```

**本核查未签署任何 Owner authority，未修改签署区，未授权实现。**

---

*Recorded 2026-09-27. 本文件为 Verification Record（evidence）。不含 `[OWNER DECISION]`；所有裁决引用 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md`。*
