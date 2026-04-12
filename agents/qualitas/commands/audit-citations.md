# Command: audit-citations

## Description

Audits Maxwell article citations across all implementations. Verifies that every function has proper citations and that citations accurately reflect the implementation.

## Functionality

### Citation Audit

1. **Coverage Check**
   - Every function has @cite_article decorator
   - All relevant articles are cited
   - Part number is specified
   - No orphan functions (missing citations)

2. **Accuracy Check**
   - Cited article matches implementation
   - All cited content is actually implemented
   - No false citations (citing unrelated articles)
   - Citation format is consistent

3. **Theory Classification**
   - Maxwell's original: verified against text
   - User theory: clearly marked as "User Original Theory"
   - Standard math: identified as standard implementation

### Traceability Reports

- Article → Function mapping
- Function → Article mapping
- Coverage statistics
- Missing citations list

## Usage

```python
from maxwell.quality.citation_audit import CitationAuditor

# Create auditor
auditor = CitationAuditor()

# Audit single function
result = auditor.audit_function(electric_field_point_charge)
# Returns: citations found, accuracy check

# Audit module
report = auditor.audit_module('maxwell.physics.electrostatics')
# Returns: coverage %, missing citations, issues

# Audit entire codebase
full_audit = auditor.audit_codebase()

# Generate traceability matrix
matrix = auditor.generate_traceability_matrix()

# Check theory classification
classification = auditor.verify_theory_classification()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `function` | callable | Function to audit |
| `module_path` | str | Module to audit |
| `strict` | bool | Fail on any issue |
| `check_accuracy` | bool | Verify citation accuracy |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `result` | AuditResult | Coverage and issues |
| `matrix` | DataFrame | Traceability matrix |
| `report` | str | Formatted report |

## Citation Format Requirements

```python
# Required format:
@cite_article([44, 45, 46, 47, 48, 49], part='I')
def electric_field_point_charge(...):
    ...

# With theory classification:
@cite_article([60, 61, 62], part='I', 
              theory_type='maxwell_original')
def electric_displacement(...):
    ...

# User theory (must be clearly marked):
@cite_article([], part='IV',
              theory_type='user_original',
              note='User theoretical extension - not Maxwell')
def custom_field_equation(...):
    ...
```

## Output Format

```
============================================================
CITATION AUDIT REPORT
============================================================
Module: maxwell.physics.electrostatics
Date: 2026-04-11
============================================================

COVERAGE
--------
Total functions: 24
With citations: 24
Coverage: 100%

CITATION ACCURACY
-----------------
electric_field_point_charge:
  Cited: Articles 44-49, Part I
  Content: Electric field definition
  Status: ACCURATE ✓

potential_point_charge:
  Cited: Articles 69-73, Part I
  Content: Potential calculations
  Status: ACCURATE ✓

gauss_law:
  Cited: Articles 75-76, Part I
  Content: Surface integrals, Gauss
  Status: ACCURATE ✓

THEORY CLASSIFICATION
---------------------
Maxwell original: 22 functions
User theory: 0 functions
Standard math: 2 functions

ISSUES FOUND
------------
None ✓

============================================================
SUMMARY: 24/24 functions properly cited (100%)
============================================================
```

## Maxwell Article Coverage

| Part | Articles | Coverage | Functions |
|------|----------|----------|-----------|
| I | 27-229 | {coverage}% | {count} |
| II | 230-370 | {coverage}% | {count} |
| III | 371-474 | {coverage}% | {count} |
| IV | 475-866 | {coverage}% | {count} |

## Theory Classification Verification

### Maxwell's Original
- [ ] Matches Maxwell's mathematical formulation
- [ ] Uses consistent notation
- [ ] Follows Maxwell's reasoning

### User's Original Theory
- [ ] Clearly marked as "User Original Theory"
- [ ] Treated as authoritative (NOT TO BE CHANGED)
- [ ] Distinguished from Maxwell's text

### Standard Mathematical Implementation
- [ ] Identified as standard (vector calculus, etc.)
- [ ] Uses established methods
- [ ] No false claims of Maxwell origin

## Related Commands

- `validate-physics` - Physics validation
- `check-units` - Unit consistency
- `verify-conservation` - Conservation laws
