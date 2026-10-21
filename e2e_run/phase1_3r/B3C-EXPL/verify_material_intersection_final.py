"""Read-only tie-break: print the FINAL resolved material spans for English and
check (a) whether any two share a line, (b) whether the adjacency pairs MIMO/DSH
disagree about actually intersect, (c) whether _enforce_material_overlap should
have fired but did not.
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
run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

spans = {}
for s in run.resolved_spans:
    if s.role == "material":
        spans[s.span_id[3:].rsplit(".material", 1)[0]] = [int(r[3:]) for r in s.line_refs]

print("=== FINAL resolved material spans (English) ===")
order = sorted(spans.items(), key=lambda kv: min(kv[1]))
for uid, nos in order:
    print(f"  {uid:<8} {min(nos)}..{max(nos)}  n={len(nos)}  "
          f"lines={nos if len(nos) <= 12 else str(nos[:6]) + '...'}")

print("\n=== ALL pairwise material intersections ===")
ids = [uid for uid, _ in order]
found = 0
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        inter = set(spans[ids[i]]) & set(spans[ids[j]])
        if inter:
            found += 1
            print(f"  {ids[i]} ∩ {ids[j]} = {sorted(inter)}")
print(f"  total intersecting pairs = {found}")

print("\n=== would _enforce_material_overlap have demoted? ===")
print("  unresolved material refs:",
      [u.reference_id for u in run.unresolved_references if u.role == "material"])
print("  (empty list above + non-empty intersections => enforcement did NOT fire)")

# recompute what markers produced these spans
print("\n=== markers that produced each span ===")
for u in payload["semantic_units"]:
    uid = u["unit_id"]
    if uid not in spans:
        continue
    mat = (u.get("shared_components") or {}).get("material") or {}
    sm = mat.get("start_marker") or {}
    em = mat.get("end_marker") or {}
    print(f"  {uid:<8} gran={sm.get('granularity')!s:<16} "
          f"start={{(sm.get('text') or '')[:34]!r}} end={(em.get('text') or '')[:34]!r}")
