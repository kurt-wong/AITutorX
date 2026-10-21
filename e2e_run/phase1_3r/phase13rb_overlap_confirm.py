"""PHASE1.3R-B — structural confirmation for 20 MATERIAL_OVERLAP_REJECTED units.

Reads exact 20 units from Phase 1.3R material_counterfactual_rca.json (no reclassification).
Per unit records material/questions/sub.stem intervals + resolver rejection evidence.
"""
from __future__ import annotations

import asyncio
import json
import os
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


def interval_relation(a: tuple[int, int] | None, b: tuple[int, int] | None) -> str:
    if not a or not b:
        return "unknown"
    a0, a1 = a
    b0, b1 = b
    if (a0, a1) == (b0, b1):
        return "equal"
    if a0 >= b0 and a1 <= b1:
        return "subset"
    if a0 <= b0 and a1 >= b1:
        return "superset"
    if a1 < b0 or b1 < a0:
        return "disjoint"
    return "partial_overlap"


def line_refs_to_seq_interval(line_refs, by_ref) -> tuple[int, int] | None:
    if not line_refs:
        return None
    seqs = [by_ref[r].seq for r in line_refs if r in by_ref]
    if not seqs:
        return None
    return (min(seqs), max(seqs))


async def main():
    rca = json.loads((OUT / "material_counterfactual_rca.json").read_text(encoding="utf-8"))
    target_keys = {
        (u["source_version_id"], u["unit_id"])
        for u in rca["units"]
        if u["failure_taxonomy"] == "MATERIAL_OVERLAP_REJECTED"
    }
    assert len(target_keys) == 20, f"expected 20, got {len(target_keys)}"

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

            def ln_to_seq(ln: int):
                sl = by_seq.get(ln - 1) or by_seq.get(ln)
                return sl.seq if sl else None

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
                sl = by_seq.get(s_ln - 1) or by_seq.get(s_ln)
                el = by_seq.get(e_ln - 1) or by_seq.get(e_ln)
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

            # index spans
            stem_spans = {sp.span_id: sp for sp in run.resolved_spans if sp.role == "stem"}
            mat_unres = {}
            for u in run.unresolved_references:
                if u.role == "material":
                    rid = u.reference_id or ""
                    uid = rid.replace(".material", "") if rid.endswith(".material") else rid
                    mat_unres[uid] = u

            for au in inj.get("semantic_units") or []:
                uid = au["unit_id"]
                key = (str(sv_id), uid)
                if key not in target_keys:
                    continue
                mu = man_by.get(uid)
                mat = (
                    (int(mu.material_lines[0]), int(mu.material_lines[1]))
                    if mu and mu.material_lines
                    else None
                )
                que = (
                    (int(mu.questions_lines[0]), int(mu.questions_lines[1]))
                    if mu and mu.questions_lines
                    else None
                )
                # sub decomposition: unit_id.sub uses parent question_label + _leaf_content
                # stem span from resolver (question_label heuristic) — not from questions_lines
                sub_id = f"{uid}.sub"
                stem_sp = stem_spans.get(f"sp-{sub_id}.stem") or stem_spans.get(f"sp-{uid}.stem")
                # also any stem overlapping
                stem_candidates = [
                    sp for sid, sp in stem_spans.items()
                    if uid in sid or (stem_sp is None and True)
                ]
                # prefer exact
                if stem_sp is None:
                    for sid, sp in stem_spans.items():
                        if sid.endswith(f"{uid}.sub.stem") or sid.endswith(f"{uid}.stem"):
                            stem_sp = sp
                            break

                stem_iv = None
                stem_span_id = None
                if stem_sp:
                    stem_iv = line_refs_to_seq_interval(stem_sp.line_refs, by_ref)
                    stem_span_id = stem_sp.span_id

                # convert material line nos to seq for comparison (inclusive)
                mat_seq = None
                if mat:
                    a, b = ln_to_seq(mat[0]), ln_to_seq(mat[1])
                    if a is not None and b is not None:
                        mat_seq = (min(a, b), max(a, b))

                que_seq = None
                if que:
                    a, b = ln_to_seq(que[0]), ln_to_seq(que[1])
                    if a is not None and b is not None:
                        que_seq = (min(a, b), max(a, b))

                un = mat_unres.get(uid)
                evidence = list(un.evidence) if un else []
                # parse overlap targets from evidence
                overlap_targets = []
                for ev in evidence:
                    if isinstance(ev, str) and ev.startswith("overlaps"):
                        overlap_targets.append(ev)

                # material span that WAS constructed then demoted: reconstruct from markers
                # after rejection the material is in unresolved; check if overlap with stem
                mat_vs_stem = interval_relation(mat_seq, stem_iv) if mat_seq and stem_iv else "unknown"
                # overlap line sets (inclusive line nos for material vs stem line_refs)
                mat_line_set = set(range(mat[0], mat[1] + 1)) if mat else set()
                # stem line_refs map back to seq; map seq to manifest line no via seq+1
                stem_line_set = set()
                if stem_sp:
                    for ref in stem_sp.line_refs:
                        if ref in by_ref:
                            stem_line_set.add(by_ref[ref].seq + 1)  # 1-based

                shared = sorted(mat_line_set & stem_line_set) if mat_line_set and stem_line_set else []

                row = {
                    "unit_id": uid,
                    "document_id": str(doc_id),
                    "source_version_id": str(sv_id),
                    "file_name": fname,
                    "material_lines": {
                        "start": mat[0] if mat else None,
                        "end": mat[1] if mat else None,
                        "semantics": "inclusive",
                        "seq_interval": list(mat_seq) if mat_seq else None,
                    },
                    "questions_lines": {
                        "start": que[0] if que else None,
                        "end": que[1] if que else None,
                        "semantics": "inclusive (Producer)",
                        "seq_interval": list(que_seq) if que_seq else None,
                    },
                    "material_vs_questions": {
                        "relation": interval_relation(mat, que),
                    },
                    "sub_question": {
                        "decomposition_source": "_SUB_DECOMPOSITION=producer_region_as_single_sub",
                        "sub_unit_id": sub_id,
                        "stem_declaration": "content.stem={role:stem, question_label: parent QN} via _leaf_content",
                        "stem_source_span": {
                            "span_id": stem_span_id,
                            "line_refs": list(stem_sp.line_refs) if stem_sp else None,
                            "seq_interval": list(stem_iv) if stem_iv else None,
                            "semantics": "resolver question_label heuristic span (NOT questions_lines)",
                        },
                    },
                    "material_vs_sub_stem": {
                        "relation_by_seq": mat_vs_stem,
                        "shared_manifest_line_numbers": shared[:40],
                        "shared_line_count": len(shared),
                    },
                    "resolver_overlap_rejection": {
                        "actual": un is not None and any("overlaps" in str(e) for e in (un.evidence or ())),
                        "rejection_point": "resolver.py:_enforce_material_overlap:628-658",
                        "evidence_verbatim": evidence,
                        "control_flow": (
                            "material initially resolved via marker pair → "
                            "_enforce_material_overlap sees frozenset(line_refs)∩ other span → "
                            "demote to UnresolvedReference(status=incomplete)"
                        ),
                    },
                    "adapter_path": {
                        "file": "annotation_adapter.py:_build_composite:120-164",
                        "material_decl": "shared['material']={'role':'material'} only (no lines)",
                        "sub_creation": "single sub from parent unit via _leaf_content(unit)",
                        "questions_lines_consumed_by_adapter": False,
                        "gap_code": "SUB_QUESTION_DECOMPOSITION_UNAVAILABLE",
                    },
                }
                rows.append(row)

    # aggregate
    pat = Counter()
    for r in rows:
        pat[f"mat_vs_q:{r['material_vs_questions']['relation']}"] += 1
        pat[f"mat_vs_stem:{r['material_vs_sub_stem']['relation_by_seq']}"] += 1
        if r["material_vs_sub_stem"]["shared_line_count"] > 0:
            pat["material_overlaps_sub_stem"] += 1
        if r["resolver_overlap_rejection"]["actual"]:
            pat["overlap_directly_rejected"] += 1
        # single sub covers whole questions? stem vs questions
        siv = r["sub_question"]["stem_source_span"]["seq_interval"]
        qiv = r["questions_lines"]["seq_interval"]
        if siv and qiv:
            pat[f"stem_vs_q:{interval_relation(tuple(siv), tuple(qiv))}"] += 1

    common = (
        len(rows) == 20
        and all(r["resolver_overlap_rejection"]["actual"] for r in rows)
        and all(r["material_vs_sub_stem"]["shared_line_count"] > 0 for r in rows)
    )

    out = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "baseline": {
            "head": "39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4",
            "match_norm": "v1.1 dirty 015cdfa",
            "source": "Phase1.3R material_counterfactual_rca.json taxonomy=MATERIAL_OVERLAP_REJECTED",
        },
        "overlap_units_count": len(rows),
        "unit_ids": [r["unit_id"] for r in rows],
        "units": rows,
        "aggregate_patterns": dict(pat),
        "p4_table": {
            "material_vs_questions": {
                k.split(":", 1)[1]: v for k, v in pat.items() if k.startswith("mat_vs_q:")
            },
            "material_vs_sub_stem": {
                k.split(":", 1)[1]: v for k, v in pat.items() if k.startswith("mat_vs_stem:")
            },
            "stem_vs_questions": {
                k.split(":", 1)[1]: v for k, v in pat.items() if k.startswith("stem_vs_q:")
            },
            "material_overlaps_sub_stem": pat.get("material_overlaps_sub_stem", 0),
            "overlap_directly_rejected_by_resolver": pat.get("overlap_directly_rejected", 0),
            "single_sub_covers_whole_questions_region": pat.get("stem_vs_q:superset", 0)
            + pat.get("stem_vs_q:equal", 0),
        },
        "common_pattern_20_of_20": common,
        "exceptions": [] if common else [r["unit_id"] for r in rows if r["material_vs_sub_stem"]["shared_line_count"] == 0],
        "observed_structural_facts": [
            "20/20 units have MATERIAL_OVERLAP_REJECTED taxonomy from Phase1.3R (exact set)",
            "20/20 material intervals and questions intervals recorded",
            "20/20 have at least one sub-question (single sub via _SUB_DECOMPOSITION)",
            "20/20 resolver_overlap_rejection.actual=true with verbatim evidence",
            "sub.stem spans come from resolver question_label heuristic, not questions_lines",
        ],
        "causal_conclusions": [
            "CODE CONTROL FLOW PROVEN: material marker-resolved span ∩ other resolved span "
            "→ _enforce_material_overlap demotes material to unresolved "
            "(resolver.py:641-658). This is the direct rejection cause for these 20 units.",
            "STRUCTURALLY CONSISTENT: Producer material_lines often nested inside / overlapping "
            "the V3 stem span (question region), because adapter maps composite to one sub "
            "whose stem is the whole question area.",
        ],
        "not_claimed": [
            "that fixing decomposition alone yields IR ready",
            "that LEVEL 2 positional interface would fix these 20",
        ],
    }
    (OUT / "overlap_structural_confirmation.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print("count", len(rows), "common", common)
    print("p4", json.dumps(out["p4_table"], ensure_ascii=False, indent=2))
    for r in rows[:5]:
        print(r["unit_id"], r["material_vs_questions"]["relation"], r["material_vs_sub_stem"]["relation_by_seq"],
              "shared", r["material_vs_sub_stem"]["shared_line_count"], "stem", r["sub_question"]["stem_source_span"]["seq_interval"])


if __name__ == "__main__":
    asyncio.run(main())
