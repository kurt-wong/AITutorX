"""G2 read-only investigation: 化学 Q23 answer=D vs labels=[A,B,C].

Full evidence chain. No code change. Classification only if evidence supports.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
MF = Path(
    r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考"
    r"\化学\2018北京春季高中会考化学（教师版）(1).manifest.json"
)
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
from app.domains.resolver.resolver import SourceResolver, decode_answer_table_cell  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    m = load_manifest(MF)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
    )
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {v.line_ref: v for v in views}
    compiled = Compiler(span_map, line_map).compile(ir)

    # manifest unit for Q23
    unit = next(u for u in m.units if u.unit_id == "Q23")
    print("=== MANIFEST Q23 ===")
    print(json.dumps({
        "unit_id": unit.unit_id, "qtype": unit.original_question_type,
        "question_numbers": list(unit.question_numbers),
        "stem_lines": unit.stem_lines, "options_lines": unit.options_lines,
        "options": [{"label": o.label, "start_line": o.start_line, "end_line": o.end_line}
                    for o in unit.options],
        "answer_lines": unit.answer_lines,
    }, ensure_ascii=False, indent=1))

    # source neighbourhood of Q23
    print("\n=== SOURCE around Q23 stem/options ===")
    if unit.stem_lines:
        lo = max(1, unit.stem_lines[0] - 2)
        hi = min(len(texts), (unit.options_lines[1] if unit.options_lines else unit.stem_lines[1]) + 3)
        for i in range(lo, hi + 1):
            print(f"  L{i}: {texts[i-1][:100]!r}")

    # option spans in resolver
    print("\n=== RESOLVED option spans for Q23 ===")
    for s in run.resolved_spans:
        if "Q23" in s.span_id and s.role == "option":
            line = line_map[s.line_refs[0]].text
            sl = line[s.start_offset:s.end_offset] if s.start_offset is not None else line[:80]
            print(f"  {s.span_id} {s.line_refs} {s.granularity} text={sl!r} ev={list(s.evidence)[:3]}")
    for u in run.unresolved_references:
        if "Q23" in u.reference_id and u.role == "option":
            print(f"  UNRES {u.reference_id} {u.resolution_status} {list(u.evidence)[:3]}")

    # compiled answer + labels
    leaf = next(l for l in compiled.leaves if l.unit_id == "Q23")
    labels = tuple(o.label for o in leaf.options)
    print("\n=== COMPILED Q23 ===")
    print(f"  answer.text={leaf.answer.text!r}" if leaf.answer else "  answer=None")
    print(f"  option labels={labels}")
    print(f"  verify(sc, text, labels)={verify(leaf.canonical_question_type, leaf.answer.text, labels)}")

    # answer table cell for qn=23
    ans_span = span_map.get(leaf.answer.span_id) if leaf.answer else None
    if ans_span:
        raw = line_map[ans_span.line_refs[0]].text
        cell = decode_answer_table_cell(raw, "23")
        print(f"\n=== ANSWER TABLE decode qn=23 → {cell}")
        print(f"  span ev={list(ans_span.evidence)}")
        print(f"  answer_lines declared={unit.answer_lines}")

    # does source contain option D near Q23?
    print("\n=== SEARCH D option near Q23 ===")
    import re
    for i, t in enumerate(texts, 1):
        if re.search(r"(?<![A-Za-z0-9_])D\s*[.．、:，,]", t) and unit.stem_lines and \
                unit.stem_lines[0] - 20 <= i <= unit.stem_lines[1] + 20:
            print(f"  L{i}: {t[:100]!r}")

    # neighbouring options of Q22/Q24 for comparison
    for qid in ("Q22", "Q24", "Q21", "Q25"):
        u2 = next((u for u in m.units if u.unit_id == qid), None)
        if u2:
            labs = [o.label for o in u2.options]
            print(f"  {qid} manifest options={labs} opt_lines={u2.options_lines}")


if __name__ == "__main__":
    main()
