"""READ-ONLY: quantify the option-span defect that the restored RAW data exposes.

Observation: 化学 Q7 option A holds the WHOLE line ('A. KCl 溶液 B. ... D. ...')
while B/C/D are bare labels. That is a per-line option-span resolution defect,
not the two isolated cases previously reported (Q4/Q7).

Measures across all 9 papers:
  - options whose text_raw is the bare label only
  - options whose text_raw contains >=2 label tokens (i.e. swallowed siblings)
  - for each such question, the correct label count vs resolved content count
  - distribution by paper
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def load_datajs():
    s = (EA / "data.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def main() -> None:
    d = load_datajs()
    per_paper = Counter()
    q_with_swallow = Counter()
    q_with_bare = Counter()
    examples = []
    total_opts = bare = swallow = 0

    for subj, e in d["subjects"].items():
        for q in (e.get("questions") or []):
            opts = q.get("options_raw") or []
            if not opts:
                continue
            local_bare = local_swallow = 0
            for o in opts:
                total_opts += 1
                t = str(o.get("text_raw") or "").strip()
                lab = str(o.get("label")).upper()
                if t.upper() == lab:
                    bare += 1
                    local_bare += 1
                    per_paper[(subj, "bare")] += 1
                hits = {m.group(1).upper() for m in LAB.finditer(t)}
                if len(hits) >= 2:
                    swallow += 1
                    local_swallow += 1
                    per_paper[(subj, "swallow")] += 1
            if local_bare:
                q_with_bare[subj] += 1
            if local_swallow:
                q_with_swallow[subj] += 1
                if len(examples) < 10:
                    examples.append((subj, q.get("unit_id"), len(opts),
                                     [(o.get("label"), str(o.get("text_raw"))[:46]) for o in opts]))

    print("=" * 94)
    print("OPTION-SPAN DEFECT exposed by restored RAW data")
    print("=" * 94)
    print(f"   total options_raw              : {total_opts}")
    print(f"   text_raw == bare label         : {bare}  ({bare*100//max(total_opts,1)}%)")
    print(f"   text_raw swallows >=2 labels   : {swallow}")

    print("\n   by paper (bare / swallow):")
    subs = sorted(d["subjects"])
    for s in subs:
        print(f"      {s:<5} bare={per_paper.get((s,'bare'),0):<5} swallow={per_paper.get((s,'swallow'),0)}")

    print("\n   questions affected:")
    for s in subs:
        print(f"      {s:<5} with_bare={q_with_bare.get(s,0):<5} with_swallow={q_with_swallow.get(s,0)}")

    print("\n   examples (whole-line swallowed by first option):")
    for subj, uid, n, opts in examples:
        print(f"      {subj} {uid} (n_opts={n})")
        for lab, t in opts:
            print(f"         {lab}: {t!r}")

    # root-cause shape: is the swallow always 'A holds the line'?
    lead = Counter()
    for subj, e in d["subjects"].items():
        for q in (e.get("questions") or []):
            for o in (q.get("options_raw") or []):
                t = str(o.get("text_raw") or "").strip()
                hits = {m.group(1).upper() for m in LAB.finditer(t)}
                if len(hits) >= 2:
                    lead[str(o.get("label"))] += 1
    print("\n   which option label carries the swallowed text:", dict(lead))


if __name__ == "__main__":
    main()
