# Command: maxwell-equations

## Description

Solves the complete Maxwell equation system for time-dependent electromagnetic fields. This is the crown jewel of the physics implementation, unifying Parts I-IV into a single coherent framework (Arts. 604-619, 781-797).

## Functionality

### Maxwell's Equations (CGS Gaussian)

1. **Gauss's Law** (Art. 604-607)
   - ∇ · D = 4πρ
   - D = εE (constitutive)

2. **No Magnetic Monopoles** (Art. 604)
   - ∇ · B = 0
   - B = ∇ × A (automatic satisfaction)

3. **Faraday's Law** (Arts. 590-592, 604)
   - ∇ × E = -(1/c) ∂B/∂t
   - E = -∇φ - (1/c) ∂A/∂t

4. **Ampère-Maxwell Law** (Arts. 604-611)
   - ∇ × H = (4π/c)J + (1/c) ∂D/∂t
   - Displacement current: (1/c) ∂D/∂t
   - H = B/μ (linear media)

### Wave Equations (Layer 74)

5. **Electromagnetic Waves** (Arts. 781-787)
   - ∇²E - (1/c²) ∂²E/∂t² = 0 (source-free)
   - ∇²B - (1/c²) ∂²B/∂t² = 0
   - Wave speed: v = c/√(εμ)

6. **Plane Wave Solutions** (Arts. 790-793)
   - E = E₀ exp(i(k·r - ωt))
   - B = (c/ω) k × E
   - Transverse: k · E = 0, k · B = 0
   - Impedance: |E|/|H| = √(μ/ε)

### Solution Methods

- **FDTD** (Finite-Difference Time-Domain): Yee lattice
- **FEM** (Finite Element Method): Unstructured grids
- **Spectral**: Fourier methods for periodic problems
- **FDFD** (Finite-Difference Frequency-Domain): Harmonic steady-state
- **Method of Moments**: Surface integral equations

### Boundary Conditions

- Perfect electric conductor (PEC): E_t = 0
- Perfect magnetic conductor (PMC): H_t = 0
- Dielectric interface: D_n, B_n, E_t, H_t continuity
- Absorbing boundaries: PML (Perfectly Matched Layer)

## Usage

```python
from maxwell.physics.maxwell_solver import MaxwellEquations
from maxwell.core import VectorField, Grid
from maxwell.materials import Material

# Define computational domain
grid = Grid(
    dimensions=[100, 100, 100],  # cells
    spacing=[0.1, 0.1, 0.1],  # cm per cell
    boundary_conditions=['pml', 'pml', 'pml', 'pml', 'pec', 'pec']
)

# Define materials
vacuum = Material(epsilon=1.0, mu=1.0, sigma=0)
glass = Material(epsilon=10.0, mu=1.0, sigma=0)
copper = Material(epsilon=1.0, mu=1.0, sigma=5.96e17)

geometry = {
    'background': vacuum,
    'sphere': {'material': glass, 'center': [5, 5, 5], 'radius': 2},
    'plate': {'material': copper, 'bounds': [[0,10], [0,10], [9.5,10]]}
}

# Define source: Gaussian pulse current
source = {
    'type': 'current',
    'location': [5, 5, 2],
    'direction': 'z',
    'waveform': 'gaussian',
    'parameters': {'amplitude': 1.0, 'width': 1e-12}  # statamperes, seconds
}

# Initialize solver
solver = MaxwellEquations(
    grid=grid,
    materials=geometry,
    sources=[source],
    method='fdtd'  # or 'fem', 'spectral'
)

# Run simulation
fields = solver.run(
    time_steps=10000,
    dt=1e-15,  # seconds (CFL condition)
    monitors=[
        {'type': 'E', 'location': [5, 5, 8]},
        {'type': 'H', 'location': [5, 5, 8]},
        {'type': 'flux', 'surface': 'z=9'}
    ]
)

# Frequency domain analysis
freq_response = solver.frequency_domain(
    frequencies=[1e9, 2e9, 5e9, 10e9],  # Hz
    excitation='plane_wave',
    direction='+z',
    polarization='x'
)

# Waveguide mode analysis
modes = solver.waveguide_modes(
    cross_section='rectangular',
    dimensions=[2.286, 1.016],  # cm (WR-90)
    frequency=10e9  # Hz
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `grid` | Grid | Computational mesh |
| `materials` | dict | Material distribution |
| `sources` | list | Current and field sources |
| `method` | str | 'fdtd', 'fem', 'spectral', 'fdfd' |
| `time_steps` | int | Number of time iterations |
| `dt` | float | Time step (seconds) |
| `frequencies` | ndarray | Frequency points for harmonic analysis |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `E_field` | VectorFieldGrid | Electric field vs. space and time |
| `B_field` | VectorFieldGrid | Magnetic field vs. space and time |
| `energy` | ScalarFieldGrid | Energy density evolution |
| `flux` | float | Power through monitors (erg/s) |
| `s_parameters` | dict | Scattering parameters (frequency domain) |
| `metadata` | dict | Citations, CFL number, convergence info |

## Implementation Notes

- CGS units throughout
- CFL condition: dt ≤ min(Δx,Δy,Δz)/(c√3) for FDTD
- PML absorption coefficient optimized for reflection < -60 dB
- Dispersion relations verified for plane waves
- Energy conservation monitored throughout

## Validation

- Plane wave propagation at speed c
- Snell's law at dielectric interfaces
- Reflection/transmission coefficients
- Cavity resonance frequencies
- Waveguide cutoff frequencies

## Maxwell Article References

| Article | Content |
|---------|---------|
| 604-611 | General field equations |
| 606-607 | Ampère-Maxwell law |
| 610-611 | Total current (conduction + displacement) |
| 781-787 | Wave equation derivation |
| 786-787 | Speed of light calculation |
| 790-793 | Plane wave solutions |
| 794-797 | Crystal optics |

## Related Commands

- `wave-propagation` - For specialized wave analysis
- `em-coupling` - For near-field coupling
- `optics-module` - For light propagation

## Error Handling

- Warns if CFL condition violated
- Raises `MaxwellError` for non-physical materials
- Monitors energy conservation (should be < 1% drift)
