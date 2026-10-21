"""READ-ONLY: is the answer BLOB a line-selection miss or a boundary miss?

For every choice unit: within the manifest-declared answer_lines range, list the
lines and mark (a) which line holds 故选/答案 + letter, (b) whether that line's
content is EXCLUSIVELY the answer token by the project's own G3 parser-compat
allowance (comment in gate/grammar.py: '字母 + 句号' forms like `D.`).

If the token-bearing line is token-exclusive, then a deterministic
'prefer the token-exclusive line inside the declared answer range' rule is
derivable and provable from source alone -> it is NOT answer->option inference
(it is answer-slice selection), and it is testable.

If instead the token is glued to explanation prose, no such rule exists.
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
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_3r\OPTION-EVIDENCE-V2")

sys.path.insert(0, str(BACKEND))
for _line in (BACKEND / ".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

from scripts.preprocessing_consumer.manifest_reader import find_manifests, load_manifest  # noqa: E402

# token-exclusive line: optional 【答案】 marker + optional qn prefix + letter + optional 。
TOKEN_LINE = re.compile(r"^\s*(?:【答案】\s*)?(?:\d{1,3}\s*[.．、]\s*)?([A-Ha-h])\s*[。．.]?\s*$")
TOKEN_ANYWHERE = re.compile(r"(?:故选|答案)\s*[:：]?\s*([A-Ha-h])(?![A-Za-z])")


def main() -> None:
    stats = Counter()
    samples = []
    per_paper = Counter()
    tokens_exclusive = []
    tokens_glued = []
    token_starved = []

    for p in find_manifests(CORPUS):
        paper = p.parent.name
        m = load_manifest(p)
        sf = Path(m.source_file)
        if not sf.is_absolute():
            sf = CORPUS / sf
        texts = sf.read_text(encoding="utf-8").splitlines()
        for u in m.units:
            al = u.answer_lines
            if not al or u.original_question_type not in (
                "single_choice", "multiple_choice", "true_false"
            ):
                continue
            lo, hi = al[0], al[1]
            lo = max(1, min(lo, len(texts)))
            hi = max(lo, min(hi, len(texts)))
            block = texts[lo - 1:hi]
            per_paper[paper] += 1
            stats["answer_blocks"] += 1
            stats["span_1_line" if lo == hi else "span_multi_line"] += 1

            excl, glued, anyhit = [], [], []
            for i, t in enumerate(block, start=lo):
                mt = TOKEN_LINE.match(t)
                if mt:
                    excl.append((i, mt.group(1).upper(), t.strip()[:50]))
                ma = TOKEN_ANYWHERE.search(t)
                if ma:
                    anyhit.append((i, ma.group(1).upper(), t.strip()[:70]))
                    if not mt:
                        glued.append((i, ma.group(1).upper(), t.strip()[:70]))

            rec = {"paper": paper, "unit": u.unit_id, "answer_lines": [lo, hi],
                   "n_lines": hi - lo + 1, "exclusive": excl, "glued": glued}
            if excl:
                tokens_exclusive.append(rec)
            elif glued:
                tokens_glued.append(rec)
            else:
                token_starved.append(rec)

    stats["blocks_with_token_exclusive_line"] = len(tokens_exclusive)
    stats["blocks_with_token_only_glued_to_prose"] = len(tokens_glued)
    stats["blocks_with_no_故选/答案_token_at_all"] = len(token_starved)

    print("=" * 92)
    print("ANSWER-BLOCK SHAPE — is a deterministic line-selection rule derivable?")
    print("=" * 92)
    for k, v in stats.items():
        print(f"   {k:<44}{v}")
    print()
    print("blocks WITH a token-exclusive line (rule derivable):")
    for r in tokens_exclusive[:18]:
        print(f"   {r['paper']}/{r['unit']:<10} lines={r['answer_lines']} n={r['n_lines']:<3} "
              f"excl={r['exclusive'][:2]}")
    print()
    print("blocks where the token is GLUED to prose (rule NOT derivable):")
    for r in tokens_glued[:18]:
        print(f"   {r['paper']}/{r['unit']:<10} lines={r['answer_lines']} n={r['n_lines']:<3} "
              f"glued={r['glued'][:1]}")
    print()
    print("blocks with NO 故选/答案 token at all:")
    for r in token_starved[:18]:
        print(f"   {r['paper']}/{r['unit']:<10} lines={r['answer_lines']} n={r['n_lines']}")
    print()
    print("by paper (choice units):", dict(per_paper))

    OUT.joinpath("_p14b_answer_block_shape.json").write_text(
        json.dumps({
            "stats": dict(stats),
            "exclusive": tokens_exclusive,
            "glued": tokens_glued,
            "starved": token_starved,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {OUT / '_p14b_answer_block_shape.json'}")


if __name__ == "__main__":
    main()
