"""READ-ONLY: manifest identity sanity for the 4 focus papers.

Checks whether a paper's manifest unit actually corresponds to that paper's own
source lines, or whether a unit has bled across papers during annotation.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
PAPERS = ["数学", "化学", "历史", "英语"]


def load_texts(source_file: str):
    p = Path(source_file)
    if not p.is_absolute():
        p = CORPUS / source_file
    return p.read_text(encoding="utf-8").splitlines() if p.exists() else []


for paper in PAPERS:
    for mf in sorted((CORPUS / paper).glob("*.manifest.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        sf = m.get("source_file")
        texts = load_texts(sf)
        print("=" * 90)
        print(f"{paper}  manifest={mf.name}")
        print(f"   declared source_file = {sf!r}   (lines loaded: {len(texts)})")
        units = m.get("units", [])
        print(f"   units: {len(units)}   "
              f"unit_ids: {[u.get('unit_id') for u in units][:12]}"
              f"{' ...' if len(units) > 12 else ''}")
        qtypes = Counter(u.get("original_question_type") for u in units)
        print(f"   question_type histogram: {dict(qtypes)}")
        # show first stem line of each unit to prove it belongs to THIS paper
        for u in units[:6]:
            sl = u.get("stem_lines")
            if sl and texts:
                lo = max(1, min(sl[0], len(texts)))
                print(f"     {str(u.get('unit_id')):<8} stem L{lo}: {texts[lo-1].strip()[:76]}")
        # the focus units specifically
        for uid in ("Q4", "Q23", "Q29"):
            for u in units:
                if str(u.get("unit_id")) == uid:
                    sl = u.get("stem_lines")
                    if sl and texts:
                        lo = max(1, min(sl[0], len(texts)))
                        print(f"   >> {uid} stem L{lo}: {texts[lo-1].strip()[:90]}")
                        print(f"      type={u.get('original_question_type')} "
                              f"opts={[o.get('label') for o in (u.get('options') or [])]} "
                              f"options_lines={u.get('options_lines')} "
                              f"answer_lines={u.get('answer_lines')}")
