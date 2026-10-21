"""INDEPENDENT P1.4-B — exact option span evidence (declared vs compiled).

For Q20/Q23/Q4/Q29 prints, per declared label:
  - manifest declared (label, start_line, end_line)
  - resolved span kind / text / resolution_status
  - compiled option text
This proves whether a repaired option carries its content or is label-only.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate, leaf_unit_ids  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

WATCH = {"化学": {"Q20", "Q23"}, "数学": {"Q4"}, "历史": {"Q29"}}

# the span attributed to each option, harvested from the ResolvedRun
def main() -> None:
    report = []
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        if paper not in WATCH:
            continue
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
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
        )
        sv = uuid.uuid4()
        run = SourceResolver(source_version_id=sv, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv, uuid.uuid4())
        span_by_id = {s.span_id: s for s in run.resolved_spans}
        compiled = Compiler(span_by_id, {v.line_ref: v for v in views}).compile(ir)

        for root in ir.units:
            if root.unit_id not in WATCH[paper]:
                continue
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id not in want:
                    continue
                gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                rows = []
                for o in leaf.options:
                    sp = span_by_id.get(o.span_id)
                    rows.append({
                        "label": str(o.label),
                        "span_id": o.span_id,
                        "granularity": getattr(sp, "granularity", None),
                        "resolution_status": getattr(sp, "resolution_status", None),
                        "span_line_refs": list(getattr(sp, "line_refs", ()) or ()),
                        "span_text": getattr(sp, "text", None),
                        "compiled_text": o.text,
                    })
                report.append({"paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                               "decision": gate["decision"], "options": rows})

    for r in sorted(report, key=lambda x: (x["paper"], x["root"])):
        print("=" * 96)
        print(f"{r['paper']}/{r['root']}  leaf={r['leaf']}  gate={r['decision']}")
        for o in r["options"]:
            st = o["span_text"]
            deg = (st is not None and st.strip().upper() == o["label"].upper())
            print(f"   option {o['label']}:")
            print(f"      granularity={o['granularity']} status={o['resolution_status']} "
                  f"lines={o['span_line_refs']}")
            print(f"      span_text = {st!r}")
            print(f"      compiled  = {o['compiled_text'][:60]!r}"
                  f"{'   <<< LABEL-ONLY SPAN: content absent' if deg else ''}")

    OUT.joinpath("_p14b_option_span_evidence.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_option_span_evidence.json'}")


if __name__ == "__main__":
    main()
