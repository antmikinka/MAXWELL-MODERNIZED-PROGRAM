# Checklist: Release Readiness

## Purpose

Final checklist before releasing mathematical components to the maxwell package.

## Release Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Version | {version_number} |
| Release Date | {date} |
| Release Type | {MAJOR|MINOR|PATCH} |

## Pre-Release Requirements

### Code Quality
- [ ] **All Tests Pass**: Unit, integration, validation tests
- [ ] **Code Review**: Completed and approved
- [ ] **Documentation**: Complete and accurate
- [ ] **Type Checking**: mypy passes without errors
- [ ] **Linting**: flake8/black checks pass

### Testing
- [ ] **Test Coverage**: > 90% coverage
- [ ] **Regression Tests**: All regression tests pass
- [ ] **Performance Tests**: Performance within bounds
- [ ] **Stress Tests**: Stress tests completed
- [ ] **Cross-Platform**: Tested on all platforms

### Documentation
- [ ] **API Docs**: Generated and reviewed
- [ ] **User Guide**: Updated for changes
- [ ] **Release Notes**: Drafted and reviewed
- [ ] **Migration Guide**: Created (if breaking changes)
- [ ] **Examples**: Updated and working

### Dependencies
- [ ] **Dependency Check**: All dependencies resolved
- [ ] **Version Pins**: Versions appropriately pinned
- [ ] **Security Scan**: No known vulnerabilities
- [ ] **License Check**: All licenses compatible

## Maxwell Package Integration

- [ ] **Package Structure**: Follows maxwell package structure
- [ ] **Import Path**: Correct import path (maxwell.mathematics.*)
- [ ] **__init__.py**: Exports configured correctly
- [ ] **pyproject.toml**: Dependencies listed
- [ ] **Entry Points**: Entry points configured (if applicable)

## Citation Tracking

- [ ] **Article Citations**: All @cite_article decorators present
- [ ] **Citation Index**: Citations indexed for search
- [ ] **Cross-Reference**: Links to related articles

## Quality Gates

### MATHEMATICA Agent
- [ ] **Math Correctness**: Verified by math lead
- [ ] **Physics Validation**: Verified by physics lead
- [ ] **Code Quality**: Verified by tech lead

### QUALITAS Agent
- [ ] **Validation Suite**: All validation tests pass
- [ ] **Quality Report**: Generated and reviewed

### ARCHITECTUS Agent
- [ ] **Build Pipeline**: Build succeeds
- [ ] **CI/CD**: Pipeline passes
- [ ] **Package Build**: Wheel and sdist build

## Release Artifacts

- [ ] **Wheel**: Built successfully
- [ ] **Source Distribution**: Built successfully
- [ ] **Documentation**: Generated (HTML, PDF)
- [ ] **Changelog**: Updated
- [ ] **Version Tag**: Git tag created

## Post-Release Tasks

- [ ] **Announcement**: Release announced
- [ ] **Documentation Deploy**: Docs published
- [ ] **Package Published**: Published to package index
- [ ] **Monitoring**: Monitoring configured
- [ ] **Support Plan**: Support plan in place

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Release Manager | | | |
| Math Lead | | | |
| Physics Lead | | | |
| Engineering Lead | | | |

## Release Notes Summary

{release_notes_summary}

## Known Issues

| Issue | Impact | Workaround |
|-------|--------|------------|
| {issue} | {impact} | {workaround} |
