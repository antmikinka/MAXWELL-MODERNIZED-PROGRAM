# Template: Version Change Log

## Description

Template for tracking architecture version history and changes across all 6 Parts of Maxwell's Treatise. This template ensures proper versioning, changelog documentation, and change tracking.

## Structure

```markdown
# Architecture Version Change Log

## Project Information

**Project:** Maxwell Treatise Modernization  
**Repository:** {REPO_URL}  
**Maintainer:** ARCHITECTUS Agent  
**Versioning Scheme:** Semantic Versioning (MAJOR.MINOR.PATCH)

---

## Current Version

**Version:** {CURRENT_VERSION}  
**Release Date:** {RELEASE_DATE}  
**Status:** {STATUS} (Current/Stable/Deprecated)

---

## Version History

### [MAJOR.MINOR.PATCH] - {DATE}

#### Change Type: {MAJOR|MINOR|PATCH}

#### Summary

{Brief summary of changes in this version}

#### Changed

| Part | Layer | Module | Change Description |
|------|-------|--------|-------------------|
| {PART} | {LAYER} | {MODULE} | {DESCRIPTION} |

#### Added

| Part | Layer | Module | Description |
|------|-------|--------|-------------|
| {PART} | {LAYER} | {MODULE} | {DESCRIPTION} |

#### Removed

| Part | Layer | Module | Reason |
|------|-------|--------|--------|
| {PART} | {LAYER} | {MODULE} | {REASON} |

#### Fixed

| Part | Article | Issue | Resolution |
|------|---------|-------|------------|
| {PART} | {ARTICLE} | {ISSUE} | {RESOLUTION} |

#### Affected Agents

| Agent | Changes Required | Status |
|-------|------------------|--------|
| PHYSICUS | {CHANGES} | {STATUS} |
| MATHEMATICA | {CHANGES} | {STATUS} |
| QUALITAS | {CHANGES} | {STATUS} |

#### Migration Notes

{Any migration steps required for this version}

#### Breaking Changes

{List any breaking changes and how to handle them}

---

### [MAJOR.MINOR.PATCH] - {DATE}

#### Change Type: {MAJOR|MINOR|PATCH}

#### Summary

{Brief summary of changes}

#### Changed

...

---

## Version Comparison

### v{OLD} → v{NEW}

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Articles | {COUNT} | {COUNT} | {DIFF} |
| Mapped Articles | {COUNT} | {COUNT} | {DIFF} |
| Implemented | {COUNT} | {COUNT} | {DIFF} |
| Coverage | {PERCENT}% | {PERCENT}% | {DIFF}% |
| Layers | {COUNT} | {COUNT} | {DIFF} |
| Modules | {COUNT} | {COUNT} | {DIFF} |

---

## Release Checklist

For each version release:

- [ ] Architecture documents updated
- [ ] Version numbers incremented
- [ ] Changelog entry created
- [ ] Agent knowledge synced
- [ ] Git tag created
- [ ] Release notes published
- [ ] Stakeholders notified

---

## Version Numbering Guidelines

### MAJOR Version (Breaking Changes)

- Layer renumbering
- Part restructuring
- Module path changes
- Interface changes

### MINOR Version (New Features)

- New layers added
- New modules added
- New article mappings
- Backward-compatible changes

### PATCH Version (Bug Fixes)

- Article mapping corrections
- Documentation fixes
- Typos and clarifications
- Non-breaking updates

---

## Deprecation Policy

### Deprecated Versions

| Version | Deprecated Date | End of Support | Reason |
|---------|-----------------|----------------|--------|
| {VERSION} | {DATE} | {DATE} | {REASON} |

### Migration Path

{Instructions for migrating from deprecated versions}

---

## Git Tags

### Tag Format

```
architecture-v{MAJOR}.{MINOR}.{PATCH}
```

### Recent Tags

| Tag | Date | Version |
|-----|------|---------|
| architecture-v2.1.0 | 2026-04-11 | 2.1.0 |
| architecture-v2.0.0 | 2026-01-15 | 2.0.0 |
| architecture-v1.5.3 | 2025-12-01 | 1.5.3 |

---

## Change Request Process

### Submitting Changes

1. Create change request document
2. Specify change type (MAJOR/MINOR/PATCH)
3. List affected modules and articles
4. Get architecture review approval
5. Implement changes
6. Update version number
7. Create git tag

### Change Request Template

```markdown
**Change Type:** {MAJOR|MINOR|PATCH}
**Affected Parts:** {PARTS}
**Affected Modules:** {MODULES}
**Description:** {DESCRIPTION}
**Justification:** {JUSTIFICATION}
```

---

## Version History Summary

| Version | Date | Type | Key Changes |
|---------|------------|--------|-------------|
| 2.1.0 | 2026-04-11 | MINOR | Layer 67b added, Part VI expanded |
| 2.0.0 | 2026-01-15 | MAJOR | Complete architecture revision |
| 1.5.3 | 2025-12-01 | PATCH | Article mapping corrections |
| 1.5.0 | 2025-11-15 | MINOR | Part V system core added |
| 1.0.0 | 2025-01-01 | MAJOR | Initial architecture release |

---

**END OF CHANGE LOG**
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{REPO_URL}` | Repository URL | github.com/maxwell-treatise/modernized |
| `{CURRENT_VERSION}` | Current version | 2.1.0 |
| `{RELEASE_DATE}` | Release date | 2026-04-11 |
| `{STATUS}` | Version status | Current |
| `{MAJOR}` | Major version | 2 |
| `{MINOR}` | Minor version | 1 |
| `{PATCH}` | Patch version | 0 |
| `{PART}` | Part number | I |
| `{LAYER}` | Layer number | 8 |
| `{MODULE}` | Module path | maxwell/math/spherical/ |

## Usage Instructions

1. Copy this template to changelog document
2. Add new version entry for each release
3. Document all changes by category
4. Update version history summary
5. Track git tags
6. Maintain deprecation schedule

## Related Templates

- `architecture-document.md` - Architecture documentation
- `agent-coordination.md` - Agent coordination

## Example Changelog Entry

```markdown
## [2.1.0] - 2026-04-11

### Change Type: MINOR

### Summary

Added Layer 67b for advanced wave propagation modules and expanded
Part VI coverage with 12 new articles.

### Added

| Part | Layer | Module | Description |
|------|-------|--------|-------------|
| IV | 67b | maxwell/em/wave_advanced.py | Advanced wave propagation |
| VI | 96 | maxwell/scalar/partial_differential.py | PDE formulations |

### Changed

| Part | Layer | Module | Change Description |
|------|-------|--------|-------------------|
| IV | 67 | maxwell/em/wave_propagation.py | Refactored for clarity |

### Affected Agents

| Agent | Changes Required | Status |
|-------|------------------|--------|
| PHYSICUS | Update import paths | Complete |
| MATHEMATICA | No changes | N/A |
| QUALITAS | Add new test templates | In Progress |

### Migration Notes

No breaking changes. Backward compatible with v2.0.0.
```
