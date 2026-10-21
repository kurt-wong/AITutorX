"""Independent verification of MIMO's Phase 1 E2E Replay.

Read-only. For all 9 papers / 284 units computes:
  - IR ready / incomplete  (top-level unit status AND leaf status)
  - Gate decision per unit via the REAL GatePolicy.evaluate (no DB write)
  - decision_status census, rejected reasons, auto_approve count
  - leaf-level reason-kind census

Purpose: (a) reconcile MIMO's 226 against my earlier 219; (b) test whether the
per-paper Gate table MIMO published actually sums to 226.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

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


def main() -> None:
    rows = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid, aid = uuid.uuid4(), uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, aid)
        compiled = Compiler(
            {s.span_id: s for s in run.resolved_spans},
            {l.line_ref: l for l in srs},
        ).compile(ir)

        dec = Counter()
        reasons = Counter()
        n_top_ready = 0
        n_leaf_ready = 0
        n_leaf = 0
        for root in ir.units:
            if root.semantic_status == "ready":
                n_top_ready += 1
            leaves = list(root.sub_questions) if root.unit_type == "composite_unit" else [root]
            for s in leaves:
                n_leaf += 1
                if s.semantic_status == "ready":
                    n_leaf_ready += 1
            # gate only for ready top-level units (service.py:178)
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            ds = g.get("decision_status") or g.get("decision") or "?"
            dec[ds] += 1
            for layer in ("structural", "provenance", "semantic", "admission"):
                for r in (g.get(layer) or {}).get("reasons") or []:
                    reasons[r] += 1

        rows.append({
            "paper": p.parent.name,
            "units": len(ir.units),
            "top_ready": n_top_ready,
            "top_incomplete": len(ir.units) - n_top_ready,
            "leaf_ready": n_leaf_ready,
            "leaves": n_leaf,
            "gate": dict(dec),
        })

    print(f"{'paper':<6}{'units':>6}{'topRdy':>7}{'topInc':>7}{'leafRdy':>8}{'leaves':>7}"
          f"   gate")
    for r in rows:
        print(f"{r['paper']:<6}{r['units']:>6}{r['top_ready']:>7}{r['top_incomplete']:>7}"
              f"{r['leaf_ready']:>8}{r['leaves']:>7}   {r['gate']}")

    t = Counter()
    for r in rows:
        t["units"] += r["units"]
        t["top_ready"] += r["top_ready"]
        t["top_incomplete"] += r["top_incomplete"]
        t["leaf_ready"] += r["leaf_ready"]
        t["leaves"] += r["leaves"]
        for k, v in r["gate"].items():
            t[f"gate_{k}"] += v
    print("\nTOTALS:", json.dumps(dict(t), ensure_ascii=False))
    gate_sum = sum(v for k, v in t.items() if k.startswith("gate_"))
    print(f"gate decision sum = {gate_sum}   (compare: top_ready={t['top_ready']})")

    (OUT / "verify_e2e_replay.json").write_text(
        json.dumps({"rows": rows, "totals": dict(t), "gate_sum": gate_sum},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"written: {OUT / 'verify_e2e_replay.json'}")


if __name__ == "__main__":
    main()
