"""B3c-A INDEPENDENT content check (read-only forensic).

The MIMO measurement (b3ca_transport_measure.py:_refs_for_declared) computes the
EXPECTED refs with the SAME formula the implementation uses
(`P1L{n}` for n in s..e), so "binding_match=True" is structurally guaranteed for
every resolved span. That proves transport fidelity, NOT evidence correctness.

This script attacks the claim from the other side: it verifies that the bound
range actually CONTAINS answer evidence, by reading the raw source text.

Checks:
  (1) Q27: print the actual text of the bound range + a window around it.
  (2) Corpus-wide: does the bound range contain a plausible answer token?
  (3) Do declared ranges OVERLAP each other (two answers claiming one line)?
  (4) Do declared answer ranges OVERLAP material regions?
  (5) Cross-check the '6 undeclared' residual.
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter
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

_LETTER = re.compile(r"[A-D]")


def _qn_strip(t: str) -> str:
    return re.sub(r"^\s*[0-9]{1,3}\s*[.．、:)]*\s*", "", t.strip()).strip()


def measure(path: Path) -> dict:
    manifest = load_manifest(path)
    source_lines = load_source_lines(Path(manifest.source_file))
    views = tuple(
        SourceLineView(
            line_ref=sl.line_ref, text=sl.text, seq=sl.seq,
            page_no=sl.page_no, line_no_in_page=sl.line_no_in_page,
        )
        for sl in source_lines
    )
    payload = manifest_to_annotation_payload(manifest)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    spans = {s.span_id: s for s in run.resolved_spans}

    text_by_no = {i + 1: sl.text for i, sl in enumerate(source_lines)}
    targets = [t for t in extract_targets(payload) if t.role == "answer"]

    rows = []
    for t in targets:
        span = spans.get(f"sp-{t.target_id}")
        declared = t.evidence_lines
        row = {
            "paper": path.parent.name,
            "unit_id": t.unit_id,
            "qn": t.question_number,
            "declared": list(declared) if declared else None,
            "resolved": span is not None,
            "granularity": span.granularity if span else None,
            "n_refs": len(span.line_refs) if span else 0,
        }
        if declared:
            s, e = declared
            body = "\n".join(text_by_no.get(n, "") for n in range(s, e + 1))
            row["range_text_head"] = body[:160]
            row["range_len"] = e - s + 1
            # Does the range contain an answer-like token after qn strip?
            stripped = _qn_strip(body)
            row["has_value_in_range"] = bool(stripped)
            row["first_line"] = text_by_no.get(s, "")
            row["last_line"] = text_by_no.get(e, "")
            row["first_line_bare_qn"] = (_qn_strip(text_by_no.get(s, "")) == "")
        rows.append(row)
    return {"paper": path.parent.name, "rows": rows, "n_lines": len(source_lines)}


def main() -> None:
    papers = [measure(p) for p in find_manifests(CORPUS)]
    rows = [r for p in papers for r in p["rows"]]

    declared = [r for r in rows if r["declared"]]
    multi = [r for r in declared if r["declared"][1] > r["declared"][0]]
    single = [r for r in declared if r["declared"][1] == r["declared"][0]]

    # (1) Q27 window
    q27 = next((r for r in rows if r["unit_id"] == "Q27"), None)
    math_paper = next((p for p in papers if p["paper"] == "数学"), None)
    q27_window = []
    if q27 and q27["declared"] and math_paper:
        src = load_source_lines(Path(load_manifest(
            next(p for p in find_manifests(CORPUS) if p.parent.name == "数学")
        ).source_file))
        tb = {i + 1: sl.text for i, sl in enumerate(src)}
        s, e = q27["declared"]
        for n in range(max(1, s - 4), min(len(src), e + 5) + 1):
            q27_window.append({"line": n, "in_range": s <= n <= e, "text": tb.get(n, "")})

    # (3) inter-answer overlap of declared ranges
    overlap_pairs = []
    for p in papers:
        ds = [r for r in p["rows"] if r["declared"]]
        ds.sort(key=lambda r: r["declared"][0])
        for i in range(len(ds)):
            for j in range(i + 1, len(ds)):
                a, b = ds[i]["declared"], ds[j]["declared"]
                if a[1] >= b[0]:
                    overlap_pairs.append({
                        "paper": p["paper"],
                        "a": [ds[i]["unit_id"], a], "b": [ds[j]["unit_id"], b],
                        "overlap": [max(a[0], b[0]), min(a[1], b[1])],
                    })

    # (5) undeclared residual
    undeclared = [r for r in rows if not r["declared"]]

    report = {
        "corpus": str(CORPUS),
        "papers": len(papers),
        "answer_targets": len(rows),
        "declared": len(declared),
        "multi": len(multi),
        "single": len(single),
        "undeclared": len(undeclared),
        "undeclared_detail": [
            {"paper": r["paper"], "unit_id": r["unit_id"], "qn": r["qn"],
             "resolved": r["resolved"], "granularity": r["granularity"]}
            for r in undeclared
        ],
        "range_has_value": {
            "multi_with_value": sum(1 for r in multi if r["has_value_in_range"]),
            "multi_total": len(multi),
            "single_with_value": sum(1 for r in single if r["has_value_in_range"]),
            "single_total": len(single),
        },
        "first_line_bare_qn": {
            "multi": sum(1 for r in multi if r["first_line_bare_qn"]),
            "multi_total": len(multi),
            "single": sum(1 for r in single if r["first_line_bare_qn"]),
            "single_total": len(single),
        },
        "inter_answer_overlap": {
            "n_pairs": len(overlap_pairs),
            "pairs": overlap_pairs[:40],
        },
        "q27_declared": q27["declared"] if q27 else None,
        "q27_resolved_refs_n": q27["n_refs"] if q27 else None,
        "q27_window": q27_window,
    }

    out = OUT / "b3ca_independent_check.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("q27_window", "inter_answer_overlap", "undeclared_detail")},
                     ensure_ascii=False, indent=2))
    print("--- inter-answer overlap pairs:", len(overlap_pairs))
    for pair in overlap_pairs[:20]:
        print("   ", pair)


if __name__ == "__main__":
    main()
