# 任务 B Round 1 — 正式产品链定位 · 首个未打通环节

## 正式链（实测代码路径）

```text
API documents.py
  → DocumentImportService.import_file   【仅 .pdf / .docx】
  → Task(document_ingest, queued)
  → TaskExecutor.run_once
      → _seal_stage        SealService（从 PDF bytes 提文本）
      → _quality_check     SourceQualityGate（ocr_required 会 fail-loud）
      → _annotation_stage  AnnotationService + LLM（自有提示词）
      → _compile_stage     GateService（Admission 收口）
  → DB / Frontend
```

## 🔴 首个未打通环节

| | |
|--|--|
| **环节** | **Preprocessing 产物 → 正式 V3 输入** |
| **性质** | Integration / import 契约缺口 |
| **证据** | `_ALLOWED_EXTENSIONS = {'.pdf','.docx'}`；官方产物是 `.md`+`.manifest.json`；TaskExecutor 自己 Seal+LLM 标注，**不消费** Papers manifest；`preprocessing_consumer` 在 scripts（实验路径） |

**结论**：正式链是 **PDF/DOCX 优先、自包含 Seal+LLM Annotation**。当前**没有**接口把官方 OCR Markdown / manifest 接进去。  
⇒ Phase 1 Runner 成功 **不能** 顶替正式 E2E。

## 本轮证明 / 未证明
**证明**：正式入口与预处理产物之间存在契约断点。  
**未证明**：Seal→…→Frontend 在真实 PDF 上能否跑通（本轮未执行下游）。

## 逐层哈希
{
  "import_service.py": "ff3e3dae1433abc0",
  "executor.py": "c5f164aa5935d775",
  "quality.py": "b0569d0d55af1bdf",
  "seal.py": "35aeee12ca2027c1",
  "documents.py": "9dccde7da1994c13"
}

## 边界遵守
- 未改任何生产逻辑
- 未用 Phase 1 顶替
- 任务 A 基线保留；Q17/Q20/OCR 另案不变

## 下轮建议（待授权）
用**正式链可接收的 PDF** 跑通 Seal→Quality→Annotation→Gate→DB→前端，逐层留证；若 LLM Annotation 不足，再列最小缺口，不顺手修。
