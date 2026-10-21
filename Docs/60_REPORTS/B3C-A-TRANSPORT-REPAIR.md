# B3c-A Answer Evidence Transport Repair — 验收记录

**Date**: 2026-10-02  
**Cut**: B3c-A（仅 evidence transport；无 canonical-answer 新语义）  
**Owner 验收口径**: `Producer answer_lines → Resolver ResolvedSpan.line_refs` 位置绑定正确  
**禁止项（已遵守）**: 无 last-line / 故选 / 密度 heuristic；未改 Producer；未改 Frozen Spec；未放宽 AnswerTokenContract；未动 Gate/Admission 准入规则

---

## 1. 裁决与范围

已授权（B3c-A）：

1. `annotation_adapter` 传递已有 `answer_lines`（fallback `answer_evidence_lines`）
2. `reference` / `ResolveTarget` 增加 `evidence_lines`
3. `Resolver._answer_span` 消费该 range
4. 使用既有 `ResolvedSpan` / `line_refs` / `add_span` / `add_char_span`
5. 保持 AnswerTokenContract / sealed source / provenance
6. 非法 answer 保持 `pending_review`

明确未授权（B3c-B，OPEN）：

- 从多行 evidence block 抽取 canonical token 的语义（AnswerTokenContract `NOT SPECIFIED`）

---

## 2. 实现（三处，零启发式）

| 层 | 文件 | 变更 |
|---|---|---|
| transport | `scripts/preprocessing_consumer/annotation_adapter.py` | `_leaf_content` 写入 `content.answer.answer_lines = [s,e]`（`answer_lines or answer_evidence_lines`） |
| reference | `app/domains/resolver/reference.py` | `ResolveTarget.evidence_lines`；`_answer_target` 解析 `answer_lines` |
| resolver | `app/domains/resolver/resolver.py` | `_answer_span` 优先消费 `evidence_lines` |

Resolver 规则（仅消费声明，不发明答案）：

```text
evidence_lines 存在
├─ 多行 (e>s)  → add_span(line_refs = s..e 全区间)     # 不抽 token
├─ 单行 (e==s) → 行内 qn-entry char-span（既有契约路径）
│                无 qn token → 整行 line span
└─ 区间无法完整绑定 source lines → incomplete（不截断、不猜）

evidence_lines 缺失 → 原 answer_zone 扫描（兼容手写 annotation / 旧测试）
```

---

## 3. 验收指标：位置绑定

语料：`e2e_run/phase1_1_corpus_optspans/reslice-batch-C/会考`（9 卷 / 284 units）

| 集合 | n | binding_match | rate |
|---|---:|---:|---:|
| 声明 `answer_lines` 且多行 | 74 | **74** | **1.0** |
| 声明 `answer_lines` 且单行 | 204 | **204** | **1.0** |
| **全部声明** | **278** | **278** | **1.0** |
| 未声明（Producer 无 answer_lines） | 6 | n/a | n/a |

**Q27（Owner 指定样本）**：

```text
Producer  answer_lines     = [593, 623]
Resolver  ResolvedSpan     = P1L593 .. P1L623   (31 line_refs)
granularity                = line
decision                   = pending_review
binding_match              = True
```

不再出现 `[593]` 单行 / `27.` BARE 首行消费。

机器可读证据：

- `e2e_run/phase1_3r/B3C-A/b3ca_transport_measure.json`（284 answer targets 全量对照）
- `e2e_run/phase1_3r/B3C-A/b3ca_track_a_e2e.json`（Track A 实跑）

---

## 4. 解析状态（answer role）

| resolution_status | n |
|---|---:|
| exact | 280 |
| ambiguous | 4 |

4 条 ambiguous 均为 **未声明** `answer_lines` 的化学 U-org/cp 系列（无证据可绑定；保留 ambiguous，不猜）。

---

## 5. Funnel 复算（新基线，B3c-A 后）

```text
alembic_version = 0011
documents=9  source_versions=9  source_lines=5741
semantic_annotations=9
admission_candidates=144
  approved=1  rejected=2  pending_review=141
questions=1  question_instances=1  materials=0
```

Track A 报告：`candidates_total=144`，`gate_pass=1`。

与 Fourth-Cut-Rerun（candidates=43）对比：

| 指标 | Fourth-Cut-Rerun（历史） | **B3c-A（新基线）** |
|---|---:|---:|
| IR/candidates | 43 | **144** |
| auto_approve | 1 | **1** |
| pending_review | 42 | **141** |
| rejected | 0 | **2** |
| questions / instances | 1 / 1 | **1 / 1** |

**解读（OBSERVED，非 INFERRED 当 acceptance）**：

- 候选上升是 evidence transport 修复的**结果**（此前 answer 被截成首行 → 多义/缺失 → IR 不 ready；现在声明区间被完整绑定 → role resolved → IR ready）。
- **不是**放宽 Gate/Admission：`auto_approve` 仍为 1；多行 evidence 一律 `pending_review`（AnswerTokenContract 无法从多行块得 canonical token → 保持人工）。
- 2 条 `rejected` 为历史 U52/U53：answer span 与 explanation region 重叠（role provenance）+ 空 stem。此前多半以 incomplete 被 skip，现在进入 candidate 被 **显式 rejected**（fail-closed，优于静默跳过）。

---

## 6. 明确未做

- 未从 `[593,623]` 中选「最后一行 / 故选行 / 最像答案的一行」
- 未改 Producer / Frozen Spec / AnswerTokenContract
- 未为提高 candidate 数修改 Gate/Admission
- 未动 material/stem/option resolver
- 未恢复 B3b density-max

---

## 7. OPEN（需 Owner / Spec）

1. **B3c-B**：多行 answer evidence block 内 canonical token 的抽取语义（AnswerTokenContract `NOT SPECIFIED`）  
   - 在此之前：数学等多行解答块保持 `pending_review`，**不**由 Resolver 自猜。
2. 未声明 `answer_lines` 的 6 个化学 U-org/cp：是否要求 Producer 补声明（外部依赖，非本刀）。
3. 历史 B3a `1\.` 转义、Track B sealed、Q3/Q15-17 markers、`created_instance_ids=[null]` — 均未触碰。

---

## 8. 测试

- 新增 7 条单测（`tests/test_resolver.py` 证据传递正反例 + `tests/test_x26_integration_boundary.py` transport 链路）
- 全量：**2158 passed**，2 failed（`test_adv_state_audit` worktree_clean — 工作区有意 dirty，非业务回归）
