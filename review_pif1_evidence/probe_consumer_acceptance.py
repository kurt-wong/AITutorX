"""DSH probe: does the V3 consumer gate actually ACCEPT the producer's new output,
and does it accept the frozen 87-manifest interface face? Read-only."""
import json
import pathlib
import sys
from collections import Counter

V3 = pathlib.Path(r"D:\Project\AITutors-v3")
sys.path.insert(0, str(V3 / "backend"))
sys.path.insert(0, str(V3 / "backend" / "scripts" / "preprocessing_consumer"))

import manifest_reader  # noqa: E402
import boundary  # noqa: E402

FRESH = pathlib.Path(r"D:\Project\AITutor-X\review_pif1_evidence\tmp\p3a\s.manifest.json")

print("=== A. fresh producer manifest through the real consumer chain ===")
m = manifest_reader.load_manifest(FRESH)
print("reader.source_content_sha256:", m.source_content_sha256)
print("reader.identity_version    :", repr(m.identity_version))
d = boundary.enforce_interface_scope(m.source_content_sha256, m.identity_version)
print("gate.accepted:", d.accepted, "| code:", d.code, "|", d.reason)
print("gate.identity sha:", getattr(d.identity, "source_content_sha256", None))

print("\n=== B. negative controls (proves the gate is real, not a rubber stamp) ===")
SHA = "a" * 64
for label, sha, iv in [
    ("baseline_v2_int", SHA, 2),
    ("baseline_v2_str", SHA, "2"),
    ("pre-round_shape (no sha, v2)", None, 2),
    ("pre-round_shape (no sha, no iv)", None, None),
    ("v1 legacy", SHA, 1),
    ("malformed sha", "NOT-A-SHA", 2),
    ("missing version only", SHA, None),
]:
    dd = boundary.enforce_interface_scope(sha, iv)
    print(f"  {label:32s} accepted={dd.accepted!s:5s} code={dd.code}")

print("\n=== C. real frozen corpus census (Papers) ===")
root = pathlib.Path(r"D:\Project\Papers")
mans = [p for p in root.rglob("*.manifest.json")
        if "_archive" not in p.parts and ".pytest" not in str(p)]
print("manifests found:", len(mans))
iv_types = Counter()
sha_state = Counter()
gate = Counter()
gate_by_ivtype = Counter()
rejected_examples = []
for p in mans:
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        sha_state[f"unreadable_json:{type(e).__name__}"] += 1
        continue
    iv = raw.get("identity_version")
    iv_types[repr(iv)] += 1
    sha = raw.get("source_content_sha256")
    if sha is None:
        sha_state["absent"] += 1
    elif not isinstance(sha, str):
        sha_state["non_str"] += 1
    elif len(sha) != 64:
        sha_state[f"len{len(sha)}"] += 1
    else:
        sha_state["64hex" if all(c in "0123456789abcdef" for c in sha) else "bad_hex"] += 1
    # only score manifests that claim interface membership
    if iv in (2, "2"):
        dd = boundary.enforce_interface_scope(sha, iv)
        gate["accepted" if dd.accepted else f"rejected:{dd.code}"] += 1
        gate_by_ivtype[f"{type(iv).__name__}={iv!r}"] += 1
        if not dd.accepted and len(rejected_examples) < 6:
            rejected_examples.append((str(p.relative_to(root)), repr(iv), repr(sha)[:40], dd.code))
print("identity_version distribution:", dict(iv_types))
print("sha field state            :", dict(sha_state))
print("gate result over iv in (2,'2'):", dict(gate))
print("  note: interface-face count (iv==2) =", sum(
    v for k, v in iv_types.items() if k in ("2", "'2'")))
for e in rejected_examples:
    print("  rejected:", e)
