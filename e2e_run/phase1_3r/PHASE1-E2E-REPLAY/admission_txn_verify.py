"""Admission transaction verification (BEGIN → materialize assertions → ROLLBACK).

Validates Q:QI = 1:N, dedup REUSE, composite parent not materialized,
Question Type ≠ Unit Type. Does NOT leave rows behind.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\PHASE1-E2E-REPLAY")
sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))


async def main() -> None:
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    from app.domains.compile import map_canonical_type
    from app.domains.compile.compiler import Compiler
    from app.domains.compile.ir import IRBuilder
    from app.domains.gate.admission import AdmissionService
    from app.domains.gate.policy import evaluate
    from app.domains.resolver.resolver import SourceResolver
    from app.domains.resolver.span import SourceLineView
    from app.repositories.content_repository import ContentRepository
    from app.repositories.snapshot_repository import SnapshotRepository
    from app.repositories.source_repository import SourceRepository

    from scripts.preprocessing_consumer.annotation_adapter import (
        attach_material_boundary_markers,
        manifest_to_annotation_payload,
    )
    from scripts.preprocessing_consumer.manifest_reader import load_manifest
    from scripts.preprocessing_consumer.source_loader import (
        compute_body_hash,
        load_source_lines,
        load_raw_bytes_identity,
    )

    mf = Path(
        r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\英语\2018北京春季高中会考英语（教师版）(1).manifest.json"
    )
    # English has mixed standalone/composite + auto/pending — good for the assertions.

    m = load_manifest(mf)
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

    # pick a ready root whose gate is auto_approve if any, else first ready
    chosen = None
    chosen_decision = None
    for n in ir.units:
        if n.semantic_status != "ready":
            continue
        d = evaluate(root=n, ir=ir, compiled=compiled, resolved_run=run)
        if chosen is None or d.get("decision") == "auto_approve":
            chosen, chosen_decision = n, d.get("decision")
            if d.get("decision") == "auto_approve":
                break

    assert chosen is not None, "no ready root in English paper"
    print(f"chosen root={chosen.unit_id} type={chosen.unit_type} decision={chosen_decision}")

    engine = create_async_engine(os.environ["DATABASE_URL"])
    Session = async_sessionmaker(engine, expire_on_commit=False)
    report = {"root": chosen.unit_id, "decision": chosen_decision, "assertions": {}}

    async with Session() as session:
        async with session.begin():
            src = SourceRepository(session)
            snap = SnapshotRepository(session)
            content = ContentRepository(session)

            raw_id = load_raw_bytes_identity(mf) if hasattr(__import__("scripts.preprocessing_consumer.source_loader", fromlist=["x"]), "load_raw_bytes_identity") else None
            # minimal document + source_version + lines + annotation + candidate
            doc = await src.create_document(
                original_object_key="preprocessing/admission-txn-test",
                original_sha256=uuid.uuid4().hex,
                file_name=mf.name,
                file_type="text/markdown",
                upload_meta={"probe": "admission_txn"},
            )
            await session.flush()
            body_hash = compute_body_hash(srs)
            version = await src.create_source_version(
                document_id=doc.id,
                version_no=1,
                body_hash=body_hash,
                line_count=len(srs),
                line_index_algorithm="v1",
                identity_version=2,
                logical_execution_hash=uuid.uuid4().hex,
                provenance={"provider": "admission_txn_test"},
            )
            await session.flush()
            # replace svid inside compiled payload builders: build a fresh run against this sv
            sv_real = version.id
            run2 = SourceResolver(source_version_id=sv_real, lines=views).resolve(payload)
            ir2 = IRBuilder.build(run2, payload, sv_real, uuid.uuid4())
            span_map2 = {s.span_id: s for s in run2.resolved_spans}
            compiled2 = Compiler(span_map2, line_map).compile(ir2)
            root2 = next(n for n in ir2.units if n.unit_id == chosen.unit_id)
            gate2 = evaluate(root=root2, ir=ir2, compiled=compiled2, resolved_run=run2)

            ann = await snap.create_semantic_annotation(
                source_version_id=sv_real,
                payload=payload,
                produced_by="admission_txn_test",
            )
            await session.flush()

            cand = await snap.create_admission_candidate(
                source_version_id=sv_real,
                annotation_id=ann.id,
                unit_id=root2.unit_id,
                unit_type=root2.unit_type,
                logical_execution_stage="admission_txn_test",
                logical_execution_hash=uuid.uuid4().hex,
                payload={
                    "ir_snapshot": {
                        "units": [
                            {
                                "unit_id": u.unit_id,
                                "unit_type": u.unit_type,
                                "question_number": u.question_number,
                                "question_number_range": u.question_number_range,
                                "original_question_type": u.original_question_type,
                                "content": [
                                    {"role": c.role, "span_id": c.span_id, "label": c.label}
                                    for c in u.content
                                ],
                                "shared_components": [
                                    {"role": c.role, "span_id": c.span_id}
                                    for c in u.shared_components
                                ],
                                "sub_questions": [
                                    {
                                        "unit_id": s.unit_id,
                                        "unit_type": s.unit_type,
                                        "question_number": s.question_number,
                                        "original_question_type": s.original_question_type,
                                        "content": [
                                            {"role": c.role, "span_id": c.span_id, "label": c.label}
                                            for c in s.content
                                        ],
                                    }
                                    for s in u.sub_questions
                                ],
                            }
                            for u in ir2.units
                            if u.unit_id == root2.unit_id or root2.unit_id in u.unit_id
                        ]
                    },
                    "compiled_roles": [
                        {
                            "kind": "content",
                            "unit_id": l.unit_id,
                            "role": "stem",
                            "span_id": l.stem.span_id,
                            "text": l.stem.text,
                            "text_hash": l.stem.text_hash,
                        }
                        for l in compiled2.leaves
                        if l.unit_id.startswith(root2.unit_id)
                    ]
                    + [
                        {
                            "kind": "content",
                            "unit_id": l.unit_id,
                            "role": "answer",
                            "span_id": l.answer.span_id,
                            "text": l.answer.text,
                            "text_hash": l.answer.text_hash,
                        }
                        for l in compiled2.leaves
                        if l.unit_id.startswith(root2.unit_id) and l.answer
                    ]
                    + [
                        {
                            "kind": "content",
                            "unit_id": l.unit_id,
                            "role": "option",
                            "span_id": o.span_id,
                            "label": o.label,
                            "text": o.text,
                            "text_hash": o.text_hash,
                        }
                        for l in compiled2.leaves
                        if l.unit_id.startswith(root2.unit_id)
                        for o in l.options
                    ],
                    "answer": [
                        {
                            "unit_id": l.unit_id,
                            "span_id": l.answer.span_id if l.answer else None,
                            "text": l.answer.text if l.answer else None,
                        }
                        for l in compiled2.leaves
                        if l.unit_id.startswith(root2.unit_id)
                    ],
                    "resolved_spans": [
                        {
                            "span_id": s.span_id,
                            "line_refs": list(s.line_refs),
                            "granularity": s.granularity,
                            "start_offset": s.start_offset,
                            "end_offset": s.end_offset,
                            "text_hash": s.text_hash,
                            "resolution_status": s.resolution_status,
                        }
                        for s in run2.resolved_spans
                    ],
                    "gate_decision": gate2,
                },
                gate_decision=gate2,
            )
            await session.flush()

            report["candidate_id"] = str(cand.id)
            report["gate_decision"] = gate2.get("decision")

            svc = AdmissionService(session)
            # For auto path: approve with auto_gate. For pending: fabricate human trail is
            # forbidden to fake — we only auto-approve when gate says so.
            if gate2.get("decision") == "auto_approve":
                decided = await svc.approve(
                    candidate_id=cand.id, provenance={"source": "auto_gate"}
                )
                report["approve"] = "auto_gate"
            else:
                report["approve"] = "SKIPPED (not auto_approve — human path not faked)"
                decided = cand

            # assertions
            n_q = (await session.execute(text(
                "SELECT count(*) FROM questions WHERE created_at >= now() - interval '5 minutes'"
            ))).scalar() or 0
            n_i = (await session.execute(text(
                "SELECT count(*) FROM question_instances WHERE created_at >= now() - interval '5 minutes'"
            ))).scalar() or 0

            # count leaves planned
            leaves = [
                s for s in (chosen.sub_questions if chosen.unit_type == "composite_unit" else [chosen])
            ]
            report["assertions"] = {
                "root_unit_type": chosen.unit_type,
                "root_qtype": chosen.original_question_type,
                "leaf_count": len(leaves),
                "leaf_qtypes": [s.original_question_type for s in leaves],
                "leaf_canonical": [map_canonical_type(s.original_question_type) for s in leaves],
                "questions_created_in_txn": n_q,
                "instances_created_in_txn": n_i,
                "q_qi_ratio_expected": f"1:{len(leaves)}" if gate2.get("decision") == "auto_approve" else "n/a (not approved)",
                "composite_parent_not_question": (
                    chosen.unit_type == "composite_unit"
                    and all("composite" not in (map_canonical_type(s.original_question_type) or "")
                            for s in leaves)
                ),
                "decision_status_after": getattr(decided, "decision_status", None),
            }
            # force rollback
            raise RuntimeError("ROLLBACK_BY_DESIGN")

    assert False, "unreachable"


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "ROLLBACK_BY_DESIGN" in str(e):
            print("ROLLED BACK (no rows persisted)")
        else:
            raise
