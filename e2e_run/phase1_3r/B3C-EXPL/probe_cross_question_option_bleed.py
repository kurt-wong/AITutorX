"""Read-only: how widespread is the cross-question option-label bleed?

Root cause hypothesis (Papers reslice_pipeline.py:84-87):
  _detect_option_labels keeps the FIRST occurrence of each label, deduped across
  the whole scan range, with NO per-question boundary. When question 1's D marker
  is missed (e.g. 'D，' full-width comma not in the separator class) the next
  question's D is collected instead -> option declared at a foreign question's line.

Measure, corpus-wide:
  - units whose declared option line lies outside the unit's own question body
  - units where a declared option line is at/after the next question start
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
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
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

suspicious = []
totals = {"units_with_options": 0, "units_with_multi_qn": 0,
          "units_with_foreign_option_line": 0, "units_whose_own_first_qn_line_missing_label": 0}

for p in find_manifests(CORPUS):
    m = load_manifest(p)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    paper = p.parent.name
    # all question-start lines for the unit's declared numbers
    for u in m.units:
        if not u.options:
            continue
        totals["units_with_options"] += 1
        qns = [str(n) for n in (u.question_numbers or [])]
        if len(qns) > 1:
            totals["units_with_multi_qn"] += 1
        # find the start lines of the 2nd..nth question numbers (declared)
        later_starts = {}
        for q in qns[1:]:
            hits = [s.line_no_in_page for s in srs
                    if is_question_start(normalize_text(s.text)) == q]
            if hits:
                later_starts[q] = min(hits)
        first_later = min(later_starts.values()) if later_starts else None
        if first_later is None:
            continue
        foreign = [o for o in u.options if o.start_line >= first_later]
        if foreign:
            totals["units_with_foreign_option_line"] += 1
            suspicious.append({
                "paper": paper, "unit": u.unit_id, "qn": qns,
                "first_later_qn_start_line": first_later,
                "foreign_options": [{"label": o.label, "line": o.start_line,
                                     "text": texts[o.start_line - 1].strip()[:70]}
                                    for o in foreign],
            })

print(json.dumps(totals, ensure_ascii=False, indent=2))
print(f"\n=== units whose declared option line falls at/after the NEXT question's start ===")
for s in suspicious:
    print(f"\n{s['paper']} / {s['unit']} qn={s['qn']} next-qn starts L{s['first_later_qn_start_line']}")
    for f in s["foreign_options"]:
        print(f"   {f['label']} @L{f['line']}: {f['text']!r}")

(OUT / "cross_question_option_bleed.json").write_text(
    json.dumps({"totals": totals, "suspicious": suspicious},
               ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwritten: {OUT / 'cross_question_option_bleed.json'}")
