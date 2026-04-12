# Task: Magnetic Dipole Field

## Description

Complete workflow for computing magnetic dipole fields using Maxwell's Part III theory. This task covers both permanent magnets and current-loop dipoles.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 371-474 (Part III: Magnetism)
- **Standard Mathematical Implementation**: Dipole field calculations, spherical harmonics
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Dipole Definition

**Step 1.1: Define Magnetic Moment**
```python
from maxwell.tasks.magnetostatics import MagneticDipoleProblem
from maxwell.core.magnet import MagneticMoment

# Magnetic moment vector (CGS: emu = erg/Gauss)
m = MagneticMoment(
    magnitude=1.0,  # emu
    direction=[0, 0, 1]  # pointing in +z
)

# Create dipole problem
problem = MagneticDipoleProblem(
    moment=m,
    position=[0, 0, 0],
    dipole_type='point_dipole'  # or 'current_loop', 'magnetized_sphere'
)
```

**Step 1.2: Alternative Dipole Sources**
```python
# Current loop dipole
loop = MagneticDipoleProblem.current_loop(
    current=I=1.0,  # abampere
    radius=a=0.1,  # cm
    center=[0, 0, 0],
    normal=[0, 0, 1]
)
# Magnetic moment: m = (πa²I/c) n̂

# Uniformly magnetized sphere
sphere = MagneticDipoleProblem.magnetized_sphere(
    magnetization=M=[0, 0, 100],  # emu/cm³
    radius=R=1.0  # cm
)
# Total moment: m = (4π/3)R³M

# Magnetic shell
shell = MagneticDipoleProblem.magnetic_shell(
    strength=Phi=1.0,  # unit pole
    boundary=closed_curve,
    orientation=[0, 0, 1]
)
```

### Phase 2: Field Computation

**Step 2.1: Scalar Potential (for point dipole)**
```python
# Magnetic scalar potential Ω
Omega = problem.scalar_potential()
# Ω = (m·r̂)/r² = (m·r)/r³

Omega_numeric = Omega.evaluate(observation_points)
```

**Step 2.2: Magnetic Field H**
```python
H = problem.magnetic_field_H()
# H = -∇Ω = [3(m·r̂)r̂ - m]/r³

H_numeric = H.evaluate(observation_points)
```

**Step 2.3: Magnetic Induction B**
```python
# In vacuum: B = H (CGS, with 4π factors handled)
B = problem.magnetic_induction()
# B = H + 4πI, but I=0 outside dipole

# For current loop, use vector potential
A = problem.vector_potential()
# A = (m × r)/r³

B_from_A = A.curl()
```

**Step 2.4: On-Axis and Off-Axis Fields**
```python
# On axis (z-axis for dipole along z)
H_z_axis = problem.field_on_axis(z_values=np.linspace(-5, 5, 100))
# H_z = 2m/z³ (far field)

# Equatorial plane
H_equatorial = problem.field_in_equatorial_plane(
    rho_values=np.linspace(0.1, 5, 100)
)
# H_rho = -m/ρ³ (far field)
```

### Phase 3: Interaction Calculations

**Step 3.1: Force on Another Dipole**
```python
dipole2 = MagneticDipoleProblem(
    moment=MagneticMoment(magnitude=0.5, direction=[1, 0, 0]),
    position=[3, 0, 0]
)

force = problem.force_on_dipole(dipole2)
# F = ∇(m₂·B₁)
```

**Step 3.2: Torque on Dipole**
```python
# Torque in external field
external_H = MagneticField(uniform=[1, 0, 0])
torque = problem.torque_in_field(external_H)
# τ = m × H
```

**Step 3.3: Potential Energy**
```python
# Energy of dipole in external field
U = problem.potential_energy_in_field(external_H)
# U = -m·H

# Interaction energy between two dipoles
U_interaction = problem.interaction_energy(dipole2)
# U = (m₁·m₂ - 3(m₁·r̂)(m₂·r̂))/r³
```

### Phase 4: Special Geometries

**Step 4.1: Dipole Near Conducting Plane**
```python
# Method of images for magnetic dipole
image_problem = problem.with_image_plane(
    plane_position=0,
    plane_type='permeable_boundary',
    mu_ratio=mu2/mu1
)
```

**Step 4.2: Dipole in Spherical Cavity**
```python
# Dipole at center of spherical shell
cavity_problem = problem.in_spherical_shell(
    inner_radius=a,
    outer_radius=b,
    shell_permeability=mu
)
```

**Step 4.3: Dipole in Uniform Field**
```python
# Dipole in external uniform field
combined = problem.plus_uniform_field(H0=[0, 0, 1])
# Total field = dipole field + uniform field
```

### Phase 5: Validation

**Step 5.1: Verify Dipole Field Properties**
```python
# Check ∇ · B = 0
div_B = B.divergence()
assert max(abs(div_B)) < 1e-6

# Check ∇ × H = 0 (outside sources)
curl_H = H.curl()
assert max(abs(curl_H)) < 1e-6
```

**Step 5.2: Verify Far-Field Behavior**
```python
# At large r, should approach pure dipole
far_field = H.evaluate(r=100, theta=0)
dipole_prediction = 2*m/r**3
relative_error = abs(far_field - dipole_prediction) / dipole_prediction
assert relative_error < 0.01
```

**Step 5.3: Verify Energy Relations**
```python
# Energy from field integral
W_field = problem.compute_field_energy(integration_radius=10)

# Energy from dipole formula
W_dipole = m.magnitude**2 / (2 * R**3)  # for sphere of radius R

assert abs(W_field - W_dipole) / W_dipole < 0.01
```

### Phase 6: Visualization

**Step 6.1: Field Line Plotting**
```python
problem.plot_field_lines(
    seed_points='sphere',  # distributed on sphere
    max_length=20,
    color_by='magnitude',
    show_dipole=True
)
```

**Step 6.2: Equipotential Surfaces**
```python
problem.plot_equipotential_surfaces(
    levels=[-0.5, -0.25, 0, 0.25, 0.5],
    show_axes=True
)
```

**Step 6.3: Field Magnitude Slices**
```python
problem.plot_field_magnitude_slice(
    plane='xz',
    bounds=[-5, 5],
    colormap='log',  # logarithmic scale
    show_field_vectors=True
)
```

## Example: Earth's Magnetic Field

```python
from maxwell.tasks.magnetostatics import terrestrial_magnetic_field

# Approximate Earth as centered dipole
earth = terrestrial_magnetic_field(
    dipole_moment=7.94e25,  # emu (CGS)
    dipole_tilt=11.5,  # degrees from rotation axis
    rotation_axis=[0, 0, 1]
)

# Compute field at surface
surface_field = earth.field_at_surface(
    latitude=45,  # degrees
    longitude=-75  # degrees
)

# Get magnetic elements
H = surface_field.horizontal_intensity()
Z = surface_field.vertical_intensity()
F = surface_field.total_intensity()
declination = surface_field.declination()
inclination = surface_field.inclination()

print(f"Total field: {F:.2f} Gauss")
print(f"Inclination: {inclination:.1f} degrees")
```

## Deliverables

1. **Scalar Potential** Ω(x,y,z) or **Vector Potential** A(x,y,z)
2. **Magnetic Field H** (Oersted)
3. **Magnetic Induction B** (Gauss)
4. **Force and Torque** calculations
5. **Interaction Energies**
6. **Validation Report**
7. **Field Visualization Package**

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 371-376 | Magnet properties, magnetic moment |
| 381-384 | Magnetization vector |
| 385-386 | Magnetic potential |
| 387-388 | Dipole-dipole interaction |
| 389 | Potential energy |
| 395-398 | Magnetic field H |
| 399 | Magnetic induction B |
| 405-406 | Vector potential |
| 409-411 | Magnetic shells |

## Quality Gates

- [ ] ∇ · B = 0 verified
- [ ] ∇ × H = 0 outside sources
- [ ] Far-field dipole behavior confirmed
- [ ] Energy relations satisfied
- [ ] Maxwell article citations included

## Related Tasks

- `electrostatic-field-solution` - Electrostatic analog
- `em-wave-propagation` - Time-dependent fields
- `vector-potential-calculation` - Vector potential methods
- `solid-angle-shell-potential` - Magnetic shell theory
