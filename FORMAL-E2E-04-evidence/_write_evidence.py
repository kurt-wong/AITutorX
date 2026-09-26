import hashlib, json, platform, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

EV = Path(r"D:\Project\AITutor-X\FORMAL-E2E-04-evidence")
BACKEND = Path(r"D:\Project\AITutors-v3\backend")

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git_head(repo: Path) -> str:
    r = subprocess.run(["git","rev-parse","HEAD"], cwd=str(repo), capture_output=True, text=True)
    return r.stdout.strip()

# 00 environment
spec = {}
for name in ("00_Master_Spec.md","10_Data_Model.md","20_Document_Pipeline.md",
             "30_Task_LLM_Safety.md","40_Development_Rules.md","50_Migration_Assets.md"):
    p = Path(r"D:\Project\AITutors-v3\Docs\V3_SPEC")/name
    if p.exists():
        spec[name] = sha(p)

env_txt = f"""FORMAL-E2E-04 environment
generated_at: {now()}
platform: {platform.platform()}
python: {sys.version.split()[0]}

GIT HEAD
  AITutors-v3            : {git_head(Path(r'D:\Project\AITutors-v3'))}
  Papers                 : {git_head(Path(r'D:\Project\Papers'))}
  AITutor-X              : {git_head(Path(r'D:\Project\AITutor-X'))}
  Aitutors-preprocessing : NO .git (working tree only; not a git repo)

V3_SPEC SHA256
{json.dumps(spec, indent=2)}

WORKING TREE (uncommitted noted; Frozen Spec untouched)
  AITutors-v3: pre-existing untracked COORDINATION docs only (not modified this task)

FORMAL ENTRIES USED
  preprocessing : python reslice_pipeline.py --file <source.md> --out <dir>
                  (Aitutors-preprocessing/scripts/reslice_pipeline.py)
  V3 consumer   : python -m scripts.preprocessing_consumer.runner --corpus <dir> --output <json>
                  (AITutors-v3/backend/scripts/preprocessing_consumer/runner.py)
  NOT USED as production path: POST /api/documents/import + app.worker (PDF self-parse boundary)

PROVIDER
  configured: mimo / mimo-v2.6-pro
  peak-time policy: DeepSeek forbidden workday 08:00-12:00 / 14:00-18:00
  run local time Beijing: 2026-09-27 00:28 (outside peak; MIMO used anyway)
"""
(EV/"00_environment.txt").write_text(env_txt, encoding="utf-8")

# 01 preprocessing input
pdf = Path(r"D:\Project\Papers\maintainess\PDF\2022北京丰台高一（下）期末历史（教师版）(1).pdf")
md  = Path(r"D:\Project\Papers\Ocr-markdown\高一\历史\2022北京丰台高一（下）期末历史（教师版）(1).md")
# page count via pypdf if available
pages = None
try:
    from pypdf import PdfReader
    pages = len(PdfReader(str(pdf)).pages)
except Exception:
    try:
        import fitz
        pages = fitz.open(str(pdf)).page_count
    except Exception:
        pages = "unknown"

inp = {
    "selected_sample": {
        "role": "standalone + composite + material candidate",
        "pdf_path": str(pdf),
        "pdf_sha256": sha(pdf),
        "pdf_bytes": pdf.stat().st_size,
        "page_count": pages,
        "source_markdown_path": str(md),
        "source_markdown_sha256": sha(md),
        "source_markdown_bytes": md.stat().st_size,
        "source_markdown_lines": len(md.read_text(encoding="utf-8", errors="ignore").splitlines()),
        "selection_rationale": "existing real exam PDF + existing OCR markdown; no manual PDF/manifest fabrication",
    },
    "formal_entry": "python reslice_pipeline.py --file <source.md> --out FORMAL-E2E-04-evidence/preproc_out",
    "provider_env": {"LLM_PROVIDER": "mimo", "MIMO_MODEL": "mimo-v2.6-pro",
                     "MIMO_BASE_URL": "https://api.xiaomimimo.com/v1", "MIMO_API_KEY": "PRESENT(not recorded)"},
}
(EV/"01_preprocessing_input.json").write_text(json.dumps(inp, ensure_ascii=False, indent=2), encoding="utf-8")

# 02 preprocessing output
out_dir = EV/"preproc_out"
man = next(out_dir.glob("*.manifest.json"))
md_out = next(out_dir.glob("*.md"))
ann_md = next(out_dir.glob("*.annotated.md"))
d = json.loads(man.read_text(encoding="utf-8"))
units = d.get("units") or []
types = {}
mats = 0
figs = 0
for u in units:
    types[u.get("unit_type")] = types.get(u.get("unit_type"), 0)+1
    if u.get("material_lines"):
        mats += 1
    if u.get("figure_lines") or u.get("figures"):
        figs += 1

outp = {
    "formal_entry": "reslice_pipeline.py --file ... --out ...",
    "exit": "success (units=30 validation_issues=0 warnings=0)",
    "artifacts": {
        "manifest": {"path": str(man), "sha256": sha(man), "bytes": man.stat().st_size},
        "markdown_sliced": {"path": str(md_out), "sha256": sha(md_out), "bytes": md_out.stat().st_size},
        "annotated_md": {"path": str(ann_md), "sha256": sha(ann_md), "bytes": ann_md.stat().st_size},
    },
    "units": {"total": len(units), "by_type": types, "with_material_lines": mats, "with_figure_fields": figs},
    "model_declared": d.get("model"),
    "prompt_version": (d.get("annotation_meta") or {}).get("prompt_version"),
    "identity_fields": {
        "source_content_sha256": d.get("source_content_sha256"),
        "identity_version": d.get("identity_version"),
    },
    "llm_call": {
        "provider": "mimo",
        "model": d.get("model"),
        "timestamp_utc": now(),
        "token_usage": "NOT PERSISTED by reslice_pipeline (call_llm returns usage but pipeline does not write llm_call_audit)",
        "note": "preprocessing has no llm_call_audit equivalent; model tag from manifest only",
    },
}
(EV/"02_preprocessing_output.json").write_text(json.dumps(outp, ensure_ascii=False, indent=2), encoding="utf-8")

# 03 consumer mapping
c1 = json.loads((EV/"consumer-report.json").read_text(encoding="utf-8"))
c2 = json.loads((EV/"consumer-report-identity-ok.json").read_text(encoding="utf-8"))
mapping = {
    "consumer_entry": "python -m scripts.preprocessing_consumer.runner --corpus ... --output ...",
    "path_A_fresh_reslice_output": {
        "artifact": str(man),
        "interface_scope": c1.get("papers",[{}])[0].get("interface_scope_rejected"),
        "result": "BLOCKED before Track A/B",
    },
    "path_B_identity_complete_real_artifact": {
        "artifact": r"D:\Project\Papers\Ocr-markdown\reslice-batch-C\会考\历史\2018北京夏季高中会考历史（教师版）(1).manifest.json",
        "why": "real producer artifact WITH source_content_sha256 (not hand-crafted); used to verify consumer mapping + V3 semantic path",
        "interface_scope": "accepted",
        "track_a": c2.get("papers",[{}])[0].get("track_a"),
        "track_b": c2.get("papers",[{}])[0].get("track_b"),
    },
    "mapping_checks": {
        "standalone_question -> standalone_unit": "PERFORMED by annotation_adapter (canonical OD-2)",
        "composite_question -> composite_unit": "PERFORMED by annotation_adapter",
        "shared_material preserved": "shared_components.material role; NOT merged into stem (adapter code)",
        "sub_questions preserved": "1:1 deterministic translation (GAP_SUB_QUESTION_DECOMPOSITION registered)",
        "source lineage": "source_content_sha256 retained verbatim when present; path never used as identity",
    },
    "consumer_persistence": {
        "runner_always_rollback": True,
        "evidence": "scripts/preprocessing_consumer/runner.py run_corpus finally: await session.rollback()",
        "impact": "Track A/B validate mapping in-transaction then discard; NO persistent V3 ingest of preprocessing artifacts exists",
    },
}
(EV/"03_consumer_mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")

# 04 v3 execution log (summary of formal consumer runs)
log = f"""FORMAL-E2E-04 V3 consumer execution log
generated_at: {now()}

=== RUN 1: fresh reslice_pipeline output (formal preprocessing) ===
command: python -m scripts.preprocessing_consumer.runner --corpus .../preproc_out --output consumer-report.json
result: Found 1 manifests / Interface Scope blocked: 1 / Track A: 0/1 / Track B: 0/1
FIRST BLOCKING (formal chain): MISSING_IDENTITY
  reason: Manifest does not declare source_content_sha256;
          cross-system identity cannot be established (path must never be used as identity).
  downstream_executed: false

=== RUN 2: identity-complete real producer artifact ===
command: python -m scripts.preprocessing_consumer.runner --corpus .../consumer_input_identity_ok --output consumer-report-identity-ok.json
result: Interface Scope blocked: 0 / Track A: 1/1 completed / Track B: 1/1 completed
  track_b spans_constructed=212 spans_failed=0
  track_a candidates_created=0 skipped=53/53 (ALL units)
  gate_pass=0 gate_rejected=0 pending_review=0
  persistence: session.rollback() — no rows committed

=== NOT USED (wrong production boundary per task) ===
POST /api/documents/import + python -m app.worker run  (V3 self-parse PDF path)

=== API / Frontend read path ===
Question API     : NOT IMPLEMENTED
Material API     : NOT IMPLEMENTED
Instance API     : NOT IMPLEMENTED
Present read API : GET /api/documents/{id}, source-lines, source-quality, GET /api/candidates/{id}
"""
(EV/"04_v3_execution.log").write_text(log, encoding="utf-8")

# 07 pipeline summary
summary = {
    "task": "FORMAL-E2E-04",
    "generated_at": now(),
    "outcome": "BLOCKED",
    "pipeline_status": {
        "PDF->Preprocessing": {"status": "PASS", "evidence": "02_preprocessing_output.json; units=30 model=mimo-v2.6-pro"},
        "Preprocessing Artifact": {"status": "PARTIAL", "evidence": "manifest lacks source_content_sha256/identity_version (fresh formal output)"},
        "Consumer": {"status": "BLOCKED_FOR_FRESH_OUTPUT", "evidence": "MISSING_IDENTITY; identity-ok historical artifact accepted"},
        "Annotation": {"status": "PASS_ON_IDENTITY_OK", "evidence": "adapter payload + SemanticAnnotation created in Track A transaction"},
        "Resolver": {"status": "EXECUTED_IN_TRACK_A", "evidence": "GateService internally resolves; NOT re-executed for this report"},
        "IR": {"status": "INCOMPLETE_UNITS", "evidence": "53/53 units skipped by Gate (incomplete IR)"},
        "Admission": {"status": "NOT_REACHED", "evidence": "0 candidates from consumer path"},
        "Frontend": {"status": "NOT IMPLEMENTED", "evidence": "no Question/Material/Instance API"},
    },
    "first_blocking_point": {
        "stage": "Preprocessing artifact -> V3 Consumer Interface Scope",
        "error": "MISSING_IDENTITY: Manifest does not declare source_content_sha256",
        "source": "scripts/preprocessing_consumer/boundary.enforce_interface_scope",
        "cause": "formal reslice_pipeline.py does not emit source_content_sha256/identity_version; historical set was backfilled by one-shot interface_scope_step2_backfill.py (not formal pipeline)",
    },
    "second_blocking_point": {
        "stage": "Consumer Track A Gate/IR",
        "error": "53/53 units skipped (semantic_status incomplete)",
        "note": "adapter known gaps: option per-label spans unavailable; choice units cannot be ready",
    },
    "architecture_boundary_note": {
        "pdf_import_path": "EXISTS but is NOT the Frozen Spec production boundary for this task; not used as E2E entry",
        "consumer_runner": "verification harness with mandatory rollback; not a persistent production ingest",
    },
    "findings_count": 5,
}
(EV/"07_pipeline_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print("evidence written")
for p in sorted(EV.iterdir()):
    if p.is_file():
        print(p.name, p.stat().st_size)
