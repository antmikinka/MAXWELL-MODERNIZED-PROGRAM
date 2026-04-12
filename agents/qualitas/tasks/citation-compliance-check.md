# Task: citation-compliance-check

## Description

Ensures all implementations have proper Maxwell article citations and theory classification.

## Workflow Steps

### 1. Codebase Scan
- Parse all function definitions
- Extract citation decorators
- Identify uncited functions
- Build citation database

### 2. Citation Verification
- Check citation format
- Verify article numbers exist
- Confirm part specification
- Validate theory classification

### 3. Accuracy Check
- Verify cited content matches implementation
- Check for missing citations
- Identify false citations
- Assess coverage

### 4. Report Generation
- Create citation coverage report
- List missing citations
- Document issues
- Track remediation

## Requirements

**Input:**
- `codebase_path`: str - Path to codebase
- `check_accuracy`: bool - Verify citation accuracy
- `report_path`: str - Output path

**Output:**
- `coverage`: float - Citation coverage %
- `issues`: list - Citation issues
- `report`: str - Detailed report

## Implementation

```python
from maxwell.quality.tasks import CitationComplianceCheck

# Configure check
checker = CitationComplianceCheck(
    codebase_path='maxwell/',
    check_accuracy=True
)

# Run check
results = checker.run()

print(f"Citation coverage: {results['coverage']}%")
for issue in results['issues']:
    print(f"  - {issue}")
```

## Maxwell Article References

All articles (citation audit covers entire Treatise).
