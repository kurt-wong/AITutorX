from pathlib import Path
p = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM\p14e_e2e_trace.py")
s = p.read_text(encoding="utf-8")
s = s.replace(
    '"text_preview": (s.text or "")[:100],',
    '"text_preview": (getattr(s, "evidence", None) or str(getattr(s, "line_refs", "")))[:100],',
)
p.write_text(s, encoding="utf-8")
print("patched")
