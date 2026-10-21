"""Read-only: exact identity -> option causal chain for 地理, per unit.

Owner requires the 17 `option incomplete` to be split by mechanism, not lumped.
Also confirms that V3 never consumes printed_number (the Producer identity
evidence that would be needed for U51-55).
"""
from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
ROOT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考")
MAN = ROOT / "地理" / "2018北京春季高中会考地理（教师版）(1).manifest.json"
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\B3C-EXPL")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        k, v = _line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from app.domains.resolver.resolver import SourceResolver  # noqa: E402
from app.domains.resolver.span import SourceLineView  # noqa: E402

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    attach_material_boundary_markers,
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.source_loader import load_source_lines  # noqa: E402

m = load_manifest(MAN)
srs = load_source_lines(Path(m.source_file))
texts = [s.text for s in srs]
views = tuple(SourceLineView(line_ref=s.line_ref, text=s.text, seq=s.seq,
                             page_no=s.page_no, line_no_in_page=s.line_no_in_page)
              for s in srs)
payload = manifest_to_annotation_payload(m)
payload = attach_material_boundary_markers(
    payload, {u.unit_id: u.material_lines for u in m.units if u.material_lines}, texts)
run = SourceResolver(source_version_id=uuid.uuid4(), lines=views).resolve(payload)

# unresolved option refs keyed by unit
# reference_id shape: <unit>.option.<label>          e.g. U1-2.sub.option.A
unres_opt = Counter()
for u in run.unresolved_references:
    if u.role != "option":
        continue
    uid = u.reference_id.split(".option.")[0]
    unres_opt[uid] += 1

# resolved span_id shape: sp-<unit>.option.<label>    e.g. sp-U6-7.sub.option.A
opt_resolved = Counter()
for s in run.resolved_spans:
    if s.role == "option":
        uid = s.span_id[3:].split(".option.")[0]
        opt_resolved[uid] += 1

stem_ok = {s.span_id[3:-5] for s in run.resolved_spans
           if s.role == "stem" and s.span_id.endswith(".stem")}

# classify each unit
rows = []
for u in m.units:
    if u.original_question_type not in {"single_choice", "multiple_choice", "true_false"}:
        continue
    sub = f"{u.unit_id}.sub"
    declared = len(u.options or [])
    res = opt_resolved.get(sub, 0)
    unr = unres_opt.get(sub, 0)
    if res == declared:
        cls = "all options resolved"
    elif sub not in stem_ok:
        cls = "BLOCKED: start_ref not established (identity)"
    else:
        cls = "unresolved despite start_ref (separate mechanism)"
    rows.append({"unit": u.unit_id, "qn": list(u.question_numbers),
                 "declared": declared, "resolved": res, "unresolved": unr,
                 "stem_ok": sub in stem_ok, "class": cls})

print(f"{'unit':<10}{'qn':<18}{'decl':>5}{'res':>5}{'unres':>6}  stem  class")
for r in rows:
    print(f"{r['unit']:<10}{str(r['qn']):<18}{r['declared']:>5}{r['resolved']:>5}"
          f"{r['unresolved']:>6}  {'Y' if r['stem_ok'] else 'N':<5} {r['class']}")

agg = Counter(r["class"] for r in rows)
print("\nclass totals:", dict(agg))
print("total option unresolved:", sum(r["unresolved"] for r in rows))
print("total option resolved  :", sum(r["resolved"] for r in rows))

print("\n=== does V3 consume printed_number? ===")
import subprocess
out = subprocess.run(
    ["git", "grep", "-n", "printed_number", "--", "backend/app", "backend/scripts"],
    cwd=r"D:\Project\AITutors-v3", capture_output=True, text=True)
print(out.stdout or "(no matches in app/ or scripts/ other than manifest_reader)")

(OUT / "identity_option_causal.json").write_text(
    json.dumps({"rows": rows, "class_totals": dict(agg)}, ensure_ascii=False, indent=2),
    encoding="utf-8")
print(f"\nwritten: {OUT / 'identity_option_causal.json'}")
