# Task: wave-equation-solution

## Description

Solves electromagnetic wave equations for specific geometries and boundary conditions from Maxwell's Part IV (Arts. 781-805). This task provides analytical and numerical solutions for wave propagation problems.

## Workflow Steps

### 1. Wave Problem Definition
- Specify geometry (free space, waveguide, cavity, etc.)
- Define material properties (ε, μ, σ)
- Set source characteristics (frequency, polarization)
- Identify boundary conditions

### 2. Wave Equation Setup
- **Helmholtz equation**: ∇²E + k²E = 0 (frequency domain)
- **Wave equation**: ∇²E - (1/c²)∂²E/∂t² = 0 (time domain)
- **Wave number**: k = ω√(εμ)/c
- **Dispersion relation**: ω(k) for guided waves

### 3. Solution Methods
- **Separation of variables**: For separable geometries
- **Modal expansion**: For waveguides and cavities
- **Green's functions**: For radiation problems
- **Numerical**: FDTD, FEM for complex problems

### 4. Post-Processing
- Field distributions E(x,y,z), H(x,y,z)
- Power flow (Poynting vector)
- Resonant frequencies (cavities)
- Scattering parameters

## Requirements

**Input:**
- `geometry`: dict - Domain and boundaries
- `materials`: dict - ε, μ, σ distribution
- `sources`: list - Current and field sources
- `frequency`: float or array - Operating frequency
- `method`: str - Solution approach

**Output:**
- `E_field`: VectorFieldGrid - Electric field
- `H_field`: VectorFieldGrid - Magnetic field
- `modes`: list - Modal solutions (for guided waves)
- `s_parameters`: dict - Scattering matrix
- `metadata`: dict - Citations, validation

## Implementation

```python
from maxwell.tasks.wave_equation import WaveEquationSolver
from maxwell.materials import Material

# Problem 1: Rectangular waveguide
waveguide = {
    'geometry': 'rectangular',
    'dimensions': [2.286, 1.016],  # cm (WR-90)
    'material': 'vacuum',
    'boundaries': 'PEC'
}

solver_wg = WaveEquationSolver(waveguide)
modes = solver_wg.compute_modes(
    mode_types=['TE', 'TM'],
    max_mode_index=3,
    frequency=10e9  # 10 GHz
)
# Returns: TE10, TE20, TE01, etc. with cutoff frequencies

# Problem 2: Spherical cavity resonator
cavity = {
    'geometry': 'spherical',
    'radius': 5,  # cm
    'material': 'vacuum',
    'boundaries': 'PEC'
}

solver_cav = WaveEquationSolver(cavity)
resonances = solver_cav.compute_resonant_frequencies(
    max_order=5
)
# Returns: TE and TM modes with resonant frequencies

# Problem 3: Plane wave scattering by sphere
scattering = {
    'geometry': 'sphere',
    'radius': 1,  # cm
    'material': 'dielectric',
    'incident_wave': {
        'type': 'plane_wave',
        'frequency': 1e10,
        'polarization': 'x',
        'direction': '+z'
    }
}

solver_scat = WaveEquationSolver(scattering)
result = solver_scat.mie_scattering()
# Returns: scattering coefficients, cross-sections

# Problem 4: Antenna radiation
antenna = {
    'type': 'dipole',
    'length': 15,  # cm (half-wave at 1 GHz)
    'feed_point': 'center',
    'frequency': 1e9
}

solver_ant = WaveEquationSolver(antenna)
radiation = solver_ant.compute_radiation_pattern(
    distance=100,  # far-field
    angular_resolution=5  # degrees
)
# Returns: E(θ,φ), gain, directivity

# Problem 5: Transmission line discontinuity
tline = {
    'geometry': 'coaxial',
    'dimensions': {'a': 0.5, 'b': 1.5},  # cm
    'discontinuity': 'step',
    'section1': {'Z0': 50},
    'section2': {'Z0': 75},
    'frequency': 1e9
}

solver_tl = WaveEquationSolver(tline)
s_params = solver_tl.compute_scattering_parameters()
# Returns: S11 (reflection), S21 (transmission)
```

## Example Problems

### 1. Plane Wave at Dielectric Interface
```python
# Fresnel reflection and transmission
# r_s, r_p, t_s, t_p coefficients
```

### 2. Cylindrical Waveguide (Optical Fiber)
```python
# LP modes, V-number, cutoff conditions
```

### 3. Patch Antenna
```python
# Microstrip patch resonant frequency and pattern
```

## Validation Criteria

- [ ] Helmholtz equation satisfied: (∇² + k²)E = 0
- [ ] Boundary conditions met
- [ ] ∇ · E = 0 (source-free)
- [ ] Power conservation: |S11|² + |S21|² = 1 (lossless)
- [ ] Cutoff frequencies match analytical formulas
- [ ] Far-field radiation pattern integrates to total power

## Maxwell Article References

| Article | Content |
|---------|---------|
| 781-785 | Wave equation derivation |
| 786-787 | Speed of light calculation |
| 790-791 | Plane wave solutions |
| 792-793 | Radiation pressure |
| 794-797 | Crystal optics |
| 798-801 | Conducting media |

## Related Tasks

- `maxwell-solver-setup` - Full time-domain simulation
- `antenna-design` - Radiation problems
- `optical-system` - Lens and mirror systems
