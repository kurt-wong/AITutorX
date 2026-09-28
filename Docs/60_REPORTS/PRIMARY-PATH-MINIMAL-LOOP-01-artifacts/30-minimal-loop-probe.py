"""Endpoint probe: with per-label option spans, does a choice unit pass the Gate?

READ-ONLY. Uses the scratch copy of the V3 backend; the real repo is untouched.
No DB, no LLM: manifest -> payload -> ResolvedRun -> IR -> Compiler -> gate.evaluate.
"""
import re
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutor-X\_audit_scratch\backend")
sys.path.insert(0, str(BACKEND))

from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.runner_b2 import _build_resolved_run  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.span import ResolvedRun, ResolvedSpan  # noqa: E402
from app.domains.gate import STRICT_AUTO_TYPES  # noqa: E402

# resolver/reference.py:69-75 — the frozen option-label line grammar.
_OPT = re.compile(r"^([A-Z])\s*[.．、):）]")
_OPT_PAREN = re.compile(r"^[（(]([A-Z])[)）]")


def option_label_of(text: str):
    s = text.strip()
    m = _OPT.match(s) or _OPT_PAREN.match(s)
    return m.group(1) if m else None


def add_option_content(payload, manifest, lines) -> int:
    """Inject content['options'] per-label (the adapter deliberately omits it)."""
    units = {u.unit_id: u for u in manifest.units}
    added = 0

    def fill(uid, content):
        nonlocal added
        u = units.get(uid.rsplit(".sub", 1)[0])
        if u is None or not u.options_lines or not isinstance(content, dict):
            return
        ql = str(u.question_numbers[0]) if u.question_numbers else None
        opts = []
        for ln in range(u.options_lines[0], u.options_lines[1] + 1):
            if 1 <= ln <= len(lines):
                lab = option_label_of(lines[ln - 1].text)
                if lab:
                    opts.append({"label": lab, "role": "option", "question_label": ql})
        if opts:
            content["options"] = opts
            added += len(opts)

    for su in payload.get("semantic_units", []):
        fill(su["unit_id"], su.get("content"))
        for sub in su.get("sub_questions", []) or []:
            fill(sub["unit_id"], sub.get("content"))
    return added


MANIFEST = Path(
    r"D:\Project\AITutor-X\FORMAL-E2E-04-evidence"
    r"\consumer_input_identity_ok\2018北京夏季高中会考历史（教师版）(1).manifest.json"
)


def with_option_spans(run: ResolvedRun, manifest, lines, sv_id):
    """Add per-label option spans alongside the existing region span."""
    span_map = {s.span_id: s for s in run.resolved_spans}
    units = {u.unit_id: u for u in manifest.units}
    added = 0
    for uid in {s.span_id[3:-5] for s in run.resolved_spans if s.span_id.endswith(".stem")}:
        u = units.get(uid.rsplit(".sub", 1)[0])
        if u is None or not u.options_lines:
            continue
        start, end = u.options_lines
        for ln in range(start, end + 1):
            if not (1 <= ln <= len(lines)):
                continue
            lab = option_label_of(lines[ln - 1].text)
            if not lab:
                continue
            sid = f"sp-{uid}.option.{lab}"
            if sid in span_map:
                continue
            ref = f"P1L{ln:03d}"
            span_map[sid] = ResolvedSpan(
                span_id=sid, source_version_id=sv_id, role="option",
                start_line_ref=ref, end_line_ref=ref, line_refs=(ref,),
                granularity="line", start_offset=None, end_offset=None,
                text_hash=lines[ln - 1].line_hash, resolution_status="exact",
                evidence=(),
            )
            added += 1
    return ResolvedRun(source_version_id=run.source_version_id,
                       resolved_spans=tuple(span_map.values())), added


def run_case(manifest, lines, sv_id, patch: bool):
    payload = manifest_to_annotation_payload(manifest)
    if patch:
        add_option_content(payload, manifest, lines)
    run = _build_resolved_run(manifest, lines, sv_id)
    n_opts = 0
    if patch:
        run, n_opts = with_option_spans(run, manifest, lines, sv_id)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {sl.line_ref: sl for sl in lines}
    compiled = Compiler(span_map, line_map).compile(ir)

    ready = [u for u in ir.units if u.semantic_status == "ready"]
    decisions = {}
    for u in ready:
        d = evaluate(root=u, ir=ir, compiled=compiled, resolved_run=run)
        decisions[d.get("decision", "?")] = decisions.get(d.get("decision", "?"), 0) + 1
    return {
        "option_spans": n_opts,
        "total": len(ir.units),
        "ready": len(ready),
        "incomplete": sum(1 for u in ir.units if u.semantic_status == "incomplete"),
        "unknown": sum(1 for u in ir.units if u.semantic_status == "unknown"),
        "decisions": decisions,
        "sample_reasons": _sample(ir, compiled, run, ready),
    }


def _sample(ir, compiled, run, ready):
    """Full gate reasons for every ready unit, grouped."""
    by_reason: dict = {}
    detail = []
    for u in ready:
        d = evaluate(root=u, ir=ir, compiled=compiled, resolved_run=run)
        reasons = tuple(
            (d.get("structural_reasons") or [])
            + (d.get("provenance_reasons") or [])
            + (d.get("semantic_reasons") or [])
            + (d.get("admission_reasons") or [])
        )
        key = (d.get("decision"), reasons[:1])
        by_reason[key] = by_reason.get(key, 0) + 1
        detail.append({
            "unit_id": u.unit_id,
            "type": u.original_question_type,
            "decision": d.get("decision"),
            "reasons": list(reasons)[:2],
        })
    print("     reason groups (decision, first reason) -> count:")
    for (dec, rs), n in sorted(by_reason.items(), key=lambda kv: -kv[1]):
        print(f"       {dec:14} {n:3}  {list(rs)}")
    return detail


def main():
    manifest = load_manifest(MANIFEST)
    lines = load_source_lines(Path(manifest.source_file))
    sv_id = uuid.uuid4()
    print(f"units={len(manifest.units)} lines={len(lines)} "
          f"strict_auto_types={sorted(STRICT_AUTO_TYPES)}\n")

    for patch in (False, True):
        r = run_case(manifest, lines, sv_id, patch)
        tag = "PATCHED " if patch else "BASELINE"
        print(f"[{tag}] option_spans=+{r['option_spans']}  "
              f"ready={r['ready']}/{r['total']} incomplete={r['incomplete']} unknown={r['unknown']}")
        print(f"[{tag}] gate decisions: {r['decisions']}")
        for s in r["sample_reasons"]:
            print(f"          {s['unit_id']} ({s['type']}) -> {s['decision']} {s['reasons']}")
        print()


if __name__ == "__main__":
    main()
