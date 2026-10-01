import json
from pathlib import Path
from collections import Counter

x27_path = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\X2.7-INT-FULL-01-artifacts\31-per-input-results.json")
e2e_dir = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts")
out = e2e_dir / "32-x27-vs-e2e01-compare.json"

x27 = json.loads(x27_path.read_text(encoding="utf-8"))
inputs = x27["legs"]["B2_primary"]["inputs"]
print("sample x27 input:", json.dumps(inputs[0], ensure_ascii=False)[:500])

def classify_text(text: str) -> str:
    t = text.lower()
    if "manifest_sha_missing" in t or "missing_identity" in t or "sha_missing" in t:
        return "B"
    if "semantic_pending" in t or "ir_absent" in t:
        return "A+E"
    return "OTHER"

x27_rows = []
for rec in inputs:
    name = rec.get("paper") or rec.get("manifest") or rec.get("name") or rec.get("id") or "?"
    cls = classify_text(json.dumps(rec, ensure_ascii=False))
    x27_rows.append((str(name), cls))

def classify_e2e(item):
    r = item.get("result") or {}
    ig = r.get("identity_gate") or {}
    isc = ig.get("interface_scope") or {}
    if ig.get("identity_state") == "VERIFIED":
        return "A+E"
    mm = ig.get("mismatches") or []
    if isc.get("code") == "MISSING_IDENTITY" or "manifest_sha_missing" in mm:
        return "B"
    return "OTHER"

e2e_rows = []
for fn in ["10-raw-b2-data.json", "10-raw-b2-tests.json", "10-raw-b2-Ocr-markdown.json"]:
    raw = json.loads((e2e_dir / fn).read_text(encoding="utf-8"))
    for item in raw.get("papers") or []:
        e2e_rows.append((str(item.get("paper")), classify_e2e(item)))

x27_c = Counter(x27_rows)
e2e_c = Counter(e2e_rows)
only_x = x27_c - e2e_c
only_e = e2e_c - x27_c

result = {
    "document_id": "E2E-01-X27-COMPARE",
    "note": "Multiset compare of (paper, class). Supports H-3 fact sentence only; no causal claim.",
    "x27_source": str(x27_path),
    "x27_leg": "legs.B2_primary.inputs",
    "class_mapping": {
        "B": "MISSING_IDENTITY / manifest_sha_missing",
        "A+E": "identity VERIFIED or semantic_pending/ir_absent",
    },
    "x27_rows": len(x27_rows),
    "e2e01_rows": len(e2e_rows),
    "x27_class_counts": dict(Counter(c for _, c in x27_rows)),
    "e2e01_class_counts": dict(Counter(c for _, c in e2e_rows)),
    "multiset_equal": (not only_x and not only_e),
    "only_in_x27": [{"paper": k[0], "class": k[1], "n": v} for k, v in only_x.most_common(20)],
    "only_in_e2e01": [{"paper": k[0], "class": k[1], "n": v} for k, v in only_e.most_common(20)],
    "only_x_count": sum(only_x.values()),
    "only_e_count": sum(only_e.values()),
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k: result[k] for k in ["x27_rows","e2e01_rows","x27_class_counts","e2e01_class_counts","multiset_equal","only_x_count","only_e_count"]}, ensure_ascii=False, indent=2))
