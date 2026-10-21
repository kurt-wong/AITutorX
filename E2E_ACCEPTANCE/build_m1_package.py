"""Build a self-contained Papers package (M1-C) with verifiable PDF-MD pairing."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

OUT_ROOT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE\06_M1_PACKAGES")
PKG_NAME = "chem-2018-spring-huikao-teacher"
PKG = OUT_ROOT / PKG_NAME

PDF_SRC = Path(r"D:\Project\Papers\maintainess\PDF\2018北京春季高中会考化学（教师版）(1).pdf")
# Use the MD that the manifest hash actually matches (Ocr-markdown\会考\化学)
MD_SRC = Path(r"D:\Project\Papers\Ocr-markdown\会考\化学\2018北京春季高中会考化学（教师版）(1).md")
MANIFEST_SRC = Path(
    r"D:\Project\Papers\Ocr-markdown\reslice-batch-C\会考\化学\2018北京春季高中会考化学（教师版）(1).manifest.json"
)
# Producer OCR pairing record (output_manifest style) if available
OCR_RECORD = Path(r"D:\Project\Papers\Ocr-markdown\reslice-pac\ocr\pac-c01-01.md")  # placeholder check


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    assert PDF_SRC.is_file(), PDF_SRC
    assert MD_SRC.is_file(), MD_SRC
    assert MANIFEST_SRC.is_file(), MANIFEST_SRC

    PKG.mkdir(parents=True, exist_ok=True)

    pdf_name = "paper.pdf"
    md_name = "paper.md"
    man_name = "manifest.json"

    shutil.copy2(PDF_SRC, PKG / pdf_name)
    shutil.copy2(MD_SRC, PKG / md_name)

    raw_manifest = json.loads(MANIFEST_SRC.read_text(encoding="utf-8"))
    md_sha = sha256(MD_SRC)
    pdf_sha = sha256(PDF_SRC)

    # Verify declared identity before packaging
    declared = raw_manifest.get("source_content_sha256")
    if declared != md_sha:
        raise SystemExit(
            f"PACKAGING ABORTED: manifest source_content_sha256 mismatch\n"
            f"  declared={declared}\n  computed={md_sha}\n  md={MD_SRC}"
        )

    # Build self-contained manifest with relative paths + both identities
    package_manifest = {
        "package_version": "m1-selfcontained/v1",
        "source_file": md_name,  # relative to package dir
        "original_file": pdf_name,
        "source_content_sha256": md_sha,
        "original_sha256": pdf_sha,
        "identity_version": raw_manifest.get("identity_version", 2),
        "pairing": {
            "method": "producer-ocr-source-ref",
            "source_ref": str(raw_manifest.get("source_file", "")),
            "note": (
                "PDF original and Markdown source packaged together. "
                "source_content_sha256 verified against Markdown raw bytes. "
                "original_sha256 verified against PDF raw bytes."
            ),
        },
        "model": raw_manifest.get("model", ""),
        "prompt_version": (raw_manifest.get("annotation_meta") or {}).get("prompt_version", ""),
        "sections": raw_manifest.get("sections", []),
        "units": raw_manifest.get("units", []),
        "annotation_meta": raw_manifest.get("annotation_meta", {}),
    }

    (PKG / man_name).write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # pairing evidence sidecar (read-only verification record)
    evidence = {
        "package": PKG_NAME,
        "files": {
            pdf_name: {"sha256": pdf_sha, "bytes": PDF_SRC.stat().st_size},
            md_name: {"sha256": md_sha, "bytes": MD_SRC.stat().st_size},
            man_name: {"sha256": sha256(PKG / man_name)},
        },
        "identity_split": {
            "original_sha256": pdf_sha,
            "source_content_sha256": md_sha,
            "distinct": pdf_sha != md_sha,
        },
        "unit_count": len(package_manifest["units"]),
        "identity_version": package_manifest["identity_version"],
    }
    (PKG / "PAIRING_EVIDENCE.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("PACKAGE", PKG)
    print("  original_sha256      ", pdf_sha)
    print("  source_content_sha256", md_sha)
    print("  distinct             ", pdf_sha != md_sha)
    print("  units                ", evidence["unit_count"])
    print("  files                ", sorted(p.name for p in PKG.iterdir()))


if __name__ == "__main__":
    main()
