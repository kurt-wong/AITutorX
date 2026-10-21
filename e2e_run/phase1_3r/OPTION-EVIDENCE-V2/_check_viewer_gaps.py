"""READ-ONLY: does MIMO's export expose the two known-bad cases, and what does
"无题目预览" actually mean?

Checks:
  - 化学 Q20: 4 or 5 options? (E = the P1.4-B artifact)
  - 数学 Q4 : option texts (label-only D? C carrying 2D.?)
  - how many questions have gate == "incomplete" and empty stem (unpreviewable)
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.loads(Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE\viewer_data.json").read_text(encoding="utf-8"))


def find(subj, uid):
    return [q for q in (d["subjects"][subj].get("questions") or [])
            if str(q.get("unit_id")) == uid]


for subj, uid in (("化学", "Q20"), ("数学", "Q4"), ("化学", "Q23")):
    qs = find(subj, uid)
    print("=" * 88)
    print(f"{subj} {uid}  ({len(qs)} record)")
    for q in qs:
        print(f"   gate   : {q.get('gate')}")
        print(f"   reason : {q.get('reason')}")
        print(f"   stem   : {str(q.get('stem'))[:90]!r}")
        print(f"   labels : {q.get('labels')}  n_options={q.get('n_options')}")
        for o in (q.get("options") or []):
            t = str(o.get("text") or "")
            deg = t.strip().upper() == str(o.get("label")).upper()
            print(f"      {o.get('label')}: len={len(t.strip()):<4} {t.strip()[:60]!r}"
                  f"{'   <<< LABEL-ONLY' if deg else ''}")
        print(f"   answer : {str(q.get('answer_text'))[:60]!r} -> {q.get('answer_letter')}")

print("\n" + "=" * 88)
print('What "无题目预览" corresponds to: questions with EMPTY stem')
print("=" * 88)
tot = empty = 0
for s, e in d["subjects"].items():
    qs = e.get("questions") or []
    em = [q for q in qs if not (q.get("stem") or "").strip()]
    recs = [q for q in qs if str(q.get("gate")) == "incomplete"]
    tot += len(qs)
    empty += len(em)
    print(f"   {s:<4} listed={len(qs):<4} empty_stem={len(em):<4} gate_incomplete={len(recs):<4}"
          f"  first_empty={em[0].get('unit_id') if em else '-'}")
print(f"\n   TOTAL listed={tot}  empty_stem={empty}  ({empty * 100 // tot}%)")
one = [q for e in d["subjects"].values() for q in (e.get("questions") or [])
       if not (q.get("stem") or "").strip()][:1]
if one:
    print("   sample empty record:", json.dumps(one[0], ensure_ascii=False)[:300])
