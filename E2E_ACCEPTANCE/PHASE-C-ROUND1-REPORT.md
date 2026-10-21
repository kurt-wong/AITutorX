# Phase C 首轮报告 — Papers Producer 最小修复与产物层验证

## 1. 本轮目标

按 Owner 有条件授权（仅 Papers Producer 及其测试）：

1. 追加 O2 根因证据；
2. 修复印刷题号抽取（`\\.`）并回归；
3. Q9 图像资源随 artifact 打包；
4. Q9/Q19/Q24/Q25 结构回归；
5. 建立独立实验库并固定 21 题基线快照；
6. 登记 `M3C-FE-001` 字号缺陷（独立、不修）。

**未做**：Resolver / Gate / V3 前端 / U-cl2 规则 / 反馈改动 / 人工验收库与 testsuite 写入。

## 2. 实际成果

### 2.1 O2 证据已追加
`PHASE-B-R1-ADDENDUM.md` 末尾新增「O2 根因证据补记」：7 个 `\\.` 题干、`PRINTED_LINE` 缺转义分支、`unknown/unverified` 对照、section 已存在、U-org1 非抽取器例外。

### 2.2 Producer #1 题号抽取（已修）

`question_identity.PRINTED_LINE`：

```python
# 旧：r"^\s*(\d{1,3})\s*[\.、．]"
# 新：r"^\s*(\d{1,3})\s*\\?\s*[\.、．]"   # 含 OCR 转义点 \\.
```

回归：`tests/test_printed_number_escaped_dot.py` — 7 个历史 NULL 单元 + 全角/半角/顿号 + 身份字段分离。

### 2.3 Producer #2 图像打包（已实现）

`reslice_pipeline.package_image_assets()`：源 md `src=` → 实体复制到 `out_dir/_imgs/` + `image_assets` 清单（sha256）。

- 解析顺序：md 相对 → `SRC_ROOT` → 从 `_imgs/` 起拼 `Ocr-markdown`（打包移位场景）；
- **找不到文件记 `resolved=false`，不生成悬空 figure_ref**。

实测 chem 卷：**22/22** 图像可解析；**Q9 四图**均落盘 `phase-c-image-pack/_imgs/`。

### 2.4 Producer #3 结构回归（已测）

`tests/test_phase_c_structure_and_images.py`：

| 题 | 断言 |
|---|---|
| Q9 | 4 标签 A–D ↔ 4 图列对齐 |
| Q19 | 列头矩阵 5 列×数据行，**非**文本选项列表 |
| Q24 | F4/F3/F5/F2 ↔ A/B/C/D 列对齐 |
| Q25 | 行 A–D × 3 列复合，不拆成 8 假选项 |

### 2.5 独立实验库 + 基线快照

| 项 | 值 |
|---|---|
| 实验库 | **`aitutors_phasec_exp`**（新建，非 test / 非 testsuite） |
| 基线来源 | `aitutors_test` **只读**快照 |
| questions | 21 |
| role_contents | 126 |
| candidates | approved=21，pending_review=3 |
| content_hash | `8945aff32ebdb4b5…` |
| feedbacks | 3（含 `f335fd96`） |

第一轮**只做 Producer/产物层**；V3 同卷导入对比待 DSH 核验后再批。

### 2.6 M3C-FE-001 已登记

`M3C-FE-001-FONT-SIZE.md`：15px vs 18.15px（~21%），反馈 `f335fd96`。**未改前端。**

## 3. 验收证据

| 项 | 结果 |
|---|---|
| 基线 | Papers `b141bfd` → **本轮提交**；AITutors-v3 `9a4bfb7` 未动 |
| 测试 | **46 passed** 口径：**29 新增**（printed_dot + structure/images）+ **17 既有**（`test_question_identity_phase2`）|
| 图像 | Q9 四图 resolved/on_disk=true（`PHASE-C-IMAGE-PACK.json`） |
| 实验库 | `aitutors_phasec_exp` **仅建库、零表、未导入**；21 题数据为 `aitutors_test` **只读快照**（非实验库验收） |
| 人工验收库 | 本轮**未写入**（仅只读快照） |
| testsuite | **更正**：测试**曾写入**（3 docs / 3 questions / 11 feedbacks）；其后业务表被选择性清空（见 R2 取证）。不得记为「未写入」 |
| 反馈 3 条 | **未删/未改** |

## 4. 未完成事项

1. **DSH 独立核验**本轮 Producer 提交与产物。
2. V3 同卷导入 `aitutors_phasec_exp` 并对比 21 题/hash（待批准，属 Resolver/V3 层）。
3. M1 配置包是否正式纳入 `_imgs/`（Owner 方案一的打包契约扩展）— 产物层已具备能力，包格式待 DSH/Owner 确认。
4. U-cl2 仍 pending_review（按裁决不改）。
5. M3C-FE-001 前端修复（独立任务）。

## 5. 整体进度

| 阶段 | 状态 |
|---|---|
| Phase B 诊断 | ✅ 关闭 |
| Phase C #1 题号抽取 | ✅ 已修+回归 |
| Phase C #2 图像打包 | ✅ 产物层 22/22 |
| Phase C #3 结构回归 | ✅ 4 题已测 |
| Phase C #4 实验库基线 | ✅ 快照固定 |
| M3C-FE-001 | ⬜ 已登记未修 |
| Resolver/Gate/前端 | ⬜ 未授权 |

## 6. 下一步

DSH 只读核验 Papers 本轮提交（`PRINTED_LINE`、`package_image_assets`、46 测试、Q9 四图、`aitutors_phasec_exp` 与 21 题基线）。核验通过后再决定是否进入 Resolver 或 V3 图像持久化。

---

### 固定提交

- **Papers** `main`：**`785f651`** — `fix(producer): printed_number accepts OCR escaped-dot; package image assets in artifact (Phase C)`（基线 `b141bfd` → 本提交；**未推送**）
- AITutors-v3：**无新提交**（仍 `9a4bfb7`）

### 附件

- `PHASE-B-R1-ADDENDUM.md`（含 O2 补记）
- `PHASE-C-IMAGE-PACK.json`
- `PHASE-C-BASELINE-SNAPSHOT.json`
- `M3C-FE-001-FONT-SIZE.md`
- `Papers/tests/test_printed_number_escaped_dot.py`
- `Papers/tests/test_phase_c_structure_and_images.py`
