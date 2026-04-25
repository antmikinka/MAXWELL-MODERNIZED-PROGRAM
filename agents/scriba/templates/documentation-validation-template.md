# Template: documentation-validation-template

## Purpose

Standardized template for validating documentation quality and completeness.

## Applicability

Documentation reviews, quality assurance, compliance checking

---

## YAML Frontmatter

```yaml
documentation_type: validation_template
version: "{{VERSION}}"
validation_level: "{{VALIDATION_LEVEL}}"
maxwell_articles_required: {{MAXWELL_ARTICLES_REQUIRED}}
cgs_units_required: {{CGS_UNITS_REQUIRED}}
theory_classification_required: {{THEORY_CLASSIFICATION_REQUIRED}}
```

---

## LLM Instructions

You are validating documentation for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **CGS Compliance**: Verify all units are CGS (SI only as reference)
2. **Maxwell Citations**: Verify article citations are accurate
3. **Theory Classification**: Verify classification is correct and not altered
4. **Completeness**: Verify all required sections present
5. **Accuracy**: Verify technical content is correct

---

## Template Structure

### Validation Header

```markdown
# Documentation Validation: {{DOCUMENT_NAME}}

**Validator:** {{VALIDATOR}}  
**Date:** {{VALIDATION_DATE}}  
**Version:** {{DOCUMENT_VERSION}}  
**Validation Level:** {{VALIDATION_LEVEL}}

## Summary

**Overall Status:** [ ] Pass [ ] Conditional [ ] Fail

**Score:** {{SCORE}} / 100
```

### Level 1: Required Elements

```markdown
## Level 1: Required Elements (Required)

### Document Structure

- [ ] Title present and descriptive
- [ ] Purpose/overview section
- [ ] Table of contents (if > 5 sections)
- [ ] Clear section hierarchy

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### CGS Unit Compliance

- [ ] All electrical units in CGS (statvolt, statampere, statohm)
- [ ] CGS explicitly stated as primary system
- [ ] SI equivalents only as reference (if present)
- [ ] Unit conversions accurate

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Maxwell Article Citations

- [ ] Maxwell articles cited where applicable
- [ ] Article numbers accurate
- [ ] Citation format consistent
- [ ] Article context correct

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Theory Classification

- [ ] Classification provided (maxwell_original, user_original, standard_math)
- [ ] User extensions marked as user_original
- [ ] No alteration of user_original content
- [ ] Classification accurate

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

**Level 1 Score:** {{L1_SCORE}} / 40
```

### Level 2: Technical Accuracy

```markdown
## Level 2: Technical Accuracy (Required)

### Equations and Formulas

- [ ] Equations correctly formatted
- [ ] CGS units in equations
- [ ] Variables defined
- [ ] Formulas accurate

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Code Examples

- [ ] Code examples provided where applicable
- [ ] Code uses CGS units
- [ ] Code is executable
- [ ] Expected output shown

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Technical Terminology

- [ ] Terms used consistently
- [ ] Terms defined on first use
- [ ] Maxwell's terminology preserved
- [ ] Modern terms distinguished

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

**Level 2 Score:** {{L2_SCORE}} / 30
```

### Level 3: Completeness

```markdown
## Level 3: Completeness (Expert)

### Topic Coverage

- [ ] Topic introduced adequately
- [ ] Background provided
- [ ] Examples sufficient
- [ ] Edge cases addressed

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Cross-References

- [ ] Related documents linked
- [ ] Maxwell articles linked
- [ ] Internal links valid
- [ ] External links valid

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Documentation Types

- [ ] API documentation (if applicable)
- [ ] Tutorials (if applicable)
- [ ] How-to guides (if applicable)
- [ ] Reference material (if applicable)

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

**Level 3 Score:** {{L3_SCORE}} / 20
```

### Level 4: Quality Excellence

```markdown
## Level 4: Quality Excellence (Expert)

### Readability

- [ ] Clear, concise writing
- [ ] Logical flow
- [ ] Appropriate technical level
- [ ] No ambiguity

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Maintainability

- [ ] Version tracked
- [ ] Change history available
- [ ] Owner identified
- [ ] Review date set

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

### Accessibility

- [ ] Searchable structure
- [ ] Clear navigation
- [ ] Helpful indices
- [ ] Multiple access paths

**Status:** [ ] Pass [ ] Fail  
**Notes:** {{NOTES}}

**Level 4 Score:** {{L4_SCORE}} / 10
```

### Validation Summary

```markdown
## Validation Summary

| Level | Category | Score | Max | Status |
|-------|----------|-------|-----|--------|
| 1 | Required Elements | {{L1}} | 40 | {{STATUS}} |
| 2 | Technical Accuracy | {{L2}} | 30 | {{STATUS}} |
| 3 | Completeness | {{L3}} | 20 | {{STATUS}} |
| 4 | Quality Excellence | {{L4}} | 10 | {{STATUS}} |
| **TOTAL** | | **{{TOTAL}}** | **100** | **{{OVERALL_STATUS}}** |

## Action Items

| Priority | Issue | Category | Status |
|----------|-------|----------|--------|
| {{PRIORITY}} | {{ISSUE}} | {{CATEGORY}} | {{STATUS}} |

## Approval

**Approved:** [ ] Yes [ ] No [ ] Conditional

**Approver:** ______________________

**Date:** ______________________

**Next Review:** ______________________
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Template version | Yes | - |
| `{{VALIDATION_LEVEL}}` | Basic/Standard/Expert | Yes | - |
| `{{MAXWELL_ARTICLES_REQUIRED}}` | Citation requirement | Yes | - |
| `{{CGS_UNITS_REQUIRED}}` | CGS requirement | Yes | - |
| `{{THEORY_CLASSIFICATION_REQUIRED}}` | Classification requirement | Yes | - |
| `{{DOCUMENT_NAME}}` | Document being validated | Yes | - |
| `{{VALIDATOR}}` | Validator name | Yes | - |
| `{{VALIDATION_DATE}}` | Validation date | Yes | - |
| `{{DOCUMENT_VERSION}}` | Document version | Yes | - |
| `{{NOTES}}` | Validation notes | Conditional | - |
| `{{L1_SCORE}}` | Level 1 score | Auto | - |
| `{{L2_SCORE}}` | Level 2 score | Auto | - |
| `{{L3_SCORE}}` | Level 3 score | Auto | - |
| `{{L4_SCORE}}` | Level 4 score | Auto | - |
| `{{SCORE}}` | Total score | Auto | - |
| `{{STATUS}}` | Pass/Fail status | Auto | - |
| `{{OVERALL_STATUS}}` | Overall status | Auto | - |
| `{{PRIORITY}}` | Issue priority | Conditional | - |
| `{{ISSUE}}` | Issue description | Conditional | - |
| `{{CATEGORY}}` | Issue category | Conditional | - |

---

## Conditional Logic

### Validation Level

```
IF validation_level == "Basic":
  REQUIRE Level 1 only
  PASS_THRESHOLD = 80%
ELSE IF validation_level == "Standard":
  REQUIRE Level 1 + Level 2
  PASS_THRESHOLD = 85%
ELSE IF validation_level == "Expert":
  REQUIRE All levels
  PASS_THRESHOLD = 90%
```

### Required Elements

```
IF Level 1 fails:
  OVERALL_STATUS = "Fail"
  STOP validation
ELSE:
  CONTINUE to Level 2
```

---

## Validation Levels

### Basic

- Level 1 only
- For draft documentation
- 80% threshold

### Standard

- Level 1 + Level 2
- For release documentation
- 85% threshold

### Expert

- All levels
- For reference documentation
- 90% threshold

---

## Quality Criteria

### Validation Quality

- [ ] Validator qualified
- [ ] Validation thorough
- [ ] Issues clearly identified
- [ ] Action items actionable

### Documentation Quality

- [ ] CGS compliance verified
- [ ] Maxwell citations verified
- [ ] Theory classification verified
- [ ] Technical accuracy verified

---

## Output Format

Validation report should be:
- Markdown format
- Clear pass/fail indicators
- Actionable items listed
- Approval section completed

---

## Related Templates

- `{{api-documentation-template.md}}` - API reference
- `{{tutorial-documentation-template.md}}` - Tutorials
- `{{release-notes-template.md}}` - Release notes
