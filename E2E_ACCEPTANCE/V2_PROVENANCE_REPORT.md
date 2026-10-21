# Viewer Gate Decision Provenance — COMPLETE

## 冻结保护
- FROZEN_EVIDENCE/ 未写入
- 05_V3_OUTPUT/*.v3.json 未修改
- 05_V3_OUTPUT/*.pdf.txt 已设只读 + SHA 记录
- protected files changed: **NONE**（V2_SHA256.json）

## 字段语义（v2）
| 字段 | 含义 |
|------|------|
| leaf_present | 结构事实：是否存在 compiled leaf |
| ir_status | 结构：ready / incomplete |
| gate_original | **仅当 Gate 真正执行**时非空；否则 null |
| gate_original_source | absent_no_leaf / absent_ir_incomplete_skipped / evaluate_replay_equivalent |
| gate_replay | 独立重放 evaluate()，单独记录 |
| replay_match | true / false / null |
| gate_display | 展示用；**null = 无决策**，绝不显示 rejected/approved |
| reason_display | 展示文案；不覆盖 gate_reasons_original |

**incomplete 不是合法 Gate 决策** — Gate service 对 semantic_status≠ready 的 unit 是 skip（不产 candidate）。

## 六情形验证
| 情形 | n | 结果 |
|------|---|------|
| C1 leaf + original decision | 227 | PASS |
| C2 no leaf + original | **0** | **UNVERIFIED**（当前路径无样本；零命中≠已验证） |
| C3 no leaf + no original | 57 | PASS |
| C4 replay == original | 227 | PASS |
| C5 replay != original | 0 | **UNVERIFIED**（当前路径无样本） |
| C6 replay error/missing | 0 | **UNVERIFIED**（当前路径无样本） |

**RAW 字段（stem/options/answer/labels）相对 FROZEN 差异 = 0**
**伪造决策 = NONE**
**VERDICT: COMPLETE**

## 版本化产物
- `viewer_data_raw_v2.json` / `data_v2.js`（新版本，不覆盖冻结基线）
- `V2_SHA256.json` 哈希清单
- `export_v2_gate_provenance.py` / `verify_v2_provenance.py`

## 未做（按禁令）
- 未改 Resolver / Producer / Gate Policy / Schema / P1.4-B
- 未修补/切分题干选项答案
- 未改冻结证据
- 未把重放冒充原始执行
- 未宣布九科 E2E / 正式产品链通过


## 裁定更正（Owner / DSH）
C2 / C5 / C6 **未验证**——当前路径没有相应样本。零命中不得记为 PASS。
C1 / C3 / C4 为当前路径实测样本（227 / 57 / 227）。

## 项目状态（非 COMPLETE 收口）
> Viewer 数据保真核验完成；已知选项结构缺陷待修复；正式产品链 E2E 待验证；九科人工验收尚未完成。

## 下一阶段（独立任务，本轮未启动）
- **任务 A**：Resolver 单行多选项缺陷修复 + 内容区间断言（A='1' B='2' C='π' D='2π'）+ 回归
- **任务 B**：正式产品链 E2E（TaskExecutor document_ingest → … → 前端），不以 Phase1 manifest Runner 代替
