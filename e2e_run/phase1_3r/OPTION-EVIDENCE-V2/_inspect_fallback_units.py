"""READ-ONLY: the fallback trigger fires in 3 units, not 1.

  化学/Q2   L20  label C
  化学/Q17  L125 label B
  物理/U12-14 L136 label A

Inspect the SOURCE lines and the POST-FIX resolved options for all three.
If the other two also produce whole-line swallowing, the fallback risk is NOT
contained to Q17 and must be registered against Task A's baseline.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
POST = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_POSTFIX_RESULT.json")
BASE = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_PREFIX_BASELINE.json")

TARGETS = [("化学", "Q2", 20), ("化学", "Q17", 125), ("物理", "U12-14", 136)]


def main() -> None:
    post = json.loads(POST.read_text(encoding="utf-8"))["now"]
    base_raw = json.loads(BASE.read_text(encoding="utf-8"))
    base = {s.replace(".manifest", ""): {str(q["unit_id"]): q for q in e["questions"]}
            for s, e in base_raw["subjects"].items()}

    for subj, uid, ln in TARGETS:
        print("=" * 94)
        print(f"{subj} {uid}   (empty-content label on L{ln})")
        print("=" * 94)

        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        m = json.loads(man_p.read_text(encoding="utf-8"))
        src = Path(str(m.get("source_file", "")))
        lines = src.read_text(encoding="utf-8").splitlines()
        lo = max(1, ln - 3)
        hi = min(len(lines), ln + 3)
        for i in range(lo, hi + 1):
            mark = "  <<<" if i == ln else ""
            print(f"   L{i:<5} {lines[i-1][:96]}{mark}")

        for u in m.get("units", []):
            if str(u.get("unit_id")) == uid:
                print(f"   manifest options: "
                      f"{[(o.get('label'), o.get('start_line'), o.get('end_line')) for o in (u.get('options') or [])]}")

        b = base.get(subj, {}).get(uid)
        p = post.get(subj, {}).get(uid)
        for label, rec, tag in (("BASE", b, "修复前"), ("POST", p, "修复后")):
            if not rec:
                print(f"   {tag}: MISSING")
                continue
            print(f"   {tag}: gate={rec['gate']} labels={rec['labels']}")
            for o in (rec.get("options") or []):
                sw = "  <<< SWALLOW" if o.get("swallow") else ""
                ba = "  <<< BARE" if o.get("bare") else ""
                print(f"      {o['label']}: {o['text_raw']!r}{ba}{sw}{'' if tag=='BASE' else ''}")
        print()


if __name__ == "__main__":
    main()
