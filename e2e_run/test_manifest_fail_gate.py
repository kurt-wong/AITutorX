"""Manifest failure-gate: REAL script-level negative tests (DSH correction).

These tests import and call the production orchestration functions from
AITutor-X/e2e_run/x_pdf_papers_v3.py — they do NOT reimplement the hash
if-conditions locally. Each case asserts:
  - non-zero exit code
  - V3 invocation count == 0
  - identifiable failure reason (no silent fallback)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT = Path(r"D:\Project\AITutor-X\e2e_run\x_pdf_papers_v3.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("x_pdf_papers_v3", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def xpv():
    return _load_module()


class _V3Counter:
    """Injectable V3 invoker that records every real call attempt."""

    def __init__(self):
        self.calls = 0
        self.last_arg = None

    def __call__(self, *args, **kwargs):
        self.calls += 1
        self.last_arg = args
        return 0


def _md_file(tmp_path: Path, content: str = "1. Q\nA. a\n") -> Path:
    md = tmp_path / "paper.md"
    md.write_text(content, encoding="utf-8")
    return md


def test_manifest_missing_hash_blocks_v3(xpv, tmp_path):
    md = _md_file(tmp_path)
    man = {"source_file": "paper.md", "units": []}
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code != 0, "missing hash must be non-zero exit"
    assert v3_calls == 0, "V3 must not be invoked when hash is missing"
    assert counter.calls == 0, "V3 invoker must not be called"
    assert reason and "source_content_sha256" in reason, reason


def test_manifest_invalid_hash_blocks_v3(xpv, tmp_path):
    md = _md_file(tmp_path)
    # 63 hex chars + one 'g' — not a valid 64-hex SHA-256
    bad = "abc123" * 10 + "zz"
    assert len(bad) != 64 or any(c not in "0123456789abcdef" for c in bad.lower())
    man = {"source_file": "paper.md", "source_content_sha256": bad, "units": []}
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code != 0, "invalid hash must be non-zero exit"
    assert v3_calls == 0
    assert counter.calls == 0
    assert reason and "source_content_sha256" in reason, reason


def test_manifest_wrong_length_hash_blocks_v3(xpv, tmp_path):
    md = _md_file(tmp_path)
    man = {"source_file": "paper.md", "source_content_sha256": "ab" * 16, "units": []}
    # "ab"*16 is 32 chars, not 64
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code != 0
    assert v3_calls == 0
    assert counter.calls == 0
    assert reason and "source_content_sha256" in reason, reason


def test_manifest_hash_mismatch_blocks_v3(xpv, tmp_path):
    content = "1. Q\nA. a\n"
    md = _md_file(tmp_path, content)
    actual = hashlib.sha256(md.read_bytes()).hexdigest()
    wrong = ("0" if actual[0] != "0" else "1") + actual[1:]
    assert wrong != actual
    man = {
        "source_file": "paper.md",
        "source_content_sha256": wrong,
        "units": [],
    }
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code != 0, "hash mismatch must be non-zero exit"
    assert v3_calls == 0
    assert counter.calls == 0
    assert reason and "mismatch" in reason.lower(), reason


def test_manifest_wrong_source_file_blocks_v3(xpv, tmp_path):
    md = _md_file(tmp_path)
    actual = hashlib.sha256(md.read_bytes()).hexdigest()
    man = {
        "source_file": "OTHER.md",
        "source_content_sha256": actual,
        "units": [],
    }
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code != 0
    assert v3_calls == 0
    assert counter.calls == 0
    assert reason and "source_file" in reason, reason


def test_valid_manifest_reaches_v3(xpv, tmp_path):
    """Positive control: gate must let a correct package through to V3."""
    content = "1. Q\nA. a\n"
    md = _md_file(tmp_path, content)
    actual = hashlib.sha256(md.read_bytes()).hexdigest()
    man = {
        "source_file": "paper.md",
        "source_content_sha256": actual,
        "units": [],
    }
    counter = _V3Counter()
    code, reason, v3_calls = xpv.run_v3_after_manifest(man, md, invoke_v3=counter)

    assert code == 0
    assert reason is None
    assert v3_calls == 1
    assert counter.calls == 1


def test_main_uses_same_gate_not_local_reimplementation(xpv):
    """Guard: main() must call check_manifest_identity, not a private copy."""
    import inspect

    src = inspect.getsource(xpv.main)
    assert "check_manifest_identity" in src or "run_v3_after_manifest" in src
    # The old inline hex-check must no longer be the only gate in main.
    assert "run_v3_after_manifest" in src
