# JAX Adapter — Maxwell Modernized

> GPU/TPU-accelerated, auto-differentiable implementations of Maxwell's 1873 Treatise computations.

## Overview

The `maxwell.jax` package provides JAX-compatible versions of core Maxwell Treatise calculations, enabling:

- **JIT compilation** via `jax.jit` — compiled XLA kernels for repeated evaluations
- **Automatic differentiation** via `jax.grad` — compute field gradients, sensitivities, optimization
- **Vectorized evaluation** via `jax.vmap` — batch over thousands of field points simultaneously
- **GPU/TPU execution** — deploy on accelerators without code changes

All computations preserve **CGS-EMU units** and are **citation-traceable** to Maxwell's original articles.

## Package Structure

```
maxwell/jax/
├── __init__.py                  # x64 config, package exports
├── _compat.py                   # Pytree registration, safe arithmetic
├── _scipy_special.py            # Pure JAX wrappers: lpmv, legendre, sph_harm_y
├── _elliptic.py                 # AGM-based elliptic integrals (no scipy)
├── core/
│   ├── __init__.py
│   ├── charge.py                # PointChargeJAX, multi-charge systems
│   └── magnet.py                # MagneticPoleJAX, MagnetJAX (force, torque, mutual action)
├── electromagnetism/
│   ├── __init__.py
│   ├── induction.py             # FaradayInductionJAX (Lenz's law, EMF)
│   ├── equations.py             # MaxwellEquationsJAX (all 9 equations)
│   ├── forces.py                # LorentzForceJAX, MaxwellStressTensorJAX
│   ├── ampere_maxwell.py        # DisplacementCurrentJAX, AmpereMaxwellLawJAX
│   ├── field.py                 # ElectricFieldJAX (flux, Gauss's law, EMF)
│   ├── energy.py                # ElectrostaticEnergyJAX, CapacitorEnergyJAX
│   └── electrokinetic.py        # ElectrokineticEnergyJAX, CoupledCircuitEnergyJAX
│   └── ohms_law.py              # OhmsLawJAX, ResistanceJAX, ConductivityJAX, PowerDissipationJAX
└── math/
    ├── __init__.py
    └── spherical_harmonics.py   # SphericalHarmonicExpansionJAX
```

## Quick Start

```python
import jax
from maxwell.jax.core.charge import PointChargeJAX

# Enable float64 for CGS precision
jax.config.update("jax_enable_x64", True)

# Single charge
charge = PointChargeJAX(q=1.0, position=jax.numpy.array([0.0, 0.0, 0.0]))
E = charge.field_at(jax.numpy.array([5.0, 0.0, 0.0]))
# E = [0.04, 0.0, 0.0] statvolt/cm

# Batched evaluation over 1000 points
points = jax.numpy.linspace(-10, 10, 1000).reshape(-1, 3)
E_batched = charge.field_at_batched(points)

# JIT-compiled
from jax import jit, vmap, grad

@jit
def field_on_grid(q, pos, point):
    c = PointChargeJAX(q=q, position=pos)
    return c.field_at(point)
```

## Pytree Registration

All JAX dataclasses use the `@jax_tree` decorator for pytree registration:

```python
from maxwell.jax._compat import jax_tree
from dataclasses import dataclass

@jax_tree
@dataclass
class MyClass:
    field: jax.Array
    value: float

# Now works with jax.jit, jax.grad, jax.vmap
```

## Safe Arithmetic

The `_compat` module provides JAX-safe alternatives to division, sqrt, and norm:

```python
from maxwell.jax._compat import safe_div, safe_sqrt, safe_norm

# Safe division: returns 0 when denominator is zero
result = safe_div(numerator, denominator, safe_default=0.0)

# Safe sqrt: returns 0 for negative inputs
result = safe_sqrt(x, safe_default=0.0)

# Safe norm: returns floor value for zero vectors
result = safe_norm(x, axis=-1, safe_default=1e-30)
```

## Elliptic Integrals

Pure JAX AGM-based implementation — no scipy dependency:

```python
from maxwell.jax._elliptic import ellipk_jax, ellipe_jax

# Complete elliptic integrals
K = ellipk_jax(0.5)  # ~1.854
E = ellipe_jax(0.5)  # ~1.351

# JIT and vmap compatible
@jit
def compute_k(m):
    return ellipk_jax(m)
```

## Faraday Induction

```python
from maxwell.jax.electromagnetism.induction import FaradayInductionJAX

coil = FaradayInductionJAX(num_turns=100, resistance=50.0)

# Magnetic flux
flux = coil.magnetic_flux(B_field, area=10.0)

# Induced EMF (Lenz's law)
emf = coil.induced_emf(flux_change_rate=10000.0)

# Full analysis
from maxwell.jax.electromagnetism.induction import analyze_faraday_induction_jax
result = analyze_faraday_induction_jax(
    B_initial=jnp.zeros(3),
    B_final=jnp.array([0, 0, 1000]),
    loop_area=10.0,
    time_interval=0.5,
    num_turns=100,
)
```

## Maxwell's Equations

```python
from maxwell.jax.electromagnetism.equations import MaxwellEquationsJAX

eq = MaxwellEquationsJAX(permittivity=1.0, permeability=1.0, conductivity=0.0)

# Gauss's law
div_D = eq.gauss_law_electric(D_field, dx=0.1, rho=0.0)

# Faraday's law
curl_E = eq.equation_A_faraday(dB_dt)

# Verify all equations
report = verify_maxwell_equations_jax()
```

## Spherical Harmonics

```python
from maxwell.jax.math.spherical_harmonics import (
    SphericalHarmonicExpansionJAX,
    legendre_batched,
    addition_theorem_jax,
)

# Legendre polynomials (batched)
x = jnp.linspace(-1, 1, 100)
P3 = legendre_batched(3, x)

# Expansion
expansion = SphericalHarmonicExpansionJAX(max_l=8)
expansion.compute_coefficients(f_theta, theta_grid)
reconstructed = expansion.reconstruct(theta, phi)
```

## Lorentz Force & Stress Tensor

```python
from maxwell.jax.electromagnetism.forces import (
    LorentzForceJAX,
    MaxwellStressTensorJAX,
    force_on_wire_jax,
    force_on_charge_jax,
    stress_tensor_jax,
)

# Lorentz force on wire
force = LorentzForceJAX(
    current=1.0,
    length=jnp.array([10.0, 0.0, 0.0]),
    B_field=jnp.array([0.0, 0.0, 1000.0]),
)
F = force.force_vector  # [0, -10000, 0] dynes

# Force on moving charge
F = force_on_charge_jax(
    charge=1.0,
    velocity=jnp.array([1e8, 0.0, 0.0]),
    B_field=jnp.array([0.0, 0.0, 100.0]),
)

# Maxwell stress tensor
tensor = MaxwellStressTensorJAX(
    E_field=jnp.array([100.0, 0.0, 0.0]),
    H_field=jnp.array([0.0, 50.0, 0.0]),
)
T = tensor.stress_tensor()  # 3x3 tensor
P = tensor.electromagnetic_pressure  # scalar pressure
```

## Electric Field

```python
from maxwell.jax.electromagnetism.field import (
    ElectricFieldJAX,
    electric_flux_jax,
    gauss_law_closed_surface_jax,
    field_from_potential_jax,
    superposition_field_jax,
)
from maxwell.jax.core.charge import PointChargeJAX

# Electric field from a point charge
charge = PointChargeJAX(q=1.0, position=jnp.array([0.0, 0.0, 0.0]))
E = ElectricFieldJAX.from_point_charge(charge, jnp.array([5.0, 0.0, 0.0]))
# E.value = [0.04, 0.0, 0.0] statvolt/cm
# E.magnitude = 0.04 statvolt/cm

# Superposition: field from multiple charges
charges = [
    PointChargeJAX(q=1.0, position=jnp.array([1.0, 0.0, 0.0])),
    PointChargeJAX(q=-1.0, position=jnp.array([-1.0, 0.0, 0.0])),
]
E_resultant = ElectricFieldJAX.superposition(charges, jnp.array([0.0, 1.0, 0.0]))

# Electric flux through a surface (Gauss's law)
flux = electric_flux_jax(
    field_value=jnp.array([100.0, 0.0, 0.0]),
    surface_normal=jnp.array([1.0, 0.0, 0.0]),
    area=25.0,
)  # = 2500.0

# Gauss's law: flux through closed surface = 4*pi*Q
expected_flux = gauss_law_closed_surface_jax(total_charge=1.0)
# = 4 * pi = 12.566...

# Field from potential via auto-differentiation
V_func = lambda r: 1.0 / jnp.linalg.norm(r)  # V = q/r for q=1
E_from_V = field_from_potential_jax(V_func, jnp.array([1.0, 0.0, 0.0]))
# E = -grad(V) = [1.0, 0.0, 0.0] at r=1
```

## Permanent Magnets

```python
from maxwell.jax.core.magnet import (
    MagneticPoleJAX,
    MagnetJAX,
    pole_force_jax,
    mutual_action_jax,
    torque_on_magnet_jax,
)

# Single magnetic pole (Art. 371)
pole = MagneticPoleJAX(strength=10.0, position=jnp.array([0.0, 0.0, 0.0]))
H = pole.field_at(jnp.array([5.0, 0.0, 0.0]))
# H = [0.4, 0.0, 0.0] gauss

# Permanent magnet with N and S poles (Arts. 372-376)
magnet = MagnetJAX(
    pole_strength=10.0,
    north_position=jnp.array([1.0, 0.0, 0.0]),
    south_position=jnp.array([-1.0, 0.0, 0.0]),
)
# Properties
moment = magnet.magnetic_moment       # [20.0, 0.0, 0.0] emu
length = magnet.magnetic_length        # 2.0 cm
axis = magnet.magnetic_axis            # [1.0, 0.0, 0.0]

# Field at a point
H = magnet.field_at(jnp.array([0.0, 5.0, 0.0]))

# Force on magnet in non-uniform field
F = magnet.force_in_field(
    H_north=jnp.array([100.0, 0.0, 0.0]),
    H_south=jnp.array([90.0, 0.0, 0.0]),
)

# Torque in uniform field
tau = magnet.torque_in_uniform_field(jnp.array([0.0, 100.0, 0.0]))

# Potential energy in field
W = magnet.potential_energy_in_field(jnp.array([100.0, 0.0, 0.0]))
# W = -m dot H = -2000.0 erg

# Mutual action between two magnets (Art. 392)
interaction = mutual_action_jax(
    m1_strength=10.0, m1_north=jnp.array([1.0, 0.0, 0.0]), m1_south=jnp.array([0.0, 0.0, 0.0]),
    m2_strength=5.0,  m2_north=jnp.array([5.0, 0.0, 0.0]), m2_south=jnp.array([4.0, 0.0, 0.0]),
)
# interaction['force_on_2'], interaction['torque_on_2'], interaction['potential_energy']

# JIT-compiled torque
from jax import jit
torque_fn = jit(MagnetJAX._torque_jit)
tau = torque_fn(10.0, jnp.array([1.0, 0.0, 0.0]), jnp.array([-1.0, 0.0, 0.0]),
                jnp.array([0.0, 100.0, 0.0]))
```

## Electrostatic Energy

```python
from maxwell.jax.electromagnetism.energy import (
    ElectrostaticEnergyJAX,
    CapacitorEnergyJAX,
    calc_electrostatic_energy_density_jax,
    calc_capacitor_energy_jax,
    analyze_electrostatic_energy_jax,
)

# Energy density in electric field (Art. 630)
E_field = jnp.array([100.0, 0.0, 0.0])  # statvolt/cm
u = calc_electrostatic_energy_density_jax(E_field, permittivity=1.0)
# u = E^2 / (8*pi) = 10000 / (8*pi) erg/cm^3

# Using the class interface
energy = ElectrostaticEnergyJAX(E_field=jnp.array([100.0, 0.0, 0.0]))
density = energy.energy_density             # erg/cm^3
D = energy.D_field                           # D = eps * E
total = energy.total_energy(volume=1.0)     # erg, for V = 1 cm^3

# From E and D fields directly (general dielectric)
energy_general = ElectrostaticEnergyJAX.from_E_and_D(
    E=jnp.array([100.0, 0.0, 0.0]),
    D=jnp.array([200.0, 0.0, 0.0]),
)

# JIT-compiled
from jax import jit
density_jit = jit(ElectrostaticEnergyJAX._density_jit)
u_fast = density_jit(jnp.array([100.0, 0.0, 0.0]), 1.0)

# Capacitor energy (Art. 631)
cap = CapacitorEnergyJAX(capacitance=10.0)  # C = 10 cm (CGS)
U1 = cap.from_voltage(voltage=5.0)           # U = 0.5 * 10 * 25 = 125 erg
U2 = cap.from_charge(charge=50.0)            # U = 2500 / 20 = 125 erg
U3 = cap.from_QV(charge=50.0, voltage=5.0)  # U = 0.5 * 50 * 5 = 125 erg

# Standalone function with auto-selection
U = calc_capacitor_energy_jax(capacitance=10.0, voltage=5.0)

# Comprehensive analysis
result = analyze_electrostatic_energy_jax(
    E_field=jnp.array([100.0, 0.0, 0.0]),
    permittivity=1.0,
    volume=1.0,
    capacitance=10.0,
    voltage=5.0,
)
# result['energy_density'], result['total_energy'],
# result['capacitor_energy'], result['energy_ratio']

# Auto-differentiation: d(energy)/d(E_x)
from jax import grad
dU_dEx = grad(lambda Ex: ElectrostaticEnergyJAX._density_jit(
    jnp.array([Ex, 0.0, 0.0]), 1.0
))(100.0)
```

## Electrokinetic Energy

```python
from maxwell.jax.electromagnetism.electrokinetic import (
    ElectrokineticEnergyJAX,
    CoupledCircuitEnergyJAX,
    calc_single_circuit_energy_jax,
    calc_two_circuit_energy_jax,
    calc_coupled_circuits_energy_jax,
    calc_mutual_inductance_energy_jax,
    calc_coupling_coefficient_jax,
    analyze_electrokinetic_energy_jax,
    verify_coupled_circuits_energy_jax,
)

# Single circuit energy T = (1/2) * L * I^2 (Art. 635)
U = calc_single_circuit_energy_jax(inductance=100.0, current=5.0)
# U = 0.5 * 100 * 25 = 1250.0 erg

# Using the class interface
ek = ElectrokineticEnergyJAX.from_single_circuit(inductance=100.0, current=5.0)
U = ek.energy  # 1250.0 erg

# Two coupled circuits with mutual inductance (Arts. 636-637)
T = calc_two_circuit_energy_jax(L1=100.0, L2=200.0, M=30.0, I1=5.0, I2=3.0)
# T = 0.5*100*25 + 0.5*200*9 + 30*5*3 = 1250 + 900 + 450 = 2600.0 erg

# Coupled circuits via inductance matrix
L_matrix = jnp.array([[100.0, 30.0], [30.0, 200.0]])
I_vec = jnp.array([5.0, 3.0])
T_matrix = calc_coupled_circuits_energy_jax(L_matrix, I_vec)
# T = (1/2) * I^T . L . I = 2600.0 erg

# Using CoupledCircuitEnergyJAX for matrix-based analysis
coupled = CoupledCircuitEnergyJAX(inductance_matrix=L_matrix)
T_total = coupled.from_currents(I_vec)               # total energy
T_self = coupled.self_energies(I_vec)                 # per-circuit self energy
T_mutual = coupled.mutual_energy(I_vec)               # mutual energy contribution
K = coupled.coupling_matrix(I_vec)                    # pairwise coupling coefficients

# Coupling coefficient k = M / sqrt(L1 * L2) (Art. 638)
k = calc_coupling_coefficient_jax(M=30.0, L1=100.0, L2=200.0)
# k = 30 / sqrt(20000) = 0.212...

# Mutual inductance energy contribution
T_mutual = calc_mutual_inductance_energy_jax(M=30.0, I1=5.0, I2=3.0)
# T_mutual = 30 * 5 * 3 = 450.0 erg

# Comprehensive analysis
result = analyze_electrokinetic_energy_jax(
    L1=100.0, L2=200.0, M=30.0, I1=5.0, I2=3.0,
)
# result['two_circuit_energy'], result['coupling_coefficient'],
# result['self_energy_1'], result['self_energy_2'], result['mutual_energy']

# Verify consistency between scalar and matrix formulations
verification = verify_coupled_circuits_energy_jax(
    L1=100.0, L2=200.0, M=30.0, I1=5.0, I2=3.0,
)
# verification['verified'] = True (difference < 1e-10)

# Auto-differentiation: dT/dI1
from jax import grad
dT_dI1 = grad(lambda I1: calc_two_circuit_energy_jax(100.0, 200.0, 30.0, I1, 3.0))(5.0)
# = L1*I1 + M*I2 = 100*5 + 30*3 = 590.0
```

## Ohm's Law & Resistance

```python
from maxwell.jax.electromagnetism.ohms_law import (
    OhmsLawJAX,
    ResistanceJAX,
    ConductivityJAX,
    PowerDissipationJAX,
    calc_ohms_law_jax,
    calc_series_resistance_jax,
    calc_parallel_resistance_jax,
    calc_conductivity_jax,
    calc_power_dissipation_jax,
    analyze_ohms_law_jax,
)

# Ohm's Law: V = I * R (Art. 230)
ohm = OhmsLawJAX(voltage=10.0, current=2.0, resistance=5.0)
V = ohm.from_current_and_resistance(current=2.0, resistance=5.0)  # V = 10.0
I = ohm.from_voltage_and_resistance(voltage=10.0, resistance=5.0)  # I = 2.0
R = ohm.from_voltage_and_current(voltage=10.0, current=2.0)        # R = 5.0

# Standalone function
V = calc_ohms_law_jax(current=2.0, resistance=5.0)  # V = 10.0

# Series and parallel resistance (Arts. 273-284)
R_series = calc_series_resistance_jax([10.0, 20.0, 30.0])  # 60.0 ohms
R_parallel = calc_parallel_resistance_jax([10.0, 20.0, 30.0])  # 5.454... ohms

# Using the class interface
res = ResistanceJAX(values=[10.0, 20.0, 30.0])
R_s = res.series()        # 60.0
R_p = res.parallel()      # 5.454...
R_temp = res.temperature(  # temperature-dependent resistance
    reference_resistance=10.0,
    temperature_coefficient=0.004,
    temperature_change=50.0,
)

# Conductivity: sigma = 1/rho (Arts. 285-288)
cond = ConductivityJAX(conductivity=5.96e7)  # copper, S/m
rho = cond.resistivity                        # 1.678e-8 ohm*m
sigma = ConductivityJAX.from_resistivity(1.678e-8).conductivity  # round-trip

# Standalone
sigma = calc_conductivity_jax(resistivity=1.678e-8)

# Joule heating: P = I^2 * R = V^2 / R = V * I (Art. 230)
power = PowerDissipationJAX(current=2.0, resistance=5.0)
P1 = power.from_current()   # P = I^2 * R = 20.0 W
P2 = power.from_voltage()   # P = V^2 / R = 20.0 W
P3 = power.from_VI()        # P = V * I = 20.0 W

# Standalone
P = calc_power_dissipation_jax(current=2.0, resistance=5.0)

# Comprehensive analysis
result = analyze_ohms_law_jax(
    voltage=10.0, current=2.0, resistance=5.0,
)
# result['calculated_voltage'], result['calculated_current'],
# result['calculated_resistance'], result['power_dissipation']

# Auto-differentiation: dP/dI = 2*I*R
from jax import grad
dP_dI = grad(lambda I: calc_power_dissipation_jax(current=I, resistance=5.0))(2.0)
# = 2 * I * R = 20.0
```

## Automatic Differentiation

```python
from jax import grad
from maxwell.jax.core.charge import PointChargeJAX

def potential_at_q(q):
    c = PointChargeJAX(q=q, position=jnp.zeros(3))
    return c.potential_at(jnp.array([1.0, 0.0, 0.0]))

# dV/dq at q=1
dVdq = grad(potential_at_q)(1.0)
```

## Compatibility Notes

- **Float64 required**: CGS unit ratios need ~15 digits. Always `jax.config.update("jax_enable_x64", True)`.
- **scipy.special gaps**: `jax.scipy.special.sph_harm_y` works for array inputs. The `_scipy_special` module provides pure JAX `lpmv_jax` and `legendre_jax` implementations.
- **Control flow**: All loops use `jax.lax.fori_loop` or `jax.lax.while_loop` for JIT traceability.
- **Dataclass fields**: All pytree-registered dataclass fields are JAX-traced by default.

## Test Suite

533 tests cover:
- Pytree registration (3 tests)
- PointChargeJAX correctness (9 tests)
- Multi-charge systems (3 tests)
- Auto-differentiation (2 tests)
- Elliptic integrals (8 tests)
- JAX special functions (7 tests)
- Faraday induction (16 tests)
- Maxwell equations (11 tests)
- Spherical harmonics (14 tests)
- Lorentz force (13 tests)
- Maxwell stress tensor (13 tests)
- Ampere-Maxwell law (20 tests)
- Safe arithmetic (5 tests)
- Electric field (14 tests): magnitude, direction, superposition, EMF, flux, Gauss's law
- Field from potential (12 tests): gradient via auto-diff, line integral
- Standalone functions (8 tests): tension, flux, gauss_law, superposition
- MagnetJAX (23 tests): MagneticPole, magnet properties, force, torque, mutual action
- Electrostatic energy (60 tests): energy density, capacitor energy, E.D dot, isotropy, auto-diff
- Electrokinetic energy (61 tests): single circuit, coupled circuits, mutual inductance, coupling coefficient, verification, auto-diff
- Ohm's law & resistance (93 tests): Ohm's law V=IR, series/parallel/temperature resistance, conductivity, power dissipation, Joule heating, auto-diff

```bash
pytest tests/test_jax_adapter.py -v
```

## Citation Traceability

All JAX implementations maintain the `@maxwell_cite` decorator from the NumPy versions. Each function can be traced back to its source article via `get_citation(func)`.

| JAX Class | Articles |
|-----------|----------|
| PointChargeJAX | Arts. 29-30 |
| MagneticPoleJAX | Art. 371 |
| MagnetJAX | Arts. 372-376, 392 |
| FaradayInductionJAX | Arts. 528-531, 542 |
| MaxwellEquationsJAX | Arts. 594-603 |
| SphericalHarmonicExpansionJAX | Arts. 128-146 |
| LorentzForceJAX | Arts. 490-492 |
| MaxwellStressTensorJAX | Arts. 641-646 |
| DisplacementCurrentJAX | Arts. 606-607 |
| AmpereMaxwellLawJAX | Arts. 606-607 |
| ElectricFieldJAX | Arts. 44-49, 68-76 |
| ElectrostaticEnergyJAX | Arts. 630-631 |
| CapacitorEnergyJAX | Arts. 630-631 |
| MagneticEnergyJAX | Arts. 632-633 |
| InductorEnergyJAX | Arts. 632-633 |
| ElectrokineticEnergyJAX | Arts. 634-638 |
| CoupledCircuitEnergyJAX | Arts. 634-638 |
| OhmsLawJAX | Arts. 230-234 |
| ResistanceJAX | Arts. 273-284, 359-362 |
| ConductivityJAX | Arts. 285-288 |
| PowerDissipationJAX | Art. 230 |
| ellipk_jax, ellipe_jax | Arts. 149-152 |
