# 04 — Lineage Model v0.2

**Document class**: REVIEW PROPOSAL（模型设计，非已冻结规范）  
**Task**: TASK-GF-003-B  
**Date**: 2026-09-18  
**Extends**: `GF-002-ARTIFACT-LINEAGE-SPECIFICATION.md`（**原文件不修改**）

**Classification**: `[FACT]` / `[PROPOSAL]` / `[UNKNOWN]` / `[NEED OWNER DECISION]`

**问题焦点**（任务书）: 同一路径不同时间不同字节状态 · restore 事件 · IR locator 漂移 · **interface hash 验证 ≠ IR locator 验证**

---

## 1. 模型升级 `[PROPOSAL]`

```text
v0.1 (GF-002 现行)     path  →  hash  →  identity

v0.2 (本 PROPOSAL)     logical identity
                           ↓
                       carrier observation
                           ↓
                       content fingerprint
                           ↓
                       authority state
```

**不废除** `[PROPOSAL]`: 双层 sha（PDF vs OCR md）`[FACT: REPORT-K；GF-002 §2]`；Contract path non-identity `[FACT: GF-003 P2 / Contract v0.2]`；L1–L6 层链 `[FACT: GF-002 §1]`。

**v0.1 缺口** `[FACT]`: GF-002 无时间维/载体态；恢复事件未建模；V-Manifest 与 V-Snapshot 未分列 interface vs locator（GF-002 §6）。

---

## 2. 核心定义 `[PROPOSAL]`

### 2.1 Carrier（载体）

| Field | Definition |
|-------|------------|
| **Meaning** | 持有字节的**逻辑对象**；身份 ≠ 目录路径 |
| **carrier_id** | 治理分配 |
| **logical_role** | RSD-A / RSD-B / PIS-operational / OCRA-tree / SEM-ledger / GOV-doc / EVD-ledger / EXT-capability / … |
| **declared_locators[]** | 观测过的 path（可多个；仅 locator） |
| **bytes_kind** | pdf \| ocr_md \| manifest \| ir \| document \| code \| … |
| **authority_status** | unknown \| claimed_only \| verified \| disputed |

**双树映射** `[FACT 计数 + PROPOSAL 角色名]`:

| Carrier | logical_role | Evidence |
|---------|--------------|----------|
| `D:\Project\Papers\original\` | RSD 候选 A（authority UNKNOWN） | REPORT-K：PDF 38,893；basename 交集 12,626；抽样 6/6 sha 一致 |
| `D:\Project\Papers\maintainess\PDF` | PIS-operational `[FACT]` | REPORT-K：`PDF_ROOT` 硬编码；恢复后 12,707 PDF |
| `D:\Project\Papers\Ocr-markdown\` | OCRA-tree | REPORT-K：md 树；manifest 166 |
| `D:\Project\Papers\data\*.json` 等 | SEM/EVD ledger | REPORT-K：部分 tracked；snapshot/manifest |

**禁止** `[PROPOSAL，延续 GF-001]`: 不假设 maintainess 权威；不假设 original 权威；Path ≠ Role ≠ Authority。

### 2.2 Carrier Observation（观测）

| Field | Definition |
|-------|------------|
| **observation_id** | 不可变 ID |
| **carrier_id** | 外键 |
| **observed_at** | 时点（显式时区） |
| **observed_by** | actor / tool / session |
| **method** | full_inventory \| sample_recompute \| manifest_crosscheck \| owner_attested |
| **content_fingerprint.sha256** | 对该次覆盖 bytes |
| **content_fingerprint.hash_meaning** | 必填 |
| **bytes_coverage** | full \| sample_n \| manifest_subset |
| **snapshot_locator** | 观测清单只读路径（可空） |
| **restoration_event_ref** | 可空 |

**hash 归属** `[PROPOSAL]`: hash 属于 **Observation**（时点事实）。治理引用须带 `observation_id` 或 `observed_at`。

### 2.3 Carrier State（状态序列）

| Field | Definition |
|-------|------------|
| **carrier_id** | |
| **state 推导** | 由 observation 序列推导；**禁止**覆盖历史 |
| **inventory_claimed** | 声称数量（如 12,707） |
| **inventory_verified** | 已验证数量（可 < claimed） |
| **completeness_class** | A/B/C/D **挂在 Observation** `[PROPOSAL]` |
| **lineage_status** | 见 §5 |

**当前 State 摘要** `[FACT]`:

| Carrier | claimed | verified | 缺口 |
|---------|---------|----------|------|
| maintainess/PDF | 12,707（恢复后实测） | 计数+抽样 6 组 | 恢复前全量 hash = UNKNOWN（UNKNOWN-004）；增减清单 NOT VERIFIED |
| original/ | PDF 38,893 等 | 抽样一致 | 是否 canonical RSD = UNKNOWN（OQ-GF-001） |
| OCR md 树 | 源树≈4,224；清单 1,801；manifest 166（sha 87） | 有清单/manifest 者可复算 | 清单外 Class B/D；UNKNOWN-003 |
| 接口 snapshot | n_rows=87 | r50 match 87；IR ADMITTED match 71 | 71≠87≠166 三层不等 |

### 2.4 Restoration Event（恢复事件）`[PROPOSAL]`

```text
restoration_event
├─ restoration_event_id
├─ carrier_id
├─ incident_ref                 # 可考则填；否则 UNKNOWN
├─ pre_event_state_ref          # 无则 UNKNOWN + 原因
├─ post_event_state_ref         # 必填
├─ evidence_standard            # count+sample | full_hash_ledger | owner_attested
│                                 # 充分性 = OQ-GF-005 [FACT: OPEN，不关闭]
├─ byte_level_equivalence       # match | mismatch | not_verified
└─ open_questions[]             # 如 OQ-GF-005
```

**已观测事件** `[FACT]` REPORT-K §1.11 / UNKNOWN-004:
- 会话中途 `maintainess/PDF` 观测仅 6 文件；Owner 声明误删并已恢复
- 恢复后复测 12,707 PDF
- **byte_level_equivalence = not_verified**（无恢复前全量 hash 台账）
- 6 文件态 **不得**作语料治理结论

### 2.5 Verification 与 Authority

| 概念 | v0.2 定义 `[PROPOSAL]` |
|------|------------------------|
| **Verification** | 对某 Observation 的 method + result + timestamp + environment；fail-closed `[FACT: P5 保留]` |
| **Authority** | 治理裁决状态；**验证通过 ≠ 权威成立**（Provenance ≠ Quality `[FACT: AGENTS.md]`） |
| **authority state** | unknown / claimed_only / verified / disputed + frozen_ref（若有） |

---

## 3. 同一路径 · 不同时间 · 不同字节状态

**场景** `[FACT]`: `D:\Project\Papers\maintainess\PDF`

| 时点 | 观测 | 字节状态含义 |
|------|------|--------------|
| 首跑日志 `2026-09-06 10:42:46` | 扫根目录 12,528 / 合计 12,703 `[FACT: REPORT-K / ocr log]` | 历史 PIS 候选；**pre-git**，代码 Input path = `[UNKNOWN]` |
| git 首 commit `85784a9` `2026-09-12` | 代码入库 | 晚于首跑 `[FACT: REPORT-K]` |
| 本轮审计中途 | 6 文件 | **误删过程态** `[FACT: REPORT-K §1.11]` |
| Owner 恢复后 | 12,707 PDF | 当前 operational 观测；与 12,703 差额 +4，清单 NOT VERIFIED `[FACT]` |

**v0.2 规则** `[PROPOSAL]`:
1. path `maintainess/PDF` **不**携带身份；身份 = Carrier + Observation(fingerprint, observed_at)。  
2. 引用「12,707」必须绑定恢复后 observation；引用「12,703」绑定首跑日志 observation。  
3. 首跑输入路径字节级 = `[UNKNOWN]`（无 pre-git 快照）`[FACT: GF-001 §2.2 / REPORT-K]`；不得升格。  
4. OQ-GF-001/004/005/006 **不因**本模型自动关闭。

---

## 4. Interface Integrity ≠ Locator Integrity

### 4.1 观测数字 `[FACT]`

| 指标 | 值 | Evidence |
|------|-----|----------|
| reslice/接口 manifest 总数 | 166 | REPORT-K §4 |
| 其中含 sha 键 | 87 | REPORT-K |
| interface snapshot n_rows | 87 | `interface_scope_snapshot_step1.json` |
| r50 source sha match | 87/87 | 同上 |
| ir_admitted sha match | **71** | 同上 |
| OCR 输出清单条目 | 1,801（全含 `source_sha256`=PDF 字节） | REPORT-K §4 |
| 源树 md 约 | 4,224 | REPORT-K |

### 4.2 两类验证 `[PROPOSAL]`

| 验证 | 对象 | 方法 | 通过条件 |
|------|------|------|----------|
| **Interface Integrity** | 接口/冻结定义层 | manifest/接口键 `hash_meaning` + 语义 == Frozen Contract v0.2 identity 定义 | 接口键可复算且与冻结定义一致 |
| **Locator Integrity** | 具体 IR/条目 | `ir.locator → 当前 bytes → sha256 == 登记 sha` | 逐条 match；fail-closed |

**不可互相替代** `[PROPOSAL]`:

```text
Interface Integrity PASS  ⇏  Locator Integrity PASS
Locator Integrity PASS    ⇏  全树 lineage 完整
INTERFACE_VERIFIED ∧ LOCATOR_LINEAGE_BROKEN  ⇒ 该 IR 不得迁移本体
两者 PASS ∧ coverage_class=A  ⇒ 仅可作数据类 Gate 证据输入（仍须 Gate 9 有效）
```

**易混读纠正** `[PROPOSAL]`: 「snapshot 87/87 match」≠ 「全部 166 manifest 或全部 IR locator 已验证」。71/87 差值须单独 disposition，不得用 interface 结论掩盖。

---

## 5. Lineage State 定义 `[PROPOSAL]`

| 状态 | 含义 | 典型触发 |
|------|------|----------|
| `INTERFACE_VERIFIED` | 接口键/冻结 identity 定义对账通过 | Contract 四元组 + 样本一致 `[FACT 锚: REPORT-I F1]` |
| `LOCATOR_VERIFIED` | 当前 bytes 可解析且 sha match | snapshot 87/87；IR 71 子集 `[FACT]` |
| `LINEAGE_BROKEN` | 登记 hash ≠ 当前 bytes，或 locator 失效 | 恢复后未复算；文件漂移 |
| `REBUILD_REQUIRED` | 需按可复现流水线重建才可信 | 大范围 Class B；pre-git 链 `[UNKNOWN]` |
| `CARRIER_UNKNOWN` | 载体权威未裁 | 双树 OQ-GF-001 未关 `[FACT: OPEN]` |
| `EVIDENCE_LOCAL_ONLY` | 证据仅本地可核验 | REPORT-G/H/I/K untracked `[FACT: git ls-files]` |
| `RESTORATION_UNVERIFIED` | 恢复事件 byte equivalence 未验 | maintainess/PDF 现状 `[FACT: UNKNOWN-004]` |

**与 Completeness Class 关系** `[PROPOSAL]`: Class A/B/C/D = 登记完整度；lineage_status = 当前可验证状态。二者同时记录，不互相覆盖。

---

## 6. v0.2 Lineage Diagram `[PROPOSAL 结构 + FACT 计数]`

```text
[UNKNOWN 上游 / Papers 之外]  OQ-GF-006 · UNKNOWN-002/005 — 不升格
                │
                ▼ 血缘方向 UNKNOWN
┌───────────────────────────────────────┐
│ Carrier RSD-A : original/             │
│ authority: UNKNOWN (OQ-GF-001)        │
│ obs: PDF 38,893 / DOCX 30,254 / …    │
└───────────────────┬───────────────────┘
                    │ name∩ 12,626; sample 6/6 sha equal [FACT]
                    ▼
┌───────────────────────────────────────┐
│ Carrier PIS : maintainess/PDF         │
│ operational OCR input [FACT]          │
│ Restoration: delete→restore           │
│ post: 12,707 · equivalence not_verified│
│ state: RESTORATION_UNVERIFIED         │
└───────────────────┬───────────────────┘
                    │ L1: source_sha256 = PDF bytes
                    │ [FACT: ocr_output_manifest.jsonl 1,801]
                    ▼
┌───────────────────────────────────────┐
│ Carrier OCRA : Ocr-markdown/          │
│ L2: sha256(ocr_md_bytes)              │
│ coverage: 1,801 manifest ⊂ tree≈4,224 │
│ Class A/B/D 子集并存 [FACT]           │
└───────────┬───────────────┬───────────┘
            │               │
            ▼               ▼
┌───────────────────┐  ┌──────────────────────────┐
│ EVD/SEM manifests │  │ L3 Semantic annotation   │
│ 166 · sha=87      │  │ stage + execution hash   │
│ snapshot n=87     │  │ [FACT: reslice 产物区]   │
└─────────┬─────────┘  └────────────┬─────────────┘
          │ INTERFACE_VERIFIED       │
          │ LOCATOR: match 87/87     │
          │ IR ADMITTED match 71     │
          ▼                          ▼
┌──────────────────────────────────────────────────┐
│ L4 Question IR（历史）                            │
│ ir.source_sha256 = OCR md bytes [FACT]           │
│ V3: IR transient → candidate payload [FACT:20 §1]│
│ locator_status 逐条 · LINEAGE_BROKEN 隔离         │
└──────────────────────┬───────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────┐
│ L5 Admission Candidate                            │
│ input_identity + build_versions + Gate evidence   │
│ LLM 无 Admission Authority [FACT: V3 00 P2]      │
└──────────────────────┬───────────────────────────┘
                       │ Gate 1–10 + EvidencePackage v0.2
                       │ F4/F5 + OQ-GF-014/015 [FACT: OPEN]
                       ▼
┌──────────────────────────────────────────────────┐
│ L6 AITutor-X Entity                               │
│ repo@commit + path + sha + record_id             │
│ post_copy_sha256 + rollback_ref                   │
│ Cluster A 未关 ⇒ 默认无 active migrated entity   │
│ [FACT: REPORT-I §0.7]                             │
└──────────────────────────────────────────────────┘
```

---

## 7. 状态机 — 验证结果如何影响迁移资格 `[PROPOSAL]`

```text
Observation 完成
    │
    ├─ hash mismatch ──────────────► LINEAGE_BROKEN ──► BLOCK（不得迁本体）
    │
    ├─ not_verified ───────────────► 保持 Class B/D ──► 不得称 verified
    │
    ├─ Interface PASS only ────────► INTERFACE_VERIFIED
    │         │                         仅文档/接口副本可议；IR 本体不可迁
    │         ▼
    ├─ Locator PASS（子集）────────► LOCATOR_VERIFIED(subset)
    │         │                         须标注 coverage；非全树
    │         ▼
    ├─ authority unknown ──────────► CARRIER_UNKNOWN
    │         │                         OQ-GF-001/002 未关前数据模式不默认放行
    │         ▼
    ├─ approval_block invalid ─────► invalid_without_charter
    │         │                         Gate 9 无授权人 [FACT: F4]
    │         ▼
    └─ 仍 DEFAULT-BLOCKED（Cluster A）until Owner
```

---

## 8. 与 OQ 关系（不关闭）

| OQ | 与本模型关系 | 动作 |
|----|--------------|------|
| OQ-GF-001 | Carrier 权威仍 UNKNOWN | 不关闭 |
| OQ-GF-002 | 数据引用/交付模式未裁 | 不关闭 |
| OQ-GF-003 | hash 词面 vs 目录；v0.2 强化 hash_meaning/bytes_kind | 不关闭 |
| OQ-GF-004 | 双树保留策略 | 不关闭 |
| OQ-GF-005 | Restoration evidence 充分性 | 不关闭 |
| OQ-GF-006 | 血缘方向 | 不关闭 |
| OQ-GF-007 | lineage 补全 | 不关闭 |
| OQ-GF-013/014/015 | Set B / Authority / Taxonomy | 不关闭 |

---

## 9. Non-Actions

- 不修改 GF-002 原文件  
- 不将本模型写成 Frozen lineage 规范  
- 不关闭任何 OQ；不假设双树任一权威  
- 不执行 re-index / 数据迁移 / hash 全量台账立项（均待 Owner）  

---

*04_LINEAGE_MODEL_V0.2.md · REVIEW/GF-003 · TASK-GF-003-B · 2026-09-18*
