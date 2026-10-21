# PHASE1.2R — Evidence Addendum

**Level**: LEVEL 1（纯证据补强，非修复）
**Date**: 2026-10-02
**Scope**: sealed replay 内容级证据 + 284-unit IR census + Producer→Adapter→IR 位置证据因果核验
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

**Git binding（全文数字强制）**：

```text
branch   od01-r3-convergence
HEAD     39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4
worktree M backend/app/domains/resolver/match_normalization.py
         blob 015cdfa515ce23661ac1d9f02fb861869e111363
HEAD     blob 73badc31fe94d4066f9e53469cb704b11ba8844b
version  match-norm/v1.1 (dirty, uncommitted)
```

**NOT-GO 已遵守**：未改业务代码 / Adapter / Resolver / IR Builder / Frozen Spec / Contract /
AnswerTokenContract / Authority / DB 既有数据。仅新增 verification scripts + evidence + report。

---

## 0. 锁定参数（DSH 补丁）

| 项 | 锁定值 |
|---|---|
| 13 表 | `documents` · `document_source_versions` · `document_source_lines` · `document_source_spans` · `document_active_sources` · `semantic_annotations` · `admission_candidates` · `admission_events` · `questions` · `question_instances` · `instance_role_contents` · `unit_groups` · `materials` |
| fingerprint | per-table `sha256` over rows sorted by PK；每行 canonical JSON（`sort_keys=True`, `separators=(',',':')`）；行间 `\n`；**同时记 row_count** |
| 受控对照 | 独立 harness 内构造 annotation payload（补 producer 位置），**不改** resolver/adapter 源码 |

---

## 1. P0-A Replay 内容级证据

### A. OBSERVED FACTS

产物（`e2e_run/phase1_2r/replay/`）：

| 文件 | 内容 |
|---|---|
| `phase12r_replay_fingerprint.py` | 可独立复跑的 script |
| `snapshot_before.json` | 13 表 row_count + fingerprint |
| `replay_run.json` | 只读计算链 9/9 sealed pairs |
| `snapshot_after.json` | 同上 |
| `diff_before_after.json` | count_diff + content_diff |

Diff 结果：

```text
tables_compared = 13 (locked list)
count_diff      = {}
content_diff    = {}
identical       = true
```

Replay 路径（未调用 `GateService.run`）：

```text
sealed source_version
  → get_lines_by_version / get_figures_by_version   (SELECT)
  → semantic_annotations.payload                    (SELECT)
  → SourceResolver.resolve                          (pure)
  → IRBuilder.build                                 (pure)
  → Compiler.compile                                (pure)
  → gate.policy.evaluate                            (pure, ready only)
```

### B. VERIFIED

**Q1 = SUPPORTED（内容级）**：before/after 13 表 row_count 与 content fingerprint 全等。
未 append/update/delete/reseal。脚本与三份 JSON 可被 DSH 独立复跑。

> 范围限定：**计算重放**只读。`GateService.run` / Admission `_materialize` / Track B append
> 仍是写路径，不在本结论内。

**Replay verdict:**

```text
SUPPORTED
```

---

## 2. P0-B 284-unit IR Census

### A. OBSERVED FACTS

产物：`e2e_run/phase1_2r/census/phase1_2_ir_census.json`（284 行，逐 unit）。

| IR status | n |
|---|---:|
| ready | **35** |
| not ready | **249** |
| **total** | **284** |

**Q2 = YES，可逐 unit 复现**（census 含 document_id / source_version_id / unit_id / ir_ready / reasons / 三层 reference 字段）。

### B. primary reason 分布（Q3）

规则：`material > answer_missing > answer_ambiguous > option_incomplete > option_ambiguous > stem_missing > stem_ambiguous > group_related > other`

| primary_reason | n | 占 249 |
|---|---:|---:|
| answer_missing | **161** | 64.7% |
| material_missing_or_incomplete | **54** | 21.7% |
| option_incomplete | **15** | 6.0% |
| answer_ambiguous | **15** | 6.0% |
| stem_ambiguous | **3** | 1.2% |
| stem_missing | **1** | 0.4% |

54 composite 全部落在 `material_missing_or_incomplete`。

---

## 3. P0-C Producer → Adapter → IR 位置证据

### 3.1 代码双侧证据（区分「丢弃」vs「未解析」）

| 侧 | 位置 | 事实 |
|---|---|---|
| **manifest_reader 解析** | `manifest_reader.py:51` | `material_lines: tuple[int,int] \| None` 字段声明 |
| | `manifest_reader.py:45-50,96-107` | `stem_lines` / `options` / `answer_lines` / `explanation_lines` / `material_lines` **确实解析进 ManifestUnit** |
| **adapter 持有却丢弃** | `annotation_adapter.py:131-132` | `if unit.material_lines: shared["material"] = {"role":"material"}` — **已持有 producer 位置，payload 只写 role** |
| | `annotation_adapter.py:52-73` `_leaf_content` | stem/option/answer 只写 `role` / `label` / `answer_zone`，**无 start_line/end_line** |

⇒ **(a) adapter 收到了位置但未写出**，不是 (b) 上游未解析。

### 3.2 字段统计（Q4 / Q5）— `producer_adapter_ir_field_stats.json`

| field | Producer has | Adapter preserves position | Adapter drops |
|---|---:|---:|---:|
| material_lines | **54** | **0** | **54** |
| stem_lines | **230** | **0** | **230** |
| options (per-label) | **174** | **0** | **174** |
| options_lines | **176** | **0** | **176** |
| answer_lines | **278** | **0** | **278** |
| explanation_lines | 53 | 53（仅 role） | 0 |

**Q4**：Producer 提供的位置证据 = stem 230 / answer 278 / options 174 / material 54（units 计）。
**Q5**：Adapter **全部位置字段 drop = 100%**（explanation 只保留 role，属声明形态）。

### 3.3 IR/Resolver 消费路径（Layer 3）

| 问题 | 事实 |
|---|---|
| IR Builder 是否要求 material reference？ | IR 对 material role 无 span → `semantic_status=incomplete`（实测 54 composite 全灭） |
| Resolver 是否从正文猜 material？ | **否**（resolver.py 文档：「E 可以失败，但不能猜」）；material 走 `start_marker/end_marker`，**不读 role 内 start_line** |
| 无 reference 时失败点 | `SourceResolver.resolve` → UnresolvedReference（`material incomplete` / `answer missing`…）→ IRBuilder 标 incomplete → Gate skip |
| failure reason 原文 | census `unresolved` 角色×status：`answer missing` / `material incomplete` / `option incomplete` 等 |
| 是否由 reference 不存在触发？ | **是**（UnresolvedReference 为 reference 未解析；非 compile 崩溃） |

**关键代码事实**（防止循环论证）：

```text
reference.py::_stem_target / _option_target / _answer_target
  → ResolveTarget(kind=question_label|option_label|answer_zone)
  → 不读取 start_line / end_line / line_refs
```

现有 Annotation reference 契约**根本不消费**行号字段。

---

## 4. 受控对照实验（Q6 / Q7 / Q8 的实证）

### A. OBSERVED

`controlled_position_injection.json`（harness deep-copy payload，注入 producer
`start_line/end_line`；**resolver/adapter/IR 源码零修改**；不写 DB）：

```text
total_units                     = 284
ir_ready_A  (as-is payload)     = 35
ir_ready_B  (positions injected)= 35
delta_B_minus_A                 = 0
```

### B. VERIFIED CAUSAL

| 命题 | 证据强度 | 结论 |
|---|---|---|
| Adapter 丢弃 producer 位置 | 代码+字段统计 | **成立** |
| 「位置丢弃」经**现有契约**直接导致 249 IR loss | 受控注入 | **不成立**（注入后 ready 不变） |
| 54 composite material 失败是独立 parser 问题还是通用 reference-loss 的表现 | 见下 | **通用 reference 未解析机制的表现**（material 也是 UnresolvedReference），**但**受控注入对其无效 ⇒ 不是「缺 start_line 字段」单独造成 |

**Q6**：co-occurrence（adapter drop ∧ not-ready）= 249；
**经位置注入的直接因果 = 0**。
不能把 249 全部归因于「adapter 丢字段」。causality for the full 249 via field-drop:

```text
NOT ESTABLISHED
```

**Q7**：54 composite material failure =
**通用 reference-resolution 机制的表现**（同属 UnresolvedReference→IR incomplete），
**不是**与 249 无关的独立 parser 子系统；但其修复不能靠「payload 补 start_line」（已实测无效）。

**Q8**：

```text
REQUIRED
```

**限定语义**：若裁决方向是「让 Resolver 消费 Producer 位置证据」，则 **LEVEL 2 必需**
——因为必须改 ResolveTarget / extract_targets / resolver policy（现契约不读行号）。
**不是**「只改 annotation payload 加几个字段」就够（对照实验 Δ=0）。

备选方向（加固 `answer_zone`/label 启发式、改 H-3 匹配）**不需要** payload 契约变更，
但那是另一条修复线，本轮不选边。

---

## 5. 249 loss 归因表

| primary_reason | n | Producer 有对应位置 | Adapter 写出位置 | 位置注入后仍失败 |
|---|---:|---|---|---|
| answer_missing | 161 | 161 有 answer_lines | 0 | 是（B=A） |
| material_missing_or_incomplete | 54 | 54 有 material_lines | 0 | 是 |
| option_incomplete | 15 | 有 options/options_lines | 0 | 是 |
| answer_ambiguous | 15 | 11 有 answer_lines | 0 | 是 |
| stem_ambiguous | 3 | 有 stem_lines | 0 | 是 |
| stem_missing | 1 | 有 stem_lines | 0 | 是 |
| **合计** | **249** | | | |

| 归因桶 | n | 依据 |
|---|---:|---|
| co-occurrence: adapter drop ∧ not-ready | 249 | census |
| **causal via position-injection** | **0** | controlled Δ=0 |
| residual primary=answer/material/option resolve 失败 | 249 | resolver 启发式 + 契约不消费行号 |

---

## 6. 三层表述纪律

### A. OBSERVED FACTS
见 §1–§3 表格与产物 JSON。

### B. VERIFIED CAUSAL RELATION
1. `manifest_reader` 解析位置 → `annotation_adapter` 持有后只写 role（代码行号）。
2. 生产 `extract_targets` 不读 `start_line/end_line`（`reference.py`）。
3. payload 注入位置 → IR Ready 不变（A=B=35）。

### C. HYPOTHESIS / NEXT DECISION
- 249 的主因更可能是 **Resolver label/zone 定位启发式在真实北京卷上失败**（answer_zone=`answer_table`、单行多选项、材料区边界），而非单纯「缺行号字段」。
- 该假设**尚未**用反事实（改 resolver 启发式）验证。
- LEVEL 2 annotation/interface change **REQUIRED**（若走 producer-span 消费路线）——**待 Owner 裁决**，本轮不实施。

---

## 7. Q1–Q8

| # | 答案 |
|---|---|
| **Q1** | **SUPPORTED**（13 表 content fingerprint identical=true，可复跑） |
| **Q2** | **35 ready / 249 not**；`phase1_2_ir_census.json` 逐 unit 可复现 |
| **Q3** | answer_missing 161 · material 54 · option_incomplete 15 · answer_ambiguous 15 · stem_ambiguous 3 · stem_missing 1 |
| **Q4** | stem 230 / answer 278 / options 174 / material 54 units 带位置 |
| **Q5** | Adapter **位置保留 0**（explanation 仅 role） |
| **Q6** | co-occurrence 249；**直接因果（位置注入）= 0** ⇒ full causality **NOT ESTABLISHED** |
| **Q7** | 通用 reference-resolution 机制的表现，**不是**独立 material parser；补 start_line **无效** |
| **Q8** | **REQUIRED**（LEVEL 2：ResolveTarget/extract/resolver 消费 producer span）；仅改 payload 字段 **不够** |

---

## 8. 完成标准核对

```text
[x] Replay evidence 可独立复核
[x] 284 units machine-readable census
[x] 249 failures 逐 unit primary/secondary reason
[x] Producer positional evidence 已统计
[x] Adapter positional evidence 已统计
[x] IR consumption path 已核验（reference.py 不读行号）
[x] reference-loss 与 IR loss 已做关联（co-occurrence + 反事实）
[x] 54 composite 已放回整体漏斗解释
[x] 未修改业务代码 / Frozen Spec / Contract
[x] DSH 可从产物复算主要结论
```

**不以「下一步直接修 composite material」收尾。**
唯一交付给 Owner 的裁决问题是：

> **是否批准 LEVEL 2：Resolver reference 模型消费 Producer 行号/span（ResolveTarget + extract_targets + resolver policy）。**
> 证据表明：不改契约则位置补回无效；改契约属 LEVEL 2。

---

## Evidence index

```text
e2e_run/phase1_2r/replay/phase12r_replay_fingerprint.py
e2e_run/phase1_2r/replay/snapshot_before.json
e2e_run/phase1_2r/replay/replay_run.json
e2e_run/phase1_2r/replay/snapshot_after.json
e2e_run/phase1_2r/replay/diff_before_after.json
e2e_run/phase1_2r/census/phase12r_ir_census.py
e2e_run/phase1_2r/census/phase1_2_ir_census.json
e2e_run/phase1_2r/census/producer_adapter_ir_field_stats.json
e2e_run/phase1_2r/census/ir_loss_attribution.json
e2e_run/phase1_2r/census/controlled_position_injection.json
```
