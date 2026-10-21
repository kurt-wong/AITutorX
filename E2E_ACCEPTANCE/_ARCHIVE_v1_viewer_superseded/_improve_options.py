from pathlib import Path
import json, re

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
viewer = json.loads((OUT / "viewer_data.json").read_text(encoding="utf-8"))

# Also need source lines — rebuild questions' option text by splitting shared lines
# We'll re-read MD files and improve option text in-place using label-splitting.

LAB = re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]")

def split_line_options(text: str):
    """Return {LABEL: content} from a line like `A. x B. y C. z D. w`."""
    if not text:
        return {}
    hits = list(LAB.finditer(text))
    out = {}
    for i, m in enumerate(hits):
        lab = m.group(1).upper()
        start = m.end()
        end = hits[i+1].start() if i+1 < len(hits) else len(text)
        content = text[start:end].strip()
        if lab not in out:  # first occurrence
            out[lab] = content
    return out

def improve_options(q, md_lines):
    """If option texts look like label-only or whole-line dump, resplit from source."""
    opts = q.get("options") or []
    if not opts:
        return
    # gather line texts referenced by span via unit stem/options — fallback: search MD
    texts = [o.get("text") or "" for o in opts]
    # case 1: one option holds the whole line with multiple labels
    for o in opts:
        t = o.get("text") or ""
        parts = split_line_options(t)
        if len(parts) >= 2:
            for lab, content in parts.items():
                for x in opts:
                    if x.get("label") == lab:
                        x["text"] = content
            break
    # case 2: some options are bare labels ("A","B","C","D") — try to find content from siblings
    bare = [o for o in opts if (o.get("text") or "").strip() in {o.get("label"), ""} or len((o.get("text") or "").strip()) <= 2]
    if bare and md_lines:
        # search first option's text in md to locate the option block
        first = next((o for o in opts if len((o.get("text") or "")) > 5), None)
        if first:
            key = first["text"][:20]
            for i, line in enumerate(md_lines):
                if key and key in line:
                    parts = split_line_options(line)
                    # also next few lines
                    window = " ".join(md_lines[i:i+4])
                    parts.update({k: v for k, v in split_line_options(window).items() if k not in parts})
                    for o in opts:
                        lab = o.get("label")
                        if lab in parts and len((o.get("text") or "").strip()) <= 2:
                            o["text"] = parts[lab]
                    break

# load md texts
md_cache = {}
for subj, entry in viewer["subjects"].items():
    md_path = entry.get("md_text_path")
    if md_path and (OUT / md_path).is_file():
        md_cache[subj] = (OUT / md_path).read_text(encoding="utf-8").splitlines()
    else:
        md_cache[subj] = []

for subj, entry in viewer["subjects"].items():
    lines = md_cache[subj]
    for q in entry.get("questions") or []:
        improve_options(q, lines)

(OUT / "viewer_data.json").write_text(json.dumps(viewer, ensure_ascii=False), encoding="utf-8")

# rebuild data.js slim
def slim(v):
    out = dict(v)
    if out.get("pdf_text_preview"):
        out["pdf_text_preview"] = out["pdf_text_preview"][:3000]
    if out.get("md_text_preview"):
        out["md_text_preview"] = out["md_text_preview"][:3000]
    return out

data = {
    "run_id": viewer.get("run_id"),
    "purpose": viewer.get("purpose"),
    "frozen": viewer.get("frozen"),
    "note": viewer.get("note"),
    "git": viewer.get("git"),
    "subjects": {k: slim(v) for k, v in viewer.get("subjects", {}).items()},
}
(OUT / "data.js").write_text("window.E2E_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
print("data.js", (OUT/"data.js").stat().st_size)

# verify
for subj in ["数学", "化学"]:
    qs = data["subjects"][subj]["questions"]
    print("===", subj)
    for q in qs[:2]:
        print(" ", q.get("unit_id"), "gate", q.get("gate"))
        for o in (q.get("options") or [])[:4]:
            print("   ", o.get("label"), repr((o.get("text") or "")[:50]))
