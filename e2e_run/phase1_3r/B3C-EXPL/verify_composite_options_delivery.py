"""Independent verification of MIMO's composite-options delivery (873a343).

Runs the REAL Track A order on the BACKFILLED corpus and reports:
  - options declared (manifest)
  - option spans resolved (resolver)
  - IR option content + IR ready
  - remaining unresolved reasons

Also re-checks the two things the report claims but my earlier probes contradicted:
  - "material marker text missing" for all 地理 composite units
  - option spans collapsing onto one line (P1L064 x4)
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
    collapse = []
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

        declared_units = sum(1 for u in m.units if u.options)
        comp_units = [u for u in m.units if u.unit_type == "composite_question"]
        comp_with = sum(1 for u in comp_units if u.options)
        opt_spans = [s for s in run.resolved_spans if s.role == "option"]

        # collapse check: one source span reused by many option spans of same unit
        per_unit_lines = defaultdict(list)
        for s in opt_spans:
            unit = s.span_id.split(".option.")[0]
            per_unit_lines[unit].append((s.span_id.split(".option.")[-1],
                                         tuple(s.line_refs), s.granularity))
        for unit, entries in per_unit_lines.items():
            lines = [e[1] for e in entries]
            if len(lines) > 1 and len(set(lines)) == 1:
                collapse.append({"unit": unit, "line": lines[0],
                                 "labels": [e[0] for e in entries],
                                 "gran": [e[2] for e in entries]})

        # IR option content
        n_opt_ir = 0
        n_leaves = 0
        for u in ir.units:
            leaves = list(u.sub_questions) if u.unit_type == "composite_unit" else [u]
            for s in leaves:
                n_leaves += 1
                if any(c.role == "option" for c in s.content):
                    n_opt_ir += 1
        unres = Counter((u.role, u.resolution_status, " / ".join(u.evidence))
                        for u in run.unresolved_references)
        rows.append({
            "paper": p.parent.name,
            "units": len(m.units),
            "composite": len(comp_units),
            "composite_with_options": comp_with,
            "units_with_options_declared": declared_units,
            "option_spans_resolved": len(opt_spans),
            "ir_leaves_with_option_content": n_opt_ir,
            "ir_leaves": n_leaves,
            "ir_ready": sum(1 for u in ir.units if u.semantic_status == "ready"),
            "material_marker_missing": unres.get(("material", "incomplete",
                                                  "material marker text missing"), 0),
            "unresolved": [{"role": r, "status": s, "evidence": e, "count": n}
                           for (r, s, e), n in unres.most_common()],
        })

    print(f"{'paper':<6}{'units':>6}{'comp':>5}{'compOpt':>8}{'optDecl':>8}"
          f"{'optSpans':>9}{'irlOpt':>7}{'ready':>6}{'matMiss':>8}")
    for r in rows:
        print(f"{r['paper']:<6}{r['units']:>6}{r['composite']:>5}"
              f"{r['composite_with_options']:>8}{r['units_with_options_declared']:>8}"
              f"{r['option_spans_resolved']:>9}{r['ir_leaves_with_option_content']:>7}"
              f"{r['ir_ready']:>6}{r['material_marker_missing']:>8}")

    tot = Counter()
    for r in rows:
        for k in ("units", "composite", "composite_with_options",
                  "units_with_options_declared", "option_spans_resolved",
                  "ir_leaves_with_option_content", "ir_leaves", "ir_ready",
                  "material_marker_missing"):
            tot[k] += r[k]
    print("\nTOTALS:", json.dumps(dict(tot), ensure_ascii=False))

    print(f"\n=== option spans collapsing onto ONE line ===")
    print(f"units affected: {len(collapse)}")
    for c in collapse[:12]:
        print(f"   {c['unit']:<14} line={c['line']} labels={c['labels']} gran={c['gran']}")

    print("\n=== 地理 unresolved (detail) ===")
    for r in rows:
        if r["paper"] != "地理":
            continue
        for u in r["unresolved"]:
            print(f"   {u['count']:>3}  {u['role']:<10} {u['status']:<12} {u['evidence'][:90]}")

    (OUT / "verify_composite_options_delivery.json").write_text(
        json.dumps({"rows": rows, "totals": dict(tot), "collapse": collapse},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_composite_options_delivery.json'}")


if __name__ == "__main__":
    main()
