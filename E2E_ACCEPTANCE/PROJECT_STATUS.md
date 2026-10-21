# 项目状态（本轮收口）

Viewer 数据保真核验完成；已知选项结构缺陷待修复；正式产品链 E2E 待验证；九科人工验收尚未完成。

## 本轮完成
1. 旧版 v1 viewer 数据归档 → `_ARCHIVE_v1_viewer_superseded/`（含哈希清单，非删除）
2. 证据绑定清单 → `EVIDENCE_BINDING_INVENTORY.json`
   （manifest declared source_file ↔ 实际路径 ↔ SHA256 ↔ v3 输入/输出）
3. C2/C5/C6 更正为 **UNVERIFIED（无样本）**

## 明确未做
- 未修 Resolver / 未跑正式产品链 E2E / 未宣布九科验收通过
- 未改 FROZEN_EVIDENCE / v2 数据

## 清单小修订（本轮）
- `EVIDENCE_BINDING_INVENTORY.json` 增加 `declared_source_sha256`：
  `source_content_sha256` / `declared_source_file_sha256` / `packaged_md_sha256` 与三项 checks
- 增加 `evidence_scope`：本清单只证包内绑定；上游 PDF↔OCR 由 `Papers/data/ocr_output_manifest.jsonl` 凭证；
  **哈希匹配 ≠ OCR 内容正确 ≠ 正式产品链已验证**
- 未重导出题目数据；未改 FROZEN / v2 基线；**未启动任务 A / B**

## 任务 A 边界（只读记录 · 待授权）
- P1 composite 传导面：不变量须含 root/ready/incomplete/rejected(root)/D=29/leaf 数
- P2 两形态：单行 73 + 跨行 24，均需断言
- P3 **已定**：化学 Q17 **排除**（标注层假阳性 label=H）· 英语 Q5-6 **保留**（真阳性）
- 断言 = 内容区间，不是空壳数
详见 `TASK_A_BOUNDARY_BRIEF.md`。**未启动实施。**

- 标签越界仅 H/E 各 1，均已定因（Q17 标注层 / Q20 P1.4-B）；任务 A 断言含 labels ⊆ A–D
