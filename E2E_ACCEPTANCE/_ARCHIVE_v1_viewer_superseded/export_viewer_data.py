"""Export full Question details + PDF text for Owner Viewer. READ-ONLY on production."""
from __future__ import annotations
import hashlib, json, os, re, sys, uuid
from pathlib import Path

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

def extract_pdf_text(pdf_path: Path, max_chars=200000) -> str:
    try:
        import pypdfium2 as pdfium
        pdf = pdfium.PdfDocument(str(pdf_path))
        parts = []
        for i, page in enumerate(pdf):
            try:
                tp = page.get_textpage()
                t = tp.get_text_bounded() or ""
            except Exception:
                t = ""
            parts.append(t)
            if sum(len(x) for x in parts) > max_chars:
                break
        return "\n\n---PAGE---\n\n".join(parts)
    except Exception as e:
        try:
            from pypdf import PdfReader
            r = PdfReader(str(pdf_path))
            return "\n\n---PAGE---\n\n".join((p.extract_text() or "") for p in r.pages)
        except Exception as e2:
            return f"[PDF_TEXT_EXTRACT_FAILED: {e}; {e2}]"

def load_md_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def extract_questions(man_path: Path, md_path: Path):
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
                    "status": "not_compiled", "gate": "incomplete",
                    "stem": "", "options": [], "answer_text": "", "answer_letter": None,
                    "material_preview": "", "reason": "IR incomplete / leaf absent",
                })
                continue
            opts = []
            for o in cl.options:
                opts.append({
                    "label": o.label,
                    "text": (o.text or "")[:500],
                    "span_id": o.span_id,
                })
            ans = cl.answer.text if cl.answer else ""
            letter = _answer_form_single_choice(_clean_answer(ans or ""))
            v = verify(cl.canonical_question_type, ans or "", [o.label for o in cl.options])
            try:
                gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                decision = gd.get("decision")
                reasons = (gd.get("reasons") or [])[:4]
            except Exception as e:
                decision, reasons = "error", [str(e)]
            # reason classification for owner
            if letter is None and ans:
                reason = "answer_not_expressible (answer-side / S0 family) — data may still be correct"
            elif decision == "auto_approve":
                reason = "strict-auto grammar OK"
            elif decision == "rejected":
                reason = "gate rejected (structural/provenance/semantic)"
            else:
                reason = "pending_review"
            questions.append({
                "unit_id": root.unit_id,
                "leaf_id": cl.unit_id,
                "qtype": cl.canonical_question_type,
                "gate": decision,
                "reason": reason,
                "gate_reasons": reasons,
                "verify": v,
                "stem": (cl.stem.text if cl.stem else "")[:800],
                "options": opts,
                "answer_text": ans[:300] if ans else "",
                "answer_letter": letter,
                "n_options": len(opts),
                "labels": [o.label for o in cl.options],
            })
    return questions

def main():
    meta = json.loads((OUT/"MANIFEST.json").read_text(encoding="utf-8"))
    viewer = {
        "run_id": meta.get("run_id"),
        "purpose": meta.get("purpose"),
        "frozen": meta.get("frozen"),
        "note": (
            "Owner Viewer — Gate1 PDF↔MD diff; Gate2 full Question display. "
            "auto/pending/rejected are MACHINE STATUS, not correctness verdicts. "
            "No production code changed."
        ),
        "git": meta.get("git"),
        "subjects": {},
    }

    for subj in SUBJECTS:
        s = meta["subjects"].get(subj, {})
        entry = {
            "subject": subj,
            "paper_label": s.get("paper_label"),
            "status": s.get("status", {}),
            "hashes": {
                "pdf": (s.get("pdf") or {}).get("sha256"),
                "md": (s.get("preproc_md") or {}).get("sha256"),
                "manifest": s.get("v3_manifest_sha256"),
            },
        }
        # locate sealed files
        pdf_files = list((OUT/"01_INPUT_PDF").glob("*.pdf"))
        md_files = list((OUT/"02_PREPROCESSING_OUTPUT").glob("*.md"))
        man = OUT/"04_V3_INPUT"/f"{subj}.manifest.json"
        # match by subject's known paper label / hashes
        pdf_p = None
        for p in pdf_files:
            if s.get("pdf") and hashlib.sha256(p.read_bytes()).hexdigest() == s["pdf"]["sha256"]:
                pdf_p = p
                break
        md_p = None
        for p in md_files:
            if s.get("preproc_md") and hashlib.sha256(p.read_bytes()).hexdigest() == s["preproc_md"]["sha256"]:
                md_p = p
                break

        if pdf_p:
            pdf_text = extract_pdf_text(pdf_p)
            (OUT/"05_V3_OUTPUT"/f"{subj}.pdf.txt").write_text(pdf_text, encoding="utf-8")
            entry["pdf_text_path"] = f"05_V3_OUTPUT/{subj}.pdf.txt"
            entry["pdf_text_len"] = len(pdf_text)
            entry["pdf_text_preview"] = pdf_text[:1500]
        else:
            entry["pdf_text_path"] = None
            entry["pdf_text_preview"] = ""

        if md_p:
            md_text = load_md_text(md_p)
            entry["md_text_path"] = f"02_PREPROCESSING_OUTPUT/{md_p.name}"
            entry["md_text_len"] = len(md_text)
            entry["md_text_preview"] = md_text[:1500]
        else:
            entry["md_text_preview"] = ""

        if man.is_file() and md_p:
            try:
                qs = extract_questions(man, md_p)
                entry["questions"] = qs
                entry["n_questions"] = len(qs)
                # machine status rollup
                from collections import Counter
                c = Counter(q.get("gate") for q in qs)
                entry["gate_counts"] = dict(c)
                print(f"{subj}: {len(qs)} questions, gates={dict(c)}")
            except Exception as e:
                entry["questions"] = []
                entry["extract_error"] = f"{type(e).__name__}: {e}"
                print(f"{subj}: EXTRACT FAIL {e}")
        else:
            entry["questions"] = []
            print(f"{subj}: missing man/md")

        viewer["subjects"][subj] = entry

    (OUT/"viewer_data.json").write_text(json.dumps(viewer, ensure_ascii=False), encoding="utf-8")
    print("wrote viewer_data.json", (OUT/"viewer_data.json").stat().st_size)

if __name__ == "__main__":
    main()
