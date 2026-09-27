# X2-06 — Decision Mapping

> **[CLOSED 2026-09-27]** 本文件的生命周期已结束（阶段完成）。**正文保持原样不改写**（DOC-GOV §7）。
> 保留在主视野：其内容仍具参考价值。当前状态见 [`Docs/50_OPERATIONS/CURRENT_STATE.md`](../50_OPERATIONS/CURRENT_STATE.md)。


**Document ID**: X2-06
**Task**: TASK-X2-CLAUDE
**Document Type**: Decisions / Mapping
**Status**: `CLOSED`（原状态：`ACTIVE — X2 MAPPING (not renumbering)`）
**Date**: 2026-09-18
**Hard rule**: **历史 ID 不得擅自重编号**；用 mapping / alias / legacy reference

---

## 1. Namespaces in play

| NS | Owner ledger | Range observed | Authority |
|----|--------------|----------------|-----------|
| `OD-*` | AITutorX GF-006 | OD-01,03,04,05,06,10,14,18（本批已裁）；OD-001+ 为 REPORT-E **队列项**（非已裁） | GF-006 = 正典 |
| `OQ-GF-*` | AITutorX GF-005 | 001–018 | GF-005 |
| `BL-*` | AITutorX REVIEW/GF-003/06 等 | 09/10/11 OPEN | GF 文本 |
| `V3 DEC-*` | AITutors-v3 COORDINATION | 001–036 | V3 CURRENT/state.yaml |
| `DSH DEC-*` | Papers COORDINATION | 012–049 | Papers state.yaml / ODR（canonical） |
| `Papers OQ-*` | Papers/Contract discussions | 5,6,8,10–21 等 | 不等于 OQ-GF |
| `EB-*` | 双仓 coordination | EB-0.3B, EB-001–009… | 双仓叙事 |
| `BUG-V3-*` | V3 bugs.md | ~50 条叙事 | V3 |
| `BUG-*` | Papers bugs.md | 09… 等 | Papers |
| `D-048-*` | Papers Guardian | 1/2/3 | Papers CURRENT；GF binding |
| `AIT-DEC-*` | REPORT-C **提案** | 001+ | **未被账本采用** |
| `C-X2-*` | 本阶段冲突登记 | 01–10 | X2-01 |
| `X2-*` | 本阶段文档 | 00–10 + REPORT-X2 | AITutorX |

---

## 2. AITutorX OD（已裁，GF-006 正典）

| ID | Topic | Status | Must not read as |
|----|-------|--------|------------------|
| OD-14 | GF v0.2 Freeze | `[OWNER DECISION]` | Migration Authorization |
| OD-01 | Migration Authority Charter 建立 | `[OWNER DECISION]` | 迁移执行权限 |
| OD-10 | Artifact Registry 建立 | `[OWNER DECISION]` | Registry 实例已创建 / admitted |
| OD-03 | 分层 Authority Taxonomy（GOV/EVD/EXT + RSD/PIS/OCRA/SEM/MIG） | `[OWNER DECISION]` | 互替 / 执行已完成 |
| OD-04 | Hash-based Source Identity | `[OWNER DECISION]` | maintainess 或 original = canonical |
| OD-05 | NAS-backed Read-only Data Model | `[OWNER DECISION]` | 数据已迁入 |
| OD-18 | Difference Ledger 建立 | `[OWNER DECISION]` | OQ-GF-007 已关 |
| OD-06 | REPORT-G/H/I/K 整理后收编 | `[OWNER DECISION]` | admitted=true |

**REPORT-E OD-001+ = Owner Decision Queue items，不是已裁 OD。** 不得与 GF OD-* 混读。

---

## 3. Known cross-ledger collisions（须双侧标注）

| Colliding ID | V3 meaning | DSH/Papers meaning | AITutorX rule |
|--------------|------------|--------------------|---------------|
| DEC-021 | B2 Identity（唯一 source identity = SHA-256 raw bytes 等） | Interface Decision Finalization / 四项裁决族 | 引用写 `V3 DEC-021` / `DSH DEC-021` |
| DEC-022 | B3 Semantic Boundary | Interface Decision Finalization v1（≡ V3 DEC-027） | 双标 |
| DEC-023 | Interface Scope 87/71 | Interface Finalization Revision v1（≡ V3 DEC-028） | 双标 |
| DEC-031~036 | Contract freeze 执行/审计/Freeze 令序列 | DSH 侧另有编号（DEC-025/026/027/028 等；DEC-048/049 Guardian/Brief） | 双标 + 引用 Papers ODR § |

`[FACT]` 双仓 CURRENT 对照（部分）: V3 DEC-023~026 ≡ DSH DEC-021-1~4；V3 DEC-027 ≡ DSH DEC-022；V3 DEC-028 ≡ DSH DEC-023；V3 DEC-030 ≡ DSH DEC-025；V3 DEC-031 ≡ DSH DEC-026；V3 DEC-036 = Owner Freeze 令。

---

## 4. Mapping table format（AITutorX `Docs/40_DECISIONS/` 使用）

`[PROPOSAL]` 未来 40_DECISIONS 条目必须使用双栏/多栏，**禁止**覆盖 legacy ID:

```text
Canonical reference (display): AITutorX ref to <legacy-id> @ <repo> @ <commit/path>
Legacy IDs:
  - V3 DEC-xxx @ AITutors-v3
  - DSH DEC-yyy @ Aitutors-preprocessing
Topic: ...
Status in source ledger: ...
GF/OQ cross-links: ...
Authority: SOURCE LEDGER (unchanged)
```

**本阶段不批量填充 40_DECISIONS 历史正文**（OQ-GF-016 仍 OPEN-BLOCKING）；仅固化映射规则与碰撞表。

---

## 5. REPORT-C status

`[FACT]` REPORT-C 提出 `AIT-DEC-*` / `AIT-BUG-*` canonical 化。
`[FACT]` 任一源账本 **未采用** 该前缀。
`[CONFLICT]` REPORT-C 部分主题标签与 V3 CURRENT 不符（REPORT-H 已登记）。

**X2 处置**: REPORT-C = `RETAIN-AS-HISTORICAL` 映射**草稿**；**不是** mapping authority。
`[OWNER DECISION REQUIRED]` 唯一 mapping authority 载体。

---

## 6. Decision families relevant to X2 lifecycle

| Lifecycle area | Key decisions (source IDs) | Mapping note |
|----------------|----------------------------|--------------|
| Identity | OD-04；V3/DSH DEC-021 族；DEC-030/031 naming | 语义一致层已冻结 |
| Semantic states | V3/DSH DEC-025/027/028 Part5/6 | 双层词表 |
| Interface scope | V3 DEC-023/024/028 Part4 | 87/71/16/79 |
| Contract freeze | V3 DEC-032–036；DSH freeze evidence DEC-027/028 | Freeze object 唯一 |
| Guardian / gaps | DSH DEC-037–049；D-048-1/2/3 | binding ≠ closed |
| AITutorX governance | OD-14/01/03/05/06/10/18 | GF-006 |
| EB-008 evidence authority | V3 DEC 75–92 / 87–92 系列 | implementation vs external verification |

---

## 7. Open mapping decisions（不关闭）

| Item | Status |
|------|--------|
| OQ-GF-016 DEC/BUG/OQ namespace policy | OPEN-BLOCKING |
| OQ-GF-017 Design/untracked + D2/D4 authority | OPEN-BLOCKING |
| D2/D3/D4 Owner must decide（Papers DEC-049） | OPEN |
| Mapping authority 指定 | `[OWNER DECISION REQUIRED]` |
| 是否禁止 40_DECISIONS 新增无前缀 `DEC-*` | `[OWNER DECISION REQUIRED]` |

---

*Decision mapping registered. No historical ID renumbered.*
