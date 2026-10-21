"""Read-only: verify the P0-A diagnostic is RETAINED with the expected volume.

Owner acceptance requires `role_region diagnostic count 保持存在`.
My pre-P0 recomputation measured: 72 roots with a role-region hit, 77 reason
occurrences. After P0-A the diagnostics must still be present, unchanged.

Also confirms: none of the OTHER auto_allowed sources were touched
(span resolution non-exact and material resolution must still block auto),
and the terminal-rejected path is unaffected.
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
from app.domains.gate import policy as gp  # noqa: E402
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

_AUTO = gp._AUTO_RESOLUTIONS


def main() -> None:
    t = Counter()
    per_paper = Counter()
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
        resolved = {s.span_id: s for s in run.resolved_spans}

        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = gp.evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            prov = g["layers"]["provenance"]
            diags = prov.get("role_region_diagnostics") or []
            t["roots_evaluated"] += 1
            if diags:
                t["roots_with_diag"] += 1
                t["diag_reason_occurrences"] += len(diags)
                per_paper[paper] += 1
            # field presence
            if "role_region_diagnostics" in prov:
                t["field_present"] += 1
            # other blockers must still work
            if prov.get("auto_allowed") is False:
                t["auto_allowed_false"] += 1
            if g["decision"] == "rejected":
                t["rejected"] += 1
            # regression: a diagnostic must NOT appear as a blocker reason
            if any("role provenance" in r and "diagnostic" not in r
                   for r in (g.get("reasons") or ())):
                t["LEAKED_AS_BLOCKER"] += 1

    print("DIAGNOSTIC RETENTION:", json.dumps(dict(t), ensure_ascii=False, indent=2))
    print("\nroots with diagnostics, per paper:")
    for k, v in per_paper.most_common():
        print(f"   {k:<6} {v}")

    (OUT / "verify_p0_diagnostics.json").write_text(
        json.dumps({"totals": dict(t), "per_paper": dict(per_paper)},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_p0_diagnostics.json'}")


if __name__ == "__main__":
    main()
