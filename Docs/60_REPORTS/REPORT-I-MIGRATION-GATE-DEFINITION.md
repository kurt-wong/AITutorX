# Report I — Migration Gate Definition

**日期**: 2026-09-17
**性质**: 迁移闸门定义（gate definition，非迁移授权）
**上游**: REPORT-G（对账矩阵）、REPORT-H（权威冲突登记册）、REPORT-D（候选资产与 10 步 Gate 草案）、REPORT-E（Owner 决策队列）
**纪律**: 本文不授权迁移、不创建 DEC/BUG ID、不修改源仓。任何资产在 Gate 满足前进入 AITutorX active tree 均视为违规（AGENTS.md 原则 5）。
**Temporal Scope**: This report reflects repository state as of 2026-09-17. Subsequent commits have not been re-audited. Findings are as-of that date and are retained as historical audit artifacts; they are not current-state authority.

---

## 0. Gate 总原则

1. **Migration Gate ≠ Implementation Authority**
   通过 Gate 只表示“允许把某资产以指定身份放入 AITutorX 治理树”，不表示允许修改 Contract、不表示允许继续开发、不表示 Owner 已裁 D2/D3/D4。

2. **Provenance ≠ Quality Authority**（AGENTS.md）
   来自 V3 或 Papers 的文件不自动获得 AITutorX 权威层级。

3. **Git presence ≠ Authority**
   tracked 文件可迁移候选；untracked 文件默认不可进入 active tree，除非 Owner 完成 authority 处置。

4. **UNKNOWN is retained data**
   迁移记录必须保留 UNKNOWN / 冲突 / known-issue，禁止静默丢弃。

5. **禁止整仓 copy**
   `backend/`、`preprocessing/`、`frontend/` 不得作为目录整体拷贝；只能按资产逐项过 Gate。

6. **双仓源纪律**
   - Consumer 源：`D:\Project\AITutors-v3` @ 迁移时点 commit
   - Producer 源：`D:\Project\Papers` @ 迁移时点 commit
   - 每次迁移记录必须写明 source repo + source commit + source path + sha256（适用时）

7. **停止线**
   在 Cluster A（REPORT-H）未由 Owner 关闭前，**默认全面禁止迁移**。例外仅限：Owner 书面批准的“证据副本”（只读、不进 active tree、不参与构建）。

---

## 1. Required frozen items（迁移前必须已冻结/已锚定）

| # | Frozen item | 当前状态 | 迁移前要求 |
|---|-------------|----------|------------|
| F1 | **Contract v0.2 Freeze Object** | 已冻结：`f4941ff` + `9c6b9063…7528` | 迁移副本必须逐字节一致；记录双点 sha256；禁止改写正文头部状态语句 |
| F2 | **Freeze 状态叙事规则** | 未在治理仓成文 | Owner 确认“账本=状态权威 / 冻结对象=内容权威”（或替代规则）后，方可将 Contract 标为 active frozen asset |
| F3 | **AITutorX Authority Taxonomy** | 三套层级并存 | Owner 指定唯一层级体系；否则任何迁移文档的 L* 标签无效 |
| F4 | **Migration Authority Charter** | 未设立 | 必须先有：授权人/角色、Gate 执行者、批准记录格式、存放路径 |
| F5 | **Migration Gate 本文（或 Owner 修订版）** | 本 REPORT-I 为草案 | Owner 批准后方可作为 Gate 依据；批准前 REPORT-D 10 步仅为草案 |
| F6 | **Canonical namespace policy（DEC/BUG/OQ）** | 未解决 | 决策/缺陷/OQ 类文档迁移前必须有映射政策（至少：legacy 保留 + 引用格式） |
| F7 | **Design v1.1 authority 锚定** | untracked / authority unknown | 凡迁移物引用 Design v1.1 作为接口权威，必须先完成 Owner 处置 |
| F8 | **Data authority mode（OD-009）** | 未决 | preprocessing 数据/IR/manifest 资产迁移或引用前必须明确模式 |
| F9 | **Canonical test baseline** | 冲突（337+1failed vs 338 passed） | 宣称“迁移后测试等价”前必须固化受控重跑基线；r67 必须显式登记 |
| F10 | **Observation Set B** | 未导入 | Owner 提供 Set B，或书面豁免“本轮仅以 Set A + 仓库现实对账” |

---

## 2. Required owner decisions（迁移前 Owner 必须裁决）

按阻塞范围排序。编号沿用 REPORT-E 的 OD-*（**不新建 ID**）；REPORT-H 冲突簇用 Cluster 字母引用。

### 2.1 P0 — 阻塞一切迁移（Cluster A）

| 决策 | 对应 | 为何阻塞 |
|------|------|----------|
| 设立 Migration Authority 与批准记录机制 | REPORT-H Migration authority | 无授权人则 Gate 9 不存在 |
| 批准 Migration Gate 版本（本文或修订） | F5 / REPORT-D | 无 Gate 则无合格判据 |
| 指定唯一 Authority Taxonomy | F3 | 否则资产层级标签自相矛盾 |
| Set B 提供或豁免 | F10 | 决定对账是否完整、报告是否可引用 |

### 2.2 P0 — 阻塞 Class E 与设计引用（Cluster B）

| 决策 | 对应 | 为何阻塞 |
|------|------|----------|
| Design v1.1：commit / 降级 / working ref / v1.2 令 | OD-002；REPORT-H Design authority | D2/D3/D4 与 M1–M5 迁移身份依赖此项 |
| 其余 untracked CONTRACTS 文档 + G0 docs 处置 | OD-001、OD-008 | 无处置则 Class E 不可迁，且丢失风险仍在 |
| D2 / D3 / D4 裁决（按 DEC-049 Brief 逐项） | OD-003 | 接口权威未定则 identity 实现资产无法定性 |
| Contract 状态叙事规则 | REPORT-H Contract（状态叙事） | 否则 AITutorX 内会出现“同一 Contract 两种状态” |

### 2.3 P1 — 阻塞命名空间相关文档迁移（Cluster C）

| 决策 | 对应 | 为何阻塞 |
|------|------|----------|
| DEC canonical：采纳 / 重做 / 仅 disambiguation 前缀 | OD-004；REPORT-C 与 G0 冲突 | 否则 `Docs/40_DECISIONS/` 无法安全填充 |
| 指定 mapping authority 载体 | REPORT-H mapping authority | 禁止多表并行且互斥 |
| BUG / OQ 命名规则 | REPORT-H BUG/OQ | bugs 迁移与跨仓引用完整性 |
| SEMANTIC_STATUS `unknown` 实现与否 | OD-005 | 影响 UNKNOWN 资产在迁移后的行为标注 |

### 2.4 P1 — 阻塞数据与 preprocessing 资产（Cluster D）

| 决策 | 对应 | 为何阻塞 |
|------|------|----------|
| 数据权威模式（path-ref / NAS / copy / 其他） | OD-009；GAP-007 | 无模式则 `preprocessing/` 与数据字典不可迁 |
| scripts / ocr_service 是否纳入本轮范围 | REPORT-D Class B | 决定适配工作量与 Gate 6 范围 |
| 绝对路径与 path≠identity 的迁移适配策略 | GAP-008；Contract path 条款 | 否则迁入代码会固化违规路径身份假设 |

### 2.5 P2 — 阻塞“可验证迁移”声明（Cluster E）

| 决策 | 对应 | 为何阻塞 |
|------|------|----------|
| r67：迁移前修复 / known-issue 挂账 / expected failure | OD-006；GAP-006 | 影响 Producer 测试资产的 Gate 3 |
| 受控环境重跑两仓测试并固化 baseline | REPORT-H test baseline | 迁移前后等价性证明 |
| frontend 是否在范围 | OD-010 | 决定 backend-only 还是全栈 Gate |

### 2.6 已过时或状态已变（仍需 Owner 确认关闭）

| 原决策 | 现实 | 建议 Owner 动作（不代执行） |
|--------|------|------------------------------|
| OD-007 AITutorX git init | 已完成（`659db9b`） | 在正式 Owner Queue 中标记 CLOSED（STALE） |
| OD-003 的“UNKNOWN”表述 | DEC-049 Brief 已交付，裁决仍暂停 | 更新队列表述为 “Brief delivered / ruling pending” |

---

## 3. Automatically migratable assets（在 Cluster A 关闭后可自动过 Gate 的资产）

**前提**：F1–F5 已满足（至少 Migration Authority + Taxonomy + Gate 已批）。
“自动”指：无需再等 D2/D3/D4 或数据模式裁决，但仍须完成 Gate 1–10 记录。

| Asset class | 具体资产（已核实存在） | 目标位置（建议） | Gate 备注 |
|-------------|------------------------|------------------|-----------|
| Frozen Contract 副本 | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` @ `f4941ff` | `Docs/30_CONTRACTS/` | 字节级复制 + sha256 双点记录；不改正文 |
| L0 Frozen Spec（V3） | `Docs/V3_SPEC/00` `10` `20` `30` `40` `50` `90` `91` `README` | `Docs/10_SPEC/` | TRACKED；复制时保留 V3 内权威标注 + AITutorX taxonomy 重映射 |
| 已 tracked 的 Consumer 协调账本镜像 | `Docs/COORDINATION/state.yaml`、`CURRENT.md`、`log.md`、`COMPLETION_PROTOCOL.md` | `Docs/50_OPERATIONS/` 或 archive | 标注 mirror/canonical；不覆盖 Papers canonical 叙事 |
| Producer governance 三件套 | `governance/rule_registry.md`、`risk_register.md`、`phase_p2_charter.md` | `Docs/00_GOVERNANCE/` 或附录 | TRACKED；层级按 F3 重标注 |
| Consumer L2 决策记录（已 tracked） | `Docs/DECISIONS/` 16 份（已入库者） | `Docs/40_DECISIONS/` | **仅在 F6 namespace policy 批准后**自动迁；迁时加 legacy 标注 |
| Review protocol / 完成协议 | Papers `review_protocol.md`；V3 `COMPLETION_PROTOCOL.md` | `Docs/00_GOVERNANCE/` | 无跨仓 ID 冲突 |
| 历史证据目录（只读） | Papers `Docs/COORDINATION/EVIDENCE/`（7）、V3 EVIDENCE（2） | `Docs/90_ARCHIVE/EVIDENCE/` | 只读归档；不作为现行权威 |
| 测试套件（代码文件本身） | V3 `backend/tests/**`；Papers `tests/**` | 对应 backend/preprocessing tests | **代码文件**可自动迁；**测试结论/基线**须 F9 |

**明确不在“自动”集合**：

- M1–M5 及 runner（见 §4：需处理 authority pending 身份）
- 任何 untracked 文档
- 任何数据/IR/manifest 本体
- REPORT-B 中无法在仓库定位的“伪文件名”
- frontend
- Papers `scripts/` / `ocr_service/` / `attacks/`

---

## 4. Assets requiring transformation（必须转换/适配后才能迁）

| Asset | 源 | 必须的 transformation | Gate 重点 |
|-------|----|----------------------|-----------|
| DEC/BUG/OQ 引用密集文档 | 两仓 CURRENT/log/bugs/INTEGRATION | 增加 dual-ID 栏或引用注解；**不重写历史 ID** | Gate 5 dup + Gate 8 class |
| M1–M5 + `runner_b2.py` + gate/compile 相关 | V3 backend | 保留代码字节可追溯副本；**同时**附 “authority pending（D2/D3/D4）” 标签与 hash 锚 | Gate 3 validity + Gate 9 |
| SEMANTIC_STATUS / UNKNOWN 相关文档与代码说明 | V3 | 文档必须同时写：已裁词表 `{ready,incomplete,unknown}` vs 代码现状 `{ready,incomplete}` | 禁止只迁一侧表述 |
| Producer `scripts/**`（约 77） | Papers | 路径抽象（去 `D:\Project\Papers\...` 绝对依赖）、import/工作目录适配、代码分类标签 | Gate 6 arch compat |
| `ocr_service/**`（6 tracked + 运行配置） | Papers | Docker/路径/环境变量文档化；符合 project-rules（Dockerfile + compose 示例 + env 说明） | Gate 6 + 安全审查 |
| `attacks/**` | Papers | 测试框架适配；与 tests/ 双 conftest 冲突（DSH S-1）必须在文档中登记 | Gate 6 |
| `docs_audit/authority_matrix.yaml` 等 | V3 | 与 AITutorX F3 taxonomy 合并/映射，不得直接当作 AITutorX 权威矩阵 | Gate 5 |
| REPORT-B / REPORT-C 中的错误映射 | AITutorX REPORTS | **不修改已提交报告**；新建勘误/对账（即本 G/H/I）并在迁移记录中引用 | 证据纪律 |
| 双账本叙事（canonical vs mirror） | Papers/V3 | 转换为 AITutorX 账本策略（待 Owner：保留 Producer canonical / 迁入 / 双写） | Gate 9 |
| 数据字典 / 接口键说明 | Contract + Papers 工件清单 | 双名域并列表述；hash 清单优先于数据本体 | F8 + Gate 7 |

---

## 5. Assets requiring archival only（只归档，不进 active tree）

| Asset | 源 | 归档理由 | 目标（建议） |
|-------|----|----------|--------------|
| HANDOFFS 全集 | V3 + Papers `Docs/COORDINATION/HANDOFFS/` | 历史跨 Agent 通信，Class C | `Docs/90_ARCHIVE/HANDOFFS/` |
| Guardian / 历史轮次 INTEGRATION 报告 | Papers `INTEGRATION/`（约 32） | 过程证据，非现行规格；部分结论已被更新轮取代 | `Docs/90_ARCHIVE/INTEGRATION/` |
| Producer `reports/**` 历史报告 | Papers | Class C | `Docs/90_ARCHIVE/PRODUCER_REPORTS/` |
| DSH 自审与 Decision Brief | `…DSH-SELF-ADVERSARIAL-AUDIT-v1.md`、`…D2-D3-D4-DECISION-BRIEF-v1.md` 等 | **高价值证据，但不是 Owner 裁决**；归档 + 在 Owner Queue 中引用 | `Docs/90_ARCHIVE/DSH/` |
| untracked 文档在 Owner 处置前的**快照副本** | V3 working tree | 防丢失（REPORT-D 风险表 HIGH）；副本必须标 `UNTRACKED SNAPSHOT / AUTHORITY UNKNOWN` | `Docs/90_ARCHIVE/UNTRACKED_SNAPSHOT/` |
| V3 G0 四文件快照 | `Docs/GOVERNANCE/` untracked | 同上；commit 前不得当作现行权威 | 同上 |
| RS.MD、日志、`.pytest_work` 探针 | Papers | 非治理资产 / 设计为不入库 | 不迁或 archive-only |
| 空目录 `D:\Project\AITutors-X` | 磁盘 | 路径混淆风险 | Owner 令后再处理（本轮不动） |
| 生产数据本体 `Ocr-markdown/` 等 | Papers | 不入 git；默认 **archive/external reference only**，不进 AITutorX tree | 依 F8 决策 |
| frontend（若 Owner 裁延后） | V3 `frontend/` | 范围外则 archive note only | `Docs/90_ARCHIVE/SCOPE_NOTES/` |

---

## 6. Migration Gate 检查表（10 步，执行时逐资产填写）

沿用 REPORT-D 草案并补证据字段。**任一步 FAIL = 不得迁入 active tree。**

| Step | 检查项 | 必填证据 | FAIL 处理 |
|------|--------|----------|-----------|
| 1 | Source identified | source repo + commit + path | 停止 |
| 2 | Authority identified | F3 层级 + 依据文件 | 停止或降为 archive-only |
| 3 | Current validity verified | 与冻结对象/账本一致性；测试或 hash | known-issue 须 Owner 确认 |
| 4 | Historical status classified | active / superseded / historical / unknown | unknown → Class E |
| 5 | Duplicate check | 与 AITutorX 现有树及对侧 repo 比对 | 冲突 → Owner |
| 6 | Architecture compatibility | 路径、依赖、Docker、硬件约束（i7/64GB/4060 8GB） | 需 transformation 则改 Class B |
| 7 | Evidence attached | sha256、测试输出、对账报告引用（G/H/I） | 缺证据 → 停止 |
| 8 | Migration class assigned | A / B / C / D / E（REPORT-B 定义） | Class E 不得进 active tree |
| 9 | Governance approval | Migration Authority 签字/记录（格式由 F4 定） | **当前不可满足** |
| 10 | Migration record created | 记录：时间、资产、class、source commit、目标 path、approver | 迁入后补全 |

### 6.1 建议的 Migration Record 最小字段（合成示例）

```text
migration_id: <由 Migration Authority 分配，本任务不创建>
asset: Docs/30_CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
class: A
source_repo: kurt-wong/AITutors-v3
source_commit: f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1
source_path: Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md
sha256: 9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528
authority_level: <per F3 taxonomy>
authority_basis: Owner freeze order + ledger registration (status narrative rule per F2)
gate_status: 1-8 PASS / 9 PENDING / 10 N/A
approver: <Migration Authority>
approved_at: YYYY-MM-DD
notes: freeze object content not modified; status wording remains DRAFT in artifact body
```

日期格式：`YYYY-MM-DD`。哈希：64 位小写 hex。Commit：40 位 hex。

---

## 7. 迁移顺序建议（仅在 Gate 可满足后）

与 REPORT-D §5 一致，并加入权威前置：

1. **Governance 先行**：Taxonomy + Migration Authority + Gate 批准记录 + namespace policy
2. **Frozen Contract 副本** + 状态叙事规则文档
3. **L0 SPEC（V3_SPEC）**
4. **Owner 已处置的 untracked 文档**（若批准 commit/copy）
5. **Decision / protocol / governance 文件**（带 dual-ID）
6. **Tests（代码）**，随后才谈 baseline 对比
7. **Identity 实现代码（M1–M5…）** — 仅当 Owner 明确“authority pending 也可迁”或 D2/D3/D4 已裁
8. **Producer scripts / ocr_service**（Class B 适配）
9. **数据字典 / hash 清单**（依 F8）
10. **frontend / 其他范围外项** — 仅当 OD-010 打开

---

## 8. 当前可执行性结论

| 问题 | 答案 |
|------|------|
| 现在可以开始迁移吗？ | **不可以。** Cluster A 全未关闭；Gate 9 无授权人。 |
| 现在可以做“证据快照”吗？ | 仅当 Owner 书面允许；且必须 archive-only、标 AUTHORITY UNKNOWN。 |
| REPORT-D 的 Class A 清单可直接执行吗？ | **不可以。** 其中部分资产名不存在；真实可迁集合以 REPORT-G 仓库现实为准。 |
| Design 相关资产怎么办？ | 等 OD-002 + OD-003；在此之前任何“按 Design 冻结签名迁移”都不成立。 |
| 数据资产怎么办？ | 等 OD-009 / F8；治理仓优先登记 hash 与路径别名，不先复制数据本体。 |
| 本报告是否构成迁移授权？ | **否。** 这是 gate definition。授权只能来自 Owner + Migration Authority 记录。 |

---

## 9. Stop Condition（任务书）

REPORT-G / H / I 已产出。

**STOP。**

- 不迁移
- 不实现
- 不清理
- 不创建 DEC / BUG ID
- 不修改 V3 / preprocessing / 既有 REPORT-A~F
- **等待 Owner 审阅**
