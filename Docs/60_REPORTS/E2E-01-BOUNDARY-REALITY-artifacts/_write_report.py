from pathlib import Path
from datetime import datetime, timezone

report = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-VERIFICATION-v1.1.md")
artifacts = "Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts"
ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")

text = """# E2E-01 — Frozen Boundary Reality Verification

**Document ID**: E2E-01-BOUNDARY-REALITY-VERIFICATION
**Document Type**: Task Report (C — Informative; not a Gate Report)
**Date**: __DATE__
**Authorization**: OD-E2E-01（甲方案：只验证既有现实，不实施 A8 接线）
**Name**: Frozen Boundary Reality Verification（非完整闭环 E2E）

> 证据标准：本文结论均可由 `__ART__` 下原始 JSON 与当场命令复算。无运行证据的断言一律不写。

---

## 0. 范围与 STOP

| 允许 | 禁止（本轮零触碰） |
|---|---|
| 执行 `runner_b2` | A8：M1–M5 → Gate 接线 |
| 验证 identity boundary / fail-closed | 修改 runner / Admission / schema |
| 观察 Gate/Admission、记录 seam | 修改 Frozen Contract / Frozen Spec |
| 复用既有 negative asset | Migration、新造 fixture、改 Papers 数据 |

主入口：`scripts.preprocessing_consumer.runner_b2`（M1–M5）。
`runner.py` 仅历史对照，**不作 PASS 依据**。

---

## 1. 三仓 pin（当场实测）

| 角色 | 仓库 | Commit | 备注 |
|---|---|---|---|
| Producer | Papers | `969d39aac00aca54df6db8a5a52d33089dfd9150` | **已 push**，`origin/main == HEAD`（fast-forward `b2266d2..969d39a`） |
| Consumer | AITutors-v3 | `39840ff` | D4 封线后 HEAD |
| Governance | AITutor-X | `3ee35e697648e58f69a9c8302d1b796a09701ecf` | 证据落盘仓 |

Papers worktree 仍见 2 个 untracked（`data/reslice_preproc_out_result.json`、`logs/reslice_preproc_out_log.txt`）= 既有运行日志，**非语料输入**，未入库。

### Frozen Contract Authority（唯一）

| 类型 | 值 |
|---|---|
| 文件 | `PREPROCESSING-V3-CONTRACT-v0.3-DRAFT.md` |
| Freeze Artifact（内容） | `b743c5daf0806ea00c84afb1b92ca2a3b5dbfc98` |
| Freeze Registration（登记） | `79348441dae0efce6855017b2b5c0491b08d6bb8` |
| 原则 | Freeze Artifact ≠ Freeze Registration |
| 不作权威 | `PREPROCESSING-V3-CONTRACT.md`（v0.1 前身）、`v0.2-DRAFT`（READY FOR FREEZE NOT FROZEN） |

五件冻结配套文件 SHA256（工作区实测）：

```text
1b952feec0fde866c07555dcb0ebe763ef1dd1cb1b80a050719a51666ebb6ea3  PREPROCESSING-V3-CONTRACT-v0.3-DRAFT.md
3febfff53a3ace9b488bb6174b0e44271176c488de11c2ecaafbc0ae568ff2bf  PREPROCESSING-V3-INFORMATION-PRESERVATION-MATRIX-v0.3-DRAFT.md
b5800b552ce48c540c68fc1a55df696fb0bfdea1581274f7e6d9ebe9dd554eae  PREPROCESSING-V3-OPEN-DECISIONS-v0.3-DRAFT.md
f0770cb975e5cb2ea83843a9983bc1a15a8ab6e556c550c38b413eb81124fd1e  PREPROCESSING-V3-SEMANTIC-AUTHORITY-MATRIX-v0.3-DRAFT.md
10c01cfbed03135449dce6602c65710b5a357ba7f3a148fb53965caa41b28056  V3-POST-ADMISSION-ENRICHMENT-CONTRACT-v0.3-DRAFT.md
```

### 语料口径（与 X2.7 定义一致）

```text
discovered 204
excluded   32  (.pytest_work / _archive 路径段)
eligible  172  = Ocr-markdown 166 + data 4 + tests 2
```

---

## 2. X2.7 定位（历史证据，非当前基线）

| 项 | X2.7 | 本任务 |
|---|---|---|
| 用途 | Historical Boundary Verification Evidence | Current frozen implementation verification |
| V3 commit | `3e2f9bb` | `39840ff` |
| Contract | v0.2-DRAFT `9c6b9063…` | **v0.3 Freeze Artifact `b743c5d`** |
| 结论效力 | 仅对照 | 本报告数字全部当场重跑 |

---

## 3. E2E-01a — 全量复验（172）

命令（三片，均 `runner_b2`，无 `--resolver-ir`）：

```text
cd AITutors-v3/backend
python -m scripts.preprocessing_consumer.runner_b2 --corpus Papers/<shard> --output ...
# shards = Ocr-markdown | data | tests
```

原始报告：`__ART__/10-raw-b2-*.json`。

### 3.1 总表

| 指标 | 值 |
|---|---|
| 执行 | **172 / 172**（真实执行，无跳过） |
| Errors | 0 |
| identity_state=VERIFIED | **87** |
| identity_state=FAILED | **85** |
| Completed（进入持久语义链） | 0 |
| Gate auto_approve / rejected / pending_review | 0 / 0 / 0 |
| downstream_executed | **172 全 false** |

### 3.2 拒绝码拆分（当场解析 `identity_gate`）

| interface_scope / reason | 件数 | identity_state | mismatches | 归因 |
|---|---|---|---|---|
| `MISSING_IDENTITY`（manifest 未声明 `source_content_sha256`） | **85** | FAILED | `manifest_sha_missing` | **C — Producer gap** |
| `interface_scope_accepted: identity_version==2`，`semantic_pending` | **87** | **VERIFIED** | `[]` | **D — Boundary seam**（见 §5） |

分片：

| shard | MISSING_IDENTITY | semantic_pending (VERIFIED) |
|---|---|---|
| data | 4 | 0 |
| tests | 2 | 0 |
| Ocr-markdown | 79 | 87 |
| **合计** | **85** | **87** |

VERIFIED 样例（`2018北京春季高中会考化学（教师版）(1)`）：

```json
{
  "gate": "BLOCK",
  "identity_state": "VERIFIED",
  "semantic_state": "PENDING",
  "reason": "semantic_pending",
  "mismatches": [],
  "interface_scope": {"accepted": true, "declared_identity_version": 2},
  "downstream_executed": false
}
```

### 3.3 与 X2.7 对照

| | X2.7（历史） | E2E-01（当前） |
|---|---|---|
| 阻塞总量 | 172/172 M5 BLOCK | 172/172 blocked |
| 缺 identity | 85 `manifest_sha_missing` | **85** `MISSING_IDENTITY` |
| identity 过、语义未就绪 | 87 `semantic_pending/ir_absent` | **87** VERIFIED + PENDING |

**分裂结构 85/87 未变。** D4 M1–M5 冻结 + Contract v0.3 未改变 boundary 拒绝面。

---

## 4. E2E-01b — 受控样例

**未新增 fixture 文件、未改 Papers。** 仅：既有 negative asset + 真实 manifest 错配组合 + 既有 identity-ok 语料。

| # | 样例 | 结果 | 归因 |
|---|---|---|---|
| 1 | identity-ok 历史语料（`FORMAL-E2E-04-evidence/consumer_input_identity_ok`，53 units） | `identity_state=VERIFIED`，`semantic_state=PENDING`，BLOCK | **A — M1–M5 identity PASS**；语义 seam 同 §5 |
| 2 | 真实 manifest + 错误 source bytes（`30-mismatch-combo`，化学卷） | `computed_manifest_mismatch`，`downstream_executed=false` | **A — fail-closed PASS** |
| 3 | 既有 `negB-report.json` | `computed_manifest_mismatch`，下游未执行 | **A — fail-closed PASS**（历史对照） |
| 4 | 既有 `negC-report.json` | `OUT_OF_SCOPE_IDENTITY_VERSION`（声明 v3） | **A — contract rejection PASS**（历史对照） |
| 5 | 85 件 MISSING_IDENTITY 真实语料 | `downstream_executed=false` | **A — fail-closed** + **C — Producer gap** |
| 6 | composite 覆盖 | VERIFIED 集内含 `composite_question`（全库 673 条 type） | **A — 路径覆盖存在** |
| 7 | M1–M5 单元/接口测试 | **98 passed**（`test_identity_*` 面） | **A — 接口实现成立** |

### 4.1 fail-closed 真相表（当前实现）

| 输入缺陷 | identity_state | downstream |
|---|---|---|
| 缺 `source_content_sha256` | FAILED | 未执行 |
| SHA 不匹配 | FAILED | 未执行 |
| `identity_version` 出界（≠2） | 拒绝（interface_scope） | 未执行 |
| identity VERIFIED 但 semantic PENDING | VERIFIED | 未执行（M5 硬化） |

---

## 5. D — Boundary seam（观察记录，不修复）

**不得写成「E2E 失败」。** 以下为架构断点事实：

```text
链 A（runner_b2，本任务主入口）:
  Producer artifact → M1–M5 → interface_scope → (IR) → … → AdmissionCandidate
  ✅ M1–M5   ❌ GateService   ❌ AdmissionService

链 B（runner.py / 生产 GateService）:
  Producer artifact → GateService → AdmissionService
  ✅ Gate/Admission   ❌ M1–M5
```

1. **当前不存在** `M1–M5 → GateService → AdmissionService` 统一执行链。该断点属 **A8**，OD-E2E-01 明确 NOT AUTHORIZED，本任务只记录。
2. **87 件 VERIFIED+PENDING=BLOCK**：identity 已过，默认路径无 resolver IR ⇒ `semantic_pending`。M5 对 VERIFIED+PENDING 的 BLOCK 严于 Design §4.6，此前已定性为 fail-closed hardening。
3. **consumer runner 持久化**：`runner_b2` 为 `session.rollback()` 验证 harness，**不是**生产 ingest；「不落库」是设计事实，不是缺陷。
4. **Admission** 在本任务路径上 `NOT_REACHED`——因 IR 未就绪 + 无 A8 接线，属预期 seam，不是 PASS/FAIL 判定项。

---

## 6. C — Producer gap（回 Producer，不在 V3 修）

| ID | 事实 | 证据 |
|---|---|---|
| C-1 | 85/172 manifest 未声明 `source_content_sha256`（`identity_version` 为空） | `10-raw-b2-*.json`，code=`MISSING_IDENTITY` |
| C-2 | 词表异常 1 条：`unit_type='andalone_question'`（疑 `standalone_question` 拼写残缺） | Ocr-markdown 全量 unit_type 统计 |

C-1 与 FORMAL-E2E-04「fresh formal pipeline 不产出 identity 字段」同源。身份齐全的 87 件多来自带 identity 的历史/增强产物，**不能**代表 formal pipeline 已闭环。

---

## 7. 五类归因汇总

| 类型 | 数量/状态 | 后续 |
|---|---|---|
| **A — PASS** | M1–M5 87 VERIFIED；fail-closed 4 路径全成立；98 tests | 保留证据 |
| **B — Consumer gap** | 本轮**未发现**接口实现违背已冻结 M1–M5 契约 | — |
| **C — Producer gap** | 85 缺 identity；1 词表残缺 | 回 Producer 单独裁决 |
| **D — Unauthorized semantic** | 链 A/链 B 断点（A8）；IR 缺省；M5 硬化 | **STOP**，待 Owner |
| **Contract gap** | v0.3 已冻结；默认路径对「无 IR 时的语义就绪定义」未在本任务展开（不扩审） | 不在本轮处理 |

---

## 8. Migration 闸门（不在本任务决定）

本任务**只提供** Boundary Reality 证据。是否进入 Migration Readiness，须 Owner 在 A8 决策之后另裁。当前仍：

```text
Migration NOT AUTHORIZED
A8 BLOCKED / NOT AUTHORIZED
N-values NOT IMPLEMENTED
multi-blank BLOCKED
R-5 NOT AUTHORIZED
```

---

## 9. 证据索引

| 文件 | 内容 |
|---|---|
| `__ART__/00-run-manifest.json` | 运行前固定基线（不可变） |
| `__ART__/10-raw-b2-{data,tests,Ocr-markdown}.json` | 全量 172 原始结果 |
| `__ART__/20-raw-b2-identity-ok.json` | identity-ok 受控样例 |
| `__ART__/30-raw-b2-mismatch.json` | 真实 manifest 错配 fail-closed |
| `__ART__/30-mismatch-combo/` | 错配组合输入（真实 manifest + 他源 bytes） |
| `AITutor-X/e2e_run/negB-report.json` / `negC-report.json` | 既有 fail-closed 资产 |
| X2.7 `Docs/60_REPORTS/X2.7-INT-FULL-01-*` | 历史对照 |

---

*E2E-01 executed under OD-E2E-01 Plan-A. Reality verified, seams recorded, nothing wired, nothing migrated.*
"""

text = text.replace("__DATE__", ts).replace("__ART__", artifacts)
report.write_text(text, encoding="utf-8")
print("wrote", report)
print("bytes", report.stat().st_size)
