# -*- coding: utf-8 -*-
"""RL evidence probe — H-01 regression test hermeticity under the report's own
recommended credential mechanism (MIMO_API_KEY via environment).

Question under test:
    tests/test_no_config_import.py::test_call_llm_fails_loudly_without_config
    asserts that call_llm() fails loudly "without config".  Its helper
    _run() builds the child env as dict(os.environ, RESLICE_ROOT=..., PYTHONPATH=...)
    i.e. it never scrubs MIMO_API_KEY / MIMO_BASE_URL / MIMO_MODEL / LLM_PROVIDER.

    Report-L B-2 recommends exactly "MIMO_API_KEY 环境变量注入" as the long-term
    credential mechanism.  So on any host that follows that recommendation the
    "without config" precondition is silently false.

This probe reproduces the test's subprocess invocation verbatim, twice:
    case A: ambient env scrubbed        -> expect ProviderConfigError, '.llm_config' in msg
    case B: ambient MIMO_* present      -> config resolution SUCCEEDS and call_llm
                                           proceeds to the transport layer

Base URL is pointed at 127.0.0.1:9 (discard port) so case B performs NO external
call; it only proves that the no-config precondition was bypassed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\Project\Aitutors-preprocessing")
SCRIPTS = ROOT / "scripts"
SANDBOX = Path(r"D:\Project\AITutor-X\review_l_evidence\_sandbox")
SANDBOX.mkdir(parents=True, exist_ok=True)

CODE = (
    "import reslice_pipeline as rp\n"
    "try:\n"
    "    rp.call_llm('hi', retries=0)\n"
    "    print('SWALLOWED')\n"
    "except Exception as e:\n"
    "    print('EXC_TYPE', type(e).__name__)\n"
    "    print('EXPECTED', '.llm_config' in str(e))\n"
    "    print('MSG_HEAD', str(e)[:160])\n"
)

VARS = ("MIMO_API_KEY", "MIMO_BASE_URL", "MIMO_MODEL", "LLM_PROVIDER", "DEEPSEEK_API_KEY")


def run(case, extra):
    env = dict(os.environ)
    for v in VARS:                       # case A scrubs; case B re-adds below
        env.pop(v, None)
    env.update({"RESLICE_ROOT": str(SANDBOX), "PYTHONPATH": str(SCRIPTS)})
    env.update(extra)
    r = subprocess.run([sys.executable, "-c", CODE], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env,
                       cwd=str(SANDBOX), timeout=180)
    return {"case": case, "returncode": r.returncode,
            "stdout": r.stdout.strip().splitlines(),
            "stderr_tail": r.stderr.strip()[-300:]}


out = [
    run("A_ambient_env_scrubbed", {}),
    run("B_ambient_MIMO_present_as_report_recommends", {
        "MIMO_API_KEY": "synthetic-fake-key-for-hermeticity-probe",
        "MIMO_BASE_URL": "http://127.0.0.1:9/v1",
        "MIMO_MODEL": "mimo-v2.6-pro",
    }),
]
print(json.dumps(out, ensure_ascii=False, indent=2))
Path(r"D:\Project\AITutor-X\review_l_evidence\rl-hermeticity-probe.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
