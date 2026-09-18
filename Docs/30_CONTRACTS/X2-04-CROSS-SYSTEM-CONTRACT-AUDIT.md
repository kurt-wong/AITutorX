# X2-04 — Cross-System Contract Audit

**Document ID**: X2-04
**Task**: TASK-X2-CLAUDE
**Document Type**: Contracts / Audit
**Status**: `ACTIVE — X2 CONTRACT AUDIT`
**Date**: 2026-09-18
**Upstream**: Contract v0.2 Freeze Object（`f4941ff` / sha256 `9c6b9063…7528`）；X2-01/02/03
**Hard rule**: Audit ≠ 修改 Frozen Contract；≠ Implementation Authorization

---

## 0. Freeze Object Verification

`[FACT]` 唯一 Contract Freeze Object:

| Field | Value |
|-------|-------|
| repository | `kurt-wong/AITutors-v3` |
| commit | `f4941ff87c0130ee0b79ff6b807c4ec2826b8ff1` |
| path | `Docs/COORDINATION/CONTRACTS/PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` |
| sha256 | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |

`[FACT]` 双仓账本（V3 CURRENT / Papers CURRENT）均指向上述四元组；`c6e771c` 排除。

`[CONFLICT]` C-X2-01：账本状态 = `FROZEN`（V3 DEC-036）；当前 tracked Contract 正文文首仍含 `DRAFT / READY FOR FREEZE / NOT FROZEN` 叙事（因 Freeze Artifact 禁改，正文无法追记）。**AITutorX 处置建议** `[PROPOSAL]`: 账本 = 状态权威；Freeze Object = 内容权威。**待 Owner 确认。**

---

## 1. Identity

| Question | Audit result | Label |
|----------|--------------|-------|
| Producer 与 Consumer 是否使用相同 identity semantics？ | **Contract 层已裁统一**: `source_content_sha256 = SHA256(original source bytes)` 64 hex；path 仅 locator | `[FACT]` DEC-030/031 |
| 实现层是否已对齐？ | **否**。V3 五项能力 NOT IMPLEMENTED（Manifest identity verification / raw bytes acquisition / independent SHA256 / IR identity verification / identity gate） | `[FACT]` Contract §5.6.1 |
| 历史异名 | Producer IR `source_sha256`；V3 internal `source_version_id`；OCR `source_sha256`=PDF bytes | `[FACT]` 双层/双名域 |
| D3 内部字段名争议 | M3 实现 `source_content_sha256` vs Design v1.1 `source_sha256`；Contract 对 Python 签名零规定 | `[UNKNOWN]` authority；Papers DEC-049 D3 OPEN |
| OD-04 AITutorX 层 | Hash-based Source Identity；双树均输入来源；不建永久排序 | `[OWNER DECISION]` |

**结论**: Identity **语义** 已冻结且双侧书面一致；**实现消费验证链**未完成；**接口 Python 签名**未冻结。

---

## 2. Manifest

| Question | Audit result | Label |
|----------|--------------|-------|
| Manifest 如何进入 V3？ | Contract: Manifest = Source Identity Authority；V3 义务 = 验证 Manifest + 重算 hash + 判断接受 | `[FACT]` Contract §0.5 |
| V3 现状 | `manifest_reader.py` 无校验叙事（REPORT-F/FACT-043）；历史观测 manifest 仅作事实输入 | `[OBSERVED]` |
| 接口面数字 | Manifest scope **87**；Step2 回填 87/87 `source_content_sha256` | `[FACT]` CURRENT 关键数字 |
| 总 manifest 规模 | 166 manifests（历史资产面） | `[FACT]` |
| 禁则 | 禁「IR available = Interface available」；166 ≠ 正式接口 | `[FACT]` DEC-023/024 |

**结论**: Manifest 作为 identity authority 已裁；V3 消费验证未实现；数字必须区分 87 / 71 / 16 / 166 / 79。

---

## 3. OCR

| Question | Audit result | Label |
|----------|--------------|-------|
| OCR 产物是什么？ | 源 markdown（ground truth）+ 图片库 `_imgs/` + OCR 清单 `ocr_output_manifest.jsonl` | `[FACT]` prd §2.1/§3 |
| 引擎 | PaddleOCR-VL-1.6 API（现行叙事） | `[OBSERVED]` prd |
| 输入路径 | operational = `maintainess\PDF`（代码硬编码） | `[FACT]` REPORT-K |
| 身份词面 | OCR 清单 `source_sha256` = PDF 字节 sha（与 md 字节 sha 双层语义） | `[FACT]` GF-000 |
| 覆盖 | 清单 1801 vs manifest 166（sha 键 87）等数字不一致叙事 | `[FACT]` 覆盖缺口；OQ-GF-007 |
| AITutorX 数据模式 | OD-05 NAS-backed read-only；实施细节 OPEN | `[OWNER DECISION]` + OPEN |

**结论**: OCR 产物形态清晰；lineage 覆盖不全；数据本体不在 git。

---

## 4. IR

| Question | Audit result | Label |
|----------|--------------|-------|
| 谁产生？ | **Producer** 产 resolver IR artifact（resolver-ir-0.1） | `[FACT]` |
| 谁消费？ | **V3** 应为 Semantic Consumption Authority；现实 = 零/未完成 IR 消费能力 | `[FACT]` Contract；`[OBSERVED]` gap |
| 谁负责验证？ | Contract: V3 验证 IR 是否符合契约；不符合则拒收 | `[FACT]` §0.5 |
| 当前规模 | IR **71** ADMITTED（1,664 单元叙事）；16 Semantic Pending；v1 legacy **79** 隔离 | `[FACT]` CURRENT |
| V3 Semantic IR | transient；持久化形态 = candidate payload；禁另建中间表 | `[FACT]` V3_SPEC 20 |
| D2/D3/D4 | 接口形状/字段名/门面偏离；Evidence Brief 已交付；裁决暂停 | `[UNKNOWN]` / OPEN |

**结论**: IR 生产侧已冻结证据；消费验证与接口权威未收口。

---

## 5. Material（图片/图表/题图贯穿）

| Question | Audit result | Label |
|----------|--------------|-------|
| 概念 | Material 含题图/配图/图表/图片/外部材料；single question 可有 Material | `[FACT]` X2-03 §8 |
| Producer 侧 | manifest roles `material`/`extra`；`Ocr-markdown/_imgs/`；`recover_images.py` | `[FACT]` prd |
| Consumer 侧 | `materials` / `source_figures` / `material_links` / `instance_figure_links` | `[FACT]` V3 10 |
| 跨 pipeline 贯穿 | Producer figure_reference evidence → V3 source_figures → Question Material | `[PROPOSAL]` 统一叙事；实现未验证 |
| 已知缺口 | FACT-034 dangling figure refs；Step5 图片恢复未执行；V3 SourceFigure 字段级 interoperability 疑义 | `[OBSERVED]` / `[UNKNOWN]` |
| Contract 冻结范围 | 图片恢复流程 **不在** v0.2 冻结范围 | `[FACT]` Contract §0.2 |

**结论**: Material 概念两侧都有模型；**图片恢复与跨系统 figure identity 贯穿未冻结、未完成**。

---

## 6. Question

| Question | Audit result | Label |
|----------|--------------|-------|
| 何时从 IR 变成 Question？ | **仅当** Gate 通过 + Admission Transaction 物化 A 域 | `[FACT]` V3 10 §5.4 |
| Producer 是否产 Question？ | **否**（charter §12 / prd 非目标） | `[FACT]` |
| LLM 能否直接写 Question？ | **否**（V3 P2） | `[FACT]` |
| 历史 P2.3「输出 V3 Admission 格式」 | 已被 §12 取代 | `[FACT]` charter |

---

## 7. QuestionInstance

| Question | Audit result | Label |
|----------|--------------|-------|
| 定义 | Question 在某 Source 中的一次 occurrence | `[FACT]` V3 10 §6.2 |
| 与 Producer unit 关系 | `unit_id` 为 display alias，禁作跨系统键；汇编卷内可重复 | `[FACT]` Papers integration contract §2.1 |
| Occurrence 如何进入系统 | 依赖 Source seal + Annotation/Resolver/IR/Compiler/Gate/Admission 链 | `[FACT]` V3_SPEC |
| 迁移映射 | **未执行** | `[UNKNOWN]` |

---

## 8. Knowledge

| Question | Audit result | Label |
|----------|--------------|-------|
| 何时建立？ | Admission 之后的领域关联（schema 已定义） | `[FACT]` V3 10 |
| 由谁建立？ | 管理员维护 Knowledge Tree；AI 映射需 `mapping_source` + review | `[FACT]` DICTIONARY |
| Producer 是否建 Knowledge？ | **否**（非目标） | `[FACT]` |
| 本阶段是否验证关联流程实现？ | **否** | `[UNKNOWN]` |

---

## 9. State Separation Audit

| Axis | Producer / Contract | V3 | Separation held? |
|------|---------------------|----|------------------|
| Semantic | `{ready,incomplete,unknown}` | `{ready,incomplete}` frozen；`unknown` 未解冻 | **语义层词表**已裁统一；**V3 实现未齐** |
| Decision | `{pending_review,approved,rejected}` | candidate `decision_status` | 词表一致 |
| unknown 路由 | unknown → reviewable record → pending_review | 实现上 candidate 仅由 ready 产生 | **结构性缺口 C-X2-09** |
| ready/incomplete vs pending_review/approved/rejected | 明令禁合并（DEC-028 Part 5） | 两正交层（SEMANTIC vs DECISION） | **原则成立**；可达性缺口 |
| citation exists/tracked/referenced/admitted | GF Registry 总则 | n/a | held；admitted 全空 |
| Migration statuses | X2 登记 | n/a | held；无 GATE_PASSED/MIGRATED |

---

## 10. Contract Audit Summary

| ID | Topic | Semantic frozen? | Implementation aligned? | Blocking |
|----|-------|------------------|-------------------------|----------|
| CA-01 | Identity key | YES | NO | OQ-GF-001/002/017；D2/D3 |
| CA-02 | Path non-identity | YES | YES (FACT-044 path 仅 locator) | bytes 可达性 OQ-12 |
| CA-03 | Manifest verification | YES (requirement) | NO | 五项 NOT IMPLEMENTED |
| CA-04 | IR verification | YES (requirement) | NO | 同上 + D3/D4 |
| CA-05 | Semantic vs Decision state | YES (vocab) | PARTIAL | C-X2-09；BUG-V3-018 |
| CA-06 | Material/figures | PARTIAL (concept) | UNKNOWN | Step5；interoperability |
| CA-07 | Question/Instance/Knowledge boundary | YES (V3 L0) | N/A for migration yet | Migration Gate 未开 |
| CA-08 | Freeze status narrative | CONFLICT C-X2-01 | n/a | Owner 双文件规则 |
| CA-09 | Interface Python signatures | NO | disputed | DEC-049 D2/D4 |
| CA-10 | Scope numbers 87/71/16/166/79 | YES | Producer side verified | 禁止混用 |

---

## 11. Non-Claims

- 不修改 Frozen Contract 正文
- 不宣布 Consumer Identity Verification 已实现
- 不关闭 D2/D3/D4
- 不授权 migration

---

*Cross-system contract audit registered.*
