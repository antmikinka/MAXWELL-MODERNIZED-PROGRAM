# Tolerance Guidelines

## Purpose

Guidelines for setting appropriate validation tolerances.

## Tolerance Levels

| Level | Tolerance | Use Case |
|-------|-----------|----------|
| Exact | 1e-12 | Mathematical identities |
| Analytical | 1e-8 | Analytical solution comparison |
| Physics | 1e-6 | Physics law verification |
| Numerical | 1e-4 | Numerical method validation |
| System | 1e-3 | Full system integration |

## Setting Tolerances

### Consider Factors
1. Numerical precision (float64 ~ 1e-15)
2. Discretization error
3. Round-off accumulation
4. Physical significance

### Recommended Approach
```
tolerance = max(
    1e-6,  # floor tolerance
    10 * expected_numerical_error,
    100 * machine_epsilon
)
```

## Tolerance by Test Type

| Test Type | Recommended | Justification |
|-----------|-------------|---------------|
| Unit tests | 1e-10 | Isolated functions |
| Integration | 1e-6 | Accumulated errors |
| Physics | 1e-4 | Physical approximations |
| Performance | 5% | Natural variation |

## Usage

Apply these guidelines when setting validation tolerances.
