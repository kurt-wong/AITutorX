# 冻结基线复核 —— 最强可证明性 + 一处 Gate 标签保真缺口

> DSH 独立复核。**只读**，未改动任何文件。
> 对象：`E2E_ACCEPTANCE/FROZEN_EVIDENCE/`（SHA `1c2fce64…`）+ 分维度 Viewer。
> 结论：**管线内容完全忠实（这是本轮最强的证明）；但 Gate 标签在 54 个单元上与真实 Gate Policy 不一致。**

---

## 1. 冻结与只读位：已确认

```text
FROZEN_EVIDENCE/viewer_data_raw.json   1,006,769 B   readonly=True   sha 1c2fce64…
FROZEN_EVIDENCE/data.js                1,006,790 B   readonly=True
FROZEN_EVIDENCE/FROZEN_BASELINE_SHA256.json             readonly=True

05_V3_OUTPUT/*.v3.json   18 个文件全部 readonly=True
05_V3_OUTPUT/*.pdf.txt   未设只读（不影响，见 §4）
```

**活文件与冻结副本哈希一致**：`viewer_data_raw.json` 活副本 = 冻结副本 = `1c2fce64e2e580258e7c6c70a1aeca40ee66eb18f1bf4035ae5fb9ad1c1a0835`。✅

**脚本时间戳**：最后一个数据写脚本是 `export_raw_full.py`（10:15:29）；之后是
`freeze_and_mark.py`（10:50:51）与 `_build_dims_viewer.py`（10:52:37）。
⇒ **冻结后未重跑导出脚本**。✅（文件从 861KB 增至 1,006KB，见 §2 已解释）

---

## 2. 最强可证明性：`frozen` ↔ 独立重放逐字段比对

这是我上一轮承诺的那件事（`_prove_frozen_vs_replay.py`）。方法：**不信任导出脚本**，
直接用 `04_V3_INPUT/*.manifest.json` + **manifest 自己声明的 `source_file`**
（并校验 `source_content_sha256`）重跑 `Resolver → IR → Compiler → GatePolicy`，
逐题逐字段比对。

### 2.1 结果

```text
subjects compared          9 / 9
题目总体                    frozen 284  ↔  replay 284   （逐卷完全一致：30/22/40/18/10/36/25/53/50）
有 compiled leaf 的实体      230  →  逐字段比对
字段不一致                  108 处，只有两类：
     MISSING_IN_REPLAY  54
     gate               54
```

**关键结论：**

| 类别 | 结果 |
|------|------|
| `stem_raw` | ✅ **全部一致** |
| `options_raw[].text_raw` | ✅ **全部一致** |
| `options_raw[].label` / `.span_id` / `.line_refs` | ✅ **全部一致** |
| `answer_raw` / `answer_letter` | ✅ **全部一致** |
| `labels` / `qtype` / `verify` | ✅ **全部一致** |
| 选项数量 | ✅ **逐题一致** |
| **`gate`** | ❌ **54 处不一致**（见 §3） |

⇒ **文件从 861KB 增至 1,006KB，是"加字段"而非"改原值"** —— 因为所有管线内容字段与独立重放逐字相符。
⇒ 这也**强于 S1**：S1 只证内部一致，本比对证明**导出内容 = 管线真实产物**。

> 附带纠正我自己的一个过程错误：第一次比对用了 `02_PREPROCESSING_OUTPUT` 的 MD，
> 而 manifest 指向 `e2e_run/phase1_1_corpus_optspans/reslice-batch-C/` 下的 MD。
> 两者 SHA 相同（内容一致），但按 manifest 自述绑定后才是正确方法。重放已修正。

---

## 3. ❌ 发现的保真缺口：54 个单元的 `gate` 标签不是管线值

### 3.1 现象

```text
frozen gate='incomplete'   ↔   replay（真实 Gate Policy）='rejected'
```

分布：化学 25 + 生物 21 + 政治 7 + 英语 3 + 物理 1 = 57 个无 leaf 单元中的 **54 个**。

### 3.2 根因（`export_raw_full.py` L46–58）

```python
for root in ir.units:
    leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
    for leaf in leaves:
        cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
        if cl is None:
            questions.append({
                "unit_id": root.unit_id, "leaf_id": leaf.unit_id,
                "raw": True, "gate": "incomplete",              # ← 硬编码
                "reason": "IR incomplete / leaf absent",        # ← 硬编码
                ... })
            continue
        ...
        gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)   # ← 只有有 leaf 才真跑
```

**即：导出脚本对"无 compiled leaf"的单元，用字面量 `"incomplete"` 代替了 Gate Policy 输出。**

而**真实 Gate Policy 对这些 root 会返回 `rejected`**——因为 `policy.py::evaluate` 第一层就判：

```python
if root.semantic_status != "ready":
    structural_reasons.append(f"unit {root.unit_id!r} semantic_status={root.semantic_status} (not ready)")
...
if not (structural_pass and provenance_pass and semantic_pass):
    decision = "rejected"
```

本语料里恰好 **IR incomplete = 57**（root 作用域），与这批单元重合。

### 3.3 为什么这值得修

| | 影响 |
|--|------|
| 目视影响 | Gate 2 里这 54 个单元显示 `incomplete` 徽章，**看起来像"尚未处理"**，而真实 Gate 判它是 **`rejected`（终态，`approve()` 必拒）** |
| 语义影响 | `incomplete` 是**导出脚本的词汇**，不是 `decision_status` 的合法值域（`pending_review/approved/rejected`）——**把两种不同状态混为一谈** |
| 与已修问题同类 | 这与"选项文本被修补"属**同一类保真问题**：显示层替管线做了判断 |

这与我们此前反复确认的口径直接相关：**`rejected=5` 是 leaf 作用域、root 作用域是 62**。
导出脚本这一硬编码，恰好让 **root 作用域的 rejected 在 Viewer 里全部消失**（显示成 incomplete）。

### 3.4 修法（很小，且不碰生产代码）

```python
if cl is None:
    gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)   # 照常跑
    decision = gd.get("decision")          # -> "rejected"
    greasons = (gd.get("reasons") or [])[:5]
    gate = decision
    # 若要保留"无 leaf"这一信息，另加字段：
    #   leaf_present: False
    #   reason_display: "no compiled leaf (semantic_status=incomplete)"
```

**要点**：`gate` 必须是管线值；"无 leaf"应作为**额外字段**表达，不得覆盖 `gate`。

---

## 4. 关于 `reason` 字段（提醒后续比对者）

我第一轮比对出现 297 处不一致，**全部来自 `reason`**：

```text
frozen : "answer_not_expressible (answer-side / S0 family) — data may still be correct"
replay : "leaf 'Q1' answer grammar: answer not expressible as canonical value"
```

`reason` 是**导出脚本拼的展示文案**，不是管线值；**管线值是 `gate_reasons`**（我在比对中单独校验，全部一致）。
⇒ 建议把该字段更名为 `reason_display`，并**同时导出 `gate_reasons`**（现已导出），
避免以后把它当作管线结论引用。

---

## 5. 其余核查

| 项 | 结果 |
|----|------|
| 分维度反馈（题干/选项/答案/LaTeX/整体） | ✅ 未跳过 97 题；答案维度标"暂不可判"，与我的修正一致 |
| 选项异常题数 284 / 97 | ✅ 与我口径一致 |
| Gate1 全文 + 题号锚定 + 检索 | ✅ 已实现（`pdf_text`/`md_text` 为全量字段） |
| Resolver/Producer/Gate/Schema/P1.4-B | ✅ 未改（时间戳与 git 未显示生产树被动） |
| `05_V3_OUTPUT/*.pdf.txt` 未设只读 | ⚠️ 建议一并设只读——它们是 Gate 1 的证据来源 |

---

## 6. 结论与建议

**可以按你已批准的只读口径继续，但有两处应先落**（都不碰生产代码）：

1. **修 `gate` 硬编码**（§3.4）——这是唯一实质性保真缺口，且会误导 Gate 2 徽章。
   修完后 `root 作用域 rejected` 才第一次在 Viewer 里如实出现（≈62，而非 0）。
2. **`reason` → `reason_display` 更名**（§4），并把 `05_V3_OUTPUT/*.pdf.txt` 一并设只读（§5）。

**关于"可证明上限"的更新**：本比对把上限从"S1 内部一致"提升为
**"导出内容 = 独立重放的管线产物（除 `gate` 标签外逐字段相符）"**。
你此前写的"更强证据 = viewer_data_raw.json ↔ DSH 独立重放"——**已完成**，
并且结论是**内容忠实、标签有一处缺口**。

**未变**：Resolver 未动、九科 E2E 不宣布通过、97 题不跳过。
Resolver 最小断言仍应为内容区间（`A='1' B='2' C='\pi' D='2\pi'`），不是空壳计数。

---

## 7. 本轮产物（全部只读，写在你仓内）

| 文件 | 内容 |
|------|------|
| `_prove_frozen_vs_replay.py` | 冻结导出 ↔ 独立重放逐字段比对（最强的可证明性证据） |
| `_check_manifest_source_binding.py` | manifest `source_file` 与其声明 SHA 的绑定核查 |
| `_audit_option_span_defect.py` | 260 空壳 / 121 吞并的量化（上轮产物，仍有效） |
| `_audit_option_span_cause.py` | 不经 Viewer 的直接重放（确认缺陷在 Resolver） |
