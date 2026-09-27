# IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01

```text
Document Type : Implementation Authorization（**草案 — 未签发**）
supersedes    : —
superseded_by : —
readers       : MIMO CODE（执行方）；Owner（签发方）；后续 migration 授权作者
Status: CLOSED

Signature:
  Signed by: <kurt>
  Date: 2026-09-27

Authorization:
  ☑ AUTHORIZED (Phase A only)Date          : 2026-09-27
Scope         : Phase A only（No Migration）
Authority     : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md
                FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

> ## ⛔ 本文件为**草案**，尚未生效
>
> ```text
> ✗ 未获 Owner 签署
> ✗ 不授权任何实现
> ✗ 不授权任何 migration
> ✓ 签发后方可依据本文件执行 Phase A
> ```
>
> **签发方式**：由 Owner 将本文件 `Status` 改为 `CLOSED`、`Signature` 改为署名人/日期，
> 或在下方签署区内记录。**未签署前，本文件不构成授权。**

```text
── OWNER SIGNATURE ─────────────────────────────────────────
Signed by : ______________________
Date      : ______________________
Verdict   : ☐ AUTHORIZED (Phase A only)   ☐ REJECTED   ☐ REVISE
────────────────────────────────────────────────────────────
```

---

## 1. Authorization Boundary

`[OWNER DECISION]` 授权范围：

```text
Primary Path Identity Implementation
```

仅包含下列能力（**能力名称即边界标识；编号不构成授权边界**）：

| 能力 | 内容 | 位置 |
|---|---|---|
| `identity byte-domain correction` | 消除「正确身份已算出却被丢弃」：复用已核对的 raw-bytes identity | `runner_b2.py:118-121` |
| `original_sha256 identity-domain correction` | `original_sha256` 改为 **接收字节** 的 SHA256（2-B Scoped Byte-Domain） | `runner.py:74,78`；`runner_b2.py:322,326` |
| `role-provider enforcement` | Primary Path 写入 `role=preprocessing` / `provider=preprocessing` | `runner.py:90-91`；`runner_b2.py:338-339` |
| `artifact-kind compatibility enforcement` | `artifact_kind` 由 `"markdown"` 改为 `canonical_l1` | `runner.py:89`；`runner_b2.py:337` |
| `artifact-kind validation` | 新增闭集校验器并接入两条写入路径（当前**无**校验器） | 现仅 `seal.py:39-44` 校验 role/provider |
| `seal role-provider enum extension` | `_SEAL_ROLE_PROVIDERS` 纳入 `preprocessing ⟺ preprocessing` | `seal.py:39-44` |
| `derived hash recalculation logic` | 因 `le_hash = f(original_sha256)`，`le_hash` / version identity / replay / uniqueness 假设须**同批**重新验证 | `runner.py:86`；`seal.py:98-106` |
| `source repository predicate alignment` | `_version_by_le` 与 `ON CONFLICT` 目标索引**同步**修改 | `source_repository.py:110-113` 与 `:128-138` |
| `identity invariant tests` | 新增 identity invariant 测试（现有测试不覆盖） | 见 §4 |
| `model schema test alignment` | 更新 `tests/test_models_schema.py`（含 `assert len(seen) == 11`）——**不得以改断言绕过** | `tests/test_models_schema.py:39,103-107,124,126` |
| `api compatibility review` | `role` 是**排序键**且经 API 暴露，须核对行为变化 | `api/schemas.py:22-32`；`api/routers/documents.py:224-232`、`:129-133` |

### 1.1 授权的强制同批条件

`[OWNER DECISION]`（引自 Errata §4.4 Derived Hash Impact）：

```text
original_sha256 change
        ↓
le_hash change
        ↓
SourceVersion identity assumptions require revalidation
```

⇒ 实施方**不得**只改 `original_sha256` 赋值而不同批处理上列四项
（`le_hash` / source version identity / replay behavior / uniqueness assumptions）。

### 1.2 语义来源（禁止重新解释）

实现方**必须**直接采用下列已冻结语义，**不得**重新解释或提出替代方案：

```text
identity      : original_sha256 = SHA256(该 pipeline 实际接收到的 artifact 原始字节)
                同一字节域内同字节 = 同一 artifact identity
                跨域（PDF / Markdown / canonical L1）【不要求】相同 original_sha256
provenance    : role/provider = producer identity（preprocessing / preprocessing）
artifact      : canonical_l1 = artifact maturity，不代表 producer identity
seal          : Primary Path requires valid identity creation, not mandatory Seal pipeline
producer meta : 独立 metadata entity/table；不进入 role/provider，不作 source_meta 长期扩展字段
```

---

## 2. Explicit Non-Authorization

Explicit Non-Authorization:
- producer_metadata schema introduction
- any DDL
- migration execution
- existing data migration
- production DB mutation
```

**特别声明**：

```text
producer_metadata schema
    =
separate migration authorization required
```

> **依据**：`producer_metadata schema introduction` 属 schema 变更 ⇒ 归 **Phase B**，
> 须由 Owner 单独签发 migration 授权。**本次授权不覆盖该项。**

**附带说明**：Blocking-2 已实测关闭，数据库为空 ⇒
`existing data migration` **在本项目当前状态下无适用对象**；
但该事实**不构成**对 `production DB mutation` 或 `migration execution` 的授权。

---

## 3. Implementation Phasing

### Phase A — No Migration（**本次授权范围**）

允许：

```text
✅ code changes
✅ validation
✅ tests
✅ non-persistent model changes
```

具体覆盖 §1 表中**除** `producer_metadata schema introduction` 以外的全部能力。

### Phase B — Migration（**未授权，须另立**）

Migration:
  NOT AUTHORIZED
```text
⛔ producer_metadata table
⛔ 任何 schema migration
```

**Phase A 与 Phase B 的边界**：任何需要 DDL 的动作（含建表、改约束、加列）
一律属 Phase B。Phase A 内**不得**以任何形式触发 DDL。

> `[FACT]` 注意：`source repository predicate alignment` 若涉及**唯一约束变更**
> （而非仅 re-read 谓词），则该部分属 Phase B。实施方须在开工前判定并报备。

---

## 4. Required Tests（Phase A 内必须交付）

```text
tests green  ≠  identity correctness proven
```

最低要求（现有测试**不覆盖**下列任何一项）：

| 能力 | 断言要点 |
|---|---|
| `identity invariant tests` | `original_sha256 == SHA256(接收字节)`，且 `≠ sha256_hex(body_text)` |
| `identity invariant tests` | 同文档同输入 ⇒ 幂等命中既有 version |
| `artifact-kind validation` | `role`/`provider`/`artifact_kind` ∈ 闭集；非法值 **fail-fast** |
| `identity invariant tests` | 跨域（PDF vs md）**不要求** `original_sha256` 相等（2-B 不变量） |

> 护栏说明：现有 `test_x26_fint08` / `test_x26_frb01` 的**源码文本 / AST 断言**
> **不得**以改断言方式绕过；两 runner 必须保留 `enforce_interface_scope` 调用及其顺序。

---

## 5. Exit Criteria（Phase A 完成条件）

```text
[ ] §1 表中全部能力已实现（producer_metadata 除外）
[ ] §4 全部测试通过，且为【新增】断言
[ ] le_hash / version identity / replay / uniqueness 四项已同批验证
[ ] 无 DDL / 无 migration / 无 DB 写入
[ ] 冻结的 Spec / Contract 正文未改动
[ ] Papers 工作树 0 改动
```

---

## 6. Current Governance Preconditions（全部已满足）

```text
Blocking-1  : RESOLVED（2-B）
Blocking-2  : RESOLVED（2026-09-27T09:13:28Z 实测：数据库为空）
Blocking-3  : RESOLVED（canonical_l1 × preprocessing 合法）
Errata      : READY FOR FINAL APPROVAL
```

⇒ 除**本文件签署**与 **Errata FINAL APPROVED** 外，无剩余前置。

---

*Recorded 2026-09-27 as DRAFT. 本文件未生效，不构成授权。签发后由 Owner 更新 Status / Signature。*
