from __future__ import annotations
import hashlib, json, os, shutil, sys, uuid, datetime, subprocess
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

SEL = {
 "数学": (r"D:\Project\Papers\original\BaiduSyncdisk\高三\2018\合格考试\数学\2018北京春季高中会考数学（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\数学\2018北京春季高中会考数学（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\数学\2018北京春季高中会考数学（教师版）(1).manifest.json",
     "2018北京春季高中会考数学"),
 "物理": (r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\物理\2018北京夏季高中会考物理（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\物理\2018北京夏季高中会考物理（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\物理\2018北京夏季高中会考物理（教师版）(1).manifest.json",
     "2018北京夏季高中会考物理"),
 "化学": (r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\化学\2018北京春季高中会考化学（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\化学\2018北京春季高中会考化学（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\化学\2018北京春季高中会考化学（教师版）(1).manifest.json",
     "2018北京春季高中会考化学"),
 "英语": (r"D:\Project\Papers\original\BaiduSyncdisk\高三\2018\合格考试\英语\2018北京春季高中会考英语（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\英语\2018北京春季高中会考英语（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\英语\2018北京春季高中会考英语（教师版）(1).manifest.json",
     "2018北京春季高中会考英语"),
 "语文": (r"D:\Project\Papers\original\BaiduSyncdisk\高三\2018\合格考试\语文\2018北京春季高中会考语文（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\语文\2018北京春季高中会考语文（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\语文\2018北京春季高中会考语文（教师版）(1).manifest.json",
     "2018北京春季高中会考语文"),
 "政治": (r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\政治\2018北京夏季高中会考政治（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\政治\2018北京夏季高中会考政治（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\政治\2018北京夏季高中会考政治（教师版）(1).manifest.json",
     "2018北京夏季高中会考政治"),
 "地理": (r"D:\Project\Papers\original\BaiduSyncdisk\高一\2018\合格考试\地理\2018北京春季高中会考地理（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\地理\2018北京春季高中会考地理（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\地理\2018北京春季高中会考地理（教师版）(1).manifest.json",
     "2018北京春季高中会考地理"),
 "历史": (r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\历史\2018北京夏季高中会考历史（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\历史\2018北京夏季高中会考历史（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\历史\2018北京夏季高中会考历史（教师版）(1).manifest.json",
     "2018北京夏季高中会考历史"),
 "生物": (r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\生物\2018北京春季高中会考生物（教师版）.pdf",
     r"D:\Project\Papers\Ocr-markdown\会考\生物\2018北京春季高中会考生物（教师版）(1).md",
     r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\生物\2018北京春季高中会考生物（教师版）(1).manifest.json",
     "2018北京春季高中会考生物"),
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run_v3(man_path, md_path):
    m = load_manifest(man_path)
    srs = load_source_lines(md_path)
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(s.line_ref, s.text, s.seq, s.page_no, s.line_no_in_page) for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(payload,
        {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {v.line_ref: v for v in views}
    compiled = Compiler(span_map, line_map).compile(ir)
    n_ready = n_incomplete = n_auto = n_pending = n_rej = 0
    questions = []
    for root in ir.units:
        leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        if root.semantic_status == "ready":
            n_ready += 1
        else:
            n_incomplete += 1
        for leaf in leaves:
            cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
            labels = [o.label for o in (cl.options if cl else [])]
            ans_text = cl.answer.text if cl and cl.answer else None
            letter = _answer_form_single_choice(_clean_answer(ans_text or "")) if ans_text else None
            v = verify(cl.canonical_question_type, ans_text or "", labels) if cl else None
            try:
                decision = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run).get("decision")
            except Exception as e:
                decision = f"error:{e}"
            if decision == "auto_approve":
                n_auto += 1
            elif decision == "rejected":
                n_rej += 1
            else:
                n_pending += 1
            questions.append({
                "unit_id": root.unit_id,
                "labels": labels,
                "answer_letter": letter,
                "answer_preview": (ans_text or "")[:80],
                "verify": v,
                "gate": decision,
                "n_options": len(labels),
                "stem_preview": (cl.stem.text[:100] if cl and cl.stem else ""),
            })
    return {
        "ir_ready": n_ready, "ir_incomplete": n_incomplete,
        "gate_auto": n_auto, "gate_pending": n_pending, "gate_rejected": n_rej,
        "n_units": len(ir.units), "n_questions_tracked": len(questions),
        "questions": questions[:15],
    }

def main():
    for d in ["01_INPUT_PDF","02_PREPROCESSING_OUTPUT","03_OWNER_ACCEPTED","04_V3_INPUT","05_V3_OUTPUT"]:
        (OUT/d).mkdir(parents=True, exist_ok=True)
    meta = {
        "run_id": "E2E-ACCEPT-" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "purpose": "9-subject formal E2E Acceptance Run Round 1",
        "frozen": {"P1.4_B": "FROZEN", "no_fix": True},
        "preprocessing_note": (
            "MD = official Ocr-markdown product (not re-OCR this round). "
            "PDF hash recorded. Manifest = reslice-batch-C structural annotation."
        ),
        "subjects": {},
    }
    for repo, key in [(r"D:\Project\AITutors-v3","AITutors_v3_HEAD"), (r"D:\Project\Papers","Papers_HEAD")]:
        try:
            meta.setdefault("git", {})[key] = subprocess.check_output(
                ["git","rev-parse","HEAD"], cwd=repo, text=True).strip()
        except Exception as e:
            meta.setdefault("git", {})[key] = str(e)

    for subject, (pdf_s, md_s, man_s, label) in SEL.items():
        pdf, md, man = Path(pdf_s), Path(md_s), Path(man_s)
        e = {"subject": subject, "paper_label": label, "status": {}}
        if not pdf.is_file():
            e["status"]["gate0"] = "FAIL_MISSING_PDF"
            meta["subjects"][subject] = e
            print(subject, "FAIL pdf")
            continue
        dp = OUT/"01_INPUT_PDF"/pdf.name
        if not dp.exists():
            shutil.copy2(pdf, dp)
        e["pdf"] = {"sha256": sha(dp), "bytes": dp.stat().st_size, "name": pdf.name}

        if not md.is_file():
            e["status"]["gate1"] = "FAIL_MISSING_MD"
            meta["subjects"][subject] = e
            print(subject, "FAIL md")
            continue
        dm = OUT/"02_PREPROCESSING_OUTPUT"/md.name
        if not dm.exists():
            shutil.copy2(md, dm)
        e["preproc_md"] = {"sha256": sha(dm), "bytes": dm.stat().st_size,
                           "lines": sum(1 for _ in dm.open(encoding="utf-8"))}

        da = OUT/"03_OWNER_ACCEPTED"/md.name
        if not da.exists():
            shutil.copy2(dm, da)
        e["owner_accepted"] = {
            "sha256": sha(da),
            "identical_to_preproc": sha(da)==sha(dm),
            "owner_decision": "AWAITING_OWNER",
        }

        if not man.is_file():
            e["status"]["gate2"] = "FAIL_MISSING_MANIFEST"
            meta["subjects"][subject] = e
            print(subject, "FAIL manifest")
            continue
        dman = OUT/"04_V3_INPUT"/f"{subject}.manifest.json"
        if not dman.exists():
            shutil.copy2(man, dman)
        e["v3_manifest_sha256"] = sha(dman)

        try:
            res = run_v3(dman, da)
            op = OUT/"05_V3_OUTPUT"/f"{subject}.v3.json"
            op.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
            e["v3"] = {k: res[k] for k in (
                "ir_ready","ir_incomplete","gate_auto","gate_pending",
                "gate_rejected","n_units","n_questions_tracked")}
            e["v3"]["output_sha256"] = sha(op)
            e["status"]["gate2_machine"] = "PASS_COMPLETED" if res["n_units"]>0 else "FAIL_EMPTY"
            e["status"]["gate2_owner"] = "AWAITING_OWNER"
            e["status"]["gate1_owner"] = "AWAITING_OWNER"
        except Exception as ex:
            e["status"]["gate2_machine"] = f"FAIL_ERROR:{type(ex).__name__}:{ex}"
        meta["subjects"][subject] = e
        print(f"{subject}: {e['status'].get('gate2_machine')} auto={e.get('v3',{}).get('gate_auto')} "
              f"pend={e.get('v3',{}).get('gate_pending')} rej={e.get('v3',{}).get('gate_rejected')}")

    (OUT/"MANIFEST.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("WROTE MANIFEST.json")

if __name__ == "__main__":
    main()
