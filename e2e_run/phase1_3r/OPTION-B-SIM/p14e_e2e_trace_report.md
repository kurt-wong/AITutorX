# P1.4-E2E-TRACE — Data Flow Responsibility Report (READ-ONLY)

## 0. Adjudication start
P1.4-B **FROZEN**. `ec62d29`/`d42cde6` = diagnostic checkpoints only.
This report does **not** assume Producer is at fault.

## 1. Interface truth: Preprocessing vs V3

| Layer | What it is | Where |
|-------|------------|-------|
| **L0 Preprocessing (official)** | OCR → Markdown (lines/text/imgs/formulas) | `Papers/Ocr-markdown/{会考,合格考,…}/*.md` |
| **L1 Annotation/manifest** | unit_id, stem/options/answer **line spans + labels** | `*.manifest.json` (reslice_pipeline + LLM) |
| **L2 V3 consumer** | manifest+md → annotation payload → Resolver → IR → Compile → Gate | `preprocessing_consumer` + `app/domains/*` |

**Input transport fact:** for 2018 spring chemistry,
`Ocr-markdown/会考/化学/*.md` and Phase 1 `reslice-batch-C/会考/化学/*.md`
are **byte-identical** (same SHA256). Transport does **not** mutate text.

**Architecture classification:** **Architecture B** —
preprocessing = document normalization; **structure is a later annotation layer**.
V3 does not re-OCR; it consumes declared structure + source lines.

**Critical:** Phase 1 runs on **experimental** `reslice-batch-C`, not the formal
TaskExecutor production path. These symptoms are **not yet proven** to be formal V3 product defects.

## 2. Four questions + golden (actual text per layer)

### Chemistry Q20 — cross-line option D
Source (official = Phase 1):
```
157: D. 硫在自然界的循环过程中，涉及了氧
158:
159: 还原反应
```
True option D = 「涉及了**氧化还原**反应」(OCR line-wrap).

| Layer | Content |
|-------|---------|
| Preprocessing MD | D split L157+L159; **no E in text** |
| Manifest **before** P1.4-B (bak) | A,B,C,D (D only at L157) |
| Manifest **after** P1.4-B | A,B,C,**D,E** — **E = 还原反应 (FALSE)** |
| V3 leaf | labels A,B,C,D,E |
| Gate | auto_approve (answer B) |

**First change layer:** **P1.4-B Rule A** treated L159 as trailing option → invented E.
**Responsibility:** **P1.4-B Rule A (our checkpoint)** + original Producer D span incomplete.
**This is a product-risk defect we introduced.**

### Math Q4 — `2D.`
| Layer | Content |
|-------|---------|
| MD | `C. …对称 2D. 关于直线…` |
| Manifest before | A,B,C |
| Manifest after P1.4-B | A,B,C,D (Rule B) |
| Answer | teacher block → letter=None |
| Gate | pending (unchanged, as simulated) |

**Responsibility:** option labels repaired; Gate blocker is **answer-slice (S0 family)** — out of P1.4-B scope.

### Chemistry Q23 — trailing unlabeled D
| Layer | Content |
|-------|---------|
| MD | L194 ionic equation, **no `D．` token** (OCR dropped label) |
| Manifest before | A,B,C |
| After | A,B,C,D |
| Gate | pending → **auto (+1 measured)** |

**Responsibility:** Preprocessing dropped label glyph; recovery via Rule A.

### History Q29 — `D 麦哲伦`
| Layer | Content |
|-------|---------|
| MD | `D 麦哲伦` (missing `.`) |
| After P1.4-B | A,B,C,D |
| Gate | auto → auto (completeness only) |

### Chemistry Q22 GOLDEN
Normal A./B./C./D. → A,B,C,D → auto. **No defect.** Golden path holds for clean input.

## 3. Responsibility matrix

| Q | Preproc output | V3 input MD | First change | Final symptom | Responsibility layer |
|---|----------------|-------------|--------------|---------------|----------------------|
| Q20 | D跨行续文正确，无E | byte-identical | **P1.4-B Rule A** | 虚假 E | **V3 Producer (p14b Rule A)** |
| Q4 | `2D.` 在文中 | byte-identical | annotation 漏 D / p14b 补 | labels全，answer仍None | No option defect after repair；answer-side 独立 |
| Q23 | 4th content 无标签 | byte-identical | annotation 漏 D / p14b 补 | +1 auto | Preprocessing 标签字形 + Producer 恢复 |
| Q29 | `D 麦哲伦` 缺点 | byte-identical | annotation 漏 D / p14b 补 | completeness | Preprocessing 分隔符 + Producer 恢复 |
| Q22 golden | 正常 | byte-identical | 无 | auto | **No defect** |

## 4. Acceptance levels
- **L1 data correct: PARTIAL FAIL** — Q20 was made **worse** by our Rule A
- **L2 product correct: not assessed** (no frontend)
- **L3 governance: frozen**

## 5. Proven vs NOT proven
**Proven:** MD transport clean; structure lives in manifest; Q20 E is P1.4-B artifact; Q23 +1 real.
**Not proven:** reslice_pipeline == formal V3 integration; formal TaskExecutor path has same symptoms; frontend correctness.

## 6. Recommendation (for Owner — no action taken)
1. Keep P1.4-B frozen.
2. **Rule A as-is must not ship** — it fabricates options from cross-line continuations (Q20).
3. Next: formal raw→preprocessing→V3 TaskExecutor E2E on 4 questions + golden. Then decide blame.
