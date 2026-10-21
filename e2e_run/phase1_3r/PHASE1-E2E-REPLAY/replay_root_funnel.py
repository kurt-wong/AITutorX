# -*- coding: utf-8 -*-
"""Root-level funnel after material scope constraint (all papers)."""
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
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
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


def measure(path: Path) -> dict:
    m = load_manifest(path)
    srs = load_source_lines(Path(m.source_file))
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload,
        {u.unit_id: u.material_lines for u in m.units if u.material_lines},
        [s.text for s in srs],
    )
    sv_id = uuid.uuid4()
    run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
    line_map = {v.line_ref: v for v in views}
    span_map = {s.span_id: s for s in run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(ir)

    root_status = Counter()
    mat_status = Counter()
    gate = Counter()
    leaf_ready_root_blocked = 0
    mat_unres = 0
    mat_ok = 0
    details = []

    for n in ir.units:
        root_status[n.semantic_status] += 1
        is_comp = n.unit_type == "composite_unit"
        mat_id = f"sp-{n.unit_id}.material"
        has_mat = is_comp and any(c.role == "material" for c in n.shared_components)
        mat_resolved = any(
            c.role == "material" and c.span_id for c in n.shared_components
        )
        if is_comp:
            if mat_resolved:
                mat_status["resolved"] += 1
                mat_ok += 1
            else:
                mat_status["unresolved"] += 1
                mat_unres += 1
        subs = list(n.sub_questions) if is_comp else [n]
        sub_ready = all(s.semantic_status == "ready" for s in subs)
        if is_comp and sub_ready and n.semantic_status != "ready" and not mat_resolved:
            leaf_ready_root_blocked += 1

        if n.semantic_status == "ready":
            d = evaluate(root=n, ir=ir, compiled=compiled, resolved_run=run)
            gate[d.get("decision") or "?"] += 1
        details.append({
            "unit": n.unit_id,
            "type": n.unit_type,
            "root": n.semantic_status,
            "mat": "ok" if mat_resolved else ("unres" if is_comp else "-"),
            "subs_ready": sub_ready,
        })

    return {
        "paper": path.parent.name,
        "units": len(m.units),
        "root_status": dict(root_status),
        "mat": dict(mat_status),
        "gate": dict(gate),
        "leaf_ready_root_blocked_by_mat": leaf_ready_root_blocked,
        "mat_ok": mat_ok,
        "mat_unres": mat_unres,
        "details": details,
    }


def main() -> None:
    papers = [measure(p) for p in find_manifests(CORPUS)]
    tot_root = Counter()
    tot_gate = Counter()
    tot_mat = Counter()
    tot_blocked = 0
    for p in papers:
        tot_root.update(p["root_status"])
        tot_gate.update(p["gate"])
        tot_mat.update(p["mat"])
        tot_blocked += p["leaf_ready_root_blocked_by_mat"]

    report = {
        "cut": "Material boundary marker scope constraint",
        "root_funnel": {
            "root_status": dict(tot_root),
            "gate": dict(tot_gate),
            "mat": dict(tot_mat),
            "leaf_ready_root_blocked_by_mat": tot_blocked,
        },
        "per_paper": papers,
    }
    out = OUT / "phase1_root_after_mat_scope.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("ROOT status:", dict(tot_root))
    print("ROOT gate:  ", dict(tot_gate))
    print("MAT:        ", dict(tot_mat))
    print("leaf-ready root blocked by mat:", tot_blocked)
    print()
    for p in papers:
        print(f"  {p['paper']:8} root={p['root_status']} mat={p['mat']} "
              f"gate={p['gate']} blocked={p['leaf_ready_root_blocked_by_mat']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
