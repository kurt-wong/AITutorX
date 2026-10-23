"""PDF → OCR/MD → Papers reslice → V3 formal → isolated DB (same-run artifacts).

Each stage consumes ONLY the previous stage's output from this run directory.
Fails closed at Papers/OCR if no product; never falls back to old md/manifest.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PAPERS = Path(r"D:\Project\Papers")
BACKEND = Path(r"D:\Project\AITutors-v3\backend")
PKG = Path(
    r"D:\Project\AITutor-X\E2E_ACCEPTANCE\06_M1_PACKAGES\chem-2018-spring-huikao-teacher"
)
PDF_SRC = PKG / "paper.pdf"
RUN_ROOT = Path(r"D:\Project\AITutor-X\e2e_run\pdf_chain_runs")
DB_URL = (
    "postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors_testsuite_chem_e2e"
)


def _parse_args(argv: list[str] | None = None):
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=Path, default=None, help="source PDF path")
    ap.add_argument("--db-url", default=None, help="isolated postgres async URL")
    return ap.parse_args(argv)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_manifest_identity(man_raw: dict, md_new: Path) -> tuple[int, str | None]:
    """Manifest source identity gate (production). Returns (exit_code, fail_reason).

    exit_code 0 = gate passed; 4 = rejected. fail_reason identifies the cause.
    Rejects: missing hash, non-hex / wrong-length hash, hash mismatch with md.
    """
    declared = str(man_raw.get("source_file") or "").replace("\\", "/")
    expected_sha = str(man_raw.get("source_content_sha256") or "").strip()
    if not expected_sha or len(expected_sha) != 64 or any(
        c not in "0123456789abcdef" for c in expected_sha.lower()
    ):
        return 4, f"manifest source_content_sha256 missing/invalid: {expected_sha!r}"
    md_name = md_new.name
    if Path(declared).name != md_name and md_name not in declared:
        return 4, (
            f"manifest source_file {declared!r} does not name this-run md {md_name!r}"
        )
    actual_sha = sha256(md_new)
    if expected_sha != actual_sha:
        return 4, (
            f"source_content_sha256 mismatch: manifest={expected_sha} actual={actual_sha}"
        )
    return 0, None


def run_v3_after_manifest(
    man_raw: dict,
    md_new: Path,
    *,
    invoke_v3,
) -> tuple[int, str | None, int]:
    """Production orchestration: identity gate, then V3 only if gate passes.

    invoke_v3: callable returning V3 entry exit code. Injected so tests can
    count real invocations without launching a subprocess.

    Returns (exit_code, fail_reason, v3_call_count).
    """
    code, reason = check_manifest_identity(man_raw, md_new)
    if code != 0:
        return code, reason, 0
    v3_code = int(invoke_v3())
    return v3_code, None, 1


def main() -> int:
    global PDF_SRC, DB_URL
    args = _parse_args()
    if args.pdf is not None:
        PDF_SRC = args.pdf
    if args.db_url is not None:
        DB_URL = args.db_url
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUN_ROOT / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    result: dict = {
        "started": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "stages": {},
    }

    # ---- 0. Input identity ----
    if not PDF_SRC.is_file():
        result["fail"] = f"PDF not found: {PDF_SRC}"
        _write(run_dir, result)
        return 1
    result["pdf_path"] = str(PDF_SRC)
    result["pdf_sha256"] = sha256(PDF_SRC)

    # ---- 1. PDF → Markdown (existing OCR entry) ----
    ocr_out = run_dir / "ocr_md"
    ocr_out.mkdir()
    sys.path.insert(0, str(PAPERS / "ocr_service"))
    os.environ.setdefault("OCR_API_TOKEN", _ocr_token())
    import batch_convert_pdf as ocr  # noqa: E402

    # Local mitm proxy in OCR client is ephemeral; clear when unreachable.
    try:
        ocr.session.proxies = {}
    except Exception:
        pass

    t0 = time.time()
    ok, pages = ocr.process_pdf(
        str(PDF_SRC), str(ocr_out), PDF_SRC.name, page_usage={"used": 0}
    )
    result["stages"]["ocr"] = {
        "ok": bool(ok),
        "pages": pages,
        "seconds": round(time.time() - t0, 2),
        "entry": "ocr_service/batch_convert_pdf.py::process_pdf",
    }
    if not ok:
        result["fail"] = "OCR/PDF→MD failed; abort before Papers"
        _write(run_dir, result)
        return 2
    md_new = next(ocr_out.glob("*.md"), None)
    if md_new is None or md_new.stat().st_size < 100:
        result["fail"] = "OCR produced no usable markdown"
        _write(run_dir, result)
        return 2
    result["stages"]["ocr"]["md_path"] = str(md_new)
    result["stages"]["ocr"]["md_sha256"] = sha256(md_new)

    # ---- 2. Papers reslice on THIS md ----
    papers_out = run_dir / "papers_out"
    papers_out.mkdir()
    env = os.environ.copy()
    env["MIMO_MODEL"] = _v3_settings().mimo_model
    env["MIMO_API_KEY"] = _v3_settings().mimo_api_key or ""
    env["MIMO_BASE_URL"] = _v3_settings().mimo_base_url
    cmd = [
        sys.executable,
        str(PAPERS / "scripts" / "reslice_pipeline.py"),
        "--file",
        str(md_new),
        "--out",
        str(papers_out),
    ]
    t1 = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(PAPERS),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=900,
    )
    result["stages"]["papers"] = {
        "cmd": " ".join(cmd),
        "exit": proc.returncode,
        "seconds": round(time.time() - t1, 2),
        "stdout_tail": (proc.stdout or "")[-1000:],
        "stderr_tail": (proc.stderr or "")[-500:],
    }
    if proc.returncode != 0:
        result["fail"] = "Papers reslice non-zero exit"
        _write(run_dir, result)
        return 3
    mans = list(papers_out.rglob("*.manifest.json"))
    if not mans:
        result["fail"] = "Papers produced no manifest; abort before V3"
        _write(run_dir, result)
        return 3
    man_path = mans[0]
    man_raw = json.loads(man_path.read_text(encoding="utf-8"))
    declared = str(man_raw.get("source_file") or "").replace("\\", "/")
    expected_sha = str(man_raw.get("source_content_sha256") or "").strip()
    gate_code, gate_reason = check_manifest_identity(man_raw, md_new)
    if gate_code != 0:
        result["fail"] = gate_reason
        result["stages"]["papers"]["manifest"] = str(man_path)
        result["v3_call_count"] = 0
        _write(run_dir, result)
        return gate_code
    result["stages"]["papers"]["manifest"] = str(man_path)
    result["stages"]["papers"]["manifest_sha256"] = sha256(man_path)
    actual_sha = sha256(md_new)
    result["stages"]["papers"]["source_content_sha256"] = expected_sha or actual_sha
    result["stages"]["papers"]["md_consumed"] = str(md_new)
    result["stages"]["papers"]["md_sha256"] = actual_sha

    # ---- 3. V3 package = THIS run's PDF + THIS md + THIS manifest ----
    v3_pkg = run_dir / "v3_package"
    v3_pkg.mkdir()
    shutil.copy2(PDF_SRC, v3_pkg / "paper.pdf")
    shutil.copy2(md_new, v3_pkg / "paper.md")
    shutil.copy2(man_path, v3_pkg / "paper.manifest.json")
    # Rewrite manifest source_file to package-relative so formal import resolves
    man2 = json.loads(man_path.read_text(encoding="utf-8"))
    man2["source_file"] = "paper.md"
    (v3_pkg / "paper.manifest.json").write_text(
        json.dumps(man2, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    result["stages"]["v3_package"] = {
        "dir": str(v3_pkg),
        "paper_md_sha256": sha256(v3_pkg / "paper.md"),
        "matches_ocr_md": sha256(v3_pkg / "paper.md") == actual_sha,
    }

    # ---- 4. V3 formal entry + TaskExecutor ----
    entry = Path(r"D:\Project\AITutor-X\e2e_run\x_integrate_entry.py")
    cmd2 = [
        sys.executable,
        str(entry),
        str(v3_pkg),
        "--db-url",
        DB_URL,
        "--out",
        str(run_dir / "v3_result.json"),
    ]
    t2 = time.time()

    def _invoke_v3() -> int:
        proc2 = subprocess.run(
            cmd2,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=str(BACKEND),
            timeout=900,
        )
        result["stages"]["v3"] = {
            "cmd": " ".join(cmd2),
            "exit": proc2.returncode,
            "seconds": round(time.time() - t2, 2),
        }
        vr = run_dir / "v3_result.json"
        if vr.is_file():
            v3 = json.loads(vr.read_text(encoding="utf-8"))
            result["stages"]["v3"]["task_id"] = v3.get("task_id")
            result["stages"]["v3"]["new_questions"] = v3.get("new_questions")
            result["stages"]["v3"]["new_instances"] = v3.get("new_instances")
            result["stages"]["v3"]["db_answers_by_publish"] = v3.get("db_answers_by_publish")
            result["stages"]["v3"]["import_ok"] = v3.get("import_ok")
            result["stages"]["v3"]["new_question_ids"] = v3.get("new_question_ids")
            result["stages"]["v3"]["new_instance_ids"] = v3.get("new_instance_ids")
            result["stages"]["v3"]["source_version_id"] = v3.get("source_version_id")
            result["stages"]["v3"]["task_source_version_id"] = v3.get(
                "task_source_version_id"
            )
        return proc2.returncode

    v3_exit, v3_fail, v3_calls = run_v3_after_manifest(
        man_raw, md_new, invoke_v3=_invoke_v3
    )
    result["v3_call_count"] = v3_calls
    if v3_fail:
        result["fail"] = v3_fail
        _write(run_dir, result)
        return 4
    if v3_exit != 0:
        result["fail"] = "V3 entry non-zero exit"
        _write(run_dir, result)
        return 5

    result["e2e_ok"] = True
    _write(run_dir, result)
    return 0


def _ocr_token() -> str:
    cfg = PAPERS / "data" / ".ocr_config"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            if line.startswith("token"):
                return line.split("=", 1)[1].strip()
    return os.environ.get("OCR_API_TOKEN", "")


def _v3_settings():
    sys.path.insert(0, str(BACKEND))
    os.chdir(str(BACKEND))
    os.environ["APP_ENV"] = "test"
    from app.core.config import settings

    return settings


def _write(run_dir: Path, result: dict) -> None:
    result["finished"] = datetime.now(timezone.utc).isoformat()
    out = run_dir / "e2e_result.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2)[:4000])


if __name__ == "__main__":
    raise SystemExit(main())
