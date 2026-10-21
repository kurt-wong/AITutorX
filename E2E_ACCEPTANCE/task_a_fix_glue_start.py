from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")
old = '''    for m in _LABEL_DIGIT_GLUE_RE.finditer(text):
        # token is `2D.` — content starts after glue+letter+sep
        hits.append((m.start(2), m.end(), m.group(2).upper()))'''
new = '''    for m in _LABEL_DIGIT_GLUE_RE.finditer(text):
        # token is `2D.` — glue digit belongs to the label TOKEN (not previous content)
        # so previous option content ends before `2`, and D content starts after `D.`
        hits.append((m.start(1), m.end(), m.group(2).upper()))'''
if old not in s:
    print("digit glue span block not found")
else:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("fixed digit-glue token start")
