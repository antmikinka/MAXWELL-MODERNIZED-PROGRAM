# Template: regression-test-template

## Description

Template for defining regression tests.

## Structure

```markdown
# Regression Test: {test_name}

## Background
{issue_being_prevented}

## Test Case
{test_description}

## Expected Behavior
{expected_outcome}

## Verification
- [ ] Test added to suite
- [ ] Test passes currently
- [ ] Test will catch regression
```

## LLM Instructions

1. Document the original issue
2. Create minimal reproducing test
3. Define expected behavior clearly
4. Verify test catches the bug
