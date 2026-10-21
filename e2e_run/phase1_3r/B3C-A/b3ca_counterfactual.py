"""B3c-A counterfactual: same corpus/resolver, evidence_lines disabled.

Simulates pre-B3c-A behaviour exactly (the fallback answer_zone scan is still in
the code) by force-returning None from _answer_span's evidence_lines read.

Measures, for BOTH modes:
  - IR semantic_status census
  - gate decision census
  - answer spans overlapping the explanation region  (role provenance violation)
  - answer spans overlapping material regions
  - answer refs vs explanation refs collisions (line level)

This is the control the MIMO report does not contain.
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

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver import resolver as resolver_mod  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

_ORIG_ANSWER_SPAN = SourceResolver._answer_span


def _patched_off(self, out, unit_id, t):
    """Force the pre-B3c-A path: pretend nothing was declared."""
    object.__setattr__(t, "evidence_lines", None)
    return _ORIG_ANSWER_SPAN(self, out, unit_id, t)


def _run_one(path: Path, mode: str) -> dict:
    manifest = load_manifest(path)
    source_lines = load_source_lines(Path(manifest.source_file))
    views = tuple(
        SourceLineView(line_ref=sl.line_ref, text=sl.text, seq=sl.seq,
                       page_no=sl.page_no, line_no_in_page=sl.line_no_in_page)
        for sl in source_lines
    )
    payload = manifest_to_annotation_payload(manifest)
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)

    ans = [s for s in run.resolved_spans if s.role == "answer"]
    expl = [s for s in run.resolved_spans if s.role == "explanation"]
    mats = [s for s in run.resolved_spans
            if s.role in ("material", "shared_material", "instruction")]
    ans_expl = sum(1 for a in ans for e in expl if set(a.line_refs) & set(e.line_refs))
    ans_mat = sum(1 for a in ans for m in mats if set(a.line_refs) & set(m.line_refs))
    ans_ans = 0
    for i in range(len(ans)):
        for j in range(i + 1, len(ans)):
            if set(ans[i].line_refs) & set(ans[j].line_refs):
                ans_ans += 1

    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)
    ir_status = Counter(n.semantic_status for n in ir.units)
    gate = Counter()
    for root in ir.units:
        if root.semantic_status != "ready":
            continue
        d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
        gate[d.get("decision") or "?"] += 1

    return {
        "paper": path.parent.name,
        "mode": mode,
        "ir_status": dict(ir_status),
        "gate": dict(gate),
        "answer_spans": len(ans),
        "answer_span_status": dict(Counter(s.resolution_status for s in ans)),
        "answer_granularity": dict(Counter(s.granularity for s in ans)),
        "ans_expl_collisions": ans_expl,
        "ans_mat_collisions": ans_mat,
        "ans_ans_collisions": ans_ans,
        "unresolved_roles": dict(Counter(u.role for u in run.unresolved_references)),
    }


def main() -> None:
    manifests = list(find_manifests(CORPUS))
    results = {"ON": [], "OFF": []}

    # mode ON (real B3c-A)
    for p in manifests:
        results["ON"].append(_run_one(p, "ON"))

    # mode OFF (pre-B3c-A)
    SourceResolver._answer_span = _patched_off
    try:
        for p in manifests:
            results["OFF"].append(_run_one(p, "OFF"))
    finally:
        SourceResolver._answer_span = _ORIG_ANSWER_SPAN

    summary = {}
    for mode in ("ON", "OFF"):
        rs = results[mode]
        summary[mode] = {
            "ir_status": dict(sum((Counter(r["ir_status"]) for r in rs), Counter())),
            "gate": dict(sum((Counter(r["gate"]) for r in rs), Counter())),
            "answer_spans": sum(r["answer_spans"] for r in rs),
            "answer_span_status": dict(sum((Counter(r["answer_span_status"]) for r in rs), Counter())),
            "answer_granularity": dict(sum((Counter(r["answer_granularity"]) for r in rs), Counter())),
            "ans_expl_collisions": sum(r["ans_expl_collisions"] for r in rs),
            "ans_mat_collisions": sum(r["ans_mat_collisions"] for r in rs),
            "ans_ans_collisions": sum(r["ans_ans_collisions"] for r in rs),
            "unresolved_roles": dict(sum((Counter(r["unresolved_roles"]) for r in rs), Counter())),
        }

    report = {"corpus": str(CORPUS), "summary": summary, "per_paper": results}
    (OUT / "b3ca_counterfactual.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for mode in ("ON", "OFF"):
        s = summary[mode]
        label = "B3c-A ON (real)" if mode == "ON" else "B3c-A OFF (pre-fix)"
        print(f"=== {label} ===")
        print("  ir_status           :", s["ir_status"])
        print("  gate                :", s["gate"])
        print("  answer spans        :", s["answer_spans"], s["answer_span_status"])
        print("  answer granularity  :", s["answer_granularity"])
        print("  ans∩explanation     :", s["ans_expl_collisions"])
        print("  ans∩material        :", s["ans_mat_collisions"])
        print("  ans∩ans             :", s["ans_ans_collisions"])
        print("  unresolved roles    :", s["unresolved_roles"])
        print()


if __name__ == "__main__":
    main()
