# Template: Master Index

## Description

Template for generating the unified master index of all Maxwell Treatise articles mapped to their modern Python module implementations. This template ensures consistent indexing across all Parts.

## Structure

```markdown
# Maxwell Treatise Master Index

## Index Metadata

**Generated:** {DATE}  
**Architecture Version:** {ARCH_VERSION}  
**Total Articles:** {TOTAL_ARTICLES}  
**Total Modules:** {TOTAL_MODULES}  
**Parts Covered:** {PARTS_COVERED}

---

## Quick Reference

### Article Ranges by Part

| Part | Domain | Article Range | Layer Range |
|------|--------|---------------|-------------|
| I | Electrostatics | 27-229 | 0-12 |
| II | Electrokinematics | 230-370 | 13-30 |
| III | Magnetism | 371-521 | 30b-42 |
| IV | Electromagnetism | 522-710 | 43-86 |
| V | System Core | 711-780 | 90-94 |
| VI | Scalar Physics | 781-866 | 95-97 |

---

## Part I: Electrostatics (Articles 27-229)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Part II: Electrokinematics (Articles 230-370)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Part III: Magnetism (Articles 371-521)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Part IV: Electromagnetism (Articles 522-710)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Part V: System Core (Articles 711-780)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Part VI: Scalar Physics (Articles 781-866)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| {ARTICLE} | {CHAPTER} | {TITLE} | {MODULE} | {LAYER} | {STATUS} |

---

## Appendices

| Article | Title | Module Path | Status |
|---------|-------|-------------|--------|
| {ARTICLE} | {TITLE} | {MODULE} | {STATUS} |

---

## Reverse Index: Module to Article

### By Module Path

| Module Path | Articles Covered | Part | Layer |
|-------------|------------------|------|-------|
| `maxwell/core/charge.py` | 27-35, 54 | I | 1 |
| `maxwell/core/fields.py` | 44-49 | I | 4 |
| `maxwell/physics/potential.py` | 69-73 | I | 2 |

---

## Index by Layer

### Layer 0: Units, Dimensions & Configuration

| Article | Title | Module | Part |
|---------|-------|--------|------|
| {ARTICLE} | {TITLE} | {MODULE} | {PART} |

### Layer 1: Core Primitives

| Article | Title | Module | Part |
|---------|-------|--------|------|
| {ARTICLE} | {TITLE} | {MODULE} | {PART} |

---

## Status Legend

| Status | Meaning | Count |
|--------|---------|-------|
| ✅ Implemented | Module exists and functional | {COUNT} |
| 🔄 Mapped | Module assigned, pending implementation | {COUNT} |
| ❌ Unmapped | No module assignment | {COUNT} |
| ⚠️ Partial | Module partially implemented | {COUNT} |

---

## Search Guide

### By Article Number

```bash
# Find article by number
architectus search-index --article {NUMBER}
```

### By Module

```bash
# Find articles in module
architectus search-index --module {MODULE_PATH}
```

### By Layer

```bash
# Find articles in layer
architectus search-index --layer {LAYER_NUMBER}
```

### By Topic

```bash
# Find articles about topic
architectus search-index --topic "{TOPIC}"
```

---

## Cross-References

### Related Articles

| Article | Related To | Relationship |
|---------|------------|--------------|
| {ARTICLE} | {RELATED} | {RELATIONSHIP} |

### See Also

- Article 70: Electric potential (Part I, Layer 2)
- Article 339: Current sheet (Part II, Layer 21)
- Article 412: Magnetic potential (Part III, Layer 35)

---

## Version History

| Version | Date | Changes |
|---------|------------|---------|
| {VERSION} | {DATE} | {CHANGES} |

---

**END OF INDEX**
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{DATE}` | Index generation date | 2026-04-11 |
| `{ARCH_VERSION}` | Architecture version | 2.0.0 |
| `{TOTAL_ARTICLES}` | Total article count | 885 |
| `{TOTAL_MODULES}` | Total module count | 313 |
| `{PARTS_COVERED}` | Number of parts | 6 |
| `{ARTICLE}` | Article number | 27 |
| `{CHAPTER}` | Chapter number | I |
| `{TITLE}` | Article title | Electrification by friction |
| `{MODULE}` | Module path | maxwell/core/charge.py |
| `{LAYER}` | Layer number | 1 |
| `{STATUS}` | Implementation status | Implemented |

## Usage Instructions

1. Copy this template to new index document
2. Run master index generation command
3. Populate all Part sections
4. Generate reverse index
5. Create layer-based index
6. Add cross-references
7. Update version history

## Related Templates

- `coverage-report.md` - Coverage report template
- `architecture-document.md` - Architecture documentation

## Example Index Entry

```markdown
## Part I: Electrostatics (Articles 27-229)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| 27 | I | Electrification by friction | maxwell/core/charge.py | 1 | ✅ |
| 28 | I | Electrification by induction | maxwell/core/charge.py | 1 | ✅ |
| 29 | I | Conduction; conductors | maxwell/core/materials.py | 1 | ✅ |
| 30 | I | Conservation of charge | maxwell/core/charge.py | 1 | ✅ |
| 74a | II | Cavendish modified experiment | maxwell/tests/verify_cavendish.py | 13 | ✅ |
| 74b | II | Theoretical basis | maxwell/tests/verify_cavendish.py | 13 | ✅ |
```
