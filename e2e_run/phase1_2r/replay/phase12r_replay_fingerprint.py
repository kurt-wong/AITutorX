"""PHASE1.2R P0-A — sealed read-only replay with content fingerprints.

Locked table set (13) per DSH instruction:
  documents · document_source_versions · document_source_lines · document_source_spans
  document_active_sources · semantic_annotations · admission_candidates · admission_events
  questions · question_instances · instance_role_contents · unit_groups · materials

Fingerprint algorithm (locked):
  per-table fingerprint = sha256 over rows sorted by primary key,
  each row serialized as canonical JSON (sort_keys=True, separators=(',',':')),
  rows joined with '\\n'.
  Always record row_count AND fingerprint (count alone is insufficient).

Usage:
  python phase12r_replay_fingerprint.py snapshot --label before
  python phase12r_replay_fingerprint.py replay
  python phase12r_replay_fingerprint.py snapshot --label after
  python phase12r_replay_fingerprint.py diff

Business code is NOT modified. Replay is compute-only (Resolver/IR/Compiler/evaluate).
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BACKEND = Path(r"D:\Project\AITutors-v3\backend")
OUT = Path(r"D:\Project\AITutor-X\e2e_run\phase1_2r\replay")
sys.path.insert(0, str(BACKEND))
# load backend/.env before app.core.config Settings()
_env = BACKEND / ".env"
if _env.exists():
    for _line in _env.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if not _line or _line.startswith("#") or "=" not in _line:
            continue
        _k, _v = _line.split("=", 1)
        os.environ.setdefault(_k.strip(), _v.strip())

from sqlalchemy import text  # noqa: E402

TABLES = [
    "documents",
    "document_source_versions",
    "document_source_lines",
    "document_source_spans",
    "document_active_sources",
    "semantic_annotations",
    "admission_candidates",
    "admission_events",
    "questions",
    "question_instances",
    "instance_role_contents",
    "unit_groups",
    "materials",
]

# PK orders for stable row sort (fallback: full row string)
PKS = {
    "documents": ["id"],
    "document_source_versions": ["id"],
    "document_source_lines": ["id"],
    "document_source_spans": ["id"],
    "document_active_sources": ["document_id", "role"],
    "semantic_annotations": ["id"],
    "admission_candidates": ["id"],
    "admission_events": ["id"],
    "questions": ["id"],
    "question_instances": ["id"],
    "instance_role_contents": ["instance_id", "role", "role_index"],
    "unit_groups": ["id"],
    "materials": ["id"],
}


def _canon(value: Any) -> Any:
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _canon(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_canon(v) for v in value]
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _row_fp(rows: list[dict]) -> str:
    parts = []
    for r in rows:
        parts.append(json.dumps(_canon(r), sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    payload = "\n".join(parts).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


async def snapshot(label: str) -> Path:
    from app.db.session import async_session_maker

    OUT.mkdir(parents=True, exist_ok=True)
    snap: dict[str, Any] = {
        "label": label,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "tables": {},
        "git_binding": {
            "branch": "od01-r3-convergence",
            "head": "39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4",
            "match_norm": "match-norm/v1.1 (worktree dirty 015cdfa vs HEAD 73badc3)",
        },
    }
    async with async_session_maker() as s:
        for t in TABLES:
            pks = PKS[t]
            order = ", ".join(pks)
            r = await s.execute(text(f"select * from {t} order by {order}"))
            cols = list(r.keys())
            rows = [dict(zip(cols, row)) for row in r.fetchall()]
            snap["tables"][t] = {
                "row_count": len(rows),
                "pk_order": pks,
                "fingerprint_sha256": _row_fp(rows),
                "columns": cols,
            }
    path = OUT / f"snapshot_{label}.json"
    path.write_text(json.dumps(snap, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"wrote {path}")
    return path


async def replay() -> Path:
    from app.db.session import async_session_maker
    from app.repositories.source_repository import SourceRepository
    from app.domains.resolver.resolver import SourceResolver
    from app.domains.resolver.span import SourceLineView, SourceFigureView
    from app.domains.compile.ir import IRBuilder
    from app.domains.compile.compiler import Compiler
    from app.domains.gate.policy import evaluate

    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    async with async_session_maker() as s:
        r = await s.execute(
            text(
                """
                select sv.id as sv_id, sa.id as ann_id, sa.payload
                from document_source_versions sv
                join semantic_annotations sa on sa.source_version_id = sv.id
                where sv.status = 'sealed'
                """
            )
        )
        pairs = r.fetchall()
        for sv_id, ann_id, payload in pairs:
            if isinstance(payload, str):
                payload = json.loads(payload)
            src = SourceRepository(s)
            lines = tuple(
                SourceLineView(
                    line_ref=x.line_ref,
                    text=x.text,
                    seq=x.seq,
                    page_no=x.page_no,
                    line_no_in_page=x.line_no_in_page,
                )
                for x in await src.get_lines_by_version(sv_id)
            )
            figures = tuple(
                SourceFigureView(
                    figure_id=f.figure_id,
                    page_no=f.page_no,
                    bbox=f.bbox,
                    placement=f.placement,
                    source=f.source,
                    object_key=f.object_key,
                    figure_hash=f.figure_hash,
                )
                for f in await src.get_figures_by_version(sv_id)
            )
            run = SourceResolver(source_version_id=sv_id, lines=lines, figures=figures).resolve(payload)
            ir = IRBuilder().build(
                resolved_run=run,
                annotation_payload=payload,
                source_version_id=sv_id,
                annotation_id=ann_id,
            )
            compiled = Compiler(
                {sp.span_id: sp for sp in run.resolved_spans},
                {l.line_ref: l for l in lines},
            ).compile(ir)
            gate = Counter()
            ready = 0
            for root in ir.units:
                if root.semantic_status != "ready":
                    continue
                ready += 1
                g = evaluate(root=root, ir=ir, compiled=compiled, resolved_run=run)
                gate[g.get("decision")] += 1
            results.append(
                {
                    "source_version_id": str(sv_id),
                    "annotation_id": str(ann_id),
                    "lines": len(lines),
                    "resolved_spans": len(run.resolved_spans),
                    "unresolved": len(run.unresolved_references),
                    "ir_status": dict(Counter(u.semantic_status for u in ir.units)),
                    "ir_ready": ready,
                    "gate_if_ready": dict(gate),
                    "mode": "read_only_compute",
                    "writes_attempted": False,
                }
            )
    path = OUT / "replay_run.json"
    path.write_text(
        json.dumps(
            {
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "mode": "read_only_compute (SourceResolver/IRBuilder/Compiler/evaluate)",
                "gate_service_run_called": False,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"wrote {path}")
    return path


def diff() -> Path:
    before = json.loads((OUT / "snapshot_before.json").read_text(encoding="utf-8"))
    after = json.loads((OUT / "snapshot_after.json").read_text(encoding="utf-8"))
    table_diff = {}
    for t in TABLES:
        b = before["tables"][t]
        a = after["tables"][t]
        if b != a:
            table_diff[t] = {
                "row_count": [b["row_count"], a["row_count"]],
                "fingerprint": [b["fingerprint_sha256"], a["fingerprint_sha256"]],
            }
    out = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "tables_compared": TABLES,
        "count_diff": {
            t: [before["tables"][t]["row_count"], after["tables"][t]["row_count"]]
            for t in TABLES
            if before["tables"][t]["row_count"] != after["tables"][t]["row_count"]
        },
        "content_diff": table_diff,
        "identical": not table_diff,
    }
    path = OUT / "diff_before_after.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {path} identical={out['identical']}")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["snapshot", "replay", "diff"])
    ap.add_argument("--label", default="before")
    args = ap.parse_args()
    if args.cmd == "snapshot":
        asyncio.run(snapshot(args.label))
    elif args.cmd == "replay":
        asyncio.run(replay())
    else:
        diff()


if __name__ == "__main__":
    main()
