from pathlib import Path
import json

out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")
jpath = out / "b_label_repair_simulation.json"
data = json.loads(jpath.read_text(encoding="utf-8"))

# annotate simulation-method caveat
data["simulation_method"] = {
    "meaningful_prediction": "simulated_decision_grammar_path + other_layers_pass",
    "full_evaluate_artifact": (
        "simulated_gate_decision_full_evaluate injects a SYNTHETIC span "
        "(span_id=sim-option-label, text_hash=sim) that is NOT in ResolvedRun. "
        "Gate therefore reports structural/provenance fail → rejected. "
        "This is a SIMULATION ARTIFACT, NOT the post-repair prediction."
    ),
    "real_fix_would": (
        "Producer recognizes damaged label from source-local form, then binds the "
        "ALREADY-PRESENT option content (Q23 L194 / Math Q4 L23 / History Q29 L307) "
        "as a real ResolvedSpan with exact resolution. Then structural/provenance "
        "stay pass and only grammar.verify changes."
    ),
    "grammar_path_is_authoritative_for_delta": True,
}
data["rollup"]["refined_conclusion"] = (
    "Measured auto delta if all 3 B labels repaired = 1 (Chem Q23 only). "
    "Math Q4: 0 (answer text is multi-line teacher block, AnswerTokenContract still fails). "
    "History Q29: 0 (already auto_approve with labels A,B,C; answer C). "
    "B=3 → auto+3 is FALSIFIED by measurement."
)
data["boundary_precision"] = {
    "chem_Q23": {"q_boundary": [186, 186], "options_lines": [188, 194], "issue": "observed"},
    "math_Q4": {"q_boundary": [19, 19], "options_lines": [21, 23], "issue": "observed"},
    "history_Q29": {"q_boundary": [299, 299], "options_lines": [301, 307], "issue": "observed"},
    "b_repair_depends_on_boundary_change": False,
    "stop_condition_monitor": (
        "If implementing B fix requires changing question boundary semantics → STOP."
    ),
}
jpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

md = out / "b_label_repair_simulation.md"
s = md.read_text(encoding="utf-8")
extra = """
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
   (`4.\\n【考点】...`), `_answer_form_single_choice` → None. Adding D to labels
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
"""
if "## Simulation method caveat" not in s:
    s = s.rstrip() + "\n" + extra
md.write_text(s, encoding="utf-8")
print("updated json + md")
print("auto_delta_sum", data["rollup"]["sum_auto_delta_if_repair"])
