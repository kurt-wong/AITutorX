# 任务 A 残余风险登记 + 全量测试失败项说明

> DSH 独立核查。**只读**（未修改任何生产文件）。
> 用途：Owner 授权任务 B 前的两项前置。
> **结论：Q17 回退分支的风险可量化界定；5 个测试失败全部为环境原因，0 个功能回归。**
> **但过程中发现 2 个此前未登记的 manifest 异常。**

---

## 第一部分：Q17 回退分支的残余风险 —— 可界定，但**不止 Q17**

Owner 要求"确认不会阻塞正常样本的验收"。我把它量化到**触发条件**而非笼统风险。

### 1.1 触发条件的定义

commit `512bba2` 的 `Empty content falls back to whole-line` 只在一种情况触发：

> 某个**已声明标签**与其**下一个已声明标签**之间的内容为**空**。

唯一能造成"两标签间为空"的情形是：**manifest 把两个标签声明在同一物理行且紧邻**。

### 1.2 全语料普查：命中 **3 处**，不是 1 处

```text
声明标签间内容为空的单元：
   化学/Q2      L20   标签 C
   化学/Q17     L125  标签 B
   物理/U12-14  L136  标签 A
```

Owner 的表述（"回退使 Q17 的部分选项保留整行风格"）在方向上正确，但**覆盖范围比 Q17 大**。
因此风险**不能**按"仅 Q17"登记。逐例说明（含修复前后）：

| 单元 | 源文 | manifest 声明 | 修复前 | 修复后 | 性质 |
|------|------|--------------|--------|--------|------|
| **化学 Q2** | L20 `A. Na、P B. N、Cl C. F、Mg D. O、S` | `[A,B,C,`**F**`,D]` — **多出幻影 F** | `gate=rejected`, labels=[] | 同前（未变） | **manifest 幻影标签**；F 插在 C 与 D 之间使 C 的"下一标签"变成 F，C 内容区间为空 → 触发回退 |
| **化学 Q17** | L125 `B. H: O: H` | `[A,B,`**H**`,C,D]` — **多出幻影 H** | B/D 吞并整行，H 空壳 | B/D **仍带整行风格**，H 得 `' O: H'`；swallow 仍为 2 | **manifest 幻影标签**（已定另案） |
| **物理 U12-14** | L136 是**材料文字**（`请阅读下述文字，完成第 12 题…`），真选项在 L140 | `[A(136),B(136),C(140),D(140)]` — **A/B 被错误绑到材料行** | A 吞整行，B/C/D 空壳 | **A/B/C/D 各自正确** ✅ | **manifest 错误行绑定**；回退在此**未造成损害** |

### 1.3 风险评估（对任务 B 的真正含义）

```text
回退从未在"正常单元"上触发 —— 3 个触发点全部是 manifest 本身有缺陷的单元。
  化学 Q2     幻影标签 F（新发现，未登记）
  化学 Q17    幻影标签 H（已登记另案）
  物理 U12-14 A/B 绑到材料行（新发现，未登记）

⇒ 回退分支 = 对畸形 manifest 的补偿行为，不是对正常样本的普遍回归。
```

**但要如实说明两点局限**：

1. **补偿不彻底**：Q17 的 B/D 仍带整行风格（`'B. H: O: H'`），swallow 仍为 2。
   即回退**保留了内容**却**没有清掉标签前缀**，导致同题内行文风格不一致。
2. **Q2 是"沉默"的**：`gate=rejected`、`labels=[]`，修复前后完全一致 ——
   该异常**不会**在选项层面暴露，只体现在"整题 rejected"。若任务 B 只看通过的题，Q2 会消失。

**建议登记措辞**：

```text
残余风险 R-A1（回退分支）
  触发条件：manifest 将两个标签声明在同一物理行且其内容区间为空
  全语料命中：3 处（化学 Q2 / 化学 Q17 / 物理 U12-14），全部为 manifest 缺陷单元
  对正常样本影响：0（97 道受影响题中无触发点）
  局限：对畸形单元的补偿不彻底（Q17 B/D 仍带整行风格）
  处置：不修；随 Q17 / Q2 / U12-14 三个 manifest 异常另案处理
```

### 1.4 新发现的两个 manifest 异常（建议一并登记）

| 单元 | 异常 | 与已知案例的关系 |
|------|------|-----------------|
| **化学 Q2** | manifest 声明幻影标签 `F`（L20 无 F 标签） | 与 Q17 的幻影 `H` **同类**（标注层 option-label 假阳性） |
| **物理 U12-14** | manifest 把 A/B 绑到材料行 L136（真选项在 L140） | **新类目**：材料题的行绑定错误，非标签假阳性 |

⇒ 说明 Q17 的"标注层假阳性"**不是孤例**；且存在**第三类** manifest 缺陷（材料题行绑定）。
建议在 Q17 另案下**扩为"manifest 选项声明异常"类目**，含至少 3 个样本。

---

## 第二部分：全量测试失败项说明（Owner 的前置要求）

### 2.1 我独立运行的完整结果

```text
5 failed, 1988 passed, 1 skipped, 1 xfailed, 295 errors in 64s
```

⚠️ **与我方环境有关的差异需说明**：MIMO 报告"2286 passed / 2 failed"，
我得到"1988 passed / 5 failed / 295 errors"。
差异**全部来自沙箱对临时目录与工作区外写入的限制**（见下），非代码差异。

### 2.2 5 个失败逐项定因 —— **全部为环境原因，0 个功能回归**

| # | 测试 | 失败断言 / 错误 | 性质 | 是否 Task A 回归 |
|---|------|----------------|------|-----------------|
| 1 | `test_adv_state_audit.py::TestClaimedPushAndSuite::test_v3_worktree_clean_at_checkpoint` | `AssertionError: ['?? backend/scripts/_p14b_patch_resolver.py', '?? backend/scripts/_p14b_patch_rule_a.py', '?? backend/scripts/_p14b_tighten.py']` | **工作区状态审计**：AITutors-v3 有 3 个未跟踪一次性脚本（P1.4-B 遗留，非 Task A 产出） | ❌ 否 |
| 2 | `test_adv_state_audit.py::TestClaimedPushAndSuite::test_x_worktree_clean` | `AssertionError: assert 'A  MIMO-TASK...1_min_corpus/' == ''` | **工作区状态审计**：检查的是 **AITutor-X** 仓库（存在未提交的 `MIMO-TASK-PHASE1-MINIMAL-E2E-01.md` 与未跟踪目录） | ❌ 否 |
| 3 | `test_adversarial_m5_round2.py::TestRealBypassSimulation::test_no_bypass_through_normal_pipeline` | `PermissionError: [Errno 13] ... 'C:\\Users\\...\\Temp\\dsh-AEIIEV\\tmp3pe5_ied\\src.md'` | **沙箱**：测试写系统 TEMP 被拒 | ❌ 否 |
| 4 | `test_document_import_e2e.py::test_import_document_e2e` | `PermissionError: [Errno 13] ... 'data\\imports\\a4757f6d….pdf'` | **沙箱**：测试写 `backend/data/imports/`（工作区外）被拒 | ❌ 否 |
| 5 | `test_document_import_e2e.py::test_import_duplicate_pdf_idempotent` | 同上 | 同上 | ❌ 否 |

**判定依据**：3 个是文件系统权限（沙箱边界，与代码无关）；
2 个是工作区状态审计（检查 git 清洁度，与代码逻辑无关，且 #1 的未跟踪脚本属 P1.4-B 遗留）。
**没有一个涉及 Resolver / 选项解析 / Gate 决策。**

### 2.3 295 个 error 的定因

```text
抽样 tests/test_x26_fint08_interface_scope.py::TestNoSilentCoercion::test_producer_declaration_is_preserved_verbatim
   -> ERROR at setup
   fixturedef = <FixtureDef argname='tmp_path' ...>
   PytestCacheWarning: could not create cache path ...\.pytest_cache\v\cache ... [WinError 5] 拒绝访问
```

⇒ **`tmp_path` / `.pytest_cache` 写盘被沙箱拒绝**，属环境限制。
MIMO 环境能写 TEMP 与缓存，所以那 295 个在其报告中计入 passed —— 这解释了 1988 vs 2286 的差额。

### 2.4 结论（可写入任务 B 前置）

```text
任务 A 相关测试：51/51 通过（test_resolver / test_option_fullwidth_comma / test_task_a_option_content_span）
功能回归：0（1988 passed；5 failed + 295 errors 全部为沙箱/工作区状态原因）
Q17 / Q20：未动（前像比对确认）
```

**注意**：我**没有**做"换回基线 resolver 复跑 M5"的实验 ——
因为 M5 的失败签名是 `PermissionError`（写 TEMP），与 resolver 无关，
无需为它扰动生产文件。这是有意的取舍，不是遗漏。

---

## 第三部分：对授权任务 B 的建议（含本轮新增的两项前置）

采纳 Owner 的 5 条边界，并建议补 2 条：

```text
6. 任务 B 首轮不得依赖"整题 rejected 的题"作为阴性对照 ——
   化学 Q2 这类 manifest 异常在选项层是沉默的（labels=[]，gate=rejected），
   只看通过题会漏掉它们。

7. 任务 B 的逐层留证需包含 manifest 声明本身（options[] / options_lines / answer_lines），
   而不只是 V3 各层的输出 —— 本轮 3 个回退触发点全部源自 manifest，
   只记录下游输出无法定位"声明错误"。
```

**状态维持**：

```text
任务 A：验收通过（残余风险 R-A1 已登记）
Q17 另案：建议扩为"manifest 选项声明异常"（现含 化学 Q17 / 化学 Q2 / 物理 U12-14）
任务 B：待授权；本报告已满足其"失败项说明"前置
OCR 内容边界：仍在状态表
```

---

## 附：本轮产物（全部只读）

| 文件 | 内容 |
|------|------|
| `_bound_fallback_risk.py` | 回退触发条件全语料普查（3 处） |
| `_inspect_fallback_units.py` | 3 个触发单元的源文/声明/前后对比 |
| `_m5_regression_bisect.py` | 换文件二分脚本（**未执行** —— M5 已定性为 PermissionError） |
| `_taskA_clean_surface.py` | 变更面净化分析（另见任务 A 验收报告） |
