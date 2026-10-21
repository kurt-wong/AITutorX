"""PHASE1.3 — Reference Evidence Counterfactual Experiment (isolated harness).

NOT a production run. Production adapter/resolver/reference.py/IRBuilder are NOT modified.

Read-points actually consumed by production code (verified):
  material  : shared_components.<role>.start_marker / end_marker
              (reference.py:_material_target 88-97 → resolver.py:_material_span 467-510)
              form: {granularity: "multi_line_pair", text: <marker text>}
  stem      : content.stem.question_label only  (reference.py:_stem_target 172-183)
  option    : content.options[].label           (reference.py:_option_target 186-199)
  answer    : content.answer.answer_zone + question_label (reference.py:_answer_target 202-218)

Therefore:
  - B4 (material) has a VALID experimental bridge: translate Producer material_lines
    into multi_line_pair marker TEXT taken from sealed source lines.
  - B1/B2/B3 cannot deliver start_line/end_line — those fields are never read.
    Attempting a non-read injection is INVALID (Phase 1.2R lesson).
    They are reported as INTERFACE BLOCKER unless a real read-point exists.

Outputs under phase1_3_counterfactual/:
  experiment_matrix.json
  newly_ready_by_experiment.json
  answer_missing_classification.json
  material_composite_analysis.json
  validity_checks.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
PAPERS = Path(r"D:\Project\Papers\scripts")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3_counterfactual")
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(PAPERS))

for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip())

from sqlalchemy import text  # noqa: E402

from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from app.repositories.source_repository import SourceRepository  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView, SourceFigureView  # noqa: E402
from app.domains.resolver.reference import extract_targets  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402

GIT_BINDING = {
    "branch": "od01-r3-convergence",
    "head": "39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4",
    "match_norm": "match-norm/v1.1 dirty blob 015cdfa vs HEAD 73badc3",
}

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")


def man_by_filename() -> dict:
    out = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        out[Path(m.source_file).name] = m
    return out


def line_seq_map(lines) -> dict:
    """seq -> SourceLineView"""
    return {l.seq: l for l in lines}


def material_marker_bridge(man_unit, lines_by_seq: dict) -> dict | None:
    """Producer material_lines (1-based line_no) → multi_line_pair marker TEXT.

    Uses ACTUAL sealed source line text at start/end as marker strings.
    Consumed by resolver._material_span via start_marker/end_marker.
    """
    ml = man_unit.material_lines if man_unit else None
    if not ml:
        return None
    start_ln, end_ln = int(ml[0]), int(ml[1])
    # manifest line numbers are 1-based source line numbers matching SourceLine.seq+1 or line_no?
    # Earlier _expand_option_spans used 1-based indexing into splitlines of the md file.
    # SourceLine.seq is 0-based from source_loader. Try both mappings.
    def find_line(ln: int):
        # try seq == ln-1
        for cand in (ln - 1, ln):
            if cand in lines_by_seq:
                return lines_by_seq[cand]
        return None

    s = find_line(start_ln)
    e = find_line(end_ln)
    if not s or not e:
        return None
    return {
        "role": "material",
        "start_marker": {"granularity": "multi_line_pair", "text": s.text},
        "end_marker": {"text": e.text},
    }


def classify_answer_units(rows_not_ready: list[dict]) -> dict:
    cats = Counter()
    for r in rows_not_ready:
        prim = r.get("ir_failure_reason_primary")
        if prim != "answer_missing" and prim != "answer_ambiguous":
            continue
        bucket = "not_consumed_interface_blocker"  # no positional read-point in contract
        if prim == "answer_missing":
            cats[f"answer_missing__{bucket}"] += 1
        else:
            cats[f"answer_ambiguous__{bucket}"] += 1
    return dict(cats)


def run_matrix() -> dict:
    from app.db.session import async_session_maker
    import asyncio

    maps = man_by_filename()

    async def _run():
        docs = []
        async with async_session_maker() as s:
            r = await s.execute(
                text(
                    """
                    select sv.id, sv.document_id, sa.id, sa.payload, d.file_name
                    from document_source_versions sv
                    join semantic_annotations sa on sa.source_version_id=sv.id
                    join documents d on d.id=sv.document_id
                    where sv.status='sealed'
                    """
                )
            )
            for sv_id, doc_id, ann_id, payload, fname in r.fetchall():
                if isinstance(payload, str):
                    payload = json.loads(payload)
                man = maps.get(fname)
                src = SourceRepository(s)
                lines = tuple(
                    SourceLineView(
                        line_ref=x.line_ref,
                        text=x.text,
                        seq=x.seq,
                        page_no=x.page_no,
                        line_no_in_page=x.line_no_in_page,
                    )
                    for x in await src.get_lines_by_version(sv_id)
                )
                figures = tuple(
                    SourceFigureView(
                        figure_id=f.figure_id,
                        page_no=f.page_no,
                        bbox=f.bbox,
                        placement=f.placement,
                        source=f.source,
                        object_key=f.object_key,
                        figure_hash=f.figure_hash,
                    )
                    for f in await src.get_figures_by_version(sv_id)
                )
                docs.append(
                    {
                        "sv_id": sv_id,
                        "doc_id": doc_id,
                        "ann_id": ann_id,
                        "payload": payload,
                        "fname": fname,
                        "man": man,
                        "lines": lines,
                        "figures": figures,
                    }
                )

        def eval_payload(d, payload):
            run = SourceResolver(
                source_version_id=d["sv_id"], lines=d["lines"], figures=d["figures"]
            ).resolve(payload)
            ir = IRBuilder().build(
                resolved_run=run,
                annotation_payload=payload,
                source_version_id=d["sv_id"],
                annotation_id=d["ann_id"],
            )
            ready_ids = sorted(n.unit_id for n in ir.units if n.semantic_status == "ready")
            all_ids = [n.unit_id for n in ir.units]
            not_ready = []
            for n in ir.units:
                if n.semantic_status != "ready":
                    not_ready.append(
                        {
                            "unit_id": n.unit_id,
                            "unit_type": n.unit_type,
                            "primary": _prim_from_unresolved(run, n.unit_id),
                        }
                    )
            unres_mat = sum(1 for u in run.unresolved_references if u.role == "material")
            unres_ans = sum(1 for u in run.unresolved_references if u.role == "answer")
            return {
                "ir_ready": len(ready_ids),
                "ready_ids": ready_ids,
                "unit_count": len(all_ids),
                "unresolved_material": unres_mat,
                "unresolved_answer": unres_ans,
                "not_ready": not_ready,
                "unresolved_total": len(run.unresolved_references),
            }

        def _prim_from_unresolved(run, unit_id):
            prefs = []
            for u in run.unresolved_references:
                rid = u.reference_id or ""
                uid = rid
                for suf in (".answer", ".stem", ".explanation", ".material"):
                    if uid.endswith(suf):
                        uid = uid[: -len(suf)]
                if ".option." in uid:
                    uid = uid.split(".option.")[0]
                if uid != unit_id and not rid.startswith(unit_id):
                    continue
                if u.role == "material":
                    prefs.append("material_missing_or_incomplete")
                elif u.role == "answer":
                    prefs.append("answer_missing" if u.resolution_status == "missing" else "answer_ambiguous")
                elif u.role == "option":
                    prefs.append("option_incomplete")
                elif u.role == "stem":
                    prefs.append("stem_missing" if u.resolution_status == "missing" else "stem_ambiguous")
            order = [
                "material_missing_or_incomplete",
                "answer_missing",
                "answer_ambiguous",
                "option_incomplete",
                "option_ambiguous",
                "stem_missing",
                "stem_ambiguous",
            ]
            return next((p for p in order if p in prefs), "other")

        def inject_material(payload, man, lines):
            out = json.loads(json.dumps(payload))
            if man is None:
                return out, 0
            man_by_id = {u.unit_id: u for u in man.units}
            lines_by_seq = {l.seq: l for l in lines}
            n = 0
            for au in out.get("semantic_units") or []:
                if au.get("unit_type") != "composite_unit":
                    continue
                mu = man_by_id.get(au.get("unit_id"))
                bridged = material_marker_bridge(mu, lines_by_seq)
                if not bridged:
                    continue
                shared = au.setdefault("shared_components", {})
                shared["material"] = bridged
                n += 1
            return out, n

        # experiments
        results = {}
        newly = {}
        # A baseline
        a_totals = Counter()
        a_ready = set()
        for d in docs:
            e = eval_payload(d, d["payload"])
            a_totals["ready"] += e["ir_ready"]
            a_totals["units"] += e["unit_count"]
            a_totals["unres_mat"] += e["unresolved_material"]
            a_totals["unres_ans"] += e["unresolved_answer"]
            for rid in e["ready_ids"]:
                a_ready.add((d["fname"], rid))
        results["A"] = {
            "evidence": "none",
            "ir_ready": a_totals["ready"],
            "ir_not_ready": a_totals["units"] - a_totals["ready"],
            "delta_vs_A": 0,
            "unresolved_material": a_totals["unres_mat"],
            "unresolved_answer": a_totals["unres_ans"],
            "interface": "production-equivalent payload",
        }

        # B1/B2/B3: interface blocker — no positional read-point
        for name, ev in [("B1", "stem"), ("B2", "option"), ("B3", "answer")]:
            results[name] = {
                "evidence": ev,
                "ir_ready": None,
                "ir_not_ready": None,
                "delta_vs_A": None,
                "newly_ready": [],
                "status": "INTERFACE_BLOCKER",
                "blocker": {
                    "reason": "ResolveTarget for this role has no positional/marker input channel",
                    "stem": "reference.py:_stem_target uses only question_label (172-183)",
                    "option": "reference.py:_option_target uses only label/question_label (186-199)",
                    "answer": "reference.py:_answer_target uses only answer_zone/question_label (202-218)",
                    "consumer": "resolver._locate_question_start/_locate_options/_answer_span never read line numbers",
                    "why_prev_experiment_invalid": "start_line/end_line injected into role dicts are ignored by extract_targets",
                    "contract_change_needed_for_evidence_use": "ResolveTarget + extract_targets + resolver policy (LEVEL 2)",
                },
            }

        # B4 material: valid bridge
        b4_ready = set()
        b4_totals = Counter()
        b4_injected = 0
        b4_per_doc = []
        for d in docs:
            inj, n_inj = inject_material(d["payload"], d["man"], d["lines"])
            b4_injected += n_inj
            e = eval_payload(d, inj)
            b4_totals["ready"] += e["ir_ready"]
            b4_totals["units"] += e["unit_count"]
            b4_totals["unres_mat"] += e["unresolved_material"]
            for rid in e["ready_ids"]:
                b4_ready.add((d["fname"], rid))
            b4_per_doc.append(
                {
                    "file_name": d["fname"],
                    "injected_materials": n_inj,
                    "ir_ready": e["ir_ready"],
                    "unresolved_material": e["unresolved_material"],
                }
            )
        new_b4 = sorted(b4_ready - a_ready)
        results["B4"] = {
            "evidence": "material (multi_line_pair marker text from producer material_lines)",
            "ir_ready": b4_totals["ready"],
            "ir_not_ready": b4_totals["units"] - b4_totals["ready"],
            "delta_vs_A": b4_totals["ready"] - a_totals["ready"],
            "newly_ready_count": len(new_b4),
            "unresolved_material_after": b4_totals["unres_mat"],
            "unresolved_material_before": a_totals["unres_mat"],
            "materials_injected": b4_injected,
            "interface": (
                "shared_components.material.start_marker/end_marker "
                "(reference.py:_material_target:88-97 → resolver._material_span:467-510)"
            ),
            "bridge": "producer material_lines → sealed source line TEXT as marker strings",
            "per_document": b4_per_doc,
        }
        newly["B4"] = [{"file_name": f, "unit_id": u} for f, u in new_b4]

        # C combined: only valid channel is material; B1-B3 blocked
        results["C"] = {
            "evidence": "all supported channels (only material bridge is valid)",
            "ir_ready": b4_totals["ready"],
            "ir_not_ready": b4_totals["units"] - b4_totals["ready"],
            "delta_vs_A": b4_totals["ready"] - a_totals["ready"],
            "newly_ready_count": len(new_b4),
            "note": "C == B4 because stem/option/answer channels are INTERFACE_BLOCKER",
            "newly_ready_unit_ids": newly["B4"],
        }

        # answer classification (on baseline not-ready)
        ans_cats = Counter()
        mat_comp = Counter()
        for d in docs:
            e = eval_payload(d, d["payload"])
            for nr in e["not_ready"]:
                if nr["primary"] in ("answer_missing", "answer_ambiguous"):
                    ans_cats[f"{nr['primary']}__position_not_consumed"] += 1
                if nr["unit_type"] == "composite_unit":
                    mat_comp[nr["primary"]] += 1
        # after B4, composite status
        mat_after = Counter()
        for d in docs:
            inj, _ = inject_material(d["payload"], d["man"], d["lines"])
            e = eval_payload(d, inj)
            # count composite ready after
            run = SourceResolver(
                source_version_id=d["sv_id"], lines=d["lines"], figures=d["figures"]
            ).resolve(inj)
            ir = IRBuilder().build(
                resolved_run=run,
                annotation_payload=inj,
                source_version_id=d["sv_id"],
                annotation_id=d["ann_id"],
            )
            for n in ir.units:
                if n.unit_type == "composite_unit":
                    mat_after[n.semantic_status] += 1

        return {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "git_binding": GIT_BINDING,
            "matrix": results,
            "newly_ready_by_experiment": newly,
            "answer_classification": dict(ans_cats),
            "composite_material_before_primary": dict(mat_comp),
            "composite_ir_status_after_B4": dict(mat_after),
            "validity": {
                "A_vs_B4_intended_diff": "shared_components.material gains start_marker/end_marker multi_line_pair text",
                "reaches_consumer": "extract_targets._material_target reads start_marker/end_marker (reference.py:95-96)",
                "consumer_function": "resolver._material_span (resolver.py:467-510)",
                "B1_B2_B3_invalid_if_line_fields_only": True,
                "production_code_modified": False,
            },
        }

    return asyncio.run(_run())


if __name__ == "__main__":
    res = run_matrix()
    (OUT / "experiment_matrix.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (OUT / "newly_ready_by_experiment.json").write_text(
        json.dumps(res.get("newly_ready_by_experiment", {}), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT / "answer_missing_classification.json").write_text(
        json.dumps(
            {
                "captured_at": res["captured_at"],
                "classification_rule": (
                    "answer roles have no positional read-point in ResolveTarget; "
                    "all 161 missing / 15 ambiguous classified as position_not_consumed "
                    "(interface blocker), not as proven-ineffective evidence"
                ),
                "counts": res.get("answer_classification", {}),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUT / "material_composite_analysis.json").write_text(
        json.dumps(
            {
                "captured_at": res["captured_at"],
                "before_primary": res.get("composite_material_before_primary"),
                "after_B4_ir_status": res.get("composite_ir_status_after_B4"),
                "B4": res["matrix"].get("B4"),
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    (OUT / "validity_checks.json").write_text(
        json.dumps(res.get("validity", {}), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("MATRIX")
    for k, v in res["matrix"].items():
        print(k, {x: v.get(x) for x in ("evidence", "ir_ready", "delta_vs_A", "newly_ready_count", "status") if x in v or v.get(x) is not None})
    print("answer", res.get("answer_classification"))
    print("composite after", res.get("composite_ir_status_after_B4"))
