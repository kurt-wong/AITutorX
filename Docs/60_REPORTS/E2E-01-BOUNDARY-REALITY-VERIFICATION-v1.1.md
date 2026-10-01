# E2E-01 — Frozen Boundary Reality Verification (v1.1)

**Document ID**: E2E-01-BOUNDARY-REALITY-VERIFICATION-v1.1
**Document Type**: Task Report (C — Informative; not a Gate Report)
**Date**: 2026-10-01
**Authorization**: OD-E2E-01（甲方案）+ E2E-01-R1 Correction Closure（分类 A–E 冻结）
**Name**: Frozen Boundary Reality Verification（非完整闭环 E2E）

## 治理元数据（R3/R5）

| 字段 | 值 |
|---|---|
| Readers | Owner / DSH / Migration Gate 评估者 |
| Supersedes | `E2E-01-BOUNDARY-REALITY-VERIFICATION.md` |
| Superseded_by | — |
| Disposition | `SUPERSEDES-E2E-01-BOUNDARY-REALITY-VERIFICATION.md` |
| R1 例外依据 | OD-E2E-01 / E2E-01-R1：同任务保留 v1.0（ARCHIVED）+ 产出 v1.1，经 Owner 显式批准 |
| Authority level | C — Informative（非 Gate Report） |
| Security | 无凭据入库 |

> 证据标准：结论均可由 `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/` 原始 JSON 与当场命令复算。无运行证据的断言一律不写。
> **本文件不得单独作为 A8 或 Migration 授权依据。**

---

## 0. 范围与 STOP

| 允许 | 禁止（本轮零触碰） |
|---|---|
| 执行 `runner_b2` | A8：M1–M5 → Gate 接线 |
| 验证 identity boundary / fail-closed | 修改 runner / Admission / schema |
| 观察 Gate/Admission、记录 seam | 修改 Frozen Contract / Frozen Spec / 00-run-manifest.json |
| 复用既有 negative asset | Migration、改 Papers、改 V3 代码 |

主入口：`scripts.preprocessing_consumer.runner_b2`（M1–M5）。`runner.py` 仅历史对照，**不作 PASS 依据**。

---

## 1. 分类体系（冻结，取代 v1.0 §7）

| 字母 | 含义 | 当前计数 |
|---|---|---|
| **A** | PASS / identity boundary accepted | **87**（与 E 联合） |
| **B** | Producer gap | **85** |
| **C** | Consumer gap | **0** |
| **D** | Unauthorized semantic / architecture boundary | **—**（不进逐件统计） |
| **E** | Artifact readiness gap | **87**（分母 = 87，**不是 172**） |

**Contract gap** = cross-cutting observation，**不占 A–E 字母**。

禁止：把 87 件整体归 D；禁止推论「解决 A8 ⇒ 可进 Admission」。

---

## 2. 三仓 pin（当场实测）

| 角色 | 仓库 | Commit | 备注 |
|---|---|---|---|
| Producer | Papers | `969d39aac00aca54df6db8a5a52d33089dfd9150` | 已 push，`origin/main == HEAD` |
| Consumer | AITutors-v3 | `39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4` | D4 封线后 HEAD |
| Governance | AITutor-X | `3ee35e697648e58f69a9c8302d1b796a09701ecf` | 证据落盘仓 |

### Frozen Contract Authority（唯一）

| 类型 | 值 |
|---|---|
| 文件 | `PREPROCESSING-V3-CONTRACT-v0.3-DRAFT.md` |
| Freeze Artifact | `b743c5daf0806ea00c84afb1b92ca2a3b5dbfc98` |
| Freeze Registration | `79348441dae0efce6855017b2b5c0491b08d6bb8` |
| 不作权威 | v0.1 前身 / v0.2-DRAFT（READY FOR FREEZE NOT FROZEN） |

五件封套 SHA256 见 `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/00-run-manifest.json`（immutable）。

### 语料

```text
discovered 204
excluded   32  (.pytest_work / _archive)
eligible  172  = Ocr-markdown 166 + data 4 + tests 2
```

---

## 3. E2E-01a 全量复验（172）

原始：`Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/10-raw-b2-{data,tests,Ocr-markdown}.json`。

| 指标 | 值 |
|---|---|
| 执行 | 172 / 172 |
| Errors | 0 |
| downstream_executed | 172 全 false |

### 3.1 归因（A–E）

| 归因 | 件数 | 事实 |
|---|---|---|
| **B** Producer gap | **85** | `MISSING_IDENTITY` / `manifest_sha_missing`；未声明 `source_content_sha256`，M1 即停，**未到达 IR 轴** |
| **A + E**（双标签，不合并） | **87** | A：`identity_state=VERIFIED`，`identity_version==2`，`mismatches=[]`；E：默认路径无 resolver IR ⇒ `semantic_state=PENDING` ⇒ M5 BLOCK |
| **C** | **0** | 本轮未发现违反已冻结 M1–M5 的 Consumer 实现 |
| **D** | **—** | 架构事实（见 §5），无逐件计数 |

分片：MISSING_IDENTITY = data 4 + tests 2 + Ocr-markdown 79 = 85；VERIFIED+PENDING = Ocr-markdown 87。

VERIFIED 样例（化学卷）：`identity_state=VERIFIED`，`semantic_state=PENDING`，`reason=semantic_pending`，`mismatches=[]`，`downstream_executed=false`。

### 3.2 H-3 事实句（无因果）

> E2E-01 当场重跑的 85 / 87 分裂结构，与 X2.7 历史运行 `legs.B2_primary` 的 85 / 87 分裂结构一致。

**证据件**：`Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/32-x27-vs-e2e01-compare.json`  
`x27_rows=172`，`e2e01_rows=172`，多重集 `(paper, class)` 相等，`only_in_x27=0`，`only_in_e2e01=0`。

**不声明**「因 D4 / Contract v0.3 而不变」（`3e2f9bb→39840ff` 为 91 files / 17781 insertions 级差异，不足以支撑因果）。

---

## 4. E2E-01b 受控样例

**未修改 Papers；未新增 Producer corpus 成员。** `30-mismatch-combo/` 为 Consumer 侧受控 negative 组合（真实 manifest + 他源 raw bytes），按 OD 允许的「真实 manifest + 不匹配组合」执行，**不进入** 172 计数。

| # | 样例 | 结果 | 归因 |
|---|---|---|---|
| 1 | identity-ok 历史语料（53 units） | VERIFIED + semantic PENDING | A + E |
| 2 | `30-mismatch-combo` | `computed_manifest_mismatch`，downstream false | A fail-closed |
| 3 | 既有 negB | `computed_manifest_mismatch` | A fail-closed |
| 4 | 既有 negC | `OUT_OF_SCOPE_IDENTITY_VERSION` | A fail-closed |
| 5 | 85 件 MISSING_IDENTITY | downstream false | A fail-closed + B |
| 6 | composite 覆盖 | 见 M-5 口径 | A 覆盖存在 |

### 4.1 fail-closed

| 输入缺陷 | identity_state | downstream |
|---|---|---|
| 缺 `source_content_sha256` | FAILED | 未执行 |
| SHA 不匹配 | FAILED | 未执行 |
| `identity_version` 出界 | 拒绝 | 未执行 |
| VERIFIED + PENDING | VERIFIED | 未执行（M5 硬化） |

---

## 5. D — 架构 seam（无逐件计数）

```text
链 A runner_b2:  Producer → M1–M5 → (IR) → …     ✅M1–M5  ❌GateService  ❌AdmissionService
链 B runner.py:  Producer → GateService → Admission  ✅Gate/Admission  ❌M1–M5
```

1. **当前不存在** `M1–M5 → GateService → AdmissionService` 统一入口。属 **A8 / D**，本任务只记录。
2. **与 E 正交**：E（IR 缺席）解决后 D 仍在。禁止「解 A8 即可 Admission」推论。
3. `runner_b2` 为 `session.rollback()` 验证 harness，非生产 ingest。
4. Admission `NOT_REACHED` 为预期 seam。

---

## 6. 更正项对照（相对 v1.0）

| ID | v1.0 问题 | v1.1 处置 |
|---|---|---|
| H-1 | 字母 B/C 对调 | 已按 A–E 冻结重写 |
| H-2 | 87 件笼统归 D | 拆为 A（identity）+ E（IR readiness）；D 无计数 |
| H-3 | 因果句 | 改为事实句 + `32-x27-vs-e2e01-compare.json` |
| M-4 | 「98 passed」无四件套 | 见 §7 命令/范围/日志 |
| M-5 | 673 口径冒充全库 | 673=Ocr-markdown；**729=全量 eligible** |
| M-6 | 「未新增 fixture」不精确 | 见 §4 来源说明 |

---

## 7. M-4 可复现四件套

| 项 | 值 |
|---|---|
| command | `cd AITutors-v3/backend && python -m pytest tests/test_identity_interface_freeze.py tests/test_identity_gate.py tests/test_identity_verifier.py tests/test_manifest_identity.py tests/test_raw_bytes_identity.py tests/test_ir_identity.py -q` |
| environment | Windows 11 / Python 3.12.9 |
| scope | **六文件**（非 `test_identity_*` 通配，非 D.2 十一面，非全量 suite） |
| result | **98 passed, 1 warning** |
| 日志 | `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/40-pytest-identity-6files.txt` |
| 逐文件 | interface_freeze 9 + gate 17 + verifier 27 + manifest 17 + raw_bytes 10 + ir 18 = 98 |

**口径声明**：v1.0 曾写「（test_identity_* 面）」，该通配不成立。本表以六文件命令为准。  
D.2 十一文件面（含 adversarial_m5_*）= 355，属 D4 Phase Evidence，不在本报告计数。

---

## 8. M-5 / M-6

**M-5 composite_question**

| 口径 | 条数 |
|---|---|
| Ocr-markdown 分片 | 673 |
| **全量 eligible（172 manifests）** | **729**（673+31+25） |

**M-6** mismatch 来源：Consumer 侧受控组合；未改 Papers；非 Producer corpus 成员；negB/negC 为既有资产。

---

## 9. B — Producer gap（回 Producer）

| ID | 事实 |
|---|---|
| B-1 | 85/172 未声明 `source_content_sha256` / `identity_version` |
| B-2 | 词表 `unit_type=andalone_question` ×1（疑拼写残缺） |

B-1 与 FORMAL-E2E-04「fresh formal pipeline 不产出 identity 字段」同源。87 件 identity 齐全者多为历史/增强产物，**不能**代表 formal pipeline 闭环。

---

## 10. Contract gap（cross-cutting，不占字母）

默认路径对「无 IR 时语义就绪如何定义」未在本任务展开。不扩审、不处置。

---

## 11. 修正后归因终表

| 类型 | 状态 | 后续 |
|---|---|---|
| **A** PASS | 87 identity VERIFIED；fail-closed 四路径；98 tests | 保留 |
| **B** Producer gap | 85 缺 identity；E 面上 IR artifact 缺席亦归 readiness→见 E；词表×1 | 回 Producer |
| **C** Consumer gap | 0 | — |
| **D** Unauthorized semantic | 链断点（A8）；M5 硬化 | STOP |
| **E** Artifact readiness | 87（仅 IR 轴） | 回 Producer/upstream |
| Contract gap | cross-cutting | 不处理 |

> 说明：87 件的 IR 缺席按 F-1 记 **E**，不记 B（B 的 85 件在 M1 即停）。若上游把 IR 视为 Producer 交付物，可另裁并入 B；**本报告按 E 计数**，避免与 85 混淆。

---

## 12. Errata（不改 immutable 文件）

`Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/00-run-manifest.json` 自述 immutable（corrections → errata）。故：

| 项 | manifest 原值 | Errata |
|---|---|---|
| `commits.aitutors_v3` | `"39840ff"`（7 位） | 完整 SHA：`39840ff8f0b3d7e9e2c75155ba043a8ed6b03aa4` |

**未编辑** `00-run-manifest.json`。

---

## 13. 闸门（不变）

```text
Migration NOT AUTHORIZED
A8 NOT AUTHORIZED
N-values NOT IMPLEMENTED
multi-blank BLOCKED
R-5 NOT AUTHORIZED
```

本报告可支撑：M1–M5 边界在真实 Producer 产物上是否成立（可）；Producer identity 合规（可，85 件否）。  
**不可**支撑 A8 授权或 Migration。

---

## 14. 证据索引

| 文件 | 内容 |
|---|---|
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/00-run-manifest.json` | 基线（immutable） |
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/10-raw-b2-*.json` | 全量 172 |
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/20-raw-b2-identity-ok.json` | identity-ok |
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/30-raw-b2-mismatch.json` + `30-mismatch-combo/` | fail-closed 错配 |
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/32-x27-vs-e2e01-compare.json` | H-3 比对件 |
| `Docs/60_REPORTS/E2E-01-BOUNDARY-REALITY-artifacts/40-pytest-identity-6files.txt` | M-4 日志 |
| `E2E-01-BOUNDARY-REALITY-VERIFICATION.md` | v1.0 ARCHIVED 历史 |

---

*v1.1 generated under OD-E2E-01 + E2E-01-R1. Taxonomy A–E frozen. v1.0 preserved. Nothing wired, nothing migrated.*
