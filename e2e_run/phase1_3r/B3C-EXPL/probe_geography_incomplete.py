"""Read-only probe: WHY are all 25 地理 units `incomplete`?

Preparation for the Owner-directed investigation. Makes no assumptions:
- prints the resolver's actual unresolved references (role + status + evidence)
  for 地理, grouped by reason, so the true blocking cause is observable.
- also prints, per unit, which content roles failed to resolve.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter, defaultdict
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
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        svid = uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, uuid.uuid4())

        print(f"=== {TARGET}: {p.name}")
        print(f"resolved_spans by role: "
              f"{dict(Counter(s.role for s in run.resolved_spans))}")
        print(f"unresolved_references by status: "
              f"{dict(Counter(u.resolution_status for u in run.unresolved_references))}")
        print(f"unresolved_relations: resolved="
              f"{sum(1 for r in run.resolved_relations if r.status == 'resolved')} "
              f"total={len(run.resolved_relations)}")

        print("\n-- unresolved references (role | status | evidence) --")
        by_reason = Counter()
        for u in run.unresolved_references:
            ev = " / ".join(u.evidence)
            by_reason[(u.role, u.resolution_status, ev)] += 1
        for (role, status, ev), n in by_reason.most_common():
            print(f"  {n:>4}  {role:<20} {status:<12} {ev[:90]}")

        print("\n-- IR per-unit status --")
        st = Counter(u.semantic_status for u in ir.units)
        print(f"  {dict(st)}")
        for u in ir.units:
            print(f"  {u.unit_id:<10} {u.semantic_status:<11} "
                  f"content={[(c.role, c.span_id, c.unsupported) for c in u.content]}")

        # L601 context
        for s in srs:
            if s.line_no_in_page == 601 or s.seq == 601:
                print(f"\n  source L601: {s.text[:220]!r}")
                break

        out = {
            "paper": TARGET,
            "resolved_by_role": dict(Counter(s.role for s in run.resolved_spans)),
            "unresolved_by_status": dict(
                Counter(u.resolution_status for u in run.unresolved_references)),
            "unresolved_reasons": [
                {"role": r, "status": s, "evidence": e, "count": n}
                for (r, s, e), n in by_reason.most_common()
            ],
            "ir_status": dict(st),
            "units": [
                {"unit_id": u.unit_id, "status": u.semantic_status,
                 "content": [{"role": c.role, "span_id": c.span_id,
                              "unsupported": c.unsupported} for c in u.content]}
                for u in ir.units
            ],
        }
        (OUT / "geography_incomplete_probe.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_incomplete_probe.json'}")


if __name__ == "__main__":
    main()
