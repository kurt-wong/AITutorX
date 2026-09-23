# OD-01 Frozen Spec Change Proposal — DSH 定向对抗性复核

```text
STATUS: INDEPENDENT ADVERSARIAL REVIEW — COMPLETE
SCOPE: OD-01 ONLY（Frozen Resolved Span / P04 Option Provenance）
REVIEWER: DSH（独立复核方）
SUBJECT-A: Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md §OD-01（D1）
SUBJECT-B: Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md（D4）
SUBJECT-C: Docs/COORDINATION/IMPLEMENTATION-PLAN-v0.3.md 与
           Docs/COORDINATION/LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md 的 OD-01 条款
REPO-OF-SUBJECT: D:\Project\AITutors-v3（HEAD 506ffa8，ahead origin/main 3，未 push）
REPORT-REPO: D:\Project\AITutor-X
VERDICT: VERIFIED WITH FINDINGS
CLOSURE BLOCKING: NO
RECOMMENDATION: OWNER ACTION REQUIRED BEFORE CLOSURE
FINDINGS REGISTERED: 8（未修复）
```

> 本报告**不**评审 OD-02 / OD-03 / OD-04 / OD-05 / G-01 / G-02 的实体内容（越界即违规）。
> 本报告**不**修改 Frozen Spec / Frozen Contract / 生产代码 / schema / corpus / D1–D5 原文。
> 本报告**不**进入 Phase 1，**不**做 migration，**不**执行 re-freeze。

---

## 0. 复核边界与判定口径

### 0.1 本次只回答九个问题

| # | 对抗性问题 | 结论 |
|---|---|---|
| Q1 | D4 是否**真实地**未生效（Frozen Spec 逐字节未变）？ | **是（已证实）** |
| Q2 | D4 §1/§2.1「Current Frozen Semantics」是否与 Frozen Spec / Frozen Contract 原文相符？ | **部分不符（F-OD01-01、F-OD01-08）** |
| Q3 | D4 的变更集是否完整到可据以 re-freeze？ | **不完整（F-OD01-02）** |
| Q4 | OD-01 的「禁 V3 rediscovery」与现行 Frozen Spec 是否自洽？ | **不自洽且未处置（F-OD01-03）** |
| Q5 | 新增 Producer `options[].provenance` 与既有 IR option span 的权威关系是否定义？ | **未定义（F-OD01-04）** |
| Q6 | fail-closed 表征是否已钉死并可被 Owner 批准？ | **未钉死（F-OD01-05）** |
| Q7 | 语料实测要求的最小原语集是否被 OD-01 完整覆盖？ | **有缺口（F-OD01-06）** |
| Q8 | L0 修改路径是否符合仓库自身冻结的元规范？ | **不符合（F-OD01-07）** |
| Q9 | 本轮是否已把 OD-01 当作生效 Frozen Spec，或有越权实施？ | **否（已证实）** |

### 0.2 证据标签

- **DIRECTLY VERIFIED**：本沙箱内实测命令/实读文件所得。
- **SOURCE-LEVEL VERIFIED**：引用原文逐字核对所得（含 file:line）。
- **VERIFIED BUT NOT REPRODUCED**：原件声称可核实但本环境无法复跑。
- **NOT VERIFIED**：无法证实（含证据缺口）。

---

## 1. Git / 隔离事实（Q1、Q9）

### 1.1 三笔分离与未 push 声明 —— DIRECTLY VERIFIED

```text
D:\Project\AITutors-v3  HEAD = 506ffa81e5639333ba2bfae61fb8d9d09c2e9aca
  main...origin/main [ahead 3]
  506ffa8  docs(governance): add OD-01 frozen spec change proposal (not effective)   1 file, +316
  ee6d915  docs(governance): register limited implementation authorization (G-01)    1 file, +361
  c55797f  docs(governance): record OD-01~05/G-01/G-02 and reconcile implementation plan  3 files, +1229
```

- 三笔确实分离：Owner Decision+Plan / Limited Auth / OD-01 Proposal 各自独立提交，**未混提**。
- `origin/main..HEAD` 仅触及 **5 个文件**，全部位于 `Docs/COORDINATION/**`：

```text
Docs/COORDINATION/FROZEN-SPEC-CHANGE-PROPOSAL-OD-01-OPTION-PROVENANCE.md
Docs/COORDINATION/G-02-FREEZE-REGISTRATION-VERIFICATION.md
Docs/COORDINATION/IMPLEMENTATION-PLAN-v0.3.md
Docs/COORDINATION/LIMITED-IMPLEMENTATION-AUTHORIZATION-v0.3.md
Docs/COORDINATION/OWNER-DECISIONS-OD-01-OD-05-G-01-G-02.md
```

- **未 push 声明成立**（ahead 3）。本报告**未** push v3。

### 1.2 Frozen Spec 逐字节未变 —— DIRECTLY VERIFIED

```text
git rev-parse <rev>:Docs/V3_SPEC
  b743c5d -> b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
  7934844 -> b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
  3e2f9bb -> b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
  HEAD    -> b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f
git rev-parse HEAD:Docs/V3_SPEC        ✅ 与 D4 文首 line 14 声明值一致
git diff --name-only origin/main..HEAD -- Docs/V3_SPEC   → 空
git log --oneline -- Docs/V3_SPEC      → 最近一次内容提交 = f708370（远早于本轮）
```

D4 line 14 声称「当前生效 Frozen Spec 仍为 `Docs/V3_SPEC/**` @ tree
`b3eeb3e9a600347f18eae4e1becc1ec4fa4b6b4f`（unchanged）」—— **逐字成立**。

### 1.3 「未生效」表述一致性 —— SOURCE-LEVEL VERIFIED

| 位置 | 原文要点 | 是否把 OD-01 当已生效 |
|---|---|---|
| D1 line 14 | OD-01 = APPROVED DESIGN DECISION / PENDING FROZEN SPEC INCORPORATION | 否 |
| D1 line 22 | APPROVED — Frozen Spec Change Proposal pending；未 re-freeze 前不生效 | 否 |
| D1 line 72 | 「不是已经生效的 Frozen Spec」 | 否 |
| D1 line 280 | OD-01 \| Design approved；Frozen Spec incorporation pending | 否 |
| D4 line 4-14 | STATUS: PROPOSAL / NOT YET EFFECTIVE / RE-FREEZE: NOT DONE | 否 |
| D4 line 277-284 | OD-01 = APPROVED DESIGN DECISION；NOT EFFECTIVE AS FROZEN SPEC | 否 |
| D4 line 304 | 「本文件不直接编辑 `Docs/V3_SPEC/**`」 | 否 |
| D2 line 67 | APPROVED design / PENDING；re-freeze 前不得实施 Resolved Span 扩展 | 否 |
| D2 line 462 | Phase 1 Entry 含「OD-01 Proposal 完成 Owner review / re-freeze」 | 否 |
| D2 line 464 | Forbidden 含「在 re-freeze 前实施 OD-01 Resolved Span 扩展」 | 否 |
| D3 line 187 | Resolved Span ontology 扩展 — **pending re-freeze** | 否 |
| D3 line 227 | Phase 1 在 Owner review + re-freeze 之前不得启动 P04 Resolved Span 相关实现 | 否 |
| D3 line 320 | UNCHANGED (OD-01 change is PROPOSAL only until re-freeze) | 否 |

**未发现任何一处把 OD-01 表述为已生效 Frozen Spec**。全仓 grep `OD-01` 命中处亦无例外。

### 1.4 附带确认（非本报告评审对象，仅记录以免误读）

```text
git rev-list --count b743c5d..7934844 = 1
git rev-list --count 7934844..b743c5d = 0
git diff --stat b743c5d..7934844 = 7 files changed, 29 insertions(+), 21 deletions(-)
```

与 D1 §G-02 / D5 §1-§3 声明**逐字吻合**。另确认 `3e2f9bb`（F-RBC-01 修复）是 `7934844`
的**祖先**（`7934844..3e2f9bb = 0`），本轮治理链未丢失该修复，无历史改写。
`D:\Project\Papers`（= `kurt-wong/Aitutors-preprocessing`）HEAD = `2b92898f…`，与 D5
line 91 / D2 line 35 一致。**G-02 实体内容不在本次评审范围。**

---

## 2. Q2 —— D4「现状」基线与原文的对抗核对

### 2.1 逐行核对结果

| D4 §2.1 / §2.2 断言 | 原文 | 判定 |
|---|---|---|
| Role spans = `stem`/`options`/`answer`/`explanation` | `10 §6.3` role 列 | ✅ 准确 |
| `label` 在 `instance_role_contents.label`（options only） | `10_Data_Model.md:458`「仅 options 用，如 `A`」 | ✅ 准确 |
| `text_hash = SHA256(text.encode("utf-8"))` | `10_Data_Model.md:461` | ✅ 逐字准确 |
| Storage = `instance_role_contents.source_span` JSONB | `10_Data_Model.md:462, 469-471` | ✅ 准确 |
| exact / normalized 解析级联 | `20 §5.2`（`:262-270`） | ✅ 准确 |
| `options` = 整区 role span；per-label = GAP | 契约 `:974`「仅整块 `options_lines` … PREPROCESSING granularity GAP」 | ✅ 准确 |
| P04.2 `options_lines` 必须保留 | 契约 `:295-299` | ✅ 准确 |
| **Primary granularity = Source line / line range** | `20 §5.5`：`granularity ∈ {line, line_character}`（`:322`） | ⚠️ **不完整** |
| **Example keys = `sp-<unit>.option.<label>`（IR 示例中的 role key）** | `20 §6.1` 示例 span_id 实为 `sp-Q1-stem` / `sp-Q1-A` / `sp-Q1-answer` / `sp-M1`（`:312, 367-369`） | ❌ **与原文不符** |

### 2.2 关键遗漏：`granularity {line, line_character}` 与既有的「单行多选项」能力

Frozen Spec `20_Document_Pipeline.md` §5.5（`:308-324`）原文：

```text
"span_id": "sp-Q1-stem", "source_version_id": "<uuid>",
"start_line_ref": "P1L001", "end_line_ref": "P1L002",
"line_refs": ["P1L001", "P1L002"],
"granularity": "line",
"start_offset": null, "end_offset": null,
"text_hash": "<sha256>", "resolution_status": "exact",
...
- `granularity` ∈ {line, line_character}（M1；table_cell/fragment 延后，见 00 §5）。
- line_ref 必须存在于该 source_version；line_character 的 start/end_offset 必须能唯
  一定位"同行多题答案/单行多选项"场景。
```

**即：现行 Frozen Resolved Span 已经含有字符级粒度 `line_character` + `start_offset` /
`end_offset`，且其存在的理由被明文写成「单行多选项」。** D4 §2.1 完全没有记载这一既有
维度，也没有记载 `table_cell` / `fragment` 的**明确延后条款**。

这直接影响 D4 §1 的缺口主张：

| D4 §1 点名缺失的形态 | 实测定性 |
|---|---|
| `multiple_source_spans` | **真缺口** —— `20 §5.5` 的 ResolvedSpan 是单一行区间（`start_line_ref`/`end_line_ref`/`line_refs`），不连续多段无法表达 |
| `table_cell` | **真缺口，但障碍性质不同** —— 它被 `00 §5` 列为**明确非目标（M1 不做）**，不只是「ontology 未定义多态类型」 |
| `char_span_in_line` | **存疑** —— `granularity: line_character` + `start/end_offset` 与其实质能力重合；D4 需说明这是**新增 form** 还是**既有粒度的正式化/别名** |
| `other` | 真缺口（现行无开放 form） |
| （D4 未列入的）`fragment` | `20 §5.5` 延后项之一；D4 五形态未提及 |

### 2.3 遗漏的硬约束：`00 §5` 把 table cell/fragment 字符粒度列为「明确非目标」

`Docs/V3_SPEC/00_Master_Spec.md` §5（`:264-279`）：

```text
## 5. 明确非目标（M1 不做）
...
- 用 JSONB 隐式承载整个业务模型。
...
- 文档级表格 cell/fragment 字符粒度索引（首版只做 line + 必要 inline，见 20；待样本
  证明需要再加回）。
```

两点后果：

1. OD-01 的 `table_cell` 要求**不是**在空白处新增 ontology，而是**废止一条冻结的
   「明确非目标」**。该条目自带解除条件（「待样本证明需要再加回」），因此 re-freeze
   change set 必须显式引用并改写该条，否则 re-freeze 后 Frozen Spec 内部自相矛盾
   （同一能力既是非目标又是强制要求）。
2. 同节还有一条「**用 JSONB 隐式承载整个业务模型**」为非目标。D4 §4.1/§7 把多态
   provenance 放进 `source_span` JSONB，仅在 §13 第 5 项把「是否需正式更新
   `10_Data_Model` 文本」挂给 Owner；**未引用该非目标**，未论证扩展后的 JSONB 与
   「不隐式承载业务模型」红线的边界。

### 2.4 遗漏的硬条款：`20 §7.2` 步 1 只允许 `line / line_character`

`20_Document_Pipeline.md:454`：

```text
1. 逐 content role 从 resolved span（line / line_character）**确定性提取**正文 →
   `compiled_roles[]`，每个带 `text_hash`（= source slice hash，供 10 §8 2c 校验）。
```

新增 `table_cell` / `multiple_source_spans` / `other` 之后，Compiler 的确定性提取规则
必须一并扩展；D4 §9 只说「provenance 进入 compiled source_span」，**未把该条列为受影响
条款**，§14 也未提及。

### 2.5 遗漏的硬条款：`20 §7.3` Question `dedup_key` 含 own options

`20_Document_Pipeline.md:523`：

```text
| Question `dedup_key` | canonical question type + own stem + own options
  （options 按 canonical label order 排序，声明序无关；label 重复 fail-fast） |
  排除 shared material / answer / explanation / image / question no. /
  page / source_version_id / unit_id / occurrence 信息
```

本轮同目录的 P04 根因调查报告已把这一点登记为**待裁影响面**：

```text
P04-OPTION-EVIDENCE-ROOT-CAUSE-INVESTIGATION.md
  :212  「V3 Spec §7.3 的 Question dedup_key = ... own options ... 即 option label 参与
         Question identity。P04 若不定，不仅阻断 ready-IR，也阻断 choice 题的 dedup_key
         计算——影响范围需 Owner 确认」
  :1045 E-32  Question dedup_key 含 own options（OBSERVED，强）
  :1108 U-07  「P04 是否涵盖 dedup_key 阻断面」= 裁决项
  :1138 D-5   「P04 影响面是否含 dedup_key」= Owner 裁决项
```

**D4 全文（316 行）未出现 `dedup_key` / Question identity / label order / label 重复
fail-fast 任何字样。** §4.4 的 Identity 段落只覆盖 `source_content_sha256 ⊥
derived_text_hash`（源身份/派生哈希），§5 变更表只写「Existing role spans / text_hash /
source_content_sha256 \| UNCHANGED」，**均未覆盖 Question 去重身份**。

这是本次复核中最具实质性的遗漏：option label/text 的来源一旦改为 Producer
`options[]`，`dedup_key` 的输入来源即改变，而 Question identity 属 Frozen Spec 语义层。

### 2.6 Q2 结论

D4 §2.1 对**存储/role/text_hash/label 列/解析级联**的描述准确；但对**「Resolved Span
ontology 现状」的核心描述不完整**（漏 `granularity` 枚举与 offset、漏 `20 §5.5` 延后
注、漏 `00 §5` 非目标），且有一条**引用错误**（Example keys）。

---

## 3. Q3 —— 变更集完整性

### 3.1 D1 规定的链路要求「explicit diff」

D1 `:62-70`：

```text
OD-01 明确触发 **Frozen Spec Change Required**。
Owner Decision
  → Frozen Spec Change Proposal（本任务产出 D4）
  → explicit diff
  → Owner review
  → re-freeze
```

D4 §14 自称 `Explicit Diff Preview（illustrative；非生效文本）`，并声明：

> 正式 diff 将在 Owner 指示的 re-freeze change set 中以 track-change / 完整章节替换方式
> 提出；**本文件不直接编辑 `Docs/V3_SPEC/**`**。

**因此链路中的 `explicit diff` 环节在 D4 阶段尚未交付**（仅 `+` 5 行示意）。这本身可以是
有意的分步（Owner 尚未回答 §13 的 7 项），但必须显式登记为「Owner 在批准 §13 前看不到
将被改写的确切文本」。

### 3.2 至少 5 处 L0 条款需要修改/废止，D4 未列

| # | 条款 | 现状 | OD-01 落地后必须 | D4 是否列出 |
|---|---|---|---|---|
| 1 | `00_Master_Spec.md:274-275` | table cell/fragment 字符粒度 = 明确非目标 | 废止/改写该非目标条目 | ❌ |
| 2 | `20_Document_Pipeline.md:322` | `granularity ∈ {line, line_character}`；`table_cell/fragment 延后` | 扩展枚举或新增 form 维度；解除延后注 | ❌ |
| 3 | `20_Document_Pipeline.md:454` | Compiler 只从 `line / line_character` 确定性提取 | 扩展提取规则至新 form | ❌ |
| 4 | `20_Document_Pipeline.md:280` | `option_label` 解析规则 = V3 侧确定 option 边界 | 与「V3 不得 rediscovery」调和（见 §4） | ❌ |
| 5 | `20_Document_Pipeline.md:523` | Question `dedup_key` = type + own stem + own options | 明确 option 来源变更后 dedup 身份是否变化 | ❌ |

D4 §6「Affected Components」按**组件**（Producer prompt / IRBuilder / Gate Provenance /
`InstanceRoleContent.source_span` / Tests）列举，**按条款的改动清单缺失**；§14 target 只写
`20_Document_Pipeline.md`（及必要时 `10_Data_Model.md`），未含 `00_Master_Spec.md`——
而 `00 §5` 恰恰是必须改的文件。

---

## 4. Q4 —— 「禁 V3 rediscovery」与 `20 §5.3` 的未处置冲突

P04（Frozen Contract，CLOSED）原文 `:282`：

> **如果 Canonical V3 IR 对 Choice Question 要求 per-option structure/evidence，则
> AITutors-preprocessing 必须在当前 Preprocessing Contract 中正式产生 per-option
> structured information；AITutors-v3 不负责重新发现或猜测 option structure。**

OD-01 Binding Requirement 7（D1 `:58`）：V3 不得通过 LLM 自行猜测 Option 边界。
D4 §8 把它写成测试要求：「**禁止 V3 rediscovery**（不得从 `options_lines` 自行切 option）」。

现行 Frozen Spec `20 §5.3`（`:280-281`）却规定：

```text
- **option_label**：按 A/B/C/D 顺序；每项到下一标签/下一题结束；重复标签 →
  ambiguous；缺标签 → incomplete。
```

即 **Resolver 在 V3 侧按标签顺序确定每个 option 的边界**——与「V3 不得 rediscovery」
直接抵触。该规则是确定性的（非 LLM），因此 P04「不负责重新发现或猜测」与它
是否相容，必须显式裁决。

D4 §6 / §9 / §14 **未把 `20 §5.3` 列为受影响条款**，也未定义「Producer `options[]`
存在时 `§5.3` 是否被取代 / 降级 / 仅作 fallback」。re-freeze 后 Frozen Spec 将同时含有
「V3 不得重新发现 option 结构」与「Resolver 按 A/B/C/D 顺序定位 option 边界」两条规则。

---

## 5. Q5 —— 双份 option provenance 表征的权威关系未定义

```text
现有（冻结）：20 §6.1 IR 示例（:365-369）
  "content": {
    "stem":    {"source_span": {"span_id": "sp-Q1-stem"}, "status": "resolved"},
    "options": {"A": {"source_span": {"span_id": "sp-Q1-A"}, "status": "resolved"}},
    ...
  }
  → V3 侧已存在 per-label option 的 Resolved Span 表征（由 Resolver 产出）

OD-01 新增（D4 §4.2）：
  options: [{ label, text, provenance: [ {form, ...} ] }]
  → Producer 侧 per-option provenance
```

D4 §4.1 明言「在 Frozen Resolved Span 语义层增加 **provenance form 维度**」，§9 说
Compiler「option leaf text + label 来自 Preprocessing `options[]`；provenance 进入
compiled source_span」。但**未定义**：

1. 当 Producer `options[].provenance` 与 Resolver 由 `§5.3` 得出的
   `content.options[label].source_span` **不一致**时以谁为准；
2. 该不一致是否构成 conflict signal（OD-02 的「双保留、Source-derived 权威」精神
   在 Producer↔Resolver 之间的对应形态）；
3. 二者是否共享同一 span，是否触发既有 **no double consumption** 校验
   （D4 §2.2 自述该不变式保持不变）、以及两个表征同时消费同一源区是否双双被拒；
4. `text_hash`（`10 §8` 2c/2d）与 `10 §8` 2b 的 offset 子不变量在新 form 下如何核验。

OD-04 明确「禁止保留第二条具有独立 semantic authority 的正式 ingestion path」。
两份 option provenance 表征并存而无优先级/冲突规则，是本 Proposal 需要显式对齐 OD-04 的
点，而 D4 §9 的 Authority 行只写「不建立新 Authority」，未触及该内部二义性。

---

## 6. Q6 —— fail-closed 表征未钉死

| 出处 | 表述 |
|---|---|
| P04.4（契约 `:309`） | 必须显式表示 `unresolved` / `INCOMPLETE` / `QC_FAIL`（**具体状态按最终 Contract 定义**） |
| D1 `:57` | 必须进入 explicit `unresolved` / `QC_FAIL` / `INCOMPLETE` |
| D4 §4.1 `:109` | 「不可靠时整体 `unresolved`，不得 0-span 静默通过」 |
| D4 §4.2 `:125` | 「或整体：`options_unresolved: true`」 |
| D4 §4.3 `:133` | 「**不可靠 → fail closed**：`unresolved` / `INCOMPLETE` / `QC_FAIL`」 |

问题：

1. **两套机制并存且未定名**：`unresolved`（§4.1/§4.3）与 `options_unresolved: true`
   （§4.2）关系不明——是同一状态的不同书写，还是两个字段？
2. **`0..n` 与「不得 0-span 静默通过」并存**：§4.1 允许 provenance 为「**0..n** 显式
   结构」，同时又禁止 0-span 静默通过。空列表 `provenance: []` 是否合法、若合法如何
   与「整体 unresolved」区分，未定义；对照 `multiple_source_spans` 明写「**有序
   non-empty 列表**」，一致性不足。
3. **§13 的 Owner 批准清单（7 项）不含该项**：清单覆盖 form/字段名、char 编码单位、
   `table_cell` 身份、legacy 读取规则、JSONB/DDL、Gate 校验深度、Freeze Order——
   **没有一项要求钉死 fail-closed 的状态值与承载字段**。
   P04 的核心恰恰是 fail-closed（P04.4），这是本次变更安全键。

---

## 7. Q7 —— 语料实测覆盖缺口

本轮同目录、同 git 历史线的 P04 根因调查报告（commit `e3a59e2`，
`Docs/COORDINATION/CONTRACTS/P04-OPTION-EVIDENCE-ROOT-CAUSE-INVESTIGATION.md`）在
945 个 `options_lines` block 全量上给出的最小充分集（`:192-208`、`:1000-1005`、`:1090`）：

```text
option label + option text
+ provenance ∈ { line_range | char_span_in_line | table_cell | image_region }
  （多态，必需其一）
+ 多 span 支持
必需：残差显式降级声明（不得伪造）

覆盖实测：line_range 40.95% → +char_span_in_line 92.17%
        → +table_cell 93.86% → +image_region/degraded 94.29%
残差 54/945 = 5.71% 需更强标签识别或人工 review
U-03 / D-3：T7（4 个图片化选项）在 Markdown 层**不可能**恢复文字，除非图片 OCR
```

对照 D1 Binding Requirements 与 D4 §4.1 的五形态
（`line_range` / `char_span_in_line` / `table_cell` / `multiple_source_spans` / `other`）：

| 调查要求 | OD-01 是否覆盖 |
|---|---|
| `line_range` | ✅ |
| `char_span_in_line` | ✅（但与既有 `line_character` 关系待定，见 §2.2） |
| `table_cell` | ✅ |
| 多 span 支持 | ✅ `multiple_source_spans` |
| **`image_region` / 显式 `degraded`** | ❌ **未列入强制清单** |
| **残差显式降级声明** | ⚠️ 仅由 P04.4 的一般 fail-closed 间接覆盖，未针对图片化选项说明 |

D4 **未说明图片化选项（4/945 = 0.42%，选项文字仅存在于 `<img>`）由哪个 form 承载**：
`line_range`/`char_span_in_line`/`table_cell`/`multiple_source_spans` 均不可表达；
`other`（`method` + `locator` + 可独立验证回溯信息）**可能**可以，但 D4 从未如此说明，
§11 风险表也没有对应条目。§11 列了 char 编码与 table_cell 坐标两项 HIGH，却未列图片化
选项这一已实测的形态。

---

## 8. Q8 —— L0 修改路径与仓库自身冻结元规范不符

`Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md`（**L0-META，Status: ACTIVE，Normative: YES，
Superseded By: —**，且位于 D4 声称未变的 `Docs/V3_SPEC/**` 内）规定：

```text
:41   | L1 | **Contract Change Record** | 暂无（67 是候选，NOT RELEASED）
        | **修改 L0 的唯一入口** | 未走完流程不得生效 |
:79   | Docs/V3_SPEC/ | 允许：引用；补 Change Record；新增 L1 | 禁止：直接编辑；隐式改变 |
:107  R1 — L0 只能经 L1 修改
:109  任何 L2–L5 文档不得改写、扩充、或「事实上修订」L0 语义。
      新增强制 invariant 同样需要 L1（见 §3 CHANGE-2）。
:112  R2 — L2 不得产生新的架构事实
:114  L2 只能解释 L0 已有事实，或裁决 L0 未覆盖的具体问题。
      若 L2 的裁决要成为系统事实，必须走 L1。
:226  §11 「任何对 L0 的修改…都必须在本节登记」
:328  登记义务：90 §11 自此对任何 L0 修改强制生效。
      90 生效后的 L0 修改若不在此登记，即为违规。
:342  §3 规范变更分类 CHANGE-0…5；判定规则：拿不准往高里归
:368  §4 Status Header 规范（强制）：Document Type / Authority Level / Status /
      Normative / Supersedes / Superseded By / Gate State Authority
```

先例 `CR-001`（`90:271-329`）展示了 L0 变更的正式形态：
`Change Record ID / Target / Change Class / Source Commit / Audit ID / Date`。

D4/D1 给出的流程只有：

```text
Owner Decision → Frozen Spec Change Proposal → explicit diff → Owner review → re-freeze
```

**未出现**：`L1` / `Contract Change Record` / `90` / `CHANGE-0…5` 分类 / `90 §11` 登记 /
`90 §4` Status Header。全仓对 `Docs/COORDINATION/**` grep `Change Record|L1 |CA-00|90 §`
仅命中无关处（`log.md` 的 90 §1.2 历史、`CURRENT.md` 的根目录模型行、`CONSUMER-GAP-MAP`
的「L1 · 载体读取」分层标题）。

后果：

1. 按 D4 §13 的 7 项勾选完成 re-freeze，将**绕过 `90 R1/R2` 规定的 L1 唯一入口**，并使
   该次 L0 修改**未在 `90 §11` 登记**——按 `90:328-338` 自身表述即构成违规。
2. 变更**未经 `90 §3` 分类**，因此无法确定所需流程强度：按「拿不准往高里归」，
   新增多态 form + option 结构属 **CHANGE-2（Normative Addition）**以上；而废止
   `00 §5` 非目标、改变 `20 §5.5` granularity 枚举、改变 Compiler 提取规则、可能改变
   `dedup_key` 输入，属**改变既有规定的行为 = CHANGE-3（Normative Modification）**，
   其要求是「Change Record **+ 受影响层回归**」——回归义务未被识别。
3. D4 的文档类型（`FROZEN SPEC CHANGE PROPOSAL`）不在 `90 §1` 的 L0–L5 分类中，也未使用
   `90 §4` 强制的 7 字段 Status Header。

**未发生违规**（本轮未改 L0）。风险落在**未来的 re-freeze 动作**上。

---

## 9. 已登记的 findings（仅登记，**未修复**）

| ID | 级别 | Re-freeze 前置 | 内容 |
|---|---|---|---|
| **F-OD01-01** | MED | YES | §2.1「Current Frozen Semantics」遗漏 `20 §5.5` 既有 `granularity ∈ {line, line_character}` + `start/end_offset`（其存在理由即「单行多选项」）与 `table_cell/fragment 延后` 注；遗漏 `00 §5` 把 table cell/fragment 字符粒度列为**明确非目标**。导致 §1 对 `char_span_in_line` 的缺口主张存疑、对 `table_cell` 的障碍定性偏轻（实为废止冻结非目标）。 |
| **F-OD01-02** | MED | YES | 变更集不完整：至少 5 处 L0 条款（`00:274-275`、`20:322`、`20:454`、`20:280`、`20:523`）需修改/废止而 D4 §6/§14 未列；§14 target 未含 `00_Master_Spec.md`。D1 规定的 `explicit diff` 环节未交付。 |
| **F-OD01-03** | MED | YES | 「禁 V3 rediscovery」（P04/OD-01 requirement 7）与现行 `20 §5.3` `option_label` 解析规则（V3 侧按 A/B/C/D 顺序确定 option 边界）冲突未处置；未定义 `options[]` 存在时 `§5.3` 的地位。 |
| **F-OD01-04** | MED | YES | 新增 Producer `options[].provenance` 与既有 IR `content.options[label].source_span`（`20 §6.1:368`）的**权威顺序、冲突信号、no-double-consumption 交互、`10 §8` 2b/2c 核验**全部未定义 → 与 OD-04「禁第二 semantic authority path」需显式对齐。 |
| **F-OD01-05** | MED | YES | fail-closed 表征歧义：`unresolved`（§4.1/§4.3）与 `options_unresolved: true`（§4.2）并存未定名；§4.1「0..n」与「不得 0-span 静默通过」并存；且该安全关键项**不在 §13 的 7 项 Owner 批准清单**内。 |
| **F-OD01-06** | MED | YES | 语料实测最小充分集中的 `image_region` / 显式 `degraded`（4/945 = 0.42%，选项文字仅存于 `<img>`）未纳入 OD-01 强制形态清单，未说明由哪个 form 承载，§11 风险表无该项。 |
| **F-OD01-07** | MED | YES | L0 修改路径未对齐仓库自身冻结元规范：未按 `90 §3` 分类（新增强制 ontology 至少 CHANGE-2；废止 `00 §5` 非目标 / 改 granularity 枚举 / 改 Compiler 提取属 CHANGE-3，需「受影响层回归」）；未声明经 `90 R1/R2` 唯一入口 **L1 Contract Change Record**；未含 `90 §11` Change Audit Record 登记；未用 `90 §4` 强制 Status Header。 |
| **F-OD01-08** | LOW | NO | 引用精度：§2.1「Example keys = `sp-<unit>.option.<label>`（IR 示例中的 role key）」与原文不符 —— `20 §6.1` 示例实为 `sp-Q1-A`；`sp-<unit>.option.<label>` 是**代码** `backend/app/domains/compile/ir.py:73-76` 的构造（同目录调查报告附录 C `:1207` 亦如此归类），D4 沿用了调查正文 §Q6 `:185` 把它写成「V3 Spec 要求」的说法。 |

> 全部 8 项**仅登记，未修改任何文件**。修复属 Owner / 实施方权限。

---

## 10. 经证实的正面结论

| # | 结论 | 标签 |
|---|---|---|
| P1 | D4 为 Proposal，**未生效**；`Docs/V3_SPEC` 树在 `b743c5d`/`7934844`/`3e2f9bb`/HEAD 四处**完全一致**（`b3eeb3e9…`） | DIRECTLY VERIFIED |
| P2 | 本轮 3 笔提交未触及 `Docs/V3_SPEC/**`（unpushed diff 仅 5 个 `Docs/COORDINATION/**` 文件） | DIRECTLY VERIFIED |
| P3 | D1/D2/D3/D4 全部一致地把 OD-01 标为 APPROVED design / PENDING incorporation；**无一处**自称已生效 | SOURCE-LEVEL VERIFIED |
| P4 | Phase 1 Entry 与 Forbidden 正确包含「OD-01 re-freeze 前不得实施 Resolved Span 扩展」；Phase 顺序 `0→1→2→3→5→6→4` 一致（D2 `:442`、D3 `:213-221`） | SOURCE-LEVEL VERIFIED |
| P5 | P04 条款引用忠实：`options[]={label,text,provenance}`、`options_lines` 不得删除、禁一 option 一行、fail closed、历史不 patch 均与契约 `:278-320` 原文一致 | SOURCE-LEVEL VERIFIED |
| P6 | `label` 仅 options 用 / `text_hash = SHA256(text.encode("utf-8"))` / `source_span` 为应用层 invariant 而非 FK —— 与 `10 §6.3` 原文逐字一致 | SOURCE-LEVEL VERIFIED |
| P7 | 使用既有冻结术语 `Historical Source Reprocessing Principle`（契约 §1c `:493`）而非自造术语 | SOURCE-LEVEL VERIFIED |
| P8 | `Docs/COORDINATION` 无任何文件引用 OD-01 为生效规范；`AITutor-X` 侧 `F-RBC-01` 状态记法与 D1 声明无矛盾 | DIRECTLY VERIFIED |

---

## 11. 对「本轮交付报告」自述的核对

| 交付报告自述 | 实测 | 判定 |
|---|---|---|
| D1–D5 五个交付件及提交号 | 5 文件全部存在；`c55797f`(3 files,+1229) / `ee6d915`(1,+361) / `506ffa8`(1,+316) 归属正确 | ✅ |
| 「三笔分离」 | 实测三笔互不混提 | ✅ |
| 「本地已 commit，未 push」 | v3 `main...origin/main [ahead 3]`，`reflog HEAD@{0..2}` 为本地 commit | ✅ |
| 「LOCAL_ONLY / GOVERNANCE untracked 按惯例保留未入库」 | v3 工作树 10 项全部 `??`（9 个 `Docs/COORDINATION/CONTRACTS/*` + `Docs/GOVERNANCE/`），未入库 | ✅ |
| G-02「rev-list count = 1 / 反向 0；7 files, 29 insertions, 21 deletions」 | 三条命令输出**逐字吻合** | ✅（附带确认，非本报告评审对象） |
| Frozen Spec / Frozen Contract / production / schema / corpus 未改 | `Docs/V3_SPEC` tree 未变；unpushed diff 全为 docs；Papers HEAD 仍 `2b92898` | ✅ |
| Phase 1 未启动、migration/X3 未进入 | 未见任何 implementation/schema/migration 变更 | ✅ |
| D5「Phase 0 test baselines：Preprocessing 338 passed, 1 xfailed；V3 backend 2030 passed, 1 skipped, 1 xfailed」 | **未复跑**（属 G-02 范围，非 OD-01 评审对象；且本沙箱无 PostgreSQL、`tmp_path` 写入被拒，全量基线不可比） | **VERIFIED BUT NOT REPRODUCED**（SHA 前置条件已确认） |

**未发现交付报告对 OD-01 的实质夸大**：它没有声称 D4 已生效、没有声称 Frozen Spec 已改、
没有声称 Phase 1 已启动。「OD-01 APPROVED — Frozen Spec Change Proposal pending」的记法
与实测一致。

---

## 12. 限制（必须与结论一并阅读）

- **L-1 —— 未复跑任何测试基线。** 本报告为文档/规格层对抗复核，`338 passed` /
  `2030 passed` 两项未复现（详见 §11 末行）。本沙箱无 PostgreSQL；`tmp_path` 写入被拒。
- **L-2 —— 原始 PDF 版面未取证。** 本报告引用语料统计（945 / 498 / 16 / 4）时，接受的
  是调查报告所声明的 OCR/Markdown 层实测；该报告自身 `:1102-1104` 声明的 PDF 层证据缺口
  （U-01/U-02）本报告**未补齐**，故 F-OD01-06 的 4/945 属「调查已登记、本报告未独立复跑」。
- **L-3 —— 未做语料重算。** 本报告不重新统计 945/1664/4609 等数字，仅核对报告内部一致性
  与其对 Frozen Spec / Contract 的引用。
- **L-4 —— 沙箱限制。** 本会话 `workspace-write` 模式下 `pwsh` 沙箱初始化失败
  （`SetNamedSecurityInfoW failed (Win32 5)`），全部 git 只读命令经一次性 `danger-full-access`
  升级执行；未执行任何写操作于 `AITutors-v3`。
- **L-5 —— `git fetch` 不可用**，故 `origin/main` 读数取自本地 remote-tracking ref；未 push
  的 3 笔提交无法与远端权威比对，但「本地未 push」这一声明本身可由 `ahead 3` 证实。
- **L-6 —— 本报告的判定仅覆盖 OD-01。** OD-02/03/04/05/G-01/G-02 的实体正确性**未被评审**；
  本报告对它们的一切提及（如 OD-04 的「禁第二 authority path」）仅作为 OD-01 自洽性检验的
  参照，不构成对它们的背书或否定。
- **L-7 —— 07 号 finding 的判定基于仓库现存 L0-META 文档 `90_DOCUMENT_GOVERNANCE.md`。**
  若 Owner 认为 COORDINATION 治理栈已另行取代 `90`，则该 finding 应重判；本报告未发现任何
  取代记录（`90` 头部 `Superseded By: —`、`Status: ACTIVE`）。

---

## 13. 最终判定

```text
OD-01 Frozen Spec Change Proposal = VERIFIED WITH FINDINGS
Closure Blocking = NO
Recommendation    = OWNER ACTION REQUIRED BEFORE CLOSURE
```

**判定口径（务必按此读）**：

- `Closure Blocking = NO` 指：**本 Proposal 自身不需要被"关闭"**——它被正确地标记为
  NOT EFFECTIVE，Frozen Spec 逐字节未变，Phase 1 被正确门禁，OD-01 未被实施。
  因此没有任何"被错误关闭"的对象，隔离性与非生效性 **全部成立**。
- 8 项 findings **不阻断本轮治理记录**，但它们**阻断 `re-freeze` 这一步**。
  Owner 若据 D4 §13 的 7 项勾选直接 re-freeze，将产生一份**内部自相矛盾的 Frozen Spec**
  （`00 §5` 非目标 vs 强制 table_cell；`20 §5.3` rediscovery vs 禁 rediscovery；
  `granularity` 枚举未定；`dedup_key` 输入悄然改变），并**绕过 `90 R1/R2` 的 L1 唯一入口**。

**re-freeze 前必须处置（Owner 决策面）**：

```text
1. 补齐「现状基线」：20 §5.5 granularity{line,line_character}+offset、00 §5 非目标、
   延后注 —— 并明确 char_span_in_line 与既有 line_character 的关系（F-OD01-01）
2. 交付确切 change set（条款级，含 00_Master_Spec.md）＝ D1 要求的 explicit diff（F-OD01-02）
3. 裁决 20 §5.3 option_label 的地位（取代 / fallback / 保留）（F-OD01-03）
4. 定义 Producer options[].provenance 与 IR content.options[].source_span 的权威与冲突规则（F-OD01-04）
5. 钉死 fail-closed 状态值与承载字段，并纳入 §13 批准清单（F-OD01-05）
6. 补 image_region / 显式 degraded 的承载形态（4/945 已实测）（F-OD01-06）
7. 按 90 §3 分类本次变更、经 L1 Contract Change Record、登记 90 §11、补 90 §4 Status Header（F-OD01-07）
8. （可选、低优先）修正 §2.1 Example keys 引用（F-OD01-08）
```

```text
Frozen Spec:        UNCHANGED（Docs/V3_SPEC tree = b3eeb3e9…，四处一致）
Frozen Contract:    UNCHANGED
Production Code:    UNCHANGED
Preprocessing Code: UNCHANGED
Database Schema:    UNCHANGED
Corpus:             UNCHANGED
Migration:          NOT AUTHORIZED
X3:                 NOT ENTERED
Phase 1:            NOT STARTED
OD-01 as Frozen Spec:  NOT EFFECTIVE（Proposal only）
Findings:           8 REGISTERED, 0 REPAIRED
Next:               Owner 处置上述 8 项 → explicit diff → L1 Change Record
                    → re-freeze → DSH 复核 re-freeze 结果 → 方可 Phase 1
```

---

## 附录 A — 复核命令与产物（可复现）

```text
仓库基线
  D:\Project\AITutor-X      HEAD = 5618b0075d34f5e0763682d75a9f223202a3e9cb（= origin/main，clean）
  D:\Project\AITutors-v3    HEAD = 506ffa81e5639333ba2bfae61fb8d9d09c2e9aca（ahead 3，未 push）
  D:\Project\Papers         HEAD = 2b92898f05f6541a5fc65c8300cb8a59a06c4928（= origin/main，clean）

隔离证据
  git rev-parse {b743c5d,7934844,3e2f9bb,HEAD}:Docs/V3_SPEC   → 同一 tree
  git diff --name-only origin/main..HEAD -- Docs/V3_SPEC      → 空
  git rev-list --count b743c5d..7934844 = 1 / 反向 = 0
  git diff --stat b743c5d..7934844 → 7 files, 29 insertions(+), 21 deletions(-)

条款引用（逐字核对）
  Docs/V3_SPEC/00_Master_Spec.md:264-279        §5 明确非目标
  Docs/V3_SPEC/20_Document_Pipeline.md:280      §5.3 option_label
  Docs/V3_SPEC/20_Document_Pipeline.md:308-324  §5.5 Resolved Span + granularity
  Docs/V3_SPEC/20_Document_Pipeline.md:365-369  §6.1 IR 示例 span_id
  Docs/V3_SPEC/20_Document_Pipeline.md:454      §7.2 步 1（line / line_character）
  Docs/V3_SPEC/20_Document_Pipeline.md:523      §7.3 Question dedup_key
  Docs/V3_SPEC/10_Data_Model.md:451-471         §6.3 instance_role_contents
  Docs/V3_SPEC/10_Data_Model.md:625-640         §8 provenance 不变量 2a-2d
  Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md:40-45,79,107-115,224-230,271-329,342-383
  Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.3-DRAFT.md:278-320,493
  Docs/COORDINATION/CONTRACTS/P04-OPTION-EVIDENCE-ROOT-CAUSE-INVESTIGATION.md
      :185-186, :192-208, :212, :1000-1005, :1045, :1090, :1108, :1136, :1138, :1207
  backend/app/domains/compile/ir.py:73-76      _content_span_id

本报告未写入 AITutors-v3；v3 工作树在本轮复核前后均为 10 项未跟踪文档，无变化。
```

## 附录 B — 本报告未做的事

```text
未修改 Frozen Spec（Docs/V3_SPEC/**）
未修改 Frozen Contract / P01–P25
未修改 D1 / D2 / D3 / D4 / D5 原文
未修改 production / preprocessing 代码、Gate、Admission、DB schema
未修改 corpus（Papers 仓只读）
未修复任何 finding
未 re-freeze；未把 OD-01 标为已生效 Frozen Spec
未进入 Phase 1；未 migration；未 X3；未 push AITutors-v3
未评审 OD-02 / OD-03 / OD-04 / OD-05 / G-01 / G-02 的实体内容
```

---

**Document control**

| Field | Value |
|---|---|
| Path | `Docs/60_REPORTS/OD-01-FROZEN-SPEC-PROPOSAL-DSH-ADVERSARIAL-REVIEW.md` |
| Status | COMPLETE — ADVERSARIAL REVIEW (OD-01 ONLY) |
| Verdict | VERIFIED WITH FINDINGS |
| Closure Blocking | NO |
| Recommendation | OWNER ACTION REQUIRED BEFORE CLOSURE |
| Findings | F-OD01-01 … F-OD01-08（8 项，未修复） |
| Subject HEAD | `AITutors-v3` 506ffa8（未 push）· Frozen Spec tree `b3eeb3e9…`（unchanged） |
| Reviewed at | AITutor-X HEAD 5618b00 |
