"""Read-only feasibility test: can the HTML answer table be decoded
DETERMINISTICALLY by 题号 lookup (no human judgement)?

Your MIMO proposes deferring the answer-table contract until "human feedback".
If the table has a 题号 row that indexes the 答案 row, decoding is mechanical:
    find the cell whose text == str(question_number) in a 题号 row,
    take the cell at the same column in the adjacent 答案 row.

This measures how many of the pending single_choice units that would unblock,
using ONLY the resolver-compiled answer text (no new data, no code change).
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


def parse_table(html: str) -> list[list[str]]:
    rows = []
    for tr in ROW_RE.findall(html):
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in CELL_RE.findall(tr)]
        if cells:
            rows.append(cells)
    return rows


def decode_answer(html: str, qn: str) -> str | None:
    """Deterministic: locate qn in a 题号 row, take same-column cell of the
    immediately following 答案 row."""
    rows = parse_table(html)
    for i, row in enumerate(rows):
        if any(c == qn for c in row):
            # find the answer row: next row that starts with 答案
            for j in range(i + 1, min(i + 3, len(rows))):
                if rows[j] and rows[j][0] == "答案":
                    col = row.index(qn)
                    if col < len(rows[j]):
                        return rows[j][col]
            # or the row above is 答案
            for j in range(max(0, i - 2), i):
                if rows[j] and rows[j][0] == "答案":
                    col = row.index(qn)
                    if col < len(rows[j]):
                        return rows[j][col]
    return None


def main() -> None:
    tot = Counter()
    samples = []
    per_paper = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        qn_by_unit = {}
        for u in m.units:
            if u.question_numbers:
                qn_by_unit[u.unit_id] = str(u.question_numbers[0])
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
        for leaf in compiled.leaves:
            ans = leaf.answer
            txt = (ans.text if ans else "") or ""
            if verify(leaf.canonical_question_type, txt,
                      tuple(str(o.label) for o in leaf.options if o.label)) is True:
                continue
            is_table = txt.lstrip().startswith("<table")
            c["pending"] += 1
            c["table_answer" if is_table else "nontable_answer"] += 1
            if not is_table:
                continue
            qn = qn_by_unit.get(leaf.unit_id)
            got = decode_answer(txt, qn) if qn else None
            ok = got is not None and verify(
                leaf.canonical_question_type, got,
                tuple(str(o.label) for o in leaf.options if o.label)) is True
            c["decoded" if got else "decode_failed"] += 1
            if ok:
                c["decoded_ok"] += 1
                c["decoded_INVALID"] += 0
            elif got:
                c["decoded_INVALID"] += 1
            if len(samples) < 8:
                samples.append({"paper": p.parent.name, "unit": leaf.unit_id,
                                "qn": qn, "decoded": got, "valid": bool(ok)})
        per_paper[p.parent.name] = dict(c)
        tot.update(c)

    print(f"{'paper':<6}{'pending':>8}{'tableAns':>9}{'nonTable':>9}"
          f"{'decoded':>8}{'decOK':>7}{'decBAD':>7}{'fail':>6}")
    for paper, c in per_paper.items():
        print(f"{paper:<6}{c.get('pending',0):>8}{c.get('table_answer',0):>9}"
              f"{c.get('nontable_answer',0):>9}{c.get('decoded',0):>8}"
              f"{c.get('decoded_ok',0):>7}{c.get('decoded_INVALID',0):>7}"
              f"{c.get('decode_failed',0):>6}")
    print("\nTOTALS:", dict(tot))
    print("\nsamples:")
    for s in samples:
        print(f"   {s['paper']}/{s['unit']} qn={s['qn']} decoded={s['decoded']!r} "
              f"valid={s['valid']}")

    (OUT / "table_answer_decodability.json").write_text(
        __import__("json").dumps({"per_paper": per_paper, "totals": dict(tot),
                                  "samples": samples}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'table_answer_decodability.json'}")


if __name__ == "__main__":
    main()
