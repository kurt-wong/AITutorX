"""READ-ONLY: inspect specific units post-fix."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.loads(Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_POSTFIX_RESULT.json").read_text(encoding="utf-8"))
for subj, uid in (("化学", "Q17"), ("化学", "Q20"), ("历史", "Q29"), ("英语", "Q5-6"), ("数学", "Q1")):
    q = d["now"].get(subj, {}).get(uid)
    print("=" * 76)
    if not q:
        print(f"{subj} {uid}: MISSING")
        continue
    print(f"{subj} {uid}   gate={q['gate']}   labels={q['labels']}")
    for o in q["options"]:
        print(f"    {o['label']}: {o['text_raw']!r}")
