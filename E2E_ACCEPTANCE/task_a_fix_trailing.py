from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")
old = '''        found_ok = [lab for lab in labels if lab in found and found[lab][0] in ("ok", "inline")]'''
new = '''        # Task A: "content" hits count as located options for sequential trailing
        found_ok = [lab for lab in labels if lab in found and found[lab][0] in ("ok", "inline", "content")]'''
if old not in s:
    print("found_ok line not found")
else:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("patched found_ok to include content")
