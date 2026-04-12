# Task: Electrostatic Field Solution

## Description

Complete workflow for solving electrostatic field problems using Maxwell's Part I theory. This task guides through the complete process from problem definition to validated solution.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 27-229 (Part I: Electrostatics)
- **Standard Mathematical Implementation**: PDE solvers, boundary value problems
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Problem Definition

**Step 1.1: Define Geometry**
```python
from maxwell.tasks.electrostatics import ElectrostaticProblem

problem = ElectrostaticProblem(
    name='conducting_sphere_in_field',
    geometry={
        'type': 'sphere',
        'radius': R=1.0,  # cm
        'center': [0, 0, 0]
    },
    boundary_conditions={
        'sphere_surface': {'type': 'dirichlet', 'value': 0},  # grounded
        'infinity': {'type': 'uniform_field', 'E0': [0, 0, 1]}
    }
)
```

**Step 1.2: Define Charge Distribution**
```python
# Option A: Point charges
problem.add_point_charge(q=1.0, position=[2, 0, 0])

# Option B: Continuous distribution
problem.add_charge_distribution(
    rho=lambda x, y, z: exp(-(x**2 + y**2 + z**2)),
    support='all_space'
)

# Option C: Surface charge
problem.add_surface_charge(
    sigma=lambda theta, phi: sigma_0 * cos(theta),
    surface='sphere'
)
```

**Step 1.3: Define Material Properties**
```python
problem.set_material(
    region='exterior',
    material='vacuum',
    epsilon=1.0
)

problem.set_material(
    region='interior',
    material='conductor',
    conductivity='infinite'
)
```

### Phase 2: Method Selection

**Step 2.1: Choose Solution Method**

| Geometry | Recommended Method | Maxwell Articles |
|----------|-------------------|------------------|
| Spherical | Spherical harmonics | 128-146 |
| Planar | Method of images | 161 |
| Point near sphere | Image charges | 166-170 |
| General | Green's function | 96-98 |
| Numerical | Finite element | - |

```python
# For sphere in uniform field: spherical harmonics
solution = problem.solve(
    method='spherical_harmonics',
    max_degree=10
)

# For point charge near plane: image method
solution = problem.solve(
    method='images',
    include_first_order_only=True
)
```

### Phase 3: Solution Computation

**Step 3.1: Compute Potential**
```python
V = solution.potential
V_numeric = V.evaluate(grid)
```

**Step 3.2: Compute Electric Field**
```python
E = solution.electric_field
E_numeric = E.evaluate(grid)
```

**Step 3.3: Compute Derived Quantities**
```python
# Surface charge density
sigma = solution.surface_charge_density

# Force on conductor
F = solution.compute_force()

# Capacitance (if applicable)
C = solution.compute_capacitance()

# Energy
W = solution.compute_energy()
```

### Phase 4: Validation

**Step 4.1: Verify Boundary Conditions**
```python
# Check V = 0 on grounded sphere
V_surface = V.evaluate(sphere_surface)
assert max(abs(V_surface)) < 1e-6

# Check E normal discontinuity = 4πσ
E_normal_jump = solution.verify_boundary_condition('surface_charge')
assert abs(E_normal_jump - 4*np.pi*sigma) < 1e-6
```

**Step 4.2: Verify Field Equations**
```python
# Check ∇ × E = 0 (electrostatics)
curl_E = E.curl()
assert max(abs(curl_E)) < 1e-6

# Check ∇ · E = 4πρ (Poisson)
div_E = E.divergence()
residual = div_E - 4*np.pi*rho
assert max(abs(residual)) < 1e-6
```

**Step 4.3: Verify Energy Relations**
```python
# Energy from field integral
W_field = solution.energy_field_integral()

# Energy from charge-potential integral
W_charge = solution.energy_charge_integral()

# Should match
assert abs(W_field - W_charge) / W_field < 1e-6
```

### Phase 5: Output and Visualization

**Step 5.1: Generate Reports**
```python
solution.generate_report(
    include=['potential', 'field', 'energy', 'forces'],
    format='pdf'
)
```

**Step 5.2: Create Visualizations**
```python
# Equipotential contours
solution.plot_equipotentials(
    plane='xz',
    levels=20,
    show_conductors=True
)

# Field lines
solution.plot_field_lines(
    seed_points=seed_points,
    max_length=10,
    color_by='magnitude'
)

# 3D field visualization
solution.plot_3D_field(
    show_vectors=True,
    vector_density='sparse',
    colormap='viridis'
)
```

## Example: Complete Solution

```python
from maxwell.tasks.electrostatics import complete_electrostatic_solution

# Define the classic problem: conducting sphere in uniform field
result = complete_electrostatic_solution(
    problem_type='conducting_sphere_uniform_field',
    parameters={
        'radius': 1.0,
        'E0': [0, 0, 1]
    },
    validation_level='full',
    output_format='complete'
)

# Access results
print(f"Maximum field enhancement: {result.field_enhancement}")
print(f"Induced dipole moment: {result.induced_dipole}")
print(f"Total energy: {result.energy}")

# Verify against analytical solution
analytical = ElectrostaticSolutions.conducting_sphere_in_field(
    radius=1.0,
    applied_field=[0, 0, 1]
)
error = result.compare_with(analytical)
print(f"Maximum relative error: {error.max_relative_error}")
```

## Deliverables

1. **Potential Solution** V(x,y,z)
2. **Electric Field** E(x,y,z)
3. **Surface Charge Distribution** σ (if conductors present)
4. **Force Calculations** on conductors/charges
5. **Energy Computation** total electrostatic energy
6. **Validation Report** with error analysis
7. **Visualization Package** with field plots

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 44-49 | Electric field definition |
| 69-73 | Electric potential |
| 77 | Poisson/Laplace equations |
| 78a-c | Boundary conditions |
| 96-98 | Green's theorem |
| 128-146 | Spherical harmonics |
| 155-175 | Method of images |

## Quality Gates

- [ ] Boundary conditions satisfied to tolerance
- [ ] Field equations verified (∇×E=0, ∇·E=4πρ)
- [ ] Energy consistency checked
- [ ] Maxwell article citations included
- [ ] Convergence demonstrated (for numerical methods)

## Related Tasks

- `magnetic-dipole-field` - Magnetostatic analog
- `em-wave-propagation` - Time-dependent extension
- `vector-potential-calculation` - Vector potential methods
- `energy-momentum-tensor` - Stress tensor computation
