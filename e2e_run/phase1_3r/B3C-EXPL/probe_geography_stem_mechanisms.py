"""Read-only Q2 deep-dive: exact mechanism per stem failure class.

Classes to prove:
  escaped-dot  : source has '21\\. ' etc. -> is_question_start() cannot match
  missing      : number absent from question zone in ANY recognized form
  ambiguous    : number occurs >1x in question zone (section-local numbering)

Also establishes the target-count fact: 25 stem targets for 55 question_numbers.
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

from app.domains.resolver.match_normalization import (  # noqa: E402
    is_question_start,
    normalize_text,
)
from app.domains.resolver.resolver import (  # noqa: E402
    SourceResolver,
    _entry_offsets,
)
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
            payload,
            {u.unit_id: u.material_lines for u in m.units if u.material_lines},
            texts,
        )
        resolver = SourceResolver(source_version_id=uuid.uuid4(), lines=views)
        run = resolver.resolve(payload)

        # what zone does the resolver actually scan for question starts?
        qzone = resolver._question_zone()
        qz_refs = {l.line_ref for l in qzone}
        qz_end = resolver._qzone_end
        print(f"source lines total : {len(srs)}")
        print(f"question zone size : {len(qzone)}  (_qzone_end={qz_end})")
        if qzone:
            print(f"question zone span : {qzone[0].line_ref} .. {qzone[-1].line_ref}")
        print(f"resolved by role   : {dict(Counter(s.role for s in run.resolved_spans))}")

        # ---- target count fact ----
        tot_qn = sum(len(u.question_numbers or []) for u in m.units)
        print(f"\nmanifest units={len(m.units)} declared question_numbers={tot_qn}")
        print(f"stem targets emitted (1 per unit, first qn only) = {len(m.units)}")

        # ---- per declared question number: why did its unit's stem fail? ----
        entry = re.compile(r"(?<![\d])(\d{1,3})\s*[.．、:]")
        esc = re.compile(r"(?<![\d])(\d{1,3})\\\s*[.．、:]")
        print("\n-- per-unit first-qn classification --")
        buckets = Counter()
        detail = []
        for u in m.units:
            qn = str(u.question_numbers[0]) if u.question_numbers else None
            if qn is None:
                continue
            # lines in question zone where is_question_start == qn
            zone_hits = [(l.line_no_in_page, l.text.strip())
                         for l in qzone if is_question_start(normalize_text(l.text)) == qn]
            # any line in the whole doc where is_question_start == qn
            all_hits = [(l.line_no_in_page, l.text.strip())
                        for l in srs if is_question_start(normalize_text(l.text)) == qn]
            esc_hits = [(s.line_no_in_page, s.text.strip())
                        for s in srs if (mm := esc.search(s.text.strip()))
                        and mm.group(1) == qn]
            if len(zone_hits) == 1:
                cls = "resolved"
            elif len(zone_hits) > 1:
                cls = "ambiguous"
            elif esc_hits:
                cls = "escaped_dot"
            else:
                cls = "missing"
            buckets[cls] += 1
            detail.append({
                "unit_id": u.unit_id, "first_qn": qn, "class": cls,
                "question_zone_hits": zone_hits,
                "outside_zone_hits": [h for h in all_hits if h not in zone_hits],
                "escaped_hits": esc_hits,
            })
        print("classification counts:", dict(buckets))
        for d in detail:
            if d["class"] != "resolved":
                print(f"   {d['unit_id']:<10} qn={d['first_qn']:<3} {d['class']:<12} "
                      f"zone={d['question_zone_hits']} "
                      f"esc={[e[0] for e in d['escaped_hits']]} "
                      f"outside={[o[0] for o in d['outside_zone_hits']]}")

        # ---- _ENTRY_RE behaviour on the escaped forms ----
        print("\n-- _ENTRY_RE / is_question_start behaviour on escaped-dot lines --")
        for s in srs:
            t = s.text.strip()
            if esc.search(t):
                mm = esc.search(t)
                qn = mm.group(1)
                print(f"   L{s.line_no_in_page:<4} qn={qn:<3} "
                      f"_ENTRY_RE offsets={_entry_offsets(t, qn)} "
                      f"is_question_start={is_question_start(normalize_text(t))!r} "
                      f"text={t[:52]!r}")

        # ---- ambiguous detail ----
        print("\n-- ambiguous numbers: every zone_hit --")
        for d in detail:
            if d["class"] == "ambiguous":
                print(f"   qn={d['first_qn']} unit={d['unit_id']}")
                for n, tx in d["question_zone_hits"]:
                    print(f"      L{n}: {tx[:80]!r}")
                print(f"      outside zone: "
                      f"{[(n, tx[:60]) for n, tx in d['outside_zone_hits']]}")

        # ---- where do 51..55 live? ----
        print("\n-- numbers 51..55 and 26: all raw occurrences in source --")
        for q in ["26", "51", "52", "53", "54", "55"]:
            pat = re.compile(rf"(?<![\d]){q}\s*\\?\s*[.．、:）)）]")
            hits = [(s.line_no_in_page, s.text.strip()[:90])
                    for s in srs if pat.search(s.text.strip())]
            print(f"   q{q}: {hits[:4] if hits else 'NOT FOUND'}")

        out = {
            "source_lines": len(srs),
            "question_zone_size": len(qzone),
            "question_zone_end": qz_end,
            "resolved_by_role": dict(Counter(s.role for s in run.resolved_spans)),
            "total_declared_question_numbers": tot_qn,
            "stem_targets": len(m.units),
            "classification_counts": dict(buckets),
            "unit_detail": detail,
        }
        (OUT / "geography_stem_mechanisms.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_stem_mechanisms.json'}")


if __name__ == "__main__":
    main()
