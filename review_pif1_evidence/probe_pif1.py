"""DSH independent probe for PRIMARY-PATH-IDENTITY-ENABLEMENT-01.

Read-only w.r.t. Papers: imports the producer module and exercises it with
synthetic inputs inside this workspace. No network, no config required.
"""
import hashlib
import json
import pathlib
import sys
import time
import urllib.error

PAPERS = pathlib.Path(r"D:\Project\Papers")
sys.path.insert(0, str(PAPERS / "scripts"))
sys.path.insert(0, str(PAPERS))

import reslice_pipeline as rp  # noqa: E402

WORK = pathlib.Path(__file__).resolve().parent / "tmp"
WORK.mkdir(parents=True, exist_ok=True)
out = []


def rec(k, v):
    out.append(f"{k}: {v}")
    print(f"{k}: {v}")


# ---------------------------------------------------------------- P1: 4xx fail-fast
calls = {"n": 0}


def fake_urlopen(req, timeout=None):
    calls["n"] += 1
    raise urllib.error.HTTPError(
        req.full_url, 401, "Unauthorized token=sk-abcdefgh12345678 sent",
        {}, None)


rp.load_cfg = lambda: {"model": "m", "base_url": "http://127.0.0.1:9",
                       "api_key": "sk-SECRET-abcdefghijklmnop"}
rp.urllib.request.urlopen = fake_urlopen

t0 = time.time()
try:
    rp.call_llm("hi", retries=4)
    rec("P1_4xx", "FAIL - no exception raised")
except RuntimeError as e:
    msg = str(e)
    rec("P1_4xx_raised", msg)
    rec("P1_4xx_redacted", "sk-abcdefgh12345678" not in msg)
except Exception as e:  # noqa: BLE001
    rec("P1_4xx", f"FAIL - wrong type {type(e).__name__}: {e}")
rec("P1_attempts", f"{calls['n']} (expect 1 = no retry)")
rec("P1_elapsed_s", f"{time.time() - t0:.2f} (expect <1.0 = no backoff sleep)")

# ---------------------------------------------------------------- P2: _redact coverage
key = "sk-abcdefgh12345678"
cases = {
    "bearer_sk": f"Authorization: Bearer {key}",
    "bearer_bare": "Authorization: Bearer abcdefghijklmnopqrst",
    "sk_with_dashes": "key sk-12345678-abcdefgh-9999 end",
    "env_style": f"api_key={key}",
    "json_style": f"{{'api_key': '{key}'}}",
    "jwt": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.abcdefghijklmnop",
}
for name, s in cases.items():
    red = rp._redact(s)
    leaked = [tok for tok in (key, "abcdefghijklmnopqrst", "abcdefghijklmnop",
                              "12345678-abcdefgh-9999", "eyJhbGciOiJIUzI1NiJ9")
              if tok in red]
    rec(f"P2_{name}", f"clean={not leaked} leaked={leaked} -> {red}")

# real key from live config (value never printed)
try:
    real = rp.load_cfg.__wrapped__ if hasattr(rp.load_cfg, "__wrapped__") else None
    import llm_provider  # noqa: E402
    cfg = llm_provider.resolve(PAPERS)
    rk = cfg["api_key"]
    red = rp._redact(rk)
    rec("P2_real_key_fully_redacted", f"{rk not in red} (key len={len(rk)}, prefix={rk[:3]!r})")
except Exception as e:  # noqa: BLE001
    rec("P2_real_key_fully_redacted", f"not resolvable offline: {type(e).__name__}")

# ---------------------------------------------------------------- P3: write_outputs identity
LINES = ["1. 题干（ ）", "", "1.【答案】A"]
MAN_UNITS = [{"unit_id": "Q1", "unit_type": "standalone_question",
              "question_numbers": [1], "original_question_type": "single_choice",
              "stem_lines": [1, 1], "options_lines": None,
              "answer_lines": [3, 3], "explanation_lines": None}]

src = WORK / "probe_src.md"
src.write_text("\n".join(LINES), encoding="utf-8")
correct = hashlib.sha256(src.read_bytes()).hexdigest()

# P3a: no sha in man -> computed value must land
d1 = WORK / "p3a"
man_a = {"identity_version": 2, "units": json.loads(json.dumps(MAN_UNITS))}
rp.write_outputs(d1, "s", list(LINES), man_a, [], {"warnings": []}, src.name, src)
m1 = json.loads((d1 / "s.manifest.json").read_text(encoding="utf-8"))
rec("P3a_fresh_computed", m1.get("source_content_sha256") == correct)
rec("P3a_identity_version", m1.get("identity_version"))

# P3b: STALE/WRONG sha already in man -> does it override the computed value?
d2 = WORK / "p3b"
man_b = {"identity_version": 2, "units": json.loads(json.dumps(MAN_UNITS)),
         "source_content_sha256": "f" * 64}
rp.write_outputs(d2, "s", list(LINES), man_b, [], {"warnings": []}, src.name, src)
m2 = json.loads((d2 / "s.manifest.json").read_text(encoding="utf-8"))
rec("P3b_carried_sha", m2.get("source_content_sha256"))
rec("P3b_wrong_sha_overrides_correct",
    m2.get("source_content_sha256") == "f" * 64)
rec("P3b_binds_wrong_source", m2.get("source_content_sha256") != correct)

# P3c: src_path missing -> field silently absent?
d3 = WORK / "p3c"
man_c = {"identity_version": 2, "units": json.loads(json.dumps(MAN_UNITS))}
rp.write_outputs(d3, "s", list(LINES), man_c, [], {"warnings": []}, "ghost.md",
                 WORK / "ghost.md")
m3 = json.loads((d3 / "s.manifest.json").read_text(encoding="utf-8"))
rec("P3c_field_when_src_absent", repr(m3.get("source_content_sha256", "<ABSENT>")))
rec("P3c_still_written", (d3 / "s.manifest.json").exists())

# P3d: is the published companion md byte-identical to the anchored source?
d4 = WORK / "p4"
rp.write_outputs(d4, "s", list(LINES), {"identity_version": 2,
                                        "units": json.loads(json.dumps(MAN_UNITS))},
                 [], {"warnings": []}, src.name, src)
pub = d4 / "s.md"
pub_sha = hashlib.sha256(pub.read_bytes()).hexdigest() if pub.exists() else None
rec("P3d_published_md_bytes", f"n={pub.stat().st_size if pub.exists() else None}")
rec("P3d_published_equals_anchor", pub_sha == correct)
rec("P3d_source_file_value", json.loads(
    (d4 / "s.manifest.json").read_text(encoding="utf-8"))["source_file"])

(WORK / "probe_result.txt").write_text("\n".join(out), encoding="utf-8")
print("\n[probe complete]")
