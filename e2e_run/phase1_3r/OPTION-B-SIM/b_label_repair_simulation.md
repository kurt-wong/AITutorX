# P1.4-B Phase 1 — Pre-repair Impact Simulation (READ-ONLY)

No production code / Schema / DB / Gate policy / Decomposition changed.
Simulated labels come from SOURCE-LOCAL structure only. Answer never creates labels.

## Delta table

| sample | form | old labels | sim labels | ans | ans∈old | ans∈sim | old gate | sim gate (grammar path) | auto Δ |
|--------|------|------------|------------|-----|---------|---------|----------|-------------------------|--------|
| Chemistry Q23 | trailing_label_lost | ['A', 'B', 'C'] | ['A', 'B', 'C', 'D'] | D | False | True | pending_review | auto_approve | 1 |
| Math Q4 | glued_label | ['A', 'B', 'C'] | ['A', 'B', 'C', 'D'] | None | None | None | pending_review | pending_review | 0 |
| History Q29 | separator_loss | ['A', 'B', 'C'] | ['A', 'B', 'C', 'D'] | C | True | True | auto_approve | auto_approve | 0 |

**Sum auto delta = 1** (forbidden to assume 3).

## Per-sample reasons

### Chemistry Q23

- form: `trailing_label_lost` — 4th option content present; `D．` label token dropped
- source proof: L194 ionic equation content, no label token; L188/190/192 have A．B．C．
- simulated label source: SOURCE-LOCAL: parallel label sequence A./B./C. + 4th content position in options_lines=(188,194); NOT from answer
- answer evidence: `D` → letter=D
- verify: None → True
- old gate: `pending_review` (S=pass P=pass Sem=pass)
- simulated decision (grammar path): `auto_approve`
- other_layers_pass: True
- **auto Δ = 1** — grammar flip enables auto IF no other blockers (see other_layers_pass)
- reason delta: ['grammar.verify: None -> True', 'decision(grammar-path): pending_review -> auto_approve', 'answer_in_labels: False -> True']
- boundary: q=[186, 186] o=[188, 194] issue=observed: options_lines outside questions_lines
- B repair depends on boundary change? **False**

### Math Q4

- form: `glued_label` — 4th option content present; label glued as `2D.`
- source proof: L23 `C. ...对称 2D. 关于直线 y= -x 对称`; digit `2` is boundary glue
- simulated label source: SOURCE-LOCAL: digit-glued `2D.` deterministic parse (strip leading digit glue) → label D + content 关于直线 y= -x 对称; NOT from answer
- answer evidence: `4.

【考点】余弦函数的图象.

【分析】根据当自变量相同时，它们的函数值相反，可得它们的图象关于x轴对称.

【解答】解：由于当自变量相同时，它们的函数值相` → letter=None
- verify: None → None
- old gate: `pending_review` (S=pass P=pass Sem=pass)
- simulated decision (grammar path): `pending_review`
- other_layers_pass: True
- **auto Δ = 0** — label repair alone does NOT flip gate to auto (verify None->None; decision stays pending_review)
- boundary: q=[19, 19] o=[21, 23] issue=observed: options_lines outside questions_lines
- B repair depends on boundary change? **False**

### History Q29

- form: `separator_loss` — 4th option content present; label `D ` missing `.` separator
- source proof: L307 `D 麦哲伦`; L301-305 have A. B. C.
- simulated label source: SOURCE-LOCAL: line-start `D` + CJK content parallel to A./B./C. → label D with missing separator; NOT from answer
- answer evidence: `29. 【答案】C` → letter=C
- verify: True → True
- old gate: `auto_approve` (S=pass P=pass Sem=pass)
- simulated decision (grammar path): `auto_approve`
- other_layers_pass: True
- **auto Δ = 0** — already auto; label repair does not change AnswerTokenContract
- boundary: q=[299, 299] o=[301, 307] issue=observed: options_lines outside questions_lines
- B repair depends on boundary change? **False**

## Boundary precision (Q23)

Q23 `q_boundary=[186,186]` / `options_lines=[188,194]` → `boundary_precision_issue = observed`.
B label parsing uses options region content + label token form. **Does not require boundary semantics change.**
If a future fix required boundary change → STOP CONDITION #1.

## Authority red line

```
Answer Evidence → detect inconsistency ONLY
Source Evidence → deterministic label parsing → recognize already-present label
FORBIDDEN: answer letter → create option / infer missing content / LLM label
```

## Simulation method caveat (IMPORTANT)

`simulated_gate_decision_full_evaluate` injects a **synthetic span** (`sim-option-label`,
`text_hash=sim`) that is **not** in ResolvedRun. Gate correctly reports structural/provenance
fail → `rejected`. That is a **simulation artifact**, not the post-repair prediction.

**Authoritative delta** = `simulated_decision_grammar_path` + `other_layers_pass`
(old structural/provenance/semantic already `pass` on all three samples).

A real Producer fix binds the **already-present** source content as a real ResolvedSpan
(exact), so only `grammar.verify` changes. Under that model:

| sample | old gate | post-repair (grammar path) | auto Δ |
|--------|----------|----------------------------|--------|
| Chemistry Q23 | pending_review | **auto_approve** | **+1** |
| Math Q4 | pending_review | pending_review | **0** (answer text not canonical) |
| History Q29 | **auto_approve** | auto_approve | **0** (already auto) |

**Sum auto Δ = 1. `B=3 → auto+3` is FALSIFIED.**

### Why each delta

1. **Chem Q23** — answer=D ∉ [A,B,C] → verify None. After label D recognized from
   source-local trailing content: answer=D ∈ [A,B,C,D] → verify True → auto
   (other layers already pass). **Only real Gate gain.**

2. **Math Q4** — answer text is the whole teacher solution block
   (`4.\n【考点】...`), `_answer_form_single_choice` → None. Adding D to labels
   does **not** fix AnswerTokenContract. Stays pending. Auto gain **0**.
   (Separate F/S0 answer-evidence issue — out of this B-repair scope.)

3. **History Q29** — answer=C ∈ [A,B,C] already; **already auto_approve**.
   Recognizing `D 麦哲伦` repairs Option Evidence completeness only.
   Auto gain **0**. Must NOT be reported as "Gate improved".

## Boundary precision (all three)

All three show `options_lines` start **after** `questions_lines` end
(`boundary_precision_issue = observed`).

**B label parsing does NOT depend on changing question boundary semantics.**
It reads: options region content span + label token form (drop/glue/separator).

If a future fix required boundary change → **STOP CONDITION #1**.

## Phase 2 gate (parser rule readiness)

Three forms satisfy Source-local deterministic evidence:

| form | sample | deterministic rule (source-local) | uses answer? | uses LLM? |
|------|--------|-----------------------------------|--------------|-----------|
| trailing label lost | Q23 | unlabeled content after last clean label in options region, expected label sequence next letter | NO | NO |
| glued label `2D.` | Math Q4 | digit/char glued before `A-H` + separator → strip glue, take letter | NO | NO |
| separator loss `D 麦哲伦` | Q29 | line-start letter + CJK content parallel to clean labels | NO | NO |

Common constraints hold: no question identity change, no decomposition change,
no option content change, no free-text A/B/C/D harvesting.

## Recommendation for next step

Phase 1 complete. **Do not implement Producer fix yet without accepting that
only Q23 yields auto+1.** If the goal is Gate auto, Q23 is the only candidate;
Q4 needs answer-evidence work (separate); Q29 is already auto.

Option Evidence completeness still justifies recognizing all three labels
(B gap is real), but **gain accounting must stay honest**.
