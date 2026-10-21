# M1 修复 + M2 真实小卷 E2E · 六项报告

**执行基线**：AITutors-v3 `od01-r3-convergence` @ `d16a5e9` + M1 修复（本地未推送）  
**输入包**：`E2E_ACCEPTANCE/06_M1_PACKAGES/chem-2018-spring-huikao-teacher/`  
**正式入口**：`PreprocessingImportService.import_package` → `TaskExecutor._process`  
**数据库**：`aitutors_test`（隔离库）· 共享库未改动  
**证据文件**：`e2e_run/m2-real-chem-20261010T062722Z.json` · `m2-targeted-20261010T063013Z.json`

---

## 1. 本轮目标

用真实化学试卷包，经正式消费入口完成 Annotation → Gate → Candidate 主链，产出可解释漏斗；并完成 M1 两项缺口修复。

## 2. 实际成果

### M1 两项修复

| 修复 | 内容 | 验证 |
|---|---|---|
| **A. role/artifact_kind 强制** | `validate_artifact_compatibility` 拒绝 `preprocessing+raw_l1`、`native+canonical_l1` 等冲突 | 45 passed（含冲突拒绝） |
| **B. PDF-MD 配对证据** | `PAIRING_EVIDENCE.json` 绑定真实 OCR 台账：`source_sha256=8d3f9dad…`、`output_rel=会考/化学/….md`、`written_at=2026-09-13` | 哈希一致；不以文件名代替身份 |

### M2 正式主链

| 阶段 | 结果 |
|---|---|
| 正式导入 | ✅ Document + SourceVersion(`role=preprocessing`, `artifact_kind=canonical_l1`, `sealed`, 273 行) |
| Task 执行 | ✅ `succeeded`，`llm_invocations=1`（live MIMO，单次 Annotation） |
| Annotation | ✅ `valid`（semantic-annotation/v1） |
| Gate | ✅ 运行；产出 **1** 个 Candidate |
| Candidate | `pending_review`（admission 层 fail） |
| Question / Instance | **0**（待人工审核后才物化） |

## 3. 验收证据

### 漏斗（真实）

| 阶段 | 数量 | 说明 |
|---|---|---|
| 输入单元（Producer） | 40 | manifest units |
| identity_ok | 1 | 双哈希 + Interface Scope 通过 |
| IR Ready / sealed SV | 1 | canonical_l1 273 行 |
| LLM 语义单元 | **1** | ⚠️ 仅抽出 1/40 |
| Candidates | 1 | unit_type=standalone_unit |
| pending_review | 1 | gate admission fail |
| Questions / Instances | 0 | 未物化 |

### 内容抽检（Q 候选）

- stem：`8．下列物质中，含有离子键的是` — 与原卷第 8 题一致
- options：A `HCl` 等 — 已解析
- answer：`8、 $ 32^{\circ} $C` — **含 LaTeX/题号前缀，Gate 判定「answer not expressible as canonical value」→ pending_review**（正确 fail-closed）
- ⚠️ 单元 ID 错位：Annotation 标 `Q1`，span/内容实为 `Q8`

### 身份与隔离

| 检查 | 结果 |
|---|---|
| `original_sha256` = PDF `8d3f9dad…` | ✅ |
| `source_content_sha256` = MD `0443945f…` | ✅ |
| SourceVersion `artifact_kind` | `canonical_l1` ✅（CR-005） |
| 共享业务库 | **未写入**（全程 aitutors_test） |
| 归档证据 | `PAIRING_EVIDENCE.json` 含 OCR 台账 `source_rel/output_rel/written_at/pages` |

### 费用/用量

- live LLM 调用：**1** 次 document annotation（77 秒）
- 无重试风暴；失败即停

## 4. 未完成事项

| 事项 | 级别 |
|---|---|
| **LLM Annotation 只抽出 1/40 单元** | 阻塞 M2 达标（内容完整性） |
| **单元 ID 错位**（标 Q1 / 实 Q8） | 阻塞内容正确性 |
| 答案含 LaTeX/前缀 → 无法自动 canonical | 合理 pending_review（需 M3 人工审核或答案归一化） |
| Question/Instance 未物化 | 待 pending_review 处理 |
| 本地提交未推送 GitHub | 记录 |

## 5. 整体进度

| 里程碑 | 状态 | 证据 |
|---|---|---|
| **M1 输入就绪** | ✅ **完成** | 自包含包 + 配对证据 + 强制校验 |
| **M2 后端闭环** | 🟡 **部分** | 正式链 **跑通**；1 题入 Candidate；0 题入库；Annotation 覆盖率 1/40 |
| **M3 可用产品** | ⬜ | Console 骨架在 |

**诚实结论**：正式主链已证明可跑通，但 **Annotation 覆盖率与单元对齐未达标**，不能宣称 M2 完成。

## 6. 下一步

**唯一主任务：修复 Annotation 覆盖率（40→应接近 40）与单元 ID 对齐。**

建议方向（供裁决）：
1. 检查 prompt/分段是否导致模型只输出 1 个 unit
2. 或改用 Producer 已有 manifest units 作为 Annotation 输入（正式路径内适配，而非实验 Runner）
3. 答案 LaTeX 归一化规则（M3 或 M2 扩展）

需你裁决：是否授权「以 Producer manifest units 作为正式 Annotation 来源」以避免 LLM 重新抽取？这将显著提高覆盖率并保留人工验收结构。

---

**DSH 独立核验清单**（同包同提交只读）：
1. `PAIRING_EVIDENCE.json` 与 OCR 台账一致
2. `validate_artifact_compatibility` 拒绝冲突组合
3. DB 中 SV=`canonical_l1`、`original_sha256`=PDF
4. 漏斗 JSON 与库内计数一致
5. 共享库无变化
