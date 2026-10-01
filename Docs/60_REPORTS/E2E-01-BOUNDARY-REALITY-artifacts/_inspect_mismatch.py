import json
from pathlib import Path
p = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts\30-raw-b2-mismatch.json")
raw = json.loads(p.read_text(encoding="utf-8"))
print(json.dumps(raw["papers"][0]["result"], ensure_ascii=False, indent=2)[:2000])
