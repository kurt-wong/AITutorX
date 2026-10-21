"""Read-only: is the HTML answer table SELF-DESCRIBING?

This decides the B3c-B boundary question MIMO raised:
  - if every table carries an explicit 题号 row AND a 答案 row, then decoding is
    *structured evidence consumption* (Producer-declared mapping, read positionally
    WITHIN the table) -- not token guessing from context.
  - if tables lack the 题号 row, decoding would rely on POSITION => guessing, and
    would fall under the frozen AnswerTokenContract prohibition.

Also: which declared field points at the table (answer_lines?), i.e. is the table
already an explicitly declared evidence object?
"""
from __future__ import annotations

import json
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

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.grammar import verify  # noqa: E402
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

ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)


def rows_of(html: str) -> list[list[str]]:
    out = []
    for tr in ROW_RE.findall(html):
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in CELL_RE.findall(tr)]
        if cells:
            out.append(cells)
    return out


def main() -> None:
    tot = Counter()
    detail = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        # does the manifest declare answer_lines pointing at a table line?
        declared_tbl = 0
        for u in m.units:
            if u.answer_lines:
                declared_tbl += 1
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid, aid = uuid.uuid4(), uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, aid)
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {l.line_ref: l for l in srs}).compile(ir)
        c = Counter()
        seen_html = set()
        for leaf in compiled.leaves:
            ans = leaf.answer
            txt = (ans.text if ans else "") or ""
            if verify(leaf.canonical_question_type, txt,
                      tuple(str(o.label) for o in leaf.options if o.label)) is True:
                continue
            if not txt.lstrip().startswith("<table"):
                continue
            c["pending_table"] += 1
            rows = rows_of(txt)
            has_qn = any(r and r[0] == "题号" for r in rows)
            has_ans = any(r and r[0] == "答案" for r in rows)
            if has_qn:
                c["self_describing_qn_row"] += 1
            if has_ans:
                c["has_answer_row"] += 1
            if has_qn and has_ans:
                c["both_rows"] += 1
            else:
                c["MISSING_ROW"] += 1
            if txt not in seen_html and len(detail) < 6:
                seen_html.add(txt)
                detail.append({"paper": paper, "unit": leaf.unit_id,
                               "n_rows": len(rows),
                               "first_row": rows[0][:12] if rows else [],
                               "second_row": rows[1][:12] if len(rows) > 1 else []})
        c["manifest_units_with_answer_lines"] = declared_tbl
        for k, v in c.items():
            tot[k] += v

    print("TOTALS:", json.dumps(dict(tot), ensure_ascii=False, indent=2))
    print("\nsamples (structure):")
    for d in detail:
        print(f"  {d['paper']}/{d['unit']} rows={d['n_rows']}")
        print(f"      r0={d['first_row']}")
        print(f"      r1={d['second_row']}")

    (OUT / "table_self_describing.json").write_text(
        json.dumps({"totals": dict(tot), "samples": detail},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'table_self_describing.json'}")


if __name__ == "__main__":
    main()
