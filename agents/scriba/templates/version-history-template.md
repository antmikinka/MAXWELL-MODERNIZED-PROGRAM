# Template: version-history-template

## Purpose

Standardized template for maintaining comprehensive version history.

## Applicability

Changelog maintenance, version tracking, release history

---

## YAML Frontmatter

```yaml
documentation_type: version_history
version: "{{VERSION}}"
maintained_by: "{{MAINTAINER}}"
first_release: "{{FIRST_RELEASE}}"
latest_release: "{{LATEST_RELEASE}}"
total_releases: {{TOTAL_RELEASES}}
maxwell_coverage_evolution: {{COVERAGE_EVOLUTION}}
```

---

## LLM Instructions

You are maintaining version history for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **Chronological Order**: List versions newest to oldest
2. **Semantic Versioning**: Use MAJOR.MINOR.PATCH format
3. **CGS Evolution**: Track CGS unit additions/corrections
4. **Maxwell Coverage**: Track article coverage growth
5. **Theory Classification**: Note classification system changes

---

## Template Structure

### Version History Header

```markdown
# Version History

## Project: {{PROJECT_NAME}}

**First Release:** {{FIRST_RELEASE}}  
**Latest Release:** {{LATEST_RELEASE}}  
**Total Releases:** {{TOTAL_RELEASES}}

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible changes
- **MINOR**: Backward-compatible features
- **PATCH**: Backward-compatible bug fixes
```

### Release Entries

```markdown
## [{{VERSION}}] - {{RELEASE_DATE}}

### Summary

{{VERSION_SUMMARY}}

### Added

- {{ADDED_1}}
- {{ADDED_2}}

### Changed

- {{CHANGED_1}}
- {{CHANGED_2}}

### Fixed

- {{FIXED_1}}
- {{FIXED_2}}

### Deprecated

- {{DEPRECATED_1}}

### Removed

- {{REMOVED_1}}

### Security

- {{SECURITY_1}}

### CGS Units

- {{CGS_CHANGE_1}}
- {{CGS_CHANGE_2}}

### Maxwell Articles

- Coverage added: Art. {{XX}}-{{YY}}
- Coverage improved: Art. {{ZZ}}

[Full Release Notes]({{RELEASE_NOTES_LINK}})
```

### Version Comparison

```markdown
## Version Comparison

### v{{VERSION_1}} vs v{{VERSION_2}}

| Metric | v{{VERSION_1}} | v{{VERSION_2}} | Change |
|--------|----------------|----------------|--------|
| Maxwell Coverage | {{COVERAGE_1}} | {{COVERAGE_2}} | {{DELTA}} |
| CGS Units | {{UNITS_1}} | {{UNITS_2}} | {{DELTA}} |
| Components | {{COUNT_1}} | {{COUNT_2}} | {{DELTA}} |
| Documentation | {{DOCS_1}} | {{DOCS_2}} | {{DELTA}} |
```

### Milestone Releases

```markdown
## Milestone Releases

### v{{MAJOR_VERSION}}.0.0 - {{MILESTONE_NAME}}

**Release Date:** {{DATE}}

**Significance:** {{SIGNIFICANCE}}

**Key Features:**
- {{FEATURE_1}}
- {{FEATURE_2}}

**Maxwell Coverage:** {{COVERAGE}}

**CGS Units:** {{CGS_STATUS}}
```

### Release Statistics

```markdown
## Release Statistics

### Releases by Year

| Year | Major | Minor | Patch | Total |
|------|-------|-------|-------|-------|
| {{YEAR}} | {{MAJOR_COUNT}} | {{MINOR_COUNT}} | {{PATCH_COUNT}} | {{TOTAL}} |

### Average Release Cycle

| Version Type | Average Days |
|--------------|--------------|
| Major | {{DAYS}} |
| Minor | {{DAYS}} |
| Patch | {{DAYS}} |
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Version number | Yes | - |
| `{{MAINTAINER}}` | Maintainer name | Yes | - |
| `{{FIRST_RELEASE}}` | First release date | Yes | - |
| `{{LATEST_RELEASE}}` | Latest release date | Yes | - |
| `{{TOTAL_RELEASES}}` | Total release count | Yes | - |
| `{{COVERAGE_EVOLUTION}}` | Coverage growth | Yes | - |
| `{{PROJECT_NAME}}` | Project name | Yes | - |
| `{{VERSION_SUMMARY}}` | Version summary | Yes | - |
| `{{ADDED_N}}` | Added items | Conditional | - |
| `{{CHANGED_N}}` | Changed items | Conditional | - |
| `{{FIXED_N}}` | Fixed items | Conditional | - |
| `{{DEPRECATED_N}}` | Deprecated items | Conditional | - |
| `{{REMOVED_N}}` | Removed items | Conditional | - |
| `{{SECURITY_N}}` | Security fixes | Conditional | - |
| `{{CGS_CHANGE_N}}` | CGS unit changes | Conditional | - |
| `{{RELEASE_NOTES_LINK}}` | Link to full notes | Conditional | - |
| `{{VERSION_1}}` | Comparison version 1 | Conditional | - |
| `{{VERSION_2}}` | Comparison version 2 | Conditional | - |
| `{{COVERAGE_1}}` | Coverage at v1 | Conditional | - |
| `{{COVERAGE_2}}` | Coverage at v2 | Conditional | - |
| `{{MAJOR_VERSION}}` | Major version number | Conditional | - |
| `{{MILESTONE_NAME}}` | Milestone name | Conditional | - |
| `{{SIGNIFICANCE}}` | Milestone significance | Conditional | - |
| `{{DATE}}` | Milestone date | Conditional | - |
| `{{YEAR}}` | Calendar year | Conditional | - |
| `{{DAYS}}` | Days between releases | Conditional | - |

---

## Conditional Logic

### Include Version Comparison If:

```
IF has_significant_changes:
  INCLUDE version_comparison_table
  SHOW key_metrics
```

### Include Milestone Section If:

```
IF has_milestone_releases:
  INCLUDE milestone_releases_section
  HIGHLIGHT major_versions
```

### Include Statistics If:

```
IF release_count > 5:
  INCLUDE release_statistics
  SHOW yearly_breakdown
  SHOW release_cycle
```

---

## Change Categories

### Added

New features, capabilities, documentation

### Changed

Modified existing functionality

### Fixed

Bug fixes, corrections

### Deprecated

Features to be removed in future

### Removed

Features removed in this version

### Security

Security-related fixes

### CGS Units

CGS unit additions or corrections

### Maxwell Articles

Article coverage changes

---

## Quality Criteria

### Completeness

- [ ] All versions documented
- [ ] All changes categorized
- [ ] Migration notes included
- [ ] Links valid

### Accuracy

- [ ] Version numbers correct
- [ ] Dates accurate
- [ ] Change descriptions accurate
- [ ] Statistics verified

### Consistency

- [ ] Format consistent across versions
- [ ] Categories used consistently
- [ ] CGS changes highlighted
- [ ] Maxwell citations correct

---

## Output Format

Version history should be:
- Markdown format
- Reverse chronological order
- Clear section hierarchy
- Tables for comparisons
- Links to detailed release notes

---

## Related Templates

- `{{release-notes-template.md}}` - Individual release notes
- `{{api-documentation-template.md}}` - API reference
- `{{cross-reference-template.md}}` - Cross-references
