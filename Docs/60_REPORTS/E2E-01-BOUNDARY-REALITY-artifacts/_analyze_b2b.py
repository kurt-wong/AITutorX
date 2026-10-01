import json
from pathlib import Path
from collections import Counter

base = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
files = ["10-raw-b2-data.json", "10-raw-b2-tests.json", "10-raw-b2-Ocr-markdown.json"]

# dump one result shape
raw0 = json.loads((base/files[0]).read_text(encoding="utf-8"))
print("summary keys:", raw0.get("summary"))
print("first result:", json.dumps(raw0["papers"][0]["result"], ensure_ascii=False, indent=2)[:1500])

codes = Counter()
states = Counter()
mismatches = Counter()
total = 0
examples = {}
for fn in files:
    raw = json.loads((base/fn).read_text(encoding="utf-8"))
    for item in raw["papers"]:
        total += 1
        r = item.get("result") or {}
        code = r.get("code") or r.get("reason_code") or r.get("error_code")
        st = r.get("identity_state") or r.get("status") or r.get("gate")
        reason = r.get("reason") or r.get("message") or ""
        codes[str(code)] += 1
        states[str(st)] += 1
        mm = tuple(r.get("mismatches") or r.get("missing_fields") or ())
        mismatches[str(mm)] += 1
        key = str(code)
        if key not in examples:
            examples[key] = {"paper": item.get("paper"), "result": r}

print("total", total)
print("codes", dict(codes))
print("states", dict(states))
print("mismatches top", mismatches.most_common(6))
for k,v in examples.items():
    print("EXAMPLE", k, json.dumps(v, ensure_ascii=False)[:500])
