from pathlib import Path
p = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-VERIFICATION.md")
text = p.read_text(encoding="utf-8")
needle = "**Name**: Frozen Boundary Reality Verification（非完整闭环 E2E）"
if needle not in text:
    raise SystemExit("anchor not found")
if "superseded_by" not in text:
    insert = needle + "\n**superseded_by**: E2E-01-BOUNDARY-REALITY-VERIFICATION-v1.1.md\n**Disposition**: ARCHIVED"
    text = text.replace(needle, insert, 1)
    p.write_text(text, encoding="utf-8")
    print("header pointer added")
else:
    print("already present")
print("bytes", p.stat().st_size)
