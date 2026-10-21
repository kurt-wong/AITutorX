"""Versioned export with Gate decision provenance (READ-ONLY on production).

Layering:
  leaf_present     — structural: compiled leaf exists?
  ir_status        — structural: ready / incomplete
  gate_original    — production/replay decision IF Gate was executed; else null
  gate_original_source — 'absent_no_leaf' | 'absent_ir_incomplete' | 'replay_evaluate' | ...
  gate_replay      — independent re-evaluate() now (clearly marked)
  gate_replay_source
  gate_display     — what Viewer shows (never fabricates a decision)
  reason_display   — display copy only; never overwrites gate_reasons

HARD RULES:
  - incomplete is NOT a legal gate decision
  - do not write FROZEN_EVIDENCE/
  - do not modify 05_V3_OUTPUT/*.v3.json
"""
from __future__ import annotations
import hashlib, json, os, sys, uuid
from pathlib import Path
from collections import Counter

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
sys.path.insert(0, str(BACKEND))
for line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler
from app.domains.compile.ir import IRBuilder
from app.domains.gate.policy import evaluate
from app.domains.gate.grammar import verify, _clean_answer, _answer_form_single_choice
from app.domains.resolver.resolver import SourceResolver
from app.domains.resolver.span import SourceLineView
from scripts.preprocessing_consumer.annotation_adapter import (
    attach_material_boundary_markers, manifest_to_annotation_payload)
from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"]
VERSION = "v2-gate-provenance"

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def extract(man_path: Path, md_path: Path):
    """Extract with layered gate provenance. Never invent gate_original."""
    m = load_manifest(man_path)
    srs = load_source_lines(md_path)
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(s.line_ref, s.text, s.seq, s.page_no, s.line_no_in_page) for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {v.line_ref: v for v in views}
    compiled = Compiler(span_map, line_map).compile(ir)

    questions = []
    for root in ir.units:
        # composite → leaves; standalone → self
        nodes = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        for leaf in nodes:
            cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
            leaf_present = cl is not None
            ir_status = leaf.semantic_status  # ready / incomplete
            options_raw = []
            if cl is not None:
                options_raw = [
                    {"label": o.label, "text_raw": o.text, "span_id": o.span_id,
                     "line_refs": list(getattr(o, "line_refs", ()) or ())}
                    for o in cl.options
                ]
            ans = cl.answer.text if cl and cl.answer else ""
            letter = _answer_form_single_choice(_clean_answer(ans or "")) if cl else None
            verify_r = None
            if cl is not None:
                verify_r = verify(cl.canonical_question_type, ans or "",
                                  [o.label for o in cl.options])

            # ---- ORIGINAL Gate: only when production would execute ----
            # Gate service: semantic_status != ready → skipped, NO evaluate, NO decision.
            # replay_phase1_e2e.py: same — continue without evaluate.
            gate_original = None
            gate_original_source = None
            gate_reasons_original = []
            if not leaf_present:
                gate_original = None
                gate_original_source = "absent_no_leaf"
            elif ir_status != "ready":
                gate_original = None
                gate_original_source = "absent_ir_incomplete_skipped"
            else:
                # ready + leaf → Gate would execute. This export runs evaluate once
                # as REPLAY of that decision (same pure function). Mark as replay-backed
                # original-equivalent, not as a DB row.
                try:
                    d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                    gate_original = d.get("decision")
                    gate_reasons_original = (d.get("reasons") or [])[:5]
                    gate_original_source = "evaluate_replay_equivalent"
                except Exception as e:
                    gate_original = None
                    gate_original_source = f"evaluate_error:{type(e).__name__}"
                    gate_reasons_original = [str(e)]

            # ---- INDEPENDENT replay (same call, recorded separately) ----
            gate_replay = None
            gate_replay_source = "not_run"
            gate_reasons_replay = []
            # always attempt replay for observability, including incomplete
            try:
                d2 = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                gate_replay = d2.get("decision")
                gate_reasons_replay = (d2.get("reasons") or [])[:5]
                gate_replay_source = "independent_evaluate_now"
            except Exception as e:
                gate_replay = None
                gate_replay_source = f"replay_error:{type(e).__name__}"
                gate_reasons_replay = [str(e)]

            # ---- DISPLAY: never fabricate ----
            if gate_original is not None:
                gate_display = gate_original
                gate_display_kind = "original_decision"
            elif not leaf_present:
                gate_display = None
                gate_display_kind = "no_decision_no_leaf"
            elif ir_status != "ready":
                gate_display = None
                gate_display_kind = "no_decision_ir_incomplete"
            else:
                gate_display = None
                gate_display_kind = "no_decision_other"

            if not leaf_present:
                reason_display = "IR incomplete / leaf absent（结构状态，非 Gate 决策）"
            elif ir_status != "ready":
                reason_display = "IR incomplete — Gate service 会 skip，不产 decision（非 Gate 决策）"
            elif gate_original == "auto_approve":
                reason_display = "strict-auto grammar OK"
            elif gate_original is None:
                reason_display = "无原始 Gate 决策"
            elif letter is None and ans:
                reason_display = "answer_not_expressible（answer-side / S0）— 题目数据可能完好"
            else:
                reason_display = gate_original or ""

            # replay agreement
            if gate_original is not None and gate_replay is not None:
                replay_match = (gate_original == gate_replay)
            else:
                replay_match = None  # N/A

            questions.append({
                "unit_id": root.unit_id,
                "leaf_id": cl.unit_id if cl else leaf.unit_id,
                "leaf_present": leaf_present,
                "ir_status": ir_status,
                "qtype": cl.canonical_question_type if cl else leaf.original_question_type,
                # provenance-split gate
                "gate_original": gate_original,
                "gate_original_source": gate_original_source,
                "gate_reasons_original": gate_reasons_original,
                "gate_replay": gate_replay,
                "gate_replay_source": gate_replay_source,
                "gate_reasons_replay": gate_reasons_replay,
                "replay_match": replay_match,
                "gate_display": gate_display,
                "gate_display_kind": gate_display_kind,
                "reason_display": reason_display,
                # raw content unchanged
                "stem_raw": cl.stem.text if cl and cl.stem else "",
                "options_raw": options_raw,
                "answer_raw": ans,
                "answer_letter": letter,
                "labels": [o.label for o in cl.options] if cl else [],
                "verify": verify_r,
            })
    return questions

def main():
    # lock hashes of frozen + v3 outputs BEFORE
    before = {}
    for p in list((OUT/"FROZEN_EVIDENCE").iterdir()) + list((OUT/"05_V3_OUTPUT").glob("*.v3.json")) + list((OUT/"05_V3_OUTPUT").glob("*.pdf.txt")):
        if p.is_file():
            before[str(p.relative_to(OUT))] = sha(p)

    frozen = json.loads((OUT/"FROZEN_EVIDENCE"/"viewer_data_raw.json").read_text(encoding="utf-8"))
    viewer = {
        "run_id": (frozen.get("run_id") or "") + "+" + VERSION,
        "purpose": "Owner Viewer — Gate decision provenance split",
        "version": VERSION,
        "data_policy": {
            "frozen_untouched": True,
            "incomplete_is_not_gate_decision": True,
            "no_fabricated_gate_original": True,
            "replay_marked_separately": True,
            "reason_display_does_not_overwrite_gate_reasons": True,
        },
        "field_provenance": {
            "leaf_present": "structural fact (compiled leaf exists)",
            "ir_status": "structural fact (ready|incomplete)",
            "gate_original": "Gate decision IFF Gate executed (ready+leaf); else null",
            "gate_original_source": "absent_no_leaf | absent_ir_incomplete_skipped | evaluate_replay_equivalent",
            "gate_replay": "independent evaluate() now — NEVER presented as original",
            "replay_match": "true/false/null (null = comparison N/A)",
            "gate_display": "what UI shows; null means NO decision (not rejected/approved)",
            "reason_display": "display copy only",
            "gate_reasons_original": "raw reasons from evaluate when it ran",
        },
        "raw_v3_output_sha256": frozen.get("raw_v3_output_sha256"),
        "FROZEN_BASELINE": frozen.get("FROZEN_BASELINE"),
        "subjects": {},
    }

    for subj in SUBJECTS:
        s = frozen["subjects"].get(subj, {})
        man = OUT/"04_V3_INPUT"/f"{subj}.manifest.json"
        md_p = None
        target = (s.get("hashes") or {}).get("md") or (s.get("preproc_md") or {}).get("sha256")
        # find md by hash or path
        for p in (OUT/"02_PREPROCESSING_OUTPUT").glob("*.md"):
            if target and sha(p) == target:
                md_p = p
                break
        if md_p is None and s.get("md_text_path"):
            cand = OUT/s["md_text_path"]
            if cand.is_file():
                md_p = cand

        entry = {
            "subject": subj,
            "paper_label": s.get("paper_label"),
            "hashes": s.get("hashes") or {},
            "pdf_text": s.get("pdf_text") or s.get("pdf_text_preview") or "",
            "md_text": s.get("md_text") or s.get("md_text_preview") or "",
            "option_anomaly_count": s.get("option_anomaly_count"),
            "owner_feedback_schema": s.get("owner_feedback"),
        }
        # carry option_integrity from frozen if present
        if man.is_file() and md_p:
            qs = extract(man, md_p)
            # merge option_integrity from frozen by unit_id
            frozen_qs = {q.get("unit_id"): q for q in (s.get("questions") or [])}
            for q in qs:
                fq = frozen_qs.get(q["unit_id"]) or {}
                q["option_integrity"] = fq.get("option_integrity")
                # keep raw fields identical check
                q["_raw_stem_sha"] = hashlib.sha256((q.get("stem_raw") or "").encode()).hexdigest()[:16]
            entry["questions"] = qs
            entry["n_questions"] = len(qs)
            c = Counter()
            for q in qs:
                key = q["gate_display"] if q["gate_display"] is not None else f"no_decision:{q['gate_display_kind']}"
                c[key] += 1
            entry["gate_display_counts"] = dict(c)
            print(subj, len(qs), dict(c))
        else:
            entry["questions"] = []
            print(subj, "MISSING man/md")

        viewer["subjects"][subj] = entry

    out_path = OUT / "viewer_data_raw_v2.json"
    out_path.write_text(json.dumps(viewer, ensure_ascii=False), encoding="utf-8")
    js_path = OUT / "data_v2.js"
    js_path.write_text("window.E2E_DATA = " + json.dumps(viewer, ensure_ascii=False) + ";\n", encoding="utf-8")

    # after hashes — frozen/v3/pdf.txt must be unchanged
    after = {}
    for k in before:
        p = OUT / k
        after[k] = sha(p)
    changed = {k for k in before if before[k] != after[k]}
    print("protected files changed:", changed or "NONE")
    assert not changed, changed

    manifest = {
        "version": VERSION,
        "viewer_data_raw_v2.json": sha(out_path),
        "data_v2.js": sha(js_path),
        "protected_unchanged": after,
        "protected_count": len(after),
    }
    (OUT / "V2_SHA256.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out_path)
    print("wrote", js_path)
    print("wrote V2_SHA256.json")

if __name__ == "__main__":
    main()
