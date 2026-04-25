# Command: magnetization-model

## Description

Models magnetic material response including induced magnetization, hysteresis, and saturation from Maxwell's Part III (Arts. 424-448). Implements susceptibility, permeability, and Weber's molecular theory.

## Functionality

### Constitutive Relations (Layer 37)

1. **Linear Response** (Arts. 424-426)
   - I = κH (magnetization intensity)
   - B = H + 4πI = μH (CGS)
   - μ = 1 + 4πκ (permeability-susceptibility relation)

2. **Induced Magnetization** (Arts. 427-428)
   - Soft iron: high κ, no remanence
   - Diamagnetic: κ < 0 (copper, bismuth)
   - Paramagnetic: κ > 0 (aluminum, platinum)

3. **Shape Effects** (Arts. 431-440)
   - Demagnetizing field: H_demag = -N·M
   - Demagnetizing factors for ellipsoids
   - Hollow spheres and cylindrical shells

### Nonlinear Phenomena (Layer 38)

4. **Weber's Molecular Theory** (Art. 430, 442-443)
   - Elementary molecular dipoles
   - Saturation at high fields
   - Langevin function: M/M_s = L(μH/kT)

5. **Hysteresis** (Arts. 444-446)
   - Remanence: M at H = 0
   - Coercivity: H needed to demagnetize
   - Hysteresis loss per cycle

6. **Magnetostriction** (Arts. 447-448)
   - Dimensional changes with magnetization
   - Villari effect (inverse magnetostriction)

### Material Classes

- **Soft magnetic**: Iron, permalloy (low coercivity)
- **Hard magnetic**: Alnico, rare-earth (high coercivity)
- **Ferrimagnetic**: Ferrites (mixed sublattices)

## Usage

```python
from maxwell.physics.magnetic_materials import MagnetizationModel
from maxwell.materials import MagneticMaterial

# Linear soft iron
soft_iron = MagneticMaterial(
    name='soft_iron',
    susceptibility=200,  # dimensionless (CGS)
    saturation=21800,  # gauss
    hysteresis=False
)

H_applied = VectorField([100, 0, 0])  # oersted

M = MagnetizationModel.compute_magnetization(
    material=soft_iron,
    H_field=H_applied,
    model='linear'
)

B = MagnetizationModel.compute_induction(
    H_field=H_applied,
    magnetization=M
)

# Nonlinear with saturation
steel = MagneticMaterial(
    name='silicon_steel',
    saturation=20000,  # gauss
    initial_permeability=1500,
    hysteresis=True,
    coercivity=0.5,  # oersted
    remanence=12000  # gauss
)

M_nonlinear = MagnetizationModel.nonlinear_response(
    material=steel,
    H_field=H_applied,
    model='langevin'  # or 'stoerzels', 'jiles_atherton'
)

# Hysteresis loop
hysteresis_loop = MagnetizationModel.compute_hysteresis_loop(
    material=steel,
    H_range=[-100, 100],
    num_points=100,
    model='preisach'
)

# Demagnetizing effects (ellipsoid)
ellipsoid_M = MagnetizationModel.ellipsoid_response(
    material=soft_iron,
    H_applied=H_applied,
    semi_axes=[10, 5, 2],  # cm
    orientation=[0, 0, 1]
)
# Returns demagnetizing factors N_x, N_y, N_z
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `material` | MagneticMaterial | Magnetic properties |
| `H_field` | VectorField | Applied field (oersted) |
| `temperature` | float | Temperature (Kelvin) |
| `stress` | float | Applied mechanical stress (dynes/cm²) |
| `model` | str | 'linear', 'langevin', 'jiles_atherton', 'preisach' |
| `geometry` | dict | Shape for demagnetizing calculations |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `M` | VectorField | Magnetization intensity (erg/gauss·cm³) |
| `B` | VectorField | Magnetic induction (gauss) |
| `susceptibility` | float or tensor | Effective κ |
| `hysteresis_loss` | float | Energy loss per cycle (erg/cm³) |
| `metadata` | dict | Citations, validation, material data |

## Implementation Notes

- CGS: B, H, M all have same dimensions
- Demagnetizing factors satisfy N_x + N_y + N_z = 4π (CGS)
- Langevin function: L(x) = coth(x) - 1/x
- Jiles-Atherton model: modern extension (clearly marked)
- Temperature dependence via Curie-Weiss law

## Validation

- Low-field limit matches handbook susceptibility
- Saturation matches material specifications
- Demagnetizing factors for sphere: N = 4π/3
- Hysteresis area matches loss measurements

## Maxwell Article References

| Article | Content |
|---------|---------|
| 424-426 | Induced magnetization |
| 427-428 | Poisson's and Faraday's theories |
| 430 | Poisson's molecular theory |
| 431-440 | Shape-dependent magnetization |
| 442-443 | Weber's saturation theory |
| 444-446 | Hysteresis phenomena |
| 447-448 | Magnetostriction |

## Related Commands

- `magnetic-field` - For field computation
- `dielectric-response` - Analogous electric response
- `material-properties` - For material database

## Error Handling

- Warns if approaching saturation
- Raises `MagneticError` for negative permeability
- Validates thermodynamic stability

## Modern Extensions (Clearly Marked)

- Jiles-Atherton hysteresis model
- Landau-Lifshitz-Gilbert dynamics
- Micromagnetic simulations
