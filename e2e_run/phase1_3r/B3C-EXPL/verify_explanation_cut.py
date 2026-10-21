"""Verify the explanation-boundary cut (d831d3f) independently.

MIMO claims on 历史 (53 units):
  explanation max span   353 -> 11
  exp spans swallowing another unit's answer row   53/53 -> 0/53
  Q1.explanation   P1L640..P1L1045 -> P1L639..P1L641
  Q2.explanation                  -> P1L645..P1L649
  U52: answer P1L1007..1015 ∩ explanation P1L1017..1023 = empty
  Gate: auto_approve 1->1, candidates 144->144, enter=0 leave=0
  B3c-A: Q27.answer P1L593..P1L623 n=31 unchanged

Also tests the two ROOT-CAUSE claims:
  (1) "line 715 break eaten by line 710 continue (dead code)"
  (2) "question_label missing -> qn=None -> owned filter disabled"

And re-measures answer∩explanation under BOTH semantics:
  span-level (resolved spans) and region-level (_compute_regions).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")
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
from app.domains.resolver import resolver as rm  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

_ORIG_EXPL = SourceResolver._explanation_span


def _pre_fix_expl(self, out, unit_id, t):
    """Reproduce the PRE-fix control flow verbatim (original lines 704-731)."""
    qn = t.question_number
    header_seen = False
    region: list[str] = []
    for l in self._idx.lines:
        norm = rm.normalize_text(l.text)
        if is_expl(norm):
            header_seen = True
            continue
        if not header_seen:
            continue
        if is_expl(norm) or is_ans(norm):
            break
        region.append(l.line_ref)
    if not header_seen:
        out.add_unresolved(t, "missing", ("no header",))
        return
    if not region:
        out.add_unresolved(t, "missing", ("empty region",))
        return
    owned = [
        r for r in region
        if qn is None or rm.is_question_start(rm.normalize_text(self._idx.get(r).text)) == qn
    ]
    if not owned:
        out.add_unresolved(t, "missing", (f"no row for qn={qn}",))
        return
    out.add_span(unit_id, t, owned, "exact", ("explanation", f"qn={qn}"))


is_expl = rm.is_explanation_header
is_ans = rm.is_answer_header


def _views(srs):
    return tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )


def measure(path: Path, mode: str) -> dict:
    m = load_manifest(path)
    srs = load_source_lines(Path(m.source_file))
    views = _views(srs)
    tb = {s.line_ref: s.text for s in srs}
    payload = manifest_to_annotation_payload(m)
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)

    ans = {s.span_id: s for s in run.resolved_spans if s.role == "answer"}
    expl = {s.span_id: s for s in run.resolved_spans if s.role == "explanation"}

    # per-unit explanation/answer table
    units = sorted({sid[3:].rsplit(".explanation", 1)[0] for sid in expl})
    rows = []
    swallow = 0
    for uid in units:
        e = expl[f"sp-{uid}.explanation"]
        a = ans.get(f"sp-{uid}.answer")
        # any OTHER unit's answer row inside this explanation span?
        others = [
            aid for aid in ans
            if not aid.startswith(f"sp-{uid}.")
            and (set(ans[aid].line_refs) & set(e.line_refs))
        ]
        if others:
            swallow += 1
        rows.append({
            "unit_id": uid,
            "explanation_n": len(e.line_refs),
            "explanation_first": e.line_refs[0] if e.line_refs else None,
            "explanation_last": e.line_refs[-1] if e.line_refs else None,
            "answer_refs": list(a.line_refs) if a else None,
            "swallows_other_answers": len(others),
        })

    expl_ns = [r["explanation_n"] for r in rows]

    # region-level collision (independent of spans)
    regions = run.structural_regions
    region_refs = {r.role: set(r.line_refs) for r in regions}
    reg_coll = sum(
        1 for uid in units
        if ans.get(f"sp-{uid}.answer")
        and (set(ans[f"sp-{uid}.answer"].line_refs) & region_refs.get("explanation", set()))
    )

    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)
    gate = Counter()
    for root in ir.units:
        if root.semantic_status != "ready":
            continue
        d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
        gate[d.get("decision") or "?"] += 1

    return {
        "paper": path.parent.name,
        "mode": mode,
        "units": len(m.units),
        "expl_spans": len(expl),
        "expl_max": max(expl_ns) if expl_ns else 0,
        "expl_mean": round(sum(expl_ns) / len(expl_ns), 2) if expl_ns else 0,
        "swallow_units": swallow,
        "ans_expl_span_pairs": sum(
            1 for a in ans.values() for e in expl.values()
            if set(a.line_refs) & set(e.line_refs)
        ),
        "ans_expl_region_collision_units": reg_coll,
        "gate": dict(gate),
        "ir_status": dict(Counter(n.semantic_status for n in ir.units)),
        "rows": rows,
        "region_refs_n": {k: len(v) for k, v in region_refs.items()},
        "tb": tb if path.parent.name == "历史" else None,
    }


def main() -> None:
    manifests = list(find_manifests(CORPUS))
    res = {"AFTER": [], "PRE": []}
    for p in manifests:
        res["AFTER"].append(measure(p, "AFTER"))
    SourceResolver._explanation_span = _pre_fix_expl
    try:
        for p in manifests:
            res["PRE"].append(measure(p, "PRE"))
    finally:
        SourceResolver._explanation_span = _ORIG_EXPL

    summary = {}
    for mode in ("PRE", "AFTER"):
        rs = res[mode]
        summary[mode] = {
            "expl_spans": sum(r["expl_spans"] for r in rs),
            "expl_max": max(r["expl_max"] for r in rs),
            "swallow_units": sum(r["swallow_units"] for r in rs),
            "ans_expl_span_pairs": sum(r["ans_expl_span_pairs"] for r in rs),
            "ans_expl_region_collision_units": sum(r["ans_expl_region_collision_units"] for r in rs),
            "gate": dict(sum((Counter(r["gate"]) for r in rs), Counter())),
            "ir_status": dict(sum((Counter(r["ir_status"]) for r in rs), Counter())),
        }

    hist_after = next(r for r in res["AFTER"] if r["paper"] == "历史")
    hist_pre = next(r for r in res["PRE"] if r["paper"] == "历史")
    q1a = next((r for r in hist_after["rows"] if r["unit_id"] == "Q1"), None)
    q1p = next((r for r in hist_pre["rows"] if r["unit_id"] == "Q1"), None)
    q2a = next((r for r in hist_after["rows"] if r["unit_id"] == "Q2"), None)
    u52 = next((r for r in hist_after["rows"] if r["unit_id"] == "U52"), None)

    report = {
        "summary": summary,
        "history": {
            "pre": {k: hist_pre[k] for k in
                    ("expl_spans", "expl_max", "swallow_units", "ans_expl_span_pairs",
                     "ans_expl_region_collision_units", "gate", "region_refs_n")},
            "after": {k: hist_after[k] for k in
                      ("expl_spans", "expl_max", "swallow_units", "ans_expl_span_pairs",
                       "ans_expl_region_collision_units", "gate", "region_refs_n")},
            "Q1_pre": q1p, "Q1_after": q1a, "Q2_after": q2a, "U52_after": u52,
            "expl_mean_after": hist_after["expl_mean"],
        },
        "per_paper": res,
    }
    (OUT / "explanation_cut_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    for mode in ("PRE", "AFTER"):
        s = summary[mode]
        print(f"=== {mode} ===")
        print("  expl spans        :", s["expl_spans"])
        print("  expl max span     :", s["expl_max"])
        print("  swallow units     :", s["swallow_units"])
        print("  ans∩expl pairs    :", s["ans_expl_span_pairs"])
        print("  ans∩expl region   :", s["ans_expl_region_collision_units"])
        print("  gate              :", s["gate"])
        print("  ir_status         :", s["ir_status"])
        print()
    print("history PRE  :", json.dumps(report["history"]["pre"], ensure_ascii=False))
    print("history AFTER:", json.dumps(report["history"]["after"], ensure_ascii=False))
    print("Q1 pre   :", q1p["explanation_first"], "..", q1p["explanation_last"], q1p["explanation_n"])
    print("Q1 after :", q1a["explanation_first"], "..", q1a["explanation_last"], q1a["explanation_n"])
    print("Q2 after :", q2a["explanation_first"], "..", q2a["explanation_last"], q2a["explanation_n"])
    print("U52 after:", json.dumps(u52, ensure_ascii=False))


if __name__ == "__main__":
    main()
