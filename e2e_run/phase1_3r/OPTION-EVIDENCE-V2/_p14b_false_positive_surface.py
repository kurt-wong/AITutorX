"""READ-ONLY: false-positive surface for each candidate label-recovery rule.

For every damaged-label regex candidate, scan the WHOLE corpus (not just unit
spans) and classify each hit as:
   - TRUE_POSITIVE: inside a declared options_lines range
   - NEAR_MISS: inside a unit's stem/answer range (would corrupt content)
   - PROSE_HIT: outside every unit range (ordinary prose)

This is the raw material for the negative tests the task requires, and it shows
how narrow a rule must be to be safe.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

RULES = {
    "CLEAN (current producer-like)": re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]"),
    "DIGIT_GLUE  (2D.)": re.compile(r"(?<![A-Za-z0-9_])(\d)([A-Ha-h])\s*[.．、:：,，。)）]"),
    "CHAR_GLUE": re.compile(r"(?<![A-Za-z0-9_\s.．、:：,，。)）])([^\sA-Za-z0-9_])([A-Ha-h])\s*[.．、:：,，。)）]"),
    "SPACE_SEP (D 麦哲伦)": re.compile(r"(?:^|(?<=[。；;：:\n]))([A-Ha-h])[  　]{1,3}(?=[一-鿿])", re.M),
    "SPACE_SEP_LOOSE (any)": re.compile(r"(?<![A-Za-z0-9_])([A-Ha-h])[  　]{1,3}(?=[一-鿿])"),
}


def load_manifest_lines(mf: Path):
    return json.loads(mf.read_text(encoding="utf-8"))


def main() -> None:
    report = {}
    for p in sorted(CORPUS.glob("*/*.manifest.json")):
        paper = p.parent.name
        m = load_manifest_lines(p)
        sf = Path(m.get("source_file", ""))
        if not sf.is_absolute():
            sf = CORPUS / sf
        if not sf.exists():
            continue
        texts = sf.read_text(encoding="utf-8").splitlines()

        opt_ranges, stem_ranges, ans_ranges = [], [], []
        for u in m.get("units", []):
            for key, bucket in (("options_lines", opt_ranges),
                                ("stem_lines", stem_ranges),
                                ("answer_lines", ans_ranges)):
                r = u.get(key)
                if r:
                    bucket.append((r[0], r[1], u.get("unit_id")))

        def where(ln: int) -> str:
            for lo, hi, uid in opt_ranges:
                if lo <= ln <= hi:
                    return "OPTIONS"
            for lo, hi, uid in stem_ranges:
                if lo <= ln <= hi:
                    return "STEM"
            for lo, hi, uid in ans_ranges:
                if lo <= ln <= hi:
                    return "ANSWER/EXPL"
            return "OUTSIDE_ALL"

        for rule_name, rx in RULES.items():
            key = (paper, rule_name)
            c = Counter()
            ex = []
            for i, t in enumerate(texts, start=1):
                for mm in rx.finditer(t):
                    bucket = where(i)
                    c[bucket] += 1
                    if bucket != "OPTIONS" and len(ex) < 3:
                        ex.append({"line": i, "bucket": bucket, "match": mm.group(0)[:30],
                                   "text": t.strip()[:70]})
            report[f"{paper}|{rule_name}"] = {"counts": dict(c), "false_positive_examples": ex}

    totals = {}
    for rule_name in RULES:
        agg = Counter()
        for k, v in report.items():
            if k.endswith("|" + rule_name):
                agg.update(v["counts"])
        totals[rule_name] = dict(agg)

    print("=" * 96)
    print("FALSE-POSITIVE SURFACE PER CANDIDATE RULE (whole corpus)")
    print("=" * 96)
    for rule_name, agg in totals.items():
        tot = sum(agg.values())
        bad = tot - agg.get("OPTIONS", 0)
        print(f"\n{rule_name}")
        print(f"   total hits {tot:<6} in OPTIONS {agg.get('OPTIONS',0):<6} "
              f"STEM {agg.get('STEM',0):<5} ANSWER/EXPL {agg.get('ANSWER/EXPL',0):<5} "
              f"OUTSIDE {agg.get('OUTSIDE_ALL',0):<5}  -> false positives {bad}")
        for k, v in report.items():
            if k.endswith("|" + rule_name) and v["counts"].get("OUTSIDE_ALL", 0) + \
                    v["counts"].get("STEM", 0) + v["counts"].get("ANSWER/EXPL", 0) > 0:
                for e in v["false_positive_examples"][:1]:
                    print(f"      e.g. {k.split('|')[0]} L{e['line']} [{e['bucket']}] "
                          f"{e['match']!r} :: {e['text']!r}")

    OUT.joinpath("_p14b_false_positive_surface.json").write_text(
        json.dumps({"per_paper": report, "totals": totals}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_false_positive_surface.json'}")


if __name__ == "__main__":
    main()
