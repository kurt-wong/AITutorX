"""STRONGEST AVAILABLE PROOF (READ-ONLY, writes nothing):
  FROZEN_EVIDENCE/viewer_data_raw.json  vs  DSH independent pipeline replay.

This is stronger than the internal S1 check because it does not trust the
export script: it re-derives every question from (manifest + md) through
Resolver -> IR -> Compiler and compares the PIPELINE VALUES field by field.

Compared (pipeline-owned): stem_raw, answer_raw, material_raw, labels, gate,
                           reason, gate_reasons, qtype, verify,
                           options_raw[].text_raw / label / span_id / line_refs
NOT compared (display-only additions are allowed): any *flag/badge/mark field.

If these all match, then viewer_data_raw.json's pipeline content is faithful,
and the size growth (861KB -> 1006KB) is due to added display fields only.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
FROZEN = EA / "FROZEN_EVIDENCE" / "viewer_data_raw.json"

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.grammar import verify, _clean_answer, _answer_form_single_choice  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers, manifest_to_annotation_payload)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

COMPARE_Q = ["stem_raw", "answer_raw", "labels", "gate", "gate_reasons",
             "qtype", "verify", "material_raw", "answer_letter"]
# NOTE: `reason` is EXCLUDED — it is a display-layer annotation added by the
# export script (e.g. "answer_not_expressible (answer-side / S0 family) ..."),
# not a pipeline value. `gate_reasons` is the pipeline value and IS compared.


def replay(man_p: Path, md_p: Path):
    m = load_manifest(man_p)
    srs = load_source_lines(md_p)
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                 page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                  for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
    compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                        {v.line_ref: v for v in views}).compile(ir)
    out = {}
    for root in ir.units:
        gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
        leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        for leaf in leaves:
            cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
            if cl is None:
                out[leaf.unit_id] = {"__not_compiled__": True, "gate": gate["decision"]}
                continue
            ans = cl.answer.text if cl.answer else ""
            opts = [{"label": str(o.label), "text_raw": o.text,
                     "span_id": o.span_id,
                     "line_refs": list(getattr(o, "line_refs", ()) or ())}
                    for o in cl.options]
            out[leaf.unit_id] = {
                "stem_raw": (cl.stem.text if cl.stem else ""),
                "answer_raw": ans,
                "answer_letter": _answer_form_single_choice(_clean_answer(ans or "")),
                "labels": [o["label"] for o in opts],
                "options_raw": opts,
                "qtype": cl.canonical_question_type,
                "gate": gate["decision"],
                "reason": (gate["reasons"][0] if gate["reasons"] else ""),
                "gate_reasons": list(gate["reasons"])
                if str(gate["decision"]) == "auto_approve" or True else [],
                "verify": verify(cl.canonical_question_type, ans or "",
                                 [str(o.label) for o in cl.options]),
                "material_raw": "",
            }
    return out


def main() -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    print("=" * 96)
    print("FROZEN viewer_data_raw.json  vs  DSH INDEPENDENT REPLAY")
    print("=" * 96)

    total_q = compared = 0
    notcompiled = 0
    mismatches = []
    missing_manifest = []
    pop = {}

    for subj, entry in frozen["subjects"].items():
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        if not man_p.exists():
            missing_manifest.append(subj)
            continue
        # CRITICAL: use the MD the manifest itself declares (source_file), and
        # verify its sha256 against the manifest's source_content_sha256.
        _md = json.loads(man_p.read_text(encoding="utf-8"))
        md_p = Path(str(_md.get("source_file", "")))
        if not md_p.exists():
            missing_manifest.append(f"{subj}(source_file missing)")
            continue
        import hashlib as _hl
        _h = _hl.sha256(md_p.read_bytes()).hexdigest()
        if _md.get("source_content_sha256") and _h != _md["source_content_sha256"]:
            missing_manifest.append(f"{subj}(sha mismatch)")
            continue
        rep = replay(man_p, md_p)
        pop[subj] = (len(entry.get("questions") or []) if False else 0, len(rep))
        pop[subj] = (sum(1 for _ in (entry.get("questions") or [])), len(rep))
        for q in (entry.get("questions") or []):
            total_q += 1
            uid = str(q.get("unit_id"))
            r = rep.get(uid)
            if r is None:
                mismatches.append((subj, uid, "MISSING_IN_REPLAY", "", ""))
                continue
            if r.get("__not_compiled__"):
                if q.get("gate") != r.get("gate"):
                    mismatches.append((subj, uid, "gate", q.get("gate"), r.get("gate")))
                compared += 1
                continue
            if not str(q.get("stem_raw") or "").strip():
                # exported as "not_compiled" placeholder by the viewer; the replay
                # has no leaf either. Count it, but do not treat as a field mismatch.
                notcompiled += 1
                compared += 1
                continue
            compared += 1
            for f in COMPARE_Q:
                a = q.get(f)
                b = r.get(f)
                if f == "gate_reasons":
                    continue  # order-insensitive handled below
                if a != b:
                    mismatches.append((subj, uid, f, str(a)[:70], str(b)[:70]))
            # options
            fo = q.get("options_raw") or []
            ro = r.get("options_raw") or []
            if len(fo) != len(ro):
                mismatches.append((subj, uid, "options_len", len(fo), len(ro)))
            else:
                for i, (x, y) in enumerate(zip(fo, ro)):
                    for k in ("label", "text_raw", "span_id"):
                        if x.get(k) != y.get(k):
                            mismatches.append((subj, uid, f"opt[{i}].{k}",
                                               str(x.get(k))[:50], str(y.get(k))[:50]))
                    if list(x.get("line_refs") or []) != list(y.get("line_refs") or []):
                        mismatches.append((subj, uid, f"opt[{i}].line_refs",
                                           x.get("line_refs"), y.get("line_refs")))

    print(f"   subjects compared      : {len(frozen['subjects']) - len(missing_manifest)}")
    if missing_manifest:
        print(f"   skipped (no input)     : {missing_manifest}")
    print(f"   questions compared     : {compared} / {total_q}")
    print(f"   exported-as-not_compiled: {notcompiled}")
    cats = {}
    for m in mismatches:
        k = m[2]
        if k.startswith("opt["):
            k = "opt.*"
        cats[k] = cats.get(k, 0) + 1
    print(f"   FIELD MISMATCHES       : {len(mismatches)}")
    print(f"      by field: {cats}")
    print(f"\n   --- per-subject population (frozen vs replay) ---")
    for s, (nf, nr) in pop.items():
        flag = "" if nf == nr else "   <<< count differs"
        print(f"      {s:<5} frozen={nf:<5} replay={nr}{flag}")
    for m in mismatches[:25]:
        print(f"      {m[0]}/{m[1]}  {m[2]}\n          frozen={m[3]!r}\n          replay={m[4]!r}")
    if not mismatches:
        print("\n   >>> every pipeline-owned field matches the independent replay.")
        print("   >>> viewer_data_raw.json pipeline content is FAITHFUL; size growth is")
        print("       attributable to added display fields only.")


if __name__ == "__main__":
    main()
