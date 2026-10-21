"""READ-ONLY PRE-FIX BASELINE SNAPSHOT for Task A.

Must be taken BEFORE the resolver is modified; it cannot be reconstructed
afterwards. Captures, for all 9 papers / 284 questions:
  - pinned code identity (HEAD sha + resolver.py / match_normalization.py sha256)
  - per question: unit_id / leaf_id / leaf_present / ir_status / gate / labels
  - per option: label, text_raw, span_id, line_refs, text_length
  - summary counts (bare / swallow / gate histogram) for delta comparison

Output is written to the E2E_ACCEPTANCE evidence area as a NEW file; nothing
existing is touched.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
OUTDIR = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

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

import re
LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_head(repo: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as e:
        return f"<err {e}>"


def main() -> None:
    snap = {
        "purpose": "PRE-FIX baseline snapshot for Task A (resolver single-line multi-option)",
        "taken_at": datetime.now(timezone.utc).isoformat(),
        "code_identity": {
            "AITutors_v3_HEAD": git_head(Path(r"D:\Project\AITutors-v3")),
            "Papers_HEAD": git_head(Path(r"D:\Project\Papers")),
            "resolver.py_sha256": sha(BACKEND / "app/domains/resolver/resolver.py"),
            "match_normalization.py_sha256": sha(BACKEND / "app/domains/resolver/match_normalization.py"),
        },
        "subjects": {},
    }

    total_opts = bare_total = swallow_total = 0
    gate_all = Counter()

    for man_p in sorted((EA / "04_V3_INPUT").glob("*.manifest.json")):
        subj = man_p.stem
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
        spanmap = {s.span_id: s for s in run.resolved_spans}
        compiled = Compiler(spanmap, {v.line_ref: v for v in views}).compile(ir)

        qs = []
        for root in ir.units:
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            for leaf in leaves:
                cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
                rec = {
                    "unit_id": root.unit_id, "leaf_id": leaf.unit_id,
                    "leaf_present": cl is not None,
                    "ir_status": root.semantic_status,
                    "gate": gate["decision"],
                }
                if cl is None:
                    rec["labels"] = []
                    rec["options"] = []
                    qs.append(rec)
                    continue
                opts = []
                for o in cl.options:
                    t = o.text
                    lab = str(o.label)
                    bare = t.strip().upper() == lab.upper()
                    sw = len({x.group(1).upper() for x in LAB.finditer(t)}) >= 2
                    opts.append({
                        "label": lab, "text_raw": t, "len": len(t.strip()),
                        "span_id": o.span_id,
                        "line_refs": list(getattr(o, "line_refs", ()) or ()),
                        "bare": bare, "swallow": sw,
                    })
                    total_opts += 1
                    bare_total += int(bare)
                    swallow_total += int(sw)
                rec["labels"] = [x["label"] for x in opts]
                rec["options"] = opts
                qs.append(rec)
            gate_all[gate["decision"]] += 1

        snap["subjects"][subj] = {"manifest": man_p.name, "md": md_p.name, "questions": qs}

    snap["summary"] = {
        "total_options": total_opts,
        "bare_options": bare_total,
        "swallow_options": swallow_total,
        "gate_histogram_units": dict(gate_all),
    }

    out = OUTDIR / "_TASKA_PREFIX_BASELINE.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 88)
    print("PRE-FIX BASELINE SNAPSHOT (Task A)")
    print("=" * 88)
    print("   code identity:")
    for k, v in snap["code_identity"].items():
        print(f"      {k:<32}{str(v)[:56]}")
    print(f"\n   subjects      : {len(snap['subjects'])}")
    print(f"   total options : {total_opts}")
    print(f"   bare options  : {bare_total}")
    print(f"   swallow opts  : {swallow_total}")
    print(f"   gate hist     : {dict(gate_all)}")
    print(f"\n   written: {out}")
    print(f"   sha256 : {sha(out)}")


if __name__ == "__main__":
    main()
