import json
from pathlib import Path
p = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts\20-raw-b2-identity-ok.json")
raw = json.loads(p.read_text(encoding="utf-8"))
print("summary", raw.get("summary"))
for item in raw["papers"]:
    print(json.dumps(item, ensure_ascii=False, indent=2)[:2500])
