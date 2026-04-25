# Command: solve-analytical

## Description

Solves analytical benchmark problems in electromagnetism using exact mathematical solutions. This command provides reference solutions for validating numerical implementations and understanding fundamental physics from Maxwell's treatise.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Analytical solutions from Articles across all Parts
- **Standard Mathematical Implementation**: Special functions, integral transforms, series solutions
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Electrostatic Benchmark Problems (Part I)

1. **Point Charge** (Arts. 44-49)
   ```
   E = q/r² r̂
   V = q/r
   ```

2. **Electric Dipole** (Arts. 69-71)
   ```
   V = (p·r̂)/r²
   E = [3(p·r̂)r̂ - p]/r³
   ```

3. **Uniformly Charged Sphere** (Arts. 96-98)
   ```
   Inside (r < R):  E = Qr/R³,  V = Q(3R² - r²)/(2R³)
   Outside (r > R): E = Q/r²,  V = Q/r
   ```

4. **Conducting Sphere in Uniform Field** (Arts. 155-160)
   ```
   V = -E₀r cosθ + E₀R³ cosθ/r²
   E = E₀(ẑ + 3R³/r⁵[3zr - r²ẑ])  (outside)
   E = 0  (inside)
   ```

5. **Point Charge Near Conducting Plane** (Art. 161)
   ```
   Method of images: q' = -q at mirror position
   V = q/|r - r_q| - q/|r - r_q'|
   ```

6. **Point Charge Near Conducting Sphere** (Arts. 166-170)
   ```
   Image charge: q' = -qR/a at r' = R²/a
   Force: F = q²Ra/(a² - R²)²
   ```

### Electrokinematic Benchmark Problems (Part II)

7. **Current in Infinite Wire** (Arts. 475-479)
   ```
   H = 2I/(cr) φ̂  (azimuthal field)
   B = μH
   ```

8. **Current Sheet** (Art. 294)
   ```
   Discontinuity: H_above - H_below = (4π/c)K × n̂
   ```

9. **Spherical Conductor with Steady Current** (Arts. 431-433)
   ```
   V = -J₀r cosθ + (J₀R³/r²) cosθ  (outside)
   V = -(3σ₂/(σ₁+2σ₂))J₀r cosθ  (inside)
   ```

### Magnetostatic Benchmark Problems (Part III)

10. **Magnetic Dipole** (Arts. 387-388)
    ```
    Ω = (m·r̂)/r²
    H = [3(m·r̂)r̂ - m]/r³
    ```

11. **Uniformly Magnetized Sphere** (Arts. 431-433)
    ```
    Inside:  H = -(4π/3)M,  B = (8π/3)M
    Outside: H = dipole field with m = (4π/3)R³M
    ```

12. **Magnetic Shell** (Arts. 409-411)
    ```
    Ω = Φ ω  (strength × solid angle)
    ΔΩ = 4πΦ  (across shell)
    ```

13. **Spherical Shell in Uniform Field** (Arts. 431-433)
    ```
    Complete solution using spherical harmonics
    Internal field uniform, external field dipole perturbation
    ```

### Electromagnetic Benchmark Problems (Part IV)

14. **Infinite Solenoid** (Arts. 675-677)
    ```
    Inside:  B = (4π/c)nI ẑ
    Outside: B = 0
    ```

15. **Circular Current Loop** (Arts. 694-696)
    ```
    On axis: B_z = (2πI/c)R²/(z² + R²)^(3/2)
    Off axis: Elliptic integral solution
    ```

16. **Plane EM Wave in Vacuum** (Arts. 790-791)
    ```
    E = E₀ exp[i(k·r - ωt)]
    B = (c/ω) k × E
    ω/k = c
    ```

17. **Plane EM Wave in Dielectric** (Arts. 794-797)
    ```
    Phase velocity: v = c/√(εμ) = c/n
    Refractive index: n = √(εμ)
    ```

18. **Wave in Conducting Medium** (Arts. 798-800)
    ```
    Attenuation: E ~ exp(-αz)
    Skin depth: δ = c/√(2πσωμ)
    ```

## Usage

```python
from maxwell.solvers.analytical import (
    ElectrostaticSolutions,
    MagnetostaticSolutions,
    WaveSolutions
)
from maxwell.physics.benchmarks import BenchmarkProblem

# ===== ELECTROSTATIC SOLUTIONS =====

# Point charge field
point = ElectrostaticSolutions.point_charge(
    charge=1.0,  # statcoulomb
    position=[0, 0, 0]
)
E = point.field_at([1, 0, 0])  # Returns [1, 0, 0] statvolt/cm

# Dipole field
dipole = ElectrostaticSolutions.dipole(
    moment=[0, 0, 1],  # statcoulomb·cm
    position=[0, 0, 0]
)
E_axial = dipole.field_at([0, 0, 10])  # On axis
E_equatorial = dipole.field_at([10, 0, 0])  # Equatorial

# Charged sphere
sphere = ElectrostaticSolutions.uniformly_charged_sphere(
    total_charge=Q=1.0,
    radius=R=1.0
)
E_inside = sphere.field_at([0.5, 0, 0])  # E = Qr/R³
E_outside = sphere.field_at([2, 0, 0])  # E = Q/r²

# Conducting sphere in uniform field
sphere_field = ElectrostaticSolutions.conducting_sphere_in_field(
    radius=1.0,
    applied_field=[0, 0, 1]  # E₀ = 1 statvolt/cm
)
V = sphere_field.potential_at(r, theta)
E = sphere_field.field_at(r, theta)

# Point charge near plane
image_plane = ElectrostaticSolutions.point_near_conducting_plane(
    charge=1.0,
    charge_position=[0, 0, d],
    plane_position=0
)
force = image_plane.force_on_charge()  # F = q²/(4d²)

# ===== MAGNETOSTATIC SOLUTIONS =====

# Magnetic dipole
mag_dipole = MagnetostaticSolutions.dipole(
    moment=[0, 0, 1],  # emu
    position=[0, 0, 0]
)
H = mag_dipole.field_at([1, 0, 0])

# Uniformly magnetized sphere
mag_sphere = MagnetostaticSolutions.magnetized_sphere(
    magnetization=[0, 0, M],
    radius=1.0
)
H_inside = mag_sphere.field_inside()  # H = -(4π/3)M
B_outside = mag_sphere.field_outside([2, 0, 0])

# Solenoid
solenoid = MagnetostaticSolutions.infinite_solenoid(
    turns_per_length=n=100,
    current=I=1.0,  # abampere
    radius=1.0
)
B_inside = solenoid.field_inside()  # B = (4π/c)nI
B_outside = solenoid.field_outside()  # = 0

# Circular loop
loop = MagnetostaticSolutions.circular_loop(
    current=1.0,
    radius=1.0
)
B_on_axis = loop.field_on_axis(z=2)
B_off_axis = loop.field_elliptic(rho=0.5, z=1)

# ===== WAVE SOLUTIONS =====

# Plane wave in vacuum
wave = WaveSolutions.plane_wave_vacuum(
    frequency=omega=1e10,  # rad/s
    polarization='linear_x',
    propagation='z'
)
E = wave.E_field(t=0, z=0)
B = wave.B_field(t=0, z=0)
poynting = wave.poynting_vector()

# Plane wave in dielectric
dielectric_wave = WaveSolutions.plane_wave_dielectric(
    frequency=omega=1e10,
    epsilon=4.0,
    mu=1.0
)
phase_velocity = dielectric_wave.phase_velocity()  # c/2
wavelength = dielectric_wave.wavelength()

# Plane wave in conductor
conductor_wave = WaveSolutions.plane_wave_conductor(
    frequency=omega=1e10,
    conductivity=sigma=5.96e17,  # copper in CGS
    epsilon=1.0,
    mu=1.0
)
skin_depth = conductor_wave.skin_depth()
attenuation = conductor_wave.attenuation_constant()

# ===== BENCHMARK VALIDATION =====

# Run standard benchmark suite
results = BenchmarkProblem.run_suite('electrostatics')
for test in results:
    print(f"{test.name}: error = {test.relative_error}")

# Compare with numerical solution
numerical_solution = get_from_simulation()
analytical_solution = ElectrostaticSolutions.point_charge(...)
error = analytical_solution.compare(numerical_solution)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `problem_type` | str | Geometry/physics type |
| `parameters` | dict | Problem-specific parameters |
| `observation_points` | ndarray | Points for evaluation |
| `coordinate_system` | str | 'cartesian', 'cylindrical', 'spherical' |
| `time` | float | Time for time-dependent problems |
| `frequency` | float | Frequency for AC/wave problems |
| `include_images` | bool | Include image method solutions |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `field` | VectorField | E, B, H, or D field |
| `potential` | ScalarField | V or Ω potential |
| `force` | ndarray | Force on test charge/current |
| `energy` | float | Field energy or interaction energy |
| `metadata` | dict | Solution details, article references |

## Implementation Notes

### Special Functions Used

- **Legendre polynomials** P_n(cos θ) for spherical problems
- **Bessel functions** J_n, Y_n for cylindrical problems
- **Spherical harmonics** Y_lm for general spherical
- **Elliptic integrals** K(k), E(k) for loop fields

### Series Solutions

Many analytical solutions involve infinite series:
- Image charge series for multiple boundaries
- Spherical harmonic expansions
- Bessel function series for cylindrical

Convergence acceleration techniques applied where needed.

### Validation Against Known Results

All solutions verified against:
- Limiting cases (r → 0, r → ∞)
- Symmetry requirements
- Conservation laws
- Handbook values where available

## Maxwell Article References

| Article | Benchmark |
|---------|-----------|
| 44-49 | Point charge |
| 69-71 | Dipole |
| 96-98 | Charged sphere, Green's function |
| 155-160 | Sphere in uniform field |
| 161 | Plane image method |
| 166-170 | Sphere image method |
| 387-388 | Magnetic dipole |
| 409-411 | Magnetic shell |
| 431-433 | Magnetic sphere |
| 675-677 | Solenoid |
| 694-696 | Circular loop |
| 781-785 | Wave equation |
| 790-791 | Plane wave |
| 798-800 | Conducting medium |

## Related Commands

- `implement-field` - Numerical field implementation
- `validate-physics` - Compare with analytical solutions
- `derive-equations` - Derive governing equations
- `implement-wave` - Wave propagation implementation

## Error Handling

- Raises `NoAnalyticalSolutionError` for problems without closed form
- Warns about series convergence issues
- Provides error bounds for truncated series
- Flags singular points

## Theory Preservation Protocol

All analytical solutions:
1. Derived from Maxwell's original equations
2. Cited to specific articles
3. Verified against Maxwell's results where given
4. User theories handled separately and marked clearly
