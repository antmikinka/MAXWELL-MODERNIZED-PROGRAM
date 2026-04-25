# Command: electrolysis-model

## Description

Simulates electrolytic processes and ionic conduction from Maxwell's Part II (Arts. 236-238, 269-286). Implements Faraday's laws of electrolysis, ion transport modeling, and electrochemical cell dynamics.

## Functionality

### Electrolysis Fundamentals (Layer 14, 18-19)
1. **Faraday's Laws** (Arts. 236-237)
   - First law: m = ZQ (mass deposited proportional to charge)
   - Second law: m = (M/nF)Q for ions with valence n
   - Electrochemical equivalent Z = M/(nF)

2. **Ion Transport** (Art. 238)
   - Migration in electric field: v = μE
   - Diffusion: J_diff = -D∇c
   - Nernst-Planck equation: J = -D∇c + μcE

3. **Electrolyte Conductivity**
   - Kohlrausch's law: Λ = Λ₀ - K√c
   - Ion mobility and conductivity relation

### Electrochemical Cell Modeling
- **Voltaic Battery** (Arts. 232-234): Chemistry-based EMF
- **Polarization** (Arts. 269-275): Back EMF from electrolysis products
- **Energy Conservation** (Art. 273): Gibbs free energy → electrical work

### Advanced Phenomena
- Concentration overpotential
- Butler-Volmer kinetics (modern extension)
- Double layer charging
- Ion selectivity and membranes

## Usage

```python
from maxwell.physics.electrochemistry import ElectrolysisModel
from maxwell.chemistry import Electrolyte, Ion

# Define electrolyte
copper_sulfate = Electrolyte(
    name='CuSO4',
    concentration=1.0,  # mol/L
    temperature=298.15,  # K
    ions=[
        Ion('Cu²⁺', charge=+2, mobility=5.5e-4),
        Ion('SO4²⁻', charge=-2, mobility=8.3e-4)
    ]
)

# Compute electrolysis parameters
faraday_params = ElectrolysisModel.faraday_laws(
    electrolyte=copper_sulfate,
    current=0.5,  # amperes
    time=3600  # seconds
)
# Returns: mass_deposited, charge_passed, efficiency

# Ion transport simulation
transport = ElectrolysisModel.nernst_planck(
    ion='Cu²⁺',
    concentration_profile=c_initial,
    E_field=E_applied,
    boundary_conditions={'anode': 'blocking', 'cathode': 'reactive'},
    time_span=[0, 1000]
)

# Back EMF from polarization
back_emf = ElectrolysisModel.compute_polarization(
    electrolyte=copper_sulfate,
    current_density=0.1,  # A/cm²
    electrode_material='platinum',
    model='concentration_overpotential'
)

# Full cell simulation
cell_response = ElectrolysisModel.simulate_cell(
    anode='Zn',
    cathode='Cu',
    electrolyte=copper_sulfate,
    external_resistance=10,  # ohms
    include_polarization=True
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `electrolyte` | Electrolyte | Electrolyte composition and properties |
| `current` | float | Applied current (amperes) |
| `voltage` | float | Applied voltage (volts) |
| `time` | float or ndarray | Time or time array (seconds) |
| `electrode_material` | str | Anode and cathode materials |
| `temperature` | float | Temperature (Kelvin) |
| `model` | str | 'faraday', 'nernst_planck', 'butler_volmer' |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `mass_deposited` | float | Mass at electrode (grams) |
| `charge_efficiency` | float | Coulombic efficiency (0-1) |
| `concentration_profile` | ndarray | c(x,t) evolution |
| `back_emf` | float | Polarization voltage (volts) |
| `metadata` | dict | Citations, Faraday constants, validation |

## Implementation Notes

- CGS units converted to practical electrochemical units
- Faraday constant F = 96485 C/mol = 28924 statcoulomb/equivalent
- Nernst-Planck uses finite difference or finite element
- Butler-Volmer is modern extension (clearly marked as such)
- Ion mobility relates to conductivity: σ = Σ n_i q_i μ_i

## Validation

- Faraday's laws verified against standard equivalents
- Limiting current density matches theory
- Nernst equation for equilibrium potentials
- Conductivity matches handbook values

## Maxwell Article References

| Article | Content |
|---------|---------|
| 236-237 | Electrolysis terminology and Faraday's laws |
| 238 | Modes of ionic conduction |
| 269-275 | Polarization and back EMF |
| 276-286 | Battery theory and energy conservation |
| 287-290 | Contact potentials in cells |

## Related Commands

- `current-flow` - For general conduction
- `dielectric-response` - For non-ionic conduction
- `thermoelectric-model` - For thermal coupling

## Error Handling

- Warns if current exceeds limiting value
- Raises `ElectrolysisError` for impossible stoichiometry
- Validates charge neutrality in electrolyte

## Modern Extensions (Clearly Marked)

- Butler-Volmer kinetics: Post-Maxwell development
- Double layer models: Helmholtz, Gouy-Chapman, Stern
- Ion-selective membranes: Modern electrochemistry
