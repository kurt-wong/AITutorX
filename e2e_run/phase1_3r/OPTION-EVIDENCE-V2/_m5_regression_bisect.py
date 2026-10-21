"""READ-ONLY experiment: is test_adversarial_m5_round2 a Task A regression?

Method: save the current resolver.py, byte-exact restore the PRE-Task-A version
from git (ec62d29), run the failing test, then restore the post version.
Restoration is verified by sha256 at each step. No other file is touched.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(r"D:\Project\AITutors-v3")
RES = REPO / "backend/app/domains/resolver/resolver.py"
BACKEND = REPO / "backend"
SWAP = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_tmp_swap")

TEST = "tests/test_adversarial_m5_round2.py::TestRealBypassSimulation::test_no_bypass_through_normal_pipeline"
PRE_SHA_EXPECT = None  # filled at runtime


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_show(rev: str, path: str) -> bytes:
    r = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{path}"],
                       capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"git show failed: {r.stderr[:200]!r}")
    return r.stdout


def run_test() -> str:
    r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q"],
                       cwd=str(BACKEND), capture_output=True, text=True,
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    tail = [l for l in (r.stdout or "").splitlines() if "passed" in l or "failed" in l]
    return tail[-1] if tail else (r.stdout or "")[-200:]


def main() -> None:
    SWAP.mkdir(parents=True, exist_ok=True)
    post_bytes = RES.read_bytes()
    post_sha = sha(RES)
    (SWAP / "resolver_post.bin").write_bytes(post_bytes)
    print(f"post resolver sha : {post_sha}")

    pre_bytes = git_show("ec62d29", "backend/app/domains/resolver/resolver.py")
    (SWAP / "resolver_pre.bin").write_bytes(pre_bytes)
    print(f"pre  resolver sha : {hashlib.sha256(pre_bytes).hexdigest()}")

    # sanity: lengths should be close and both should contain the class
    assert b"class SourceResolver" in pre_bytes and b"class SourceResolver" in post_bytes

    try:
        print("\n[1] running test with POST (Task A) resolver ...")
        RES.write_bytes(post_bytes)
        assert sha(RES) == post_sha
        print("    ->", run_test())

        print("\n[2] running test with PRE (baseline) resolver ...")
        RES.write_bytes(pre_bytes)
        print("    restored sha:", sha(RES))
        print("    ->", run_test())
    finally:
        RES.write_bytes(post_bytes)
        ok = sha(RES) == post_sha
        print(f"\n[restore] resolver.py sha={sha(RES)}  matches post={ok}")
        if not ok:
            print("   !! RESTORE FAILED — manual fix required")


if __name__ == "__main__":
    main()
