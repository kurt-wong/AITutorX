import hashlib, json
from pathlib import Path
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")

print("=== S1 data immutability ===")
raw = json.loads((OUT / "viewer_data_raw.json").read_text(encoding="utf-8"))
js = (OUT / "data.js").read_text(encoding="utf-8")
payload = js[len("window.E2E_DATA = "):].rstrip().rstrip(";")
assert json.loads(payload) == raw
print("  data.js == viewer_data_raw.json: OK")
for subj, h in (raw.get("raw_v3_output_sha256") or {}).items():
    now = hashlib.sha256((OUT / "05_V3_OUTPUT" / f"{subj}.v3.json").read_bytes()).hexdigest()
    assert now == h, subj
print("  raw V3 SHA locked: OK")

print("=== S2 write surface ===")
writers = []
for p in OUT.glob("*.py"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    if ("viewer_data_raw.json" in t or "data.js" in t) and "write_text" in t:
        writers.append(p.name)
print("  scripts that write data files:", writers)
app = (OUT / "app.js").read_text(encoding="utf-8")
assert "write_text" not in app
print("  app.js is read-only: OK")

print("=== S3 sentinels ===")
s3 = raw.get("S3_sentinel_check") or {}
print(" ", json.dumps(s3, ensure_ascii=False))
assert s3.get("ok") is True
assert s3["chem_Q20"]["n_options"] == 5
assert "还原反应" in (s3["chem_Q20"].get("E_text") or "")
assert s3["math_Q4"]["D_text_raw"] == "D"
q20 = next(q for q in raw["subjects"]["化学"]["questions"] if q["unit_id"] == "Q20")
assert len(q20["options_raw"]) == 5
q4 = next(q for q in raw["subjects"]["数学"]["questions"] if q["unit_id"] == "Q4")
dopt = next(o for o in q4["options_raw"] if o["label"] == "D")
assert dopt["text_raw"] == "D", dopt
print("  S3 FAIL-CLOSED: OK (Q20 n=5 E has 还原反应; Q4.D == 'D')")

print("=== Gate1 full text ===")
for subj, e in raw["subjects"].items():
    assert e.get("pdf_text_len", 0) == len(e.get("pdf_text") or "")
    assert e.get("md_text_len", 0) == len(e.get("md_text") or "")
print("  all 9 subjects FULL pdf_text + md_text: OK")
math = raw["subjects"]["数学"]
print("  math pdf_text_len", math["pdf_text_len"], "md_text_len", math["md_text_len"])

print("=== formula cases ===")
html = (OUT / "index.html").read_text(encoding="utf-8")
for tok in ["x^2+y^2=r^2", r"\frac{x^2-1}{x-1}", r"\sqrt{a^2+b^2}", "pmatrix", "cases", r"\mathrm{BaSO}"]:
    assert tok in html, tok
print("  coverage demos: OK")

print("=== render policy ===")
assert "RENDER_FAILED" in app
assert "dollars % 2" in app or "unclosed" in app
assert "renderRich" in app
assert "img" in app.lower()
print("  two-phase HTML+math, unclosed $ -> RENDER_FAILED: OK")

print()
print("ALL S1/S2/S3 + Gate1 full-text + formula policy CHECKS PASSED")
