"""B3a geography real replay — before/after measurement (read-only).

Uses the full chain:
  manifest_to_annotation_payload → attach_material_boundary_markers
  → SourceResolver.resolve → IRBuilder
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
GEO_MF = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3A-ESCAPED-DOT")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

# Units whose printed stem uses Markdown escaped-dot (from source evidence).
ESCAPED_DOT_QNS = {1, 7, 11, 17, 21, 23, 24, 27, 29, 33, 40, 41, 42, 43, 44, 45, 46}
# Owner-highlighted units previously blocked by escaped-dot stems.
FOCUS_UNITS = {"U21-23", "U24-25", "U40-41", "U42-43", "U44-46", "U1-2"}


def measure(label: str, *, force_old_pattern: bool = False) -> dict:
    import app.domains.resolver.match_normalization as mn
    import app.domains.resolver.resolver as rp

    old_is_mn = mn.is_question_start
    old_is_rp = rp.is_question_start
    old_entry = rp._ENTRY_RE
    if force_old_pattern:
        def _old_is(normalized_line: str):
            m = re.match(r"^(\d{1,3})\s*([.．、:]|\s|$)", normalized_line)
            return m.group(1) if m else None
        # resolver imported the symbol directly — patch BOTH bindings.
        mn.is_question_start = _old_is
        rp.is_question_start = _old_is
        rp._ENTRY_RE = re.compile(r"(?<![\d])(\d{1,3})\s*[.．、:]")

    try:
        m = load_manifest(GEO_MF)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload,
            {u.unit_id: u.material_lines for u in m.units if u.material_lines},
            [s.text for s in srs],
        )
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

        stem_res = opt_res = 0
        stem_un = opt_un = 0
        unit_rows = []
        for unit in m.units:
            uid = unit.unit_id
            stems = [s for s in run.resolved_spans if s.role == "stem" and uid in s.span_id]
            opts = [s for s in run.resolved_spans if s.role == "option" and uid in s.span_id]
            s_un = [u for u in run.unresolved_references
                    if u.role in ("stem", "question_label") and uid in u.reference_id]
            o_un = [u for u in run.unresolved_references
                    if u.role == "option" and uid in u.reference_id]
            stem_res += len(stems)
            opt_res += len(opts)
            stem_un += len(s_un)
            opt_un += len(o_un)
            qns = set(unit.question_numbers or [])
            if qns & ESCAPED_DOT_QNS or uid in FOCUS_UNITS:
                unit_rows.append({
                    "unit_id": uid,
                    "question_numbers": list(unit.question_numbers),
                    "escaped_qns": sorted(qns & ESCAPED_DOT_QNS),
                    "stem_resolved": len(stems),
                    "opt_resolved": len(opts),
                    "stem_unresolved": [(u.reference_id, u.resolution_status, list(u.evidence))
                                        for u in s_un],
                    "opt_unresolved": [(u.reference_id, u.resolution_status) for u in o_un],
                })

        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        ir_ready = ir_incomplete = 0
        ir_rows = []
        for n in ir.units:
            for leaf in ([n] if n.unit_type != "composite_unit" else list(n.sub_questions)):
                if leaf.semantic_status == "ready":
                    ir_ready += 1
                else:
                    ir_incomplete += 1
                if leaf.unit_id.replace(".sub", "") in FOCUS_UNITS or any(
                    (leaf.unit_id.replace(".sub", "") == r["unit_id"] for r in unit_rows)
                ):
                    opt_items = [c for c in leaf.content if c.role == "option"]
                    ir_rows.append({
                        "unit_id": leaf.unit_id,
                        "status": leaf.semantic_status,
                        "n_options": len(opt_items),
                        "opt_resolved": sum(1 for c in opt_items if c.span_id),
                        "has_stem": any(c.role == "stem" and c.span_id for c in leaf.content),
                    })

        return {
            "label": label,
            "stem_resolved": stem_res,
            "stem_unresolved": stem_un,
            "opt_resolved": opt_res,
            "opt_unresolved": opt_un,
            "ir_ready": ir_ready,
            "ir_incomplete": ir_incomplete,
            "focus_units": unit_rows,
            "ir_focus": ir_rows,
            "unresolved_summary": _summarize_unres(run),
        }
    finally:
        mn.is_question_start = old_is_mn
        rp.is_question_start = old_is_rp
        rp._ENTRY_RE = old_entry


def _summarize_unres(run) -> dict:
    from collections import Counter
    c = Counter()
    samples = {}
    for u in run.unresolved_references:
        key = f"{u.role}:{u.resolution_status}"
        c[key] += 1
        samples.setdefault(key, []).append(
            (u.reference_id, list(u.evidence)[:2])
        )
    return {k: {"n": c[k], "samples": samples[k][:3]} for k in sorted(c)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    before = measure("before", force_old_pattern=True)
    after = measure("after", force_old_pattern=False)

    def fmt(m):
        return (f"  stem_resolved={m['stem_resolved']}  stem_unresolved={m['stem_unresolved']}\n"
                f"  opt_resolved={m['opt_resolved']}  opt_unresolved={m['opt_unresolved']}\n"
                f"  IR ready={m['ir_ready']}  incomplete={m['ir_incomplete']}")

    print("BEFORE (match-norm v1.1 pattern)")
    print(fmt(before))
    print("AFTER  (match-norm v1.2 escaped-dot)")
    print(fmt(after))

    print("\nFocus units:")
    bmap = {r["unit_id"]: r for r in before["focus_units"]}
    amap = {r["unit_id"]: r for r in after["focus_units"]}
    for uid in sorted(set(bmap) | set(amap)):
        b, a = bmap.get(uid, {}), amap.get(uid, {})
        print(f"  {uid:12} stem {b.get('stem_resolved','?')}->{a.get('stem_resolved','?')} "
              f"opt {b.get('opt_resolved','?')}->{a.get('opt_resolved','?')} "
              f"esc={a.get('escaped_qns')}")

    print("\nUnresolved AFTER:")
    for k, v in after["unresolved_summary"].items():
        print(f"  {k}: {v['n']}  e.g. {v['samples'][:2]}")

    (OUT / "b3a_replay_measure.json").write_text(
        json.dumps({"before": before, "after": after}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT / 'b3a_replay_measure.json'}")


if __name__ == "__main__":
    main()
