# UNTRACKED-ASSET-DISPOSITION-EXECUTION-01

```text
Document Type : Execution Record (执行结果登记；非决定、非权威结论)
supersedes    : —
superseded_by : —
readers       : Owner；MIMO CODE；Migration Authority（待设立）；后续 audit 执行者
Status        : CLOSED
Date          : 2026-09-28
Authority     : Owner 授权（UNTRACKED ASSET DISPOSITION 执行令，2026-09-28）
Input         : UNTRACKED-ASSET-DISPOSITION-LIST-01.md（处置清单，提案）
Scope         : 仅登记已执行的处置动作与状态变更；不改写任何历史证据结论
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 本文件与处置清单的分工

```text
UNTRACKED-ASSET-DISPOSITION-LIST-01.md      = 处置前的提案（当前状态参考文档，可修正路径）
UNTRACKED-ASSET-DISPOSITION-EXECUTION-01.md = 处置后的执行结果登记（本文件）
REPORT-G/H/I/K                              = as-of 2026-09-17 历史证据（不修改）
```

**原则**：历史证据 ≠ 当前状态。故本文件**不修改** `REPORT-*`，
而用本文件独立登记其状态的**变化**，避免下一轮审计把已解决项重新报为 gap。

---

## 1. 执行结果：两个 commit

```text
AITutor-X    main                    40e0816
    docs: disposition untracked governance artifacts and restore evidence chain
    12 files changed, 4410 insertions(+), 0 deletions(-)

AITutors-v3  od01-r3-convergence     a4cf6a6
    docs: restore untracked consumer-identity verification design chain (G8)
    5 files changed, 1299 insertions(+), 0 deletions(-)
```

**说明：为何是两个 commit 而非一个。**
`AITutor-X` 与 `AITutors-v3` 是两个独立 git 仓库，无法以单次 commit 跨仓提交。
Owner 的「single commit」要求按「一个治理事件 = 每仓一个提交」执行，两提交同属
`UNTRACKED ASSET DISPOSITION` 事件。

---

## 2. 逐组执行登记

| 组 | 范围 | 授权动作 | 实际结果 |
|---|---|---|---|
| **G1** | X `Docs/60_REPORTS/` 治理文档（A1–A8） | (a) COMMIT | ✅ 8 份入库 |
| **G2** | X probe（A9 + A8 结果） | (b) ARCHIVE（方案 B） | ✅ 移入 `PRIMARY-PATH-MINIMAL-LOOP-01-artifacts/` |
| **G4** | X `e2e_run/inputs/*.pdf` | (c) EXCLUDE + .gitignore | ✅ `.gitignore:59` `*.pdf` |
| **G8** | V3 `CONTRACTS/` 设计文档（B1/B3–B6） | (a) COMMIT | ✅ 5 份入库 |
| **G4b** | X `caseC_wrongext.txt` | 未列入授权 | ⏳ **PENDING**（本次首次登记，见 §5） |
| G3/G5/G6/G7/G9/G10 | 其余组 | 未授权 | ⛔ 未执行（保持原状） |

### 2.1 G1 明细（X，8 份）

```text
Docs/60_REPORTS/E2E-VERIFICATION-REPORT.md
Docs/60_REPORTS/E2E-VERIFICATION-EXECUTION-REPORT.md
Docs/60_REPORTS/MIMO-PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION.md
Docs/60_REPORTS/REPORT-G-GOVERNANCE-RECONCILIATION-MATRIX.md
Docs/60_REPORTS/REPORT-H-AUTHORITY-CONFLICT-REGISTRY.md
Docs/60_REPORTS/REPORT-I-MIGRATION-GATE-DEFINITION.md
Docs/60_REPORTS/REPORT-K-SOURCE-LINEAGE-AUDIT.md
Docs/60_REPORTS/UNTRACKED-ASSET-DISPOSITION-LIST-01.md
```

**Temporal Scope 追加（G/H/I/K 各 1 行，add-only）：**

```text
Temporal Scope: This report reflects repository state as of 2026-09-17.
Subsequent commits have not been re-audited. Findings are as-of that date and are
retained as historical audit artifacts; they are not current-state authority.
```

插入位置：G→第 9 行、H→第 7 行、I→第 7 行、K→第 10 行（各自 header block 末行之后）。
**未改写任何 findings、未改日期、未改结论。**

### 2.2 G2 明细（probe 归档，方案 B）

```text
原位置                                          → 现位置
Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-PROBE.py
    → Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-01-artifacts/30-minimal-loop-probe.py
Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-PROBE-RESULT.md
    → Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-01-artifacts/20-minimal-loop-probe-result.md
新增：
    → Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-01-artifacts/README.md
```

编号依据本仓先例 `X2.7-INT-FULL-01-artifacts/`（产物在前、脚本在末位）。

**内容完整性实测（disk vs git blob 逐字节）：**

```text
30-minimal-loop-probe.py          7020b == 7020b   identical = True
20-minimal-loop-probe-result.md   2286b == 2286b   identical = True
```

⇒ **移动未损坏任何内容**（两个文件逐字节一致）。

**可复现性缺口（登记，未修复）：**
脚本第 9 行依赖 `D:\Project\AITutor-X\_audit_scratch\backend`，该目录实测**已不存在**
⇒ 脚本当前**不可独立复现**。因脚本 + 结果 + 执行证明必须同 bundle 才构成完整证据，
故按方案 (B) 一并归档，**不分离**。详见该目录 `README.md §3`。

### 2.3 G4 明细（PDF 边界保护）

```text
.gitignore 追加：
    # Binary document fixtures (source corpus; evidence kept in reports, not the binary)
    # Disposition: UNTRACKED-ASSET-DISPOSITION-LIST-01.md §2.3 (group G4, decision (c) EXCLUDE)
    *.pdf
```

**实测覆盖（`git check-ignore` 逐文件）：**

```text
IGNORED  e2e_run/inputs/caseA_real.pdf        (.gitignore:59)
IGNORED  e2e_run/inputs/caseB_real_exam.pdf   (.gitignore:59)
IGNORED  e2e_run/inputs/caseC_empty.pdf       (.gitignore:59)   ← 0 B，亦被覆盖
VISIBLE  e2e_run/inputs/caseC_wrongext.txt                      ← 见 §5
```

**勘误登记**：处置清单 §2.3 表格原将 `caseC_empty.pdf` 与 `caseC_wrongext.txt` 同列为
「随证据 (b) ARCHIVE」，与 G4 行的 **(c) EXCLUDE** 自相矛盾。
实际 `*.pdf` 规则**一并覆盖 0 B 的空 PDF**，该行已修正为 **(c) EXCLUDE**。
另：G4 行原写「2 份」，实测 PDF 共 **3 份**（含 0 B 那份），已修正为 3。

### 2.4 G8 明细（V3，5 份）

```text
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-DESIGN-v1.1.md
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-PLAN-v1.md
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-READINESS-v1.md
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-REPORT-PHASE1.md
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-REPORT-PHASE2.md
```

内容字节未改（未加 header、未改 status）。

**⚠️ Authority 声明（重要）：入库 ≠ 授予权威。**
`DESIGN-v1.1` 自陈 `IMPLEMENTATION READY DESIGN`，`REPORT-PHASE1.md` 自陈
`Status: IMPLEMENTED / TESTS PASS`，`DESIGN-v1.1` 并含「V3-side self-declared freeze」表述。
按 `AGENTS.md` 原则 1 与 4（Provenance ≠ Quality Authority；Git presence ≠ Authority），
**本次 commit 不构成 D2/D3/D4 裁决**，亦不使该文档成为 interface authority。
其 D2/D3/D4 裁决仍 `pending Owner`（`REPORT-I §2.2` / OD-002、OD-003）。

---

## 3. **F7 状态变更登记**（本文件的核心目的）

`REPORT-I-MIGRATION-GATE-DEFINITION.md §1 F7` 原文（as-of 2026-09-17）：

```text
F7 | Design v1.1 authority 锚定 | untracked / authority unknown
   | 凡迁移物引用 Design v1.1 作为接口权威，必须先完成 Owner 处置
```

**实测现状（2026-09-28）：**

| 维度 | as-of 2026-09-17 | 现状 2026-09-28 |
|---|---|---|
| Design v1.1 git 状态 | untracked | ✅ **TRACKED**（V3 `a4cf6a6`） |
| 引用的 9 份 CONTRACTS 文档丢失风险 | HIGH | 其中 5 份**已入库**；4 份仍 untracked（见 §4） |
| Authority 是否已定 | unknown | ⚠️ **仍 unknown**（未裁决） |
| F7 是否关闭 | — | ⚠️ **部分解决** |

**准确结论：**

```text
F7 的「untracked / 丢失风险」部分 → 已解决（DESIGN-v1.1 及 4 份实现文档已入库）
F7 的「authority unknown」部分     → 未解决（需 Owner 裁决 D2/D3/D4，见 REPORT-I §2.2）
F7 整体                            → 不得标 CLOSED，应标 PARTIAL
```

> **给后续审计的提示（防假阳性）**：下一轮审计**不应**再把
> 「DESIGN-v1.1 未入 git」报为 gap —— 该项已于 `a4cf6a6` 解决。
> 但「DESIGN-v1.1 authority 未定」**仍是真实 OPEN 项**，应继续报。
> 二者不可混为一谈。

**未修改 `REPORT-I` 本体**（其为 as-of 2026-09-17 历史证据）；本登记为其状态变更的独立记录。

---

## 4. 执行后仍未跟踪的资产（盘点）

```text
AITutor-X   : 81 entries（其中 1 项为本文件的父清单 modified，非新资产）
AITutors-v3 : 6 entries
```

**AITutors-v3（6 项）**：

```text
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-DESIGN-v1.md    (B2, 建议 (b) ARCHIVE)
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-CONSUMER-REVIEW.md                    (B7, 建议 (b) ARCHIVE)
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT-SKELETON.md                (B8, 建议 (b) ARCHIVE)
Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT.md                                    (B9, 建议 (b) ARCHIVE)
Docs/GOVERNANCE/                                                                            (B10–B13, G9, 未授权)
backend/provider_reality.json                                                               (B14, G10, 未授权)
```

⇒ **§3 表中「其中 5 份已入库、4 份仍 untracked」即指 B2/B7/B8/B9。**

**AITutor-X**：`tools/` ×46、`e2e_run/` 运行产物、`Docs/90_ARCHIVE/misc/`、`review_pif1_evidence/`
（对应 G3/G5/G6/G7，**均未授权执行**，保持原状）。

---

## 5. G4b — `caseC_wrongext.txt` 首次登记（待裁决）

**这是处置清单的遗漏项，本文件补登记。**

```text
文件     : e2e_run/inputs/caseC_wrongext.txt
大小     : 17 B
性质     : 畸形扩展名 fixture（.txt 承载本应为 PDF 的输入）
忽略状态 : 实测 VISIBLE —— *.pdf 不覆盖，git 仍视其为未跟踪
影响     : e2e_run/inputs/ 因它保持「未跟踪目录」状态
```

**未执行任何动作**：它不在 Owner 授权的 6 项范围内。
按 `AGENTS.md`「不删除旧文档/旧代码」，已排除删除选项。

**裁决点（三选一，待 Owner）**：

```text
(a) COMMIT   — 作为负向测试 fixture 入库
(b) ARCHIVE  — 与 G3 运行产物一并归档
(c) EXCLUDE  — 判定一次性产物，加 ignore
```

**已并入处置清单 §2.3 与 §4 汇总表（G4b 行）。**

---

## 6. 边界声明（本执行未做的事）

```text
未修改 REPORT-G/H/I/K 的任何 findings/结论/日期        ✅
未修改 Frozen Spec 或任何 Decision 文档                ✅
未删除任何文件（含 tools/ 46 份）                       ✅
未提交 provider_reality.json                           ✅
未提交 tools/ / e2e_run/ 运行产物 / 90_ARCHIVE / review_pif1_evidence ✅
未触碰 Papers（Producer）仓库                          ✅
未创建 / 未重编号 DEC / BUG / OQ ID                     ✅
未对 D2/D3/D4 做任何裁决                               ✅
未修复 probe 的可复现性缺口（仅登记）                    ✅
```

**核验方式（实测，非声明）：**

```text
两个 commit 中匹配 tools/ | e2e_run/ | provider_reality | 90_ARCHIVE 的文件数 = 0
probe 两文件 disk vs git blob 逐字节一致 = True
G/H/I/K 提交 numstat 删除行 = 0（add-only）
临时分析脚本清理 = 0 残留
```

---

## 7. 后续待办（不属本次授权）

```text
1. G4b caseC_wrongext.txt 裁决（§5）
2. G3 / G5 / G6 / G7 归档或排除裁决
3. G9  Docs/GOVERNANCE/ G0 四件套裁决 —— 建议并入 F3 Authority Taxonomy 裁决
4. G10 provider_reality.json 排除
5. B2 / B7–B9 archive-only 处置
6. REPORT-I §2.1 四项 P0（Migration Authority / Gate 批准 / 唯一 Taxonomy / Set B）
7. REPORT-I §2.6 两条 STALE 条目的 CLOSED 登记
```

*Prepared 2026-09-28 by DSH（治理收口角色）。Status: CLOSED（本登记动作已完结；§7 为后续待办）。*
