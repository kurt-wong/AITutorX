"""Patch survey v2.2 — tighten SPACE_SEP and C/B0 handling."""
from pathlib import Path
p = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\option_evidence_survey_v2.py")
s = p.read_text(encoding="utf-8")
old = r'SPACE_SEP = re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])[  ]{1,3}(?=[\u4e00-\u9fffA-Za-z(（$\\])")'
# the file has a real space char class; find the line
import re
m = re.search(r'SPACE_SEP = re\.compile\(r".*?"\)', s)
print("found SPACE_SEP:", bool(m), m.group(0)[:80] if m else None)
if m:
    s = s[:m.start()] + r'SPACE_SEP = re.compile(r"(?:^|(?<=[。；;：:\n]))([A-Ha-h])[  　]{1,3}(?=[一-鿿])", re.M)' + s[m.end():]
# also remove SPACE_SEP from scan loop patterns that fire mid-line — already via regex
# Fix classify: empty declared+resolved+no clean labels -> IR incomplete not B/C
old_b = '''    if b_damaged_undeclared:
        d0 = b_damaged_undeclared[0]
        primary = "B"'''
new_b = '''    ir_absent = (not declared) and (not resolved) and (not src_clean_u) and (not src_damaged)

    if ir_absent and not src_option_like:
        primary = "F0"
        detail = "IR_INCOMPLETE: no declared/resolved/source labels; out of option-evidence scope"
        evidence.append("F0 via empty IR and empty source labels")
    elif ir_absent and src_option_like:
        primary = "F0"
        detail = (
            f"IR_INCOMPLETE_WITH_RAW_TEXT: no labels at all; raw option-like/other text "
            f"L{[u['line'] for u in src_option_like[:3]]} — not counted as B (no label contract yet)"
        )
        evidence.append("F0 via IR absent; raw text present but no label contract")
    elif b_damaged_undeclared:
        d0 = b_damaged_undeclared[0]
        primary = "B"'''
if old_b not in s:
    print("old_b block not found")
else:
    s = s.replace(old_b, new_b, 1)
    print("patched classify prefix")
# update classification model note
s = s.replace('"survey_version": "option-evidence-v2.1-source-first"',
              '"survey_version": "option-evidence-v2.2-source-first"')
p.write_text(s, encoding="utf-8")
print("patched", p)
