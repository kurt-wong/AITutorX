"""INDEPENDENT P1.4-B verification — is the repaired option span degenerate?

Q4 replay shows option texts ['A. 关于 x 轴对称 B. 关于 y 轴对称', 'B', 'C. ... 2D. ...', 'D'].
The 4th option text is literally 'D' (label only), and the recovered content
`关于直线 y= -x 对称` appears to live inside the *C* option span.

This checks, for Q20/Q23/Q4/Q29:
  - each compiled option's span text and length
  - whether any option span is label-only / degenerate
  - whether the recovered content is actually carried by some option
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
PAPERS = {"化学", "数学", "历史"}


def main() -> None:
    out_rows = []
    degenerate_global = []
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        if paper not in PAPERS:
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
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)

        for root in ir.units:
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id not in want:
                    continue
                recs = []
                for o in leaf.options:
                    txt = o.text
                    stripped = txt.strip()
                    label_only = stripped.upper() == str(o.label).upper()
                    recs.append({"label": str(o.label), "len": len(stripped),
                                 "text": stripped[:70], "label_only": label_only})
                    if label_only:
                        degenerate_global.append(
                            {"paper": paper, "root": root.unit_id, "leaf": leaf.unit_id,
                             "label": str(o.label), "text": stripped[:40]})
                if root.unit_id in WATCH.get(paper, set()):
                    out_rows.append({"paper": paper, "root": root.unit_id,
                                     "leaf": leaf.unit_id, "options": recs})

    print("=" * 94)
    print("REPAIRED OPTION SPANS — content integrity check")
    print("=" * 94)
    for r in sorted(out_rows, key=lambda x: (x["paper"], x["root"])):
        print(f"\n{r['paper']}/{r['root']}  leaf={r['leaf']}")
        for o in r["options"]:
            flag = "  <<< DEGENERATE (label only)" if o["label_only"] else ""
            print(f"   {o['label']}: len={o['len']:<4} {o['text']!r}{flag}")

    print("\n" + "=" * 94)
    print("DEGENERATE (label-only) option spans — 3 papers")
    print("=" * 94)
    print(f"count: {len(degenerate_global)}")
    for d in degenerate_global:
        print(f"   {d['paper']}/{d['root']} label={d['label']} text={d['text']!r}")

    OUT.joinpath("_p14b_option_span_integrity.json").write_text(
        json.dumps({"watch": out_rows, "degenerate": degenerate_global},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_option_span_integrity.json'}")


if __name__ == "__main__":
    main()
