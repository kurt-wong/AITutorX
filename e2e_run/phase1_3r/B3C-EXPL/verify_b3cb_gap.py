"""Read-only: reconcile the B3c-B population post-fix and measure the gap MIMO
reported (decoded-but-not-auto_approve = 31).

For every leaf: qtype, whether answer is a valid table-derived token, whether it
auto-approves, and if not WHY (which other role blocks it).
"""
from __future__ import annotations

import json
import os
import re
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
from app.domains.gate.grammar import verify  # noqa: E402
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
    tot = Counter()
    blockers = Counter()
    decoded_not_auto = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
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

        auto_ids = set()
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if g.get("decision") == "auto_approve":
                auto_ids.add(root.unit_id)

        for leaf in compiled.leaves:
            ans = leaf.answer
            tok = (ans.text if ans else "") or ""
            valid = verify(leaf.canonical_question_type, tok,
                           tuple(str(o.label) for o in leaf.options if o.label)) is True
            if not valid or not tok or len(tok) > 3:
                continue
            # a short valid token => derived from structured evidence (or plain prose)
            ev = " ".join(getattr(ans, "evidence", ()) or ())
            from_table = "structured_answer_table" in ev or "table" in ev.lower()
            tot["short_valid_total"] += 1
            if from_table:
                tot["token_from_table"] += 1
            owner = leaf.unit_id[:-4] if leaf.unit_id.endswith(".sub") else leaf.unit_id
            parent_auto = owner in auto_ids
            leaf_ready = leaf.unit_id in auto_ids
            if from_table:
                if parent_auto:
                    tot["table_token_auto_approve"] += 1
                else:
                    tot["table_token_NOT_auto"] += 1
                    # why? inspect the owner IR node
                    node = next((u for u in ir.units if u.unit_id == owner), None)
                    why = []
                    if node is not None:
                        if node.semantic_status != "ready":
                            why.append(f"IR {node.semantic_status}")
                            for s in node.sub_questions:
                                for c in s.content:
                                    if c.span_id is None:
                                        why.append(f"sub role {c.role} unresolved")
                            for c in node.shared_components:
                                if c.span_id is None:
                                    why.append(f"shared {c.role} unresolved")
                        else:
                            g = evaluate(root=node, ir=ir, compiled=compiled, resolved_run=run)
                            why.append(f"gate {g.get('decision')}")
                            for r in (g.get("reasons") or [])[:2]:
                                why.append(r[:70])
                    for w in why:
                        blockers[w] += 1
                    if len(decoded_not_auto) < 10:
                        decoded_not_auto.append({"paper": paper, "unit": leaf.unit_id,
                                                 "qn_owner": owner, "why": why})

    print("TOTALS:", json.dumps(dict(tot), ensure_ascii=False))
    print("\nblockers for table-derived tokens that are NOT auto_approve:")
    for k, v in blockers.most_common(12):
        print(f"   {v:>4}  {k}")
    print("\nsamples:")
    for d in decoded_not_auto:
        print(f"   {d['paper']}/{d['unit']} owner={d['qn_owner']} why={d['why']}")

    (OUT / "verify_b3cb_gap.json").write_text(
        json.dumps({"totals": dict(tot), "blockers": dict(blockers),
                    "samples": decoded_not_auto}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_b3cb_gap.json'}")


if __name__ == "__main__":
    main()
