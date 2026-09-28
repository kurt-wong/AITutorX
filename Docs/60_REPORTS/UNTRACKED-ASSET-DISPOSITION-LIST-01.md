# UNTRACKED-ASSET-DISPOSITION-LIST-01

```text
Document Type : Disposition List (PROPOSAL — 待 Owner 裁决，非决定)
supersedes    : —
superseded_by : —
readers       : Owner（裁决方）；MIMO CODE（执行方，需单独授权）；Migration Authority（待设立）
Status        : OPEN
Date          : 2026-09-28
Authority     : REPORT-I-MIGRATION-GATE-DEFINITION.md §1 F7 / §5
                AGENTS.md 原则 4（Git presence ≠ Authority）、原则 5（未经 Migration Gate 不得进入 active tree）
Method        : 实地枚举 `git status --porcelain` + 逐文件读头部；未修改任何未跟踪文件
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 0. 本文件性质

本文件**不是**迁移授权，**不创建** DEC/BUG/OQ ID，**不修改**任何被枚举文件，**不代 Owner 裁决**。
它只做一件事：把当前未跟踪资产按 `REPORT-I` 的分类体系整理成**可逐项打勾的处置表**，供 Owner 执行 `REPORT-I §1 F7` 要求的处置动作。

处置动作仅三选一：

```text
(a) COMMIT   — 以指定 Authority Level 与路径入治理树
(b) ARCHIVE  — archive-only，标 UNTRACKED SNAPSHOT / AUTHORITY UNKNOWN，不进 active tree
(c) EXCLUDE  — 明确不迁，记录理由（或加入 .gitignore）
```

---

## 1. 实地枚举结果

```text
AITutor-X   : 89 top-level entries → 109 files → 1.28 MB
AITutors-v3 : 11 top-level entries →  14 files → 0.15 MB
```

关键结构事实（本次新查，影响处置判断）：

```text
AITutor-X tracked files 总计 : 305
Docs/ 已跟踪树               : 00_GOVERNANCE 17 / 10_SPEC 5 / 20_ARCHITECTURE 11
                               30_CONTRACTS 4 / 40_DECISIONS 36 / 50_OPERATIONS 19
                               60_REPORTS 134 / 90_ARCHIVE 1
```

⇒ `Docs/60_REPORTS/` 是**已建立的活跃证据树（134 份在库）**，且 `REPORT-A`~`REPORT-F` 已在库。
本文件 §2.1 的 8 份未跟踪文档，除 1 份外均属**该既有序列的缺失尾段**，路径位置本就正确，不存在"新建子树"问题。

---

## 2. AITutor-X 未跟踪资产

### 2.1 Docs/60_REPORTS/ — 治理级证据（8 份，0.21 MB）

| # | 文件 | 大小 | 日期 | 来源/角色 | 建议 Class | 建议动作 |
|---|---|---|---|---|---|---|
| A1 | `REPORT-G-GOVERNANCE-RECONCILIATION-MATRIX.md` | 24.0 KB | 2026-09-17 | Implementation Governance Analyst | 证据 L3/L4 | **(a) COMMIT** |
| A2 | `REPORT-H-AUTHORITY-CONFLICT-REGISTRY.md` | 13.3 KB | 2026-09-17 | 权威冲突登记册（只登记，不裁决） | 证据 L3 | **(a) COMMIT** |
| A3 | `REPORT-I-MIGRATION-GATE-DEFINITION.md` | 16.5 KB | 2026-09-17 | 迁移闸门定义（gate definition） | 证据 L3 | **(a) COMMIT** |
| A4 | `REPORT-K-SOURCE-LINEAGE-AUDIT.md` | 32.1 KB | 2026-09-17 | Independent Evidence Auditor | 证据 L3/L4 | **(a) COMMIT** |
| A5 | `E2E-VERIFICATION-REPORT.md` | 58.5 KB | 2026-09-25 | E2E 验证报告（含 fixture/commit/DB evidence） | 证据 L3 | **(a) COMMIT** |
| A6 | `E2E-VERIFICATION-EXECUTION-REPORT.md` | 47.8 KB | 2026-09-26 | E2E 执行证据记录（含 V3@d2b9a26 / Producer@2b92898 锚） | 证据 L3 | **(a) COMMIT** |
| A7 | `MIMO-PREPROCESSING-V3-LOCAL-INDEPENDENT-VERIFICATION.md` | 51.1 KB | 2026-09-22 | Independent Forensic Audit（Evidence-first） | 证据 L3/L4 | **(a) COMMIT** |
| A8 | `PRIMARY-PATH-MINIMAL-LOOP-PROBE-RESULT.md` | 2.3 KB | 2026-09-27 | READ-ONLY 探针结果 | 证据 L4 | **(a) COMMIT** |

**支撑 (a) 的三条事实：**

1. **路径已在既有树内** — `Docs/60_REPORTS/` 已有 134 份在库，`REPORT-A`~`REPORT-F` 已跟踪；A1/A2/A3/A4 是该序列的 G/H/I/K 续段，A5/A6 的 DSH 对抗审查版已被跟踪（`E2E-VERIFICATION-DSH-ADVERSARIAL-REVIEW.md`、`E2E-VERIFICATION-EXECUTION-DSH-ADVERSARIAL-REVIEW.md`），**只有被审查的正本未入库** ⇒ 现有证据链存在"只有评论、没有被评论对象"的悬空引用。
2. **A3 是 Phase B 的唯一合法入口** — `REPORT-I §2.1` 的 4 项 P0 与 `Gate 9` 依赖本文件被批准；不落库则后续任何迁移引用均悬空。
3. **A7 是身份工作的独立审计证据** — 与已签署的 `PRIMARY-PATH-IDENTITY-*` 证据链直接相关。

> **注意（不构成反对）**：A1–A4 撰写于 2026-09-17，其后 AITutor-X 已发生
> `45cc7da`/`4be2ba4`/`b5f9f9e`/`e969fac`/`1c500ba`/`e2c039d`/`a1f6d50` 等变更。
> `REPORT-I §2.6` 自陈部分条目已 STALE（如 OD-007 git init 已完成）。
> 故 (a) COMMIT 时应保留其**原始日期与结论**，不得回改正文；时效性另见 §5。

### 2.2 Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-PROBE.py — 需单独裁决（1 份）

| # | 文件 | 大小 | 建议 Class | 建议动作 |
|---|---|---|---|---|
| A9 | `PRIMARY-PATH-MINIMAL-LOOP-PROBE.py` | 7.0 KB | Probe（已失效） | **(b) ARCHIVE** 或 (c) EXCLUDE |

**依据（实测）：**

```text
A9 第 9 行：BACKEND = Path(r"D:\Project\AITutor-X\_audit_scratch\backend")
实测     ：D:\Project\AITutor-X\_audit_scratch  → 不存在（Test-Path = False）
```

⇒ 该探针**已不可复现**（依赖的 scratch 副本已被移除）；其 `RESULTS` 由 A8 保留。
且 `Docs/60_REPORTS/` 的既有惯例是把脚本放在 `*-artifacts/` 子目录（如 `X2.7-INT-FULL-01-artifacts/40-analyze_run.py`），
A9 直接裸放在 `60_REPORTS/` 根，与惯例不符。

**这也是 `REPORT-I §1 F7` 的一个未登记实例**：脚本以绝对路径引用仓库外 scratch，属 `§4 GAP-008`（绝对路径、path≠identity）同类问题。

### 2.3 e2e_run/ — 运行产物与 fixtures（32 份，1.02 MB）

**禁止整目录 `git add`。** 其中含二进制语料：

| 子类 | 代表文件 | 大小 | 建议动作 |
|---|---|---|---|
| ⚠️ **二进制语料 PDF** | `inputs/caseA_real.pdf` | 182.6 KB | **(c) EXCLUDE**（加 .gitignore） |
| ⚠️ **二进制语料 PDF** | `inputs/caseB_real_exam.pdf` | 350.9 KB | **(c) EXCLUDE**（加 .gitignore） |
| 空/畸形 fixture | `inputs/caseC_empty.pdf` (0 B)、`inputs/caseC_wrongext.txt` (17 B) | ~0 | 随证据 (b) ARCHIVE |
| 运行结果 JSON | `e2e-live-*.json`、`golden-report-b2*.json`、`negB/negC-report.json`、`replay-run2.json`、`diag-*.json` | ~250 KB | **(b) ARCHIVE** |
| 驱动脚本 | `e2e_live_full_chain.py`、`diag_ir.py`、`diag_prod_ir.py`、`_test_*.py`、`_expand_opts.py` | ~62 KB | **(b) ARCHIVE** |
| manifest fixtures | `golden/pac-c02-01.manifest.json`、`negB/`、`negC/`、`minimal-loop-manifest.json` | ~46 KB | **(b) ARCHIVE** |

**支撑 (c) 的理由**：`REPORT-I §5` 明确要求数据本体 **archive/external reference only**，并标注
`生产数据本体 Ocr-markdown/ 等 … 不入 git`。PDF 语料属同类；且 `A6` 已把这些 PDF 的文件名/来源写进执行报告，
**证据价值在报告文本中已保留，无需入库二进制本体**。

**支撑 (b) 的理由**：`A5` 头部自陈「证据目录：`D:\Project\AITutor-X\e2e_run\`」——
即 e2e_run 是被跟踪报告**引用的证据目录**，属过程证据，按 `REPORT-I §5` 归 archive-only。

### 2.4 tools/ — 诊断脚本（46 份，0.10 MB）

统一特征（实测）：

```text
命名惯例        : 全部以 `_` 前缀（临时/一次性语义）
绝对路径依赖    : 46 份中多数硬编码 D:\Project\{AITutor-X,AITutors-v3,Papers}\...
```

| # | 范围 | 建议 Class | 建议动作 |
|---|---|---|---|
| A10 | `tools/_*.py` 共 46 份 | Utility / Probe（Class C 过程产物） | **(b) ARCHIVE** 或 (c) EXCLUDE |

**依据**：`REPORT-I §5` 将「RS.MD、日志、`.pytest_work` 探针」列为「非治理资产 / 设计为不入库」。
这 46 份属同类一次性诊断工具，且大量携带绝对路径（§4 GAP-008 同类）。

> **本项建议保持独立、不与身份决定混装** —— 与 Owner 对 `W-5` 的既有判断一致。
> 但**不建议直接删除**：删除前需确认无人在用（本次未做使用情况核查）。

### 2.5 Docs/90_ARCHIVE/misc/ — 历史可行性文档（1 份）

| # | 文件 | 大小 | 建议动作 |
|---|---|---|---|
| A11 | `v0.3-contract-to-code-feasibility.html` | 30.0 KB | **(b) ARCHIVE**（原地，路径已在 `Docs/90_ARCHIVE/`） |

**依据**：已在 `90_ARCHIVE/` 之下，语义上已是归档；但 `.html` 非本仓治理文档惯例格式，建议仅登记不转格式。

### 2.6 review_pif1_evidence/ — PIF1 复核证据（15 份）

| # | 子范围 | 建议动作 |
|---|---|---|
| A12 | `probe_*.py`（3 份）、`pytest_full.txt` | **(b) ARCHIVE** |
| A13 | `tmp/**`（11 份） | **(c) EXCLUDE** — 已被 `.gitignore:48 tmp/` 覆盖，**无需动作** |

**安全复核结论（DSH 实测，先自证伪）：**

```text
命中 `sk-` 的文件 : review_pif1_evidence/tmp/probe_result.txt
实际内容          : 该仓自身的脱敏探针夹具（P2_bearer_sk: clean=True leaked=[]）
是否真实密钥      : 否 —— 是探针输入用的合成测试串
git 状态          : .gitignore:48 `tmp/` 已忽略，不会入库
```

⇒ **无凭证泄漏，不需要密钥轮换。**
另注：`A5`/`A6` 与 `e2e_run/diag_ir.py` 含 `postgresql+asyncpg://aitutors:change-me@...`，
该 `change-me` 是仓库既有**占位口令**（`runner_b2.py:28` 同款 `os.environ.setdefault`），非真实凭据。

---

## 3. AITutors-v3 未跟踪资产（14 份，0.15 MB）

### 3.1 Docs/COORDINATION/CONTRACTS/ — 契约与设计文档（9 份）

**这一组正是 `REPORT-I §1 F7` 与 `§2.3` 点名阻塞 Class E 迁移的对象。**

| # | 文件 | 大小 | 建议 Class | 建议动作 |
|---|---|---|---|---|
| B1 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-DESIGN-v1.1.md` | 23.9 KB | **Class E（authority unknown）** | **(a) COMMIT** — 高优先 |
| B2 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-DESIGN-v1.md` | 27.5 KB | Class E（被 v1.1 取代） | **(b) ARCHIVE** + legacy 标注 |
| B3 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-PLAN-v1.md` | 16.9 KB | Class E | **(a) COMMIT** |
| B4 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-READINESS-v1.md` | 8.8 KB | Class E | **(a) COMMIT** |
| B5 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-REPORT-PHASE1.md` | 3.7 KB | Class E | **(a) COMMIT** |
| B6 | `PREPROCESSING-V3-CONSUMER-IDENTITY-VERIFICATION-IMPLEMENTATION-REPORT-PHASE2.md` | 2.8 KB | Class E | **(a) COMMIT** |
| B7 | `PREPROCESSING-V3-CONTRACT-CONSUMER-REVIEW.md` | 15.6 KB | Class E（v0.2 REVIEW 前身） | **(b) ARCHIVE** |
| B8 | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT-SKELETON.md` | 13.2 KB | Class E（v0.2 DRAFT 前身） | **(b) ARCHIVE** |
| B9 | `PREPROCESSING-V3-CONTRACT.md` | 11.2 KB | Class E（v0.2 DRAFT 前身） | **(b) ARCHIVE** |

**B1 为何是最高优先项：**

`REPORT-I §1 F7` 原文：

> `F7 Design v1.1 authority 锚定 | untracked / authority unknown | 凡迁移物引用 Design v1.1 作为接口权威，必须先完成 Owner 处置`

而 `AITutor-X/Docs/GOVERNANCE/02-AUTHORITY-MATRIX.md:55` 独立记载：

> `…IDENTITY-VERIFICATION-DESIGN-v1.1.md | LOCAL | UNTRACKED | Unknown | Never in git. **Cited extensively by DSH Guardian DEC-035~049 as the source of D2/D3/D4 interface definitions.**`

⇒ 一份**定义了 D2/D3/D4 接口**的文档，从未入 git，却已被大量引用。
若工作树丢失，AITutor-X 内的审查引用将全部悬空。这是 `REPORT-I §5` 标注的 **HIGH 丢失风险** 的实例。

**B2/B7/B8/B9 建议 (b) ARCHIVE 而非 (a) COMMIT 的理由**：它们各自有**已跟踪的后继版本**
（B2→B1；B7→`PREPROCESSING-V3-CONTRACT-CONSUMER-REVIEW-v0.2.md` 已跟踪；B8/B9→`v0.2-DRAFT.md` 已跟踪 @ `f4941ff`）。
按 `AGENTS.md` 原则 1（Provenance ≠ Quality Authority），旧版不自动获得权威；但按 `REPORT-I §5` 不得静默丢弃，故保留为 archive-only。

### 3.2 Docs/GOVERNANCE/ — G0 四件套（4 份）

| # | 文件 | 大小 | 建议 Class | 建议动作 |
|---|---|---|---|---|
| B10 | `00-SYSTEM-BASELINE.md` | 9.3 KB | Class E | **(a) COMMIT 或 (b) ARCHIVE**（见下） |
| B11 | `02-AUTHORITY-MATRIX.md` | 8.6 KB | Class E | 同上 |
| B12 | `03-DECISION-REGISTRY.md` | 8.2 KB | Class E | 同上 |
| B13 | `04-CLAIM-REGISTRY.md` | 6.7 KB | Class E | 同上 |

**实测特征：**

```text
B11 头部：`Generated: 2026-09-17 (G0 Governance Reset)`  → 早于本轮全部工作
B11 自陈：把 9 份 CONTRACTS 文档标为 "Primary Governance Risk / Never in git"
          并已在 §F 列出 16 份 V3 DECISIONS、§G 列出 Producer INTEGRATION 文档
```

**处置分歧点（请 Owner 注意）**：`REPORT-I §5:163` 要求这些标为
`UNTRACKED SNAPSHOT / AUTHORITY UNKNOWN` 并仅 archive；
但 B11 的内容**本身是权威对账材料**，且其"未跟踪风险"记载现已被 `REPORT-I` 独立确认。
⇒ 我倾向 **(a) COMMIT**（作为 2026-09-17 时点快照，正文不改），但**此项应并入 §4 F3 Authority Taxonomy 裁决**：一旦 commit，其内的 L0–L5 标签即需按唯一体系重映射。

### 3.3 backend/provider_reality.json（1 份）

| # | 文件 | 大小 | 建议 Class | 建议动作 |
|---|---|---|---|---|
| B14 | `provider_reality.json` | 2.0 KB | 运行产物（含真实 ID） | **(c) EXCLUDE** |

**实测特征：**

```text
generated_at : 2026-09-26T05:04:40Z   ← 早于 Phase A（eecd60b），非本轮产物
内容         : 含真实 document_id / task_id / request_id
```

**依据**：`Runner` 运行产物，非身份决定证据；含真实 DB 标识符。
建议**删除或加入 .gitignore**，并在处置记录中登记其来源为 2026-09-26 的 runner 运行。
**不得**随 `git add -A` 进入 `eecd60b` 之后的任何提交。

---

## 4. 汇总：给 Owner 的裁决表

| 组 | 范围 | 份数 | 体积 | 我的建议 | 阻断关系 |
|---|---|---|---|---|---|
| **G1** | X `Docs/60_REPORTS/` 治理文档（A1–A8） | 8 | 0.21 MB | **(a) COMMIT** | 解 `F7`；`REPORT-I` 自身落库 |
| **G2** | X `PRIMARY-PATH-MINIMAL-LOOP-PROBE.py`（A9） | 1 | 7 KB | (b) ARCHIVE / (c) EXCLUDE | 已失效（scratch 不存在） |
| **G3** | X `e2e_run/` 非二进制（b） | ~28 | 0.67 MB | (b) ARCHIVE | 被 A5 引用 |
| **G4** | X `e2e_run/inputs/*.pdf`（c） | 2 | 0.53 MB | **(c) EXCLUDE** + .gitignore | 数据本体不入库 |
| **G5** | X `tools/_*.py`（A10） | 46 | 0.10 MB | (b) ARCHIVE / (c) EXCLUDE | 建议独立于本决定 |
| **G6** | X `Docs/90_ARCHIVE/misc/`（A11） | 1 | 30 KB | (b) ARCHIVE | 无 |
| **G7** | X `review_pif1_evidence/`（A12） | 4 | 12 KB | (b) ARCHIVE | `tmp/` 已 ignore |
| **G8** | V3 `CONTRACTS/` 契约设计（B1–B9） | 9 | 0.13 MB | **B1/B3–B6 (a) COMMIT；B2/B7–B9 (b) ARCHIVE** | 解 `F7`、通 Class E |
| **G9** | V3 `Docs/GOVERNANCE/` G0（B10–B13） | 4 | 30 KB | (a) COMMIT（建议并入 F3 裁决） | 关联 `F3` |
| **G10** | V3 `provider_reality.json`（B14） | 1 | 2 KB | **(c) EXCLUDE** | 含真实 ID |

**最小充分动作（我的建议）**：先只做 **G1 + G8(B1,B3–B6)** —— 共 13 份、0.28 MB。
理由：这 13 份同时关闭 `REPORT-I §1 F7`、消除 HIGH 丢失风险、并让 `REPORT-I` 自身入库（Phase B 入口）。
其余组（G2–G7、G9–G10）均为整理项，可独立后置。

---

## 5. 与既有治理状态的交叉核对（时效性提示）

本文件撰写时（2026-09-28）已确认的**过时风险**，供 Owner 裁决时参考，**本文件不做修改**：

| 出处 | 原文 | 现状 | 处置建议 |
|---|---|---|---|
| `REPORT-I §2.6` | OD-007 AITutorX git init | 已完成（`659db9b`），`REPORT-I` 自陈 STALE | 裁决时标 CLOSED (STALE) |
| `REPORT-I §2.6` | OD-003 表述 "UNKNOWN" | DEC-049 Brief 已交付 | 改述为 "Brief delivered / ruling pending" |
| `REPORT-I §1 F9` | test baseline 冲突（337+1 vs 338） | 未复核（本轮未动 Producer） | 保留 OPEN |
| `REPORT-I §3` | Consumer L2 决策 16 份"已 tracked" | ✅ 与实测一致 | 无需动作 |
| `AITutor-X/02-AUTHORITY-MATRIX.md §D` | 9 份 CONTRACTS 文档 "Never in git" | ✅ 实测仍成立（§3.1） | 由 G8 处置 |

> `REPORT-G/H/I/K` 撰写于 2026-09-17，其后 AITutor-X 历经
> `45cc7da` → `4be2ba4` → `b5f9f9e` → `e969fac` → `1c500ba` → `e2c039d` → `a1f6d50`。
> **建议 Owner 在裁决 G1 前，先决定是否需要对 G/H/I/K 做一次时效性勘误**（本文件 §5 仅覆盖我已实测的部分，非完整核对）。

---

## 6. 本文件未做的事（明确边界）

```text
未修改任何未跟踪文件          ✅
未创建 / 未重编号 DEC/BUG/OQ   ✅
未执行任何迁移 / 未进入 active tree ✅
未删除任何文件                ✅
未代 Owner 做任何裁决         ✅
未对 G/H/I/K 做完整时效性核对  ⚠️ 仅 §5 覆盖实测部分
未核查 tools/ 46 份的使用情况  ⚠️ 删除前须补
未复核 Producer（Papers）仓库  ⚠️ 本文件范围外
```

---

## 7. 建议的下一步（顺序不可颠倒）

```text
1. Owner 对 §4 表逐组裁决 (a)/(b)/(c)
2. 若含 COMMIT 组 → 由 MIMO CODE 执行 commit（需单独授权；建议逐组独立提交以便回溯）
3. commit 后更新 REPORT-I §1 F7 状态 → Class E 解锁
4. 随后才进入 REPORT-I §2.1 的 4 项 P0（Migration Authority / Gate 批准 / Taxonomy / Set B）
```

*Prepared 2026-09-28 by DSH（治理收口角色）。Status: OPEN — 待 Owner 裁决。*
