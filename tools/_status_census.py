from pathlib import Path
import re
import collections

root = Path(r"D:\Project\AITutor-X\Docs")
pat = re.compile(r"^\*\*Status\*\*:\s*.{0,3}([A-Z_]{3,})", re.M)

c = collections.Counter()
examples = {}
for p in root.rglob("*.md"):
    m = pat.search(p.read_text(encoding="utf-8", errors="ignore")[:2000])
    key = m.group(1) if m else "(no lifecycle Status line)"
    c[key] += 1
    examples.setdefault(key, p.name)

print("lifecycle Status across all Docs/*.md:")
for k, v in c.most_common():
    print(f"   {k:28} {v:4}   e.g. {examples[k]}")

# explicit ACTIVE check
active = [p.name for p in root.rglob("*.md")
          if re.search(r"^\*\*Status\*\*:\s*.{0,3}ACTIVE", p.read_text(encoding="utf-8",
                                                                    errors="ignore")[:2000], re.M)]
print(f"\nfiles whose LIFECYCLE Status is ACTIVE: {len(active)}")
for a in active[:10]:
    print("   ", a)
