"""Read-only: why do the 5 escaped-dot units still get 0 option spans even after
escaped-dot recognition is fixed?

For each target unit, reproduce the resolver's own inputs and show:
  start_ref (stem line), region_upper, material span, and what
  _locate_options would find for each label.
"""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
MAN = ROOT / "地理" / "2018北京春季高中会考地理（教师版）(1).manifest.json"

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import app.domains.resolver.match_normalization as mn  # noqa: E402
import app.domains.resolver.resolver as rz  # noqa: E402
from app.domains.resolver.match_normalization import (  # noqa: E402
    normalize_text,
    option_tokens,
)
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

TARGETS = {"21", "24", "40", "42", "44"}

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
texts = [s.text for s in srs]
views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                             page_no=s.page_no, line_no_in_page=s.line_no_in_page)
              for s in srs)
payload = manifest_to_annotation_payload(m)
payload = attach_material_boundary_markers(
    payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)

# patch escaped-dot recognition in-process (same as the counterfactual)
_patched_entry = __import__("re").compile(r"(?<![\d])(\d{1,3})\s*\\?[.．、:]")
_patched_qs = __import__("re").compile(r"^(\d{1,3})\s*(\\?[.．、:]|\s|$)")


def patched_is_question_start(nl):
    mm = _patched_qs.match(nl)
    return mm.group(1) if mm else None


rz._ENTRY_RE = _patched_entry
rz.is_question_start = patched_is_question_start

resolver = rz.SourceResolver(source_version_id=uuid.uuid4(), lines=views)
run = resolver.resolve(payload)

idx = resolver._idx
qzone = resolver._question_zone()
qzone_refs = {l.line_ref for l in qzone}

print("=== label recognisability on the declared option lines ===")
for u in m.units:
    q0 = str(u.question_numbers[0]) if u.question_numbers else None
    if q0 not in TARGETS or not u.options:
        continue
    print(f"\n--- {u.unit_id} qn={list(u.question_numbers)} ---")
    qn = q0
    hits = [l for l in qzone if patched_is_question_start(normalize_text(l.text)) == qn]
    print(f"  question-zone hits for qn={qn}: "
          f"{[(l.line_no_in_page, l.text.strip()[:50]) for l in hits]}")
    start_ref = hits[0].line_ref if len(hits) == 1 else None
    print(f"  start_ref = {start_ref}")
    if not start_ref:
        print("  -> stem unresolved => _locate_options never runs (causal)")
        continue
    upper = resolver._region_end(start_ref)
    print(f"  _region_end(start_ref) = {upper}")
    start_seq = idx.seq_of(start_ref)
    labels = [o.label for o in u.options]
    print(f"  declared labels={labels}")
    for lab in labels:
        starts = [l for l in idx.lines
                  if l.seq > start_seq and (upper is None or l.seq < upper)
                  and lab in option_tokens(normalize_text(l.text), (lab,))]
        print(f"     label {lab}: candidate lines in window = "
              f"{[(l.line_no_in_page, l.text.strip()[:55]) for l in starts]}")
    # show the declared option lines vs the window
    for o in u.options:
        n = o.start_line
        t = texts[n - 1]
        print(f"     declared L{n} seq={idx.seq_of(f'P1L{n:03d}')} "
              f"tokens={option_tokens(normalize_text(t), tuple(labels))} :: {t.strip()[:55]!r}")
