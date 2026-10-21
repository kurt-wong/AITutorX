"""READ-ONLY (corrected): Papers Producer output vs V3 Phase-1 consumed corpus.

Papers batch-C contains, per paper:
    <name>.md              <- line-numbered source ([L0001] prefixes)
    <name>.annotated.md    <- sliced display form
    <name>.manifest.json   <- V3 semantic_units form

V3 phase1 corpus contains:
    <name>.md              <- what Phase 1 actually read
    <name>.manifest.json   <- what Phase 1 actually read (+ hand backfill, .p14b.bak)

Compares each role pairwise by sha256, then (for the focus papers) does a
line-by-line text comparison to locate the first divergence.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PAPERS = Path(r"D:\Project\Papers\Ocr-markdown\reslice-batch-C")
V3 = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

FOCUS = ["2018北京春季高中会考数学（教师版）(1)",
         "2018北京春季高中会考化学（教师版）(1)",
         "2018北京夏季高中会考历史（教师版）(1)",
         "2018北京春季高中会考英语（教师版）(1)"]
LN = re.compile(r"^\[L(\d+)\]\s?")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def strip_ln(text: str) -> str:
    return "\n".join(LN.sub("", l) for l in text.splitlines())


def main() -> None:
    # ---- role A: source .md (papers, line-numbered) vs V3 .md ----
    p_md = {p.relative_to(PAPERS).with_suffix("").as_posix(): p for p in PAPERS.rglob("*.md")
            if not p.name.endswith(".annotated.md")}
    v_md = {p.relative_to(V3).with_suffix("").as_posix(): p for p in V3.rglob("*.md")}

    print("=" * 96)
    print("ROLE A — Papers line-numbered .md  vs  V3 .md")
    print("=" * 96)
    common = sorted(set(p_md) & set(v_md))
    print(f"   papers .md={len(p_md)}  v3 .md={len(v_md)}  common={len(common)}")
    ident = sum(1 for k in common if sha(p_md[k]) == sha(v_md[k]))
    print(f"   byte-identical: {ident} / {len(common)}")

    print("\n   --- focus papers: line-numbered vs de-numbered ---")
    focus_recs = {}
    for k in common:
        name = Path(k).name
        if name not in FOCUS:
            continue
        pt = p_md[k].read_text(encoding="utf-8")
        vt = v_md[k].read_text(encoding="utf-8")
        stripped = strip_ln(pt)
        eq_stripped = stripped == vt
        pl, vl = pt.splitlines(), vt.splitlines()
        first_div = None
        for i in range(max(len(pl), len(vl))):
            a = LN.sub("", pl[i]) if i < len(pl) else "<missing>"
            b = vl[i] if i < len(vl) else "<missing>"
            if a != b:
                first_div = {"line": i + 1, "papers": a[:90], "v3": b[:90]}
                break
        print(f"\n   {name}")
        print(f"      papers lines={len(pl)}  v3 lines={len(vl)}")
        print(f"      sha equal={sha(p_md[k]) == sha(v_md[k])}   "
              f"equal AFTER stripping [Lnnnn]={eq_stripped}")
        print(f"      first divergence after strip: {first_div}")
        focus_recs[name] = {"papers_lines": len(pl), "v3_lines": len(vl),
                            "equal_stripped": eq_stripped, "first_div": first_div}

    # ---- role B: Papers manifest vs V3 manifest and vs V3 .p14b.bak ----
    print("\n" + "=" * 96)
    print("ROLE B — Papers .manifest.json  vs  V3 .manifest.json / .p14b.bak")
    print("=" * 96)
    p_man = {p.relative_to(PAPERS).as_posix().replace(".manifest.json", ""): p
             for p in PAPERS.rglob("*.manifest.json")}
    v_man = {p.relative_to(V3).as_posix().replace(".manifest.json", ""): p
             for p in V3.rglob("*.manifest.json")}
    commonb = sorted(set(p_man) & set(v_man))
    identb = [k for k in commonb if sha(p_man[k]) == sha(v_man[k])]
    print(f"   common={len(commonb)}  byte-identical={len(identb)}")

    for k in commonb:
        if Path(k).name not in FOCUS:
            continue
        print(f"\n   {Path(k).name}")
        print(f"      papers sha {sha(p_man[k])[:16]}")
        print(f"      v3     sha {sha(v_man[k])[:16]}")
        bak = Path(str(v_man[k]) + ".p14b.bak")
        if bak.exists():
            print(f"      v3.bak sha {sha(bak)[:16]}   "
                  f"papers==bak? {sha(p_man[k]) == sha(bak)}")
        # structural diff papers vs v3.bak (pre-P1.4-B state)
        if bak.exists():
            a = json.loads(p_man[k].read_text(encoding="utf-8"))
            b = json.loads(bak.read_text(encoding="utf-8"))
            ua = {str(u.get("unit_id")): u for u in a.get("units", [])}
            ub = {str(u.get("unit_id")): u for u in b.get("units", [])}
            diffs = []
            for uid in sorted(set(ua) & set(ub)):
                for fld in ("options", "options_lines", "stem_lines", "answer_lines"):
                    if ua[uid].get(fld) != ub[uid].get(fld):
                        diffs.append((uid, fld))
            print(f"      units papers={len(ua)} v3.bak={len(ub)}  field diffs={diffs[:12]}")

    OUT.joinpath("_p14b_papers_vs_v3.json").write_text(
        json.dumps({"role_a_focus": focus_recs,
                    "role_a_common": len(common), "role_a_identical": ident,
                    "role_b_common": len(commonb), "role_b_identical": len(identb)},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_papers_vs_v3.json'}")


if __name__ == "__main__":
    main()
