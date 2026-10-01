import json
from pathlib import Path
from collections import Counter

base = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
files = ["10-raw-b2-data.json", "10-raw-b2-tests.json", "10-raw-b2-Ocr-markdown.json"]

codes = Counter()
reasons = Counter()
mismatches = Counter()
iv_declared = Counter()
total = 0
by_shard = {}
examples = {}

for fn in files:
    raw = json.loads((base/fn).read_text(encoding="utf-8"))
    shard_codes = Counter()
    for item in raw["papers"]:
        total += 1
        r = item.get("result") or {}
        ig = r.get("identity_gate") or {}
        isc = ig.get("interface_scope") or {}
        code = isc.get("code") or ig.get("reason") or r.get("status")
        reason = isc.get("reason") or ig.get("reason") or ""
        mm = ig.get("mismatches") or ()
        iv = isc.get("declared_identity_version")
        codes[str(code)] += 1
        shard_codes[str(code)] += 1
        reasons[str(reason)[:160]] += 1
        mismatches[str(list(mm))] += 1
        iv_declared[str(iv)] += 1
        if str(code) not in examples:
            examples[str(code)] = {
                "paper": item.get("paper"),
                "code": code,
                "declared_identity_version": iv,
                "mismatches": list(mm),
                "reason": str(reason)[:300],
                "downstream_executed": r.get("downstream_executed"),
            }
    by_shard[fn] = dict(shard_codes)

print("TOTAL", total)
print("BY_SHARD", json.dumps(by_shard, ensure_ascii=False, indent=2))
print("CODES", dict(codes))
print("IDENTITY_VERSION_DECLARED", dict(iv_declared))
print("MISMATCHES", dict(mismatches))
print("REASONS top:")
for k,v in reasons.most_common(10):
    print(v, "|", k)
print("EXAMPLES:")
for k,v in examples.items():
    print(k, json.dumps(v, ensure_ascii=False))
