"""Read-only: what is on 地理's declared material_lines, and how do question
numbers appear in its source? Answers the two open sub-questions:
  (a) why 25/25 material refs -> "material marker text missing"
  (b) why only 11/55 stems resolved
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, r"D:\Project\AITutors-v3\backend")

from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

MAN = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C"
           r"\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json")

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
by_no = {s.line_no_in_page: s for s in srs}

print("== declared material_lines sample (first 5 units) ==")
for u in m.units[:5]:
    ml = u.material_lines
    print(f"\n{u.unit_id} qn={u.question_numbers} material_lines={ml}")
    if ml:
        lo, hi = ml
        for n in range(lo, min(hi, lo + 3) + 1):
            s = by_no.get(n)
            if s:
                print(f"   L{n}: {s.text[:150]!r}")

print("\n== all declared material_lines (lo,hi) ==")
print([tuple(u.material_lines) for u in m.units if u.material_lines])

print("\n== how do question numbers look in source? (first 40 non-empty lines) ==")
shown = 0
for s in srs:
    t = s.text.strip()
    if not t:
        continue
    print(f"  L{s.line_no_in_page}: {t[:100]!r}")
    shown += 1
    if shown >= 40:
        break

print("\n== lines that literally start with a number-dot (entry style) ==")
import re
ent = re.compile(r"^(\d{1,3})\s*[.．、:]")
hits = [s for s in srs if ent.match(s.text.strip())]
print(f"count={len(hits)}")
for s in hits[:30]:
    print(f"  L{s.line_no_in_page}: {s.text.strip()[:90]!r}")

print("\n== total source lines ==", len(srs))
