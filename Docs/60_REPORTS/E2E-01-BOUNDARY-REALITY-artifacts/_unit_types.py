import json
from pathlib import Path
from collections import Counter

# unit types across VERIFIED manifests (sample)
base = Path(r"D:\Project\Papers\Ocr-markdown")
types = Counter()
composite_papers = []
material_papers = []
verified_names = set()
raw = json.loads(Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts\10-raw-b2-Ocr-markdown.json").read_text(encoding="utf-8"))
for item in raw["papers"]:
    ig = (item.get("result") or {}).get("identity_gate") or {}
    if ig.get("identity_state") == "VERIFIED":
        verified_names.add(item.get("paper"))

for p in base.rglob("*.manifest.json"):
    name = p.stem.replace(".manifest","") if p.name.endswith(".manifest.json") else p.name
    # paper name in report is without .manifest.json
    paper = p.name.replace(".manifest.json","")
    if paper not in verified_names and name not in verified_names:
        # try match loosely
        pass
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    for u in m.get("units") or []:
        t = u.get("unit_type") or "?"
        types[t]+=1
        if "composite" in t and paper in verified_names:
            composite_papers.append(paper)
        if t == "material" or (u.get("extra_lines") and paper in verified_names):
            material_papers.append(paper)

print("unit types (all Ocr-markdown):", dict(types))
print("verified count names", len(verified_names))
print("composite in verified sample", list(set(composite_papers))[:5])
print("material-ish in verified sample", list(set(material_papers))[:5])
# find a verified paper with composite
for name in sorted(verified_names):
    # find file
    hits = list(base.rglob(name + ".manifest.json"))
    if not hits:
        hits = [p for p in base.rglob("*.manifest.json") if name in p.name]
    if hits:
        m = json.loads(hits[0].read_text(encoding="utf-8"))
        ts = [u.get("unit_type") for u in m.get("units") or []]
        if any(t and "composite" in t for t in ts):
            print("COMPOSITE_VERIFIED", name, Counter(ts))
            break
        if any(t=="material" or (u.get("extra_lines")) for u,t in zip(m.get("units") or [], ts)):
            print("MATERIALISH_VERIFIED", name, Counter(ts))
            break
