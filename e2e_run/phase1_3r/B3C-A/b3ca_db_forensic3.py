"""Locate the gate decision inside admission_candidates and classify outcomes."""
from __future__ import annotations

import asyncio
import json
import re
from collections import Counter, defaultdict

import asyncpg

DSN = "postgresql://aitutors:change-me@localhost:5432/aitutors"


def find_gate(obj, path=""):
    """Recursively locate dicts that look like gate policy output."""
    hits = []
    if isinstance(obj, dict):
        if "decision" in obj and "layers" in obj:
            hits.append((path, obj))
        for k, v in obj.items():
            hits.extend(find_gate(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(find_gate(v, f"{path}[{i}]"))
    return hits


async def main() -> None:
    c = await asyncpg.connect(DSN)
    cols = await c.fetch(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='admission_candidates' ORDER BY ordinal_position"
    )
    print("COLS:", [r["column_name"] for r in cols])

    rows = await c.fetch("SELECT * FROM admission_candidates")
    first = dict(rows[0])
    print("\n--- non-payload columns of row 0 ---")
    for k, v in first.items():
        if k == "payload":
            continue
        print(f"  {k} = {str(v)[:200]}")

    pl = first["payload"]
    if isinstance(pl, str):
        pl = json.loads(pl)
    print("\npayload keys:", sorted(pl.keys()))

    hits = find_gate(pl)
    print("\ngate-policy hits in row 0:", [h[0] for h in hits])
    if hits:
        print("sample:", json.dumps(hits[0][1], ensure_ascii=False)[:700])

    # gate lives in the dedicated columns, not the payload
    path = "COLUMN:gate_decision"
    print("\npath:", path)

    decisions = Counter()
    kinds = Counter()
    over_units = defaultdict(list)
    pat = re.compile(r"answer span '([^']+)' overlaps explanation region at lines \[([^\]]*)\]")

    for r in rows:
        gp = r["gate_decision"]
        if isinstance(gp, str):
            gp = json.loads(gp)
        if not isinstance(gp, dict):
            continue
        decisions[(gp.get("decision") or "?") + " | col=" + str(r["decision_status"])] += 1
        for reason in gp.get("reasons") or []:
            if "overlaps explanation region" in reason:
                kinds["answer_overlaps_explanation"] += 1
                m = pat.search(reason)
                if m:
                    over_units[m.group(1)].append(re.findall(r"P1L\d+", m.group(2)))
            elif "not strict-auto" in reason:
                kinds["type_not_strict_auto"] += 1
            elif "answer not expressible" in reason:
                kinds["answer_not_expressible"] += 1
            elif "no non-empty stem text" in reason:
                kinds["empty_stem"] += 1
            elif "not byte-proven" in reason:
                kinds["not_byte_proven"] += 1
            else:
                kinds["other: " + reason[:70]] += 1

    print("\n=== decisions ===", dict(decisions))
    print("\n=== reason kinds ===")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f"  {v:5}  {k}")
    print(f"\ndistinct spans with answer∩explanation overlap: {len(over_units)}")
    for i, (sp, refs) in enumerate(list(over_units.items())[:12]):
        print(f"   {sp}: {refs[0][:6]}{'...' if len(refs[0]) > 6 else ''} ({len(refs[0])} lines)")
    await c.close()


asyncio.run(main())
