"""READ-ONLY: bound the "empty content -> whole-line fallback" risk.

The fallback fires when the content between a declared label's end and the next
declared label is EMPTY. That can only happen when two declared option labels
share one physical line with nothing between them.

So: count, across all 9 papers, how many (unit, line) have >1 declared option
label with empty content between them. If that set is exactly Q17's L125 (B+H),
the fallback is CONTAINED to the known annotation defect and cannot affect
normal samples.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def main() -> None:
    # 1) manifest-level: two declared labels on the same line
    print("=" * 92)
    print("1. MANIFEST: units where >1 declared option shares the SAME line")
    print("=" * 92)
    same_line = []
    for man_p in sorted((EA / "04_V3_INPUT").glob("*.manifest.json")):
        subj = man_p.stem.replace(".manifest", "")
        m = json.loads(man_p.read_text(encoding="utf-8"))
        for u in m.get("units", []):
            opts = u.get("options") or []
            byline = Counter()
            for o in opts:
                byline[(o.get("start_line"), o.get("end_line"))] += 1
            for ln, n in byline.items():
                if n > 1:
                    labs = [o.get("label") for o in opts
                            if (o.get("start_line"), o.get("end_line")) == ln]
                    same_line.append((subj, u.get("unit_id"), ln, labs))
    print(f"   count: {len(same_line)}")
    for s in same_line:
        print(f"      {s[0]}/{s[1]}  lines={s[2]}  labels={s[3]}")

    # 2) does the source line actually put content between those labels?
    print("\n" + "=" * 92)
    print("2. SOURCE: is the content between those labels empty?")
    print("=" * 92)
    for subj, uid, ln, labs in same_line:
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        m = json.loads(man_p.read_text(encoding="utf-8"))
        src = Path(str(m.get("source_file", "")))
        if not src.exists():
            print(f"   {subj}/{uid}: source missing")
            continue
        lines = src.read_text(encoding="utf-8").splitlines()
        lo, hi = ln
        if not (lo and hi and 1 <= lo <= len(lines)):
            print(f"   {subj}/{uid}: bad line {ln}")
            continue
        text = lines[lo - 1]
        print(f"\n   {subj}/{uid}  L{lo}: {text.strip()!r}")
        # locate label markers and the content between consecutive ones
        hits = [(mm.group(1).upper(), mm.start(), mm.end()) for mm in LAB.finditer(text)]
        print(f"      label markers found: {[(h[0]) for h in hits]}")
        for i, (lab, _s, e) in enumerate(hits):
            end = hits[i + 1][1] if i + 1 < len(hits) else len(text)
            content = text[e:end].strip()
            print(f"         {lab}: content={content!r}  empty={not content}")

    # 3) whole-corpus: how many declared labels produce EMPTY content?
    print("\n" + "=" * 92)
    print("3. WHOLE CORPUS: declared option labels whose between-label content is EMPTY")
    print("=" * 92)
    empty_hits = []
    for man_p in sorted((EA / "04_V3_INPUT").glob("*.manifest.json")):
        subj = man_p.stem.replace(".manifest", "")
        m = json.loads(man_p.read_text(encoding="utf-8"))
        src = Path(str(m.get("source_file", "")))
        if not src.exists():
            continue
        lines = src.read_text(encoding="utf-8").splitlines()
        for u in m.get("units", []):
            opts = u.get("options") or []
            if len(opts) < 2:
                continue
            # group by line
            byline = {}
            for o in opts:
                byline.setdefault(o.get("start_line"), []).append(o.get("label"))
            for ln, labs in byline.items():
                if len(labs) < 2 or not (ln and 1 <= ln <= len(lines)):
                    continue
                text = lines[ln - 1]
                hits = [(mm.group(1).upper(), mm.start(), mm.end()) for mm in LAB.finditer(text)]
                for i, (lab, _s, e) in enumerate(hits):
                    end = hits[i + 1][1] if i + 1 < len(hits) else len(text)
                    if lab in labs and not text[e:end].strip():
                        empty_hits.append((subj, u.get("unit_id"), ln, lab))
    print(f"   count of EMPTY-content declared labels: {len(empty_hits)}")
    for h in empty_hits:
        print(f"      {h}")

    print("\n" + "=" * 92)
    print("VERDICT")
    print("=" * 92)
    if empty_hits and all(h[0] == "化学" and h[1] == "Q17" for h in empty_hits):
        print("   The fallback trigger is CONTAINED to 化学/Q17.")
        print("   => it cannot affect normal samples; risk is bounded, not general.")
    else:
        print(f"   Trigger appears in: {sorted({(h[0], h[1]) for h in empty_hits})}")
        print("   => review before concluding containment.")


if __name__ == "__main__":
    main()
