# Task: Vector Potential Calculation

## Description

Complete workflow for computing the magnetic vector potential A from current distributions using Maxwell's Part III and IV theory. The vector potential is fundamental for computing magnetic fields and understanding electromagnetic induction.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 405-406, 540-541 (Vector Potential, Electrotonic State)
- **Standard Mathematical Implementation**: Vector calculus, integral transforms
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Current Distribution Definition

**Step 1.1: Define Current Source**
```python
from maxwell.tasks.vector_potential import VectorPotentialProblem
from maxwell.kinematics.current import CurrentDistribution

# Line current (wire)
wire = CurrentDistribution.line_current(
    current=I=1.0,  # abampere
    path=parametric_curve,  # r(t) for t in [0, 1]
    filament_type='infinitesimal'
)

# Surface current
sheet = CurrentDistribution.surface_current(
    surface_current_density=K,  # abampere/cm
    surface=plane,
    direction=[1, 0, 0]
)

# Volume current
volume = CurrentDistribution.volume_current(
    current_density=J,  # abampere/cm²
    support=bounded_region,
    divergence_free=True  # ∇·J = 0 for steady currents
)
```

**Step 1.2: Current Loop (Important Case)**
```python
# Circular loop
loop = CurrentDistribution.circular_loop(
    current=I=1.0,
    radius=a=1.0,
    center=[0, 0, 0],
    normal=[0, 0, 1]
)

# Arbitrary planar loop
arbitrary_loop = CurrentDistribution.planar_loop(
    current=I,
    vertices=[...],  # list of (x, y, z) points
    plane_normal=[0, 0, 1]
)
```

### Phase 2: Vector Potential Computation

**Step 2.1: Direct Integration Formula**
```python
# A(r) = (1/c) ∫ J(r')/|r - r'| d³r'
A = VectorPotentialProblem.compute_direct(
    current_distribution=volume,
    observation_points=grid,
    integration_method='adaptive_quadrature'
)
```

**Step 2.2: Line Current Formula**
```python
# A(r) = (I/c) ∮ dl'/|r - r'|
A_wire = VectorPotentialProblem.compute_line(
    line_current=wire,
    observation_points=grid
)
```

**Step 2.3: Multipole Expansion (Far Field)**
```python
# For distant observation points
A_multipole = VectorPotentialProblem.compute_multipole(
    current_distribution=volume,
    observation_points=far_grid,
    max_order='dipole'  # or 'quadrupole', etc.
)

# Magnetic dipole term dominates:
# A_dipole = (m × r)/r³
```

**Step 2.4: Vector Potential from Magnetic Shell**
```python
# Equivalent magnetic shell
shell_potential = VectorPotentialProblem.from_magnetic_shell(
    shell_strength=Phi,
    shell_boundary=closed_curve,
    observation_points=grid
)
# A is discontinuous across the shell
```

### Phase 3: Gauge Considerations

**Step 3.1: Verify Coulomb Gauge**
```python
# For steady currents: ∇·A = 0 (Coulomb gauge)
div_A = A.divergence()
assert max(abs(div_A)) < 1e-6
```

**Step 3.2: Gauge Transformation**
```python
# A' = A + ∇χ (gauge transformation)
chi = ScalarField(lambda x, y, z: x*y*z)  # arbitrary scalar
A_prime = A + chi.gradient()

# B is unchanged
B_from_A = A.curl()
B_from_A_prime = A_prime.curl()
assert np.allclose(B_from_A, B_from_A_prime)
```

**Step 3.3: Lorenz Gauge (Time-Dependent)**
```python
# For time-dependent fields: ∇·A + (1/c)∂V/∂t = 0
A_lorenz = VectorPotentialProblem.impose_lorenz_gauge(
    A=A,
    V=V,
    time_derivative=V_time_derivative
)
```

### Phase 4: Magnetic Field from A

**Step 4.1: Compute B = ∇ × A**
```python
B = A.curl()
```

**Step 4.2: Verify Solenoidal Condition**
```python
# ∇·B = 0 (always satisfied since B = curl A)
div_B = B.divergence()
assert max(abs(div_B)) < 1e-12  # Should be machine precision
```

**Step 4.3: Compare with Direct B Calculation**
```python
# Compute B directly from Biot-Savart
B_direct = BiotSavart.compute(
    current_distribution=volume,
    observation_points=grid
)

# Should match
error = max(abs(B - B_direct)) / max(abs(B_direct))
assert error < 1e-6
```

### Phase 5: Specific Geometries

**Step 5.1: Infinite Straight Wire**
```python
A_wire = VectorPotentialProblem.infinite_straight_wire(
    current=I,
    wire_position=[0, 0],  # (x, y) in plane
    gauge_choice='cylindrical'
)
# A = (2I/c) ln(r) φ̂ (in Coulomb gauge)
```

**Step 5.2: Circular Loop - On Axis**
```python
A_on_axis = VectorPotentialProblem.circular_loop_on_axis(
    current=I,
    radius=a,
    z_values=np.linspace(-5, 5, 100)
)
# On axis, A_φ = 0 by symmetry, but off-axis requires elliptic integrals
```

**Step 5.3: Circular Loop - Full Solution**
```python
A_full = VectorPotentialProblem.circular_loop_complete(
    current=I,
    radius=a,
    observation_points=cylindrical_grid
)
# Uses complete elliptic integrals K(k), E(k)
```

**Step 5.4: Solenoid**
```python
A_solenoid = VectorPotentialProblem.solenoid(
    current=I,
    turns_per_length=n,
    radius=a,
    length=L,
    observation_points=grid
)
# Inside: A_φ = (1/2)B r (for infinite solenoid)
```

### Phase 6: Stokes' Theorem Verification

**Step 6.1: Magnetic Flux from A**
```python
# Φ = ∫ B·dA = ∮ A·dl (Stokes' theorem)
flux_surface = B.flux_through_surface(surface)
flux_loop = A.line_integral_around_contour(boundary)

assert abs(flux_surface - flux_loop) < 1e-6
```

**Step 6.2: Flux Through Loop**
```python
# Flux through current loop itself (self-flux)
self_flux = A.line_integral_around_contour(loop_boundary)

# Related to self-inductance: Φ = L I
L_self = self_flux / I
```

### Phase 7: Electrokinetic Momentum

**Step 7.1: Momentum from A**
```python
# Electrokinetic momentum (Arts. 585-592)
# p = (1/c) A (for unit charge)
p = A / c
```

**Step 7.2: Mutual Inductance from A**
```python
# Mutual inductance between circuits
M = VectorPotentialProblem.mutual_inductance(
    circuit1=current1,
    circuit2=current2
)
# M = (1/c²) ∮∮ (dl₁·dl₂)/|r₁-r₂| (Neumann formula)
```

### Phase 8: Visualization

**Step 8.1: Vector Potential Field Lines**
```python
A.plot_field_lines(
    seed_points=seed_points,
    color_by='magnitude',
    show_gauge_dependence=True
)
```

**Step 8.2: Magnitude Contours**
```python
A.plot_magnitude_contours(
    plane='xz',
    levels=20,
    show_current=True
)
```

**Step 8.3: Comparison with B**
```python
A.plot_comparison_with_B(
    plane='xz',
    show_both_fields=True,
    verify_curl_relation=True
)
```

## Example: Aharonov-Bohm Configuration

```python
from maxwell.tasks.vector_potential import aharonov_bohm_setup

# Solenoid with confined B field
result = aharonov_bohm_setup(
    solenoid_radius=R=0.1,
    magnetic_field=B0=1000,  # inside solenoid
    observation_region='outside'
)

# A is non-zero outside even though B=0
A_outside = result.A_field
B_outside = result.B_field  # Should be zero

print(f"A outside solenoid: {max(abs(A_outside))}")
print(f"B outside solenoid: {max(abs(B_outside))}")  # ~0

# But line integral of A gives flux
flux_through_loop = A_outside.line_integral_around_circle(r=1.0)
expected_flux = B0 * np.pi * R**2
print(f"Flux: {flux_through_loop} vs expected {expected_flux}")
```

## Deliverables

1. **Vector Potential** A(x,y,z)
2. **Magnetic Field** B = ∇×A
3. **Gauge Verification** (∇·A = 0 for Coulomb)
4. **Stokes' Theorem Verification**
5. **Mutual Inductance** calculations
6. **Validation Report**
7. **Visualization Package**

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 405-406 | Vector potential definition |
| 409-411 | Magnetic shell potential |
| 540-541 | Electrotonic state |
| 585-592 | Electrokinetic momentum |
| 616-617 | Vector potential equations |
| 694-696 | Circular loop potential |

## Quality Gates

- [ ] B = ∇×A verified
- [ ] ∇·B = 0 confirmed (automatic from curl)
- [ ] Gauge condition satisfied
- [ ] Stokes' theorem verified
- [ ] Maxwell article citations included

## Related Tasks

- `magnetic-dipole-field` - Dipole vector potential
- `electrostatic-field-solution` - Scalar potential analog
- `em-wave-propagation` - Time-dependent A
- `solid-angle-shell-potential` - Magnetic shell theory
