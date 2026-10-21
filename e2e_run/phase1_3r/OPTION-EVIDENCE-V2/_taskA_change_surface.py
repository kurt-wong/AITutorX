"""READ-ONLY: characterise the Task A change surface precisely.

Issues to resolve:
  a) my previous match keyed by unit_id only -> Q17/Q20 exist in 9 subjects,
     producing spurious rows. Re-key by (subject, unit_id, leaf_id).
  b) why did 183 questions change when only 97 were affected?
     Distinguish: label-strip differences vs genuine swallowing fixes.
  c) what are the 2 remaining swallow options?
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_PREFIX_BASELINE.json")
POST = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_POSTFIX_RESULT.json")
LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def keys(d):
    out = {}
    for subj, qs in d.items():
        for uid, q in qs.items():
            lid = q.get("leaf_id") or uid
            out[(subj, str(uid), str(lid))] = q
    return out


def main() -> None:
    base_raw = json.loads(BASE.read_text(encoding="utf-8"))
    post_raw = json.loads(POST.read_text(encoding="utf-8"))

    b = {}
    for subj, e in base_raw["subjects"].items():
        for q in e["questions"]:
            b[(subj.replace(".manifest", ""), str(q["unit_id"]), str(q["leaf_id"]))] = q
    p = {}
    for subj, qs in post_raw["now"].items():
        for uid, q in qs.items():
            p[(subj.replace(".manifest", ""), str(uid), str(uid))] = q

    print("=" * 94)
    print("a) key space")
    print("=" * 94)
    print(f"   baseline keys: {len(b)}   post keys: {len(p)}")
    common = set(b) & set(p)
    print(f"   common       : {len(common)}")
    print(f"   post-only    : {len(set(p) - set(b))}   sample={list(set(p)-set(b))[:4]}")

    print("\n" + "=" * 94)
    print("b) change classification (matched keys only)")
    print("=" * 94)
    cat = Counter()
    examples = {}
    q_was_affected = 0
    for k in sorted(common):
        bq, pq = b[k], p[k]
        bo = [(o["label"], o["text_raw"]) for o in (bq.get("options") or [])]
        po = [(o["label"], o["text_raw"]) for o in (pq.get("options") or [])]
        if bo == po:
            cat["unchanged"] += 1
            continue
        was = any(o.get("bare") or o.get("swallow") for o in (bq.get("options") or []))
        if was:
            q_was_affected += 1
            cat["changed_WAS_affected"] += 1
        else:
            cat["changed_was_not_affected"] += 1
            # classify the nature of the change on untouched questions
            btxt = [t for _, t in bo]
            ptxt = [t for _, t in po]
            blab = [l for l, _ in bo]
            plab = [l for l, _ in po]
            if blab != plab:
                key = "labels differ"
            elif all(t.startswith(l) for (l, t) in po) and not all(t.startswith(l) for (l, t) in bo):
                key = "post keeps label prefix, base did not"
            elif all(t.startswith(l) for (l, t) in bo) and not all(t.startswith(l) for (l, t) in po):
                key = "post STRIPS label prefix (normalisation)"
            else:
                key = "content text differs"
            cat[key] += 1
            examples.setdefault(key, (k, bo[:2], po[:2]))

    for k, v in cat.most_common():
        print(f"   {k:<40}{v}")
    print(f"\n   questions that were affected pre-fix and changed: {q_was_affected}  (expected 97)")
    print("\n   examples of changes on NOT-previously-affected questions:")
    for k, (kk, bo, po) in examples.items():
        print(f"      [{k}] {kk}")
        print(f"         base: {bo}")
        print(f"         post: {po}")

    print("\n" + "=" * 94)
    print("c) remaining swallow options post-fix")
    print("=" * 94)
    for subj, qs in post_raw["now"].items():
        for uid, q in qs.items():
            for o in q["options"]:
                if o["swallow"]:
                    print(f"   {subj}/{uid} {o['label']}: {o['text_raw'].strip()[:60]!r}")


if __name__ == "__main__":
    main()
