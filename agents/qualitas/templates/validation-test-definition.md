# Template: validation-test-definition

## Description

Template for defining validation tests for physics implementations.

## Structure

```markdown
# Validation Test: {test_name}

## Test Information
- **ID:** {test_id}
- **Component:** {component_name}
- **Maxwell Articles:** {citations}
- **Category:** {category}

## Test Objective
{what_this_test_validates}

## Test Setup
{test_configuration}

## Expected Result
{expected_outcome}

## Acceptance Criteria
- Tolerance: {tolerance}
- Pass condition: {condition}

## Test Procedure
1. {step_1}
2. {step_2}
...

## Validation
- [ ] Test implemented
- [ ] Expected result documented
- [ ] Acceptance criteria defined
```

## LLM Instructions

1. Link test to specific Maxwell articles
2. Define quantitative acceptance criteria
3. Document expected results precisely
4. Include tolerance specifications
