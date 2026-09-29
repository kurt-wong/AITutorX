"""E2E 诊断：用真实 V3 模块构建 annotation payload / ResolvedRun / IR，逐单元输出
semantic_status 判定依据。只读诊断，不修改任何生产代码，不写任何数据文件。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(_BACKEND))
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://aitutors:change-me@localhost:5432/aitutors",
)

from scripts.preprocessing_consumer.annotation_adapter import (  # noqa: E402
    manifest_to_annotation_payload,
)
from scripts.preprocessing_consumer.manifest_reader import load_manifest  # noqa: E402
from scripts.preprocessing_consumer.runner_b2 import (  # noqa: E402
    _build_resolved_run,
    _verify_identity_boundary,
)
from app.domains.compile.ir import IRBuilder, validate_ir  # noqa: E402
from app.domains.compile.compiler import Compiler  # noqa: E402
from app.domains.compile import (  # noqa: E402
    content_roles_for,
    map_canonical_type,
)

CORPUS = Path(r"D:\Project\AITutor-X\e2e_run\golden")
MANIFEST = Path(os.environ.get(
    "DIAG_MANIFEST", str(CORPUS / "pac-c02-01.manifest.json")))
IR_PATH = Path(os.environ.get(
    "DIAG_IR", r"D:\Project\Papers\data\resolver_ref_r52\resolver_ir.json"))


def node_problems(node) -> list[str]:
    """复刻 validate_ir/_validate_node 的问题清单（同一规则，仅用于报告）。"""
    problems: list[str] = []
    if node.semantic_status == "unknown":
        return ["[unknown 已声明，不触发常规校验]"]

    canonical = None
    if node.original_question_type is not None:
        canonical = map_canonical_type(node.original_question_type)
        if canonical is None:
            problems.append(
                f"unknown canonical type {node.original_question_type!r}")
    content_by_role = {c.role: c for c in node.content}

    if node.unit_type != "composite_unit":
        required_roles = content_roles_for(canonical)
        if required_roles.get("stem") == "required":
            c = content_by_role.get("stem")
            if c is None:
                problems.append("stem not declared")
            elif c.span_id is None:
                problems.append("stem unresolved")
        if required_roles.get("answer") == "required":
            c = content_by_role.get("answer")
            if c is None:
                problems.append("answer not declared")
            elif c.span_id is None:
                problems.append("answer unresolved")
        if required_roles.get("options") == "required_for_choice":
            has_opts = any(c.role == "option" for c in node.content)
            if not has_opts:
                problems.append("options missing for choice type")
        for c in node.content:
            if c.unsupported:
                problems.append(
                    f"unsupported content role {c.role} (figure_refs/blank deferred)")
            elif c.span_id is None:
                problems.append(f"role {c.role} unresolved")

    for s in node.sub_questions:
        problems.extend(f"sub[{s.unit_id}]: {p}" for p in node_problems(s))

    if node.unit_type == "composite_unit":
        if not node.shared_components:
            problems.append("composite has no shared component material")
        for sc in node.shared_components:
            if sc.span_id is None:
                problems.append(f"shared component {sc.role} unresolved")
        shared_by_role = {c.role: c for c in node.shared_components}
        for r in node.relations:
            sc = shared_by_role.get(r)
            if sc is None:
                problems.append(
                    f"material_dependency target {r!r} not in shared_components")
            elif sc.span_id is None:
                problems.append(f"material_dependency target {r!r} span unresolved")
        if any(s.semantic_status != "ready" for s in node.sub_questions):
            problems.append("composite sub_question not ready")
    return problems


def main() -> None:
    manifest = load_manifest(MANIFEST)
    source_path = Path(manifest.source_file)

    gate = _verify_identity_boundary(
        manifest_path=MANIFEST, source_path=source_path, resolver_ir_path=IR_PATH)
    print("=== IDENTITY GATE ===")
    print(json.dumps(gate, ensure_ascii=False, indent=2))

    payload = manifest_to_annotation_payload(manifest)
    print("\n=== ADAPTER known_gaps ===")
    for g in payload.get("known_gaps", []):
        print(f"  [{g['code']}] {g['unit_id']}: {g['detail'][:110]}")
    print(f"  (known_gaps total = {len(payload.get('known_gaps', []))})")
    print(f"  payload top keys = {list(payload.keys())}")

    from scripts.preprocessing_consumer.source_loader import load_source_lines
    source_lines = load_source_lines(source_path)
    resolved_run = _build_resolved_run(manifest, source_lines, sv_id="sv-diag")

    ir = IRBuilder.build(resolved_run, payload, "sv-diag", "ann-diag")
    validated = validate_ir(ir)

    print(f"\n=== IR: {len(validated.units)} top-level units, "
          f"{len(resolved_run.resolved_spans)} spans, "
          f"{len(resolved_run.unresolved_references)} unresolved ===\n")

    ready = incomplete = unknown = 0
    for node in validated.units:
        probs = node_problems(node)
        st = node.semantic_status
        if st == "ready":
            ready += 1
        elif st == "unknown":
            unknown += 1
        else:
            incomplete += 1
        canon = map_canonical_type(node.original_question_type)
        print(f"--- {node.unit_id}  type={node.unit_type}  "
              f"orig={node.original_question_type!r}  canonical={canon!r}  "
              f"status={st}")
        print(f"    content_roles={[c.role for c in node.content]}  "
              f"shared={[c.role for c in node.shared_components]}  "
              f"subs={[s.unit_id for s in node.sub_questions]}  "
              f"relations={list(node.relations)}")
        for p in probs:
            print(f"    PROBLEM: {p}")

    print(f"\n=== IR TALLY: ready={ready} incomplete={incomplete} unknown={unknown} ===")

    line_map = {sl.line_ref: sl for sl in source_lines}
    span_map = {s.span_id: s for s in resolved_run.resolved_spans}
    compiled = Compiler(span_map, line_map).compile(validated)
    print(f"=== COMPILED: leaves={len(compiled.leaves)} "
          f"materials={len(compiled.materials)} ===")
    for m in compiled.materials:
        print(f"   material: {m}")


if __name__ == "__main__":
    main()
