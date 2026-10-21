# Option Evidence Survey v2.2 — Focus Report

READ-ONLY. No production code / Schema / Gate / Producer / Decomposition / DB changed.

## Model

- **B**: content PRESENT, label damaged/missing/unrecognized
- **C**: content ABSENT
- **D**: per-sub-options composite, sibling qn has no leaf (decomposition frozen)
- **first_failed_contract** = primary (mutually exclusive); **subsequent_contracts** = residual

## Primary totals (mutually exclusive)

- A: 151
- B: 3
- C: 1
- D: 29
- F: 23
- F0: 7

## Subsequent (not roots)

- D: 1

## DSH count conflict

DSH wrote `B=3` listing english Q5 while also calling Q5-C a C-class. Contradiction.
Rule: B = content present; C = content absent. English Q5 C-option → **C only**.
English Q5-6 dual-layer: first_failed_contract=**C**, subsequent=**[D]**.

## Focus samples

### chem_Q23

- **B** subsequent=[]
  - OPTION_CONTENT_PRESENT_LABEL_MISSING: option-like content L194 after last label L192; declared=3 expected>=4; '$  \\mathrm{H}^{+} + \\mathrm{SO}_{4}^{2-} + \\mathrm{Ba}^{2+} + \\mathrm{OH}^{-} = \\mathrm{H}_{2}\\mathrm{O
  - declared=['A', 'B', 'C'] resolved=['A', 'B', 'C'] answer=D
  - option_like=[{'line': 188, 'preview': 'A．金属钠与水： $ 2Na + 2H_{2}O = 2Na^{+} + 2OH^{-} + H_{2}\\uparrow $'}, {'line': 190, 'preview': 'B．氯化钠溶液与硝酸银溶液：'}]
### history_Q29

- **B** subsequent=[]
  - OPTION_CONTENT_PRESENT_LABEL_DAMAGED: 'D ' kind=space_sep_missing_dot at L307 label=D not in declared=['A', 'B', 'C']; 'D 麦哲伦'
  - declared=['A', 'B', 'C'] resolved=['A', 'B', 'C'] answer=C
  - damaged=[{'line': 307, 'kind': 'space_sep_missing_dot', 'token': 'D ', 'label': 'D', 'preview': 'D 麦哲伦'}]
  - option_like=[{'line': 301, 'preview': 'A. 迪亚士'}, {'line': 303, 'preview': 'B. 达，伽马'}]
### math_Q4

- **B** subsequent=[]
  - OPTION_CONTENT_PRESENT_LABEL_DAMAGED: '2D.' kind=digit_glue at L23 label=D not in declared=['A', 'B', 'C']; 'C. 关于直线 y=x 对称 2D. 关于直线 y= -x 对称'
  - declared=['A', 'B', 'C'] resolved=['A', 'B', 'C'] answer=A
  - damaged=[{'line': 23, 'kind': 'digit_glue', 'token': '2D.', 'label': 'D', 'preview': 'C. 关于直线 y=x 对称 2D. 关于直线 y= -x 对称'}]
  - option_like=[{'line': 21, 'preview': 'A. 关于 x 轴对称 B. 关于 y 轴对称'}, {'line': 23, 'preview': 'C. 关于直线 y=x 对称 2D. 关于直线 y= -x 对称'}]
### english_Q5_6

- **C** subsequent=['D']
  - OPTION_CONTENT_ABSENT: answer slot C ∉ declared=['A', 'B'], no source label/content for C
  - declared=['A', 'B'] resolved=['A', 'B'] answer=C
  - option_like=[{'line': 43, 'preview': 'A. In a hotel. B. In an office.'}, {'line': 47, 'preview': 'A. Larger trousers. B. Dark blue trousers.'}]

## Math Q4 `2D.` — does `2` belong to C or to D content?

- C content is complete and parallel to A/B without `2` (对称-type phrases).
- `2` is not valid C content: bare digit after 对称 is not parallel to A/B/C.
- `2` cannot be D content under label-then-content structure: it sits BEFORE `D.`.
- Therefore `2` is inter-option label-boundary glue/contamination — not semantic content of either option.
- 4th option content `关于直线 y= -x 对称` IS present; label is damaged as digit-glued `2D.`.
- Label identity `D` is recoverable from source form alone (A./B./C. parallel + glued `D.`), WITHOUT answer evidence.
- Prior CLEAN_LABEL/GLUED probes miss `2D.` because lookbehind treats `2` as alnum — survey-level blind spot.

Verdict: `{"2_belongs_to_previous_option": false, "2_is_D_content": false, "2_is_label_boundary_glue": true, "B_subtype": "B2_label_damaged_glued (digit_glue)", "producer_gap": "label regex lookbehind excludes alnum prefix; digit-glued `2D.` invisible to CLEAN and prior GLUED probe"}`

## B generalization

YES — narrow deterministic Producer option-label parsing compatibility gap, NOT a recovery mechanism. Confirmed samples share: option CONTENT present + label token damaged/missing/unrecognized + label letter recoverable from source form WITHOUT answer evidence. Subtypes: B1 complete label drop (化学 Q23, 历史 Q29 space-sep), B2 digit/char glue (数学 Q4 `2D.`). Common contract: Producer must accept damaged-but-deterministically-identifiable option labels (G1/G3-class parser compatibility). NO Answer→Option Recovery.

Confirmed samples:
- 化学/Q23 (B1): 4th content L194, `D．` dropped entirely
- 数学/Q4 (B2): 4th content L23, label glued as `2D.`
- 历史/Q29 (B1/B2): 4th content L307 `D 麦哲伦` missing `.` separator

Common deterministic shape:
- option CONTENT span exists in the unit's options region
- label token absent (B1) or glued/damaged (B2: `2D.`, `D 麦哲伦`)
- label letter recoverable from parallel label sequence + content position WITHOUT answer
- Producer declares only clean labels → under-declares options

## Authority red line

Answer Evidence may DETECT option inconsistency but must NEVER generate Option Evidence.
No Answer→Option Recovery is proposed or implemented.

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
