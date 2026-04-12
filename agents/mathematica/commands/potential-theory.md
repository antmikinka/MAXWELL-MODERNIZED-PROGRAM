# Command: potential-theory

## Description

Implements potential theory for solving Laplace and Poisson equations in electrostatics and magnetostatics. This is foundational for Maxwell's treatment of electric and magnetic potentials (Articles 77-78, 100-103, 371-390).

## Functionality

### Governing Equations

1. **Laplace Equation** (source-free regions)
   - ∇²φ = 0
   - Electrostatics: charge-free regions
   - Magnetostatics: current-free regions

2. **Poisson Equation** (with sources)
   - ∇²φ = -4πρ (CGS electrostatics)
   - ∇²φ = -ρ/ε₀ (SI electrostatics)
   - ∇²A = -4πJ/c (CGS magnetostatics, vector potential)

3. **Green's Functions**
   - Free space: G(r,r') = 1/|r-r'|
   - Dirichlet boundary conditions
   - Neumann boundary conditions
   - Method of images

### Solution Methods

1. **Analytical Solutions**
   - Separation of variables
   - Spherical harmonic expansion
   - Cylindrical harmonic (Bessel) expansion
   - Conformal mapping (2D)

2. **Numerical Solutions**
   - Finite difference method
   - Finite element method (optional)
   - Boundary element method
   - Relaxation methods

3. **Integral Methods**
   - Single layer potential
   - Double layer potential
   - Green's reciprocal theorem

### Boundary Conditions

- Dirichlet: φ specified on boundary
- Neumann: ∂φ/∂n specified on boundary
- Mixed: Linear combination
- Interface: Continuity conditions

## Usage

```python
from maxwell.mathematics.potential import PotentialSolver
from maxwell.core.boundary import BoundaryConditions
import numpy as np

solver = PotentialSolver()

# === ANALYTICAL SOLUTIONS ===

# Point charge potential (fundamental solution)
phi_point = solver.point_charge(q=1.0, position=[0, 0, 0])
# φ = q/r (CGS units)

# Line charge potential
phi_line = solver.line_charge(lambda_=1.0, axis='z')
# φ = -2λ ln(r) (CGS units)

# Dipole potential
phi_dipole = solver.dipole(moment=[0, 0, 1], position=[0, 0, 0])
# φ = (p·r)/r³

# Sphere with uniform charge (interior and exterior)
phi_sphere = solver.charged_sphere(
    radius=5.0,
    total_charge=10.0,
    region='both'
)

# === BOUNDARY VALUE PROBLEMS ===

# Dirichlet problem: potential specified on boundary
bc_dirichlet = BoundaryConditions.dirichlet(
    boundary='sphere',
    radius=10.0,
    potential=lambda theta, phi: 100 * np.cos(theta)
)
solution = solver.solve_laplace(
    domain='sphere_interior',
    boundary_conditions=bc_dirichlet,
    method='spherical_harmonics'
)

# Method of images: point charge near conducting plane
image_solution = solver.method_of_images(
    source_charge=1.0,
    source_position=[0, 0, 5],
    conducting_plane='z=0'
)
# Creates image charge at [0, 0, -5] with opposite sign

# === NUMERICAL SOLUTIONS ===

# Finite difference solution on a grid
grid = solver.create_grid(
    shape=(50, 50, 50),
    extent=[[-10, 10], [-10, 10], [-10, 10]]
)

# Poisson equation with charge distribution
rho = np.exp(-(grid.x**2 + grid.y**2 + grid.z**2) / 4)
phi_numerical = solver.solve_poisson(
    rho=rho,
    grid=grid,
    method='relaxation',
    tolerance=1e-6
)

# === GREEN'S FUNCTIONS ===

# Free space Green's function
G = solver.green_function_free_space(r=[1, 0, 0], r_prime=[0, 0, 0])
# G = 1/|r - r'|

# Dirichlet Green's function for half-space
G_half = solver.green_function_dirichlet(
    domain='half_space',
    r=[1, 0, 1],
    r_prime=[0, 0, 2],
    boundary_plane='z=0'
)

# === INTEGRAL REPRESENTATIONS ===

# Single layer potential (surface charge distribution)
sigma = lambda x, y: np.exp(-(x**2 + y**2))  # Surface charge density
phi_single = solver.single_layer_potential(
    surface='disk',
    radius=5.0,
    density=sigma,
    observation_point=[0, 0, 3]
)

# Double layer potential (dipole layer)
tau = lambda x, y: 1.0  # Dipole moment density
phi_double = solver.double_layer_potential(
    surface='sphere',
    radius=5.0,
    density=tau,
    observation_point=[0, 0, 10]
)
```

## Implementation Notes

- CGS units by default (Gaussian system)
- Analytical solutions use special functions (Legendre, Bessel)
- Numerical solutions use iterative methods (SOR, multigrid)
- Green's functions include image charge constructions
- Spherical harmonic expansion for spherical boundaries

## Validation

- Laplace equation satisfied: ∇²φ = 0 (numerically verified)
- Poisson equation satisfied: ∇²φ = -4πρ
- Boundary conditions met to specified tolerance
- Gauss's law verified for enclosed charges
- Comparison with known analytical solutions

## Maxwell Article References

| Article | Content |
|---------|---------|
| 77-78 | Laplace operator and potential |
| 100-103 | Potential theory fundamentals |
| 113-116 | Poisson equation for electricity |
| 371-390 | Magnetic potential theory |
| 413-429 | Potential of magnetic shells |

## Related Commands

- `spherical-harmonics` - For spherical boundary problems
- `vector-calculus-ops` - For gradient (field) computation
- `validate-math` - For PDE solution verification
