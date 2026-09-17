# Report A — AITutorX Governance Baseline Audit

**日期**: 2026-09-16
**审计范围**: V3 Consumer + Preprocessing Producer（独立审查，不依赖已有报告结论）
**方法**: git log / git status / git show / sha256sum / pytest 直接验证

---

## 1. 仓库状态

### 1.1 V3 Consumer (`kurt-wong/AITutors-v3`)

| 项目 | 值 | 验证方式 |
|------|-----|---------|
| HEAD | `cc12d79` | `git log --oneline -1` |
| origin/main | `cc12d79` | `git rev-parse origin/main` |
| Local drift | NONE | HEAD == origin/main |
| Branch | main | `git branch -a` |
| Tags | `v3-phase-i2-closed` | `git tag` |
| Tracked files | ~457 | `git ls-files \| wc -l` |
| Untracked files | 10 paths (9 docs + 1 governance dir) | `git status --short` |
| Total commits | ~40 | `git log --oneline \| wc -l` |

**测试基线** (2026-09-16 实测):
```
1780 passed, 1 skipped, 1 xfailed — ALL PASS
```

### 1.2 Preprocessing Producer (`kurt-wong/Aitutors-preprocessing`)

| 项目 | 值 | 验证方式 |
|------|-----|---------|
| HEAD | `2b92898` | `git log --oneline -1` |
| origin/main | `2b92898` | `git rev-parse origin/main` |
| Local drift | NONE | HEAD == origin/main |
| Branch | main | `git branch -a` |
| Tags | (none) | `git tag` |
| Tracked files | 419 | `git ls-files \| wc -l` |
| Untracked files | 0 | `git status --short` |
| Python files | 122 | `git ls-files -- '*.py' \| wc -l` |
| Total commits | 160 | `git log --all --oneline \| wc -l` |

**测试基线** (2026-09-16 实测):
```
1 failed, 337 passed, 1 xfailed
FAILED: tests/test_r67_bootstrap.py::test_r67_t13_real_corpus_smoke (768 excluded)
```

---

## 2. Frozen Contract v0.2 验证

| 项目 | 值 |
|------|-----|
| Freeze Object commit | `f4941ff` |
| Document | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT.md` |
| SHA256 @ f4941ff | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |
| SHA256 @ HEAD | `9c6b9063e81fb2a66d85794b280c9d931f1b0074b39abf472033218149b17528` |
| Byte match | **VERIFIED** — 两处 sha256 完全一致 |
| Ancestor check | `f4941ff` is ancestor of `origin/main` — TRUE |

---

## 3. Identity 模块状态

| 模块 | 文件 | SHA256 (前16) |
|------|------|---------------|
| M1 | `backend/app/core/manifest_identity.py` | `1ca33a45a101de8c…` |
| M2 | `backend/app/core/raw_bytes_identity.py` | `803c4ed8a93f59b5…` |
| M3 | `backend/app/core/ir_identity.py` | `f960b513a935c8ca…` |
| M4 | `backend/app/core/identity_verifier.py` | `1306105c6c3d2b8b…` |
| M5 | `backend/app/core/identity_gate.py` | `8a5d267e285800f0…` |

全部已 commit 至 V3 HEAD `cc12d79`（`6c4e3ff` Phase 2 实现 + `cc12d79` Phase 2.5）。

---

## 4. V3 Untracked 文档（核心发现）

以下 9 个文档**从未进入 git 历史**（`git log --all -- <path>` 返回空）：

| # | 文件 | 用途 | Authority |
|---|------|------|-----------|
| 1 | `PREPROCESSING-V3-CONTRACT.md` | 早期 Contract 版本 | UNKNOWN |
| 2 | `PREPROCESSING-V3-CONTRACT-CONSUMER-REVIEW.md` | Consumer Review | UNKNOWN |
| 3 | `PREPROCESSING-V3-CONTRACT-v0.2-DRAFT-SKELETON.md` | Skeleton 版 | UNKNOWN |
| 4 | `…DESIGN-v1.md` | Identity Verification 设计 v1 | UNKNOWN |
| 5 | `…DESIGN-v1.1.md` | 设计 v1.1（D2/D3/D4 权威引用） | UNKNOWN |
| 6 | `…IMPLEMENTATION-PLAN-v1.md` | 实施计划 | UNKNOWN |
| 7 | `…IMPLEMENTATION-READINESS-v1.md` | 就绪检查 | UNKNOWN |
| 8 | `…IMPLEMENTATION-REPORT-PHASE1.md` | Phase 1 报告 | UNKNOWN |
| 9 | `…IMPLEMENTATION-REPORT-PHASE2.md` | Phase 2 报告 | UNKNOWN |

**Governance docs**（G0 轮创建）也是 untracked：
- `Docs/GOVERNANCE/00-SYSTEM-BASELINE.md`
- `Docs/GOVERNANCE/02-AUTHORITY-MATRIX.md`
- `Docs/GOVERNANCE/03-DECISION-REGISTRY.md`
- `Docs/GOVERNANCE/04-CLAIM-REGISTRY.md`

---

## 5. Git History 中的已删除文件

### V3
| 文件 | 删除于 | 说明 |
|------|--------|------|
| `CLAUDE.md` | `72af28d` | 治理违规修复，有意删除 |

### Producer
| 文件 | 删除于 | 说明 |
|------|--------|------|
| `RS.MD` | `7bda4d7` | 有意不入库（.gitignore line 31） |
| `data/r54_f1/f1_report.json` | `7bda4d7` | 误提交恢复 |
| `data/resolver_ref_r52/resolver_ir.json` | `7bda4d7` | 误提交恢复 |
| `logs/ocr_child_err.log` | `7bda4d7` | 日志 |
| `logs/reslice_reslice-pac-annotated_log.txt` | `7bda4d7` | 日志 |

---

## 6. Producer 目录结构

```
Papers/
├── Docs/COORDINATION/     # 协调文档（tracked）
├── governance/            # 治理文件（tracked）
│   ├── phase_p2_charter.md
│   ├── risk_register.md
│   └── rule_registry.md
├── scripts/               # Python 脚本（tracked）
├── tests/                 # 测试（tracked）
├── data/                  # 数据目录
├── reports/               # 报告
├── log.md                 # append-only 日志
├── bugs.md                # Bug registry
├── status.md              # 状态文件
└── prd.md                 # 产品需求
```

---

## 7. 关键判断

| 判断 | 结论 | 证据类型 |
|------|------|---------|
| 两 repo 均在 sync | VERIFIED | HEAD == origin/main |
| Contract freeze integrity | VERIFIED | SHA256 双点一致 |
| V3 test baseline | ALL PASS | 1780 passed |
| Producer test baseline | 1 pre-existing failure | 337 passed, 1 failed |
| 9 untracked docs 无 git traceability | VERIFIED | git log 全空 |
| Design v1.1 无 git 历史 | VERIFIED | 同上 |
| DEC 编号冲突存在 | VERIFIED | 见 Report C |
| CLAUDE.md 有意删除 | VERIFIED | commit `72af28d` |
