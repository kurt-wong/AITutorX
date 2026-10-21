"""Phase 1 E2E Replay — three cuts later (873a343 + 7c2e51a + 7c9b8aa).

Read-only measurement of the real production chain:
  Producer manifest → annotation_adapter → SourceResolver
  → IRBuilder → Compiler → Gate.evaluate

No business-code change. No number-hunting. Reports funnel + incomplete causes.
"""
from __future__ import annotations

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


def _ir_problems(leaf) -> list[str]:
    """Recompute the same checks validate_ir uses, for cause attribution."""
    problems = []
    by_role = {c.role: c for c in leaf.content}
    if leaf.unit_type == "composite_unit":
        return ["composite_root"]  # only leaves are measured
    if "stem" not in by_role:
        problems.append("stem not declared")
    elif by_role["stem"].span_id is None:
        problems.append("stem unresolved")
    if "answer" not in by_role:
        problems.append("answer not declared")
    elif by_role["answer"].span_id is None:
        problems.append("answer unresolved")
    qt = leaf.original_question_type or ""
    needs_opts = qt in {"single_choice", "multiple_choice", "true_false"}
    if needs_opts and not any(c.role == "option" for c in leaf.content):
        problems.append("options missing for choice type")
    for c in leaf.content:
        if c.unsupported:
            problems.append(f"unsupported:{c.role}")
        elif c.span_id is None:
            problems.append(f"{c.role} unresolved")
    return problems


def measure_paper(path: Path) -> dict:
    m = load_manifest(path)
    srs = load_source_lines(Path(m.source_file))
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload,
        {u.unit_id: u.material_lines for u in m.units if u.material_lines},
        [s.text for s in srs],
    )
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)

    # leaf-level funnel
    leaves = []
    for root in ir.units:
        nodes = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        for leaf in nodes:
            leaves.append(leaf)

    ir_status = Counter(n.semantic_status for n in leaves)
    gate_decisions = Counter()
    gate_reasons = Counter()
    incomplete_causes = Counter()
    incomplete_units = []

    for leaf in leaves:
        if leaf.semantic_status != "ready":
            probs = _ir_problems(leaf)
            for p in probs:
                incomplete_causes[p] += 1
            incomplete_units.append({
                "unit_id": leaf.unit_id,
                "qtype": leaf.original_question_type,
                "causes": probs,
            })
            continue
        # find parent root for evaluate()
        root = next(
            (r for r in ir.units
             if r.unit_id == leaf.unit_id or leaf.unit_id.startswith(r.unit_id + ".")),
            None,
        )
        if root is None:
            gate_decisions["no_root"] += 1
            continue
        d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
        dec = d.get("decision") or "?"
        gate_decisions[dec] += 1
        for r in (d.get("reasons") or [])[:3]:
            key = r.split(":")[0][:60]
            if dec != "auto_approve":
                gate_reasons[key] += 1

    # unresolved refs
    unres = Counter()
    for u in run.unresolved_references:
        unres[f"{u.role}:{u.resolution_status}"] += 1

    # spans by role
    spans = Counter(s.role for s in run.resolved_spans)

    return {
        "paper": path.parent.name,
        "units": len(m.units),
        "leaves": len(leaves),
        "ir_status": dict(ir_status),
        "gate_decisions": dict(gate_decisions),
        "incomplete_causes": dict(incomplete_causes),
        "incomplete_units": incomplete_units,
        "unresolved_refs": dict(unres),
        "resolved_spans_by_role": dict(spans),
        "gate_reasons": dict(gate_reasons),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    papers = [measure_paper(p) for p in find_manifests(CORPUS)]

    tot_units = sum(p["units"] for p in papers)
    tot_leaves = sum(p["leaves"] for p in papers)
    ir_total = Counter()
    gate_total = Counter()
    cause_total = Counter()
    unres_total = Counter()
    spans_total = Counter()
    for p in papers:
        ir_total.update(p["ir_status"])
        gate_total.update(p["gate_decisions"])
        cause_total.update(p["incomplete_causes"])
        unres_total.update(p["unresolved_refs"])
        spans_total.update(p["resolved_spans_by_role"])

    report = {
        "cut": "Phase 1 E2E Replay (post 873a343+7c2e51a+7c9b8aa)",
        "baseline_note": (
            "in-memory Native path: manifest→adapter→resolver→IR→compile→gate. "
            "Question/QuestionInstance materialization requires Admission approve() + DB; "
            "candidates below = IR-ready leaves that entered Gate."
        ),
        "papers": len(papers),
        "units": tot_units,
        "leaves": tot_leaves,
        "funnel": {
            "ir_status": dict(ir_total),
            "gate_decisions": dict(gate_total),
            "would_be_candidates": sum(gate_total.values()),
            "auto_approve": gate_total.get("auto_approve", 0),
            "pending_review": gate_total.get("pending_review", 0),
            "rejected": gate_total.get("rejected", 0),
        },
        "incomplete_causes": dict(cause_total),
        "unresolved_refs": dict(unres_total),
        "resolved_spans_by_role": dict(spans_total),
        "per_paper": [
            {
                "paper": p["paper"],
                "units": p["units"],
                "leaves": p["leaves"],
                "ir_status": p["ir_status"],
                "gate_decisions": p["gate_decisions"],
                "incomplete": p["incomplete_units"],
            }
            for p in papers
        ],
    }

    out = OUT / "phase1_e2e_replay.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"papers={report['papers']} units={tot_units} leaves={tot_leaves}")
    print(f"IR: {dict(ir_total)}")
    print(f"Gate: {dict(gate_total)}")
    print(f"would_be_candidates={report['funnel']['would_be_candidates']} "
          f"auto={report['funnel']['auto_approve']} "
          f"pending={report['funnel']['pending_review']} "
          f"rejected={report['funnel']['rejected']}")
    print(f"incomplete causes: {dict(cause_total)}")
    print(f"unresolved refs: {dict(unres_total)}")
    print(f"spans: {dict(spans_total)}")
    print(f"wrote {out}")

    # per-paper compact
    print("\nper-paper IR/gate:")
    for p in papers:
        print(f"  {p['paper']:8} units={p['units']:3} leaves={p['leaves']:3} "
              f"IR={p['ir_status']} gate={p['gate_decisions']}")


if __name__ == "__main__":
    main()
