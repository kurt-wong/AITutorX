"""AITutor-X unified integration entry (minimal, real-path).

Flow (the ONLY acceptance path):
  raw package (paper.pdf + paper.md + paper.manifest.json)
    → PreprocessingImportService.import_package   # formal V3 entry
    → TaskExecutor (annotation → Gate → Admission → DB)

Isolation: DATABASE_URL defaults to aitutors_testsuite.
Never uses aitutors / aitutors_test.

Usage:
  python x_integrate_entry.py <package_dir> [--db-url postgresql+asyncpg://...]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(BACKEND))
_ORIG_CWD = Path.cwd()
os.chdir(str(BACKEND))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("package_dir", type=Path)
    ap.add_argument(
        "--db-url",
        default="postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors_testsuite",
    )
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    os.environ["APP_ENV"] = "test"
    os.environ["DATABASE_URL"] = args.db_url
    os.environ.setdefault("APP_SECRET", "test-app-secret-32-bytes-minimum!!")

    from urllib.parse import urlparse

    name = urlparse(args.db_url).path.lstrip("/").split("?")[0]
    if name in ("aitutors", "aitutors_test"):
        print(f"REFUSED: protected database {name!r}")
        return 2

    from app.db.session import async_session_maker
    from app.domains.source.preprocessing_import import (
        PreprocessingImportService,
        load_package_from_dir,
    )
    from app.domains.task.executor import TaskExecutor

    package_dir = args.package_dir
    if not package_dir.is_absolute():
        package_dir = (_ORIG_CWD / package_dir).resolve()
    else:
        package_dir = package_dir.resolve()
    args.package_dir = package_dir
    pkg = load_package_from_dir(package_dir)
    result = {
        "started": datetime.now(timezone.utc).isoformat(),
        "package_dir": str(args.package_dir),
        "original_name": pkg.original_name,
        "original_sha256": __import__("hashlib").sha256(pkg.original_bytes).hexdigest(),
        "source_content_sha256": __import__("hashlib").sha256(pkg.source_md).hexdigest(),
        "manifest_units": len(pkg.manifest.get("units") or []),
        "db": name,
    }

    async def run():
        async with async_session_maker() as session:
            imp = await PreprocessingImportService(session).import_package(
                package=pkg, created_by="x-integrate"
            )
            result["document_id"] = str(imp.document.id)
            result["source_version_id"] = imp.source_version_id
            result["is_new"] = imp.is_new
            result["task_id"] = imp.task_id
            await session.commit()
            result["task_id"] = imp.task_id
            result["task_queued"] = bool(imp.task_id)
            result["import_ok"] = True

            if imp.task_id:
                from sqlalchemy import text as _sa_text

                trow = (
                    await session.execute(
                        _sa_text(
                            "select task_params->>'source_version_id' as sv from tasks "
                            "where id=:tid"
                        ),
                        {"tid": imp.task_id},
                    )
                ).first()
                result["task_source_version_id"] = trow[0] if trow else None

            # Snapshot IDs before task execution (attribution).
            from sqlalchemy import text as _sa_text
            before = {
                "questions": [
                    r[0] for r in (
                        await session.execute(_sa_text("select id::text from questions"))
                    ).all()
                ],
                "instances": [
                    r[0] for r in (
                        await session.execute(
                            _sa_text("select id::text from question_instances")
                        )
                    ).all()
                ],
            }
            result["before_question_ids"] = before["questions"]
            result["before_instance_ids"] = before["instances"]
            result["task_source_version_id"] = result.get("task_source_version_id")

            # ---- TaskExecutor: REAL annotation → Gate → Admission ----
            if imp.task_id:
                from app.ai.gateway import LLMGateway
                from app.ai.providers.http import HTTPLLMProvider
                from app.core.config import settings as _settings
                from app.domains.task.executor import TaskExecutor

                provider = HTTPLLMProvider(
                    name="mimo",
                    api_key=_settings.mimo_api_key,
                    base_url=_settings.mimo_base_url,
                    model=_settings.mimo_model,
                    timeout=_settings.llm_request_timeout_seconds * 4,
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
                    default_model=_settings.mimo_model,
                )
                stage_log = []
                for rnd in range(1, 8):
                    try:
                        claimed = await executor.run_once(
                            worker_id=f"x-integrate-{rnd}"
                        )
                        stage_log.append({"round": rnd, "claimed": bool(claimed)})
                    except Exception as exc:  # noqa: BLE001
                        stage_log.append(
                            {"round": rnd, "error": f"{type(exc).__name__}: {exc}"}
                        )
                    await session.commit()
                    if not claimed:
                        break
                result["task_stage_log"] = stage_log

            after_q = [
                r[0] for r in (
                    await session.execute(_sa_text("select id::text from questions"))
                ).all()
            ]
            after_i = [
                r[0] for r in (
                    await session.execute(
                        _sa_text("select id::text from question_instances")
                    )
                ).all()
            ]
            new_q = [x for x in after_q if x not in before["questions"]]
            new_i = [x for x in after_i if x not in before["instances"]]
            result["new_question_ids"] = new_q
            result["new_instance_ids"] = new_i
            result["new_questions"] = len(new_q)
            result["new_instances"] = len(new_i)

            # Per-new-instance SV attribution (identity acceptance).
            new_inst_sv: dict[str, str] = {}
            if new_i:
                for r in (
                    await session.execute(
                        _sa_text(
                            "select id::text, source_version_id::text "
                            "from question_instances where id = any(:ids)"
                        ),
                        {"ids": new_i},
                    )
                ).all():
                    new_inst_sv[r[0]] = r[1]
            result["new_instance_source_version_ids"] = new_inst_sv
            distinct_new_sv = sorted(set(new_inst_sv.values()))
            result["new_instance_sv_distinct"] = distinct_new_sv
            result["sv_identity_match"] = bool(
                new_inst_sv
                and len(distinct_new_sv) == 1
                and distinct_new_sv[0] == result.get("task_source_version_id")
            )

            # DB readback scoped to THIS document/source_version
            from sqlalchemy import select, text
            from app.models.content import InstanceRoleContent, Question, QuestionInstance

            # Readback by DOCUMENT (processing may seal a new SV version).
            doc_id = imp.document.id
            sv_ids = [r[0] for r in (
                await session.execute(
                    text(
                        "select id from document_source_versions where document_id=:d"
                    ),
                    {"d": doc_id},
                )
            ).all()]
            sv_id = sv_ids[-1] if sv_ids else imp.source_version_id
            result["source_versions"] = [str(x) for x in sv_ids]
            inst_rows = (
                await session.execute(
                    select(QuestionInstance).where(
                        QuestionInstance.source_version_id == sv_id
                    )
                )
            ).scalars().all()
            inst_ids = [i.id for i in inst_rows]
            q_rows = (
                await session.execute(
                    select(Question).join(QuestionInstance).where(
                        QuestionInstance.source_version_id == sv_id
                    )
                )
            ).scalars().all()
            ans_rows = []
            if inst_ids:
                ans_rows = (
                    await session.execute(
                        select(InstanceRoleContent).where(
                            InstanceRoleContent.instance_id.in_(inst_ids),
                            InstanceRoleContent.role == "answer",
                        )
                    )
                ).scalars().all()
            result["db_questions"] = len(q_rows)
            result["db_instances"] = len(inst_rows)
            result["db_answers"] = len(ans_rows)
            result["db_answers_nonempty"] = sum(
                1 for a in ans_rows if (a.text or "").strip()
            )
            by_pub = {}
            for a in ans_rows:
                pub = (a.answer_status or {}).get("publish") or "?"
                by_pub[pub] = by_pub.get(pub, 0) + 1
            result["db_answers_by_publish"] = by_pub
            result["db_answer_units"] = [
                {
                    "text": (a.text or "")[:40],
                    "publish": (a.answer_status or {}).get("publish"),
                    "ownership": (a.answer_status or {}).get("ownership"),
                }
                for a in ans_rows[:20]
            ]

    asyncio.run(run())
    result["finished"] = datetime.now(timezone.utc).isoformat()
    out = args.out or (args.package_dir / "x_integrate_result.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("document_id") else 1


if __name__ == "__main__":
    raise SystemExit(main())
