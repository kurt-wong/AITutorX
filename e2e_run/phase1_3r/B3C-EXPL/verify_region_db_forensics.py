"""Read-only DB forensics: which candidates actually carry a role-provenance
violation in gate_decision, and how many?

Prediction from resolver-level recount:
  - 历史 has 40 ready units -> 40 candidates, of which 39 should carry
    "overlaps explanation region" (Q1 excluded: its answer L637 sits in the
    answer region, before the first explanation header).
  - 地理 has 0 ready units -> 0 candidates -> zero gate writes.
"""
from __future__ import annotations

import asyncio
import json
import os
from collections import Counter
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


async def main() -> None:
    conn = await asyncpg.connect(DSN)
    try:
        rows = await conn.fetch(
            """
            SELECT id, payload->>'unit_id' AS unit_id, decision_status, gate_decision
            FROM admission_candidates
            ORDER BY id
            """
        )
    finally:
        await conn.close()

    def reasons_of(gd):
        if gd is None:
            return []
        if isinstance(gd, str):
            gd = json.loads(gd)
        out = []
        for layer in ("structural", "provenance", "semantic", "admission"):
            sec = (gd or {}).get(layer) or {}
            for r in sec.get("reasons") or []:
                out.append((layer, r))
        return out

    role_prov = []
    per_unit = {}
    for r in rows:
        rs = reasons_of(r["gate_decision"])
        hits = [(l, t) for (l, t) in rs if "role provenance violation" in t]
        if hits:
            role_prov.append((r["unit_id"], r["decision_status"], hits))
        per_unit[r["unit_id"]] = r["decision_status"]

    print(f"total candidates             : {len(rows)}")
    print(f"candidates w/ role-prov viol : {len(role_prov)}")
    print(f"distinct unit_ids            : {len({u for u, _, _ in role_prov})}")

    which_region = Counter()
    for _, _, hits in role_prov:
        for _, t in hits:
            for role in ("explanation", "question"):
                if f"overlaps {role} region" in t:
                    which_region[role] += 1
    print(f"violation region breakdown   : {dict(which_region)}")

    dec = Counter(d for _, d, _ in role_prov)
    print(f"decision_status of those     : {dict(dec)}")

    # any candidate whose unit_id starts with Q or U, listing first few
    print("\nsample violators (first 5):")
    for u, d, hits in role_prov[:5]:
        print(f"  {u:<10} {d:<14} {hits[0][1][:110]}")

    # check: is Q1 among the violators? (prediction: NO)
    viol_ids = {u for u, _, _ in role_prov}
    print(f"\nQ1 present among violators   : {'Q1' in viol_ids}")
    print(f"U52.sub present              : {'U52.sub' in viol_ids}")
    print(f"U53.sub present              : {'U53.sub' in viol_ids}")

    out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL\region_db_forensics.json")
    out.write_text(json.dumps({
        "total_candidates": len(rows),
        "candidates_with_role_provenance_violation": len(role_prov),
        "region_breakdown": dict(which_region),
        "decision_status_breakdown": dict(dec),
        "violator_unit_ids": sorted(viol_ids),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {out}")


if __name__ == "__main__":
    asyncio.run(main())
