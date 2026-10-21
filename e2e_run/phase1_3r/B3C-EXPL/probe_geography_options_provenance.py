"""Read-only: Options provenance probe for 地理 (Owner-directed, narrow scope).

For each of the 25 geography units, determine from the REAL source artifact:
  1. is the unit choice-type?
  2. does its declared source range actually contain A/B/C/D option lines?
  3. does the manifest declare options[]?
  4. where does the option evidence live (which field / which lines)?

Establishes whether 'options_missing_for_choice' is
  - source absent (-> Owner semantic question), or
  - source present but undeclared (-> Producer/interface evidence loss).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, r"D:\Project\AITutors-v3\backend")

from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

MAN = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C"
           r"\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

CHOICE = {"single_choice", "multiple_choice", "true_false"}
# option label at line start: A. A、 A． A) （A） etc.
OPT_LEAD = re.compile(r"^[（(]?\s*([A-Ha-h])\s*[.．、:：)）]")
OPT_ANY = re.compile(r"(?<![\w])([A-Ha-h])\s*[.．、:)）]")

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
by_no = {s.line_no_in_page: s for s in srs}
n_total = len(srs)


def option_labels_in(lo: int, hi: int, *, lead_only: bool) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for n in range(max(1, lo), min(hi, n_total) + 1):
        s = by_no.get(n)
        if not s:
            continue
        t = s.text.strip()
        if not t:
            continue
        mm = OPT_LEAD.match(t) if lead_only else OPT_ANY.search(t)
        if mm:
            out.setdefault(mm.group(1).upper(), []).append(n)
    return out


rows = []
for u in m.units:
    is_choice = u.original_question_type in CHOICE
    ql = u.questions_lines
    ml = u.material_lines
    # widest declared span for this unit
    spans = [x for x in (ql, ml, u.stem_lines, u.options_lines) if x]
    lo = min(x[0] for x in spans) if spans else None
    hi = max(x[1] for x in spans) if spans else None

    lead_in_range = option_labels_in(lo, hi, lead_only=True) if lo else {}
    # also look just after the declared range (options often sit after questions_lines)
    lead_after = option_labels_in(hi + 1, hi + 14, lead_only=True) if hi else {}

    full = sorted(set(lead_in_range) | set(lead_after))
    rows.append({
        "unit_id": u.unit_id,
        "choice": is_choice,
        "question_numbers": list(u.question_numbers),
        "declared_options": len(u.options),
        "has_stem_lines": bool(u.stem_lines),
        "has_options_lines": bool(u.options_lines),
        "questions_lines": list(ql) if ql else None,
        "material_lines": list(ml) if ml else None,
        "ABCD_in_declared_range": {k: v for k, v in lead_in_range.items()},
        "ABCD_just_after_range": {k: v for k, v in lead_after.items()},
        "ABCD_union": full,
        "abcd_present": sorted(set(full)) == ["A", "B", "C", "D"] or
                        {"A", "B", "C", "D"}.issubset(set(full)),
    })

print(f"{'unit':<10}{'choice':<7}{'opts[]':<7}{'stemL':<6}{'optL':<6}"
      f"{'ql':<14}{'ABCD_in_range':<16}{'justAfter':<14}")
for r in rows:
    print(f"{r['unit_id']:<10}{str(r['choice']):<7}{r['declared_options']:<7}"
          f"{str(r['has_stem_lines']):<6}{str(r['has_options_lines']):<6}"
          f"{str(r['questions_lines']):<14}"
          f"{str(sorted(r['ABCD_in_declared_range'])):<16}"
          f"{str(sorted(r['ABCD_just_after_range'])):<14}")

n_choice = sum(1 for r in rows if r["choice"])
n_present = sum(1 for r in rows if r["choice"] and r["abcd_present"])
n_absent = sum(1 for r in rows if r["choice"] and not r["abcd_present"])
print(f"\nchoice units           : {n_choice}")
print(f"  A/B/C/D found in src : {n_present}")
print(f"  no A/B/C/D in src    : {n_absent}")
print(f"non-choice units       : {sum(1 for r in rows if not r['choice'])}")

print("\n=== detailed view: first 5 units, declared range + following options ===")
for r in rows[:5]:
    u = next(x for x in m.units if x.unit_id == r["unit_id"])
    spans = [x for x in (u.questions_lines, u.material_lines) if x]
    lo = min(x[0] for x in spans)
    hi = max(x[1] for x in spans)
    print(f"\n{r['unit_id']} qn={r['question_numbers']} type={u.original_question_type} "
          f"range={lo}-{hi}")
    for n in range(lo, min(hi + 12, n_total) + 1):
        s = by_no.get(n)
        if s and s.text.strip():
            mark = "OPT" if OPT_LEAD.match(s.text.strip()) else "   "
            print(f"   {mark} L{n}: {s.text.strip()[:100]!r}")

(OUT / "geography_options_provenance.json").write_text(
    json.dumps({"rows": rows,
                "summary": {"choice": n_choice, "abcd_present": n_present,
                            "abcd_absent": n_absent}},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwritten: {OUT / 'geography_options_provenance.json'}")
