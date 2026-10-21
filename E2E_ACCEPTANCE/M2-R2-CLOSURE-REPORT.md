# M2-R2 六项报告

**提交**：`336453b`（本地 `od01-r3-convergence`，未推送）  
**输入包**：`06_M1_PACKAGES/chem-2018-spring-huikao-teacher/`（2018 春季会考化学）  
**正式入口**：`PreprocessingImportService.import_package` → `TaskExecutor._process`（manifest units 驱动）  
**数据库**：`aitutors_test` · 共享库前后一致（13 docs / 0 questions）  
**证据**：`e2e_run/m2-targeted-20261010T132440Z.json` 等

---

## 1. 本轮目标

修复 Annotation 仅 1/40、unit_id 错位（标 Q1 内容 Q8）。以 Producer manifest units 为权威输入，禁止 LLM 重切分/重编号。

## 2. 实际成果

| 项 | 内容 |
|---|---|
| **manifest 绑定** | `app/domains/source/manifest_annotation.py`：40 units 全绑定；Producer `unit_id` 保留 |
| **正式 Annotation 路径** | `annotate_from_payload`（不重切分）+ 每单元有界 LLM 核对（3 次，可审计） |
| **行号 1:1** | Seal `line_mode=raw_1to1`：含空行，manifest 行区间可绑定（根因：原抽取跳过空行→行号错位） |
| **Resolver 字段** | stem 使用 `question_search_lines`（Resolver 契约字段） |

## 3. 验收证据

### 三维度

| 维度 | 结果 |
|---|---|
| **覆盖率** | manifest 40 → 绑定 40 → Annotation 40（无静默丢失） |
| **身份正确性** | Q8 unit_id=Q8，stem_lines=[42,42]，`8．下列物质中，含有离子键的是` ✅ |
| **内容正确性** | Q8 选项 HCl / CO₂ / MgCl₂ / CH₄ 与原卷一致 ✅ |

### 逐题漏斗（真实）

| 阶段 | 数量 |
|---|---|
| Producer units | 40 |
| 绑定成功 | 40 |
| Annotation valid | 40（1 个 annotation payload） |
| Candidates | **25**（21 approved + 4 pending_review） |
| **Questions 落库** | **21** |
| **QuestionInstances** | **21** |
| pending_review | 4（含 LaTeX 答案规范化，正确 fail-closed） |

### 测试

`test_manifest_annotation_binding.py` **8 passed**（含真实包 40 units + Q8 对齐 + 越界/重复拒绝）

### 其他

- SourceVersion：`role=preprocessing`, `artifact_kind=canonical_l1`, **line_count=584**
- live LLM：3 次单元核对（任务计数 `llm_invocations=3`），单次 Annotation 不重切
- 共享业务库：**无变化**（前后 snapshot 一致）

## 4. 未完成事项

| 事项 | 级别 |
|---|---|
| 19/40 未进 Candidate（Resolver/Gate 解析缺口） | 非阻塞（有界，可解释：待逐题 skip 原因导出） |
| 4 pending_review（LaTeX 答案等） | 合理 fail-closed，留给 M3 人工审核 |
| Gate/Admission 规则未放宽 | 按要求保持 |
| 本地提交未推送 | 记录 |

## 5. 整体进度

| 里程碑 | 状态 |
|---|---|
| **M1 输入就绪** | ✅ |
| **M2 后端闭环** | ✅ **达标**（真实 21 题经正式链入库，ID/内容正确） |
| **M3 可用产品** | ⬜ 下一步 |

## 6. 下一步

**M3a：在现有 Review Console 中显示真实 Question 内容并验证公式渲染。**

（按授权不再扩展低优先级治理。）

---

## DSH 独立核验清单

1. `manifest_annotation.py` 在正式 executor 路径（非仅测试）
2. Q8 unit_id / stem_lines[42,42] / 内容一致
3. 漏斗 40/40 绑定、21 Q/21 QI 可复核
4. `llm_invocations=3` 与 `llm_unit_checks` 一致
5. 共享库 snapshot 前后相同
