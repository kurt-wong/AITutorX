"""Read-only: can the remaining blockers be root-caused from artifacts ALONE,
without a human-facing Console?

Samples the top blockers from the verified Task-E census and goes straight to the
real read-point for each:
  A. option unresolved  (declared options exist, spans do not resolve)
  B. stem unresolved    (question-number identity not located)
  C. options missing    (choice type with no option declaration)

For each, prints the declared range, the actual source lines, and the resolver's
own unresolved evidence -- i.e. whether the fix point is already determinable.
"""
from __future__ import annotations

import os
import re
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

from app.domains.resolver.match_normalization import (  # noqa: E402
    is_question_start,
    normalize_text,
)
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

SAMPLE = {"化学": ["Q1", "Q3", "Q9", "Q19", "Q25"],
          "政治": ["Q6", "Q13", "Q25", "U9-10"],
          "生物": ["Q1", "Q20"]}


def main() -> None:
    agg = Counter()
    detail = []
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        if paper not in SAMPLE:
            continue
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
        unres = {}
        for u in run.unresolved_references:
            unres.setdefault(u.reference_id, (u.resolution_status, " / ".join(u.evidence)))
        qn_hits = Counter()
        for s in srs:
            q = is_question_start(normalize_text(s.text))
            if q:
                qn_hits[q] += 1

        for mu in m.units:
            if mu.unit_id not in SAMPLE[paper]:
                continue
            q0 = str(mu.question_numbers[0]) if mu.question_numbers else None
            entry = {"paper": paper, "unit": mu.unit_id, "qn0": q0,
                     "declared_options": [f"{o.label}@{o.start_line}" for o in mu.options or []],
                     "questions_lines": tuple(mu.questions_lines) if mu.questions_lines else None,
                     "option_unresolved": [], "stem_state": None}
            for lab in [o.label for o in mu.options or []]:
                key = f"{mu.unit_id}.sub.option.{lab}"
                if key in unres:
                    entry["option_unresolved"].append((lab, unres[key]))
            stem_key = f"{mu.unit_id}.sub.stem"
            entry["stem_state"] = unres.get(stem_key, ("resolved", ""))
            agg["units"] += 1
            agg["opt_unres_units" if entry["option_unresolved"] else "opt_ok_units"] += 1
            if entry["stem_state"][0] != "resolved":
                agg["stem_unres_units"] += 1
            # show the declared option lines
            lines = sorted({o.start_line for o in mu.options or []})
            entry["option_line_texts"] = [(n, texts[n - 1][:70]) for n in lines[:5]]
            detail.append(entry)

    print("AGGREGATE:", dict(agg))
    for d in detail:
        print(f"\n=== {d['paper']}/{d['unit']} qn0={d['qn0']} "
              f"q_lines={d['questions_lines']}")
        print(f"    declared options: {d['declared_options']}")
        print(f"    stem            : {d['stem_state']}")
        print(f"    option unresolved: {d['option_unresolved']}")
        for n, t in d["option_line_texts"]:
            print(f"      L{n}: {t!r}")

    (OUT / "rootcause_from_artifacts.json").write_text(
        __import__("json").dumps({"aggregate": dict(agg), "detail": detail},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'rootcause_from_artifacts.json'}")


if __name__ == "__main__":
    main()
