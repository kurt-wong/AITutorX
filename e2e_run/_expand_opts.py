import json, re
from pathlib import Path

mf_path = Path(r'D:\Project\Papers\Ocr-markdown\reslice-p2-b1\高一\化学\2016-2019北京高一化学下学期期末汇编：化学反应原理（教师版）(1).manifest.json')
src_path = Path(json.loads(mf_path.read_text(encoding='utf-8'))['source_file'])
lines = src_path.read_text(encoding='utf-8', errors='replace').splitlines()
OPT_RE = re.compile(r'(?<![\w])([A-Ha-h])\s*[.．、:)\uff09]')

d = json.loads(mf_path.read_text(encoding='utf-8'))
expanded = 0
for u in d.get('units', []):
    if u.get('options') or not u.get('options_lines'):
        continue
    ol = u['options_lines']
    start, end = int(ol[0]), int(ol[1])
    labels = []
    for ln in range(start, min(end+1, len(lines)+1)):
        for m in OPT_RE.finditer(lines[ln-1]):
            lab = m.group(1).upper()
            if lab not in [x['label'] for x in labels]:
                labels.append({'label': lab, 'start_line': ln, 'end_line': ln})
    if labels:
        u['options'] = labels
        expanded += 1
        print(u['unit_id'], '->', [x['label'] for x in labels])

out = Path(r'D:\Project\AITutor-X\e2e_run\minimal-loop-manifest.json')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
print('Expanded', expanded, 'units ->', out)
