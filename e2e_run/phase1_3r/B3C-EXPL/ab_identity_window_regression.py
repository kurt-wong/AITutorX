"""Read-only A/B on the whole corpus: does the questions_lines window / printed
key EVER exclude a stem that the pre-fix logic would have found?

Method: monkey-patch `_locate_question_start` in-process to restore the OLD
behaviour (no printed key, no questions_lines window) and compare stem
resolution per unit across all 9 papers. Nothing is written to the repo.

This is the regression risk of 7c9b8aa: the window narrows the search, so a
mis-declared Producer questions_lines could silently drop a stem.
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

import app.domains.resolver.resolver as rz  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.match_normalization import normalize_text  # noqa: E402
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

_NEW = rz.SourceResolver._locate_question_start


def _old_locate(self, out, unit_id, t, qn):
    """Pre-7c9b8aa behaviour: whole question zone, declared qn only."""
    hits = [l.line_ref for l in self._question_zone()
            if rz.is_question_start(normalize_text(l.text)) == qn]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        out.add_unresolved(t, "ambiguous", (f"question {qn} start not unique",))
        return None
    out.add_unresolved(t, "missing", (f"question number {qn!r} not found",))
    return None


def run_corpus(label):
    per_unit = {}
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
        svid = uuid.uuid4()
        run = rz.SourceResolver(source_version_id=svid, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, svid, uuid.uuid4())
        paper = p.parent.name
        stems = {s.span_id[3:-5] for s in run.resolved_spans
                 if s.role == "stem" and s.span_id.endswith(".stem")}
        opts = Counter()
        for s in run.resolved_spans:
            if s.role == "option":
                opts[s.span_id[3:].split(".option.")[0]] += 1
        for u in ir.units:
            key = f"{paper}/{u.unit_id}"
            sub = f"{u.unit_id}.sub"
            per_unit[key] = {
                "stem": sub in stems,
                "opts": opts.get(sub, 0),
                "ready": u.semantic_status == "ready",
            }
    return per_unit


def main() -> None:
    after = run_corpus("after")
    rz.SourceResolver._locate_question_start = _old_locate
    try:
        before = run_corpus("before")
    finally:
        rz.SourceResolver._locate_question_start = _NEW

    print(f"units compared: {len(after)}")
    ta = Counter(v["stem"] for v in after.values())
    tb = Counter(v["stem"] for v in before.values())
    print(f"stem resolved  before={tb[True]}  after={ta[True]}")
    ra = sum(1 for v in after.values() if v["ready"])
    rb = sum(1 for v in before.values() if v["ready"])
    print(f"IR ready       before={rb}  after={ra}")
    sa = sum(v["opts"] for v in after.values())
    sb = sum(v["opts"] for v in before.values())
    print(f"option spans   before={sb}  after={sa}")

    lost = [k for k in after if before[k]["stem"] and not after[k]["stem"]]
    gained = [k for k in after if after[k]["stem"] and not before[k]["stem"]]
    optlost = [k for k in after if after[k]["opts"] < before[k]["opts"]]
    optgain = [k for k in after if after[k]["opts"] > before[k]["opts"]]
    regressed = [k for k in after if before[k]["ready"] and not after[k]["ready"]]

    print(f"\nstem LOST      : {len(lost)} {lost[:10]}")
    print(f"stem GAINED    : {len(gained)} {gained[:10]}")
    print(f"options LOST   : {len(optlost)} {optlost[:10]}")
    print(f"options GAINED : {len(optgain)}")
    print(f"IR REGRESSED   : {len(regressed)} {regressed[:10]}")

    (OUT / "ab_identity_window_regression.json").write_text(json.dumps({
        "stem_before": tb[True], "stem_after": ta[True],
        "ready_before": rb, "ready_after": ra,
        "opts_before": sb, "opts_after": sa,
        "stem_lost": lost, "stem_gained": gained,
        "options_lost": optlost, "options_gained": optgain,
        "ir_regressed": regressed,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwritten: {OUT / 'ab_identity_window_regression.json'}")


if __name__ == "__main__":
    main()
