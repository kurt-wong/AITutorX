# M1 收口报告（六项）

**基线**：AITutors-v3 `od01-r3-convergence` @ `d16a5e9`（本地，领先 origin 15）  
**输入包**：`AITutor-X/E2E_ACCEPTANCE/06_M1_PACKAGES/chem-2018-spring-huikao-teacher/`  
**正式入口**：`load_package_from_dir` + `PreprocessingImportService`（非 Runner）

---

## 1. 本轮目标

打通「真实试卷 → 可验证自包含包 → 正式入口可接收」，为 M2 真实小卷主链验收消除输入侧阻塞。对应产品：能导入北京高中试卷。

## 2. 实际成果

| 项 | 成果 |
|---|---|
| **A 契约收口** | `CR-005`：role=`preprocessing` 入 Spec 枚举；`artifact_kind_for_role()` 单一权威（preprocessing→`canonical_l1`）；DA-38 正文与 Errata 对齐 |
| **B 原件身份** | `runner.py` 不再把 MD 哈希写入 `original_sha256`；找不到 PDF/DOCX 时 **fail-closed**；`source_content_sha256` 入 `source_meta` |
| **C 自包含包** | 真实 2018 春季会考化学卷：`paper.pdf` + `paper.md` + `manifest.json` + `PAIRING_EVIDENCE.json`；40 题单元；双身份哈希可验证 |
| **D 漏斗准备** | `funnel_recorder.py`：input_units→identity_ok→ir_ready→candidates→questions→instances→pending_review + 逐题失败原因 |
| **E Console 核实** | 已有 5 页（CandidateReview/DocumentReview/…）；显示 stem/option/answer 纯文本；**无 KaTeX/MathJax**；无 Question/Material API |

## 3. 验收证据

| 检查 | 结果 |
|---|---|
| manifest `source_content_sha256` vs 实算 MD | **一致** `0443945f…` |
| 原件 PDF 身份 | `8d3f9dad…` ≠ MD 身份 ✅ |
| 正式入口 `load_package_from_dir` | 成功加载 `paper.pdf` / `paper.md` |
| `_verify_package_identity` | **PASSED**（含 identity_version=2 Interface Scope） |
| 负向：篡改 manifest 哈希 | **fail-closed** `source_content_sha256 mismatch` |
| 回归测试 | **82 passed**（identity_phase_a / negative / split / seal_dbflow / import_e2e / load_package） |
| PDF-MD 配对可追溯 | 包内相对路径 + 双哈希 + `pairing.source_ref` 指向 Producer 源 |

## 4. 未完成事项

| 事项 | 是否阻塞 M2 |
|---|---|
| 真实小卷 Annotation→Gate→DB 尚未跑 | **是（即 M2 本体）** |
| Review Console 无公式渲染、无结构化问题分类 | 否（M3） |
| 本地提交未推送 GitHub | 否（但 DSH 远端审查会对不上，需在 M2 前 push 或注明） |
| 9 份旧 `04_V3_INPUT` 绝对路径包未迁移 | 否（M1 已提供新包范式） |

## 5. 整体进度

| 里程碑 | 状态 | 证据 |
|---|---|---|
| **M1 输入就绪** | ✅ 基本完成 | 真实包可搬、可验、正式入口接收；错配 fail-closed |
| **M2 后端闭环** | ⬜ 未开始 | 0 题入库；funnel 已备 |
| **M3 可用产品** | ⬜ 未开始 | Console 骨架在，公式/反馈缺口已记录 |

距离「打开一道真实高中试题」：还差 **M2 全链 + M3a 展示**。

## 6. 下一步

**唯一主任务：M2 — 用本包跑正式主链，产出 3–10 题真实入库证据。**

验收条件：
1. 正式 API/服务路径（非 Runner 顶替）
2. 逐题漏斗记录（用 `funnel_recorder`）
3. DB 中 Question/Instance/内容与原卷人工对照
4. 失败阶段与原因可解释

需你裁决：无（M1 一次授权已覆盖）。若 M2 要用 live LLM Annotation，需确认 `LLM_GATEWAY_MODE=live` 的费用授权。
