"""READ-ONLY verification of MIMO's v2 Gate-Provenance COMPLETE claim.

Checks that can falsify the claim:
  1. v2 exists AND the frozen baseline is byte-identical (no overwrite)
  2. field layering actually exists (leaf_present / ir_status / gate_original /
     gate_original_source / gate_replay / gate_display / reason_display)
  3. C2/C5/C6 counts are really 0 (no synthetic originals)
  4. for gate_original non-null entries, the decision MATCHES DSH's independent
     replay -> that is the falsification test for "fabricated original decision"
  5. RAW fields (stem/options/answer/labels) identical to FROZEN
"""
from __future__ import annotations

import hashlib
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


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def loadjs(p: Path):
    s = p.read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def replay_decisions(man_p: Path, md_p: Path):
    """unit_id -> (has_leaf, semantic_status, decision)"""
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
    out = {}
    for root in ir.units:
        leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
        for leaf in leaves:
            cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
            gd = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            out[leaf.unit_id] = (cl is not None, root.semantic_status, gd["decision"],
                                 root.unit_id)
    return out


def main() -> None:
    v2 = loadjs(EA / "data_v2.js")
    frozen = json.loads((EA / "FROZEN_EVIDENCE" / "viewer_data_raw.json").read_text(encoding="utf-8"))

    print("=" * 96)
    print("1. frozen baseline untouched?")
    print("=" * 96)
    a = sha(EA / "viewer_data_raw.json")
    b = sha(EA / "FROZEN_EVIDENCE" / "viewer_data_raw.json")
    print(f"   live  sha {a[:20]}\n   frozen sha {b[:20]}\n   identical={a == b}")

    print("\n" + "=" * 96)
    print("2. field layering present?")
    print("=" * 96)
    keys = set()
    for qs in ({k: v.get("questions") or [] for k, v in v2["subjects"].items()}).values():
        for q in qs:
            keys |= set(q.keys())
    want = ["leaf_present", "ir_status", "gate_original", "gate_original_source",
            "gate_replay", "gate_display", "reason_display", "gate_reasons_original"]
    for w in want:
        print(f"   {w:<26} present={w in keys}")

    print("\n" + "=" * 96)
    print("3. C1..C6 counts (independent)")
    print("=" * 96)
    C = Counter()
    mism = []
    rawdiff = []
    fz = {k: {str(q.get("unit_id")): q for q in (v.get("questions") or [])}
          for k, v in frozen["subjects"].items()}

    for subj, entry in v2["subjects"].items():
        man_p = EA / "04_V3_INPUT" / f"{subj}.manifest.json"
        md = json.loads(man_p.read_text(encoding="utf-8"))
        md_p = Path(str(md.get("source_file", "")))
        rep = replay_decisions(man_p, md_p)
        for q in (entry.get("questions") or []):
            uid = str(q.get("unit_id"))
            has_leaf = bool(q.get("leaf_present"))
            go = q.get("gate_original")
            gr = q.get("gate_replay")
            gd = q.get("gate_display")
            src = q.get("gate_original_source")
            if has_leaf and go is not None:
                C["C1_leaf+orig"] += 1
            if (not has_leaf) and go is not None:
                C["C2_noleaf+orig"] += 1
            if (not has_leaf) and go is None:
                C["C3_noleaf+no_orig"] += 1
            r = rep.get(str(q.get("leaf_id") or uid))
            if r is None:
                C["C4_not_compared(no replay key)"] += 1
            if r:
                r_leaf, r_status, r_dec, r_root = r
                if go is not None:
                    if str(go) == str(r_dec):
                        C["C4_replay_match"] += 1
                    else:
                        C["C5_replay_mismatch"] += 1
                        mism.append((subj, uid, go, r_dec))
                # falsification: gate_original must be null exactly when the runner skipped
                if has_leaf != r_leaf:
                    mism.append((subj, uid, f"leaf_present v2={has_leaf} replay={r_leaf}", ""))
                # gate_display must never invent a decision for no-original
                if go is None and gd in ("rejected", "approved", "auto_approve", "pending_review"):
                    mism.append((subj, uid, f"gate_display invented: {gd}", ""))
            # RAW parity vs frozen
            f = fz.get(subj, {}).get(uid)
            if f:
                for k2 in ("stem_raw", "answer_raw", "labels"):
                    if q.get(k2) != f.get(k2):
                        rawdiff.append((subj, uid, k2))
                fo = [(o.get("label"), o.get("text_raw")) for o in (f.get("options_raw") or [])]
                vo = [(o.get("label"), o.get("text_raw")) for o in (q.get("options_raw") or [])]
                if fo != vo:
                    rawdiff.append((subj, uid, "options_raw"))

    for k in sorted(C):
        print(f"   {k:<22}{C[k]}")
    print(f"\n   mismatches / invented decisions : {len(mism)}")
    for m in mism[:12]:
        print(f"      {m}")
    print(f"   RAW field differences vs FROZEN : {len(rawdiff)}")
    for d in rawdiff[:12]:
        print(f"      {d}")

    # source label histogram
    srcc = Counter()
    for entry in v2["subjects"].values():
        for q in (entry.get("questions") or []):
            srcc[str(q.get("gate_original_source"))] += 1
    print(f"\n   gate_original_source histogram: {dict(srcc)}")


if __name__ == "__main__":
    main()
