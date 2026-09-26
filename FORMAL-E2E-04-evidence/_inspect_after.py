import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, r"D:\Project\AITutors-v3\backend")
os.chdir(r"D:\Project\AITutors-v3\backend")
from sqlalchemy import text
from app.db.session import async_session_maker

async def main():
    async with async_session_maker() as s:
        # latest annotation
        anns = (await s.execute(text(
            "SELECT id, source_version_id, status, model_config_hash, prompt_version, annotation_schema_version FROM semantic_annotations ORDER BY id DESC LIMIT 3"
        ))).mappings().all()
        for a in anns:
            print("ANN", dict(a))
        # latest document/source
        docs = (await s.execute(text("SELECT id, file_name, original_sha256 FROM documents ORDER BY file_name DESC LIMIT 3"))).mappings().all()
        for d in docs:
            print("DOC", dict(d))
        svs = (await s.execute(text("SELECT id, document_id, status, body_hash, line_count FROM document_source_versions"))).mappings().all()
        for v in svs:
            print("SV", dict(v))
        print("candidates", (await s.execute(text("SELECT count(*) FROM admission_candidates"))).scalar())
        print("questions", (await s.execute(text("SELECT count(*) FROM questions"))).scalar())

        # payload unit types of newest ann
        if anns:
            payload = (await s.execute(text("SELECT payload FROM semantic_annotations WHERE id=:i"), {"i": anns[0]["id"]})).scalar()
            units = payload.get("semantic_units") or []
            from collections import Counter
            print("units", len(units), Counter(u.get("unit_type") for u in units))
            # shared material
            for u in units:
                sc = u.get("shared_components") or {}
                if sc:
                    print(" shared", u.get("unit_id"), list(sc.keys()))
                    break

asyncio.run(main())
