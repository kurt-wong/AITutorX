"""Read-only: after dc051fa, does the resolved material span still cover the
Producer's declared material_lines range?

The fix's documented fallback "loses at most the non-unique edge lines of the
block". This quantifies that loss per unit and corpus-wide, and reports which
declared lines are dropped.
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
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    rows = []
    for p in find_manifests(CORPUS):
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
        span_by_unit = {}
        for s in run.resolved_spans:
            if s.role == "material":
                span_by_unit[s.span_id[3:].rsplit(".material", 1)[0]] = [
                    int(r[3:]) for r in s.line_refs]

        for mu in m.units:
            if not mu.material_lines:
                continue
            s, e = mu.material_lines
            declared = set(range(s, e + 1))
            got = set(span_by_unit.get(mu.unit_id, []))
            lost = sorted(declared - got)
            extra = sorted(got - declared)
            rows.append({
                "paper": p.parent.name, "unit": mu.unit_id,
                "declared": [s, e], "declared_n": len(declared),
                "derived": [min(got), max(got)] if got else None,
                "derived_n": len(got),
                "covers_declared": declared <= got if got else False,
                "lost_lines": lost, "extra_lines": extra,
            })

    print(f"{'paper':<6}{'unit':<10}{'declared':<13}{'derived':<13}{'cover?':<8}"
          f"{'nLost':<6}lost")
    for r in rows:
        print(f"{r['paper']:<6}{r['unit']:<10}{str(r['declared']):<13}"
              f"{str(r['derived']):<13}{str(r['covers_declared']):<8}"
              f"{r['declared_n'] - r['derived_n']:<6}{r['lost_lines'][:8]}")

    tot = Counter()
    tot["units"] = len(rows)
    tot["not_covering"] = sum(1 for r in rows if not r["covers_declared"])
    tot["lost_lines_total"] = sum(len(r["lost_lines"]) for r in rows)
    tot["extra_lines_total"] = sum(len(r["extra_lines"]) for r in rows)
    print("\nTOTALS:", json.dumps(dict(tot), ensure_ascii=False))
    print("\n=== units NOT covering their declared range ===")
    for r in rows:
        if not r["covers_declared"]:
            print(f"  {r['paper']}/{r['unit']} declared={r['declared']} "
                  f"derived={r['derived']} lost={r['lost_lines']} extra={r['extra_lines']}")

    (OUT / "material_declared_coverage.json").write_text(
        json.dumps({"rows": rows, "totals": dict(tot)}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'material_declared_coverage.json'}")


if __name__ == "__main__":
    main()
