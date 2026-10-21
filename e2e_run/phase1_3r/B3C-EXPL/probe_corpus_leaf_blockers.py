"""Read-only: corpus-wide impact of the 'choice requires options' rule.

Determines whether 'options missing for choice type' is a real production blocker
and how many units across the 9-paper corpus it affects (not just 地理).
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

from app.domains.compile import content_roles_for, map_canonical_type  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
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
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        svid = uuid.uuid4()
        run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, uuid.uuid4())

        def leaf_problems(s):
            probs = []
            canon = map_canonical_type(s.original_question_type)
            req = content_roles_for(canon)
            by_role = {c.role: c for c in s.content}
            if req.get("stem") == "required":
                c = by_role.get("stem")
                if c is None:
                    probs.append("stem_not_declared")
                elif c.span_id is None:
                    probs.append("stem_unresolved")
            if req.get("answer") == "required":
                c = by_role.get("answer")
                if c is None:
                    probs.append("answer_not_declared")
                elif c.span_id is None:
                    probs.append("answer_unresolved")
            if req.get("options") == "required_for_choice":
                if not any(c.role == "option" for c in s.content):
                    probs.append("options_missing_for_choice")
            return probs

        agg = Counter()
        for u in ir.units:
            leaves = list(u.sub_questions) if u.unit_type == "composite_unit" else [u]
            for s in leaves:
                for pr in leaf_problems(s):
                    agg[pr] += 1
        rows.append({
            "paper": p.parent.name,
            "units": len(ir.units),
            "ir_ready": sum(1 for u in ir.units if u.semantic_status == "ready"),
            "ir_incomplete": sum(1 for u in ir.units if u.semantic_status != "ready"),
            "leaf_problems": dict(agg),
            "options_declared_units": sum(1 for u in m.units if u.options),
            "stem_lines_units": sum(1 for u in m.units if u.stem_lines),
            "options_lines_units": sum(1 for u in m.units if u.options_lines),
        })

    hdr = (f"{'paper':<6}{'units':>6}{'ready':>7}{'inc':>5}{'optDecl':>8}"
           f"{'stemL':>7}{'optL':>6}  leaf-problems")
    print(hdr)
    for r in rows:
        print(f"{r['paper']:<6}{r['units']:>6}{r['ir_ready']:>7}{r['ir_incomplete']:>5}"
              f"{r['options_declared_units']:>8}{r['stem_lines_units']:>7}"
              f"{r['options_lines_units']:>6}  {r['leaf_problems']}")

    tot = Counter()
    for r in rows:
        tot["units"] += r["units"]
        tot["ir_ready"] += r["ir_ready"]
        for k, v in r["leaf_problems"].items():
            tot[k] += v
    print("\nCORPUS TOTALS:", json.dumps(dict(tot), ensure_ascii=False))

    (OUT / "corpus_leaf_blockers.json").write_text(
        json.dumps({"rows": rows, "totals": dict(tot)}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"written: {OUT / 'corpus_leaf_blockers.json'}")


if __name__ == "__main__":
    main()
