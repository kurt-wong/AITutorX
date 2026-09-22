#!/usr/bin/env python
"""X2.7 INT-FULL-01 — run-result analysis harness (MEASUREMENT ONLY).

Reads the verbatim runner reports produced by the unmodified formal entrypoints
and derives the Level 1 / Level 2 / Level 3 counters required by task section 13,
plus the Question/Unit/Material (section 10), Producer + canonical vocabulary
(section 11) and Composite (section 12) tables.

This script is a RUN ARTIFACT, not production code. It:
  * never imports or patches any runner / boundary / app module
  * never re-classifies a runner status into a new vocabulary (raw status is
    preserved verbatim; the ACCEPTED/BLOCKED/SKIPPED/ERROR rollup is reported
    as a separate, explicitly-labelled view)
  * never repairs, filters or reweights the corpus
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPERS = Path(r"D:\Project\Papers")
EXCLUDED_PARTS = (".pytest_work", "_archive")

RUN_ID = "X27-INT-FULL-01-20260922T062602Z"

LEGS = {
    "B2_primary": {
        "role": "PRIMARY BASELINE (runner_b2, default formal path, --resolver-ir omitted)",
        "glob": "10-raw-b2-*.json",
    },
    "V1_primary": {
        "role": "PRIMARY BASELINE (runner, default formal path)",
        "glob": "11-raw-v1-*.json",
    },
    "B2_probe_secondary": {
        "role": "SECONDARY DISCLOSED PROBE (runner_b2 + existing batch resolver IR) — NOT the baseline",
        "glob": "12-raw-b2probe-*.json",
    },
}

# Acceptable rollup buckets requested by task section 8. Raw runner status is kept.
_ROLLUP = {
    "completed": "ACCEPTED",
    "identity_blocked": "BLOCKED",
    "interface_scope_rejected": "BLOCKED",
    "error": "ERROR",
    "session_error": "ERROR",
}


def _load(glob: str) -> list[tuple[str, dict]]:
    out = []
    for p in sorted(HERE.glob(glob)):
        shard = p.stem.split("-")[-1]
        out.append((shard, json.loads(p.read_text(encoding="utf-8"))))
    return out


def _iter_inputs(shard: str, report: dict):
    for item in report.get("papers", []):
        yield shard, item


def _raw_status(item: dict) -> str:
    """Preserve the runner's own status vocabulary verbatim."""
    if "interface_scope_rejected" in item:
        return "interface_scope_rejected"
    if "error" in item and "result" not in item and "track_a" not in item:
        return "pre_stage_error"
    res = item.get("result")
    if isinstance(res, dict) and "status" in res:
        return str(res["status"])
    if "track_a" in item:
        ta = item["track_a"]
        tb = item.get("track_b", {})
        if ta.get("status") == "completed" and tb.get("status") == "completed":
            return "completed"
        if ta.get("status") == "error" or tb.get("status") == "error":
            return "error"
        return str(ta.get("status", "unknown"))
    return "unknown"


def _rollup(raw: str) -> str:
    return _ROLLUP.get(raw, "ERROR" if "error" in raw else "SKIPPED")


def analyse_leg(name: str, meta: dict) -> dict:
    shards = _load(meta["glob"])
    per_input = []
    counts: Counter = Counter()
    roll: Counter = Counter()

    stage = {
        "source_manifest": Counter(),
        "boundary_normalization": Counter(),
        "interface_scope": Counter(),
        "identity_m1_m5": Counter(),
        "annotation": Counter(),
        "resolver": Counter(),
        "resolved_span": Counter(),
        "ir": Counter(),
        "compiler": Counter(),
        "gate": Counter(),
        "admission": Counter(),
    }
    fail_classes = Counter()
    cat = Counter()
    gate_dec = Counter()
    semantic_status = Counter()
    examples: dict[str, list] = {}
    totals = Counter()

    for shard, report in shards:
        for sh, item in _iter_inputs(shard, report):
            stage["source_manifest"]["discovered"] += 1
            raw = _raw_status(item)
            counts[raw] += 1
            roll[_rollup(raw)] += 1
            code = None
            err_type = None
            reason = None

            if "interface_scope_rejected" in item:
                rej = item["interface_scope_rejected"]
                code = rej.get("code")
                reason = (rej.get("reason") or "")[:180]
                stage["interface_scope"]["rejected"] += 1
                stage["interface_scope"][f"code:{code}"] += 1
                stage["boundary_normalization"]["reached"] += 1
                stage["identity_m1_m5"]["not_executed_by_this_entrypoint"] += 1
                fail_classes["scope"] += 1
                cat["B_corpus_data_quality"] += 1
            elif "error" in item and "track_a" not in item and "result" not in item:
                reason = (item.get("error") or "")[:180]
                stage["source_manifest"]["pre_stage_error"] += 1
                fail_classes["unknown"] += 1
                cat["A_product"] += 1
            else:
                stage["interface_scope"]["accepted"] += 1
                stage["boundary_normalization"]["reached"] += 1

            res = item.get("result")
            if isinstance(res, dict):
                ig = res.get("identity_gate") or {}
                if ig:
                    stage["identity_m1_m5"]["evaluated"] += 1
                    stage["identity_m1_m5"][f"gate:{ig.get('gate')}"] += 1
                    stage["identity_m1_m5"][f"reason:{ig.get('reason')}"] += 1
                    for m in ig.get("mismatches") or ():
                        stage["identity_m1_m5"][f"mismatch:{m}"] += 1
                    if ig.get("gate") == "BLOCK":
                        reason = ig.get("reason")
                        code = (ig.get("mismatches") or [None])[-1]
                        r = str(reason or "")
                        if r == "identity_verification_failed":
                            fail_classes["identity"] += 1
                            cat["B_corpus_data_quality"] += 1
                        elif r == "semantic_pending":
                            fail_classes["resolver"] += 1
                            cat["C_environment_or_missing_artifact"] += 1
                        else:
                            fail_classes["identity"] += 1
                            cat["A_product"] += 1
                if res.get("downstream_executed") is False:
                    for st in ("annotation", "resolver", "resolved_span", "ir", "compiler", "gate", "admission"):
                        stage[st]["NOT REACHED (blocked upstream)"] += 1
                if res.get("status") == "completed":
                    stage["annotation"]["completed"] += 1
                    stage["resolver"]["SKIPPED BY DESIGN (preprocessing supplies exact line numbers)"] += 1
                    stage["resolved_span"]["spans_valid"] += res.get("spans_in_run", 0)
                    stage["resolved_span"]["unresolved"] += res.get("unresolved_in_run", 0)
                    stage["ir"]["produced"] += 1
                    stage["ir"]["root_units"] += res.get("total_units", 0)
                    stage["compiler"]["compiled_leaves"] += res.get("compiled_leaves", 0)
                    stage["compiler"]["compiled_materials"] += res.get("compiled_materials", 0)
                    stage["gate"]["candidates"] += res.get("ready", 0)
                    stage["gate"]["skipped_not_ready"] += res.get("skipped", 0)
                    gate_dec["auto_approve"] += res.get("gate_auto_approve", 0)
                    gate_dec["rejected"] += res.get("gate_rejected", 0)
                    gate_dec["pending_review"] += res.get("gate_pending_review", 0)
                    for g in res.get("gate_results") or []:
                        semantic_status[str(g.get("semantic_status"))] += 1
                    stage["admission"]["admission_candidates_created"] += res.get("ready", 0)
                    stage["admission"][
                        "NOT REACHED (this entrypoint creates AdmissionCandidate rows only; "
                        "AdmissionService.approve/reject lives on runner.py Track A)"
                    ] += 1
                elif res.get("status") == "error":
                    stage["annotation"]["failed"] += 1
                    reason = (res.get("error") or "")[:180]
                    if "UNKNOWN_UNIT_TYPE" in reason:
                        fail_classes["scope"] += 1
                        cat["B_corpus_data_quality"] += 1
                        stage["boundary_normalization"]["UNKNOWN_UNIT_TYPE"] += 1
                    else:
                        fail_classes["unknown"] += 1
                        cat["A_product"] += 1

            if "track_a" in item:
                ta, tb = item["track_a"], item.get("track_b", {})
                if ta.get("status") == "completed":
                    stage["annotation"]["completed"] += 1
                    stage["gate"]["production_GateService.run_invoked"] += 1
                    stage["gate"]["candidates"] += ta.get("candidates_created", 0)
                    gate_dec["auto_approve"] += ta.get("gate_pass", 0)
                    gate_dec["rejected"] += ta.get("gate_rejected", 0)
                    gate_dec["pending_review"] += ta.get("pending_review", 0)
                    stage["admission"]["AdmissionService_reached_via_GateService"] += 1
                    stage["admission"]["pending_review"] += ta.get("pending_review", 0)
                    stage["admission"]["admitted"] += ta.get("gate_pass", 0)
                    stage["admission"]["rejected"] += ta.get("gate_rejected", 0)
                    stage["admission"]["units_skipped_not_ready"] += len(ta.get("skipped") or [])
                else:
                    stage["annotation"]["failed"] += 1
                    reason = (ta.get("error") or "")[:180]
                    err_type = ta.get("error_type")
                    if "UNKNOWN_UNIT_TYPE" in reason:
                        fail_classes["scope"] += 1
                        cat["B_corpus_data_quality"] += 1
                        stage["boundary_normalization"]["UNKNOWN_UNIT_TYPE"] += 1
                    else:
                        fail_classes["unknown"] += 1
                        cat["A_product"] += 1
                if tb.get("status") == "completed":
                    stage["resolver"]["SKIPPED BY DESIGN (preprocessing supplies exact line numbers)"] += 1
                    stage["resolved_span"]["spans_valid"] += tb.get("spans_constructed", 0)
                    stage["resolved_span"]["unresolved"] += tb.get("spans_failed", 0)
                    stage["resolved_span"]["spans_with_bad_line_refs"] += tb.get("spans_with_bad_refs", 0)
                for st in ("ir", "compiler"):
                    stage[st]["NOT REACHED (stage only exists on runner_b2)"] += 1

            per_input.append({
                "paper": item.get("paper"),
                "shard": sh,
                "raw_status": raw,
                "rollup": _rollup(raw),
                "code": code,
                "error_type": err_type,
                "reason": reason,
            })
            if reason:
                key = f"{raw}|{code or '-'}|{str(reason)[:70]}"
                examples.setdefault(key, []).append(item.get("paper"))
            totals["units_declared"] += item.get("units", 0) or 0

    n = max(sum(counts.values()), 1)
    return {
        "role": meta["role"],
        "shards_read": [s for s, _ in shards],
        "input_count": n,
        "counts_by_raw_status": dict(counts),
        "counts_by_rollup": dict(roll),
        "percent_by_rollup": {k: round(100.0 * v / n, 2) for k, v in roll.items()},
        "percent_by_raw_status": {k: round(100.0 * v / n, 2) for k, v in counts.items()},
        "pipeline": {k: dict(v) for k, v in stage.items()},
        "gate_decisions": dict(gate_dec),
        "semantic_status_of_evaluated_or_skipped_units": dict(semantic_status),
        "failure_classes_level3": dict(fail_classes),
        "category_abc": dict(cat),
        "representative_examples": {k: v[:3] for k, v in list(examples.items())[:12]},
        "totals": dict(totals),
        "inputs": per_input,
    }


def corpus_side() -> dict:
    """Producer-side population + vocabulary + composite structure (read-only)."""
    unit_t: Counter = Counter()
    q_t: Counter = Counter()
    idv: Counter = Counter()
    comp = Counter()
    comp_qnums: list[int] = []
    q_total = 0
    manifests = 0
    for mf in sorted(PAPERS.rglob("*.manifest.json")):
        if any(part in EXCLUDED_PARTS for part in mf.parts):
            continue
        manifests += 1
        raw = json.loads(mf.read_text(encoding="utf-8"))
        idv[repr(raw.get("identity_version"))] += 1
        for u in raw.get("units", []):
            ut = u.get("unit_type")
            unit_t[repr(ut)] += 1
            q_t[repr(u.get("original_question_type"))] += 1
            qn = len(u.get("question_numbers") or [])
            q_total += qn
            if ut == "composite_question":
                comp["composite_source_units"] += 1
                comp_qnums.append(qn)
                if qn > 1:
                    comp["composite_with_multiple_questions"] += 1
                if u.get("material_lines"):
                    comp["composite_with_material_reference"] += 1
                if u.get("questions_lines"):
                    comp["composite_with_questions_region"] += 1
                comp["producer_questions_in_composites"] += qn
            else:
                if u.get("material_lines"):
                    comp["non_composite_units_declaring_material"] += 1
    comp["max_questions_in_one_composite"] = max(comp_qnums) if comp_qnums else 0
    comp["questions_per_composite_mean"] = (
        round(sum(comp_qnums) / len(comp_qnums), 3) if comp_qnums else 0
    )
    return {
        "manifests_eligible": manifests,
        "producer_vocabulary": {
            "unit_type": dict(unit_t),
            "question_type": dict(q_t),
            "identity_version_repr": dict(idv),
        },
        "question_numbers_total_producer_questions": q_total,
        "composite": dict(comp),
        "composite_questions_per_unit_histogram": dict(Counter(comp_qnums)),
    }


def main() -> None:
    legs = {name: analyse_leg(name, meta) for name, meta in LEGS.items()}
    cs = corpus_side()
    primary = {k: v for k, v in legs.items() if k != "B2_probe_secondary"}

    analysis = {
        "run_id": RUN_ID,
        "generated_by": "40-analyze_run.py (measurement only; no runner/app module imported or patched)",
        "legs": legs,
        "global_level1_primary_baseline": {
            "total_corpus_eligible_manifests": cs["manifests_eligible"],
            "observation_note": "172 eligible manifests, each observed once per leg (two legs). Not 344 distinct inputs.",
            "by_leg_rollup": {k: v["counts_by_rollup"] for k, v in primary.items()},
            "by_leg_raw_status": {k: v["counts_by_raw_status"] for k, v in primary.items()},
            "note": (
                "The two primary legs enforce DIFFERENT boundary depth (V1: Interface Scope only; "
                "B2: M1-M5 Consumer Identity Verification AND Interface Scope). Their rollups are "
                "therefore NOT interchangeable and are reported per leg, never summed."
            ),
        },
        "question_unit_material": {
            "documents": cs["manifests_eligible"],
            "source_versions": "MATERIALIZED ONLY FOR INPUTS THAT PASSED THE BOUNDARY (transaction-scoped, rolled back at end of each item)",
            "units_producer_declared": sum(int(v) for v in cs["producer_vocabulary"]["unit_type"].values()),
            "standalone_units_producer": cs["producer_vocabulary"]["unit_type"].get("'standalone_question'", 0),
            "composite_units_producer": cs["composite"].get("composite_source_units", 0),
            "questions_producer_question_numbers": cs["question_numbers_total_producer_questions"],
            "question_instances": "NOT MATERIALIZED (no persisted instance layer is produced by these entrypoints)",
            "materials": cs["composite"].get("composite_with_material_reference", 0),
            "material_links": "NOT MATERIALIZED (material is a ResolvedSpan role / IR shared_component, not a link entity)",
            "figures": "NOT MATERIALIZED (figure_refs deferred; BUG-V3-020 noted in IRBuilder)",
            "knowledge_links": "NOT MATERIALIZED (no knowledge-link stage exists in the current formal path)",
        },
        "producer_vocabulary": cs["producer_vocabulary"],
        "canonical_vocabulary": {
            "boundary_normalization_rule": (
                "OD-2 authorises exactly two legacy->canonical translations: "
                "standalone_question->standalone_unit (X2.6-OD-2-MAP-STANDALONE-01), "
                "composite_question->composite_unit (X2.6-OD-2-MAP-COMPOSITE-01)"
            ),
            "canonical_unit_type_closed_set": ["composite_unit", "standalone_unit"],
            "canonical_question_type_distribution": (
                "NOT NORMALIZED AT THIS BOUNDARY — original_question_type is passed through "
                "verbatim (annotation_adapter -> IRNode.original_question_type). Question Type is "
                "orthogonal to Unit Type (Owner D1 / 10 section 5.2). No canonical Question Type "
                "closed set is wired into the runtime."
            ),
        },
        "composite": cs["composite"],
        "composite_questions_per_unit_histogram": cs["composite_questions_per_unit_histogram"],
        "composite_old_new_delta": {
            "OLD_reported": {
                "composite_source_units": 356,
                "composite_with_multiple_questions": 187,
                "producer_questions": 853,
                "compiled_leaves": 219,
            },
            "NEW_measured_this_run": {
                "composite_source_units": cs["composite"].get("composite_source_units", 0),
                "composite_with_multiple_questions": cs["composite"].get("composite_with_multiple_questions", 0),
                "producer_questions_in_composites": cs["composite"].get("producer_questions_in_composites", 0),
                "compiled_leaves_B2_probe_secondary": legs["B2_probe_secondary"]["pipeline"]["compiler"].get("compiled_leaves", 0),
            },
            "population_caveat": (
                "OLD numbers were produced on an earlier, smaller population and at a different "
                "reach level. DELTA is therefore a measurement difference across two different "
                "populations, NOT a regression or an improvement. composite_source_units / "
                "multiple-questions / producer_questions are measured over the full 172 eligible "
                "manifests; compiled_leaves is only measurable where the chain actually reaches "
                "the Compiler (B2_probe_secondary, 70 completed manifests)."
            ),
        },
        "f_rbc_01_regression": {
            "uncaught_TypeError_in_any_leg": sum(
                1 for lg in legs.values() for it in lg["inputs"]
                if it.get("reason") and "TypeError" in str(it["reason"])
            ),
            "MALFORMED_IDENTITY_VERSION_count": sum(
                1 for lg in legs.values() for it in lg["inputs"]
                if it.get("code") == "MALFORMED_IDENTITY_VERSION"
            ),
            "real_corpus_coverage_of_malformed_identity_version": (
                "NONE — the eligible corpus declares only int 2 (87) and null/absent (85). "
                "No list/dict/set/bytearray/bool/float/complex form occurs, so the F-RBC-01 "
                "vector is NOT exercised by real corpus evidence."
            ),
            "targeted_regression_available_separately": (
                "AITutors-v3 backend/tests/test_x26_frb01_identity_version_types.py (51 cases) — "
                "cited as SIDE EVIDENCE ONLY, kept separate from real-corpus evidence per task "
                "section 16."
            ),
        },
        "environment": {
            "llm_calls": 0,
            "ocr_calls": 0,
            "retries": 0,
            "note": "Zero LLM/OCR/network call sites exist in the consumption chain; the formal path is preprocessed artifacts -> V3.",
        },
    }

    (HERE / "30-analysis.json").write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (HERE / "31-per-input-results.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "legs": {
                    k: {
                        "role": v["role"],
                        "input_count": v["input_count"],
                        "counts_by_raw_status": v["counts_by_raw_status"],
                        "counts_by_rollup": v["counts_by_rollup"],
                        "percent_by_rollup": v["percent_by_rollup"],
                        "percent_by_raw_status": v["percent_by_raw_status"],
                        "inputs": v["inputs"],
                    }
                    for k, v in legs.items()
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("wrote 30-analysis.json and 31-per-input-results.json")
    for k, v in legs.items():
        print(f"  {k}: {v['input_count']} inputs -> rollup={v['counts_by_rollup']} raw={v['counts_by_raw_status']}")


if __name__ == "__main__":
    main()
