# 生产能力实测（第一批）— 不是治理报告

**库**：`aitutors_prod_batch`（新建，与 `aitutors` / `aitutors_test` / `aitutors_testsuite` 隔离）  
**输入**：4 份已 Preprocessing 的真实会考卷（化学/地理/数学/物理，2018 春）  
**入口**：`PreprocessingImportService.import_package` + `TaskExecutor.run_once`（现有管线）  
**目标**：量「准确题目产出率」，不扩架构、不调 Gate 冲数量。

---

## 一、核心结果

| 指标 | 数值 |
|---|---|
| 输入卷数 | **4** |
| Producer 单元总数 | **117**（40+25+30+22） |
| Resolver 就绪 | **72** |
| 安全拒绝（incomplete） | **45** |
| 生成 Candidate | **72** |
| **自动入库 Question** | **31** |
| 人工待审 pending_review | **41** |
| 入库题内容完整（stem+answer+option） | **31 / 31** |

**有效产出率（入库 / 单元）= 31/117 ≈ 26.5%**  
**就绪→自动入库 = 31/72 ≈ 43%**（其余 41 条待人工，未算错误）

---

## 二、分卷

| 卷 | 单元 | 就绪 | 拒绝 | Candidate | 入库 | 主要问题 |
|---|---|---|---|---|---|---|
| 化学（对照） | 40 | 24 | 16 | 24（21 批+3 待审） | **21** | Q9/19/24/25 表格选项、U-req/U-org 等 16 条 incomplete |
| 数学 | 30 | 30 | 0 | 30 **全 pending** | **0** | 能解析但 Gate 未 auto-approve（待人工） |
| 物理 | 22 | 18 | 4 | 18（10 批+8 待审） | **10** | 4 条 incomplete |
| 地理 | 25 | **0** | **25** | 0 | **0** | 单元为 composite 形态（questions_lines/material_lines，无 stem_lines）→ Resolver 全量无法绑定 |

---

## 三、质量门槛（未降低）

- 31 条入库题 **均有 stem + answer + option**（option 行 124）。
- 45 条 incomplete **拒绝入库**，FunnelRecorder 已记 unit 级原因（formal path）。
- 未改 Gate/Admission 追数量；未拆 Q9 类复杂结构。

---

## 四、主要失败类型（按影响）

1. **地理 composite 单元形态**（25 条全拒）— manifest 无 stem_lines/options_lines，与当前 `bind_units_from_manifest` 契约不匹配。  
2. **数学 30 条全 pending** — 解析成功但未过自动入库门槛（答案/题型 grammar）。  
3. **化学/物理 option 表格与部分 stem/answer 未解析** — 与已知 Q9 簇同类。  
4. **打包陷阱**（测量过程）：误用 reslice 切片 md 会 100% 失败；必须用原始 OCR md + 对齐行号 manifest。

---

## 五、下一步（按产出优先级）

1. **人工消化 41 条 pending**（尤其数学）— 零代码，直接增加正式题库。  
2. **地理 composite 绑定**（影响 25/117≈21% 单元）— 值得做。  
3. 表格选项（化学 4 题）— 看 3–5 卷样本里是否高频再决定。  
4. 显示问题（M3C-FE-001）与入库质量分开。

---

## 六、附件

- `e2e_run/phase-c-production-batch/PROD-METRICS.json`
- `backend/data/funnels/*.json`（unit 级拒绝原因）
