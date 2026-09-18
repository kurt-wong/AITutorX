# X2-07 — Difference Ledger

**Document ID**: X2-07
**Task**: TASK-X2-CLAUDE
**Document Type**: Decisions / Difference Ledger（审计登记）
**Status**: `ACTIVE — X2 DIFFERENCE LEDGER`
**Date**: 2026-09-18
**Upstream**: OD-18（建立 Difference Ledger 已裁；**不关闭 OQ-GF-007**）；X2-01 C-X2-*；REPORT-K/G/H/F
**Hard rule**: Ledger 登记 ≠ 关闭源账本；≠ 改写历史报告；87/71/166/177 引用必须关联 disposition

---

## 0. What this ledger is / is not

**是**: AITutorX 层「差异与缺口」登记，供 Owner 逐项 disposition。
**不是**: 源仓账本的替代；不是 admission；不是 Gate 结果。
`[FACT]` OD-18 明示不关闭 OQ-GF-007；本 X2 实例文件仍为 **审计登记**，非生产 Registry admitted 数据。

---

## 1. Numeric differences requiring disposition

| Diff ID | Numbers | Claimed in | Observed / cross-check | Disposition needed | Status |
|---------|---------|------------|------------------------|--------------------|--------|
| DL-01 | manifest **166** vs 接口面 **87** vs IR ADMITTED **71** vs Semantic Pending **16** vs v1 legacy **79** | Papers/V3 CURRENT；Contract §0.1② | 均为账本登记数字；语义不同不可混用 | Owner 确认 AITutorX 数据字典强制分列 | OPEN |
| DL-02 | OCR 清单 **1,801** vs manifest 166 vs snapshot 87 | GF-000；REPORT-K | 覆盖缺口叙事 | lineage 补全要求（OQ-GF-007） | OPEN-BLOCKING |
| DL-03 | maintainess/PDF **12,707** vs original PDF **38,893**；basename 交集 12,626 | REPORT-K | 抽样 6/6 sha 一致 | 双树保留策略 OQ-GF-004；口径更正 OQ-GF-011 | OPEN-BLOCKING / OPEN |
| DL-04 | R50 baseline **356** vs DRIFT **87**（预期） | Papers CURRENT | 269 MATCH / 87 SET_EQUAL drift | 引用时必须写「预期回填 drift」 | 已解释；引用纪律待固化 |
| DL-05 | IR 单元 **1,664**（71 文档） | Papers CURRENT | 与 71 ADMITTED 一致叙事 | 禁止把 1664 当 interface 数 | OPEN 引用纪律 |
| DL-06 | 177 锚定文件 | Papers Guardian G1/G2 | 双侧 177/177 PASS 叙事 | 迁移前是否重建锚 | OPEN |
| DL-07 | V3 测试 **1780 passed**（REPORT-A）vs Papers canonical **338/1** vs REPORT-I F9 **337+1failed** | 各报告 | 三套叙事；语义可能不同 harness | OQ-GF-018 canonical test baseline | OPEN-BLOCKING |
| DL-08 | V3 identity-chain **642 passed** + DB errors | Papers CURRENT/DEC-042/043 | errors 计数非基线 | 同 DL-07 | OPEN |
| DL-09 | Papers canonical pytest **338/1** vs V3 consumer suite 叙事 | Papers vs V3 | 不可互替 | 测试资产分类 | OPEN |

---

## 2. Authority / narrative differences

| Diff ID | Difference | Evidence | Disposition |
|---------|------------|----------|-------------|
| DL-10 | Contract 账本 FROZEN vs 正文 NOT FROZEN | C-X2-01 | Owner 双文件规则 |
| DL-11 | REPORT-B 列出不存在的 tracked L1 文件名 | gh contents 仅 9 files | 不得迁移引用 |
| DL-12 | REPORT-C mapping 未采用 + 主题偏差 | REPORT-H | Mapping authority 待指定 |
| DL-13 | 三套 L* taxonomy | README / V3 90 / REPORT-B | OD-03 为准；执行 OPEN |
| DL-14 | DEC 双轨撞号 | X2-06 | 双标；namespace policy OPEN |
| DL-15 | V3 CURRENT mirror 落后 Papers（DEC-049） | 状态头/时间戳 | Ledger 归属待裁 |
| DL-16 | untracked Design v1.1 被 D2/D3/D4 引用 | git log empty | OQ-GF-017 |
| DL-17 | 五项 V3 capability NOT IMPLEMENTED vs 本地 untracked 实现文件 | Contract §5.6.1 vs git status | REPORTED ≠ OBSERVED |
| DL-18 | options_region 设计 vs 生产 Resolver 零概念 | FACT-005/009 | 架构采用与否待裁 |
| DL-19 | 12,707 归属文档错误 | REPORT-K；OQ-GF-011 | 更正载体待裁 |
| DL-20 | absolute path 依赖 vs OD-05 NAS | GAP-007/008 | Data mode 实施 OPEN |
| DL-21 | D-048-1/2 hardening findings | Papers DEC-048 | pending_owner_decision |
| DL-22 | D-048-3 数据文件删除 ROOT CAUSE UNKNOWN | Papers CURRENT | Owner 排查 |
| DL-23 | Set B 未导入 | OQ-GF-013 | Owner 提供或豁免 |
| DL-24 | REPORT-G/H/I/K untracked | AITutorX git status | OD-06；admitted unknown |

---

## 3. Lineage / evidence gaps（必须保留）

| Gap ID | Gap | Blocks |
|--------|-----|--------|
| GAP-L1 | 大量源 md 无正文 lineage | 大规模 verified 迁移声明 |
| GAP-L2 | 双树血缘方向未知 | OQ-GF-006 |
| GAP-L3 | pre-git 首跑证据效力未裁 | OQ-GF-012 |
| GAP-L4 | 恢复前全量 hash 台账可能不存在 | OQ-GF-005 |
| GAP-L5 | 全量 source hash inventory 未建 | OQ-GF-008 |
| GAP-L6 | 图片 dangling / Step5 未做 | Material 贯穿完整性 |
| GAP-L7 | bytes 传输方式未裁 | V3 重算验证可执行性 |
| GAP-L8 | EB-008 外部验证 unavailable in repo | Admission Evidence Authority 主张强度 |

---

## 4. 71 / 87 / 166 / 177 disposition obligation（OD-18）

任何 AITutorX 文档引用上述数字时 **必须** 关联:

```text
number + semantic meaning + measurement source + current disposition status
```

禁止裸数字被读成「已 verified 可迁移」。

| Number | Meaning | Source reference | Disposition status |
|--------|---------|------------------|--------------------|
| 87 | Interface Scope manifests（回填后） | Contract；Step2 report | 已登记；非 admitted to AITutorX |
| 71 | IR ADMITTED docs/units 面 | Papers CURRENT；resolver IR | 已登记；非 Question 数 |
| 16 | Semantic Pending | 87−71 | Identity Available / Semantic Pending |
| 166 | Historical manifest asset scale | Papers | ≠ interface |
| 79 | v1 legacy | Papers | 隔离；禁自动入接口 |
| 177 | Guardian anchored files | Papers Guardian | 冻结基线锚叙事 |
| 356 | R50 baseline files | Papers | 269+87+0 |
| 12,707 | maintainess/PDF count | REPORT-K | 非 original |
| 38,893 | original PDF count | REPORT-K | 非 operational input |

---

## 5. Difference Ledger Non-Actions

- 不关闭 OQ-GF-007 / 001 / 002 / 004 / 011 / 018
- 不关闭 D-048-*
- 不改写 REPORT-A~K
- 不创建 admitted=true 记录
- 不把 DL 条目写成已修复

---

*Difference Ledger instance registered for audit. Source ledgers unchanged.*
