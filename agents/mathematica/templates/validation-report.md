# Template: validation-report

## Description

Template for documenting mathematical validation results. This template ensures all mathematical implementations are verified against analytical solutions and mathematical properties.

## Structure

```markdown
# Validation Report: {component_name}

## Date
{date}

## Validator
{validator_name}

## Summary
| Status | {PASS|FAIL|PARTIAL} |
|--------|---------------------|
| Tests Run | {num_tests} |
| Tests Passed | {num_passed} |
| Tests Failed | {num_failed} |
| Coverage | {coverage_percent} |

## Validation Categories

### 1. Analytical Comparison
{comparison_with_known_solutions}

| Test Case | Expected | Computed | Error | Status |
|-----------|----------|----------|-------|--------|
| {case_1} | {expected} | {computed} | {error} | {PASS|FAIL} |

### 2. Mathematical Identities
{identity_verification}

| Identity | Expected | Computed | Error | Status |
|----------|----------|----------|-------|--------|
| {identity_1} | {expected} | {computed} | {error} | {PASS|FAIL} |

### 3. Convergence Analysis
{convergence_results}

| Grid Size | Error | Ratio | Order |
|-----------|-------|-------|-------|
| {n_1} | {error_1} | - | - |
| {n_2} | {error_2} | {ratio} | {order} |

### 4. Conservation Laws
{conservation_verification}

| Law | Expected | Computed | Error | Status |
|-----|----------|----------|-------|--------|
| {law_1} | {expected} | {computed} | {error} | {PASS|FAIL} |

### 5. Edge Cases
{edge_case_testing}

| Case | Input | Expected Behavior | Actual | Status |
|------|-------|-------------------|--------|--------|
| {case_1} | {input} | {expected} | {actual} | {PASS|FAIL} |

## Detailed Results

### Test 1: {test_name}
{detailed_results}

### Test 2: {test_name}
...

## Issues Found

| Issue ID | Severity | Description | Status |
|----------|----------|-------------|--------|
| {issue_1} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |

## Recommendations
{recommendations_for_improvement}

## Sign-off
- [ ] Mathematics Lead Review
- [ ] Physics Validation Review
- [ ] Code Quality Review
```

## LLM Instructions

When using this template:

1. **Complete All Sections**: Fill in every validation category
2. **Quantitative Results**: Include numerical error values
3. **Clear Status**: Mark each test as PASS or FAIL
4. **Actionable Issues**: Document any failures with severity
5. **Traceability**: Link to specific Maxwell articles where applicable

## Variables

- `{component_name}`: Name of component being validated
- `{date}`: Validation date
- `{validator_name}`: Who performed validation
- `{num_tests}`: Total number of tests
- `{num_passed}`: Number of passing tests
- `{num_failed}`: Number of failing tests
- `{coverage_percent}`: Test coverage percentage
- All other variables as shown in structure

## Conditional Logic

IF validation fails:
  INCLUDE detailed failure analysis
  ADD root cause investigation
  DOCUMENT reproduction steps

IF component is safety-critical:
  REQUIRE additional verification
  ADD independent validation method
  INCLUDE uncertainty quantification

## Example Usage

```markdown
# Validation Report: gradient()

## Date
2026-04-11

## Summary
| Status | PASS |
| Tests Run | 24 |
| Tests Passed | 24 |

### Analytical Comparison
| Test Case | Expected | Computed | Error |
|-----------|----------|----------|-------|
| grad(x²) at x=1 | 2.0 | 2.0000001 | 1e-7 |
| grad(r²) radial | 2r | 2r (verified) | 1e-8 |
```
