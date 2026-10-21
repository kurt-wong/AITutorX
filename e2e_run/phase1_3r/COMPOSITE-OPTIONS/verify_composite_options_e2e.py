"""Verify composite options evidence transport end-to-end on real geography artifacts.

Read-point chain (no V3 business code modified):
  Producer manifest options[]
    → annotation_adapter _leaf_content → sub.content.options
    → resolver option targets → option ResolvedSpans
    → IR content role=option
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\COMPOSITE-OPTIONS")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    papers = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

        # per-unit: manifest options → payload options → resolved option spans → IR
        payload_by_id = {u["unit_id"]: u for u in payload["semantic_units"]}
        rows = []
        for unit in m.units:
            man_opts = [o.label for o in unit.options] if unit.options else []
            pu = payload_by_id.get(unit.unit_id) or {}
            if pu.get("unit_type") == "composite_unit":
                subs = pu.get("sub_questions") or []
                pay_opts = []
                for s in subs:
                    pay_opts.extend(
                        o.get("label") for o in (s.get("content", {}).get("options") or [])
                    )
            else:
                pay_opts = [
                    o.get("label") for o in (pu.get("content", {}).get("options") or [])
                ]
            # resolved option spans belonging to this unit / its .sub
            prefixes = (unit.unit_id, f"{unit.unit_id}.sub")
            res_opts = sorted({
                s.role + ":" + (s.span_id.split(".")[-1] if "." in s.span_id else "?")
                for s in run.resolved_spans
                if s.role == "option" and any(s.span_id.startswith(pr) or pr in s.span_id
                                              for pr in prefixes)
            })
            # simpler: count option spans whose span_id contains unit_id
            res_opt_labels = sorted({
                s.span_id.rsplit(".", 1)[-1]
                for s in run.resolved_spans
                if s.role == "option" and unit.unit_id in s.span_id
            })
            rows.append({
                "unit_id": unit.unit_id,
                "unit_type": unit.unit_type,
                "qtype": unit.original_question_type,
                "question_numbers": list(unit.question_numbers),
                "manifest_options": man_opts,
                "payload_options": pay_opts,
                "resolved_option_labels": res_opt_labels,
            })

        # IR-level: how many choice leaves now have option content
        try:
            ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
            ir_rows = []
            for n in ir.units:
                for leaf in ([n] if n.unit_type != "composite_unit" else list(n.sub_questions)):
                    opt_items = [c for c in leaf.content if c.role == "option"]
                    ir_rows.append({
                        "unit_id": leaf.unit_id,
                        "qtype": leaf.original_question_type,
                        "semantic_status": leaf.semantic_status,
                        "n_options": len(opt_items),
                        "options_resolved": sum(1 for c in opt_items if c.span_id),
                    })
        except Exception as e:
            ir_rows = [{"error": str(e)}]

        n_choice_comp = sum(
            1 for u in m.units
            if u.unit_type == "composite_question"
            and u.original_question_type in {"single_choice", "multiple_choice", "true_false"}
        )
        n_choice_comp_with_opts = sum(
            1 for u in m.units
            if u.unit_type == "composite_question"
            and u.original_question_type in {"single_choice", "multiple_choice", "true_false"}
            and u.options
        )
        n_nonchoice_comp = sum(
            1 for u in m.units
            if u.unit_type == "composite_question"
            and u.original_question_type not in {"single_choice", "multiple_choice", "true_false"}
        )
        n_nonchoice_with_opts = sum(
            1 for u in m.units
            if u.unit_type == "composite_question"
            and u.original_question_type not in {"single_choice", "multiple_choice", "true_false"}
            and u.options
        )
        papers.append({
            "paper": p.parent.name,
            "units": len(m.units),
            "choice_composite": n_choice_comp,
            "choice_composite_with_options": n_choice_comp_with_opts,
            "nonchoice_composite": n_nonchoice_comp,
            "nonchoice_composite_with_options": n_nonchoice_with_opts,
            "rows": rows,
            "ir": ir_rows,
        })
        print(f"{p.parent.name}: choice_comp {n_choice_comp_with_opts}/{n_choice_comp} "
              f"nonchoice_with_opts {n_nonchoice_with_opts}/{n_nonchoice_comp}")

    (OUT / "composite_options_e2e.json").write_text(
        json.dumps({"papers": papers}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Geography acceptance snapshot
    geo = next((x for x in papers if x["paper"] == "地理"), None)
    if geo:
        print("\n=== GEOGRAPHY ===")
        print(f"choice composite with options: "
              f"{geo['choice_composite_with_options']}/{geo['choice_composite']}")
        print(f"nonchoice composite with options (must be 0): "
              f"{geo['nonchoice_composite_with_options']}")
        for r in geo["rows"]:
            if r["unit_type"] == "composite_question":
                print(f"  {r['unit_id']:12} man={r['manifest_options']} "
                      f"pay={r['payload_options']} res={r['resolved_option_labels']}")
        print("\nIR:")
        for r in geo["ir"]:
            print(f"  {r}")


if __name__ == "__main__":
    main()
