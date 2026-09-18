# X2-03 — Concept / Terminology Map

**Document ID**: X2-03
**Task**: TASK-X2-CLAUDE
**Document Type**: Specification / Terminology
**Status**: `ACTIVE — X2 UNIFIED TERMS`
**Date**: 2026-09-18
**Upstream**: V3 `DICTIONARY.md`；V3 `91_PROJECT_TERMINOLOGY.md`；Contract v0.2；GF-001/002；preprocessing `prd.md`；AGENTS.md
**Rule**: 统一术语表用于 AITutorX 叙事；**不修改** Frozen Spec/Contract 原文；历史文档不强制改写（Reconcile, don't rewrite）

---

## 1. How to use this map

1. AITutorX 新治理文档优先使用本表 **Canonical** 词。
2. 引用源仓文档时保留源词面，并在本表 **Source aliases** 标注。
3. 同名异义必须双栏标注；禁止静默合并。
4. 本表不产生业务事实；业务权威仍在 GF / Contract / V3_SPEC。

---

## 2. Lifecycle & Identity Terms

| Canonical | Meaning in AITutorX | Source aliases / notes | Must not |
|-----------|---------------------|------------------------|----------|
| **Source** | 进入系统的原始考试文档事实层 | V3 Source；Producer 原始 PDF/DOCX | 不等于某目录名 |
| **Source Version** | 一次 sealed 的不可变解析/内容版本 | V3 `document_source_versions` | ≠ 文件 path |
| **Source Identity** | 由内容决定的身份 | Contract: `source_content_sha256` | ≠ storage location |
| **source_content_sha256** | SHA256(original source bytes)，64 小写 hex；**唯一跨系统身份键** | DEC-030/031 终局命名 | 禁止用 path 替代 |
| **source_version_id** | **V3 内部** UUID FK | Contract §1.2a 专用化 | ≠ 跨系统 sha |
| **source_sha256** | Producer IR/OCR 历史字段名；语义常 = raw bytes sha | Papers IR schema | 引用时标注域名 |
| **source_file / path** | Locator | Contract 冻结项 ④ | 不参与 identity 判断 |
| **Manifest** | Producer 产出的 Document Evidence Manifest；**Source Identity Authority** | prd `*.manifest.json` | ≠ 最终 Question |
| **OCR Artifact (OCRA)** | OCR 产出 md/图片等 | GF-001 role | 覆盖可能不全 |
| **Raw Source Document (RSD)** | 最初接收的原件字节 | GF-001 | ≠ 目录 `original/` 证明 |
| **Processing Input Snapshot (PIS)** | 某次执行实际消费的文件+hash 集合 | GF-001 | 当前操作观测≠历史字节全知 |
| **Seal** | 校验后置 sealed，禁止 UPDATE | V3 DICTIONARY | sealed 后不得改 |

---

## 3. Semantic Pipeline Terms

| Canonical | Meaning | Source aliases | Must not |
|-----------|---------|----------------|----------|
| **Semantic Annotation** | LLM 对 Source 的语义 claim（结构/题型/依赖等） | V3 20 §4；≠ Producer OCR 批注 | 不携带 resolved span/正文/canonical type（V3 规则） |
| **Semantic Reference** | LLM 受控位置引用 | V3 20 §4.4 | 不是 line number |
| **Resolver** | 把 Semantic Reference 解析为 Resolved Span | V3 domains/resolver | 不猜 |
| **Resolved Span** | line/character/table_cell/fragment 级范围 | V3 DICTIONARY | — |
| **IR (cross-system)** | Producer Semantic Evidence / resolver IR artifact；Semantic Consumption Authority | Papers `resolver_ir`；Contract | IR ≠ Interface；IR ≠ Question |
| **Semantic Question IR (V3)** | Resolver 后 Compiler 前的 transient 中间表示 | V3 20 §6 | M1 不另建中间表 |
| **Compiler** | Deterministic Compiler | V3 20 §7 | 不生成新语义 |
| **Gate** | Structural/Provenance/Semantic/Admission 判定 | V3 20 §8 | LLM 不拥有此权 |
| **Admission** | 唯一物化 Question 的事务 | V3 10 §5.4 | 禁绕过 Candidate |
| **Candidate** | Gate 判定后的冻结边界对象 | V3 10 | ≠ live Question |
| **Evidence (Producer)** | Document Evidence Manifest 中的结构事实 | prd 1.2 | ≠ Quality Authority |
| **Evidence (V3/EB-008)** | Admission 证据与 Authority 记录 | DEC 75–92 | 与 Producer Evidence 不同层 |

---

## 4. Domain Object Terms

| Canonical | Meaning | Source aliases | Notes |
|-----------|---------|----------------|-------|
| **Question** | Admission 后 canonical domain entity | V3 10 §6.1 | Source-derived；可重放 |
| **QuestionInstance** | Question 在某 Source 中的一次 occurrence | V3 10 §6.2；DICTIONARY | 与 Question 身份分离 |
| **Material** | 题目依赖的外部材料：**文字 + 题图 + 配图 + 图表 + 图片等** | V3 materials；prd material role | **不是纯文字**；single question 也可有 Material |
| **source_figure** | Source 域图片索引实体 | V3 10 §4.4 | `figure_id` 确定性；`figure_hash=SHA256(raw bytes)` |
| **Knowledge / Knowledge Tree** | 知识点节点与树；AI 只映射不随意创建 | DICTIONARY | 映射审核 `approved/pending/rejected` |
| **unit (Producer)** | 切分单元 `standalone_question` / `composite_question` | prd §2.2 | `unit_id` = display alias，**禁止作跨系统键** |
| **composite_question** | 共享材料的原子单元 | prd | 整块一道题，不拆子题入库 |
| **standalone_question** | 无共享材料独立题 | prd | 可含自身 Material/figures |
| **extra (Producer role)** | 配图排版漂移时的卫星锚 | prd §2.3 | 不撑大 unit 包络 |
| **content_hash** | V3 规范化文本 hash（去重用） | DICTIONARY | ≠ source_content_sha256 |

---

## 5. Status & Classification Terms（分层，禁止互替）

### 5.1 Semantic status
`ready` | `incomplete` | `unknown`

### 5.2 Decision status
`pending_review` | `approved` | `rejected`

### 5.3 Citation state（GF / X2）
| State | Meaning |
|-------|---------|
| exists | 磁盘可读 |
| tracked | 在 git 跟踪面 |
| referenced | 被治理文档引用 |
| admitted | 经 Registry + Owner/Charter 处置后准入（**当前无**） |

### 5.4 Migration classification（X2 文档/资产）
`MIGRATE` | `MERGE` | `SUPERSEDE` | `ARCHIVE` | `REJECT` | `RETAIN-AS-HISTORICAL` | `UNKNOWN`

### 5.5 GF OQ status
`OPEN` | `OPEN-BLOCKING` | `MAPPED` | `STALE-CANDIDATE`
（**零 CLOSED** @ X2 时点）

### 5.6 Authority domains（OD-03 第一层）
`GOV` Governance | `EVD` Evidence | `EXT` External Capability

### 5.7 Artifact roles（OD-03 第二层）
`RSD` | `PIS` | `OCRA` | `SEM` | `MIG`
**禁止与 Authority Domain 互相替代。**

### 5.8 Evidence labels（治理文档）
`[FACT]` | `[OBSERVED]` | `[INFERENCE]` | `[PROPOSAL]` | `[OWNER DECISION]` | `[OWNER DECISION REQUIRED]` | `[DECISION REQUIRED]` | `[UNKNOWN]` | `[CONFLICT]`

---

## 6. Identity & Numbering Namespaces（映射，不重编号）

| Namespace | Domain | Example | Rule |
|-----------|--------|---------|------|
| **OD-\*** | AITutorX GF Owner Decisions | OD-01, OD-04, OD-14 | 正典 = GF-006 |
| **OQ-GF-\*** | AITutorX Open Questions | OQ-GF-001…018 | 前缀防撞；不替代源仓 OQ |
| **BL-\*** | AITutorX Blocking list | BL-09/10/11 | OPEN |
| **V3 DEC-\*** | AITutors-v3 decisions | DEC-021…036 | 与 DSH 撞号须双标 |
| **DSH/Papers DEC-\*** | preprocessing ledger decisions | DEC-021…049 | canonical ledger in Papers |
| **Papers OQ-\*** | Contract/open items in Papers | OQ-10/12/16/21… | ≠ OQ-GF |
| **EB-\*** | Coordination workstream | EB-0.3B, EB-008 | 两仓共用叙事 |
| **BUG-V3-\*** | V3 bugs | BUG-V3-001… | 不与 Papers BUG 混号 |
| **BUG-\*\*** | Papers bugs | BUG-09… | 同号拆分需映射 |
| **D-048-\*** | Known Issue Binding | D-048-1/2/3 | binding ≠ closed |
| **REPORT-A…K / X2** | AITutorX audit reports | REPORT-X2-… | X2 为本阶段 |
| **AIT-DEC-\*** | REPORT-C 提案 canonical | AIT-DEC-001… | **未被账本采用**；见 X2-06 |
| **GF-\*** | AITutorX governance foundation | GF-000…006 | Frozen v0.2 |

`[FACT]` **历史 ID 不得擅自重编号。** 解决冲突用 mapping / alias / legacy reference。

---

## 7. Disambiguation Notes（高风险同名）

| Term | Risk | AITutorX rule |
|------|------|---------------|
| `Evidence` | Producer structure facts vs V3/EB-008 admission evidence | 必须写 `Producer Evidence` / `Admission Evidence` |
| `IR` | Producer resolver IR vs V3 transient Semantic IR | 必须写 `Producer IR` / `V3 Semantic IR` |
| `Identity` | file identity vs question identity vs authority identity | 写全限定词 |
| `Phase` | 项目生命周期 vs Evidence Promotion 子阶段 | V3 91：`Phase I-n` vs `EP-Stage n`；新文档禁单字母 |
| `Gate` | V3 验证门 vs REPORT-I Migration Gate vs Gate 9 | 写 `V3 Gate` / `Migration Gate` |
| `Frozen` | Contract content freeze vs GF governance freeze vs Design 自述冻结 | 写明 freeze object |
| `canonical` | canonical question type vs canonical ledger vs canonical identity | 写明对象 |
| `L0–L7` | 多套层级体系 | OD-03 分层模型为准；执行状态仍 OPEN（OQ-GF-015） |
| `manifest` | Producer manifest vs V3 annotation manifest | 写 `Evidence Manifest` / `Annotation Manifest` |
| `Material` | 误限为文字 | 见 §4；含视觉/外部材料 |

---

## 8. Material — Explicit Rule（任务书要求）

```text
Material 可以包含：
  题图 / 配图 / 图表 / 图片 / 其他题目依赖的外部材料

single question 也可以拥有 Material。
禁止把 Material 错误限制为文字。
```

`[FACT]` 支撑: V3 10 materials/figures schema；prd material/extra/image 库；V3 P3「题干、选项、材料、答案、详解及图片等 Source-derived content」。

---

## 9. Non-Claims

- 本表不修改 V3 91 / DICTIONARY / Contract 词面
- 不关闭 C-X2-03 taxonomy 冲突
- 不采纳 AIT-DEC-* 为正式 namespace（待 Owner）

---

*Terminology map registered. Historical IDs preserved.*
