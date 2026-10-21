"""Read-only: current DB table counts (post-truncate baseline)."""
from __future__ import annotations

import asyncio
from pathlib import Path

import asyncpg

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
env = {}
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

DSN = env["DATABASE_URL"].replace("postgresql+asyncpg", "postgresql")

TABLES = [
    "documents", "source_versions", "document_source_lines", "semantic_annotations",
    "admission_candidates", "admission_events", "questions", "question_instances",
    "materials", "llm_call_audit", "alembic_version",
]


async def main() -> None:
    conn = await asyncpg.connect(DSN)
    try:
        for t in TABLES:
            try:
                n = await conn.fetchval(f"SELECT count(*) FROM {t}")
                print(f"{t:<28} {n}")
            except Exception as e:  # noqa: BLE001
                print(f"{t:<28} ERR {type(e).__name__}: {e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
