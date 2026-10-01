import json
from pathlib import Path
from collections import Counter

x27_path = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\X2.7-INT-FULL-01-artifacts\31-per-input-results.json")
e2e_dir = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
out = e2e_dir / "32-x27-vs-e2e01-compare.json"

x27 = json.loads(x27_path.read_text(encoding="utf-8"))
legs = x27.get("legs") or {}
b2 = legs.get("B2_primary") or {}
print("B2_primary keys:", list(b2.keys()))
# find per-input list
items = None
for k in ("results", "inputs", "items", "per_input", "records"):
    if isinstance(b2.get(k), list):
        items = b2[k]
        print("found items at", k, "len", len(items))
        break
if items is None:
    # dump nested structure
    for k,v in b2.items():
        print(" ", k, type(v).__name__, (len(v) if hasattr(v,"__len__") and not isinstance(v,str) else str(v)[:80]))
    # try legs other keys
    for lk, lv in legs.items():
        print("LEG", lk, list(lv.keys()) if isinstance(lv, dict) else type(lv))
