# -*- coding: utf-8 -*-
"""Why do some geography option spans fail to resolve? Read-only diagnostic."""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
GEO_MF = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    m = load_manifest(GEO_MF)
    srs = load_source_lines(Path(m.source_file))
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

    unres = {}
    for u in run.unresolved_references:
        unres.setdefault(u.role, []).append((u.reference_id, u.resolution_status, u.evidence))

    for unit in m.units:
        if unit.unit_type != "composite_question":
            continue
        if unit.original_question_type not in {"single_choice"}:
            continue
        uid = unit.unit_id
        opt_spans = [s for s in run.resolved_spans if s.role == "option" and uid in s.span_id]
        stem_spans = [s for s in run.resolved_spans if s.role == "stem" and uid in s.span_id]
        opt_un = [x for x in unres.get("option", []) if uid in x[0]]
        stem_un = [x for x in unres.get("question_label", []) or unres.get("stem", []) if uid in x[0]]
        # also check any unresolved with uid
        any_un = [(r, rid, st, ev) for r, lst in unres.items()
                  for rid, st, ev in lst if uid in rid]
        ql = unit.questions_lines
        # show first option-marker line in questions region
        marks = []
        if ql:
            for i in range(ql[0], min(ql[1], len(srs)) + 1):
                t = srs[i - 1].text
                if any(x in t for x in ("A.", "B.", "A．", "A、")):
                    marks.append((i, t[:60]))
                    break
        print(f"{uid:12} qn={unit.question_numbers} q={ql} "
              f"stem_res={len(stem_spans)} opt_res={len(opt_spans)} "
              f"first_opt_line={marks[0] if marks else None}")
        for x in any_un[:4]:
            print(f"    UNRES {x}")


if __name__ == "__main__":
    main()
