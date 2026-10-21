"""INDEPENDENT P1.4-B verification — diff each patched manifest against its .p14b.bak.

Proves exactly what was hand-changed, and whether the change is limited to
label backfill (allowed?) or also touched boundaries / other fields.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

WATCH = ("options", "options_lines", "stem_lines", "answer_lines", "extra_lines",
         "explanation_lines", "question_numbers", "original_question_type", "unit_type")


def unit_map(m):
    return {str(u.get("unit_id")): u for u in m.get("units", [])}


def main() -> None:
    report = {}
    for bak in sorted(CORPUS.glob("*/*.manifest.json.p14b.bak")):
        cur_p = Path(str(bak)[: -len(".p14b.bak")])
        paper = bak.parent.name
        old = json.loads(bak.read_text(encoding="utf-8"))
        new = json.loads(cur_p.read_text(encoding="utf-8"))
        print("=" * 90)
        print(f"{paper}   {cur_p.name}")
        # top-level diffs
        for k in sorted(set(old) | set(new)):
            if old.get(k) != new.get(k):
                print(f"   TOP-LEVEL FIELD CHANGED: {k!r}")
        om, nm = unit_map(old), unit_map(new)
        if set(om) != set(nm):
            print(f"   UNIT SET CHANGED: added={set(nm)-set(om)} removed={set(om)-set(nm)}")
        changed_units = []
        for uid in sorted(set(om) & set(nm)):
            o, n = om[uid], nm[uid]
            diffs = {}
            for k in WATCH:
                if o.get(k) != n.get(k):
                    diffs[k] = {"old": o.get(k), "new": n.get(k)}
            # any other key
            for k in sorted(set(o) | set(n)):
                if k not in WATCH and o.get(k) != n.get(k):
                    diffs[k] = {"old": o.get(k), "new": n.get(k)}
            if diffs:
                changed_units.append({"unit": uid, "diffs": diffs})
        print(f"   units changed: {len(changed_units)} / {len(nm)}")
        for c in changed_units:
            print(f"     {c['unit']:<10} {json.dumps(c['diffs'], ensure_ascii=False)}")
        report[paper] = {"file": cur_p.name, "changed_units": changed_units,
                         "changed_unit_count": len(changed_units)}

    OUT.joinpath("_p14b_manifest_diff_vs_bak.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_manifest_diff_vs_bak.json'}")


if __name__ == "__main__":
    main()
