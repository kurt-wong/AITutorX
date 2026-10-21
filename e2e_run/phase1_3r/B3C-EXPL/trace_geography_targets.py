"""Read-only: trace 地理 material + stem targets end-to-end.

Stage 1: adapter payload (shared_components.material shape)
Stage 2: extract_targets() output (ResolveTarget objects)
Stage 3: resolver outcome per target

Answers Q1-B (which field holds "marker text", where required, why (9,9) fails)
and Q2-A/B (stem target count, why only 11 resolve).
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

from app.domains.resolver.reference import extract_targets  # noqa: E402
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
    for p in find_manifests(CORPUS):
        if p.parent.name != TARGET:
            continue
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)

        print("=== STAGE 1: adapter payload ===")
        print("top-level keys:", sorted(payload))
        pb = payload.get("producer_boundary") or {}
        gaps = pb.get("known_gaps") if isinstance(pb, dict) else None
        if gaps:
            print(f"known_gaps: {len(gaps)}")
            for g in gaps[:6]:
                print(f"   {g.get('code')} {g.get('unit_id')} {str(g.get('detail'))[:110]}")

        print("\n-- shared_components.material per unit (first 4) --")
        for u in payload.get("semantic_units", [])[:4]:
            sc = u.get("shared_components") or {}
            print(f"  {u.get('unit_id')} unit_type={u.get('unit_type')}")
            print(f"      shared keys={sorted(sc)}")
            print(f"      material={json.dumps(sc.get('material'), ensure_ascii=False)}")
            subs = u.get("sub_questions") or []
            print(f"      sub_questions={len(subs)}")

        print("\n-- ALL material declarations (marker presence) --")
        has_text = 0
        no_text = 0
        gran = Counter()
        for u in payload.get("semantic_units", []):
            sc = u.get("shared_components") or {}
            mat = sc.get("material")
            if not isinstance(mat, dict):
                continue
            sm = mat.get("start_marker") or {}
            gran[sm.get("granularity")] += 1
            if sm.get("text"):
                has_text += 1
            else:
                no_text += 1
        print(f"  start_marker with text   : {has_text}")
        print(f"  start_marker WITHOUT text: {no_text}")
        print(f"  start_marker granularity : {dict(gran)}")

        print("\n=== STAGE 2: extract_targets ===")
        targets = extract_targets(payload)
        print("targets by kind:", dict(Counter(t.kind for t in targets)))
        print("targets by role:", dict(Counter(t.role for t in targets)))
        mat_t = [t for t in targets if t.role in ("material", "word_bank",
                                                 "shared_option_pool", "task_instruction")]
        print(f"material-role targets: {len(mat_t)}")
        for t in mat_t[:4]:
            print(f"   {t.target_id:<24} kind={t.kind} "
                  f"start_marker={json.dumps(t.start_marker, ensure_ascii=False)}")
        stem_t = [t for t in targets if t.kind == "question_label"]
        print(f"question_label targets: {len(stem_t)}")
        print("stem question_numbers:", [t.question_number for t in stem_t])

        print("\n=== STAGE 3: resolver outcome ===")
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        print("resolved by role:", dict(Counter(s.role for s in run.resolved_spans)))
        unres = Counter((u.role, u.resolution_status, " / ".join(u.evidence))
                        for u in run.unresolved_references)
        print(f"unresolved total: {sum(unres.values())}")
        for (role, status, ev), n in unres.most_common():
            print(f"   {n:>4}  {role:<12} {status:<12} {ev[:80]}")

        out = {
            "targets_by_kind": dict(Counter(t.kind for t in targets)),
            "targets_by_role": dict(Counter(t.role for t in targets)),
            "material_targets": [
                {"target_id": t.target_id, "kind": t.kind,
                 "start_marker": t.start_marker, "end_marker": t.end_marker}
                for t in mat_t
            ],
            "stem_question_numbers": [t.question_number for t in stem_t],
            "resolved_by_role": dict(Counter(s.role for s in run.resolved_spans)),
            "unresolved": [
                {"role": r, "status": s, "evidence": e, "count": n}
                for (r, s, e), n in unres.most_common()
            ],
            "material_marker_presence": {"with_text": has_text, "without_text": no_text,
                                        "granularity": {str(k): v for k, v in gran.items()}},
            "known_gaps": gaps,
        }
        (OUT / "geography_target_trace.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwritten: {OUT / 'geography_target_trace.json'}")


if __name__ == "__main__":
    main()
