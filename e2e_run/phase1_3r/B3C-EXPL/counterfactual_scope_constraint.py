"""Read-only counterfactual for the AUTHORIZED plan A:
  start anchor >= previous unit's material end
  end   anchor <= next unit's material start

Applies that scope constraint in-process (no repo change) and reports, per
English unit:
  - current anchors vs constrained anchors
  - resulting interior span
  - whether the declared material_lines range is FULLY covered
  - residual pairwise overlap between adjacent materials

Purpose: detect silent truncation (overlap removed but declared lines dropped).
"""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ENG = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\英语")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    _text_occurrence_count,
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
views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                             page_no=s.page_no, line_no_in_page=s.line_no_in_page)
              for s in srs)
rz = SourceResolver(source_version_id=uuid.uuid4(), lines=views)


def walk_unique(start_no, *, forward, limit, lo_bound, hi_bound):
    """_nearest_unique_nonempty with an added [lo_bound, hi_bound] scope cap."""
    n = len(texts)
    step = 1 if forward else -1
    no = start_no
    for _ in range(limit):
        if no < 1 or no > n:
            return None
        if lo_bound is not None and no < lo_bound:
            return None
        if hi_bound is not None and no > hi_bound:
            return None
        t = texts[no - 1]
        if t and t.strip() and _text_occurrence_count(texts, t) == 1:
            return no, t
        no += step
    return None


# adjacency map: unit_id -> (start,end), in document order
mats = [(u.unit_id, tuple(u.material_lines)) for u in m.units if u.material_lines]
order = sorted(mats, key=lambda kv: kv[1][0])
prev_end = {}
next_start = {}
for i, (uid, (s, e)) in enumerate(order):
    prev_end[uid] = order[i - 1][1][1] if i > 0 else None
    next_start[uid] = order[i + 1][1][0] if i < len(order) - 1 else None


def anchors_for(uid, scope):
    s, e = dict(mats)[uid]
    if s == e:
        mk = material_boundary_markers([s, e], texts)
        return mk, None, None
    pe = prev_end[uid] if scope else None
    ns = next_start[uid] if scope else None
    # start: walk backwards from s-1, but not before previous material end
    st = walk_unique(s - 1, forward=False, limit=8,
                     lo_bound=pe, hi_bound=None)
    en = walk_unique(e + 1, forward=True, limit=8,
                     lo_bound=None, hi_bound=ns)
    if not st or not en or en[0] <= st[0] + 1:
        # fall back to unconstrained to see what the repo would do
        mk = material_boundary_markers([s, e], texts)
        return mk, st, en
    return ({"role": "material",
             "start_marker": {"granularity": "multi_line_pair", "text": st[1]},
             "end_marker": {"text": en[1]}}, st, en)


def to_span(mk):
    if not mk:
        return None
    sm = mk.get("start_marker") or {}
    em = mk.get("end_marker") or {}
    if not sm.get("text"):
        return None
    if sm.get("granularity") == "multi_line_pair":
        st, sr, _ = rz._resolve_marker_cascade(sm["text"])
        et, er, _ = rz._resolve_marker_cascade(em.get("text"))
        if not sr or not er:
            return None
        s_seq = rz._idx.seq_of(sr[0]); e_seq = rz._idx.seq_of(er[0])
        return [l.line_no_in_page for l in rz._idx.between(s_seq + 1, e_seq)]
    _, sr, _ = rz._resolve_marker_cascade(sm["text"])
    if not sr:
        return None
    return [int(sr[0][3:])]


print(f"{'unit':<9}{'declared':<12}{'CUR span':<14}{'SCOPED span':<14}"
      f"{'covers decl?':<13}{'lost lines'}")
cur_sets, sc_sets = {}, {}
for uid, (s, e) in order:
    cur = to_span(material_boundary_markers([s, e], texts))
    mk2, st2, en2 = anchors_for(uid, True)
    sc = to_span(mk2)
    cur_sets[uid] = set(cur or [])
    sc_sets[uid] = set(sc or [])
    cov = "n/a" if sc is None else str(set(range(s, e + 1)) <= set(sc))
    lost = [] if sc is None else sorted(set(range(s, e + 1)) - set(sc))
    print(f"{uid:<9}{str((s,e)):<12}{str((min(cur),max(cur)) if cur else None):<14}"
          f"{str((min(sc),max(sc)) if sc else None):<14}{cov:<13}{lost}")

print("\n=== residual overlap after scope constraint ===")
ids = [uid for uid, _ in order]
tot = 0
for i in range(len(ids) - 1):
    a, b = ids[i], ids[i + 1]
    inter = sc_sets[a] & sc_sets[b]
    if inter:
        tot += len(inter)
        print(f"  {a} ∩ {b} = {sorted(inter)}")
print(f"  adjacent overlapping pairs/total intersecting lines = {tot}")

print("\n=== units whose declared range is NOT fully covered after constraint ===")
for uid, (s, e) in order:
    sc = sc_sets[uid]
    if sc and not set(range(s, e + 1)) <= sc:
        print(f"  {uid}: declared {s}..{e} -> scoped {min(sc)}..{max(sc)} "
              f"lost {sorted(set(range(s,e+1)) - sc)}")
