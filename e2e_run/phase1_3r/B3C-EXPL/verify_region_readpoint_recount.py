"""Read-only recount: of the 历史 answer spans that overlap the explanation region,
how many belong to units that ACTUALLY reach Gate.evaluate()?

service.py:177-180 -> only semantic_status == "ready" units become candidates
and get evaluate(). The published 52 was measured over ALL 53 answer spans.

Also confirms which regions exist simultaneously (both question AND explanation
active on 历史 => "answer in question region" and "answer in explanation region"
are mutually exclusive there).
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
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    out_rows = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        svid = uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, uuid.uuid4())

        region = {r.role: set(r.line_refs) for r in run.structural_regions}
        ready = {u.unit_id for u in ir.units if u.semantic_status == "ready"}
        notready = {u.unit_id for u in ir.units if u.semantic_status != "ready"}

        # map answer span -> owning unit via IR leaf answer.span_id
        span_to_unit: dict[str, str] = {}

        def walk(n):
            if n.unit_type == "composite_unit":
                for s in n.sub_questions:
                    walk(s)
                return
            for c in n.content:
                if c.role == "answer" and c.span_id:
                    span_to_unit[c.span_id] = n.unit_id

        for u in ir.units:
            walk(u)

        ans = [s for s in run.resolved_spans if s.role == "answer"]
        expl_reg = region.get("explanation", set())
        q_reg = region.get("question", set())

        viol_expl_all = [a for a in ans if set(a.line_refs) & expl_reg]
        viol_expl_ready = [a for a in viol_expl_all
                           if span_to_unit.get(a.span_id) in ready]
        viol_expl_notready = [a for a in viol_expl_all
                              if span_to_unit.get(a.span_id) in notready]
        # how many answer spans belong to units with NO IR leaf at all
        unmapped = [a for a in viol_expl_all if a.span_id not in span_to_unit]

        out_rows.append({
            "paper": p.parent.name,
            "region_roles": sorted(region),
            "ir_ready": len(ready),
            "ir_notready": len(notready),
            "answer_spans": len(ans),
            "viol_expl_all": len(viol_expl_all),
            "viol_expl_in_ready_units": len(viol_expl_ready),
            "viol_expl_in_notready_units": len(viol_expl_notready),
            "viol_expl_unmapped_span": len(unmapped),
            "viol_quest_all": sum(1 for a in ans if set(a.line_refs) & q_reg),
        })

    hdr = (f"{'paper':<6}{'roles':<26}{'ready':>7}{'notrdy':>8}{'ans':>5}"
           f"{'vExpl':>7}{'vExplRdy':>10}{'vExplNR':>9}{'vExplUnm':>10}{'vQst':>6}")
    print(hdr)
    for r in out_rows:
        print(f"{r['paper']:<6}{','.join(r['region_roles']):<26}"
              f"{r['ir_ready']:>7}{r['ir_notready']:>8}{r['answer_spans']:>5}"
              f"{r['viol_expl_all']:>7}{r['viol_expl_in_ready_units']:>10}"
              f"{r['viol_expl_in_notready_units']:>9}{r['viol_expl_unmapped_span']:>10}"
              f"{r['viol_quest_all']:>6}")

    tot = Counter()
    for r in out_rows:
        for k in ("ir_ready", "ir_notready", "answer_spans", "viol_expl_all",
                  "viol_expl_in_ready_units", "viol_expl_in_notready_units",
                  "viol_expl_unmapped_span", "viol_quest_all"):
            tot[k] += r[k]
    print("\nTOTALS:", json.dumps(dict(tot), ensure_ascii=False))

    (OUT / "region_readpoint_recount.json").write_text(
        json.dumps({"rows": out_rows, "totals": dict(tot)},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
