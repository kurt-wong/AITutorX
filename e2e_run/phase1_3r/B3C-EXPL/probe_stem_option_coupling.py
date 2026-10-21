"""Read-only: are the 'option unresolved' blockers a CONSEQUENCE of unresolved
stems, or independent?

For every table-decoded root that is NOT auto_approve and whose IR is incomplete,
print: stem resolved?, option resolved count, and the resolver's own reason.
If option blockers collapse into stem blockers, the "24 option" line in the
taxonomy is double-counting one cause.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter, defaultdict
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
    agg = Counter()
    reason = Counter()
    rows = []
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

        stem_ok = set()
        opt_cnt = Counter()
        for s in run.resolved_spans:
            if s.role == "stem" and s.span_id.endswith(".stem"):
                stem_ok.add(s.span_id[3:-5])
            if s.role == "option":
                opt_cnt[s.span_id[3:].rsplit(".option.", 1)[0]] += 1
        unres_opt = Counter()
        unres_stem = {}
        for u in run.unresolved_references:
            if u.role == "option":
                unres_opt[u.reference_id.rsplit(".option.", 1)[0]] += 1
            elif u.role == "stem":
                unres_stem[u.reference_id.rsplit(".stem", 1)[0]] = (
                    u.resolution_status, " / ".join(u.evidence))

        tbl = {s.span_id[3:].rsplit(".answer", 1)[0]
               for s in run.resolved_spans
               if "structured_answer_table" in " ".join(s.evidence or ())}
        auto = set()
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if g.get("decision") == "auto_approve":
                auto.add(root.unit_id)

        for owner in tbl:
            rid = owner[:-4] if owner.endswith(".sub") else owner
            if rid in auto:
                continue
            node = next((u for u in ir.units if u.unit_id == rid), None)
            if node is None or node.semantic_status == "ready":
                continue
            has_stem = owner in stem_ok
            n_opt = opt_cnt.get(owner, 0)
            n_unres = unres_opt.get(owner, 0)
            agg["roots"] += 1
            if not has_stem:
                agg["stem_missing"] += 1
            if n_unres:
                agg["option_unresolved"] += 1
                if not has_stem:
                    agg["option_unres_AND_stem_missing"] += 1
                else:
                    agg["option_unres_stem_ok"] += 1
            if not has_stem and n_unres:
                agg["stem_dep_covered"] += 1  # stem blocker explains option blocker
            st = unres_stem.get(owner)
            if st:
                reason[f"stem:{st[0]}:{st[1][:40]}"] += 1
            rows.append({"paper": paper, "root": rid, "owner": owner,
                         "stem_resolved": has_stem, "options_resolved": n_opt,
                         "options_unresolved": n_unres})

    print("AGGREGATE:", json.dumps(dict(agg), ensure_ascii=False, indent=2))
    print("\nstem unresolved reasons:")
    for k, v in reason.most_common(10):
        print(f"   {v:>4}  {k}")
    print("\nrows where option unresolved AND stem missing (stem explains option):")
    for r in rows:
        if r["options_unresolved"] and not r["stem_resolved"]:
            print(f"   {r['paper']}/{r['root']} opts_res={r['options_resolved']} "
                  f"opts_unres={r['options_unresolved']}")
    print("\nrows where option unresolved but stem IS resolved (independent):")
    for r in rows:
        if r["options_unresolved"] and r["stem_resolved"]:
            print(f"   {r['paper']}/{r['root']} opts_res={r['options_resolved']} "
                  f"opts_unres={r['options_unresolved']}")

    (OUT / "stem_option_coupling.json").write_text(
        json.dumps({"aggregate": dict(agg), "stem_reasons": dict(reason),
                    "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'stem_option_coupling.json'}")


if __name__ == "__main__":
    main()
