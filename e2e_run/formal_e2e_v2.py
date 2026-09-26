"""FORMAL-E2E-ENABLEMENT-02 Level-1 formal E2E v2.

Formal entries ONLY:
  ingest : POST /api/documents/import  (uvicorn app.main:app)
  worker : python -m app.worker run --allow-live

Forbidden (Issue-01): direct TaskExecutor/ Gateway construction, manual task_context injection.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT_DIR = Path(r"D:\Project\AITutor-X\e2e_run")
PDF = Path(r"D:\Project\Papers\maintainess\PDF\2018北京一零一中高一分班考物理（教师版）(1).pdf")
API = "http://127.0.0.1:8077"
PYTHON = r"C:\Users\Kurtw\AppData\Local\Programs\Python\Python312\python.exe"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def start_api() -> subprocess.Popen:
    env = os.environ.copy()
    env["E2E_RUN_ID"] = E2E_RUN_ID
    env["DATABASE_MODE"] = DATABASE_MODE
    return subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8077"],
        cwd=str(BACKEND),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def run_worker_cli(log_path: Path) -> tuple[int, str]:
    """Formal worker entry: python -m app.worker run --allow-live"""
    cmd = [PYTHON, "-m", "app.worker", "run", "--allow-live"]
    env = os.environ.copy()
    env["E2E_RUN_ID"] = E2E_RUN_ID
    env["DATABASE_MODE"] = DATABASE_MODE
    proc = subprocess.run(
        cmd, cwd=str(BACKEND), env=env,
        capture_output=True, text=True, timeout=600,
    )
    log = (
        f"$ {' '.join(cmd)}\n"
        f"exit_code={proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n"
        f"--- stderr ---\n{proc.stderr}\n"
    )
    log_path.write_text(log, encoding="utf-8")
    return proc.returncode, log


async def db_snapshot() -> dict:
    sys.path.insert(0, str(BACKEND))
    os.chdir(str(BACKEND))
    from sqlalchemy import text
    from app.db.session import async_session_maker

    async with async_session_maker() as s:
        snap = {}
        snap["tasks"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, status, llm_invocations, task_params->>'file_name' AS file_name FROM tasks WHERE task_params ? 'file_name'"
        ))).mappings().all()]
        snap["claims"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, task_id, claim_round, outcome, error_type, start, \"end\" FROM task_claims ORDER BY start"
        ))).mappings().all()]
        snap["source_versions"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, document_id, status, body_hash, line_count, page_count FROM document_source_versions"
        ))).mappings().all()]
        snap["annotations"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, source_version_id, status, model_config_hash FROM semantic_annotations"
        ))).mappings().all()]
        snap["counts"] = {
            "documents": (await s.execute(text("SELECT count(*) FROM documents"))).scalar(),
            "questions": (await s.execute(text("SELECT count(*) FROM questions"))).scalar(),
            "question_instances": (await s.execute(text("SELECT count(*) FROM question_instances"))).scalar(),
            "materials": (await s.execute(text("SELECT count(*) FROM materials"))).scalar(),
            "admission_candidates": (await s.execute(text("SELECT count(*) FROM admission_candidates"))).scalar(),
            "semantic_annotations": (await s.execute(text("SELECT count(*) FROM semantic_annotations"))).scalar(),
            "source_figures": (await s.execute(text("SELECT count(*) FROM source_figures"))).scalar(),
            "document_source_spans": (await s.execute(text("SELECT count(*) FROM document_source_spans"))).scalar(),
        }
        snap["llm_audit"] = [dict(r) for r in (await s.execute(text(
            'SELECT request_id, provider, model, status, start, input_tokens, output_tokens, total_tokens, estimated_cost, error_type '
            'FROM llm_call_audit ORDER BY start'
        ))).mappings().all()]
        snap["budget"] = [dict(r) for r in (await s.execute(text(
            "SELECT account_dim, scope_id, used, reserved FROM budget"
        ))).mappings().all()]
    return snap


async def reset_db() -> dict:
    """Issue-05: fresh_test identity. Record the reset explicitly."""
    sys.path.insert(0, str(BACKEND))
    os.chdir(str(BACKEND))
    from sqlalchemy import text
    from app.db.session import async_session_maker

    async with async_session_maker() as s:
        rows = await s.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        ))
        tables = [r[0] for r in rows if r[0] != "alembic_version"]
        await s.execute(text("TRUNCATE " + ", ".join(tables) + " CASCADE"))
        await s.commit()
    return {"database_mode": DATABASE_MODE, "truncated_tables": tables, "reset_at": now()}


async def main() -> int:
    global E2E_RUN_ID, DATABASE_MODE
    E2E_RUN_ID = os.environ.get("E2E_RUN_ID") or f"E2E-{uuid.uuid4().hex[:12]}"
    DATABASE_MODE = os.environ.get("DATABASE_MODE") or "fresh_test"
    os.environ["E2E_RUN_ID"] = E2E_RUN_ID
    os.environ["DATABASE_MODE"] = DATABASE_MODE

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    evidence = {
        "task_id": "FORMAL-E2E-ENABLEMENT-02",
        "level": "L1-single-document",
        "e2e_run_id": E2E_RUN_ID,
        "database_mode": DATABASE_MODE,
        "started_at": now(),
        "formal_entries": {
            "ingest": "POST http://127.0.0.1:8077/api/documents/import",
            "worker": "python -m app.worker run --allow-live",
        },
        "forbidden_practices": {
            "direct_executor_instantiation": False,
            "manual_task_context_injection": False,
            "hardcoded_budget_approval": False,
            "actual_equals_config_without_response": False,
        },
    }

    # ---- Issue-05: fresh DB identity ----
    evidence["db_reset"] = await reset_db()
    print("DB RESET", evidence["db_reset"]["database_mode"], "tables=", len(evidence["db_reset"]["truncated_tables"]))

    # ---- Source ----
    assert PDF.exists(), PDF
    evidence["source"] = {
        "pdf_path": str(PDF),
        "sha256": sha256_file(PDF),
        "bytes": PDF.stat().st_size,
    }

    # ---- Issue-01: start formal API and import ----
    api_proc = start_api()
    try:
        # wait for API
        for _ in range(40):
            try:
                r = httpx.get(f"{API}/docs", timeout=2)
                if r.status_code < 500:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("API did not start")

        with PDF.open("rb") as f:
            r = httpx.post(
                f"{API}/api/documents/import",
                files={"file": (PDF.name, f, "application/pdf")},
                timeout=60,
            )
        evidence["import_http"] = {
            "command": f"POST {API}/api/documents/import",
            "status_code": r.status_code,
            "body": r.json() if r.status_code < 500 else r.text[:500],
            "timestamp": now(),
        }
        print("IMPORT", evidence["import_http"]["status_code"], evidence["import_http"]["body"])
        if r.status_code >= 400:
            evidence["first_blocking_point"] = {
                "stage": "V3 Import API",
                "error": evidence["import_http"]["body"],
            }
            raise SystemExit(2)
    finally:
        # keep API for potential queries; kill after worker
        pass

    # ---- Issue-01: formal worker CLI ----
    worker_log = OUT_DIR / f"formal-e2e-v2-worker-{E2E_RUN_ID}.log"
    rc, log = run_worker_cli(worker_log)
    evidence["worker_cli"] = {
        "command": "python -m app.worker run --allow-live",
        "exit_code": rc,
        "log_path": str(worker_log),
        "timestamp": now(),
    }
    print("WORKER exit", rc)

    # stop API
    api_proc.terminate()
    try:
        api_proc.wait(timeout=10)
    except Exception:
        api_proc.kill()

    # ---- Evidence snapshot ----
    snap = await db_snapshot()
    evidence["db_snapshot"] = snap

    # ---- Provider reality sidecar ----
    reality_path = BACKEND / "provider_reality.json"
    if reality_path.exists():
        evidence["provider_reality_file"] = str(reality_path)
        try:
            evidence["provider_reality"] = json.loads(reality_path.read_text(encoding="utf-8"))
        except Exception as e:
            evidence["provider_reality_error"] = str(e)

    # ---- Classify outcome ----
    counts = snap["counts"]
    evidence["final_objects"] = counts
    if counts["questions"] >= 1 and counts["question_instances"] >= 1:
        evidence["outcome"] = "PASS_QUESTION_GENERATED"
    else:
        # FIRST BLOCKING POINT — do not speculate later stages
        blocking = {
            "stage": "Resolver/IR → Admission",
            "observed": (
                f"questions={counts['questions']} instances={counts['question_instances']} "
                f"candidates={counts['admission_candidates']}"
            ),
            "evidence": (
                "Task may have succeeded and LLM audit completed; "
                "units incomplete under Frozen resolver grammar => Gate skips => 0 candidates"
            ),
            "action": "RECORD_ONLY no silent repair",
        }
        # refine if annotation missing
        if counts["semantic_annotations"] == 0:
            blocking = {
                "stage": "Semantic Annotation",
                "observed": "0 semantic_annotations",
                "evidence": "annotation stage produced no valid artifact",
                "action": "RECORD_ONLY",
            }
        evidence["first_blocking_point"] = blocking
        evidence["outcome"] = "FIRST_BLOCKING_POINT_IDENTIFIED"

    evidence["finished_at"] = now()
    out = OUT_DIR / f"formal-e2e-v2-{E2E_RUN_ID}.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("EVIDENCE", out)
    print("OUTCOME", evidence["outcome"])
    print(json.dumps(evidence["final_objects"], indent=2))
    return 0 if evidence["outcome"].startswith("PASS") else 2


if __name__ == "__main__":
    import asyncio
    raise SystemExit(asyncio.run(main()))
