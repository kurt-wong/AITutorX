"""Read-only: resolve the last two 'missing' mechanisms for 地理.

  q26  : is it truly absent from source, or present in an unrecognized form?
  q51-55: manifest declares question_numbers 51..55 but the 非选择题 section
          restarts numbering at 1..5 -- verify from raw source.
"""
from __future__ import annotations

import re
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

print("=== raw lines 218-240 (around declared material for U26-29) ===")
for n in range(218, 241):
    s = by_no.get(n)
    if s:
        print(f"  L{n}: {s.text[:130]!r}")

print("\n=== raw lines 450-475 (第二部分 start / first non-choice item) ===")
for n in range(450, 476):
    s = by_no.get(n)
    if s:
        print(f"  L{n}: {s.text[:130]!r}")

print("\n=== all lines containing '第二部分' or '非选择题' ===")
for s in srs:
    if "第二部分" in s.text or "非选择题" in s.text:
        print(f"  L{s.line_no_in_page}: {s.text.strip()[:120]!r}")

print("\n=== declared units U26-29 and U-P2-1..5 question_numbers ===")
for u in m.units:
    if u.unit_id in ("U26-29", "U-P2-1", "U-P2-2", "U-P2-3", "U-P2-4", "U-P2-5"):
        print(f"  {u.unit_id:<10} qn={u.question_numbers} "
              f"material_lines={u.material_lines} questions_lines={u.questions_lines} "
              f"printed_number={u.printed_number} section={u.section!r}")

print("\n=== every line whose stripped text starts with a digit (any separator) ===")
pat = re.compile(r"^(\d{1,3})\s*\\?\s*([.．、:]|\s|$)")
for s in srs:
    t = s.text.strip()
    mm = pat.match(t)
    if mm:
        print(f"  L{s.line_no_in_page:<4} qn={mm.group(1):<3} {t[:95]!r}")

print("\n=== '26' anywhere in source ===")
for s in srs:
    if re.search(r"(?<![\d])26(?![\d])", s.text):
        print(f"  L{s.line_no_in_page}: {s.text.strip()[:120]!r}")
