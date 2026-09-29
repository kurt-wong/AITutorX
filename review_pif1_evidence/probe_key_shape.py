"""Report only the SHAPE of the configured key and whether _redact() fully strips it.
The key value is never printed or written anywhere."""
import pathlib
import sys

PAPERS = pathlib.Path(r"D:\Project\Papers")
sys.path.insert(0, str(PAPERS / "scripts"))
import reslice_pipeline as rp  # noqa: E402

legacy = PAPERS / "data" / ".llm_config"
print("legacy config exists:", legacy.exists())
if legacy.exists():
    kv = {}
    for line in legacy.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    print("legacy keys present:", sorted(kv.keys()))
    key = kv.get("api_key", "")
    if key:
        shape = {
            "len": len(key),
            "prefix_first3": key[:3],
            "n_dash": key.count("-"),
            "n_underscore": key.count("_"),
            "n_dot": key.count("."),
            "all_alnum_after_prefix": all(c.isalnum() for c in key[3:]) if key.startswith("sk-") else None,
        }
        print("key shape:", shape)
        red = rp._redact(f"LLM failed with Authorization: Bearer {key}")
        print("fully_redacted_via_bearer:", key not in red)
        red2 = rp._redact(f"boom: api_key='{key}'")
        print("fully_redacted_via_json:", key not in red2)
        red3 = rp._redact(f"raw dump {key} end")
        print("fully_redacted_bare:", key not in red3)
        # residual fragment check (no full key printed)
        if key in red3:
            idx = red3.find(key[:6])
            print("residual_context:", red3[max(0, idx - 4):idx + 6] + "...<len=%d>" % len(red3))
    else:
        print("no api_key in legacy config (env-var only)")
env_key = "MIMO_API_KEY"
import os  # noqa: E402
print(f"env {env_key} set in this shell:", bool(os.environ.get(env_key)))
