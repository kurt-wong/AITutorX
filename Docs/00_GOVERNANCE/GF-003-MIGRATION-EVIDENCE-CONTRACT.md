# GF-003 — Migration Evidence Contract（草案）

**Document ID**: GF-003
**Status**: `DRAFT / PROPOSED` — 未经 Owner 批准，不构成冻结权威
**Role**: Independent System Governance Architect（TASK-GF-001）
**Date**: 2026-09-17
**Parent**: `GF-000-FOUNDATION-BASELINE.md`
**Upstream**: REPORT-I（Gate 定义）、Contract v0.2（身份原则）、V3_SPEC 10/20/30/40/50
**Evidence discipline**: `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[DECISION REQUIRED]`

---

## 1. Purpose

定义 **迁移前必须具备何种证据**，以及证据如何被记录、校验、失败时如何处置。

本契约回答：「凭什么相信这份资产可以进入 AITutor-X？」
本契约 **不** 授权迁移，**不** 替代 Owner 批准，**不** 修改任何源仓。

---

## 2. Core Evidence Principles

| # | Principle | 分类 | 依据 |
|---|-----------|------|------|
| P1 | **Evidence before admission** — 无证据包不得进入 Gate 通过态 | `[FACT]` 任务书 GF-003；REPORT-I Gate 7 | |
| P2 | **Hash over path** — 身份证据以 content hash 为主，path 仅为 locator | `[FACT]` Contract v0.2 path non-identity | |
| P3 | **UNKNOWN is retained** — 证据缺口必须显式登记，禁止 silent skip | `[FACT]` `AGENTS.md` 原则 2 | |
| P4 | **Provenance ≠ Quality** — 来源证据不等于质量合格 | `[FACT]` `AGENTS.md` 原则 1 | |
| P5 | **Fail-closed verification** — hash 不可复算/不一致 ⇒ 拒绝，不降级放行 | `[FACT]` Contract bytes verification 要求 | |
| P6 | **Dual-repo source discipline** — 每条迁移记录写明 source repo + commit + path + (适用时) sha256 | `[FACT]` REPORT-I §0.6 | |
| P7 | **No silent conflict drop** — 与既有报告/台账冲突的证据必须并列保留 | `[FACT]` REPORT-I §0.4 | |

---

## 3. Evidence Package Schema（通用信封）

任何迁移候选的证据包至少包含：

```text
EvidencePackage
├─ package_id                  # 治理侧唯一 ID（迁移时分配，草案阶段仅定义字段）
├─ asset_class                 # GF-004 迁移类别（YES / NO / CONDITIONAL）
├─ role                        # GF-001 角色（RSD/PIS/OCRA/SEM/MIG/文档/代码/…）
├─ lineage_layer               # GF-002 层（L1–L6 / N/A for docs）
├─ source
│  ├─ source_repo              # kurt-wong/AITutors-v3 | kurt-wong/Aitutors-preprocessing | …
│  ├─ source_commit            # 完整 SHA
│  ├─ source_path              # locator only
│  ├─ git_tracked              # true/false
│  └─ bytes_kind               # pdf | ocr_md | figure | document | code | n/a
├─ hashes
│  ├─ content_sha256           # 适用时必填
│  ├─ hash_meaning             # 该 sha 作用的字节类型说明（禁止裸写 “original sha”）
│  └─ verification
│     ├─ method                # independent_recompute | manifest_crosscheck | owner_attested | not_verified
│     ├─ result                # match | mismatch | partial | not_run
│     └─ evidence_ref          # 命令/工件路径/行号
├─ generation
│  ├─ generation_timestamp     # 可考则填；不可考 = UNKNOWN + 原因
│  ├─ producer_version         # 代码 commit / 工具版本 / model+config（适用时）
│  └─ pipeline_run_ref         # PIS/log/清单条目
├─ authority
│  ├─ claimed_authority_level  # 仅登记声称值；不自动生效
│  ├─ authority_status         # verified | claimed_only | unknown | disputed
│  └─ frozen_ref               # 若引用 Frozen 对象：repo@commit + file + sha256
├─ gaps[]                      # UNKNOWN / 冲突 / known-issue（P3/P7）
├─ gate_status                 # Gate 1–10 逐项 pass/fail/pending
└─ owner_decision_refs[]       # OD-* / OQ-GF-* / Cluster 字母
```

---

## 4. Required Evidence by Artifact Class

### 4.1 Source artifact（源工件：PDF / OCR md / 图片等）

| Field | 必填？ | 说明 |
|-------|--------|------|
| `source_path` | YES | locator；可多路径（双树）并列 |
| `source_hash` | YES if 可得 bytes | 对源字节；`hash_meaning` 必填 |
| `artifact_hash` | YES | 迁移/登记对象自身字节 hash（若与 source 相同须显式写 `artifact_hash == source_hash`） |
| `generation_timestamp` | YES if 存在 | 日志/清单字段；否则 UNKNOWN |
| `producer_version` | YES if 存在 | 生成代码 commit 或工具版本 |
| `bytes_kind` | YES | 防 L1/L2 hash 混用 |
| `verification.method/result` | YES | 不可复算 ⇒ `not_verified` + gap |

**Producer 数据附加要求**:

- `[FACT]` 大体量数据不在 git（REPORT-K/G）。
- `[DECISION REQUIRED]` 数据权威模式（path-ref / NAS / copy / hash-manifest-only）= OD-009 / OQ-GF-002。
- **提案**: 在模式裁决前，源工件迁移证据 **只接受 hash 清单 + 只读 locator**，不接受「把整个 `original/` 或 `maintainess/` 拷进 AITutor-X」。

### 4.2 OCR Artifact 证据

在 4.1 基础上追加：

| Field | 必填？ | 说明 |
|-------|--------|------|
| `ocr_manifest_entry` | YES if 宣称 lineage 完整 | 指向 `ocr_output_manifest.jsonl` 条目 |
| `pdf_source_sha256` | YES | L1 锚 |
| `ocr_md_sha256` | YES | L2 锚 |
| `coverage_class` | YES | GF-002 §5 Class A/B/C/D |

- `[FACT]` 无清单条目、仅文件名可定位的 md ⇒ 最高 Class B，不得写「来源已验证」。

### 4.3 Semantic / IR artifact 证据

| Field | 必填？ | 说明 |
|-------|--------|------|
| `source_content_sha256` | YES | 接口键；`hash_meaning` = ocr_md（若属实） |
| `manifest_or_ir_ref` | YES | manifest 路径 / IR 记录 |
| `identity_version` | if present | 观测样本含 `identity_version=2` |
| `stage_hash` | V3 侧 YES | `logical_execution_stage` + `hash` |
| `dual_layer_disclosure` | YES | 必须同时披露 L1 PDF sha 是否已知 |

### 4.4 Question migration 证据（L4→L6）

任务书示例三类证据，展开如下：

| Evidence class | 必填字段 | Validation |
|----------------|----------|------------|
| **Source evidence** | 上游 L1–L2 hash + manifest/IR 引用 + coverage_class | V-Bytes + V-Manifest |
| **Transformation evidence** | 转换步骤、producer_version、stage_hash / Gate 记录、输入 `input_identity` | V-Stage + 可重放 |
| **Admission evidence** | `decision_status`、Gate 分层结果、approve 唯一入口证明、materialization 记录 | V-Admission |

- `[FACT]` V3：`decision_status` 只能经确定性 Gate Policy 或人工；LLM 无 Admission Authority。
- `[FACT]` 迁移后 AITutor-X 实体还须满足 REPORT-I Gate + `AGENTS.md` 原则 5。

### 4.5 Document / Spec / Contract / Code 证据

| Asset 类型 | 必填证据 |
|------------|----------|
| Frozen Contract 副本 | 冻结四元组：`repo @ commit / path / sha256`；字节级一致；禁改正文状态句 |
| V3 Frozen Spec | 源 commit + 源路径 + 复制后 sha256；保留源权威标注 + AITutorX taxonomy 映射（若 F3 已裁） |
| Code module | source_repo + commit + path + file sha256 + code_class（`AGENTS.md` 分类）+ tests 引用 |
| Untracked doc | **默认证据不足**；须 Owner 处置记录（commit / working-ref / 降级 / 拒绝）后方可有 authority_status ≠ unknown |
| Test suite | 文件级可迁；**测试结论/基线**须受控环境重跑记录（F9） |

**Contract v0.2 冻结锚** `[FACT]`:

```text
repo    = kurt-wong/AITutors-v3
commit  = f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1
path    = Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
sha256  = 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
```

- `[FACT]` 历史登记 `c6e771c` / `c8d89586…1032` = 勿引用。
- `[FACT]` REPORT-I F2：Freeze 状态叙事规则仍未在治理仓成文 — 迁移副本引用 Contract 前需 Owner 确认账本 vs 冻结对象的权威叙事。

---

## 5. Evidence Gates（与 REPORT-I 对齐）

本契约不新建 Gate 编号；**证据字段**支撑既有 10 步：

| Gate（REPORT-D/I） | 本契约提供的证据 |
|--------------------|------------------|
| 1 Source identified | `source.repo/commit/path` + role |
| 2 Authority identified | `authority.*` + frozen_ref + OD 引用 |
| 3 Current validity verified | hash verification + tests/baseline（适用时） |
| 4 Historical status classified | code/asset class + archive 判定 |
| 5 Duplicate check | 对 AITutor-X 既有资产比对记录 |
| 6 Architecture compatibility | path 抽象、Docker/env、import 适配证据（代码类） |
| 7 Evidence attached | EvidencePackage 完整性 |
| 8 Migration class assigned | GF-004 YES/NO/CONDITIONAL |
| 9 Governance approval | Owner/Migration Authority 记录（F4/F5） |
| 10 Migration record created | 迁移账本条目（含 gaps 保留） |

**停止线** `[FACT]`：Cluster A 未关闭前默认全面禁止迁移；例外仅 Owner 书面批准的只读证据副本。

---

## 6. Failure & Disposition Rules

| 证据结果 | 处置 |
|----------|------|
| `verification.result = match` 且无 open P0 决策 | 可进入 Gate 继续评审（非自动通过） |
| `mismatch` | **BLOCK**；登记冲突；禁止迁移 |
| `not_run` / `not_verified` | 可保留在候选册，但 **不得** 宣称 verified；按 Class B/D 处理 |
| 双树 path 并列且 hash 未知 | 保留双 locator + `authority_status=unknown` |
| 与旧报告主张冲突 | 并列旧主张 + 新证据；不修改已提交旧报告；新建对账引用 |
| untracked 且无 Owner 处置 | `authority_status=unknown` → 默认不进 active tree |

---

## 7. Record Location（提案）

| 记录 | 提案落点（未创建，仅定义） |
|------|----------------------------|
| EvidencePackage 实例 / 迁移账本 | `AITutor-X/Docs/50_OPERATIONS/` 或 Owner 指定 migration ledger |
| Gate 评审记录 | 随 Migration Authority Charter（F4）指定路径 |
| Open questions | `GF-005-OPEN-QUESTIONS-REGISTRY.md` |
| 冲突 | REPORT-H 续篇或 Owner 指定载体（**不修改** REPORT-H 既有正文） |

- `[DECISION REQUIRED]` F4 Migration Authority Charter 未设立前，任何「Gate 9 通过」声明均无效。

---

## 8. Minimal Examples（示意，非真实放行）

**例 A — Hash-closed OCR 样本（Class A）**

```text
asset: 2018北京春季高中会考化学（教师版）(1).pdf + .md
bytes_kind: pdf → sha256 8d3f9dad…f3a23 (maintainess=original=manifest)
bytes_kind: ocr_md → sha256 0443945f…ad1ffb (manifest=snapshot=recompute)
authority_status: role=PIS/OCRA observed; canonical RSD = unknown
gaps: 双树权威未裁 (OQ-GF-001)
```

**例 B — 源树 md 无清单（Class B）**

```text
asset: Ocr-markdown/.../某卷.md
source_hash: not_verified (no manifest entry)
artifact_hash: 可算但未登记上游
disposition: 禁止宣称 lineage verified；迁移候选默认拒绝直至补账
```

**例 C — Frozen Contract 副本**

```text
asset: PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
source_commit: f4941ff…
content_sha256: 9c6b9063…7528
verification: owner/prior audit frozen quadruple [FACT]
open: F2 status narrative; F3 taxonomy — Gate 9 仍 pending
```

---

## 9. Success Criterion

未来工程师仅凭 EvidencePackage 应能判断：

1. 这份资产的字节身份是什么、hash 算的是哪些字节；
2. 证据是否可独立复算；
3. 还缺哪些 Owner 决策；
4. 为何允许或禁止进入 AITutor-X。

---

*GF-003 · DRAFT · TASK-GF-001 · 2026-09-17 · 仅新建治理草案，未授权迁移*
