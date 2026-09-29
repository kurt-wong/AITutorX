"""Engineering Verification Execution — full production chain with LIVE MIMO.

性质：临时验证工具（Owner task §一.1「允许修改：临时验证工具」）。
不修改 AITutors-v3 任何生产代码；只通过依赖注入把「正确接线的 MIMO provider」
交给真实 TaskExecutor / LLMExecutor / AnnotationService / GateService。

为什么需要本工具（不得误读为生产改动）：
  app/ai/gateway.py::build_gateway 在 live 模式只构造 HTTPLLMProvider(name="ollama",
  api_key=None, base_url=settings.ollama_base_url)。settings.mimo_* 存在但未被该 factory
  读取。修 factory = V3 production code modification = LIMIT-AUTH §6 Forbidden Scope，
  故 STOP，改用构造期注入（同一 HTTPLLMProvider 类，同一 LLMGateway / LLMExecutor /
  AnnotationService / GateService 生产实现）。

跑的是真实生产链：
  import → Task(queued) → TaskExecutor.run_once
    → _seal_stage       (SealService + NativeTextProvider 真实 PDF 文本抽取)
    → _quality_check_stage (SourceQualityGate)
    → _annotation_stage (build_annotation_prompt → LLMExecutor → LLMGateway → MIMO HTTP)
                        (AnnotationService: JSON parse → FORBIDDEN_FIELDS 校验 → 落库)
    → _compile_stage    (GateService.run: SourceResolver → IRBuilder → Compiler
                         → evaluate(gate) → AdmissionService)
    → _complete_task

证据纪律：本脚本输出 command / timestamp / input hash / output hash / DB before-after。
禁止在本文件写入任何 API Key / Password / Token / Secret（.env 供配置）。
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_BACKEND = Path(r"D:\Project\AITutors-v3\backend")
sys.path.insert(0, str(_BACKEND))

# 模型名走环境变量覆盖，不改 .env、不硬编码密钥。
# 实测 api.xiaomimimo.com/v1/models 返回 mimo-v2.6-pro；.env 的 mimo-x-pro-preview
# 被 API 拒绝 "Unsupported model"（见报告 CONFIG-001）。
os.environ.setdefault("MIMO_MODEL", "mimo-v2.6-pro")
os.environ.setdefault("LLM_GATEWAY_MODE", "live")

from app.core.config import settings  # noqa: E402

OUT_DIR = Path(r"D:\Project\AITutor-X\e2e_run")
# 输入可用 E2E_INPUT 覆盖，以便同一工具对多份真实输入分别留证（每份独立 artifact）。
INPUT = Path(os.environ.get(
    "E2E_INPUT", str(OUT_DIR / "inputs" / "caseA_real.pdf")))
ARTIFACT = Path(os.environ.get(
    "E2E_ARTIFACT", str(OUT_DIR / "e2e-live-full-chain.json")))


def ts() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# --------------------------------------------------------------------------
# DB evidence（真实表名，不自造）
# --------------------------------------------------------------------------
_TABLES = [
    "documents", "document_source_versions", "document_source_lines",
    "document_source_spans", "source_figures",
    "semantic_annotations", "resolved_spans", "ir_units",
    "admission_candidates", "admission_events",
    "questions", "question_instances", "materials", "material_links",
    "unit_groups", "unit_group_members", "instance_role_contents",
    "validation_events", "evidence_references",
    "tasks", "task_claims", "llm_call_audit", "budget",
]


async def snapshot(c, label: str) -> dict:
    existing = {
        r["tablename"] for r in await c.fetch(
            "select tablename from pg_tables where schemaname='public'")
    }
    out = {"label": label, "at": ts()}
    counts = {}
    for t in _TABLES:
        if t in existing:
            counts[t] = await c.fetchval(f'select count(*) from "{t}"')
    out["counts"] = counts
    out["missing_tables"] = [t for t in _TABLES if t not in existing]
    return out


def _jsonable(rows):
    out = []
    for r in rows:
        row = dict(r)
        for k, v in list(row.items()):
            if hasattr(v, "isoformat"):
                row[k] = v.isoformat()
            elif not isinstance(v, (str, int, float, bool, type(None))):
                row[k] = str(v)
        out.append(row)
    return out


# --------------------------------------------------------------------------
# 输入层：PDF / DOC / DOCX / JPG / PNG 支持矩阵（真实 ImportService 拒绝路径）
# --------------------------------------------------------------------------
async def input_layer_matrix(DocumentImportService, ImportError_, session_factory):
    results = []
    cases = [
        ("real_pdf", ".pdf", INPUT.read_bytes() if INPUT.exists() else b"%PDF-1.4 test"),
        ("docx_stub", ".docx", b"PK\x03\x04stub-docx-bytes-for-ext-matrix"),
        ("doc_stub", ".doc", b"\xd0\xcf\x11\xe0stub-doc-bytes"),
        ("jpg_stub", ".jpg", b"\xff\xd8\xff\xe0stub-jpeg-bytes"),
        ("png_stub", ".png", b"\x89PNG\r\n\x1a\nstub-png-bytes"),
        ("txt_stub", ".txt", b"plain text"),
    ]
    for name, ext, data in cases:
        rec = {"case": name, "ext": ext, "bytes": len(data),
               "sha256": hashlib.sha256(data).hexdigest(), "at": ts()}
        try:
            async with session_factory() as s:
                doc, task, is_new = await DocumentImportService(s).import_file(
                    file_bytes=data, file_name=f"extmatrix_{name}{ext}",
                    created_by="e2e-verify")
                await s.commit()
            rec["outcome"] = "ACCEPTED"
            rec["document_id"] = str(doc.id)
            rec["is_new"] = is_new
            rec["task_id"] = str(task.id) if task else None
        except ImportError_ as exc:
            rec["outcome"] = "REJECTED"
            rec["error"] = f"{type(exc).__name__}: {exc}"
        except Exception as exc:  # noqa: BLE001
            rec["outcome"] = "ERROR"
            rec["error"] = f"{type(exc).__name__}: {exc}"
        results.append(rec)
    return results


# --------------------------------------------------------------------------
async def main() -> dict:
    from app.db.session import async_session_maker
    import asyncpg

    from app.ai.gateway import LLMGateway
    from app.ai.ocr.providers import NativeTextProvider
    from app.ai.providers.http import HTTPLLMProvider
    from app.domains.source.import_service import (
        DocumentImportService, ImportError_)
    from app.domains.task.executor import TaskExecutor

    ev: dict = {
        "artifact": "E2E-LIVE-FULL-CHAIN",
        "nature": "Engineering Verification Execution (NOT LIMIT-AUTH Phase 6)",
        "started_at": ts(),
        "environment": {
            "python": sys.version.split()[0],
            "app_env": settings.app_env,
            "llm_gateway_mode": settings.llm_gateway_mode,
            "database_url_host": settings.database_url.split("@")[-1],
            "mimo_base_url": settings.mimo_base_url,
            "mimo_model_used": settings.mimo_model,
            "mimo_api_key_set": bool(settings.mimo_api_key),
            "api_key_value": "NOT RECORDED (never log secrets)",
        },
    }

    url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    pg = await asyncpg.connect(url)
    ev["db_before"] = await snapshot(pg, "BEFORE")

    # ---- 输入层支持矩阵 -------------------------------------------------
    ev["input_layer_matrix"] = await input_layer_matrix(
        DocumentImportService, ImportError_, async_session_maker)

    # ---- 真实文档导入（幂等证据） ---------------------------------------
    data = INPUT.read_bytes()
    ev["input"] = {
        "path": str(INPUT), "file_name": INPUT.name, "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(), "at": ts(),
    }
    async with async_session_maker() as s:
        doc, task, is_new = await DocumentImportService(s).import_file(
            file_bytes=data, file_name=INPUT.name, created_by="e2e-verify")
        await s.commit()
    ev["import"] = {"document_id": str(doc.id), "is_new": is_new,
                    "task_id": str(task.id) if task else None, "at": ts()}

    # 若幂等（is_new=False 且无新 task）：优先复用该 document 已有的 queued task，
    # 避免每次运行都新入队一条同文档 task（否则队列堆积、并把无关 task 的结果混入本次证据）。
    if task is None:
        from app.domains.task.service import TaskService
        existing = await pg.fetchrow(
            "select id from tasks where status='queued' and task_params->>'document_id'=$1 "
            "order by created_at limit 1", str(doc.id))
        if existing is not None:
            ev["import"]["reused_queued_task_id"] = str(existing["id"])
        else:
            import_dir = Path(r"D:\Project\AITutors-v3\backend\data\imports")
            async with async_session_maker() as s:
                task = await TaskService(s).enqueue(
                    task_type="document_ingest",
                    task_params={
                        "document_id": str(doc.id),
                        "original_sha256": ev["input"]["sha256"],
                        "file_name": INPUT.name,
                        "file_path": str(
                            import_dir / f"{ev['input']['sha256']}.pdf"),
                        "file_type": INPUT.suffix.lstrip(".").lower(),
                    },
                    created_by="e2e-verify")
                await s.commit()
            ev["import"]["enqueued_fresh_task_id"] = str(task.id)

    # ---- MIMO provider（真实 HTTP，真实密钥走 settings，不打印） ---------
    provider = HTTPLLMProvider(
        name="mimo",
        api_key=settings.mimo_api_key,
        base_url=settings.mimo_base_url,
        model=settings.mimo_model,
        timeout=settings.llm_request_timeout_seconds * 4,
    )
    gateway = LLMGateway(
        "live",
        allow_live=True,           # Owner task §三 明确授权调用外部 LLM API
        # LLMGateway._live 四前置（app/ai/gateway.py:60-73）：allow_live /
        # task_context is not None / budget_ok / 可解析 live provider。
        # 生产 app/worker/__main__.py:87 只传 allow_live → 恒 GatewayDeniedError
        # （实证见报告 DEFECT-008）。此处按契约补齐后两个前置。
        task_context=object(),
        budget_ok=True,
        live_provider=provider,
    )
    ev["llm_boundary"] = {
        "mode": gateway.mode,
        "allow_live": True,
        "authorization_basis":
            "Owner task §一.2 环境定义「允许：调用外部 API」 + §三 LLM API 调用规则"
            "（第一优先 MIMO V2.6 PRO）",
        "provider_class": type(provider).__name__,
        "provider_name": provider.name,
        "model": settings.mimo_model,
        "endpoint": settings.mimo_base_url + "/chat/completions",
        "mock_used": False,
        "fallback_used": False,
        "deepseek_used": False,
    }

    # ---- 真实生产链 -----------------------------------------------------
    executor = TaskExecutor(
        async_session_maker,
        llm_gateway=gateway,
        # 契约是「可调用」：seal.py:115 `await extractor(file_bytes)`。
        # 与 app/worker/__main__.py:93 一致传 bound method，不是实例。
        ocr_extractor=NativeTextProvider().extract,
        default_provider="mimo",
        default_model=settings.mimo_model,
    )
    t0 = time.time()
    stage_log = []
    # TaskExecutor.run_once 认领的是「队列最旧」的 queued task，不保证是本次入队的
    # 目标 task。循环消费直到目标 task 到达终态（succeeded/failed），否则会把
    # 无关 task 的结果误记成本次 E2E 结果（本 harness 首两轮即犯此错，已更正）。
    tid = (ev["import"].get("enqueued_fresh_task_id")
           or ev["import"].get("reused_queued_task_id")
           or ev["import"].get("task_id"))
    terminal = {"succeeded", "failed"}
    run_once_returns: list[bool] = []
    for i in range(1, 9):
        row = await pg.fetchrow("select status from tasks where id=$1", tid)
        if row and row["status"] in terminal:
            break
        try:
            run_once_returns.append(
                await executor.run_once(worker_id=f"e2e-verify-worker-{i}"))
        except Exception as exc:  # noqa: BLE001
            stage_log.append({"round": i, "status": "FAILED",
                              "error": f"{type(exc).__name__}: {exc}"})
            break
    wall = round(time.time() - t0, 2)

    # run_once() 的返回值语义 = 「本次是否认领并处理了一个 task」，不是「该 task 是否成功」。
    # 成败必须以 DB 中 tasks.status / task_claims.outcome 为准（否则会把 failed 报成
    # COMPLETED —— 本 harness 首轮即犯此错，已更正）。
    row = await pg.fetchrow(
        "select id,status,current_stage,llm_invocations,decided_at from tasks where id=$1", tid)
    claim = await pg.fetchrow(
        "select outcome,error_type from task_claims where task_id=$1 order by start desc limit 1", tid)
    ev["pipeline"] = {
        "run_once_returns": run_once_returns,
        "run_once_return_semantics":
            "True = a task was claimed and processed; NOT a success indicator",
        "task_id": str(tid),
        "task_status_db": row["status"] if row else None,
        "task_current_stage_db": row["current_stage"] if row else None,
        "task_llm_invocations_db": row["llm_invocations"] if row else None,
        "claim_outcome_db": claim["outcome"] if claim else None,
        "claim_error_type_db": claim["error_type"] if claim else None,
        "status": "PASS" if (row and row["status"] == "succeeded") else "FAIL",
        "wall_seconds": wall,
    }
    if stage_log:
        ev["pipeline"]["stage_log"] = stage_log

    # ---- After 快照 + Before/After 差分（EV-07/EV-08） -------------------
    ev["db_after"] = await snapshot(pg, "AFTER")
    delta = {}
    for k in ev["db_before"]["counts"]:
        b = ev["db_before"]["counts"][k]
        a = ev["db_after"]["counts"].get(k, 0)
        if a != b:
            delta[k] = {"before": b, "after": a, "delta": a - b}
    ev["db_delta"] = delta

    # ---- 落库实证（真实表名 + 实测真实列名，不自造） ---------------------
    detail = {
        "tasks": _jsonable(await pg.fetch(
            "select id, task_type, status, current_stage, created_by, created_at,"
            " decided_at, started_at, llm_invocations from tasks")),
        "task_claims": _jsonable(await pg.fetch("select * from task_claims")),
        "documents": _jsonable(await pg.fetch(
            "select id,file_name,file_type,original_sha256,processing_status "
            "from documents")),
        "document_source_versions": _jsonable(await pg.fetch(
            "select id,document_id,artifact_kind,role,provider,page_count,"
            "line_count,text_coverage,status,body_hash,integrity_hash "
            "from document_source_versions")),
        "semantic_annotations": _jsonable(await pg.fetch(
            "select id,source_version_id,annotation_schema_version,prompt_version,"
            "model_config_hash,status,logical_execution_hash "
            "from semantic_annotations")),
        "admission_candidates": _jsonable(await pg.fetch(
            "select id,unit_type,source_version_id,annotation_id,decision_status,"
            "gate_decision,logical_execution_hash from admission_candidates")),
        "admission_events": _jsonable(
            await pg.fetch("select * from admission_events")),
        "questions": _jsonable(await pg.fetch(
            "select id,subject,grade,canonical_question_type,dedup_key,created_at "
            "from questions")),
        "question_instances": _jsonable(await pg.fetch(
            "select id,question_id,document_id,source_version_id,occurrence_key,"
            "question_number,instance_order,logical_execution_hash "
            "from question_instances")),
        "materials": _jsonable(await pg.fetch(
            "select id,subject,grade,source_version_id,text_hash,dedup_key "
            "from materials")),
    }
    ev["db_detail"] = detail

    # ---- LLM 调用实证（本次产生的审计行） --------------------------------
    ev["llm_audit"] = _jsonable(await pg.fetch(
        "select provider,model,status,prompt_chars,output_tokens,total_tokens,"
        "estimated_cost,error_type,logical_execution_stage,start "
        "from llm_call_audit where provider='mimo' order by start desc limit 10"))

    ev["finished_at"] = ts()
    ARTIFACT.write_text(json.dumps(ev, ensure_ascii=False, indent=2, default=str),
                        encoding="utf-8")
    print(f"\n=== ARTIFACT WRITTEN: {ARTIFACT} ===")
    print(json.dumps({
        "pipeline": ev["pipeline"],
        "db_delta": ev["db_delta"],
        "input_layer": [(r["ext"], r["outcome"]) for r in ev["input_layer_matrix"]],
        "llm_audit_rows": len(ev["llm_audit"]),
    }, ensure_ascii=False, indent=2, default=str))
    await pg.close()
    return ev


if __name__ == "__main__":
    asyncio.run(main())
