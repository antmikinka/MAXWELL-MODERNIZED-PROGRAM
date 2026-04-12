# Task: electrostatic-problem-solution

## Description

Solves electrostatic boundary value problems using analytical and numerical methods from Maxwell's Part I (Arts. 77-180). This task workflow guides the user through formulating and solving electrostatic problems with various boundary conditions.

## Workflow Steps

### 1. Problem Formulation
- Define geometry and coordinate system
- Specify charge distribution ρ(x,y,z)
- Identify boundary conditions (Dirichlet, Neumann, mixed)
- Determine symmetry properties

### 2. Method Selection
- **Analytical**: For simple geometries (sphere, cylinder, plane)
- **Method of Images**: For conducting boundaries
- **Separation of Variables**: For rectangular, cylindrical, spherical
- **Spherical Harmonics**: For problems with spherical symmetry
- **Numerical**: For complex geometries (FEM, BEM)

### 3. Solution Implementation
- Set up governing equation (Laplace or Poisson)
- Apply boundary conditions
- Solve for potential V(x,y,z)
- Compute E = -∇V

### 4. Validation
- Check boundary conditions satisfied
- Verify ∇ · E = 4πρ
- Compare with known limiting cases
- Energy conservation check

## Requirements

**Input:**
- `geometry`: dict - Domain geometry and boundaries
- `charge_distribution`: ChargeDistribution or dict
- `boundary_conditions`: dict - BCs on each surface
- `method`: str - Solution method
- `precision`: float - Numerical tolerance

**Output:**
- `potential`: ScalarField - V(x,y,z)
- `electric_field`: VectorField - E(x,y,z)
- `surface_charge`: dict - Induced σ on conductors
- `energy`: float - Total electrostatic energy
- `validation`: dict - Verification results

## Implementation

```python
from maxwell.tasks.electrostatics import ElectrostaticProblemSolver
from maxwell.core import PointCharge, ConductingSphere
from maxwell.physics.electrostatics import ElectrostaticField

# Problem: Point charge near grounded conducting sphere
problem = {
    'geometry': {
        'type': 'exterior',
        'boundary': ConductingSphere(radius=10, center=[0,0,0], potential=0)
    },
    'sources': [PointCharge(position=[20, 0, 0], charge=1.0)],
    'boundary_conditions': {'sphere': 'dirichlet', 'value': 0},
    'method': 'image_charge'
}

solver = ElectrostaticProblemSolver(problem)

# Solve
result = solver.solve()

# Result includes:
# - Image charge location and magnitude
# - Potential everywhere (analytical formula)
# - Electric field
# - Induced surface charge density
# - Force on point charge

# Validation
validation = solver.validate(
    checks=['boundary_conditions', 'gauss_law', 'energy']
)

# For complex geometries, use numerical method
problem_numerical = {
    'geometry': {'type': 'custom', 'mesh': 'complex_geometry.msh'},
    'sources': [...],
    'boundary_conditions': {...},
    'method': 'fem'
}

solver_numerical = ElectrostaticProblemSolver(problem_numerical)
result_numerical = solver_numerical.solve(
    mesh_refinement=True,
    adaptive=True
)
```

## Example Problems

### 1. Conducting Sphere in Uniform Field
```python
# External field E₀ in z-direction
# Sphere of radius a at potential 0
# Solution: V = -E₀(r - a³/r²)cos(θ)
```

### 2. Point Charge Between Parallel Plates
```python
# Two infinite grounded plates at z=0 and z=d
# Point charge q at z=d/2
# Solution: Infinite series of image charges
```

### 3. Charged Conducting Ellipsoid
```python
# Ellipsoid with semi-axes a, b, c
# Total charge Q
# Solution: Ellipsoidal harmonics
```

## Validation Criteria

- [ ] Potential satisfies Laplace/Poisson equation
- [ ] Boundary conditions satisfied to tolerance
- [ ] Gauss's law verified for closed surfaces
- [ ] Energy computed via ∫ρV dV and ∫E² dV agree
- [ ] Force via energy gradient matches direct calculation

## Maxwell Article References

| Article | Content |
|---------|---------|
| 77-78 | Laplace and Poisson equations |
| 95-100 | Green's theorem and functions |
| 100-103 | Thomson's theorem |
| 155-175 | Method of images |
| 128-145 | Spherical harmonics |

## Related Tasks

- `magnetic-circuit-design` - Analogous magnetostatic problem
- `current-distribution-analysis` - Steady flow analog
- `wave-equation-solution` - Time-dependent extension
