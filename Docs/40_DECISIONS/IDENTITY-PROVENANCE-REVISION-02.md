# IDENTITY-PROVENANCE-REVISION-02

```text
Document Type : Revision / Withdrawal Record（撤回记录 + 留存证据 + Accepted Corrections）
supersedes    : IDENTITY-PROVENANCE-REVISION-01.md（其 §5.2 首选方向被本文件撤回；其余经本文件复核后部分保留）
superseded_by : —
readers       : 实现方（MIMO CODE）；Owner；后续任何引用 IDENTITY-* / PRODUCER-* 文档者
Status        : OPEN
Decision State: APPROVED WITH CONDITIONS（撤回记录本身已完成）
Blocking      : NONE（Blocking-2 于 2026-09-27T09:13:28Z 实测 RESOLVED）
Revision      : rev.3 — Blocking-2 RESOLVED；rev.2 新增 §6 Accepted Corrections
Date          : 2026-09-27
Authority     : OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md（对本文件涉及的 role/provider 与 identity domain 裁决）
Security      : Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env
```

**本文件性质**：**审计轨迹**。逐条记录「撤回了什么 / 依据什么 / 谁判定」，并**同时**记录
对抗性审查方自身的过度纠正 —— 使轨迹反映**两个方向**的偏差，而非只把原文档改得像一直是对的。

**判定标记**：

```text
WITHDRAWN      原结论被证伪，不得再被引用
CORRECTED      原结论方向保留，但表述/严重度/范围被修正
RETAINED       经独立复核成立，保留
REVIEW-ERROR   对抗性审查方自身的错误，一并入账
```

---

## 1. 依据的审查批次

本记录基于**三份独立对抗性审查**（架构推理 / 一致性缺口 / 计划事实核验）+ **一份外部独立复核**
（MIMO CODE，对架构视角的逐条复算）。共同结论：

```text
诊断内核成立；严重度模型与整改方案错误；本批次不应冻结。
```

---

## 2. 撤回清单

### W-1 `WITHDRAWN` — 「跨文档身份塌缩已经发生 / 可数据损坏形态」

| 项 | 内容 |
|---|---|
| 原位置 | `IDENTITY-DOMAIN-DECISION-02.md` §5.2.2；`IDENTITY-PROVENANCE-REVISION-01.md` §6.2 |
| 原表述 | 「两份内容相同的不同文档，第二次写入会静默复用第一份的 version 行」；「**真实身份损坏**，不是标注问题」；标为 `[FACT]`、列为**最高严重度** |
| 撤回理由 | **代数上不可实例化**：`le_hash = f(original_sha256)`（`runner.py:74,78,86`），而 `create_document` 以 `original_sha256` 幂等收敛（`source_repository.py:41-62`）⇒ 同内容 ⇒ 同 Document ⇒ 同 `document_id`。「两份内容相同的**不同**文档」不存在 |
| 判定者 | 架构审查（提出）＋ MIMO CODE（独立复算，确认成立）＋ 本文件作者（自行复核） |
| **改为** | `future risk under changed uniqueness assumptions` —— 即：`_version_by_le` 缺 document 过滤（`source_repository.py:128-138`）是**真实代码缺陷**；其**当前无害**由 `uq_documents_original_sha256`（另一张表的约束）**意外**提供；**若 `original_sha256` 改为不再决定 document 的域，该缺陷即被暴露**。这是**前瞻性风险**，不是已发生的损坏 |
| 连带撤回 | **Q4 探针作废**（`PLAN-01 §0.1.2`）：`v1.document_id <> v2.document_id AND hash 相等` 该 join **恒空**，作为 DB 探针**无信息量**、为**永久假阴性** |

### W-2 `WITHDRAWN` — 「Primary Path 必须经过 SealService / Seal ingestion boundary」

| 项 | 内容 |
|---|---|
| 原位置 | `PRODUCER-PROVENANCE-DECISION-01.md` §4（PP-INT-1..3）；`IDENTITY-PROVENANCE-REVISION-01.md` §1–§3 |
| 原表述 | 「所有进入系统的 SourceVersion 必须经 `SealService.seal_document()`」；并据此提出「放宽 85 号 §5 边界」 |
| 撤回理由 | **过度推断**。Owner 裁决：Seal **不进入 Semantic Path**；Primary Path 不新增 Seal Pipeline；85 号 §5 边界**无需放宽** |
| 判定者 | **Owner**（本批次任务指令明确撤回） |
| **改为** | 三者独立：`Producer Identity` + `V3 Identity Layer` + `Semantic Consumer`。真缺陷是**身份创建权归属**（`runner.py` 自行构造 Source Identity），**不是缺少一个 Seal stage** |
| 附带撤回 | `[REVIEW-ERROR]` **「Identity Flow / Semantic Flow」双流分类**：该词汇 **Frozen Spec 中不存在**，本批次却标为「权威表述」，违反 `AGENTS.md`「Agent 自写的 Frozen/Authority 不自动获得权威」。且 REVISION-01 自相矛盾：§1.2 把 `seal` 放进 Identity Flow，§1.1 又说 Primary Path 不新增 Seal stage。**该分类撤回**，仅保留「身份创建权归属」这一 Spec 可支撑的表述 |

### W-3 `WITHDRAWN` — 「`ocr_ppsv3` 是唯一诚实映射」

| 项 | 内容 |
|---|---|
| 原位置 | `IDENTITY-PROVENANCE-REVISION-01.md` §5.2.1；`PLAN-01` §0.2.1 |
| 原表述 | 「复用 `ocr_ppsv3 ⟺ ppsv3`」是「唯一不需要改 Spec 的**诚实**取值」 |
| 撤回理由 | ① `ocr_ppsv3` 字面断言 L1 来自 ppsv3 的 **OCR**，而 Primary Path 产物是结构恢复＋语义标注 → **provenance 失真**，与本批次要修的缺陷同类；② `10_Data_Model.md:150-153` 明写「**独立引擎必须独立身份，防 identity 漂移**」，复用即断言两者共享身份；③ 复用后 Primary Path 行与 cloud-OCR seal 行**不可区分**，摧毁本批次自己的判别式；④ 静默**重释冻结枚举值**，比老实 errata 更糟 |
| 判定者 | 架构审查 ＋ 计划事实核验（F8c）＋ MIMO CODE（确认成立） |
| **改为** | **errata 新增** `role = preprocessing` / `provider = preprocessing`（见 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md` Decision 1） |
| 留痕 | 本批次文档 **自己写过反驳**：`PRODUCER-PROVENANCE-DECISION-01.md:157,165-167`「丢失「semantic preprocessing ≠ raw OCR」区分」。撤回时**忽略了自己已写下的反证** |

### W-4 `CORRECTED` — 「Track A/B SourceVersion sharing 是设计意图」

| 项 | 内容 |
|---|---|
| 原位置 | `IDENTITY-DOMAIN-DECISION-02.md` §5.2 |
| 原表述 | 同文档 Track A/B 复用 SourceVersion「属设计意图」/「完全自洽」 |
| 修正理由 | 复用**客观上无害**（两者内容逐字节相同），但**无证据**证明共享 SourceVersion 是设计预期。`runner.py:132`（Track A）与 `:189`（Track B）传**相同** `source_lines`/`source_path`，撞全局 UNIQUE 后 ON CONFLICT 收敛 —— 这是**撞在约束上的幂等收敛** |
| 判定者 | MIMO CODE（提出补正，含精确行号）＋ 本文件作者（复核行号确认） |
| **改为** | `observed idempotent convergence`（碰巧无害），**不是** `by design` |

### W-5 `WITHDRAWN` — 「`UNIQUE(original_sha256)` 失效」

| 项 | 内容 |
|---|---|
| 原位置 | `IDENTITY-DOMAIN-DECISION-02.md` §5.2（M3） |
| 原表述 | 同一 artifact 两条写路径算法不同 ⇒ `UNIQUE(original_sha256)` **失效** |
| 撤回理由 | 该约束**是活的**（`models/source.py:32-34` 的 `uq_documents_original_sha256`；migration `0006:29-33`）。更严重的是：本批次所引 `30_Task_LLM_Safety.md:400` 的**下一行 `:401`** 就写着「`documents` 层 `UNIQUE(original_sha256)` 只保证一个原始文件一个主档」——**引了该段却只读后半句** |
| 判定者 | 一致性审查 ＋ 本文件作者（复核约束与 Spec 行） |
| **改为** | 两条写路径**确实算法不同**（真实），但后果是**同一内容可能产生两个 Document**（当且仅当两条路径的 I-1 域不同），**不是约束失效** |

### W-6 `WITHDRAWN` — 「sealed 后禁 UPDATE ⇒ 不可就地修正」（对 `source_meta`）

| 项 | 内容 |
|---|---|
| 原位置 | `IDENTITY-PROVENANCE-REVISION-01.md` §7；`PLAN-01` §3.1/§6.1 |
| 原表述 | 「`sealed` 后禁 UPDATE ⇒ 已 sealed 行的 `le_hash` 不可就地修正」；并把 producer metadata 放入 `source_meta`（作为「零 DDL」理由） |
| 撤回理由 | 对 `source_meta` **为假**：`task/executor.py:258-270` **直接 ORM 赋值并 commit**，绕过 `source_repository.py:148-151` 的 sealed 守卫。且 `dict(sv.source_meta or {})` 会把 NULL 变非 NULL —— 亦摧毁本批次赖以判别的「`source_meta` IS NULL」 |
| 判定者 | 一致性审查（U-J）＋ 计划事实核验（F2b/F10a）＋ MIMO CODE（确认成立）＋ 本文件作者（读 `executor.py` 确认） |
| **改为** | 「**sealed 不可变是列级的，不是行级的**」：`body_text`/`page_count` 有守卫与测试；`source_meta` 无。⇒ `producer metadata` 改放**独立表**（Owner Decision 3） |
| 附带留存 | 该缺陷**本身保留为有效缺陷**（见 §3 R-3） |

### W-7 `CORRECTED` — 「`plan` 的 Owner 示例 = DB 行」⇒「矛盾」

| 项 | 内容 |
|---|---|
| 原位置 | `PLAN-01` §0.2 |
| 原表述 | 「保持 Spec 原语义」与「不新增 role」在当前枚举下**不可同时满足**（宣布为 Owner 指令的内部矛盾） |
| 修正理由 | 该示例含 `ingestion: {service, version}` 块 —— **不是 `document_source_versions` 的列**；`provider="papers"` 亦不在 V3 枚举内。**这两点恰好说明它是 provenance 层图示，不是 DB 行。** 按 DB 行读它，才制造出「矛盾」 |
| 判定者 | 架构审查（R4）＋ MIMO CODE（确认成立） |
| **改为** | Owner 选择 **errata**（Decision 1），因此**矛盾自动消解**：语义取「产出 L1 的引擎」，并**如实新增** role。**「矛盾」这一提法撤回** |
| 附带 `[REVIEW-ERROR]` | 计划事实核验 F8(b) 据此推断「**该 #1 阻塞可能是制造的**」。归因需更正：示例**确实来自 Owner 对话指令**，作者转录忠实；审查方无法定位，是因为**裁决原文当时未落盘**（该缺口已由 Decision 4 消除） |

### W-8 `WITHDRAWN` — `[FACT]` 标签滥用与归因错误（共 6 处）

| 位置 | 问题 | 处置 |
|---|---|---|
| `REVISION-01:290` | 「这是**真实身份损坏**，不是标注问题」——**无任何标签**，且依 W-1 为假 | 撤回 |
| `REVISION-01:164` | 「实际存在的四个域（`[FACT]`）」——建模选择标为事实 | 改 `[ANALYSIS]` |
| `REVISION-01:198` | 「I-0 与 I-2 **结构上**不可能相等（`[FACT]`）」——**伪全称**（UTF-8/LF/无尾换行时往返字节相同） | 撤回该全称，改为「在有 BOM/CRLF/尾随换行时不等」 |
| `REVISION-01:178`/`:242`/`:302` | 可达性依赖的论断标为 `[FACT]` | 降为 `[ANALYSIS]`，并附可达性条件 |
| `PROVENANCE-01:148` | 「用 **Owner 的话**」引用一句，同一句在 `DECISION-02:43-44` 中被列为**作者自己的**诊断结论 | 撤回该归因（归因本身未落盘，见 Decision 4） |
| `PLAN-01:36` | `[FACT]` 标注的实为论证，且同节 `:45-46` 自行降级 | 改 `[ANALYSIS]` |

### W-9 `CORRECTED` — 自授权威（**本批次最严重的程序性错误**）

| 项 | 内容 |
|---|---|
| 原位置 | `PLAN-01` §8（`:408-424`） |
| 原表述 | 七处 `✅ APPROVED` / `🟡 APPROVED WITH REFINEMENT`，其中 **`D-ID-3`（作者自己的推荐）、`D-PP-2`、`D-PP-4`** 并无 Owner 裁决记录 |
| 修正理由 | 同一文件 `:461` 写「不含 `[OWNER DECISION]`」、`:442` 写「未产生任何 `[OWNER DECISION]`」。**一边声明无裁决，一边造了七处裁决。** 实质是把 Owner 的**裁决汇总表**篡改为作者的**完成度清单** |
| 归因更正 | `[REVIEW-ERROR]` 一致性审查称 `APPROVED` 为「非法状态词」。**该词是 Owner 在上轮表格中使用的**，且不在 `DOC-GOV:225-229` 禁用表内。真错不是造词，是**把 Owner 清单改造成门禁表并塞入自己的项** |
| **改为** | 状态一律引用 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md`；未决项标 `OPEN`；作者建议标 `[ANALYSIS]`，**不得**使用 Owner 裁决标记 |

### W-10 `WITHDRAWN` — 其他被证伪的技术断言（合并登记）

| # | 原表述 | 撤回理由 |
|---|---|---|
| a | 「`SealService` **到不了** `_version_by_le`」 | **并发路径可达**：并发 seal 同文档时两 session 均通过 `:108` 前置检查，输家 INSERT 冲突 ⇒ 落到 `:118` re-read。原表述把「顺序路径不触达」误写为「路径不可达」 |
| b | 「`file_sha → body_text_sha256` 是**零语义风险**」 | `file_sha` 是 `le_hash` 的**输入**（`runner.py:86`）；且 `:78` 写入 `original_sha256` 的**值不变** ⇒ 改名**不修** M2/M3 |
| c | 「现有测试 `_create_source_records` **全 4 处**引用、**函数体从未执行**」 | 实为 **6 处 / 4 文件**；`test_real_producer_activation.py:217-280` 以 `gate="PASS"` 断言该函数**被调用**，`test_consumer_boundary_closure.py:183-203` 亦进入函数体。**窄结论仍成立**（无测试跑完持久化路径、无测试断言 consumer 的 `role`/`provider`/`original_sha256`/`le_hash`），但**绝对化表述为假** |
| d | 「`role` 改动**不**破坏 active-source 选择逻辑」（称「风险收窄的实证」） | **反了**：`documents.py:224-232` 以 `.order_by(role).limit(1)` 选版本，`documents.py:129-133` 亦按 role 排序；`role` 是**活选择器**，经 `api/schemas.py:22-32` 暴露 |
| e | 「Query 恒返回 0」（对 Owner 原查询的失败机制） | **机制错**：PostgreSQL 会**报错**（`relation "source_versions" does not exist`）。硬错误是 fail-loud，不是静默误读。**「拒跑该查询」的纪律正确，理由需更正** |
| f | object key 只有**两种**形式 | 实为**三种**：`import_service.py:70-76` 写 `data/imports/<sha>.<ext>`。且 `seal.py:88` 的 `raw:<sha>` 在**生产几乎从不写入**（`seal.py:85-86` 仅在未命中时执行）。另有第三写入者 `p32_enforcement_experiment.py:41` 写 `obj/<uuid>.pdf` |
| g | 「`DocumentActiveSource` 零使用」的**举证** | 结论成立，但举证不实：migration 字符串与 `tests/test_models_schema.py:16` 亦有命中，非「仅定义与 `__init__`」 |
| h | 「`artifact_kind` 在 §3.1 说『改回闭集值』」 | 取值**未点名**；`runner.py:89`/`runner_b2.py:337` 现用 `"markdown"`（不在闭集 `original_binary/raw_l1/canonical_l1`） |
| i | `D-PP-8` / `D-ID-2-a/b/c` / `Step 0–6` / `Gate 2` / `开工门禁（Gate）` / `Primary Path Reference Run` | **自创编号与机制**，违反 Owner 立下的 NO-GO（`MIMO…PREP-01:244`「禁止新建编号体系」），而同一文档 `:441` 声明「未创建任何新治理机制」 |
| j | 「§8 的 migration 编号 0012 已定」 | 表述为既成事实，实为**依赖 D-ID-2-b + DB 事实 + Errata 批准**的条件项 |

---

## 3. 保留清单（**不得删除**）

### R-1 `RETAINED` — Identity 与 Execution Identity 分离

```text
content identity          vs          execution identity
```

**有效架构洞察**。依据：`documents.original_sha256` 每 Document 唯一（`models/source.py:32-34`），
`logical_execution_hash` 全局唯一（`:52-57`）—— 两个不同作用域的唯一性在冲突，
此前的文档从未点出该冲突域。

### R-2 `RETAINED` — `runner.py` identity violation

```text
问题：runner.py constructs hash from processed text
违反：raw byte identity principle
需要未来实现修复。
```

**证据**：`runner.py:74` `sha256_hex(body_text)` 违反 `app/core/raw_bytes_identity.py:14,42`
（明禁 `sha256_hex` 做身份，命其为「不同 hash 族」）；`source_loader.py:26-27` 的
`read_text()`/`splitlines()` 违反同文件 `:13`（已登记的 FACT-031 违规）。
正确实现（`load_raw_bytes_identity()`）**已存在于** `runner_b2.py:120`。

### R-3 `RETAINED` — Test gap

```text
tests green  !=  identity correctness proven
需要增加：identity invariant tests。
```

**证据**：现有测试对 `_create_source_records` 多为 `patch` + `call_count` 断言；
**无任何测试断言** consumer 的 `role`/`provider`/`original_sha256`/`le_hash`；
且 `tests/test_models_schema.py:39,103-107,124,126`（表/UNIQUE 契约，含 `assert len(seen) == 11`）
**未登记**在本批次文件清单内 —— 实现轮若改约束将直接违反它。

### R-4 `RETAINED` — 既有系统缺陷（非本批次引入）

| # | 缺陷 | 证据 |
|---|---|---|
| a | `_version_by_le` re-read **无 document 过滤** | `source_repository.py:128-138` |
| b | `source_meta` **无 sealed 不可变性** | `task/executor.py:258-270` |
| c | `ON CONFLICT` 目标索引与 re-read 谓词**必须同改**，否则 Postgres **Binder error**（响亮失败，非静默损坏） | `source_repository.py:110-113` vs `:128-138` |
| d | `0001:18` 是 `Base.metadata.create_all()` ⇒ ORM 才是 DDL 真源；`0006:37-50` 的 `IF NOT EXISTS uq_source_versions_le` 会在 `0001→0012` 链上**重建**待删约束 | `alembic/versions/20260905_0001_initial_abc.py:18`；`…0006:37-50` |
| e | `documents.original_sha256` 重键的兼容洞：改造后重跑会**新建** Document 而非收敛 | `source_repository.py:41-62`；`models/source.py:32-34` |
| f | `document_active_sources.role` 与 `document_source_selection_events.role` **闭集不相同** | `10_Data_Model.md:235` vs `:246` |

### R-5 `RETAINED` — Owner DB 事实问题已可由仓库证据部分回答

`FORMAL-E2E-04-evidence/04_v3_execution.log:18`「`persistence: session.rollback() — no rows committed`」（2026-09-26T16:41Z）；
`05_database_snapshot_before.json` 与 `06_database_snapshot_after.json` **逐项计数完全相同** ⇒ 一次完整 Track A 跑完，库内容零变化。
⇒ 高置信度推论：**无有记录的 Primary Path 运行在 `commit()` 启用后执行**。
残余不确定性：代码于同日改为 commit，**不能排除未记录的本地运行** ⇒ 一条 SELECT 仍为确证手段。

---

## 4. 审查方自身的错误（一并入账）

| # | 位置 | 错误 |
|---|---|---|
| RE-1 | 架构审查 R5 / 本记录 W-1 附带 | 「`SealService` **永远**到不了 `_version_by_le`」——**过度纠正**，并发路径可达（见 W-10a） |
| RE-2 | 计划事实核验 F8(b) | 推断「Owner 示例可能是制造的 / #1 阻塞是制造的」——**归因错误**：示例来自 Owner 对话指令，作者转录忠实；不可定位的根因是**裁决原文未落盘**（见 W-7） |
| RE-3 | 计划事实核验 F4 | 称 `DocumentActiveSource` 的「零使用」举证不实（对），但据此把结论也判为「refuted」有偏差：结论（该表零使用）**成立**，仅举证有误 |
| RE-4 | 一致性审查 G4 | 称 `APPROVED` 为「非法状态词」（援引 `AGENTS.md:33`）——**不准**：该词系 Owner 使用，且不在 `DOC-GOV:225-229` 禁用表内（见 W-9 归因更正） |

---

## 5. 本批次结论的净状态

```text
诊断内核（成立，保留）
    身份是「读路径」的选择；runner.py 写了一个它从未核对过的值。

灾难叙事（撤回）
    跨文档塌缩、不可逆身份损坏、ocr_ppsv3「诚实」映射。

严重度模型（修正）
    由「已发生的数据损坏」降为「被无关约束掩盖的前瞻性风险」。
```

---

## 6. Accepted Corrections（`[OWNER DECISION]` 固化）

本节将 §2 中三项撤回的**最终裁定表述**固定为可被实现方直接引用的文本。
与 §2 的关系：§2 记录**撤回过程与依据**；本节给出**采纳后的权威表述**。

### RC-01 — 跨文档身份塌缩

```text
删除：cross-document identity collapse occurred

采纳：cross-document collapse is unreachable under current document
      uniqueness constraint.
      Future risk only if uniqueness model changes.
```

对应 §2 W-1。**注意**：该风险仍**真实存在但不可达** —— 若 `original_sha256` 改为
不再决定 document 的域（即 Decision 2 Amendment 若选 2-A 则会发生的情形），
该风险即被暴露。**本批次已选 2-B，故该风险维持在「不可达」。**

### RC-02 — `SealService` 与 `_version_by_le` 的可达性

```text
删除：SealService cannot reach _version_by_le

采纳：Sequential path does not reach it;
      concurrent conflict path can reach it.
      Current safety depends on upstream uniqueness constraint.
```

对应 §2 W-10a。**精确表述**：`_version_by_le` 缺 document 过滤是**真实代码缺陷**
（`source_repository.py:128-138`）；其当前无害由 `uq_documents_original_sha256`
（`models/source.py:32-34`）**意外**提供，**而非该段代码自身保证**。

### RC-03 — Track A/B SourceVersion 共享

```text
删除：Track A/B sharing is design intent

采纳：Observed idempotent convergence.
      Design intent not established.
```

对应 §2 W-4。依据：`runner.py:132`（Track A）与 `:189`（Track B）传**相同**
`source_lines`/`source_path`，撞全局 UNIQUE 后 ON CONFLICT 收敛；内容逐字节相同，
故**客观无害**，但**无证据**证明共享 SourceVersion 是设计预期。

---

## 7. 本文件的残余边界

```text
· 本文件不含任何实现授权
· Blocking-2 已于 2026-09-27T09:13:28Z 实测 RESOLVED（数据库为空，无 Primary Path 数据）
· 本文件不修改 Frozen Spec；Spec 变更见 FROZEN-SPEC-ERRATA-PRIMARY-PATH-01.md
· 本文件中所有裁决性表述均引用 OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md
```

---

*Recorded 2026-09-27. 本文件为 Revision / Withdrawal Record（审计轨迹）。不含 `[OWNER DECISION]`；涉及裁决处一律引用 `OWNER-DECISION-PRIMARY-PATH-IDENTITY-01.md`。*
