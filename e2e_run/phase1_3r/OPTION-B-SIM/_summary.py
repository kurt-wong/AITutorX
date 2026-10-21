from pathlib import Path
import json
out = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-B-SIM")
data = json.loads((out / "b_label_repair_simulation.json").read_text(encoding="utf-8"))
summary = {
    "task": "P1.4-B Phase 1 — READ-ONLY pre-repair impact simulation",
    "production_changes": "NONE",
    "baseline_frozen": {
        "commit": "af70d64",
        "gate_auto": 154,
        "pending": 68,
        "rejected": 5,
        "option_survey": {"A": 151, "B": 3, "C": 1, "D": 29, "F": 23, "F0": 7},
    },
    "headline": "B=3 → auto+3 FALSIFIED. Measured auto delta = 1 (Chem Q23 only).",
    "delta_table": [
        {
            "sample": r["sample"],
            "form": r["form"],
            "old_labels": r["old_declared_labels"],
            "sim_labels": r["simulated_new_labels"],
            "answer_letter": r["old_answer_evidence"]["parsed_letter"],
            "answer_in_old": r["answer_in_old_labels"],
            "answer_in_sim": r["answer_in_simulated_labels"],
            "old_gate": r["old_gate_decision"]["decision"],
            "sim_gate_grammar_path": r["simulated_decision_grammar_path"],
            "auto_delta": r["auto_delta_if_repair"],
            "why": r["auto_delta_reason"],
        }
        for r in data["samples"]
    ],
    "sum_auto_delta": data["rollup"]["sum_auto_delta_if_repair"],
    "boundary_precision": data["boundary_precision"],
    "authority": {
        "allowed": "Source-local deterministic label parsing of already-present content",
        "forbidden": "answer → create option / infer content / LLM label",
    },
    "next": (
        "Phase 1 done. Do not implement Producer fix until accepting only Q23 yields auto+1. "
        "Q4 needs separate answer-evidence work; Q29 is already auto (completeness only)."
    ),
    "artifacts": [
        "OPTION-B-SIM/b_label_repair_simulation.json",
        "OPTION-B-SIM/b_label_repair_simulation.md",
        "OPTION-B-SIM/b_label_repair_simulation.py",
    ],
}
(out / "phase1_simulation_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(summary["headline"], ensure_ascii=False))
print("sum", summary["sum_auto_delta"])
for r in summary["delta_table"]:
    print(f"  {r['sample']}: auto_d={r['auto_delta']} old={r['old_gate']} sim={r['sim_gate_grammar_path']}")
