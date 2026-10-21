"""PHASE1.2R P0-B/C — 284-unit IR census + Producer/Adapter/IR positional evidence join.

Outputs (under phase1_2r/census/):
  phase1_2_ir_census.json          per-unit machine-readable census
  producer_adapter_ir_field_stats.json
  ir_loss_attribution.json
  controlled_position_injection.json   (harness-only annotation payload patch; NO source edits)

Git binding: od01-r3-convergence @ 39840ff + dirty match-norm/v1.1 (015cdfa).
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
PAPERS_SCRIPTS = Path(r"D:\Project\Papers\scripts")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_2r\census")
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(PAPERS_SCRIPTS))

_env = BACKEND / ".env"
if _env.exists():
    for _line in _env.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if not _line or _line.startswith("#") or "=" not in _line:
            continue
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip())

from sqlalchemy import text  # noqa: E402

from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    Manifest,
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from app.repositories.source_repository import SourceRepository  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView, SourceFigureView  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402

GIT_BINDING = {
    "branch": "od01-r3-convergence",
    "head": "39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4",
    "match_norm_worktree_blob": "015cdfa515ce23661ac1d9f02fb861869e111363",
    "match_norm_head_blob": "73badc31fe94d4066f9e53469cb704b11ba8844b",
    "match_norm_version": "match-norm/v1.1 (dirty)",
}

# primary_reason priority (documented rule): structural role missing first,
# then answer, then options, then stem, then other resolver evidence.
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


def classify_unresolved(unresolved) -> tuple[str, list[str]]:
    reasons = []
    for u in unresolved:
        role = u.role
        status = u.resolution_status
        if role == "material":
            reasons.append(f"material_{status}" if status != "incomplete" else "material_missing_or_incomplete")
        elif role == "answer":
            reasons.append(f"answer_{status}")
        elif role == "option":
            reasons.append(f"option_{status}")
        elif role == "stem":
            reasons.append(f"stem_{status}")
        else:
            reasons.append(f"{role}_{status}")
    if not reasons:
        return "none", []
    # map to primary set
    mapped = []
    for r in reasons:
        if r.startswith("material_"):
            mapped.append("material_missing_or_incomplete")
        elif r.startswith("answer_missing"):
            mapped.append("answer_missing")
        elif r.startswith("answer_ambiguous"):
            mapped.append("answer_ambiguous")
        elif r.startswith("option_incomplete"):
            mapped.append("option_incomplete")
        elif r.startswith("option_ambiguous"):
            mapped.append("option_ambiguous")
        elif r.startswith("stem_missing"):
            mapped.append("stem_missing")
        elif r.startswith("stem_ambiguous"):
            mapped.append("stem_ambiguous")
        else:
            mapped.append("other")
    uniq = list(dict.fromkeys(mapped))
    primary = next((p for p in REASON_PRIORITY if p in uniq), "other")
    secondary = [x for x in uniq if x != primary]
    return primary, secondary + uniq  # secondary_reasons unique-ish


def producer_fields(man_unit) -> dict:
    def pair(v):
        return list(v) if v else None

    opts = [
        {"label": o.label, "start_line": o.start_line, "end_line": o.end_line}
        for o in (man_unit.options or ())
    ]
    return {
        "stem_lines": pair(man_unit.stem_lines),
        "options_lines": pair(man_unit.options_lines),
        "options": opts,
        "answer_lines": pair(man_unit.answer_lines),
        "explanation_lines": pair(man_unit.explanation_lines),
        "material_lines": pair(man_unit.material_lines),
        "questions_lines": pair(man_unit.questions_lines),
        "has": {
            "stem_lines": man_unit.stem_lines is not None,
            "options": len(opts) > 0,
            "options_lines": man_unit.options_lines is not None,
            "answer_lines": man_unit.answer_lines is not None,
            "explanation_lines": man_unit.explanation_lines is not None,
            "material_lines": man_unit.material_lines is not None,
        },
    }


def adapter_emits(payload_unit: dict, is_composite: bool) -> dict:
    content = (payload_unit.get("content") or {}) if not is_composite else (
        (payload_unit.get("sub_questions") or [{}])[0].get("content") or {}
    )
    shared = payload_unit.get("shared_components") or {}
    mat = shared.get("material")
    return {
        "emits_stem_role": bool(content.get("stem")),
        "emits_stem_position": bool(
            isinstance(content.get("stem"), dict)
            and any(k in content["stem"] for k in ("start_line", "end_line", "line_refs", "span"))
        ),
        "emits_options": bool(content.get("options")),
        "emits_option_position": any(
            isinstance(o, dict)
            and any(k in o for k in ("start_line", "end_line", "line_refs", "span"))
            for o in (content.get("options") or [])
        ),
        "emits_answer_role": bool(content.get("answer")),
        "emits_answer_position": bool(
            isinstance(content.get("answer"), dict)
            and any(k in content["answer"] for k in ("start_line", "end_line", "line_refs", "span"))
        ),
        "emits_explanation_role": bool(content.get("explanation")),
        "emits_material_role": mat is not None,
        "emits_material_position": bool(
            isinstance(mat, dict)
            and any(k in mat for k in ("start_line", "end_line", "line_refs", "span", "start_marker", "end_marker"))
        ),
        "raw_material_decl": mat,
    }


def build_census() -> dict:
    from app.db.session import async_session_maker

    import asyncio

    async def _run():
        rows_out = []
        stats = Counter()
        loss_attr = Counter()
        async with async_session_maker() as s:
            r = await s.execute(
                text(
                    """
                    select sv.id, sv.document_id, sa.id, sa.payload
                    from document_source_versions sv
                    join semantic_annotations sa on sa.source_version_id = sv.id
                    where sv.status='sealed'
                    """
                )
            )
            db_rows = r.fetchall()
            # map document_id -> find matching manifest by file name
            docs = {}
            r = await s.execute(text("select id, file_name, original_sha256 from documents"))
            for did, fname, sha in r.fetchall():
                docs[str(did)] = {"file_name": fname, "sha": sha}

            corpus_root = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
            manifests = {p.stem.replace(".manifest", ""): p for p in find_manifests(corpus_root)}
            # better: key by md name
            man_by_md = {}
            for p in find_manifests(corpus_root):
                try:
                    m = load_manifest(p)
                except Exception:
                    continue
                man_by_md[Path(m.source_file).name] = (p, m)

            for sv_id, doc_id, ann_id, payload in db_rows:
                if isinstance(payload, str):
                    payload = json.loads(payload)
                doc_meta = docs.get(str(doc_id), {})
                fname = doc_meta.get("file_name")
                man_entry = man_by_md.get(fname)
                man = man_entry[1] if man_entry else None

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
                run = SourceResolver(source_version_id=sv_id, lines=lines, figures=figures).resolve(payload)
                ir = IRBuilder().build(
                    resolved_run=run,
                    annotation_payload=payload,
                    source_version_id=sv_id,
                    annotation_id=ann_id,
                )
                # unresolved by unit
                unres_by_unit = defaultdict(list)
                for u in run.unresolved_references:
                    # reference_id like Q1.answer / U51.sub.stem
                    uid = u.reference_id.split(".")[0] if u.reference_id else "?"
                    # for sub units reference may be U51.sub
                    rid = u.reference_id or ""
                    if rid.endswith(".answer") or rid.endswith(".stem") or rid.endswith(".option.A") or ".option." in rid or rid.endswith(".material") or ".material" in rid:
                        uid = rid.rsplit(".", 1)[0] if ".option." not in rid else rid.split(".option.")[0]
                        if uid.endswith(".option"):
                            uid = uid[: -len(".option")]
                    unres_by_unit[uid].append(u)

                # also group by simple prefix
                unres_by_unit2 = defaultdict(list)
                for u in run.unresolved_references:
                    rid = u.reference_id or ""
                    uid = rid
                    for suf in (".answer", ".stem", ".explanation", ".material"):
                        if uid.endswith(suf):
                            uid = uid[: -len(suf)]
                    if ".option." in uid:
                        uid = uid.split(".option.")[0]
                    unres_by_unit2[uid].append(u)

                ir_by_id = {n.unit_id: n for n in ir.units}
                ann_units = payload.get("semantic_units") or []
                man_units = {u.unit_id: u for u in (man.units if man else [])}

                for au in ann_units:
                    uid = au.get("unit_id")
                    is_comp = au.get("unit_type") == "composite_unit"
                    node = ir_by_id.get(uid) or (ir_by_id.get(f"{uid}.sub") if is_comp else None)
                    # IR unit_ids for composite may be parent
                    if node is None:
                        # try match
                        for k, n in ir_by_id.items():
                            if k == uid or k.startswith(uid):
                                node = n
                                break
                    ir_ready = bool(node and node.semantic_status == "ready")
                    primary, secondary = classify_unresolved(unres_by_unit2.get(uid, []))
                    if ir_ready:
                        primary, secondary = "none", []
                    else:
                        # if node incomplete but no unresolved mapped, still classify from node
                        if not unres_by_unit2.get(uid) and node is not None:
                            primary, secondary = "other", []

                    mu = man_units.get(uid)
                    prod = producer_fields(mu) if mu else {"has": {}, "present_in_manifest": False}
                    if mu is None:
                        prod["present_in_manifest"] = False
                    else:
                        prod["present_in_manifest"] = True
                    ad = adapter_emits(au, is_comp)

                    # reference loss definition: producer has positional evidence for role
                    # but adapter does not emit position for that role
                    ph = prod.get("has") or {}
                    ref_loss = {
                        "stem": bool(ph.get("stem_lines")) and not ad["emits_stem_position"],
                        "options": bool(ph.get("options") or ph.get("options_lines")) and not ad["emits_option_position"],
                        "answer": bool(ph.get("answer_lines")) and not ad["emits_answer_position"],
                        "material": bool(ph.get("material_lines")) and not ad["emits_material_position"],
                        "explanation": bool(ph.get("explanation_lines")) and not (
                            isinstance((au.get("content") or {}).get("explanation") if not is_comp else
                                       ((au.get("sub_questions") or [{}])[0].get("content") or {}).get("explanation"), dict)
                            and any(k in ((au.get("content") or {}).get("explanation") if not is_comp else
                                          ((au.get("sub_questions") or [{}])[0].get("content") or {}).get("explanation") or {})
                                    for k in ("start_line", "end_line", "line_refs", "span"))
                        ),
                    }
                    any_loss = any(ref_loss.values())

                    row = {
                        "document_id": str(doc_id),
                        "source_version_id": str(sv_id),
                        "annotation_id": str(ann_id),
                        "unit_id": uid,
                        "unit_type": au.get("unit_type"),
                        "original_question_type": au.get("original_question_type"),
                        "ir_ready": ir_ready,
                        "ir_failure_stage": None if ir_ready else "unit_to_ir",
                        "ir_failure_reason_primary": primary,
                        "ir_failure_reason_secondary": secondary,
                        "producer_present": prod.get("present_in_manifest", False),
                        "producer_reference_presence": prod.get("has", {}),
                        "producer_fields": {k: prod.get(k) for k in (
                            "stem_lines", "options_lines", "options", "answer_lines",
                            "explanation_lines", "material_lines", "questions_lines",
                        )},
                        "annotation_reference_presence": {
                            "stem_role": ad["emits_stem_role"],
                            "stem_position": ad["emits_stem_position"],
                            "options": ad["emits_options"],
                            "option_position": ad["emits_option_position"],
                            "answer_role": ad["emits_answer_role"],
                            "answer_position": ad["emits_answer_position"],
                            "explanation_role": ad["emits_explanation_role"],
                            "material_role": ad["emits_material_role"],
                            "material_position": ad["emits_material_position"],
                        },
                        "adapter_reference_loss": ref_loss,
                        "adapter_reference_loss_any": any_loss,
                        "stem_reference": {
                            "producer": prod.get("stem_lines"),
                            "adapter_position": ad["emits_stem_position"],
                        },
                        "material_reference": {
                            "producer": prod.get("material_lines"),
                            "adapter_decl": ad.get("raw_material_decl"),
                            "adapter_position": ad["emits_material_position"],
                        },
                        "option_reference": {
                            "producer_options": prod.get("options"),
                            "adapter_position": ad["emits_option_position"],
                        },
                        "answer_reference": {
                            "producer": prod.get("answer_lines"),
                            "adapter_position": ad["emits_answer_position"],
                        },
                        "explanation_reference": {
                            "producer": prod.get("explanation_lines"),
                            "adapter_role": ad["emits_explanation_role"],
                        },
                    }
                    rows_out.append(row)

                    stats[f"ir_{'ready' if ir_ready else 'not_ready'}"] += 1
                    stats[f"type_{row['unit_type']}"] += 1
                    if not ir_ready:
                        loss_attr[f"primary_{primary}"] += 1
                        if any_loss and primary != "other":
                            loss_attr["reference_loss_attributable"] += 1
                        elif any_loss:
                            loss_attr["reference_loss_partial"] += 1
                        else:
                            loss_attr["no_reference_loss"] += 1

        return rows_out, stats, loss_attr

    rows_out, stats, loss_attr = asyncio.run(_run())

    census = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "git_binding": GIT_BINDING,
        "total_units": len(rows_out),
        "units": rows_out,
    }
    (OUT / "phase1_2_ir_census.json").write_text(
        json.dumps(census, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )

    # field stats: producer has vs adapter preserves/drops
    def cnt(pred):
        return sum(1 for r in rows_out if pred(r))

    field_stats = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "total_units": len(rows_out),
        "fields": {},
    }
    for field, has_key, pos_key in [
        ("material", "material_lines", "material_position"),
        ("stem", "stem_lines", "stem_position"),
        ("options", "options", "option_position"),
        ("options_lines", "options_lines", "option_position"),
        ("answer", "answer_lines", "answer_position"),
        ("explanation", "explanation_lines", "explanation_role"),
    ]:
        n_prod = cnt(lambda r, k=has_key: bool((r.get("producer_reference_presence") or {}).get(k)))
        n_pres = cnt(
            lambda r, k=has_key, p=pos_key: bool((r.get("producer_reference_presence") or {}).get(k))
            and bool((r.get("annotation_reference_presence") or {}).get(p))
        )
        n_drop = n_prod - n_pres
        field_stats["fields"][field] = {
            "producer_has": n_prod,
            "adapter_preserves_position_or_role": n_pres,
            "adapter_drops": n_drop,
        }
    # clarify preserves for explanation uses role not position
    field_stats["notes"] = {
        "preserves_definition": "adapter_preserves = producer has field AND adapter emits corresponding position (explanation: role only, by adapter design)",
        "code_evidence_adapter_drop_material": "annotation_adapter.py:131-132 if unit.material_lines: shared['material']={'role':'material'}",
        "code_evidence_manifest_parses": "manifest_reader.py:51,96-107 material_lines/stem_lines/options/answer_lines/explanation_lines parsed into ManifestUnit",
    }
    (OUT / "producer_adapter_ir_field_stats.json").write_text(
        json.dumps(field_stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    attr = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "ir_ready": stats.get("ir_ready", 0),
        "ir_not_ready": stats.get("ir_not_ready", 0),
        "primary_reason_distribution": {
            k.replace("primary_", ""): v for k, v in loss_attr.items() if k.startswith("primary_")
        },
        "attribution": {
            "reference_loss_attributable": loss_attr.get("reference_loss_attributable", 0),
            "reference_loss_partial": loss_attr.get("reference_loss_partial", 0),
            "no_reference_loss": loss_attr.get("no_reference_loss", 0),
        },
        "primary_reason_rule": (
            "priority order: material_missing_or_incomplete > answer_missing > answer_ambiguous > "
            "option_incomplete > option_ambiguous > stem_missing > stem_ambiguous > group_related > other"
        ),
        "causality_note": (
            "reference_loss_attributable = not-ready AND adapter_reference_loss_any AND primary in "
            "{material/answer/option/stem missing/incomplete/ambiguous family}; "
            "this is co-occurrence + code-path evidence, not a counterfactual. "
            "Counterfactual handled in controlled_position_injection.json"
        ),
    }
    (OUT / "ir_loss_attribution.json").write_text(
        json.dumps(attr, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("census units", len(rows_out))
    print("stats", dict(stats))
    print("loss_attr", dict(loss_attr))
    return rows_out


def controlled_injection() -> dict:
    """Harness-only: rebuild annotation payload with producer positions injected into role dicts.
    Does NOT modify adapter/resolver/IR source. Compares IR Ready A (as-is payload) vs B (injected).
    """
    import asyncio

    from app.db.session import async_session_maker

    def inject_positions(payload: dict, man: Manifest | None) -> dict:
        if man is None:
            return payload
        man_by_id = {u.unit_id: u for u in man.units}
        out = json.loads(json.dumps(payload))  # deep copy via json
        for au in out.get("semantic_units") or []:
            uid = au.get("unit_id")
            mu = man_by_id.get(uid)
            if not mu:
                continue
            is_comp = au.get("unit_type") == "composite_unit"
            if is_comp:
                shared = au.setdefault("shared_components", {})
                if mu.material_lines:
                    shared["material"] = {
                        "role": "material",
                        "start_line": mu.material_lines[0],
                        "end_line": mu.material_lines[1],
                    }
                content = ((au.get("sub_questions") or [{}])[0].get("content") or {})
            else:
                content = au.get("content") or {}
            if mu.stem_lines and isinstance(content.get("stem"), dict):
                content["stem"]["start_line"] = mu.stem_lines[0]
                content["stem"]["end_line"] = mu.stem_lines[1]
            if mu.answer_lines and isinstance(content.get("answer"), dict):
                content["answer"]["start_line"] = mu.answer_lines[0]
                content["answer"]["end_line"] = mu.answer_lines[1]
            if mu.options and isinstance(content.get("options"), list):
                by_lab = {o.label: o for o in mu.options}
                for opt in content["options"]:
                    lab = opt.get("label")
                    if lab in by_lab:
                        opt["start_line"] = by_lab[lab].start_line
                        opt["end_line"] = by_lab[lab].end_line
            if is_comp and (au.get("sub_questions") or []):
                au["sub_questions"][0]["content"] = content
            else:
                au["content"] = content
        return out

    async def _run():
        corpus_root = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
        man_by_md = {}
        for p in find_manifests(corpus_root):
            m = load_manifest(p)
            man_by_md[Path(m.source_file).name] = m

        a_ready = b_ready = total = 0
        per_doc = []
        async with async_session_maker() as s:
            r = await s.execute(
                text(
                    """
                    select sv.id, sv.document_id, sa.id, sa.payload, d.file_name
                    from document_source_versions sv
                    join semantic_annotations sa on sa.source_version_id = sv.id
                    join documents d on d.id = sv.document_id
                    where sv.status='sealed'
                    """
                )
            )
            for sv_id, doc_id, ann_id, payload, fname in r.fetchall():
                if isinstance(payload, str):
                    payload = json.loads(payload)
                man = man_by_md.get(fname)
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

                def count_ready(p):
                    run = SourceResolver(source_version_id=sv_id, lines=lines, figures=figures).resolve(p)
                    ir = IRBuilder().build(
                        resolved_run=run,
                        annotation_payload=p,
                        source_version_id=sv_id,
                        annotation_id=ann_id,
                    )
                    return sum(1 for n in ir.units if n.semantic_status == "ready"), len(ir.units), run

                a_r, n_units, _ = count_ready(payload)
                injected = inject_positions(payload, man)
                b_r, _, _ = count_ready(injected)
                total += n_units
                a_ready += a_r
                b_ready += b_r
                per_doc.append(
                    {
                        "file_name": fname,
                        "source_version_id": str(sv_id),
                        "units": n_units,
                        "ir_ready_A_as_is": a_r,
                        "ir_ready_B_position_injected": b_r,
                    }
                )
        return {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "git_binding": GIT_BINDING,
            "experiment": (
                "harness-only deep-copy of annotation payload with producer line refs injected "
                "into role dicts; SourceResolver/IRBuilder/Adapter/Resolver source NOT modified"
            ),
            "not_a_production_run": True,
            "writes_to_db": False,
            "total_units": total,
            "ir_ready_A_as_is": a_ready,
            "ir_ready_B_position_injected": b_ready,
            "delta_B_minus_A": b_ready - a_ready,
            "interpretation_rule": {
                "B_significantly_gt_A": "Q8 REQUIRED (LEVEL 2 interface) has empirical support",
                "B_approx_A": "positions are not the main cause; Q8 NOT REQUIRED for this mechanism",
            },
            "per_document": per_doc,
        }

    res = asyncio.run(_run())
    (OUT / "controlled_position_injection.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print("CONTROLLED", {k: res[k] for k in ("total_units", "ir_ready_A_as_is", "ir_ready_B_position_injected", "delta_B_minus_A")})
    return res


if __name__ == "__main__":
    build_census()
    controlled_injection()
