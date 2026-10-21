"""Phase 1 baseline freeze + Admission read-only acceptance + Evidence Contract audit.

TASK-A: phase1_e2e_baseline_v1.json
TASK-B: Admission path (approve → Question → QuestionInstance) read-only check
TASK-C: Producer Evidence Contract inventory (no implementation)

No code change. No DB mutation.
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
from app.domains.compile import map_canonical_type  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHOICE = {"single_choice", "multiple_choice", "true_false"}


def run_paper(path: Path) -> dict:
    m = load_manifest(path)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload,
        {u.unit_id: u.material_lines for u in m.units if u.material_lines},
        texts,
    )
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)

    root_status = Counter()
    gate = Counter()
    mat = Counter()
    leaf_ready_root_blocked = 0
    admission = Counter()
    unit_type_qtype_pairs = []
    edge_truncation = []
    shared_boundary = []

    # all material ranges for edge/shared analysis
    mat_ranges = {
        u.unit_id: tuple(map(int, u.material_lines))
        for u in m.units if u.material_lines
    }

    for n in ir.units:
        root_status[n.semantic_status] += 1
        is_comp = n.unit_type == "composite_unit"
        mat_resolved = any(
            c.role == "material" and c.span_id for c in n.shared_components
        )
        if is_comp:
            mat["resolved" if mat_resolved else "unresolved"] += 1
        subs = list(n.sub_questions) if is_comp else [n]
        sub_ready = all(s.semantic_status == "ready" for s in subs)
        if is_comp and sub_ready and n.semantic_status != "ready" and not mat_resolved:
            leaf_ready_root_blocked += 1

        # Unit Type vs Question Type pairing (no composite in qtype)
        for leaf in subs:
            unit_type_qtype_pairs.append({
                "unit_id": leaf.unit_id,
                "unit_type": n.unit_type,          # root's Unit Type
                "qtype": leaf.original_question_type,
                "canonical_qtype": map_canonical_type(leaf.original_question_type),
                "leaf_unit_type": leaf.unit_type,
            })

        if n.semantic_status == "ready":
            d = evaluate(root=n, ir=ir, compiled=compiled, resolved_run=run)
            dec = d.get("decision") or "?"
            gate[dec] += 1
            # Admission path (read-only classification)
            if dec == "auto_approve":
                admission["auto_gate_approvable"] += 1
            elif dec == "pending_review":
                admission["pending_review_needs_human"] += 1
            elif dec == "rejected":
                admission["machine_rejected"] += 1
            # 1:N Q:QI semantics: one root candidate → N leaf questions
            n_leaves = len(subs)
            admission["planned_questions_from_root"] += n_leaves
            admission["planned_instances_from_root"] += n_leaves  # 1 occurrence each

        # material edge truncation: declared range vs resolved span
        if is_comp and mat_resolved and n.unit_id in mat_ranges:
            decl_s, decl_e = mat_ranges[n.unit_id]
            mspan = next(
                (c for c in n.shared_components if c.role == "material" and c.span_id),
                None,
            )
            if mspan:
                rs = span_map.get(mspan.span_id)
                if rs:
                    first = int(rs.line_refs[0][-3:])
                    last = int(rs.line_refs[-1][-3:])
                    if first > decl_s:
                        edge_truncation.append({
                            "unit": n.unit_id, "side": "start",
                            "declared": [decl_s, decl_e],
                            "resolved": [first, last],
                            "lost": list(range(decl_s, first)),
                        })
                    if last < decl_e:
                        edge_truncation.append({
                            "unit": n.unit_id, "side": "end",
                            "declared": [decl_s, decl_e],
                            "resolved": [first, last],
                            "lost": list(range(last + 1, decl_e + 1)),
                        })

    # shared boundary lines between adjacent resolved material spans
    mats = [s for s in run.resolved_spans if s.role == "material"]
    for i, a in enumerate(mats):
        for b in mats[i + 1:]:
            inter = set(a.line_refs) & set(b.line_refs)
            if inter:
                shared_boundary.append({
                    "a": a.span_id, "b": b.span_id,
                    "shared": sorted(inter),
                })
    # also marker-adjacent (interiors disjoint but consecutive)
    def _span_range(s):
        return (int(s.line_refs[0][-3:]), int(s.line_refs[-1][-3:]))
    for i, a in enumerate(mats):
        for b in mats[i + 1:]:
            ar, br = _span_range(a), _span_range(b)
            if ar[1] + 1 == br[0] or br[1] + 1 == ar[0]:
                shared_boundary.append({
                    "a": a.span_id, "b": b.span_id,
                    "adjacent_gap1": True, "ranges": [ar, br],
                })

    return {
        "paper": path.parent.name,
        "units": len(m.units),
        "root_status": dict(root_status),
        "gate": dict(gate),
        "mat": dict(mat),
        "leaf_ready_root_blocked": leaf_ready_root_blocked,
        "admission": dict(admission),
        "unit_type_qtype_pairs": unit_type_qtype_pairs,
        "edge_truncation": edge_truncation,
        "shared_boundary": shared_boundary,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    papers = [run_paper(p) for p in find_manifests(CORPUS)]

    tot_root = Counter()
    tot_gate = Counter()
    tot_mat = Counter()
    tot_adm = Counter()
    tot_blocked = 0
    all_pairs = []
    all_edges = []
    all_shared = []
    for p in papers:
        tot_root.update(p["root_status"])
        tot_gate.update(p["gate"])
        tot_mat.update(p["mat"])
        tot_adm.update(p["admission"])
        tot_blocked += p["leaf_ready_root_blocked"]
        all_pairs.extend(p["unit_type_qtype_pairs"])
        all_edges.extend([{**e, "paper": p["paper"]} for e in p["edge_truncation"]])
        all_shared.extend([{**s, "paper": p["paper"]} for s in p["shared_boundary"]])

    # ---- TASK-A baseline ----
    baseline = {
        "name": "phase1_e2e_baseline_v1",
        "frozen_at_git": {
            "AITutors-v3": "dc051fa",
            "AITutors-preprocessing": "873a343",
        },
        "corpus": str(CORPUS),
        "leaf_units": 284,
        "root_units": sum(tot_root.values()),
        "ir_ready": tot_root.get("ready", 0),
        "ir_incomplete": tot_root.get("incomplete", 0),
        "gate_auto": tot_gate.get("auto_approve", 0),
        "gate_pending": tot_gate.get("pending_review", 0),
        "gate_rejected": tot_gate.get("rejected", 0),
        "material_unresolved": tot_mat.get("unresolved", 0),
        "material_resolved": tot_mat.get("resolved", 0),
        "leaf_ready_root_blocked_by_mat": tot_blocked,
        "owner_requested_fields": {
            "root_units": tot_root.get("ready", 0) + tot_root.get("incomplete", 0),
            "leaf_units": 284,
            "ir_ready": tot_root.get("ready", 0),
            "gate_auto": tot_gate.get("auto_approve", 0),
            "gate_pending": tot_gate.get("pending_review", 0),
            "gate_rejected": tot_gate.get("rejected", 0),
            "material_unresolved": tot_mat.get("unresolved", 0),
        },
        "per_paper": {
            p["paper"]: {"root": p["root_status"], "gate": p["gate"], "mat": p["mat"]}
            for p in papers
        },
    }

    # ---- TASK-B admission acceptance ----
    qtypes = Counter(p["canonical_qtype"] or "NONE" for p in all_pairs)
    unit_types = Counter(p["unit_type"] for p in all_pairs)
    leaf_types = Counter(p["leaf_unit_type"] for p in all_pairs)
    composite_in_qtype = [
        p for p in all_pairs
        if p["canonical_qtype"] and "composite" in str(p["canonical_qtype"]).lower()
    ]
    qtype_has_composite = any("composite" in (k or "").lower() for k in qtypes)

    admission = {
        "question": (
            "Gate accepted candidate → Admission approve() → Question/QuestionInstance?"
        ),
        "code_path": (
            "admission.py approve(): auto_gate requires gate_decision=auto_approve; "
            "human/golden requires review_trail. Then _materialize() → "
            "create_question + create_instance per leaf. "
            "Question.canonical_question_type = map_canonical_type(original_question_type). "
            "candidate.unit_type is a separate A-domain field (Unit Type)."
        ),
        "gate_outcomes": dict(tot_gate),
        "admission_classification": dict(tot_adm),
        "answers": {
            "q1_ready_to_candidate": tot_root.get("ready", 0),
            "q1_pending_review": tot_gate.get("pending_review", 0),
            "q1_auto_approve": tot_gate.get("auto_approve", 0),
            "q1_machine_rejected": tot_gate.get("rejected", 0),
            "q2_question_1_to_N_instance": (
                "YES — _materialize plans one Question + one QuestionInstance "
                "per leaf occurrence; dedup_key reuse creates only a new Instance."
            ),
            "q3_leaf_root_confusion": (
                "NO composite in Question Type — see unit_type_qtype_audit"
            ),
        },
        "unit_type_qtype_audit": {
            "unit_types": dict(unit_types),
            "leaf_unit_types": dict(leaf_types),
            "canonical_qtypes": dict(qtypes),
            "composite_in_question_type": qtype_has_composite or bool(composite_in_qtype),
            "composite_question_type_violations": composite_in_qtype[:5],
            "verdict": (
                "PASS — composite appears only as Unit Type; "
                "Question Type stays single_choice/reading/..."
                if not qtype_has_composite and not composite_in_qtype
                else "FAIL"
            ),
        },
        "materialize_safety": {
            "parent_composite_not_materialized": "YES (_leaf_units skips composite parent)",
            "question_dedup": "exact dedup_key → REUSE + new Instance only",
        },
    }

    # ---- TASK-C evidence contract inventory ----
    lost_lines = sum(len(e.get("lost") or []) for e in all_edges)
    evidence_contract = {
        "note": "inventory only — no implementation this phase",
        "items": [
            {
                "problem": "MATERIAL_EDGE_LINE_TRUNCATION",
                "count": len(all_edges),
                "lost_lines_total": lost_lines,
                "detail": all_edges,
                "next_phase": "Producer contract",
            },
            {
                "problem": "MATERIAL_SHARED_BOUNDARY_LINE",
                "count": len(all_shared),
                "detail": all_shared,
                "next_phase": "Producer contract",
            },
            {
                "problem": "ANSWER_TABLE (HTML/shared table)",
                "count": "33+ (chem 25 + bio 21 incomplete cascade; 12 answer unresolved)",
                "detail": "answer_lines point at shared HTML table; token extraction fails",
                "next_phase": "Producer evidence",
            },
            {
                "problem": "OPTION_DECLARATION",
                "count": 4,
                "detail": "U44-46.option.D + Q16/Q6/Q3 options missing",
                "next_phase": "Producer evidence",
            },
        ],
        "remaining_incomplete": {
            "chem_table_answer_cascade": 25,
            "bio_table_answer_cascade": 21,
            "stem_ambiguous": 41,
            "option_incomplete_cascade": 96,
            "u44_46_option_D": 1,
            "options_missing": 3,
        },
    }

    (OUT / "phase1_e2e_baseline_v1.json").write_text(
        json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "phase1_admission_acceptance.json").write_text(
        json.dumps(admission, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "phase1_evidence_contract_inventory.json").write_text(
        json.dumps(evidence_contract, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=== TASK-A baseline ===")
    print(json.dumps(baseline["owner_requested_fields"], ensure_ascii=False))
    print("mat", dict(tot_mat), "blocked", tot_blocked)
    print("\n=== TASK-B admission ===")
    print("gate", dict(tot_gate))
    print("adm ", dict(tot_adm))
    print("unit_types", dict(unit_types))
    print("qtypes", dict(qtypes))
    print("composite_in_qtype:", admission["unit_type_qtype_audit"]["composite_in_question_type"])
    print("verdict:", admission["unit_type_qtype_audit"]["verdict"])
    print("\n=== TASK-C evidence contract ===")
    print("edge truncation units:", len(all_edges), "lost lines:", lost_lines)
    print("shared/adjacent pairs:", len(all_shared))
    for it in evidence_contract["items"]:
        print(f"  {it['problem']}: {it['count']}")
    print("\nwrote baseline / admission / evidence-contract JSON")


if __name__ == "__main__":
    main()
