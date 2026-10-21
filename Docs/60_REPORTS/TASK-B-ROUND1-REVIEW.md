# 任务 B Round 1 独立复核 —— 断点性质需要重新定性

> DSH 独立复核 MIMO 的 Round 1 定位。**只读**，未修改任何文件。
> **结论：断点位置正确，但性质不是「V3 无法接入预处理产物」，而是「正式摄入 API 的边界过窄」。**
> 这个差别决定任务 B 下一步该做什么。

---

## 0. 裁定

| MIMO 的说法 | DSH 复核 |
|-------------|---------|
| `_ALLOWED_EXTENSIONS = {'.pdf','.docx'}` | ✅ **准确**（`app/domains/source/import_service.py:26,52`） |
| 正式链自包含 Seal + LLM，不消费 Papers manifest | ✅ **准确** |
| `preprocessing_consumer` 在 scripts（实验路径） | ✅ **准确** |
| Phase 1 Runner 成功 ≠ 正式 E2E | ✅ **准确** |
| **「官方 preprocessing 产物 → 正式 V3 输入」未打通** | ⚠️ **方向对，定性需修正**（见 §2） |

---

## 1. MIMO 定位正确的部分（已验证）

**① 扩展名白名单确实是门禁**

```python
# app/domains/source/import_service.py
L24: _IMPORT_DIR = Path("data/imports")
L26: _ALLOWED_EXTENSIONS = {".pdf", ".docx"}
L52:     if ext not in _ALLOWED_EXTENSIONS:
L53:         raise ImportError_(f"unsupported file type: {ext!r}; allowed: {sorted(_ALLOWED_EXTENSIONS)}")
```

且该服务 docstring 明确其边界：**"禁止：OCR、LLM、Resolver、Compiler、任何 pipeline 执行"**。

**② 正式链自提文本，不读 Papers 产物**

```python
# app/worker/__main__.py
L17: from app.ai.ocr.providers import NativeTextProvider
L96:     ocr_extractor=NativeTextProvider().extract,

# app/domains/source/seal.py docstring
L8-9: extractor 由调用方注入：native = `NativeTextProvider().extract`；
      cloud = `OCRGateway(mode...).extract`（段 B 真实运行只走 native）。
```

⇒ 正式链的文本来源是 **V3 自己的 Seal 从 PDF 提取**，与 Papers 的 OCR markdown 是**两条并行路径**。

**③ `preprocessing_consumer` 仅存在于 `scripts/`**

`app/` 下无任何引用（我此前已核）。✅

---

## 2. ⚠️ 需要修正的定性：源模型**认识** preprocessing 这个角色

这是复核查出的**反证**，它改变了断点的性质。

### 2.1 `role/provider` 闭集里明确有 preprocessing

```python
# app/models/source.py
L29: _ARTIFACT_KINDS = frozenset({"original_binary", "raw_l1", "canonical_l1"})

L31: _ROLE_PROVIDER_PAIRS: dict[str, frozenset[str]] = {
L32:     "native":         frozenset({"native"}),
L33:     "ocr_ppsv3":      frozenset({"ppsv3"}),
L34:     "ocr_ppsvl":      frozenset({"paddleocr-vl"}),
L35:     "docx":           frozenset({"docx"}),
L36:     "preprocessing":  frozenset({"preprocessing"}),      # ← 它在这里
L40:     "canonical":      frozenset({""}),
L41: }
```

**"preprocessing" 是 V3 官方源模型的一等公民**，与 native / ocr 并列。

### 2.2 实验 Runner 走的正是这个官方契约

```python
# scripts/preprocessing_consumer/runner_b2.py  L336-357
le_hash = logical_execution_hash(
    task_type="document_ingest",            # ← 正式 task_type，不是 phase0
    stage="seal",                           # ← 正式 stage
    contract_domain={"seal_contract_version": "seal/v1",
                     "parser": {"provider": "preprocessing", "role": "preprocessing"}},
    input_domain={"original_sha256": file_sha},
)
version = await src_repo.create_source_version(
    document_id=doc.id, artifact_kind="canonical_l1",
    role="preprocessing", provider="preprocessing",     # ← 官方角色
    body_text=body_text, body_hash=body_hash, ..., status="draft",
    logical_execution_stage="seal",
)
```

**它用的是 `document_ingest` + `seal/v1` + `canonical_l1` + 官方 preprocessing 角色，
并通过官方的 `SourceRepository.create_source_version` 写入。**

### 2.3 那"断点"到底在哪？

**在 import API 的扩展名白名单**，不在 V3 的能力或契约。

| 层 | 是否支持 preprocessing 产物 |
|----|---------------------------|
| `app/models/source.py`（角色闭集） | ✅ 支持（`preprocessing` 一等公民） |
| 持久化路径（`create_source_version`） | ✅ 支持（Runner 已在用） |
| **import API（`_ALLOWED_EXTENSIONS`）** | ❌ **不收 `.md` / manifest** |
| 正式编排（`TaskExecutor document_ingest`） | ❌ 走自提文本（native），未接 preprocessing 角色 |

⇒ **准确表述**：

> **不是「V3 无法消费预处理产物」，而是「正式摄入 API 只收 `.pdf/.docx`，
> 而 V3 的源模型与持久化层已经为 `preprocessing` 角色预留了一等公民位置，
> 只是没有任何正式入口把它接上」。**

这个差别很实际：
- 若是"能力缺失"，任务 B 要**新建**一整套 preprocessing 摄入能力（大工程）；
- 若是"入口未接"，任务 B 要回答的是一个**架构裁定问题**——
  **Owner 到底要不要让正式链消费预处理的 md/manifest？**

---

## 3. 因此任务 B 的真正第一问（建议替换 Round 1 的结论）

```text
Q-B1（架构裁定，非技术缺陷）
  正式链的文本来源应当是哪一个？
    (a) V3 自提（现状：NativeTextProvider 从 PDF 抽取）
    (b) 已验收的 preprocessing 产物（03_OWNER_ACCEPTED 的 md + manifest）
    (c) 两者并存（preprocessing 为 preferred，native 为 fallback）
```

**这个问题的答案决定后续全部工作**：

| 若选 | 则 |
|------|-----|
| (a) | 预处理产物**不进正式链**；`preprocessing` 角色仅服务实验路径。则"断点"不存在，Round 1 结论应改为"设计如此"。**但**：Owner 花在 Gate 1 上的人工验收就不会进入产品，需确认这是否可接受 |
| (b) | 需要：import API 扩白名单 + `TaskExecutor` 接 preprocessing 角色 + 跳过 Seal 的自提（或作为 seal 的一种 extractor） |
| (c) | 需定义优先级与回退条件 |

**我倾向认为这是 (b) 或 (c)**，依据是：
1. `preprocessing` 角色被写进**官方闭集**（不是实验代码）；
2. Runner 用 `task_type="document_ingest"` 而非 phase0 构造 LE hash —— 说明**设计意图里有一条正式的 preprocessing 摄入路**；
3. 否则 Owner 在 Gate 1 上的人工验收成果无法进入产品。

---

## 4. 一个仍未验证的相邻风险（建议 Round 2 带上）

`app/models/source.py` L38-39 有一条自述的**实现约定缺口**：

```python
# Spec 10 §4.2: "canonical role 无 provider" — DB 列 NOT NULL，约定空字符串。
# [NEW-GAP-3 登记] provider="" 是实现约定（Spec 未指定 NOT NULL 列的空 provider 存储值），
# 不是 Spec 声明。如 Owner 裁定其他约定，需同步修改此处与测试 fixture。
```

这与 preprocessing 摄入直接相关（preprocessing → canonical 的角色转换会碰到这条约定）。
Round 2 若往下走，这一条会被触发。

---

## 5. 状态与建议

```text
任务 A            : 验收通过（残余风险 R-A1 已登记，回退触发 3 处）
Q17 另案          : 建议扩为「manifest 选项声明异常」（Q17 / Q2 / U12-14）
任务 B Round 1    : 断点位置 ✅ 正确；定性 ⚠️ 需修正为「正式摄入入口未接」而非「V3 无法消费」
更精确的结论       : V3 源模型已有 preprocessing 一等公民角色；缺的是正式入口
未验证            : Seal→…→前端 下游（本轮未测，与 MIMO 一致）
```

**建议任务 B Round 2 的第一件事不是跑 PDF，而是拿到 Q-B1 的架构裁定**——
否则若答案是 (a)，跑完 PDF 得到的是"正式链能自提文本"，与"预处理产物能否进产品"无关。

**若你裁定直接跑 (a) 路径验证下游**，我建议同时记录：
该次运行**不经过** `preprocessing` 角色，因此**不能**作为"预处理产物进入产品链"的证据。

---

## 6. 本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `Docs/60_REPORTS/TASK-A-RESIDUAL-RISK-AND-TEST-FAILURES.md` | 上轮：残余风险 + 测试失败说明 |
| `Docs/60_REPORTS/TASK-A-ACCEPTANCE-VERIFICATION.md` | 任务 A 验收 |
| （本轮为代码阅读 + grep 取证，未新增脚本） | |
