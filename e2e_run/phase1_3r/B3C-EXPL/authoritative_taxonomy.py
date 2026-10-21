"""Read-only: ONE authoritative taxonomy with root/leaf scopes stated explicitly.

Everything computed in a single pass so root-level and leaf-level counts can never
drift between scripts. Two scopes are reported side by side:
  ROOT scope : top-level IR unit (what Gate/Admission see)
  LEAF scope : standalone unit or composite sub_question (what spans attach to)

Populations:
  eligible_table   : root/leaf has an answer span carrying structured_answer_table
  auto             : Gate decision == auto_approve
  not_auto         : eligible_table and not auto
  gate_pending     : Gate decision == pending_review (all ready roots)
  gate_rejected    : Gate decision == rejected
Blockers are attributed from IR invariants + Gate reasons, no inference.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile import content_roles_for, map_canonical_type  # noqa: E402
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


def leaf_gap(s):
    """Named IR blockers on one leaf."""
    probs = []
    canon = map_canonical_type(s.original_question_type)
    req = content_roles_for(canon)
    by = {c.role: c for c in s.content}
    if req.get("stem") == "required":
        c = by.get("stem")
        if c is None:
            probs.append("stem_not_declared")
        elif c.span_id is None:
            probs.append("stem_unresolved")
    if req.get("answer") == "required":
        c = by.get("answer")
        if c is None:
            probs.append("answer_not_declared")
        elif c.span_id is None:
            probs.append("answer_unresolved")
    if req.get("options") == "required_for_choice":
        if not any(c.role == "option" for c in s.content):
            probs.append("options_missing")
    for c in s.content:
        if c.role in ("stem", "answer", "option"):
            continue
        if c.span_id is None:
            probs.append(f"{c.role}_unresolved")
    return probs


def gate_kinds(reasons):
    ks = set()
    for r in reasons or ():
        if "role provenance violation" in r:
            ks.add("provenance_role_region")
        elif "not byte-proven" in r:
            ks.add("span_resolution_not_exact")
        elif "not strict-auto" in r:
            ks.add("qtype_not_strict_auto")
        elif "not expressible" in r:
            ks.add("answer_grammar_not_expressible")
        elif "not source_located+complete" in r:
            ks.add("answer_not_source_located")
    return ks


def main() -> None:
    R = Counter()   # root scope
    L = Counter()   # leaf scope
    ir_gap = Counter()
    gate_kind = Counter()
    detail = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid, aid = uuid.uuid4(), uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, aid)
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {l.line_ref: l for l in srs}).compile(ir)

        table_leaves = {s.span_id[3:].rsplit(".answer", 1)[0]
                        for s in run.resolved_spans
                        if "structured_answer_table" in " ".join(s.evidence or ())}
        R["units_total"] = len(ir.units)
        for root in ir.units:
            leaves = list(root.sub_questions) if root.unit_type == "composite_unit" else [root]
            L["leaves_total"] += len(leaves)
            ready = root.semantic_status == "ready"
            R["ready" if ready else "incomplete"] += 1
            if not ready:
                for s in leaves:
                    for g in leaf_gap(s):
                        ir_gap[g] += 1
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            d = g.get("decision")
            R[f"gate_{d}"] += 1
            ks = gate_kinds(g.get("reasons"))
            for k in ks:
                gate_kind[k] += 1
            owner_ids = {root.unit_id, *(s.unit_id for s in root.sub_questions)}
            has_tbl = any(lv in table_leaves for lv in owner_ids)
            if has_tbl:
                R["eligible_table"] += 1
                if d == "auto_approve":
                    R["eligible_auto"] += 1
                else:
                    R["eligible_not_auto"] += 1
                    R[f"eligible_not_auto_{d}"] += 1
                    detail.append({"paper": p.parent.name, "root": root.unit_id,
                                   "decision": d, "gate_kinds": sorted(ks)})
        for lv in table_leaves:
            L["eligible_table"] += 1

    print("=== ROOT SCOPE (what Gate/Admission see) ===")
    for k in ("units_total", "ready", "incomplete", "gate_auto_approve",
              "gate_pending_review", "gate_rejected", "eligible_table",
              "eligible_auto", "eligible_not_auto",
              "eligible_not_auto_pending_review", "eligible_not_auto_rejected"):
        print(f"   {k:<38} {R.get(k,0)}")
    print("\n=== LEAF SCOPE (what spans attach to) ===")
    for k in ("leaves_total", "eligible_table"):
        print(f"   {k:<38} {L.get(k,0)}")

    print("\n=== IR blockers, LEAF scope (IR-incomplete units only) ===")
    for k, v in ir_gap.most_common():
        print(f"   {v:>5}  {k}")

    print("\n=== Gate blockers, ROOT scope (deduped per root, may co-occur) ===")
    for k, v in gate_kind.most_common():
        print(f"   {v:>5}  {k}")

    print("\n=== eligible-but-not-auto: composition of blockers ===")
    comp = Counter()
    for d in detail:
        if d["decision"] == "pending_review" and not d["gate_kinds"]:
            comp["pending_no_named_reason"] += 1
        for k in d["gate_kinds"]:
            comp[f"only_or_with:{k}"] += 1
    for k, v in comp.most_common():
        print(f"   {v:>5}  {k}")

    (OUT / "authoritative_taxonomy.json").write_text(
        json.dumps({"root_scope": dict(R), "leaf_scope": dict(L),
                    "ir_blockers_leaf": dict(ir_gap),
                    "gate_blockers_root": dict(gate_kind),
                    "eligible_not_auto_detail": detail},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'authoritative_taxonomy.json'}")


if __name__ == "__main__":
    main()
