# Command: vector-calculus-ops

## Description

Implements core vector calculus operations essential for Maxwell's electromagnetic theory. This command provides gradient, divergence, curl, and Laplacian operations for scalar and vector fields in multiple coordinate systems.

## Functionality

### Operations

1. **Gradient** (`grad`)
   - Scalar field to vector field
   - Cartesian, cylindrical, spherical coordinates
   - Article references: 15-18, 23-27

2. **Divergence** (`div`)
   - Vector field to scalar field
   - Flux interpretation
   - Article references: 20-22, 77-78

3. **Curl** (`curl`)
   - Vector field to vector field
   - Circulation interpretation
   - Article references: 23-27

4. **Laplacian** (`laplacian`)
   - Scalar/vector field to same type
   - Laplace and Poisson equations
   - Article references: 77-78, 100-103

5. **Vector Identities** (`identities`)
   - curl(grad) = 0
   - div(curl) = 0
   - Product rules

### Coordinate Systems

- Cartesian (x, y, z)
- Cylindrical (ρ, φ, z)
- Spherical (r, θ, φ)

## Usage

```python
from maxwell.core.vector import VectorField
from maxwell.mathematics import vector_calculus

# Create a scalar field (electric potential)
phi = ScalarField(lambda x, y, z: x**2 + y**2 + z**2)

# Compute gradient (electric field = -grad(phi))
E = vector_calculus.gradient(phi, coords='cartesian')

# Create a vector field (magnetic induction)
B = VectorField(
    lambda x, y, z: [0, 0, x**2 + y**2]
)

# Compute divergence (should be 0 for solenoidal fields)
div_B = vector_calculus.divergence(B, coords='cartesian')

# Compute curl
curl_B = vector_calculus.curl(B, coords='cartesian')

# Compute Laplacian
lap_phi = vector_calculus.laplacian(phi, coords='cartesian')
```

## Implementation Notes

- Uses NumPy broadcasting for efficient computation
- Symbolic verification available via SymPy integration
- CGS units by default, SI conversion available
- All operations decorated with article citations

## Validation

- Verified against analytical solutions
- Divergence theorem tests
- Stokes' theorem tests
- Vector identity verification

## Related Commands

- `spherical-harmonics` - For spherical coordinate expansions
- `potential-theory` - For Laplace/Poisson solvers
- `validate-math` - For mathematical verification

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector quantities and addition |
| 20-22 | Flux and divergence |
| 23-27 | Curl and rotation |
| 77-78 | Laplace operator |
| 100-103 | Potential theory |
