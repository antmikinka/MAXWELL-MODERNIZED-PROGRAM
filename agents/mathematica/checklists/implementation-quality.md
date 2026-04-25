# Checklist: Implementation Quality

## Purpose

Ensure all mathematical implementations meet quality standards before integration.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Reviewer | {reviewer_name} |
| Date | {date} |
| Version | {version} |

## Code Quality

- [ ] **Type Hints**: All functions have complete type annotations
- [ ] **Docstrings**: NumPy-style docstrings present and complete
- [ ] **Examples**: Working examples in docstrings
- [ ] **Citations**: @cite_article decorator with correct articles
- [ ] **Input Validation**: All inputs validated before use
- [ ] **Error Handling**: Appropriate exceptions raised
- [ ] **Logging**: Debug logging at appropriate levels

## Mathematical Correctness

- [ ] **Formula Verification**: Implementation matches mathematical formula
- [ ] **Coordinate Systems**: All coordinate systems handled correctly
- [ ] **Edge Cases**: Singularities and boundaries handled
- [ ] **Numerical Stability**: Algorithm is numerically stable
- [ ] **Precision**: Results match expected precision

## Unit Consistency

- [ ] **CGS Default**: CGS units used by default
- [ ] **Unit Documentation**: All parameters document units
- [ ] **Conversion Available**: SI conversion where appropriate
- [ ] **Dimensional Analysis**: Dimensions are consistent

## Testing

- [ ] **Unit Tests**: All unit tests pass
- [ ] **Analytical Comparison**: Verified against analytical solutions
- [ ] **Identity Verification**: Mathematical identities verified
- [ ] **Convergence**: Numerical convergence demonstrated
- [ ] **Coverage**: Test coverage > 90%

## Documentation

- [ ] **API Docs**: API documentation generated
- [ ] **Usage Examples**: Clear usage examples provided
- [ ] **Maxwell References**: Article citations complete
- [ ] **Cross-References**: Links to related functions

## Performance

- [ ] **Benchmark**: Performance benchmarked
- [ ] **Complexity**: Time/space complexity documented
- [ ] **Optimization**: Critical paths optimized
- [ ] **Vectorization**: NumPy vectorization used where possible

## Integration Readiness

- [ ] **Dependencies**: All dependencies available
- [ ] **Import Test**: Module imports without error
- [ ] **API Compatibility**: API matches interface specification
- [ ] **Backward Compatibility**: No breaking changes (if applicable)

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | | | |
| Reviewer | | | |
| Math Lead | | | |

## Notes

{additional_notes}
