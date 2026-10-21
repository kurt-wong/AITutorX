"""Read-only: how actionable is the taxonomy WITHOUT any human labelling?

MIMO argues human labels are needed to reach actionable granularity
("Producer segment loss"). Test that for the one bucket we never broke down:
  gate-only (IR ready but Gate != auto_approve)  -- claimed 19/21

If Gate *reasons* already resolve into distinct actionable causes deterministically,
then the residual needing human judgement is much smaller than claimed.
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


def classify(reason: str) -> str:
    if "not expressible as canonical value" in reason:
        return "ANSWER_GRAMMAR:not_expressible"
    if "not strict-auto" in reason:
        return "QUESTION_TYPE:not_strict_auto"
    if "not source_located+complete" in reason:
        return "ANSWER_STATE:not_located_or_incomplete"
    if "not byte-proven" in reason:
        return "SPAN:resolution_not_exact_normalized"
    if "role provenance violation" in reason:
        return "PROVENANCE:role_region_overlap"
    if "answer grammar" in reason:
        return "ANSWER_GRAMMAR:other"
    return "OTHER:" + reason[:40]


def main() -> None:
    kinds = Counter()
    per_paper = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=p.page_no if False else s.page_no,
                                     line_no_in_page=s.line_no_in_page) for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid, aid = uuid.uuid4(), uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, aid)
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {l.line_ref: l for l in srs}).compile(ir)
        c = Counter()
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            d = g.get("decision")
            if d == "auto_approve":
                continue
            c[f"gate_{d}"] += 1
            if d == "pending_review":
                seen = set()
                for r in (g.get("reasons") or []):
                    k = classify(r)
                    if k not in seen:
                        seen.add(k)
                        c[f"  kind:{k}"] += 1
        per_paper[paper] = dict(c)
        kinds.update(c)

    print("GATE non-auto breakdown by paper:")
    for paper, c in per_paper.items():
        gate = {k: v for k, v in c.items() if k.startswith("gate_")}
        print(f"  {paper:<6} {gate}")
    print("\nGLOBAL reason-kind census (pending_review, deduped per root):")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        if k.startswith("  kind:"):
            print(f"   {v:>5}  {k[7:]}")
    print("\nGLOBAL gate totals:")
    for k, v in sorted(kinds.items()):
        if k.startswith("gate_"):
            print(f"   {k:<24} {v}")

    (OUT / "gate_only_breakdown.json").write_text(
        json.dumps({"per_paper": per_paper, "global": dict(kinds)},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'gate_only_breakdown.json'}")


if __name__ == "__main__":
    main()
