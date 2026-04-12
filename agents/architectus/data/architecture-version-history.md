# Data: Architecture Version History

## Description

Authoritative version tracking for all architecture changes across the Maxwell Treatise modernization. This document maintains the complete history of architecture versions and changes.

---

## Current Version

**Version:** 2.1.0  
**Release Date:** 2026-04-11  
**Status:** Current/Stable  
**Architecture Lead:** ARCHITECTUS Agent

---

## Version History

### [2.1.0] - 2026-04-11

**Change Type:** MINOR

**Summary:**
ARCHITECTUS agent ecosystem completion with 35 total components.

**Added:**
- 7 commands: validate-architecture, audit-coverage, check-dependencies, generate-master-index, review-layer-mapping, sync-agents, pipeline-orchestrate
- 6 tasks: full-treatise-audit, cross-part-dependency-verification, architecture-version-bump, master-index-generation, gap-analysis, consolidation-report
- 7 templates: architecture-document, dependency-map, coverage-report, master-index, pipeline-status, version-change-log, agent-coordination
- 6 checklists: architecture-completeness, cross-part-consistency, layer-numbering-integrity, article-coverage-audit, agent-readiness, pipeline-execution
- 5 data files: complete-treatise-index, layer-numbering-scheme, cross-part-dependency-graph, architecture-version-history, agent-domain-boundaries
- 3 utilities: coverage_counter.py, dependency_checker.py, index_generator.py

**Changed:**
- ARCHITECTUS agent.md rewritten to reflect Architecture Management domain (not DevOps)

**Affected Agents:**
- All agents: New coordination capabilities

---

### [2.0.0] - 2026-01-15

**Change Type:** MAJOR

**Summary:**
Complete architecture revision with full 6-Part coverage and layer scheme update.

**Added:**
- Part V: System Core (Layers 90-94)
- Part VI: Scalar Physics (Layers 95-97)
- Complete layer numbering scheme (0-97)
- Cross-part dependency graph

**Changed:**
- Part IV layer range expanded (43-86)
- Part III layer numbering adjusted (30b-42)
- Part II layer range adjusted (13-30)

**Breaking Changes:**
- Layer renumbering for Parts III-VI
- Module path updates for all parts

**Migration Notes:**
- Update all layer references
- Update module import paths
- Regenerate agent knowledge bases

---

### [1.5.3] - 2025-12-01

**Change Type:** PATCH

**Summary:**
Article mapping corrections for Part I.

**Fixed:**
- Article 74a-e mapping corrected to verification tests
- Article 78a-c mapping corrected to boundary module
- Article 89a-e mapping corrected to constraints module
- Article 101a-h mapping corrected to anisotropic module

**Affected Modules:**
- `maxwell/tests/verify_cavendish.py`
- `maxwell/physics/boundary.py`
- `maxwell/systems/constraints.py`
- `maxwell/solvers/anisotropic.py`

---

### [1.5.0] - 2025-11-15

**Change Type:** MINOR

**Summary:**
Part V System Core architecture added.

**Added:**
- Part V initial architecture (Layers 90-94)
- System initialization modules
- Pipeline orchestration framework

---

### [1.0.0] - 2025-01-01

**Change Type:** MAJOR

**Summary:**
Initial architecture release for Part I: Electrostatics.

**Added:**
- Part I complete architecture (Layers 0-12)
- 203 base articles mapped
- 45+ sub-articles mapped
- 52 modules defined

**Foundation:**
- Layer 0: Units, Configuration
- Layer 1: Core Primitives
- Layer 2: Basic Physics Engine
- Layer 3: System Manager
- Layer 4: Advanced Solvers
- Layer 5: Field Analysis
- Layer 6: Visualization
- Layer 7: Components
- Layer 8: Spherical Harmonics
- Layer 9: Ellipsoidal Coordinates
- Layer 10: Image Methods
- Layer 11: 2D Complex Analysis
- Layer 12: Instrumentation

---

## Version Statistics

### Articles Tracked

| Version | Part I | Part II | Part III | Part IV | Part V | Part VI | Total |
|---------|--------|---------|----------|---------|--------|---------|-------|
| 2.1.0 | 248 | 153 | 151 | 189 | 70 | 86 | 897 |
| 2.0.0 | 248 | 153 | 151 | 189 | 70 | 86 | 897 |
| 1.5.3 | 248 | 153 | 151 | 189 | - | - | 741 |
| 1.0.0 | 248 | - | - | - | - | - | 248 |

### Modules Defined

| Version | Part I | Part II | Part III | Part IV | Part V | Part VI | Total |
|---------|--------|---------|----------|---------|--------|---------|-------|
| 2.1.0 | 52 | 48 | 45 | 118 | 22 | 28 | 313 |
| 2.0.0 | 52 | 48 | 45 | 118 | 22 | 28 | 313 |
| 1.5.3 | 52 | 48 | 45 | 118 | - | - | 263 |
| 1.0.0 | 52 | - | - | - | - | - | 52 |

### Layers Defined

| Version | Part I | Part II | Part III | Part IV | Part V | Part VI | Total |
|---------|--------|---------|----------|---------|--------|---------|-------|
| 2.1.0 | 13 | 18 | 13 | 44 | 5 | 3 | 96 |
| 2.0.0 | 13 | 18 | 13 | 44 | 5 | 3 | 96 |
| 1.5.3 | 13 | 18 | 13 | 44 | - | - | 88 |
| 1.0.0 | 13 | - | - | - | - | - | 13 |

---

## Git Tags

| Tag | Version | Date | Commit |
|-----|---------|------|--------|
| architecture-v2.1.0 | 2.1.0 | 2026-04-11 | {COMMIT} |
| architecture-v2.0.0 | 2.0.0 | 2026-01-15 | {COMMIT} |
| architecture-v1.5.3 | 1.5.3 | 2025-12-01 | {COMMIT} |
| architecture-v1.5.0 | 1.5.0 | 2025-11-15 | {COMMIT} |
| architecture-v1.0.0 | 1.0.0 | 2025-01-01 | {COMMIT} |

---

## Deprecation Schedule

| Version | Deprecated | End of Support | Reason |
|---------|------------|----------------|--------|
| 1.0.0 | 2025-01-01 | 2025-06-01 | Superseded by 1.5.0 |
| 1.5.0 | 2025-11-15 | 2026-01-01 | Superseded by 2.0.0 |
| 1.5.3 | 2025-12-01 | 2026-01-15 | Superseded by 2.0.0 |
| 2.0.0 | 2026-01-15 | Active | Current stable |
| 2.1.0 | - | Active | Current |

---

## Change Request Process

### Submitting a Change

1. Create change request document
2. Specify change type (MAJOR/MINOR/PATCH)
3. List affected modules and articles
4. Get architecture review approval
5. Implement changes
6. Update version number
7. Create git tag
8. Sync all agents

### Change Type Guidelines

**MAJOR (breaking):**
- Layer renumbering
- Part restructuring
- Module path changes
- Interface changes

**MINOR (new features):**
- New layers added
- New modules added
- New article mappings
- Backward-compatible changes

**PATCH (bug fixes):**
- Article mapping corrections
- Documentation fixes
- Typos and clarifications
- Non-breaking updates

---

## Version Comparison

### v2.0.0 → v2.1.0

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Components | 1 | 35 | +34 |
| Commands | 0 | 7 | +7 |
| Tasks | 0 | 6 | +6 |
| Templates | 0 | 7 | +7 |
| Checklists | 0 | 6 | +6 |
| Data Files | 0 | 5 | +5 |
| Utilities | 0 | 3 | +3 |

---

## Release Checklist

For each version release:

- [ ] Architecture documents updated
- [ ] Version numbers incremented in all files
- [ ] Changelog entry created
- [ ] Agent knowledge synced
- [ ] Git tag created and signed
- [ ] Release notes published
- [ ] Stakeholders notified
- [ ] Deprecation notices issued (if applicable)

---

**END OF VERSION HISTORY**
