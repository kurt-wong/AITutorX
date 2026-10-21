"""READ-ONLY: quantify how much of the Viewer export was PATCHED after export.

viewer_data.json / data.js were overwritten in place by
  _improve_options.py (23:31:30) and _fix_q4_opts.py (23:35:06)
with NO raw field preserved. This measures the damage and checks whether any
pre-patch copy of the export survives for recovery.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
V3OUT = EA / "05_V3_OUTPUT"


def load_datajs():
    s = (EA / "data.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def main() -> None:
    d = load_datajs()

    # how many options are now BARE label-only (cleaned) vs normal
    bare = short = total = 0
    for e in d["subjects"].values():
        for q in (e.get("questions") or []):
            for o in (q.get("options") or []):
                total += 1
                t = (o.get("text") or "").strip()
                if t.upper() == str(o.get("label")).upper():
                    bare += 1
                if 0 < len(t) <= 2:
                    short += 1
    print("=" * 92)
    print("Viewer export current state (POST-patch)")
    print("=" * 92)
    print(f"   total options           : {total}")
    print(f"   label-only (degenerate) : {bare}")
    print(f"   len<=2                  : {short}")

    # any option text that still carries a second label?
    import re
    LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")
    contaminated = []
    for e in d["subjects"].values():
        for q in (e.get("questions") or []):
            for o in (q.get("options") or []):
                t = (o.get("text") or "")
                hits = [m.group(1).upper() for m in LAB.finditer(t)]
                if len(set(hits)) >= 2:
                    contaminated.append((q.get("unit_id"), o.get("label"), t[:70]))
    print(f"   option texts carrying >=2 label tokens (residual): {len(contaminated)}")
    for c in contaminated[:8]:
        print(f"      {c[0]} opt {c[1]}: {c[2]!r}")

    # does a pre-patch copy survive anywhere?
    print("\n" + "=" * 92)
    print("Pre-patch recovery candidates")
    print("=" * 92)
    for p in sorted(EA.rglob("*")):
        if p.is_file() and p.suffix in (".json", ".js", ".bak") and p.name != "MANIFEST.json":
            print(f"   {p.relative_to(EA)}  {p.stat().st_size}  {p.stat().st_mtime}")
    print("\n   05_V3_OUTPUT/*.v3.json (written by run_e2e_acceptance.py 23:17-23:18, PRE-patch):")
    for p in sorted(V3OUT.glob("*.v3.json")):
        print(f"      {p.name}  {p.stat().st_size}")

    # does the v3.json still hold the raw option text for Q4?
    print("\n" + "=" * 92)
    print("RAW option text for 数学 Q4 in PRE-patch evidence (05_V3_OUTPUT/数学.v3.json)")
    print("=" * 92)
    mp = V3OUT / "数学.v3.json"
    if mp.exists():
        raw = json.loads(mp.read_text(encoding="utf-8"))
        s = json.dumps(raw, ensure_ascii=False)
        for probe in ("关于直线 y=x 对称 2D.", '"D"', "涉及了氧", "还原反应"):
            print(f"   contains {probe!r}: {probe in s}")
        # try to show Q4 record
        def walk(o):
            if isinstance(o, dict):
                if str(o.get("unit_id")) == "Q4" or str(o.get("leaf_id")) == "Q4":
                    print("   Q4 record:", json.dumps(o, ensure_ascii=False)[:400])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(raw)


if __name__ == "__main__":
    main()
