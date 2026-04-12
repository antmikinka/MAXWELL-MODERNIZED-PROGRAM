# Template: test-case

## Description

Template for creating mathematical test cases. This template ensures comprehensive testing of mathematical implementations with clear pass/fail criteria.

## Structure

```markdown
# Test Case: {test_name}

## Test ID
{unique_test_identifier}

## Component Under Test
{component_name}

## Test Category
{unit|integration|validation|convergence}

## Test Description
{what_is_being_tested_and_why}

## Mathematical Background

### Expected Result
{mathematical_expression_of_expected_result}

### Derivation
{brief_derivation_of_expected_result}

### Reference
{source_of_expected_result}

## Test Configuration

### Input Parameters
| Parameter | Value | Units |
|-----------|-------|-------|
| {param_1} | {value} | {units} |

### Tolerance
| Type | Value |
|------|-------|
| Absolute | {abs_tol} |
| Relative | {rel_tol} |

## Test Procedure

1. {step_1}
2. {step_2}
3. {step_3}

## Expected Output
{expected_output}

## Actual Output
{actual_output}

## Results

| Metric | Expected | Actual | Error | Status |
|--------|----------|--------|-------|--------|
| {metric_1} | {expected} | {actual} | {error} | {PASS|FAIL} |

## Pass/Fail Criteria
{explicit_criteria_for_passing}

## Maxwell Article References
{relevant_articles}

## Related Tests
{links_to_related_tests}
```

## LLM Instructions

When using this template:

1. **Clear Expectations**: State expected result mathematically
2. **Quantitative**: Include numerical tolerances
3. **Reproducible**: Document exact test procedure
4. **Traceable**: Link to Maxwell articles
5. **Actionable**: Clear pass/fail determination

## Variables

- `{test_name}`: Descriptive test name
- `{unique_test_identifier}`: Test ID (e.g., MATH-VEC-001)
- `{component_name}`: Component being tested
- `{unit|integration|validation|convergence}`: Test category
- `{what_is_being_tested_and_why}`: Test description
- `{mathematical_expression_of_expected_result}`: Expected result
- `{brief_derivation_of_expected_result}`: Derivation
- `{source_of_expected_result}`: Reference source
- All parameter and tolerance values
- `{expected_output}`: Expected output
- `{actual_output}`: Actual output from test
- `{explicit_criteria_for_passing}`: Pass/fail criteria
- `{relevant_articles}`: Maxwell citations

## Conditional Logic

IF test is analytical comparison:
  INCLUDE exact analytical solution
  COMPARE at multiple test points

IF test is identity verification:
  STATE the mathematical identity
  VERIFY to machine precision

IF test is convergence:
  INCLUDE multiple grid resolutions
  COMPUTE convergence order

## Example Usage

```markdown
# Test Case: Curl of Gradient is Zero

## Test ID
MATH-VEC-001

## Component Under Test
vector_calculus.curl(), vector_calculus.gradient()

## Test Category
validation

## Expected Result
∇×(∇φ) = 0 for any smooth scalar field φ

## Test Configuration
### Test Function
φ(x,y,z) = x²y + y²z + z²x

### Tolerance
| Type | Value |
|------|-------|
| Absolute | 1e-10 |
| Relative | 1e-10 |

## Results
| Metric | Expected | Actual | Error | Status |
|--------|----------|--------|-------|--------|
| max|curl(grad φ)| | 0 | 2.3e-14 | 2.3e-14 | PASS |
```
