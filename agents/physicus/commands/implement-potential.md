# Command: implement-potential

## Description

Implements scalar and vector potential solvers for electrostatic and magnetostatic problems. This command provides the complete potential theory from Maxwell's Parts I and III (Arts. 69-73, 405-406), including Laplace/Poisson equation solutions and vector potential computations.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Articles 69-73 (Electric Potential), 405-406 (Vector Potential)
- **Standard Mathematical Implementation**: PDE solvers, Green's functions, harmonic expansions
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Scalar Potential Theory (Part I)

1. **Electric Potential Definition** (Arts. 69-73)
   ```
   V = ∫ (ρ/r) dτ  (volume integral)
   V = ∫ (σ/r) dS  (surface integral)
   E = -∇V
   ```

2. **Laplace Equation** (Art. 77)
   ```
   ∇²V = 0  (charge-free regions)
   ```
   - Separation of variables solutions
   - Spherical harmonic expansions (Arts. 128-146)
   - Cylindrical harmonic solutions

3. **Poisson Equation** (Art. 77)
   ```
   ∇²V = -4πρ  (with charge distribution)
   ```
   - Direct integration methods
   - Green's function approach (Arts. 96-98)

4. **Boundary Conditions** (Arts. 78a-c)
   - Dirichlet: V specified on boundary
   - Neumann: ∂V/∂n specified
   - Mixed: Linear combination

5. **Method of Images** (Arts. 155-175)
   - Point charge near conducting plane
   - Point charge near conducting sphere
   - Series of images for multiple boundaries

### Vector Potential Theory (Part III & IV)

6. **Vector Potential A Definition** (Arts. 405-406)
   ```
   B = ∇ × A  (magnetic induction from vector potential)
   ```

7. **Vector Potential from Currents** (Arts. 540-541)
   ```
   A = (1/c) ∫ (J/r) dτ  (CGS electromagnetic)
   ```

8. **Gauge Conditions**
   - Coulomb gauge: ∇ · A = 0
   - Lorenz gauge: ∇ · A + (1/c²)∂V/∂t = 0

### Solution Methods

9. **Analytical Methods**
   - Separation of variables
   - Spherical harmonics (Arts. 128-146)
   - Ellipsoidal harmonics (Arts. 147-154)
   - Complex variable methods (Arts. 182-190)

10. **Numerical Methods**
    - Finite difference
    - Finite element
    - Boundary element
    - Fast multipole

## Usage

```python
from maxwell.physics.potential import ScalarPotential, VectorPotential
from maxwell.solvers.laplace import LaplaceSolver
from maxwell.solvers.poisson import PoissonSolver
from maxwell.math.spherical import SphericalHarmonics

# ===== SCALAR POTENTIAL EXAMPLES =====

# Point charge potential
q = PointCharge(position=[0, 0, 0], charge=1.0)
V = ScalarPotential.from_point_charge(
    charge=q,
    observation_point=[1, 0, 0]
)
# V = q/r = 1.0 statvolt

# From charge distribution
rho = ChargeDistribution(...)
V_dist = ScalarPotential.from_distribution(
    distribution=rho,
    method='direct_integration'
)

# Solve Laplace equation with BCs
boundary_conditions = {
    'type': 'dirichlet',
    'values': V_surface,
    'surface': sphere_surface
}
V_laplace = LaplaceSolver.solve(
    domain=exterior_domain,
    boundary_conditions=boundary_conditions,
    method='spherical_harmonics'
)

# Solve Poisson equation
V_poisson = PoissonSolver.solve(
    charge_density=rho,
    boundary_conditions=boundary_conditions,
    method='greens_function'
)

# Method of images
image_config = {
    'charge': q,
    'boundary': 'conducting_plane',
    'plane_position': z=0
}
V_images = ScalarPotential.method_of_images(
    configuration=image_config
)

# ===== VECTOR POTENTIAL EXAMPLES =====

# From current distribution
J = CurrentDensity(...)
A = VectorPotential.from_current(
    current_density=J,
    method='direct_integration'
)

# From magnetic shell
shell = MagneticShell(strength=Phi, boundary=closed_curve)
A_shell = VectorPotential.from_magnetic_shell(shell)

# Verify B = curl(A)
B_from_A = VectorPotential.compute_curl(A)
B_direct = MagneticField.from_source(...)
assert np.allclose(B_from_A, B_direct)

# Spherical harmonic expansion
V_expansion = ScalarPotential.expand_in_harmonics(
    boundary_potential=V_surface,
    degree_max=10
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | ChargeDistribution, CurrentDensity | Source of potential |
| `observation_points` | ndarray | Evaluation points |
| `equation_type` | str | 'laplace', 'poisson', 'vector' |
| `boundary_conditions` | dict | Dirichlet/Neumann/mixed BCs |
| `method` | str | 'analytical', 'numerical', 'images', 'harmonics' |
| `coordinate_system` | str | 'cartesian', 'cylindrical', 'spherical' |
| `expansion_order` | int | Maximum harmonic degree |
| `gauge` | str | 'coulomb', 'lorenz' (for vector potential) |
| `citations` | list | Maxwell article references |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `V` or `Omega` | ScalarField | Scalar potential (statvolt or unit pole potential) |
| `A` | VectorField | Vector potential (gauss·cm in CGS) |
| `field` | VectorField | Derived field (E = -∇V or B = ∇×A) |
| `coefficients` | ndarray | Harmonic expansion coefficients |
| `metadata` | dict | Solution details, convergence, citations |

## Implementation Notes

### Spherical Harmonic Solutions (Arts. 128-146)

For problems with spherical symmetry:
```
V(r,θ,φ) = Σ[n=0 to ∞] Σ[m=-n to n] [A_nm r^n + B_nm r^(-n-1)] Y_nm(θ,φ)
```

Where Y_nm are surface harmonics (Art. 129d) and coefficients determined by boundary conditions.

### Ellipsoidal Solutions (Arts. 147-154)

For ellipsoidal boundaries, use ellipsoidal harmonics with confocal coordinates.

### Method of Images (Arts. 155-175)

For conducting boundaries:
- Single plane: One image charge
- Sphere: One or two image charges depending on grounding
- Multiple boundaries: Infinite series of images

### Green's Function Method (Arts. 96-98)

```
V(r) = ∫ G(r,r') ρ(r') dτ' + surface terms
```

Where G satisfies ∇²G = -4πδ(r-r')

## Validation

### Analytical Benchmarks
- Point charge: V = q/r
- Dipole: V = (p·r̂)/r²
- Uniformly charged sphere: V = Q/R (inside), V = Q/r (outside)
- Conducting sphere in uniform field: V = -E₀r cosθ + E₀R³cosθ/r²

### PDE Verification
- Laplace equation: ∇²V = 0 (verify numerically)
- Poisson equation: ∇²V = -4πρ (verify residual)
- Boundary conditions satisfied to tolerance

### Vector Potential Checks
- Gauge condition: ∇ · A = 0 (Coulomb gauge)
- Curl relation: B = ∇ × A (verify against direct calculation)
- Asymptotic behavior: A ~ 1/r for localized currents

## Maxwell Article References

| Article | Content |
|---------|---------|
| 69-73 | Electric potential definition and properties |
| 77 | Laplace and Poisson equations |
| 78a-c | Boundary conditions at interfaces |
| 96-98 | Green's theorem and Green's function |
| 128-146 | Spherical harmonics theory |
| 147-154 | Ellipsoidal harmonics |
| 155-175 | Method of images |
| 385-386 | Magnetic scalar potential |
| 405-406 | Vector potential definition |
| 540-541 | Electrotonic state (vector potential) |

## Related Commands

- `implement-field` - Compute fields from potentials
- `implement-constitutive` - Material boundary conditions
- `solve-analytical` - Benchmark analytical solutions
- `derive-equations` - Derive potential equations

## Error Handling

- Raises `BoundaryConditionError` if BCs are inconsistent
- Warns about slow convergence for harmonic expansions
- Flags singular points for special treatment
- Validates gauge conditions for vector potential

## Theory Preservation Protocol

Before any potential computation:
1. Identify source category (Maxwell/User/Standard)
2. Apply appropriate citation label
3. For User theories: IMPLEMENT EXACTLY AS SPECIFIED - DO NOT ALTER
4. For Maxwell: Implement as described in Treatise
5. Document all mathematical assumptions
