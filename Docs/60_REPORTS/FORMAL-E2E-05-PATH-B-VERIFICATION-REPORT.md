# FORMAL-E2E-05 — Frozen Spec Path B Production Pipeline Verification

```text
Document ID : FORMAL-E2E-05-PATH-B-VERIFICATION-REPORT
Task ID     : FORMAL-E2E-05
Date        : 2026-09-27
Evidence    : D:\Project\AITutor-X\evidence\
Role        : Verification only (code modifications = 0)
Discipline  : Evidence first. No scope expansion. No speculative architecture.
```

---

## Executive Summary

```text
RESULT : FAIL
```

| 完成标准 | 判定 |
|---|---|
| PASS（Path B 真实 preprocessing 产物进入 V3 downstream） | 否 |
| PARTIAL（preprocessing 与 consumer 成功，downstream 未完成） | 否 |
| FAIL（明确阶段阻断） | **是** |

```text
阻断阶段 : CONSUMER (identity validation)
错误码   : MISSING_IDENTITY
```

---

## 1. FACT（实测事实）

### 1.1 环境与冻结物

| 项 | 值 |
|---|---|
| AITutors-v3 HEAD | `5f097f627de79a8f3c45f1c0bd22f49247f29cb9` |
| Papers HEAD | `e7c79b6ce9c61e1ee5f301170d0649d4f50d1b90` |
| AITutor-X HEAD（验证前） | `fa3a01c6a8b81d8763c25aab4713b13f2f439be3` |
| Aitutors-preprocessing | **无 `.git`**（工作树） |
| `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` SHA256 | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |
| 与任务书引用 `9C6B9063...B17528` | **一致** |
| 本轮代码修改数 | **0** |

### 1.2 SOURCE

| 项 | 值 |
|---|---|
| PDF | `2022北京丰台高一（下）期末历史（教师版）(1).pdf` |
| PDF sha256 | `72afe58664abe8366fd0404acc332c008eebfad0863b367c926fe29bccd41a26` |
| PDF bytes | 791365 |
| Source markdown | `Papers\Ocr-markdown\高一\历史\...期末历史（教师版）(1).md` |
| MD sha256 | `0938b8e8cd867da77547d3ee0b5b9f229f09c4fd3350885570dbfd755556af6a` |
| MD bytes | 68631 |
| MD lines | 929（preprocessing 日志） |

### 1.3 PREPROCESSING（正式入口）

**命令**

```bash
cd D:\Project\Aitutors-preprocessing\scripts
python reslice_pipeline.py --file "<source.md>" --out D:\Project\AITutor-X\evidence\preprocessing\out
```

**Provider identity（生产配置）**

```text
LLM_PROVIDER  = mimo
MIMO_MODEL    = mimo-v2.6-pro
MIMO_BASE_URL = https://api.xiaomimimo.com/v1
mimo-x-pro-preview : NOT USED
```

**执行结果（FACT）**

```text
exit     : success
log      : evidence/preprocessing/reslice_execution.log
           "units=30 覆盖题号=30 校验问题=0 警告=0"
manifest model tag : mimo-v2.6-pro
units    : 30
  standalone_question : 26
  composite_question  : 4
  with material_lines : 4
```

**产物 hash**

| artifact | bytes | sha256 |
|---|---|---|
| `*.manifest.json` | 20579 | `44622cf8fbaf5089835f93cd49767d3a1212dd898d8ce3a62bce5f47a02188f4` |
| `*.md`（sliced） | 61036 | `df907f5ea5adf6316b82f1f56f84862c28b04e3909fab28c6cdce0b63a7030d9` |
| `*.annotated.md` | 80127 | `16a5a65a7cd4417a7f3f5103e60ce46214c4dbb4aa43ecb7a1a447b8599f97fc` |

**Identity 字段（正式产物内，未人工修改）**

```text
source_content_sha256 = null
identity_version      = null
```

### 1.4 CONSUMER（identity validation）

**命令**

```bash
cd D:\Project\AITutors-v3\backend
python -m scripts.preprocessing_consumer.runner \
  --corpus D:\Project\AITutor-X\evidence\preprocessing\out \
  --output D:\Project\AITutor-X\evidence\preprocessing\consumer_report.json
```

**执行结果（FACT）**

```text
Found 1 manifests
Interface Scope blocked : 1
Track A : 0/1 completed
Track B : 0/1 completed
Contract gaps : 0
```

**Interface Scope 判定原文（consumer_report.json）**

```text
accepted : false
code     : MISSING_IDENTITY
declared_identity_version : null
reason   : interface_scope_rejected: MISSING_IDENTITY:
           Manifest does not declare source_content_sha256;
           cross-system identity cannot be established
           (path must never be used as identity).
downstream_executed : false
```

**代码位置（FACT）**

```text
AITutors-v3/backend/scripts/preprocessing_consumer/boundary.py
  enforce_interface_scope(...)
被 runner.py 在 Track A/B 之前调用；拒绝 → continue，不执行下游
```

### 1.5 ADAPTER / RESOLVED_RUN / DOWNSTREAM

| 阶段 | 执行与否 | 证据 |
|---|---|---|
| ADAPTER（manifest→annotation payload） | **NOT REACHED** | `downstream_executed=false`；Track A 未启动 |
| RESOLVED_RUN | **NOT REACHED** | Track B `spans_total=0` |
| DOWNSTREAM（IR/Compiler/Gate/Admission） | **NOT REACHED** | 无候选、无 DB 新行 |

---

## 2. 阶段失败定位（Stage Failure Ladder）

```text
Stage:

SOURCE            PASS
  |                 PDF/MD 读取成功，hash 已记录
  v
PREPROCESSING     PASS
  |                 reslice_pipeline.py 正式入口成功；30 units；mimo-v2.6-pro
  |                 产物完整（manifest / md / annotated.md）
  v
CONSUMER          FAIL  ← 第一次阻断
  |                 identity validation: MISSING_IDENTITY
  |                 source_content_sha256 与 identity_version 均为 null
  |                 downstream_executed = false
  v
ADAPTER           NOT REACHED
  v
RESOLVED_RUN      NOT REACHED
  v
DOWNSTREAM        NOT REACHED
```

**Failure**

```text
interface_scope_rejected: MISSING_IDENTITY
Manifest does not declare source_content_sha256;
cross-system identity cannot be established
(path must never be used as identity).
```

**Evidence**

```text
evidence/preprocessing/reslice_execution.log
evidence/preprocessing/output_summary.json
evidence/preprocessing/consumer_execution.log
evidence/preprocessing/consumer_report.json
evidence/git_and_spec_snapshot.json
```

---

## 3. INTERPRETATION（与 FACT 分离）

> 下列为解释/判断，不是 Frozen Spec 条文。

1. **当前正式 preprocessing 产出尚未满足 Frozen Spec Path B 的 consumer identity 要求。**  
   不能写成「Frozen Spec 不支持 preprocessing」——Spec/Contract 存在 Path B 与 identity 字段；缺口在当前 `reslice_pipeline.py` 输出面。

2. **historical manifest 中的 `source_content_sha256` 不能证明本轮 Path B 通。**  
   那些字段来自一次性回填脚本（`interface_scope_step2_backfill.py`），不属于 `reslice_pipeline.py` 正式入口；本轮禁止手工补字段。

3. **不能声称「Path B 不存在」。**  
   FACT 是：Path B 的 consumer 侧入口与 identity gate **存在且生效**；阻断原因是 producer 产物缺 identity 声明。

4. **`preprocessing_consumer/runner.py` 的 Track A/B 为事务内校验并 rollback**（本轮未触及；为已知实现事实）。即便 identity 通过，是否等于「正式 downstream 持久化入口」需 Owner 确认，本报告不扩展裁决。

---

## 4. BUG / GAP 登记（不修复）

### GAP-PB-01 — 正式 preprocessing 不写 identity

```text
FACT       : reslice_pipeline.py 产出 manifest 中
             source_content_sha256=null, identity_version=null
Evidence   : output_summary.json; manifest sha256 44622cf8…
Impact     : Path B 在 CONSUMER 阶段 fail-closed
Not done   : 未改代码、未手工补字段、未跑 backfill
Owner ask  : identity 生成是否应进入 reslice_pipeline 正式步骤
```

### GAP-PB-02 — identity 生成仅存在于一次性回填

```text
FACT       : interface_scope_step2_backfill.py / step1_snapshot.py
             负责写 source_content_sha256（DEC-025 FC-1）
Evidence   : Aitutors-preprocessing/scripts/interface_scope_step2_backfill.py
Impact     : 新产物无法自然获得 identity；历史 87 份不能外推为当前路径能力
```

### GAP-PB-03 — 本任务无法在不改代码/不改产物前提下继续下游

```text
FACT       : 禁止手工 manifest 修改 + 禁止绕过 consumer gate
             ⇒ ADAPTER / RESOLVED_RUN / DOWNSTREAM 不可测
Evidence   : consumer_report.json downstream_executed=false
Impact     : Path B 端到端结论只能停在 CONSUMER
```

---

## 5. Change Proposal（等待 Owner 授权，本轮不实施）

若要继续验证 Path B 下游，需要其一（**均未执行**）：

1. **Producer 侧**：`reslice_pipeline.py` 正式步骤写入 `source_content_sha256`（= SHA256(source md bytes)）与 `identity_version`  
2. **或** 定义合法的正式 post-step（非一次性 migration 脚本）  
3. **禁止**：人工改 manifest / 用 path 当 identity / 绕过 `enforce_interface_scope`

---

## 6. 报告纪律自检

```text
FACT 与 INTERPRETATION 分离     YES
未把代码现状写成 Spec 结论      YES（§3）
未使用 Native Path (PDF→V3 Import) YES
未手工修改 manifest              YES
未构造假 consumer input          YES
未绕过 consumer gate             YES
未修改 Frozen Spec               YES（hash 与任务书一致）
未顺手修代码                     YES（code modifications = 0）
结论用词 PASS/PARTIAL/FAIL       YES → FAIL
```

---

## 7. Evidence index

```text
evidence/
  git_and_spec_snapshot.json
  preprocessing/
    reslice_execution.log
    consumer_execution.log
    consumer_report.json
    output_summary.json
    out/*.manifest.json
    out/*.md
    out/*.annotated.md
```
