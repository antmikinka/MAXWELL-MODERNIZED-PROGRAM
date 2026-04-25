# Command: validate-architecture

## Description

Validates architecture maps for consistency across all 6 Parts of Maxwell's Treatise. This command performs comprehensive structural validation of the architecture COMPLETE documents, ensuring layer numbering, module mappings, and cross-part references are coherent and valid.

## Usage

```bash
architectus validate-architecture [OPTIONS]

Options:
  --part <PART>           Validate specific part only (I, II, III, IV, V, VI)
  --full                  Full validation including cross-part dependencies
  --strict                Fail on any warning, not just errors
  --output <FORMAT>       Output format: text, json, markdown (default: text)
  --report <PATH>         Write validation report to file
```

## Input

- **Architecture COMPLETE Documents**: All 6 Part architecture maps
  - `Maxwell_Treatise_Part_I_Architecture_COMPLETE.md`
  - `Maxwell_Treatise_Part_II_Architecture_COMPLETE.md`
  - `Maxwell_Treatise_Part_III_Architecture_COMPLETE.md`
  - `Maxwell_Treatise_Part_IV_Architecture_COMPLETE.md`
  - `Maxwell_Treatise_Part_V_Architecture_COMPLETE.md`
  - `Maxwell_Treatise_Part_VI_Architecture_COMPLETE.md`

## Validation Checks

### 1. Document Structure Validation

- [ ] All 6 Part architecture documents present
- [ ] Each document has required sections:
  - Executive Summary with coverage metrics
  - Layer Numbering table
  - Package Directory Structure
  - Article-to-Module mappings for all layers
  - Implementation Priority Matrix
  - Validation Checklist
- [ ] Version history present and current

### 2. Layer Numbering Validation

- [ ] No layer gaps between parts
- [ ] No layer overlaps between parts
- [ ] Layer numbers are sequential within parts
- [ ] Layer boundaries are clearly defined
- [ ] Cross-part layer references are valid

**Expected Layer Ranges:**
| Part | Domain | Layer Range |
|------|--------|-------------|
| I | Electrostatics | 0-12 |
| II | Electrokinematics | 13-30 |
| III | Magnetism | 30b-42 |
| IV | Electromagnetism | 43-86 |
| V | System Core | 90-94 |
| VI | Scalar Physics | 95-97 |

### 3. Module Mapping Validation

- [ ] Every article mapped to exactly one module
- [ ] No orphaned articles (unmapped)
- [ ] No duplicate mappings
- [ ] Sub-articles handled (e.g., 74a, 74b, 74c)
- [ ] Module paths are valid Python package paths

### 4. Cross-Part Consistency

- [ ] Cross-part dependencies explicitly declared
- [ ] No circular dependencies between parts
- [ ] Shared modules have consistent interfaces
- [ ] Part IV dependencies on Parts I-III are valid
- [ ] Bridge modules properly documented

### 5. Article Coverage Validation

- [ ] Article counts match Maxwell's original
- [ ] Sub-article counts are complete
- [ ] Coverage percentage is 100%
- [ ] No article number gaps within parts

## Output

### Success Output

```
Architecture Validation: PASSED

Parts Validated: 6/6
Total Articles: 885+
Coverage: 100%
Layer Gaps: 0
Cross-Part Dependencies: Valid
Warnings: 0
```

### Error Output

```
Architecture Validation: FAILED

Errors Found:
  [PART III] Layer 30 conflict: overlaps with Part II
  [PART IV] Article 523 unmapped: no module assignment
  [PART II] Duplicate mapping: Article 287 mapped to two modules

Parts Validated: 5/6
Total Articles: 847/885
Coverage: 95.7%
Layer Gaps: 1
Cross-Part Dependencies: 2 invalid
Warnings: 3
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed, no errors |
| 1 | Validation failed, errors found |
| 2 | Validation passed with warnings |
| 3 | Configuration error (missing files) |

## Examples

```bash
# Full architecture validation
architectus validate-architecture --full

# Validate single part
architectus validate-architecture --part IV

# Generate JSON report
architectus validate-architecture --output json --report validation_report.json

# Strict mode for CI/CD
architectus validate-architecture --strict
```

## Related Commands

- `audit-coverage` - Detailed article coverage audit
- `check-dependencies` - Cross-part dependency verification
- `review-layer-mapping` - Layer numbering scheme review
- `generate-master-index` - Master article index generation

## Implementation Notes

This command reads all architecture COMPLETE documents and performs:
1. YAML front-matter parsing for metadata
2. Markdown structure analysis for section validation
3. Article number extraction and validation
4. Layer number extraction and range validation
5. Cross-reference resolution and validation

## Error Categories

| Category | Severity | Description |
|----------|----------|-------------|
| MISSING_PART | Critical | Architecture document missing |
| LAYER_GAP | Critical | Gap in layer numbering |
| LAYER_OVERLAP | Critical | Layers overlap between parts |
| UNMAPPED_ARTICLE | Critical | Article has no module assignment |
| DUPLICATE_MAPPING | Critical | Article mapped to multiple modules |
| CIRCULAR_DEPENDENCY | Critical | Circular dependency detected |
| INVALID_MODULE_PATH | Warning | Module path may not exist |
| VERSION_MISMATCH | Warning | Version numbers inconsistent |
