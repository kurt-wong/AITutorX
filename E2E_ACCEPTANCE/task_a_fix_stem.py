from pathlib import Path
p = Path(r"D:\Project\AITutors-v3\backend\app\domains\resolver\resolver.py")
s = p.read_text(encoding="utf-8")
old = '''        first_option_seq = None
        for lab, entry in option_hits.items():
            if entry[0] == "ok" and entry[1]:
                seq = self._idx.seq_of(entry[1])
                first_option_seq = seq if first_option_seq is None else min(first_option_seq, seq)'''
new = '''        first_option_seq = None
        for lab, entry in option_hits.items():
            # Task A: content/inline hits also carry a line_ref (entry[1])
            if entry[0] in ("ok", "content", "inline") and entry[1]:
                seq = self._idx.seq_of(entry[1])
                first_option_seq = seq if first_option_seq is None else min(first_option_seq, seq)'''
if old not in s:
    print("stem first_option block not found")
else:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("patched _stem_span first_option_seq for content/inline")
