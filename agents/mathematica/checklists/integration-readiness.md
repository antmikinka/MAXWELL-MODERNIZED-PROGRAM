# Checklist: Integration Readiness

## Purpose

Verify mathematical components are ready for integration with other agents.

## Readiness Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Target Integration | {integration_target} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Interface Compatibility

- [ ] **API Contract**: Interface matches specification
- [ ] **Input Types**: Input types match expectations
- [ ] **Output Types**: Output types match expectations
- [ ] **Error Handling**: Errors propagated correctly
- [ ] **Default Values**: Defaults are appropriate

## Dependency Verification

### Internal Dependencies
- [ ] **maxwell/core**: Core types available
- [ ] **maxwell/config**: Constants accessible
- [ ] **Other Math Modules**: Dependencies available

### External Dependencies
- [ ] **NumPy**: Version >= 1.24
- [ ] **SciPy**: Version >= 1.10 (for special functions)
- [ ] **Optional Dependencies**: SymPy (if needed)

## Data Exchange

- [ ] **Data Format**: Format matches consumer expectations
- [ ] **Units**: CGS units documented and used
- [ ] **Coordinate System**: Coordinate system specified
- [ ] **Metadata**: Metadata included where needed

## Cross-Agent Integration

### PHYSICUS Agent
- [ ] **Field Operations**: Vector calculus ready for physics
- [ ] **Potential Theory**: Ready for electrostatics
- [ ] **Harmonics**: Ready for spherical problems

### MATERIA Agent
- [ ] **Tensor Operations**: Ready for anisotropy
- [ ] **Coordinate Transform**: Ready for crystal axes

### CIRCUITUS Agent
- [ ] **Vector Analysis**: Ready for field analysis
- [ ] **Potential Solver**: Ready for network problems

### INSTRUMENTUM Agent
- [ ] **Solid Angle**: Ready for instrument calibration
- [ ] **Rotation**: Ready for orientation calculations

### QUALITAS Agent
- [ ] **Validation Interface**: Ready for QA testing
- [ ] **Test Cases**: Test cases documented

## Integration Testing

- [ ] **Smoke Test**: Basic integration works
- [ ] **Functional Test**: End-to-end functionality verified
- [ ] **Performance Test**: Performance acceptable
- [ ] **Error Test**: Error handling works across boundaries

## Documentation for Integration

- [ ] **Integration Guide**: Guide for consumers
- [ ] **API Reference**: Complete API documentation
- [ ] **Examples**: Integration examples provided
- [ ] **Troubleshooting**: Common issues documented

## Version Compatibility

- [ ] **Semantic Versioning**: Version follows SemVer
- [ ] **Backward Compatibility**: No breaking changes (or documented)
- [ ] **Deprecation Warnings**: Deprecations announced

## Rollback Plan

- [ ] **Rollback Procedure**: Documented
- [ ] **Feature Flags**: Feature can be disabled
- [ ] **Data Migration**: Migration reversible (if applicable)

## Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Integration Lead | | | |
| Component Owner | | | |
| QA Representative | | | |

## Issues Blocking Integration

| Issue | Severity | Owner | Resolution Date |
|-------|----------|-------|-----------------|
| {issue} | {BLOCKING|MAJOR|MINOR} | {owner} | {date} |
