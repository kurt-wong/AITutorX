# THIRD CUT — Genuine overlap semantic RCA（对象集校正 = 14）

**Level**: 语义分类调查（**禁止改生产代码** / 禁止改 overlap invariant）
**Date**: 2026-10-02
**Baseline**: `39840ff` · `match-norm/v1.1` dirty

---

## 0. 对象集校正（口径）

| 表述 | 值 | 说明 |
|---|---|---|
| 错误 | 12 = 2+6+12 | 与 `overlap_final_evidence` 成员对不上（双重计数） |
| **正确** | **14 = 20 − 6** | 6 = 第二刀目标（B_MARKER_RELOCATION_DRIFT：Q1,Q2,Q4,Q5-6,Q7-8,Q18-20） |
| 对照样本 | 3 resolved + 3 unresolved | 第二刀后 Q2/Q7-8/Q18-20 vs Q1/Q4/Q5-6 |

**U52/U53（same-region）与 Q3/Q9-11/Q12-14/Q15-17/Q21-25（跨对象）都在这 14 里**，不是集合外的 2+5。

---

## 1. 对照样本（第二刀后为何 3 能解析、3 不能）

| unit | 旧 infl | 新 res / infl | 为何 |
|---|---:|---|---|
| Q2 | 122.8× | **6 / 1.5** | 区间外存在 **unique** 分隔文本 |
| Q7-8 | 60.8× | **10 / 1.25** | 同上 |
| Q18-20 | 94.4× | **7 / 1.4** | 同上 |
| Q1 | 82.0× | **0 / —** | 外侧无 unique 文本（padding 预算内）→ **拒发 marker** |
| Q4 | 98.0× | **0 / —** | 同上 |
| Q5-6 | 81.2× | **0 / —** | 同上 |

**判别力**：同一卷、同一机制；差别只在「能否证明 occurrence」。  
→ 支持原则：**宁可 unresolved，不制造错误大 span**；不是把 duplicate 一刀切成 unresolved。

---

## 2. 14 条语义分类（逐 unit）

| unit | 文档 | mat vs q | overlap 对象 | 重叠是否真实在原文 | 边界 or 实质 | Producer 能表达共享？ | Resolver 错 span？ | decomposition？ | ownership？ | Spec？ | 建议 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U52 | 历史 | SAME | own stem | 是 | **边界** | N/A | **是** | **是** | 否 | 否 | **修代码** stem 不进 material |
| U53 | 历史 | SAME | own stem | 是 | **边界** | N/A | **是** | **是** | 否 | 否 | **修代码** |
| Q37 | 政治 | PARTIAL | Q36.stem | 是 | **边界** | N/A | **是**（Q36 stem 过宽） | **是** | 否 | 否 | **修代码** stem 止于下一题/材料 |
| Q3 | 英语 | DISJOINT | material×4 | 是（附录） | **实质/相邻** | **是**（听力稿） | 可能 | 否 | **是** | **可能** | **语义裁决** shared listening |
| Q9-11 | 英语 | DISJOINT | material | 是 | **实质/相邻** | **是** | 可能 | 否 | **是** | **可能** | **语义裁决** |
| Q12-14 | 英语 | DISJOINT | material | 是 | **实质/相邻** | **是** | 可能 | 否 | **是** | **可能** | **语义裁决** |
| Q15-17 | 英语 | DISJOINT | material | 是 | **实质/相邻** | **是** | 可能 | 否 | **是** | **可能** | **语义裁决** |
| Q21-25 | 英语 | DISJOINT | material+answer | 是 | **实质** | **是** | 可能 | 否 | **是** | **可能** | **语义裁决** |
| U49-52 | 英语 | SUBSET | material | 是（邻接） | 边界 or 实质 | 不确定 | 否 | 否 | **是** | 否 | **核 Producer 段界** |
| U53-56 | 英语 | SUBSET | material | 是 | 边界 or 实质 | 不确定 | 否 | 否 | **是** | 否 | **核 Producer** |
| U57-60 | 英语 | SUBSET | material | 是 | 边界 or 实质 | 不确定 | 否 | 否 | **是** | 否 | **核 Producer** |
| U10-13 | 语文 | SUBSET | Q9.stem | 是 | **边界** | N/A | **是** | **是** | 否 | 否 | **修代码** stem/material 分界 |
| U14 | 语文 | SUBSET | own stem | 是 | **边界** | N/A | **是** | **是** | 否 | 否 | **修代码** |
| U15 | 语文 | SUBSET | own stem | 是 | **边界** | N/A | **是** | **是** | 否 | 否 | **修代码** |

---

## 3. 汇总

| 类 | n | unit |
|---|---:|---|
| **代码 bug 候选**（stem 边界 / decomposition） | **6** | U52 U53 Q37 U10-13 U14 U15 |
| **语义裁决**（shared listening material） | **5** | Q3 Q9-11 Q12-14 Q15-17 Q21-25 |
| **Producer 段界核查** | **3** | U49-52 U53-56 U57-60 |

```text
overlap_invariant_modified = false
production_code_modified   = false
```

---

## 4. OBSERVED vs CAUSAL

### OBSERVED
- 14 成员清单与 `overlap_final_evidence` 一致（20−6）
- 每条 declared / questions / resolved / evidence / 源文预览（JSON）
- 对照 3+3 的 inflation 与 occurrence 证明情况

### SUPPORTED
- 6 条：**stem 过宽 / 单 sub 覆盖 material** → 与 overlap 拒绝 **structurally consistent**
- 5 条：附录听力稿 **实质相邻/共享** → 不宜用「消 overlap」解决
- 3 条：阅读段落邻界 → 优先 Producer 边界

### NOT CLAIMED
- 放宽 overlap invariant
- LEVEL 2 可解这 14 条

---

## 5. 审计（简短）

`TRUNCATE … CASCADE` 曾在刀间与终测前执行（保留 `alembic_version`）。  
**历史报告中的 9 docs / 35–41 candidates / llm_call_audit=1213 仍为历史观察**；**不得**称「当前 DB 可复核」。  
不阻塞本语义调查。

---

## Evidence

```text
e2e_run/phase1_3r/cut3_overlap_semantic_rca.json   # 14 + controls + audit
e2e_run/phase1_3r/overlap_final_evidence.json
e2e_run/phase1_3r/second_cut_measurement.json
```
