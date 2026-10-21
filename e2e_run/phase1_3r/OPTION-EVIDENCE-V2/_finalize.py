from pathlib import Path
import json

out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")
fp = out / "option_evidence_focus_report.md"
s = fp.read_text(encoding="utf-8")
s = s.replace("Option Evidence Survey v2.1", "Option Evidence Survey v2.2")
extra = """
## Why D=29 now (old survey D=1)

Old survey discovered D only when `answer in labels` failed on a composite — answer-driven.
Source-first rule: **per-sub-options composite** (multiple option blocks) **and** `n_leaves < len(sub_qns)` -> D.

Surfaces the full frozen SUB_QUESTION_DECOMPOSITION footprint: geography/politics/physics multi-qn sets + English listening groups all create one leaf while source carries per-sub option blocks.

- English Q5-6 is dual-layer: primary **C** (Q5 C content absent), subsequent **D** (Q6 no leaf).
- Shared-option composites (single option block) are **not** D.

## Mutual exclusion check (DSH B=3 conflict)

| unit | content present? | correct primary | must NOT also count as |
|------|------------------|-----------------|------------------------|
| chem Q23 | YES (L194) | **B** | C |
| math Q4 | YES (`2D.` content) | **B** | C |
| history Q29 | YES (`D Mailun`) | **B** | C |
| english Q5 C | NO | **C** | B |
| english Q6 | YES (L47 A/B) | subsequent **D** | independent root |

DSH `B=3` including Q5 is **rejected**. Correct exclusive primary: B=3 (Q23/Q4/Q29), C=1 (Q5-6), D=29 (1 of them subsequent on Q5-6).

## Deliverables

- option_evidence_survey_v2.json — corrected full-corpus survey (v2.2)
- option_evidence_survey_v2.py — source-first five-layer survey script (investigation only)
- option_evidence_focus_report.md — this report
- Prior wrong classification retained at PHASE1-E2E-REPLAY/option_evidence_survey.json (B=1/D=1 answer-driven)
"""
if "## Why D=29 now" not in s:
    s = s.rstrip() + "\n" + extra
fp.write_text(s, encoding="utf-8")

data = json.loads((out / "option_evidence_survey_v2.json").read_text(encoding="utf-8"))
exec_sum = {
    "task": "Option Evidence survey correction (READ-ONLY)",
    "baseline_accepted": {
        "commit": "af70d64",
        "G1_G3": "PASS",
        "auto_baseline": "154 / 68 / 5 / 57",
        "S0": 25,
        "STRICT_AUTO_TYPES": "unchanged",
        "decomposition": "FROZEN — not modified",
        "console": "still deferred",
    },
    "rejected": [
        "MIMO survey conclusion 'real anomalies only B=1 + D=1'",
        "chem Q23 as isolated Option Evidence defect",
        "DSH B=3 counting english Q5 as B while also calling it C",
    ],
    "classification_model": data["classification_model"],
    "primary_totals_mutually_exclusive": data["totals_primary_mutually_exclusive"],
    "subsequent_not_roots": data["totals_subsequent_not_roots"],
    "focus_adjudication": {
        "chem_Q23": {"primary": "B", "form": "4th content present, D label missing"},
        "math_Q4": {
            "primary": "B",
            "form": "4th content present, label glued `2D.`",
            "2_proof": "digit `2` is label-boundary glue — NOT C content, NOT D content",
        },
        "history_Q29": {"primary": "B", "form": "4th content `D Mailun`, missing `.` separator"},
        "english_Q5_6": {
            "primary": "C",
            "subsequent": ["D"],
            "split": "Q5 C-option content absent (C) vs Q6 A/B exist without leaf (D)",
        },
    },
    "math_Q4_2D_verdict": data["math_Q4_2D_proof"]["verdict"],
    "b_generalization_answer": data["b_generalization"]["answer"],
    "b_samples": data["b_generalization"]["samples_detail"],
    "authority_red_line": "Answer Evidence may DETECT option inconsistency but must NEVER generate Option Evidence. No Answer->Option Recovery.",
    "production_changes": "NONE (zero code / Schema / Gate / Resolver / Producer / Decomposition / DB)",
    "artifacts": [
        "OPTION-EVIDENCE-V2/option_evidence_survey_v2.json",
        "OPTION-EVIDENCE-V2/option_evidence_survey_v2.py",
        "OPTION-EVIDENCE-V2/option_evidence_focus_report.md",
    ],
}
(out / "executive_summary.json").write_text(
    json.dumps(exec_sum, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("wrote executive_summary.json")
print("primary", data["totals_primary_mutually_exclusive"])
print("subseq", data["totals_subsequent_not_roots"])
