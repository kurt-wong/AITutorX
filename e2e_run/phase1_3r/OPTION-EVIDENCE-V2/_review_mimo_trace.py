"""READ-ONLY review of MIMO's P1.4-E2E-TRACE report — verify its claims.

MIMO claims:
  C1  Q20: manifest had A,B,C,D before P1.4-B; P1.4-B Rule A fabricated E.
      => E is a NEW artifact introduced by P1.4-B.
  C2  Q4 : "选项无缺陷；answer-side"  (option side has no defect)
  C3  Q22: golden path, No defect
  C4  Q23: +1 auto confirmed

Pipeline context (verified earlier): the resolver reads option labels from the
MANIFEST (`reference.py` builds option_label targets from options[]), so a label
absent from the manifest cannot produce an option. Therefore C1 is provable from
the .p14b.bak alone.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate, leaf_unit_ids  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

CHECK = {"化学": {"Q20", "Q22", "Q23"}, "数学": {"Q4"}, "历史": {"Q29"}}


def labels_of(unit: dict):
    return [o.get("label") for o in (unit.get("options") or [])]


def main() -> None:
    # ---------- part 1: manifest-level before/after (proves C1 independently) ----------
    print("=" * 96)
    print("PART 1 — manifest .p14b.bak (before) vs current (after):  Q20 / Q4 / Q22 / Q23 / Q29")
    print("=" * 96)
    for bak in sorted(CORPUS.glob("*/*.manifest.json.p14b.bak")):
        cur = Path(str(bak)[: -len(".p14b.bak")])
        paper = bak.parent.name
        old = json.loads(bak.read_text(encoding="utf-8"))
        new = json.loads(cur.read_text(encoding="utf-8"))
        om = {str(u["unit_id"]): u for u in old["units"]}
        nm = {str(u["unit_id"]): u for u in new["units"]}
        for uid in sorted(set(om) & set(nm)):
            if uid not in CHECK.get(paper, set()):
                continue
            lo, ln = labels_of(om[uid]), labels_of(nm[uid])
            mark = "  <<< CHANGED" if lo != ln else ""
            print(f"\n   {paper}/{uid}")
            print(f"      BEFORE (bak): {lo}")
            print(f"      AFTER  (cur): {ln}{mark}")

    # ---------- part 2: resolved option spans on the CURRENT corpus ----------
    print("\n" + "=" * 96)
    print("PART 2 — resolved option spans (current corpus): is any option degenerate?")
    print("=" * 96)
    for p in find_manifests(CORPUS):
        paper = p.parent.name
        if paper not in CHECK:
            continue
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
        )
        sv = uuid.uuid4()
        run = SourceResolver(source_version_id=sv, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv, uuid.uuid4())
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)
        for root in ir.units:
            if root.unit_id not in CHECK.get(paper, set()):
                continue
            want = leaf_unit_ids(root)
            for leaf in compiled.leaves:
                if leaf.unit_id not in want:
                    continue
                gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                print(f"\n   {paper}/{root.unit_id}  gate={gate['decision']}")
                deg = []
                for o in leaf.options:
                    t = o.text.strip()
                    is_deg = t.upper() == str(o.label).upper()
                    if is_deg:
                        deg.append(str(o.label))
                    print(f"      {o.label}: len={len(t):<4} {t[:58]!r}"
                          f"{'   <<< LABEL-ONLY' if is_deg else ''}")
                print(f"      degenerate options: {deg or 'none'}")
                # does any option text carry a stray label token?
                for o in leaf.options:
                    if "2D." in o.text or " D." in o.text:
                        print(f"      !! option {o.label} text carries stray label token: "
                              f"{o.text.strip()[:70]!r}")

    OUT.joinpath("_review_mimo_trace.json").write_text(
        json.dumps({"note": "see stdout"}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
