# Command: validate-math

## Description

Provides mathematical verification and testing for all mathematical implementations. This command ensures correctness through analytical comparison, identity verification, and numerical accuracy assessment.

## Functionality

### Validation Categories

1. **Analytical Comparison**
   - Compare numerical results against known analytical solutions
   - Special function verification (Legendre, Bessel, etc.)
   - Integral and derivative verification

2. **Identity Verification**
   - Vector calculus identities (∇×∇φ = 0, ∇·(∇×A) = 0)
   - Spherical harmonic orthogonality
   - Quaternion algebraic properties
   - Tensor transformation rules

3. **Convergence Testing**
   - Grid convergence for numerical methods
   - Series convergence for expansions
   - Iterative method convergence

4. **Conservation Laws**
   - Energy conservation in conservative fields
   - Flux conservation (divergence theorem)
   - Circulation conservation (Stokes' theorem)

5. **Dimensional Analysis**
   - Unit consistency checks
   - Scaling behavior verification
   - Buckingham π theorem applications

### Validation Tests

| Test Type | Description | Tolerance |
|-----------|-------------|-----------|
| `unit-test` | Basic functionality tests | Machine precision |
| `analytical` | Compare to known solutions | 1e-10 relative |
| `identity` | Mathematical identity verification | 1e-12 relative |
| `convergence` | Grid/series convergence | Order verification |
| `conservation` | Conservation law verification | 1e-8 relative |
| `dimensional` | Unit consistency | Exact |

## Usage

```python
from maxwell.mathematics.validation import MathematicalValidator
from maxwell.core.vector import VectorField
import numpy as np

validator = MathematicalValidator()

# === VECTOR CALCULUS VALIDATION ===

# Verify curl(grad φ) = 0 for any scalar field
def test_phi(x, y, z):
    return x**2 * y + y**2 * z + z**2 * x

curl_grad_result = validator.verify_curl_gradient(test_phi)
print(f"||curl(grad φ)|| max: {curl_grad_result.max_norm}")
# Should be ~machine precision

# Verify div(curl A) = 0 for any vector field
def test_A(x, y, z):
    return [x**2 * y, y**2 * z, z**2 * x]

div_curl_result = validator.verify_divergence_curl(test_A)
print(f"|div(curl A)| max: {div_curl_result.max_value}")
# Should be ~machine precision

# Verify Stokes' theorem
stokes_result = validator.verify_stokes_theorem(
    vector_field=test_A,
    surface='hemisphere',
    radius=1.0
)
print(f"Stokes' theorem error: {stokes_result.relative_error}")
# Should be < 1e-6

# Verify Divergence theorem
divergence_result = validator.verify_divergence_theorem(
    vector_field=test_A,
    volume='sphere',
    radius=1.0
)
print(f"Divergence theorem error: {divergence_result.relative_error}")

# === SPHERICAL HARMONICS VALIDATION ===

# Verify orthogonality of spherical harmonics
ortho_result = validator.verify_spherical_harmonic_orthogonality(
    l_max=6,
    quadrature_order=32
)
print(f"Orthogonality error: {ortho_result.max_error}")
# Should be < 1e-10

# Verify recurrence relations for Legendre polynomials
recurrence_result = validator.verify_legendre_recurrence(n_max=20)
print(f"Recurrence relation error: {recurrence_result.max_error}")

# === QUATERNION VALIDATION ===

# Verify quaternion associativity: (pq)r = p(qr)
assoc_result = validator.verify_quaternion_associativity(num_tests=1000)
print(f"Associativity error: {assoc_result.max_error}")

# Verify norm property: |pq| = |p||q|
norm_result = validator.verify_quaternion_norm_property(num_tests=1000)
print(f"Norm property error: {norm_result.max_error}")

# Verify rotation preserves length
rotation_result = validator.verify_quaternion_rotation_isometry(num_tests=100)
print(f"Rotation isometry error: {rotation_result.max_error}")

# === TENSOR VALIDATION ===

# Verify tensor transformation rules
transform_result = validator.verify_tensor_transformation(
    tensor_type='rank2_symmetric',
    num_rotations=100
)
print(f"Tensor transformation error: {transform_result.max_error}")

# Verify Maxwell stress tensor gives correct force
force_result = validator.verify_maxwell_stress_force(
    charge=1.0,
    sphere_radius=5.0
)
print(f"Force calculation error: {force_result.relative_error}")

# === CONVERGENCE TESTING ===

# Grid convergence for Laplace solver
convergence_result = validator.grid_convergence_analysis(
    solver='laplace_fd',
    exact_solution='dipole',
    grid_refinements=[10, 20, 40, 80]
)
print(f"Convergence order: {convergence_result.order}")
# Should be ~2 for second-order finite differences

# Series convergence for spherical harmonic expansion
series_result = validator.series_convergence_analysis(
    expansion='spherical_harmonic',
    function='point_charge_potential',
    max_order=50
)
print(f"Series convergence rate: {series_result.convergence_rate}")

# === CONSERVATION LAWS ===

# Energy conservation in electrostatic field
energy_result = validator.verify_energy_conservation(
    charge_distribution='point',
    integration_volume='sphere'
)
print(f"Energy conservation error: {energy_result.relative_error}")

# === REPORT GENERATION ===

# Run full validation suite
full_report = validator.run_full_suite()
full_report.print_summary()
full_report.save_to_json('validation_report.json')

# Run specific category
math_report = validator.run_category('identity')
math_report.print_summary()
```

## Implementation Notes

- Uses high-precision arithmetic for reference calculations when needed
- Statistical testing with multiple random samples
- Both absolute and relative error reporting
- Tolerance levels appropriate for each test type
- Automated report generation with pass/fail status

## Validation Output

```
=== MATHEMATICAL VALIDATION REPORT ===
Date: 2026-04-11
Suite: Full Mathematical Validation

Vector Calculus Identities:
  [PASS] curl(grad φ) = 0           error: 2.3e-14
  [PASS] div(curl A) = 0            error: 1.1e-14
  [PASS] Stokes' theorem            error: 4.7e-07
  [PASS] Divergence theorem         error: 3.2e-07

Spherical Harmonics:
  [PASS] Orthogonality              error: 8.9e-11
  [PASS] Recurrence relations       error: 1.2e-12
  [PASS] Addition theorem           error: 5.4e-10

Quaternions:
  [PASS] Associativity              error: 3.1e-15
  [PASS] Norm property              error: 2.8e-15
  [PASS] Rotation isometry          error: 1.9e-14

Tensors:
  [PASS] Transformation rules       error: 4.5e-14
  [PASS] Maxwell stress force       error: 1.2e-08

Convergence:
  [PASS] Laplace solver (2nd order) order: 2.01
  [PASS] Spherical expansion        rate: exponential

OVERALL: ALL TESTS PASSED (14/14)
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector identity foundations |
| 20-27 | Divergence and curl theorems |
| 77-78 | Laplace operator properties |
| 125-133 | Spherical harmonic properties |

## Related Commands

- `vector-calculus-ops` - Operations to validate
- `spherical-harmonics` - Functions to validate
- `quaternion-algebra` - Algebra to validate
- `tensor-ops` - Tensor operations to validate
