"""B3c-A independent check #2 — resolve the Q27 mixing defect.

Finding from check #1: unit_id is PER-PAPER unique. MIMO's
`next(r for r in all_rows if r["unit_id"]=="Q27" and r["declared_answer_lines"]==[593,623])`
searches across all 9 papers flattened, so the [593,623] hit may be a different
paper's Q27 than the one the report narrates as "数学 Q27". Also check #1 fell
back to the FIRST `unit_id=="Q27"` (化学, [819,819]).

This script:
  (1) enumerates EVERY unit_id=="Q27" across the 9 papers with declared range,
      resolved refs, granularity, and the actual first/last line text.
  (2) prints the math Q27 declared range + source text + resolved span.
  (3) classifies inter-answer overlap pairs by paper and by multi/single,
      to test whether 1764 is same-line table collapse (benign) or real
      multi-line cross-claiming.
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-A")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

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


def gather(path: Path) -> dict:
    manifest = load_manifest(path)
    srs = load_source_lines(Path(manifest.source_file))
    views = tuple(
        SourceLineView(line_ref=sl.line_ref, text=sl.text, seq=sl.seq,
                       page_no=sl.page_no, line_no_in_page=sl.line_no_in_page)
        for sl in srs
    )
    payload = manifest_to_annotation_payload(manifest)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    spans = {s.span_id: s for s in run.resolved_spans}
    tb = {i + 1: sl.text for i, sl in enumerate(srs)}
    text_by_ref = {sl.line_ref: sl.text for sl in srs}

    rows = []
    for t in extract_targets(payload):
        if t.role != "answer":
            continue
        span = spans.get(f"sp-{t.target_id}")
        rows.append({
            "paper": path.parent.name,
            "unit_id": t.unit_id,
            "qn": t.question_number,
            "declared": list(t.evidence_lines) if t.evidence_lines else None,
            "resolved_refs": list(span.line_refs) if span else [],
            "granularity": span.granularity if span else None,
            "status": span.resolution_status if span else None,
            "resolved_text_head": (
                text_by_ref.get(span.line_refs[0], "")[:120] if span and span.line_refs else None
            ),
        })
    return {"paper": path.parent.name, "rows": rows, "tb": tb,
            "n_lines": len(srs), "src": str(manifest.source_file)}


def main() -> None:
    papers = [gather(p) for p in find_manifests(CORPUS)]

    # (1) every Q27 across papers
    q27_all = []
    for p in papers:
        for r in p["rows"]:
            if r["unit_id"] == "Q27":
                d = r["declared"]
                entry = dict(r)
                if d:
                    entry["range_len"] = d[1] - d[0] + 1
                    entry["first_line"] = p["tb"].get(d[0], "")
                    entry["last_line"] = p["tb"].get(d[1], "")
                    entry["resolved_n"] = len(r["resolved_refs"])
                    entry["binding_ok"] = r["resolved_refs"] == [
                        f"P1L{n:03d}" for n in range(d[0], d[1] + 1)
                    ]
                q27_all.append(entry)

    # (2) math Q27 full text window
    math = next((p for p in papers if p["paper"] == "数学"), None)
    math_q27 = next((r for r in math["rows"] if r["unit_id"] == "Q27"), None) if math else None
    window = []
    if math_q27 and math_q27["declared"]:
        s, e = math_q27["declared"]
        for n in range(max(1, s - 3), min(math["n_lines"], e + 4) + 1):
            window.append({"line": n, "in_range": s <= n <= e, "text": math["tb"].get(n, "")})

    # all math multi-line declared ranges for context
    math_multi = [
        {"unit_id": r["unit_id"], "declared": r["declared"],
         "len": r["declared"][1] - r["declared"][0] + 1,
         "first_line": math["tb"].get(r["declared"][0], "")[:80]}
        for r in math["rows"] if r["declared"] and r["declared"][1] > r["declared"][0]
    ]

    # (3) overlap classification
    per_paper_pairs = Counter()
    same_line_pairs = 0
    multiline_pairs = []
    for p in papers:
        ds = sorted([r for r in p["rows"] if r["declared"]], key=lambda r: r["declared"][0])
        for i in range(len(ds)):
            for j in range(i + 1, len(ds)):
                a, b = ds[i]["declared"], ds[j]["declared"]
                if a[1] >= b[0]:
                    per_paper_pairs[p["paper"]] += 1
                    if a[0] == a[1] and b[0] == b[1]:
                        same_line_pairs += 1
                    else:
                        multiline_pairs.append({
                            "paper": p["paper"], "a": [ds[i]["unit_id"], a],
                            "b": [ds[j]["unit_id"], b],
                        })

    report = {
        "q27_across_papers": q27_all,
        "math_q27_declared": math_q27["declared"] if math_q27 else None,
        "math_q27_resolved_refs": math_q27["resolved_refs"] if math_q27 else None,
        "math_q27_granularity": math_q27["granularity"] if math_q27 else None,
        "math_q27_window": window,
        "math_multi_declared": math_multi,
        "overlap": {
            "per_paper": dict(per_paper_pairs),
            "total": sum(per_paper_pairs.values()),
            "both_single_line_same_or_adjacent": same_line_pairs,
            "at_least_one_multiline": len(multiline_pairs),
            "multiline_samples": multiline_pairs[:60],
        },
    }
    (OUT / "b3ca_independent_check2.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=== Q27 across the 9 papers ===")
    for r in q27_all:
        print(f"  {r['paper']:>3}  declared={r['declared']}  len={r.get('range_len')}  "
              f"gran={r['granularity']}  resolved_n={r.get('resolved_n')}  "
              f"binding_ok={r.get('binding_ok')}")
    print("\n=== math Q27 ===")
    print("  declared   :", report["math_q27_declared"])
    print("  resolved   :", report["math_q27_resolved_refs"])
    print("  granularity:", report["math_q27_granularity"])
    print("\n=== math Q27 window ===")
    for w in window:
        mark = "*" if w["in_range"] else " "
        print(f"  {mark} L{w['line']:>4}: {w['text'][:110]}")
    print("\n=== overlap ===")
    print(json.dumps(report["overlap"]["per_paper"], ensure_ascii=False))
    print("  total:", report["overlap"]["total"],
          " both-single:", report["overlap"]["both_single_line_same_or_adjacent"],
          " >=1 multi:", report["overlap"]["at_least_one_multiline"])


if __name__ == "__main__":
    main()
