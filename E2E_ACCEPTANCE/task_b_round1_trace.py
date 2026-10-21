from pathlib import Path
import json, hashlib
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")

# capture file hashes of key formal-chain modules
files = [
    r"D:\Project\AITutors-v3\backend\app\domains\source\import_service.py",
    r"D:\Project\AITutors-v3\backend\app\domains\task\executor.py",
    r"D:\Project\AITutors-v3\backend\app\domains\source\quality.py",
    r"D:\Project\AITutors-v3\backend\app\domains\source\seal.py",
    r"D:\Project\AITutors-v3\backend\app\api\routers\documents.py",
]
hashes = {}
for f in files:
    p = Path(f)
    if p.exists():
        hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]

report = {
    "task": "B — formal product-chain E2E (Round 1: locate first unconnected link)",
    "status": "ROUND1_COMPLETE_NO_FIX",
    "authorized_boundaries": {
        "formal_entry_first": True,
        "no_phase1_substitution": True,
        "no_production_fix_round1": True,
        "keep_task_a_baseline": True,
        "layer_evidence": True,
    },
    "formal_chain_map": [
        {"layer": "API import", "code": "app/api/routers/documents.py → DocumentImportService.import_file",
         "input": "file_bytes + file_name", "output": "Document + Task(queued)"},
        {"layer": "Import contract", "code": "import_service.py:_ALLOWED_EXTENSIONS",
         "input": "extension check", "output": "allowed = .pdf .docx ONLY"},
        {"layer": "TaskExecutor", "code": "task/executor.py:run_once → _process",
         "input": "task_params.file_path", "output": "staged pipeline"},
        {"layer": "1 Seal", "code": "source/seal.py SealService.seal_document",
         "input": "file bytes", "output": "DocumentSourceVersion (sealed text)"},
        {"layer": "2 Quality", "code": "source/quality.py SourceQualityGate",
         "input": "sealed body_text", "output": "valid|degraded|invalid|ocr_required"},
        {"layer": "3 Annotation", "code": "annotation/service.py + LLM prompt",
         "input": "sealed text", "output": "SemanticAnnotation (LLM)"},
        {"layer": "4 Compile+Gate", "code": "gate/service.py GateService.run",
         "input": "annotation + resolved", "output": "candidates / skipped"},
        {"layer": "5 DB", "code": "Admission / Question materialization",
         "input": "gate_decision=auto_approve", "output": "Question rows"},
        {"layer": "6 Frontend", "code": "AITutors-v3/frontend",
         "input": "DB / API", "output": "user-visible questions"},
    ],
    "FIRST_UNCONNECTED_LINK": {
        "name": "Preprocessing product → Formal V3 input",
        "evidence": [
            "import_service.py:26 _ALLOWED_EXTENSIONS = {'.pdf', '.docx'}",
            "Official preprocessing outputs are .md + *.manifest.json under Papers/Ocr-markdown",
            "TaskExecutor _seal_stage requires task_params.file_path (raw file bytes), then extracts text itself",
            "preprocessing_consumer lives in backend/scripts (experimental task_type=preprocessing_consumer_phase0), NOT on TaskExecutor document_ingest path",
            "No API/contract accepts Ocr-markdown MD or Papers manifest as formal input",
        ],
        "layer_enum": "Integration / import contract gap",
        "not_yet_tested_downstream": [
            "Seal→Quality→Annotation→Gate→DB→Frontend on a PDF that formal chain CAN accept",
            "Whether LLM Annotation quality is sufficient for exam questions",
        ],
    },
    "what_this_proves": (
        "Formal chain is PDF/DOCX-first and self-contains Seal+LLM Annotation. "
        "It does NOT currently consume official preprocessing MD/manifest. "
        "Therefore Phase 1 manifest Runner success cannot substitute formal E2E."
    ),
    "what_this_does_NOT_prove": (
        "Does not prove Seal/Annotation/Gate/DB/Frontend work on real papers; "
        "those layers were not executed this round."
    ),
    "layer_input_output_hashes": hashes,
    "task_a_baseline_preserved": True,
    "q17_q20_ocr_boundaries": "unchanged, separate cases",
}
(OUT / "TASK_B_ROUND1_CHAIN_TRACE.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

md = f"""# 任务 B Round 1 — 正式产品链定位 · 首个未打通环节

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
| **证据** | `_ALLOWED_EXTENSIONS = {{'.pdf','.docx'}}`；官方产物是 `.md`+`.manifest.json`；TaskExecutor 自己 Seal+LLM 标注，**不消费** Papers manifest；`preprocessing_consumer` 在 scripts（实验路径） |

**结论**：正式链是 **PDF/DOCX 优先、自包含 Seal+LLM Annotation**。当前**没有**接口把官方 OCR Markdown / manifest 接进去。  
⇒ Phase 1 Runner 成功 **不能** 顶替正式 E2E。

## 本轮证明 / 未证明
**证明**：正式入口与预处理产物之间存在契约断点。  
**未证明**：Seal→…→Frontend 在真实 PDF 上能否跑通（本轮未执行下游）。

## 逐层哈希
{json.dumps(hashes, ensure_ascii=False, indent=2)}

## 边界遵守
- 未改任何生产逻辑
- 未用 Phase 1 顶替
- 任务 A 基线保留；Q17/Q20/OCR 另案不变

## 下轮建议（待授权）
用**正式链可接收的 PDF** 跑通 Seal→Quality→Annotation→Gate→DB→前端，逐层留证；若 LLM Annotation 不足，再列最小缺口，不顺手修。
"""
(OUT / "TASK_B_ROUND1_CHAIN_TRACE.md").write_text(md, encoding="utf-8")
print("wrote TASK_B_ROUND1_CHAIN_TRACE.{json,md}")
print("hashes", hashes)
