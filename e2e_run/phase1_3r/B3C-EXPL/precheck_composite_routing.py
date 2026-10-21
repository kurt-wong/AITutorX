"""Read-only pre-check for Owner's Phase 1.4 task C-5 (composite hard boundary).

Question: can the CURRENT V3 composite runtime express per-sub-question answer
evidence from a multi-question answer table?

If a composite unit covers question_numbers [1,2] but the adapter emits exactly
ONE sub (question_number = question_numbers[0]), then a table holding answers for
BOTH 1 and 2 has no addressable destination for Q2's answer -> C-5 STOP condition.

Also checks C-6 variant tables (评分表: 题号|答案|分数) whose answer cell is not a
whitelist token (e.g. '正').
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


def rows_of(html):
    out = []
    for tr in ROW_RE.findall(html):
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in CELL_RE.findall(tr)]
        if cells:
            out.append(cells)
    return out


def main() -> None:
    tot = Counter()
    blocked = []
    variant = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        multi = {u.unit_id: list(u.question_numbers) for u in m.units
                 if len(u.question_numbers or []) > 1}
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

        # how many subs does each composite actually emit?
        for root in ir.units:
            if root.unit_type == "composite_unit":
                tot["composites"] += 1
                nsub = len(root.sub_questions)
                tot[f"subs_{nsub}"] += 1
                qns = multi.get(root.unit_id, [])
                if len(qns) > 1 and nsub == 1:
                    tot["multi_qn_single_sub"] += 1

        for leaf in compiled.leaves:
            ans = leaf.answer
            txt = (ans.text if ans else "") or ""
            if verify(leaf.canonical_question_type, txt,
                      tuple(str(o.label) for o in leaf.options if o.label)) is True:
                continue
            if not txt.lstrip().startswith("<table"):
                continue
            rows = rows_of(txt)
            has_qn = any(r and r[0] == "题号" for r in rows)
            has_ans = any(r and r[0] == "答案" for r in rows)
            if not (has_qn and has_ans):
                tot["missing_row"] += 1
                if len(variant) < 6:
                    variant.append({"paper": paper, "unit": leaf.unit_id,
                                    "rows": [r[:6] for r in rows[:3]]})
                continue
            tot["self_describing"] += 1
            # is the owning unit a multi-question composite?  -> routing gap
            owner = leaf.unit_id[:-4] if leaf.unit_id.endswith(".sub") else leaf.unit_id
            if len(multi.get(owner, [])) > 1:
                tot["blocked_multi_qn"] += 1
                if len(blocked) < 12:
                    blocked.append({"paper": paper, "unit": leaf.unit_id,
                                    "owner": owner, "qns": multi.get(owner)})
            else:
                tot["single_qn_decodable"] += 1

    print("TOTALS:", dict(tot))
    print("\n=== multi-question composites blocked by C-5 (sample) ===")
    for b in blocked:
        print(f"   {b['paper']}/{b['unit']} owner={b['owner']} qns={b['qns']}")
    print("\n=== MISSING_ROW variants ===")
    for v in variant:
        print(f"   {v['paper']}/{v['unit']} rows={v['rows']}")

    (OUT / "precheck_composite_routing.json").write_text(
        __import__("json").dumps({"totals": dict(tot), "blocked": blocked,
                                  "variant": variant}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'precheck_composite_routing.json'}")


if __name__ == "__main__":
    main()
