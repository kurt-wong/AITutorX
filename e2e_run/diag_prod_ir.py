"""生产路径逐单元 IR 诊断（只读）。

对「真实 LLM 标注载荷 + 真实 source lines/figures」跑真实
SourceResolver → IRBuilder → validate_ir → Compiler，
逐单元输出 semantic_status 判定依据。不改任何生产代码、不写业务表。

用途：GateService.run 把 semantic_status != 'ready' 的 root unit 静默加入 skipped，
只在返回值里给 unit_id；本工具给出每单元的具体 invariant 违反项。
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(_BACKEND))
os.environ.setdefault("MIMO_MODEL", "mimo-v2.6-pro")

from app.core.config import settings  # noqa: E402

OUT = Path(r"D:\Project\AITutor-X\e2e_run\diag-prod-ir.json")


def ts() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


async def main() -> None:
    import asyncpg
    from app.domains.compile import content_roles_for, map_canonical_type
    from app.domains.compile.compiler import Compiler
    from app.domains.compile.ir import IRBuilder, validate_ir
    from app.domains.resolver.resolver import (
        SourceFigureView, SourceLineView, SourceResolver)

    url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    c = await asyncpg.connect(url)

    ann = await c.fetchrow(
        "select id,source_version_id,payload,status,annotation_schema_version "
        "from semantic_annotations order by logical_execution_hash limit 1")
    payload = ann["payload"]
    if isinstance(payload, str):
        payload = json.loads(payload)
    sv = ann["source_version_id"]

    lines = tuple(
        SourceLineView(
            line_ref=r["line_ref"], text=r["text"], seq=r["seq"],
            page_no=r["page_no"], line_no_in_page=r["line_no_in_page"])
        for r in await c.fetch(
            "select line_ref,text,seq,page_no,line_no_in_page "
            "from document_source_lines where source_version_id=$1 order by seq", sv))
    frows = await c.fetch(
        "select figure_id,page_no,bbox,placement,source,object_key,figure_hash "
        "from source_figures where source_version_id=$1", sv)
    figures = tuple(
        SourceFigureView(
            figure_id=r["figure_id"], page_no=r["page_no"], bbox=r["bbox"],
            placement=r["placement"], source=r["source"],
            object_key=r["object_key"], figure_hash=r["figure_hash"])
        for r in frows)

    run = SourceResolver(source_version_id=sv, lines=lines, figures=figures).resolve(payload)
    ir = IRBuilder.build(run, payload, sv, ann["id"])
    validated = validate_ir(ir)
    span_map = {s.span_id: s for s in run.resolved_spans}
    line_map = {l.line_ref: l for l in lines}
    compiled = Compiler(span_map, line_map).compile(validated)

    def node_problems(node) -> list[str]:
        out: list[str] = []
        if node.semantic_status == "unknown":
            return ["[unknown 已声明]"]
        canon = (map_canonical_type(node.original_question_type)
                 if node.original_question_type is not None else None)
        if node.original_question_type is not None and canon is None:
            out.append(f"unknown canonical type {node.original_question_type!r}")
        by_role = {x.role: x for x in node.content}
        if node.unit_type != "composite_unit":
            req = content_roles_for(canon)
            if req.get("stem") == "required":
                x = by_role.get("stem")
                if x is None:
                    out.append("stem not declared")
                elif x.span_id is None:
                    out.append("stem unresolved")
            if req.get("answer") == "required":
                x = by_role.get("answer")
                if x is None:
                    out.append("answer not declared")
                elif x.span_id is None:
                    out.append("answer unresolved")
            if req.get("options") == "required_for_choice":
                if not any(x.role == "option" for x in node.content):
                    out.append("options missing for choice type")
            for x in node.content:
                if x.unsupported:
                    out.append(f"unsupported content role {x.role}")
                elif x.span_id is None:
                    out.append(f"role {x.role} unresolved")
        for s in node.sub_questions:
            out.extend(f"sub[{s.unit_id}]: {p}" for p in node_problems(s))
        if node.unit_type == "composite_unit":
            if not node.shared_components:
                out.append("composite has no shared component material")
            for sc in node.shared_components:
                if sc.span_id is None:
                    out.append(f"shared component {sc.role} unresolved")
            if any(s.semantic_status != "ready" for s in node.sub_questions):
                out.append("composite sub_question not ready")
        return out

    units = []
    for n in validated.units:
        units.append({
            "unit_id": n.unit_id, "unit_type": n.unit_type,
            "original_question_type": n.original_question_type,
            "canonical_type": map_canonical_type(n.original_question_type),
            "semantic_status": n.semantic_status,
            "content_roles": [x.role for x in n.content],
            "content_span_ids": [x.span_id for x in n.content],
            "shared_roles": [x.role for x in n.shared_components],
            "sub_units": [s.unit_id for s in n.sub_questions],
            "problems": node_problems(n),
        })

    tally = {}
    for u in units:
        tally[u["semantic_status"]] = tally.get(u["semantic_status"], 0) + 1

    ev = {
        "artifact": "DIAG-PROD-IR", "at": ts(),
        "annotation_id": str(ann["id"]),
        "annotation_status": ann["status"],
        "annotation_schema_version": ann["annotation_schema_version"],
        "source_version_id": str(sv),
        "resolver": {
            "lines": len(lines), "figures": len(figures),
            "resolved_spans": len(run.resolved_spans),
            "unresolved_references": [
                {"ref": str(getattr(u, "ref", u)), "reason": str(getattr(u, "reason", ""))}
                for u in run.unresolved_references],
            "unresolved_count": len(run.unresolved_references),
        },
        "ir": {"top_level_units": len(validated.units), "tally": tally},
        "units": units,
        "compiled": {
            "leaves": len(compiled.leaves),
            "materials": len(compiled.materials),
            "leaf_unit_ids": [getattr(x, "unit_id", None) for x in compiled.leaves],
        },
    }
    OUT.write_text(json.dumps(ev, ensure_ascii=False, indent=2, default=str),
                   encoding="utf-8")

    print(f"=== DIAG-PROD-IR @ {ev['at']} ===")
    print(f"annotation: id={ann['id']} status={ann['status']} "
          f"schema={ann['annotation_schema_version']}")
    print(f"resolver: lines={len(lines)} figures={len(figures)} "
          f"spans={len(run.resolved_spans)} unresolved={len(run.unresolved_references)}")
    for u in ev["resolver"]["unresolved_references"][:15]:
        print("   UNRESOLVED:", json.dumps(u, ensure_ascii=False)[:200])
    print(f"IR tally: {tally}")
    for u in units:
        print(f"--- {u['unit_id']} type={u['unit_type']} orig={u['original_question_type']!r} "
              f"canon={u['canonical_type']!r} status={u['semantic_status']}")
        print(f"    roles={u['content_roles']} spans={u['content_span_ids']}")
        for p in u["problems"]:
            print(f"    PROBLEM: {p}")
    print(f"compiled: leaves={len(compiled.leaves)} materials={len(compiled.materials)}")
    print(f"\n=== WRITTEN {OUT} ===")
    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
