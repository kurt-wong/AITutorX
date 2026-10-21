"""Read-only FEASIBILITY test for the Owner-authorized task.

Question: can the EXISTING schema express per-sub-question options, and does
UNMODIFIED V3 resolve them?

Method: build an in-memory manifest dict for 地理, add options[] to the choice
units (labels derived from REAL source lines), load it via manifest_reader,
run the NORMAL Track A pipeline. No file, Producer, or V3 code is modified.

Key risk under test: _build_composite puts _leaf_content(unit) on the SINGLE
sub-question, and _qn() = question_numbers[0]. A geography unit spans several
question numbers, each with its own A-D block. So:
  - all blocks collapse onto one sub-question id
  - _locate_options advances a cursor_seq, so it may resolve label B of block 1
    onto block 2's line -> interleaved/wrong spans
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
MAN = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C"
           r"\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    Manifest,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHOICE = {"single_choice", "multiple_choice", "true_false"}
LABEL = re.compile(r"(?<![\w])([A-Ha-h])\s*[.．、:)）]")


def derive_options(texts, lo, hi):
    """Derive ManifestOption-shaped entries from real source lines in [lo,hi]."""
    opts = {}
    for n in range(max(1, lo), min(hi, len(texts)) + 1):
        t = (texts[n - 1] or "").strip()
        if not t or t.startswith("<") or t == "---":
            continue
        labs = []
        for mm in LABEL.finditer(t):
            lb = mm.group(1).upper()
            if lb not in labs:
                labs.append(lb)
        if not labs:
            continue
        # a genuine option line: starts with a label, or carries >=2 labels
        starts_label = bool(re.match(r"^[（(]?\s*[A-Ha-h]\s*[.．、:)）]", t))
        if not starts_label and len(labs) < 2:
            continue
        for lb in labs:
            opts.setdefault(lb, [n, n])
            opts[lb][1] = n  # span first..last line where the label appears here
    return [{"label": k, "start_line": v[0], "end_line": v[1]}
            for k, v in sorted(opts.items())]


def main() -> None:
    raw = json.loads(MAN.read_text(encoding="utf-8"))
    srs = load_source_lines(Path(raw["source_file"]))
    texts = [s.text for s in srs]
    views = tuple(
        SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                       page_no=s.page_no, line_no_in_page=s.line_no_in_page)
        for s in srs
    )

    added = []
    for u in raw["units"]:
        if u.get("original_question_type") not in CHOICE:
            continue
        spans = [x for x in (u.get("questions_lines"), u.get("material_lines")) if x]
        lo = min(x[0] for x in spans)
        hi = max(x[1] for x in spans)
        opts = derive_options(texts, lo, hi)
        if opts:
            u["options"] = opts
            added.append({"unit_id": u["unit_id"], "n": len(opts), "range": [lo, hi],
                          "labels": [o["label"] for o in opts]})

    print("=== options injected in-memory (no file written) ===")
    for a in added:
        print(f"   {a['unit_id']:<10} n={a['n']} range={a['range']} {a['labels']}")
    print(f"units with options injected: {len(added)}")

    m = Manifest(
        source_file=raw["source_file"], model=raw.get("model", ""),
        prompt_version="", validation_issues=(), warnings=(),
        units=load_manifest(MAN).units, sections=(),
    )
    # rebuild ManifestUnits WITH options by re-reading the patched raw
    import scripts.preprocessing_consumer.manifest_reader as mr
    tmp = OUT / "_tmp_geo_patched.manifest.json"
    tmp.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    m2 = mr.load_manifest(tmp)
    print(f"manifest units with options now: {sum(1 for u in m2.units if u.options)}")

    payload = manifest_to_annotation_payload(m2)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m2.units if u.material_lines}, texts)

    print("\n-- adapter content.options (first 3 units) --")
    for u in payload["semantic_units"][:3]:
        for s in u.get("sub_questions") or []:
            print(f"   {s['unit_id']} content.options="
                  f"{json.dumps(s['content'].get('options'), ensure_ascii=False)[:200]}")

    svid = uuid.uuid4()
    run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
    print("\nresolved by role:", dict(Counter(s.role for s in run.resolved_spans)))
    opt_spans = [s for s in run.resolved_spans if s.role == "option"]
    print(f"option spans resolved: {len(opt_spans)}")
    by_unit = Counter()
    for s in opt_spans:
        by_unit[s.span_id.split(".option.")[0]] += 1
    print("option spans per unit (first 10):")
    for k, v in list(by_unit.items())[:10]:
        print(f"   {k:<14} {v}")

    print("\n-- sample resolved option spans (first 12) --")
    for s in opt_spans[:12]:
        print(f"   {s.span_id:<34} refs={list(s.line_refs)} gran={s.granularity} "
              f"status={s.resolution_status}")

    unres = Counter((u.role, u.resolution_status, " / ".join(u.evidence))
                    for u in run.unresolved_references)
    print("\nunresolved:")
    for (role, status, ev), n in unres.most_common(12):
        print(f"   {n:>4}  {role:<10} {status:<12} {ev[:85]}")

    ir = IRBuilder.build(run, payload, svid, uuid.uuid4())
    print("\nIR status:", dict(Counter(u.semantic_status for u in ir.units)))
    def leaf_opts(s):
        return [(c.role, c.span_id) for c in s.content if c.role == "option"]
    print("\n-- IR option content (first 4 units) --")
    for u in ir.units[:4]:
        for s in u.sub_questions:
            print(f"   {s.unit_id:<14} status={s.semantic_status:<11} "
                  f"opts={leaf_opts(s)}")

    # blocker recount
    opts_missing = 0
    for u in ir.units:
        leaves = list(u.sub_questions) if u.unit_type == "composite_unit" else [u]
        for s in leaves:
            if not any(c.role == "option" for c in s.content):
                opts_missing += 1
    print(f"\noptions_missing_for_choice after injection: {opts_missing}")
    print(f"IR ready after injection: "
          f"{sum(1 for u in ir.units if u.semantic_status == 'ready')}/{len(ir.units)}")

    tmp.unlink(missing_ok=True)  # do not leave a fake manifest behind
    print("\n(temp patched manifest removed)")


if __name__ == "__main__":
    main()
