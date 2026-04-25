# Data: scriba-reference-guide

## Purpose

Comprehensive reference guide for SCRIBA agent operations and documentation generation.

---

## SCRIBA Agent Overview

### Purpose

SCRIBA is the documentation specialist for the Maxwell Treatise Modernization Project, responsible for:
- API documentation generation
- Tutorial creation
- Cross-reference linking
- Citation management
- Release notes generation
- Version history maintenance
- Documentation validation

### Core Capabilities

| Capability | Command | Description |
|------------|---------|-------------|
| API Documentation | generate-api-docs | Generate API reference docs |
| Tutorial Creation | create-tutorial | Create educational tutorials |
| Cross-Reference | generate-cross-reference | Generate cross-references |
| Citation Linking | link-citations | Link and manage citations |
| Release Notes | generate-release-notes | Generate release documentation |
| Version History | update-version-history | Maintain version history |
| Documentation Validation | validate-documentation | Validate documentation quality |

---

## Documentation Generation Workflows

### API Documentation Workflow

```
1. Identify module/functions to document
2. Extract function signatures and parameters
3. Document CGS units for all quantities
4. Add Maxwell article citations
5. Include theory classification
6. Generate working code examples
7. Validate documentation completeness
```

### Tutorial Creation Workflow

```
1. Define learning objectives
2. Identify prerequisites
3. Map to Maxwell articles
4. Create step-by-step instructions
5. Develop working examples (CGS units)
6. Add exercises and solutions
7. Include summary and next steps
```

### Cross-Reference Generation Workflow

```
1. Identify source documents
2. Extract Maxwell article citations
3. Build article-to-document mapping
4. Create document-to-article mapping
5. Generate topic index
6. Build citation network
7. Validate all links functional
```

### Citation Linking Workflow

```
1. Scan documents for citations
2. Verify article numbers accurate
3. Link citations to reference list
4. Create bidirectional links
5. Generate citation index
6. Validate citation format
7. Update citation statistics
```

---

## Template Quick Reference

### Available Templates

| Template | Purpose | Key Variables |
|----------|---------|---------------|
| api-documentation-template | API reference | {{MODULE_NAME}}, {{MAXWELL_ARTICLES}} |
| tutorial-documentation-template | Tutorials | {{DIFFICULTY}}, {{LEARNING_OBJECTIVES}} |
| cross-reference-template | Cross-references | {{REFERENCE_TYPE}}, {{LINKED_DOCUMENTS}} |
| citation-linking-template | Citation management | {{CITATION_STYLE}}, {{TOTAL_CITATIONS}} |
| release-notes-template | Release notes | {{VERSION}}, {{CHANGE_SUMMARY}} |
| version-history-template | Version history | {{FIRST_RELEASE}}, {{TOTAL_RELEASES}} |
| documentation-validation-template | Validation | {{VALIDATION_LEVEL}}, {{SCORE}} |

### Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| {{VERSION}} | Version number | 1.0.0 |
| {{MAXWELL_ARTICLES}} | Article citations | Art. 730-750 |
| {{CGS_UNITS}} | Unit specification | statV, statA, statΩ |
| {{GENERATED_DATE}} | Generation date | 2024-01-15 |
| {{DIFFICULTY}} | Difficulty level | Intermediate |
| {{ESTIMATED_TIME}} | Time to complete | 30 minutes |

---

## Checklist Quick Reference

### Available Checklists

| Checklist | Purpose | Levels |
|-----------|---------|--------|
| documentation-quality-validation | Quality validation | 5 levels |
| maxwell-article-citation-validation | Citation validation | 5 levels |
| theory-classification-integrity | Classification integrity | 5 levels |
| cross-reference-linking | Link validation | 5 levels |
| version-control-documentation | Version control | 5 levels |
| documentation-completeness | Completeness check | 5 levels |

### Scoring System

| Level | Type | Points | Weight |
|-------|------|--------|--------|
| 1 | Required | 4-12 | 1.0x |
| 2 | Required | 4-12 | 1.0x |
| 3 | Required | 4-12 | 1.0x |
| 4 | Expert | 4-12 | 0.5x |
| 5 | Expert | 4-12 | 0.5x |

### Approval Thresholds

| Status | Score Range |
|--------|-------------|
| Approved | >= 90% |
| Conditional | 75-89% |
| Rejected | < 75% |

---

## CGS Unit Quick Reference

### Electrical CGS Units

| Quantity | Unit | Symbol | SI Equivalent |
|----------|------|--------|---------------|
| Potential | statvolt | statV | 299.79 V |
| Current | statampere | statA | 3.336×10^-10 A |
| Resistance | statohm | statΩ | 8.988×10^11 Ω |
| Charge | statcoulomb | statC | 3.336×10^-10 C |
| Capacitance | statfarad | statF | 1.113×10^-12 F |
| Magnetic field B | gauss | G | 10^-4 T |
| Magnetic field H | oersted | Oe | 79.577 A/m |

### Physical Constants

| Constant | Symbol | CGS Value |
|----------|--------|-----------|
| Speed of light | c | 2.998×10^10 cm/s |
| Boltzmann constant | k_B | 1.381×10^-16 erg/K |
| Elementary charge | e | 4.803×10^-10 statC |
| Planck constant | h | 6.626×10^-27 erg·s |

---

## Maxwell Citation Quick Reference

### Citation Format

**First citation:**
```
Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism 
(3rd ed.). Clarendon Press, Oxford. Part IV, Art. 730-750.
```

**Subsequent citations:**
```
(Maxwell, Art. 730-750)
Maxwell, Art. 730-750
```

### Article Ranges by Topic

| Topic | Articles | Part |
|-------|----------|------|
| Electrostatics | 1-229 | Part I |
| Electrokinematics | 230-370 | Part II |
| Magnetism | 371-474 | Part III |
| Electromagnetism | 475-866 | Part IV |
| Galvanometers | 730-750 | Part IV |
| Wheatstone Bridge | 343-348 | Part II |

---

## Theory Classification Quick Reference

### Classification Categories

| Classification | Description | Protection |
|----------------|-------------|------------|
| maxwell_original | Maxwell's 1873 text | Historical accuracy |
| user_original | User's extensions | **NEVER ALTER** |
| standard_math | Standard implementations | Technical accuracy |

### CRITICAL: User Original Protection

**NEVER:**
- Alter user_original content
- Falsify user_original content
- Misrepresent user_original content
- Confuse with Maxwell's text

**ALWAYS:**
- Mark user_original clearly
- Maintain authoritative status
- Preserve user's exact wording
- Respect user's theoretical contributions

---

## Version Control Quick Reference

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Incompatible changes
MINOR: Backward-compatible features
PATCH: Bug fixes
```

### Change Categories

| Category | Description |
|----------|-------------|
| Added | New features |
| Changed | Modified existing |
| Fixed | Bug fixes |
| Deprecated | Marked for removal |
| Removed | Deleted features |
| CGS | CGS unit changes |
| Maxwell | Citation changes |

---

## Quality Standards

### Documentation Quality

| Standard | Requirement |
|----------|-------------|
| CGS Units | ALWAYS primary |
| Maxwell Citations | Accurate article numbers |
| Theory Classification | Clearly marked |
| User Original | NEVER altered |
| Code Examples | Executable and tested |

### Validation Requirements

| Check | Frequency |
|-------|-----------|
| CGS unit compliance | Every document |
| Maxwell citation accuracy | Every document |
| Theory classification | Every document |
| Link validity | Every release |
| Completeness | Every release |

---

## Quick Start Guide

### Generate API Documentation

```
1. Use api-documentation-template
2. Fill in module details
3. Add CGS units for all quantities
4. Include Maxwell article citations
5. Mark theory classification
6. Validate with documentation-quality-validation
```

### Create Tutorial

```
1. Use tutorial-documentation-template
2. Define learning objectives
3. Map to Maxwell articles
4. Create step-by-step examples
5. Add exercises
6. Validate with documentation-completeness
```

### Generate Release Notes

```
1. Use release-notes-template
2. Document all changes
3. Highlight CGS unit changes
4. Note Maxwell coverage updates
5. Include migration guides (if needed)
6. Validate with version-control-documentation
```

---

## Quality Criteria

- [ ] All templates available and documented
- [ ] All checklists functional and validated
- [ ] CGS units used consistently
- [ ] Maxwell citations accurate
- [ ] Theory classification correct
- [ ] User_original protected (NEVER ALTERED)
