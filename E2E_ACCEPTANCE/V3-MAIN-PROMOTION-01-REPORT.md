# V3-MAIN-PROMOTION-01 报告：已验收基线晋级至远端 main

## 1. 本轮目标

按方案②，将 `od01-r3-convergence` 已验收提交 **`9a4bfb7`** fast-forward 晋级至 `origin/main`，使 GitHub 默认分支反映已验收产品基线。

## 2. 实际成果

- 远端 `main`：`79348441` → **`9a4bfb7`**（fast-forward，73 个提交前进，0 反向）。
- 远端 `od01-r3-convergence` 仍为 **`9a4bfb7`**。
- 默认分支 HEAD 已指向 `9a4bfb7`（即晋级后的 main）。
- 未 force、未 merge commit、未改历史、未新增提交、未动未跟踪脚本。

## 3. 验收证据

### 固定目标核对

| 项 | 预期 | 实测 |
|---|---|---|
| 仓库 | `kurt-wong/AITutors-v3` | `https://github.com/kurt-wong/AITutors-v3.git` ✅ |
| 来源分支 tip | `9a4bfb7…` | `9a4bfb7c87bd5fa2e8173374b2780b3663568631` ✅ |
| 原远端 main | `79348441…` | `79348441dae0efce6855017b2b5c0491b08d6bb8` ✅ |
| 晋级目标 | `9a4bfb7…` | 同上 ✅ |

### 安全检查

* 本地 HEAD = `9a4bfb7`（与目标一致）。
* 工作区：仅 3 个 untracked `backend/scripts/_p14b_*.py`（未提交、未删除、未纳入）。
* `merge-base --is-ancestor 79348441 9a4bfb7` = **0**（原 main 为严格祖先）。
* `rev-list --count 79348441..9a4bfb7` = **73**；`9a4bfb7..79348441` = **0** → 纯 fast-forward。
* 来源分支未前移；无并行新提交。

### 推送命令与结果

```
git push origin 9a4bfb7c87bd5fa2e8173374b2780b3663568631:refs/heads/main
→ To https://github.com/kurt-wong/AITutors-v3.git
   7934844..9a4bfb7  9a4bfb7c87bd5fa2e8173374b2780b3663568631 -> main
```

（使用一次性 `-c http.proxy= -c https.proxy=`，因本地默认代理端口不可达；未改全局 git 配置。）

### 推送后核验（`git ls-remote origin` 直读）

| ref | SHA |
|---|---|
| `refs/heads/main` | `9a4bfb7c87bd5fa2e8173374b2780b3663568631` |
| `refs/heads/od01-r3-convergence` | `9a4bfb7c87bd5fa2e8173374b2780b3663568631` |
| `HEAD`（默认分支入口） | `9a4bfb7c87bd5fa2e8173374b2780b3663568631` |

* 本地 HEAD / `origin/main` / `origin/od01-r3-convergence` 三者同一 SHA。
* `79348441` 仍为 `origin/main` 祖先（历史可访问）。
* 工作区与推送前一致。
* 远端 tip 提交 = M3b-R1 六文件（gate/funnel_recorder/executor/conftest/test_m3b_r1_*）。

## 4. 未完成事项

1. **DSH 独立核验**（任务 §6）：请 DSH 对远端 `main` 做只读核验（SHA 一致性 + tree 含测试隔离/反馈/Funnel 文件）。
2. 本地分支 `main`（`6d8a3bd`）与远程 `main`（`9a4bfb7`）不同源；本地 `main` 未晋级，本轮未触碰。

## 5. 整体进度

| 里程碑 | 状态 |
|---|---|
| M1 → M3b-R1 | ✅ `9a4bfb7` |
| M3b-R2 分支同步 | ✅ `od01-r3-convergence` |
| Papers 映射推送 | ✅ `b141bfd` |
| **V3-MAIN-PROMOTION-01** | ✅ **`origin/main` = `9a4bfb7`** |
| DSH 远端 main 核验 | ⬜ |

## 6. 下一步

DSH 只读核验远端 `main` = `9a4bfb7` 且含 M3b-R1 文件后，本任务停止，等待 Owner 决定下一阶段。
