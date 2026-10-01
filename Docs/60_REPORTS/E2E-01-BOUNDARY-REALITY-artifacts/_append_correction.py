from pathlib import Path
from datetime import datetime, timezone

p = Path(r"D:\Project\AITutor-X\Docs\60_REPORTS\E2E-01-BOUNDARY-REALITY-VERIFICATION.md")
text = p.read_text(encoding="utf-8")

gov = """
---
**治理元数据（2026-10-01 Correction v1.1 起生效）**
- **Readers**: Owner / DSH / Migration Gate 评估者
- **Disposition**: ACTIVE — Boundary Reality evidence；**不得单独作为 A8 或 Migration 授权依据**
- **Supersedes**: 无（本文为首版）
- **Superseded_by**: 无（v1.1 Correction Record 与本文同文件，见文末）
- **Authority level**: C — Informative Task Report（非 Gate Report；CLOSED/ACTIVE 等状态词不适用 Gate 语义）
- **Security**: 无凭据入库；DATABASE_URL 不写入 artifact
---
"""

correction = """

---

## Correction Record v1.1（2026-10-01，add-only）

> 本节为 **add-only 追加**。历史正文不回改。凡与正文冲突，**以本节为准**。
> 触发：DSH 对抗复核 + Owner 裁决——E2E-01 执行有效，但报告不得作为 A8/Migration 决策依据，须先修正证据语义。

### 约束（本修正零触碰）

仅改报告与治理元数据。未修改 runner / boundary / Gate / Admission / schema / Contract / Papers。

### H-1 字母体系更正（必读）

OD-E2E-01 类别定义为：

| 字母 | 含义 |
|---|---|
| **A** | PASS |
| **B** | **Producer gap** |
| **C** | **Consumer gap** |
| **D** | Unauthorized semantic |

正文 §6/§7 曾误用 `C=Producer / B=Consumer`。**作废正文旧映射。**

更正后归因：

| 事实 | 更正归因 |
|---|---|
| 85 件 `MISSING_IDENTITY`（缺 `source_content_sha256`） | **B — Producer gap** |
| M1–M5 接口实现 98 tests 通过、fail-closed 四路径成立 | **A — PASS** |
| Consumer 侧违反已冻结 M1–M5 契约 | 本轮**未发现**（故 C 无实体） |
| `M1–M5` 链与 `GateService/AdmissionService` 链不统一 | **D — Unauthorized semantic**（A8，STOP） |

### H-2 87 件双因子拆分（禁止笼统归 D）

正文将 87 件 `VERIFIED + semantic_pending` 整体挂在 D/A8 下，**易误导**为「解决 A8 即可 Admission」。实际为**两个独立因子**：

| 因子 | 事实 | 归因 |
|---|---|---|
| F1 Identity | 87/87 `identity_state=VERIFIED`，`interface_scope_accepted`，`identity_version==2`，`mismatches=[]` | **A — PASS**（M1–M5 边界成立） |
| F2 IR artifact absence | 默认路径无 resolver IR ⇒ `semantic_state=PENDING` | **B — Producer / upstream artifact readiness gap**（输入未满足后续语义就绪条件） |
| F3 Chain seam | 即便 IR 就绪，`runner_b2` 链与 GateService/AdmissionService 链仍不统一 | **D — Unauthorized semantic**（A8，独立于 F2，STOP） |

**禁止推论**：`F2 解决 ⇒ 可进 Admission`。F3 不因 F2 消失而消失。

### H-3 因果表达降级

正文 §3.3「**分裂结构 85/87 未变。** D4 M1–M5 冻结 + Contract v0.3 未改变 boundary 拒绝面」含因果推断，证据不足（`3e2f9bb→39840ff` 为 91 files / 17781 insertions 级差异）。

**更正为纯事实陈述**：

> E2E-01 当场重跑结果（85 MISSING_IDENTITY / 87 VERIFIED+PENDING）与 X2.7 历史运行的 85/87 分裂结构一致。

不声明「因 D4 / v0.3 而不变」。

### M-4 `98 passed` 补可复现四件套

| 项 | 值 |
|---|---|
| command | `cd AITutors-v3/backend && python -m pytest tests/test_identity_interface_freeze.py tests/test_identity_gate.py tests/test_identity_verifier.py tests/test_manifest_identity.py tests/test_raw_bytes_identity.py tests/test_ir_identity.py -q` |
| environment | Windows 11 / Python 3.12.9（系统 `python`，非 MIMO_PYTHON） |
| scope | 仅 M1–M5 identity 测试文件（6 文件）；**非全量 suite** |
| result | `98 passed, 1 warning`（collect-only 亦为 98） |

### M-5 composite 计数口径更正

| 口径 | `composite_question` 条数 |
|---|---|
| **Ocr-markdown 分片** | **673** |
| **全量 eligible 语料（172 manifests）** | **729**（Ocr-markdown 673 + data 31 + tests 25） |

正文 §4 行「全库 673 条 type」**口径错误**，应为「Ocr-markdown 分片 673；全量 729」。

### M-6 mismatch 产物来源说明

正文「未新增 fixture 文件」表述不精确。准确事实：

- **未修改** Papers Producer 数据；
- **未新增** fixture 文件作为 Producer corpus 成员；
- `30-mismatch-combo/` 为 **Consumer 侧受控 negative 组合**（真实 manifest + 他源 raw bytes），按 OD 允许的「真实 manifest + 不匹配组合」执行，**不是** Producer corpus 产物，**不进入** 172 计数；
- 既有 `negB`/`negC` 为历史 negative asset 复用，非本轮新建。

### 修正后五类归因终表（取代正文 §7）

| 类型 | 状态 | 后续 |
|---|---|---|
| **A — PASS** | 87 件 identity VERIFIED；fail-closed 四路径成立；identity 面 98 tests | 保留证据 |
| **B — Producer gap** | 85 件缺 `source_content_sha256`；87 件路径上 IR artifact 缺席（F2）；词表 `andalone_question`×1 | 回 Producer 单独裁决 |
| **C — Consumer gap** | 本轮未发现违反已冻结 M1–M5 的 Consumer 实现 | — |
| **D — Unauthorized semantic** | F3 链断点（A8）；M5 VERIFIED+PENDING=BLOCK 硬化语义 | **STOP**，待 Owner |
| Contract gap | 不在本轮展开（不扩审） | 不处理 |

### 对后续决策的效力

| 问题 | 本报告可否支撑 |
|---|---|
| M1–M5 边界是否在真实 Producer 产物上成立 | **可**（A 面） |
| Producer 是否满足 identity Contract | **可**（B 面，85 件否） |
| 是否授权 A8 接线 | **不可** — 须另开 Owner Decision |
| 是否进入 Migration | **不可** — 须 A8 之后另裁 |

**当前闸门保持**：Migration NOT AUTHORIZED · A8 NOT AUTHORIZED · N-values NOT IMPLEMENTED · multi-blank BLOCKED · R-5 NOT AUTHORIZED。

---

*v1.1 Correction Record ends. Original body left intact above.*
"""

# insert governance metadata after the evidence-standard blockquote
marker = "> 证据标准："
idx = text.find(marker)
if idx == -1:
    raise SystemExit("marker not found")
# find end of that blockquote paragraph (next blank line after marker line)
line_end = text.find("\n", idx)
# insert gov after the first --- following header
first_hr = text.find("\n---\n", line_end)
if first_hr == -1:
    raise SystemExit("hr not found")
insert_at = first_hr + len("\n---\n")
text = text[:insert_at] + gov + text[insert_at:]

if "Correction Record v1.1" not in text:
    text = text.rstrip() + "\n" + correction

p.write_text(text, encoding="utf-8")
print("updated", p, "bytes", p.stat().st_size)
