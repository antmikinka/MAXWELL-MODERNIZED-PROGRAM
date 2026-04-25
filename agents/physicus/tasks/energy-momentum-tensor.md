# Task: Energy Momentum Tensor

## Description

Complete workflow for computing the Maxwell stress tensor and electromagnetic energy-momentum from Maxwell's Part I and Part IV theory. This task covers mechanical forces in electromagnetic systems and energy-momentum conservation.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 103-110 (Stress Tensor), 630-646 (Electromagnetic Energy)
- **Standard Mathematical Implementation**: Tensor calculus, conservation laws
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Stress Tensor Definition

**Step 1.1: Electrostatic Stress Tensor**
```python
from maxwell.tasks.stress_tensor import MaxwellStressTensor
from maxwell.physics.fields import ElectricField

# T_ij = (1/4π)[E_i E_j - (1/2)δ_ij E²]
T_electrostatic = MaxwellStressTensor.electrostatic(
    E_field=E,
    observation_points=grid
)
```

**Step 1.2: Magnetostatic Stress Tensor**
```python
from maxwell.physics.fields import MagneticField

# T_ij = (1/4π)[B_i B_j - (1/2)δ_ij B²]
T_magnetostatic = MaxwellStressTensor.magnetostatic(
    B_field=B,
    observation_points=grid
)
```

**Step 1.3: Full Electromagnetic Stress Tensor**
```python
# Combined E and B fields
T_EM = MaxwellStressTensor.full(
    E_field=E,
    B_field=B,
    observation_points=grid
)

# T_ij = (1/4π)[E_i E_j + B_i B_j - (1/2)δ_ij(E² + B²)]
```

**Step 1.4: Stress Tensor in Matter**
```python
# With dielectric and magnetic materials
T_matter = MaxwellStressTensor.in_matter(
    E_field=E,
    D_field=D,
    H_field=H,
    B_field=B,
    material_properties=material
)
```

### Phase 2: Force from Stress Tensor

**Step 2.1: Force on Charged Body**
```python
# F_i = ∮ T_ij n_j dS
F = T_electrostatic.force_on_body(
    body_surface=conducting_body,
    method='surface_integral'
)
```

**Step 2.2: Force on Magnetic Body**
```python
F_mag = T_magnetostatic.force_on_body(
    body_surface=magnetic_body,
    include_magnetization=True
)
```

**Step 2.3: Force Between Conductors**
```python
# Force on conductor 1 due to conductor 2
F_12 = T_electrostatic.force_between(
    body1=conductor1,
    body2=conductor2
)
```

**Step 2.4: Force via Volume Integral**
```python
# Alternative: F = ∫ (ρE + J×B/c) dV
F_volume = MaxwellStressTensor.force_volume_integral(
    charge_density=rho,
    current_density=J,
    E_field=E,
    B_field=B
)

# Should match surface integral
assert np.allclose(F_surface, F_volume)
```

### Phase 3: Energy Density

**Step 3.1: Electrostatic Energy Density**
```python
# u_e = E²/8π (vacuum)
u_electric = MaxwellStressTensor.electric_energy_density(
    E_field=E
)

# u_e = E·D/8π (matter)
u_electric_matter = MaxwellStressTensor.electric_energy_density_matter(
    E_field=E,
    D_field=D
)
```

**Step 3.2: Magnetic Energy Density**
```python
# u_m = B²/8π (vacuum)
u_magnetic = MaxwellStressTensor.magnetic_energy_density(
    B_field=B
)

# u_m = B·H/8π (matter)
u_magnetic_matter = MaxwellStressTensor.magnetic_energy_density_matter(
    B_field=B,
    H_field=H
)
```

**Step 3.3: Total Field Energy**
```python
# U = ∫ u dV
U_total = MaxwellStressTensor.total_field_energy(
    E_field=E,
    B_field=B,
    integration_volume=all_space
)
```

### Phase 4: Energy Flux (Poynting Vector)

**Step 4.1: Poynting Vector**
```python
# S = (c/4π) E × H
S = MaxwellStressTensor.poynting_vector(
    E_field=E,
    H_field=H
)
```

**Step 4.2: Time-Averaged Flux**
```python
# For harmonic fields: <S> = (c/8π) Re(E × H*)
S_avg = MaxwellStressTensor.time_averaged_poynting(
    E_field=E_complex,
    H_field=H_complex,
    frequency=omega
)
```

**Step 4.3: Power Through Surface**
```python
# P = ∫ S · dA
P = S.flux_through_surface(surface)
```

### Phase 5: Momentum Density

**Step 5.1: Field Momentum**
```python
# g = S/c² = (1/4πc) E × B
g = MaxwellStressTensor.field_momentum_density(
    E_field=E,
    B_field=B
)
```

**Step 5.2: Total Field Momentum**
```python
# P_field = ∫ g dV
P_total = MaxwellStressTensor.total_field_momentum(
    E_field=E,
    B_field=B
)
```

**Step 5.3: Radiation Pressure**
```python
# p = S/c (absorbing) or p = 2S/c (reflecting)
pressure = MaxwellStress_tensor.radiation_pressure(
    S_field=S,
    surface_type='absorbing'  # or 'reflecting'
)
```

### Phase 6: Conservation Laws

**Step 6.1: Energy Conservation (Poynting Theorem)**
```python
# ∂u/∂t + ∇·S = -J·E (energy balance)
residual = MaxwellStressTensor.verify_poynting_theorem(
    E_field=E,
    B_field=B,
    current_density=J,
    time_derivative_E=dE_dt,
    time_derivative_B=dB_dt
)
assert max(abs(residual)) < 1e-6
```

**Step 6.2: Momentum Conservation**
```python
# ∂g/∂t + ∇·T = -f (force density)
momentum_balance = MaxwellStressTensor.verify_momentum_conservation(
    E_field=E,
    B_field=B,
    stress_tensor=T,
    force_density=f,
    time_derivative_g=dg_dt
)
assert max(abs(momentum_balance)) < 1e-6
```

**Step 6.3: Angular Momentum**
```python
# L_field = r × g
L = MaxwellStressTensor.field_angular_momentum(
    E_field=E,
    B_field=B,
    origin=[0, 0, 0]
)

# Torque from stress tensor
tau = MaxwellStressTensor.torque_on_body(
    stress_tensor=T,
    body_surface=body,
    origin=[0, 0, 0]
)
```

### Phase 7: Specific Applications

**Step 7.1: Capacitor Force**
```python
# Force between parallel plate capacitor plates
F_capacitor = MaxwellStressTensor.force_parallel_plates(
    voltage=V,
    plate_area=A,
    separation=d,
    dielectric_constant=K
)
# F = (1/8π) E² A = (1/2) CV²/d
```

**Step 7.2: Solenoid Force**
```python
# Force trying to expand solenoid radius
F_solenoid = MaxwellStressTensor.solenoid_radial_force(
    current=I,
    turns_per_length=n,
    radius=a
)
# F per unit area = B²/8π
```

**Step 7.3: Radiation Pressure on Surface**
```python
# Pressure from EM wave
pressure_wave = MaxwellStressTensor.wave_radiation_pressure(
    intensity=I,
    surface_type='perfect_reflector'
)
# p = 2I/c
```

**Step 7.4: Maxwell's Stress Objections** (Art. 110)
```python
# Discuss conceptual issues with stress interpretation
stress_analysis = MaxwellStressTensor.analyze_stress_interpretation(
    field_configuration=E_and_B,
    include_historical_notes=True
)
```

### Phase 8: Covariant Formulation

**Step 8.1: Stress-Energy Tensor**
```python
# T^μν in covariant form
T_covariant = MaxwellStressTensor.stress_energy_tensor_covariant(
    E_field=E,
    B_field=B
)

# T^00 = (E² + B²)/8π (energy density)
# T^0i = (c/4π)(E × B)^i (momentum density)
# T^ij = stress tensor
```

**Step 8.2: Lorentz Invariants**
```python
# Invariants of EM field
invariant1 = E**2 - B**2
invariant2 = E · B

print(f"E² - B² = {invariant1}")
print(f"E·B = {invariant2}")
```

### Phase 9: Visualization

**Step 9.1: Stress Tensor Ellipsoids**
```python
T.plot_stress_ellipsoids(
    grid=observation_grid,
    scale='auto',
    show_principal_axes=True
)
```

**Step 9.2: Energy Density Contours**
```python
T.plot_energy_density_contours(
    plane='xz',
    levels=20,
    show_field_vectors=True
)
```

**Step 9.3: Poynting Vector Flow**
```python
S.plot_energy_flow_lines(
    seed_points=source_region,
    color_by='magnitude',
    show_boundaries=True
)
```

## Example: Force on Charged Sphere

```python
from maxwell.tasks.stress_tensor import sphere_force_analysis

# Conducting sphere with charge Q
result = sphere_force_analysis(
    charge=Q=1.0,
    radius=R=1.0,
    external_field=E0=[0, 0, 1]
)

# Force from stress tensor
F_stress = result.force_from_stress_tensor()

# Force from direct calculation
F_direct = result.force_direct_calculation()  # F = QE_extern

print(f"Force from stress: {F_stress}")
print(f"Force direct: {F_direct}")
print(f"Relative error: {abs(F_stress - F_direct)/F_direct}")

# Surface stress distribution
stress_on_surface = result.surface_stress_distribution()
result.plot_surface_stress()
```

## Deliverables

1. **Maxwell Stress Tensor** T_ij
2. **Force Calculations** on bodies
3. **Energy Density** distributions
4. **Poynting Vector** (energy flux)
5. **Momentum Density** 
6. **Conservation Law Verification**
7. **Validation Report**
8. **Visualization Package**

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 103-109 | Stress tensor derivation |
| 110 | Stress interpretation discussion |
| 112-116 | Equilibrium and stability |
| 630-638 | Electrokinetic energy |
| 639-640 | Force from energy |
| 641-646 | Stress tensor properties |

## Quality Gates

- [ ] Stress tensor symmetry verified
- [ ] Force from surface integral matches volume integral
- [ ] Energy conservation (Poynting theorem) verified
- [ ] Momentum conservation verified
- [ ] Maxwell article citations included

## Related Tasks

- `electrostatic-field-solution` - Field for stress calculation
- `em-wave-propagation` - Wave energy and momentum
- `magnetic-dipole-field` - Magnetic force
- `implement-dynamics` - Energy formulation
