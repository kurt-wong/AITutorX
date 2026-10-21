"""Task A before/after snapshot — content intervals + invariants + Q20."""
from __future__ import annotations
import hashlib, json, os, sys, uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
sys.path.insert(0, str(BACKEND))
for line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler
from app.domains.compile.ir import IRBuilder
from app.domains.gate.policy import evaluate
from app.domains.resolver.resolver import SourceResolver
from app.domains.resolver.span import SourceLineView
from scripts.preprocessing_consumer.annotation_adapter import (
    attach_material_boundary_markers, manifest_to_annotation_payload)
from scripts.preprocessing_consumer.manifest_reader import load_manifest
from scripts.preprocessing_consumer.source_loader import load_source_lines

SUBJECTS = ["数学","物理","化学","英语","语文","政治","地理","历史","生物"]

def measure(man_path, md_path):
    m = load_manifest(man_path)
    srs = load_source_lines(md_path)
    views = tuple(SourceLineView(s.line_ref, s.text, s.seq, s.page_no, s.line_no_in_page) for s in srs)
    payload = manifest_to_annotation_payload(m)
    payload = attach_material_boundary_markers(
        payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines},
        [s.text for s in srs])
    run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
    ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {v.line_ref: v for v in views}
    compiled = Compiler(span_map, line_map).compile(ir)

    n_ready = sum(1 for u in ir.units if u.semantic_status == "ready")
    n_incomplete = sum(1 for u in ir.units if u.semantic_status != "ready")
    n_leaves = len(compiled.leaves)
    gate = Counter()
    rejected = 0
    labels_bad = []
    q20_opts = None
    samples = {}

    for root in ir.units:
        if root.semantic_status != "ready":
            continue
        try:
            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            gate[d.get("decision") or "?"] += 1
            if d.get("decision") == "rejected":
                rejected += 1
        except Exception:
            gate["error"] += 1

    for leaf in compiled.leaves:
        labs = [o.label for o in leaf.options]
        if not set(labs) <= {"A", "B", "C", "D"}:
            labels_bad.append((leaf.unit_id, labs))
        if leaf.unit_id == "Q20" or leaf.unit_id.endswith("Q20"):
            q20_opts = [(o.label, o.text) for o in leaf.options]
        if leaf.unit_id in ("Q1", "Q4", "Q17", "Q7"):
            samples[leaf.unit_id] = [(o.label, o.text) for o in leaf.options]

    return {
        "root": len(ir.units),
        "ready": n_ready,
        "incomplete": n_incomplete,
        "leaves": n_leaves,
        "gate": dict(gate),
        "rejected_root_scope": rejected,
        "labels_out_of_range": labels_bad,
        "q20_options": q20_opts,
        "samples": samples,
    }

def main():
    after = {}
    for subj in SUBJECTS:
        man = OUT / "04_V3_INPUT" / f"{subj}.manifest.json"
        md_p = None
        v2 = json.loads((OUT / "viewer_data_raw_v2.json").read_text(encoding="utf-8"))
        md_sha = ((v2["subjects"].get(subj) or {}).get("hashes") or {}).get("md")
        for p in (OUT / "02_PREPROCESSING_OUTPUT").glob("*.md"):
            if md_sha and hashlib.sha256(p.read_bytes()).hexdigest() == md_sha:
                md_p = p
                break
        if not man.exists() or not md_p:
            print(subj, "MISSING")
            continue
        r = measure(man, md_p)
        after[subj] = r
        print(subj, "ready", r["ready"], "inc", r["incomplete"], "leaves", r["leaves"],
              "gate", r["gate"], "bad_labels", r["labels_out_of_range"])
        if r["q20_options"] is not None:
            print("  Q20 n_opts", len(r["q20_options"]), [(x[0], (x[1] or "")[:20]) for x in r["q20_options"]])

    # load frozen v2 for before comparison
    before = {}
    v2 = json.loads((OUT / "viewer_data_raw_v2.json").read_text(encoding="utf-8"))
    for subj, e in v2["subjects"].items():
        qs = e.get("questions") or []
        before[subj] = {
            "n_questions": len(qs),
            "gate_display_counts": e.get("gate_display_counts"),
            "option_anomaly_count": e.get("option_anomaly_count"),
        }

    report = {
        "task": "A before/after content-span snapshot",
        "invariants_target": {
            "root": 284,
            "ready": 227,
            "incomplete": 57,
            "rejected_root_scope": 62,
            "D29": "decomposition surface unchanged (separate)",
        },
        "after_measure": after,
        "before_from_v2": before,
        "checks": {
            "total_root": sum(r["root"] for r in after.values()),
            "total_ready": sum(r["ready"] for r in after.values()),
            "total_incomplete": sum(r["incomplete"] for r in after.values()),
            "total_leaves": sum(r["leaves"] for r in after.values()),
            "total_rejected": sum(r["rejected_root_scope"] for r in after.values()),
            "labels_out_of_range_all": [x for r in after.values() for x in r["labels_out_of_range"]],
            "q20_n_opts": (after.get("化学") or {}).get("q20_options") and len(after["化学"]["q20_options"]),
        },
    }
    print()
    print("TOTALS", report["checks"]["total_root"], report["checks"]["total_ready"],
          report["checks"]["total_incomplete"], "rejected", report["checks"]["total_rejected"])
    print("labels out of range", report["checks"]["labels_out_of_range_all"])
    print("Q20 n_opts", report["checks"]["q20_n_opts"])
    (OUT / "TASK_A_AFTER_SNAPSHOT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote TASK_A_AFTER_SNAPSHOT.json")

if __name__ == "__main__":
    main()
