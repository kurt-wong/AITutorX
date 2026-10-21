"""P1.4-B: apply fixed Producer option-label parser to the 3 B-sample manifests."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, r"D:\Project\Papers\scripts")
import reslice_pipeline as rp  # noqa: E402

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
TARGETS = [("化学", "Q23"), ("数学", "Q4"), ("历史", "Q29")]
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")

def main():
    results = []
    for paper, unit_id in TARGETS:
        man_path = next(CORPUS.glob(f"{paper}/*.manifest.json"), None)
        if not man_path:
            results.append({"paper": paper, "unit": unit_id, "error": "manifest not found"})
            continue
        man = json.loads(man_path.read_text(encoding="utf-8"))
        src = Path(man.get("source_file") or "")
        if not src.is_file():
            results.append({"paper": paper, "unit": unit_id, "error": "source not found"})
            continue
        lines = src.read_text(encoding="utf-8").splitlines()
        u = next((x for x in man["units"] if x.get("unit_id") == unit_id), None)
        if not u:
            results.append({"paper": paper, "unit": unit_id, "error": "unit missing"})
            continue
        before = [o.get("label") for o in (u.get("options") or [])]
        notes = rp._expand_option_spans(man, lines)
        u2 = next(x for x in man["units"] if x.get("unit_id") == unit_id)
        after = [o.get("label") for o in (u2.get("options") or [])]
        changed = before != after
        if changed:
            bak = man_path.with_suffix(man_path.suffix + ".p14b.bak")
            if not bak.exists():
                shutil.copy2(man_path, bak)
            man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{paper}/{unit_id}: {before} -> {after} changed={changed}")
        for n in notes:
            if unit_id in str(n):
                print("   ", n)
        results.append({
            "paper": paper, "unit": unit_id, "manifest": str(man_path),
            "old_labels": before, "new_labels": after, "changed": changed,
            "notes": [n for n in notes if unit_id in str(n)],
        })
    (OUT / "manifest_backfill_result.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT / "manifest_backfill_result.json")

if __name__ == "__main__":
    main()
