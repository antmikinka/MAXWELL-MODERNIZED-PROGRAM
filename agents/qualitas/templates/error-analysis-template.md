# Template: error-analysis-template

## Description

Template for documenting numerical error analysis.

## Structure

```markdown
# Error Analysis: {component}

## Error Sources
1. {source_1}: {description}
2. {source_2}: {description}

## Error Metrics
- L2 norm: {value}
- L∞ norm: {value}
- Relative: {value}

## Convergence
| Resolution | Error | Rate |
|------------|-------|------|
| {res} | {err} | {rate} |

## Recommendations
- {recommendation}
```

## LLM Instructions

1. Identify all error sources
2. Report multiple error metrics
3. Document convergence behavior
4. Provide improvement recommendations
