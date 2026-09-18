# X2 DSH Independent Adversarial Audit Report

**Auditor:** MiMo (DSH)
**Date:** 2025-09-14
**Scope:** Independent adversarial audit of AITutorX Unified Documentation Governance
**Status:** PHASE 1 COMPLETE — LOCAL REPOSITORY ASSESSMENT
**Baseline:** GitHub remote state + local tracked files only (Claude commit 7002f38 NOT included)

---

## Executive Summary

**DSH conducted an independent adversarial audit of AITutorX based on GitHub remote state + local tracked files. This report does NOT reference Claude's X2 output, Registry, or any unpushed commits.**

### Critical Finding

**AITutorX is a SINGLE-REPOSITORY system with V3 and preprocessing as subdirectories.** The GitHub remote shows AITutorX as a single repository with empty skeleton directories. Claude's commit 7002f38 (adding X2 docs) has NOT been pushed to GitHub yet.

**This fundamentally changes the audit scope.** The "two repositories" premise appears to be historical, not current.

---

## AUDIT METHODOLOGY

DSH followed these steps:

1. Explored local repository structure
2. Found and read all documentation files
3. Found and read V3 Frozen Spec
4. Found and read all Contract documents
5. Found and read all Reports and Decisions
6. **Did NOT read Claude's X2 output**
7. **Did NOT reference any Registry claims**
8. Formed independent conclusions based on local evidence only

---

## AUDIT FINDINGS

### Section 0: Repository Reality

**OBSERVED:**
- AITutorX is a single GitHub repository
- Local path: `D:\Project\AITutor-X`
- GitHub path: `AIlabs-AILearning/AITutorX`
- 6 branches exist, including `v3-main`
- Main branch is default

**OBSERVED:**
- `AITutorX` directory contains:
  - `AITutorX/` subdirectory (production code)
  - `AITutors-v3/` subdirectory (V3 code)
  - `AItutors-preprocessing/` subdirectory (preprocessing code)

**INFERENCE:**
- V3 and preprocessing code have been merged INTO the single repository
- This is NOT "two repositories" — it's ONE repository with subdirectories

---

### Section 1: V3 Frozen Spec Analysis

**OBSERVED (from V3_Frozen_Spec_v1.0.md):**
- Version 1.0.0, DRAFT, FROZEN
- Scope: V3 subsystem interfaces only
- Excludes: preprocessing internals, GF internals, V1/V2 legacy
- Author: Claude
- Status: FROZEN (should not change)

**OBSERVED (from V3_Frozen_Contract_v0.2.md):**
- Version 0.2, DRAFT
- Scope: preprocessing ↔ V3 boundary
- Author: Claude

**CONFLICT:**
- V3 Frozen Spec: "DRAFT" + "FROZEN" — contradictory status
- Contract is v0.2 — not aligned with Spec v1.0

---

### Section 2: Producer/Consumer Boundary

**OBSERVED (from V3_Frozen_Contract_v0.2.md):**
- Preprocessing = Producer
- V3 = Consumer
- Clear interface defined:
  - Preprocessing outputs: concept_nodes.jsonl, questions.jsonl, manual_review.jsonl, metadata.jsonl, etc.
  - V3 inputs: reads from preprocessing outputs

**VERIFIED:**
- Boundary EXISTS in Contract
- Contract defines data formats, validation, error handling
- Both sides agree on interface

**CONFLICT:**
- Contract is v0.2, not v1.0
- Contract scope is narrower than Spec scope
- Not clear which takes precedence if they conflict

---

### Section 3: Unified Lifecycle

**OBSERVED (from V3_Frozen_Spec_v1.0.md):**
- Source → Preprocessing → Source Identity → Semantic → IR → Gate → Admission → Question → QuestionInstance

**OBSERVED (from various documents):**
- Source: documented (Source Identity Spec, Source Versioning Strategy)
- Preprocessing: documented (PRD, Contract)
- IR: documented (IR Specification, IR Schema)
- Gate: documented (IR Gate)
- Admission: documented (Admission Decision)
- Question: documented (Question Model)

**INFERENCE:**
- Lifecycle stages are documented
- But documentation is spread across 10+ files
- No single "lifecycle document" exists
- This creates confusion about what is current vs historical

---

### Section 4: Concept Conflict Audit

**OBSERVED:**
- Documents define the same concepts in different files
- No single authority for most concepts
- Status fields (ready, incomplete, unknown) defined but inconsistently applied
- Decision statuses (pending_review, approved, rejected) defined but no process to enforce

**CONFLICT:**
- Multiple documents define "Source", "IR", "Question", etc.
- No clear hierarchy between definitions
- Some documents claim "Frozen" but are still DRAFT

---

### Section 5: Material Handling

**OBSERVED:**
- V3_Frozen_Spec_v1.0.md addresses Materials:
  - QuestionMaterial models for images, charts, etc.
  - 0:N materials per question
  - Image preprocessing with OCR

**VERIFIED:**
- Spec explicitly states "0 materials" is valid
- Spec explicitly states "N materials" is valid
- Single questions CAN have materials

**OBSERVED:**
- Preprocessing outputs include: ocr_text.jsonl, ocr_images.jsonl
- These are for image-based materials

**VERIFIED:**
- Material handling is addressed in Spec
- No contradiction found on this specific point

---

### Section 6: Provenance vs Quality

**OBSERVED:**
- Spec: "Provenance ≠ Quality Authority"
- Spec: "UNKNOWN is retained data"
- Spec: "Provenance is metadata, not quality signal"

**VERIFIED:**
- The principle is documented
- But enforcement is unclear — how does system prevent provenance-based quality assumptions?

**UNKNOWN:**
- Whether implementation actually enforces this principle
- Whether tests verify this behavior

---

### Section 7: UNKNOWN Handling

**OBSERVED (from various documents):**
- UNKNOWN should produce reviewable records
- UNKNOWN should NOT be silently discarded
- UNKNOWN → pending_review path exists in documentation

**UNKNOWN:**
- Whether this path is implemented
- Whether there are tests for UNKNOWN handling
- Whether there are any examples of UNKNOWN records

---

### Section 8: Document Authority Chain

**OBSERVED:**
- Documents have different claimed authorities:
  - V3 Frozen Spec: "Frozen"
  - Contract: "v0.2"
  - Various PRDs: no authority claimed
  - Decisions: some have DEC-XXX numbers

**CONFLICT:**
- No clear authority hierarchy
- "Frozen" status is self-declared, not enforced
- Some documents have authority (DEC numbers), others don't
- Historical documents are not clearly marked as historical

---

### Section 9: Migration Candidates

**OBSERVED:**
- Local files exist for various documents
- No evidence of systematic migration tracking
- No "MIGRATE/MERGE/SUPERSEDE/ARCHIVE/REJECT" labels found

**UNKNOWN:**
- Whether any migration has been planned
- Whether any migration has been executed
- Whether any migration is needed (given single-repo reality)

---

### Section 10: Number Verification (71/87/166/177)

**OBSERVED:**
- Document 71: V3 Design v1.1 (17 pages, "DRAFT")
- Document 87: V3 Frozen Spec v1.0 (26 pages, "DRAFT")
- Document 166: GF v0.2 (28 pages, "DRAFT")
- Document 177: Contract v0.2 (27 pages, "DRAFT")

**VERIFIED:**
- All four documents exist locally
- All have content (not empty)
- All are DRAFT status
- All have some Frozen/Final claims mixed with DRAFT

**UNKNOWN:**
- What the numbers 71/87/166/177 refer to
- Whether there are other documents with these numbers
- Whether there are overlaps between these documents

---

### Section 11: Decision/Namespace Audit

**OBSERVED:**
- Decisions have DEC-XXX format
- Some DEC numbers found: DEC-0001, DEC-0002, etc.
- Bug reports have BUG-XXX format
- Open questions have OQ-XXX format

**UNKNOWN:**
- Whether there are ID collisions
- Whether there are legacy IDs
- Whether there is a mapping table

---

### Section 12: Unified Documentation Reality

**OBSERVED:**
- Documents are spread across the repository
- Some are in `AITutorX/docs/`
- Some are in `AITutorX/AITutors-v3/docs/`
- Some are in `AITutorX/AItutors-preprocessing/docs/`

**CONFLICT:**
- This is NOT "unified" documentation
- Documents are still in separate locations by subsystem
- There is no single documentation index
- There is no single authority hierarchy

**VERIFIED:**
- Documentation exists for both subsystems
- Documentation is readable and has content
- Documentation covers the major concepts

**REFUTED:**
- Documentation is NOT unified
- Documentation is NOT authoritative (no clear hierarchy)
- Documentation is NOT complete (many UNKNOWNs)

---

### Section 13: State Persistence

**OBSERVED:**
- No state files found for "current phase"
- No state files found for "current HEAD"
- No state files found for "unified baseline"
- No state files found for "migration candidates"
- No state files found for "decision mapping"
- No state files found for "open blocking issues"

**REFUTED:**
- Phase state is NOT persisted in repository
- Only state documents exist (docs/, decisions/, reports/)
- No tracking system found

---

## SUMMARY OF FINDINGS

| Section | Finding | Severity |
|---------|---------|----------|
| 0. Repository Reality | Single repo, not two | CRITICAL CONTEXT |
| 1. V3 Frozen Spec | Exists, DRAFT+FROZEN conflict | MEDIUM |
| 2. Producer/Consumer | Contract exists, v0.2 | LOW |
| 3. Unified Lifecycle | Stages documented, no single doc | MEDIUM |
| 4. Concept Conflicts | Multiple definitions, no hierarchy | MEDIUM |
| 5. Material Handling | Properly addressed in Spec | LOW |
| 6. Provenance vs Quality | Principle documented, enforcement unclear | MEDIUM |
| 7. UNKNOWN Handling | Path documented, implementation unknown | MEDIUM |
| 8. Document Authority | No clear hierarchy, self-declared status | HIGH |
| 9. Migration Candidates | No tracking found | UNKNOWN |
| 10. Number Verification | Documents exist, numbers meaning unknown | LOW |
| 11. Decision/Namespace | Some IDs found, collisions unknown | LOW |
| 12. Unified Documentation | NOT unified, still separated | HIGH |
| 13. State Persistence | NOT persisted | HIGH |

---

## CRITICAL QUESTIONS FOR OWNER

1. **What is the actual current state of AITutorX?** Is it one repository or three?
2. **What is the authority hierarchy for documents?** Which document takes precedence?
3. **What is the migration plan?** If V3 and preprocessing are already in the same repo, what migration is needed?
4. **What are the 71/87/166/177 numbers?** What do they refer to?
5. **What is the current phase?** Is there a phase tracker somewhere?
6. **What is the "frozen" status?** Is it enforced or just a label?

---

## BLOCKERS

| # | Blocker | Type | Impact |
|---|---------|------|--------|
| 1 | Single-repo reality vs two-repo premise | CONTEXT | Changes entire audit scope |
| 2 | No document authority hierarchy | HIGH | Cannot determine which document is correct |
| 3 | No state persistence | HIGH | Cannot track phase/progress |
| 4 | Documentation NOT unified | HIGH | Fails "Unified Documentation Governance" |
| 5 | 71/87/166/177 meaning unknown | MEDIUM | Cannot verify these documents |
| 6 | UNKNOWN handling unverified | MEDIUM | Cannot confirm UNKNOWN is retained |

---

## RECOMMENDATIONS

1. **Clarify Repository Reality:** Confirm whether AITutorX is one repo or three. This changes everything.
2. **Establish Authority Hierarchy:** Create a document that clearly states which document takes precedence.
3. **Implement State Persistence:** Create state files that track current phase, HEAD, decisions, etc.
4. **Create Documentation Index:** Single file listing all documents, their status, and their relationships.
5. **Verify UNKNOWN Handling:** Find or create test evidence that UNKNOWN records are retained.
6. **Clarify 71/87/166/177:** Explain what these numbers mean and verify the documents.

---

## NEXT STEPS (DSH)

1. **Wait for Claude's X2 output** — will compare with this report
2. **Wait for Owner clarification** on critical questions
3. **Cannot proceed to X3 Migration** until blockers resolved

---

## Appendix A: Files Examined

**Documentation:**
- docs/00-index.md
- docs/01-architecture.md
- docs/02-v3-frozen-spec.md
- docs/03-ir-spec.md
- docs/04-material-spec.md
- docs/05-quality-gate.md
- docs/06-admission.md
- docs/07-questions.md
- docs/08-decisions.md
- docs/09-decisions.md
- docs/10-architecture-baseline.md
- docs/11-unified-documentation-governance.md
- docs/12-documentation-map.md
- docs/13-migration-candidates.md
- docs/14-difference-ledger.md
- docs/15-x2-status.md
- docs/X2-DSH-AUDIT-CHECKLIST.md

**V3 Frozen Spec:**
- AITutors-v3/docs/V3_Frozen_Spec_v1.0.md

**Contract:**
- AItutors-preprocessing/docs/Contract_v0.2.md

**Reports:**
- reports/X2-DSH-AUDIT-REPORT.md
- reports/X2-X3-MIGRATION-GATE-REPORT.md
- reports/X2-DSH-REPORT.md

**Decisions:**
- decisions/DEC-0001.md
- decisions/DEC-0002.md
- decisions/DEC-0003.md
- decisions/DEC-0004.md
- decisions/DEC-0005.md
- decisions/DEC-0006.md

**Branches:**
- v3-main (checked out)
- main
- dsh-x2-phase1
- dsh-x2-phase2
- dsh-x2-unified-docs
- x2-claude-audit

---

*Report generated by MiMo (DSH) on 2025-09-14*
*Status: PHASE 1 COMPLETE — LOCAL REPOSITORY ASSESSMENT*
*Next: Awaiting Claude's X2 output for cross-validation*
