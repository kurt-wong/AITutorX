# Owner 裁定 · Round 2 执行范围限定（一页指令）

```text
裁定时间   : 2026-10-09
效力       : 即时生效，覆盖/取代 MIMO-TASK-PHASE1-MINIMAL-E2E-01.md 中与本文件冲突的条款
执行授权   : TASK_B_BOUNDARY_BRIEF.md + 本文件
```

---

## 0. 三项矛盾裁定（先于一切执行）

### 矛盾 1 — 库状态不成立 → 裁定：基线作废，按 fresh_test 处理

- 任务书 PART 1.3 的 `llm_call_audit=1213` / 2026-09-30 现场 **已不存在**。
- 当前库是 **2026-10-09 14:30 UTC 之后的新库**（PG 启动时间可证）。
- **裁定**：
  1. 承认历史现场丢失，**不得伪造或回填** 1213 条对照基线。
  2. 本轮前后对照 **不以 2026-09-30 为基准**；以「本轮开工前的只读快照」为唯一基线。
  3. OD-P1-B「禁止清库」在本轮记为 **已被事实违反一次**；后续若再清库 = LEVEL 3。
  4. 执行体必须在开工前留存只读快照（表计数 + 时间戳 + PG 启动时间）。

### 矛盾 2 — 合成僵尸 task → 裁定：禁止按真实僵尸处置

- 16 task / 15 task_claims 落在 7 秒窗口 = **种子写入**，不是历史运行残留。
- **裁定**：
  1. 禁止把它们 `mark interrupted` 后记作「历史僵尸已处置」。
  2. 若需处置，必须先写明 seed 来源脚本，并在 provenance 标注 `synthetic_seed`。
  3. 否则原样保留，只在报告中列为「合成数据，不计入验收」。

### 矛盾 3 — 旧任务书效力 → 裁定：Superseded，只认 TASK_B

| 冲突项 | 旧任务书 | 本裁定 |
|---|---|---|
| 扩展名白名单 | 允许放宽 | **禁止顺手改**；改前必须完成身份裁定 |
| 实验路径 | 允许 preprocessing_consumer Runner 跑通 | **禁止 Runner 顶替正式入口** |
| 成功定义 | 表里出现行 | 必须证明产物**沿正式入口**进入 |

- `MIMO-TASK-PHASE1-MINIMAL-E2E-01.md` **保留为历史授权记录**，首页加 SUPERSEDED 标注。
- 执行体 **只允许** 按 `E2E_ACCEPTANCE/TASK_B_BOUNDARY_BRIEF.md` + 本文件行动。

---

## 1. 架构硬约束（Round 2，不可协商）

1. **唯一主路径**：已验收 preprocessing 产物 → 正式 V3 入口 → Seal → Annotation → Gate → DB → 前端。
2. **禁止静默回退**：manifest 缺失 / hash 不匹配 / 源 .md 不可读 / 适配失败 → **明确失败**，禁止调用 `NativeTextProvider`。
3. **禁止双路径择优**：不得同时跑 preprocessing + native 再取更好的结果。
4. **禁止用 Phase 1 `preprocessing_consumer` Runner 顶替正式入口**。Runner 只可作只读定位工具。
5. **负向验收必须通过**（见 §3）。

---

## 2. 身份边界（实现前必须遵守）

| 字段 | 允许写入 | 禁止 |
|---|---|---|
| `documents.original_sha256` | **仅**原始上传字节（PDF/DOCX/用户原件） | Markdown 字节、产物字节 |
| source version 层 | `source_content_sha256`（Markdown 原始字节）经 jsonb `source_meta` / `input_identity` | 塞进 `original_sha256` |
| `DocumentSourceVersion.role` | `preprocessing` + `provider=preprocessing`（已存在合法配对） | 混用 `canonical` 空 provider |

- `canonical` 空 Provider 是**非 Seal 路径实现约定**，本任务不得复用。
- 需要表达「原始文档 → 多源版本」时，使用现有 `parent_version_id` / `DocumentSourceVersion`，**不新增身份体系**。

---

## 3. 负向验收（必须全部明确失败）

- [ ] preprocessing manifest 缺失 → 明确失败
- [ ] `source_content_sha256` 不匹配 → 拒绝消费
- [ ] 源 Markdown 缺失或不可读 → 明确失败
- [ ] 结构与 V3 消费契约不兼容 → 明确失败并记录阶段
- [ ] 以上任一失败 **均未** 调用 `NativeTextProvider`

---

## 4. 成功定义（四种结果不可互换）

| 结果 | 是否算本任务成功 |
|---|---|
| Runner / 脚本 exit 0 | 否 |
| 生成候选题 JSON | 否 |
| **正式 API 入库**（documents→source_versions→questions 等） | 需全部满足 |
| **前端正确显示**题干/选项/答案 | 需全部满足 |

机械可查验收：目标表出现可追溯到 `source_content_sha256` 的行，且 `original_sha256` 指向原始 PDF。

---

## 5. 证据要求

- 文件哈希一律 **全 64 hex + 标注 `sha256:`**，禁止只报 16 hex。
- 每层记录：输入 / 输出 / 数量 / ID 关联 / 失败原因 / 文件哈希。
- 开工前只读快照 + 收工后对照快照，两者都必须落在交付证据里。

---

## 6. 明确禁止

- 顺手重构 Resolver / Gate / Admission / 数据库身份体系
- 改 Frozen Spec / Migration / 清库
- 用实验路径或旧任务书条款宣布成功
- 把合成 seed 数据记作真实历史处置

---

**一句话**：先打通唯一正式主链；任何绕过该路径的“成功”，本轮一律无效。
