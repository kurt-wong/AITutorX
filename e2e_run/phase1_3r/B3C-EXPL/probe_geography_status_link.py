"""Read-only: establish causal link between stem resolution and unit semantic_status,
and split geography production loss by section (choice vs non-choice).
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")
TARGET = "地理"

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    for p in find_manifests(CORPUS):
        if p.parent.name != TARGET:
            continue
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid = uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, uuid.uuid4())

        # unit_id -> resolved stem present?
        stem_units = {s.evidence[0].split("=")[-1] if s.evidence else "?"
                      for s in run.resolved_spans if s.role == "stem"}
        # resolver target ids encode unit: sp-<unit>.stem
        resolved_stem_units = set()
        for s in run.resolved_spans:
            if s.role == "stem":
                # span_id shape: sp-<unit_id>.stem
                sid = s.span_id
                if sid.startswith("sp-") and sid.endswith(".stem"):
                    resolved_stem_units.add(sid[3:-5])

        print("units with a resolved stem:", len(resolved_stem_units))
        print("resolved:", sorted(resolved_stem_units))

        sec = {}
        for u in m.units:
            sec[u.unit_id] = u.section

        print("\n-- per unit: stem resolved? IR status --")
        tally = Counter()
        for u in ir.units:
            has_stem = u.unit_id in resolved_stem_units
            key = (has_stem, u.semantic_status, "非选择" in (sec.get(u.unit_id) or ""))
            tally[key] += 1
        for (has_stem, status, is_p2), n in sorted(tally.items()):
            print(f"   stem_resolved={str(has_stem):<5} status={status:<11} "
                  f"part2={str(is_p2):<5} -> {n}")

        print("\n-- full per-unit table --")
        for u in ir.units:
            has_stem = u.unit_id in resolved_stem_units
            print(f"   {u.unit_id:<10} stem={'Y' if has_stem else 'N'} "
                  f"status={u.semantic_status:<11} section={(sec.get(u.unit_id) or '')[:22]!r}")

        out = {
            "units_with_resolved_stem": sorted(resolved_stem_units),
            "tally": {f"stem={k[0]}|status={k[1]}|part2={k[2]}": v
                      for k, v in tally.items()},
            "units": [{"unit_id": u.unit_id,
                       "stem_resolved": u.unit_id in resolved_stem_units,
                       "status": u.semantic_status,
                       "section": sec.get(u.unit_id)} for u in ir.units],
        }
        (OUT / "geography_status_link.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_status_link.json'}")


if __name__ == "__main__":
    main()
