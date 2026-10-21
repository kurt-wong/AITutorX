"""Read-only: authoritative IR blocker breakdown for the 29 table-decoded
IR-incomplete roots (Task E), plus the 6 root-level gap cases.

Instrumentation: the IR validator builds a private `problems` list then discards
it. We replicate exactly the ir.py invariant checks so the named blocker is real
code semantics, not inference. This does NOT modify the repo.
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

from app.domains.compile import content_roles_for, map_canonical_type  # noqa: E402
from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate  # noqa: E402
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


def leaf_problems(s, canon_parent):
    probs = []
    canon = map_canonical_type(s.original_question_type)
    req = content_roles_for(canon)
    by_role = {c.role: c for c in s.content}
    if req.get("stem") == "required":
        c = by_role.get("stem")
        if c is None:
            probs.append("leaf stem not declared")
        elif c.span_id is None:
            probs.append("leaf stem unresolved")
    if req.get("answer") == "required":
        c = by_role.get("answer")
        if c is None:
            probs.append("leaf answer not declared")
        elif c.span_id is None:
            probs.append("leaf answer unresolved")
    if req.get("options") == "required_for_choice":
        if not any(c.role == "option" for c in s.content):
            probs.append("leaf options missing for choice type")
    for c in s.content:
        if c.unsupported:
            probs.append(f"leaf unsupported role {c.role}")
        elif c.span_id is None and c.role not in ("stem", "answer"):
            probs.append(f"leaf role {c.role} unresolved")
    return probs


def root_problems(root):
    probs = []
    if root.unit_type == "composite_unit":
        if not root.shared_components:
            probs.append("composite has no shared component material")
        for sc in root.shared_components:
            if sc.span_id is None:
                probs.append(f"shared component {sc.role} unresolved")
        shared_by_role = {c.role: c for c in root.shared_components}
        for r in root.relations:
            sc = shared_by_role.get(r)
            if sc is None:
                probs.append(f"material_dependency target {r!r} not in shared_components")
            elif sc.span_id is None:
                probs.append(f"material_dependency target {r!r} span unresolved")
        ready = {s.unit_id for s in root.sub_questions if s.semantic_status == "ready"}
        for s in root.sub_questions:
            if s.semantic_status != "ready":
                probs.extend(leaf_problems(s, root.original_question_type))
        if root.sub_questions and not ready:
            pass
    else:
        probs.extend(leaf_problems(root, None))
    return probs


def main() -> None:
    tot = Counter()
    hist = Counter()
    rows = []
    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        paper = p.parent.name
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
        tbl = {s.span_id[3:].rsplit(".answer", 1)[0]
               for s in run.resolved_spans
               if "structured_answer_table" in " ".join(s.evidence or ())}
        auto = set()
        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if g.get("decision") == "auto_approve":
                auto.add(root.unit_id)

        for owner in tbl:
            rid = owner[:-4] if owner.endswith(".sub") else owner
            if rid in auto:
                continue
            node = next((u for u in ir.units if u.unit_id == rid), None)
            if node is None or node.semantic_status == "ready":
                continue
            probs = root_problems(node) or ["(no named invariant fired)"]
            for pr in probs:
                hist[pr] += 1
            tot["roots"] += 1
            if any("option" in x for x in probs):
                tot["has_option_blocker"] += 1
            if any("stem" in x for x in probs):
                tot["has_stem_blocker"] += 1
            rows.append({"paper": paper, "root": rid, "problems": probs})

    print("IR-incomplete table-decoded roots:", tot.get("roots"))
    print("with option blocker:", tot.get("has_option_blocker"),
          " with stem blocker:", tot.get("has_stem_blocker"))
    print("\nblocker histogram:")
    for k, v in hist.most_common():
        print(f"   {v:>4}  {k}")
    print("\nper-root detail (first 15):")
    for r in rows[:15]:
        print(f"   {r['paper']}/{r['root']}: {r['problems']}")

    (OUT / "verify_task_e_census.json").write_text(
        __import__("json").dumps({"totals": dict(tot), "histogram": dict(hist),
                                  "rows": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nwritten: {OUT / 'verify_task_e_census.json'}")


if __name__ == "__main__":
    main()
