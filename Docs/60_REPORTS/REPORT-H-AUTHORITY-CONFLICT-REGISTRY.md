# Report H — Authority Conflict Registry

**日期**: 2026-09-17
**性质**: 权威冲突登记册（只登记，不裁决）
**上游**: REPORT-G（仓库现实与主张对账）
**纪律**: 不创建 DEC ID / BUG ID；不修改 Contract / Design / 既有报告；不代 Owner 选择 A/B
**Temporal Scope**: This report reflects repository state as of 2026-09-17. Subsequent commits have not been re-audited. Findings are as-of that date and are retained as historical audit artifacts; they are not current-state authority.

---

## 1. Registry

| Object | Current State | Evidence | Required Owner Decision |
|--------|---------------|----------|-------------------------|
| **Contract authority（冻结对象字节）** | Freeze Object 唯一且可复算：`AITutors-v3@f4941ff` + `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` + sha256 `9c6b9063…7528`（92,197 B）。双仓账本均指向同一四元组。 | REPORT-G §1.2；`git show f4941ff:<path> \| sha256sum` 双点一致；`f4941ff` is-ancestor of origin/main = TRUE；Papers/V3 CURRENT.md | 是否确认该四元组继续作为 AITutorX 唯一 Contract Freeze Object？迁入 `Docs/30_CONTRACTS/` 时是否要求附带 Owner Freeze 令摘录与 sha256 校验记录？ |
| **Contract authority（状态叙事）** | 账本写 `FROZEN`（V3 DEC-036）；Contract 正文头部仍写 `DRAFT / READY FOR FREEZE / NOT FROZEN`。读者仅读正文会得到相反状态。 | V3 `CURRENT.md` 状态头；Contract v0.2 DRAFT 文首；冻结对象禁改导致正文无法追记 | 是否接受“**账本 = 状态权威，冻结对象 = 内容权威**”的双文件规则并写入 AITutorX Governance？若否，状态权威以何载体登记？ |
| **Contract authority（实现接口层）** | Contract 冻结能力/行为，但对 M1–M5 **Python 级签名零规定**（grep 0 命中）。REPORT-B 曾暗示存在多份 L1 Finalization/Spec tracked 文档，**仓库中不存在这些文件名**。 | DSH DEC-049 §D2.4/D3.4；REPORT-G §2.2；两仓文件名检索 0 命中 | 是否确认“Contract 不冻结函数名/字段名/异常类名”？若确认，实现接口权威应落在何处（Design v1.x / 代码即事实 / 新 L3 文档）？ |
| **Design authority（Design v1.1）** | untracked、无 git 历史；自述 `IMPLEMENTATION READY DESIGN` + §4.7 自称签名已冻结；被 DSH Guardian/DEC-049 引用为 D2/D3/D4 争议来源；与 `cc12d79` 实现存在多处偏离。 | `git log --all` 空；sha256 `f9e3f4fa…`；DESIGN-v1.1 §0/§4.7；DEC-049；V3 G0 Authority Matrix（untracked）亦标 Unknown | **必须裁决**：(A) commit + 赋予正式 authority level；(B) 标记无权威、D2/D3/D4 按 Contract/行为重裁；(C) 仅作 working reference；(D) 令出 Design v1.2 追认或否定现行实现。并明确 D2/D3/D4 是否以该裁决为前置。 |
| **Design authority（Design v1 / 其他 untracked 文档）** | 与 v1.1 同目录另有 DESIGN-v1、IMPLEMENTATION-PLAN/READINESS/REPORT-PHASE1/2、CONTRACT 早期版、SKELETON、CONSUMER-REVIEW 等，全部 untracked、authority UNKNOWN。 | REPORT-A §4；V3 `git status`；G0 docs | 逐项或批量处置：commit 到 V3 / 复制入 AITutorX 并标注层级 / 确认 historical / 组合。不处置则 Class E 迁移不可启动。 |
| **Decision namespace ownership（DEC）** | 双轨编号仍活跃：V3 DEC-001~036；Producer/DSH DEC-012~049。已知撞号含 DEC-021/022/023 及 DEC-031~036。REPORT-C 提出的 `AIT-DEC-*` **未被任一账本采用**，且 REPORT-C V3 侧 DEC-021/023 等主题与 `CURRENT.md` 不符。 | REPORT-C；REPORT-G §2.4；V3/Papers `CURRENT.md`；V3 G0 `03-DECISION-REGISTRY.md`（untracked） | 是否采纳统一 canonical namespace？若采纳：以 REPORT-C、G0 Registry 或新 Owner 令中的哪一份为基准？历史 ID 是否只映射不重写？在裁决前，AITutorX `Docs/40_DECISIONS/` 是否禁止新增无前缀 `DEC-*`？ |
| **Decision namespace ownership（映射表权威）** | 至少三套并存：REPORT-C AIT-DEC 表；V3 G0 Decision Registry；双仓 CURRENT.md 双向标注惯例。三者主题标签不完全一致。 | 同上 | 指定**唯一 mapping authority** 载体与维护者；未指定前，任何迁移文档不得单方面引用 REPORT-C 表为最终映射。 |
| **Bug namespace ownership（BUG）** | V3 使用 `BUG-V3-###`（约 50 条）；Producer 使用 `BUG-##` 族及 `BUG-14-DATA/CHAIN` 拆分；REPORT-C 提案 `AIT-BUG-*` 未落地。 | 两仓 `bugs.md` 实测；REPORT-C §4 | 是否建立跨仓 BUG 命名规则？Producer 同号拆分如何在 AITutorX 表示？迁移 bugs.md 时是否强制双栏（legacy ID + canonical ID）？ |
| **Open Question namespace（OQ）** | REPORT-C 称 Producer 无独立 OQ；实际 Papers 账本/契约讨论中大量使用 OQ-xx（OQ-10/12/13/15/16/21 等），与 V3 OQ 段可能同号异义。 | REPORT-C §3；Papers CURRENT.md / Contract §0.2 / DEC-049 | 是否将 OQ 纳入与 DEC 相同的 canonical 化流程？ |
| **Migration authority** | AITutorX `AGENTS.md` 禁止无 Gate 迁移；REPORT-D Gate 9 = “Governance approval”但未指明授权人；`Docs/00_GOVERNANCE/` 为空；无 Migration Charter。Contract/DEC-036 只区分了“冻结 ≠ 实现授权”，**未**指定 AITutorX 迁移授权者。 | REPORT-G §3.5；AGENTS.md；README.md；空目录 `Docs/00_GOVERNANCE/` | **必须设立**：Migration Authority 是谁（Owner 本人 / 指定 Agent / 双人复核）？Gate 执行者与批准者是否分离？批准记录格式与存放路径？未设立前是否全面禁止迁移？ |
| **Migration gate completeness** | REPORT-D 列 10 步 Gate，但 Gate 证据模板、重复检查基线、架构兼容判定标准均未成文入 AITutorX。 | REPORT-D；AITutorX 现有文件清单 | 是否批准 REPORT-D 的 10 步 Gate 为正式 Gate？需要补充哪些必填证据字段？ |
| **Data authority（生产数据与冻结基线）** | 数据主体在 Papers 本地（`Ocr-markdown/` 等不入 git）；账本称 Producer Baseline FINALIZED+ARCHIVED；无法仅从 git 重建；绝对路径依赖 `D:\Project\Papers\...`；AITutorX 无数据引用机制。 | `.gitignore`；`Ocr-markdown/*` tracked=0；GAP-007/008；OD-009 | 数据权威模式：Producer path-reference / NAS 共享 / 复制入 AITutorX / 其他？冻结数据工件清单以何为准？AITutorX 是否只登记 hash 清单而不持有数据本体？ |
| **Data authority（接口身份键两侧表达）** | 跨系统键已裁为 `source_content_sha256`；Producer IR 字段仍为 `source_sha256`（同值异名，契约允许双名域）；manifest 回填叙事为 87/87；V3 消费能力争议 D2/D3/D4 未裁。 | Contract §0.1①/§1.2/§1.2a；Papers CURRENT 关键数字；REPORT-G §2.3 | 是否确认双名域分离长期有效？AITutorX 数据字典采用哪一侧命名？迁移数据文档时是否强制同时标注两域名？ |
| **Ledger authority（协调账本）** | Papers `state.yaml` 自称 canonical；V3 `CURRENT.md` 自称 mirror，Last Updated=2026-09-16，落后于 Papers 2026-09-17（DEC-049）。AITutorX 尚无协调账本。 | Papers `state.yaml` 头注释；V3/Papers `CURRENT.md` | AITutorX 建立后：canonical ledger 仍留 Producer、迁入 AITutorX、还是双写过渡？mirror 滞后是否允许？ |
| **Governance doc authority（G0 in V3）** | V3 `Docs/GOVERNANCE/` 4 文件内容较 REPORT-A~F 更新（含 DEC-031~036 撞号、Design 权威质疑），但 **untracked**，无 git 权威。 | V3 working tree；`git status`；REPORT-G §2.4 | 是否 commit 到 V3、复制到 AITutorX `Docs/00_GOVERNANCE/`、或两者都做？在 commit 前其结论能否作为迁移依据？ |
| **Authority taxonomy（层级定义）** | 至少三套：AITutorX README（L0=Owner/System Decision … L7=Working Notes）；V3 `90_DOCUMENT_GOVERNANCE`（L0=Frozen Spec，L0-META，L1=Contract Change Record…）；REPORT-B 另用 L1–L7 且与前两者不完全同构。 | AITutorX README.md；V3 `Docs/V3_SPEC/90_DOCUMENT_GOVERNANCE.md`；`docs_audit/authority_matrix.yaml`；REPORT-B | **AITutorX 采用哪一套层级为唯一标准**？历史文档中的 L* 标签如何重映射？是否禁止新文档混用未声明的层级体系？ |
| **Observation Set B authority（DSH 独立审计）** | 任务书称 Set B 由 Owner 另行提供；AITutorX 未导入。Papers 内 DSH 材料（DEC-045 自审、Guardian 系列、DEC-049 Brief）是相关证据但**不是**与 REPORT-A~F 同构的独立治理审计包。 | REPORT-G §2.5–2.6；Papers `INTEGRATION/` 目录 | Set B 是否存在、以何路径/commit 提供？若不存在，是否将 Papers 内 DSH 系列指定为“受限 Set B”并限定用途？对账报告是否必须补做 Set B 导入后的二次对照？ |
| **Path / repo naming authority** | 本地路径 `AITutor-X` vs GitHub `AITutorX`；Producer 本地 `Papers` vs remote `Aitutors-preprocessing`；另有空目录 `AITutors-X`。任务书路径与磁盘不一致。 | REPORT-G §0；目录实测 | 是否公布**官方路径别名表**并写入 AITutorX README/GOVERNANCE？空目录 `AITutors-X` 是否删除或改名（需 Owner 令，本轮不处理）？ |
| **Test baseline authority** | Claude REPORT-A：Producer 337+1failed+1xfail（本轮复现）；DSH DEC-045：338 passed/1 xfailed。V3：REPORT-A/DSH 称 1780 passed，本轮仅 collect=1782 未全量重跑。 | REPORT-G §1.1 | 以哪次运行为 canonical test baseline？AITutorX 迁移前是否要求两仓在受控环境重跑并固化报告？r67 失败是否列为 known-issue 且不得静默忽略？ |
| **Implementation authority（M1–M5 现行代码）** | 代码已 tracked 于 V3，哈希稳定且与 DSH 锚一致；但接口面权威（Design vs 实现）未决，D2/D3/D4 OPEN；行为面 fail-closed 被 DSH 多轮描述为符合 Contract 能力条款。 | REPORT-G §1.2/§2.3；DEC-047/048/049 | 在 D2/D3/D4 裁决前，AITutorX 是否允许将 M1–M5 以“现状实现（authority pending）”身份迁移，还是必须等接口权威收口？ |
| **UNKNOWN semantic authority（词表 vs 代码）** | 契约/AGENTS 词表含 `ready/incomplete/unknown` + `pending_review/approved/rejected`；V3 代码 `SEMANTIC_STATUS={ready,incomplete}`；runner 对 non-ready 走 skip。UNKNOWN retained 原则与现行执行面冲突。 | Contract §0.3；AGENTS.md；`compile/__init__.py:29`；`runner_b2.py` skip 路径 | 是否令解冻 `SEMANTIC_STATUS` 增加 `unknown`？unknown→reviewable→pending_review 的执行面归属 V3 哪一层？在实现前，治理文档如何表述“已裁词表 ≠ 代码现状”？ |
| **Agent / tool authority（谁可写治理仓）** | AITutorX AGENTS.md 有禁止行为列表，但无 “who may approve writes / who may create IDs” 条款。本任务被限制为仅新建对账文档。 | AGENTS.md；任务书 Hard Restrictions | 治理仓写权限与 ID 创建权（DEC/BUG/OD/REPORT）归属谁？Claude/DSH 是否允许在 Owner 令后创建 canonical ID？ |
| **Owner decision queue authority（OD-*）** | REPORT-E 定义 OD-001~010；OD-007（git init）已过时完成；OD-003 已被 DSH DEC-049 推进到“Brief 已交付待裁”；其余多数字面仍开放。OD-* 未在任一源仓账本中作为正式 ID 系统运行。 | REPORT-E；REPORT-G §2.5；Papers CURRENT.md DEC-049 | OD-* 是否升格为 AITutorX 正式 Owner Decision Queue？与 DSH Owner Decision Record（ODR）关系为何（并存 / 吸收 / 映射）？ |

---

## 2. 冲突簇（便于 Owner 按簇处理）

### Cluster A — 迁移总闸门（阻塞一切 Class A/B 迁移）

1. Migration Authority 未设立
2. Migration Gate 未正式批准
3. Authority taxonomy 未统一
4. Observation Set B 未导入或未豁免

### Cluster B — 文档权威锚定（阻塞 Class E 与 Design 相关引用）

1. Design v1.1 authority
2. 其余 untracked CONTRACTS 文档 + G0 docs
3. Contract 状态叙事规则（账本 vs 正文）
4. REPORT-B 伪文件名 / REPORT-C 错误映射如何在 AITutorX 更正（新建报告 vs 不改旧报告仅登记）

### Cluster C — 命名空间（阻塞决策/缺陷文档迁移与引用完整性）

1. DEC canonical 化
2. BUG canonical 化
3. OQ 是否纳入
4. Mapping authority 指定

### Cluster D — 数据与接口（阻塞 preprocessing 资产与数据字典迁移）

1. Data authority 模式（OD-009）
2. 双名域 `source_content_sha256` / `source_sha256` 在治理层的表述
3. 绝对路径与 path≠identity 的迁移适配策略
4. 冻结数据工件清单是否入 AITutorX（只登记 hash）

### Cluster E — 运行基线（阻塞“迁移后可验证”声明）

1. Canonical test baseline（含 r67 known failure）
2. M1–M5 在 D2/D3/D4 未决时的迁移身份
3. SEMANTIC_STATUS 词表与代码不一致的治理表述

---

## 3. 明确不在本登记册内裁决的事项

以下均 **保持 OPEN**，等待 Owner：

- D2 / D3 / D4 的 A/B（或混合）选择（材料见 Papers `PREPROCESSING-D2-D3-D4-DECISION-BRIEF-v1.md`）
- Design v1.1 的最终 authority level
- 是否迁移 frontend
- Producer r67 是迁移前修复还是 known-issue 挂账
- 数据是否复制入 AITutorX
- REPORT-A~F 是否需要正式勘误流程（本任务按 Hard Restrictions **未修改**既有报告）

---

## 4. 停止条件

本登记册完成即触发任务书 Stop Condition：

**不迁移 · 不实现 · 不清理 · 不创建新 ID · 等待 Owner 审阅 REPORT-G / REPORT-H / REPORT-I。**
