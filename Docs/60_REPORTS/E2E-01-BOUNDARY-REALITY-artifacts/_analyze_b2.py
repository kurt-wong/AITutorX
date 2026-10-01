import json
from pathlib import Path
from collections import Counter

base = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
files = ["10-raw-b2-data.json", "10-raw-b2-tests.json", "10-raw-b2-Ocr-markdown.json"]
codes = Counter()
reasons = Counter()
total = 0
sample = []
for fn in files:
    p = base / fn
    raw = json.loads(p.read_text(encoding="utf-8"))
    papers = raw.get("papers") or raw.get("items") or raw
    if isinstance(papers, dict):
        papers = papers.get("papers", [])
    for item in papers:
        total += 1
        # try several shapes
        rej = item.get("interface_scope_rejected") or item.get("identity_gate") or item.get("result") or {}
        code = rej.get("code") or item.get("code") or item.get("identity_state") or item.get("status")
        reason = rej.get("reason") or item.get("reason") or ""
        codes[str(code)] += 1
        key = str(reason)[:120]
        reasons[key] += 1
        if len(sample) < 8:
            sample.append({"name": item.get("paper") or item.get("manifest") or item.get("name"), "code": code, "reason": str(reason)[:200], "keys": list(item.keys())[:12]})

print("total", total)
print("codes", dict(codes))
print("top reasons:")
for k,v in reasons.most_common(8):
    print(v, k[:150])
print("samples:")
for s in sample:
    print(s)
print("top-level keys of first file:", list(json.loads((base/files[0]).read_text(encoding="utf-8")).keys()))
