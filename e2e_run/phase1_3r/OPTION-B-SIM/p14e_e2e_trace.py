"""P1.4-E2E-TRACE: four questions + golden path — READ-ONLY text at each layer."""
from __future__ import annotations
import hashlib, json, os, sys, uuid
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
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
    attach_material_boundary_markers, manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

OFFICIAL_MD_ROOT = Path(r"D:\Project\Papers\Ocr-markdown")
BATCH = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")

TARGETS = [
    ("化学", "Q20", "cross-line option D (涉及了氧 / 还原反应)"),
    ("数学", "Q4", "digit-glued 2D. option boundary"),
    ("化学", "Q23", "trailing unlabeled 4th option"),
    ("历史", "Q29", "space-sep D 麦哲伦"),
    ("化学", "Q22", "GOLDEN PATH control (normal A/B/C/D)"),
]

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest().hexdigest() if False else hashlib.sha256(p.read_bytes()).hexdigest().upper()

def find_official_md(paper: str, name_sub: str) -> Path | None:
    # search official Ocr-markdown for matching paper
    for p in OFFICIAL_MD_ROOT.rglob("*.md"):
        if paper in str(p) and name_sub in p.name:
            return p
    return None

def main():
    rows = []
    for paper, uid, purpose in TARGETS:
        man_path = next(BATCH.glob(f"{paper}/*.manifest.json"), None)
        if not man_path:
            rows.append({"unit": uid, "error": "no manifest"})
            continue
        m = load_manifest(man_path)
        src_path = Path(m.source_file)
        srs = load_source_lines(src_path)
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)

        mu = next((u for u in m.units if u.unit_id == uid), None)
        root = next((u for u in ir.units if u.unit_id == uid), None)
        leaf = next((l for l in compiled.leaves if l.unit_id == uid or l.unit_id.startswith(uid)), None)

        # official md identity
        official = find_official_md(paper, src_path.stem.split("（")[0][-8:] if False else "")
        # simpler: match by filename
        official = None
        for p in OFFICIAL_MD_ROOT.rglob("*.md"):
            if p.name == src_path.name:
                official = p
                break
        md_identical = None
        official_sha = batch_sha = None
        if official and official.is_file():
            official_sha = sha256_file(official)
            batch_sha = sha256_file(src_path)
            md_identical = official_sha == batch_sha

        # L0 preprocessing: raw source lines around unit
        if mu:
            lo = (mu.options_lines or mu.stem_lines or mu.questions_lines or (1, 1))[0]
            hi = (mu.options_lines or mu.stem_lines or mu.questions_lines or (1, 1))[1]
            lo = max(1, lo - 2)
            hi = min(len(texts), hi + 2)
            source_excerpt = [{"line": i, "text": texts[i-1]} for i in range(lo, hi + 1)]
        else:
            source_excerpt = []

        # L1 manifest/Producer declaration
        man_decl = None
        if mu:
            man_decl = {
                "unit_id": mu.unit_id,
                "qtype": mu.original_question_type,
                "question_numbers": list(mu.question_numbers),
                "stem_lines": list(mu.stem_lines) if mu.stem_lines else None,
                "options_lines": list(mu.options_lines) if mu.options_lines else None,
                "options": [{"label": o.label, "start_line": o.start_line, "end_line": o.end_line}
                            for o in (mu.options or ())],
                "answer_lines": list(mu.answer_lines) if mu.answer_lines else None,
            }

        # L2 annotation payload options
        ann_opts = None
        if root is not None or mu:
            # find in payload
            for su in payload.get("semantic_units", []):
                if su.get("unit_id") == uid:
                    content = su.get("content") or {}
                    # composite
                    for sq in su.get("sub_questions") or []:
                        c = sq.get("content") or {}
                        if c.get("options"):
                            ann_opts = c.get("options")
                    if content.get("options"):
                        ann_opts = content.get("options")
                    break

        # L3 resolved spans for options
        resolved_opts = []
        for s in run.resolved_spans:
            if s.role == "option" and (uid in s.span_id or (leaf and leaf.unit_id in s.span_id)):
                resolved_opts.append({
                    "span_id": s.span_id,
                    "label": getattr(s, "label", None) or s.span_id.rsplit(".", 1)[-1],
                    "line_refs": list(s.line_refs),
                    "text_preview": (getattr(s, "evidence", None) or str(getattr(s, "line_refs", "")))[:100],
                    "resolution": s.resolution_status,
                })
        # also from leaf options
        leaf_opts = []
        if leaf:
            for o in leaf.options:
                leaf_opts.append({
                    "label": o.label, "span_id": o.span_id,
                    "text_preview": (o.text or "")[:120],
                    "line_refs": list(getattr(o, "line_refs", ()) or ()),
                })

        # L4 IR
        ir_info = None
        if root is not None:
            ir_info = {
                "unit_id": root.unit_id,
                "unit_type": root.unit_type,
                "semantic_status": root.semantic_status,
                "question_numbers": list(getattr(root, "question_numbers", ()) or ()),
            }
            if leaf:
                ir_info["leaf"] = {
                    "unit_id": leaf.unit_id,
                    "qtype": leaf.canonical_question_type,
                    "stem_preview": (leaf.stem.text[:80] if leaf.stem else None),
                }

        # L5 compile + answer
        ans_letter = None
        ans_text = None
        verify_r = None
        labels = []
        if leaf:
            labels = [o.label for o in leaf.options]
            ans_text = leaf.answer.text if leaf.answer else None
            ans_letter = _answer_form_single_choice(_clean_answer(ans_text or ""))
            verify_r = verify(leaf.canonical_question_type, ans_text or "", labels)

        # L6 gate
        gate = None
        if root is not None and leaf is not None:
            gd = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            gate = {
                "decision": gd.get("decision"),
                "structural": gd["layers"]["structural"]["status"],
                "provenance": gd["layers"]["provenance"]["status"],
                "semantic": gd["layers"]["semantic"]["status"],
                "reasons": (gd.get("reasons") or [])[:6],
            }

        rows.append({
            "unit": uid,
            "paper": paper,
            "purpose": purpose,
            "md_identity": {
                "official_path": str(official) if official else None,
                "batch_path": str(src_path),
                "official_sha256": official_sha,
                "batch_sha256": batch_sha,
                "byte_identical": md_identical,
            },
            "L0_preprocessing_source_excerpt": source_excerpt,
            "L1_manifest_declaration": man_decl,
            "L2_annotation_options": ann_opts,
            "L3_resolved_option_spans": resolved_opts,
            "L3b_compiled_leaf_options": leaf_opts,
            "L4_ir": ir_info,
            "L5_compile_answer": {
                "labels": labels,
                "answer_text_preview": (ans_text or "")[:150],
                "answer_letter": ans_letter,
                "verify": verify_r,
            },
            "L6_gate": gate,
        })
        print(f"=== {paper} {uid} ({purpose}) ===")
        print(f"  md_identical={md_identical}")
        print(f"  manifest options={man_decl and man_decl['options']}")
        print(f"  leaf labels={labels} ans_letter={ans_letter} verify={verify_r}")
        print(f"  gate={gate and gate['decision']}")

    out = OUT / "p14e_e2e_trace.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out)

if __name__ == "__main__":
    main()
