# FOURTH CUT — Material / Stem / Answer Boundary Repair

**Date**: 2026-10-02  
**HEAD**: `39840ff` · **dirty baseline**: `match_normalization.py` v1.1 + `annotation_adapter.py` + `runner.py` (cuts 1–2)  
**Frozen Spec / overlap invariant / AnswerTokenContract / LEVEL 2 / schema**: **未改**

---

## 基线

| 项 | 值 |
|---|---|
| focused tests before | 98 passed（gate/annotation/resolver/ir/compiler） |
| IR Ready before | **41**（Second Cut） |
| candidates before | **41**（historical E2E；当前 DB 已清空后重跑） |
| llm_call_audit | 0 new（全程无 LLM） |

---

## A — Material Boundary Normalization

**实现**：`_material_span` 在 raw interior 后 **trim 首尾纯空白**（`_trim_blank_edge_refs`）。  
保留 Second Cut unique-marker + bounded outward search。

| unit | declared | before (raw) | **after (trimmed)** | == declared |
|---|---|---|---|---|
| Q9-11 | 538–541 | 537–542 | **538–541** | **YES** |
| Q12-14 | 543–561 | 542–562 | **543–561** | **YES** |
| Q21-25 | 586–610 | 585–611 | **586–610** | **YES**（material 侧） |

material–material padding overlap：**消失**（542/585 空行不再进 span）。

> Q21-25 仍可能被 **answer@593** 拒（B3，见下）——不计入 A 失败。

**A = PASS**

---

## B1 — Own-Stem Boundary（U52 U53 U14 U15）

**实现**：先解析全部 material → stem **exclude material line_refs**；region_upper 亦止于 material 起点。

| unit | stem before | stem after | ∩ own mat before | **∩ after** |
|---|---|---|---:|---:|
| U52 | 569–593 | 593 | 24 | **0** |
| U53 | 594–630 | 630 | 34 | **0** |
| U14 | 244–285 | 244–245 | 15 | **0** |
| U15 | 286–329 | 286–287 | 21 | **0** |

**B1 = PASS**（own stem ∩ own material = 0）

---

## B2 — Neighbor-Stem Boundary（Q37 U10-13）

| 检查 | before | after |
|---|---|---|
| Q36.stem ∩ Q37.mat | 448–544 ∩ 472–496 = **25** | **448–469**（止于 material 前）∩ = **0** |
| Q9.stem ∩ U10-13.mat | 76–189 ∩ 80–188 = **109** | **76–79** ∩ = **0** |

**B2 = PASS**

---

## B3 — Answer Boundary

### B3a — Producer 缺陷（登记，不改 Producer 仓）

```text
line 451 = '1\. C2\. C3\. A…'   ← 转义句点 \.
_ENTRY_RE 无法识别 1\. / 12\.
合法答案表行匹配失败
```

**依赖项**：Producer/preprocessing 需去除答案表 `\\\.` 转义（另行授权，本轮不改 Papers）。

### B3b — Resolver 最小校验（已实现）

纠正 Producer 行后，451 与台词 593 同时命中 → multi-line ambiguous。  
实现：**多行命中时保留 qn-entry 密度最高的行**（答案表），证据记 `multi-line pick density; dropped=…`。

| 输入 | Q12-14 answer | 593 |
|---|---|---|
| 原 Producer + density | 仍 593（451 无 entry） | 未拒 |
| **纠正 Producer + density** | **451** ✓ | **拒** ✓ |

| | Q9-11 | Q12-14 | Q21-25 |
|---|---|---|---|
| 纠正后 answer | **[451]** | **[451]** | **[455]** |
| mat ∩ ans | — | — | **∅** |

**B3b = IMPLEMENTED + VERIFIED with corrected artifact**  
**B3a = OPEN dependency**（Producer unescape）；未改 Producer。

> Success 条件：legal 保留 + 非法 593 拒绝 —— 在 **纠正 Producer** 输入下满足；  
> 原 Producer 输入下 593 仍可能出现（451 匹配失败）→ 记为 B3a 依赖，非 V3 回归。

---

## 回归

### Tests
| | |
|---|---|
| before | 98 passed（聚焦） |
| after | **115 passed**（+ identity 等） |

### 284 / 9-paper E2E（重跑 DB）

| 指标 | Second Cut（历史） | **Fourth Cut** |
|---|---:|---:|
| IR Ready（compute） | 41 | **43** |
| **candidates** | 41 | **49** |
| auto_approve | 1 | **1** |
| 数学 | 23 | **28** |
| 语文 | 3 | **5** |
| 物理 | 3 | **4** |
| 英语 | 6 | 6 |
| skip | 243 | 235 |
| questions / instances | 1 / 1 | 1 / 1 |
| **new LLM calls** | — | **0** |
| lost ready | — | **0**（41 基线保留并增加） |

**新 unresolved**：无导致 ready 丢失。  
**unrelated files**：仅 `resolver.py` + 既有 dirty 三文件。

---

## 分支报告

```text
A   PASS (trim blanks; 3/3 declared match; padding overlap gone)
B1  PASS (4/4 own∩mat = 0)
B2  PASS (Q36/Q9 neighbor stem clipped)
B3a OPEN dependency (Producer \\. unescape) — 不改 Producer
B3b IMPLEMENTED (density pick) — corrected artifact 下 451 保留 / 593 拒绝
```

---

## Evidence

```text
e2e_run/phase1_3r/fourth_cut_e2e_report.json
code: app/domains/resolver/resolver.py  (_trim_blank_edge_refs, two-phase material, stem exclude, answer density)
      scripts/preprocessing_consumer/annotation_adapter.py (unique-marker walk)
```

**历史 DB 标注**：Second Cut 的 41 candidates / llm_call_audit=1213 为历史观察；本轮为清库后重跑。
