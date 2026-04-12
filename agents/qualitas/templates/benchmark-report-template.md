# Template: benchmark-report-template

## Description

Template for performance benchmark reports.

## Structure

```markdown
# Benchmark Report

## Configuration
- **Scenario:** {scenario}
- **Resolution:** {resolution}
- **Date:** {date}

## Results
| Metric | Value |
|--------|-------|
| Time | {time} |
| Memory | {memory} |
| Accuracy | {accuracy} |

## Comparison
| Solver | Time | Accuracy | Winner |
|--------|------|----------|--------|
| A | {time} | {acc} | {win} |

## Recommendations
- {recommendation}
```

## LLM Instructions

1. Document benchmark configuration
2. Report all relevant metrics
3. Compare alternatives fairly
4. Provide actionable recommendations
