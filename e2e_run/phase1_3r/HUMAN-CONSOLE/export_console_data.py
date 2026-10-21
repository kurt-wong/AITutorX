"""Export Human Verification Console dataset (read-only)."""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\HUMAN-CONSOLE")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver, decode_answer_table_cell  # noqa: E402
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


def span_row(span, line_map):
    if span is None:
        return None
    texts = []
    for ref in span.line_refs[:6]:
        ln = line_map.get(ref)
        texts.append((ln.text if ln else "")[:160])
    ev = list(span.evidence)
    structured = None
    for e in ev:
        if e == "structured_answer_table":
            structured = {}
        elif structured is not None and isinstance(e, str) and "=" in e:
            k, _, v = e.partition("=")
            structured[k] = v
    return {
        "span_id": span.span_id,
        "role": span.role,
        "granularity": span.granularity,
        "line_refs": list(span.line_refs),
        "start_offset": span.start_offset,
        "end_offset": span.end_offset,
        "resolution_status": span.resolution_status,
        "evidence": ev,
        "structured_table": structured,
        "preview": texts,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    items = []
    counts = {"auto_approve": 0, "pending_review": 0, "rejected": 0, "ir_incomplete": 0}

    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        line_map = {v.line_ref: v for v in views}
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
        )
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        compiled = Compiler(span_map, line_map).compile(ir)

        for root in ir.units:
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            # pick first leaf with answer for detail
            detail_leaf = None
            for leaf in leaves:
                if any(c.role == "answer" and c.span_id for c in leaf.content):
                    detail_leaf = leaf
                    break
            if detail_leaf is None and leaves:
                detail_leaf = leaves[0]

            evidence = {}
            for role in ("stem", "answer", "explanation"):
                c = next((x for x in detail_leaf.content if x.role == role), None)
                evidence[role] = span_row(span_map.get(c.span_id) if c else None, line_map)
            evidence["options"] = [
                span_row(span_map.get(c.span_id), line_map)
                for c in detail_leaf.content if c.role == "option"
            ]
            evidence["material"] = [
                span_row(span_map.get(c.span_id), line_map)
                for c in root.shared_components if c.role == "material"
            ]

            if root.semantic_status != "ready":
                decision = "ir_incomplete"
                counts["ir_incomplete"] += 1
                gate_reasons = []
            else:
                d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                decision = d.get("decision") or "?"
                counts[decision] = counts.get(decision, 0) + 1
                gate_reasons = (d.get("reasons") or [])[:8]

            ans_ev = evidence.get("answer") or {}
            is_table = bool(ans_ev.get("structured_table"))
            cell = (ans_ev.get("structured_table") or {}).get("cell")

            items.append({
                "paper": p.parent.name,
                "root": root.unit_id,
                "unit_type": root.unit_type,
                "qtype": detail_leaf.original_question_type if detail_leaf else None,
                "qn": detail_leaf.question_number if detail_leaf else None,
                "decision": decision,
                "gate_reasons": gate_reasons,
                "is_table_answer": is_table,
                "cell": cell,
                "n_leaves": len(leaves),
                "leaf_ids": [l.unit_id for l in leaves],
                "evidence": evidence,
            })

    # pick display samples per Owner D-2
    def _pick(pred, n=3):
        return [i["root"] + "@" + i["paper"] for i in items if pred(i)][:n]

    samples = {
        "auto_approve": _pick(lambda i: i["decision"] == "auto_approve", 3),
        "pending_review": _pick(lambda i: i["decision"] == "pending_review", 3),
        "decoded_but_not_auto": _pick(
            lambda i: i["is_table_answer"] and i["decision"] != "auto_approve", 3
        ),
        "composite": _pick(lambda i: i["unit_type"] == "composite_unit", 3),
        "material": _pick(lambda i: bool(i["evidence"].get("material")), 3),
        "structured_table": _pick(lambda i: i["is_table_answer"], 3),
    }

    data = {
        "title": "Phase 1.4 Human Verification Console",
        "subtitle": "Read-only Evidence Viewer — no approve/reject/edit",
        "baseline": {
            "AITutors-v3": "54c2cc9+",
            "AITutors-preprocessing": "8377c56",
            "corpus": "会考 9 papers / 284 units",
        },
        "counts": counts,
        "samples": samples,
        "items": items,
    }
    (OUT / "console_data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print("counts", counts)
    print("items", len(items))
    print("samples", samples)
    print("wrote", OUT / "console_data.json")


if __name__ == "__main__":
    main()
