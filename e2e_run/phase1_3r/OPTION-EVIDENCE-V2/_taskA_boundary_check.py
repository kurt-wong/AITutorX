"""READ-ONLY: before Task A is authorized, check two boundary facts on the
affected set (97 questions with bare/swallowed options):

  1. are any affected questions COMPOSITE units?  (English listening groups,
     geography multi-qn sets). If yes, an options fix can change leaf counts /
     composite recursion and Task A's invariant set is wider than "option text".
  2. is the defect spread across BOTH line shapes (multi-option-per-line vs
     wrapped continuation), i.e. is one fix enough?
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def loadjs(p: Path):
    s = p.read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def main() -> None:
    v2 = loadjs(EA / "data_v2.js")
    affected = []
    for subj, e in v2["subjects"].items():
        for q in (e.get("questions") or []):
            opts = q.get("options_raw") or []
            if not opts:
                continue
            bare = sum(1 for o in opts
                       if str(o.get("text_raw") or "").strip().upper()
                       == str(o.get("label") or "").upper())
            swallow = sum(1 for o in opts
                          if len({m.group(1).upper()
                                  for m in LAB.finditer(str(o.get("text_raw") or ""))}) >= 2)
            if bare or swallow:
                affected.append({
                    "subj": subj, "unit_id": str(q.get("unit_id")),
                    "leaf_id": str(q.get("leaf_id") or ""),
                    "bare": bare, "swallow": swallow, "n_opts": len(opts),
                    "ir_status": q.get("ir_status"),
                    "line_refs": sorted({r for o in opts for r in (o.get("line_refs") or [])}),
                })

    print("=" * 92)
    print(f"1. AFFECTED SET: {len(affected)} questions")
    print("=" * 92)
    print("   by subject:", dict(Counter(a["subj"] for a in affected)))

    # composite detection: leaf_id != unit_id indicates a sub-question leaf
    comp = [a for a in affected if a["leaf_id"] and a["leaf_id"] != a["unit_id"]]
    print(f"\n   leaf_id != unit_id (composite sub-question): {len(comp)}")
    for c in comp[:15]:
        print(f"      {c['subj']}/{c['unit_id']}  leaf={c['leaf_id']}  n_opts={c['n_opts']}")

    # line shape: how many distinct lines do the option spans cover?
    multi_line = [a for a in affected if len(a["line_refs"]) > 1]
    same_line = [a for a in affected if len(a["line_refs"]) == 1]
    print(f"\n2. LINE SHAPE of affected questions")
    print(f"   all options on ONE line  : {len(same_line)}   (the 单行多选项 case)")
    print(f"   options span >1 line     : {len(multi_line)}   (wrapped / other)")
    print("\n   examples of multi-line affected questions:")
    for a in multi_line[:10]:
        print(f"      {a['subj']}/{a['unit_id']} lines={a['line_refs']} bare={a['bare']} swallow={a['swallow']}")

    # distribution of bare counts: full-loss vs partial
    dist = Counter(a["bare"] for a in affected)
    print(f"\n3. bare-count distribution (how many options lost per question): {dict(sorted(dist.items()))}")
    tot_opts = sum(a["n_opts"] for a in affected)
    tot_bare = sum(a["bare"] for a in affected)
    print(f"   affected questions hold {tot_opts} options, of which {tot_bare} are bare "
          f"({tot_bare*100//max(tot_opts,1)}%)")


if __name__ == "__main__":
    main()
