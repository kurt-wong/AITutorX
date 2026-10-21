"""Side-effect boundary check (Owner gap 3).

The explanation fix must NOT change stem / option / material / answer / image
resolved spans. Compare the full non-explanation resolved-span set under the
pre-fix vs post-fix _explanation_span.

Note: the PRE control here *re-enables the old loop only*; the adapter now always
emits explanation_lines, so we additionally force evidence_lines=None for
explanation targets to reproduce the true pre-fix span.
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
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.resolver import resolver as rm  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

_ORIG = SourceResolver._explanation_span


def _pre_fix(self, out, unit_id, t):
    object.__setattr__(t, "evidence_lines", None)   # pre-fix: adapter dropped it
    qn = t.question_number
    header_seen = False
    region = []
    for l in self._idx.lines:
        norm = rm.normalize_text(l.text)
        if rm.is_explanation_header(norm):
            header_seen = True
            continue
        if not header_seen:
            continue
        if rm.is_explanation_header(norm) or rm.is_answer_header(norm):
            break
        region.append(l.line_ref)
    if not header_seen or not region:
        out.add_unresolved(t, "missing", ("pre-fix",))
        return
    owned = [r for r in region
             if qn is None or rm.is_question_start(rm.normalize_text(self._idx.get(r).text)) == qn]
    if not owned:
        out.add_unresolved(t, "missing", ("pre-fix no row",))
        return
    out.add_span(unit_id, t, owned, "exact", ("explanation", f"qn={qn}"))


def spans_of(path: Path) -> dict:
    m = load_manifest(path)
    srs = load_source_lines(Path(m.source_file))
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )
    payload = manifest_to_annotation_payload(m)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    by_role: dict[str, dict[str, list[str]]] = {}
    for s in run.resolved_spans:
        by_role.setdefault(s.role, {})[s.span_id] = list(s.line_refs)
    unres = {u.reference_id: u.resolution_status for u in run.unresolved_references}
    return {"resolved": by_role, "unresolved": unres}


def main() -> None:
    manifests = list(find_manifests(CORPUS))
    after = {p.parent.name: spans_of(p) for p in manifests}
    SourceResolver._explanation_span = _pre_fix
    try:
        pre = {p.parent.name: spans_of(p) for p in manifests}
    finally:
        SourceResolver._explanation_span = _ORIG

    diffs = []
    for paper in after:
        a, b = after[paper], pre[paper]
        for role in sorted(set(a["resolved"]) | set(b["resolved"])):
            if role == "explanation":
                continue
            sa, sb = a["resolved"].get(role, {}), b["resolved"].get(role, {})
            for sid in sorted(set(sa) | set(sb)):
                if sa.get(sid) != sb.get(sid):
                    diffs.append({"paper": paper, "role": role, "span": sid,
                                  "after": sa.get(sid), "pre": sb.get(sid)})
        for rid in sorted(set(a["unresolved"]) | set(b["unresolved"])):
            va, vb = a["unresolved"].get(rid), b["unresolved"].get(rid)
            if va != vb and not rid.endswith(".explanation"):
                diffs.append({"paper": paper, "role": "unresolved", "span": rid,
                              "after": va, "pre": vb})

    expl_delta = []
    for paper in after:
        sa = after[paper]["resolved"].get("explanation", {})
        sb = pre[paper]["resolved"].get("explanation", {})
        expl_delta.append({"paper": paper, "after_n": len(sa), "pre_n": len(sb)})

    report = {
        "non_explanation_span_diffs": diffs,
        "n_diffs": len(diffs),
        "explanation_counts": expl_delta,
        "role_totals_after": {
            r: sum(len(v["resolved"].get(r, {})) for v in after.values())
            for r in {k for v in after.values() for k in v["resolved"]}
        },
        "role_totals_pre": {
            r: sum(len(v["resolved"].get(r, {})) for v in pre.values())
            for r in {k for v in pre.values() for k in v["resolved"]}
        },
    }
    (OUT / "explanation_side_effects.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("non-explanation span diffs:", len(diffs))
    for d in diffs[:20]:
        print("  ", d)
    print("\nrole totals AFTER:", json.dumps(report["role_totals_after"], ensure_ascii=False))
    print("role totals PRE  :", json.dumps(report["role_totals_pre"], ensure_ascii=False))
    print("\nexplanation counts per paper:")
    for e in expl_delta:
        print("  ", e)


if __name__ == "__main__":
    main()
