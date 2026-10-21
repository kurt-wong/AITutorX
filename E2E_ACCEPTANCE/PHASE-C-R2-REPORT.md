# Phase C-R2 报告 — 真实结构输出 · 碰撞防护 · testsuite 取证 · 口径修正

## 1. 本轮目标

在 **仅 Papers** 授权内完成：A 真实 Producer 结构回归、B 图像碰撞防护、C testsuite 只读取证、D 验收口径修正。

**未修改**：AITutors-v3 / U-cl2 规则 / 三条反馈 / 任何库写入。

---

## 2. 工作项 A — 真实 Producer 结构回归

### 入口

`reslice_pipeline.write_outputs()`（与 `recompile_outputs` 同一生产入口，**不调 LLM**）。

### 运行命令

```text
python -m pytest tests/test_phase_c_r2_real_output.py -q
# 内部：_run_real_producer() → write_outputs(chem paper.md + manifest) → 读 paper.manifest.json / paper.annotated.md
```

### 产物位置

`<pytest tmp>/producer_out/`（每次测试运行现场生成）+ 手动对照 `Papers/Ocr-markdown/phase-c-r2-producer-out/`  
证据 JSON：`PHASE-C-R2-PRODUCER-OUT.json`

### 四题断言（均对**本次 write_outputs 产物**，非测试内手写 HTML）

| 题 | 产物内结构（annotated.md options META 块） | 断言 |
|---|---|---|
| **Q9** | `<table>` 行1 `A. 青铜器皿…D. 中草药`；行2 四 `<img src=…>` | labels=`[A,B,C,D]`；`img_refs=4`；`image_assets` 四条 `resolved=true` 且文件在 `_imgs/` |
| **Q19** | 列头 `<td>A</td>…<td>D</td>` + `t / °C` / `c(H2SO4)` 矩阵行 | 保留表格矩阵；**禁止**拍成 `>A. 文本` 形态 |
| **Q24** | 行1 `[F_{4}][F_{3}][F_{5}][F_{2}]`；行2 `A. 收集氯气…` | F 引用保留 + labels=`[A,B,C,D]` 列对齐 |
| **Q25** | 表头「选项\|实验操作及现象\|推理或结论」+ 4 行×3 `<td>` | labels=`[A,B,C,D]`；每数据行恰好 3 列（复合，非 8 假选项） |

### 契约现状（如实）

- **正式产物已保留**完整 HTML 表格于 `annotated.md` 的 `options` META 块 + 源 `paper.md`。
- **manifest `units[].options_lines` 仍是行区间**，未拆成 per-label 对象。列/行/图文对应关系的**结构载体是 annotated 表格 HTML**，不是独立 schema 字段。
- 本轮**不伪造** per-option JSON 字段；若 Consumer 需要结构化选项对象，属契约扩展，需 Owner 另批。

---

## 3. 工作项 B — 图像同名碰撞 + 旧字节刷新

`package_image_assets()` 修复两处（DSH 指出）：

1. **异源同名**：basename 相同、sha256 不同 → `resolved=false, reason=basename_collision`（附 `existing_sha256` / `incoming_sha256`），**不静默合并**。
2. **dest.exists() 跳过复制**：源字节变更时**强制刷新**，清单 sha256 与磁盘一致。

### 三情形测试（`test_phase_c_r2_real_output.py`）

| 情形 | 结果 |
|---|---|
| 同一源重复引用 | 去重，两条 resolved，同 sha256 |
| 异源同名、内容不同 | 第二条 **basename_collision**，磁盘仅 1 个文件 |
| 同名源内容变更重跑 | **刷新**产物，`h2≠h1`，磁盘 hash=清单 hash |
| 文件不存在 | `file_not_found`，不生成悬空 ref |

### 真实 chem 卷重跑

```
python _phase_c_image_pack.py
→ total assets 22, resolved 22, unresolved 0
→ Q9 四图 resolved/on_disk=true
```

### Q9 四图 vs DSH 固定参照

| 文件 | sha256 | bytes | 一致 |
|---|---|---|---|
| img_in_image_box_157_151_247_252.jpg | `42644ed0…d5017c` | 2594 | ✅ |
| img_in_image_box_328_147_444_230.jpg | `5aa84d67…5ba8650` | 3964 | ✅ |
| img_in_image_box_529_136_618_235.jpg | `b9a6acfa…60ca93` | 4043 | ✅ |
| img_in_image_box_725_140_864_227.jpg | `45af11e7…5b5f976f4` | 5246 | ✅ |

断言：`test_q9_four_image_hashes_match_dsh_baseline`（对 write_outputs 产物 + 磁盘字节）。

---

## 4. 工作项 C — testsuite 数据消失（只读取证）

### 实测（与 DSH 一致）

`aitutors_testsuite`：**选择性清空**，非库级重建。

| 存活 | 零 |
|---|---|
| `alembic_version(1)` · `budget(100)` · `llm_call_audit(28)` | 其余业务表（documents/questions/…/question_feedbacks 等） |

### 已证实

1. **机制类型**：枚举表集的 `DELETE FROM` 清理例程，**不是** `DROP SCHEMA` / 重建 / `TRUNCATE ALL`（否则 budget/llm_call_audit 也会归零）。
2. **代码中存在多处 autouse 清理**（对 testsuite 生效，经 conftest）：
   - `tests/test_task_executor.py` `_purge_all` → `DELETE FROM` **16 表**（含 questions/documents/…，**不含** question_feedbacks / llm_call_audit / budget）
   - `tests/test_question_dedup_concurrency.py` → DELETE question_instances/questions
   - `tests/test_h_seal_concurrency.py`、`scripts/live_smoke_ollama.py` 同类
3. **`llm_call_audit=28` 存活**与「按表 DELETE、不碰审计/计量表」一致。
4. **Phase C 首轮「testsuite 未写入」表述不实**：M3b/M3b-R1 测试曾写入（当时观察到 3 documents / 3 questions / 11 feedbacks）；其后变为零。**纠正：曾写入 → 后被选择性清理。**

### 可能原因（非已证实）

- 某次包含 `_purge_all` 的 pytest 运行（如 `test_task_executor`）在反馈行已不在或 FK 策略允许时清空了 questions 族。
- `question_feedbacks` **不在**任何 `_CLEANUP_TABLES` 列表中；其行消失与 `DELETE FROM questions` 的 FK 约束如何并存，**尚未完全解释**（可能：清理时反馈已空 / 另有未检索到的删除路径 / 事务失败顺序）。

### 未查明

- **谁、何时、哪条命令**执行了清理 — 无执行日志，**原因不能写成已证实**。
- 不归因于「MIMO 故意清库」，也不当作无影响事件。

### 本轮

**未**对 `aitutors` / `aitutors_test` / `aitutors_testsuite` / `aitutors_phasec_exp` 执行任何写入或恢复。

---

## 5. 工作项 D — 验收口径修正

### 测试数量（精确）

| 集合 | 文件 | 数量 |
|---|---|---|
| Phase C 新增（R1） | `test_printed_number_escaped_dot.py` + `test_phase_c_structure_and_images.py` | **29** |
| 既有 | `test_question_identity_phase2.py` | **17** |
| R1 合计 | 29+17 | **46** |
| Phase C-R2 新增 | `test_phase_c_r2_real_output.py` | **10** |
| **R2 合计（本轮命令）** | 上列 4 文件 | **56 passed** |

### 实验库状态（纠正误读）

| 库 | 状态 |
|---|---|
| `aitutors_phasec_exp` | **仅 CREATE DATABASE，零表、未导入、未做同卷 DB 回归** |
| 21 题 / 126 contents / 3 反馈 | **只读快照自 `aitutors_test`**（`PHASE-C-BASELINE-SNAPSHOT.json`），**不是**实验库验收结果 |
| `aitutors_test` | **本轮零写入**；仍为 21 题基线 |
| `aitutors` | 零变化 |

---

## 6. 修改文件清单

| 文件 | 变更 |
|---|---|
| `Papers/scripts/reslice_pipeline.py` | 碰撞检测 + dest 旧字节刷新（`package_image_assets`） |
| `Papers/tests/test_phase_c_r2_real_output.py` | **新增** 真实产物结构 4 题 + 碰撞 3 情形 + Q9 哈希基准 |
| `AITutor-X/…/PHASE-C-R2-*.md/json` | 报告与证据（只写报告目录） |
| `AITutor-X/…/PHASE-C-ROUND1-REPORT.md` | 口径更正（见下） |

**AITutors-v3**：HEAD 仍 `9a4bfb7`，worktree 仅 3 个既有 untracked `_p14b_*.py` — **零改动**。

---

## 7. 测试命令与结果

```text
cd Papers
python -m pytest tests/test_printed_number_escaped_dot.py \
  tests/test_phase_c_structure_and_images.py \
  tests/test_phase_c_r2_real_output.py \
  tests/test_question_identity_phase2.py -q
→ 56 passed

python -m pytest tests/test_phase_c_r2_real_output.py -q
→ 10 passed   # 含 Q9 哈希与 DSH 基准一致
```

---

## 8. 停止条件

**固定提交**：Papers `main` **`a4a0a8c`**（基线 `785f651` → 本提交，**未推送**，ahead 2）。

已停止。交 DSH 只读核验（真实产物结构、三情形碰撞、Q9 哈希、testsuite 取证、口径、三库零写入）。不进入 Resolver / V3 图像持久化 / 数据库导入 / 前端。
