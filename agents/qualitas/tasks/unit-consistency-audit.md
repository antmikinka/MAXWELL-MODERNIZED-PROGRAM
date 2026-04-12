# Task: unit-consistency-audit

## Description

Performs comprehensive audit of CGS unit consistency across codebase. Ensures all implementations use correct CGS units without SI contamination.

## Workflow Steps

### 1. Codebase Scan
- Parse all Python files
- Extract function signatures and annotations
- Identify unit-related constants
- Find dimensional expressions

### 2. Dimensional Analysis
- Check input/output dimensions
- Verify equation consistency
- Validate constant values
- Detect SI concepts (ε₀, μ₀)

### 3. Issue Classification
- Categorize unit errors
- Prioritize fixes
- Generate fix recommendations
- Track remediation

### 4. Report Generation
- Create unit consistency report
- Document all issues found
- Provide remediation guidance
- Sign off on compliance

## Requirements

**Input:**
- `codebase_path`: str - Path to codebase
- `strict_mode`: bool - Fail on any SI contamination
- `report_path`: str - Output report path

**Output:**
- `issues`: list - Unit consistency issues
- `compliance_score`: float - 0-100% score
- `report`: str - Detailed report

## Implementation

```python
from maxwell.quality.tasks import UnitConsistencyAudit

# Configure audit
audit = UnitConsistencyAudit(
    codebase_path='maxwell/',
    strict_mode=True
)

# Run audit
results = audit.run()

# Get compliance score
score = results['compliance_score']
print(f"Unit compliance: {score}%")

# Review issues
for issue in results['issues']:
    print(f"{issue['severity']}: {issue['description']}")
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 41-42 | Dimensions and units |
