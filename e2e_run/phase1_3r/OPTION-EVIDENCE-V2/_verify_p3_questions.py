"""READ-ONLY: verify P3 — the two bare=1 questions.

Key question: is 化学 Q17's shell='H' an option-splitting artefact (same defect as
the other 95), or is 'H' a CHEMISTRY SYMBOL misparsed as an option label
(a DIFFERENT defect class)? If the latter, Task A must not touch it.

Also verifies 英语 Q5-6 (composite; known answer=C).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def loadjs(p: Path):
    s = p.read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def main() -> None:
    v2 = loadjs(EA / "data_v2.js")

    for subj, uid in (("化学", "Q17"), ("英语", "Q5-6")):
        recs = [q for q in (v2["subjects"][subj].get("questions") or [])
                if str(q.get("unit_id")) == uid]
        print("=" * 92)
        print(f"{subj} {uid}   ({len(recs)} record)")
        for q in recs:
            print(f"   leaf_id={q.get('leaf_id')} gate={q.get('gate_display')} "
                  f"ir={q.get('ir_status')} leaf_present={q.get('leaf_present')}")
            print(f"   labels={q.get('labels')}  n_opts={len(q.get('options_raw') or [])}")
            for o in (q.get("options_raw") or []):
                t = str(o.get("text_raw") or "")
                bare = t.strip().upper() == str(o.get("label")).upper()
                print(f"      {o.get('label')}: len={len(t.strip()):<4} {t.strip()[:66]!r}"
                      f"{'   <<< BARE' if bare else ''}")
                print(f"           span={o.get('span_id')} lines={o.get('line_refs')}")

        # manifest declaration for the same unit
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        if man_p.exists():
            m = json.loads(man_p.read_text(encoding="utf-8"))
            for u in m.get("units", []):
                if str(u.get("unit_id")) == uid:
                    print(f"\n   --- manifest declaration ---")
                    print(f"   unit_type={u.get('unit_type')} qtype={u.get('original_question_type')}")
                    print(f"   options_lines={u.get('options_lines')}")
                    print(f"   options={[(o.get('label'), o.get('start_line'), o.get('end_line')) for o in (u.get('options') or [])]}")
                    print(f"   question_numbers={u.get('question_numbers')}")

    # where does the 'H' come from? show the source lines
    print("\n" + "=" * 92)
    print("SOURCE LINES around 化学 Q17")
    print("=" * 92)
    mp = json.loads((EA / "04_V3_INPUT" / "化学.manifest.json").read_text(encoding="utf-8"))
    src = Path(str(mp.get("source_file", "")))
    if src.exists():
        lines = src.read_text(encoding="utf-8").splitlines()
        for i in range(118, min(132, len(lines)) + 1):
            print(f"   L{i:<5} {lines[i-1][:100]}")

    # global: any option label whose letter is outside A-D among affected?
    print("\n" + "=" * 92)
    print("Any option labels beyond A-D anywhere in the corpus?")
    print("=" * 92)
    from collections import Counter
    c = Counter()
    for s, e in v2["subjects"].items():
        for q in (e.get("questions") or []):
            for o in (q.get("options_raw") or []):
                c[str(o.get("label"))] += 1
    print("   label histogram:", dict(c))


if __name__ == "__main__":
    main()
