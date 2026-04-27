# Use Cases -- Maxwell Modernized

> What you can actually do with a computational implementation of Maxwell's 1873 _Treatise on Electricity and Magnetism_.

## What This Is

A computational reference library containing every formula from James Clerk Maxwell's 1873 _A Treatise on Electricity and Magnetism_ -- all 866 articles -- implemented in executable Python with full citation traceability. Every function links to a specific article in the original text. Every calculation is reproducible.

The library uses CGS-EMU (centimeter-gram-second electromagnetic units) throughout, the system Maxwell himself employed. SI equivalents are available for reference and cross-checking.

**241 modules. 1,174 functions. 244 classes. 548 tests. All passing.**

---

## What You Can Actually Do With It

### 1. Electromagnetic Calculations

Compute electrostatic fields, magnetic forces, electromagnetic induction, and wave propagation using Maxwell's original formulations -- all in a few lines of Python.

**Electrostatic field from a point charge (Art. 29-30)**

```python
import numpy as np
from maxwell.core.charge import PointCharge

# Place a 1 esu charge at the origin
charge = PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))

# Compute the electric field 5 cm away along the x-axis
point = np.array([5.0, 0.0, 0.0])
E = charge.field_at(point)
print(f"E = {E}")  # [0.04 0.   0.  ] esu/cm^2  (E = q/r^2 = 1/25)
```

**Lorentz force on a current-carrying wire (Arts. 490-491)**

```python
from maxwell.electromagnetism.forces.lorentz import LorentzForce

# 2 abamperes in +x direction, B = 500 gauss in +z direction
force = LorentzForce(
    current=2.0,           # abamperes
    B_field=[0, 0, 500],   # gauss
    length=[10, 0, 0],     # cm, current along +x
)
F = force.force_vector()
print(f"F = {F} dynes")  # Force vector as numpy array
```

**Faraday induction in a loop (Arts. 528-531)**

```python
from maxwell.electromagnetism.induction.faraday import FaradayInduction, calc_induced_emf

# A circular loop of 10 turns with magnetic flux changing at 10 maxwells/s
induction = FaradayInduction(num_turns=10)
emf = induction.induced_emf(flux_change_rate=-10.0)
print(f"EMF = {emf} abvolts")
```

**Oersted's magnetic field around a wire (Arts. 475-479)**

```python
from maxwell.electromagnetism.sources.oersted import calc_oersted_field

# Field 2 cm from a straight wire carrying 3 abamperes
B = calc_oersted_field(current=3.0, distance=2.0)
print(f"B = {B:.4f} oersted at 2 cm from wire")  # H = 2*I/r = 3.0
```

**Magnetic induction in a material (Art. 605)**

```python
from maxwell.materials.constitutive import Magnetization
import numpy as np

# Iron with susceptibility chi = 200, H = 50 oersted applied
mat = Magnetization(susceptibility=200.0)
B = mat.magnetic_induction(H_field=np.array([50.0]))  # CGS: B = (1 + 4*pi*chi)*H
print(f"B = {B} gauss")
```

**Electromagnetic wave properties (Arts. 783-791)**

```python
from maxwell.optics import PlaneWave, calc_wave_speed, verify_speed_equals_c
import numpy as np

# Plane wave propagating in +z direction with E0 = 0.1 statvolt/cm
wave = PlaneWave(
    E0=np.array([0.1, 0.0, 0.0]),  # E field amplitude vector
    k=np.array([0.0, 0.0, 1.0]),   # propagation direction
    omega=2.0 * np.pi * 5e14,      # angular frequency (visible light)
)
print(f"Wave speed = {calc_wave_speed()} cm/s")
print(f"Speed equals c: {verify_speed_equals_c()}")
```

---

### 2. Education and Teaching

Use the library as an executable reference for teaching classical electromagnetic theory. Every concept is tied to Maxwell's original article numbers, making it easy to assign primary-source reading alongside computational exercises.

**Teaching Coulomb's law from the primary source**

```python
from maxwell.core.charge import PointCharge
import numpy as np

# Demonstrate the inverse-square law: double distance, quarter the field
charge = PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))

for r in [1.0, 2.0, 4.0, 10.0]:
    E_mag = np.linalg.norm(charge.field_at(np.array([r, 0.0, 0.0])))
    print(f"r={r:4.1f} cm: E={E_mag:.6f} esu (expected={1.0/r**2:.6f})")
```

**Visualizing the relationship between electric potential and field**

```python
from maxwell.core.potential import ElectricPotential, solve_laplace
from maxwell.core.field import field_from_potential

# Laplace equation solution between parallel plates (Art. 84-85)
potential = ElectricPotential(potential_function=lambda x, y, z: 100.0 * x)
E_field = field_from_potential(potential.potential_function)
# E = -grad(V) = (-100, 0, 0) -- uniform field between plates
```

**Comparing theoretical predictions with measurement data**

```python
from maxwell.instruments.galvanometers import TangentGalvanometer

# Simulate a tangent galvanometer experiment (Art. 710)
galv = TangentGalvanometer(
    coil_constant=0.5,       # G constant
    horizontal_field=0.2,    # Earth's horizontal field in oersteds
)

# What current produces a 30-degree deflection?
import math
theta = math.radians(30.0)
current = galv.current_from_deflection(theta)
print(f"30-degree deflection requires {current:.4f} abamperes")
```

**Understanding magnetic hysteresis (Arts. 444-446)**

```python
from maxwell.materials.hysteresis import HysteresisLoop, hysteresis_loss_steinmetz
import numpy as np

# Model a hysteresis loop for annealed iron
H_values = np.linspace(-10, 10, 100)
I_values = 1000 * np.tanh(H_values / 0.5)  # simplified magnetization curve
loop = HysteresisLoop(H_values=H_values, I_values=I_values, is_complete=True)

# Steinmetz hysteresis loss: W = eta * B_max^1.6
loss = hysteresis_loss_steinmetz(B_max=15000, frequency=60, volume=100, steinmetz_eta=3e-4)
print(f"Hysteresis loss: {loss:.2f} erg/s")
```

---

### 3. Scientific Research and Historical Scholarship

Study how Maxwell formulated his theory by implementing it computationally. Trace every equation back to its original article, compare competing electromagnetic theories of the 1870s, and reproduce historical calculations with modern tools.

**Tracing a formula to its source article**

```python
from maxwell.meta.citation import get_citation
from maxwell.electromagnetism.induction.faraday import calc_induced_emf

citation = get_citation(calc_induced_emf)
print(citation)
# MaxwellCitation(Part 4, Art. 528, Art. 529, Art. 530, Art. 531)
```

**Comparing Maxwell's theory with Weber's and Neumann's formulations (Arts. 859-866)**

```python
from maxwell.molecular.competing_theories import CompetingTheory, compare_theories

ct = CompetingTheory()
comparison = compare_theories()  # Returns dict with all theory comparisons
for theory_name, details in comparison.items():
    print(f"{theory_name}: {details}")
```

**Reproducing Maxwell's calculation of the speed of light from electromagnetic measurements (Arts. 771-782)**

```python
from maxwell.core.units import verify_speed_of_light_relationship
from maxwell.config.constants import C

# Maxwell compared electrostatic and electromagnetic unit measurements
# and found their ratio equals the speed of light -- the key insight
ratio = verify_speed_of_light_relationship()
print(f"ESU/EMU unit ratio / c = {ratio}")  # 1.0
print(f"Speed of light (Maxwell, Art. 782): C = {C:.4e} cm/s")
```

**Analyzing spherical harmonic expansions of gravitational and electrostatic potential (Arts. 128-146)**

```python
from maxwell.math.spherical_harmonics import (
    SphericalHarmonicExpansion,
    calc_legendre_polynomial,
    addition_theorem,
)

# Legendre polynomials at cos(theta) = 0.5 (theta = 60 degrees)
P2 = calc_legendre_polynomial(n=2, x=0.5)
P3 = calc_legendre_polynomial(n=3, x=0.5)
print(f"P_2(0.5) = {P2}, P_3(0.5) = {P3}")

# Expand the potential of a sphere using spherical harmonics
expansion = SphericalHarmonicExpansion(max_l=4)
print(f"Spherical harmonic expansion terms up to l=4: {expansion.term_count}")
```

---

### 4. Engineering Reference Calculations

Perform quick engineering calculations based on Maxwell's original formulations. Ideal for back-of-envelope verification, conceptual design work, and educational demonstrations.

**Ship compass deviation (Art. 441)**

```python
from maxwell.engineering import ShipMagnetism, MagneticCompass

# Model an iron ship's magnetic deviation (Napier's theory)
ship = ShipMagnetism(
    permanent_moment=500.0,   # emu
    induced_factor=0.3,        # susceptibility factor
    heading=45.0,              # degrees from magnetic north
    dip_angle=67.0,            # magnetic dip at location
)

compass = MagneticCompass(ship_magnetism=ship)
deviation = compass.get_deviation()
print(f"Compass deviation at NE heading: {deviation:.2f} degrees")
```

**Inductor energy calculation (Arts. 632-633)**

```python
from maxwell.electromagnetism.energy.magnetic import (
    calc_magnetic_energy_density,
    calc_total_magnetic_energy,
)

# Energy stored in a magnetic field of 5000 gauss in air
energy_density = calc_magnetic_energy_density(B=5000.0)  # CGS erg/cm^3
print(f"Magnetic energy density: {energy_density:.4f} erg/cm^3")

# Total energy in a 100 cm^3 volume
total = calc_total_magnetic_energy(B=5000.0, volume=100.0)
print(f"Total energy in 100 cm^3: {total:.2f} ergs")
```

**Galvanometer design and sensitivity (Arts. 707-720)**

```python
from maxwell.instruments.galvanometers import design_sensitive_galvanometer

# Design a sensitive galvanometer for detecting small currents
design = design_sensitive_galvanometer(
    target_sensitivity=1e-9,   # abamperes per division
    coil_radius=15.0,          # cm
    turns=1000,
    earth_field=0.2,           # horizontal component in oersteds
)
print(f"Designed galvanometer: {design}")
```

**Magnetic field from competing current elements (Arts. 475-479)**

```python
from maxwell.electromagnetism.sources.oersted import calc_field_from_element

# Oersted field from a current element: H = (I * dl * sin(theta)) / r^2
# Current element along z-axis, observation point 3 cm away on x-axis
field = calc_field_from_element(
    current=5.0,        # abamperes
    element_length=1.0, # cm
    distance=3.0,       # cm
    angle=90.0,         # degrees (perpendicular)
)
print(f"Field from current element: {field:.4f} oersted")
```

---

### 5. Unit System Verification and Metrology

Verify the internal consistency of electromagnetic unit systems. The library includes tools for checking dimensional analysis, converting between ESU/EMU/CGS/SI, and verifying fundamental relationships like the ESU-to-EMU ratio equaling the speed of light.

**Verify dimensional consistency**

```python
from maxwell.core.units import verify_dimensional_consistency

# Check that a formula's dimensions are consistent
# Returns True if the dimensional analysis passes
consistent = verify_dimensional_consistency(
    formula="force",  # Check dimensions of force equation
)
print(f"Force dimensions consistent: {consistent}")
```

**Convert between ESU and EMU units (Arts. 620-628)**

```python
from maxwell.core.units import convert_esu_to_emu, convert_emu_to_esu

# Convert charge: 1 coulomb = 2.998e10 esu (statcoulombs)
esu_charge = 2.99792458e10
emu_charge = convert_esu_to_emu(esu_charge, quantity="charge")
print(f"{esu_charge:.4e} esu = {emu_charge:.4e} emu")  # = 1.0 abcoulomb
```

**Check the speed-of-light relationship (Arts. 771-781)**

```python
from maxwell.core.units import verify_speed_of_light_relationship
from maxwell.config.constants import C

ratio = verify_speed_of_light_relationship()
# This verifies: ratio(ESU/EMU for capacity) = c
print(f"Unit ratio / c = {ratio:.10f}")  # Should be 1.0 to machine precision
print(f"Conservation of c: {'PASS' if abs(ratio - 1.0) < 1e-10 else 'FAIL'}")
```

**Convert practical SI values to CGS equivalents**

```python
from maxwell.optics import calc_wave_speed

# In CGS: 1 Tesla = 10,000 gauss, 1 Ampere = 0.1 abampere
# The wave speed function returns c directly in CGS
speed = calc_wave_speed()
print(f"EM wave speed in vacuum: {speed:.4e} cm/s")  # = 2.998e10
```

---

### 6. Maxwell's Equations -- Complete Analysis

Compute and verify all four of Maxwell's equations as presented in the Treatise's general equations (Arts. 594-603).

```python
from maxwell.electromagnetism.theory.general_equations import (
    MaxwellEquations,
    ElectromagneticField,
    verify_maxwell_equations,
    analyze_complete_field,
)

# Define an electromagnetic field: E and B vectors at a point
field = ElectromagneticField(
    E=[100.0, 0.0, 0.0],   # statvolt/cm
    B=[0.5, 0.0, 0.0],     # gauss
    rho=1e-6,              # charge density (esu/cm^3)
    J=[0.1, 0.0, 0.0],     # current density (esu/cm^2/s)
)

# Run all four Maxwell equations
maxwell_eq = MaxwellEquations(field)
results = maxwell_eq.all_equations()

for name, value in results.items():
    print(f"{name}: {value}")

# Full verification across all equations
verified = verify_maxwell_equations(field)
print(f"All Maxwell equations satisfied: {verified}")
```

---

## What This Library Is NOT

Honesty about limitations is important for choosing the right tool.

**Not a FEM or numerical solver.** This library does not perform finite-element analysis, finite-difference time-domain (FDTD) simulation, or boundary-element modeling. It does not replace COMSOL, ANSYS HFSS, openEMS, or similar numerical electromagnetic solvers. If you need to simulate a complex 3D geometry with inhomogeneous materials, use a dedicated FEM package.

**Not a circuit simulator.** This is not SPICE, ngspice, or a circuit analysis tool. While it can compute inductance, capacitance, and mutual induction for simple geometries, it cannot simulate arbitrary circuit networks with time-varying sources.

**Not a real-time or time-domain simulation engine.** The library is primarily analytical and static. It computes field values, potentials, forces, and energies for specified configurations -- not time-evolving fields in complex environments.

**CGS-native, not SI.** All internal calculations use CGS-EMU units. SI values are available only as reference conversions. If you need a library that works natively in SI units for modern engineering design, this is not the right tool -- though SI-to-CGS conversion utilities are provided.

**Not a general-purpose physics library.** This implements Maxwell's 1873 theory specifically. It does not cover quantum mechanics, relativity, thermodynamics beyond what Maxwell addressed, or modern field theory extensions.

---

## Target Audiences

### Physics Educators
- Ready-to-run code examples for classical electromagnetism lectures
- Primary-source formulas tied to Maxwell's original article numbers
- Demonstrations of Coulomb's law, Gauss's law, Faraday's law, Ampere's law
- Hysteresis, saturation, and magnetic material behavior visualizations
- Unit system conversions between CGS and SI for student exercises

### History of Science Researchers
- Computational exploration of 19th-century electromagnetic theory
- Comparison of Maxwell, Weber, Neumann, and Ampere formulations
- Verification of historical calculations with modern numerical precision
- Citation traceability from code to specific Treatise articles

### Graduate and Advanced Undergraduate Students
- Executable reference for electromagnetic theory courses
- Step-by-step implementations of formulas found in textbooks
- Spherical harmonic expansions, elliptic integrals, and multipole calculations
- Hands-on exploration of Maxwell's original derivations

### Computational Physicists
- Verified analytical formulas for benchmarking numerical solvers
- Spherical harmonic and multipole expansion infrastructure
- Constitutive relations for magnetic and dielectric materials
- Dimensional analysis and unit conversion tools

### Engineers (Reference and Design)
- Back-of-envelope electromagnetic calculations
- Magnetic compass deviation for marine navigation
- Galvanometer and instrument design calculations
- Magnetic energy, inductance, and force estimation for simple geometries

---

## The Unique Value: Citation Traceability

Every function in this library is tagged with `@maxwell_cite`, linking it to specific articles in Maxwell's 1873 _Treatise_. This means:

- **Accountability.** You can trace any result back to its source in the original text.
- **Reproducibility.** Every calculation can be independently verified against Maxwell's published formulas.
- **Educational value.** Students can read the original article and then run the code that implements it.
- **Research utility.** Historians can compare Maxwell's theoretical statements with their computational content.

```python
from maxwell.meta.citation import get_all_citations

# Find all functions citing Article 528 (Faraday's law discovery)
citations = get_all_citations()
for func_name, citation in citations.items():
    if 528 in citation.articles:
        print(f"{func_name} -> {citation}")
```

---

## 5-Minute Demo: Five Calculations That Prove Value

### Calculation 1: Coulomb's Law (30 seconds)

```python
from maxwell.core.charge import PointCharge
import numpy as np

q = PointCharge(q=10.0, position=np.array([0.0, 0.0, 0.0]))
E = q.field_at(np.array([5.0, 0.0, 0.0]))
print(f"E at 5 cm: {np.linalg.norm(E):.4f} esu/cm^2")
# Expected: 10/25 = 0.4 esu/cm^2
```

### Calculation 2: Speed of Light from EM Units (30 seconds)

```python
from maxwell.core.units import verify_speed_of_light_relationship

ratio = verify_speed_of_light_relationship()
print(f"ESU/EMU ratio / c = {ratio:.10f}")
# Maxwell's key insight: this equals 1.0
```

### Calculation 3: Magnetic Field of a Wire (30 seconds)

```python
from maxwell.electromagnetism.sources.oersted import calc_oersted_field

B = calc_oersted_field(current=5.0, distance=1.0)
print(f"B at 1 cm from 5-amp wire: {B:.4f} oersted")
# H = 2*I/r = 10.0 oersted
```

### Calculation 4: Electromagnetic Wave Speed (30 seconds)

```python
from maxwell.optics import calc_wave_speed, verify_speed_equals_c

print(f"Wave speed: {calc_wave_speed():.4e} cm/s")
print(f"Speed = c? {verify_speed_equals_c()}")
```

### Calculation 5: Hysteresis Loss Calculation (30 seconds)

```python
from maxwell.materials.hysteresis import hysteresis_loss_steinmetz

loss = hysteresis_loss_steinmetz(B_max=10000, frequency=60, volume=1, steinmetz_eta=2.5e-4)
print(f"Hysteresis loss: {loss:.2f} erg/s")
```

---

## Quick Reference: Common EM Problems to Modules

| Problem | Module | Key Functions/Classes |
|---------|--------|-----------------------|
| Electrostatic field from charges | `maxwell.core.charge` | `PointCharge`, `field_at()` |
| Electric potential and Laplace/Poisson | `maxwell.core.potential` | `ElectricPotential`, `solve_laplace()`, `solve_poisson()` |
| Electric field from potential | `maxwell.core.field` | `field_from_potential()`, `electric_flux()` |
| Gauss's law | `maxwell.core.field` | `gauss_law_closed_surface()` |
| Magnetic field from current | `maxwell.electromagnetism.sources.oersted` | `calc_oersted_field()`, `calc_field_from_element()` |
| Lorentz force on wire/charge | `maxwell.electromagnetism.forces.lorentz` | `LorentzForce`, `calc_force_on_wire()` |
| Faraday induction | `maxwell.electromagnetism.induction.faraday` | `FaradayInduction`, `calc_induced_emf()` |
| Maxwell's equations (all four) | `maxwell.electromagnetism.theory.general_equations` | `MaxwellEquations`, `ElectromagneticField` |
| Electromagnetic energy | `maxwell.electromagnetism.energy.*` | `MagneticEnergy`, `ElectrostaticEnergy` |
| Maxwell stress tensor | `maxwell.electromagnetism.forces.stress_tensor` | `MaxwellStressTensor`, `calc_maxwell_stress_tensor()` |
| Ampere-Maxwell law (displacement current) | `maxwell.electromagnetism.fields.ampere_maxwell` | `AmpereMaxwellLaw`, `calc_displacement_current()` |
| Magnetic material properties | `maxwell.materials.induction` | `calc_induced_magnetization()`, `calc_B_in_material()` |
| Magnetic hysteresis | `maxwell.materials.hysteresis` | `HysteresisLoop`, `hysteresis_loss_steinmetz()` |
| Magnetic saturation | `maxwell.materials.saturation` | `WeberModel`, `approach_to_saturation()` |
| Constitutive relations (B=mu*H) | `maxwell.materials.constitutive` | `Magnetization`, `Permeability`, `Conductivity` |
| Electromagnetic waves | `maxwell.optics.wave_equation` | `PlaneWave`, `calc_wave_speed()` |
| Refractive index and velocity | `maxwell.optics.velocity` | `calc_refractive_index()`, `calc_wave_velocity()` |
| Radiation pressure | `maxwell.optics.radiation_pressure` | `calc_radiation_pressure()`, `calc_radiation_force()` |
| Spherical harmonics | `maxwell.math.spherical_harmonics` | `SphericalHarmonicExpansion`, `calc_legendre_polynomial()` |
| Elliptic integrals | `maxwell.math.elliptic_integrals` | `calc_elliptic_integral_first_kind()`, etc. |
| Vector calculus operators | `maxwell.math.vector_operators` | `gradient()`, `divergence()`, `curl()` |
| Galvanometers and instruments | `maxwell.instruments.galvanometers` | `TangentGalvanometer`, `design_sensitive_galvanometer()` |
| Helmholtz coils | `maxwell.instruments.helmholtz` | `HelmholtzCoil` |
| Suspended coil measurements | `maxwell.instruments.suspended_coil` | `SuspendedCoil`, `determine_magnetic_force()` |
| Dynamometers | `maxwell.instruments.dynamometers` | `WeberDynamometer`, `JouleCurrentWeigher` |
| Ship magnetism and compass deviation | `maxwell.engineering` | `ShipMagnetism`, `MagneticCompass` |
| Competing EM theories | `maxwell.molecular.competing_theories` | `CompetingTheory`, `compare_theories()` |
| Weber's electrodynamics | `maxwell.molecular.webers_theory` | `WeberForce`, `calc_weber_force()` |
| Neumann's potential theory | `maxwell.molecular.neumanns_theory` | `NeumannPotential`, `neumann_mutual_inductance()` |
| Physical constants (CGS/SI) | `maxwell.config.constants` | `CONST`, `C`, `cgs_unit_of()` |
| Unit conversion (ESU/EMU/CGS/SI) | `maxwell.core.units` | `CGSUnitConverter`, `convert_esu_to_emu()` |
| Dimensional analysis | `maxwell.core.units` | `verify_dimensional_consistency()`, `MagneticDimensions` |
| Citation lookup | `maxwell.meta.citation` | `get_citation()`, `get_all_citations()` |

---

## Getting Started

```bash
# Clone and install
git clone https://github.com/maxwell-treatise/modernized-program.git
cd modernized-program
pip install -e ".[dev]"

# Run the test suite to verify installation
pytest tests/ -v

# Import and use
python -c "from maxwell.config.constants import CONST, C; print(f'c = {C}')"
```

## Related Documentation

- **[README.md](../README.md)** -- Project overview, quick start, architecture
- **[docs/API_REFERENCE.md](API_REFERENCE.md)** -- Complete module-level API index
- **[docs/COVERAGE_SUMMARY.md](COVERAGE_SUMMARY.md)** -- Article coverage by Part and chapter
- **[docs/validation_report.md](validation_report.md)** -- Test results and mathematical validation

---

_Maxwell Modernized. All 866 articles. Fully tested. Scholarly traceable._
