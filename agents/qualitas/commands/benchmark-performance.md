# Command: benchmark-performance

## Description

Runs performance benchmarks and accuracy comparisons for electromagnetic implementations. Measures execution time, memory usage, and numerical accuracy.

## Functionality

### Performance Metrics

1. **Execution Time**
   - Wall clock time
   - CPU time
   - Time per iteration/step
   - Scaling with problem size

2. **Memory Usage**
   - Peak memory
   - Memory per grid point
   - Scaling with resolution

3. **Accuracy**
   - Error vs. analytical solution
   - Error vs. reference implementation
   - Accuracy per unit time

4. **Efficiency**
   - Accuracy/time
   - Problem size scalability
   - Parallel efficiency

### Benchmark Scenarios

- Point charge field (small)
- Dipole radiation (medium)
- Waveguide mode (medium)
- Full Maxwell solver (large)
- Multi-scale problem (very large)

## Usage

```python
from maxwell.quality.benchmark import PerformanceBenchmark

# Create benchmark
benchmark = PerformanceBenchmark()

# Run standard benchmarks
results = benchmark.run_suite(
    scenarios=['small', 'medium', 'large'],
    repetitions=3
)

# Run specific benchmark
result = benchmark.run_benchmark(
    name='waveguide_mode',
    solver=fdtd_solver,
    resolution=[100, 50, 50],
    time_steps=1000
)

# Compare solvers
comparison = benchmark.compare_solvers(
    solvers=[fdtd_solver, fem_solver],
    scenario='cavity_resonance'
)

# Generate report
report = benchmark.generate_report(format='markdown')
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `scenario` | str | Benchmark scenario |
| `solver` | Solver | Solver to benchmark |
| `resolution` | array | Grid resolution |
| `repetitions` | int | Number of runs |
| `compare` | bool | Compare multiple solvers |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `results` | BenchmarkResults | Timing and accuracy |
| `comparison` | dict | Solver comparison |
| `report` | str | Performance report |

## Benchmark Scenarios

### Small Problem
| Parameter | Value |
|-----------|-------|
| Grid | 50³ cells |
| Time steps | 100 |
| Expected time | < 1 second |
| Memory | < 100 MB |

### Medium Problem
| Parameter | Value |
|-----------|-------|
| Grid | 100³ cells |
| Time steps | 1000 |
| Expected time | < 1 minute |
| Memory | < 1 GB |

### Large Problem
| Parameter | Value |
|-----------|-------|
| Grid | 200³ cells |
| Time steps | 10000 |
| Expected time | < 10 minutes |
| Memory | < 10 GB |

## Output Format

```
============================================================
PERFORMANCE BENCHMARK REPORT
============================================================

Scenario: Waveguide Mode
Resolution: 100 × 50 × 50 cells
Time steps: 1000

EXECUTION TIME
--------------
Run 1: 12.34 seconds
Run 2: 12.28 seconds
Run 3: 12.31 seconds
Average: 12.31 ± 0.03 seconds

Per time step: 12.31 ms
Per cell per step: 2.46 ns

MEMORY USAGE
------------
Peak memory: 234.5 MB
Per cell: 93.8 KB

ACCURACY
--------
L2 error vs. analytical: 1.23e-4
L∞ error: 5.67e-4
Cutoff frequency error: 0.02%

EFFICIENCY
----------
Accuracy/time: 9.8e-6 per second
Cells/ms: 406,000

============================================================
COMPARISON: FDTD vs FEM
============================================================

Metric          FDTD      FEM       Winner
Time (s)        12.31     45.67     FDTD
Memory (MB)     234.5     189.2     FEM
L2 Error        1.23e-4   5.67e-5   FEM
Accuracy/time   9.8e-6    1.2e-6    FDTD

============================================================
```

## Scaling Analysis

| Resolution | Time (s) | Memory (MB) | Time/Cell |
|------------|----------|-------------|-----------|
| 50³ | 0.5 | 50 | 4.0e-6 |
| 100³ | 12.3 | 234 | 2.5e-6 |
| 200³ | 156.2 | 1456 | 1.9e-6 |

Expected scaling: O(N) for time, O(N) for memory

## Maxwell Article References

Performance benchmarks are modern computational tools, not explicitly covered in Maxwell's text.

## Related Commands

- `convergence-study` - Accuracy analysis
- `integration-test` - System testing
- `validate-physics` - Physics validation
