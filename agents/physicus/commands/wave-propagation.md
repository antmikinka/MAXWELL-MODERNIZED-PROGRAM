# Command: wave-propagation

## Description

Analyzes electromagnetic wave generation, propagation, and interaction with matter from Maxwell's Part IV (Arts. 781-805). Implements wave equations, propagation in various media, and optical phenomena.

## Functionality

### Wave Fundamentals (Layer 74)

1. **Wave Equation** (Arts. 781-785)
   - ∇²E - (εμ/c²) ∂²E/∂t² = 0
   - ∇²B - (εμ/c²) ∂²B/∂t² = 0
   - Phase velocity: v = c/√(εμ)

2. **Plane Wave Solutions** (Arts. 790-791)
   - E(r,t) = E₀ cos(k·r - ωt + φ)
   - Dispersion: ω = ck/√(εμ)
   - Transverse nature: k · E = 0

3. **Wave Impedance** (Arts. 792-793)
   - η = |E|/|H| = √(μ/ε)
   - Vacuum: η₀ = 1 (CGS) ≈ 377 Ω (SI)
   - Poynting vector: S = (c/4π) E × H

### Propagation Media (Layer 75-78)

4. **Dielectrics** (Arts. 788-789)
   - Refractive index: n = √(εμ)
   - Maxwell relation: n² = ε_r μ_r
   - Dispersion: n(λ) variation

5. **Conductors** (Arts. 798-801)
   - Skin depth: δ = √(2/μσω)
   - Attenuation: e^(-z/δ)
   - Complex wave number

6. **Crystals** (Arts. 794-797)
   - Birefringence (double refraction)
   - Ordinary and extraordinary rays
   - Index ellipsoid

7. **Metals** (Arts. 798-800)
   - Complex refractive index
   - Opacity and absorption
   - Reflectivity

### Wave Phenomena

- **Reflection/Refraction**: Fresnel coefficients
- **Total Internal Reflection**: Evanescent waves
- **Diffraction**: Huygens-Fresnel principle
- **Interference**: Coherent superposition
- **Polarization**: Linear, circular, elliptical

## Usage

```python
from maxwell.physics.wave_optics import WavePropagation
from maxwell.materials import OpticalMaterial

# Plane wave in vacuum
vacuum_wave = WavePropagation.plane_wave(
    frequency=5e14,  # Hz (green light)
    amplitude=1.0,  # statvolt/cm
    polarization='x',
    direction='+z',
    phase=0
)

# Propagation in dielectric
glass = OpticalMaterial(
    name='BK7',
    refractive_index=1.517,
    absorption_coefficient=0  # transparent
)

transmitted = WavePropagation.refraction(
    incident_wave=vacuum_wave,
    medium=glass,
    incidence_angle=30  # degrees
)
# Returns: transmitted wave, reflected wave, Fresnel coefficients

# Skin depth in copper
copper = OpticalMaterial(
    conductivity=5.96e17,  # CGS s⁻¹
    permeability=1
)

skin_depth = WavePropagation.skin_depth(
    material=copper,
    frequency=1e9  # 1 GHz
)
# Returns: δ in cm

# Birefringent crystal
calcite = OpticalMaterial(
    name='calcite',
    n_ordinary=1.658,
    n_extraordinary=1.486,
    optic_axis=[0, 0, 1]
)

ordinary, extraordinary = WavePropagation.birefringence(
    incident_wave=vacuum_wave,
    crystal=calcite,
    thickness=1.0  # cm
)

# Total internal reflection
tir = WavePropagation.total_internal_reflection(
    n1=1.5,  # glass
    n2=1.0,  # air
    incidence_angle=45  # degrees
)
# Returns: reflection_coefficient, evanescent_decay_length

# Diffraction through aperture
diffraction = WavePropagation.fresnel_diffraction(
    aperture='circular',
    radius=0.1,  # cm
    wavelength=5e-5,  # cm (green)
    distance=100  # cm to screen
)

# Waveguide modes
waveguide = WavePropagation.rectangular_waveguide(
    dimensions=[2.286, 1.016],  # cm (WR-90)
    mode='TE10',
    frequency=10e9  # 10 GHz
)
# Returns: cutoff frequency, propagation constant, field distribution
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `frequency` | float | Wave frequency (Hz) |
| `wavelength` | float | Wavelength in vacuum (cm) |
| `medium` | OpticalMaterial | Propagation medium |
| `polarization` | str | 'linear', 'circular', 'elliptical' |
| `direction` | VectorField | Propagation direction |
| `incidence_angle` | float | Angle for reflection/refraction |
| `geometry` | dict | Aperture or waveguide geometry |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `E_field` | VectorField | Electric field distribution |
| `B_field` | VectorField | Magnetic field distribution |
| `intensity` | ScalarField | |S| (power per area) |
| `reflection_coef` | complex | Fresnel r coefficient |
| `transmission_coef` | complex | Fresnel t coefficient |
| `phase_shift` | float | Phase change (radians) |
| `metadata` | dict | Citations, validation, method info |

## Implementation Notes

- CGS units: E in statvolt/cm, H in oersted
- Complex notation for harmonic fields: E e^(-iωt)
- Jones calculus for polarization
- Transfer matrix for multilayer structures
- FFT-based propagation for diffraction

## Validation

- Snell's law: n₁ sin θ₁ = n₂ sin θ₂
- Fresnel coefficients at normal incidence
- Skin depth formula for conductors
- Waveguide cutoff frequencies
- Rayleigh range for Gaussian beams

## Maxwell Article References

| Article | Content |
|---------|---------|
| 781-785 | Wave equation derivation |
| 786-787 | Speed of light = c/√(εμ) |
| 788-789 | Refractive index relation |
| 790-791 | Plane wave solutions |
| 792-793 | Radiation pressure |
| 794-797 | Crystal optics |
| 798-801 | Conducting media |
| 802-805 | Diffusion in conductors |

## Related Commands

- `maxwell-equations` - For full wave simulation
- `magneto-optics` - For Faraday rotation
- `material-properties` - For optical constants

## Error Handling

- Warns if absorption is high
- Raises `WaveError` for evanescent propagation in wrong context
- Validates energy conservation at interfaces

## Modern Extensions (Clearly Marked)

- Gaussian beam optics
- Fiber optic modes
- Photonic crystal band structure
- Metamaterial effective parameters
