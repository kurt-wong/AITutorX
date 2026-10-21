"""Read-only: two checks on MIMO's report claims.

1. Does "material marker text missing" really apply to 地理 composite units?
   (My full-pipeline run reports 0.)
2. Are the 12 unresolved-option 地理 units exactly the 12 with stem failure?
   And are any declared options fabricated (labels not actually on the cited line)?
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter
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

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

LABEL = re.compile(r"(?<![\w])([A-Ha-h])\s*[.．、:)）]")


def main() -> None:
    m = load_manifest(MAN)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                 page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                  for s in srs)

    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

    print("=== claim 1: material marker text missing ===")
    mat_unres = [(u.resolution_status, " / ".join(u.evidence))
                 for u in run.unresolved_references if u.role == "material"]
    print(f"material unresolved refs : {len(mat_unres)}  {mat_unres[:3]}")
    mat_spans = [s for s in run.resolved_spans if s.role == "material"]
    print(f"material resolved spans  : {len(mat_spans)}")
    print("shared_component material resolved in payload units: "
          f"{sum(1 for u in payload['semantic_units'] for k, v in (u.get('shared_components') or {}).items() if k == 'material' and (v.get('start_marker') or {}).get('text'))}/25")

    print("\n=== claim 2: stem-resolved units vs option-resolved units ===")
    resolved_stem_units = {s.span_id[3:-5] for s in run.resolved_spans
                           if s.role == "stem" and s.span_id.endswith(".stem")}
    opt_by_unit = Counter()
    for s in run.resolved_spans:
        if s.role == "option":
            opt_by_unit[s.span_id.split(".option.")[0]] += 1
    print(f"units with a resolved stem   : {len(resolved_stem_units)}")
    print(f"units with 4 option spans    : "
          f"{sum(1 for k, v in opt_by_unit.items() if v == 4)}")
    print(f"stem-resolved set == option-4 set ? "
          f"{resolved_stem_units == {k for k, v in opt_by_unit.items() if v == 4}}")
    print(f"  stem units   : {sorted(resolved_stem_units)}")
    print(f"  option4 units: {sorted(k for k, v in opt_by_unit.items() if v == 4)}")

    print("\n=== claim 3: are declared options source-grounded? ===")
    bad = []
    for u in m.units:
        for o in u.options or []:
            s = texts[o.start_line - 1] if 1 <= o.start_line <= len(texts) else ""
            labs = {mm.group(1).upper() for mm in LABEL.finditer(s)}
            if o.label.upper() not in labs:
                bad.append((u.unit_id, o.label, o.start_line, s[:70]))
    print(f"declared options: {sum(len(u.options or []) for u in m.units)}")
    print(f"options whose label is NOT on the cited line: {len(bad)}")
    for b in bad[:10]:
        print(f"   {b[0]} {b[1]} L{b[2]} {b[3]!r}")

    print("\n=== claim 4: options confined to first question number? ===")
    for u in m.units[:6]:
        if not u.options:
            continue
        lines = sorted({o.start_line for o in u.options})
        print(f"   {u.unit_id:<10} qn={list(u.question_numbers)} option_lines={lines} "
              f"questions_lines={u.questions_lines}")


if __name__ == "__main__":
    main()
