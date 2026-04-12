# Template: api-documentation-template

## Purpose

Standardized template for generating comprehensive API documentation.

## Applicability

API reference documentation, module documentation, function/class documentation

---

## YAML Frontmatter

```yaml
documentation_type: api_reference
version: "{{VERSION}}"
generated_date: "{{GENERATED_DATE}}"
maxwell_articles: "{{MAXWELL_ARTICLES}}"
cgs_units: "{{CGS_UNITS}}"
modules_covered:
  {{MODULES}}
target_audience:
  - developers
  - researchers
  - integrators
```

---

## LLM Instructions

You are generating API documentation for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **CGS Units**: All electrical quantities MUST use CGS units (statvolt, statampere, statohm, etc.)
2. **Theory Classification**: Clearly distinguish between:
   - `maxwell_original`: Maxwell's 1873 formulations
   - `user_original`: User's theoretical extensions (DO NOT ALTER)
   - `standard_math`: Standard mathematical implementations
3. **Article Citations**: Include Maxwell article references where applicable
4. **Code Examples**: Provide working examples in CGS units
5. **Parameters**: Document all parameters with units and valid ranges

---

## Template Structure

### Module Overview

```markdown
# Module: {{MODULE_NAME}}

## Purpose

{{MODULE_PURPOSE}}

## Maxwell Article References

{{MAXWELL_ARTICLE_CITATIONS}}

## Theory Classification

| Component | Classification | Description |
|-----------|----------------|-------------|
| {{component}} | {{classification}} | {{description}} |
```

### Function/Class Documentation

```markdown
## {{FUNCTION_NAME}}

### Signature

```python
def {{function_name}}({{parameters}}) -> {{return_type}}:
```

### Description

{{FUNCTION_DESCRIPTION}}

### Parameters

| Parameter | Type | Unit | Description | Valid Range |
|-----------|------|------|-------------|-------------|
| {{param}} | {{type}} | {{unit}} | {{description}} | {{range}} |

### Returns

| Return Value | Type | Unit | Description |
|--------------|------|------|-------------|
| {{return}} | {{type}} | {{unit}} | {{description}} |

### Maxwell Reference

{{MAXWELL_ARTICLE}}

### Example

```python
# CGS units example
{{CODE_EXAMPLE}}
```

### Notes

- {{NOTE_1}}
- {{NOTE_2}}
```

### Constants and Variables

```markdown
## Constants

| Name | Value | Unit | Description |
|------|-------|------|-------------|
| {{CONSTANT}} | {{value}} | {{unit}} | {{description}} |

## Physical Constants (CGS)

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Boltzmann | k_B | 1.381×10^-16 | erg/K |
| Elementary charge | q | 4.803×10^-10 | statC |
| Speed of light | c | 2.998×10^10 | cm/s |
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Documentation version | Yes | - |
| `{{GENERATED_DATE}}` | Generation date | Auto | - |
| `{{MAXWELL_ARTICLES}}` | Relevant article citations | Yes | - |
| `{{CGS_UNITS}}` | Unit system specification | Yes | CGS |
| `{{MODULES}}` | Modules covered | Yes | - |
| `{{MODULE_NAME}}` | Current module name | Yes | - |
| `{{MODULE_PURPOSE}}` | Module purpose description | Yes | - |
| `{{MAXWELL_ARTICLE_CITATIONS}}` | Article references | Conditional | - |
| `{{FUNCTION_NAME}}` | Function/class name | Yes | - |
| `{{parameters}}` | Function parameters | Yes | - |
| `{{return_type}}` | Return type | Yes | - |
| `{{CODE_EXAMPLE}}` | Working code example | Yes | - |
| `{{CONSTANT}}` | Constant name | Conditional | - |
| `{{value}}` | Constant value | Conditional | - |

---

## Conditional Logic

### Include Maxwell Articles Section If:

```
IF module_has_maxwell_reference:
  INCLUDE maxwell_article_citations
ELSE:
  OMIT maxwell_article_citations
```

### Include Theory Classification If:

```
IF has_user_extensions OR has_standard_implementations:
  INCLUDE theory_classification_table
ELSE:
  USE default_maxwell_original
```

### Include CGS Unit Table If:

```
IF electrical_module:
  INCLUDE cgs_units_table
  INCLUDE si_equivalents (as reference only)
ELSE IF mechanical_module:
  INCLUDE cgs_mechanical_units
```

### Include Examples If:

```
IF function_has_clear_use_case:
  INCLUDE working_code_example
  INCLUDE expected_output
```

---

## Quality Criteria

### Required Elements

- [ ] Module purpose clearly stated
- [ ] All parameters documented with units
- [ ] Return values documented with units
- [ ] Maxwell articles cited where applicable
- [ ] Theory classification provided
- [ ] CGS units used consistently

### Code Quality

- [ ] Examples are executable
- [ ] Examples use CGS units
- [ ] Examples include expected output
- [ ] Edge cases documented

### Documentation Quality

- [ ] No SI units as primary (CGS only)
- [ ] User extensions marked as user_original
- [ ] Standard implementations marked as standard_math
- [ ] Maxwell's original text marked as maxwell_original

---

## Output Format

The generated documentation should be in Markdown format with:
- Clear hierarchical structure (H1, H2, H3)
- Code blocks with syntax highlighting
- Tables for parameters and constants
- Cross-references to related modules

---

## Maxwell Article Quick Reference

### For API Documentation

| Topic | Articles | Relevance |
|-------|----------|-----------|
| Units and measurement | Art. 1-50 | Fundamental definitions |
| Electrostatics | Art. 1-229 | Electrometer APIs |
| Magnetism | Art. 371-474 | Magnetometer APIs |
| Electromagnetism | Art. 475-866 | Galvanometer APIs |
| Networks | Art. 287-300 | Circuit analysis APIs |
| Bridges | Art. 343-348 | Bridge measurement APIs |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | {{VERSION_DATE}} | Initial template |

---

## Related Templates

- `{{tutorial-template.md}}` - For tutorial documentation
- `{{cross-reference-template.md}}` - For citation linking
- `{{release-notes-template.md}}` - For version changes
