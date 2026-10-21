"""READ-ONLY independent audit of the rebuilt Viewer (data truth + display fidelity)."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_datajs():
    s = (EA / "data.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def main() -> None:
    raw = load_json(EA / "viewer_data_raw.json")
    dj = load_datajs()

    print("=" * 92)
    print("1. S1 claim: data.js == viewer_data_raw.json (questions)")
    print("=" * 92)
    rq = {k: (v.get("questions") or []) for k, v in raw["subjects"].items()}
    dq = {k: (v.get("questions") or []) for k, v in dj["subjects"].items()}
    print(f"   subjects raw={len(rq)} datajs={len(dq)}")
    same = json.dumps(rq, ensure_ascii=False, sort_keys=True) == json.dumps(dq, ensure_ascii=False, sort_keys=True)
    print(f"   questions identical: {same}")

    print("\n" + "=" * 92)
    print("2. option record shape (raw vs display fields?)")
    print("=" * 92)
    qkeys = set()
    for qs in dq.values():
        for q in qs:
            qkeys |= set(q.keys())
    print("   question keys:", sorted(qkeys))
    for qs in dq.values():
        for q in qs:
            if q.get("options_raw"):
                print("   option_raw keys:", sorted(q["options_raw"][0].keys()))
                break
        else:
            continue
        break

    print("\n" + "=" * 92)
    print("3. SENTINELS (independent)")
    print("=" * 92)
    for subj, uid, want_n in (("化学", "Q20", 5), ("数学", "Q4", 4), ("化学", "Q7", 4)):
        rec = [q for q in dq.get(subj, []) if str(q.get("unit_id")) == uid]
        if not rec:
            print(f"   {subj} {uid}: MISSING")
            continue
        q = rec[0]
        oraw = q.get("options_raw") or []
        print(f"   {subj} {uid}: n_options_raw={len(oraw)}")
        for o in oraw:
            t = str(o.get("text_raw") or "")
            print(f"      {o.get('label')}: len={len(t.strip()):<4} {t.strip()[:58]!r}")

    print("\n" + "=" * 92)
    print("4. display fidelity: is anything normalised away?")
    print("=" * 92)
    bare = contam = total = 0
    for qs in dq.values():
        for q in qs:
            for o in (q.get("options_raw") or []):
                total += 1
                t = str(o.get("text_raw") or "").strip()
                if t.upper() == str(o.get("label")).upper():
                    bare += 1
                hits = {m.group(1).upper() for m in re.finditer(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]", t)}
                if len(hits) >= 2:
                    contam += 1
    print(f"   total options_raw       : {total}")
    print(f"   label-only (degenerate) : {bare}   (pre-patch baseline was 2)")
    print(f"   carrying >=2 label token: {contam}   (pre-patch baseline was >0)")

    print("\n" + "=" * 92)
    print("5. Gate1 diff DISPLAY truncation (app.js slices)")
    print("=" * 92)
    aj = (EA / "app.js").read_text(encoding="utf-8")
    for probe in ("p.slice(0, 800)", "m.slice(0, 800)", "r.x.slice(0, 120)"):
        print(f"   app.js contains {probe!r}: {probe in aj}")
    e = dj["subjects"]["数学"]
    print(f"   math pdf_text_len={e.get('pdf_text_len')}  md_text_len={e.get('md_text_len')}")
    print(f"   math pdf_text field present: {'pdf_text' in e}   md_text: {'md_text' in e}")
    print(f"   gate1_anchors present: {len(e.get('gate1_anchors') or [])}")
    an = (e.get("gate1_anchors") or [])
    if an:
        print("   anchor sample keys:", sorted(an[0].keys()))
        for a in an[:4]:
            print(f"      Q{a.get('qn')}: pdf_len={len(str(a.get('pdf') or ''))} "
                  f"md_len={len(str(a.get('md') or ''))} same={a.get('same')}")


if __name__ == "__main__":
    main()
