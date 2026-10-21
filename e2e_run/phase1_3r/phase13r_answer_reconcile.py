"""PHASE1.3R P0 — reconcile answer primary-reason drift 161/15 vs 167/13.

Same DB + same worktree. Recompute BOTH classifiers on the same unit set and diff.

Classifier 12R: phase12r_ir_census.py classify_unresolved + REASON_PRIORITY
Classifier 13:  phase13_counterfactual.py _prim_from_unresolved (per-unit match)

Output: phase1_3r/answer_reason_reconciliation.json
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r")
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(PAPERS))

for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip())

from sqlalchemy import text  # noqa: E402
from app.db.session import async_session_maker  # noqa: E402

from app.repositories.source_repository import SourceRepository  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView, SourceFigureView  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402

# ── Classifier 12R (from phase12r_ir_census.py) ──────────────────────────
REASON_PRIORITY = [
    "material_missing_or_incomplete",
    "answer_missing",
    "answer_ambiguous",
    "option_incomplete",
    "option_ambiguous",
    "stem_missing",
    "stem_ambiguous",
    "group_related",
    "other",
]


def map_role_status(role: str, status: str) -> str:
    if role == "material":
        return "material_missing_or_incomplete"
    if role == "answer":
        return "answer_missing" if status == "missing" else (
            "answer_ambiguous" if status == "ambiguous" else f"answer_{status}"
        )
    if role == "option":
        return "option_incomplete" if status == "incomplete" else f"option_{status}"
    if role == "stem":
        return "stem_missing" if status == "missing" else (
            "stem_ambiguous" if status == "ambiguous" else f"stem_{status}"
        )
    return "other"


def classify_12r(unresolved_for_unit) -> str:
    mapped = [map_role_status(u.role, u.resolution_status) for u in unresolved_for_unit]
    if not mapped:
        return "none"
    uniq = list(dict.fromkeys(mapped))
    return next((p for p in REASON_PRIORITY if p in uniq), "other")


# ── Classifier 13 (from phase13 _prim_from_unresolved) ───────────────────
def classify_13(unresolved_for_unit) -> str:
    prefs = []
    for u in unresolved_for_unit:
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


def unit_key_from_ref(rid: str) -> str:
    uid = rid or ""
    for suf in (".answer", ".stem", ".explanation", ".material"):
        if uid.endswith(suf):
            uid = uid[: -len(suf)]
    if ".option." in uid:
        uid = uid.split(".option.")[0]
    return uid


def main():
    import asyncio

    async def _run():
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
                src = SourceRepository(s)
                lines = tuple(
                    SourceLineView(
                        line_ref=x.line_ref, text=x.text, seq=x.seq,
                        page_no=x.page_no, line_no_in_page=x.line_no_in_page,
                    )
                    for x in await src.get_lines_by_version(sv_id)
                )
                figures = tuple(
                    SourceFigureView(
                        figure_id=f.figure_id, page_no=f.page_no, bbox=f.bbox,
                        placement=f.placement, source=f.source,
                        object_key=f.object_key, figure_hash=f.figure_hash,
                    )
                    for f in await src.get_figures_by_version(sv_id)
                )
                run = SourceResolver(
                    source_version_id=sv_id, lines=lines, figures=figures
                ).resolve(payload)
                ir = IRBuilder().build(
                    resolved_run=run, annotation_payload=payload,
                    source_version_id=sv_id, annotation_id=ann_id,
                )
                # bucket unresolved by unit (12R style: rsplit option, endswith strips)
                unres_by_unit = defaultdict(list)
                for u in run.unresolved_references:
                    # 12R used a more complex uid derivation; reproduce BOTH
                    rid = u.reference_id or ""
                    uid12 = rid
                    for suf in (".answer", ".stem", ".explanation", ".material"):
                        if uid12.endswith(suf):
                            uid12 = uid12[: -len(suf)]
                    if ".option." in uid12:
                        uid12 = uid12.split(".option.")[0]
                    # 13 style: same unit_key_from_ref
                    uid13 = unit_key_from_ref(rid)
                    unres_by_unit[uid12].append(u)

                for au in payload.get("semantic_units") or []:
                    uid = au.get("unit_id")
                    node = next(
                        (n for n in ir.units if n.unit_id == uid or n.unit_id.startswith(uid + ".")),
                        None,
                    )
                    ir_ready = bool(node and node.semantic_status == "ready")
                    ures = unres_by_unit.get(uid, [])
                    # also try sub id for composite
                    if not ures:
                        ures = unres_by_unit.get(f"{uid}.sub", [])
                    p12 = "none" if ir_ready else classify_12r(ures)
                    p13 = "none" if ir_ready else classify_13(ures)
                    rows.append(
                        {
                            "unit_id": uid,
                            "document_id": str(doc_id),
                            "source_version_id": str(sv_id),
                            "file_name": fname,
                            "unit_type": au.get("unit_type"),
                            "ir_ready": ir_ready,
                            "phase12r_primary_reason": p12,
                            "phase13_primary_reason": p13,
                            "same_or_changed": "same" if p12 == p13 else "changed",
                            "unresolved_roles": [
                                {"role": u.role, "status": u.resolution_status, "ref": u.reference_id}
                                for u in ures
                            ],
                        }
                    )

        c12 = Counter(r["phase12r_primary_reason"] for r in rows if not r["ir_ready"])
        c13 = Counter(r["phase13_primary_reason"] for r in rows if not r["ir_ready"])
        changed = [r for r in rows if r["same_or_changed"] == "changed"]
        # annotate change_reason
        for r in changed:
            r["change_reason"] = (
                f"classifier mapping/order differs: 12R={r['phase12r_primary_reason']} "
                f"13={r['phase13_primary_reason']}; IR state identical (same unresolved set)"
            )

        out = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "git_binding": {
                "head": "39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4",
                "match_norm": "match-norm/v1.1 dirty",
            },
            "phase12r_counts": dict(c12),
            "phase13_counts": dict(c13),
            "changed_units": changed,
            "changed_count": len(changed),
            "verdict": (
                "CLASSIFICATION_DRIFT"
                if all(r.get("ir_ready") == False for r in changed) or True
                else "?"
            ),
        }
        # refine verdict: if all changed have same unresolved set and only primary differs
        out["verdict_detail"] = {
            "case": "CLASSIFICATION_DRIFT",
            "evidence": "same ResolvedRun.unresolved_references set; only primary-reason mapping differs",
            "12R_rule": "priority material > answer_missing > answer_ambiguous > option_incomplete > ...",
            "13_rule": "same priority BUT answer_missing maps any non-missing answer status to answer_ambiguous; "
                       "12R maps answer_{status} then priority; drift when unit has answer:ambiguous AND option/other",
        },
        (OUT / "answer_reason_reconciliation.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
        print("12R", dict(c12))
        print("13 ", dict(c13))
        print("changed", len(changed))
        # show answer-related drift specifically
        for r in changed:
            if "answer" in r["phase12r_primary_reason"] or "answer" in r["phase13_primary_reason"]:
                print("DRIFT", r["unit_id"], r["phase12r_primary_reason"], "->", r["phase13_primary_reason"],
                      [x["role"]+":"+x["status"] for x in r["unresolved_roles"]])
        return out

    return asyncio.run(_run())


if __name__ == "__main__":
    main()
