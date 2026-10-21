"""Read-only GROUND TRUTH check for B3c-B.

For every auto_approve leaf whose answer is a short token, verify the token
equals the cell of the answer table at the column whose 题号 cell == the leaf's
own question number. Any mismatch = fabrication/off-by-one and must be reported.
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
from app.domains.gate.policy import evaluate  # noqa: E402
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


def rows_of(html):
    out = []
    for tr in ROW_RE.findall(html):
        c = [re.sub(r"<[^>]+>", "", x).strip() for x in CELL_RE.findall(tr)]
        if c:
            out.append(c)
    return out


def expected_token(html: str, qn: str) -> str | None:
    """Independent re-implementation: locate qn in a 题号 row, take the
    immediately-following 答案 row's same column."""
    rows = rows_of(html)
    for i, r in enumerate(rows):
        if r and r[0] == "题号" and qn in r[1:]:
            col = r.index(qn)
            for j in range(i + 1, min(i + 3, len(rows))):
                if rows[j] and rows[j][0] == "答案":
                    return rows[j][col] if col < len(rows[j]) else None
    return None


def main() -> None:
    tot = Counter()
    mismatches = []
    samples = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        # declared qn per unit AND per (leaf) unit id
        qn_of = {}
        for u in m.units:
            if u.question_numbers:
                qn_of[u.unit_id] = str(u.question_numbers[0])
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
        # raw manifest html per unit: find the answer table in source
        raw_tables = [t for t in texts if t.lstrip().startswith("<table") and "答案" in t]

        for leaf in compiled.leaves:
            ans = leaf.answer
            tok = (ans.text if ans else "") or ""
            if verify(leaf.canonical_question_type, tok,
                      tuple(str(o.label) for o in leaf.options if o.label)) is not True:
                continue
            if not tok or len(tok) > 3:
                continue
            owner = leaf.unit_id[:-4] if leaf.unit_id.endswith(".sub") else leaf.unit_id
            qn = qn_of.get(owner)
            if qn is None:
                tot["no_qn"] += 1
                continue
            # find a raw table that contains this qn in a 题号 row
            exp = None
            for t in raw_tables:
                e = expected_token(t, qn)
                if e is not None:
                    exp = e
                    break
            if exp is None:
                tot["no_table_hit(short-answer/other)"] += 1
                continue
            tot["checked"] += 1
            if exp.upper() == tok.upper():
                tot["MATCH"] += 1
            else:
                tot["MISMATCH"] += 1
                mismatches.append({"paper": paper, "unit": leaf.unit_id, "qn": qn,
                                   "compiled": tok, "table": exp})
            if len(samples) < 12:
                samples.append({"paper": paper, "unit": leaf.unit_id, "qn": qn,
                                "token": tok, "table_cell": exp})

    print("TOTALS:", json.dumps(dict(tot), ensure_ascii=False))
    print("\nsamples (unit, qn, compiled token, table cell):")
    for s in samples:
        flag = "OK " if (s["token"] or "").upper() == (s["table_cell"] or "").upper() else "BAD"
        print(f"   {flag} {s['paper']}/{s['unit']} qn={s['qn']} "
              f"compiled={s['token']!r} table={s['table_cell']!r}")
    print("\nMISMATCHES:")
    for x in mismatches[:20]:
        print(f"   {x['paper']}/{x['unit']} qn={x['qn']} compiled={x['compiled']!r} "
              f"table={x['table']!r}")

    (OUT / "verify_b3cb_groundtruth.json").write_text(
        json.dumps({"totals": dict(tot), "samples": samples, "mismatches": mismatches},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_b3cb_groundtruth.json'}")


if __name__ == "__main__":
    main()
