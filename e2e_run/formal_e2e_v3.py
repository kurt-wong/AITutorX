"""FORMAL-E2E-ENABLEMENT-03: evidence stabilization + business pipeline verification.

Formal entries ONLY:
  POST /api/documents/import
  python -m app.worker run --allow-live

Issue-A: full evidence metadata
Issue-B: reset_db only when DATABASE_MODE in {test, fresh_test}
Issue-C/D: response evidence + reality state isolation (in provider/gateway)
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
API = "http://127.0.0.1:8077"
PYTHON = r"C:\Users\Kurtw\AppData\Local\Programs\Python\Python312\python.exe"
V3_ROOT = Path(r"D:\Project\AITutors-v3")

# 1 standalone + 1 composite/material candidate
DOCS = [
    {
        "role": "standalone",
        "path": Path(r"D:\Project\Papers\maintainess\PDF\2021北京高三二模数学汇编：集合（教师版）.pdf"),
    },
    {
        "role": "composite_material_candidate",
        "path": Path(r"D:\Project\Papers\maintainess\PDF\2021北京高三一模二模政治汇编：生活与哲学（材料题）（教师版）(1).pdf"),
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha256_dir_files(root: Path, patterns: tuple[str, ...] = (".md",)) -> str:
    h = hashlib.sha256()
    files = sorted(root.rglob("*"))
    for f in files:
        if f.is_file() and f.suffix in patterns:
            h.update(str(f.relative_to(root)).replace("\\", "/").encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def git_head(repo: Path) -> str:
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo), capture_output=True, text=True)
    return r.stdout.strip()


ALLOWED_RESET_MODES = {"test", "fresh_test"}


async def reset_db_guarded(database_mode: str) -> dict:
    """Issue-B: refuse TRUNCATE unless DATABASE_MODE is an explicit test mode."""
    if database_mode not in ALLOWED_RESET_MODES:
        raise RuntimeError(
            f"reset_db refused: DATABASE_MODE={database_mode!r} not in {sorted(ALLOWED_RESET_MODES)}"
        )
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
    return {
        "database_mode": database_mode,
        "allowed_modes": sorted(ALLOWED_RESET_MODES),
        "truncated_tables": tables,
        "reset_at": now(),
    }


def start_api(e2e_run_id: str, database_mode: str) -> subprocess.Popen:
    env = os.environ.copy()
    env["E2E_RUN_ID"] = e2e_run_id
    env["DATABASE_MODE"] = database_mode
    return subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8077"],
        cwd=str(BACKEND), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )


def run_worker_cli(log_path: Path, e2e_run_id: str, database_mode: str) -> dict:
    cmd = [PYTHON, "-m", "app.worker", "run", "--allow-live"]
    env = os.environ.copy()
    env["E2E_RUN_ID"] = e2e_run_id
    env["DATABASE_MODE"] = database_mode
    t0 = now()
    proc = subprocess.run(cmd, cwd=str(BACKEND), env=env, capture_output=True, text=True, timeout=900)
    t1 = now()
    log = (
        f"# FORMAL-E2E-ENABLEMENT-03 worker log\n"
        f"E2E_RUN_ID={e2e_run_id}\nDATABASE_MODE={database_mode}\n"
        f"started_at={t0}\nfinished_at={t1}\n"
        f"$ {' '.join(cmd)}\nexit_code={proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n"
    )
    log_path.write_text(log, encoding="utf-8")
    return {"command": " ".join(cmd), "exit_code": proc.returncode, "log_path": str(log_path),
            "started_at": t0, "finished_at": t1}


async def collect_staged_evidence() -> dict:
    sys.path.insert(0, str(BACKEND))
    os.chdir(str(BACKEND))
    from sqlalchemy import text
    from app.db.session import async_session_maker

    async with async_session_maker() as s:
        ev = {}
        ev["documents"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, file_name, original_sha256, processing_status FROM documents"
        ))).mappings().all()]
        ev["tasks"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, status, llm_invocations, task_params->>'file_name' AS file_name FROM tasks WHERE task_params ? 'file_name'"
        ))).mappings().all()]
        ev["claims"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, task_id, claim_round, outcome, error_type, start, \"end\" FROM task_claims ORDER BY start"
        ))).mappings().all()]
        ev["source_versions"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, document_id, status, body_hash, line_count, page_count FROM document_source_versions"
        ))).mappings().all()]
        # Import stage extras
        ev["import_counts"] = {
            "source_figures": (await s.execute(text("SELECT count(*) FROM source_figures"))).scalar(),
            "document_source_spans": (await s.execute(text("SELECT count(*) FROM document_source_spans"))).scalar(),
            "document_source_lines": (await s.execute(text("SELECT count(*) FROM document_source_lines"))).scalar(),
        }
        ev["annotations"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, source_version_id, status, model_config_hash, prompt_version FROM semantic_annotations"
        ))).mappings().all()]
        ev["llm_audit"] = [dict(r) for r in (await s.execute(text(
            'SELECT request_id, provider, model, status, start, input_tokens, output_tokens, total_tokens, error_type '
            'FROM llm_call_audit ORDER BY start'
        ))).mappings().all()]
        ev["final_counts"] = {
            "questions": (await s.execute(text("SELECT count(*) FROM questions"))).scalar(),
            "question_instances": (await s.execute(text("SELECT count(*) FROM question_instances"))).scalar(),
            "materials": (await s.execute(text("SELECT count(*) FROM materials"))).scalar(),
            "admission_candidates": (await s.execute(text("SELECT count(*) FROM admission_candidates"))).scalar(),
            "admission_events": (await s.execute(text("SELECT count(*) FROM admission_events"))).scalar(),
            "unit_groups": (await s.execute(text("SELECT count(*) FROM unit_groups"))).scalar(),
        }
        ev["candidates"] = [dict(r) for r in (await s.execute(text(
            "SELECT id, decision_status FROM admission_candidates"
        ))).mappings().all()]
    return ev


async def annotation_stage_summary(ann_id) -> dict:
    """Per-annotation payload summary + resolver/IR diagnostic (read-only)."""
    sys.path.insert(0, str(BACKEND))
    os.chdir(str(BACKEND))
    import uuid as uuid_mod
    from sqlalchemy import text
    from app.db.session import async_session_maker
    from app.domains.compile.ir import IRBuilder
    from app.domains.gate.service import _annotation_identity_projection
    from app.domains.resolver.resolver import SourceResolver
    from app.domains.resolver.span import SourceLineView

    async with async_session_maker() as s:
        row = (await s.execute(text(
            "SELECT id, source_version_id, payload FROM semantic_annotations WHERE id=:i"
        ), {"i": ann_id})).mappings().first()
        if not row:
            return {"error": "annotation not found"}
        payload = row["payload"]
        sv_id = row["source_version_id"]
        units = payload.get("semantic_units") or []
        summary = {
            "annotation_id": str(row["id"]),
            "source_version_id": str(sv_id),
            "unit_count": len(units),
            "unit_types": [u.get("unit_type") for u in units],
            "has_shared_material": any(
                (u.get("shared_components") or {}).get("material") for u in units
            ),
        }
        lines = (await s.execute(text(
            "SELECT line_ref, seq, text FROM document_source_lines WHERE source_version_id=:s ORDER BY seq"
        ), {"s": sv_id})).mappings().all()
        views = tuple(SourceLineView(line_ref=L["line_ref"], seq=L["seq"], text=L["text"]) for L in lines)
        resolver = SourceResolver(source_version_id=sv_id, lines=views)
        run = resolver.resolve(_annotation_identity_projection(payload))
        from collections import Counter
        unres = list(run.unresolved_references)
        summary["resolver"] = {
            "resolved_spans": len(run.resolved_spans),
            "unresolved": len(unres),
            "unresolved_reasons": dict(Counter(f"{u.role}:{u.resolution_status}" for u in unres)),
        }
        try:
            ir = IRBuilder.build(run, _annotation_identity_projection(payload), sv_id, uuid_mod.UUID(str(row["id"])))
            ir_rows = []
            for n in ir.units:
                ir_rows.append({
                    "unit_id": n.unit_id,
                    "unit_type": n.unit_type,
                    "original_question_type": n.original_question_type,
                    "semantic_status": n.semantic_status,
                    "shared_components": [c.role for c in n.shared_components],
                    "content_roles": [c.role for c in n.content],
                })
            summary["ir"] = {
                "units": ir_rows,
                "ready": sum(1 for r in ir_rows if r["semantic_status"] == "ready"),
                "incomplete": sum(1 for r in ir_rows if r["semantic_status"] == "incomplete"),
            }
        except Exception as e:
            summary["ir"] = {"error": str(e)}
        return summary


async def main() -> int:
    e2e_run_id = os.environ.get("E2E_RUN_ID") or f"E2E3-{uuid.uuid4().hex[:12]}"
    database_mode = os.environ.get("DATABASE_MODE") or "fresh_test"
    os.environ["E2E_RUN_ID"] = e2e_run_id
    os.environ["DATABASE_MODE"] = database_mode

    started_at = now()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Issue-A: evidence metadata ----
    spec_hashes = {}
    for name in ("00_Master_Spec.md", "10_Data_Model.md", "20_Document_Pipeline.md",
                 "30_Task_LLM_Safety.md", "40_Development_Rules.md", "50_Migration_Assets.md"):
        fp = V3_ROOT / "Docs" / "V3_SPEC" / name
        if fp.exists():
            spec_hashes[name] = hashlib.sha256(fp.read_bytes()).hexdigest()

    evidence = {
        "task_id": "FORMAL-E2E-ENABLEMENT-03",
        "evidence_metadata": {
            "E2E_RUN_ID": e2e_run_id,
            "DATABASE_MODE": database_mode,
            "START_TIME": started_at,
            "END_TIME": None,
            "GIT_COMMIT": {
                "AITutors-v3": git_head(V3_ROOT),
                "Papers": git_head(Path(r"D:\Project\Papers")),
                "AITutor-X": git_head(Path(r"D:\Project\AITutor-X")),
            },
            "V3_SPEC_HASH": spec_hashes,
            "PROVIDER": "mimo",
            "MODEL": "mimo-v2.6-pro",
            "INPUT_DOCUMENT_SHA256": {},
        },
        "formal_entries": {
            "ingest": "POST /api/documents/import",
            "worker": "python -m app.worker run --allow-live",
        },
        "api_surface_note": {
            "Question API": "NOT PRESENT",
            "Material API": "NOT PRESENT",
            "Instance API": "NOT PRESENT",
            "present": ["POST /api/documents/import", "GET /api/documents/{id}",
                        "GET /api/documents/{id}/source-quality", "GET /api/documents/{id}/source-lines",
                        "GET /api/candidates/{id}", "POST /api/candidates/{id}/approve",
                        "POST /api/candidates/{id}/reject", "GET /api/admin/stats"],
        },
    }

    for d in DOCS:
        assert d["path"].exists(), d["path"]
        evidence["evidence_metadata"]["INPUT_DOCUMENT_SHA256"][d["role"]] = {
            "path": str(d["path"]),
            "sha256": sha256_file(d["path"]),
            "bytes": d["path"].stat().st_size,
        }

    # ---- Issue-B: guarded reset ----
    evidence["db_reset"] = await reset_db_guarded(database_mode)
    print("DB RESET", database_mode, "tables", len(evidence["db_reset"]["truncated_tables"]))

    # ---- Formal API import both docs ----
    api = start_api(e2e_run_id, database_mode)
    try:
        for _ in range(40):
            try:
                if httpx.get(f"{API}/docs", timeout=2).status_code < 500:
                    break
            except Exception:
                time.sleep(0.5)
        imports = []
        for d in DOCS:
            with d["path"].open("rb") as f:
                r = httpx.post(f"{API}/api/documents/import",
                               files={"file": (d["path"].name, f, "application/pdf")},
                               timeout=60)
            body = r.json() if r.status_code < 500 else {"raw": r.text[:500]}
            imports.append({"role": d["role"], "status_code": r.status_code, "body": body, "at": now()})
            print("IMPORT", d["role"], r.status_code, body)
        evidence["import_stage"] = imports
    finally:
        api.terminate()
        try:
            api.wait(timeout=10)
        except Exception:
            api.kill()

    # ---- Formal worker CLI ----
    wlog = OUT_DIR / f"formal-e2e-v3-worker-{e2e_run_id}.log"
    evidence["worker_cli"] = run_worker_cli(wlog, e2e_run_id, database_mode)
    print("WORKER exit", evidence["worker_cli"]["exit_code"])

    # ---- Staged evidence ----
    staged = await collect_staged_evidence()
    evidence["staged"] = staged

    # Per-annotation resolver/IR diagnostics
    ann_diags = []
    for a in staged.get("annotations") or []:
        ann_diags.append(await annotation_stage_summary(a["id"]))
    evidence["annotation_resolver_ir"] = ann_diags

    # Provider reality sidecar
    reality = BACKEND / "provider_reality.json"
    if reality.exists():
        try:
            evidence["provider_reality"] = json.loads(reality.read_text(encoding="utf-8"))
        except Exception as e:
            evidence["provider_reality_error"] = str(e)

    # ---- Outcome ----
    fc = staged["final_counts"]
    if fc["questions"] >= 1 and fc["question_instances"] >= 1:
        evidence["outcome"] = "PASS"
    elif staged.get("annotations") and any(
        (d.get("ir") or {}).get("ready", 0) > 0 for d in ann_diags
    ):
        evidence["outcome"] = "PARTIAL"
        evidence["first_blocking_point"] = {
            "stage": "Compiler/Admission",
            "observed": f"ready IR units exist but questions={fc['questions']} candidates={fc['admission_candidates']}",
        }
    elif staged.get("annotations"):
        evidence["outcome"] = "PARTIAL"
        # pick first incomplete reason as blocking
        d0 = ann_diags[0] if ann_diags else {}
        evidence["first_blocking_point"] = {
            "stage": "Resolver/IR",
            "observed": d0.get("resolver"),
            "ir": d0.get("ir"),
            "action": "RECORD_ONLY",
        }
    else:
        evidence["outcome"] = "BLOCKED"
        # find why annotation missing
        claims = staged.get("claims") or []
        last = claims[-1] if claims else {}
        evidence["first_blocking_point"] = {
            "stage": "Semantic Annotation",
            "claim_error_type": last.get("error_type"),
            "observed": "0 semantic_annotations",
        }

    evidence["evidence_metadata"]["END_TIME"] = now()
    out = OUT_DIR / f"formal-e2e-v3-{e2e_run_id}.json"
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("EVIDENCE", out)
    print("OUTCOME", evidence["outcome"])
    print(json.dumps(fc, indent=2))
    return 0 if evidence["outcome"] == "PASS" else 2


if __name__ == "__main__":
    import asyncio
    raise SystemExit(asyncio.run(main()))
