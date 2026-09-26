import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, r"D:\Project\AITutors-v3\backend")
os.chdir(r"D:\Project\AITutors-v3\backend")
from sqlalchemy import text
from app.db.session import async_session_maker

async def snap(path: str):
    async with async_session_maker() as s:
        tables = [r[0] for r in (await s.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public'"))).all()]
        out = {}
        for t in tables:
            if t == "alembic_version":
                continue
            n = (await s.execute(text(f"SELECT count(*) FROM {t}"))).scalar()
            out[t] = n
        Path(path).write_text(json.dumps(out, indent=2), encoding="utf-8")
        print("snap", path, out)

asyncio.run(snap(sys.argv[1]))
