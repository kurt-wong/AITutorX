"""PHASE1.3R P1 — material marker RCA for 54 composite (11 resolved / 43 unresolved).

Also records Producer material_lines semantics vs Resolver marker interior semantics.
Outputs under phase1_3r/:
  material_counterfactual_rca.json
  material_resolved_controls.json
  material_lines_semantics.json
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
from app.domains.compile.ir import IRBuilder  # noqa: E402

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")


def classify_failure(start_st, end_st, s_cnt, e_cnt, s_seq, e_seq, interior_ok, resolved) -> str:
    if resolved:
        return "RESOLVED"
    if start_st in ("missing", "incomplete") or s_cnt == 0:
        return "START_MARKER_NOT_FOUND"
    if end_st in ("missing", "incomplete") or e_cnt == 0:
        return "END_MARKER_NOT_FOUND"
    if start_st == "ambiguous" or s_cnt > 1:
        return "START_MARKER_AMBIGUOUS"
    if end_st == "ambiguous" or e_cnt > 1:
        return "END_MARKER_AMBIGUOUS"
    if s_seq is not None and e_seq is not None and e_seq <= s_seq:
        return "MARKER_ORDER_INVALID"
    if s_seq is not None and e_seq is not None and e_seq <= s_seq + 1:
        return "INTERIOR_EMPTY"
    return "OTHER"


async def main():
    maps = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        maps[Path(m.source_file).name] = m

    unresolved_rows = []
    resolved_rows = []

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
            raw_lines = list(await src.get_lines_by_version(sv_id))
            lines = tuple(
                SourceLineView(
                    line_ref=x.line_ref, text=x.text, seq=x.seq,
                    page_no=x.page_no, line_no_in_page=x.line_no_in_page,
                )
                for x in raw_lines
            )
            by_seq = {l.seq: l for l in lines}
            # map 1-based manifest line no -> SourceLine
            def line_at(ln: int):
                return by_seq.get(ln - 1) or by_seq.get(ln)

            figures = tuple(
                SourceFigureView(
                    figure_id=f.figure_id, page_no=f.page_no, bbox=f.bbox,
                    placement=f.placement, source=f.source,
                    object_key=f.object_key, figure_hash=f.figure_hash,
                )
                for f in await src.get_figures_by_version(sv_id)
            )

            # inject material markers
            inj = json.loads(json.dumps(payload))
            injected_units = {}
            for au in inj.get("semantic_units") or []:
                if au.get("unit_type") != "composite_unit":
                    continue
                mu = man_by.get(au["unit_id"])
                if not mu or not mu.material_lines:
                    continue
                s_ln, e_ln = int(mu.material_lines[0]), int(mu.material_lines[1])
                sl, el = line_at(s_ln), line_at(e_ln)
                if not sl or not el:
                    continue
                marker = {
                    "role": "material",
                    "start_marker": {"granularity": "multi_line_pair", "text": sl.text},
                    "end_marker": {"text": el.text},
                }
                au.setdefault("shared_components", {})["material"] = marker
                injected_units[au["unit_id"]] = {
                    "material_lines": [s_ln, e_ln],
                    "start_marker_text": sl.text,
                    "end_marker_text": el.text,
                    "start_line_ref": sl.line_ref,
                    "end_line_ref": el.line_ref,
                    "start_seq": sl.seq,
                    "end_seq": el.seq,
                    "n_content_lines_inclusive": e_ln - s_ln + 1,
                }

            run = SourceResolver(
                source_version_id=sv_id, lines=lines, figures=figures
            ).resolve(inj)
            ir = IRBuilder().build(
                resolved_run=run, annotation_payload=inj,
                source_version_id=sv_id, annotation_id=ann_id,
            )
            ir_by = {}
            for n in ir.units:
                ir_by[n.unit_id] = n

            # index material resolved/unresolved
            mat_resolved_by_unit = {}
            for sp in run.resolved_spans:
                if sp.role == "material":
                    # span_id sp-<target_id> e.g. sp-U2-5.material
                    tid = sp.span_id[3:] if sp.span_id.startswith("sp-") else sp.span_id
                    uid = tid.replace(".material", "") if tid.endswith(".material") else tid
                    mat_resolved_by_unit[uid] = sp

            mat_unres_by_unit = {}
            for u in run.unresolved_references:
                if u.role != "material":
                    continue
                rid = u.reference_id or ""
                uid = rid.replace(".material", "") if rid.endswith(".material") else rid
                mat_unres_by_unit[uid] = u

            # match counts in source for marker texts
            def match_count(t: str) -> int:
                return sum(1 for l in lines if l.text == t)

            for uid, meta in injected_units.items():
                sc = match_count(meta["start_marker_text"])
                ec = match_count(meta["end_marker_text"])
                other = []
                for u in run.unresolved_references:
                    rid = u.reference_id or ""
                    if rid == uid or rid.startswith(uid + ".") or rid.startswith(uid + ".sub"):
                        if u.role != "material":
                            other.append(f"{u.role}:{u.resolution_status}")

                sp = mat_resolved_by_unit.get(uid)
                un = mat_unres_by_unit.get(uid)
                resolved = sp is not None
                # taxonomy
                if resolved:
                    tax = "RESOLVED"
                    reason = f"span={sp.span_id} status={sp.resolution_status}"
                    material_span_status = sp.resolution_status
                else:
                    # parse unresolved evidence for start/end
                    ev = tuple(un.evidence) if un else ()
                    ev_s = " ".join(str(x) for x in ev)
                    if "start" in ev_s and "not uniquely" in ev_s:
                        start_st = "ambiguous" if sc > 1 else "missing"
                        end_st = "ok"
                    elif "end" in ev_s and "not uniquely" in ev_s:
                        start_st = "ok"
                        end_st = "ambiguous" if ec > 1 else "missing"
                    elif "pair requires" in ev_s or "marker text missing" in ev_s:
                        start_st = "missing"
                        end_st = "missing"
                    elif "interior empty" in ev_s:
                        start_st = "resolved"
                        end_st = "resolved"
                    elif "ambiguous" in ev_s:
                        start_st = "ambiguous" if sc > 1 else "ok"
                        end_st = "ambiguous" if ec > 1 else "ok"
                    else:
                        start_st = "unknown"
                        end_st = "unknown"
                    tax = classify_failure(
                        start_st, end_st, sc, ec,
                        meta["start_seq"], meta["end_seq"],
                        interior_ok=True, resolved=False,
                    )
                    if "interior empty" in ev_s:
                        tax = "INTERIOR_EMPTY"
                    elif "not uniquely" in ev_s and "start" in ev_s:
                        tax = "START_MARKER_AMBIGUOUS" if sc > 1 else "START_MARKER_NOT_FOUND"
                    elif "not uniquely" in ev_s and "end" in ev_s:
                        tax = "END_MARKER_AMBIGUOUS" if ec > 1 else "END_MARKER_NOT_FOUND"
                    material_span_status = un.resolution_status if un else "unknown"
                    reason = ev_s

                row = {
                    "unit_id": uid,
                    "document_id": str(doc_id),
                    "source_version_id": str(sv_id),
                    "file_name": fname,
                    "material_lines": meta["material_lines"],
                    "n_content_lines_inclusive": meta["n_content_lines_inclusive"],
                    "start_marker_text": meta["start_marker_text"][:120],
                    "end_marker_text": meta["end_marker_text"][:120],
                    "start_line_ref": meta["start_line_ref"],
                    "end_line_ref": meta["end_line_ref"],
                    "start_seq": meta["start_seq"],
                    "end_seq": meta["end_seq"],
                    "marker_start_match_count": sc,
                    "marker_end_match_count": ec,
                    "material_span_status": material_span_status,
                    "material_span_reason": reason,
                    "failure_taxonomy": tax,
                    "other_ir_blockers": other,
                    "ir_unit_status": (
                        ir_by[uid].semantic_status
                        if uid in ir_by
                        else next(
                            (n.semantic_status for n in ir.units if n.unit_id.startswith(uid)),
                            "?",
                        )
                    ),
                }
                if resolved:
                    resolved_rows.append(row)
                else:
                    unresolved_rows.append(row)

    tax_counts = Counter(r["failure_taxonomy"] for r in unresolved_rows)
    n_lines = Counter(r["n_content_lines_inclusive"] for r in unresolved_rows)
    n_lines_ok = Counter(r["n_content_lines_inclusive"] for r in resolved_rows)

    semantics = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "producer_material_lines": {
            "definition": "reslice_pipeline.py prompt schema: [起始行号, 结束行号]",
            "validation": "chk_range rg[0]>=1, rg[1]<=n_lines, rg[0]<=rg[1] (start==end legal → single line)",
            "semantics": "INCLUSIVE content line range (material ⊆ questions; image baseline treats as content zone)",
            "evidence": "reslice_pipeline.py:312,391-397,581-584; reslice_qc.py C12 material⊆questions",
        },
        "resolver_marker_interior": {
            "definition": "resolver.py:_material_span multi_line_pair",
            "semantics": "EXCLUSIVE interior between marker lines: refs = between(s_seq+1, e_seq)",
            "evidence": "resolver.py:485-496 comment 'material 正文 = start/end marker 之间（排他）'",
        },
        "bridge_used_in_1_3": {
            "mapping": "start_marker.text = source line at material_lines[0]; end_marker.text = line at material_lines[1]",
            "effect": "Producer inclusive content endpoints become markers; resolver returns INTERIOR only",
            "mismatch": "MISALIGNED — drops first and last content lines; N<=2 → INTERIOR_EMPTY",
        },
        "q5_alignment": "MISALIGNED",
    }

    out_rca = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "total_composite_injected": len(unresolved_rows) + len(resolved_rows),
        "resolved_n": len(resolved_rows),
        "unresolved_n": len(unresolved_rows),
        "failure_taxonomy_distribution": dict(tax_counts),
        "taxonomy_buckets": {
            "marker_resolution_failure": sum(
                tax_counts[k]
                for k in (
                    "START_MARKER_NOT_FOUND",
                    "END_MARKER_NOT_FOUND",
                    "START_MARKER_AMBIGUOUS",
                    "END_MARKER_AMBIGUOUS",
                )
            ),
            "span_boundary_interior_semantics": sum(
                tax_counts[k] for k in ("MARKER_ORDER_INVALID", "INTERIOR_EMPTY", "INTERIOR_INCOMPLETE")
            ),
            "other_ir_blocker": sum(tax_counts[k] for k in ("OTHER", "MATERIAL_SPAN_RESOLVED_BUT_OTHER_IR_BLOCKER")),
        },
        "content_line_count_unresolved": {str(k): v for k, v in sorted(n_lines.items())},
        "content_line_count_resolved": {str(k): v for k, v in sorted(n_lines_ok.items())},
        "units": unresolved_rows,
    }
    (OUT / "material_counterfactual_rca.json").write_text(
        json.dumps(out_rca, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (OUT / "material_resolved_controls.json").write_text(
        json.dumps(
            {
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "resolved_n": len(resolved_rows),
                "units": resolved_rows,
                "contrast_note": "resolved units tend to have longer unique marker text / unique line text; see match counts",
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    (OUT / "material_lines_semantics.json").write_text(
        json.dumps(semantics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("unresolved", len(unresolved_rows), "resolved", len(resolved_rows))
    print("taxonomy", dict(tax_counts))
    print("content_len unresolved", dict(n_lines))
    print("content_len resolved", dict(n_lines_ok))
    print("buckets", out_rca["taxonomy_buckets"])


if __name__ == "__main__":
    asyncio.run(main())
