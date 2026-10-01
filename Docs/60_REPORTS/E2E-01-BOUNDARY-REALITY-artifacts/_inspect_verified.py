import json
from pathlib import Path
from collections import Counter

base = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
raw = json.loads((base/"10-raw-b2-Ocr-markdown.json").read_text(encoding="utf-8"))

verified = []
failed = []
for item in raw["papers"]:
    r = item.get("result") or {}
    ig = r.get("identity_gate") or {}
    if ig.get("identity_state") == "VERIFIED":
        verified.append((item.get("paper"), ig, r.get("status"), r.get("downstream_executed")))
    else:
        failed.append((item.get("paper"), ig.get("mismatches"), (ig.get("interface_scope") or {}).get("code")))

print("VERIFIED count", len(verified))
# dump one full VERIFIED identity_gate
print("VERIFIED sample identity_gate:")
print(json.dumps(verified[0][1], ensure_ascii=False, indent=2)[:2000])
print("verified papers sample:", [v[0] for v in verified[:5]])
print("FAILED count", len(failed))
print("failed codes", Counter(f[2] for f in failed))
