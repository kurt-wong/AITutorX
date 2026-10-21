"""READ-ONLY: clean characterisation of the Task A change surface.

Two confounds in the previous pass must be removed:
  1. label-prefix stripping ("A. xxx" -> " xxx") is a *representation* change in
     the new label-after -> before-next-label span; comparing raw text counts it
     as a change. Normalise by stripping a leading "<label>." prefix on BOTH sides.
  2. composite leaf/root keying: baseline stores leaf_id, post stores unit_id.
     Compare on (subject, unit_id) and report key-space gaps separately.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")
BASE = D / "_TASKA_PREFIX_BASELINE.json"
POST = D / "_TASKA_POSTFIX_RESULT.json"

PREFIX = re.compile(r"^\s*[A-Ha-h]\s*[.．、:：,，。)）]\s*")


def strip(t: str) -> str:
    return PREFIX.sub("", str(t or "")).strip()


def main() -> None:
    braw = json.loads(BASE.read_text(encoding="utf-8"))
    praw = json.loads(POST.read_text(encoding="utf-8"))

    b = {(s.replace(".manifest", ""), str(q["unit_id"])): q
         for s, e in braw["subjects"].items() for q in e["questions"]}
    p = {(s.replace(".manifest", ""), str(uid)): q
         for s, qs in praw["now"].items() for uid, q in qs.items()}

    print("=" * 94)
    print("1. KEY SPACE (subject, unit_id)")
    print("=" * 94)
    print(f"   baseline={len(b)}  post={len(p)}  common={len(set(b)&set(p))}")
    only_b = sorted(set(b) - set(p))
    only_p = sorted(set(p) - set(b))
    print(f"   baseline-only={len(only_b)}  post-only={len(only_p)}")
    print(f"   baseline-only sample: {only_b[:8]}")
    print(f"   post-only sample    : {only_p[:8]}")
    # do the post-only ones exist in baseline under a DIFFERENT unit_id? (composite root vs leaf)
    b_by_unit = {}
    for s, e in braw["subjects"].items():
        for q in e["questions"]:
            b_by_unit.setdefault((s.replace(".manifest", ""), str(q["unit_id"])), []).append(q)
    explain = []
    for k in only_p[:10]:
        subj, uid = k
        # baseline composite roots whose leaf ids start with uid
        cands = [k2 for k2 in b if k2[0] == subj and (uid.startswith(k2[1]) or k2[1].startswith(uid))]
        explain.append((k, cands[:3]))
    print("   post-only key -> candidate baseline keys:")
    for k, c in explain:
        print(f"      {k}  ->  {c}")

    print("\n" + "=" * 94)
    print("2. REAL CONTENT CHANGE (after stripping label prefix on both sides)")
    print("=" * 94)
    cat = Counter()
    real = []
    for k in sorted(set(b) & set(p)):
        bq, pq = b[k], p[k]
        bo = [(o["label"], strip(o.get("text_raw") or "")) for o in (bq.get("options") or [])]
        po = [(o["label"], strip(o.get("text_raw") or "")) for o in (pq.get("options") or [])]
        was = any(o.get("bare") or o.get("swallow") for o in (bq.get("options") or []))
        if bo == po:
            cat["REPRESENTATION-ONLY (label prefix)"] += 1 if (
                [(o["label"], o.get("text_raw") or "") for o in (bq.get("options") or [])]
                != [(o["label"], o.get("text_raw") or "") for o in (pq.get("options") or [])]
            ) else 0
            cat["truly unchanged"] += 1
            continue
        cat["REAL content change"] += 1
        real.append((k, was, bo, po))

    for k, v in cat.most_common():
        print(f"   {k:<40}{v}")

    print(f"\n   REAL changes: {len(real)}")
    was_n = sum(1 for r in real if r[1])
    print(f"      of which previously-affected questions: {was_n}")
    print(f"      of which previously-CLEAN questions    : {len(real) - was_n}")
    for (k, was, bo, po) in [r for r in real if not r[1]][:6]:
        print(f"\n      [clean before] {k}")
        print(f"         base: {bo}")
        print(f"         post: {po}")

    print("\n" + "=" * 94)
    print("3. ACCEPTANCE ASSERTIONS (content spans, label prefix stripped)")
    print("=" * 94)
    checks = [("数学", "Q1"), ("数学", "Q4")]
    for subj, uid in checks:
        q = p.get((subj, uid))
        if not q:
            print(f"   {subj} {uid}: MISSING")
            continue
        got = {o["label"]: strip(o["text_raw"]) for o in q["options"]}
        print(f"   {subj} {uid}: {got}")
    q1 = p.get(("数学", "Q1"))
    if q1:
        got = {o["label"]: strip(o["text_raw"]) for o in q1["options"]}
        want = {"A": "1", "B": "2", "C": "$ \\pi $", "D": "$ 2\\pi $"}
        print(f"\n   数学 Q1 == expected? {got == want}   (expected {want})")
        alt = {"A": "1", "B": "2", "C": "π", "D": "2π"}
        print(f"   数学 Q1 == literal  A='1' B='2' C='π' D='2π'? "
              f"{got.get('A')=='1' and got.get('B')=='2' and 'pi' in got.get('C','') and 'pi' in got.get('D','')}")
    q4 = p.get(("数学", "Q4"))
    if q4:
        print(f"\n   数学 Q4 no '2D.' swallowed? "
              f"{not any('2D.' in (o['text_raw'] or '') or '2D.' in strip(o['text_raw']) for o in q4['options'])}")
    q17 = p.get(("化学", "Q17"))
    if q17:
        print(f"   化学 Q17 unchanged labels? {[o['label'] for o in q17['options']]}")
    q20 = p.get(("化学", "Q20"))
    if q20:
        print(f"   化学 Q20 n_options = {len(q20['options'])} (expect 5)")


if __name__ == "__main__":
    main()
