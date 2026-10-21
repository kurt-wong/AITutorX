"""Read-only: pre-implementation evidence table for the 7 `question number not found`
units (Owner-requested), plus the exact identity -> option causal counts.

No code change. Reports, for each not-found unit:
  manifest question_numbers / printed_number / printed_provenance
  material_lines / questions_lines
  the real source line(s) where the number appears, in raw text
  what is_question_start currently sees
  classification: source identity present-but-unparsed  vs  genuinely absent
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
MAN = ROOT / "地理" / "2018北京春季高中会考地理（教师版）(1).manifest.json"
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.resolver.match_normalization import (  # noqa: E402
    is_question_start,
    normalize_text,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

NOT_FOUND = {"16", "26", "51", "52", "53", "54", "55"}

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
texts = [s.text for s in srs]
by_no = {s.line_no_in_page: s for s in srs}

print("=" * 100)
print("EVIDENCE TABLE — 7 `question number not found` units (地理)")
print("=" * 100)
rows = []
for u in m.units:
    q0 = str(u.question_numbers[0]) if u.question_numbers else None
    if q0 not in NOT_FOUND:
        continue
    # where does the number appear anywhere in source?
    occ = []
    for s in srs:
        raw = s.text
        norm = normalize_text(raw)
        if is_question_start(norm) == q0:
            occ.append(("line_start", s.line_no_in_page, raw.strip()))
        # mid-line <qn>. or <qn>\. form
        if re.search(rf"(?<![\d]){q0}\s*\\?[.．、:]", raw):
            occ.append(("in_line", s.line_no_in_page, raw.strip()))
    lo, hi = u.material_lines or (None, None)
    mat_line = texts[lo - 1].strip() if lo else None
    rows.append({
        "unit_id": u.unit_id,
        "question_numbers": list(u.question_numbers),
        "printed_number": u.printed_number,
        "printed_provenance": u.printed_provenance,
        "material_lines": list(u.material_lines) if u.material_lines else None,
        "questions_lines": list(u.questions_lines) if u.questions_lines else None,
        "material_line_text": mat_line,
        "occurrences": occ,
    })
    print(f"\n--- {u.unit_id} ---")
    print(f"  question_numbers    : {list(u.question_numbers)}")
    print(f"  printed_number      : {u.printed_number}  "
          f"(provenance={u.printed_provenance})")
    print(f"  material_lines      : {u.material_lines}")
    print(f"  questions_lines     : {u.questions_lines}")
    print(f"  material line text  : {mat_line[:100] if mat_line else None!r}")
    ls = [o for o in occ if o[0] == "line_start"]
    il = [o for o in occ if o[0] == "in_line"]
    print(f"  line-start hits     : {[(o[1]) for o in ls]}")
    print(f"  in-line hits        : {[(o[1]) for o in il]}")
    for kind, n, t in il[:3]:
        print(f"      L{n}: {t[:105]!r}")
    if ls:
        cls = "PARSED (should not be not-found -> investigate)"
    elif il:
        cls = "SOURCE IDENTITY PRESENT, mid-line only -> unparsed"
    else:
        cls = "GENUINELY ABSENT from source"
    print(f"  CLASSIFICATION      : {cls}")
    rows[-1]["classification"] = cls

print("\n" + "=" * 100)
print("U51-55 local vs global (Producer authority check)")
print("=" * 100)
for u in m.units:
    if str(u.question_numbers[0]) in {"51", "52", "53", "54", "55"}:
        pn = u.printed_number
        print(f"  {u.unit_id:<10} question_numbers={list(u.question_numbers)} "
              f"printed_number={pn} provenance={u.printed_provenance} "
              f"material_lines={u.material_lines}")
        lo = u.material_lines[0] if u.material_lines else None
        if lo:
            print(f"      L{lo}: {texts[lo-1].strip()[:95]!r}")

(OUT / "evidence_table_not_found.json").write_text(
    json.dumps({"rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwritten: {OUT / 'evidence_table_not_found.json'}")
