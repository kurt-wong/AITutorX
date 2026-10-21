"""Read-only: print the ACTUAL compiled answer text for pending units.

Decides whether 'answer not expressible as canonical value' is
  (a) a DATA gap  -> evidence chain missing the answer, or
  (b) a GRAMMAR gap -> answer present but rejected by the strict-auto whitelist.
"""
from __future__ import annotations

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
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.grammar import verify  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import (  # noqa: E402
    find_manifests,
    load_manifest,
)
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

WANT = {"化学": 6, "历史": 3, "地理": 3, "生物": 4}
shown = Counter()
rows = []

for p in find_manifests(CORPUS):
    paper = p.parent.name
    if paper not in WANT:
        continue
    m = load_manifest(p)
    srs = load_source_lines(Path(m.source_file))
    texts = [s.text for s in srs]
    views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                 page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                  for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
    svid, aid = uuid.uuid4(), uuid.uuid4()
    run = SourceResolver(source_version_id=svid, lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, svid, aid)
    compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                        {l.line_ref: l for l in srs}).compile(ir)

    print(f"\n===== {paper} =====")
    for leaf in compiled.leaves:
        if shown[paper] >= WANT[paper]:
            break
        ans = leaf.answer
        txt = ans.text if ans else None
        labels = tuple(str(o.label) for o in leaf.options if o.label)
        verdict = verify(leaf.canonical_question_type, txt or "", labels)
        if verdict is True:
            continue
        shown[paper] += 1
        print(f"  {leaf.unit_id:<12} qtype={leaf.canonical_question_type:<14} "
              f"verify={verdict!r}")
        print(f"      answer.text = {txt!r}")
        print(f"      source_located={getattr(ans, 'source_located', None)} "
              f"complete={getattr(ans, 'complete', None)}")
        print(f"      options={labels}")
        rows.append({"paper": paper, "unit": leaf.unit_id,
                     "qtype": leaf.canonical_question_type,
                     "answer_text": txt, "verify": str(verdict),
                     "labels": list(labels)})

(OUT / "answer_expressibility_samples.json").write_text(
    __import__("json").dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nwritten: {OUT / 'answer_expressibility_samples.json'}")
