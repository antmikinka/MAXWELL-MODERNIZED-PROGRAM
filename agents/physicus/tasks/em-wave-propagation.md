# Task: EM Wave Propagation

## Description

Complete workflow for simulating electromagnetic wave propagation using Maxwell's Part IV theory. This task covers wave generation, propagation in various media, and optical phenomena.

## Source Category

**CRITICAL: Theory Preservation**

This task implements:
- **Maxwell's 1873 Historical Text**: Articles 781-805 (Electromagnetic Theory of Light)
- **Standard Mathematical Implementation**: Wave equation solvers, Fourier optics
- **User Original Theory**: NONE - mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Task Workflow

### Phase 1: Wave Source Definition

**Step 1.1: Define Wave Parameters**
```python
from maxwell.tasks.wave_propagation import EMWaveProblem
from maxwell.optics.wave import PlaneWave

wave = EMWaveProblem(
    frequency=omega=2*np.pi*5e14,  # rad/s (green light)
    wavelength=lambda_0=2*np.pi*c/omega,  # cm
    polarization='linear_x',
    propagation_direction=[0, 0, 1]
)
```

**Step 1.2: Define Source Geometry**
```python
# Point source (spherical wave)
problem = EMWaveProblem.point_source(
    frequency=omega,
    position=[0, 0, 0],
    dipole_moment=[1, 0, 0]  # oscillating dipole
)

# Plane wave source
problem = EMWaveProblem.plane_wave(
    frequency=omega,
    amplitude=E0=1.0,
    wave_vector=[0, 0, k]
)

# Gaussian beam
problem = EMWaveProblem.gaussian_beam(
    frequency=omega,
    waist_radius=w0=0.1,  # cm
    waist_position=[0, 0, 0]
)
```

### Phase 2: Medium Definition

**Step 2.1: Homogeneous Medium**
```python
# Vacuum
problem.set_medium('vacuum', epsilon=1, mu=1, sigma=0)

# Dielectric
problem.set_medium('glass', epsilon=4.0, mu=1.0, sigma=0)

# Conductor
problem.set_medium('copper', epsilon=1, mu=1, sigma=5.96e17)

# Lossy dielectric
problem.set_medium('water', epsilon=80, mu=1, sigma=1e-4)
```

**Step 2.2: Inhomogeneous Medium**
```python
# Graded index
problem.set_medium(
    'graded_index',
    epsilon=lambda x, y, z: 1 + exp(-(x**2 + y**2)),
    mu=1,
    sigma=0
)

# Layered medium
problem.set_layered_medium([
    {'z_min': -np.inf, 'z_max': 0, 'epsilon': 1, 'mu': 1},
    {'z_min': 0, 'z_max': 1, 'epsilon': 4, 'mu': 1},
    {'z_min': 1, 'z_max': np.inf, 'epsilon': 1, 'mu': 1}
])
```

**Step 2.3: Anisotropic Medium (Crystal)**
```python
problem.set_anisotropic_medium(
    epsilon_tensor=[
        [n_o**2, 0, 0],
        [0, n_o**2, 0],
        [0, 0, n_e**2]
    ],
    mu=1,
    optic_axis=[0, 0, 1]
)
```

### Phase 3: Wave Equation Solution

**Step 3.1: Analytical Solution (Plane Wave)**
```python
solution = problem.solve_analytical(
    solution_type='plane_wave',
    include_reflection=True,
    include_transmission=True
)

# Get fields
E = solution.E_field
B = solution.B_field
```

**Step 3.2: Numerical Solution (FDTD)**
```python
solution = problem.solve_numerical(
    method='FDTD',
    grid_spacing=dx=lambda_0/20,
    time_step=dt=dx/(2*c),
    total_time=10*period,
    boundary_conditions='PML'  # Perfectly matched layer
)
```

**Step 3.3: Frequency Domain Solution**
```python
solution = problem.solve_frequency_domain(
    method='finite_element',
    mesh_density='fine',
    solver='direct'
)
```

### Phase 4: Wave Phenomena

**Step 4.1: Reflection and Refraction**
```python
# Fresnel coefficients
fresnel = solution.compute_fresnel_coefficients(
    interface='dielectric',
    n1=1.0,
    n2=1.5,
    incidence_angle=45  # degrees
)

r_s = fresnel.reflection_coefficient_s()
r_p = fresnel.reflection_coefficient_p()
t_s = fresnel.transmission_coefficient_s()
t_p = fresnel.transmission_coefficient_p()

# Verify energy conservation
R = abs(r_s)**2 + abs(r_p)**2  # Reflectance
T = ...  # Transmittance
assert abs(R + T - 1) < 1e-6
```

**Step 4.2: Total Internal Reflection**
```python
tir = solution.check_total_internal_reflection(
    n1=1.5, n2=1.0,
    incidence_angle=60  # Above critical angle
)
print(f"Evanescent decay length: {tir.decay_length}")
```

**Step 4.3: Dispersion Analysis**
```python
# Group velocity
v_group = solution.group_velocity()
v_phase = solution.phase_velocity()

# Dispersion relation
omega_k = solution.dispersion_relation()
```

### Phase 5: Optical Phenomena

**Step 5.1: Birefringence**
```python
birefringence = solution.compute_birefringence(
    crystal='calcite',
    propagation_direction=[1, 0, 0]
)

n_ordinary = birefringence.n_o
n_extraordinary = birefringence.n_e
delta_n = birefringence.n_e - birefringence.n_o
```

**Step 5.2: Faraday Rotation**
```python
faraday = solution.compute_faraday_rotation(
    material='flint_glass',
    magnetic_field=1000,  # Gauss
    path_length=10,  # cm
    wavelength=lambda_0
)

rotation_angle = faraday.rotation  # radians
verdet_constant = faraday.verdet
```

**Step 5.3: Diffraction**
```python
# Fraunhofer diffraction
diffraction = solution.fraunhofer_diffraction(
    aperture='circular',
    aperture_radius=a=0.1
)

# Airy pattern
airy_intensity = diffraction.airy_pattern()
first_minimum_angle = diffraction.first_minimum_angle()  # 1.22*lambda/a
```

### Phase 6: Energy and Momentum

**Step 6.1: Poynting Vector**
```python
S = solution.poynting_vector()
S_avg = solution.time_averaged_poynting()

# Power through surface
power = solution.power_through_surface(surface)
```

**Step 6.2: Radiation Pressure**
```python
pressure = solution.radiation_pressure(
    surface_type='absorbing'  # or 'reflecting'
)
# p = S/c (absorbing) or p = 2S/c (reflecting)
```

**Step 6.3: Energy Density**
```python
u_electric = solution.electric_energy_density()  # E²/8π
u_magnetic = solution.magnetic_energy_density()  # B²/8π
u_total = solution.total_energy_density()
```

### Phase 7: Validation

**Step 7.1: Verify Wave Equation**
```python
# Check that solution satisfies wave equation
residual = solution.verify_wave_equation()
assert max(abs(residual)) < 1e-6
```

**Step 7.2: Verify Maxwell's Equations**
```python
# All four equations should be satisfied
div_E = solution.verify_gauss_law()
div_B = solution.verify_no_monopoles()
curl_E = solution.verify_faradays_law()
curl_B = solution.verify_ampere_maxwell()

assert all(abs(x) < 1e-6 for x in [div_E, div_B, curl_E, curl_B])
```

**Step 7.3: Verify Energy Conservation**
```python
# Poynting theorem
energy_balance = solution.verify_poynting_theorem()
assert abs(energy_balance) < 1e-6
```

### Phase 8: Visualization

**Step 8.1: Field Snapshots**
```python
solution.plot_field_snapshot(
    field='E',
    plane='xz',
    time=0,
    colormap='RdBu',
    show_contours=True
)
```

**Step 8.2: Animation**
```python
solution.animate_wave_propagation(
    duration=2*period,
    frames=100,
    show='both',  # E and B fields
    output='mp4'
)
```

**Step 8.3: Interference Pattern**
```python
solution.plot_interference_pattern(
    sources=['point1', 'point2'],
    observation_plane='xy',
    show_fringes=True
)
```

## Example: Waveguide Mode Analysis

```python
from maxwell.tasks.wave_propagation import waveguide_analysis

# Rectangular waveguide
result = waveguide_analysis(
    geometry='rectangular',
    width=a=2.0,  # cm
    height=b=1.0,  # cm
    frequency=10e10  # 10 GHz
)

# Get mode properties
TE10 = result.get_mode('TE10')
cutoff = TE10.cutoff_frequency()
beta = TE10.propagation_constant()
lambda_g = TE10.guide_wavelength()

print(f"Cutoff frequency: {cutoff/1e9:.2f} GHz")
print(f"Guide wavelength: {lambda_g:.3f} cm")

# Field distribution
TE10.plot_field_distribution()
```

## Deliverables

1. **Electric Field** E(x,y,z,t)
2. **Magnetic Field** B(x,y,z,t)
3. **Poynting Vector** S (energy flux)
4. **Wave Properties** (wavelength, velocity, impedance)
5. **Optical Properties** (reflection, transmission, rotation)
6. **Validation Report**
7. **Visualization Package**

## Maxwell Article References

| Article | Relevance |
|---------|-----------|
| 781-785 | Wave equation derivation |
| 786-787 | Speed of light identity |
| 790-791 | Plane wave solutions |
| 792-793 | Energy flux (Poynting) |
| 794-797 | Crystal optics |
| 798-800 | Conducting media |
| 801-805 | Diffusion in conductors |

## Quality Gates

- [ ] Wave equation satisfied
- [ ] Maxwell's equations verified
- [ ] Energy conservation confirmed
- [ ] Boundary conditions satisfied
- [ ] Maxwell article citations included

## Related Tasks

- `electrostatic-field-solution` - Static limit
- `magnetic-dipole-field` - Magnetostatic limit
- `vector-potential-calculation` - Potential formulation
- `energy-momentum-tensor` - Stress tensor
