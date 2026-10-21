"""READ-ONLY: is the 260-option defect caused by the VIEWER's slicing, or by the
RESOLVER's option-span semantics?

Replay the pipeline directly (no viewer involved) and compare, for known
single-line multi-option questions (数学 Q1/Q2/Q7, 化学 Q7), the raw resolved
option texts.

Decision rule:
  if the direct replay ALSO yields bare 'B'/'C'/'D' -> defect is upstream (V3 Resolver)
  if the direct replay yields correct per-option text  -> defect would be viewer-side
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers, manifest_to_annotation_payload)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

WATCH = {"数学": {"Q1", "Q2", "Q7"}, "化学": {"Q7"}}


def main() -> None:
    for subj, uids in WATCH.items():
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        md_p = next((EA / "02_PREPROCESSING_OUTPUT").glob(f"*{subj}*.md"))
        m = load_manifest(man_p)
        srs = load_source_lines(md_p)
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)

        print("=" * 90)
        print(f"{subj}   md={md_p.name}")
        for uid in sorted(uids):
            leaf = next((l for l in compiled.leaves if l.unit_id == uid), None)
            if leaf is None:
                print(f"   {uid}: NO LEAF")
                continue
            print(f"\n   {uid}  (manifest-declared options / resolved spans)")
            for o in leaf.options:
                print(f"      {o.label}: gran={getattr(o,'granularity',None)} "
                      f"lines={getattr(o,'line_refs',None)} text={o.text.strip()[:64]!r}")

        # also show the manifest declaration for the same units
        print(f"\n   --- manifest declarations ---")
        for u in m.units:
            if u.unit_id in uids:
                print(f"      {u.unit_id}: options_lines={u.options_lines} "
                      f"options={[(o.label, o.start_line, o.end_line) for o in u.options]}")


if __name__ == "__main__":
    main()
