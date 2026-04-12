# Command: implement-wave

## Description

Implements electromagnetic wave propagation from Maxwell's equations. This command provides the complete wave theory from Maxwell's Part IV (Arts. 781-805), proving that light is an electromagnetic phenomenon.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Articles 781-805 (Electromagnetic Theory of Light)
- **Standard Mathematical Implementation**: Wave equation solvers, Fourier methods
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Wave Equation Derivation (Arts. 781-785)

1. **Wave Equation in Vacuum**
   ```
   From Maxwell's equations in vacuum (ρ=0, J=0):
   
   ∇ × E = -(1/c) ∂B/∂t
   ∇ × H = (1/c) ∂D/∂t
   
   Taking curl of first and substituting:
   ∇²E - (1/c²) ∂²E/∂t² = 0
   ∇²B - (1/c²) ∂²B/∂t² = 0
   ```

2. **Speed of Light Identity** (Arts. 786-787)
   ```
   Wave speed: v = c/√(εμ)
   
   For vacuum (ε=1, μ=1): v = c
   This proves light IS electromagnetic waves!
   ```

### Plane Wave Solutions (Arts. 790-791)

3. **Plane Wave in Vacuum**
   ```
   E(r,t) = E₀ exp[i(k·r - ωt)]
   B(r,t) = B₀ exp[i(k·r - ωt)]
   
   Relations:
   |E| = |B|  (in CGS)
   k × E = (ω/c) B
   k · E = 0  (transverse)
   k · B = 0  (transverse)
   ```

4. **Polarization States**
   - Linear: E oscillates in fixed direction
   - Circular: E rotates with constant magnitude
   - Elliptical: General case

### Wave Propagation in Media

5. **Dielectric Media** (Arts. 794-797)
   ```
   Phase velocity: v = c/n
   Refractive index: n = √(εμ)
   
   Wavelength: λ = λ₀/n
   Frequency unchanged: ω = constant
   ```

6. **Crystal Optics** (Arts. 794-797)
   - Birefringence (double refraction)
   - Ordinary and extraordinary rays
   - Index ellipsoid

7. **Conducting Media** (Arts. 798-800)
   ```
   Complex wave number: k = k' + ik''
   
   Attenuation: E ~ exp(-k''z)
   Skin depth: δ = 1/k'' = c/√(2πσωμ)
   
   For good conductors (σ >> ωε):
   δ ≈ c/√(2πσω)
   ```

### Energy and Momentum

8. **Poynting Vector** (Arts. 792-793)
   ```
   Energy flux: S = (c/4π) E × H
   
   Time average for plane wave:
   <S> = (c/8π) |E₀|² k̂
   
   Radiation pressure:
   p = <S>/c  (perfect absorption)
   p = 2<S>/c  (perfect reflection)
   ```

### Magneto-Optics (Arts. 806-821)

9. **Faraday Rotation**
   ```
   Rotation angle: θ = V B L
   
   V = Verdet constant
   B = magnetic field strength
   L = path length
   
   Circular birefringence:
   n_± = n₀ ± Δn (for σ± circular)
   ```

10. **Molecular Vortex Model** (Arts. 822-831)
    - Maxwell's mechanistic model
    - Vortex angular velocity
    - Connection to magnetic field

### Waveguide and Cavity Solutions

11. **Waveguide Modes**
    - TE modes (transverse electric)
    - TM modes (transverse magnetic)
    - Cutoff frequencies

12. **Cavity Resonances**
    - Rectangular cavity modes
    - Spherical cavity modes
    - Quality factor Q

## Usage

```python
from maxwell.optics.wave_propagation import (
    PlaneWave,
    WaveInDielectric,
    WaveInConductor,
    Waveguide
)
from maxwell.optics.magneto_optics import FaradayRotation
from maxwell.physics.poynting import compute_energy_flux

# ===== PLANE WAVE IN VACUUM =====

wave = PlaneWave(
    frequency=omega=2*np.pi*5e14,  # green light
    propagation_direction=[0, 0, 1],  # +z
    polarization='linear_x',  # E along x
    amplitude=E0=1.0  # statvolt/cm
)

# Get fields at position and time
E = wave.E_field(position=[0, 0, 0], time=0)
B = wave.B_field(position=[0, 0, 0], time=0)

# Wave properties
wavelength = wave.wavelength  # lambda = 2pi*c/omega
k_vector = wave.wave_vector  # k = omega/c
period = wave.period

# ===== WAVE IN DIELECTRIC =====

glass_wave = WaveInDielectric(
    frequency=omega=2*np.pi*5e14,
    epsilon=4.0,  # n = 2
    mu=1.0,
    propagation_direction=[0, 0, 1]
)

phase_velocity = glass_wave.phase_velocity  # c/2
wavelength_in_medium = glass_wave.wavelength  # lambda_0/2
refractive_index = glass_wave.refractive_index  # n = 2

# ===== WAVE IN CONDUCTOR =====

copper_wave = WaveInConductor(
    frequency=omega=2*np.pi*60,  # 60 Hz
    conductivity=5.96e17,  # copper in CGS
    epsilon=1.0,
    mu=1.0
)

skin_depth = copper_wave.skin_depth()  # ~0.8 cm at 60 Hz
attenuation = copper_wave.attenuation_constant()
penetration_depth = 1/attenuation

# For optical frequencies
optical_wave = WaveInConductor(
    frequency=2*np.pi*5e14,
    conductivity=5.96e17,
    epsilon=1.0,
    mu=1.0
)
optical_skin_depth = optical_wave.skin_depth()  # ~25 nm

# ===== ENERGY AND MOMENTUM =====

# Poynting vector
S = compute_energy_flux(E, B)
S_avg = wave.time_averaged_poynting()

# Radiation pressure
pressure_absorb = wave.radiation_pressure(surface='absorbing')
pressure_reflect = wave.radiation_pressure(surface='reflecting')

# Intensity
intensity = wave.intensity  # |<S>|

# ===== CRYSTAL OPTICS =====

# Birefringent crystal
crystal_wave = WaveInDielectric(
    epsilon_tensor=[
        [n_o**2, 0, 0],
        [0, n_o**2, 0],
        [0, 0, n_e**2]
    ],
    propagation_direction=[1, 0, 0]
)

ordinary_index = crystal_wave.ordinary_refractive_index()
extraordinary_index = crystal_wave.extraordinary_refractive_index()
birefringence = extraordinary_index - ordinary_index

# ===== FARADAY ROTATION =====

faraday = FaradayRotation(
    material='flint_glass',
    magnetic_field=1000,  # Gauss
    path_length=10  # cm
)

rotation_angle = faraday.rotation_angle()  # radians
verdet_constant = faraday.verdet_constant()

# Circular birefringence
n_plus, n_minus = faraday.circular_indices()
rotation = (np.pi*L/lambda_0) * (n_plus - n_minus)

# ===== WAVEGUIDE MODES =====

# Rectangular waveguide
waveguide = Waveguide(
    geometry='rectangular',
    width=a=2.0,  # cm
    height=b=1.0,  # cm
    mode='TE10'
)

cutoff_frequency = waveguide.cutoff_frequency()  # TE10
propagation_constant = waveguide.beta(frequency=10e10)
guide_wavelength = waveguide.guide_wavelength(frequency=10e10)

# Check if mode propagates
if frequency > cutoff_frequency:
    print("Mode propagates")
else:
    print("Mode evanescent")

# ===== VISUALIZATION =====

# Plot field distribution
wave.plot_field_snapshot(
    plane='xz',
    time=0,
    show_vectors=True
)

# Animation
wave.animate_wave_propagation(
    duration=2*period,
    frames=100
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `frequency` | float | Angular frequency ω (rad/s) |
| `propagation_direction` | ndarray | Unit vector k̂ |
| `polarization` | str | 'linear', 'circular', 'elliptical' |
| `medium` | dict | Material properties (ε, μ, σ) |
| `geometry` | str | 'plane', 'waveguide', 'cavity' |
| `boundary_conditions` | dict | For bounded problems |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `E_field` | VectorField | Electric field |
| `B_field` | VectorField | Magnetic field |
| `S` | VectorField | Poynting vector |
| `properties` | dict | Wavelength, velocity, impedance |
| `metadata` | dict | Mode info, citations, validation |

## Implementation Notes

### CGS Units for Waves

| Quantity | CGS Unit |
|----------|----------|
| E field | statvolt/cm |
| B field | gauss |
| Frequency | rad/s |
| Wavelength | cm |
| Poynting vector | erg/(cm²·s) |

### Dispersion Relations

For various media:
- Vacuum: ω = ck
- Dielectric: ω = ck/n
- Conductor: k² = (ω²/c²)(ε + i4πσ/ω)

### Polarization Handling

Jones calculus for polarization:
- Linear: Jones vector [1, 0] or [0, 1]
- Circular: [1, ±i]/√2
- Elliptical: General complex vector

## Validation

### Analytical Checks
- Transversality: k · E = 0, k · B = 0
- Field relation: |E| = |B| in vacuum
- Dispersion: ω/k = c/n
- Energy conservation: ∇ · S + ∂u/∂t = 0

### Physical Checks
- Speed of light in vacuum equals c
- Snell's law at interfaces
- Fresnel coefficients for reflection/transmission
- Faraday rotation proportional to B·L

## Maxwell Article References

| Article | Content |
|---------|---------|
| 781-785 | Wave equation derivation |
| 786-787 | Speed of light = c/√(εμ) |
| 788-789 | Refractive index relation |
| 790-791 | Plane wave solutions |
| 792-793 | Energy flux (Poynting) |
| 794-797 | Crystal optics |
| 798-800 | Conducting media, opacity |
| 801-805 | Diffusion in conductors |
| 806-810 | Faraday rotation |
| 811-817 | Circular polarization |
| 822-831 | Molecular vortex model |

## Related Commands

- `derive-equations` - Derive wave equation
- `implement-field` - Field computations
- `solve-analytical` - Plane wave solutions
- `implement-constitutive` - Material optical properties

## Error Handling

- Raises `NoPropagationError` below cutoff
- Warns about numerical dispersion
- Flags absorbing boundary requirements
- Validates stability conditions

## Theory Preservation Protocol

All wave implementations:
1. Derived from Maxwell's equations as in Arts. 781-785
2. Light speed identity proven as in Arts. 786-787
3. User theories marked and preserved exactly
4. Historical notes on Maxwell's optical insights
