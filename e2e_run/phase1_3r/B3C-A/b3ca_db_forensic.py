"""B3c-A DB forensic: candidate decision distribution + rejected reasons."""
from __future__ import annotations

import asyncio
import json
from collections import Counter

import asyncpg

DSN = "postgresql://aitutors:change-me@localhost:5432/aitutors"


async def main() -> None:
    c = await asyncpg.connect(DSN)
    cols = await c.fetch(
        "SELECT column_name, data_type FROM information_schema.columns "
        "WHERE table_name='admission_candidates' ORDER BY ordinal_position"
    )
    print("COLUMNS:", [(r["column_name"], r["data_type"]) for r in cols])
    print()

    rows = await c.fetch("SELECT * FROM admission_candidates")
    print("total candidates:", len(rows))
    first = dict(rows[0])
    print("sample keys:", sorted(first.keys()))
    print()

    for key in ("decision", "status", "semantic_status", "gate_decision", "review_status"):
        if key in first:
            print(f"{key}: {dict(Counter(str(r[key]) for r in rows))}")
    print()

    # payload shape
    p = first.get("payload")
    if isinstance(p, str):
        p = json.loads(p)
    if isinstance(p, dict):
        print("payload top keys:", sorted(p.keys()))
        ir = p.get("ir_snapshot") or {}
        units = ir.get("units") or []
        print("ir units:", len(units), "root keys:", sorted(units[0].keys()) if units else None)
        if units:
            print("root semantic_status:", units[0].get("semantic_status"),
                  "unit_type:", units[0].get("unit_type"))
    print()

    # rejected detail
    dkey = "decision" if "decision" in first else ("status" if "status" in first else None)
    if dkey:
        for r in rows:
            if str(r[dkey]) != "rejected":
                continue
            d = dict(r)
            pl = d.get("payload")
            if isinstance(pl, str):
                pl = json.loads(pl)
            ir = (pl or {}).get("ir_snapshot") or {}
            units = ir.get("units") or []
            root = units[0] if units else {}
            print("=" * 70)
            print("REJECTED candidate id:", d.get("id"))
            print("  unit_id:", root.get("unit_id"), "type:", root.get("unit_type"))
            print("  ir semantic_status:", root.get("semantic_status"))
            sp = (pl or {}).get("span_validation") or {}
            reasons = None
            for cand_key in ("reasons", "policy", "gate", "validation"):
                if cand_key in (pl or {}):
                    v = pl[cand_key]
                    reasons = json.dumps(v, ensure_ascii=False)[:1500]
                    break
            print("  payload reasons:", reasons)
            # any decision/reason columns
            for k, v in d.items():
                if k in ("payload", "id"):
                    continue
                sv = str(v)
                if len(sv) > 400:
                    sv = sv[:400] + "..."
                print(f"    {k} = {sv}")
    await c.close()


asyncio.run(main())
