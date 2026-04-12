# Template: test-report-template

## Description

Template for generating validation test reports.

## Structure

```markdown
# Validation Test Report

## Summary
- **Date:** {date}
- **Component:** {component}
- **Tests Run:** {count}
- **Pass Rate:** {percentage}%

## Results by Category

### Physics Validation
| Test | Expected | Actual | Error | Status |
|------|----------|--------|-------|--------|
| {test} | {exp} | {act} | {err} | {status} |

### Unit Consistency
| Function | Dimensions | Status |
|----------|------------|--------|
| {func} | {dims} | {status} |

### Conservation Laws
| Law | Balance Error | Status |
|-----|---------------|--------|
| Energy | {error} | {status} |

## Issues Found
| Issue | Severity | Status |
|-------|----------|--------|
| {issue} | {sev} | {status} |

## Sign-off
- Physics Lead: _______________
- QA Lead: _______________
```

## LLM Instructions

1. Include all test results
2. Highlight failures prominently
3. Provide actionable issue descriptions
4. Document sign-off requirements
