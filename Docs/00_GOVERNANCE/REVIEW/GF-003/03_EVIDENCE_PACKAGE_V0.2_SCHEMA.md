# 03 — EvidencePackage v0.2 Schema

**Document class**: REVIEW PROPOSAL（schema 设计，非已生效契约）  
**Task**: TASK-GF-003-B  
**Date**: 2026-09-18  
**Extends**: `GF-003-MIGRATION-EVIDENCE-CONTRACT.md` §3（**原文件不修改**）

**Classification**: `[FACT]` / `[PROPOSAL]` / `[UNKNOWN]` / `[NEED OWNER DECISION]`

**Preserved from GF-003 v0.1** `[FACT: GF-003 §2–§3]`: P1 Evidence before admission；P2 Hash over path；P3 UNKNOWN is retained；P4 Provenance ≠ Quality；P5 Fail-closed；P6 Dual-repo source discipline；P7 No silent conflict drop。

**说明**: 下列嵌套结构为 `[PROPOSAL]` 文档 schema 描述，**非可执行代码**。

---

## 1. EvidencePackage v0.2 Envelope `[PROPOSAL]`

```text
EvidencePackage
├─ package_id                    # 治理侧唯一 ID
├─ schema_version                # PROPOSAL: "evidence-package-0.2"
├─ asset_class                   # GF-004 YES / NO / CONDITIONAL（v0.2 见 05_*.md）
├─ role                          # GF-001 角色 + PROPOSAL 扩展 GOV/EVD/EXT/MIG…
├─ lineage_layer                 # GF-002 L1–L6 / N/A
├─ source
│  ├─ source_repo
│  ├─ source_commit              # 完整 SHA
│  ├─ source_path                # locator only
│  ├─ git_tracked                # true / false
│  └─ bytes_kind                 # pdf | ocr_md | figure | document | code | n/a
├─ carrier_state_ref             # PROPOSAL → Carrier State / observation_id 列表
├─ hashes
│  ├─ content_sha256
│  ├─ hash_meaning               # 禁止裸写 "original sha" [FACT: GF-002 §4.3]
│  ├─ bytes_kind_of_hash         # PROPOSAL
│  └─ verification
│     ├─ method                  # independent_recompute | manifest_crosscheck | owner_attested | not_verified
│     ├─ result                  # match | mismatch | partial | not_run
│     ├─ evidence_ref
│     ├─ verification_timestamp  # PROPOSAL mandatory
│     ├─ verification_environment# PROPOSAL conditional
│     ├─ verifier_identity       # PROPOSAL
│     ├─ interface_integrity     # PROPOSAL: SEM/IR/manifest 类
│     └─ locator_integrity       # PROPOSAL: 与 interface 分列
├─ generation
│  ├─ generation_timestamp       # 可考则填；否则 UNKNOWN + 原因 [FACT: GF-003 §3]
│  ├─ producer_version
│  └─ pipeline_run_ref
├─ authority
│  ├─ claimed_authority_level
│  ├─ authority_status          # verified | claimed_only | unknown | disputed
│  └─ frozen_ref
├─ evidence_lifecycle
│  ├─ as_of_semantics           # PROPOSAL: hash/verification 时点语义
│  ├─ restoration_event_ref[]   # PROPOSAL
│  ├─ post_copy_sha256          # PROPOSAL: 物理复制后复算
│  ├─ test_baseline             # PROPOSAL: F9 受控重跑记录引用
│  └─ known_issues_refs[]       # PROPOSAL
├─ gate_evidence_slots           # PROPOSAL: Gate 1–10 证据槽（非批准本身）
├─ approval_block
│  ├─ status                    # PROPOSAL: valid | invalid_without_charter | pending_owner | rejected
│  ├─ migration_authority_ref
│  ├─ owner_decision_ref
│  ├─ approved_at
│  └─ notes
├─ rollback_ref                  # PROPOSAL: 可为 none_documented + gap
├─ gaps[]                        # P3/P7
└─ owner_decision_refs[]         # OD-* / OQ-GF-* / Cluster 字母
```

---

## 2. Field Requirements — Mandatory / Optional / Conditional

**级别定义** `[PROPOSAL]`:
- **Mandatory**: 缺失或 silent-skip ⇒ Gate 7 证据不完整（P1）
- **Optional**: 可空，填写时必须可核验
- **Conditional**: 条件触发时 Mandatory；未触发时填 `n/a` + 理由（禁止 silent skip，P3）

| Field | Level | 条件 / 说明 | 源 |
|-------|-------|-------------|-----|
| `package_id` | Mandatory | 治理分配 | GF-003 §3 |
| `schema_version` | Mandatory | v0.2 字面量 | PROPOSAL |
| `asset_class` | Mandatory | GF-004 / 05_*.md | GF-003 §3 |
| `role` | Mandatory | GF-001；v0.2 可用 GOV/EVD/EXT | GF-003 + PROPOSAL |
| `lineage_layer` | Mandatory | 文档类可 `N/A` | GF-003 §3 |
| `source.source_repo` | Mandatory | | GF-003 P6 |
| `source.source_commit` | Mandatory | untracked 则显式 `untracked` + gap | REPORT-I F7 `[FACT]` |
| `source.source_path` | Mandatory | locator only | GF-003 P2 |
| `source.git_tracked` | Mandatory | | GF-003 §3 |
| `source.bytes_kind` | Mandatory | 防 L1/L2 hash 混用 | GF-003 §4.1 |
| `carrier_state_ref` | Conditional | 数据/语料/OCR/清单类；纯冻结文档副本可 `n/a` | PROPOSAL R2 |
| `hashes.content_sha256` | Conditional | 可得 bytes 时 Mandatory | GF-003 P2 |
| `hashes.hash_meaning` | Mandatory when hash present | 禁止裸写 original sha | GF-002 §4.3 `[FACT]` |
| `hashes.bytes_kind_of_hash` | PROPOSAL Mandatory when hash present | 与 hash_meaning 互补 | PROPOSAL |
| `verification.method` | Mandatory | | GF-003 §3 |
| `verification.result` | Mandatory | | GF-003 §3 |
| `verification.evidence_ref` | Mandatory when method ≠ not_verified | | GF-003 §3 |
| `verification_timestamp` | **Mandatory**（PROPOSAL 升级） | method ≠ not_verified 时；not_run 亦须占位说明 | PROPOSAL R1 |
| `verification_environment` | Conditional | 代码/测试类 Mandatory | PROPOSAL R1 / REPORT-I F9 `[FACT]` |
| `verifier_identity` | PROPOSAL Mandatory when verified | chain of custody | PROPOSAL |
| `verification.interface_integrity` | Conditional | SEM/IR/manifest/接口类 | PROPOSAL R8 |
| `verification.locator_integrity` | Conditional | 同上；**不可**被 interface 替代 | PROPOSAL R8 |
| `generation.generation_timestamp` | Conditional | 存在则 Mandatory；否则 UNKNOWN+原因 | GF-003 §3 |
| `generation.producer_version` | Conditional | 可考则填 | GF-003 §3 |
| `generation.pipeline_run_ref` | Optional | | GF-003 §3 |
| `authority.claimed_authority_level` | Optional（仅登记声称） | | GF-003 §3 |
| `authority.authority_status` | Mandatory | | GF-003 §3 |
| `authority.frozen_ref` | Conditional | 引用 Frozen 对象时 | GF-003 §3 |
| `as_of_semantics` | PROPOSAL Mandatory when hash/verification 填写 | 见 §3 | PROPOSAL R1 |
| `restoration_event_ref[]` | Conditional | 载体经历 restore 时 Mandatory | PROPOSAL R3；REPORT-K §1.11 `[FACT]` |
| `post_copy_sha256` | Conditional | **物理复制**进入 AITutor-X 时 Mandatory；manifest-only = `n/a` | PROPOSAL R11 |
| `test_baseline` | Conditional | 宣称测试等价或代码类迁移时 Mandatory；指向 F9 | PROPOSAL；OQ-GF-018 `[FACT: OPEN]` |
| `known_issues_refs[]` | PROPOSAL Mandatory（可为空数组） | 代码/服务资产禁止 silent empty 当源账本有 issue | PROPOSAL R5 |
| `gate_evidence_slots` | Conditional | 进入 Gate 评审时 Mandatory（槽可为 pending） | PROPOSAL |
| `approval_block` | Conditional | Gate 8–9 时 Mandatory；F4 未设 ⇒ `invalid_without_charter` | PROPOSAL R10；REPORT-I F4 `[FACT]` |
| `approval_block.status` | Mandatory when approval_block present | 枚举见 §5 | PROPOSAL |
| `rollback_ref` | PROPOSAL Mandatory（可 `none_documented`） | none 须写 gap | PROPOSAL R11 |
| `gaps[]` | Mandatory（可为空数组） | P3/P7 | GF-003 §3 |
| `owner_decision_refs[]` | Mandatory when 存在开放决策 | | GF-003 §3 |

---

## 3. `as_of` Semantics `[PROPOSAL]`

**问题** `[FACT]`: REPORT-K §1.11 — maintainess/PDF 会话中途观测仅 6 文件（误删过程态），Owner 恢复后复测 12,707；同一路径不同时间字节状态不同。GF-003 v0.1 无时点字段。

```text
as_of_semantics
├─ kind
│    observation_as_of      # hash/计数属于某次 Carrier Observation
│    inventory_as_of        # 目录计数属于某次盘点
│    assertion_as_of        # 文档主张的陈述时点（≠ bytes 时点）
│    unknown_time           # 时点不可考 → 保持 UNKNOWN
├─ observed_at              # timestamp；时区显式；unknown_time 时 null + reason
├─ observation_id           # 指向 Carrier Observation（04_*.md）
├─ coverage                 # full | sample | manifest_subset
└─ replacement_of           # supersede 旧观测时填旧 observation_id（历史保留）
```

**规则** `[PROPOSAL]`:
1. 引用 hash/计数时必须可追溯到 `observation_id`，或显式声明「当前未钉时点」+ gap。  
2. **禁止**用最新观测静默覆盖历史观测。  
3. 恢复事件前后必须各有 observation，或显式 `not_verified`。  
4. REPORT-K「6 文件」态 = incident 观测，**不得**作语料治理结论 `[FACT: REPORT-K §1.11 已禁]`。

---

## 4. Known Issues Binding `[PROPOSAL]`

**依据** `[FACT]`: Papers `PREPROCESSING-PHASE25-GUARDIAN-REVIEW-v1.md` — D-048-1（M5 subclass 绕过，WARNING-hardening）；D-048-2（M3 positional fallback，NOTE）；登记不代改；fail-closed 主张不受影响。

```text
known_issues_refs[] 条目
├─ asset_ref                 # repo@commit + path + file_sha256
├─ issue_id                  # 如 D-048-1（源编号保留）
├─ issue_namespace           # papers / v3 / aitutorx（F6 未裁前双轨）[FACT: REPORT-I F6 OPEN]
├─ severity                  # 沿用源账本
├─ source_ledger             # Guardian Review 等 locator
├─ claim_scope
└─ disposition               # PROPOSAL 枚举（治理侧，≠ 关闭源账本）
     ├─ accepted_risk
     ├─ blocked
     ├─ pending_owner_decision
     ├─ mitigated_in_evidence
     └─ not_applicable_to_scope
```

**规则** `[PROPOSAL]`:
1. 源账本存在已知 issue 时禁止 silent empty。  
2. disposition **不**关闭 Papers D-048。  
3. M1–M5 在 D2/D3/D4 与 OQ-GF-017 未决前：默认 `pending_owner_decision`，不得写 `accepted_risk` `[FACT: GF-005 OQ-GF-017 OPEN-BLOCKING]`。  
4. CRITICAL 且否定 fail-closed ⇒ 默认 `blocked`（当前 D-048 级别未触发）`[FACT: Guardian Review]`。

---

## 5. Gate Evidence Slots & Approval Block `[PROPOSAL]`

```text
gate_evidence_slots          # 对齐 REPORT-I Gate 1–10 [FACT: REPORT-I；GF-003 §5]
├─ gate_1_source_identified
├─ gate_2_authority_identified
├─ gate_3_validity_verified
├─ gate_4_historical_status
├─ gate_5_duplicate_check
├─ gate_6_arch_compatibility
├─ gate_7_evidence_attached
├─ gate_8_migration_class
├─ gate_9_governance_approval
└─ gate_10_migration_record
# 每槽: pass | fail | pending | blocked_by(<ref>)
# 槽记录证据，不授予批准权
```

| approval_block.status | 含义 | 当前全仓默认 `[FACT]` |
|----------------------|------|----------------------|
| `valid` | Charter 存在 + 按 F4 格式批准 | **不可用** — F4 未设立 |
| `invalid_without_charter` | 无 F4 时的强制值 | **适用中** |
| `pending_owner` | 材料齐备等 Owner | Cluster A 未关 |
| `rejected` | Owner 拒绝 | — |

依据 `[FACT]`: REPORT-I F4 Charter 未设立；F5 Gate 文本草案；GF-003 §7「F4 前 Gate 9 通过无效」。

---

## 6. Failure Disposition (v0.2 增补) `[PROPOSAL]`

| 结果 | 处置 | 相对 v0.1 |
|------|------|-----------|
| `verification.result = mismatch` | **BLOCK** + 登记冲突 | 保留 `[FACT: GF-003 §6]` |
| `not_run` / `not_verified` | 不得称 verified；Class B/D | 保留 |
| 迁移后 `post_copy_sha256` 漂移 | BLOCK + `LINEAGE_BROKEN` + 评估 rollback_ref | **新增** |
| `known_issues_refs` 有条目但 disposition 空 | Gate 7 失败 | **新增** |
| `approval_block.status=invalid_without_charter` | package 在 Gate 9 意义上不完整 | **新增（硬化）** |
| 双 locator 且 authority unknown | 保留并列 + `authority_status=unknown` | 保留 |

---

## 7. Minimal Examples `[PROPOSAL 示意，非放行]`

**例 A — Frozen Contract 副本（文档类）**

```text
role: GOV / contract-copy
source: kurt-wong/AITutors-v3 @ f4941ff… / PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
hashes.content_sha256: 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
hash_meaning: contract_file_bytes_sha256
carrier_state_ref: n/a (document)
approval_block.status: invalid_without_charter   # F4 未设
gaps: F2 status narrative；F3 taxonomy；OQ-GF-014/015 OPEN
```

**例 B — IR/manifest 证据（接口类）**

```text
role: SEM / EVD
interface_integrity: manifest 键 vs Frozen identity 定义
locator_integrity: ir.locator → 当前 md bytes → sha
                   # 观测：snapshot 87/87；IR ADMITTED 71 [FACT: REPORT-K]
coverage_class: A (subset) — 非全树
known_issues_refs: DQ 口径差（87/166 vs「0/166」）→ 登记
approval_block: invalid_without_charter
```

**例 C — 代码模块 M5**

```text
role: code / identity-module
known_issues_refs:
  - issue_id: D-048-1
    severity: WARNING-hardening
    source_ledger: Papers INTEGRATION/PREPROCESSING-PHASE25-GUARDIAN-REVIEW-v1.md
    disposition: pending_owner_decision
  - issue_id: D-048-2
    severity: NOTE
    disposition: pending_owner_decision
test_baseline: UNKNOWN — F9 未完成受控重跑 [FACT: REPORT-I F9]
authority_status: unknown — OQ-GF-017 OPEN
rollback_ref: none_documented + gap
approval_block: invalid_without_charter
```

---

## 8. Non-Actions

- 不修改 `GF-003` 原文件；本 schema **不得**当作已生效 Evidence 合同  
- 不关闭 OQ-GF-005/013/014/015/017/018；不关闭 D-048  
- 不降低 fail-closed / 停止线  
- 标记 `[PROPOSAL]` 的字段与规则不得写入迁移记录为 FACT  

---

*03_EVIDENCE_PACKAGE_V0.2_SCHEMA.md · REVIEW/GF-003 · TASK-GF-003-B · 2026-09-18*
