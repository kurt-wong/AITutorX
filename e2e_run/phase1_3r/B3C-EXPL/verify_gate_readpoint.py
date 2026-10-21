"""Final check: what does the gate's role-provenance check ACTUALLY read, and
which regions cause the residual 52 violations?

policy.py:204 loops over ("explanation", "question") only -- NOT "answer".
_compute_regions() emits at most ONE region per role (first header only),
with explanation region = (first explanation header, +inf).

So on 数学 (no explanation header) there is NO explanation region and the
answer-region check cannot produce an answer∩explanation violation at all.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests, load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def main() -> None:
    rows = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        region = {r.role: set(r.line_refs) for r in run.structural_regions}
        ans = [s for s in run.resolved_spans if s.role == "answer"]
        expl = [s for s in run.resolved_spans if s.role == "explanation"]

        # the gate's actual check (policy.py:197-215)
        viol_expl = sum(1 for a in ans if set(a.line_refs) & region.get("explanation", set()))
        viol_quest = sum(1 for a in ans if set(a.line_refs) & region.get("question", set()))
        # what the gate does NOT check
        viol_region_answer = sum(1 for a in ans if set(a.line_refs) & region.get("answer", set()))

        rows.append({
            "paper": p.parent.name,
            "answer_spans": len(ans),
            "explanation_spans": len(expl),
            "explanation_region_present": "explanation" in region,
            "explanation_region_n": len(region.get("explanation", ())),
            "question_region_n": len(region.get("question", ())),
            "answer_region_n": len(region.get("answer", ())),
            "gate_viol_answer_in_explanation_region": viol_expl,
            "gate_viol_answer_in_question_region": viol_quest,
            "gate_does_not_check_answer_in_answer_region": viol_region_answer,
        })

    tot = Counter()
    for r in rows:
        tot["gate_viol_answer_in_explanation_region"] += r["gate_viol_answer_in_explanation_region"]
        tot["gate_viol_answer_in_question_region"] += r["gate_viol_answer_in_question_region"]
        tot["answer_spans"] += r["answer_spans"]

    print(f"{'paper':<6}{'ans':>5}{'expl':>6}{'explReg':>9}{'explRegN':>10}"
          f"{'qRegN':>7}{'ansRegN':>9}{'violExpl':>9}{'violQuest':>10}")
    for r in rows:
        print(f"{r['paper']:<6}{r['answer_spans']:>5}{r['explanation_spans']:>6}"
              f"{str(r['explanation_region_present']):>9}{r['explanation_region_n']:>10}"
              f"{r['question_region_n']:>7}{r['answer_region_n']:>9}"
              f"{r['gate_viol_answer_in_explanation_region']:>9}"
              f"{r['gate_viol_answer_in_question_region']:>10}")
    print("\nTOTALS:", json.dumps(dict(tot), ensure_ascii=False))

    (OUT / "gate_readpoint_evidence.json").write_text(
        json.dumps({"rows": rows, "totals": dict(tot)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
