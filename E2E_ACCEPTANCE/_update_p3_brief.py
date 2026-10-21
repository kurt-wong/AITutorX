from pathlib import Path
import json

OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")

# --- update JSON brief ---
jp = OUT / "TASK_A_BOUNDARY_BRIEF.json"
brief = json.loads(jp.read_text(encoding="utf-8"))
brief["premises_from_adjudication"]["P3_bare1_false_positive_risk"] = {
    "status": "RESOLVED",
    "n_bare1": 2,
    "split": {
        "exclude_from_task_A": {
            "unit": "化学 Q17",
            "reason": (
                "根因在标注层 manifest：声明了源中不存在的 label `H`"
                "（L125 `B. H: O: H` 电子式的 H 被当成选项标签）。"
                "正式 MD L123-129 选项标签完全正确（A/B/C/D）。"
                "Resolver 只遍历 manifest labels —— 只改 Resolver 修不了；"
                "若顺手修会改到标注/manifest 数据，越界。"
            ),
            "defect_class": "annotation_option_label_false_positive",
            "manifest_labels": ["A", "B", "H", "C", "D"],
            "md_labels_correct": ["A", "B", "C", "D"],
        },
        "in_task_A": {
            "unit": "英语 Q5-6",
            "reason": (
                "真·单行多选项（L43 一行两选项）+ composite（P1 传导面）。"
                "A 吞掉整行，B 空壳。bare=1 唯一有效样本。"
            ),
            "role": "bare=1 真阳性样本",
        },
    },
    "label_histogram_corpus": {
        "A": 183, "B": 183, "C": 182, "D": 174, "H": 1, "E": 1,
        "note": "超出 A–D 仅 2 个，均已定因：H=Q17 标注层；E=化学 Q20 P1.4-B Rule A",
    },
    "mechanical_assertion_added": (
        "修复后每个 unit 的 labels 必须恰为 A–D 的子集且无重复；"
        "Q17 的 ['A','B','H','C','D'] 会被此判据立即抓住"
    ),
}
brief["assertion_style"]["labels_must_be_A_to_D_subset"] = True
brief["assertion_style"]["reject_duplicate_or_out_of_range_labels"] = True
brief["explicit_exclusions"] = [
    {
        "unit": "化学 Q17",
        "defect_class": "annotation_option_label_false_positive",
        "owner": "annotation/manifest layer — NOT Task A",
    }
]
jp.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
print("updated JSON")

# --- update MD ---
md = (OUT / "TASK_A_BOUNDARY_BRIEF.md").read_text(encoding="utf-8")
# replace P3 section
import re
new_p3 = """## 前提三：bare=1 —— **已定**（1 真阳性 / 1 排除）

| 科目 | unit | shell | 处置 | 根因 |
|------|------|-------|------|------|
| **化学 Q17** | Q17 | H | **已排除，不进任务 A** | **标注层 manifest**：声明了源中不存在的 label `H`（L125 `B. H: O: H` 电子式的 H）；MD L123–129 标签正确为 A/B/C/D。Resolver 只遍历 manifest labels → 只改 Resolver 修不了，顺手修会越界改标注数据 |
| **英语 Q5-6** | Q5-6 | B | **保留，任务 A 真阳性** | 真·单行多选项（L43）+ composite（P1）；A 吞整行、B 空壳 |

**缺陷类目**：`annotation_option_label_false_positive`（Q17）——另案，不属 Resolver。

### 全语料标签直方图
`A:183  B:183  C:182  D:174  H:1  E:1`  
超出 A–D 仅 2 个，均已定因：`H`=Q17 标注层；`E`=化学 Q20 P1.4-B Rule A。

### P3 机械判据（任务 A 断言）
- 修复后每个 unit 的 `labels` **必须恰为 A–D 的子集且无重复**
- Q17 的 `['A','B','H','C','D']` 会被此判据立即抓住，避免被当成「选项缺陷」一起改
"""
# find P3 section and replace
pat = re.compile(r"## 前提三：.*?(?=\n## )", re.S)
if pat.search(md):
    md = pat.sub(new_p3 + "\n", md, count=1)
else:
    md = md.replace("## 断言口径", new_p3 + "\n## 断言口径")
# ensure assertion list mentions labels subset
if "labels 必须恰为 A–D" not in md.split("断言口径")[0]:
    md = md.replace(
        "- **不通过**：空壳数下降但内容错切/吞并",
        "- **不通过**：空壳数下降但内容错切/吞并\n- **附加**：labels 必须恰为 A–D 子集且无重复（抓 Q17 型标注假阳性）",
    )
md += """

## 本轮更新
- P3 定案：Q17 排除（`annotation_option_label_false_positive`）· Q5-6 保留
- 增补 labels ⊆ {A,B,C,D} 机械判据
- **仍未授权任务 A；未改生产/冻结/v2**
"""
(OUT / "TASK_A_BOUNDARY_BRIEF.md").write_text(md, encoding="utf-8")
print("updated MD")

st = OUT / "PROJECT_STATUS.md"
t = st.read_text(encoding="utf-8")
t = t.replace(
    "- P3 bare=1 共 2 题：修复前人工确认/排除清单",
    "- P3 **已定**：化学 Q17 **排除**（标注层假阳性 label=H）· 英语 Q5-6 **保留**（真阳性）",
)
if "annotation_option_label_false_positive" not in t:
    t += "\n- 标签越界仅 H/E 各 1，均已定因（Q17 标注层 / Q20 P1.4-B）；任务 A 断言含 labels ⊆ A–D\n"
st.write_text(t, encoding="utf-8")
print("status updated")
