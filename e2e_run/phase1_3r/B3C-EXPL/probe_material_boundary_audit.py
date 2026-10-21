"""Read-only Q3: is Producer content-based material anchoring sound in principle?

For every corpus unit with material_lines, compare the Producer's declared
inclusive range against the span the Resolver actually derives from the
adapter's markers. If derived spans systematically extend beyond declared
ranges into neighbouring units, the anchoring METHOD (anchor = nearest UNIQUE
non-empty text) is unsound on documents with repeated/blank-heavy regions --
independent of subject.

Also censuses all material-overlap demotions corpus-wide.
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
    rows = []
    ovl = Counter()
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

        mat_spans = {}
        for s in run.resolved_spans:
            if s.role == "material":
                mat_spans[s.span_id[3:].rsplit(".material", 1)[0]] = s
        # unresolved material refs and why
        for u in run.unresolved_references:
            if u.role == "material":
                ovl[(p.parent.name, u.reference_id)] = " / ".join(u.evidence)

        for mu in m.units:
            if not mu.material_lines:
                continue
            lo, hi = mu.material_lines
            sp = mat_spans.get(mu.unit_id)
            if sp is None:
                derived = None
            else:
                nos = [int(r[3:]) for r in sp.line_refs]
                derived = (min(nos), max(nos))
            rows.append({
                "paper": p.parent.name, "unit": mu.unit_id,
                "declared": [lo, hi],
                "derived": list(derived) if derived else None,
                "extends_beyond": bool(derived and (derived[1] > hi or derived[0] < lo)),
                "unresolved": mu.unit_id in {k[1].split(".")[0] for k in ovl},
            })

    print(f"{'paper':<6}{'unit':<12}{'declared':<14}{'derived':<14}{'beyond?':<9}unresolved")
    for r in rows:
        print(f"{r['paper']:<6}{r['unit']:<12}{str(r['declared']):<14}"
              f"{str(r['derived']):<14}{str(r['extends_beyond']):<9}{r['unresolved']}")

    print("\n=== material overlap demotions (corpus-wide) ===")
    for (paper, rid), ev in ovl.items():
        print(f"  {paper}/{rid}: {ev[:95]}")
    print(f"\ntotal material units      : {len(rows)}")
    print(f"units deriving beyond decl: {sum(1 for r in rows if r['extends_beyond'])}")
    print(f"units unresolved (overlap): {sum(1 for r in rows if r['unresolved'])}")

    print("\n=== per-paper material units / overlap-demoted ===")
    agg = Counter()
    for r in rows:
        agg[(r["paper"], "units")] += 1
        if r["unresolved"]:
            agg[(r["paper"], "overlap")] += 1
    for paper in sorted({r["paper"] for r in rows}):
        print(f"  {paper:<6} units={agg[(paper,'units')]:<4} overlap_demoted={agg[(paper,'overlap')]}")

    (OUT / "material_boundary_audit.json").write_text(
        json.dumps({"rows": rows,
                    "overlaps": {f"{p}/{r}": e for (p, r), e in ovl.items()}},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'material_boundary_audit.json'}")


if __name__ == "__main__":
    main()
