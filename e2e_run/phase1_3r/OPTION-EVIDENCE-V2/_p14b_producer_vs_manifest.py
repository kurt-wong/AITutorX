"""INDEPENDENT P1.4-B verification — does the new Producer produce the patched manifests?

The resolver reads option labels from the MANIFEST (`reference.py` builds
`option_label` targets from `options[]`). So the +1 can only appear if the
manifest carries label D. MIMO reports "corpus Q23/Q4/Q29 manifests: backfilled
label=D (.p14b.bak kept)" -> a HAND EDIT, not a Producer regeneration.

This script:
  1. imports the NEW Papers `_detect_option_labels` from the Papers repo
  2. replays it over EVERY unit in ALL 9 papers
  3. compares detected labels vs the manifest's current `options[]`
  4. reports which units the new Producer would ADD/MISS, and whether the
     three hand-patched manifests agree with what the Producer would emit
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PAPERS = Path(r"D:\Project\Papers")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

spec = importlib.util.spec_from_file_location("reslice_pipeline", PAPERS / "scripts" / "reslice_pipeline.py")
rp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rp)
print("loaded", rp.__file__)
print("has _detect_option_labels:", hasattr(rp, "_detect_option_labels"))


def main() -> None:
    changes, agree, disagree = [], [], []
    total_units = 0
    for mf in sorted(CORPUS.glob("*/*.manifest.json")):
        paper = mf.parent.name
        man = json.loads(mf.read_text(encoding="utf-8"))
        sf = Path(man.get("source_file", ""))
        if not sf.is_absolute():
            sf = CORPUS / sf
        if not sf.exists():
            print("!! missing source", sf)
            continue
        lines = sf.read_text(encoding="utf-8").splitlines()

        for u in man.get("units", []):
            total_units += 1
            ol = u.get("options_lines")
            if not ol or len(ol) != 2:
                continue
            start, end = int(ol[0]), int(ol[1])
            if start < 1 or end > len(lines) or start > end:
                continue
            detected = rp._detect_option_labels(lines, start, end)
            det_labels = [lab for lab, _, _ in detected]
            cur = [o.get("label") for o in (u.get("options") or []) if isinstance(o, dict)]
            added = [l for l in det_labels if l not in cur]
            missing = [l for l in cur if l not in det_labels]
            rec = {"paper": paper, "unit": u.get("unit_id"), "options_lines": [start, end],
                   "current": cur, "detected": det_labels,
                   "would_add": added, "would_lose": missing,
                   "detected_lines": [{"label": l, "line": ln} for l, ln, _ in detected]}
            if added or missing:
                changes.append(rec)
            if set(added) | set(missing):
                disagree.append(rec)
            else:
                agree.append(rec)

    print("=" * 94)
    print("NEW PRODUCER vs CURRENT MANIFESTS — all 9 papers")
    print("=" * 94)
    print(f"units scanned                : {total_units}")
    print(f"units WITH options_lines     : {len(agree) + len(disagree)}")
    print(f"units where Producer == manifest : {len(agree)}")
    print(f"units where Producer != manifest : {len(disagree)}")
    print()
    from collections import Counter
    print("would_add by paper:", dict(Counter((c['paper'], tuple(c['would_add'])) for c in changes)))

    print("\n--- units the new Producer would CHANGE ---")
    for c in changes:
        print(f"  {c['paper']}/{c['unit']:<12} lines={c['options_lines']}")
        print(f"      manifest : {c['current']}")
        print(f"      producer : {c['detected']}   add={c['would_add']} lose={c['would_lose']}")
        print(f"      detected labels@lines: {c['detected_lines']}")

    OUT.joinpath("_p14b_producer_vs_manifest.json").write_text(
        json.dumps({"changes": changes, "agree_count": len(agree),
                    "disagree_count": len(disagree)}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_producer_vs_manifest.json'}")


if __name__ == "__main__":
    main()
