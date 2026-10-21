"""Read-only: what would the Authorized fix ACTUALLY attach, per unit?

The single sub-question carries ALL of the unit's declared options, but the sub
represents only question_numbers[0]. For a multi-question unit that means the
first question gets its own options and the remaining questions would receive
them too. Quantify how many units that affects, and how many are single-question
(where the mapping is unambiguous).
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"D:\Project\AITutors-v3\backend")

from scripts.preprocessing_consumer.manifest_reader import load_manifest

ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
MAN = ROOT / "地理" / "2018北京春季高中会考地理（教师版）(1).manifest.json"
CHOICE = {"single_choice", "multiple_choice", "true_false"}

m = load_manifest(MAN)
single = multi = 0
print("=== 地理 choice units: how many question numbers does each sub represent? ===")
multi_units = []
for u in m.units:
    if u.original_question_type not in CHOICE:
        continue
    k = len(u.question_numbers)
    if k <= 1:
        single += 1
    else:
        multi += 1
        multi_units.append((u.unit_id, list(u.question_numbers)))
    qns = str(list(u.question_numbers))
    print(f"   {u.unit_id:<10} question_numbers={qns:<16} "
          f"({'multi -> ambiguous mapping' if k > 1 else 'single -> unambiguous'})")

print(f"\nchoice units with exactly 1 question number : {single}")
print(f"choice units with >1 question numbers       : {multi}")
print(f"total question numbers behind those units   : "
      f"{sum(len(q) for _, q in multi_units) + single}")

print("\n=== the SAME issue across the whole corpus (composite + choice) ===")
tot = Counter()
for f in sorted(ROOT.rglob("*.manifest.json")):
    j = load_manifest(f)
    for u in j.units:
        if u.unit_type != "composite_question":
            continue
        if u.original_question_type not in CHOICE:
            continue
        tot["composite_choice"] += 1
        if len(u.question_numbers) > 1:
            tot["multi_qn"] += 1
        else:
            tot["single_qn"] += 1
print(dict(tot))
