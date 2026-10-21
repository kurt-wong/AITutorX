"""Read-only: what EXACTLY do the resolved material spans cover, and on which
lines do they intersect?

MIMO's table lists marker anchors; here I print the final ResolvedSpan interior
(what _enforce_material_overlap actually compares), so the reported overlap is
proven or refuted rather than inferred from anchors.
"""
from __future__ import annotations

import os
import sys
import uuid
from collections import Counter
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
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
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
payload = manifest_to_annotation_payload(m)
payload = attach_material_boundary_markers(
    payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)

# --- stage 1: markers BEFORE overlap enforcement ---
run_pre = SourceResolver(source_version_id=uuid.uuid4(), lines=views)
# capture spans before demotion by re-running the material resolution only
out_spans = {}
for u in payload["semantic_units"]:
    mat = (u.get("shared_components") or {}).get("material") or {}
    if not (mat.get("start_marker") or {}).get("text"):
        continue
    sm = mat["start_marker"]; em = mat.get("end_marker") or {}
    st, sr, _ = run_pre._resolve_marker_cascade(sm["text"])
    if not sr:
        continue
    if sm.get("granularity") == "multi_line_pair":
        et, er, _ = run_pre._resolve_marker_cascade(em["text"])
        if not er:
            continue
        s_seq = run_pre._idx.seq_of(sr[0]); e_seq = run_pre._idx.seq_of(er[0])
        refs = [l.line_ref for l in run_pre._idx.between(s_seq + 1, e_seq)]
    else:
        refs = [sr[0]]
    out_spans[u["unit_id"]] = refs

print("=== pre-demotion material line sets (from markers) ===")
items = sorted(out_spans.items(), key=lambda kv: int(kv[1][0][3:]) if kv[1] else 0)
for uid, refs in items:
    if not refs:
        continue
    nos = [int(r[3:]) for r in refs]
    print(f"  {uid:<8} {mins(nos) if False else min(nos)}..{max(nos)}  n={len(refs)}")

def mins(x):
    return min(x)

print("\n=== pairwise intersections between adjacent ENGLISH material sets ===")
ids = [uid for uid, _ in items if out_spans[uid]]
sets = {uid: set(out_spans[uid]) for uid in ids}
for i in range(len(ids) - 1):
    a, b = ids[i], ids[i + 1]
    inter = sets[a] & sets[b]
    if inter:
        print(f"  {a} ∩ {b} = {sorted(inter)}")

print("\n=== full run: resolved vs unresolved material ===")
run = run_pre.resolve(payload)
print("  resolved material spans:", [s.span_id for s in run.resolved_spans if s.role == "material"])
print("  unresolved material refs:",
      [u.reference_id for u in run.unresolved_references if u.role == "material"])
