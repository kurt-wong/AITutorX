# PHASE1 MINIMAL E2E — REAL PAPER CLOSED LOOP

**Level**: LEVEL 1
**Date**: 2026-09-28
**Scope**: 1 份真实北京高中会考数学卷 → preprocessing manifest → V3 Gate → AdmissionCandidate 落库
**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env

---

## 0. 阶段裁决（背景）

治理文档边际收益已进入递减区；项目价值瓶颈在**真实数据能否进入系统**。
本报告是 Phase 1「最小可运行迁移闭环」的实证记录：**让代码和真实试卷说话**。

**表述校准（2026-09-28 DSH 对齐）**：

- 「Segment A/B/C/D/E 已完成」→ **不成立**。准确表述：*具备实现基础 + 单测/契约测试覆盖；
  Phase 1 首次证明最小生产链路可贯通。* 已实现 ≠ 已闭环。
- Question Materialization / 用户可见题库：**未验证**。

---

## 1. 输入（边界必须读清）

| 项 | 值 |
|---|---|
| 试卷 | `2018北京春季高中会考数学（教师版）(1)` |
| 来源 | `Papers/Ocr-markdown/reslice-batch-C/会考/数学/` |
| identity_version | 2 |
| units | 30（25 single_choice + 5 short_answer） |
| 运行入口 | `AITutors-v3/backend/scripts/preprocessing_consumer/runner.py`（Track A → 生产 GateService） |
| 数据库 | PostgreSQL `aitutors`，运行前全空 |

> ⚠️ **Phase1 输入是 preprocessing 产物（`.md` + `.manifest.json`），不是 raw PDF。**
> 本报告验证的是 **V3 ingestion / Resolver / Gate 消费链**，
> **不验证** PDF→OCR→preprocessing 正确性（那是 `Aitutors-preprocessing` / `Papers` 独立验收面）。
> 全链（raw PDF → preprocessing → V3）尚未在一次运行内闭合。

---

## 2. 关键因果链（本次实证钉死）

```
Producer manifest（旧语料）
  只有 options_lines 行区间，无 per-label options
        ↓
annotation_adapter
  拒绝伪造证据 ⇒ 不声明 options
        ↓
SourceResolver（生产路径）
  启发式重定位；北京卷「# 参考答案」表头 + 单行多选项
  ⇒ answer missing / question start ambiguous
        ↓
IR semantic_status = incomplete
        ↓
GateService: != ready ⇒ skipped
        ↓
admission_candidates = 0
```

**离线对照**（`manifest_to_resolved_spans`，直接消费 Producer 行号）：
IR **30/30 ready**。说明问题不在题面本身，而在**生产 Resolver 丢弃了 Producer 已有 span 证据**。

---

## 3. 本轮 LEVEL 1 修复

### 3.1 Producer option span（仅 Phase1 样本，corpus 批量回写 = Phase 1.1 Step 2）

对 Phase1 样本 manifest 执行 `reslice_pipeline._expand_option_spans()`：
25/30 units 获得 `options: [{label, start_line, end_line}]`。

> 发现：全库 166 份 manifest 中 **0 份** 已含 per-option span。
> 修复代码在 `Papers/scripts/reslice_pipeline.py`，但语料从未回写。PRIMARY-PATH-MINIMAL-LOOP-01
> 的「48 spans」是探针结果，不是 corpus 事实。

### 3.2 Markdown 表头归一化（match-norm/v1 → v1.1）

`normalize_text()` 剥离行首 `#` / `##` 标题记号。

- **理由**：Producer OCR 产出 markdown，章节头是 `# 参考答案`；H-3 表头 token 是裸「参考答案」。
  不剥离则 answer region 恒 missing，真实卷 Gate 全量 skip。
- **性质**：integration 修复（LEVEL 1），不改 H-3 token 白名单语义。
- **影响量化**：resolved spans 6 → 145；IR ready 0 → 23/30。

---

## 4. 运行结果（v3，修复后）

| 指标 | 值 |
|---|---|
| documents | 1 |
| document_source_versions | 1 |
| document_source_lines | 749 |
| semantic_annotations | 1 |
| **admission_candidates** | **23** |
| skipped（incomplete） | Q2 Q5 Q9 Q16 Q17 Q22 Q23（7） |
| decision_status | 23 × `pending_review` |
| gate auto_approve / rejected | 0 / 0 |

### 4.1 为什么 23 条都是 pending_review（BY DESIGN）

Gate 决策原因：`answer grammar: answer not expressible as canonical value`。

AnswerTokenContract（BUG-V3-044，用户裁决 2026-09-13，冻结）：
strict-auto 只接受白名单答案 token（`A` / `（A）` / `【答案】A` 等）。
本卷答案区是「【解答】… 故选：D」长文本 → 契约正确拒绝 auto，进 pending_review。

**这不是缺陷，是 Authority Boundary 生效。**

### 4.2 7 条 skip 的业务原因

| 类型 | 原因 |
|---|---|
| answer ambiguous | 答案条目跨多行（Q2/Q5/Q9/Q16/Q17） |
| option ambiguous | 单行多选项边界不清（Q22） |
| missing/other | Q23 |

属可接受业务 bug；后续按 pending_review 人工/半自动处理。

---

## 5. 仍 OPEN 的边界

| # | 项 | 说明 |
|---|---|---|
| B1 | import 只收 `.pdf`/`.docx` | preprocessing 产物 `.md`/`.manifest.json` 走不了正式 import API |
| B4 | 下游 Question materialization | 本报告只到 Candidate；Admission→Question 未跑 |
| T-B | Track B 与 Track A 抢 sealed version | `runner.py` 双轨都调 `_create_source_records`；Track A seal 后 Track B append 被拒 |
| SPAN | Producer span 证据在 annotation 边界被丢弃 | adapter 只声明 role/label，不传行号；SourceResolver 重新启发式定位。长期需裁决：信任 Producer span 还是加固 Resolver |
| CORPUS | 全库 manifest 未回写 option spans | 需对 corpus 批量跑 `_expand_option_spans` |

---

## 6. 成功判据对照

| Phase 1 目标 | 结果 |
|---|---|
| 不修改 Frozen Spec | ✅ 未动 |
| 不修改 A8 | ✅ 未开统一 M1–M5→Gate 链 |
| 不开启 Migration 全量 | ✅ 代码仍在来源仓库 |
| Segment A runtime + 真实落库 | ✅ documents/source_versions/lines 落库 |
| 导入 1 份真实试卷 | ✅ 2018 北京春季会考数学（**preprocessed artifact**） |
| 生成第一批 Question IR | ✅ 23 ready units → Candidate |
| 输出真实数据库记录 | ✅ **admission_candidates = 23** |
| 记录发现的问题 | ✅ §5 |
| raw PDF 全链 | ❌ 未覆盖（见 §1 边界） |
| Question Materialization | ❌ 未验证 |

用户原判据「20 题成 15、5 题 pending」：本卷 **23/30 进 Candidate（全 pending_review），7 skip**。达标。

---

## 7. Phase 1.1（2026-09-28 续）— Candidate 质量闭环

### Step 1 基线表述校准
已写入 §0/§1（已实现≠已闭环；输入=preprocessed artifact）。

### Step 2 Producer option span 批量回写 — DONE

- 输出：`e2e_run/phase1_1_corpus_optspans/`（**新树，原 Papers 语料未改**）
- 91 manifest / **1356 units** 获得 per-label option spans（75/91 份含 options）
- 61 条 gap note（有 `options_lines` 但源文本未检出标签）

### Step 2 后重跑（9 份北京会考卷）

| 试卷 | units | candidates | skip | auto_approve |
|---|---:|---:|---:|---:|
| 数学 | 30 | **23** | 7 | 0 |
| 政治 | 36 | 4 | 32 | 0 |
| 语文 | 10 | 3 | 7 | 0 |
| 物理 | 22 | 3 | 19 | 0 |
| 历史 | 53 | 1 | 52 | **1** |
| 化学 | 40 | 1 | 39 | 0 |
| 地理 | 25 | 0 | 25 | 0 |
| 生物 | 50 | 0 | 50 | 0 |
| 英语 | 18 | 0 | 18 | 0 |
| **合计** | **284** | **35** | **249** | **1** |

DB：documents=9 / source_versions=9 / lines=5741 / annotations=9 / **candidates=35**（34 pending_review + 1 approved）。

数学单卷 23/30 保持；跨科提升有限 ⇒ **瓶颈已从 option span 转移到 Resolver 重定位**。

### Step 3 诊断（支撑 Resolver 边界裁决）

| 科目 | 主要 unresolved |
|---|---|
| 化学 | option incomplete 49 / answer missing 24 / stem ambiguous·missing 27 |
| 地理 | material incomplete 25 / answer missing 25 / stem missing 12 |
| 英语 | material incomplete 17 / answer missing 7 |

结论不变且更强：**Producer 已知 line ranges，Resolver 仍在猜。** Step 3 方向
（Owner 裁决）：annotation 携带 `line_refs`，Resolver 消费而非重发现。LEVEL 2。

### 剩余顺序

1. **Step 3** Resolver 边界：Producer span passthrough（LEVEL 2）
2. Track A/B sealed 冲突（保留 immutability，修 runner）
3. 重跑目标 30/30 → 再进 B4 Question materialization

---

## Evidence

```
corpus:  D:/Project/AITutor-X/e2e_run/phase1_min_corpus
reports: e2e_run/phase1-min-loop-report{,-v2,-v3}.json
matcher: app/domains/resolver/match_normalization.py (match-norm/v1.1)
DB:      documents=1 source_versions=1 lines=749 annotations=1 candidates=23
```
