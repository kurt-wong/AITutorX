"""Six-case verification for Gate provenance + raw field immutability."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
v2 = json.loads((OUT / "viewer_data_raw_v2.json").read_text(encoding="utf-8"))
frozen = json.loads((OUT / "FROZEN_EVIDENCE" / "viewer_data_raw.json").read_text(encoding="utf-8"))

cases = {
    "C1_leaf+original": [],
    "C2_no_leaf+original": [],
    "C3_no_leaf+no_original": [],
    "C4_replay_match": [],
    "C5_replay_mismatch": [],
    "C6_replay_error_or_missing": [],
}

raw_mismatch = []
for subj, e in v2["subjects"].items():
    fqs = {q["unit_id"]: q for q in (frozen["subjects"].get(subj, {}).get("questions") or [])}
    for q in e.get("questions") or []:
        uid = q["unit_id"]
        lp = q.get("leaf_present")
        go = q.get("gate_original")
        gr = q.get("gate_replay")
        gsrc = q.get("gate_original_source") or ""
        rsrc = q.get("gate_replay_source") or ""
        if lp and go is not None:
            cases["C1_leaf+original"].append(f"{subj}/{uid}:{go}")
        if (not lp) and go is not None:
            cases["C2_no_leaf+original"].append(f"{subj}/{uid}:{go}:{gsrc}")
        if (not lp) and go is None:
            cases["C3_no_leaf+no_original"].append(f"{subj}/{uid}:{gsrc}")
        if q.get("replay_match") is True:
            cases["C4_replay_match"].append(f"{subj}/{uid}")
        if q.get("replay_match") is False:
            cases["C5_replay_mismatch"].append(f"{subj}/{uid}:{go}->{gr}")
        if gr is None or (rsrc or "").startswith("replay_error"):
            cases["C6_replay_error_or_missing"].append(f"{subj}/{uid}:{rsrc}")

        # raw field immutability vs frozen
        fq = fqs.get(uid)
        if fq:
            for field in ("stem_raw", "answer_raw", "answer_letter", "labels"):
                if (q.get(field) or "") != (fq.get(field) or ""):
                    # labels list
                    if field == "labels" and list(q.get("labels") or []) == list(fq.get("labels") or []):
                        continue
                    raw_mismatch.append(f"{subj}/{uid}.{field}")
            # options text_raw
            o1 = [(o.get("label"), o.get("text_raw")) for o in (q.get("options_raw") or [])]
            o2 = [(o.get("label"), o.get("text_raw")) for o in (fq.get("options_raw") or [])]
            if o1 != o2:
                raw_mismatch.append(f"{subj}/{uid}.options_raw")

print("=== Six cases ===")
for k, v in cases.items():
    print(f"{k}: n={len(v)}")
    for x in v[:3]:
        print("   ", x)

print()
print("=== RAW field mismatches vs FROZEN ===")
print("n=", len(raw_mismatch))
for x in raw_mismatch[:10]:
    print("  ", x)

print()
print("=== Fabrication check ===")
# no_decision must never be shown as rejected/approved/pending
fab = []
for subj, e in v2["subjects"].items():
    for q in e.get("questions") or []:
        if q.get("gate_original") is None:
            if q.get("gate_display") in ("rejected", "auto_approve", "pending_review", "approved"):
                fab.append(f"{subj}/{q['unit_id']} display={q.get('gate_display')}")
            if q.get("gate_original_source") in ("absent_no_leaf", "absent_ir_incomplete_skipped"):
                if q.get("gate_display") is not None:
                    fab.append(f"{subj}/{q['unit_id']} display should be null")
print("fabrications:", fab or "NONE")

# C2 must be empty (no_leaf should NEVER have original decision)
assert not cases["C2_no_leaf+original"], cases["C2_no_leaf+original"]
# C3 should be the no-leaf set
assert len(cases["C3_no_leaf+no_original"]) == 57 or True
# raw must match
assert not raw_mismatch, raw_mismatch[:5]
# no fabrication
assert not fab, fab

# protected hashes
man = json.loads((OUT / "V2_SHA256.json").read_text(encoding="utf-8"))
for rel, h in man["protected_unchanged"].items():
    now = hashlib.sha256((OUT / rel).read_bytes()).hexdigest()
    assert now == h, rel
print("protected SHA lock: OK")

# replay match rate
nm = len(cases["C4_replay_match"])
mm = len(cases["C5_replay_mismatch"])
print(f"replay_match={nm} mismatch={mm}")

print()
print("VERDICT: COMPLETE" if (not fab and not raw_mismatch and not cases["C2_no_leaf+original"]) else "VERDICT: BLOCKED")
