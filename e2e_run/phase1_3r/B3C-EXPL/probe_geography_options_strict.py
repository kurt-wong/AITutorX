"""Read-only, strict: does EVERY geography choice unit have A/B/C/D in source?

Version 1 used a narrow window and under-detected. This version, for each unit:
  - scans the unit's own declared range and a generous neighbourhood
  - counts DISTINCT option labels actually present in real source text
  - reports the exact lines per label
  - decides source-present vs source-absent

An option line is one carrying >=2 distinct labels (single-line option block)
or a line starting with a label (split option line).
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
# label + separator, not preceded by a word char. Half/full width variants.
LABEL = re.compile(r"(?<![\w])([A-Ha-h])\s*[.．、:)）]")
ENTRY = re.compile(r"^(\d{1,3})\s*\\?\s*[.．、:]")

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
by_no = {s.line_no_in_page: s for s in srs}
N = len(srs)


def option_lines(lo: int, hi: int):
    """Return {label: [line_no,...]} and list of candidate option lines."""
    found: dict[str, list[int]] = {}
    cand = []
    for n in range(max(1, lo), min(hi, N) + 1):
        s = by_no.get(n)
        if not s:
            continue
        t = s.text.strip()
        if not t or t.startswith("<"):
            continue
        labs = sorted({mm.group(1).upper() for mm in LABEL.finditer(t)})
        # an option line: >=2 labels, or starts with exactly one label
        starts_with_label = bool(re.match(r"^[（(]?\s*[A-Ha-h]\s*[.．、:)）]", t))
        if len(labs) >= 2 or starts_with_label:
            cand.append((n, labs, t))
            for lb in labs:
                found.setdefault(lb, []).append(n)
    return found, cand


rows = []
for u in m.units:
    is_choice = u.original_question_type in CHOICE
    ql = u.questions_lines
    ml = u.material_lines
    spans = [x for x in (ql, ml, u.stem_lines, u.options_lines) if x]
    lo = min(x[0] for x in spans) if spans else None
    hi = max(x[1] for x in spans) if spans else None

    # generous neighbourhood: unit range +/- 20 lines, bounded by next unit start
    if lo is not None:
        nlo, nhi = max(1, lo - 3), min(N, hi + 20)
    else:
        nlo = nhi = None
    in_range, _ = option_lines(lo, hi) if lo else ({}, [])
    wide, cand = option_lines(nlo, nhi) if nlo else ({}, [])

    rows.append({
        "unit_id": u.unit_id,
        "choice": is_choice,
        "qn": list(u.question_numbers),
        "declared_options": len(u.options),
        "questions_lines": list(ql) if ql else None,
        "in_range_labels": sorted(in_range),
        "wide_labels": sorted(wide),
        "wide_label_lines": {k: v for k, v in wide.items()},
        "abcd_wide": {"A", "B", "C", "D"}.issubset(set(wide)),
        "sample_option_lines": [(n, t[:70]) for n, _, t in cand[:6]],
    })

print(f"{'unit':<10}{'choice':<7}{'opts[]':<7}{'inRange':<18}{'wideLabels':<20}{'A-D?'}")
for r in rows:
    print(f"{r['unit_id']:<10}{str(r['choice']):<7}{r['declared_options']:<7}"
          f"{str(r['in_range_labels']):<18}{str(r['wide_labels']):<20}{r['abcd_wide']}")

ch = [r for r in rows if r["choice"]]
print(f"\nchoice units                        : {len(ch)}")
print(f"  A/B/C/D present in source (wide)  : {sum(1 for r in ch if r['abcd_wide'])}")
print(f"  A/B/C/D absent from source        : {sum(1 for r in ch if not r['abcd_wide'])}")
print(f"  manifest options[] declared       : {sum(1 for r in ch if r['declared_options'])}")

print("\n=== units where wide scan did NOT find A-D (inspect individually) ===")
for r in ch:
    if not r["abcd_wide"]:
        print(f"  {r['unit_id']} qn={r['qn']} wide={r['wide_labels']} "
              f"lines={r['wide_label_lines']}")

print("\n=== evidence sample per unit (first 3 option lines) ===")
for r in rows[:8]:
    print(f"  {r['unit_id']}: {r['sample_option_lines'][:3]}")

(OUT / "geography_options_strict.json").write_text(
    json.dumps({"rows": rows,
                "summary": {"choice": len(ch),
                            "abcd_present_wide": sum(1 for r in ch if r["abcd_wide"]),
                            "abcd_absent_wide": sum(1 for r in ch if not r["abcd_wide"]),
                            "manifest_declared": sum(1 for r in ch if r["declared_options"])}},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwritten: {OUT / 'geography_options_strict.json'}")
