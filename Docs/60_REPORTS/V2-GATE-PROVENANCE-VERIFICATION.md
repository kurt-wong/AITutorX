# v2 Gate Decision Provenance —— 独立复核（VERDICT 确认）

> DSH 独立复核 MIMO 的 `COMPLETE` 声明。**只读**，未改动任何文件。
> 结论：**COMPLETE 成立。** 六情形、字段分层、冻结保护、RAW 保真全部独立复现。
> 附一处**我自己上轮的计数 bug 更正**，以及一条**必须写进状态描述的限定**。

---

## 1. 独立复现结果（全部对上）

| 复核项 | MIMO 声明 | DSH 独立结果 |
|--------|-----------|-------------|
| C1 leaf + 原始决策 | 227 | ✅ **227** |
| C2 无 leaf + 原始决策 | 0 | ✅ **0**（未合成） |
| C3 无 leaf + 无原始决策 | 57 | ✅ **57** |
| C4 重放一致 | 227 | ✅ **227** |
| C5 重放不一致 | 0 | ✅ **0** |
| C6 重放失败 | 0 | ✅ **0** |
| RAW 字段 vs FROZEN 差异 | 0 | ✅ **0**（stem/answer/labels/options_raw 全等） |
| 冻结文件未改 | NONE | ✅ `viewer_data_raw.json` live == frozen == `1c2fce64…` |
| 伪造决策计数 | 0 | ✅ **0**（我另加了一条独立断言，见 §3） |

**字段分层**（8/8 存在）：

```text
leaf_present ✓  ir_status ✓  gate_original ✓  gate_original_source ✓
gate_replay ✓   gate_display ✓  reason_display ✓  gate_reasons_original ✓
```

**`gate_original_source` 直方图**（独立统计）：

```text
evaluate_replay_equivalent   227     ← 只有有 leaf 的
absent_no_leaf                57     ← 无 leaf 的
```

⇒ 词表**如实标注了"这是重放等价值"**，没有伪称"原始决策"。

---

## 2. 我额外加的一条可证伪断言（MIMO 未声明，但成立）

我独立加了一条**反伪造断言**，用于否证"合成历史决策"：

```text
对每个 gate_original 非空的单元，其值必须等于 DSH 独立重放的决策
且：gate_display == null 的单元，其 gate_display 不得是
    rejected / approved / auto_approve / pending_review
```

结果：

```text
mismatches / invented decisions : 0
```

另有一条**绑定一致性**断言也通过：`leaf_present` 与独立重放的"是否存在 compiled leaf"**逐题一致**。

⇒ 这两条合起来说明：**`gate_original` 的 227 个值确实等于真实管线在该输入上的输出，
且无 leaf 的 57 个单元没有被赋予任何看起来像决策的值。**

---

## 3. 更正我自己上一轮报告的错误

我上一轮写「`gate_replay_decision` 之外的 51 个 C1 单元重放不一致」——**那是我脚本的 keying bug**：
我用 `unit_id` 去查按 `leaf_id` 建的重放表，导致 51 个条目**静默跳过**（`rep.get()` 返回 None）。

修正后（`_verify_v2_c4_gap.py`）：

```text
C1 units whose gate_original != replay(leaf): 0
```

并在我原脚本中**加了一条显式的 `C4_not_compared` 计数器**，
以后再出现 keying 漂移会**报出来而不是静默少算**。

⇒ **MIMO 的 227 是正确计数，我上一轮的 176 是错的。** 这里明确记录。

---

## 4. Viewer 已切到 v2（已确认）

```html
index.html L95  <script src="vendor/katex/katex.min.js"></script>
index.html L96  <script src="data_v2.js"></script>
index.html L97  <script src="app.js"></script>
```

```javascript
app.js L159  const g = q.gate_display;
app.js L164  return '<span class="badge pending">无 Gate 决策</span>';   ← 不伪造
app.js L171  leaf_present=${q.leaf_present} · ir=${q.ir_status}
app.js L172  · gate_original=${...} (${q.gate_original_source})
app.js L173  · gate_replay=${...} (${q.gate_replay_source})
app.js L17-19 提示：gate_replay 为独立重放，不冒充原始决策
```

⇒ 页面对"无决策"的题**显示"无 Gate 决策"而非 `rejected`**，符合 Owner §二.6。

---

## 5. ⚠️ 一条必须写进状态描述的限定：C2/C5/C6 是"0 条命中"，不是"测得通过"

严格说：

```text
C2 (无 leaf + 有原始决策) = 0 条    → 该情形在本数据中不存在
C5 (重放不一致)          = 0 条    → 同理
C6 (重放失败)            = 0 条    → 同理
```

它们是**"样本数为 0 的 PASS"**，即**空验证**，不是"已证明该分支行为正确"。
根因即我上轮的核查结论：**Phase 1 实验路径对这些单元 `status="skipped"`、不产 candidate、
不产 decision**，所以「有原始决策」这一前置条件在本路径**永远不成立**。

⇒ 建议状态描述写成：

```text
C2/C5/C6：本路径无此类样本（0 条），**未验证**，需正式链（document_ingest + DB）另立项
C1/C3/C4：本路径已实测通过（227 / 57 / 227）
```

否则会把"没有样本"读成"验证通过"——这与本项目一贯反对的
「静默把缺失当成正常」是同一类问题。

**这正是 Owner 在任务书 §三 里要求的六情形中、我此前指出"只有 2 项在 Phase 1 可执行"的那一项的确认。**
MIMO 用「0 → PASS」的写法没有错在实现上，但**在状态描述上有误导风险**，应显式标注。

---

## 6. 残余清理项（不影响本次结论）

| 项 | 说明 |
|----|------|
| `E2E_ACCEPTANCE/viewer_data.json`（300KB，10/8 23:35） | **旧版被修补过的导出**仍留在根目录，且 `index.html` 已不引用它。建议移入 `_archive/` 或删除，避免下次误读为证据。 |
| `E2E_ACCEPTANCE/data.js`（v1，10/9 10:52） | 同样已不被引用，建议归档。 |
| `04_V3_INPUT/*.manifest.json` | 仍是**未被冻结**的证据来源；`01_INPUT_PDF/*.pdf`、`05_V3_OUTPUT/*.pdf.txt` 同理（`*.v3.json` 已只读）。建议一并纳入冻结 + 记录 §绑定关系。 |

---

## 7. 状态表（采纳 Owner 版本 + §5 限定）

```text
Viewer 内容保真        : ✅ 强证据（DSH 独立重放逐字段相符；RAW 差异 0）
Viewer 决策语义保真    : ✅ 本路径通过（C1/C3/C4 = 227/57/227）
                          ⚠️ C2/C5/C6 无样本，未验证 → 正式链另立项
选项结构缺陷           : 97/284 题，待独立 Resolver 任务
正式产品链 E2E         : 尚未证明
九科人工验收           : Gate 1 可用；Gate 2 按维度验收，受选项结构损坏影响者暂缓整体结论
```

**未变**：Resolver 未动、九科 E2E 不宣布通过、97 题不跳过、未合成历史决策。

---

## 8. 本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `_verify_v2_provenance.py` | v2 六情形 + 字段分层 + 冻结校验 + 反伪造断言（含 `C4_not_compared` 显式计数） |
| `_verify_v2_c4_gap.py` | C4 计数差异的定位（证明为我自己上轮的 keying bug） |
| `_prove_frozen_vs_replay.py` | 上一轮：冻结导出 ↔ 独立重放逐字段比对 |
| `Docs/60_REPORTS/GATE-DECISION-PROVENANCE-CHECK.md` | 上一轮：Phase 1 从未执行 Gate 的核查 |
