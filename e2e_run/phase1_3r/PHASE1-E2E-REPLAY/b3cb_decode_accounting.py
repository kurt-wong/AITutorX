# -*- coding: utf-8 -*-
"""B3c-B decode accounting: eligible / decoded / contract_rejected / unresolved."""
import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\PHASE1-E2E-REPLAY")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.grammar import verify  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver, decode_answer_table_cell  # noqa: E402
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
    rows = []
    tot = Counter()
    for p in find_manifests(CORPUS):
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
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)

        for n in ir.units:
            leaves = [n] if n.unit_type != "composite_unit" else list(n.sub_questions)
            for leaf in leaves:
                ans = next((c for c in leaf.content if c.role == "answer"), None)
                if ans is None or ans.span_id is None:
                    continue
                span = span_map.get(ans.span_id)
                if span is None:
                    continue
                # is the raw source a table?
                raw = line_map[span.line_refs[0]].text if span.line_refs else ""
                is_table = "<td" in raw.lower()
                decoded = False
                cell = None
                if is_table:
                    qn = leaf.question_number or ""
                    cell = decode_answer_table_cell(raw, qn)
                    decoded = cell is not None
                # compiled answer text + grammar
                aleaf = next(
                    (l for l in compiled.leaves if l.unit_id == leaf.unit_id), None
                )
                ans_text = aleaf.answer.text if aleaf and aleaf.answer else ""
                labels = tuple(o.label for o in (aleaf.options if aleaf else ()))
                v = verify(leaf.original_question_type, ans_text, labels) if aleaf else None

                if is_table:
                    tot["table_answer"] += 1
                    if decoded:
                        tot["table_decoded"] += 1
                        tot[f"table_decoded__{cell[2][:20]}"] += 0  # placeholder
                    else:
                        tot["table_decode_failed"] += 1
                    # missing answer row vs other
                    if not decoded:
                        if "答案" not in raw:
                            tot["MISSING_ROW"] += 1
                        else:
                            tot["DECODE_FAIL_other"] += 1
                else:
                    tot["non_table_answer"] += 1

                if v is True:
                    tot["grammar_TRUE"] += 1
                elif v is None:
                    tot["grammar_NONE"] += 1
                else:
                    tot["grammar_FALSE"] += 1

                rows.append({
                    "paper": p.parent.name,
                    "unit": leaf.unit_id,
                    "qtype": leaf.original_question_type,
                    "qn": leaf.question_number,
                    "is_table": is_table,
                    "decoded": decoded,
                    "cell": cell[2] if cell else None,
                    "ans_text_preview": (ans_text or "")[:40],
                    "grammar": v,
                    "granularity": span.granularity,
                })

    (OUT / "b3cb_decode_accounting.json").write_text(
        json.dumps({"totals": dict(tot), "rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("TOTALS:")
    for k, v in sorted(tot.items(), key=lambda kv: -kv[1]):
        if v:
            print(f"  {k}: {v}")
    # sample failures
    fails = [r for r in rows if r["is_table"] and not r["decoded"]]
    print(f"\ntable decode failed: {len(fails)}")
    for r in fails[:12]:
        print(f"  {r['paper']} {r['unit']} qn={r['qn']} preview={r['ans_text_preview']!r}")
    # grammar false on decoded
    gf = [r for r in rows if r["decoded"] and r["grammar"] is not True]
    print(f"\ndecoded but grammar not True: {len(gf)}")
    for r in gf[:12]:
        print(f"  {r['paper']} {r['unit']} cell={r['cell']!r} grammar={r['grammar']} qtype={r['qtype']}")


if __name__ == "__main__":
    main()
