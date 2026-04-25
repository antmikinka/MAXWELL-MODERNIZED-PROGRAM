# Command: dielectric-response

## Description

Models dielectric materials and polarization effects from Maxwell's Part I (Arts. 50-58, 103-110). Implements electric displacement D, polarization P, and the constitutive relation D = εE = E + 4πP (CGS).

## Functionality

### Constitutive Relations
1. **Electric Displacement** (Arts. 60-62)
   - D = εE (linear isotropic)
   - D = ε̿ · E (anisotropic, tensor permittivity)
   - CGS: D = E + 4πP

2. **Polarization** (Art. 111)
   - P = χ_e E (linear response)
   - ε = 1 + 4πχ_e (CGS relation)
   - Bound charge: ρ_b = -∇ · P, σ_b = P · n̂

3. **Specific Inductive Capacity** (Arts. 79-83)
   - K = ε/ε_0 (dielectric constant)
   - Measurement via capacitor comparison

### Dielectric Phenomena
- **Electrical Absorption** ("soakage"): Time-dependent polarization
- **Residual Charge**: Memory effects in dielectrics
- **Dielectric Loss**: Energy dissipation in AC fields
- **Breakdown**: Field ionization at high fields

### Anisotropic Media
- Crystal permittivity tensors
- Stratified materials (Layer 25)
- Effective medium approximations

## Usage

```python
from maxwell.physics.dielectrics import DielectricResponse
from maxwell.materials import DielectricMaterial

# Define linear isotropic dielectric
glass = DielectricMaterial(
    name='flint_glass',
    permittivity=10.0,  # relative to vacuum
    loss_tangent=0.01,
    breakdown_field=1e6  # statvolt/cm
)

# Compute polarization in applied field
E_applied = VectorField([100, 0, 0])  # statvolt/cm
P = DielectricResponse.compute_polarization(
    material=glass,
    E_field=E_applied,
    model='linear'  # or 'nonlinear', 'frequency_dependent'
)

# Get displacement field
D = DielectricResponse.compute_displacement(
    E_field=E_applied,
    polarization=P
)

# Anisotropic crystal
quartz = DielectricMaterial(
    name='quartz',
    permittivity_tensor=[
        [4.3, 0, 0],
        [0, 4.3, 0],
        [0, 0, 4.6]
    ]
)

D_aniso = DielectricResponse.anisotropic_response(
    material=quartz,
    E_field=E_applied
)

# Time-dependent absorption (soakage)
P_time = DielectricResponse.time_dependent_polarization(
    material=glass,
    E_field=E_applied,
    time_array=[0, 1, 10, 100, 1000],  # seconds
    model='dielectric_relaxation'
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `material` | DielectricMaterial | Material properties and constants |
| `E_field` | VectorField | Applied electric field (statvolt/cm) |
| `frequency` | float | AC field frequency (Hz, optional) |
| `time_array` | ndarray | Time points for transient response |
| `model` | str | 'linear', 'nonlinear', 'frequency_dependent', 'relaxation' |
| `temperature` | float | Temperature in Kelvin (optional) |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `P` | VectorField | Polarization (dipole moment per volume) |
| `D` | VectorField | Electric displacement |
| `bound_charge` | dict | Volume (ρ_b) and surface (σ_b) bound charges |
| `energy_density` | float | Energy stored per unit volume (erg/cm³) |
| `metadata` | dict | Material properties, citations, validation |

## Implementation Notes

- CGS units: D and E have same dimensions (unlike SI)
- Factor of 4π appears in D = E + 4πP
- Nonlinear models include Kerr effect, ferroelectric hysteresis
- Frequency dependence via complex permittivity ε(ω) = ε' + iε''
- Relaxation models: Debye, Cole-Cole, Havriliak-Negami

## Validation

- Static limit matches handbook permittivity values
- Energy density: U = (1/8π) E · D
- Boundary conditions: D_n continuous, E_t continuous
- Clausius-Mossotti relation for dilute media

## Maxwell Article References

| Article | Content |
|---------|---------|
| 50-58 | Dielectric properties and induction |
| 60-62 | Electric displacement |
| 79-83 | Specific inductive capacity |
| 103-110 | Maxwell stress in dielectrics |
| 111 | Polarization theory |

## Related Commands

- `electrostatic-field` - For field computation
- `magnetization-model` - Analogous magnetic response
- `material-properties` - For material database access

## Error Handling

- Warns if field exceeds breakdown threshold
- Raises `AnisotropyError` if tensor not positive definite
- Validates causality for frequency-dependent models (Kramers-Kronig)
