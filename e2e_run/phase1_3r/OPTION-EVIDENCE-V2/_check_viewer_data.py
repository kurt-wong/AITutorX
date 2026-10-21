"""READ-ONLY: verify MIMO's viewer_data.json actually carries question content."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE\viewer_data.json")
d = json.loads(P.read_text(encoding="utf-8"))

print("run_id :", d.get("run_id"))
print("frozen :", d.get("frozen"))
print("git    :", d.get("git"))
print()
tot = 0
for s, e in d["subjects"].items():
    qs = e.get("questions") or []
    tot += len(qs)
    nonempty = sum(1 for q in qs if (q.get("stem") or "").strip())
    withopts = sum(1 for q in qs if q.get("options"))
    print(f"{s:<4} n={e.get('n_questions')!s:<5} listed={len(qs):<5} "
          f"stem_nonempty={nonempty:<5} with_options={withopts:<5} gate={e.get('gate_counts')}")
print("\nTOTAL questions listed:", tot)

for subj, qn in (("化学", "23"), ("数学", "4")):
    qs = [x for x in (d["subjects"][subj].get("questions") or [])
          if str(x.get("qnum")) == qn or str(x.get("unit_id")) == f"Q{qn}"]
    print(f"\n--- {subj} Q{qn} exported record ({len(qs)} found) ---")
    for x in qs[:1]:
        for k, v in x.items():
            print(f"   {k}: {str(v)[:170]}")
