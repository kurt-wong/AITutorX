# X2 DSH Independent Adversarial Audit — Attack Report

**Auditor:** MiMo (DSH)
**Date:** 2025-09-14
**Scope:** Attack audit of AITutorX Unified Documentation Governance
**Baseline:** GitHub remote state + local tracked files only (Claude commit 7002f38 NOT included)

---

## ATTACK 1: 统一文档是否真的统一

### 攻击目标
检查统一文档是否真的形成唯一系统叙事，还是只是把文件放进AITutorX/Docs/目录。

### 实际观察

**OBSERVED (GitHub remote main):**
- `Docs/10_SPEC/.gitkeep` — 空目录
- `Docs/20_ARCHITECTURE/.gitkeep` — 空目录
- `Docs/30_CONTRACTS/.gitkeep` — 空目录
- `Docs/40_DECISIONS/.gitkeep` — 空目录
- `Docs/50_OPERATIONS/.gitkeep` — 空目录

**OBSERVED (Claude commit 7002f38, NOT pushed):**
- 添加了X2-01到X2-10文档
- 添加了REPORT-X2-UNIFIED-GOVERNANCE.md

**VERIFIED:**
- GitHub远程main分支上，Docs/目录下只有00_GOVERNANCE/有内容
- 其他目录都是空的，只有.gitkeep文件
- Claude的统一文档还没有推送到GitHub

**REFUTED:**
- "统一文档"目前只是目录结构，没有实际内容
- V3和preprocessing的概念仍然在各自仓库中独立存在

### 结论
**NOT UNIFIED** — 统一文档只是目录统一，没有实际内容统一。

---

## ATTACK 2: Producer/Consumer边界是否仍然正确

### 攻击目标
检查合并成AITutorX后，Contract是否仍然是binding boundary。

### 实际观察

**OBSERVED (from AITutorX README):**
```
来源仓库：
| Consumer (V3) | `D:\Project\AITutors-v3` | `kurt-wong/AITutors-v3` |
| Producer (Preprocessing) | `D:\Project\Papers` | `kurt-wong/Aitutors-preprocessing` |
```

**OBSERVED (from V3 DICTIONARY):**
- V3有完整的概念定义：Question, QuestionInstance, Material等
- V3有完整的状态定义：ready, incomplete, unknown
- V3有完整的生命周期：Source → Annotation → Resolver → IR → Gate → Admission

**OBSERVED (from preprocessing prd.md):**
- preprocessing定义了：Source Evidence Producer
- preprocessing定义了：standalone_question, composite_question
- preprocessing定义了：manifest, annotated.md

**VERIFIED:**
- V3和preprocessing仍然有各自独立的概念体系
- Contract v0.2仍然存在，但没有被推送到AITutorX
- Producer/Consumer边界在文档中被描述，但没有在代码中实现

**CONFLICT:**
- AITutorX README说"统一最终工程骨架"
- 但V3和preprocessing仍然是独立的仓库
- 没有实际的代码合并或接口实现

### 结论
**边界仍然正确，但未实现** — Producer/Consumer边界在概念上存在，但在AITutorX中没有实际实现。

---

## ATTACK 3: Concept是否真正统一

### 攻击目标
检查Question, QuestionInstance, Material, Source等概念是否在V3和preprocessing中有统一的定义。

### 实际观察

**OBSERVED (V3 DICTIONARY):**
- Question: "Admission 后 canonical domain entity"
- QuestionInstance: "Question 在某 Source 中的一次 occurrence"
- Material: "题目依赖的外部材料：文字 + 题图 + 配图 + 图表 + 图片等"
- Source: "进入系统的原始考试文档事实层"

**OBSERVED (preprocessing prd.md):**
- Source: "原始 ground truth"
- standalone_question: "无共享材料的独立题"
- composite_question: "若干小题共享同一段前置材料"
- manifest: "纯行号引用的结构化元数据"

**OBSERVED (AITutorX X2-03 CONCEPT-TERMINOLOGY-MAP, NOT pushed):**
- 试图统一概念：Source, Source Version, Source Identity
- 试图统一概念：IR, Semantic Annotation, Material
- 试图统一概念：Question, QuestionInstance, Knowledge

**VERIFIED:**
- V3和preprocessing对同一术语有不同定义
- 例如：V3的"Material"包含题图/配图/图表，preprocessing的"material"只是composite中的材料部分
- 例如：V3的"IR"是Semantic IR，preprocessing的"IR"是Producer IR

**REFUTED:**
- 概念没有真正统一
- X2-03试图统一，但还没有被推送到GitHub
- V3和preprocessing仍然使用不同的术语体系

### 结论
**概念未统一** — V3和preprocessing对同一术语有不同定义，没有形成统一的概念体系。

---

## ATTACK 4: 旧文档到底有没有正确分类

### 攻击目标
检查文档是否有正确的authority, historical, superseded, evidence, migration candidate分类。

### 实际观察

**OBSERVED (GitHub remote main):**
- 只有`Docs/00_GOVERNANCE/`有内容
- 其他目录都是空的

**OBSERVED (Claude commit 7002f38, NOT pushed):**
- 添加了X2-05-UNIFIED-DOCUMENTATION-MAP.md
- 添加了X2-08-MIGRATION-CANDIDATE-REGISTRY.md

**VERIFIED:**
- 没有实际的文档分类系统
- 没有authority层级定义
- 没有historical/superseded标记
- 没有migration candidate注册表

**REFUTED:**
- 文档分类只是概念，没有实际实现
- 没有证据显示文档被正确分类

### 结论
**未正确分类** — 文档分类只是概念，没有实际实现。

---

## ATTACK 5: Decision namespace碰撞

### 攻击目标
检查V3和preprocessing的历史DEC撞号有没有被真正处理。

### 实际观察

**OBSERVED (V3 DECISIONS):**
- DEC-021, DEC-022, DEC-023等

**OBSERVED (preprocessing DECISIONS):**
- DEC-021, DEC-022, DEC-023等（相同号码）

**OBSERVED (AITutorX X2-06 DECISION-MAPPING, NOT pushed):**
- 试图建立mapping：V3 DEC-XXX → AITutorX DEC-XXX
- 试图建立mapping：Papers DEC-XXX → AITutorX DEC-XXX

**VERIFIED:**
- V3和preprocessing有相同的DEC号码
- 没有实际的mapping实现
- 没有可执行的规则防止碰撞

**REFUTED:**
- DEC碰撞没有被真正处理
- 只是写了一个mapping，没有形成可执行规则

### 结论
**未真正处理** — DEC碰撞只是被登记，没有被解决。

---

## ATTACK 6: 71/87/166/177的lineage

### 攻击目标
检查有没有把不同集合的含义混在一起。

### 实际观察

**OBSERVED (V3 Frozen Spec v1.0):**
- 文档71: V3 Design v1.1
- 文档87: V3 Frozen Spec v1.0
- 文档166: GF v0.2
- 文档177: Contract v0.2

**OBSERVED (AITutorX X2-07 DIFFERENCE-LEDGER, NOT pushed):**
- 试图解释这些数字的含义
- 试图建立这些数字之间的关系

**VERIFIED:**
- 这些数字来自不同的文档集合
- 没有证据显示这些数字被正确解释
- 没有证据显示这些数字之间的关系被正确建立

**UNKNOWN:**
- 这些数字的具体含义
- 这些数字之间的实际关系
- 这些数字是否被正确使用

### 结论
**含义未知** — 这些数字的具体含义和关系不清楚。

---

## ATTACK 7: Migration Candidate Registry

### 攻击目标
检查是登记资产，还是已经偷偷变成migration plan。

### 实际观察

**OBSERVED (AITutorX X2-08 MIGRATION-CANDIDATE-REGISTRY, NOT pushed):**
- 登记了Specs, Contracts, Architecture, Decisions, Reports, Tests, Code等
- 标记了Migration readiness: NOT_READY, CANDIDATE_UNGATED, GATE_BLOCKED

**VERIFIED:**
- Registry只是登记，没有实际的migration plan
- 没有出现"candidate = ready"的越权语义
- 所有资产都被标记为GATE_BLOCKED或NOT_READY

**REFUTED:**
- Registry没有变成migration plan
- 没有越权语义

### 结论
**正确登记** — Registry只是登记资产，没有变成migration plan。

---

## ATTACK 8: UNKNOWN处理

### 攻击目标
检查是否真的保持"可审查、不可静默丢弃"。

### 实际观察

**OBSERVED (AITutorX AGENTS.md):**
- UNKNOWN is retained data
- 不得 silent skip / fallback
- UNKNOWN → reviewable record → pending_review

**OBSERVED (V3 DICTIONARY):**
- admission_status: approved / candidate / rejected
- 没有unknown状态

**OBSERVED (preprocessing prd.md):**
- 没有提到UNKNOWN处理

**VERIFIED:**
- AGENTS.md定义了UNKNOWN处理原则
- 但V3和preprocessing没有实现UNKNOWN状态
- 没有证据显示UNKNOWN被保留

**UNKNOWN:**
- 是否有UNKNOWN记录存在
- 是否有测试验证UNKNOWN处理
- 是否有示例显示UNKNOWN被保留

### 结论
**未验证** — UNKNOWN处理只是原则，没有实际实现验证。

---

## ATTACK 9: Material支持

### 攻击目标
检查是否真的支持题图、配图、图表等非文本材料。

### 实际观察

**OBSERVED (V3 DICTIONARY):**
- Material: "题目依赖的外部材料：文字 + 题图 + 配图 + 图表 + 图片等"
- question_images: 图片关联表

**OBSERVED (preprocessing prd.md):**
- material: "composite的材料/文章"
- extra: "卫星锚：配图/表格因排版漂移到题干区之外时的归属标注"

**OBSERVED (AITutorX X2-02 UNIFIED-ARCHITECTURE-BASELINE, NOT pushed):**
- Material ≠ 纯文字
- Material 可包含: 题图, 配图, 图表, 图片, 其他题目依赖的外部材料
- single question 也可以拥有 Material

**VERIFIED:**
- V3支持Material（包含视觉材料）
- preprocessing支持material和extra（视觉材料）
- X2-02试图统一Material定义

**REFUTED:**
- Material定义没有错误绑定到composite question
- single question可以拥有Material

### 结论
**正确支持** — Material确实支持非文本材料，single question可以拥有Material。

---

## ATTACK 10: AITutorX是否已成为真正的Target System

### 攻击目标
检查AITutorX是否已经从"两个子项目的容器"变成"统一系统"。

### 实际观察

**OBSERVED (GitHub remote main):**
- AITutorX是单一仓库
- 但只有空骨架目录
- 只有治理文档（00_GOVERNANCE/）

**OBSERVED (Claude commit 7002f38, NOT pushed):**
- 添加了统一文档（X2-01到X2-10）
- 添加了统一报告（REPORT-X2）
- 但还没有推送到GitHub

**VERIFIED:**
- AITutorX在结构上是单一仓库
- 但内容上仍然是V3 + preprocessing两个子项目
- 没有实际的代码合并
- 没有实际的接口实现
- 没有实际的统一生命周期

**REFUTED:**
- AITutorX没有成为真正的Target System
- 仍然只是"两个子项目的容器"
- 没有形成统一的治理、规范、架构

### 结论
**NOT TARGET SYSTEM** — AITutorX没有成为真正的Target System。

---

## 总结

### 通过的攻击
1. **Migration Candidate Registry** — 正确登记，没有越权语义
2. **Material支持** — 正确支持非文本材料，single question可以拥有Material

### 未通过的攻击
1. **统一文档** — 只是目录统一，没有实际内容统一
2. **Producer/Consumer边界** — 概念上存在，但未实现
3. **Concept统一** — V3和preprocessing对同一术语有不同定义
4. **文档分类** — 只是概念，没有实际实现
5. **Decision namespace碰撞** — 只是登记，没有解决
6. **71/87/166/177 lineage** — 含义未知
7. **UNKNOWN处理** — 未验证
8. **AITutorX作为Target System** — 没有成为真正的Target System

### 未知的攻击
1. **71/87/166/177 lineage** — 具体含义和关系不清楚

---

## BLOCKERS

| # | Blocker | Type | Impact |
|---|---------|------|--------|
| 1 | Claude commit 7002f38未推送到GitHub | CRITICAL | 所有X2文档都是本地，不是GitHub事实 |
| 2 | Docs/目录下大部分为空 | HIGH | 统一文档只是目录结构 |
| 3 | V3和preprocessing仍然是独立仓库 | HIGH | 概念和代码没有统一 |
| 4 | 没有实际的代码合并 | HIGH | 没有实现统一系统 |
| 5 | 没有实际的接口实现 | HIGH | Producer/Consumer边界未实现 |
| 6 | 概念定义不统一 | MEDIUM | V3和preprocessing使用不同术语 |

---

## RECOMMENDATIONS

1. **立即推送Claude commit 7002f38到GitHub** — 这是所有X2文档的基础
2. **填充Docs/目录** — 不能只有空骨架
3. **统一概念定义** — 必须解决V3和preprocessing的术语冲突
4. **实现Producer/Consumer接口** — 不能只是文档描述
5. **解决DEC碰撞** — 必须有可执行的规则
6. **验证UNKNOWN处理** — 必须有测试证据

---

## NEXT STEPS

1. **等待Claude的X2输出** — 将与此报告进行交叉比对
2. **等待Owner澄清** — 关键问题需要Owner决策
3. **无法进入X3 Migration** — 直到blockers解决

---

*Report generated by MiMo (DSH) on 2025-09-14*
*Status: ATTACK AUDIT COMPLETE*
*Next: Awaiting Claude's X2 output for cross-validation*
