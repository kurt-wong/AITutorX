"""P0 read-only impact recompute.

Simulates: role_region overlap no longer sets auto_allowed=False and no longer
emits role_provenance_violations as auto_blockers (diagnostic reasons stay).

Zero code change. Outputs p0_impact_recompute.json.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\PHASE1-E2E-REPLAY")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate import STRICT_AUTO_TYPES  # noqa: E402
from app.domains.gate.grammar import verify  # noqa: E402
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

_AUTO_RES = frozenset({"exact", "normalized"})


def classify_auto_blockers(root, ir, compiled, resolved_run, *, drop_role_region: bool):
    """Recompute auto_blockers with the same rules as policy.evaluate().

    drop_role_region=True is the P0 simulation (A).
    Returns (decision, blockers, meta).
    """
    resolved = {s.span_id: s for s in resolved_run.resolved_spans}
    # partition like policy
    from app.domains.gate.policy import partition_candidate

    leaves, materials = partition_candidate(root, compiled)

    # --- byte-proven (auto_allowed) EXCLUDING role_region ---
    auto_allowed = True
    for leaf in leaves:
        spans = []
        if leaf.stem:
            spans.append(leaf.stem.span_id)
        spans += [o.span_id for o in leaf.options]
        if leaf.explanation:
            spans.append(leaf.explanation.span_id)
        if leaf.answer:
            spans.append(leaf.answer.span_id)
        for sid in spans:
            sp = resolved.get(sid)
            if sp is None or sp.resolution_status not in _AUTO_RES:
                auto_allowed = False
    for m in materials:
        sp = resolved.get(m.span_id)
        if sp is None or sp.resolution_status not in _AUTO_RES:
            auto_allowed = False

    # --- role_region detection ---
    role_region_hits = []
    if resolved_run.structural_regions:
        region_by_role = {}
        for reg in resolved_run.structural_regions:
            region_by_role.setdefault(reg.role, set()).update(reg.line_refs)
        for leaf in leaves:
            if leaf.answer is None:
                continue
            ans_span = resolved.get(leaf.answer.span_id)
            if ans_span is None:
                continue
            ans_lines = set(ans_span.line_refs)
            for bad_role in ("explanation", "question"):
                overlap = ans_lines & region_by_role.get(bad_role, set())
                if overlap:
                    role_region_hits.append({
                        "leaf": leaf.unit_id,
                        "bad_role": bad_role,
                        "n_lines": len(overlap),
                    })

    # --- other auto_blockers ---
    blockers = []
    if not auto_allowed:
        blockers.append("not byte-proven (resolution not in {exact, normalized})")
    if not drop_role_region:
        for h in role_region_hits:
            blockers.append(
                f"role_region:{h['bad_role']}:{h['leaf']}"
            )
    for leaf in leaves:
        if leaf.canonical_question_type not in STRICT_AUTO_TYPES:
            blockers.append(f"not strict-auto:{leaf.canonical_question_type}")
        else:
            if leaf.answer is None or not leaf.answer.text:
                blockers.append(f"answer grammar:no answer text:{leaf.unit_id}")
            else:
                labels = tuple(str(o.label) for o in leaf.options if o.label)
                r = verify(leaf.canonical_question_type, leaf.answer.text, labels)
                if r is not True:
                    blockers.append(f"answer grammar:not expressible:{leaf.unit_id}")
        if leaf.answer is None or not leaf.answer.source_located or not leaf.answer.complete:
            blockers.append(f"answer not source_located+complete:{leaf.unit_id}")

    # structural/semantic fail → rejected (unchanged by P0)
    # we trust evaluate() for that; if evaluate says rejected, keep rejected
    decision = "pending_review" if blockers else "auto_approve"
    return decision, blockers, {
        "auto_allowed": auto_allowed,
        "role_region_hits": role_region_hits,
    }


def main() -> None:
    rows = []
    cur_c = Counter()
    sim_c = Counter()
    flip = []

    for p in find_manifests(CORPUS):
        m = load_manifest(p)
        srs = load_source_lines(Path(m.source_file))
        texts = [s.text for s in srs]
        views = tuple(
            SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                           page_no=s.page_no, line_no_in_page=s.line_no_in_page)
            for s in srs
        )
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts
        )
        sv_id = uuid.uuid4()
        run = SourceResolver(source_version_id=sv_id, lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, sv_id, uuid.uuid4())
        span_map = {s.span_id: s for s in run.resolved_spans}
        line_map = {v.line_ref: v for v in views}
        compiled = Compiler(span_map, line_map).compile(ir)

        for root in ir.units:
            if root.semantic_status != "ready":
                cur_c["ir_incomplete"] += 1
                sim_c["ir_incomplete"] += 1
                continue
            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            cur = d.get("decision") or "?"
            cur_c[cur] += 1

            # rejected stays rejected (structural/semantic/hash) — P0 does not touch
            if cur == "rejected":
                sim_c["rejected"] += 1
                rows.append({
                    "paper": p.parent.name, "root": root.unit_id,
                    "current": cur, "p0": cur, "flipped": False,
                    "role_region": 0,
                })
                continue

            sim_dec, blockers, meta = classify_auto_blockers(
                root, ir, compiled, run, drop_role_region=True
            )
            # sanity: without drop, should match current pending/auto
            chk_dec, chk_blockers, _ = classify_auto_blockers(
                root, ir, compiled, run, drop_role_region=False
            )
            # if chk_dec != cur, note mismatch (algorithm drift)
            sim_c[sim_dec] += 1
            flipped = cur != sim_dec
            if flipped:
                flip.append({
                    "paper": p.parent.name,
                    "root": root.unit_id,
                    "unit_type": root.unit_type,
                    "current": cur,
                    "p0": sim_dec,
                    "role_region_hits": meta["role_region_hits"],
                    "remaining_blockers_after_p0": blockers,
                    "chk_mismatch": chk_dec != cur,
                })
            rows.append({
                "paper": p.parent.name,
                "root": root.unit_id,
                "unit_type": root.unit_type,
                "current": cur,
                "p0": sim_dec,
                "flipped": flipped,
                "role_region": len(meta["role_region_hits"]),
                "blockers_after_p0": blockers,
                "chk_mismatch": chk_dec != cur,
            })

    mismatches = sum(1 for r in rows if r.get("chk_mismatch"))
    report = {
        "metric_scope": "root",
        "simulation": "P0-A: role_region does not set auto_allowed=False and is not an auto_blocker (diagnostic retained)",
        "current": dict(cur_c),
        "p0_predicted": dict(sim_c),
        "delta": {
            "auto_approve": sim_c.get("auto_approve", 0) - cur_c.get("auto_approve", 0),
            "pending_review": sim_c.get("pending_review", 0) - cur_c.get("pending_review", 0),
            "rejected": sim_c.get("rejected", 0) - cur_c.get("rejected", 0),
        },
        "flipped_to_auto": len(flip),
        "algorithm_mismatches": mismatches,
        "flips": flip,
        "rows": rows,
    }
    out = OUT / "p0_impact_recompute.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("metric_scope=root")
    print("current   ", dict(cur_c))
    print("p0 predict", dict(sim_c))
    print("delta     ", report["delta"])
    print("flipped_to_auto", len(flip), " chk_mismatch", mismatches)
    print("\nflips:")
    for f in flip[:25]:
        print(f"  {f['paper']} {f['root']} {f['unit_type']} "
              f"{f['current']}→{f['p0']} role_region={len(f['role_region_hits'])} "
              f"remain={f['remaining_blockers_after_p0'][:3]}")
    print("wrote", out)


if __name__ == "__main__":
    main()
