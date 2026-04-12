# Task: Solid Angle Shell Potential

## Description

Complete workflow for computing magnetic shell potentials using solid angle methods from Maxwell's Part III. This is a powerful technique for computing magnetic fields from current loops and magnetized surfaces.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 409-411, 417-423 (Magnetic Shells, Solid Angles)
- **Standard Mathematical Implementation**: Solid angle calculations, surface integrals
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Magnetic Shell Definition

**Step 1.1: Define Shell Geometry**
```python
from maxwell.tasks.solid_angle import MagneticShellProblem
from maxwell.geometry.shell import MagneticShell

# Simple planar shell (current loop boundary)
shell = MagneticShell.planar(
    boundary=closed_curve,  # list of 3D points
    strength=Phi=1.0,  # unit pole strength
    orientation=[0, 0, 1]  # normal direction
)

# Spherical cap shell
shell = MagneticShell.spherical_cap(
    sphere_radius=R=1.0,
    cap_angle=theta_0,  # half-angle of cap
    strength=Phi=1.0
)

# Arbitrary surface shell
shell = MagneticShell.arbitrary(
    surface=parametric_surface,
    boundary=closed_curve,
    strength=Phi=1.0
)
```

**Step 1.2: Shell Strength from Current**
```python
# For a current loop, shell strength Φ = I/c (CGS)
shell = MagneticShell.from_current_loop(
    current=I=1.0,  # abampere
    loop_boundary=closed_curve
)
# Phi = I/c
```

### Phase 2: Solid Angle Computation

**Step 2.1: Solid Angle from Planar Loop**
```python
# Omega = solid angle subtended by loop at observation point
Omega = shell.solid_angle_at(
    observation_point=[x, y, z],
    method='gauss_integral'  # or 'monte_carlo', 'analytical'
)
```

**Step 2.2: Solid Angle via Line Integral**
```python
# Art. 419: Solid angle from double line integral
Omega_line = shell.solid_angle_line_integral(
    observation_point=r,
    integration_method='adaptive'
)
# Omega = ∮∮ (dl × dl')·(r - r')/|r - r'|³
```

**Step 2.3: Solid Angle via Determinant**
```python
# Art. 420: Determinant formulation
Omega_det = shell.solid_angle_determinant(
    observation_point=r,
    triangulate_surface=True
)
```

**Step 2.4: Solid Angle for Spherical Cap**
```python
# Analytical formula for spherical cap
Omega_cap = shell.solid_angle_spherical_cap(
    observation_point=r,
    cap_angle=theta_0
)
# Omega = 2π(1 - cos(alpha)) where alpha is half-angle from point
```

### Phase 3: Magnetic Scalar Potential

**Step 3.1: Potential from Shell**
```python
# Art. 409: Ω = Φ × ω (strength × solid angle)
Omega_magnetic = shell.magnetic_scalar_potential(
    observation_point=r
)
# Omega = Phi * solid_angle
```

**Step 3.2: Potential Discontinuity**
```python
# Art. 411: Potential jumps by 4πΦ across shell
Omega_plus = shell.potential_on_positive_side(r_near)
Omega_minus = shell.potential_on_negative_side(r_near)

discontinuity = Omega_plus - Omega_minus
assert abs(discontinuity - 4*np.pi*shell.strength) < 1e-6
```

**Step 3.3: Multiple Shells**
```python
# Superposition of multiple shells
total_Omega = sum(shell_i.magnetic_scalar_potential(r) 
                  for shell_i in shells)
```

### Phase 4: Magnetic Field from Potential

**Step 4.1: H = -∇Ω**
```python
H = -Omega_magnetic.gradient()
```

**Step 4.2: Numerical Gradient**
```python
H_numeric = -Omega_magnetic.numerical_gradient(
    grid=observation_grid,
    method='central_difference'
)
```

**Step 4.3: Verify Field Properties**
```python
# Check ∇ × H = 0 (outside shell)
curl_H = H.curl()
assert max(abs(curl_H)) < 1e-6

# Check ∇ · H = 0 (in vacuum)
div_H = H.divergence()
assert max(abs(div_H)) < 1e-6
```

### Phase 5: Specific Geometries

**Step 5.1: Circular Current Loop**
```python
loop = MagneticShell.circular_loop(
    current=I=1.0,
    radius=a=1.0,
    center=[0, 0, 0]
)

# On-axis potential
Omega_axis = loop.potential_on_axis(z_values=np.linspace(-5, 5, 100))
# Omega = 2πI/c * (1 - z/√(z² + a²))

# On-axis field
H_axis = loop.field_on_axis(z_values)
# H_z = (2πI/c) * a²/(z² + a²)^(3/2)
```

**Step 5.2: Magnetic Dipole Limit**
```python
# Small loop → dipole
dipole_limit = loop.dipole_approximation()
# m = (πa²I/c) n̂

# Verify far-field matches dipole
H_far = loop.field_at(r=100)
H_dipole = dipole_limit.field_at(r=100)
relative_error = abs(H_far - H_dipole) / abs(H_dipole)
assert relative_error < 0.01
```

**Step 5.3: Helmholtz Coils**
```python
helmholtz = MagneticShell.helmholtz_coils(
    current=I=1.0,
    radius=a=1.0,
    separation=a  # Equal to radius for uniform field
)

# Uniform field at center
H_center = helmholtz.field_at([0, 0, 0])
# H = (8/5^(3/2)) * (4πI/ca) ≈ 0.716 * (4πI/ca)
```

### Phase 6: Vector Potential from Shell

**Step 6.1: A from Shell Boundary**
```python
# Vector potential is along shell boundary
A = shell.vector_potential(
    observation_points=grid
)
# A = (Φ/c) ∮ dl'/|r - r'| (around boundary)
```

**Step 6.2: Verify B = ∇ × A**
```python
B_from_A = A.curl()
B_from_H = shell.magnetic_induction()  # B = H in vacuum

assert np.allclose(B_from_A, B_from_H)
```

### Phase 7: Energy and Force

**Step 7.1: Shell Energy in External Field**
```python
# Art. 423: Work to bring shell into field
U = shell.potential_energy_in_field(
    external_H=external_field
)
# U = -Φ × (flux through shell)
```

**Step 7.2: Force on Shell**
```python
F = shell.force_in_field(
    external_H=nonuniform_field
)
# F = -∇U
```

**Step 7.3: Torque on Shell**
```python
tau = shell.torque_in_field(
    external_H=uniform_field
)
# τ = m × H where m is equivalent dipole moment
```

### Phase 8: Applications

**Step 8.1: Current Loop Inductance**
```python
# Self-inductance from shell energy
L = shell.self_inductance()
# L = (1/c²) × (magnetic flux) / I
```

**Step 8.2: Mutual Inductance**
```python
# Between two loops
M = shell1.mutual_inductance_with(shell2)
# M = (1/c²) × (flux through 1 due to 2) / I_2
```

**Step 8.3: Magnetic Force Between Loops**
```python
F = shell1.force_on_shell(shell2)
# Can compute via energy gradient or direct integration
```

### Phase 9: Visualization

**Step 9.1: Solid Angle Visualization**
```python
shell.plot_solid_angle_contours(
    observation_plane='xz',
    levels=20,
    show_boundary=True
)
```

**Step 9.2: Potential Surfaces**
```python
shell.plot_equipotential_surfaces(
    levels=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    show_shell=True
)
```

**Step 9.3: Field Lines**
```python
shell.plot_magnetic_field_lines(
    seed_points='around_shell',
    max_length=20,
    show_shell_boundary=True
)
```

## Example: Complete Circular Loop Analysis

```python
from maxwell.tasks.solid_angle import circular_loop_analysis

result = circular_loop_analysis(
    current=I=1.0,  # abampere
    radius=a=1.0,  # cm
    observation_region={'r_max': 5, 'grid_resolution': 100}
)

# Get all results
Omega = result.magnetic_scalar_potential
H = result.magnetic_field
B = result.magnetic_induction
A = result.vector_potential

# Verify on-axis formula
H_axis_analytical = (2*np.pi*I/c) * a**2 / (result.z**2 + a**2)**(3/2)
H_axis_computed = result.H_on_axis

error = max(abs(H_axis_analytical - H_axis_computed))
print(f"Maximum on-axis error: {error}")

# Compute inductance
L = result.self_inductance()
print(f"Self-inductance: {L} cm")

# Visualize
result.plot_complete_field_distribution()
```

## Deliverables

1. **Solid Angle** ω(x,y,z)
2. **Magnetic Scalar Potential** Ω = Φω
3. **Magnetic Field** H = -∇Ω
4. **Vector Potential** A
5. **Energy and Force** calculations
6. **Inductance** values
7. **Validation Report**
8. **Visualization Package**

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 409-411 | Magnetic shell potential |
| 417-422 | Solid angle computations |
| 423 | Shell energy in field |
| 694-696 | Circular loop potential |
| 701-705 | Elliptic integrals for loops |

## Quality Gates

- [ ] Potential discontinuity = 4πΦ verified
- [ ] H = -∇Ω verified
- [ ] ∇ × H = 0 outside shell
- [ ] Far-field matches dipole
- [ ] Maxwell article citations included

## Related Tasks

- `vector-potential-calculation` - Vector potential approach
- `magnetic-dipole-field` - Dipole limit
- `electrostatic-field-solution` - Scalar potential analog
- `energy-momentum-tensor` - Force calculations
