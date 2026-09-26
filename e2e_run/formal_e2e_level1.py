"""FORMAL-E2E-ENABLEMENT-01 Level 1: single real PDF through formal pipeline.

Formal entries only:
  ingest: DocumentImportService.import_file  (same as POST /api/documents/import)
  worker: python -m app.worker run --allow-live

No fake provider, no bypass authorization, no dummy context.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(BACKEND))
os.chdir(str(BACKEND))

from sqlalchemy import select, text  # noqa: E402

from app.ai.gateway import build_gateway  # noqa: E402
from app.ai.ocr.providers import NativeTextProvider  # noqa: E402
from app.ai.provider_reality import default_tracker  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402
from app.domains.source.import_service import DocumentImportService  # noqa: E402
from app.domains.task.executor import TaskExecutor  # noqa: E402
from app.domains.task.service import TaskService  # noqa: E402
from app.models.content import Question, QuestionInstance  # noqa: E402
from app.models.snapshot import AdmissionCandidate, SemanticAnnotation  # noqa: E402
from app.models.source import Document, DocumentSourceVersion  # noqa: E402

PDF = Path(r"D:\Project\Papers\maintainess\PDF\2021北京高三二模数学汇编：集合（教师版）.pdf")
OUT_DIR = Path(r"D:\Project\AITutor-X\e2e_run")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


async def main() -> int:
    assert PDF.exists(), f"PDF missing: {PDF}"
    doc_sha = sha256_file(PDF)
    file_bytes = PDF.read_bytes()
    started_at = datetime.now(timezone.utc).isoformat()

    evidence: dict = {
        "task_id": "FORMAL-E2E-ENABLEMENT-01",
        "level": "L1-single-document",
        "started_at": started_at,
        "pdf_path": str(PDF),
        "document_sha256": doc_sha,
        "document_bytes": len(file_bytes),
        "formal_entries": {
            "ingest": "DocumentImportService.import_file (== POST /api/documents/import)",
            "worker": "python -m app.worker run --allow-live  (TaskExecutor.run_once)",
        },
        "peak_time_policy": "Beijing workday 08:00-12:00/14:00-18:00 => MIMO only (DeepSeek forbidden)",
        "provider_target": {"provider": "mimo", "model": "mimo-v2.6-pro"},
    }

    # ---- 1. Formal ingest ----
    async with async_session_maker() as s:
        service = DocumentImportService(s)
        document, task, is_new = await service.import_file(
            file_bytes=file_bytes,
            file_name=PDF.name,
            created_by="formal-e2e-l1",
        )
        await s.commit()
        import_task_id = task.id if task else None
        evidence["import"] = {
            "document_id": str(document.id),
            "task_id": str(import_task_id) if import_task_id else None,
            "is_new": is_new,
            "original_sha256": document.original_sha256,
        }
        print("INGEST OK", evidence["import"])

    # ---- 2. Formal worker (allow-live = documented human authorization param) ----
    # Worker CLI equivalent: build_gateway(allow_live=True) + TaskExecutor.run_once
    # TaskExecutor authorizes gateway from real claimed task + budget ensure.
    gateway = build_gateway(allow_live=True)
    executor = TaskExecutor(
        async_session_maker,
        llm_gateway=gateway,
        ocr_extractor=NativeTextProvider().extract,
        default_provider="mimo",
        default_model="mimo-v2.6-pro",
    )
    worker_id = f"formal-e2e-l1-{uuid.uuid4().hex[:8]}"
    processed = 0
    while await executor.run_once(worker_id=worker_id):
        processed += 1
    evidence["worker"] = {"worker_id": worker_id, "processed_tasks": processed}
    print("WORKER DONE processed=", processed)

    # ---- 3. Collect DB evidence ----
    async with async_session_maker() as s:
        # task status
        if import_task_id:
            trow = (await s.execute(
                text("SELECT id, status, task_type, llm_invocations, current_stage FROM tasks WHERE id=:i"),
                {"i": import_task_id},
            )).mappings().first()
            evidence["task_row"] = dict(trow) if trow else None

        # source version
        sv = (await s.execute(
            text(
                "SELECT id, status, body_hash, integrity_hash, line_count, page_count "
                "FROM document_source_versions WHERE document_id=:d ORDER BY created_at DESC LIMIT 1"
            ),
            {"d": document.id},
        )).mappings().first()
        evidence["source_version"] = dict(sv) if sv else None

        # annotation
        anns = (await s.execute(
            text(
                "SELECT id, status, model_config_hash, prompt_version, annotation_schema_version "
                "FROM semantic_annotations ORDER BY created_at DESC LIMIT 5"
            )
        )).mappings().all()
        evidence["annotations"] = [dict(a) for a in anns]

        # admission candidates
        cands = (await s.execute(
            text(
                "SELECT id, decision_status, unit_id FROM admission_candidates "
                "ORDER BY created_at DESC LIMIT 10"
            )
        )).mappings().all()
        evidence["admission_candidates"] = [dict(c) for c in cands]

        # questions / instances
        n_q = (await s.execute(select(Question))).scalars().all()
        n_i = (await s.execute(select(QuestionInstance))).scalars().all()
        evidence["final_objects"] = {
            "questions": len(n_q),
            "question_instances": len(n_i),
            "materials": (
                await s.execute(text("SELECT count(*) FROM materials"))
            ).scalar(),
            "semantic_annotations": (
                await s.execute(text("SELECT count(*) FROM semantic_annotations"))
            ).scalar(),
            "admission_candidates": (
                await s.execute(text("SELECT count(*) FROM admission_candidates"))
            ).scalar(),
        }

        # LLM audit (provider reality)
        audits = (await s.execute(
            text(
                "SELECT request_id, provider, model, status, start, end, "
                "input_tokens, output_tokens, total_tokens, estimated_cost, error_type "
                "FROM llm_call_audit ORDER BY start"
            )
        )).mappings().all()
        evidence["llm_call_audit"] = [dict(a) for a in audits]

        # budget
        budgets = (await s.execute(
            text("SELECT account_dim, scope_id, stage, used, reserved FROM budget")
        )).mappings().all()
        evidence["budget"] = [dict(b) for b in budgets]

    # ---- 4. Provider reality sidecar ----
    default_tracker._output_path = OUT_DIR / "provider-reality-level1.json"
    default_tracker.flush()
    evidence["provider_reality_file"] = str(OUT_DIR / "provider-reality-level1.json")
    evidence["provider_reality_records"] = [r.to_dict() for r in default_tracker.records]

    evidence["finished_at"] = datetime.now(timezone.utc).isoformat()
    evidence["gateway_last_actual_provider"] = gateway.last_actual_provider

    out = OUT_DIR / "formal-e2e-level1.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("EVIDENCE WRITTEN", out)

    # Summary gate
    ok = (
        evidence["final_objects"]["questions"] >= 1
        and evidence["final_objects"]["question_instances"] >= 1
    )
    print("LEVEL1 RESULT:", "PASS" if ok else "INCOMPLETE")
    print(json.dumps(evidence["final_objects"], indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
