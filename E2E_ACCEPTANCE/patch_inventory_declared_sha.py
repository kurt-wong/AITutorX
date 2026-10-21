"""Inventory patch: declared_source_sha256 + OCR ledger scope note.
Only touches EVIDENCE_BINDING_INVENTORY.json + generation script.
Does NOT re-export questions. Does NOT modify FROZEN/v2 baselines.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
inv_path = OUT / "EVIDENCE_BINDING_INVENTORY.json"
inv = json.loads(inv_path.read_text(encoding="utf-8"))

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

# scope notes (Advice b)
inv["evidence_scope"] = {
    "this_inventory_proves": (
        "Acceptance-package INTERNAL bindings: declared source_file, actual path, "
        "SHA-256 of packaged files, and v3 input/output correspondence."
    ),
    "upstream_ocr_provenance": (
        "PDF ↔ OCR-output source correspondence is provided by "
        "Papers/data/ocr_output_manifest.jsonl (OCR ledger). "
        "See notes.upstream_ocr_ledger below."
    ),
    "hash_match_does_NOT_prove": [
        "OCR content is correct (needs human Gate 1 / Owner acceptance)",
        "formal V3 product chain (TaskExecutor document_ingest → … → frontend) is verified",
        "initial binding was correct at generation time — only that current files match recorded hashes",
    ],
}
inv["notes"] = {
    "upstream_ocr_ledger": {
        "path": "D:/Project/Papers/data/ocr_output_manifest.jsonl",
        "role": "upstream source credential for PDF → OCR markdown",
        "scope": "outside acceptance package; not re-verified in this inventory",
    },
    "declared_source_sha256_meaning": (
        "source_content_sha256 from manifest (if present) is the Producer-declared hash "
        "of the source document; actual_sha256 is the hash of the file currently on disk. "
        "match=false means declared vs actual diverge (wrong file bound or file changed)."
    ),
}

# Advice a: declared_source_sha256 + actual binding check per subject
for subj, e in inv.get("subjects", {}).items():
    b = e.setdefault("bindings", {})
    man_rec = b.get("manifest") or {}
    man_path = man_rec.get("path")
    declared_src = man_rec.get("declared_source_file")
    declared_sha = None
    source_content_sha256 = None
    if man_path and (OUT / man_path).exists():
        man_obj = json.loads((OUT / man_path).read_text(encoding="utf-8"))
        source_content_sha256 = man_obj.get("source_content_sha256")
        declared_src = man_obj.get("source_file") or declared_src

    # actual md currently bound
    md_rec = b.get("preprocessing_md") or {}
    actual_md_path = md_rec.get("path")
    actual_md_sha = md_rec.get("sha256")

    # declared file path may live outside package (Papers / corpus)
    declared_path = Path(declared_src) if declared_src else None
    declared_file_exists = declared_path.is_file() if declared_path else None
    declared_file_sha = None
    if declared_path and declared_path.is_file():
        declared_file_sha = sha(declared_path)

    # mechanical checks
    checks = {
        "manifest_has_source_content_sha256": source_content_sha256 is not None,
        "declared_source_file_exists": declared_file_exists,
        "packaged_md_sha_matches_declared_source_file": (
            (actual_md_sha == declared_file_sha)
            if (actual_md_sha and declared_file_sha) else None
        ),
        "packaged_md_sha_matches_source_content_sha256": (
            (actual_md_sha == source_content_sha256)
            if (actual_md_sha and source_content_sha256) else None
        ),
    }
    b["declared_source_sha256"] = {
        "declared_source_file": declared_src,
        "source_content_sha256": source_content_sha256,
        "declared_source_file_exists": declared_file_exists,
        "declared_source_file_sha256": declared_file_sha,
        "packaged_md_sha256": actual_md_sha,
        "packaged_md_path": actual_md_path,
        "checks": checks,
    }
    print(subj,
          "sc", bool(source_content_sha256),
          "declared_exists", declared_file_exists,
          "md==declared", checks["packaged_md_sha_matches_declared_source_file"],
          "md==sc", checks["packaged_md_sha_matches_source_content_sha256"])

inv_path.write_text(json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")

# summary rollup
n = len(inv.get("subjects", {}))
n_sc = sum(1 for e in inv["subjects"].values()
           if (e["bindings"].get("declared_source_sha256") or {}).get("source_content_sha256"))
n_md_decl = sum(1 for e in inv["subjects"].values()
                if (e["bindings"].get("declared_source_sha256") or {}).get("checks", {})
                .get("packaged_md_sha_matches_declared_source_file") is True)
n_md_sc = sum(1 for e in inv["subjects"].values()
              if (e["bindings"].get("declared_source_sha256") or {}).get("checks", {})
              .get("packaged_md_sha_matches_source_content_sha256") is True)
print(f"subjects={n} has_sc={n_sc} md==declared_file={n_md_decl} md==source_content_sha256={n_md_sc}")

# append to project status (small)
status = OUT / "PROJECT_STATUS.md"
if status.exists():
    t = status.read_text(encoding="utf-8")
    if "declared_source_sha256" not in t:
        t += """
## 清单小修订（本轮）
- `EVIDENCE_BINDING_INVENTORY.json` 增加 `declared_source_sha256`：
  `source_content_sha256` / `declared_source_file_sha256` / `packaged_md_sha256` 与三项 checks
- 增加 `evidence_scope`：本清单只证包内绑定；上游 PDF↔OCR 由 `Papers/data/ocr_output_manifest.jsonl` 凭证；
  **哈希匹配 ≠ OCR 内容正确 ≠ 正式产品链已验证**
- 未重导出题目数据；未改 FROZEN / v2 基线；**未启动任务 A / B**
"""
        status.write_text(t, encoding="utf-8")
print("done")
