"""Task B interface inspection + Task E census of 50 decoded-but-not-auto.

Read-only. Official口径:
  B3c-B eligible 126 = root auto (from table) + 50 decoded-but-not-auto
  50 = IR incomplete + Gate pending + Gate rejected
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
from app.domains.resolver.resolver import (  # noqa: E402
    SourceResolver,
    decode_answer_table_cell,
)
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


def leaf_blockers(leaf, span_map) -> list[str]:
    """Read-point blockers from IR content roles (not guesses)."""
    out = []
    for c in leaf.content:
        if c.unsupported:
            out.append(f"unsupported:{c.role}")
        elif c.span_id is None:
            out.append(f"{c.role}:unresolved")
        elif c.span_id not in span_map:
            out.append(f"{c.role}:span_missing")
    if not any(c.role == "option" for c in leaf.content):
        qt = leaf.original_question_type or ""
        if qt in {"single_choice", "multiple_choice", "true_false"}:
            out.append("options:missing")
    return out


def main() -> None:
    decoded_not_auto = []
    auto_from_table = []
    eligible = 0
    tot = Counter()

    for p in find_manifests(CORPUS):
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
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)

        # map leaf_id -> compiled leaf
        c_by_id = {l.unit_id: l for l in compiled.leaves}

        for root in ir.units:
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            # did any leaf decode a table answer?
            decoded_leaves = []
            for leaf in leaves:
                ans = next((c for c in leaf.content if c.role == "answer"), None)
                if ans is None or ans.span_id is None:
                    continue
                span = span_map.get(ans.span_id)
                if not span or not span.line_refs:
                    continue
                raw = line_map[span.line_refs[0]].text
                if "<td" not in raw.lower():
                    continue
                qn = leaf.question_number or ""
                cell = decode_answer_table_cell(raw, qn)
                if cell is None:
                    tot["table_decode_failed"] += 1
                    continue
                eligible += 1
                decoded_leaves.append((leaf, cell, span, raw))

            if not decoded_leaves:
                continue

            # root-level gate
            if root.semantic_status != "ready":
                blockers = []
                for leaf, cell, span, raw in decoded_leaves:
                    blockers.extend(leaf_blockers(leaf, span_map))
                # also shared material
                for sc in root.shared_components:
                    if sc.span_id is None:
                        blockers.append(f"shared:{sc.role}:unresolved")
                decoded_not_auto.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "root_unit_type": root.unit_type,
                    "bucket": "IR_incomplete",
                    "qn": decoded_leaves[0][0].question_number,
                    "cell": decoded_leaves[0][1][2],
                    "answer_span": decoded_leaves[0][2].span_id,
                    "answer_evidence": list(decoded_leaves[0][2].evidence),
                    "blockers": sorted(set(blockers)),
                    "gate": None,
                })
                tot["bucket_IR_incomplete"] += 1
                continue

            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            dec = d.get("decision") or "?"
            if dec == "auto_approve":
                auto_from_table.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "qn": decoded_leaves[0][0].question_number,
                    "cell": decoded_leaves[0][1][2],
                })
                tot["bucket_auto"] += 1
            else:
                # Gate-only blockers from reasons
                reasons = d.get("reasons") or []
                blockers = []
                for leaf, cell, span, raw in decoded_leaves:
                    blockers.extend(leaf_blockers(leaf, span_map))
                decoded_not_auto.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "root_unit_type": root.unit_type,
                    "bucket": f"Gate_{dec}",
                    "qn": decoded_leaves[0][0].question_number,
                    "cell": decoded_leaves[0][1][2],
                    "answer_span": decoded_leaves[0][2].span_id,
                    "answer_evidence": list(decoded_leaves[0][2].evidence),
                    "blockers": sorted(set(blockers)) or ["gate_only"],
                    "gate_reasons": [r[:80] for r in reasons[:6]],
                    "gate": dec,
                })
                tot[f"bucket_Gate_{dec}"] += 1

    # Task B inspection: can inclusive end be expressed?
    task_b = {
        "question": "inclusive final material line expressible in current contract?",
        "mechanism": (
            "annotation_adapter.material_boundary_markers → "
            "resolver._material_span multi_line_pair; interior = strictly "
            "between start_marker and end_marker (exclusive of both markers)."
        ),
        "constraint": (
            "Last content line L502 can only enter the interior if end_marker "
            "is at L503+. Within neighbour scope (next_start=504) the only "
            "candidates are L503 (blank, not unique) and L504 (duplicate "
            "header, not unique). Unique-text marker requirement + exclusive "
            "interior + neighbour scope make inclusive-end unexpressible."
        ),
        "verdict": "INTERFACE_GAP",
        "minimal_contract_change": (
            "Either (1) allow end_marker to be the declared material end line "
            "itself with interior including that line (inclusive-end form), or "
            "(2) accept a non-unique positional marker at the hard scope "
            "boundary. Both are schema/contract changes beyond this task."
        ),
        "affected_files": [
            "backend/scripts/preprocessing_consumer/annotation_adapter.py",
            "backend/app/domains/resolver/resolver.py (_material_span)",
        ],
        "do_not": "weaken _enforce_material_overlap / invent neighbour guessing",
    }

    # blocker rollup for the 50
    blocker_c = Counter()
    for row in decoded_not_auto:
        for b in row["blockers"]:
            key = b.split(":")[0]
            blocker_c[key] += 1
        if not row["blockers"]:
            blocker_c["gate_only"] += 1

    report = {
        "official_scale": {
            "B3c_B_eligible": eligible,
            "root_auto_from_table": len(auto_from_table),
            "decoded_but_not_auto": len(decoded_not_auto),
        },
        "buckets": {k: v for k, v in tot.items() if k.startswith("bucket_")},
        "blocker_role_counts": dict(blocker_c),
        "decoded_but_not_auto": decoded_not_auto,
        "auto_from_table_sample": auto_from_table[:20],
        "auto_from_table_total": len(auto_from_table),
        "task_b_interface": task_b,
    }
    out = OUT / "phase14_census_and_gap.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("official", report["official_scale"])
    print("buckets", report["buckets"])
    print("blocker roles", dict(blocker_c))
    print("task_B", task_b["verdict"])
    print("wrote", out)


if __name__ == "__main__":
    main()
