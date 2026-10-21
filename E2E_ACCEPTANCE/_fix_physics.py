from pathlib import Path
import json, hashlib, shutil, sys, os, uuid

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
sys.path.insert(0, str(BACKEND))
for line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

# reuse runner
sys.path.insert(0, str(OUT))
from run_e2e_acceptance import run_v3, sha

pdf = Path(r"D:\Project\Papers\original\BaiduSyncdisk\高二\2018\合格考试\物理\2018北京春季高中会考物理（教师版）.pdf")
md = Path(r"D:\Project\Papers\Ocr-markdown\会考\物理\2018北京春季高中会考物理（教师版）(1).md")
man = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\物理\2018北京春季高中会考物理（教师版）(1).manifest.json")

meta = json.loads((OUT/"MANIFEST.json").read_text(encoding="utf-8"))
e = {"subject": "物理", "paper_label": "2018北京春季高中会考物理", "status": {}}

dp = OUT/"01_INPUT_PDF"/pdf.name
shutil.copy2(pdf, dp)
e["pdf"] = {"sha256": sha(dp), "bytes": dp.stat().st_size, "name": pdf.name}

dm = OUT/"02_PREPROCESSING_OUTPUT"/md.name
shutil.copy2(md, dm)
e["preproc_md"] = {"sha256": sha(dm), "bytes": dm.stat().st_size,
                   "lines": sum(1 for _ in dm.open(encoding="utf-8"))}

da = OUT/"03_OWNER_ACCEPTED"/md.name
shutil.copy2(dm, da)
e["owner_accepted"] = {"sha256": sha(da), "identical_to_preproc": sha(da)==sha(dm),
                       "owner_decision": "AWAITING_OWNER"}

dman = OUT/"04_V3_INPUT"/"物理.manifest.json"
shutil.copy2(man, dman)
e["v3_manifest_sha256"] = sha(dman)

res = run_v3(dman, da)
op = OUT/"05_V3_OUTPUT"/"物理.v3.json"
op.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
e["v3"] = {k: res[k] for k in (
    "ir_ready","ir_incomplete","gate_auto","gate_pending","gate_rejected",
    "n_units","n_questions_tracked")}
e["v3"]["output_sha256"] = sha(op)
e["status"]["gate2_machine"] = "PASS_COMPLETED"
e["status"]["gate2_owner"] = "AWAITING_OWNER"
e["status"]["gate1_owner"] = "AWAITING_OWNER"
meta["subjects"]["物理"] = e
(OUT/"MANIFEST.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("物理", e["status"]["gate2_machine"], e["v3"])
