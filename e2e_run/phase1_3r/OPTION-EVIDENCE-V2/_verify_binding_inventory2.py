"""READ-ONLY: independently recompute EVERY hash in EVIDENCE_BINDING_INVENTORY.json.

Purpose: prove the 9/9 numbers are computed, not written constants, and that the
binding RELATIONS actually hold (freeze != initial correctness).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def sha(p: Path) -> str | None:
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> None:
    inv = json.loads((EA / "EVIDENCE_BINDING_INVENTORY.json").read_text(encoding="utf-8"))
    subs = inv["subjects"]

    n = len(subs)
    res = {"manifest": 0, "preproc_md": 0, "pdf": 0, "pdf_txt": 0,
           "v3_out": 0, "owner_md": 0, "declared_bind": 0}
    claims = {"sha_match": 0, "sha_match_bad": 0,
              "identical": 0, "identical_bad": 0}
    problems = []

    for subj, e in subs.items():
        b = e["bindings"]
        man = b["manifest"]
        pm = b["preprocessing_md"]
        pdf = b["input_pdf"]
        pt = b.get("pdf_text_extract", {})
        v3 = b.get("v3_output", {})
        oa = b.get("owner_accepted_md", {})

        # recompute
        man_actual = sha(EA / man["path"])
        decl = Path(str(man.get("declared_source_file", "")))
        decl_actual = sha(decl)
        pm_actual = sha(EA / pm["path"])
        pdf_actual = sha(EA / pdf["path"])
        pt_actual = sha(EA / pt["path"]) if pt.get("path") else None
        v3_actual = sha(EA / v3["path"]) if v3.get("path") else None
        oa_actual = sha(EA / oa["path"]) if oa.get("path") else None

        if man_actual == man.get("sha256"):
            res["manifest"] += 1
        else:
            problems.append((subj, "manifest sha", man.get("sha256"), man_actual))
        if pm_actual == pm.get("sha256"):
            res["preproc_md"] += 1
        else:
            problems.append((subj, "preproc md sha", pm.get("sha256"), pm_actual))
        if pdf_actual == pdf.get("sha256"):
            res["pdf"] += 1
        else:
            problems.append((subj, "pdf sha", pdf.get("sha256"), pdf_actual))
        if pt_actual == pt.get("sha256"):
            res["pdf_txt"] += 1
        else:
            problems.append((subj, "pdf.txt sha", pt.get("sha256"), pt_actual))
        if v3_actual == v3.get("sha256"):
            res["v3_out"] += 1
        else:
            problems.append((subj, "v3 sha", v3.get("sha256"), v3_actual))
        if oa_actual == oa.get("sha256"):
            res["owner_md"] += 1
        else:
            problems.append((subj, "owner md sha", oa.get("sha256"), oa_actual))

        # --- BINDING relation: declared_source_file must hash-equal the 02 md
        if decl_actual and decl_actual == pm_actual:
            res["declared_bind"] += 1
        else:
            problems.append((subj, "declared_source != preprocessing_md",
                             decl_actual, pm_actual))

        # --- claims must match recomputation
        if pm.get("sha_match") is True:
            claims["sha_match"] += 1
            if decl_actual != pm_actual or pm_actual != pm.get("expected_sha_from_v2"):
                claims["sha_match_bad"] += 1
                problems.append((subj, "sha_match=true but relation fails", "", ""))
        if pdf.get("sha_match") is True:
            claims["sha_match"] += 1
            if pdf_actual != pdf.get("expected_sha_from_v2"):
                claims["sha_match_bad"] += 1
                problems.append((subj, "pdf sha_match=true but relation fails", "", ""))
        if oa.get("identical_to_preprocessing") is True:
            claims["identical"] += 1
            if oa_actual != pm_actual:
                claims["identical_bad"] += 1
                problems.append((subj, "owner_md identical=true but differs", "", ""))

    print("=" * 96)
    print("INDEPENDENT RECOMPUTATION of EVIDENCE_BINDING_INVENTORY.json")
    print("=" * 96)
    print(f"subjects: {n}")
    print("\nrecomputed hash matches (claim == actual):")
    for k, v in res.items():
        print(f"   {k:<16}{v}/{n}")
    print(f"\nclaims of sha_match=true : {claims['sha_match']}"
          f"   (contradicted by recomputation: {claims['sha_match_bad']})")
    print(f"claims of identical=true : {claims['identical']}"
          f"   (contradicted: {claims['identical_bad']})")
    print(f"\nPROBLEMS: {len(problems)}")
    for p in problems[:15]:
        print(f"   {p}")

    # the crucial semantic check the Owner asked for
    print("\n" + "=" * 96)
    print("Owner's requirement: freeze != initial correctness — is the binding chain")
    print("manifest -> declared_source_file -> 02 md -> owner_accepted -> pdf coherent?")
    print("=" * 96)
    bad = 0
    for subj, e in subs.items():
        b = e["bindings"]
        decl = Path(str(b["manifest"].get("declared_source_file", "")))
        d = sha(decl)
        pm = sha(EA / b["preprocessing_md"]["path"])
        oa = sha(EA / b["owner_accepted_md"]["path"]) if b.get("owner_accepted_md") else None
        ok = (d is not None and d == pm == oa)
        if not ok:
            bad += 1
            print(f"   {subj}: chain broken  declared={str(d)[:12]} md={str(pm)[:12]} owner={str(oa)[:12]}")
    print(f"   coherent chains: {n - bad}/{n}")
    print("\n   NOTE: this proves the acceptance package is internally bound.")
    print("   It does NOT prove the upstream (OCR/annotation) produced it from the PDF —")
    print("   that requires the Papers-side ledger, verified separately.")


if __name__ == "__main__":
    main()
