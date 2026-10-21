"""Freeze RAW baseline + annotate option integrity (READ-ONLY on production)."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
raw_path = OUT / "viewer_data_raw.json"
data_js_path = OUT / "data.js"

raw = json.loads(raw_path.read_text(encoding="utf-8"))

# ---- option integrity detector (read-only labels; never rewrites text_raw) ----
def option_integrity(options_raw):
    """Return per-option integrity flags. Does NOT modify text_raw."""
    flags = []
    for o in options_raw or []:
        t = (o.get("text_raw") or "").strip()
        lab = o.get("label") or ""
        # shell: text is only the label letter, or label + separator, or empty
        shell = (not t) or (t == lab) or (t in {f"{lab}.", f"{lab}．", f"{lab}、", f"{lab})"})
        # whole-line dump: text contains 2+ other labels
        import re
        n_labs = len(re.findall(r"(?<![A-Za-z0-9_])[A-H]\s*[.．、:：,，)）]", t))
        multi = n_labs >= 2
        flags.append({
            "label": lab,
            "is_shell": shell,
            "is_multilabel_line": multi,
            "text_len": len(t),
            "text_preview": t[:60],
        })
    n_shell = sum(1 for f in flags if f["is_shell"])
    n_multi = sum(1 for f in flags if f["is_multilabel_line"])
    if n_shell >= 1 or n_multi >= 1:
        level = "ANOMALY"
    else:
        level = "OK"
    return {
        "level": level,
        "n_options": len(flags),
        "n_shell": n_shell,
        "n_multilabel_line": n_multi,
        "options": flags,
        "owner_note": (
            "选项结构异常时：不要求判断选项内容正确性；仍可检查题干/答案/LaTeX。"
            if level == "ANOMALY" else "选项结构完整，可正常验收。"
        ),
    }

# ---- Gate1 full-text indexes (no 800-char slice in data; viewer renders full) ----
for subj, e in raw["subjects"].items():
    qs = e.get("questions") or []
    for q in qs:
        q["option_integrity"] = option_integrity(q.get("options_raw"))
    # mark dimensions available for owner feedback
    e["owner_feedback"] = {
        "stem": {"status": "", "note": ""},
        "options": {"status": "", "note": "受选项结构影响时只标异常，不判内容对错"},
        "answer": {"status": "", "note": ""},
        "latex_render": {"status": "", "note": "渲染失败已在页面标注"},
        "overall": {"status": "", "note": "选项结构损坏时暂缓整体结论"},
    }
    n_anom = sum(1 for q in qs if (q.get("option_integrity") or {}).get("level") == "ANOMALY")
    e["option_anomaly_count"] = n_anom
    print(subj, "questions", len(qs), "option_anomaly", n_anom)

# freeze block
locks = {}
for label, p in [
    ("viewer_data_raw.json", raw_path),
    ("data.js", data_js_path),
]:
    if p.exists():
        locks[label] = hashlib.sha256(p.read_bytes()).hexdigest()
for subj in raw["subjects"]:
    p = OUT / "05_V3_OUTPUT" / f"{subj}.v3.json"
    if p.exists():
        locks[f"05_V3_OUTPUT/{subj}.v3.json"] = hashlib.sha256(p.read_bytes()).hexdigest()

raw["FROZEN_BASELINE"] = {
    "note": "RAW evidence freeze — no option split/complete/fix after this point",
    "sha256": locks,
    "resolver_fix": "SEPARATE TASK — not in this Viewer round",
    "e2e_verdict": "NOT YET PASSED — Gate2 blocked on 97-ish option-structure defects; formal TaskExecutor path unproven",
}

# write annotations into raw + data.js (this is export layer, not renderer)
raw_path.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
data_js_path.write_text("window.E2E_DATA = " + json.dumps(raw, ensure_ascii=False) + ";\n", encoding="utf-8")

# lock file after write
final_locks = {
    "viewer_data_raw.json": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
    "data.js": hashlib.sha256(data_js_path.read_bytes()).hexdigest(),
}
(OUT / "FROZEN_BASELINE_SHA256.json").write_text(
    json.dumps({"locks_after_annotation": final_locks, "raw_v3": locks,
                "policy": "read-only evidence; renderer must not mutate"},
               ensure_ascii=False, indent=2),
    encoding="utf-8")
print("FROZEN_BASELINE_SHA256.json written")
print("viewer_data_raw.json", final_locks["viewer_data_raw.json"])
