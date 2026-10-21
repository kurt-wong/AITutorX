# 清理与绑定清单 —— 独立复核

> DSH 独立复核 Owner 已批准的两项清理。**只读**，未改动任何文件。
> 结论：**两项清理均成立；绑定清单的 9/9 是算出来的，不是写的常量。**

---

## 1. 旧版数据归档 —— ✅ 成立

```text
_ARCHIVE_v1_viewer_superseded/
   viewer_data.json            300,258   ← v1（曾被 _improve_options.py 修补过的那份）
   data.js                   1,006,790   ← v1 导出
   _improve_options.py           4,187   ← 回读 MD 补齐选项的脚本（事故源）
   _fix_q4_opts.py               2,565   ← 同上
   _build_viewer.py / _build_html.py / _build_raw_viewer.py
   export_viewer_data.py / export_raw_viewer_data.py
   ARCHIVE_MANIFEST.json         3,115   ← 先记 SHA 再移动 ✅
```

**根目录残留检查**：`viewer_data.json` / `data.js` / `_improve_options.py` / `_fix_q4_opts.py`
等 v1 文件**均已不在根目录** ✅（归档而非删除）

**引用检查**：

```html
index.html L95  <script src="vendor/katex/katex.min.js"></script>
index.html L96  <script src="data_v2.js"></script>      ← 只引 v2
index.html L97  <script src="app.js"></script>
```

✅ 无任何入口引用旧 `data.js` / `viewer_data.json`

**未动检查**：

```text
FROZEN_EVIDENCE/viewer_data_raw.json   1c2fce64e2e58025…   ← 与冻结时一致 ✅
viewer_data_raw_v2.json                6b6b406a4a218f47…   ← == V2_SHA256.json 声明 ✅
data_v2.js                             8162059a63affce7…   ← == V2_SHA256.json 声明 ✅
```

---

## 2. 证据绑定清单 —— ✅ 成立，且 9/9 是**算出来的**

我把清单里**每一个哈希全部独立重算**，并与声明值逐项比对：

```text
subjects: 9

recomputed hash matches (claim == actual):
   manifest        9/9
   preproc_md      9/9
   pdf             9/9
   pdf_txt         9/9
   v3_out          9/9
   owner_md        9/9
   declared_bind   9/9        ← manifest.declared_source_file 实际哈希 == 02 md 哈希

claims of sha_match=true  : 18   （被重算推翻：0）
claims of identical=true  : 9    （被重算推翻：0）
PROBLEMS: 0
```

⇒ **没有任何一项是把 `true` 写成常量。** 这正是本轮最值得确认的一点——
本项目此前多次出现"声明与事实不符"，而这份清单经受住了逐项重算。

**绑定链连贯性**（Owner 要求的"冻结 ≠ 初始正确"）：

```text
manifest → declared_source_file → 02 md → 03 owner_accepted
coherent chains: 9/9
```

✅ 验收包**内部绑定完整**。Owner 在清单里写的 `note` 措辞准确：
"Freeze prevents later mutation; does NOT prove initial correctness."

---

## 3. 两处非阻塞建议（不改变本轮结论）

**(a) `manifest` 项未登记 `declared_source_sha256`**

当前 `bindings.manifest` 只有 `path` / `sha256` / `declared_source_file`，
**没有记录 `declared_source_file` 的哈希**。虽然我已独立确认
「declared_source_file 实际哈希 == 02 md 哈希 == manifest 的 `source_content_sha256`」，
但清单本身没有把这条写成可核验字段。

建议补一行：

```json
"manifest": {
  "path": "...", "sha256": "...",
  "declared_source_file": "...",
  "declared_source_sha256": "934dec78…",      // 加这一行
  "declared_matches_actual": true
}
```

理由：我上一轮正是因为**没按 manifest 自述的 source_file 绑定**，才得出 138 条假不一致。
这条字段是防止同类错误的唯一机械防线。

**(b) 上游一环仍需 Papers-side 侧证**

清单证明的是**验收包内部绑定**（manifest ↔ md ↔ pdf ↔ v3 输出）。
它**不证明**上游「OCR/标注确实从该 PDF 产出了该 md」。
那一环的凭证在 `Papers/data/ocr_output_manifest.jsonl`（含 `source_sha256` / `pages` / `written_at`），
我此前已核 9/9 相符——建议在清单 `note` 里点明"上游凭证在 ledger"，避免读者误以为清单已覆盖全链。

---

## 4. C2/C5/C6 口径更正 —— ✅ 已确认

MIMO 声明已改为 `UNVERIFIED`。这与我的核查结论一致：

```text
C2 (无 leaf + 有原始决策) = 0 条   ← 本路径不存在该样本
C5 (重放不一致)          = 0 条
C6 (重放失败)            = 0 条
```

根因：Phase 1 对 `semantic_status ≠ ready` 的单元 `status="skipped"`、不产 candidate、不产 decision。
**零命中 ≠ 通过**，措辞已正确。

---

## 5. 状态确认（与 Owner 一致）

```text
Viewer 数据保真核验完成；已知选项结构缺陷待修复；正式产品链 E2E 待验证；九科人工验收尚未完成。

Viewer 数据保真        : ✅ 完成（含 Gate 决策来源分层）
证据归档与绑定清单      : ✅ 完成，独立重算 0 问题
C1/C3/C4              : 当前路径实测（227 / 57 / 227）
C2/C5/C6              : UNVERIFIED（无样本）
选项结构缺陷           : 97/284 题，待独立 Resolver 任务
正式产品链 E2E         : 未证明
```

**下一阶段任务 A / B 已记录，等你授权再开。我这边无待办、不动作。**

---

## 6. 本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `_verify_binding_inventory2.py` | 绑定清单逐项重算（computed vs claimed） |
| `_verify_v2_provenance.py` | 上一轮：v2 六情形 + 反伪造断言 |
| `Docs/60_REPORTS/V2-GATE-PROVENANCE-VERIFICATION.md` | 上一轮：v2 独立复核 |
