"""READ-ONLY: independently verify EVIDENCE_BINDING_INVENTORY.json.

The risk with a binding inventory is that `sha_match: true` / "9/9" is a written
constant rather than a computed result (the "auto-fix" failure mode this project
has hit repeatedly). So: recompute every hash from the files and compare with
what the inventory claims, and verify the binding relations themselves.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EA = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> None:
    inv_p = EA / "EVIDENCE_BINDING_INVENTORY.json"
    if not inv_p.exists():
        print("!! inventory missing:", inv_p)
        return
    inv = json.loads(inv_p.read_text(encoding="utf-8"))
    print("=" * 96)
    print("EVIDENCE_BINDING_INVENTORY.json — keys:", list(inv.keys())[:12])

    rows = inv.get("subjects") or inv.get("corpus") or inv.get("entries") or []
    if isinstance(rows, dict):
        rows = list(rows.values())
    print(f"entries: {len(rows)}\n")

    ok_pdf = ok_md = ok_bind = 0
    claims_true = claims_false = 0
    problems = []

    for r in rows:
        subj = r.get("subject") or Path(str(r.get("manifest", ""))).stem
        print("-" * 96)
        print(f"{subj}")

        # --- manifest side
        man_p = r.get("manifest") or r.get("manifest_path")
        man_path = (EA / man_p) if man_p and not Path(str(man_p)).is_absolute() else Path(str(man_p or ""))
        man_sha_actual = sha(man_path) if man_path.exists() else None
        man_sha_claim = r.get("manifest_sha256")
        # --- declared source (from the manifest itself)
        decl = r.get("declared_source_file")
        decl_sha_claim = r.get("declared_source_sha256") or r.get("source_content_sha256")
        decl_path = Path(str(decl)) if decl else None
        decl_sha_actual = sha(decl_path) if decl_path and decl_path.exists() else None
        # --- copy under 02/03
        md02 = r.get("md_02") or r.get("preprocessing_md")
        md02_path = (EA / md02) if md02 else None
        md02_sha = sha(md02_path) if md02_path and md02_path.exists() else None
        # --- pdf
        pdf = r.get("pdf") or r.get("source_pdf")
        pdf_path = (EA / pdf) if pdf else None
        pdf_sha_actual = sha(pdf_path) if pdf_path and pdf_path.exists() else None

        print(f"   manifest           : {man_p}")
        print(f"      exists={man_path.exists()} claim={str(man_sha_claim)[:16]} actual={str(man_sha_actual)[:16]}"
              f" match={man_sha_claim == man_sha_actual}")
        print(f"   declared_source    : {decl}")
        print(f"      exists={decl_path.exists() if decl_path else None} "
              f"declared_sha={str(decl_sha_claim)[:16]} actual_sha={str(decl_sha_actual)[:16]}"
              f" match={decl_sha_claim == decl_sha_actual}")
        if decl_sha_actual and decl_path and decl_path.exists():
            if decl_sha_actual == decl_path and False:
                pass
        print(f"   02 md              : {md02}")
        print(f"      exists={md02_path.exists() if md02_path else None} sha={str(md02_sha)[:16]}"
              f"  ==declared_source:{md02_sha == decl_sha_actual}")
        print(f"   pdf                : {pdf}")
        print(f"      exists={pdf_path.exists() if pdf_path else None} actual={str(pdf_sha_actual)[:16]}"
              f" claim={str(r.get('pdf_sha256'))[:16]} match={r.get('pdf_sha256') == pdf_sha_actual}")

        # relations
        if decl_sha_actual and md02_sha and decl_sha_actual == md02_sha:
            ok_md += 1
        if r.get("pdf_sha256") == pdf_sha_actual and pdf_sha_actual:
            ok_pdf += 1
        if decl_sha_claim == decl_sha_actual:
            ok_bind += 1
        if r.get("sha_match") is True:
            claims_true += 1
            if not (decl_sha_actual == md02_sha == decl_sha_claim):
                claims_false += 1
                problems.append((subj, "sha_match=true but recomputation disagrees"))

    print("\n" + "=" * 96)
    print("INDEPENDENT RECOMPUTATION")
    print("=" * 96)
    print(f"   declared_source sha matches actual : {ok_bind}/{len(rows)}")
    print(f"   02 md sha == declared source sha   : {ok_md}/{len(rows)}")
    print(f"   pdf sha claim matches actual       : {ok_pdf}/{len(rows)}")
    print(f"   entries claiming sha_match=true    : {claims_true}")
    print(f"   ...of which recomputation DISAGREES: {claims_false}")
    for p in problems:
        print(f"      !! {p}")
    if not problems and rows:
        print("\n   >>> every claim recomputes correctly (not a written constant).")


if __name__ == "__main__":
    main()
