"""READ-ONLY Task A verification: post-fix pipeline vs PRE-FIX baseline snapshot.

Mechanical, field-level. Answers:
  1. Do math Q1 / math Q4 now carry correct content spans?
  2. Are labels now within A-D (except the two out-of-scope cases Q17.H / Q20.E)?
  3. Do the P1 invariants hold (root/ready/incomplete/gate histogram)?
  4. Did anything change that Task A should NOT have changed?
     (Q17 labels, Q20 n_options, any unrelated question's text)
  5. How large is the unintended-change surface?
"""
from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter
from pathlib import Path

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
BASE = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_PREFIX_BASELINE.json")

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

LAB = re.compile(r"(?<![A-Za-z0-9_])(?:\d)?([A-Ha-h])\s*[.．、:：,，。)）]")


def run_now():
    out = {}
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
        compiled = Compiler({s.span_id: s for s in run.resolved_spans},
                            {v.line_ref: v for v in views}).compile(ir)
        qs = {}
        for root in ir.units:
            gate = gate_evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            for leaf in leaves:
                cl = next((l for l in compiled.leaves if l.unit_id == leaf.unit_id), None)
                if cl is None:
                    qs[str(root.unit_id)] = {"gate": gate["decision"], "labels": [], "options": []}
                    continue
                opts = [{"label": str(o.label), "text_raw": o.text,
                         "bare": o.text.strip().upper() == str(o.label).upper(),
                         "swallow": len({x.group(1).upper()
                                         for x in LAB.finditer(o.text)}) >= 2}
                        for o in cl.options]
                qs[str(root.unit_id)] = {"gate": gate["decision"],
                                         "labels": [o["label"] for o in opts],
                                         "options": opts}
        out[subj] = qs
    return out


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    now = run_now()
    # key normalisation: manifest stems are "<subj>.manifest"; strip the suffix
    now = {k.replace(".manifest", ""): v for k, v in now.items()}
    base = {**base, "subjects": {k.replace(".manifest", ""): v
                                 for k, v in base["subjects"].items()}}

    print("=" * 96)
    print("1. TARGETED ASSERTIONS")
    print("=" * 96)
    def show(subj, uid):
        q = now[subj].get(uid)
        if not q:
            print(f"   {subj} {uid}: MISSING")
            return
        print(f"   {subj} {uid}: gate={q['gate']} labels={q['labels']}")
        for o in q["options"]:
            flag = "  <<< BARE" if o["bare"] else ("  <<< SWALLOW" if o["swallow"] else "")
            print(f"      {o['label']}: {o['text_raw'].strip()[:60]!r}{flag}")
    for subj, uid in (("数学", "Q1"), ("数学", "Q4"), ("化学", "Q17"), ("化学", "Q20")):
        show(subj, uid)

    print("\n" + "=" * 96)
    print("2. labels ⊆ {A,B,C,D} ? (exceptions allowed: Q17.H, Q20.E)")
    print("=" * 96)
    bad = []
    for subj, qs in now.items():
        for uid, q in qs.items():
            labs = q["labels"]
            if len(set(labs)) != len(labs):
                bad.append((subj, uid, "DUPLICATE", labs))
            extra = [x for x in labs if x not in ("A", "B", "C", "D")]
            if extra and not ((subj, uid) in (("化学", "Q17"), ("化学", "Q20"))):
                bad.append((subj, uid, "EXTRA_LABEL", labs))
    print(f"   violations: {len(bad)}")
    for b in bad[:12]:
        print(f"      {b}")

    print("\n" + "=" * 96)
    print("3. P1 INVARIANTS  baseline -> now")
    print("=" * 96)
    def hist(d):
        c = Counter()
        for qs in d.values():
            for q in qs.values():
                c[q["gate"]] += 1
        return c
    base_gate = {s: {str(x["unit_id"]): {"gate": x["gate"]}
                     for x in base["subjects"][s]["questions"]}
                 for s in base["subjects"]}
    hb, hn = hist(base_gate), hist(now)
    print(f"   baseline gate hist : {dict(hb)}  total={sum(hb.values())}")
    print(f"   now      gate hist : {dict(hn)}  total={sum(hn.values())}")

    # option counts
    def counts(d):
        tot = bare = sw = 0
        for qs in d.values():
            for q in qs.values():
                for o in q["options"]:
                    tot += 1
                    bare += int(o["bare"])
                    sw += int(o["swallow"])
        return tot, bare, sw
    print(f"   baseline options   : total={base['summary']['total_options']} "
          f"bare={base['summary']['bare_options']} swallow={base['summary']['swallow_options']}")
    print(f"   now      options   : total={counts(now)[0]} bare={counts(now)[1]} swallow={counts(now)[2]}")

    print("\n" + "=" * 96)
    print("4. UNINTENDED-CHANGE SURFACE (per question, text-level)")
    print("=" * 96)
    base_q = {s: {str(x["unit_id"]): x for x in base["subjects"][s]["questions"]}
              for s in base["subjects"]}
    changed, unchanged = [], 0
    for subj, qs in now.items():
        for uid, q in qs.items():
            b = base_q.get(subj, {}).get(uid)
            if b is None:
                continue
            bo = [(o["label"], o["text_raw"]) for o in (b.get("options") or [])]
            no = [(o["label"], o["text_raw"]) for o in q["options"]]
            if bo != no or b.get("gate") != q["gate"]:
                changed.append((subj, uid, len(bo), len(no)))
            else:
                unchanged += 1
    print(f"   questions with ANY change : {len(changed)}")
    print(f"   questions unchanged       : {unchanged}")
    print(f"   (affected set was 97; expect changed ~97 + Q17/Q20 untouched)")
    outside = [c for c in changed if c[1] in ("Q17", "Q20")]
    print(f"   Q17/Q20 changed?          : {outside if outside else 'NO (correct)'}")

    out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2\_TASKA_POSTFIX_RESULT.json")
    out.write_text(json.dumps({"now": now, "changed": changed}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\n   written: {out}")


if __name__ == "__main__":
    main()
