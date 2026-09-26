"""FORMAL-E2E-ENABLEMENT-01 Level 1 retry: physics teacher-edition PDF with exact
frozen explanation headers (【详解】 standalone lines).
"""
from __future__ import annotations

import asyncio, hashlib, json, os, sys, uuid
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(BACKEND))
os.chdir(str(BACKEND))

from sqlalchemy import text
from app.ai.gateway import build_gateway
from app.ai.ocr.providers import NativeTextProvider
from app.ai.provider_reality import default_tracker
from app.db.session import async_session_maker
from app.domains.source.import_service import DocumentImportService
from app.domains.task.executor import TaskExecutor
from app.models.content import Question, QuestionInstance

PDF = Path(r"D:\Project\Papers\maintainess\PDF\2018北京一零一中高一分班考物理（教师版）(1).pdf")
OUT_DIR = Path(r"D:\Project\AITutor-X\e2e_run")

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

async def main() -> int:
    assert PDF.exists()
    doc_sha = sha256_file(PDF)
    file_bytes = PDF.read_bytes()
    started_at = datetime.now(timezone.utc).isoformat()
    evidence = {
        "task_id": "FORMAL-E2E-ENABLEMENT-01",
        "level": "L1-single-document",
        "run": "b-physics-teacher-edition",
        "started_at": started_at,
        "pdf_path": str(PDF),
        "document_sha256": doc_sha,
        "document_bytes": len(file_bytes),
        "provider_target": {"provider": "mimo", "model": "mimo-v2.6-pro"},
    }

    async with async_session_maker() as s:
        service = DocumentImportService(s)
        document, task, is_new = await service.import_file(
            file_bytes=file_bytes, file_name=PDF.name, created_by="formal-e2e-l1b"
        )
        await s.commit()
        import_task_id = task.id if task else None
        evidence["import"] = {
            "document_id": str(document.id),
            "task_id": str(import_task_id),
            "is_new": is_new,
            "original_sha256": document.original_sha256,
        }
        print("INGEST", evidence["import"])

    gateway = build_gateway(allow_live=True)
    executor = TaskExecutor(
        async_session_maker, llm_gateway=gateway,
        ocr_extractor=NativeTextProvider().extract,
        default_provider="mimo", default_model="mimo-v2.6-pro",
    )
    worker_id = f"formal-e2e-l1b-{uuid.uuid4().hex[:8]}"
    processed = 0
    while await executor.run_once(worker_id=worker_id):
        processed += 1
    evidence["worker"] = {"worker_id": worker_id, "processed": processed}
    print("WORKER processed", processed)

    async with async_session_maker() as s:
        if import_task_id:
            trow = (await s.execute(text(
                'SELECT id, status, llm_invocations FROM tasks WHERE id=:i'
            ), {"i": import_task_id})).mappings().first()
            evidence["task_row"] = dict(trow) if trow else None

        sv = (await s.execute(text(
            "SELECT id, status, body_hash, line_count FROM document_source_versions WHERE document_id=:d"
        ), {"d": document.id})).mappings().first()
        evidence["source_version"] = dict(sv) if sv else None

        anns = (await s.execute(text(
            "SELECT id, status, model_config_hash FROM semantic_annotations"
        ))).mappings().all()
        evidence["annotations"] = [dict(a) for a in anns]

        # check IR completeness via annotation payload unit count
        if anns:
            ap = (await s.execute(text(
                "SELECT payload FROM semantic_annotations WHERE id=:i"
            ), {"i": anns[-1]["id"]})).scalar()
            if isinstance(ap, str):
                ap = json.loads(ap)
            evidence["annotation_unit_count"] = len(ap.get("semantic_units") or [])

        cands = (await s.execute(text(
            "SELECT id, decision_status FROM admission_candidates"
        ))).mappings().all()
        evidence["admission_candidates"] = [dict(c) for c in cands]

        n_q = (await s.execute(text("SELECT count(*) FROM questions"))).scalar()
        n_i = (await s.execute(text("SELECT count(*) FROM question_instances"))).scalar()
        n_m = (await s.execute(text("SELECT count(*) FROM materials"))).scalar()
        evidence["final_objects"] = {
            "questions": n_q, "question_instances": n_i, "materials": n_m,
            "semantic_annotations": len(anns),
            "admission_candidates": len(cands),
        }

        audits = (await s.execute(text(
            'SELECT provider, model, status, start, "end", input_tokens, output_tokens, total_tokens, estimated_cost, error_type FROM llm_call_audit WHERE provider=:p ORDER BY start'
        ), {"p": "mimo"})).mappings().all()
        evidence["llm_call_audit_mimo"] = [dict(a) for a in audits]

    default_tracker._output_path = OUT_DIR / "provider-reality-level1b.json"
    default_tracker.flush()
    evidence["provider_reality"] = [r.to_dict() for r in default_tracker.records]
    evidence["finished_at"] = datetime.now(timezone.utc).isoformat()

    out = OUT_DIR / "formal-e2e-level1b.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("EVIDENCE", out)
    print(json.dumps(evidence["final_objects"], indent=2))
    ok = n_q >= 1 and n_i >= 1
    print("LEVEL1B:", "PASS" if ok else "INCOMPLETE")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
