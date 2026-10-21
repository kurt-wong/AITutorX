"""B3c-A Answer Evidence Transport Repair — acceptance measurement.

Owner acceptance criterion (NOT "BARE 23→0"):
    Producer answer_lines  →  Resolver ResolvedSpan.line_refs
    position binding must be correct.

Also recomputes the 284-unit / 9-paper funnel after the transport fix.

Zero semantic invention: we only compare declared range to resolved span.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-A")
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.reference import extract_targets  # noqa: E402
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


def _to_views(source_lines):
    return tuple(
        SourceLineView(
            line_ref=sl.line_ref,
            text=sl.text,
            seq=sl.seq,
            page_no=sl.page_no,
            line_no_in_page=sl.line_no_in_page,
        )
        for sl in source_lines
    )


def _refs_for_declared(s: int, e: int) -> list[str]:
    return [f"P1L{n:03d}" for n in range(s, e + 1)]


def _answer_value_state(text: str) -> str:
    if not text or not text.strip():
        return "EMPTY"
    t = text.strip()
    # strip leading qn token like "27." / "1."
    import re

    t2 = re.sub(r"^\s*[0-9]{1,3}\s*[.．、:)]*\s*", "", t).strip()
    if not t2:
        return "BARE_QUESTION_NUMBER"
    return "HAS_VALUE"


def measure_paper(path: Path) -> dict:
    manifest = load_manifest(path)
    source_path = Path(manifest.source_file)
    source_lines = load_source_lines(source_path)
    views = _to_views(source_lines)

    payload = manifest_to_annotation_payload(manifest)
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)

    spans = {s.span_id: s for s in run.resolved_spans}
    unresolved = {u.reference_id: u for u in run.unresolved_references}
    targets = extract_targets(payload)
    ans_targets = [t for t in targets if t.role == "answer"]

    # map unit_id → declared answer_lines from payload (transport proof)
    declared_by_unit: dict[str, tuple[int, int] | None] = {}
    for unit in payload.get("semantic_units") or []:
        if unit.get("unit_type") == "composite_unit":
            for sub in unit.get("sub_questions") or []:
                sid = sub.get("unit_id") or f"{unit.get('unit_id')}.sub"
                ans = (sub.get("content") or {}).get("answer") or {}
                al = ans.get("answer_lines")
                declared_by_unit[sid] = tuple(al) if al else None
        else:
            ans = (unit.get("content") or {}).get("answer") or {}
            al = ans.get("answer_lines")
            declared_by_unit[unit.get("unit_id")] = tuple(al) if al else None

    binding_rows = []
    for t in ans_targets:
        declared = t.evidence_lines
        span = spans.get(f"sp-{t.target_id}")
        unres = unresolved.get(t.target_id)
        row = {
            "unit_id": t.unit_id,
            "target_id": t.target_id,
            "declared_answer_lines": list(declared) if declared else None,
            "transport_emitted": declared_by_unit.get(t.unit_id) is not None,
            "resolved": span is not None,
            "resolution_status": (
                span.resolution_status if span else (unres.resolution_status if unres else None)
            ),
        }
        if span is not None:
            row["resolved_line_refs"] = list(span.line_refs)
            row["resolved_start_end"] = [span.start_line_ref, span.end_line_ref]
            row["granularity"] = span.granularity
            # binding correctness
            if declared is not None:
                expected = _refs_for_declared(declared[0], declared[1])
                row["binding_match"] = list(span.line_refs) == expected
                row["binding_mode"] = (
                    "multi_line_full_range" if declared[1] > declared[0]
                    else "single_line"
                )
                # single-line may be char-slice on that line → still match if
                # line_refs == [declared line]
                if declared[1] == declared[0]:
                    row["binding_match"] = list(span.line_refs) == expected
            else:
                row["binding_match"] = None
                row["binding_mode"] = "no_declared_range"
        else:
            row["resolved_line_refs"] = []
            row["binding_match"] = False if declared is not None else None
        binding_rows.append(row)

    # IR + gate funnel (same as Track A)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)

    ir_status = Counter(n.semantic_status for n in ir.units)
    gate_decisions = Counter()
    for root in ir.units:
        if root.semantic_status != "ready":
            continue
        d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
        gate_decisions[d.get("decision") or "?"] += 1

    return {
        "paper": path.parent.name + "/" + path.name,
        "source_file": str(source_path),
        "units": len(manifest.units),
        "payload_units": len(payload.get("semantic_units") or []),
        "binding_rows": binding_rows,
        "ir_status": dict(ir_status),
        "gate_decisions": dict(gate_decisions),
    }


def main() -> None:
    manifests = find_manifests(CORPUS)
    papers = [measure_paper(p) for p in manifests]

    all_rows = [r for p in papers for r in p["binding_rows"]]
    with_declared = [r for r in all_rows if r["declared_answer_lines"] is not None]
    multi = [r for r in with_declared if r["declared_answer_lines"][1] > r["declared_answer_lines"][0]]
    single = [r for r in with_declared if r["declared_answer_lines"][1] == r["declared_answer_lines"][0]]

    def _match_rate(rows):
        if not rows:
            return None
        ok = sum(1 for r in rows if r.get("binding_match"))
        return {"n": len(rows), "match": ok, "rate": ok / len(rows)}

    ir_total = Counter()
    gate_total = Counter()
    for p in papers:
        ir_total.update(p["ir_status"])
        gate_total.update(p["gate_decisions"])

    # Q27 sample (math)
    q27 = next(
        (r for r in all_rows if r["unit_id"] == "Q27" and r["declared_answer_lines"] == [593, 623]),
        next((r for r in all_rows if r["unit_id"] == "Q27"), None),
    )

    report = {
        "cut": "B3C-A Answer Evidence Transport Repair",
        "acceptance": (
            "Producer answer_lines → Resolver ResolvedSpan.line_refs position binding; "
            "NOT BARE→0"
        ),
        "corpus": str(CORPUS),
        "papers": len(papers),
        "units": sum(p["units"] for p in papers),
        "answer_targets": len(all_rows),
        "with_declared_answer_lines": len(with_declared),
        "transport_emitted": sum(1 for r in all_rows if r["transport_emitted"]),
        "binding": {
            "multi_line": _match_rate(multi),
            "single_line": _match_rate(single),
            "all_declared": _match_rate(with_declared),
        },
        "resolution_status": dict(Counter(r["resolution_status"] for r in all_rows)),
        "binding_mode": dict(Counter(r.get("binding_mode") for r in all_rows)),
        "q27_sample": q27,
        "funnel": {
            "ir_status": dict(ir_total),
            "gate_decisions": dict(gate_total),
        },
        "per_paper": [
            {
                "paper": p["paper"],
                "units": p["units"],
                "ir_status": p["ir_status"],
                "gate_decisions": p["gate_decisions"],
                "binding_rows": len(p["binding_rows"]),
                "binding_match": sum(1 for r in p["binding_rows"] if r.get("binding_match")),
            }
            for p in papers
        ],
        "rows": all_rows,
    }

    out_path = OUT / "b3ca_transport_measure.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out_path)
    print("units", report["units"], "answer_targets", report["answer_targets"])
    print("transport_emitted", report["transport_emitted"])
    print("binding multi", report["binding"]["multi_line"])
    print("binding single", report["binding"]["single_line"])
    print("binding all", report["binding"]["all_declared"])
    print("ir", report["funnel"]["ir_status"])
    print("gate", report["funnel"]["gate_decisions"])
    if q27:
        print("Q27 declared", q27.get("declared_answer_lines"),
              "resolved", q27.get("resolved_line_refs"),
              "match", q27.get("binding_match"))


if __name__ == "__main__":
    main()
