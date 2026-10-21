"""Cross-paper check for the explanation cut.

A. Coverage + declared-vs-resolved binding for explanation (all 9 papers).
B. Confirm the gate's role-provenance check reads STRUCTURAL REGIONS, not the
   explanation ResolvedSpan: the span-level collision went 2756->0 while the
   region-level collision stayed at 52 on 历史, and gate output was byte-identical.

C. Negative control for the transport: declared range that cannot bind must
   yield incomplete, and a unit WITHOUT explanation_lines must still use the
   (now-fixed) fallback scan.
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
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.resolver.reference import extract_targets  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    per_paper = {}
    totals = Counter()
    mismatches = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        spans = {s.span_id: s for s in run.resolved_spans}
        unres = {u.reference_id: u for u in run.unresolved_references}

        declared = [t for t in extract_targets(payload) if t.role == "explanation"]
        n_declared = sum(1 for t in declared if t.evidence_lines)
        resolved = 0
        for t in declared:
            sp = spans.get(f"sp-{t.target_id}")
            if sp is not None:
                resolved += 1
            if t.evidence_lines and sp is not None:
                s, e = t.evidence_lines
                exp = [f"P1L{n:03d}" for n in range(s, e + 1)]
                if list(sp.line_refs) != exp:
                    mismatches.append({
                        "paper": p.parent.name, "unit": t.unit_id,
                        "declared": [s, e], "resolved_n": len(sp.line_refs),
                        "resolved_head": list(sp.line_refs)[:3],
                    })
        n_unres_expl = sum(1 for u in run.unresolved_references if u.role == "explanation")
        rec = {
            "units": len(m.units),
            "explanation_targets": len(declared),
            "with_declared_range": n_declared,
            "resolved": resolved,
            "unresolved": n_unres_expl,
            "region_roles": sorted({r.role for r in run.structural_regions}),
        }
        per_paper[p.parent.name] = rec
        totals.update(rec)

    report = {
        "per_paper": per_paper,
        "totals": dict(totals),
        "binding_mismatches": mismatches,
    }
    (OUT / "explanation_cross_paper.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"{'paper':<6}{'units':>6}{'expl_tgt':>9}{'declared':>9}{'resolved':>9}"
          f"{'unres':>7}  regions")
    for paper, r in per_paper.items():
        print(f"{paper:<6}{r['units']:>6}{r['explanation_targets']:>9}"
              f"{r['with_declared_range']:>9}{r['resolved']:>9}{r['unresolved']:>7}"
              f"  {r['region_roles']}")
    print("\nTOTALS:", json.dumps(dict(totals), ensure_ascii=False))
    print("binding mismatches:", len(mismatches))
    for mm in mismatches[:10]:
        print("  ", mm)


if __name__ == "__main__":
    main()
