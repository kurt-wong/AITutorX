"""READ-ONLY: survey the LaTeX/HTML shapes the Gate-1/Gate-2 renderer must survive.

Measures, over the 9-subject acceptance corpus question records (data.js) and the
MD/PDF preview text:
  - how much math is inline ($...$) vs display ($$...$$)
  - which LaTeX constructs appear (frac, sqrt, matrices, cases, arrows, charges)
  - whether option/stem text mixes raw HTML (<div>, <img>, <table>)
  - occurrences of unclosed $ (the classic silent-render-failure case)
This defines the renderer's required feature set and its negative tests.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def load():
    s = (EA / "data.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


D = load()

# gather all question-facing text
texts = []
for subj, e in D["subjects"].items():
    for q in (e.get("questions") or []):
        texts.append(("stem", subj, q.get("stem") or ""))
        texts.append(("answer", subj, q.get("answer_text") or ""))
        for o in (q.get("options") or []):
            texts.append(("option", subj, o.get("text") or ""))
    texts.append(("md_preview", subj, e.get("md_text_preview") or ""))
    texts.append(("pdf_preview", subj, e.get("pdf_text_preview") or ""))

blob = "\n".join(t[2] for t in texts)


def count(pattern, flags=0):
    return len(re.findall(pattern, blob, flags))


print("=" * 94)
print("A. corpus text volume")
print("=" * 94)
print(f"   text fields collected : {len(texts)}")
print(f"   chars                 : {len(blob)}")

print("\n" + "=" * 94)
print("B. math delimiters")
print("=" * 94)
disp = count(r"\$\$")
inline = count(r"(?<!\$)\$(?!\$)")
print(f"   $$...$$ (display) occurrences : {disp}")
print(f"   $...$   (inline)  occurrences : {inline}")
print(f"   $ count total                 : {blob.count('$')}  (odd => at least one unclosed)")

print("\n" + "=" * 94)
print("C. LaTeX constructs present (renderer feature requirements)")
print("=" * 94)
feats = {
    "frac": r"\\frac",
    "sqrt": r"\\sqrt",
    "superscript ^": r"\^",
    "subscript _": r"_\{",
    "begin/end env": r"\\begin\{",
    "matrix/array": r"\\begin\{(array|matrix|pmatrix|bmatrix|cases)\}",
    "cases": r"\\begin\{cases\}",
    "arrow (to/rightarrow)": r"\\x?rightarrow|\\to\b",
    "mathrm (chem)": r"\\mathrm",
    "overset/underset": r"\\(over|under)set",
    "uparrow/downarrow": r"\\(up|down)arrow",
    "cdot/times": r"\\c?dot|\\times",
    "left/right": r"\\(left|right)",
    "text{": r"\\text\{",
    "displaystyle": r"\\displaystyle",
    "hspace/underline": r"\\hspace|\\underline",
}
for name, pat in feats.items():
    n = count(pat)
    mark = "" if n else "   (absent)"
    print(f"   {name:<26}{n:>6}{mark}")

print("\n" + "=" * 94)
print("D. HTML mixed into question-facing text (renderer must not eat/show raw)")
print("=" * 94)
for name, pat in (("<div", r"<div"), ("<img", r"<img"), ("<table", r"<table"),
                  ("<tr/<td", r"<t[rd]"), ("<span", r"<span")):
    n = count(pat)
    print(f"   {name:<10}{n:>6}")

print("\n" + "=" * 94)
print("E. hazard cases for a naive renderer")
print("=" * 94)
# dollar used as currency / stray
stray = [t for t in texts if t[2].count("$") % 2 == 1]
print(f"   fields with ODD number of $ (unclosed -> silent failure risk): {len(stray)}")
for kind, subj, s in stray[:6]:
    print(f"      [{kind}/{subj}] {s[:88]!r}")

raw_bs = [t for t in texts if re.search(r"\\[a-zA-Z]{2,}", t[2]) and "$" not in t[2]]
print(f"   fields with LaTeX-ish backslash but NO $ delimiter: {len(raw_bs)}")
for kind, subj, s in raw_bs[:6]:
    print(f"      [{kind}/{subj}] {s[:88]!r}")

# chemical formula patterns in chemistry
chem = [t for t in texts if t[1] == "化学" and ("\\mathrm" in t[2] or "$" in t[2])]
print(f"   chemistry fields containing math: {len(chem)}")
for kind, subj, s in chem[:4]:
    print(f"      [{kind}] {s[:88]!r}")
