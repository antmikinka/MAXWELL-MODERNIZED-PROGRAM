# Command: convergence-study

## Description

Performs numerical convergence studies to verify accuracy and order of numerical methods. This command validates that numerical solutions converge to correct answers.

## Functionality

### Convergence Analysis

1. **Mesh Refinement Studies**
   - Systematically refine spatial grid
   - Track error vs. grid spacing
   - Verify convergence rate matches theory
   - Identify asymptotic range

2. **Time Step Studies**
   - Refine temporal resolution
   - Verify temporal order of accuracy
   - Check CFL stability limit
   - Identify optimal time step

3. **Order Verification**
   - Compute observed order of accuracy
   - Compare with theoretical order
   - Richardson extrapolation
   - Error estimation

### Error Metrics

- L₂ norm (RMS error)
- L_∞ norm (maximum error)
- Relative error
- Absolute error

## Usage

```python
from maxwell.quality.convergence import ConvergenceStudy

# Create study
study = ConvergenceStudy()

# Run mesh refinement study
results = study.mesh_refinement(
    solver=fdtd_solver,
    analytical_solution=plane_wave_solution,
    base_resolution=[50, 50, 50],
    refinement_levels=4,
    error_metric='L2'
)

# Run time step study
results = study.time_refinement(
    solver=fdtd_solver,
    base_dt=1e-15,
    refinement_levels=4,
    error_metric='L2'
)

# Compute observed order
order = study.compute_order(results)

# Generate convergence plot
plot = study.plot_convergence(results)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `solver` | Solver | Numerical solver |
| `analytical_solution` | callable | Reference solution |
| `base_resolution` | array | Coarsest grid |
| `refinement_levels` | int | Number of refinements |
| `error_metric` | str | 'L2', 'L∞', 'relative' |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `results` | ConvergenceResults | Error vs. resolution |
| `order` | float | Observed order of accuracy |
| `plot` | Figure | Convergence plot |

## Expected Convergence Rates

| Method | Spatial Order | Temporal Order |
|--------|---------------|----------------|
| FDTD (Yee) | 2nd | 2nd |
| FEM (linear) | 2nd | Depends |
| FEM (quadratic) | 3rd | Depends |
| Spectral | Exponential | Depends |
| RK4 | Depends | 4th |

## Output Format

```
============================================================
CONVERGENCE STUDY: FDTD Plane Wave
============================================================

MESH REFINEMENT STUDY
---------------------
Level  Resolution    h (cm)     L2 Error     Rate
0      50³           0.100      1.23e-2      -
1      100³          0.050      3.12e-3      1.98
2      200³          0.025      7.85e-4      1.99
3      400³          0.0125     1.97e-4      2.00

Observed Order: 1.99
Expected Order: 2.00
Status: PASS (order within 5%)

TIME STEP REFINEMENT STUDY
--------------------------
Level  dt (s)       L2 Error     Rate
0      1.00e-15     5.67e-3      -
1      5.00e-16     1.42e-3      2.00
2      2.50e-16     3.56e-4      2.00
3      1.25e-16     8.91e-5      2.00

Observed Order: 2.00
Expected Order: 2.00
Status: PASS

============================================================
SUMMARY: Convergence verified
Spatial order: 1.99 (expected 2.00)
Temporal order: 2.00 (expected 2.00)
============================================================
```

## Richardson Extrapolation

```
If u_h = u_exact + C h^p + O(h^{p+1})

Then: u_exact ≈ (2^p * u_{h/2} - u_h) / (2^p - 1)

And: error estimate = |u_{h/2} - u_h| / (2^p - 1)
```

## Maxwell Article References

Convergence studies are modern numerical validation tools, not explicitly covered in Maxwell's text. However, they validate implementations of:

| Article | Content | Validation |
|---------|---------|------------|
| 781-785 | Wave equation | Wave propagation |
| 604-611 | Field equations | Full Maxwell solver |

## Related Commands

- `validate-physics` - Physics validation
- `test-analytical` - Analytical benchmarks
- `benchmark-performance` - Performance tests
