# Task: analytical-benchmark-comparison

## Description

Compares numerical implementations against known analytical solutions for benchmark validation.

## Workflow Steps

### 1. Select Benchmark
- Choose appropriate analytical solution
- Define geometry and parameters
- Set up numerical simulation
- Configure comparison metrics

### 2. Run Simulation
- Execute numerical solver
- Extract results at comparison points
- Compute error metrics
- Document numerical parameters

### 3. Compare Results
- Compute relative error
- Check against tolerance
- Identify discrepancy sources
- Assess accuracy

### 4. Document Comparison
- Record benchmark results
- Note numerical parameters
- Assess validation status

## Requirements

**Input:**
- `benchmark_name`: str - Analytical solution name
- `numerical_result`: dict - Simulation output
- `tolerance`: float - Acceptance tolerance

**Output:**
- `comparison`: dict - Expected vs actual
- `error`: float - Relative error
- `status`: str - PASS/FAIL

## Implementation

```python
from maxwell.quality.tasks import AnalyticalBenchmarkComparison

# Configure comparison
comparison = AnalyticalBenchmarkComparison(
    benchmark_name='point_charge_field',
    numerical_result=simulation_output,
    tolerance=1e-6
)

# Run comparison
result = comparison.compare()

print(f"Benchmark error: {result['error']}")
print(f"Status: {result['status']}")
```

## Maxwell Article References

Varies by benchmark selected.
