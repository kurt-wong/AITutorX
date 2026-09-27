# OWNER-DECISION-PRIMARY-PATH-IDENTITY-02

```text
Document Type : Owner Decision Record（本仓 Owner Decision Authority）
supersedes    : —
superseded_by : —
readers       : MIMO CODE；DSH；后续授权作者；任何引用 I-1/I-2/I-3 或路径裁决者
Status        : CLOSED
Decision State: APPROVED
Date          : 2026-09-27
Authority     : 本文件（Owner Decision Authority）
Parent        : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

**本文件性质**：对 `PRIMARY-PATH-IDENTITY-PRE-SIGNATURE-CHECK.md` §8 三项待确认项
（I-1 / I-2 / I-3）与文件放置事项的 **Owner 裁决落盘**。依 `OWNER-DECISION-…-01.md` Decision 4，
Owner 裁决必须落于 `Docs/40_DECISIONS/OWNER-DECISION-*.md`，**不得只存在于聊天记录**。

**Hard rule**：

```text
本文件下裁决 ≠ Errata 批准
本文件下裁决 ≠ Implementation 授权
本文件下裁决 ≠ 签署 Implementation Authorization
```

---

## Decision I-1 — Decision 编号保持不変

`[OWNER DECISION]`

```text
Keep Decision numbering unchanged.
Derived Hash Impact remains under Decision 2.
```

**含义**：

```text
· Decision 1–4 的既有编号【不变更】
· Decision 4 仍 = Owner Decision 原文入仓
· Derived Hash Impact 仍隶属 Decision 2（§2.6）
· 【不】为对齐 pre-signature check §3.2 的措辞而重新编号
```

**理由（记录）**：重新编号会造成既有交叉引用漂移，且 `Derived Hash Impact` 与
`original_sha256` identity domain 同源（`le_hash = f(original_sha256)`），
置于 Decision 2 之下在语义上是自洽的。

⇒ **pre-signature check §3.2 的 I-1 项据此关闭，状态 = RESOLVED（编号不变）。**
该 check 文档的措辞（check B 将 Decision 4 描述为 derived hash dependency）
**保留为历史记录，不修改**。

---

## Decision I-2 — 谓词对齐的 Phase 边界保持有条件

`[OWNER DECISION]`

```text
Keep source repository predicate alignment conditional boundary:

    predicate-only correction      → Phase A
    constraint / schema / index change → Phase B
```

**含义**（对应 `IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md:151-153`）：

```text
source repository predicate alignment 恒属 Phase A
        【当且仅当】其实现仅涉及谓词（predicate）修正；

若该能力的实现涉及
    · 唯一约束变更（constraint）
    · schema 变更
    · 索引变更（index）
则【该部分】属 Phase B，须独立 migration 授权。
```

**实施方义务**：开工前判定本能力是否触及上列三类变更，并**报备**；
触及者不得在 Phase A 内实施。

⇒ **pre-signature check §4.3 的 C-1 项据此关闭，状态 = RESOLVED（条件保持）。**

---

## Decision I-3 — 无需变更

`[OWNER DECISION]`

```text
No change required.
```

**含义**：pre-signature check §4.3 的 C-2 项（check C 的 Phase A 列举未含
`seal role-provider enum extension` 与 `model schema test alignment`，二者实际在 Phase A）
**不需要任何文档变更**。

⇒ 该二能力**维持**于 Phase A（`IMPLEMENTATION-AUTHORIZATION-…-01.md:67`、`:72`）。
check C 措辞为 `Includes:`（非穷举），不构成失败。

⇒ **C-2 项关闭，状态 = RESOLVED（无需变更）。**

---

## Decision I-4 — 文件放置

`[OWNER DECISION]`

```text
Keep PRIMARY-PATH-IDENTITY-PRE-SIGNATURE-CHECK.md under Docs/60_REPORTS/.
```

**含义**：

```text
· 该文件性质 = Verification Record（evidence），置于 Docs/60_REPORTS/
· 【不】移至 Docs/40_DECISIONS/
符合 DOC-GOV:282-283「结论 → 40_DECISIONS/；证据 → 60_REPORTS/」
```

⇒ 与 `PRIMARY-PATH-IDENTITY-CLOSURE-SUMMARY-01.md` 保持 `40_DECISIONS/`
（结论载体）**不冲突**：二者性质不同。

---

## Authority Boundary（本文件不授权事项）

`[OWNER DECISION]` 本文件：

```text
✗ 不修改任何 signature 字段
✗ 不批准 Errata（FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md 仍为 READY FOR FINAL APPROVAL）
✗ 不授权 Implementation
✗ 不签署 IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md
✗ 不修改 pre-signature check 文档
✗ 不修改 OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md（Decision 编号保持）
```

---

## Status

```text
STATUS:
  READY FOR OWNER SIGNATURE
```

**仍未完成、需 Owner 亲自执行的动作**（与 `PRE-SIGNATURE-CHECK.md` §9 一致）：

```text
前置 1  Errata FINAL APPROVED
        Docs/30_CONTRACTS/FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md
        Decision State: READY FOR FINAL APPROVAL → FINAL APPROVED

前置 2  Implementation Authorization 签署（Phase A only）
        Docs/40_DECISIONS/IMPLEMENTATION-AUTHORIZATION-PRIMARY-PATH-IDENTITY-01.md
        签署区填 Signed by / Date，Verdict 勾 ☐ AUTHORIZED (Phase A only)，
        Status: OPEN → CLOSED
```

---

*Recorded 2026-09-27. 本文件为 Owner Decision Record。close 项 I-1 / I-2 / I-3 / 文件放置均已 RESOLVED；不含 Errata 批准与 Implementation 授权。*
