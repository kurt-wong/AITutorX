"""Contract-first reclassification of answer_not_expressible 36.

Level-1 first_failed_contract (Owner taxonomy):
  N0 no answer text
  S0 span/provenance invalid (or interval not carrying a canonical token)
  Q0 qtype not strict-auto
  G1 answer form cannot parse
  G2 answer parsed but not in option labels
  G3 canonical grammar unsupported
  I0 invariant violation

Read-only. No code change.
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
from app.domains.compile import map_canonical_type  # noqa: E402
from app.domains.gate import STRICT_AUTO_TYPES  # noqa: E402
from app.domains.gate.grammar import verify, _clean_answer, _SC_FORMS_RE  # noqa: E402
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

_MULTILINE_BLOCK = "multi-line block (no token extraction)"


def first_failed_contract(*, has_text, span, canonical, labels, text, verify_ret) -> tuple[str, str]:
    """Return (code, detail) — first failing contract in the chain."""
    # N0
    if not has_text:
        return "N0", "answer text empty after compile (verify not reached)"
    # S0 — span/provenance, OR interval not carrying a canonical token
    if span is None:
        return "S0", "answer span_id not in ResolvedRun"
    if span.resolution_status not in {"exact", "normalized"}:
        return "S0", f"span resolution_status={span.resolution_status} not byte-proven"
    ev = tuple(span.evidence or ())
    if _MULTILINE_BLOCK in ev:
        return (
            "S0",
            "answer_lines interval is a multi-line block without token extraction "
            "(B3c-B multi-line token NOT SPECIFIED); grammar never receives a "
            "canonical answer token — Producer/Resolver interval contract gap",
        )
    # Q0
    if canonical not in STRICT_AUTO_TYPES:
        return "Q0", f"qtype {canonical!r} ∉ STRICT_AUTO_TYPES (capability boundary)"
    # G2 — parsed letter not in labels (empty labels = option evidence missing)
    cleaned = _clean_answer(text)
    m = _SC_FORMS_RE.match(cleaned)
    letter = None
    if m:
        for g in ("bare", "paren_fw", "paren_hw", "marker", "score_fw", "score_hw", "period"):
            val = m.group(g)
            if val:
                letters = [ch for ch in val if ch.isascii() and ch.isalpha()]
                letter = letters[-1].upper() if letters else None
                break
    if letter is not None and labels is not None and letter not in labels:
        return (
            "G2",
            f"parsed letter {letter!r} not in resolved_option_labels={labels} "
            f"(option evidence contract)",
        )
    if verify_ret is None and not labels:
        return "G2", f"verify()=None with empty labels; text={text!r} parses but no options"
    # G3 — form not in whitelist (coverage gap) vs G1 — unparseable prefix
    if verify_ret is None or verify_ret is False:
        # escaped-dot / lead qn not stripped → G1 parser compatibility
        if re.match(r"^\d{1,3}\\\.", text or "") or re.match(r"^\d{1,3}\\\.", cleaned or ""):
            return "G1", (
                "answer text has Markdown escaped-dot qn prefix (`N\\. X`); "
                "_LEAD_QN_RE does not strip `\\.` — parser compatibility"
            )
        if cleaned and _SC_FORMS_RE.match(cleaned) is None:
            # known trailing-score form?
            if re.match(r"^[A-Za-z][（(]\s*\d+\s*分\s*[)）]", cleaned):
                return "G3", (
                    f"form {cleaned!r} = letter+trailing score; _SC_FORMS_RE covers "
                    f"leading score only — grammar coverage gap"
                )
            return "G1", f"answer form {cleaned[:60]!r} cannot be parsed to a canonical token"
        return "G3", f"parsed form not accepted by verify()={verify_ret!r} — coverage/contract"
    return "I0", f"unexpected verify()={verify_ret!r}"


def main() -> None:
    rows = []
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
        c_by_id = {l.unit_id: l for l in compiled.leaves}

        for root in ir.units:
            if root.semantic_status != "ready":
                continue
            d = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
            if d.get("decision") == "auto_approve":
                continue

            leaves = [root] if root.unit_type != "composite_unit" else list(root.sub_questions)
            for leaf in leaves:
                ans_c = next((c for c in leaf.content if c.role == "answer"), None)
                span = span_map.get(ans_c.span_id) if ans_c and ans_c.span_id else None
                canonical = map_canonical_type(leaf.original_question_type) if leaf.original_question_type else None
                cl = c_by_id.get(leaf.unit_id)
                ans_text = cl.answer.text if cl and cl.answer else None
                labels = tuple(str(o.label) for o in (cl.options if cl else ()))
                has_text = bool(ans_text and str(ans_text).strip())

                # only the 36 = strict-auto type + text present + verify != True
                if canonical not in STRICT_AUTO_TYPES:
                    continue
                if not has_text:
                    continue
                vret = verify(canonical, ans_text, labels)
                if vret is True:
                    continue

                code, detail = first_failed_contract(
                    has_text=has_text, span=span, canonical=canonical,
                    labels=labels, text=ans_text, verify_ret=vret,
                )
                rows.append({
                    "root_id": root.unit_id,
                    "leaf_id": leaf.unit_id,
                    "paper": p.parent.name,
                    "qtype": leaf.original_question_type,
                    "canonical_qtype": canonical,
                    "answer_text": (ans_text or "")[:200],
                    "answer_span": ans_c.span_id if ans_c else None,
                    "span_evidence": list(span.evidence) if span else [],
                    "resolution_status": span.resolution_status if span else None,
                    "verify_return": vret,
                    "resolved_option_labels": list(labels),
                    "grammar_path": (
                        f"verify({canonical}, text, labels={list(labels)}) -> {vret!r}"
                    ),
                    "first_failed_contract": code,
                    "detail": detail,
                    "gate_decision": d.get("decision"),
                })

    tot = Counter(r["first_failed_contract"] for r in rows)
    by_paper = Counter((r["first_failed_contract"], r["paper"]) for r in rows)
    report = {
        "metric_scope": "root/leaf",
        "baseline": "07d9e34",
        "taxonomy": {
            "N0": "no answer text",
            "S0": "span/provenance invalid OR interval has no canonical token",
            "Q0": "qtype not strict-auto",
            "G1": "answer form cannot parse",
            "G2": "answer parsed but not in option labels",
            "G3": "canonical grammar unsupported",
            "I0": "invariant violation",
        },
        "n": len(rows),
        "totals": dict(tot),
        "by_code_paper": {f"{k[0]}|{k[1]}": v for k, v in by_paper.items()},
        "rows": rows,
    }
    out = OUT / "answer_36_contract_first.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("n =", len(rows), " (expect 36)")
    print("first_failed_contract:", dict(tot))
    print()
    for code in ("S0", "G1", "G2", "G3", "N0", "Q0", "I0"):
        sub = [r for r in rows if r["first_failed_contract"] == code]
        if not sub:
            continue
        print(f"--- {code} ({len(sub)}) ---")
        for r in sub[:6]:
            print(f"  {r['paper']} {r['leaf_id']:14} labels={r['resolved_option_labels']} "
                  f"verify={r['verify_return']}")
            print(f"     text={r['answer_text'][:70]!r}")
            print(f"     {r['detail'][:90]}")
        if len(sub) > 6:
            print(f"  ... +{len(sub)-6} more")
    print("\nwrote", out)


if __name__ == "__main__":
    main()
