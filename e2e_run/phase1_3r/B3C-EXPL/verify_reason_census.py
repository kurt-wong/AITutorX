"""Read-only: leaf reason-kind census to check MIMO's aggregated unresolved list.

MIMO reported:
  stem:ambiguous 41 | stem:missing 6 | option:incomplete 96
  option:ambiguous 2 | answer:ambiguous 6 | material:incomplete 8

Counts the underlying unresolved references on ready-relevant paths, corpus-wide.
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
    per_paper = {}
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
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        c = Counter((u.role, u.resolution_status) for u in run.unresolved_references)
        per_paper[p.parent.name] = {f"{r}:{s}": n for (r, s), n in c.items()}
        tot.update(c)

    print(f"{'role:status':<28}{'count':>7}")
    for (r, s), n in sorted(tot.items(), key=lambda x: -x[1]):
        print(f"{r + ':' + s:<28}{n:>7}")

    print("\n=== MIMO's reported list ===")
    mimos = {"stem:ambiguous": 41, "stem:missing": 6, "option:incomplete": 96,
             "option:ambiguous": 2, "answer:ambiguous": 6, "material:incomplete": 8}
    for k, v in mimos.items():
        role, status = k.split(":")
        mine = tot.get((role, status), 0)
        flag = "OK" if mine == v else f"DIFF (mine={mine})"
        print(f"  {k:<22} MIMO={v:<5} {flag}")

    (OUT / "verify_reason_census.json").write_text(
        json.dumps({"totals": {f"{r}:{s}": n for (r, s), n in tot.items()},
                    "per_paper": per_paper, "mimo_claimed": mimos},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_reason_census.json'}")


if __name__ == "__main__":
    main()
