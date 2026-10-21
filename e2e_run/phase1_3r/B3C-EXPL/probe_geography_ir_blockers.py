"""Read-only: dump the actual IR node structure for 地理 so the real
blocking problems are visible (not inferred).

For each top-level composite: shared_components span_ids + sub-question
content/span_ids + status. Then apply the same required-role rules the
validator uses (ir.py:239-283) to name each blocker explicitly.
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
TARGET = "地理"

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
    for p in find_manifests(CORPUS):
        if p.parent.name != TARGET:
            continue
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

        print("=== IR node structure (first 3 composites) ===")
        for u in ir.units[:3]:
            print(f"\n{u.unit_id} type={u.unit_type} status={u.semantic_status} "
                  f"orig_type={u.original_question_type!r} canonical="
                  f"{map_canonical_type(u.original_question_type)!r}")
            print(f"  shared_components: "
                  f"{[(c.role, c.span_id, c.unsupported) for c in u.shared_components]}")
            for s in u.sub_questions:
                print(f"  sub {s.unit_id} status={s.semantic_status} "
                      f"canonical={map_canonical_type(s.original_question_type)!r} "
                      f"required={content_roles_for(map_canonical_type(s.original_question_type))}")
                print(f"      content: {[(c.role, c.span_id, c.unsupported) for c in s.content]}")

        # ---- explicit blocker naming across all units ----
        print("\n=== blocker analysis (all units) ===")
        blocker_counter = Counter()
        for u in ir.units:
            probs = []
            if not u.shared_components:
                probs.append("composite has no shared component material")
            for sc in u.shared_components:
                if sc.span_id is None:
                    probs.append(f"shared component {sc.role} unresolved")
            for s in u.sub_questions:
                canon = map_canonical_type(s.original_question_type)
                req = content_roles_for(canon)
                by_role = {c.role: c for c in s.content}
                if req.get("stem") == "required":
                    c = by_role.get("stem")
                    if c is None:
                        probs.append("sub stem not declared")
                    elif c.span_id is None:
                        probs.append("sub stem unresolved")
                if req.get("answer") == "required":
                    c = by_role.get("answer")
                    if c is None:
                        probs.append("sub answer not declared")
                    elif c.span_id is None:
                        probs.append("sub answer unresolved")
                if req.get("options") == "required_for_choice":
                    if not any(c.role == "option" for c in s.content):
                        probs.append("sub options missing for choice type")
                for c in s.content:
                    if c.unsupported:
                        probs.append(f"sub unsupported role {c.role}")
                    elif c.span_id is None:
                        probs.append(f"sub role {c.role} unresolved")
                if s.semantic_status != "ready":
                    probs.append("composite sub_question not ready")
            for pr in probs:
                blocker_counter[pr] += 1
            print(f"   {u.unit_id:<10} {probs}")

        print("\nblocker histogram:", dict(blocker_counter))

        out = {"blocker_histogram": dict(blocker_counter)}
        (OUT / "geography_ir_blockers.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_ir_blockers.json'}")


if __name__ == "__main__":
    main()
