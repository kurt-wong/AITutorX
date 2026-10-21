from pathlib import Path
import json, re

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
viewer = json.loads((OUT / "viewer_data.json").read_text(encoding="utf-8"))

# include digit-glued labels in splitter
LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")

def split_line_options(text: str):
    if not text:
        return {}
    hits = list(LAB.finditer(text))
    out = {}
    for i, m in enumerate(hits):
        lab = m.group(1).upper()
        start = m.end()
        end = hits[i+1].start() if i+1 < len(hits) else len(text)
        content = text[start:end].strip()
        if lab not in out:
            out[lab] = content
    return out

for subj, entry in viewer["subjects"].items():
    for q in entry.get("questions") or []:
        opts = q.get("options") or []
        # if any option text looks like it contains multiple labels, resplit
        for o in opts:
            parts = split_line_options(o.get("text") or "")
            if len(parts) >= 2:
                for lab, content in parts.items():
                    for x in opts:
                        if x.get("label") == lab:
                            x["text"] = content
                break
        # if D is still bare 'D' and C holds `2D.` form, fix
        by = {o.get("label"): o for o in opts}
        if by.get("C") and "2D." in (by["C"].get("text") or ""):
            t = by["C"]["text"]
            parts = split_line_options(t)
            if parts.get("C") is not None:
                by["C"]["text"] = parts["C"]
            if parts.get("D") is not None:
                by["D"]["text"] = parts["D"]

(OUT / "viewer_data.json").write_text(json.dumps(viewer, ensure_ascii=False), encoding="utf-8")

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

for q in data["subjects"]["数学"]["questions"]:
    if q["unit_id"] == "Q4":
        print("Math Q4:")
        for o in q["options"]:
            print(" ", o["label"], repr((o.get("text") or "")[:70]))
