"""READ-ONLY audit of MIMO's updated Viewer.

CRITICAL question: MIMO reports "已校正选项切分" (corrected option splitting) and
added _improve_options.py / _fix_q4_opts.py, and viewer_data.json SHRANK
(302031 -> 300258 bytes). If the viewer now displays normalised options instead
of the pipeline's raw output, it would HIDE the very defects it exists to reveal.

Checks:
  A. does data.js carry questions now?
  B. are the KNOWN defects still visible in the export?
       - 化学 Q20 must still show 5 options incl. E='还原反应'
       - 数学 Q4  must still show label-only D (text == 'D')
  C. does the export keep RAW values alongside any corrected display form?
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def load_datajs():
    s = (EA / "data.js").read_text(encoding="utf-8")
    body = s[s.index("{"): s.rindex("}") + 1]
    return json.loads(body)


def show(rec, title):
    print("=" * 92)
    print(title)
    if not rec:
        print("   <no record>")
        return
    print(f"   gate   : {rec.get('gate')}")
    print(f"   reason : {str(rec.get('reason'))[:110]}")
    print(f"   labels : {rec.get('labels')}  n_options={rec.get('n_options')}")
    for o in (rec.get("options") or []):
        t = str(o.get("text") or "")
        lab = str(o.get("label"))
        deg = t.strip().upper() == lab.upper()
        print(f"      {lab}: len={len(t.strip()):<4} {t.strip()[:62]!r}"
              f"{'   <<< LABEL-ONLY' if deg else ''}")
    print(f"   answer : {str(rec.get('answer_text'))[:70]!r}")
    keys = sorted(rec.keys())
    print(f"   keys   : {keys}")


def main() -> None:
    d = load_datajs()
    tot = sum(len(e.get("questions") or []) for e in d["subjects"].values())
    print("=" * 92)
    print("A. data.js now carries questions?")
    print("=" * 92)
    print(f"   subjects={len(d['subjects'])}  total questions={tot}")

    for subj, uid in (("化学", "Q20"), ("数学", "Q4"), ("化学", "Q7")):
        recs = [q for q in (d["subjects"].get(subj, {}).get("questions") or [])
                if str(q.get("unit_id")) == uid]
        show(recs[0] if recs else None, f"B. {subj} {uid}  (as exported)")

    # look for any 'raw' style field anywhere
    print("\n" + "=" * 92)
    print("C. raw-vs-display: which keys exist on question records?")
    print("=" * 92)
    allkeys = set()
    for e in d["subjects"].values():
        for q in (e.get("questions") or []):
            allkeys |= set(q.keys())
    print("   union of question keys:", sorted(allkeys))
    print("   any key containing 'raw'/'orig'/'source':",
          [k for k in allkeys if any(s in k.lower() for s in ("raw", "orig", "source"))])


if __name__ == "__main__":
    main()
