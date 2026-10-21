"""Read-only: exact gap between table-derived answers and auto_approve.

Uses the real provenance marker emitted by B3c-B:
    evidence contains 'structured_answer_table' and 'qn=<N>' and 'cell=<X>'
Counts:
    table_derived           (answer span carries the marker)
    table_derived_auto      (its owner root auto_approves)
    table_derived_not_auto  (decoded but blocked elsewhere) -> WHY
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
    tot = Counter()
    blockers = Counter()
    samples = []
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

        table_units = {}
        for s in run.resolved_spans:
            ev = " ".join(s.evidence or ())
            if "structured_answer_table" in ev:
                owner = s.span_id[3:].rsplit(".answer", 1)[0]
                qn = next((e.split("=", 1)[1] for e in s.evidence if e.startswith("qn=")), "?")
                cell = next((e.split("=", 1)[1] for e in s.evidence if e.startswith("cell=")), "?")
                table_units[owner] = (qn, cell)
        tot["table_derived_spans"] += len(table_units)

        auto_ids = set()
        decisions = {}
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            decisions[root.unit_id] = g.get("decision")
            if g.get("decision") == "auto_approve":
                auto_ids.add(root.unit_id)

        for owner, (qn, cell) in table_units.items():
            root_id = owner[:-4] if owner.endswith(".sub") else owner
            if root_id in auto_ids:
                tot["table_derived_auto"] += 1
            else:
                tot["table_derived_not_auto"] += 1
                node = next((u for u in ir.units if u.unit_id == root_id), None)
                why = []
                if node is not None:
                    if node.semantic_status != "ready":
                        why.append(f"IR={node.semantic_status}")
                        for s in node.sub_questions:
                            for c in s.content:
                                if c.span_id is None:
                                    why.append(f"sub.{c.role}=unresolved")
                        for c in node.shared_components:
                            if c.span_id is None:
                                why.append(f"shared.{c.role}=unresolved")
                    else:
                        why.append(f"gate={decisions.get(root_id)}")
                for w in (why or ["unknown"]):
                    blockers[w] += 1
                if len(samples) < 12:
                    samples.append({"paper": paper, "owner": owner, "qn": qn,
                                    "cell": cell, "root": root_id, "why": why})

    print("TOTALS:", json.dumps(dict(tot), ensure_ascii=False))
    print("\nblockers for table-derived-but-not-auto:")
    for k, v in blockers.most_common(15):
        print(f"   {v:>4}  {k}")
    print("\nsamples:")
    for s in samples:
        print(f"   {s['paper']}/{s['owner']} qn={s['qn']} cell={s['cell']} "
              f"root={s['root']} why={s['why']}")

    (OUT / "verify_b3cb_gap2.json").write_text(
        json.dumps({"totals": dict(tot), "blockers": dict(blockers),
                    "samples": samples}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_b3cb_gap2.json'}")


if __name__ == "__main__":
    main()
