import json, shutil
from pathlib import Path

src_manifest = None
base = Path(r"D:\Project\Papers\Ocr-markdown")
for p in base.rglob("*化学*manifest.json"):
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if m.get("source_content_sha256") and m.get("identity_version")==2:
        src_manifest = p
        break
print("src_manifest", src_manifest)

# also find a different md as wrong source
wrong_md = None
for p in base.rglob("*.md"):
    if src_manifest and p.parent == src_manifest.parent and p.stem != src_manifest.name.replace(".manifest.json",""):
        wrong_md = p
        break
if not wrong_md:
    for p in base.rglob("*.md"):
        wrong_md = p
        break
print("wrong_md", wrong_md)

out = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts\30-mismatch-combo")
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
# copy wrong source bytes under the expected source basename
m = json.loads(src_manifest.read_text(encoding="utf-8"))
source_name = Path(m["source_file"]).name
shutil.copy2(wrong_md, out / source_name)
# copy manifest but rewrite source_file to local
m2 = dict(m)
m2["source_file"] = str(out / source_name)
# keep declared sha as ORIGINAL (so mismatch)
(out / src_manifest.name).write_text(json.dumps(m2, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote combo to", out)
print("expected_declared_sha", m.get("source_content_sha256"))
print("source_name", source_name)
