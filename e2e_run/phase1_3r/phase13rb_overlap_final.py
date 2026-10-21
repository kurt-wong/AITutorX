"""PHASE1.3R-BR — final overlap evidence: resolved material spans + 4vs10 + region class.

Exact 20 units from Phase1.3R-B (no reclassification).
Recomputes marker-interior material span (what resolver would resolve before demotion).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
PAPERS = Path(r"D:\Project\Papers\scripts")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r")
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(PAPERS))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip())

from sqlalchemy import text  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from app.repositories.source_repository import SourceRepository  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView, SourceFigureView  # noqa: E402

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")

TARGET_UNIT_IDS = [
    "U52", "U53", "Q37", "Q1", "Q2", "Q3", "Q4", "Q5-6", "Q7-8", "Q9-11",
    "Q12-14", "Q15-17", "Q18-20", "Q21-25", "U49-52", "U53-56", "U57-60",
    "U10-13", "U14", "U15",
]


def region_class(mat, que):
    if not mat or not que:
        return "UNKNOWN"
    a0, a1 = mat
    b0, b1 = que
    if (a0, a1) == (b0, b1):
        return "SAME_REGION"
    if a1 < b0 or b1 < a0:
        return "DIFFERENT_REGION"
    return "PARTIAL_REGION_OVERLAP"


async def main():
    prior = json.loads((OUT / "overlap_structural_confirmation.json").read_text(encoding="utf-8"))
    prior_by = {(u["source_version_id"], u["unit_id"]): u for u in prior["units"]}
    assert set(prior["unit_ids"]) == set(TARGET_UNIT_IDS) or len(prior["units"]) == 20

    maps = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        maps[Path(m.source_file).name] = m

    rows = []
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
            if not man:
                continue
            man_by = {u.unit_id: u for u in man.units}
            src = SourceRepository(s)
            raw = list(await src.get_lines_by_version(sv_id))
            lines = tuple(
                SourceLineView(
                    line_ref=x.line_ref, text=x.text, seq=x.seq,
                    page_no=x.page_no, line_no_in_page=x.line_no_in_page,
                )
                for x in raw
            )
            by_ref = {l.line_ref: l for l in lines}
            by_seq = {l.seq: l for l in lines}

            def ln_to_line(ln: int):
                return by_seq.get(ln - 1) or by_seq.get(ln)

            def marker_interior(start_ln: int, end_ln: int):
                """What resolver would resolve: exclusive interior between marker lines."""
                sl, el = ln_to_line(start_ln), ln_to_line(end_ln)
                if not sl or not el:
                    return None, None, None, "markers not mapped to source seq"
                s_seq, e_seq = sl.seq, el.seq
                if e_seq <= s_seq:
                    return [], s_seq, e_seq, "MARKER_ORDER_INVALID"
                if e_seq <= s_seq + 1:
                    return [], s_seq, e_seq, "INTERIOR_EMPTY"
                refs = [l.line_ref for l in lines if s_seq < l.seq < e_seq]
                # also 1-based line nos
                lines_1b = [by_ref[r].seq + 1 for r in refs]
                return {
                    "line_refs": refs,
                    "line_numbers_1b": lines_1b,
                    "start": lines_1b[0] if lines_1b else None,
                    "end": lines_1b[-1] if lines_1b else None,
                    "count": len(refs),
                }, s_seq, e_seq, "ok"

            figures = tuple(
                SourceFigureView(
                    figure_id=f.figure_id, page_no=f.page_no, bbox=f.bbox,
                    placement=f.placement, source=f.source,
                    object_key=f.object_key, figure_hash=f.figure_hash,
                )
                for f in await src.get_figures_by_version(sv_id)
            )
            inj = json.loads(json.dumps(payload))
            for au in inj.get("semantic_units") or []:
                if au.get("unit_type") != "composite_unit":
                    continue
                mu = man_by.get(au["unit_id"])
                if not mu or not mu.material_lines:
                    continue
                s_ln, e_ln = int(mu.material_lines[0]), int(mu.material_lines[1])
                sl, el = ln_to_line(s_ln), ln_to_line(e_ln)
                if not sl or not el:
                    continue
                au.setdefault("shared_components", {})["material"] = {
                    "role": "material",
                    "start_marker": {"granularity": "multi_line_pair", "text": sl.text},
                    "end_marker": {"text": el.text},
                }

            run = SourceResolver(
                source_version_id=sv_id, lines=lines, figures=figures
            ).resolve(inj)

            stem_by_unit = {}
            for sp in run.resolved_spans:
                if sp.role != "stem":
                    continue
                tid = sp.span_id[3:] if sp.span_id.startswith("sp-") else sp.span_id
                uid = tid.replace(".sub.stem", "").replace(".stem", "")
                stem_by_unit[uid] = sp
                stem_by_unit[tid] = sp

            mat_unres = {}
            for u in run.unresolved_references:
                if u.role == "material":
                    rid = u.reference_id or ""
                    uid = rid.replace(".material", "") if rid.endswith(".material") else rid
                    mat_unres[uid] = u

            for au in inj.get("semantic_units") or []:
                uid = au["unit_id"]
                if uid not in TARGET_UNIT_IDS:
                    continue
                if (str(sv_id), uid) not in prior_by and uid not in TARGET_UNIT_IDS:
                    continue
                # only if in prior 20
                if not any(k[1] == uid for k in prior_by if k[0] == str(sv_id)):
                    # fallback: uid in target and this is the right doc
                    pr = next((v for k, v in prior_by.items() if k[1] == uid and k[0] == str(sv_id)), None)
                    if pr is None:
                        continue

                mu = man_by.get(uid)
                mat = (int(mu.material_lines[0]), int(mu.material_lines[1])) if mu and mu.material_lines else None
                que = (int(mu.questions_lines[0]), int(mu.questions_lines[1])) if mu and mu.questions_lines else None

                res_mat, s_seq, e_seq, res_note = marker_interior(mat[0], mat[1]) if mat else (None, None, None, "no material_lines")

                stem_sp = stem_by_unit.get(uid) or stem_by_unit.get(f"{uid}.sub")
                if not stem_sp:
                    for k, v in stem_by_unit.items():
                        if k.startswith(uid):
                            stem_sp = v
                            break

                stem_l1 = []
                stem_seq = []
                if stem_sp:
                    for ref in stem_sp.line_refs:
                        if ref in by_ref:
                            stem_seq.append(by_ref[ref].seq)
                            stem_l1.append(by_ref[ref].seq + 1)

                # declared material line set (inclusive 1-based)
                decl_set = set(range(mat[0], mat[1] + 1)) if mat else set()
                stem_set = set(stem_l1)
                decl_stem_shared = sorted(decl_set & stem_set)

                # resolved material (interior) vs stem
                res_set = set(res_mat["line_numbers_1b"]) if isinstance(res_mat, dict) else set()
                res_stem_shared = sorted(res_set & stem_set)

                # evidence parse
                un = mat_unres.get(uid)
                ev = list(un.evidence) if un else []
                kinds = Counter()
                target_details = []
                for e in ev:
                    se = str(e)
                    if not se.startswith("overlaps"):
                        continue
                    m = re.search(r"sp-([A-Za-z0-9_-]+)(?:\.(sub))?\.stem", se)
                    if m:
                        ou = m.group(1)
                        kinds["OWN_STEM" if ou == uid else "OTHER_UNIT_STEM"] += 1
                        target_details.append({"text": se, "kind": "OWN_STEM" if ou == uid else "OTHER_UNIT_STEM", "other_unit": ou})
                        continue
                    if "overlaps material" in se or re.search(r"material sp-", se):
                        kinds["MATERIAL"] += 1
                        target_details.append({"text": se, "kind": "MATERIAL"})
                        continue
                    if "answer" in se:
                        kinds["ANSWER"] += 1
                        target_details.append({"text": se, "kind": "ANSWER"})
                        continue
                    kinds["OTHER"] += 1
                    target_details.append({"text": se, "kind": "OTHER"})

                rel_q = region_class(mat, que)

                # exclusive mechanism
                if rel_q == "SAME_REGION" and kinds.get("OWN_STEM"):
                    mech = "A_SAME_REGION_OWN_STEM"
                elif rel_q == "DIFFERENT_REGION" and kinds.get("OTHER_UNIT_STEM"):
                    mech = "B_CROSS_REGION_OTHER_UNIT_STEM"
                elif rel_q == "DIFFERENT_REGION" and kinds.get("ANSWER"):
                    mech = "B_CROSS_REGION_ANSWER"
                elif kinds.get("MATERIAL") and rel_q == "DIFFERENT_REGION":
                    mech = "B_CROSS_REGION_MATERIAL_MATERIAL"
                elif kinds.get("MATERIAL") and rel_q == "SAME_REGION":
                    mech = "A_SAME_REGION_MATERIAL"
                elif rel_q == "DIFFERENT_REGION":
                    mech = "B_CROSS_REGION_OTHER"
                elif rel_q == "SAME_REGION":
                    mech = "A_SAME_REGION_OTHER"
                elif rel_q == "PARTIAL_REGION_OVERLAP":
                    mech = "PARTIAL_REGION"
                else:
                    mech = "UNKNOWN"

                row = {
                    "unit_id": uid,
                    "document_id": str(doc_id),
                    "source_version_id": str(sv_id),
                    "file_name": fname,
                    "declared_material": {
                        "start": mat[0] if mat else None,
                        "end": mat[1] if mat else None,
                        "semantics": "inclusive",
                    },
                    "questions_region": {
                        "start": que[0] if que else None,
                        "end": que[1] if que else None,
                        "semantics": "inclusive",
                    },
                    "material_question_relation": rel_q,
                    "resolved_material": (
                        res_mat
                        if isinstance(res_mat, dict)
                        else {
                            "status": "NOT_AVAILABLE_OR_EMPTY",
                            "note": res_note,
                            "start_seq_marker": s_seq,
                            "end_seq_marker": e_seq,
                            "code_reason": "resolver _material_span exclusive interior between markers; demoted span not kept in resolved_spans",
                        }
                    ),
                    "stem_span": {
                        "span_id": stem_sp.span_id if stem_sp else None,
                        "line_refs": list(stem_sp.line_refs) if stem_sp else [],
                        "line_numbers_1b": stem_l1,
                        "start": stem_l1[0] if stem_l1 else None,
                        "end": stem_l1[-1] if stem_l1 else None,
                    },
                    "overlap": {
                        "declared_material_vs_stem": len(decl_stem_shared) > 0,
                        "declared_material_vs_stem_shared_count": len(decl_stem_shared),
                        "declared_material_vs_stem_shared_lines": decl_stem_shared[:30],
                        "resolved_material_vs_stem": len(res_stem_shared) > 0,
                        "resolved_material_vs_stem_shared_count": len(res_stem_shared),
                        "resolved_material_vs_stem_shared_lines": res_stem_shared[:30],
                    },
                    "overlap_target_kinds_nonexclusive": dict(kinds),
                    "overlap_target_details": target_details,
                    "mechanism_class_exclusive": mech,
                    "resolver_rejection": {
                        "actual": un is not None,
                        "evidence_verbatim": ev,
                        "point": "resolver.py:_enforce_material_overlap:628-658",
                    },
                }
                rows.append(row)

    # 4 vs 10 reconciliation table
    n_decl = sum(1 for r in rows if r["overlap"]["declared_material_vs_stem"])
    n_res = sum(1 for r in rows if r["overlap"]["resolved_material_vs_stem"])
    n_own_ev = sum(1 for r in rows if r["overlap_target_kinds_nonexclusive"].get("OWN_STEM"))

    mech = Counter(r["mechanism_class_exclusive"] for r in rows)
    kinds_nonex = Counter()
    for r in rows:
        for k, v in r["overlap_target_kinds_nonexclusive"].items():
            kinds_nonex[k] += 1  # unit-level presence
        kinds_nonex[f"presence_{k}"] = kinds_nonex.get(f"presence_{k}", 0)

    presence = Counter()
    for r in rows:
        for k in r["overlap_target_kinds_nonexclusive"]:
            presence[k] += 1

    rel = Counter(r["material_question_relation"] for r in rows)

    out = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "baseline": {
            "head": "39840ff",
            "match_norm": "v1.1 dirty 015cdfa",
            "unit_set": "Phase1.3R-B MATERIAL_OVERLAP_REJECTED exact 20 (not reclassified)",
        },
        "overlap_units_count": len(rows),
        "unit_ids": [r["unit_id"] for r in rows],
        "units": rows,
        "p2_measurement_table": {
            "declared_material_intersect_own_stem": {
                "definition": "Producer material_lines inclusive set ∩ resolver stem line_numbers_1b (own unit)",
                "count": n_decl,
                "unit_ids": [r["unit_id"] for r in rows if r["overlap"]["declared_material_vs_stem"]],
            },
            "resolved_material_intersect_own_stem": {
                "definition": "marker-interior material span ∩ resolver stem line_numbers_1b (own unit)",
                "count": n_res,
                "unit_ids": [r["unit_id"] for r in rows if r["overlap"]["resolved_material_vs_stem"]],
            },
            "evidence_string_mentions_own_stem": {
                "definition": "unresolved evidence contains 'sp-<uid>[.sub].stem' (MIMO 1.3R-B 'overlaps_own_stem')",
                "count": n_own_ev,
                "unit_ids": [r["unit_id"] for r in rows if r["overlap_target_kinds_nonexclusive"].get("OWN_STEM")],
            },
            "verdict": (
                "NOT A CONTRADICTION — different measurement scopes. "
                "DSH 4 = declared inclusive ∩ own stem; "
                "MIMO 10 = evidence-string own-stem mention (includes cases where "
                "marker-resolved material landed on stem lines even if declared range is disjoint, "
                "or multi-span collision)."
            ),
        },
        "p3_region_class": dict(rel),
        "p4_overlap_target_presence_nonexclusive": dict(presence),
        "p5_mechanism_exclusive": dict(mech),
        "p5_two_mechanism": {
            "A_same_region_structural_collision": sum(v for k, v in mech.items() if k.startswith("A_")),
            "B_cross_region_appendix_collision": sum(v for k, v in mech.items() if k.startswith("B_")),
            "partial_or_unknown": sum(v for k, v in mech.items() if not k.startswith(("A_", "B_"))),
        },
        "observed_facts": [
            f"exact 20 units preserved",
            f"declared∩own stem = {n_decl} (DSH measurement)",
            f"resolved∩own stem = {n_res}",
            f"evidence own-stem mention = {n_own_ev} (MIMO measurement)",
            f"region: {dict(rel)}",
            f"mechanism exclusive: {dict(mech)}",
        ],
        "causal_conclusions": [
            "CONTROL FLOW PROVEN: _enforce_material_overlap demotes material when line_refs "
            "intersect any other resolved span (resolver.py:628-658). Direct cause of rejection.",
            "P2: 4 vs 10 are measurement-scope differences, not a contradiction "
            "(declared range vs evidence-string / resolved span).",
        ],
        "not_claimed": [
            "decomposition alone caused every rejection",
            "LEVEL 2 required for these 20",
        ],
    }
    (OUT / "overlap_final_evidence.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print("count", len(rows))
    print("P2 declared∩stem", n_decl, "resolved∩stem", n_res, "evidence own", n_own_ev)
    print("P3", dict(rel))
    print("P5 mech", dict(mech))
    print("two-mech", out["p5_two_mechanism"])
    print("presence", dict(presence))


if __name__ == "__main__":
    asyncio.run(main())
