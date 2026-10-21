"""INDEPENDENT P1.4-B — negative-test coverage audit.

Enumerates the 24 tests and checks whether ANY of them covers:
  (a) a wrapped/continuation content line being promoted to a NEW option (Q20 bug)
  (b) asserting the repaired option's resolved TEXT is non-degenerate (Q4 bug)
Both are the failure modes this verification found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
F = Path(r"D:\Project\AITutors-v3\backend\tests\test_p14b_option_label_compat.py")
src = F.read_text(encoding="utf-8")
lines = src.splitlines()

# list all test functions with their body
tests = []
cur = None
for i, l in enumerate(lines, 1):
    m = re.match(r"\s*def (test_\w+)", l)
    if m:
        if cur:
            tests.append(cur)
        cur = {"name": m.group(1), "line": i, "body": []}
    elif cur is not None:
        cur["body"].append(l)
if cur:
    tests.append(cur)

print(f"total tests: {len(tests)}")
print()
kw_wrap = ("contin", "wrap", "159", "还原", "Q20")
kw_text = ("compiled_text", ".text", "content", "span_text", "len(")
for t in tests:
    body = "\n".join(t["body"])
    wrap_hit = [k for k in kw_wrap if k in body]
    text_hit = [k for k in kw_text if k in body]
    print(f"  L{t['line']:<4} {t['name']}")
    print(f"        wrap/continuation coverage: {wrap_hit or 'NONE'}")
    print(f"        option-text assertion     : {text_hit or 'NONE'}")

print()
print("=" * 80)
print("files/classes referenced by the suite:")
for m in re.finditer(r"^(class \w+|\s*from [\w.]+ import .*|\s*import .*)$", src, re.M):
    print("   ", m.group(0).strip()[:100])
