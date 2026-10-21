"""Read-only: structural audit of option LABEL integrity (not answer-driven).

Owner requires the survey NOT to use `answer in labels` as the discovery entry.
This probe discovers candidates purely from the SOURCE side:
  for each choice unit, scan its own declared question/option range and count
  how many option labels are LITERALLY present in source, versus how many the
  manifest declared, plus detect damaged/glued label forms (e.g. '2D.').

Purpose: decide whether the 2 known B-class samples are isolated or whether a
deterministic Producer label-parsing gap is generalizable -- WITHOUT touching
any code.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHOICE = {"single_choice", "multiple_choice", "true_false"}
# a well-formed label at start-of-line or after a boundary
LEAD_LABEL = re.compile(r"(?<![A-Za-z0-9_])([A-H])\s*[.．、:)）]")
# glue pattern: a non-space, non-label char immediately before a label token
GLUED = re.compile(r"(?<![A-Za-z0-9_\s.．、:)）])([^\sA-Za-z0-9_])([A-H])\s*[.．、:)）]")


def main() -> None:
    tot = Counter()
    suspects = []
    glued = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        for u in m.units:
            if u.original_question_type not in CHOICE:
                continue
            tot["choice_units"] += 1
            # the unit's own source window
            spans = [x for x in (u.questions_lines, u.material_lines) if x]
            if not spans:
                continue
            lo = min(x[0] for x in spans)
            hi = max(x[1] for x in spans)
            lo = max(1, lo)
            hi = min(len(texts), hi)
            labels_in_src = set()
            glue_hits = []
            for n in range(lo, hi + 1):
                t = texts[n - 1]
                for mm in LEAD_LABEL.finditer(t):
                    labels_in_src.add(mm.group(1).upper())
                for gm in GLUED.finditer(t):
                    glue_hits.append((n, gm.group(0), t.strip()[:70]))
            declared = {o.label.upper() for o in u.options}
            if glue_hits:
                tot["units_with_glued_label"] += 1
                glued.append({"paper": paper, "unit": u.unit_id,
                              "declared": sorted(declared),
                              "src_labels": sorted(labels_in_src),
                              "glue": glue_hits[:3],
                              "range": [lo, hi]})
            # structural mismatch: source shows more labels than declared
            if declared and labels_in_src - declared:
                tot["src_has_labels_not_declared"] += 1
                suspects.append({"paper": paper, "unit": u.unit_id,
                                 "declared": sorted(declared),
                                 "src_only": sorted(labels_in_src - declared),
                                 "range": [lo, hi],
                                 "qtype": u.original_question_type})

    print("TOTALS:", json.dumps(dict(tot), ensure_ascii=False, indent=2))
    print(f"\n=== units where SOURCE shows labels the manifest did NOT declare ===")
    for s in suspects:
        print(f"   {s['paper']}/{s['unit']:<10} declared={s['declared']} "
              f"src_only={s['src_only']} range={s['range']} qtype={s['qtype']}")
    print(f"\n=== units with a GLUED/damaged label token in their option range ===")
    for g in glued:
        print(f"   {g['paper']}/{g['unit']:<10} declared={g['declared']} "
              f"src={g['src_labels']} range={g['range']}")
        for n, tok, txt in g["glue"]:
            print(f"        L{n}: token={tok!r}  {txt!r}")

    (OUT / "structural_option_label_audit.json").write_text(
        json.dumps({"totals": dict(tot), "src_only_labels": suspects,
                    "glued": glued}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'structural_option_label_audit.json'}")


if __name__ == "__main__":
    main()
