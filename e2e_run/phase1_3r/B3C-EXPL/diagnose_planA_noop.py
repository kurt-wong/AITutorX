"""Read-only: why plan A is a no-op on English, and what would actually work.

(a) For each English unit, show the scoped walk's bound check -> None -> fallback.
(b) Counterfactual: if material span were the DECLARED range itself (no marker
    walk), is overlap eliminated and are declared lines fully covered?
    (This is the option the task forbids modifying -- measured only, not proposed.)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ENG = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\英语")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    _text_occurrence_count,
    material_boundary_markers,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

p = [x for x in ENG.glob("*.manifest.json")][0]
m = load_manifest(p)
srs = load_source_lines(Path(m.source_file))
texts = [s.text for s in srs]

mats = [(u.unit_id, tuple(u.material_lines)) for u in m.units if u.material_lines]
order = sorted(mats, key=lambda kv: kv[1][0])
prev_end, next_start = {}, {}
for i, (uid, (s, e)) in enumerate(order):
    prev_end[uid] = order[i - 1][1][1] if i > 0 else None
    next_start[uid] = order[i + 1][1][0] if i < len(order) - 1 else None


def walk(start_no, *, forward, limit, lo=None, hi=None, trace=False):
    n = len(texts)
    step = 1 if forward else -1
    no = start_no
    for _ in range(limit):
        if no < 1 or no > n:
            if trace: print(f"        out of range at {no}")
            return None
        if lo is not None and no < lo:
            if trace: print(f"        hit lo bound {lo} at {no} -> None")
            return None
        if hi is not None and no > hi:
            if trace: print(f"        hit hi bound {hi} at {no} -> None")
            return None
        t = texts[no - 1]
        uniq = bool(t and t.strip()) and _text_occurrence_count(texts, t) == 1
        if trace:
            print(f"        L{no} uniq={uniq} {t[:44]!r}")
        if uniq:
            return no
        no += step
    return None


print("=== (a) why plan A falls back: the bound is hit immediately ===")
for uid in ("Q1", "Q2", "Q3"):
    s, e = dict(mats)[uid]
    pe, ns = prev_end[uid], next_start[uid]
    print(f"\n{uid} declared=({s},{e}) prev_end={pe} next_start={ns}")
    print(f"   end walk from e+1={e+1} with hi<=next_start={ns}:")
    r = walk(e + 1, forward=True, limit=8, hi=ns, trace=True)
    print(f"   -> {'L' + str(r) if r else 'None  => FALLBACK to unconstrained'}")
    print(f"   start walk from s-1={s-1} with lo>=prev_end={pe}:")
    r2 = walk(s - 1, forward=False, limit=8, lo=pe, trace=False)
    print(f"   -> {'L' + str(r2) if r2 else 'None'}")

print("\n=== (b) counterfactual: span = DECLARED range (no marker walk) ===")
declared_sets = {uid: set(range(s, e + 1)) for uid, (s, e) in order}
ids = [uid for uid, _ in order]
tot = 0
for i in range(len(ids) - 1):
    a, b = ids[i], ids[i + 1]
    inter = declared_sets[a] & declared_sets[b]
    if inter:
        tot += len(inter)
        print(f"  OVERLAP {a} ∩ {b} = {sorted(inter)}")
print(f"  adjacent overlaps = {tot}")
print(f"  units fully covering their own declared range = "
      f"{sum(1 for u, (s, e) in order if set(range(s, e+1)) <= declared_sets[u])}/{len(order)}")

print("\n=== (c) gaps between adjacent declared ranges (room for a delimiter?) ===")
for i in range(len(ids) - 1):
    a, b = ids[i], ids[i + 1]
    ae = dict(mats)[a][1]
    bs = dict(mats)[b][0]
    gap = bs - ae - 1
    beltxt = [f"L{n}:{texts[n-1].strip()[:0] or '<blank>'}" for n in range(ae + 1, bs)]
    print(f"  {a}({dict(mats)[a][0]},{ae}) -> {b}({bs},{dict(mats)[b][1]})  "
          f"between-lines={bs-ae-1} {beltxt if gap >= 0 and gap < 4 else ''}")
