# Template: release-notes-template

## Purpose

Standardized template for generating release notes and changelog entries.

## Applicability

Version releases, changelog entries, update announcements

---

## YAML Frontmatter

```yaml
documentation_type: release_notes
version: "{{VERSION}}"
release_date: "{{RELEASE_DATE}}"
previous_version: "{{PREVIOUS_VERSION}}"
maxwell_articles_added: "{{MAXWELL_ARTICLES}}"
cgs_units_added: "{{CGS_UNITS}}"
change_summary:
  features: {{FEATURE_COUNT}}
  fixes: {{FIX_COUNT}}
  documentation: {{DOC_COUNT}}
```

---

## LLM Instructions

You are generating release notes for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **Clear Versioning**: Use semantic versioning (MAJOR.MINOR.PATCH)
2. **CGS Emphasis**: Highlight CGS unit additions/changes
3. **Maxwell Citations**: Note new Maxwell article coverage
4. **Theory Classification**: Document changes to classification system
5. **Backward Compatibility**: Note any breaking changes

---

## Template Structure

### Release Header

```markdown
# Release Notes: Version {{VERSION}}

**Release Date:** {{RELEASE_DATE}}  
**Previous Version:** {{PREVIOUS_VERSION}}

## Summary

{{RELEASE_SUMMARY}}

**Highlights:**
- {{HIGHLIGHT_1}}
- {{HIGHLIGHT_2}}
- {{HIGHLIGHT_3}}
```

### New Features

```markdown
## New Features

### {{FEATURE_NAME}}

**Description:** {{FEATURE_DESCRIPTION}}

**Maxwell Articles:** {{MAXWELL_ARTICLES}}

**CGS Units:** {{CGS_UNITS}}

**Theory Classification:** {{CLASSIFICATION}}

**Example:**
```python
{{FEATURE_EXAMPLE}}
```

**Related Documentation:**
- {{DOC_LINK_1}}
- {{DOC_LINK_2}}
```

### Bug Fixes

```markdown
## Bug Fixes

### {{FIX_ID}}: {{FIX_DESCRIPTION}}

**Severity:** {{SEVERITY}}  
**Affected Components:** {{COMPONENTS}}

**Before:**
```python
{{BEFORE_CODE}}
```

**After:**
```python
{{AFTER_CODE}}
```

**CGS Impact:** {{CGS_IMPACT}}
```

### Documentation Updates

```markdown
## Documentation Updates

### New Documentation

| Document | Type | Maxwell Articles | CGS Units |
|----------|------|------------------|-----------|
| {{DOC_NAME}} | {{TYPE}} | {{ARTICLES}} | {{UNITS}} |

### Updated Documentation

| Document | Change Type | Description |
|----------|-------------|-------------|
| {{DOC_NAME}} | {{CHANGE_TYPE}} | {{DESCRIPTION}} |
```

### Breaking Changes

```markdown
## Breaking Changes

{{BREAKING_CHANGE_NOTICE}}

### {{CHANGE_NAME}}

**Description:** {{CHANGE_DESCRIPTION}}

**Migration Path:**
```python
# Before (v{{PREVIOUS_VERSION}})
{{OLD_CODE}}

# After (v{{VERSION}})
{{NEW_CODE}}
```

**Affected Components:**
- {{AFFECTED_1}}
- {{AFFECTED_2}}
```

### Deprecations

```markdown
## Deprecations

### {{DEPRECATED_NAME}}

**Deprecation Notice:** {{NOTICE}}

**Removal Version:** {{REMOVAL_VERSION}}

**Replacement:**
```python
{{REPLACEMENT_CODE}}
```

**Migration Guide:** {{MIGRATION_LINK}}
```

### CGS Unit Changes

```markdown
## CGS Unit Changes

### New CGS Units

| Quantity | Unit | Symbol | SI Equivalent |
|----------|------|--------|---------------|
| {{QUANTITY}} | {{UNIT}} | {{SYMBOL}} | {{SI_EQUIV}} |

### CGS Unit Corrections

| Component | Previous | Corrected | Notes |
|-----------|----------|-----------|-------|
| {{COMPONENT}} | {{PREV_UNIT}} | {{CORRECT_UNIT}} | {{NOTES}} |
```

### Maxwell Article Coverage

```markdown
## Maxwell Article Coverage

### Newly Covered Articles

| Part | Articles | Topic | Implementation |
|------|----------|-------|----------------|
| {{PART}} | Art. {{XX}}-{{YY}} | {{TOPIC}} | {{IMPLEMENTATION}} |

### Coverage Statistics

| Part | Total Articles | Covered | Percentage |
|------|----------------|---------|------------|
| I: Electrostatics | 229 | {{COUNT}} | {{PCT}}% |
| II: Electrokinematics | 141 | {{COUNT}} | {{PCT}}% |
| III: Magnetism | 104 | {{COUNT}} | {{PCT}}% |
| IV: Electromagnetism | 392 | {{COUNT}} | {{PCT}}% |
```

### Installation/Upgrade

```markdown
## Installation/Upgrade

### From Previous Version

```bash
{{UPGRADE_COMMAND}}
```

### Fresh Installation

```bash
{{INSTALL_COMMAND}}
```

### Verification

```python
{{VERIFICATION_CODE}}
```

Expected output:
```
{{EXPECTED_OUTPUT}}
```
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Release version | Yes | - |
| `{{RELEASE_DATE}}` | Release date | Yes | - |
| `{{PREVIOUS_VERSION}}` | Previous version | Yes | - |
| `{{MAXWELL_ARTICLES}}` | New article coverage | Conditional | - |
| `{{CGS_UNITS}}` | CGS unit changes | Conditional | - |
| `{{FEATURE_COUNT}}` | Number of features | Auto | - |
| `{{FIX_COUNT}}` | Number of fixes | Auto | - |
| `{{DOC_COUNT}}` | Documentation updates | Auto | - |
| `{{RELEASE_SUMMARY}}` | Release summary | Yes | - |
| `{{HIGHLIGHT_N}}` | Release highlights | Yes | - |
| `{{FEATURE_NAME}}` | Feature name | Conditional | - |
| `{{FEATURE_DESCRIPTION}}` | Feature description | Conditional | - |
| `{{FEATURE_EXAMPLE}}` | Feature example | Conditional | - |
| `{{FIX_ID}}` | Fix identifier | Conditional | - |
| `{{FIX_DESCRIPTION}}` | Fix description | Conditional | - |
| `{{SEVERITY}}` | Bug severity | Conditional | - |
| `{{BEFORE_CODE}}` | Code before fix | Conditional | - |
| `{{AFTER_CODE}}` | Code after fix | Conditional | - |
| `{{BREAKING_CHANGE_NOTICE}}` | Breaking change warning | Conditional | - |
| `{{CHANGE_DESCRIPTION}}` | Change description | Conditional | - |
| `{{OLD_CODE}}` | Deprecated code | Conditional | - |
| `{{NEW_CODE}}` | New code | Conditional | - |
| `{{DEPRECATED_NAME}}` | Deprecated feature | Conditional | - |
| `{{NOTICE}}` | Deprecation notice | Conditional | - |
| `{{REMOVAL_VERSION}}` | Version for removal | Conditional | - |
| `{{REPLACEMENT_CODE}}` | Replacement code | Conditional | - |

---

## Conditional Logic

### Include Breaking Changes If:

```
IF has_breaking_changes:
  INCLUDE breaking_changes_section
  INCLUDE migration_guide
  MARK prominently
ELSE:
  NOTE "No breaking changes"
```

### Include Deprecations If:

```
IF has_deprecations:
  INCLUDE deprecations_section
  INCLUDE removal_timeline
  INCLUDE migration_guide
```

### Include CGS Unit Changes If:

```
IF cgs_units_changed OR new_cgs_units_added:
  INCLUDE cgs_unit_changes_section
  HIGHLIGHT prominently (critical for users)
```

### Include Maxwell Coverage If:

```
IF new_articles_covered:
  INCLUDE maxwell_article_coverage
  SHOW coverage_statistics
```

---

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| Critical | System broken | Immediate |
| High | Major feature broken | 24 hours |
| Medium | Minor issue | 1 week |
| Low | Cosmetic/enhancement | Next release |

---

## Quality Criteria

### Completeness

- [ ] All changes documented
- [ ] Migration paths provided
- [ ] Examples verified
- [ ] Links valid

### Clarity

- [ ] Changes clearly described
- [ ] Breaking changes prominent
- [ ] CGS changes highlighted
- [ ] Maxwell citations accurate

### Accuracy

- [ ] Version numbers correct
- [ ] Code examples tested
- [ ] Migration paths verified
- [ ] Statistics accurate

---

## Output Format

Release notes should be:
- Markdown format
- Clear section hierarchy
- Code blocks with syntax highlighting
- Tables for comparisons
- Links to documentation

---

## Related Templates

- `{{api-documentation-template.md}}` - API reference
- `{{tutorial-documentation-template.md}}` - Tutorials
- `{{cross-reference-template.md}}` - Cross-references
