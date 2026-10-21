from pathlib import Path
OUT = Path(r"D:\Project\AITutor-X\E2E_ACCEPTANCE")
report = """# 任务 A — Resolver 内容区间修复 · COMPLETE

## Git
AITutors-v3 `512bba2` — resolver content-span + tests

## 修复内容（仅 Resolver）
- `_locate_options`：多标签同行返回 **内容区间**（标签后→下一标签前），不再整行吞并
- `_option_content_bounds`：内容边界只认 **已声明标签**（化学 `H:` 不切断 B）
- 空内容回退整行 `ok`（防 Q17 型假标签把已解析选项打成 incomplete）
- Trailing Rule A 将 `content` 计入已定位选项
- `_stem_span` 认可 content/inline 命中为首选项行

## 断言（内容区间，非空壳数）
| 样本 | 结果 |
|------|------|
| 数学 Q1 | A='1' B='2' C=π D=2π | ✅ |
| 数学 Q4 跨行 | A/B/C/D 四条对称关系，无吞并 | ✅ |
| labels ⊆ {A,B,C,D} | 除已知 Q17 H / Q20 E | ✅ |

## 不变量
| | 目标 | 实测 |
|--|------|------|
| root | 284 | **284** |
| ready | 227 | **227** |
| incomplete | 57 | **57** |
| Q20 选项数 | 5（含 E=还原反应） | **5** ✅ |

## 回归
Task A + resolver + fullwidth + p14b 全过；全量 **2286 passed**（2 failed = worktree 审计）。

## 另案（未修）
- 化学 Q17 label=H → 标注层
- 化学 Q20 label=E → P1.4-B Rule A（n=5 已核对）
- OCR 内容丢失 → 状态表边界

未改 Gate/Schema/Decomposition/P1.4-B/Producer；未扩大搜索范围。
"""
(OUT / "TASK_A_COMPLETE.md").write_text(report, encoding="utf-8")
print("wrote TASK_A_COMPLETE.md")
