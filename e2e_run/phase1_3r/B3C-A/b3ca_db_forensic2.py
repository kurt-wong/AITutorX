"""B3c-A DB forensic #2 — classify gate outcomes; test the
'answer_lines actually points at the 解答/解析 block' hypothesis.

Observed in forensic #1:
  every 数学 Q2..Q50 pending_review carries
    "answer span 'sp-Qn.answer' overlaps explanation region at lines [P1Lxxx]
     (role provenance violation)"
  and the 2 rejected (U52.sub / U53.sub) carry the same class + empty stem.

That is the signature of answer evidence now containing 详解 content.
"""
from __future__ import annotations

import asyncio
import json
import re
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

import asyncpg

sys.path.insert(0, r"D:\Project\AITutors-v3\backend")
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

DSN = "postgresql://aitutors:change-me@localhost:5432/aitutors"
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-A")

_EXPL_HEADERS = ("【详解】", "【解析】", "【解答】", "【答案及解析】", "【分析】", "【考点】")
_ANS_OVERLAP = re.compile(r"answer span '([^']+)' overlaps explanation region at lines \[([^\]]*)\]")


async def db_part() -> dict:
    c = await asyncpg.connect(DSN)
    rows = await c.fetch("SELECT id, payload FROM admission_candidates")
    await c.close()

    decisions = Counter()
    reason_kind = Counter()
    overlap_by_unit = defaultdict(list)
    stem_empty = []
    for r in rows:
        pl = r["payload"]
        if isinstance(pl, str):
            pl = json.loads(pl)
        gp = (pl or {}).get("gate_policy") or {}
        d = gp.get("decision") or "?"
        decisions[d] += 1
        for reason in gp.get("reasons") or []:
            if "overlaps explanation region" in reason:
                reason_kind["answer_overlaps_explanation"] += 1
                m = _ANS_OVERLAP.search(reason)
                if m:
                    refs = re.findall(r"P1L\d+", m.group(2))
                    overlap_by_unit[m.group(1)].append(refs)
            elif "not strict-auto" in reason:
                reason_kind["type_not_strict_auto"] += 1
            elif "answer not expressible as canonical value" in reason:
                reason_kind["answer_not_expressible"] += 1
            elif "no non-empty stem text" in reason:
                reason_kind["empty_stem"] += 1
                stem_empty.append(r["id"])
            elif "not byte-proven" in reason:
                reason_kind["not_byte_proven"] += 1
            else:
                reason_kind[f"other:{reason[:60]}"] += 1
    return {
        "decisions": dict(decisions),
        "reason_kind": dict(reason_kind),
        "n_candidates_with_answer_explanation_overlap": len(overlap_by_unit),
        "sample_overlap_units": dict(list(overlap_by_unit.items())[:15]),
        "empty_stem_count": len(stem_empty),
    }


def content_part() -> dict:
    """Check: does the declared answer_lines range contain explanation headers,
    i.e. does the Producer's 'answer_lines' point at the 解答 block?"""
    per_paper = {}
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        tb = {i + 1: sl.text for i, sl in enumerate(srs)}
        rec = {"units": 0, "declared": 0, "multi": 0,
               "range_has_expl_header": 0, "range_has_solution_word": 0,
               "single_declared": 0, "single_has_letter": 0, "single_is_solution": 0,
               "samples": []}
        for u in m.units:
            rec["units"] += 1
            al = u.answer_lines
            if not al:
                continue
            s, e = int(al[0]), int(al[1])
            body = "\n".join(tb.get(n, "") for n in range(s, e + 1))
            rec["declared"] += 1
            has_hdr = any(h in body for h in _EXPL_HEADERS)
            if has_hdr:
                rec["range_has_expl_header"] += 1
            if e > s:
                rec["multi"] += 1
                if has_hdr:
                    rec["range_has_solution_word"] += 1
            else:
                rec["single_declared"] += 1
                if has_hdr:
                    rec["single_is_solution"] += 1
                # does the single declared line look like a plain answer value?
                t = tb.get(s, "")
                t2 = re.sub(r"^\s*[0-9]{1,3}\s*[.．、:)]*\s*", "", t).strip()
                if re.fullmatch(r"[（(]?[A-Da-d][）)]?[。．.]?", t2 or ""):
                    rec["single_has_letter"] += 1
                if len(rec["samples"]) < 6:
                    rec["samples"].append({
                        "unit_id": u.unit_id, "answer_lines": [s, e],
                        "text": t[:120],
                    })
        per_paper[p.parent.name] = rec
    return per_paper


async def main() -> None:
    db = await db_part()
    content = content_part()
    report = {"db": db, "content": content}
    (OUT / "b3ca_db_forensic2.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("=== DB gate decisions ===")
    print(json.dumps(db["decisions"], ensure_ascii=False))
    print("\n=== reason kinds ===")
    for k, v in sorted(db["reason_kind"].items(), key=lambda x: -x[1]):
        print(f"  {v:5}  {k}")
    print(f"\ncandidates with answer∩explanation overlap: "
          f"{db['n_candidates_with_answer_explanation_overlap']}")
    print("\n=== content: does declared answer_lines contain 详解 headers? ===")
    hdr = f"{'paper':<6}{'units':>6}{'decl':>6}{'multi':>6}{'multi+hdr':>10}{'single':>7}{'sng+hdr':>8}{'sng_letter':>11}"
    print(hdr)
    for paper, r in content.items():
        print(f"{paper:<6}{r['units']:>6}{r['declared']:>6}{r['multi']:>6}"
              f"{r['range_has_solution_word']:>10}{r['single_declared']:>7}"
              f"{r['single_is_solution']:>8}{r['single_has_letter']:>11}")
    print("\n=== single-line answer_lines samples ===")
    for paper, r in content.items():
        for s in r["samples"][:3]:
            print(f"  [{paper}] {s['unit_id']} {s['answer_lines']}: {s['text']!r}")


asyncio.run(main())
