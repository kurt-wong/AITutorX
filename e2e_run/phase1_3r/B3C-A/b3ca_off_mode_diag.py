"""Why does OFF mode report ans∩explanation = 0 for 历史?

Compare the 历史 answer/explanation spans in ON vs OFF. In OFF nothing is
declared, so Q50 should still resolve via the answer_zone scan and should still
collide with the 353-line explanation span -- unless the OFF run differs.

Hypothesis to test: in OFF mode the answer_zone scan finds entries but they are
rejected as multi-line ambiguous, OR the collision counter is wrong.

Also: is the 353-line explanation span itself a pre-existing defect?
"""
from __future__ import annotations

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

_ORIG = SourceResolver._answer_span


def _off(self, out, unit_id, t):
    object.__setattr__(t, "evidence_lines", None)
    return _ORIG(self, out, unit_id, t)


def run_hist(mode: str):
    p = next(x for x in find_manifests(CORPUS) if x.parent.name == "历史")
    m = load_manifest(p)
    srs = load_source_lines(Path(m.source_file))
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    ans = {s.span_id: s for s in run.resolved_spans if s.role == "answer"}
    expl = {s.span_id: s for s in run.resolved_spans if s.role == "explanation"}
    coll = 0
    for aid, a in ans.items():
        uid = aid[3:].rsplit(".answer", 1)[0]
        e = expl.get(f"sp-{uid}.explanation")
        if e and (set(a.line_refs) & set(e.line_refs)):
            coll += 1
    print(f"[{mode}] answer spans={len(ans)}  explanation spans={len(expl)}  "
          f"colliding units={coll}")
    for uid in ("Q1", "Q2", "Q50"):
        a = ans.get(f"sp-{uid}.answer")
        e = expl.get(f"sp-{uid}.explanation")
        print(f"   {uid}: answer={None if not a else (a.granularity, list(a.line_refs))} "
              f"expl={None if not e else (e.granularity, len(e.line_refs), list(e.line_refs)[:2])}")
    unres = [u for u in run.unresolved_references if u.role == "answer"]
    print(f"   unresolved answer refs: {len(unres)}; first: "
          f"{[(u.reference_id, u.resolution_status) for u in unres[:3]]}")


print("--- ON ---")
run_hist("ON")
SourceResolver._answer_span = _off
try:
    print("--- OFF ---")
    run_hist("OFF")
finally:
    SourceResolver._answer_span = _ORIG
