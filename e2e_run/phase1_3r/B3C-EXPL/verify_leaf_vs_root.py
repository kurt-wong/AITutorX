"""Read-only: reconcile the English/leaf discrepancy in MIMO's replay table.

Findings to prove:
  1. `ready` LEAF count (226) != `ready` TOP-LEVEL unit count (219), because a
     composite root can be incomplete while its sub is ready.
  2. MIMO's "IR ready 226" is the leaf count; its per-paper English row (15) is
     also the leaf count, while only 8 English top-level units reach the Gate.
  3. 'rejected' total is 5 (历史3 + 地理2), not 12; the extra 7 = English
     incomplete roots that never entered the Gate.
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
    print("=== composite roots: root status vs sub status (English focus) ===")
    for p in find_manifests(CORPUS):
        if p.parent.name != "英语":
            continue
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
        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        for root in ir.units:
            if root.unit_type != "composite_unit":
                print(f"  {root.unit_id:<12} standalone status={root.semantic_status}")
                continue
            subs = {s.unit_id: s.semantic_status for s in root.sub_questions}
            print(f"  {root.unit_id:<12} composite root={root.semantic_status:<11} "
                  f"subs={subs}")

    print("\n=== corpus: root-ready vs sub-ready divergence ===")
    div = []
    tot_root_ready = tot_sub_ready = tot_subs = 0
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
        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        for root in ir.units:
            subs = list(root.sub_questions) if root.unit_type == "composite_unit" else [root]
            for s in subs:
                tot_subs += 1
                if s.semantic_status == "ready":
                    tot_sub_ready += 1
            if root.semantic_status == "ready":
                tot_root_ready += 1
            elif root.unit_type == "composite_unit" and any(
                    s.semantic_status == "ready" for s in root.sub_questions):
                div.append((p.parent.name, root.unit_id,
                            root.semantic_status,
                            {s.unit_id: s.semantic_status for s in root.sub_questions}))
    print(f"  top-level units ready : {tot_root_ready}")
    print(f"  leaves ready          : {tot_sub_ready} / {tot_subs}")
    print(f"  roots incomplete BUT some sub ready : {len(div)}")
    for paper, uid, st, subs in div:
        print(f"     {paper}/{uid} root={st} subs={subs}")

    (OUT / "verify_leaf_vs_root.json").write_text(
        json.dumps({"top_ready": tot_root_ready, "leaf_ready": tot_sub_ready,
                    "leaves": tot_subs, "divergent": div},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_leaf_vs_root.json'}")


if __name__ == "__main__":
    main()
