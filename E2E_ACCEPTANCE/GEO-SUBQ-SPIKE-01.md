# Geography 子题可行性 Spike + IR 边缘最小修正 — 执行报告

**日期**：2026-09-27 · **范围**：只读诊断 + IR 局部修复 · **未改 Gate/Admission/Producer 正式输出**

---

## 1. 三仓库本地/远端同步状态

| 仓库 | 分支 | 本地 HEAD | 远端 HEAD | 状态 |
|---|---|---|---|---|
| `kurt-wong/AITutors-v3` | `od01-r3-convergence` | `5689ef1`（本轮后新 commit） | `origin/od01-r3-convergence` 原 `9a4bfb7` | 开工前 **ahead 5**，无 behind；untracked `backend/scripts/_p14b_*` 保留未提交 |
| `kurt-wong/Aitutors-preprocessing`（`D:\Project\Papers`） | `main` | `a4a0a8c` | `b141bfd` | **ahead 2**，无 behind；untracked `data/` `logs/` `_p14b_patch_producer.py` 保留 |
| `kurt-wong/AITutorX` | `main` | `7bce066` | `7bce066` | commit 一致；工作区大量 untracked 报告/e2e_run 及 staged `MIMO-TASK-PHASE1-MINIMAL-E2E-01.md`，**保留现场未动** |

开工前已 `git fetch` 实测比对，未假设与 GitHub 一致。无 reset/rebase/force-push。V3 与 Papers 的既有未推送提交本轮一并推送同步（见 §5）。

---

## 2. 地理子题边界实测覆盖

**输入**：`2018北京春季高中会考地理（教师版）(1)` · `source_content_sha256=3f4a7a82…`（与 manifest 一致，已断言）· 原始 OCR Markdown 661 行 · 25 units（20 choice composite + 5 short_answer）。

一次性只读脚本 `_dsh_review/geo_subq_feasibility.py` → `geo_subq_feasibility.json`。整卷统计（非单样本）：

| 能力 | 覆盖 | 说明 |
|---|---|---|
| 子题题干起止行 | **50/50** | 需容纳 OCR 分隔符变体（`1\.` `15·` `20，`）、行中粘连题号（`…题。16.`）、区间后粘连（`完成26－2926.`） |
| 选项标签 A–D 唯一绑定 | **49/50** | 唯一失败 **Q43**：OCR 截断 `A.①②③B.①②④C`（D 缺失、C 误入 B） |
| 选项文本 | 49/50 | Q20 选项 D 尾部粘了下一组材料 `读表1完成21～23题。`（可确定裁剪，非歧义） |
| 答案唯一对应 | **50/50 choice** + **5/5 short_answer** | 选择题答案表 L601 可解析出 50 键；短答 printed 1–5 ↔ 答案区小问 (1)(2)(3)… 行号对齐 |

**短答（U-P2-1…5）**：题干小问 (1)–(5) 与答案小问 (1)–(5) 一一对应（printed 号唯一）。例外：**U-P2-5** manifest `answer_lines=[653,660]` 未覆盖第 (4) 问答案 L661（差 1 行，Producer 区间声明可修）。

**例外/歧义汇总**：① Q43 选项 OCR 截断（不可恢复，应拒）；② Q20 选项 D 尾部污染（可确定裁剪）；③ U-P2-5 答案区间声明偏紧（差 1 行）；④ 粘连题号需规则特判（已验证可确定，非猜测）。无答案映射歧义。

---

## 3. 是否值得授权最小 Producer 实现

**值得。** 边界与答案映射确定性充分，无需改 Gate/Admission。

- **最小 Producer 输出**：composite 单元增补 `sub_questions[]`，每子题声明 `question_number`、`stem_lines`、`option_lines`（标签+文本）、`answer_ref`（指向答案表键或答案小问行）；不改现有 `material_lines`/`questions_lines`/`answer_lines` 契约。
- **V3 消费改动范围**：`manifest_annotation.py` 绑定 `sub_questions` → IR 子题节点（已有 `sub_questions` 通道，geo 现因空子题被拒）。Resolver/Gate/Admission 不动。
- **预期收益**：25 现 0 入库 → **约 49 道 single_choice 可验证 Question**（Q43 拒）+ **5 道 short_answer 结构可验证**（答案多空，是否过 Gate 取决于短答答案规则，保守计不计入本轮承诺）。相对四卷基线 56 题，地理单项可再增 **+49**（约 +87%）。
- **仍会拒绝**：Q43（选项截断）。Q20/Q44/Q45 若裁剪规则不严可能带噪，实现时以整卷回归为准。

等待授权后再动 Papers/V3 生产代码。

---

## 4. IR 边缘测试复现与修复

**DSH 推论成立。** `probe_ir_seen.py` 复现：composite 兄弟子题共享 `unit_id` 时，`collect_validation_problems` 用 `set(seen)` 副本（兄弟互不可见）而 `_validate_node` 共享 `seen`（后者报 duplicate）→ **父 `ready`/原因 `[]`，子 `['ready','incomplete']`**，违反 invariant 7。

**局部修正**（`backend/app/domains/compile/ir.py`，不改 `IRNode` 接口）：
1. composite 子题遍历改为共享同一 `child_seen` 快照 → 兄弟重复 id 在原因列表即被发现，父节点报 `composite sub_question not ready` 并判 `incomplete`。
2. 子题 `semantic_status=="unknown"`（M.2）亦视为未就绪 → 父节点不再假 `ready`。
3. `unknown` 父节点不再向调用方 `seen` 预写后代 id，消除后续递归把子题误判 `duplicate unit_id`。

修正后：父 `incomplete` + 原因非空 ⇔ 存在非 ready 子题；正常兄弟 id 不同路径仍 `ready`；unresolved span 仍被拦。

---

## 5. 测试结果、代码变更、commit

**测试**（系统 Python + pytest 9.0.3）：
- 新增 `tests/test_ir_composite_sibling_unit_id.py`（5 例：兄弟同 id / 异 id / validate_ir 全路径 / unknown 子题 / unknown 父不误判）
- 回归：`test_ir` `test_compiler` `test_funnel_reasons_match_ir` `test_gate_service` `test_composite_no_fake_single` `test_manifest_annotation_binding` `test_answer_marker_and_composite` `test_funnel_unexplained_loss` `test_x26_m1` `test_x26_m2` 等 **86 + 135 passed**，无失败。
- 修正后 DSH 探针：父 `incomplete`，`父 ready 而子未 ready = False`。

**代码变更**：
- `backend/app/domains/compile/ir.py`（seen 语义一致化）
- `backend/tests/test_ir_composite_sibling_unit_id.py`（新增）
- 诊断只读：`D:\Project\_dsh_review\geo_subq_feasibility.py` / `.json`（不入库）

**Commit / 同步复核**：
- V3 `od01-r3-convergence` → **`b640036`**（`fix(ir): share sibling seen snapshot so composite status matches problem list`），已推送，本地与 `origin/od01-r3-convergence` 同 commit。
- Papers `main` → **`a4a0a8c`**，既有 ahead 2 提交已推送，本地与 `origin/main` 同 commit。
- AITutorX `main` 本地 **`228fad1`**（报告 2 commits：`f87b03c` + `228fad1`）；**推送失败**：github.com:443 当前不可达（TCP connect failed，重试 4 次）。远端仍为 `7bce066`，**本地 ahead 2，未同步**。工作区 untracked/staged 现场原样保留（误带 staged `MIMO-TASK` 的 commit 已软回退，仅保留报告）。
- 未提交保留：V3 `backend/scripts/_p14b_*`；Papers `data/` `logs/` `_p14b_patch_producer.py`。

---

## 6. 数据库

**本轮零数据库写入。** 全程只读本地 Markdown/manifest 与内存 IR 构造；未连 aitutors / aitutors_test / aitutors_testsuite，未建实验库，未重算历史 56 题。

---

## 明确未做

正式地理切分实现 · Producer/Resolver/IR 全面重构 · 数学短答入库 · 批量消化 pending · 表格/图片选项通用支持 · Gate/Admission 修改 · 新建治理文件体系。
