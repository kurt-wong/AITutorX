import json
from pathlib import Path

base = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
raw = json.loads((base/"10-raw-b2-Ocr-markdown.json").read_text(encoding="utf-8"))

for item in raw["papers"]:
    r = item.get("result") or {}
    ig = r.get("identity_gate") or {}
    isc = ig.get("interface_scope") or {}
    if isc.get("code") == "semantic_pending" or (ig.get("identity_state") == "PASSED") or (r.get("status") != "identity_blocked"):
        print(json.dumps({"paper": item.get("paper"), "result": r}, ensure_ascii=False, indent=2)[:2500])
        break

# also print distribution of identity_state
from collections import Counter
c=Counter(); st=Counter(); st2=Counter(); de=Counter()
for item in raw["papers"]:
    r=item.get("result") or {}
    ig=r.get("identity_gate") or {}
    c[str(ig.get("identity_state"))]+=1
    st[str(ig.get("semantic_state"))]+=1
    st2[str(r.get("status"))]+=1
    de[str(r.get("downstream_executed"))]+=1
print("identity_state", dict(c))
print("semantic_state", dict(st))
print("status", dict(st2))
print("downstream_executed", dict(de))
print("top summary", raw.get("summary"))
