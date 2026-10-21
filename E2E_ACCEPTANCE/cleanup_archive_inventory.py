"""Cleanup 1: archive old viewer data (with hashes first). Cleanup 2: evidence binding inventory.
Does NOT touch FROZEN_EVIDENCE/ or v2 files. Does NOT touch production.
"""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

# ---------- 1) archive old v1 viewer data ----------
ARCHIVE = OUT / "_ARCHIVE_v1_viewer_superseded"
ARCHIVE.mkdir(exist_ok=True)

old_candidates = [
    OUT / "viewer_data.json",
    OUT / "data.js",  # v1 data.js — careful: if index still refs it we must not break v2
]
# Check what index.html currently references
index = (OUT / "index.html").read_text(encoding="utf-8")
print("index.html refs data_v2.js:", "data_v2.js" in index)
print("index.html refs data.js:", 'src="data.js"' in index)

# Also old patched artifacts from improve/fix scripts
old_extra = [
    OUT / "_improve_options.py",
    OUT / "_fix_q4_opts.py",
    OUT / "_build_html.py",
    OUT / "_build_viewer.py",
    OUT / "_build_raw_viewer.py",
    OUT / "export_viewer_data.py",
    OUT / "export_raw_viewer_data.py",
]

archive_log = {
    "purpose": "v1 viewer data superseded — DO NOT use as current evidence",
    "reason": "v1 export applied option split/patch (improve_options / fix_q4_opts); replaced by RAW + v2 provenance",
    "files": [],
}

for p in old_candidates + old_extra:
    if not p.exists():
        continue
    rec = {
        "original_path": str(p.relative_to(OUT)),
        "sha256": sha(p),
        "bytes": p.stat().st_size,
        "version_use": "v1 viewer / helper — superseded",
    }
    dest = ARCHIVE / p.name
    if not dest.exists():
        shutil.move(str(p), str(dest))
        rec["archived_to"] = str(dest.relative_to(OUT))
        rec["moved"] = True
    else:
        rec["archived_to"] = str(dest.relative_to(OUT))
        rec["moved"] = False
    archive_log["files"].append(rec)
    print("archived", p.name, rec["sha256"][:12])

# ensure index no longer references removed data.js
index2 = (OUT / "index.html").read_text(encoding="utf-8")
assert "data_v2.js" in index2
assert 'src="data.js"' not in index2, "index still references old data.js"
print("index.html does not reference archived v1 data.js: OK")

(ARCHIVE / "ARCHIVE_MANIFEST.json").write_text(
    json.dumps(archive_log, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- 2) evidence binding inventory ----------
inv = {
    "purpose": "Evidence binding inventory — source_file declaration vs actual path vs SHA256",
    "note": "Freeze prevents later mutation; does NOT prove initial correctness. Bindings must be verified.",
    "subjects": {},
}

for subj in ["数学","物理","化学","英语","语文","政治","地理","历史","生物"]:
    e = {"subject": subj, "bindings": {}}
    man = OUT / "04_V3_INPUT" / f"{subj}.manifest.json"
    if man.exists():
        man_obj = json.loads(man.read_text(encoding="utf-8"))
        declared_src = man_obj.get("source_file")
        e["bindings"]["manifest"] = {
            "path": str(man.relative_to(OUT)),
            "sha256": sha(man),
            "declared_source_file": declared_src,
        }
        # find actual sealed md
        md_files = list((OUT / "02_PREPROCESSING_OUTPUT").glob("*.md"))
        actual_md = None
        for p in md_files:
            # match by filename stem of declared source
            if declared_src and Path(declared_src).name in p.name:
                actual_md = p
                break
        if actual_md is None:
            # match by hash if v2 has it
            pass
        if actual_md:
            e["bindings"]["preprocessing_md"] = {
                "path": str(actual_md.relative_to(OUT)),
                "sha256": sha(actual_md),
                "matches_declared_name": (Path(declared_src).name == actual_md.name) if declared_src else None,
            }
        else:
            e["bindings"]["preprocessing_md"] = {"path": None, "sha256": None, "error": "not matched"}
    # pdf
    pdfs = list((OUT / "01_INPUT_PDF").glob("*.pdf"))
    # use V2 hashes if available
    v2p = OUT / "viewer_data_raw_v2.json"
    v2 = json.loads(v2p.read_text(encoding="utf-8")) if v2p.exists() else {}
    subj_v2 = (v2.get("subjects") or {}).get(subj) or {}
    pdf_sha = (subj_v2.get("hashes") or {}).get("pdf")
    md_sha = (subj_v2.get("hashes") or {}).get("md")
    man_sha = (subj_v2.get("hashes") or {}).get("manifest")

    pdf_file = None
    for p in pdfs:
        if pdf_sha and sha(p) == pdf_sha:
            pdf_file = p
            break
    if pdf_file:
        e["bindings"]["input_pdf"] = {
            "path": str(pdf_file.relative_to(OUT)),
            "sha256": sha(pdf_file),
            "expected_sha_from_v2": pdf_sha,
            "sha_match": sha(pdf_file) == pdf_sha,
        }
    else:
        e["bindings"]["input_pdf"] = {"path": None, "expected_sha_from_v2": pdf_sha, "sha_match": False}

    md_file = None
    for p in (OUT / "02_PREPROCESSING_OUTPUT").glob("*.md"):
        if md_sha and sha(p) == md_sha:
            md_file = p
            break
    if md_file:
        e["bindings"]["preprocessing_md"] = {
            "path": str(md_file.relative_to(OUT)),
            "sha256": sha(md_file),
            "expected_sha_from_v2": md_sha,
            "sha_match": sha(md_file) == md_sha,
        }

    # pdf.txt
    pdf_txt = OUT / "05_V3_OUTPUT" / f"{subj}.pdf.txt"
    if pdf_txt.exists():
        e["bindings"]["pdf_text_extract"] = {
            "path": str(pdf_txt.relative_to(OUT)),
            "sha256": sha(pdf_txt),
            "derived_from": e["bindings"].get("input_pdf", {}).get("path"),
        }

    # v3 output
    v3 = OUT / "05_V3_OUTPUT" / f"{subj}.v3.json"
    if v3.exists():
        e["bindings"]["v3_output"] = {
            "path": str(v3.relative_to(OUT)),
            "sha256": sha(v3),
            "inputs": {
                "manifest": e["bindings"].get("manifest", {}).get("path"),
                "md": e["bindings"].get("preprocessing_md", {}).get("path"),
            },
        }

    # accepted md (03)
    acc = list((OUT / "03_OWNER_ACCEPTED").glob("*.md"))
    for p in acc:
        if md_sha and sha(p) == md_sha:
            e["bindings"]["owner_accepted_md"] = {
                "path": str(p.relative_to(OUT)),
                "sha256": sha(p),
                "identical_to_preprocessing": True,
            }
            break

    inv["subjects"][subj] = e
    print(subj, "pdf", e["bindings"].get("input_pdf", {}).get("sha_match"),
          "md", e["bindings"].get("preprocessing_md", {}).get("sha_match"),
          "man", "ok" if e["bindings"].get("manifest") else "MISSING")

(OUT / "EVIDENCE_BINDING_INVENTORY.json").write_text(
    json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote EVIDENCE_BINDING_INVENTORY.json")

# ---------- 3) correct C2/C5/C6 status ----------
report = OUT / "V2_PROVENANCE_REPORT.md"
if report.exists():
    t = report.read_text(encoding="utf-8")
    t = t.replace(
        "| C2 no leaf + original | **0** | PASS（无伪造） |",
        "| C2 no leaf + original | **0** | **UNVERIFIED**（当前路径无样本；零命中≠已验证） |",
    )
    t = t.replace(
        "| C5 replay != original | 0 | PASS |",
        "| C5 replay != original | 0 | **UNVERIFIED**（当前路径无样本） |",
    )
    t = t.replace(
        "| C6 replay error/missing | 0 | PASS |",
        "| C6 replay error/missing | 0 | **UNVERIFIED**（当前路径无样本） |",
    )
    t += """

## 裁定更正（Owner / DSH）
C2 / C5 / C6 **未验证**——当前路径没有相应样本。零命中不得记为 PASS。
C1 / C3 / C4 为当前路径实测样本（227 / 57 / 227）。

## 项目状态（非 COMPLETE 收口）
> Viewer 数据保真核验完成；已知选项结构缺陷待修复；正式产品链 E2E 待验证；九科人工验收尚未完成。

## 下一阶段（独立任务，本轮未启动）
- **任务 A**：Resolver 单行多选项缺陷修复 + 内容区间断言（A='1' B='2' C='π' D='2π'）+ 回归
- **任务 B**：正式产品链 E2E（TaskExecutor document_ingest → … → 前端），不以 Phase1 manifest Runner 代替
"""
    report.write_text(t, encoding="utf-8")
    print("updated V2_PROVENANCE_REPORT.md")

# status note
status = """# 项目状态（本轮收口）

Viewer 数据保真核验完成；已知选项结构缺陷待修复；正式产品链 E2E 待验证；九科人工验收尚未完成。

## 本轮完成
1. 旧版 v1 viewer 数据归档 → `_ARCHIVE_v1_viewer_superseded/`（含哈希清单，非删除）
2. 证据绑定清单 → `EVIDENCE_BINDING_INVENTORY.json`
   （manifest declared source_file ↔ 实际路径 ↔ SHA256 ↔ v3 输入/输出）
3. C2/C5/C6 更正为 **UNVERIFIED（无样本）**

## 明确未做
- 未修 Resolver / 未跑正式产品链 E2E / 未宣布九科验收通过
- 未改 FROZEN_EVIDENCE / v2 数据
"""
(OUT / "PROJECT_STATUS.md").write_text(status, encoding="utf-8")
print("wrote PROJECT_STATUS.md")
