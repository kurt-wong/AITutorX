# Report G — Governance Reconciliation Matrix

**日期**: 2026-09-17
**角色**: Implementation Governance Analyst（对账，非迁移）
**方法**: 三仓 git 直接验证 + REPORT-A~F 交叉核对 + V3/Producer 工作树与关键实现定点复查
**Observation Set A**: Claude Stage-1（`Docs/60_REPORTS/REPORT-A` ~ `REPORT-F`）
**Observation Set B**: DSH Independent Audit — **未以独立审计包形式导入 AITutorX**
**本轮未执行**: 迁移 / 编码 / 修改 V3 / 修改 Producer / 创建 DEC ID / 创建 BUG ID / 修改 Contract / 裁决 Owner 决策
**Temporal Scope**: This report reflects repository state as of 2026-09-17. Subsequent commits have not been re-audited. Findings are as-of that date and are retained as historical audit artifacts; they are not current-state authority.

---

## 0. 路径与命名核对（本轮前置发现）

任务书中的两条本地路径与磁盘实际状态不一致。本报告一律以 **git 实测路径** 为准。

| 角色 | 任务书路径 | 磁盘实际路径 | GitHub Remote | 结论 |
|------|------------|--------------|---------------|------|
| Governance | `D:\Project\AITutorX` | **`D:\Project\AITutor-X`** | `kurt-wong/AITutorX` | 本地目录名含连字符；GitHub 名无连字符 |
| Consumer | `D:\Project\AITutors-v3` | `D:\Project\AITutors-v3` | `kurt-wong/AITutors-v3` | 一致 |
| Producer | `D:\Project\Aitutors-preprocessing` | **`D:\Project\Papers`** | `kurt-wong/Aitutors-preprocessing` | 本地目录名 ≠ 仓库名 |

附加风险：

- `D:\Project\AITutors-X` 存在，但为 **空目录、无 `.git`**，易与 `AITutor-X` 混淆。
- AITutorX `README.md` 已正确登记 Producer 本地路径为 `D:\Project\Papers`。
- V3 `Docs/GOVERNANCE/00-SYSTEM-BASELINE.md`（untracked）同样登记 `D:\Project\Papers`。

**Status**: 路径不一致 = 事实；治理文档中的路径书写须统一，但本轮不改既有报告。

---

## 1. Repository Reality

三仓均于 2026-09-17 以 `git rev-parse` / `git status` / `git remote -v` / `git log -1` / `git ls-files` 直接验证。

| 字段 | Governance `AITutor-X` | Consumer `AITutors-v3` | Producer `Papers` |
|------|------------------------|------------------------|-------------------|
| Local path | `D:\Project\AITutor-X` | `D:\Project\AITutors-v3` | `D:\Project\Papers` |
| Remote URL | `https://github.com/kurt-wong/AITutorX.git` | `https://github.com/kurt-wong/AITutors-v3.git` | `https://github.com/kurt-wong/Aitutors-preprocessing.git` |
| Branch | `main` | `main` | `main` |
| HEAD | `659db9b47e82123d8698ff6b9ab9615adf0f59ad` | `cc12d79e9a22f6274100ea0bb61f92493ba88509` | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` |
| origin/main | 与 HEAD 一致（本地 `refs/remotes/origin/main` 存在） | `cc12d79…`（HEAD == origin/main） | `2b92898…`（HEAD == origin/main） |
| Working tree | **CLEAN** | 无 modified/deleted；存在 **untracked** | **CLEAN**，untracked = 0 |
| Tracked files | 22（骨架 + REPORT-A~F + README + AGENTS + .gitignore） | **457** | **419** |
| Untracked | 0 | **10 paths**：9 个 CONTRACTS 文档 + `Docs/GOVERNANCE/`（4 文件） | 0 |
| Tags | 无 | `v3-phase-i2-closed` | 无 |
| Latest commit | `chore: establish AITutorX governance workspace` | `feat: Phase 2.5 Consumer Data Activation & Interface Closure` | `DEC-049: D2/D3/D4 Decision Brief (Evidence First, No Self-Fix)` |
| Commit time | 2026-09-17 22:53:59 +0800 | 2026-09-17 13:17:37 +0800 | 2026-09-17 20:16:20 +0800 |
| Commit count | 1（initial） | 206 | 160 |
| Python files | 0 | backend 存在（本表不展开） | 122 |
| 生产代码是否已迁入 | **否**（仅 `.gitkeep`） | 实现仍在 V3 | 实现仍在 Papers |

### 1.1 测试状态（本轮实测）

| 仓库 | 本轮动作 | 结果 | 与 REPORT-A 对照 |
|------|----------|------|------------------|
| V3 | `pytest --collect-only -q`（backend） | **1782 tests collected** | REPORT-A 称基线 `1780 passed, 1 skipped, 1 xfailed`（2026-09-16）。收集数与“1780+1+1”量级一致；**本轮未重跑 V3 全量** |
| Papers | `python -m pytest -q`（canonical，testpaths=tests） | **1 failed, 337 passed, 1 xfailed** | **与 REPORT-A 完全一致** |
| Papers | 定点 `tests/test_r67_bootstrap.py::test_r67_t13_real_corpus_smoke` | **FAIL**：`assert 768 == 0`，`AUDIT_FROM_UNMATCHED` ×768 | 与 REPORT-A / REPORT-F GAP-006 / OD-006 一致，**问题仍在** |

说明：Producer canonical 全量与定点复跑均确认 r67 失败仍为 pre-existing。DSH 自审材料中出现过 `338 passed / 1 xfailed` 表述，与本轮 `337 passed + 1 failed + 1 xfailed` 不一致；本报告以本轮实测为准，将该差异登记为 Observation Set 间冲突（见 §2）。

### 1.2 冻结对象与 Identity 模块（本轮定点）

| 对象 | 本轮验证 | 结果 |
|------|----------|------|
| Contract freeze commit | `git cat-file -t f4941ff` | commit 存在 |
| 亲缘 | `git merge-base --is-ancestor f4941ff origin/main` | **TRUE** |
| SHA256 @ `f4941ff` | `git show f4941ff:…CONTRACT-v0.2-DRAFT.md \| sha256sum` | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |
| SHA256 @ working tree | 同路径文件 | **同一哈希** |
| 字节数（账本登记） | 92,197 B | 与 Producer CURRENT.md / DEC-049 登记一致 |
| M1 `manifest_identity.py` | sha256 | `1ca33a45a101de8c…` **MATCH REPORT-A** |
| M2 `raw_bytes_identity.py` | sha256 | `803c4ed8a93f59b5…` **MATCH** |
| M3 `ir_identity.py` | sha256 | `f960b513a935c8ca…` **MATCH** |
| M4 `identity_verifier.py` | sha256 | `1306105c6c3d2b8b…` **MATCH** |
| M5 `identity_gate.py` | sha256 | `8a5d267e285800f0…` **MATCH** |
| `SEMANTIC_STATUS` | `backend/app/domains/compile/__init__.py:29` | `frozenset({"ready", "incomplete"})` — **无 `unknown`** |
| `identity_version` | V3 `backend/app/core/` + `backend/app/domains/` | **0 命中** |
| non-ready skip | `runner_b2.py` ~L322-329 | `semantic_status != "ready"` → skip + `reason=not_ready` |
| Design v1.1 | untracked；本轮 sha256 | `f9e3f4fa12df9a20…`，23,900 B；**仍不在 git 追踪集** |
| V3 untracked 文档 | `git log --all -- <path>` | CONTRACTS 下 9 件 **仍无 git 历史** |
| `Docs/GOVERNANCE/` | V3 working tree | 4 文件存在且 **untracked** |

---

## 2. Audit Claim Comparison

Status 取值：`VERIFIED` / `STALE` / `PARTIALLY VERIFIED` / `UNVERIFIED` / `OWNER DECISION REQUIRED`

### 2.1 仓库与基线类主张

| Claim | Claude Report | Repository Evidence | Status |
|-------|---------------|---------------------|--------|
| V3 HEAD = `cc12d79`，与 origin/main 同步 | REPORT-A §1.1 | 本轮 `git rev-parse` 双侧一致 | **VERIFIED** |
| V3 tracked ≈ 457 | REPORT-A §1.1 | `git ls-files \| wc -l` = 457 | **VERIFIED** |
| V3 untracked = 9 docs + governance dir | REPORT-A §4 / REPORT-B §4 | `git status` = 10 paths，构成一致 | **VERIFIED** |
| V3 测试基线 1780 passed（2026-09-16） | REPORT-A §1.1 | 本轮仅 collect=1782；未重跑全量；DSH DEC-048 亦称 1780 passed | **PARTIALLY VERIFIED** |
| Producer HEAD = `2b92898`，与 remote 同步 | REPORT-A §1.2 | 本轮实测仍为 `2b92898`，HEAD==origin/main | **VERIFIED** |
| Producer tracked=419 / py=122 / commits=160 / untracked=0 | REPORT-A §1.2 | 本轮逐项一致 | **VERIFIED** |
| Producer 测试 1 failed / 337 passed / 1 xfailed | REPORT-A §1.2 | 本轮全量重跑完全一致 | **VERIFIED** |
| r67_t13 失败 = 768 AUDIT_FROM_UNMATCHED | REPORT-A / REPORT-F GAP-006 / REPORT-E OD-006 | 本轮定点复跑 `assert 768 == 0` 复现 | **VERIFIED** |
| DSH/Producer canonical = 338 passed / 1 xfailed（无 failed） | DSH DEC-045 自审（Papers） | 本轮 canonical = 337 passed + **1 failed** + 1 xfailed | **STALE / CONFLICTING** |
| 两 repo 均无 local drift | REPORT-A §7 | 本轮 V3/Papers 均 HEAD==origin/main；AITutor-X 亦 clean | **VERIFIED** |
| AITutorX 尚未 git init | REPORT-E OD-007 | 已存在 git 仓库，HEAD `659db9b`，remote 已配置 | **STALE** |

### 2.2 Contract / 冻结类主张

| Claim | Claude Report | Repository Evidence | Status |
|-------|---------------|---------------------|--------|
| Freeze Object = `f4941ff` + Contract v0.2 DRAFT | REPORT-A §2 / REPORT-B #1 | commit 存在；路径 tracked；内容可导出 | **VERIFIED** |
| SHA256 双点一致 `9c6b9063…7528` | REPORT-A §2 | 本轮 `f4941ff` 与 working tree 双点一致 | **VERIFIED** |
| `f4941ff` 是 origin/main 祖先 | REPORT-A §2 | `merge-base --is-ancestor` = TRUE | **VERIFIED** |
| Contract 状态 = FROZEN（Owner DEC-036） | REPORT-A 隐含 / V3 CURRENT.md | V3/Papers 账本均写 FROZEN；**Contract 正文自述仍为 DRAFT/READY FOR FREEZE/NOT FROZEN**（冻结对象禁止改写所致） | **PARTIALLY VERIFIED** |
| Contract 是跨系统最高冻结权威 | REPORT-B L1 | 双仓账本 + 哈希锚支持；但 Python 签名层零规定（DSH DEC-049 grep 证据） | **PARTIALLY VERIFIED** |
| REPORT-B L1 #2 `…INTEGRATION-SPEC-v0.1.md` tracked | REPORT-B §1 | V3/Papers **均无此文件名**（tracked 或 on disk） | **UNVERIFIED** |
| REPORT-B L1 #3–#6 INTERFACE/OWNER FINALIZATION 系列文件 tracked | REPORT-B §1 | 六个声称文件名在两仓 **全部 0 命中**；相关决策内容实际存在于 Papers `INTEGRATION/` 下**不同文件名**中 | **UNVERIFIED** |
| REPORT-B L1 #7 `…OWNER-B1-B2-B3-DECISION-ALIGNMENT-v1.md` | REPORT-B §1 | 两仓 0 命中；裁决原文在 `PREPROCESSING-OWNER-DECISION-RECORD-v1.md` | **UNVERIFIED** |

### 2.3 Identity / 实现缺口类主张

| Claim | Claude Report | Repository Evidence | Status |
|-------|---------------|---------------------|--------|
| M1–M5 已 commit 于 V3，哈希前缀如 REPORT-A | REPORT-A §3 / REPORT-B #8–12 | 五文件均 tracked，sha256 逐项 MATCH | **VERIFIED** |
| D2：identity gate 的 `identity_version` 无实现 | REPORT-F GAP-001 | 本轮 grep 0 命中 | **VERIFIED** |
| D3：SEMANTIC_STATUS 无 `unknown` | REPORT-F GAP-002 / OD-005 | `compile/__init__.py:29` 仍为 `{ready, incomplete}` | **VERIFIED** |
| D4：Execution ordering 未实现 | REPORT-F GAP-003 | 无新增实现证据；DSH DEC-049 将 D4 还原为 M5 接口面 + Design 文本 + OQ-21 张力 | **PARTIALLY VERIFIED** |
| non-ready 静默 skip 违反 UNKNOWN retained 原则 | REPORT-F GAP-004 / AGENTS.md 原则2 | `runner_b2.py` 仍 skip 并记 `not_ready` | **VERIFIED** |
| Design v1.1 被 D2/D3/D4 引用为权威 | REPORT-E OD-002 / REPORT-F GAP-009 | DSH DEC-049 明确引用其 §4.3/§4.4/§4.7；同时证明其 untracked 且“冻结”为 V3 自述 | **VERIFIED（引用事实） / OWNER DECISION REQUIRED（权威是否成立）** |
| 9 untracked 文档无 git traceability | REPORT-A §4 / REPORT-D Class E | `git log --all` 仍全空 | **VERIFIED** |
| Contract 对 M1–M5 Python 签名有规定 | REPORT-B 将 Design/Contract 混作迁移权威的隐含前提 | DSH DEC-049：`SourceBytes\|raw_bytes\|bytes_source` 在 Contract 中 grep **0 命中** | **UNVERIFIED（该隐含前提不成立）** |

### 2.4 命名空间类主张

| Claim | Claude Report | Repository Evidence | Status |
|-------|---------------|---------------------|--------|
| DEC-012~036 存在跨仓撞号 | REPORT-C §1 / REPORT-F GAP-010 | 双仓 CURRENT.md + V3 G0 Decision Registry 均确认；且 G0 另发现 DEC-031~036 未文档化撞号 | **VERIFIED** |
| REPORT-C V3 DEC-021 主题 = FINALIZATION v1 (B1-B4) | REPORT-C §2.1 | V3 `CURRENT.md`：DEC-021 = **B2 Identity** | **STALE / 错误映射** |
| REPORT-C V3 DEC-023 主题 = FINALIZATION four decisions | REPORT-C §2.1 | V3 `CURRENT.md`：DEC-023 = **Interface Scope = 87** | **STALE / 错误映射** |
| REPORT-C Producer DEC-021 = CONTRACT-DECISION-FINALIZATION | REPORT-C §2.2 | G0/Papers：DSH DEC-021 ≈ Interface Decision Finalization（≡ V3 DEC-027）；与 REPORT-C 标签不完全同构 | **PARTIALLY VERIFIED** |
| Canonical `AIT-DEC-*` 映射可消除冲突 | REPORT-C §5 | 该映射 **仅存在于 REPORT-C**；V3/Papers 账本均未采用 AIT-DEC 前缀 | **UNVERIFIED（未落地）** |
| BUG：V3 = BUG-V3-001~050；Producer 映射 AIT-BUG-101+ | REPORT-C §4 | V3 `bugs.md` 确有 BUG-V3-…（去重计数 50）；Papers `bugs.md` 使用 **BUG-01…BUG-33** 族，**未使用 AIT-BUG-*** | **PARTIALLY VERIFIED** |
| OQ：V3 有 OQ-1~21，Producer 无独立 OQ | REPORT-C §3 | Papers 账本/契约讨论中同样使用 OQ-xx；“Producer 无独立 OQ”过于绝对 | **PARTIALLY VERIFIED** |

### 2.5 迁移候选与 Owner 队列类主张

| Claim | Claude Report | Repository Evidence | Status |
|-------|---------------|---------------------|--------|
| Class A 资产 Gate 1–8 已过、仅差 Gate 9 | REPORT-D §1 | 对**真实存在且 tracked** 的资产（Contract、M1–M5、V3_SPEC、tests、governance 三文件等）大体成立；对 REPORT-B 伪文件名不成立 | **PARTIALLY VERIFIED** |
| Class B scripts/ocr_service 需适配 | REPORT-D §2 | Papers `scripts/`（77 项）、`ocr_service/`（6 tracked）存在；含绝对路径风险（GAP-008） | **VERIFIED（存在） / OWNER DECISION REQUIRED（是否迁）** |
| Producer 数据不在 git，baseline 无法独立重建 | REPORT-F GAP-007 / OD-009 | `.gitignore` 含 `/Ocr-markdown/` 等；`Ocr-markdown/*` tracked=0；manifest/IR 证据工件在 `data/` 部分 tracked | **VERIFIED** |
| 数据侧 `source_content_sha256` 回填 87/87 | REPORT-A 隐含 / 契约 §9 / Papers CURRENT | Papers 存在 step1 snapshot、step2 backfill report、freeze_evidence 等工件；账本称 87/87 | **PARTIALLY VERIFIED（工件存在；本轮未重算 87 份字节）** |
| G0 governance docs 需处置 | REPORT-E OD-008 | V3 `Docs/GOVERNANCE/` 4 文件仍 untracked | **VERIFIED** |
| D2/D3/D4 状态 UNKNOWN / NOT STARTED | REPORT-E OD-003 / REPORT-F | 状态已推进：DSH **DEC-049 Decision Brief 已交付**（2026-09-17），三项争议已还原，**裁决仍暂停，等 Owner** | **STALE（描述过时） / OWNER DECISION REQUIRED（实质未决）** |
| REPORT-A~F 结论可直接作为迁移权威 | 任务书前提 | 报告内多处文件名/主题映射与仓库不符；DSH Observation Set B 未导入 | **OWNER DECISION REQUIRED** |
| DSH 独立审计（Set B）已可用于对账 | 任务书前提 | AITutorX 无 Set B 导入物；Papers 仅有 DSH **自审**（DEC-045）与 Guardian/DEC-049 系列，**不是与 REPORT-A~F 同构的独立治理审计包** | **UNVERIFIED** |

### 2.6 Claude vs DSH 关键冲突摘要

| 冲突点 | Claude 侧 | DSH 侧（Papers 内材料） | 仓库证据倾向 |
|--------|-----------|-------------------------|--------------|
| Producer 测试基线 | 337 passed + 1 failed + 1 xfailed | DEC-045：338 passed / 1 xfailed（无 failed 表述） | **支持 Claude 侧数字**（本轮复跑） |
| Design v1.1 权威 | 报告称其为 D2/D3/D4 权威来源 | DEC-049：权威不成立，属 V3 自述冻结 + untracked | **支持 DSH 对权威层级的分析**；引用事实双方一致 |
| Contract 是否规定实现签名 | REPORT-B 将多份“Finalization”文档列为 L1 frozen | DEC-049：Contract 对 Python 签名零规定 | **支持 DSH**；且 REPORT-B 伪文件名无法在仓库落地 |
| DEC 撞号范围 | REPORT-C 给出 AIT-DEC 全表 | G0（V3 untracked）指出 REPORT-C 主题映射有误，并补充 DEC-031~036 撞号 | **两套映射均未被账本采用**；冲突存在，canonical 未定 |
| M1–M5 哈希 | REPORT-A 五模块前缀 | DEC-048/049 同前缀 MATCH | **双方一致 = VERIFIED** |
| 冻结对象四元组 | `f4941ff` + `9c6b9063…7528` | 同四元组，92,197 B | **双方一致 = VERIFIED** |

---

## 3. Authority Analysis

### 3.1 Contract v0.2 — Is authority clear?

**结论：Freeze Object 权威清晰；Freeze 叙事与实现层权威不完全清晰。**

| 维度 | 现状 | 证据 |
|------|------|------|
| 冻结对象身份 | **清晰** | repo=`AITutors-v3` / commit=`f4941ff` / document=`PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` / sha256=`9c6b9063…7528` |
| Owner 冻结令 | **账本层清晰** | V3 `CURRENT.md` DEC-036；Papers 侧冻结收口 DEC-027~032 链 |
| 文档自述状态 | **与账本不一致** | 正文头部仍写 `DRAFT / READY FOR FREEZE / NOT FROZEN`（因冻结对象禁止改写） |
| 冻结范围 | **相对清晰** | 六项（§0.1）；其余暂缓 |
| 对实现的约束力 | **部分清晰** | 冻结的是能力/行为，不是 Python 签名；“Contract Freeze ≠ Implementation”双账本均强调 |
| 冻结编号权威 | **分裂** | 同一冻结事件在 V3/Producer 使用不同 DEC 号段 |

**回答**：若问题指“哪一份字节是 Owner 冻结的 Contract”——**清晰且可复算**。
若问题指“读者能否仅凭 Contract 文档判断当前是否 FROZEN、以及实现接口以何为准”——**不清晰**，必须叠加账本 + Owner 令 + 未决 Design 权威。

### 3.2 Design v1.1 — Current status?

**结论：不是 frozen specification；不是已批准的 implementation authority；处于 pending owner approval / unanchored design 状态。**

| 判据 | 事实 |
|------|------|
| Git 状态 | **UNTRACKED**，从未进入 git history |
| 自述 | `IMPLEMENTATION READY DESIGN / NOT IMPLEMENTED / WAITING OWNER IMPLEMENTATION AUTHORIZATION` |
| §4.7 | 自称签名/异常/状态码“已冻结”，且“任何修改须 Owner 另行下令” |
| 与 Owner 冻结令关系 | Owner 冻结令（DEC-036）指向 Contract v0.2，**未**指向 Design v1.1 |
| 被谁引用 | DSH Guardian DEC-035~049、DEC-049 Decision Brief、V3 G0 docs |
| 与实现关系 | 实现（`cc12d79`）与 Design §4.3/§4.4/§4.6 存在多处接口面偏离（D2/D3/D4） |
| Claude 报告定性 | REPORT-B/E/F 多处将其当作 D2/D3/D4 权威 —— **该定性超出仓库证据** |

**可选状态归类（供 Owner，不代裁）**：

1. **Pending owner approval** — 未来可能被 anchoring 为正式层级；
2. **Implementation working document（无治理权威）** — 仅作历史设计参考；
3. **Superseded / 待 v1.2** — 由 Owner 令改写以追认或否定现行实现。

在 Owner 明确处置前，任何迁移或实现若声称“依据 Design v1.1 冻结签名”，均属 **authority 未锚定**。

### 3.3 DEC namespace — Are collisions resolved?

**结论：未解决。**

| 项 | 现状 |
|----|------|
| 撞号是否存在 | **是**（至少 DEC-021/022/023 + DEC-031~036） |
| 双仓是否仍双轨编号 | **是**（V3 DEC-001~036；Producer/DSH DEC-012~049） |
| 账本是否采用 AIT-DEC | **否** |
| REPORT-C 映射质量 | V3 侧 DEC-021/023 等主题与 `CURRENT.md` **不符** |
| V3 G0 Decision Registry | 补充了未文档化撞号，但自身 **untracked** |
| Owner/系统是否已裁统一编号 | **否**；DEC-031 延期清单明确将“DEC 编号统一”列为非架构阻塞的延期项 |

碰撞**已被观察和记录**，但**canonical namespace 尚未建立、未被两仓账本采纳、且候选映射本身存在错误**。

### 3.4 BUG namespace — Are collisions resolved?

**结论：未解决；且“已解决”的证据不足。**

| 侧 | 实际编号形态 | 证据 |
|----|--------------|------|
| V3 | `BUG-V3-001` … `BUG-V3-050`（`bugs.md` 去重 50） | `rg` 实测 |
| Producer | `BUG-01` … `BUG-33` 族 + `BUG-14-DATA` / `BUG-14-CHAIN` 等变体 | `bugs.md` 实测 |
| REPORT-C 提案 | Producer → `AIT-BUG-101+` | **两仓均未使用** |

风险不在“同号同名冲突爆炸”，而在：

1. 跨仓引用时 `BUG-14` 与 `BUG-V3-014` 可能被误读为同一问题；
2. Producer 侧存在同号语义拆分（BUG-14-DATA vs BUG-14-CHAIN）；
3. AIT-BUG 映射停留在报告层。

### 3.5 Migration authority — Who authorizes migration?

**结论：当前没有已生效的、写入治理仓的 Migration Authority。**

| 来源 | 关于迁移授权说了什么 | 状态 |
|------|----------------------|------|
| AITutorX `AGENTS.md` | “未经 Migration Gate 不得进入 active tree”；禁止两仓直接 copy | 有原则，**无授权人/程序** |
| AITutorX `README.md` | “由 V3 与 Producer 经治理验证后合并”；Stage 1 audit 进行中 | 描述性，非授权 |
| REPORT-D | Gate 9 = Governance approval | 未指明谁行使 Gate 9 |
| REPORT-E | Owner Decision Queue（OD-001~010） | 暗示 Owner 为裁决者，**无正式 charter** |
| Contract v0.2 / DEC-036 | 冻结 ≠ 实现授权；实现须另获 Owner 令 | 对 **实现** 明确；对 **迁入 AITutorX** 未明确 |
| `Docs/00_GOVERNANCE/` | 仅 `.gitkeep` | **空** |

因此：

- **事实上的等待对象** = Owner；
- **正式 Migration Authority** = **尚未设立**（无 charter、无 Gate 执行角色、无批准记录格式）；
- 在 Authority 设立前启动迁移，将违反本仓 `AGENTS.md` 原则 5。

### 3.6 补充：Data authority

| 项 | 现状 |
|----|------|
| 生产数据物理位置 | Papers 工作树（`Ocr-markdown/`、`data/` 大量内容不入 git） |
| 冻结基线叙事 | Papers 账本：Producer Baseline FINALIZED + ARCHIVED（DEC-033/034） |
| 可从 git 独立重建？ | **否**（REPORT-F GAP-007；本轮 `.gitignore` 证实） |
| 路径身份问题 | 契约禁 path-as-identity；但双层现有关联与脚本仍含 `D:\Project\Papers\...` 绝对路径 |
| AITutorX 中的数据引用机制 | **未定义**（OD-009 仍开放） |

数据权威目前停留在 **Producer 仓 + 本地工件 + Owner 延期决策**，治理仓无数据权威载体。

### 3.7 Authority Analysis 汇总

| Authority 对象 | 是否清晰 | 阻塞迁移？ |
|----------------|----------|------------|
| Contract freeze object 字节 | 清晰 | 否 |
| Contract 状态叙事 / 实现接口层 | 不完全清晰 | 是（接口层） |
| Design v1.1 | 不清晰（unanchored） | 是（若迁移依赖其签名） |
| DEC namespace | 不清晰（未解决） | 是（决策文档迁移前） |
| BUG namespace | 不清晰（未解决） | 中（引用完整性） |
| Migration Authority | **未设立** | **是（总闸门）** |
| Data Authority | 不清晰 | 是（数据/预处理资产） |

---

## 4. 本轮对账结论（非裁决）

1. **仓库现实**：三仓均可定位、均 clean（V3 仅治理/契约文档 untracked）；Producer 本地路径是 `D:\Project\Papers`，不是任务书中的 `Aitutors-preprocessing`。
2. **Claude Stage-1 中可独立复算的核心事实**（HEAD、冻结哈希、M1–M5 哈希、untracked 集合、r67 失败、SEMANTIC_STATUS、identity_version 零命中）**大多 VERIFIED**。
3. **Claude Stage-1 中的结构性弱点**：REPORT-B 多个 L1 “tracked” 文件在仓库中不存在；REPORT-C V3 侧 DEC 主题映射与账本冲突；AIT-DEC/AIT-BUG 未落地；OD-007 已过时。
4. **DSH Observation Set B**：**未作为独立审计包导入**；Papers 内 DSH 材料是生产/监护/决策简报，不能自动等同于 Set B。完整“三方对照”目前只能做到 **Claude vs 仓库现实**，外加 **DSH 关键主张抽查**。
5. **迁移总闸门**：Migration Authority 未设立；Design/namespace/data 权威未决。
   → **STOP：不迁移、不实现、不清理，等待 Owner 审阅 REPORT-G/H/I。**

---

## 5. 证据索引（本轮直接使用的可复核锚）

| 锚 | 值 |
|----|-----|
| AITutor-X HEAD | `659db9b47e82123d8698ff6b9ab9615adf0f59ad` |
| V3 HEAD / origin/main | `cc12d79e9a22f6274100ea0bb61f92493ba88509` |
| Papers HEAD / origin/main | `2b92898f05f6541a5fc65c8300cb8a59a06c4928` |
| Contract sha256 | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |
| Design v1.1 sha256（本地 untracked） | `f9e3f4fa12df9a2017a2c83abc591e60d71d3e1a2ef8d1d2c503bca54bc44a54` |
| Producer canonical pytest（本轮） | 1 failed / 337 passed / 1 xfailed |
| r67 失败计数 | 768 `AUDIT_FROM_UNMATCHED` |
| V3 test collect（本轮） | 1782 |
| SEMANTIC_STATUS | `compile/__init__.py:29` = `{ready, incomplete}` |
| 关键 DSH 材料 | Papers `Docs/COORDINATION/INTEGRATION/PREPROCESSING-D2-D3-D4-DECISION-BRIEF-v1.md`、`…DSH-SELF-ADVERSARIAL-AUDIT-v1.md`、`…OWNER-DECISION-RECORD-v1.md` |
