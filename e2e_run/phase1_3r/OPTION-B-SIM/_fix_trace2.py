from pathlib import Path
p = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM\p14e_e2e_trace.py")
s = p.read_text(encoding="utf-8")
s = s.replace('"qtype": leaf.original_question_type,', '"qtype": leaf.canonical_question_type,')
s = s.replace('"content_roles": [(c.role, c.span_id) for c in leaf.content],',
              '"stem_preview": (leaf.stem.text[:80] if leaf.stem else None),')
p.write_text(s, encoding="utf-8")
print("patched")
