"""Read-only counterfactual: would an escaped-dot fix actually unblock the 5 units?

The Owner's task premise is that `N\\.` blocks BOTH stem identity and the option
evidence that is already declared. This measures that premise BEFORE the fix,
by monkey-patching ONLY the two recognition regexes in-process:

  match_normalization.is_question_start
  resolver._ENTRY_RE / _entry_offsets

Nothing is written; the module source is untouched (patch lives in this process).

Reports before/after for the 5 affected units (21,24,40,42,44):
  stem resolved, option spans resolved, IR ready, and whether options were
  merely gated behind stem (dependency) or blocked on their own.
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
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
MAN = ROOT / "地理" / "2018北京春季高中会考地理（教师版）(1).manifest.json"
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import app.domains.resolver.match_normalization as mn  # noqa: E402
import app.domains.resolver.resolver as rz  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

TARGET_QNS = {"21", "24", "40", "42", "44"}


def build():
    m = load_manifest(MAN)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                 page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                  for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    return m, texts, views, payload


def measure(label, m, views, payload):
    svid = uuid.uuid4()
    run = rz.SourceResolver(source_version_id=svid, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, svid, uuid.uuid4())

    stem_units = {s.span_id[3:-5] for s in run.resolved_spans
                  if s.role == "stem" and s.span_id.endswith(".stem")}
    opt_by_unit = Counter()
    for s in run.resolved_spans:
        if s.role == "option":
            opt_by_unit[s.span_id.split(".option.")[0]] += 1

    # per-unit first question number -> unit id
    un = {u.unit_id: (str(u.question_numbers[0]) if u.question_numbers else None)
          for u in m.units}
    tgt_units = {uid for uid, q in un.items() if q in TARGET_QNS}

    print(f"\n===== {label} =====")
    print(f"stem resolved units total : {len(stem_units)}")
    print(f"option spans total        : {sum(opt_by_unit.values())}")
    print(f"IR ready                  : "
          f"{sum(1 for u in ir.units if u.semantic_status == 'ready')}/{len(ir.units)}")
    print(f"\n-- the 5 escaped-dot units (qn {sorted(TARGET_QNS)}) --")
    for uid in sorted(tgt_units):
        sub = f"{uid}.sub"
        n_opt = opt_by_unit.get(sub, 0)
        print(f"   {uid:<10} qn={un[uid]:<3} stem={'Y' if sub in stem_units else 'N'} "
              f"option_spans={n_opt}")
    unres = Counter((u.role, u.resolution_status, " / ".join(u.evidence))
                    for u in run.unresolved_references)
    print("   unresolved reasons:")
    for (role, status, ev), n in unres.most_common(8):
        print(f"      {n:>3} {role:<9} {status:<11} {ev[:70]}")
    return {"stem_units": len(stem_units),
            "option_spans": sum(opt_by_unit.values()),
            "ir_ready": sum(1 for u in ir.units if u.semantic_status == "ready"),
            "targets": {uid: {"qn": un[uid], "stem": f"{uid}.sub" in stem_units,
                              "option_spans": opt_by_unit.get(f"{uid}.sub", 0)}
                        for uid in sorted(tgt_units)}}


def main() -> None:
    m, texts, views, payload = build()

    before = measure("BEFORE (current recognition)", m, views, payload)

    # ---- in-process patch: accept an optional markdown escape before the dot ----
    _orig_is_qs = mn.is_question_start
    _orig_entry = rz._ENTRY_RE

    _patched_entry = re.compile(r"(?<![\d])(\d{1,3})\s*\\?[.．、:]")
    _patched_qs = re.compile(r"^(\d{1,3})\s*(\\?[.．、:]|\s|$)")

    def patched_is_question_start(normalized_line: str):
        mm = _patched_qs.match(normalized_line)
        return mm.group(1) if mm else None

    mn.is_question_start = patched_is_question_start
    rz._ENTRY_RE = _patched_entry
    # resolver imported is_question_start by name -> rebind there too
    _orig_rz_iqs = rz.is_question_start
    rz.is_question_start = patched_is_question_start
    try:
        after = measure("AFTER (escaped-dot accepted, in-process patch)", m, views, payload)
    finally:
        mn.is_question_start = _orig_is_qs
        rz.is_question_start = _orig_rz_iqs
        rz._ENTRY_RE = _orig_entry

    print("\n===== DELTA =====")
    for k in ("stem_units", "option_spans", "ir_ready"):
        print(f"   {k:<14} {before[k]:>4} -> {after[k]:<4} "
              f"({after[k] - before[k]:+d})")
    print("\n   target units:")
    for uid in sorted(before["targets"]):
        b, a = before["targets"][uid], after["targets"][uid]
        print(f"      {uid:<10} qn={b['qn']:<3} "
              f"stem {b['stem']!s:<5}->{a['stem']!s:<5} "
              f"opts {b['option_spans']}->{a['option_spans']}")

    (OUT / "counterfactual_escaped_dot.json").write_text(
        json.dumps({"before": before, "after": after}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'counterfactual_escaped_dot.json'}")


if __name__ == "__main__":
    main()
