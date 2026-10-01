from pathlib import Path
p = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-artifacts\_write_report.py")
t = p.read_text(encoding="utf-8")
old = 'report = Path(r"D:\\Project\\AITutor-X\\Docs\\60_REPORTS\\E2E-01-BOUNDARY-REALITY-VERIFICATION.md")'
new = 'report = Path(r"D:\\Project\\AITutor-X\\Docs\\60_REPORTS\\E2E-01-BOUNDARY-REALITY-VERIFICATION-v1.1.md")'
if old not in t:
    raise SystemExit("path line not found")
t = t.replace(old, new, 1)
# also neutralize any ACTIVE if present in generator body
t2 = t.replace("ACTIVE", "ARCHIVED-PENDING-OWNER")  # never write ACTIVE into outputs
p.write_text(t, encoding="utf-8")
print("generator path now:", new)
print("ACTIVE in generator:", "ACTIVE" in t)
