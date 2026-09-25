# OD-R-01 最终卫生收口 H-09～H-13（`4d591cd` + `d2b9a26`）— DSH 独立对抗性审查

## 0. 审查对象与元信息

| 项 | 值 |
|---|---|
| 审查对象 | Claude 任务报告「OD-R-01 Final Hygiene Closure — H-09 ~ H-13 最终报告」（STATUS: COMPLETE） |
| 仓库 | `D:\Project\AITutors-v3`（分支 `od01-r3-convergence`） |
| 被审 commit | `4d591cd5e42a1a0d6c888b4d79ad1094a0dd6fa8`（`docs: finalize OD-R-01 hygiene closure findings`；3 files, +200/−23）+ `d2b9a26f1a1c0297b4536b273b8999a071433079`（`docs: fix G-02 6.4 environment-assumption table wording`；1 file, +6/−4） |
| 审查基线 | HEAD = `d2b9a26`（tracked 改动 0） |
| 审查方式 | 对 git 对象 / 仓内文本独立取证；**未采信报告自述**；审查期间未修改 `AITutors-v3` 任何文件、未 commit、未 push |
| 关联 | DSH 第 6 轮：`AITutor-X/Docs/60_REPORTS/OD-R-01-H01-FOLLOWUP-DSH-ADVERSARIAL-REVIEW.md`（`08a900e`）——H-09/H-10 MED、H-11/H-12/H-13 LOW = 本轮被修对象 |

---

## 1. VERDICT

```text
VERDICT: ACCEPTED WITH FINDINGS
（H-09 / H-10 / H-11 / H-12 / H-13 五项**全部 CLOSED**，逐条实测可证；
 新增 4 项 LOW，全部是报告与文档的精确性残留，无一触及治理结构、无一阻断 OD-R-01 CLOSED）
```

**一句话结论**：五项修法**都是实质性的**，不是措辞敷衍——H-10 写出了可复核性边界且**拒绝**建内部映射表；H-11 用「内容首次出现」的 P1/P2 判据**真正**替换了 subject 模糊匹配；H-13 主动把 A/B/C 结果**限定为历史时点值**（正是过去三轮反复复发的缺陷类）；H-12 把活指令改 commit 锚定并**逐字保留**原文以存历史证据；H-09 用「注册补记」补全描述完整性而**未**新建 CR 文档类型（避免"为治理文档再建治理文档"）。

还有一处必须记分：**任务书要求「Push to main」，实施方拒绝了**，并给出机械理由（main 是本分支严格祖先、会把 `origin/main` 快进 23 个 commit、属发布动作、与 `Do not expand scope` 冲突）——这是**正确的不服从**，且已显式披露（计数残留见 H-17）。

本轮新增项全部为 LOW：分类递归未终止（H-14）、自指行机械判据只覆盖一处（H-15）、报告 Validation A 段快照不自洽（H-16）、偏差披露计数未随第二个 commit 更新（H-17）。

---

## 2. 已独立复核的关键事实（DIRECTLY VERIFIED）

```text
HEAD = d2b9a26… ✓   branch = od01-r3-convergence ✓   parent(4d591cd) = 6152899 ✓
origin/od01-r3-convergence = d2b9a26… ✓（git ls-remote 直接核验远程 ref，两个 commit 均已推送）
origin/main = 7934844…（未动）✓   main = 6d8a3bd…（未动）✓
main 是 od01-r3-convergence 的严格祖先 ✓（merge-base --is-ancestor exit 0）

4d591cd：3 files, +200/−23 ✓  非 .md = 0 ✓  L0 00–50 = 0 ✓
  name-only = G-02 / 90_DOCUMENT_GOVERNANCE.md / CR-003
d2b9a26：1 file（G-02）, +6/−4 ✓  L0 = 0 ✓

tree 等式：
  6152899:Docs/V3_SPEC = ecd12c0e9682eaed2e3ad7c2416984b9cff92bee  （previous）✓
  4d591cd:Docs/V3_SPEC = 14a7450809d4932036f415d765ab29c53671843c
  d2b9a26:Docs/V3_SPEC = 14a7450809d4932036f415d765ab29c53671843c  = HEAD:Docs/V3_SPEC ✓
  G-02:192 CURRENT 字面值 = 14a7450809d4932036f415d765ab29c53671843c  ⇒ EQUAL ✓
  ⇒ 第二个 commit 只动 G-02（在 Docs/V3_SPEC 之外），故 CURRENT 字面值在两次提交后仍等于事实值 ✓

固定点（自指防火墙）：`14a74508…` 全仓 3 处**全部**在 G-02（:192 / :221 / :222）；
  在 `Docs/V3_SPEC/` 内命中 = 0 ✓

(c) 链完整性：`git log 5a46d33..HEAD -- Docs/V3_SPEC` = 1ee84cd / 6152899 / 4d591cd 三个
  → 与 :513 / :514 / :515 三行逐一对应 ✓（d2b9a26 未触及 V3_SPEC，依规则无需加行 ✓）

AITutor-X：HEAD = origin/main = 08a900e…（未动）· tracked 改动 0 ✓
  · DSH 审查记录 `OD-R-01-H01-FOLLOWUP-…md` 最后触碰者仍是 DSH 自己的 08a900e ⇒ **未被改写** ✓
```

---

## 3. H-09～H-13 闭合核验（逐条实测）

| 上轮 finding | 本轮修法（实测） | 判定 |
|---|---|---|
| **H-09** `(c)` 行改动面漏登 + 未分类 | `90:533-545` 新增「注册补记（H-09）」，三要素齐备：① **改了什么**（新增解释性/不变式注记 + **废止**原 `git log -1` 指令）；② **分类** = CHANGE-1 Clarification（引 `§3` 定义，声明规范语义零变化）；③ **既有义务是否改变** = 未改变，`:489-491`「必须」逐字未动（实测 `git grep '必须能在本节找到对应 CA 条目'` → **:489** ✓）；补记明写不改写历史取值 / 不新建 CR 文档类型 / 不新增机制。另 `:515` 新行「改动面」列全 **8 项** ✓（实测与其自述一致） | **CLOSED**（递归残留见 H-14） |
| **H-10** 仓外坐标不可解析 | `90:547-554`「仓外坐标可复核性边界」为权威表述：`H-*`/`HYG-D*`/「DSH 第 N 轮」**源自仓外 DSH 审查产物**，**不是** L0/L0-META/L1/L2 条目、**不是** CA/CR/OD 编号、**不**承载授权效力、引用**仅**为审计可追溯性；「仓内可核验证据边界 = 仓内路径 + commit（完整 SHA）+ 可复现机械检查命令；**不包含**仓外报告正文」；**不**建内部替代 registry / 编号映射表；口径对照 `CR-004 §2.4`。落位三处：`90`（权威）+ `CR-003:59-61` + `G-02:110-115`（指针）✓ | **CLOSED** |
| **H-11** 解析需人工模糊匹配 / exclude 盲区 | ① `90:525-531` + `G-02:298-302`：**核验一律以精确 commit identity（完整 SHA）为准**，**不得**以 subject 模糊比对作判据，并**点名**括注阶段名与实际 subject「文本不等、不构成判据」；② `G-02:326-340` 给出**内容首次出现**判据 P1/P2（实测：`git show 6152899:G-02` 含 `### 6.4` **= 1**；其 parent **= 0** ✓），取代 subject 匹配；③ `G-02:304-319` 明写 exclude **只**适用 A 类通用陈旧文本扫描、B/C 类作用于 git 对象**无需也未**排除、**盲区代价**（永久 exclude ⇒ A 类对 G-02 自身永不报警）由 **G-02 专用身份核验**（C1/C4/B1）覆盖，且「A 类**不得**被当作 G-02 自身的清洁度证据」 | **CLOSED**（覆盖面残留见 H-15） |
| **H-12** `§6.1` 活指令与 90 禁令冲突 | `G-02:124-131` 改为 **commit 锚定实名** `60fa9ff30f70037e1990db7dd5bc255310073432` + commit-specific 机械核验；实测 `git show --name-only --format= 60fa9ff…` 含 `CR-003` / `90` / `10_Data_Model` / `20_Document_Pipeline` ✓，`git rev-parse 60fa9ff:Docs/V3_SPEC` = `8659e2fa…` ✓；原文**逐字保留**在 `:133-138` 的 superseded 注内（**未删除**）并注明「不再作为活指令」+ 两条废止理由。实测 `git grep '机械取值：`git log -1' -- Docs/` → **唯一命中 `90:537`**（即注册补记中的历史引述）✓；`git grep 'git log -1'` 其余命中均为「禁令」或 superseded 引述或 `IMPLEMENTATION-PLAN` 历史 baseline 记录 | **CLOSED** |
| **H-13** 复现前提 / 推导口径 | ① `G-02:279-285`「环境与命令实现前提」表（Git 版本 / `:(exclude)` 需 Git ≥ 1.9 / 正则引擎 / 裸 `grep` 需 GNU grep 在 PATH / shell；实测本机 `git version 2.54.0.windows.1` ✓ 与其所载一致）；② `:287-291` 无 GNU grep / 无 pathspec magic 时的等价替代；③ `:292-296`「谁执行了什么、证明了什么」+ 明写**未证明**边界；④ `:207-229` tree 推导口径：**权威推导**（`git rev-parse <被验 commit>:Docs/V3_SPEC`）vs **预演推导**（`git add`→`write-tree`→T），明写「T 是工作树中间快照的根 tree，与最终 commit 根 tree **不必相等**」「中间 T 的**根** tree 不入本记录、不作核验依据」；⑤ **`G-02:271-275`「结果时点范围」**：A/B/C 结果限定为引入本节 commit 的历史实测值，「**不得**读作对当前状态的断言」 | **CLOSED** |

**报告其余自述核对**：路径披露（AITutor-X 0 tracked）✓ · 未改写 DSH 审查记录（实测 `08a900e` 未被触碰）✓ · Validation B/C（commit-specific 核验，3 个 `.md` / 非 `.md` = 0 / L0 = 0）✓ · D 段（`:489` + 计数 **5**）✓ · E 段 tree 三等式的 EQUAL ✓ · F 段固定点（写入 G-02 不改变被记 tree）✓ · G 段 P1/P2 = 1/0 ✓ · H 段 A1–A4（4 / `84:176` / 0 / `CR-003:50`）✓ · I 段 `git log -1` 残留判定 ✓ · J 段 markdown 表（修复前两行为 4 列 / 5 列，修复后全部 3 列）✓ · Governance boundary 各条 ✓ · 两个 commit 均已推送、`origin/main` 未动 ✓。

---

## 4. Findings（本轮新增，全部 LOW）

### H-14 [LOW] 分类递归未终止：本 commit 为**上一** commit 的注记补了分类，却未分类**自己**新增的三则注

`90:533-545` 的注册补记只覆盖 `6152899` 的行锚定注（判为 CHANGE-1）。但本 commit 自身又新增三则 L0-META 文本：`H-10` 边界注、`H-11`「**不得**以 commit subject 文本的模糊比对作为核验判据」、`H-13` 环境前提（G-02 侧）——其中 `:528` 的「不得…作判据」同样是**强制措辞**，而 `:515` 行的声明列只写「L0-META / L1 面改动，非 L0 修改」，**未给分类**。

按 `90 §3:530`「**新增强制 invariant 同样是正式变更**」与 `:541`「**拿不准往高里归**」，这一族注记的分类不应逐条追补。**建议（终止递归）**：在 `:533-545` 注册补记内加**一句类规则**——例如「本节内凡属**审计程序澄清**（自指解析、取值方式、取证环境、坐标边界）的注记，一律判 **CHANGE-1**，规范语义零变化；凡**新增/改变/放宽/删除任何规范约束或义务**者，须单独分类登记」——此后同类注记依类规则归类，无需逐条补记。

**反方最强辩解**：这些注记讲的都是"**怎么审计**"，而 `(c)` 节本身就是审计程序节，落在既有授权面内；且逐条分类会陷入"每则声明又要一则声明"的无限回归。**但**正因如此，才更应给出**类规则**而非沉默——本 finding 的建议正是反方逻辑的结论，不是额外负担。严重度 LOW：不影响任何义务、权限或结论。

---

### H-15 [LOW] 自指行的机械判据只覆盖 `§6.4` 一处，另两处自指行仍无对应命令

P1/P2 判据（`G-02:326-340`）机械地解决了「**引入 §6.4 的 commit**」。但仓内现有**三处**自指行：
① `G-02 §6.4` 的「被验 commit」→ 已由 P1/P2 覆盖 ✓；
② `G-02 §6.2:171`「H-09~H-13 闭合」行（`= current`，取值命令为 `<本行登记所在 commit>:Docs/V3_SPEC`）；
③ `90:515` 的「本行所在 commit」行。
②③ 未给出同类命令，只能由读者"照 P1/P2 的精神自行构造"。**建议**：各补两行同型判据（例如 `git show <sha>:G-02 | grep -c 'H-09~H-13 闭合'` → 1 且其 parent → 0；`git show <sha>:90_… | grep -c '最终卫生收口 H-09~H-13'` → 1 且其 parent → 0），使三处自指行**全部**可机械解析。这是 H-11 判据的**同型延伸**（非新增要求），成本两行。

---

### H-16 [LOW] 报告 Validation A 段三条陈述不可能来自同一快照

报告 A 段同时给出：① `git status --short` 显示 `G-02` 为**未暂存**（` M`）；② `git diff --cached --name-only` 列出**3** 个 `.md`；③ `git diff --cached --stat` = **+202/−23**。而提交实测 `git show --stat 4d591cd` = **+200/−23**。

三者互相矛盾：若 G-02 未暂存，`--cached` 不可能列出 3 个文件；若已暂存，计数应为最终 200 而非 202。**建议**：A 段只保留**一条时点明确**的快照，或直接以 commit-specific 数值为唯一证据（报告 B 段已如此做，值得推广）。这与 H-13(b) 所指「中间快照 ≠ 最终结果」是**同一机制**，本轮已在 G-02 侧澄清 ✓，报告侧 A 段未同步。

---

### H-17 [LOW] 偏差披露段的关键计数未随第二个 commit 更新

报告「偏差披露 1」称 `git rev-list --left-right --count main...od01-r3-convergence = 0 10`，并把推 main 描述为「快进 **22** 个 commit」。实测：**`0 11`**，且 `git rev-list --count origin/main..od01-r3-convergence` = **23**。

差值恰为第二个 commit `d2b9a26` ⇒ 该计数取自 `d2b9a26` 创建之前，此后未重算。这两个数字用于支撑「不推 main」这一**治理判断**，应当准确。**建议**：更新为 `0 11` / `23`，或注明取值时点。

---

### INFO（不需处理，供参考）

```text
INFO-1  `G-02:231-233`（本轮新增「历史值不改写」注）与紧随的 `:235-236`（既有「历史 hash 处置」段）
        内容重叠（同指 b3eeb3e9… / fa1e953e… 永久保留 + 90 §4 引述）。建议择一保留或合并，
        以免两处将来漂移不一致。
INFO-2  H-10 的边界注给出了「来源仓 + 目录」，但未给外部报告的 commit SHA。若 Owner 希望坐标可
        **解析**（而非仅声明边界），可在 `90:547` 处补一句形如「（示例锚点：`AITutor-X@08a900e`）」；
        本轮选择的是"边界声明"路线，符合 DSH 第 6 轮给出的两个选项之一，不构成缺陷。
INFO-3  `IMPLEMENTATION-PLAN-v0.3.md:95/:122` 的 `git log -1` 属历史 baseline 取值记录
        （自标 HEAD at planning time），非活指令，未改 ✓（与报告 residual #3 一致）。
INFO-4  `84_CONFLICT_LEDGER.md:176`（H-02 / HYG-D2）仍为无限定现行断言，NON-AUTHORIZED 保留 ✓；
        H-03 / H-04 未触碰 ✓。
```

---

## 5. 记分：本轮做对的地方

1. **五项全部实质闭合**，且闭合方式比"补一句说明"更硬：H-11 用**内容首次出现**判据替代文本匹配；H-13 把结果**限定为历史时点**；H-12 把活指令换为 commit 锚定并**保留原文存证**。
2. **H-10 的克制**：写出边界，同时明确「**不**建内部替代 registry / 编号映射表」「**不**复制外部审查正文入仓」——既解决可追溯性，又没有把仓外权威搬进仓内（延续 M-01 / H-04 的正确处置方向）。
3. **H-13 的时点限定是主动的**：`G-02:271-275` 把 A/B/C 结果声明为"引入本节的 commit 时点的历史实测值""**不得**读作对当前状态的断言"——这正是第 4/5/6 轮**各复发一次**的缺陷类，本轮**事先**堵住，而非等 DSH 再报。
4. **自查自纠**：主动更正自己上一轮的表述（`G-02:266-267`：原写「BRE 下 `\|` 是字面量」与实测不符 → 改为「BRE 下裸 `|` 是字面量，`\|` 是 GNU BRE 的 alternation 扩展」），与 DSH 上一轮撤回 H-08(a) 形成**双向纠错**。
5. **正确的不服从**：拒绝任务书「Push to main」并要求 Owner 明示，理由机械且成立（main 为严格祖先、快进 23 个 commit、属发布动作、与 `Do not expand scope` 冲突、前四轮惯例）——并**显式披露**该偏差。
6. **不改写已发布历史**：发现 `4d591cd` 自身的 markdown 表缺陷后，不 `--amend`、不 force-push，改用独立修补 commit `d2b9a26` + 显式披露 ✓（实测修复前该表两行为 4 列 / 5 列，修复后全部 3 列 ✓）。
7. **不触碰审计记录**：AITutor-X 侧 0 tracked 改动，DSH 报告未被改写 ✓（实测最后触碰者仍是 `08a900e`）。
8. **`(c)` 链无缺口**：`5a46d33` → `1ee84cd` → `6152899` → `4d591cd` 四个 V3_SPEC 阶段与四行声明一一对应；`d2b9a26` 未触及 V3_SPEC，依规则无需加行 ✓。

---

## 6. Owner 裁决清单（DSH 只列项与证据，不作裁决）

```text
OD-R-01-H09R-D1  【LOW】H-14：在 90:533-545 注册补记内加一句**类规则**（审计程序澄清类注记一律
                 CHANGE-1；凡新增/改变/放宽/删除约束者须单独分类），终止递归
OD-R-01-H09R-D2  【LOW】H-15：为 `G-02 §6.2:171` 与 `90:515` 两处自指行各补两行同型机械判据
                 （`git show <sha>:<file> | grep -c '<该行标识串>'` → 1；其 parent → 0）
OD-R-01-H09R-D3  【LOW】H-16：报告 Validation A 段改为单一时点快照，或径以 commit-specific 数值为准
OD-R-01-H09R-D4  【LOW】H-17：偏差披露计数更新为 0 11 / 23（或注明取值时点）
OD-R-01-H09R-D5  【INFO】INFO-1（重复注记择一）/ INFO-2（是否给外部报告 SHA 锚点）/ 由 Owner 定
OD-R-01-H09R-D6  【OD-R-01 是否 CLOSED】DSH 立场（承接第 6 轮 D6）：
                 H-05 / H-06 / H-07 / H-08 / H-09 / H-10 / H-11 / H-12 / H-13 **九项全部 CLOSED**；
                 (c) 登记链 5a46d33 → 1ee84cd → 6152899 → 4d591cd **完整无缺口**；
                 授权 / 分类 / re-freeze / provenance / 审计链**均闭合**；
                 H-14~H-17 为 LOW 精确性残留（合计约 6 行修法），**不阻断 CLOSED**。
                 DSH 不代行该裁决；若 Owner 判 CLOSED，建议同时决定是否顺手清 H-14~H-17。
```

**Security**: Never hardcode API Keys/Passwords/Tokens/Secrets; Always use .env for configuration.

---

## 7. 未验证 / UNKNOWN

```text
UNKNOWN  仓外任务书原文（§3 Expected location 四项、§8「Push to main」措辞、H-09~H-13 原始判据）
         —— 不在仓内；DSH 只核验其可核验后果
UNKNOWN  实施代理侧的 GNU grep 3.0 / POSIX sh 环境实测
         —— DSH 沙箱禁用 `grep.exe`（signal pipe 被拒），故仅能以 `git grep` 等价复现；
            本机 `git version 2.54.0.windows.1` 与其所载一致 ✓
INFO     本地 `main` = 6d8a3bd 领先 `origin/main` = 7934844 共 12 commit（均不触及 Docs/V3_SPEC）
         —— 既存状态，本轮两个 commit 未改变；是否推送属 Owner 事由
```

---

**Document control**

| Field | Value |
|---|---|
| Path | `Docs/60_REPORTS/OD-R-01-FINAL-HYGIENE-H09-H13-DSH-ADVERSARIAL-REVIEW.md` |
| Status | FINAL |
| Reviewed commits | `4d591cd5e42a1a0d6c888b4d79ad1094a0dd6fa8` · `d2b9a26f1a1c0297b4536b273b8999a071433079` |
| Round | OD-R-01 对抗性审查第 7 轮 |
| Verdict | ACCEPTED WITH FINDINGS（H-09~H-13 全部 CLOSED；H-14/H-15/H-16/H-17 LOW + 4 INFO） |
| Repo of subject | `kurt-wong/AITutors-v3` @ `od01-r3-convergence` |
| This report repo | `D:\Project\AITutor-X`（DSH 侧，未修改被审仓任何文件） |
