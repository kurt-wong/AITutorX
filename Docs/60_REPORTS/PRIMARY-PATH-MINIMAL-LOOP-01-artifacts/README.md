# PRIMARY-PATH-MINIMAL-LOOP-01 — Artifacts

```text
Document Type : Artifacts Index (non-authority; 附属物索引)
supersedes    : —
superseded_by : —
readers       : Owner；MIMO CODE；后续 audit 引用者
Status        : OPEN
Date          : 2026-09-28
Parent report : ../PRIMARY-PATH-MINIMAL-LOOP-01.md（已跟踪）
Provenance    : UNTRACKED ASSET DISPOSITION（UNTRACKED-ASSET-DISPOSITION-LIST-01.md §2.2，group G2）
Authority     : 本目录不含权威结论，仅承载执行证据；结论见 parent report 与 20- 结果文件
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

---

## 1. 本目录内容

| 文件 | 说明 |
|---|---|
| `20-minimal-loop-probe-result.md` | 探针结果（READ-ONLY validation 输出），日期 2026-09-27 |
| `30-minimal-loop-probe.py` | 产生上述结果的探针脚本 |

原位置：`Docs/60_REPORTS/PRIMARY-PATH-MINIMAL-LOOP-PROBE.py` 与 `...-PROBE-RESULT.md`（均未跟踪）。
按 `UNTRACKED-ASSET-DISPOSITION-LIST-01.md` 的建议 (B)，两者作为同一证据 bundle 一并移入本目录；
编号沿用本仓既有 `X2.7-INT-FULL-01-artifacts/` 惯例（产物在前、脚本在末位）。

---

## 2. 该探针做了什么（据其 self-documented docstring）

```text
READ-ONLY. Uses the scratch copy of the V3 backend; the real repo is untouched.
No DB, no LLM: manifest -> payload -> ResolvedRun -> IR -> Compiler -> gate.evaluate.
```

结果文件记录：53 units / 1045 source lines，
`STRICT_AUTO_TYPES = {single_choice, multiple_choice, true_false}`。

---

## 3. ⚠️ 可复现性缺口（登记，非缺陷修补）

```text
30-minimal-loop-probe.py:9
    BACKEND = Path(r"D:\Project\AITutor-X\_audit_scratch\backend")

实测（2026-09-28）：D:\Project\AITutor-X\_audit_scratch  →  不存在
```

⇒ **脚本当前不可独立复现。** 原因不是探针逻辑错误，而是它刻意在**隔离副本**上运行
（这正是其 docstring 声明的「the real repo is untouched」），而该副本事后已被移除。

**为何仍保留本目录**：脚本 + 结果 + 执行证明三者同在，才构成一次审查证据的完整 bundle。
仅有脚本（不可运行）或仅有结果（无产生方式）都会削弱证据价值。故按处置清单建议
**不得将两者分离**。

**副作用（已核，正面）**：该绝对路径恰好**印证**了结果的独立性主张 ——
即探针确实跑在 scratch 副本、未触碰真实仓库。

本项属 `REPORT-I §4 GAP-008`（绝对路径 / path≠identity）的同类实例，
**未在 REPORT-I 中登记**；建议在后续 P0 裁决时一并纳入。

---

## 4. 边界声明

```text
未修改 20- 结果文件任何内容（内容逐字节保持原样，仅路径变更）  ✅
未修改 30- 脚本任何内容（含其失效的绝对路径，保留原样）        ✅
本目录不构成任何权威结论                                      ✅
未修复可复现性缺口（§3 仅登记）                                ✅
```

*Prepared 2026-09-28 by DSH（治理收口角色）。Status: OPEN。*
