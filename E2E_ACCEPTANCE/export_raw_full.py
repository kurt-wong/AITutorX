"""Re-export RAW with FULL texts + untruncated answers + sentinel fields.

Fail-closed S3: chem Q20 must show 5 options (incl E=还原反应); math Q4 option D text_raw == 'D'.
"""
from __future__ import annotations
import hashlib, json, os, re, sys, uuid
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

def extract_raw(man_path, md_path):
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
        leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        for leaf in leaves:
            cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
            if cl is None:
                questions.append({
                    "unit_id": root.unit_id, "leaf_id": leaf.unit_id,
                    "raw": True, "gate": "incomplete",
                    "reason": "IR incomplete / leaf absent",
                    "stem_raw": "", "options_raw": [], "answer_raw": "",
                    "answer_letter": None, "labels": [], "qtype": None,
                    "material_raw": "",
                })
                continue
            options_raw = [
                {"label": o.label, "text_raw": o.text, "span_id": o.span_id,
                 "line_refs": list(getattr(o, "line_refs", ()) or ())}
                for o in cl.options
            ]
            # UNTRUNCATED answer — truncation creates false unclosed $
            ans = cl.answer.text if cl.answer else ""
            letter = _answer_form_single_choice(_clean_answer(ans or ""))
            v = verify(cl.canonical_question_type, ans or "", [o.label for o in cl.options])
            try:
                gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                decision = gd.get("decision")
                greasons = (gd.get("reasons") or [])[:5]
            except Exception as e:
                decision, greasons = "error", [str(e)]
            if letter is None and ans:
                reason = "answer_not_expressible (answer-side / S0 family) — data may still be correct"
            elif decision == "auto_approve":
                reason = "strict-auto grammar OK"
            elif decision == "rejected":
                reason = "gate rejected"
            else:
                reason = "pending_review"
            questions.append({
                "unit_id": root.unit_id,
                "leaf_id": cl.unit_id,
                "qtype": cl.canonical_question_type,
                "raw": True,
                "gate": decision,
                "reason": reason,
                "gate_reasons": greasons,
                "verify": v,
                "stem_raw": cl.stem.text if cl.stem else "",
                "options_raw": options_raw,
                "answer_raw": ans,  # FULL
                "answer_letter": letter,
                "labels": [o.label for o in cl.options],
                "material_raw": "",
            })
    return questions

def main():
    # lock raw v3 hashes
    raw_v3 = {}
    for subj in SUBJECTS:
        p = OUT / "05_V3_OUTPUT" / f"{subj}.v3.json"
        if p.exists():
            raw_v3[subj] = hashlib.sha256(p.read_bytes()).hexdigest()

    meta = json.loads((OUT / "MANIFEST.json").read_text(encoding="utf-8"))
    viewer = {
        "run_id": meta.get("run_id"),
        "purpose": "Owner Viewer — RAW V3 + full-text Gate1 + read-only KaTeX",
        "frozen": meta.get("frozen"),
        "data_policy": {
            "raw_only": True,
            "no_option_split": True,
            "no_auto_complete": True,
            "no_text_truncation": True,
            "renderer_must_not_mutate_data": True,
        },
        "raw_v3_output_sha256": raw_v3,
        "git": meta.get("git"),
        "subjects": {},
        "sentinels": {
            "S3_chem_Q20": "options count must be 5 including E text containing 还原反应",
            "S3_math_Q4": "options_raw D text_raw must be exactly 'D'",
        },
    }

    for subj in SUBJECTS:
        s = meta["subjects"].get(subj, {})
        man = OUT / "04_V3_INPUT" / f"{subj}.manifest.json"
        md_p = None
        target = (s.get("preproc_md") or {}).get("sha256")
        for p in (OUT / "02_PREPROCESSING_OUTPUT").glob("*.md"):
            if hashlib.sha256(p.read_bytes()).hexdigest() == target:
                md_p = p
                break

        entry = {
            "subject": subj,
            "paper_label": s.get("paper_label"),
            "status": s.get("status", {}),
            "hashes": {
                "pdf": (s.get("pdf") or {}).get("sha256"),
                "md": (s.get("preproc_md") or {}).get("sha256"),
                "manifest": s.get("v3_manifest_sha256"),
            },
            # FULL text paths for Gate1 (not truncated)
            "pdf_text_path": f"05_V3_OUTPUT/{subj}.pdf.txt",
            "md_text_path": f"02_PREPROCESSING_OUTPUT/{md_p.name}" if md_p else None,
        }
        pdf_txt = OUT / "05_V3_OUTPUT" / f"{subj}.pdf.txt"
        if pdf_txt.exists():
            t = pdf_txt.read_text(encoding="utf-8")
            entry["pdf_text"] = t  # FULL — Gate1 needs this
            entry["pdf_text_len"] = len(t)
        else:
            entry["pdf_text"] = ""
            entry["pdf_text_len"] = 0
        if md_p:
            t = md_p.read_text(encoding="utf-8")
            entry["md_text"] = t  # FULL
            entry["md_text_len"] = len(t)
        else:
            entry["md_text"] = ""
            entry["md_text_len"] = 0

        if man.is_file() and md_p:
            qs = extract_raw(man, md_p)
            entry["questions"] = qs
            entry["n_questions"] = len(qs)
            entry["gate_counts"] = dict(Counter(q.get("gate") for q in qs))
            print(subj, len(qs), entry["gate_counts"])
        else:
            entry["questions"] = []
            print(subj, "MISSING")

        viewer["subjects"][subj] = entry

    # ---- S3 SENTINELS (fail-closed, never auto-fix) ----
    chem = viewer["subjects"].get("化学", {}).get("questions") or []
    q20 = next((q for q in chem if q.get("unit_id") == "Q20"), None)
    s3 = {"chem_Q20": None, "math_Q4": None, "ok": True}
    if q20 is None:
        s3["chem_Q20"] = "MISSING Q20"
        s3["ok"] = False
    else:
        n = len(q20.get("options_raw") or [])
        e_txt = next((o.get("text_raw") or "" for o in (q20.get("options_raw") or []) if o.get("label") == "E"), "")
        s3["chem_Q20"] = {"n_options": n, "E_text": e_txt[:80], "expect_n": 5}
        if n != 5 or "还原反应" not in e_txt:
            s3["ok"] = False
    math = viewer["subjects"].get("数学", {}).get("questions") or []
    q4 = next((q for q in math if q.get("unit_id") == "Q4"), None)
    if q4 is None:
        s3["math_Q4"] = "MISSING Q4"
        s3["ok"] = False
    else:
        d_txt = next((o.get("text_raw") or "" for o in (q4.get("options_raw") or []) if o.get("label") == "D"), None)
        s3["math_Q4"] = {"D_text_raw": d_txt, "expect": "D"}
        if d_txt != "D":
            s3["ok"] = False
    viewer["S3_sentinel_check"] = s3
    print("S3 sentinels:", json.dumps(s3, ensure_ascii=False))

    raw_path = OUT / "viewer_data_raw.json"
    raw_path.write_text(json.dumps(viewer, ensure_ascii=False), encoding="utf-8")
    # data.js mirrors it
    (OUT / "data.js").write_text(
        "window.E2E_DATA = " + json.dumps(viewer, ensure_ascii=False) + ";\n",
        encoding="utf-8")
    sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    print("viewer_data_raw.json sha256", sha)
    print("data.js bytes", (OUT/"data.js").stat().st_size)

    # verify raw v3 not mutated during export
    for subj, h in raw_v3.items():
        now = hashlib.sha256((OUT/"05_V3_OUTPUT"/f"{subj}.v3.json").read_bytes()).hexdigest()
        assert now == h
    print("raw V3 SHA unchanged: OK")
    if not s3["ok"]:
        print("WARNING: S3 SENTINEL FAIL — do not repair, report only")

if __name__ == "__main__":
    main()
