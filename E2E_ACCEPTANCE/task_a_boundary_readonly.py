"""Read-only: identify bare=1 questions + composite/multi-line split for Task A brief."""
from __future__ import annotations
import json, re
from pathlib import Path

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
# use v2 (current) for structure; option_integrity from frozen annotations is in v2
v2 = json.loads((OUT / "viewer_data_raw_v2.json").read_text(encoding="utf-8"))
frozen = json.loads((OUT / "FROZEN_EVIDENCE" / "viewer_data_raw.json").read_text(encoding="utf-8"))

# merge option_integrity if missing in v2
for subj, e in v2["subjects"].items():
    fqs = {q["unit_id"]: q for q in (frozen["subjects"].get(subj, {}).get("questions") or [])}
    for q in e.get("questions") or []:
        if not q.get("option_integrity"):
            q["option_integrity"] = (fqs.get(q["unit_id"]) or {}).get("option_integrity")

rows = []
for subj, e in v2["subjects"].items():
    for q in e.get("questions") or []:
        oi = q.get("option_integrity") or {}
        if oi.get("level") != "ANOMALY":
            continue
        # leaf_id vs unit_id for composite
        is_composite_sub = (q.get("leaf_id") != q.get("unit_id"))
        # line span of options
        line_sets = []
        for o in q.get("options_raw") or []:
            for lr in (o.get("line_refs") or []):
                # like P1L021
                m = re.search(r"L(\d+)", str(lr))
                if m:
                    line_sets.append(int(m.group(1)))
        uniq_lines = sorted(set(line_sets))
        rows.append({
            "subject": subj,
            "unit_id": q.get("unit_id"),
            "leaf_id": q.get("leaf_id"),
            "is_composite_sub": is_composite_sub,
            "n_shell": oi.get("n_shell"),
            "n_multi": oi.get("n_multilabel_line"),
            "n_options": oi.get("n_options"),
            "option_lines": uniq_lines,
            "n_option_lines": len(uniq_lines),
            "form": "single_line_multi_label" if len(uniq_lines) <= 1 else "cross_line",
            "shell_labels": [f["label"] for f in (oi.get("options") or []) if f.get("is_shell")],
            "sample_shell_preview": next(
                (f.get("text_preview") for f in (oi.get("options") or []) if f.get("is_shell")), None),
        })

n = len(rows)
n_comp = sum(1 for r in rows if r["is_composite_sub"])
n_single = sum(1 for r in rows if r["form"] == "single_line_multi_label")
n_cross = sum(1 for r in rows if r["form"] == "cross_line")
bare_dist = {}
for r in rows:
    k = r["n_shell"]
    bare_dist[k] = bare_dist.get(k, 0) + 1

bare1 = [r for r in rows if r["n_shell"] == 1]
print("affected", n, "composite_sub", n_comp, "single_line", n_single, "cross_line", n_cross)
print("bare dist", bare_dist)
print("bare=1 questions:")
for r in bare1:
    print(" ", r["subject"], r["unit_id"], "shell_labels", r["shell_labels"],
          "preview", r["sample_shell_preview"], "lines", r["option_lines"])

brief = {
    "task": "A — Resolver single-line multi-label / option content-span defect",
    "status": "NOT AUTHORIZED — brief only (read-only recording)",
    "premises_from_adjudication": {
        "P1_composite_propagation": {
            "n_composite_sub_questions": n_comp,
            "must_hold_invariants": [
                "root count",
                "ready / incomplete",
                "rejected (root scope, currently 62)",
                "D=29 decomposition surface",
                "composite leaf counts",
            ],
            "note": "option re-slice on composite leaves may shift gate decisions and root-scoped counts",
        },
        "P2_two_line_forms": {
            "single_line_multi_label": n_single,
            "cross_line": n_cross,
            "min_assertion_math_Q1": "A='1' B='2' C='\\pi' D='2\\pi'",
            "cross_line_assertion_needed": "e.g. math Q4 P1L021+P1L023, chem Q17 P1L123..129",
            "fix_scope": f"{n_single} + {n_cross} = {n} questions, not only single-line",
        },
        "P3_bare1_false_positive_risk": {
            "n_bare1": len(bare1),
            "questions": bare1,
            "requirement": "human confirm or explicit exclusion list before fix; "
                           "some 'shells' may be legitimately short options (e.g. A. 是 B. 否)",
        },
    },
    "assertion_style": {
        "pass_condition": "each option text == chars from after its label to before next label (content span)",
        "fail_condition": "empty-shell count decreases but content mis-attributed",
    },
    "ocr_boundary_remains": (
        "Hash green + OCR ledger match is COMPATIBLE with OCR content loss "
        "(e.g. chem Q23 PDF has 'D．稀硫酸与氢氧化钡溶液：' but md lost label+prefix). "
        "This boundary stays on the status board."
    ),
    "execution_order": [
        "1. list small-fix (declared_source_sha256 + OCR ledger note) — DONE",
        "2. authorize Task A with P1/P2/P3 boundaries",
        "3. before/after diff by content spans, not shell counts",
        "4. Task B formal product-chain E2E after A passes",
    ],
    "not_started": ["Resolver code change", "Task B"],
}
(OUT / "TASK_A_BOUNDARY_BRIEF.json").write_text(
    json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

# markdown
md = f"""# 任务 A 边界书（只读记录 · 未授权实施）

## 前提一：composite 传导面（{n_comp} 题）
修选项切分会改 leaf option 内容 → 可能改 gate → 影响 **root 作用域 rejected（当前 62）** 与 composite leaf 计数。
**不变量必须显式覆盖**：root / ready / incomplete / rejected(root) / D=29 / composite leaf 数。

## 前提二：两种行形态（{n_single} + {n_cross}）
- 单行多选项：{n_single}（最小断言 A='1' B='2' C='π' D='2π'）
- **跨行：{n_cross}**（如数学 Q4 = L021+L023；化学 Q17 = L123..129）— 需独立断言

## 前提三：bare=1 假阳性风险（{len(bare1)} 题）
| 科目 | unit | shell 标签 | 预览 | 行 |
|------|------|-----------|------|-----|
"""
for r in bare1:
    md += f"| {r['subject']} | {r['unit_id']} | {r['shell_labels']} | `{r['sample_shell_preview']}` | {r['option_lines']} |\n"
md += """
**要求**：修复前人工确认或写入显式排除清单——部分「空壳」可能是源文本本就极短的选项（如 `A. 是 B. 否`）。

## 断言口径
- **通过**：每选项 text =「该标签后 → 下一标签前」的内容区间
- **不通过**：空壳数下降但内容错切/吞并

## OCR 边界（保持挂在状态表）
哈希全绿 + ledger 全匹配 **兼容** OCR 内容丢失（化学 Q23：PDF 有 `D．稀硫酸…`，md 只剩方程式）。

## 执行顺序
1. ~~清单小修~~（已完成）
2. **等你正式授权任务 A**（含 P1/P2/P3）
3. 修复前后按内容区间 diff（不按空壳数）
4. 任务 A 通过后再独立授权任务 B

**本轮未改任何生产代码 / 冻结证据 / v2 数据。**
"""
(OUT / "TASK_A_BOUNDARY_BRIEF.md").write_text(md, encoding="utf-8")
print("wrote TASK_A_BOUNDARY_BRIEF.{json,md}")

# update status
st = OUT / "PROJECT_STATUS.md"
if st.exists():
    t = st.read_text(encoding="utf-8")
    if "任务 A 边界书" not in t:
        t += """
## 任务 A 边界（只读记录 · 待授权）
- P1 composite 传导面：不变量须含 root/ready/incomplete/rejected(root)/D=29/leaf 数
- P2 两形态：单行 {a} + 跨行 {b}，均需断言
- P3 bare=1 共 {c} 题：修复前人工确认/排除清单
- 断言 = 内容区间，不是空壳数
详见 `TASK_A_BOUNDARY_BRIEF.md`。**未启动实施。**
""".format(a=n_single, b=n_cross, c=len(bare1))
        st.write_text(t, encoding="utf-8")
print("status updated")
