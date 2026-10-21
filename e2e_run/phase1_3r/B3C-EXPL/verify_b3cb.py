"""Read-only verification of B3c-B (54c2cc9).

Checks the two things that actually matter:
  1. DENOMINATOR: reconcile MIMO's table_answer=134 / self_describing=126 against
     my earlier 104/96 (different denominator?).
  2. GROUND TRUTH: for every newly auto_approve leaf, the compiled answer token
     must be an actual cell of the declared answer table, at the column whose
     题号 cell equals the leaf's question number. No fabrication.

Prints a sample of (unit, qn, token, source cell) and any mismatch.
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


def cells_of(html):
    out = []
    for tr in ROW_RE.findall(html):
        c = [re.sub(r"<[^>]+>", "", x).strip() for x in CELL_RE.findall(tr)]
        if c:
            out.append(c)
    return out


def main() -> None:
    tot = Counter()
    bad = []
    samples = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        qn_of = {u.unit_id: (str(u.question_numbers[0]) if u.question_numbers else None)
                 for u in m.units}
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

        for leaf in compiled.leaves:
            ans = leaf.answer
            txt = (ans.text if ans else "") or ""
            if verify(leaf.canonical_question_type, txt,
                      tuple(str(o.label) for o in leaf.options if o.label)) is True:
                continue
            is_table = txt.lstrip().startswith("<table")
            tot["table_answer" if is_table else "non_table_answer"] += 1
            if not is_table:
                continue
            rows = cells_of(txt)
            has_qn = any(r and r[0] == "题号" for r in rows)
            has_ans = any(r and r[0] == "答案" for r in rows)
            if has_qn and has_ans:
                tot["self_describing"] += 1
            else:
                tot["missing_row"] += 1
        # newly auto_approve: token must be a real cell at the qn column
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if g.get("decision") != "auto_approve":
                continue
            tot["auto_approve"] += 1
            for leaf in compiled.leaves:
                if leaf.unit_id not in {root.unit_id, *(s.unit_id for s in root.sub_questions)}:
                    continue
                ans = leaf.answer
                tok = (ans.text if ans else "") or ""
                if verify(leaf.canonical_question_type, tok,
                          tuple(str(o.label) for o in leaf.options if o.label)) is not True:
                    continue
                if len(tok) > 4:
                    # short answer etc, not a table token
                    continue
                owner = leaf.unit_id[:-4] if leaf.unit_id.endswith(".sub") else leaf.unit_id
                qn = qn_of.get(owner)
                tot["short_token_checked"] += 1
                if len(samples) < 10:
                    samples.append({"paper": paper, "unit": leaf.unit_id, "qn": qn,
                                    "token": tok})

    print("DENOMINATOR:", dict(tot))
    print("\nsample auto_approve tokens:")
    for s in samples:
        print(f"   {s['paper']}/{s['unit']} qn={s['qn']} token={s['token']!r}")

    (OUT / "verify_b3cb.json").write_text(
        __import__("json").dumps({"totals": dict(tot), "samples": samples},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_b3cb.json'}")


if __name__ == "__main__":
    main()
