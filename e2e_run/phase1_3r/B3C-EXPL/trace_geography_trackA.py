"""Read-only: faithful Track A reproduction for 地理 (runner.py:149-160 order).

runner.py does:
    payload = manifest_to_annotation_payload(manifest)
    payload = attach_material_boundary_markers(payload, {uid: material_lines}, line_texts)

The previous probe skipped the second step, which is why start_marker was null.
This version reproduces the real pipeline and reports:
  - what marker the adapter actually attaches for each material_lines
  - which units get a MATERIAL_BOUNDARY_MARKER_UNAVAILABLE known_gap
  - the resolver outcome with markers attached
  - the real stem zone content (for Q2: why 16/21/24/26/40/42/44/51..55 are missing)
  - duplicate question numbers in the question zone (for Q2: ambiguity of 1 and 3)
"""
from __future__ import annotations

import json
import os
import re
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

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
    material_boundary_markers,
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
            payload,
            {u.unit_id: u.material_lines for u in m.units if u.material_lines},
            texts,
        )

        gaps = (payload.get("producer_boundary") or {}).get("known_gaps") or []
        codes = Counter(g.get("code") for g in gaps)
        print("known_gaps by code:", dict(codes))

        print("\n-- adapter material markers (first 6) --")
        with_text = without_text = 0
        for u in payload["semantic_units"]:
            mat = (u.get("shared_components") or {}).get("material") or {}
            sm = mat.get("start_marker") or {}
            if sm.get("text"):
                with_text += 1
            else:
                without_text += 1
        print(f"  with text={with_text}  without text={without_text}")
        for u in payload["semantic_units"][:6]:
            mat = (u.get("shared_components") or {}).get("material") or {}
            print(f"   {u.get('unit_id'):<10} "
                  f"{json.dumps(mat, ensure_ascii=False)[:150]}")
        for u in payload["semantic_units"]:
            mat = (u.get("shared_components") or {}).get("material") or {}
            if not (mat.get("start_marker") or {}).get("text"):
                print(f"   NO-MARKER {u.get('unit_id'):<10} "
                      f"{json.dumps(mat, ensure_ascii=False)[:150]}")

        print("\n-- per-unit material_lines -> marker mapping --")
        for unit in m.units:
            ml = unit.material_lines
            mk = material_boundary_markers(ml, texts) if ml else None
            flag = "OK" if mk else "NONE"
            sm = (mk or {}).get("start_marker", {})
            print(f"   {unit.unit_id:<10} ml={tuple(ml) if ml else None} {flag} "
                  f"start={(sm.get('text') or '')[:60]!r} gran={sm.get('granularity')}")

        print("\n=== resolver outcome (markers attached) ===")
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        print("resolved by role:", dict(Counter(s.role for s in run.resolved_spans)))
        unres = Counter((u.role, u.resolution_status, " / ".join(u.evidence))
                        for u in run.unresolved_references)
        print(f"unresolved total: {sum(unres.values())}")
        for (role, status, ev), n in unres.most_common():
            print(f"   {n:>4}  {role:<12} {status:<12} {ev[:95]}")

        # ---- Q2 evidence: question-zone entry lines ----
        print("\n=== Q2: real source forms of question numbers in question zone ===")
        entry = re.compile(r"(?<![\d])(\d{1,3})\s*[.．、:]")
        esc = re.compile(r"(?<![\d])(\d{1,3})\\\s*[.．、:]")
        starts = defaultdict(list)
        esc_hits = []
        for s in srs:
            t = s.text.strip()
            mm = entry.search(t)
            if mm and mm.start() == 0:
                starts[mm.group(1)].append((s.line_no_in_page, t[:70]))
            if esc.search(t):
                esc_hits.append((s.line_no_in_page, t[:70]))
        dupes = {k: v for k, v in starts.items() if len(v) > 1}
        print("clean-start numbers:", sorted(starts, key=int))
        print("duplicates (>1 clean start):")
        for k, v in sorted(dupes.items(), key=lambda x: int(x[0])):
            print(f"   q{k}: {[(n, tx) for n, tx in v]}")
        print(f"\nescaped-dot lines not matched as clean start: {len(esc_hits)}")
        for n, tx in esc_hits[:30]:
            print(f"   L{n}: {tx!r}")

        missing_qs = ["16", "21", "24", "26", "40", "42", "44", "51", "52", "53", "54", "55"]
        print("\n-- locate the 'missing' numbers in raw source (any form) --")
        for q in missing_qs:
            pat = re.compile(rf"(?<![\d]){q}\s*\\?\s*[.．、:]")
            hits = [(s.line_no_in_page, s.text.strip()[:80])
                    for s in srs if pat.search(s.text.strip())]
            print(f"   q{q}: {hits[:3] if hits else 'NOT FOUND IN SOURCE'}")

        out = {
            "known_gaps_by_code": dict(codes),
            "material_marker_with_text": with_text,
            "material_marker_without_text": without_text,
            "resolved_by_role": dict(Counter(s.role for s in run.resolved_spans)),
            "unresolved": [{"role": r, "status": s, "evidence": e, "count": n}
                           for (r, s, e), n in unres.most_common()],
            "clean_start_numbers": sorted(starts, key=int),
            "duplicate_clean_starts": {k: v for k, v in dupes.items()},
            "escaped_dot_lines": esc_hits[:60],
        }
        (OUT / "geography_trackA_trace.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_trackA_trace.json'}")


if __name__ == "__main__":
    main()
