# Task: validation-test-execution

## Description

Executes comprehensive validation test suites for physics implementations. This task workflow guides users through running complete validation campaigns.

## Workflow Steps

### 1. Test Planning
- Identify components to validate
- Select appropriate validation tests
- Define success criteria and tolerances
- Schedule test execution

### 2. Test Setup
- Configure test environment
- Load test fixtures and reference data
- Set up monitoring and logging
- Verify test prerequisites

### 3. Test Execution
- Run unit-level validation
- Run integration tests
- Run system-level tests
- Collect results and metrics

### 4. Result Analysis
- Compare against acceptance criteria
- Identify failures and root causes
- Generate validation report
- Document known issues

## Requirements

**Input:**
- `components`: list - Components to validate
- `test_suite`: str - Test suite name
- `tolerance`: float - Acceptance tolerance
- `output_format`: str - Report format

**Output:**
- `results`: list - Test results
- `summary`: dict - Summary statistics
- `report`: str - Validation report
- `status`: str - Overall status (PASS/FAIL)

## Implementation

```python
from maxwell.quality.tasks import ValidationTestExecution

# Configure validation campaign
campaign = ValidationTestExecution(
    components=['electrostatics', 'magnetostatics', 'electrodynamics'],
    test_suite='physics_validation',
    tolerance=1e-6
)

# Execute tests
results = campaign.execute()

# Generate report
report = campaign.generate_report(format='markdown')
print(report)

# Check status
if results['status'] == 'PASS':
    print("All validation tests passed!")
else:
    print(f"Failed: {results['failed_count']} tests")
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 41-42 | Dimensions and units (validation basis) |
| 75-76 | Gauss's law (validation target) |
| 604-611 | Field equations (validation target) |
