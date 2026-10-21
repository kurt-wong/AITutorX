# 记录：Gate Decision Provenance 指令 + 一项关键只读核查结果

> Owner 指令：Viewer 必须区分**原始管线决策**、**独立重放结果**、**结构事实**、**展示文案**。
> 核心要求：**不得把导出阶段重新计算的结果写成历史事实。**
> 本轮**只记录 + 只读核查**，未改动任何文件。

---

## 1. Owner 对 DSH 修法的收紧 —— 已确认成立，且比 Owner 预想更彻底

DSH 此前建议：`if cl is None:` 分支照常调用 `evaluate()`，把真实 `decision` 写进 `gate`。
Owner 质疑：**这些没有 compiled leaf 的单元，在原始执行中是否真的执行过 Gate Policy？**

### 1.1 只读核查结果：**在 Phase 1 实验路径上，它们从未被执行过**

三条证据：

**(a) `runner_b2.py` 在 Gate 之前就跳过非 ready 单元**

```python
# L445-455
gate_results.append({
    "unit_id": root.unit_id,
    "status": "skipped",                 # ← 非 ready
    "reason": "semantic_status not ready ...",
})
continue                                 # ← 在 L457 ready_count += 1 / L458 evaluate() 之前

# L457-458
ready_count += 1
gate = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=resolved_run)
```

⇒ **对非 ready 单元，`evaluate()` 根本没被调用**，也没有产生任何 decision。

**(b) `runner_b2.py` 虽 import 了 `AdmissionCandidate`，但从未实例化或写库**

```text
L43: from app.models.snapshot import AdmissionCandidate, SemanticAnnotation
grep "AdmissionCandidate|add_candidate|create_candidate" -> 仅 L43（import 行本身）
```

`gate_results` 只是放进 `result["gate_results"]` 的**返回结构**（L512），不落库。

**(c) `export_raw_full.py` 是自算的，不读任何持久化决策**

```text
L33  m = load_manifest(man_path)
L37  payload = manifest_to_annotation_payload(m)
L70  gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)   ← 自己重算
```

### 1.2 结论：Owner 的质疑成立，而且结论比 Owner 的表述更强

- 对**有 compiled leaf 的 227 个单元**：`export_raw_full.py` 的 `evaluate()` 是**重算**，
  但 `policy.py::evaluate` docstring 自述「**纯函数；不触 DB**」，
  且 `runner_b2` 对同一 (manifest, md, 代码) 会得到同一结果 —— 所以**内容等价**。
  即便如此，**语义上它仍是重放结果，不是历史记录**（Phase 1 无历史记录）。

- 对**无 compiled leaf 的 57 个单元**：
  **原始执行从未调用 `evaluate()`**。因此
  - 不存在"原始 Gate 决策"；
  - DSH 原先建议的"照常跑 `evaluate()` 写进 `gate`"，会**为从未被评估过的单元伪造一个 `rejected`**；
  - 这**正是 Owner 警告的"把导出阶段计算伪装成历史事实"**。

**⇒ DSH 的原修法建议撤回。Owner 的字段语义分离方案是正确的。**

### 1.3 附带纠正 DSH 上一轮报告的一处解释

上一轮我写「这 54 个单元的真实 Gate Policy 会是 `rejected`」——**这句话的因果是错的**。
准确表述是：

```text
这些单元在原始执行中 status = "skipped"，从未进入 Gate；
它们没有候选（no candidate）；
"rejected" 只是 DSH 重放（对全部 root 调用 evaluate）得到的结果，
而那条路径并不是本次验收所走的路径。
```

⇒ 问题不只是"标签写成 incomplete"，而是**Viewer 把一个"从未评估"的状态，
显示成了看起来像 `decision_status` 的值**。修法必须分离"结构事实"与"决策来源"。

---

## 2. 对 Owner 任务指令的评估

| Owner 要求 | 评估 |
|-----------|------|
| §二.1 检查是否真的执行过 Gate、是否有原始决策记录 | ✅ **已可回答**：Phase 1 未执行、无记录（见 §1） |
| §二.3 不得把 `evaluate()` 结果伪装成原始决策 | ✅ 正确，DSH 原建议已撤回 |
| §二.5 `leaf_present` 独立字段 | ✅ 合理；建议再加 `candidate_present`（本次路径恒 false，但正式链会有） |
| §二.6 `incomplete` 不得作为 Gate 决策状态 | ✅ 正确——它不在 `DECISION_STATUS = {pending_review, approved, rejected}` 值域内 |
| §二.7 `reason_display` 更名 | ✅ 已同意（管线值应看 `gate_reasons`） |
| §三 六个验证情形 | ⚠️ **见 §3：Phase 1 只能覆盖其中 1 个，其余 5 个需正式链** |
| §五 禁止项 | ✅ 全部同意 |

---

## 3. ⚠️ 六情形验证在 Phase 1 上**大部分不可执行**（需在任务书里写明）

Owner 要求验证：

| # | 情形 | Phase 1 实验路径是否可满足 |
|---|------|--------------------------|
| 1 | 有 leaf，且有原始 Gate 决策 | ❌ **不可**——本路径无持久化决策 |
| 2 | 无 leaf，但有原始 Gate 决策 | ❌ **不可** |
| 3 | 无 leaf，且无原始 Gate 决策 | ✅ **可**（就是那 57 个单元） |
| 4 | 重放决策与原始决策一致 | ❌ 不可（无原始可比） |
| 5 | 重放决策与原始决策不一致 | ❌ 不可 |
| 6 | 重放失败或未执行 | ✅ 可（构造异常输入） |

**因此建议把任务书改成两段**：

```text
A. Phase 1（当前语料，无 DB 决策）
   - 必须证明：57 个无 leaf 单元的 gate_decision_raw 为空 / 明标 "no original decision"
   - 必须证明：Viewer 不会为该情形显示 rejected/approved/pending
   - 必须证明：若展示重放结果，字段名与来源标注明确（gate_replay_decision + status）
   - 情形 3、6 可测

B. 正式链（需 document_ingest + DB，另行立项）
   - 情形 1、2、4、5 依赖「原始决策被持久化」（admission_candidates.gate_decision JSONB）
   - 此段不能在当前任务内完成，应列为后续验收项
```

**否则会出现**：MIMO 为了"通过"六个情形，**构造合成数据**去满足 1/2/4/5——
那等于用假数据证明"能区分真假来源"，反而引入新的证据污染。

**这一点建议写进任务书作为禁止项**：不得为满足验证矩阵而合成历史决策。

---

## 4. 关于"只读 ≠ 不可篡改"（同意并补充）

Owner 指出只读位不是密码学保护，需记录 SHA-256 并在后续验收时校验。同意。补充两点：

1. **仅对 `*.pdf.txt` 设只读不够**：`04_V3_INPUT/*.manifest.json` 也是证据来源，
   而且是**比我更权威的那一份**（我终于按它自述的 `source_file` 绑定才做对重放）。
   建议一并纳入冻结范围。
2. **建议在冻结清单里记录"绑定关系"**而非仅文件哈希：

```json
{"subject":"数学",
 "manifest":"04_V3_INPUT/数学.manifest.json", "manifest_sha256":"…",
 "declared_source_file":"…/reslice-batch-C/会考/数学/…md",
 "declared_source_sha256":"934dec78…", "source_sha256_actual":"934dec78…",
 "declared_matches_actual": true,
 "pdf":"01_INPUT_PDF/…pdf", "pdf_sha256":"3b87f19f…",
 "md_02_sha256":"934dec78…", "md_03_sha256":"934dec78…"}
```

理由：**哈希只证明文件没变，不证明"哪个文件配哪个 manifest"**。
我上一轮就因为配错 MD 得到 138 条假不一致——这类错误的唯一防线就是记录绑定关系。

---

## 5. 本轮结论

- **Owner 的收紧成立**：Phase 1 的 57 个无 leaf 单元**从未执行 Gate、无原始决策**；
  把它们显示为重放算出的 `rejected` 同样是伪造。DSH 原建议**撤回**。
- **建议字段**（采纳 Owner 方案，补两个）：

```text
leaf_present            bool     结构事实
candidate_present       bool     结构事实（本路径恒 false；正式链会 true）
gate_decision_raw       dict|null 原始管线决策；null = 无（不得用重放填充）
gate_replay_decision    str|null  独立重放结果；null = 未重放
gate_replay_status      str       ok | not_run | failed
reason_display          str       展示文案，非证据
gate_reasons            list      管线原因（保持原样）
```

- **建议把六情形验证拆成 A（Phase 1，可执行 2 项）/ B（正式链，另立项 4 项）**，
  并**明令禁止为满足验证矩阵而合成历史决策**。
- 状态描述维持 Owner 版本不变；**Resolver 未动、九科 E2E 不宣布通过**。

---

## 6. 本轮产物

| 文件 | 内容 |
|------|------|
| `Docs/60_REPORTS/FROZEN-BASELINE-REVIEW.md` | 上一轮冻结基线复核 |
| `_prove_frozen_vs_replay.py` | 冻结导出 ↔ 独立重放逐字段比对 |
| （本轮核查为代码阅读 + grep，未新增脚本） | |
