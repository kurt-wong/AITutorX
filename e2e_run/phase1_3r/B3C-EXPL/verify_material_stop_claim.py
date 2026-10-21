"""Independent verification of MIMO's English material STOP claim.

Checks, read-only:
  1. Where does material_boundary_markers actually live? (repo boundary claim)
  2. Uniqueness counts MIMO asserts (L491/L495/L504/L506).
  3. Derived start/end anchors + interior for the 8 demoted units.
  4. Counterfactual: does narrowing / widening material_lines change the anchors?
     (MIMO claims the walk lands on the same unique pair regardless)
"""
from __future__ import annotations

import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ENG = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\英语")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
    material_boundary_markers,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

p = [x for x in ENG.glob("*.manifest.json")][0]
m = load_manifest(p)
srs = load_source_lines(Path(m.source_file))
texts = [s.text for s in srs]
by_no = {s.line_no_in_page: s for s in srs}
idx = {s.line_ref: s.line_no_in_page for s in srs}

print("=== 1. module location of material_boundary_markers ===")
import scripts.preprocessing_consumer.annotation_adapter as aa  # noqa: E402
print("  ", aa.__file__)
print("   repo =", "AITutors-v3" if "AITutors-v3" in aa.__file__ else "?")

print("\n=== 2. uniqueness counts MIMO asserts ===")
for n in (491, 495, 502, 504, 506, 509, 518):
    txt = texts[n - 1]
    cnt = sum(1 for x in texts if x == txt)
    print(f"  L{n:<4} count={cnt:<4} {txt[:72]!r}")

print("\n=== 3. per-unit marker anchors + interior ===")
units = ["Q1", "Q2", "Q3", "Q4", "Q5-6", "Q7-8", "Q15-17", "Q18-20"]
mk_by_unit = {}
for u in m.units:
    if u.unit_id not in units or not u.material_lines:
        continue
    mk = material_boundary_markers(u.material_lines, texts)
    mk_by_unit[u.unit_id] = (u.material_lines, mk)

# resolve each anchor text to its line number (resolver uses _locate)
views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                             page_no=s.page_no, line_no_in_page=s.line_no_in_page)
              for s in srs)
rz = SourceResolver(source_version_id=uuid.uuid4(), lines=views)
for uid in units:
    ml, mk = mk_by_unit.get(uid, (None, None))
    if not mk:
        print(f"  {uid:<8} ml={ml} marker=NONE")
        continue
    sm = mk.get("start_marker") or {}
    em = mk.get("end_marker") or {}
    sq, eq = sm.get("text"), em.get("text")
    st, sr, _ = rz._resolve_marker_cascade(sq)
    et, er, _ = rz._resolve_marker_cascade(eq) if eq else ("n/a", [], ())
    s_line = idx.get(sr[0]) if sr else None
    e_line = idx.get(er[0]) if er else None
    interior = None
    if s_line and e_line and e_line > s_line:
        interior = (s_line + 1, e_line - 1)
    print(f"  {uid:<8} ml={tuple(ml)}")
    print(f"      start {st:<6} L{s_line} :: {(sq or '')[:58]!r}")
    if eq:
        print(f"      end   {et:<6} L{e_line} :: {(eq or '')[:58]!r}   interior={interior}")

print("\n=== 4. counterfactual: does changing material_lines move the anchors? ===")
for uid in ("Q1", "Q2"):
    ml, _ = mk_by_unit.get(uid, (None, None))
    if not ml:
        continue
    s, e = ml
    print(f"  {uid} original ml=({s},{e})")
    for ds, de in [(s, e), (s + 2, e - 1), (s - 2, e + 2), (s, s), (s + 1, e)]:
        if ds < 1 or de > len(texts) or ds > de:
            continue
        mk2 = material_boundary_markers([ds, de], texts)
        if not mk2:
            print(f"      ml=({ds},{de}) -> marker NONE")
            continue
        sm2 = (mk2.get("start_marker") or {}).get("text")
        em2 = (mk2.get("end_marker") or {}).get("text")
        _, r2, _ = rz._resolve_marker_cascade(sm2)
        s2 = idx.get(r2[0]) if r2 else None
        e2 = None
        if em2:
            _, r3, _ = rz._resolve_marker_cascade(em2)
            e2 = idx.get(r3[0]) if r3 else None
        print(f"      ml=({ds},{de}) -> start L{s2}, end L{e2}")
