# Viewer（RAW 重导出 + KaTeX）审查 —— 以及它暴露出的 260 处系统性缺陷

> DSH 独立复核。**只读**，未改动任何文件。
> 结论：**MIMO 这轮的修复是真的、数据已忠实恢复**；但恢复后暴露一个**远大于已知两例的系统性缺陷**，
> 因此 **Gate 2 现在还不能用于人工验收**。

---

## 0. 先说你的直觉：**你的感觉是对的，而且比你预期的更严重**

你看到"好像没什么问题"，是因为**上一轮的修补把缺陷盖住了**。这一轮把 RAW 恢复之后，
页面会**大规模显示成"选项只有字母、没有内容"**——那不是页面坏了，是**数据本来就是坏的**，
以前被 `_improve_options.py` 回读 MD 补好了，所以看起来正常。

---

## 1. MIMO 这轮做对的部分（已独立验证为真）

| 项 | 独立验证结果 |
|----|-------------|
| ① RAW 重导出 | ✅ `viewer_data_raw.json` 861KB，**恢复为管线原值** |
| 原始值字段 | ✅ 新增 `stem_raw` / `answer_raw` / `material_raw` / `options_raw[].text_raw` / `raw` |
| **哨兵 S3** | ✅ `化学 Q20` = **5 options，E='还原反应'**；`数学 Q4` option D `text_raw='D'` |
| `answer_text[:300]` 截断 | ✅ **已移除**，`answer_raw` 为全文（8 处假"未闭合 `$`"根因消除） |
| S1 | ✅ 我独立复算：`data.js` 与 `viewer_data_raw.json` 的 questions **完全一致** |
| KaTeX | ✅ 本地 `vendor/katex/`（`katex.min.js` 272KB + `katex.min.css` + **60 个字体**），**无 CDN** |
| 两段式渲染 | ✅ `renderRich()` 命中 `<div|img|table|span|p>` 时切分，HTML 片段原样、文本节点再过 math |
| 图片不替换 | ✅ HTML 片段直接 `innerHTML` 注入，未做文本替换 |
| 失败可见 | ✅ 未闭合 `$` → `throw` → `[RENDER_FAILED]` + `raw: <源码>` |
| app.js 写入面 | ✅ 只读 `D`，无写盘调用 |
| 渲染不写数据 | ✅ 渲染路径不触碰 `viewer_data_raw.json` / `data.js` |

**关于你问的 `index.html`**：接线是正确的——

```html
L8   <link rel="stylesheet" href="vendor/katex/katex.min.css"/>
L9   <link rel="stylesheet" href="style.css"/>
L103 <script src="vendor/katex/katex.min.js"></script>
L104 <script src="data.js"></script>
L105 <script src="app.js"></script>
```

全部**相对路径、本地文件、无外部请求**。页面本身没有问题。

---

## 2. 🔴 但 RAW 恢复后暴露：**260 个选项（35%）是空壳**

独立实测（`_audit_option_span_defect.py`，全部 9 卷 284 题）：

```text
总 options_raw                        724
text_raw == 仅标签（无内容）            260   (36%)
text_raw 吞掉 >=2 个标签（含兄弟选项）    121
```

**受影响题目：97 / 284（34%）**，各卷分布：

| 卷 | 空壳选项数 | 被吞并选项数 | 受影响题数 |
|----|-----------|-------------|-----------|
| 数学 | 74 | 26 | 25 |
| 地理 | 45 | 23 | 17 |
| 生物 | 36 | 16 | 13 |
| 政治 | 32 | 16 | 12 |
| 历史 | 27 | 9 | 9 |
| 物理 | 19 | 13 | 8 |
| 化学 | 18 | 13 | 8 |
| 英语 | 9 | 5 | 5 |
| 语文 | 0 | 0 | 0（无选择题） |

**每一卷的「空壳数」与「吞并数」在题级上完全对应**（`with_bare == with_swallow`，逐卷相等）——
说明这是**同一个缺陷**：**整行被第一个选项吞掉，其余选项变成裸字母**。

### 2.1 典型形态（数学 Q1，manifest 声明 4 个选项）

```text
A: 'A. 1 B. 2 C.  $ \pi $ D.  $ 2\pi $'    ← A 吞掉整行
B: 'B'                                        ← 空
C: 'C'                                        ← 空
D: 'D'                                        ← 空
```

数学 Q2 / Q5 / Q7 亦然（`A. 800 B. 900 C. 1000 D. 1100` → A 全吞、B/C/D 空）。
化学 Q7 亦同（`A. KCl 溶液 B. $C_2H_5OH$ 溶液 …` → A 全吞）。

---

## 3. 根因：**Resolver 的单行多选项分支永远走不到**

我**直接重放管线（完全不经过 Viewer）**，结论相同（`_audit_option_span_cause.py`）：
⇒ **缺陷在上游 V3 Resolver，不在 Viewer。** Viewer 是忠实呈现。

manifest 声明：

```json
{"unit_id":"Q1","options_lines":[9,9],
 "options":[{"label":"A","start_line":9,"end_line":9},
            {"label":"B","start_line":9,"end_line":9},
            {"label":"C","start_line":9,"end_line":9},
            {"label":"D","start_line":9,"end_line":9}]}
```

`resolver.py::_locate_options`（L588–611）：

```python
for lab in labels:
    starts = [
        l for l in self._idx.lines
        if l.seq > cursor_seq
        and (lab in option_tokens(normalize_text(l.text), (lab,)))   # ← 该行含此标签
    ]
    if len(starts) == 1:
        found[lab] = ("ok", starts[0].line_ref)      # ← 命中！整行 span
        ...
        continue
    ...
    # 无行首选项：尝试在前一个选项行上 bounded inline   ← 设计意图所在
    if cursor_ref is not None:
        offs = [o for o in _label_offsets(line.text, lab) if o >= cursor_end]
        if len(offs) == 1:
            found[lab] = ("inline", cursor_ref, offs[0], offs[0] + len(lab))
```

**问题**：对 `A. x B. y C. z D. w` 这一行，

- 查 A → 行内含 A → `len(starts)==1` → 命中**整行 span**
- 查 B → **同一行也含 B** → 再次 `len(starts)==1` → 命中**同一整行**
- 查 C、D 同理

⇒ **`starts` 分支总是先命中，`inline`（按字符 offset 切分）分支永远不会执行**。
每个 label 都拿到**整行**，但 `CompiledRole.text` 只按**行 span** 取文，
所以只有 A 的文本是"整行"，B/C/D **落在行内却没有字符区间 → 文本退化为标签本身**。

**这是设计意图与分支顺序的矛盾，不是数据问题**：注释明写"单行多选项"应由 inline 处理，
但 inline 只在"行内找不到该标签"时才跑——而单行多选项恰恰"行内找得到"。

**受影响面**：任何把多个选项放在同一物理行的题目。本语料里就是**绝大多数选择题**。

---

## 4. 这对验收意味着什么（重要）

| | 现状 |
|--|------|
| Gate 1（PDF↔MD 对照） | ✅ 可用 |
| Gate 2（逐题看 Question） | ⚠️ **对 97/284 题（34%）不可用**——选项 A 是全行乱码、B/C/D 空 |

**结论**：现在开始人工验收，你会在 Gate 2 里看到大量"选项只有字母"的卡片，
**无法判断题本身对不对**。所以**不能按当前状态开始 Gate 2 验收**。

**但请注意**：这**不是** Viewer 的缺陷，是 Viewer **终于如实呈现了 V3 的真实缺陷**。
从这个角度说，这一轮 Viewer 修复**达到了目的**——它让一个被修补掩盖的系统性缺陷第一次可见。

---

## 5. 两个次要但需要记录的点

1. **Gate 1 差异**显示仍被切片**（与"全文"声称不符的部分）：

   ```javascript
   app.js:171-172  esc(p.slice(0, 800)) / esc(m.slice(0, 800))   ← 锚点并排
   app.js:192-193  esc(r.x.slice(0, 120))                        ← 行级差异
   ```

   数据侧确已是全文（`pdf_text_len=10231 / md_text_len=19228`，`pdf_text`/`md_text` 字段存在），
   但这三处**展示**仍截断。数学 PDF 锚点 10,231 字 → 只显示 800 字（7.8%）。
   建议：锚点差异**按差异行高亮**而不是首 800 字，或加"展开全文"。

2. **`gate1_anchors` 字段为空**（我实测 `math gate1_anchors present: 0`）。
   页面上的"题号锚点"是 `app.js` 现算的，不是导出字段——可用，但不便于复核与回归。

---

## 6. 建议下一步（仍未到"人工验收"）

```text
① 先修 V3 Resolver 的单行多选项分支（这是 260 处缺陷的根因）
   —— 但这是**生产逻辑**，需要独立立项与授权，不在 Viewer 任务内
①b 或：先在 Viewer 上加一个"选项完整性"标记（只读、不改数据），
   把 97 题标出来，避免人工验收时逐题卡住
② 然后再开始 Gate 1 → Gate 2 人工验收
```

**我倾向 ①b 先行**：它不需要碰生产代码，就能让你在 Gate 2 里**跳过已知缺陷题**、
把有限的人工时间用在"缺陷未知"的题目上。这也符合"先看见、再修"的顺序。

---

## 7. 本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `_audit_viewer_v3.py` | S1/哨兵/字段形态/截断的独立复核 |
| `_audit_option_span_defect.py` | 260 处空壳 + 121 处吞并的量化与分布 |
| `_audit_option_span_cause.py` | 不经过 Viewer 的直接重放，确认缺陷在 Resolver |
| `Docs/60_REPORTS/VIEWER-FORMULA-RENDERING-INSTRUCTION-RECORD.md` | 上一轮指令记录 |

**未改动任何文件。** `ec62d29` / `d42cde6` 保持冻结。
