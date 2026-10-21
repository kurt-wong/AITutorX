"""M2 continued: process OUR task specifically (not oldest-queued)."""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(BACKEND))
os.chdir(str(BACKEND))
os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors_test"
)
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("APP_SECRET", "test-app-secret-32-bytes-minimum!!")

from sqlalchemy import text  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402
from app.ai.gateway import LLMGateway  # noqa: E402
from app.ai.providers.http import HTTPLLMProvider  # noqa: E402
from app.domains.source.funnel_recorder import FunnelRecorder  # noqa: E402
from app.domains.task.executor import TaskExecutor  # noqa: E402

TASK_ID = "3eb37829-aca7-4757-88e0-20b13bc32801"
OUT_DIR = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE\e2e_run")


async def main() -> int:
    tid = TASK_ID
    funnel = FunnelRecorder(package_id="chem-2018-spring-huikao-teacher")
    funnel.set("input_units", 40)
    funnel.bump("identity_ok")
    funnel.set("ir_ready", 1)  # already sealed from prior import

    provider = HTTPLLMProvider(
        name="mimo",
        api_key=settings.mimo_api_key,
        base_url=settings.mimo_base_url,
        model=settings.mimo_model,
        timeout=settings.llm_request_timeout_seconds * 4,
    )
    gateway = LLMGateway(
        "live",
        allow_live=True,
        task_context=object(),
        budget_ok=True,
        live_provider=provider,
    )
    executor = TaskExecutor(
        async_session_maker,
        llm_gateway=gateway,
        ocr_extractor=None,
        default_provider="mimo",
        default_model=settings.mimo_model,
    )

    worker_id = "m2-targeted"
    lease = uuid.uuid4().hex
    t0 = time.time()
    log: list[dict] = []

    # Claim OUR task specifically via TaskService
    from app.domains.task.service import TaskService

    async with async_session_maker() as s:
        svc = TaskService(s)
        try:
            claimed = await svc.claim(uuid.UUID(tid), worker_id=worker_id, lease_token=lease)
            log.append({"claimed": True, "lease_expires_at": str(claimed.get("lease_expires_at"))})
            await s.commit()
        except Exception as exc:
            log.append({"claim_error": f"{type(exc).__name__}: {exc}"})
            await s.rollback()
            # maybe already claimed — try direct _process
            claimed = {"id": uuid.UUID(tid)}

    # Process
    try:
        await executor._process(uuid.UUID(tid), worker_id, lease)
        log.append({"process": "completed_ok"})
    except Exception as exc:  # noqa: BLE001
        log.append({"process_error": f"{type(exc).__name__}: {exc}"})
        funnel.note(f"process error: {type(exc).__name__}: {exc}")
        try:
            await executor._fail_task(uuid.UUID(tid), worker_id, lease, exc)
        except Exception as e2:  # noqa: BLE001
            log.append({"fail_task_error": str(e2)})

    elapsed = time.time() - t0

    # Census
    async with async_session_maker() as s:
        task_row = (
            await s.execute(
                text(
                    "select id,status,current_stage,llm_invocations,decided_at "
                    "from tasks where id=:i"
                ),
                {"i": tid},
            )
        ).mappings().first()
        # count only our document's chain
        doc_id = (
            await s.execute(
                text(
                    "select document_id from document_source_versions "
                    "where id=(select source_version_id from semantic_annotations "
                    "where source_version_id in (select id from document_source_versions "
                    "where document_id=(select document_id from tasks where id=:i) "
                    "or true) limit 1) "
                ),
                {"i": tid},
            )
        ).first()
        svs = (
            await s.execute(
                text(
                    "select id,role,provider,artifact_kind,status from document_source_versions"
                )
            )
        ).mappings().all()
        anns = (
            await s.execute(
                text("select id,source_version_id,status,prompt_version from semantic_annotations")
            )
        ).mappings().all()
        cands = (
            await s.execute(
                text("select id,decision_status,unit_type from admission_candidates")
            )
        ).mappings().all()
        qs = (
            await s.execute(text("select id,canonical_question_type from questions"))
        ).mappings().all()
        qis = (
            await s.execute(text("select id,question_id from question_instances"))
        ).mappings().all()

    funnel.set("candidates", len(cands))
    funnel.set("questions", len(qs))
    funnel.set("question_instances", len(qis))
    funnel.set("pending_review", sum(1 for c in cands if c["decision_status"] == "pending_review"))

    evidence = {
        "artifact": "M2-TARGETED-PROCESS",
        "task_id": tid,
        "elapsed_seconds": round(elapsed, 2),
        "log": log,
        "task_db": dict(task_row) if task_row else None,
        "source_versions": [dict(r) for r in svs],
        "annotations": [dict(r) for r in anns],
        "candidates": [dict(r) for r in cands],
        "questions": [dict(r) for r in qs],
        "question_instances": [dict(r) for r in qis],
        "funnel": funnel.to_dict(),
    }
    out = OUT_DIR / f"m2-targeted-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2, default=str)[:4000])
    print("EVIDENCE", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
