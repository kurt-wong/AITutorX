"""B3c-A root-cause for the single-line-paper answer∩explanation collisions.

For a single-line paper (e.g. 历史) find, for one unit, the answer span and the
explanation span, and print the actual source text of the colliding line.
Question: is the explanation span wrongly absorbing the answer row?
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    for want in ("历史", "数学"):
        p = next(x for x in find_manifests(CORPUS) if x.parent.name == want)
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        tb = {s.line_ref: s.text for s in srs}
        payload = manifest_to_annotation_payload(m)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

        ans = {s.span_id: s for s in run.resolved_spans if s.role == "answer"}
        expl = {s.span_id: s for s in run.resolved_spans if s.role == "explanation"}

        print("=" * 78)
        print(f"PAPER {want}: answer spans={len(ans)} explanation spans={len(expl)}")
        shown = 0
        for aid, a in ans.items():
            uid = aid[3:].rsplit(".answer", 1)[0]
            eid = f"sp-{uid}.explanation"
            e = expl.get(eid)
            if not e:
                continue
            inter = set(a.line_refs) & set(e.line_refs)
            if not inter:
                continue
            print(f"\n  unit {uid}")
            print(f"    answer      {a.granularity:<14} {list(a.line_refs)[:4]}"
                  f"{'...' if len(a.line_refs) > 4 else ''} ({len(a.line_refs)})")
            print(f"    explanation {e.granularity:<14} {list(e.line_refs)[:4]}"
                  f"{'...' if len(e.line_refs) > 4 else ''} ({len(e.line_refs)})")
            print(f"    intersection: {sorted(inter)[:6]}")
            for r in sorted(inter)[:3]:
                print(f"      {r}: {tb.get(r, '')[:110]!r}")
            shown += 1
            if shown >= 3:
                break

        # Also: the explanation header / region for this paper
        from app.domains.resolver.match_normalization import (  # noqa: E402
            is_answer_header, is_explanation_header, normalize_text,
        )
        hdrs = [(s.line_ref, s.text[:40]) for s in srs
                if is_explanation_header(normalize_text(s.text))]
        ahdr = [(s.line_ref, s.text[:40]) for s in srs
                if is_answer_header(normalize_text(s.text))]
        print(f"\n  explanation headers: {hdrs[:5]}")
        print(f"  answer headers     : {ahdr[:5]}")


if __name__ == "__main__":
    main()
