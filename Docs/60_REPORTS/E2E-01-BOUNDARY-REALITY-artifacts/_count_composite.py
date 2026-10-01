import json
from pathlib import Path
from collections import Counter

# full-corpus composite_question count (all three shards)
base = Path(r"D:\Project\Papers")
types = Counter()
per = Counter()
for p in base.rglob("*.manifest.json"):
    rel = str(p.relative_to(base))
    if ".pytest_work" in rel or "_archive" in rel:
        continue
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    shard = rel.split("\\")[0]
    for u in m.get("units") or []:
        t = u.get("unit_type") or "?"
        types[t] += 1
        if t == "composite_question":
            per[shard] += 1
print("eligible unit types", dict(types))
print("composite by shard", dict(per), "total", sum(per.values()))
