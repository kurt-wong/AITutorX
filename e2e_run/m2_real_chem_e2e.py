"""M2 real-paper E2E via formal consumption entry (NOT experimental runner).

Flow:
  load_package_from_dir -> PreprocessingImportService.import_package
    -> Seal(preprocessing) -> Task(queued)
  TaskExecutor.run_once  (live MIMO Annotation -> Gate -> Admission)

Scope: chemistry 2018 paper, verify funnel + DB content. Live LLM authorized.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(BACKEND))
os.chdir(str(BACKEND))

os.environ.setdefault("APP_ENV", "test")
# Use isolated test DB for this run; shared business DB must stay untouched.
os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors_test"
)
os.environ.setdefault("APP_SECRET", "test-app-secret-32-bytes-minimum!!")

from sqlalchemy import text  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402
from app.ai.gateway import LLMGateway  # noqa: E402
from app.ai.providers.http import HTTPLLMProvider  # noqa: E402
from app.domains.source.funnel_recorder import FunnelRecorder  # noqa: E402
from app.domains.source.preprocessing_import import (  # noqa: E402
    PreprocessingImportService,
    load_package_from_dir,
)
from app.domains.task.executor import TaskExecutor  # noqa: E402

PKG = Path(
    r"D:\Project\AITutor-X\E2E_ACCEPTANCE\06_M1_PACKAGES\chem-2018-spring-huikao-teacher"
)
OUT_DIR = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE\e2e_run")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Verify-only first 8 Producer units for funnel reconciliation
VERIFY_UNIT_PREFIX = tuple(f"Q{i}" for i in range(1, 9))


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


async def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    pdf_sha = sha256_file(PKG / "paper.pdf")
    md_sha = sha256_file(PKG / "paper.md")

    funnel = FunnelRecorder(package_id="chem-2018-spring-huikao-teacher")
    evidence: dict = {
        "artifact": "M2-REAL-PAPER-E2E",
        "started_at": started,
        "repo": {
            "path": r"D:\Project\AITutors-v3",
            "branch": "od01-r3-convergence",
            "head": "d16a5e9+M1-fixes",
        },
        "package": {
            "path": str(PKG),
            "original_sha256": pdf_sha,
            "source_content_sha256": md_sha,
            "pairing_evidence": str(PKG / "PAIRING_EVIDENCE.json"),
        },
        "environment": {
            "database_url_db": "aitutors_test",
            "llm_gateway_mode": settings.llm_gateway_mode,
            "mimo_model": settings.mimo_model,
            "formal_entry": "PreprocessingImportService.import_package + TaskExecutor",
        },
        "live_llm": {
            "authorized": True,
            "scope": "3-10 questions (Q1-Q8 verify)",
            "budget_note": "1 document annotation call + gate; no retry storms",
        },
    }

    # ---- 1. Formal import (identity-verified) ----
    package = load_package_from_dir(PKG)
    funnel.note(f"loaded package md_bytes={len(package.source_md)}")

    async with async_session_maker() as s:
        svc = PreprocessingImportService(s)
        result = await svc.import_package(package=package, created_by="m2-e2e")
        await s.commit()

    evidence["import"] = {
        "document_id": str(result.document.id),
        "source_version_id": result.source_version_id,
        "task_id": result.task_id,
        "original_sha256": result.original_sha256,
        "source_content_sha256": result.source_content_sha256,
        "is_new": result.is_new,
    }
    funnel.set("input_units", 40)  # Producer manifest unit count
    funnel.bump("identity_ok")

    # ---- 2. Formal pipeline via TaskExecutor ----
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
        ocr_extractor=None,  # preprocessing mode uses source_md_path; no native extract
        default_provider="mimo",
        default_model=settings.mimo_model,
    )

    tid = result.task_id
    t0 = time.time()
    stage_log: list[dict] = []

    async with async_session_maker() as s:
        row = (
            await s.execute(text("select status from tasks where id=:i"), {"i": tid})
        ).first()
        initial_status = row.status if row else None
    stage_log.append({"phase": "before_run", "task_status": initial_status})

    for round_i in range(1, 6):
        async with async_session_maker() as s:
            row = (
                await s.execute(text("select status from tasks where id=:i"), {"i": tid})
            ).first()
            if row and row.status in ("succeeded", "failed"):
                break
        try:
            claimed = await executor.run_once(worker_id=f"m2-e2e-{round_i}")
            stage_log.append({"round": round_i, "claimed": bool(claimed)})
        except Exception as exc:  # noqa: BLE001
            stage_log.append(
                {
                    "round": round_i,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            funnel.note(f"run_once round {round_i} error: {type(exc).__name__}: {exc}")
            # do not retry storm — record and stop after first failure
            if round_i >= 2:
                break

    elapsed = time.time() - t0

    # ---- 3. DB census ----
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
        sv_rows = (
            await s.execute(
                text(
                    "select id,role,provider,artifact_kind,status,line_count "
                    "from document_source_versions where document_id=:d"
                ),
                {"d": result.document.id},
            )
        ).mappings().all()
        ann_rows = (
            await s.execute(
                text(
                    "select id,source_version_id,status from semantic_annotations"
                )
            )
        ).mappings().all()
        cand_rows = (
            await s.execute(
                text("select id,decision_status from admission_candidates")
            )
        ).mappings().all()
        q_rows = (
            await s.execute(
                text("select id,canonical_question_type from questions")
            )
        ).mappings().all()
        qi_rows = (
            await s.execute(text("select id,question_id from question_instances"))
        ).mappings().all()

    funnel.set("ir_ready", 1 if sv_rows and sv_rows[0]["status"] == "sealed" else 0)
    funnel.set("candidates", len(cand_rows))
    funnel.set("questions", len(q_rows))
    funnel.set("question_instances", len(qi_rows))
    pending = [c for c in cand_rows if c["decision_status"] == "pending_review"]
    funnel.set("pending_review", len(pending))

    evidence["pipeline"] = {
        "task_id": tid,
        "task_status_db": task_row["status"] if task_row else None,
        "current_stage": task_row["current_stage"] if task_row else None,
        "llm_invocations": task_row["llm_invocations"] if task_row else None,
        "elapsed_seconds": round(elapsed, 2),
        "stage_log": stage_log,
    }
    evidence["db"] = {
        "source_versions": [dict(r) for r in sv_rows],
        "annotations": [dict(r) for r in ann_rows],
        "candidates": [dict(r) for r in cand_rows],
        "questions": [dict(r) for r in q_rows],
        "question_instances": [dict(r) for r in qi_rows],
    }
    evidence["funnel"] = funnel.to_dict()

    out = OUT_DIR / f"m2-real-chem-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps(evidence["pipeline"], ensure_ascii=False, indent=2, default=str))
    print(json.dumps(evidence["funnel"], ensure_ascii=False, indent=2, default=str))
    print("EVIDENCE", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
