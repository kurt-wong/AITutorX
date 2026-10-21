"""READ-ONLY: why did the C4 (replay-match) count come out 176 instead of 227?

Diagnose the 51 C1 units whose gate_original did NOT equal my replayed decision,
and check whether that is (a) a real mismatch, (b) my keying/root-vs-leaf error.
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile.ir import IRBuilder  # noqa: E402
from app.domains.gate.policy import evaluate as gate_evaluate  # noqa: E402
from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402
from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers, manifest_to_annotation_payload)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402


def loadjs(p: Path):
    s = p.read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def main() -> None:
    v2 = loadjs(EA / "data_v2.js")
    unmatched = []
    for subj, entry in v2["subjects"].items():
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        md = json.loads(man_p.read_text(encoding="utf-8"))
        md_p = Path(str(md.get("source_file", "")))
        m = load_manifest(man_p)
        srs = load_source_lines(md_p)
        texts = [s.text for s in srs]
        views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                                     page_no=s.page_no, line_no_in_page=s.line_no_in_page)
                      for s in srs)
        payload = manifest_to_annotation_payload(m)
        payload = attach_material_boundary_markers(
            payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
        run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)
        ir = IRBuilder.build(run, payload, uuid.uuid4(), uuid.uuid4())
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)

        by_leaf = {}
        by_root = {}
        for root in ir.units:
            gd = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            by_root[root.unit_id] = gd["decision"]
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            for leaf in leaves:
                by_leaf[leaf.unit_id] = gd["decision"]

        for q in (entry.get("questions") or []):
            go = q.get("gate_original")
            if go is None:
                continue
            uid = str(q.get("unit_id"))
            lid = str(q.get("leaf_id") or uid)
            d_leaf = by_leaf.get(lid)
            d_root = by_root.get(uid)
            if str(go) != str(d_leaf):
                unmatched.append({
                    "subj": subj, "unit_id": uid, "leaf_id": lid,
                    "gate_original": go, "replay_by_leaf": d_leaf, "replay_by_root": d_root,
                    "root_unit_type": next((r.unit_type for r in ir.units if r.unit_id == uid), None),
                    "note": q.get("gate_original_source"),
                })

    print("=" * 96)
    print(f"C1 units whose gate_original != replay(leaf): {len(unmatched)}")
    print("=" * 96)
    cat = Counter()
    for u in unmatched:
        if u["replay_by_leaf"] is None and u["replay_by_root"] is not None:
            cat["leaf_id not in replay (keying)"] += 1
        elif str(u["gate_original"]) == str(u["replay_by_root"]):
            cat["matches REPLAY BY ROOT (keying difference)"] += 1
        else:
            cat["REAL mismatch"] += 1
    print("   diagnosis:", dict(cat))
    for u in unmatched[:12]:
        print(f"   {u['subj']}/{u['unit_id']} leaf={u['leaf_id']} type={u['root_unit_type']}")
        print(f"      gate_original={u['gate_original']}  replay_leaf={u['replay_by_leaf']}"
              f"  replay_root={u['replay_by_root']}  src={u['note']}")
    print(f"\n   by subject: {dict(Counter(u['subj'] for u in unmatched))}")


if __name__ == "__main__":
    main()
