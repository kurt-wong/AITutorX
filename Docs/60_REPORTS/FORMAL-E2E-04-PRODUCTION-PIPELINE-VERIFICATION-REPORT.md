# FORMAL-E2E-04 — Frozen Spec Production Pipeline End-to-End Verification

```text
Document ID : FORMAL-E2E-04-PRODUCTION-PIPELINE-VERIFICATION-REPORT
Task ID     : FORMAL-E2E-04
Date        : 2026-09-27
Evidence    : D:\Project\AITutor-X\FORMAL-E2E-04-evidence\
Executor    : MIMO CODE (verify only; no refactor; no Frozen Spec change)
Discipline  : Evidence first. No assumption. No silent fallback.
              执行边界：验证，不重构；发现，不修复；依据 Frozen Spec，不依据仓库里偶然存在的代码路径。
```

---

## Executive Summary

```text
OUTCOME : BLOCKED
```

| 判定 | 说明 |
|---|---|
| Frozen Spec 生产链是否端到端可运行 | **否** |
| 正式 preprocessing 入口 | **PASS**（真实 LLM，产出 30 units） |
| preprocessing → V3 Consumer | **BLOCKED**（fresh artifact 缺 identity） |
| V3 语义链（annotation→resolver→IR→gate→admission→Question） | **未达持久化结果** |

```text
FIRST BLOCKING POINT（正式 Frozen Spec 链路）
  Stage : Preprocessing Artifact → V3 Consumer Interface Scope
  Error : MISSING_IDENTITY — manifest 未声明 source_content_sha256
  Source: scripts/preprocessing_consumer/boundary.enforce_interface_scope
  Effect: downstream_executed=false；后续语义链未进入
```

---

## Pipeline Status

| Stage | Status | Evidence |
| --- | --- | --- |
| PDF→Preprocessing | **PASS** | `02_preprocessing_output.json`：`reslice_pipeline.py --file` 成功；units=30（standalone 26 / composite 4 / material 4）；model=`mimo-v2.6-pro` |
| Preprocessing Artifact | **PARTIAL** | manifest/md/annotated.md 产出完整；**缺** `source_content_sha256` / `identity_version` |
| Consumer | **BLOCKED**（fresh） / accepted（identity-ok 样本） | `consumer-report.json` MISSING_IDENTITY；`consumer-report-identity-ok.json` Track A/B completed |
| Annotation | **PASS**（事务内） | adapter 映射 `standalone_question→standalone_unit` / `composite_question→composite_unit`；SemanticAnnotation 在 Track A 事务创建 |
| Resolver | **EXECUTED**（GateService 内） | 未另跑 `resolver.resolve()` 作证据；Track B spans_constructed=212 / failed=0 |
| IR | **INCOMPLETE** | Track A：53/53 units skipped（Gate 不为 incomplete 建 candidate） |
| Admission | **NOT REACHED** | candidates_created=0 |
| Frontend | **NOT IMPLEMENTED** | Question/Material/Instance API 均不存在 |

---

## First Blocking Point

> 正式 Frozen Spec 链路第一次失败在哪里？

```text
Stage    : Preprocessing → V3 Consumer（Interface Scope / identity boundary）
Error    : interface_scope_rejected: MISSING_IDENTITY
           "Manifest does not declare source_content_sha256;
            cross-system identity cannot be established
            (path must never be used as identity)."
Source   : AITutors-v3/backend/scripts/preprocessing_consumer/boundary.py
           (enforce_interface_scope, F-INT-08 / F-INT-01)
Observed : 本轮 formal reslice_pipeline.py 新鲜产出的 manifest
           source_content_sha256=null, identity_version=null
Root     : reslice_pipeline.py 正式入口不写 identity 字段；
           历史 87 份 manifest 的 identity 由一次性脚本
           interface_scope_step2_backfill.py 回填（非正式生产步骤）
Effect   : consumer 不执行 Track A/B；语义链未启动
```

**不是**「某个测试脚本失败」——是 producer artifact 契约与 consumer identity 边界之间的正式缺口。

---

## Findings

### F04-01 — 正式 preprocessing 不产出 identity

```
FACT     : reslice_pipeline.py --file 正式入口产出的 manifest
           不含 source_content_sha256 / identity_version
Evidence : FORMAL-E2E-04-evidence/preproc_out/*.manifest.json
           02_preprocessing_output.json.identity_fields
           对比：reslice-batch-C 87 份有 identity；85 份无
Impact   : V3 Consumer Interface Scope fail-closed；正式链在此中断
Not in scope : 不在本轮补写 reslice_pipeline / 不跑 backfill / 不改 Frozen Spec
Suggested owner decision : identity 生成应进入正式 preprocessing 步骤，
           或定义合法的 post-step；禁止 path-as-identity
```

### F04-02 — Consumer runner 永不持久化

```
FACT     : preprocessing_consumer/runner.py run_corpus 在 finally 中
           await session.rollback()；Track A/B 只验证后丢弃
Evidence : runner.py run_corpus；05/06 snapshot 完全一致（无新行）
Impact   : 仓库中不存在「preprocessing artifact → V3 持久化业务链」的正式入口；
           现有 consumer 是 dry-run 校验器
Not in scope : 不新建 production importer；不把 PDF import 当替代
Suggested owner decision : 定义正式 Consumer Ingest 入口（commit 语义）
```

### F04-03 — identity-ok 样本 53/53 IR incomplete

```
FACT     : 使用带 identity 的真实 producer 产物时 Interface Scope 通过，
           但 Gate 将全部 53 units 记为 skipped（0 candidates）
Evidence : consumer-report-identity-ok.json track_a.skipped
Impact   : 即便 identity 解决，IR 粒度/adapter 证据缺口仍挡住 Admission
Not in scope : 不改 Resolver/IR/adapter 语义
Suggested owner decision : option per-label span 契约（已知 GAP_OPTION_LABEL_SPAN_UNAVAILABLE）
```

### F04-04 — PDF Import 路径存在但非本任务正式边界

```
FACT     : POST /api/documents/import + app.worker 可持久化跑通（前几轮已证），
           属 V3 自解析 PDF 边界
Evidence : task instruction §2.2；本任务 04_v3_execution.log 标注 NOT USED
Impact   : 若误用该路径会得到「E2E PASS」假象
Not in scope : 不清理、不删除、不标 legacy 改码
```

### F04-05 — Frontend/API 读路径未实现

```
FACT     : 无 Question / Material / Instance API
Evidence : app/api/routers 仅 documents / candidates / admin
Impact   : 无法展示最终对象
Not in scope : 不开发前端/临时 API
```

---

## 输入 hash

| Item | sha256 |
|---|---|
| PDF `2022北京丰台高一（下）期末历史（教师版）(1).pdf` | `72afe58664abe8366fd0404acc332c008eebfad0863b367c926fe29bccd41a26` |
| Source markdown（同名 OCR） | `0938b8e8cd867da77547d3ee0b5b9f229f09c4fd3350885570dbfd755556af6a` |
| Fresh manifest | 见 `02_preprocessing_output.json` |

---

## E2E 运行命令

```bash
# Step 2 formal preprocessing
cd D:\Project\Aitutors-preprocessing\scripts
python reslice_pipeline.py --file "D:\Project\Papers\Ocr-markdown\高一\历史\2022北京丰台高一（下）期末历史（教师版）(1).md" --out "D:\Project\AITutor-X\FORMAL-E2E-04-evidence\preproc_out"

# Step 3 V3 consumer (fresh artifacts)
cd D:\Project\AITutors-v3\backend
python -m scripts.preprocessing_consumer.runner --corpus "D:\Project\AITutor-X\FORMAL-E2E-04-evidence\preproc_out" --output "...\consumer-report.json"

# Step 3 V3 consumer (identity-complete real artifact)
python -m scripts.preprocessing_consumer.runner --corpus "...\consumer_input_identity_ok" --output "...\consumer-report-identity-ok.json"
```

未使用：`POST /api/documents/import`、`python -m app.worker run`（PDF 自解析边界）。

---

## Evidence index

```
FORMAL-E2E-04-evidence/
  00_environment.txt
  01_preprocessing_input.json
  02_preprocessing_output.json
  03_consumer_mapping.json
  04_v3_execution.log
  05_database_snapshot_before.json
  06_database_snapshot_after.json
  07_pipeline_summary.json
  consumer-report.json
  consumer-report-identity-ok.json
  preproc_out/**
  consumer_input_identity_ok/**
```

---

## 结论

> Frozen Spec 定义的生产链路（Preprocessing → V3 Consumer → 语义链）**当前不能端到端运行**。  
> 正式 preprocessing 入口本身可用，但产物缺少 consumer 强制的 identity；  
> 且现有 consumer 为 rollback 校验器，不存在持久化正式接入。  
> 本报告只验证、不修复；所有缺口记 Finding，待 Owner Decision。
