# Template: Architecture Document

## Description

Template for creating complete architecture documents for each Part of Maxwell's Treatise. This template ensures consistent structure, comprehensive coverage, and proper documentation across all architecture maps.

## Structure

```markdown
# Maxwell's Treatise: Modernized Architecture Map
## Part {PART_NUMBER}: {PART_NAME} — COMPLETE EDITION

**Version:** {VERSION}  
**Coverage:** {COVERAGE_PERCENTAGE}% of Articles {ARTICLE_RANGE}  
**Author:** {AUTHOR}  
**Date:** {DATE}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Articles** | {ARTICLE_COUNT} ({ARTICLE_RANGE}) |
| **Chapters** | {CHAPTER_COUNT} |
| **Layers** | {LAYER_COUNT} (Layers {LAYER_RANGE}) |
| **Modules** | {MODULE_COUNT} |
| **Coverage** | {COVERAGE_PERCENTAGE}% |

### Part {PART_NUMBER} Scope

{Brief description of what this Part covers and its role in the overall treatise}

### Key Concepts

- {Key concept 1}
- {Key concept 2}
- {Key concept 3}

---

## Package Directory Structure

```
maxwell/
├── {package}/                   # [{Part}, Layers {LAYER_RANGE}] {Description}
│   ├── __init__.py
│   ├── {module1}.py             # Arts. {ARTICLE_RANGE}: {Description}
│   ├── {module2}.py             # Arts. {ARTICLE_RANGE}: {Description}
│   └── {subpackage}/
│       ├── __init__.py
│       └── {module3}.py         # Arts. {ARTICLE_RANGE}: {Description}
```

---

## Layer {N}: {LAYER_NAME}

**Source:** Chapter {CHAPTER}, Arts. {ARTICLE_RANGE}  
**Goal:** {Layer goal description}

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| {ARTICLE} | {TITLE} | `{MODULE_PATH}` | `{CLASS_FUNCTION}` |

---

## Article Coverage Index

### Complete Article-to-Module Lookup Table

| Art. | Chapter | Title (Abbreviated) | Module Path |
|------|---------|---------------------|-------------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE_PATH} |

---

## Implementation Priority Matrix

### Phase {PHASE}: {PHASE_NAME} ({WEEKS} weeks)

| Priority | Module | Articles | Justification |
|----------|--------|----------|---------------|
| P{PRIORITY} | {MODULE} | {ARTICLES} | {JUSTIFICATION} |

---

## Validation Checklist

- [ ] All {ARTICLE_COUNT} articles mapped
- [ ] All sub-articles mapped
- [ ] No orphaned articles
- [ ] Layer dependencies are acyclic
- [ ] Module names reflect Maxwell's terminology
- [ ] Function signatures follow modern Python conventions
- [ ] Documentation references original article numbers

---

## Version History

| Version | Date | Changes |
|---------|------------|---------|
| {VERSION} | {DATE} | {CHANGES} |

---

**END OF DOCUMENT**
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{PART_NUMBER}` | Roman numeral (I-VI) | I |
| `{PART_NAME}` | Part name | Electrostatics |
| `{VERSION}` | Document version | 2.0 |
| `{ARTICLE_RANGE}` | Article number range | 27-229 |
| `{ARTICLE_COUNT}` | Number of articles | 203 |
| `{CHAPTER_COUNT}` | Number of chapters | 13 |
| `{LAYER_COUNT}` | Number of layers | 13 |
| `{LAYER_RANGE}` | Layer number range | 0-12 |
| `{MODULE_COUNT}` | Number of modules | 52 |
| `{COVERAGE_PERCENTAGE}` | Coverage percentage | 100 |
| `{AUTHOR}` | Document author | Technical Architecture Review |
| `{DATE}` | Document date | December 2024 |

## Usage Instructions

1. Copy this template to new architecture document
2. Replace all `{VARIABLES}` with actual values
3. Fill in directory structure for the Part
4. Create layer sections for each layer
5. Populate article-to-module mappings
6. Define implementation priorities
7. Complete validation checklist
8. Add version history entry

## Related Templates

- `dependency-map.md` - Cross-part dependency documentation
- `coverage-report.md` - Coverage report format
- `version-change-log.md` - Version history template

## Example Usage

```markdown
# Maxwell's Treatise: Modernized Architecture Map
## Part I: Electrostatics — COMPLETE EDITION

**Version:** 2.0 (Corrected & Comprehensive)  
**Coverage:** 100% of Articles 27-229 (203 base articles + 45 sub-articles)  
**Author:** Technical Architecture Review  
**Date:** December 2024

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Articles** | 203 (Arts. 27-229) |
| **Chapters** | 13 |
| **Layers** | 13 (Layers 0-12) |
| **Modules** | 52 |
| **Coverage** | 100% |
```
