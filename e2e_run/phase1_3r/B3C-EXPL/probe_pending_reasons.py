"""Read-only: is 219/226 pending_review a HUMAN-CAPACITY fact, or a GATE-layer fact?

If pending is driven by one dominant, structural layer (e.g. answer grammar), then
a Review Console automates around the symptom instead of fixing the cause.
This censuses the actual reasons behind every pending_review decision.
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
    reason_kind = Counter()
    per_layer = Counter()
    auto_allowed_false_only = 0
    pending_total = 0
    sample = []
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
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {l.line_ref: l for l in srs}).compile(ir)
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            ds = g.get("decision")
            if ds != "pending_review":
                continue
            pending_total += 1
            reasons = []
            layers = g.get("layers") or {}
            for layer in ("structural", "provenance", "semantic", "admission"):
                sec = layers.get(layer) or {}
                if sec.get("status") == "fail":
                    per_layer[layer] += 1
                for r in sec.get("reasons") or []:
                    reasons.append((layer, r))
            for r in g.get("reasons") or []:
                reasons.append(("admission", r))
            auto_ok = ((layers.get("provenance") or {}).get("auto_allowed"))
            if not reasons and auto_ok is False:
                auto_allowed_false_only += 1
            for layer, r in reasons:
                # bucket by a coarse kind
                if "not expressible" in r:
                    kind = "answer_not_expressible"
                elif "type not strict auto" in r or "strict auto" in r:
                    kind = "type_not_strict_auto"
                elif "not byte proven" in r or "byte_proven" in r:
                    kind = "not_byte_proven"
                elif "role provenance violation" in r:
                    kind = "role_provenance_violation"
                elif "contextual" in r or "resolution" in r:
                    kind = "resolution_not_exact"
                elif "duplicate" in r:
                    kind = "duplicate_span"
                else:
                    kind = r[:46]
                reason_kind[(layer, kind)] += 1
            if len(sample) < 6:
                sample.append({"paper": p.parent.name, "unit": root.unit_id,
                               "auto_allowed": auto_ok,
                               "reasons": [f"{l}:{r}"[:120] for l, r in reasons]})

    print(f"pending_review total = {pending_total}")
    print(f"pending with NO reasons but auto_allowed=False = {auto_allowed_false_only}")
    print("\n=== failed layers among pending ===")
    for k, v in per_layer.most_common():
        print(f"  {k:<14} {v}")
    print("\n=== reason kinds among pending ===")
    for (layer, kind), n in reason_kind.most_common(20):
        print(f"  {n:>5}  [{layer}] {kind}")
    print("\n=== samples ===")
    for s in sample:
        print(f"  {s['paper']}/{s['unit']} auto_allowed={s['auto_allowed']}")
        for r in s["reasons"]:
            print(f"      {r}")

    (OUT / "verify_pending_reasons.json").write_text(
        json.dumps({"pending_total": pending_total,
                    "failing_layers": dict(per_layer),
                    "reason_kinds": {f"{l}|{k}": v for (l, k), v in reason_kind.items()},
                    "samples": sample}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_pending_reasons.json'}")


if __name__ == "__main__":
    main()
