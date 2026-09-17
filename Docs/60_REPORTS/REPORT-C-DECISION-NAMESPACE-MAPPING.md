# Report C — AITutorX Decision Namespace Mapping

**日期**: 2026-09-16
**目的**: 建立 Legacy ID → Canonical AIT Decision ID 映射，消除跨 repo 命名冲突

---

## 1. 命名空间问题

两 repo 独立使用 `DEC-*` 编号，DEC-012~036 范围存在大量冲突。

**冲突组**:
- DEC-021: V3=FINALIZATION v1 four decisions / Producer=CONTRACT-DECISION-FINALIZATION
- DEC-022: V3=Interface Decision Finalization / Producer=INTERFACE-DECISION-FINALIZATION
- DEC-023~026: V3=FINALIZATION 系列 / Producer=Contract Freeze Candidate 系列
- DEC-027~036: 两 repo 各有不同含义

---

## 2. Canonical AIT Decision ID 映射

### 2.1 V3 Consumer DEC → AIT-DEC (001–036)

| Legacy | Canonical | Topic |
|--------|-----------|-------|
| DEC-001~010 | AIT-DEC-001~010 | EB-004/EB-008 系列 |
| DEC-011 | AIT-DEC-011 | EB-004 Owner confirmation |
| DEC-012~020 | AIT-DEC-012~020 | EB-008 design/review 系列 |
| DEC-021 | AIT-DEC-021 | FINALIZATION v1 (B1-B4) |
| DEC-022 | AIT-DEC-022 | Interface Decision Finalization v1 |
| DEC-023 | AIT-DEC-023 | FINALIZATION v1 four decisions |
| DEC-024 | AIT-DEC-024 | Contract v0.2 Freeze Candidate Review |
| DEC-025 | AIT-DEC-025 | Contract v0.2 Freeze Candidate Final |
| DEC-026 | AIT-DEC-026 | Owner Final Decision Instruction |
| DEC-027 | AIT-DEC-027 | Interface Decision Finalization v1 |
| DEC-028 | AIT-DEC-028 | Interface Finalization Revision v1 |
| DEC-029 | AIT-DEC-029 | Freeze Candidate Review v1 |
| DEC-030 | AIT-DEC-030 | Freeze Candidate Finalization |
| DEC-031 | AIT-DEC-031 | Owner Final Decision v1 |
| DEC-032 | AIT-DEC-032 | freeze-pre final registration |
| DEC-033 | AIT-DEC-033 | Freeze Finalization Audit |
| DEC-034 | AIT-DEC-034 | Freeze Object Final Alignment |
| DEC-035 | AIT-DEC-035 | Freeze Artifact remote reproducibility |
| DEC-036 | AIT-DEC-036 | Contract v0.2 FROZEN |

### 2.2 Producer DEC → AIT-DEC (101–138)

| Legacy | Canonical | Topic |
|--------|-----------|-------|
| DEC-012 | AIT-DEC-101 | Owner B1-B3 裁决 |
| DEC-013 | AIT-DEC-102 | EB-008 Design Frozen |
| DEC-014 | AIT-DEC-103 | Agent Completion Protocol |
| DEC-015 | AIT-DEC-104 | EB-008 Owner Feedback |
| DEC-016 | AIT-DEC-105 | Owner 四项冻结决策 |
| DEC-017 | AIT-DEC-106 | EB-008 Owner 确认入册 |
| DEC-018 | AIT-DEC-107 | EB-008 Design Frozen |
| DEC-019 | AIT-DEC-108 | Owner B1-B3 裁决回应 |
| DEC-020 | AIT-DEC-109 | DEC-B1 分项裁决入册 |
| DEC-021 | AIT-DEC-110 | CONTRACT-DECISION-FINALIZATION |
| DEC-022 | AIT-DEC-111 | INTERFACE-DECISION-FINALIZATION |
| DEC-023 | AIT-DEC-112 | INTERFACE-FINALIZATION-REVISION |
| DEC-024 | AIT-DEC-113 | Contract v0.2 Freeze Candidate Review |
| DEC-025 | AIT-DEC-114 | Contract v0.2 Freeze Candidate Final |
| DEC-026 | AIT-DEC-115 | Owner Final Decision Instruction |
| DEC-027 | AIT-DEC-116 | Contract v0.2 final freeze closeout |
| DEC-028 | AIT-DEC-117 | Producer-side Contract Freeze final |
| DEC-029 | AIT-DEC-118 | Contract v0.2 Freeze Producer Final Audit |
| DEC-030 | AIT-DEC-119 | Producer Final Freeze Object Verification |
| DEC-031 | AIT-DEC-120 | Contract v0.2 Freeze Artifact final remote |
| DEC-032 | AIT-DEC-121 | Contract v0.2 FROZEN registration |
| DEC-033 | AIT-DEC-122 | Producer Frozen Baseline Final Integrity |
| DEC-034 | AIT-DEC-123 | Producer Frozen Baseline Archive Final |
| DEC-035 | AIT-DEC-124 | Producer Frozen Baseline Guardian Mode |
| DEC-036 | AIT-DEC-125 | Guardian During Consumer Phase 1 |
| DEC-037 | AIT-DEC-126 | Phase 2 Pre-Start Baseline Check |
| DEC-038 | AIT-DEC-127 | Consumer Phase 2 Guardian round 2 |
| DEC-039 | AIT-DEC-128 | Guardian During Phase 2-M3 |
| DEC-040 | AIT-DEC-129 | Phase 2-M4 Guardian Check |
| DEC-041 | AIT-DEC-130 | adversarial review of DEC-040 |
| DEC-042 | AIT-DEC-131 | Consumer M5 Boundary Guardian |
| DEC-043 | AIT-DEC-132 | adversarial review of DEC-042 |
| DEC-044 | AIT-DEC-133 | Consumer Boundary Closure |
| DEC-045 | AIT-DEC-134 | DSH self adversarial audit |
| DEC-046 | AIT-DEC-135 | Owner ruling on DEC-045 |
| DEC-047 | AIT-DEC-136 | Consumer Boundary Closure Guardian Review |
| DEC-048 | AIT-DEC-137 | Phase 2.5 Consumer Data Activation Guardian |
| DEC-049 | AIT-DEC-138 | D2/D3/D4 Decision Brief |

---

## 3. OQ Namespace

| Legacy | Repo | Canonical | 说明 |
|--------|------|-----------|------|
| OQ-1~21 | V3 | AIT-OQ-001~021 | Consumer Open Questions |
| (none) | Producer | — | Producer 无独立 OQ |

## 4. BUG Namespace

| Legacy | Repo | Canonical | 说明 |
|--------|------|-----------|------|
| BUG-V3-001~050 | V3 | AIT-BUG-001~050 | Consumer bugs |
| (various) | Producer | AIT-BUG-101+ | Producer bugs in bugs.md |

---

## 5. 命名空间规则

1. **不重写历史** — Legacy ID 保留在映射表中
2. **未来新决策** 使用 `AIT-DEC-*`（从 AIT-DEC-200 开始）
3. **引用格式**: `AIT-DEC-XXX (was V3 DEC-YYY / was DSH DEC-ZZZ)`
4. **OQ / BUG** 同理: `AIT-OQ-*` / `AIT-BUG-*`
