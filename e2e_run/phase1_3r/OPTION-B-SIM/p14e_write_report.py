from pathlib import Path
import json, hashlib

OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")
OFF = Path(r"D:\Project\Papers\Ocr-markdown\会考\化学\2018北京春季高中会考化学（教师版）(1).md")
BAT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_1_corpus_optspans\reslice-batch-C\会考\化学\2018北京春季高中会考化学（教师版）(1).md")

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

report = {
    "task": "P1.4-E2E-TRACE (READ-ONLY) — Preprocessing → V3 → Question responsibility",
    "adjudication_start": (
        "P1.4-B FROZEN. ec62d29/d42cde6 are diagnostic checkpoints only. "
        "Do NOT assume Producer is at fault. Do NOT fix anything this round."
    ),
    "L0_contract_finding": {
        "question": "What does Preprocessing officially output? What does V3 consume?",
        "official_preprocessing_location": "Papers/Ocr-markdown/<category>/<paper>.md (+ _imgs)",
        "phase1_consumed_input": "AITutor-X/e2e_run/phase1_1_corpus_optspans/reslice-batch-C/会考/...",
        "md_byte_identity_chem_2018_spring": {
            "official_sha256": sha(OFF),
            "phase1_sha256": sha(BAT),
            "byte_identical": sha(OFF) == sha(BAT),
        },
        "conclusion_on_input_transport": (
            "For the spring chemistry paper, the MD text Phase 1 consumes is BYTE-IDENTICAL "
            "to the official Ocr-markdown output. Input transport did NOT mutate the text."
        ),
        "who_adds_structure": (
            "Preprocessing produces MD (OCR lines/text/images/formulas). "
            "Structural declarations (unit_id, stem_lines, options[].label, answer_lines) "
            "come from a SEPARATE annotation/manifest layer (reslice_pipeline + LLM manifests) "
            "in Papers/scripts + *.manifest.json. "
            "V3 preprocessing_consumer reads manifest + md and maps them into annotation payload."
        ),
        "architecture_classification": (
            "CLOSEST TO Architecture B: preprocessing = document normalization "
            "(OCR/line/formula/image); structure (question/option/answer boundaries) is declared "
            "by a later annotation layer and consumed by V3. "
            "NOT Architecture A (preprocessing does not emit full Question/Option/Answer objects)."
        ),
        "official_vs_experiment": (
            "Official curated MD lives under Ocr-markdown/{会考,合格考,学业水平考试,...}. "
            "reslice-batch-C / reslice-pac / auto-annotated-* are EXPERIMENTAL reslice/annotation "
            "variants used by Phase 1. Phase 1 has NOT completed raw-PDF→preprocessing→V3 formal E2E "
            "via the TaskExecutor production path (per PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION)."
        ),
    },
    "four_questions_plus_golden": [],
    "critical_side_effect": {
        "finding": "P1.4-B Rule A false-positive on Chemistry Q20",
        "source_L157_159": "D. 硫在自然界的循环过程中，涉及了氧 / (blank) / 还原反应",
        "semantics": "D content = 涉及了氧化还原反应 (cross-line OCR break)",
        "manifest_before_P1_4B": ["A", "B", "C", "D"],  # bak
        "manifest_after_P1_4B": ["A", "B", "C", "D", "E"],
        "false_E_line": 159,
        "cause": (
            "_expand_option_spans Rule A treats L159 还原反应 as trailing unlabeled option content "
            "and assigns next sequential letter E. That is WRONG: L159 is D's line-wrapped content."
        ),
        "implication": (
            "P1.4-B is NOT a pure win. Rule A as implemented can fabricate extra options from "
            "cross-line continuations. This is a real product risk, not just cosmetic."
        ),
    },
    "responsibility_matrix": [
        {
            "question": "Chemistry Q20",
            "preprocessing_output": (
                "MD correct as text: D spans L157+L159 with blank between "
                "(OCR line-wrap of 氧化还原反应). No E in text."
            ),
            "v3_input_md": "byte-identical to official MD",
            "manifest_before": "A,B,C,D (D only at L157; L159 unassigned)",
            "first_change_layer": "P1.4-B Rule A in Producer _expand_option_spans (our patch)",
            "final_symptom": "spurious option E = 还原反应; D content truncated",
            "responsibility": "P1.4-B Rule A (our diagnostic checkpoint) + original Producer incomplete D span",
            "layer_enum": "V3 Producer (p14b rule) — and Producer span completeness",
            "severity": "HIGH — fabricates wrong structure",
        },
        {
            "question": "Math Q4",
            "preprocessing_output": (
                "MD: C. …对称 2D. 关于直线… — digit-glued label form present in text"
            ),
            "v3_input_md": "byte-identical to official MD",
            "manifest_before": "A,B,C (D missed)",
            "manifest_after_p14b": "A,B,C,D (D recovered via Rule B)",
            "first_change_layer": "annotation/manifest (original missed D); P1.4-B recovered it",
            "final_symptom": "labels complete, but answer is teacher-block → verify None → pending",
            "responsibility": "NOT option-label for Gate. Gate blocker is answer-slice (S0 family).",
            "layer_enum": "No defect in option labels after repair; answer-side is separate issue",
            "severity": "MEDIUM — evidence completeness fixed; Gate unchanged as predicted",
        },
        {
            "question": "Chemistry Q23",
            "preprocessing_output": "MD: 4th option content L194 with NO label token (OCR dropped D．)",
            "v3_input_md": "byte-identical to official MD",
            "manifest_before": "A,B,C",
            "manifest_after_p14b": "A,B,C,D (Rule A trailing)",
            "first_change_layer": "annotation/manifest originally missed D; P1.4-B recovered",
            "final_symptom": "answer D ∈ labels → auto",
            "responsibility": "Preprocessing dropped label glyph (OCR); Producer/manifest did not recover; P1.4-B did",
            "layer_enum": "Preprocessing (label glyph) + V3 Producer (recovery)",
            "severity": "LOW after repair — Gate +1 as measured",
        },
        {
            "question": "History Q29",
            "preprocessing_output": "MD: `D 麦哲伦` missing `.` separator (OCR)",
            "v3_input_md": "byte-identical",
            "manifest_before": "A,B,C",
            "manifest_after_p14b": "A,B,C,D (Rule C)",
            "first_change_layer": "annotation/manifest missed D; P1.4-B recovered",
            "final_symptom": "already auto before (answer C ∈ ABC); now complete",
            "responsibility": "Preprocessing separator damage; Producer recovery",
            "layer_enum": "Preprocessing (separator) + V3 Producer (recovery)",
            "severity": "INFO — completeness only, no Gate change",
        },
        {
            "question": "Chemistry Q22 GOLDEN",
            "preprocessing_output": "MD: normal A./B./C./D. lines",
            "v3_input_md": "byte-identical",
            "manifest": "A,B,C,D complete",
            "first_change_layer": "none",
            "final_symptom": "auto_approve, labels complete",
            "responsibility": "No defect",
            "layer_enum": "No defect",
            "severity": "none",
        },
    ],
    "acceptance_levels": {
        "L1_data_correct": (
            "PARTIAL FAIL on Q20 after P1.4-B: a correct MD was turned into worse structure (E). "
            "Q23/Q29 improved. Q4 option labels improved. Golden Q22 stable."
        ),
        "L2_product_correct": "NOT ASSESSED — no frontend rendering in this trace",
        "L3_governance_correct": "NOT the current bottleneck; frozen per Owner",
    },
    "what_is_proven_vs_not": {
        "proven": [
            "Phase 1 input MD for chem 2018 spring == official Ocr-markdown MD (byte-identical)",
            "Structure (options labels) is NOT in the MD; it is in *.manifest.json annotation layer",
            "Q20 spurious E was INTRODUCED by P1.4-B Rule A (bak proves prior A,B,C,D)",
            "P1.4-B Q23 +1 auto is real and measured",
            "P1.4-B can fabricate options from cross-line continuations (Q20)",
        ],
        "NOT_proven": [
            "That reslice_pipeline is the formal V3 integration adapter",
            "That Q20/Q4/Q23/Q29 are formal V3 product defects (Phase 1 is experimental corpus path)",
            "That official TaskExecutor production path has the same symptoms",
            "Frontend rendering correctness",
        ],
    },
    "recommendation_to_owner": {
        "1_freeze": "P1.4-B stays frozen. Do not ship Rule A as-is — Q20 shows it fabricates options.",
        "2_rollback_or_scope": (
            "Either revert P1.4-B Rule A, or restrict Rule A to 'single-line trailing content only' "
            "and never bind a line that could be a continuation of the previous option."
        ),
        "3_next": (
            "P1.4-E2E formal path: raw PDF → official preprocessing → V3 TaskExecutor → Question. "
            "Four questions + golden. Do not expand governance until L1 data path is closed."
        ),
    },
}

# fill source excerpts
for paper, uid, purpose in [
    ("化学", "Q20", "cross-line option D"),
    ("数学", "Q4", "digit-glued 2D."),
    ("化学", "Q23", "trailing unlabeled D"),
    ("历史", "Q29", "space-sep D 麦哲伦"),
    ("化学", "Q22", "GOLDEN"),
]:
    report["four_questions_plus_golden"].append({
        "unit": f"{paper}/{uid}",
        "purpose": purpose,
    })

(OUT / "p14e_e2e_trace_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

md = """# P1.4-E2E-TRACE — Data Flow Responsibility Report (READ-ONLY)

## 0. Adjudication start
P1.4-B **FROZEN**. `ec62d29`/`d42cde6` = diagnostic checkpoints only.
This report does **not** assume Producer is at fault.

## 1. Interface truth: Preprocessing vs V3

| Layer | What it is | Where |
|-------|------------|-------|
| **L0 Preprocessing (official)** | OCR → Markdown (lines/text/imgs/formulas) | `Papers/Ocr-markdown/{会考,合格考,…}/*.md` |
| **L1 Annotation/manifest** | unit_id, stem/options/answer **line spans + labels** | `*.manifest.json` (reslice_pipeline + LLM) |
| **L2 V3 consumer** | manifest+md → annotation payload → Resolver → IR → Compile → Gate | `preprocessing_consumer` + `app/domains/*` |

**Input transport fact:** for 2018 spring chemistry,
`Ocr-markdown/会考/化学/*.md` and Phase 1 `reslice-batch-C/会考/化学/*.md`
are **byte-identical** (same SHA256). Transport does **not** mutate text.

**Architecture classification:** **Architecture B** —
preprocessing = document normalization; **structure is a later annotation layer**.
V3 does not re-OCR; it consumes declared structure + source lines.

**Critical:** Phase 1 runs on **experimental** `reslice-batch-C`, not the formal
TaskExecutor production path. These symptoms are **not yet proven** to be formal V3 product defects.

## 2. Four questions + golden (actual text per layer)

### Chemistry Q20 — cross-line option D
Source (official = Phase 1):
```
157: D. 硫在自然界的循环过程中，涉及了氧
158:
159: 还原反应
```
True option D = 「涉及了**氧化还原**反应」(OCR line-wrap).

| Layer | Content |
|-------|---------|
| Preprocessing MD | D split L157+L159; **no E in text** |
| Manifest **before** P1.4-B (bak) | A,B,C,D (D only at L157) |
| Manifest **after** P1.4-B | A,B,C,**D,E** — **E = 还原反应 (FALSE)** |
| V3 leaf | labels A,B,C,D,E |
| Gate | auto_approve (answer B) |

**First change layer:** **P1.4-B Rule A** treated L159 as trailing option → invented E.
**Responsibility:** **P1.4-B Rule A (our checkpoint)** + original Producer D span incomplete.
**This is a product-risk defect we introduced.**

### Math Q4 — `2D.`
| Layer | Content |
|-------|---------|
| MD | `C. …对称 2D. 关于直线…` |
| Manifest before | A,B,C |
| Manifest after P1.4-B | A,B,C,D (Rule B) |
| Answer | teacher block → letter=None |
| Gate | pending (unchanged, as simulated) |

**Responsibility:** option labels repaired; Gate blocker is **answer-slice (S0 family)** — out of P1.4-B scope.

### Chemistry Q23 — trailing unlabeled D
| Layer | Content |
|-------|---------|
| MD | L194 ionic equation, **no `D．` token** (OCR dropped label) |
| Manifest before | A,B,C |
| After | A,B,C,D |
| Gate | pending → **auto (+1 measured)** |

**Responsibility:** Preprocessing dropped label glyph; recovery via Rule A.

### History Q29 — `D 麦哲伦`
| Layer | Content |
|-------|---------|
| MD | `D 麦哲伦` (missing `.`) |
| After P1.4-B | A,B,C,D |
| Gate | auto → auto (completeness only) |

### Chemistry Q22 GOLDEN
Normal A./B./C./D. → A,B,C,D → auto. **No defect.** Golden path holds for clean input.

## 3. Responsibility matrix

| Q | Preproc output | V3 input MD | First change | Final symptom | Responsibility layer |
|---|----------------|-------------|--------------|---------------|----------------------|
| Q20 | D跨行续文正确，无E | byte-identical | **P1.4-B Rule A** | 虚假 E | **V3 Producer (p14b Rule A)** |
| Q4 | `2D.` 在文中 | byte-identical | annotation 漏 D / p14b 补 | labels全，answer仍None | No option defect after repair；answer-side 独立 |
| Q23 | 4th content 无标签 | byte-identical | annotation 漏 D / p14b 补 | +1 auto | Preprocessing 标签字形 + Producer 恢复 |
| Q29 | `D 麦哲伦` 缺点 | byte-identical | annotation 漏 D / p14b 补 | completeness | Preprocessing 分隔符 + Producer 恢复 |
| Q22 golden | 正常 | byte-identical | 无 | auto | **No defect** |

## 4. Acceptance levels
- **L1 data correct: PARTIAL FAIL** — Q20 was made **worse** by our Rule A
- **L2 product correct: not assessed** (no frontend)
- **L3 governance: frozen**

## 5. Proven vs NOT proven
**Proven:** MD transport clean; structure lives in manifest; Q20 E is P1.4-B artifact; Q23 +1 real.
**Not proven:** reslice_pipeline == formal V3 integration; formal TaskExecutor path has same symptoms; frontend correctness.

## 6. Recommendation (for Owner — no action taken)
1. Keep P1.4-B frozen.
2. **Rule A as-is must not ship** — it fabricates options from cross-line continuations (Q20).
3. Next: formal raw→preprocessing→V3 TaskExecutor E2E on 4 questions + golden. Then decide blame.
"""
(OUT / "p14e_e2e_trace_report.md").write_text(md, encoding="utf-8")
print("md_identical", sha(OFF) == sha(BAT))
print("wrote", OUT / "p14e_e2e_trace_report.md")
