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
│   └── network_solver.py        # NetworkSolverJAX, KirchhoffJAX, WheatstoneBridgeJAX, ReciprocityVerifierJAX
│   └── conduction_3d.py         # Conduction3DJAX, SpreadingResistanceJAX, EffectiveConductivityJAX
│   └── electrolysis.py          # FaradayLawsJAX, IonTransportJAX, PolarizationJAX, ElectrolysisCellJAX
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

## Network Analysis & Kirchhoff's Laws

```python
from maxwell.jax.electromagnetism.network_solver import (
    NetworkSolverJAX,
    KirchhoffJAX,
    WheatstoneBridgeJAX,
    ReciprocityVerifierJAX,
    kirchhoff_junction_rule_jax,
    kirchhoff_loop_rule_jax,
    analyze_network_jax,
    wheatstone_bridge_balance_jax,
    wheatstone_bridge_sensitivity_jax,
    reciprocity_theorem_jax,
)
```

### Network Solver — Conductance Matrix Method (Arts. 276-280)

For a network of linear conductors, node potentials are found by solving `G @ V = I`,
where `G` is the conductance (admittance) matrix.

```python
# Simple 3-node network:
#   Node 0 (ground) --g=0.1-- Node 1 --g=0.2-- Node 2
#   Current injection: 1.0A into Node 1, -1.0A out of Node 2
solver = NetworkSolverJAX.from_edges(
    n_nodes=3,
    edges=[
        (0, 1, 0.1),  # conductance between nodes 0 and 1
        (1, 2, 0.2),  # conductance between nodes 1 and 2
    ],
    current_sources=[
        (1, 1.0),   # inject 1A at node 1
        (2, -1.0),  # extract 1A at node 2
    ],
    reference_node=0,
)

# Node potentials (V_0 = 0 by definition)
V = solver.node_potentials
# V = [0.0, 15.0, 5.0] volts

# Branch currents: I[i,j] = -G[i,j] * (V[i] - V[j])
I_branch = solver.branch_currents
# I_branch[0,1] = 1.5A (from node 0 to node 1)
# I_branch[1,2] = 2.0A (from node 1 to node 2)

# Branch power dissipation: P[i,j] = I[i,j]^2 / |G[i,j]|
P_branch = solver.branch_power

# Total power dissipated (each branch counted once)
P_total = solver.total_power
```

### Effective Resistance Between Nodes

```python
# Effective resistance between nodes 1 and 2
# (inject 1A at node 1, extract at node 2, measure voltage difference)
R_eff = solver.effective_resistance(1, 2)
# R_eff = V_1 - V_2 = 10.0 ohms (for 0.2S conductance)

# Verify Kirchhoff's current law: G @ V == I
result = solver.verify_kirchhoff()
# result['kcl_satisfied'] = True
# result['max_residual'] < 1e-10
```

### Wheatstone Bridge (Arts. 281-284)

```python
# Balanced bridge: R1*R4 = R2*R3
bridge = WheatstoneBridgeJAX(R1=100.0, R2=200.0, R3=300.0, R4=600.0)

# Balance check
balanced = bridge.is_balanced          # True
error = bridge.balance_error            # 0.0 (R1*R4 - R2*R3)
R4_for_balance = bridge.balance_point_R4  # R4 = R2*R3/R1

# Thevenin equivalent seen by galvanometer
V_th = bridge.thevenin_voltage(V_battery=10.0)
R_th = bridge.thevenin_resistance()

# Galvanometer current with 50 ohm meter resistance
I_galv = bridge.galvanometer_current(V_battery=10.0, R_galvanometer=50.0)

# Comprehensive balance analysis
result = wheatstone_bridge_balance_jax(
    R1=100.0, R2=200.0, R3=300.0, R4=600.0,
)
# result['is_balanced'], result['ratio_1_2'], result['ratio_3_4']

# Sensitivity analysis (unbalanced bridge)
sensitivity = wheatstone_bridge_sensitivity_jax(
    R1=100.0, R2=200.0, R3=300.0, R4=601.0,  # slightly unbalanced
    V_battery=10.0,
    R_galvanometer=50.0,
)
# sensitivity['galvanometer_current'], sensitivity['thevenin_voltage']
```

### Reciprocity Theorem (Arts. 277-278)

Maxwell's reciprocity theorem: for any linear passive network, the transfer
resistance between two port pairs is symmetric (R_12 = R_21).

```python
# Using the same conductance matrix from the 3-node network above
verifier = ReciprocityVerifierJAX(
    conductance_matrix=solver.conductance_matrix,
    reference_node=0,
)

# Transfer resistance: inject at port_a, measure at port_b
R_transfer = verifier.transfer_resistance(port_a=1, port_b=2)

# Verify reciprocity between two port pairs
result = verifier.verify(
    port1_a=1, port1_b=2,
    port2_a=2, port2_b=1,
)
# result['R_12'], result['R_21'], result['is_reciprocal'] = True

# Standalone reciprocity verification
result = reciprocity_theorem_jax(
    conductance_matrix=solver.conductance_matrix,
    port1=(1, 0),
    port2=(2, 0),
    reference_node=0,
)
```

### Kirchhoff's Laws — Junction and Loop Rules

```python
# Junction rule: sum of currents at a node = 0 (Arts. 273-274)
junction = kirchhoff_junction_rule_jax(
    currents=jnp.array([1.0, -0.6, -0.4])
)
# junction['sum'] = 0.0, junction['satisfied'] = True

# Loop rule: sum of voltage drops around a closed loop = 0 (Art. 275)
loop = kirchhoff_loop_rule_jax(
    voltage_drops=jnp.array([5.0, -3.0, -2.0])
)
# loop['sum'] = 0.0, loop['satisfied'] = True
```

### Comprehensive Network Analysis

```python
# Full analysis from edge list
result = analyze_network_jax(
    edges=[(0, 1, 0.1), (1, 2, 0.2), (0, 2, 0.05)],
    current_sources=[(1, 1.0), (2, -1.0)],
    reference_node=0,
)
# result['node_potentials'], result['branch_currents'],
# result['total_power'], result['kirchhoff_verification'],
# result['effective_resistances']
```

## 3D Conduction & Effective Conductivity

```python
from maxwell.jax.electromagnetism.conduction_3d import (
    Conduction3DJAX,
    SpreadingResistanceJAX,
    EffectiveConductivityJAX,
    ohms_law_3d_jax,
    conduction_power_density_jax,
    spherical_spreading_resistance_jax,
    hemispherical_spreading_resistance_jax,
    circular_contact_resistance_jax,
    maxwell_garnett_conductivity_jax,
    effective_conductivity_series_jax,
    effective_conductivity_parallel_jax,
    verify_conduction_3d_jax,
    analyze_conduction_jax,
)
```

### Scalar & Tensor Conductivity (Arts. 285-288)

```python
# Isotropic conduction: J = sigma * E
cond = Conduction3DJAX(conductivity=5.96e7)  # copper, S/m
E = jnp.array([1.0, 0.0, 0.0])
J = cond.current_density(E)
# J = [5.96e7, 0.0, 0.0] A/m^2

# Recover E from J
E_recovered = cond.electric_field(J)
# E_recovered = [1.0, 0.0, 0.0] (round-trip verified)

# Power density: P = J . E
P = cond.power_density(E)
# P = 5.96e7 W/m^3

# Create from resistivity: sigma = 1/rho
cond2 = Conduction3DJAX.from_resistivity(jnp.array(1.678e-8))  # copper resistivity

# Anisotropic conduction: J = sigma @ E (3x3 tensor conductivity)
sigma_tensor = jnp.array([
    [5.0, 1.0, 0.0],
    [1.0, 3.0, 0.0],
    [0.0, 0.0, 2.0],
])
cond_aniso = Conduction3DJAX(conductivity=sigma_tensor)
cond_aniso.is_anisotropic  # True

J_aniso = cond_aniso.current_density(jnp.array([1.0, 0.0, 0.0]))
# J = [5.0, 1.0, 0.0] (tensor cross-coupling)

# Standalone 3D Ohm's law
J = ohms_law_3d_jax(jnp.array([1.0, 0.0, 0.0]), sigma=5.96e7)

# Verification: J = sigma*E, E = J/sigma, P = J.E consistency
result = verify_conduction_3d_jax(E=jnp.array([1.0, 0.0, 0.0]), sigma=1.0)
# result['verified'] = True (round-trip error < 1e-10)
```

### Spreading Resistance (Arts. 297-309)

```python
# Spreading resistance for various electrode geometries
sr = SpreadingResistanceJAX(conductivity=0.01)  # soil, S/m

# Spherical electrode in infinite medium: R = 1/(4*pi*sigma*r)
R_sphere = sr.spherical_surface(radius=0.5)
# R = 1/(4*pi*0.01*0.5) = 15.915... ohms

# Hemispherical contact on surface: R = 1/(2*pi*sigma*r)
R_hemi = sr.hemispherical_surface(radius=0.5)
# R = 1/(2*pi*0.01*0.5) = 31.831... ohms (2x spherical)

# Circular disk contact: R = 1/(4*sigma*r)
R_disk = sr.circular_contact(radius=0.5)
# R = 1/(4*0.01*0.5) = 50.0 ohms

# Cylindrical wire contact
R_wire = sr.cylindrical_wire(radius=0.001, length=1.0)
# R = ln(2*l/r) / (2*pi*sigma*l)

# Standalone functions
R = spherical_spreading_resistance_jax(sigma=0.01, radius=0.5)
R = hemispherical_spreading_resistance_jax(sigma=0.01, radius=0.5)
R = circular_contact_resistance_jax(sigma=0.01, radius=0.5)

# Comprehensive analysis with spreading resistance
result = analyze_conduction_jax(
    E=jnp.array([1.0, 0.0, 0.0]),
    sigma=0.01,
    geometry={'type': 'sphere', 'radius': 0.5},
)
# result['current_density'], result['power_density'],
# result['spreading_resistance'], result['is_anisotropic']
```

### Effective Conductivity Mixing Models (Arts. 310-324)

```python
# Maxwell-Garnett effective medium theory
ec = EffectiveConductivityJAX(
    sigma_matrix=1.0,
    sigma_inclusion=100.0,
    volume_fraction=0.3,
)

# Series mixing (lower bound): sigma_eff = 1 / (f/sigma2 + (1-f)/sigma1)
sigma_series = ec.series_mix()
# sigma_eff = 1 / (0.3/100 + 0.7/1.0) = 1.424...

# Parallel mixing (upper bound): sigma_eff = (1-f)*sigma1 + f*sigma2
sigma_parallel = ec.parallel_mix()
# sigma_eff = 0.7*1.0 + 0.3*100 = 30.7

# Maxwell-Garnett: for dilute spherical inclusions
sigma_mg = ec.maxwell_garnett()
# sigma_eff = sigma_m * (sigma_i + 2*sigma_m - 2*f*(sigma_m - sigma_i)) /
#                      (sigma_i + 2*sigma_m + f*(sigma_m - sigma_i))

# Brickell/Bruggeman symmetric model (higher concentration)
sigma_brickell = ec.brickell()
# Analytical solution: sigma_eff = (1/4)*(B + sqrt(B^2 + 8*sigma1*sigma2))

# Bounds check: series < MG < MG < parallel
# sigma_series < sigma_mg < sigma_parallel

# Standalone mixing functions
sigma_eff = maxwell_garnett_conductivity_jax(sigma_m=1.0, sigma_i=100.0, vol_frac=0.3)
sigma_eff = effective_conductivity_series_jax(sigma1=1.0, sigma2=100.0, f=0.3)
sigma_eff = effective_conductivity_parallel_jax(sigma1=1.0, sigma2=100.0, f=0.3)

# Auto-differentiation: d(sigma_eff)/d(vol_frac)
from jax import grad
d_sigma_df = grad(lambda f: EffectiveConductivityJAX._maxwell_garnett_jit(1.0, 100.0, f))(0.3)
```

## Electrolysis & Ion Transport

```python
from maxwell.jax.electromagnetism.electrolysis import (
    FaradayLawsJAX,
    IonTransportJAX,
    PolarizationJAX,
    ElectrolysisCellJAX,
    FARADAY_CONSTANT_JAX,
    faraday_first_law_jax,
    faraday_second_law_jax,
    electrochemical_equivalent_jax,
    ion_migration_velocity_jax,
    transference_number_jax,
    polarization_emf_jax,
    decomposition_voltage_jax,
    verify_electrolysis_jax,
)
```

### Faraday's Laws of Electrolysis (Arts. 249-252)

```python
# Faraday's first law: m = I * t * Z (Arts. 249-250)
m = faraday_first_law_jax(
    current=1.0,        # 1 abA
    time=100.0,         # 100 s
    Z=1.118e-3,         # electrochemical equivalent of Ag, g/abC
)
# m = 0.1118 g of silver deposited

# Faraday's second law: m = I*t*M/(n*F) (Arts. 251-252)
m = faraday_second_law_jax(
    current=1.0,
    time=100.0,
    molar_mass=107.87,  # Ag molar mass, g/mol
    valence=1.0,
)
# m = I*t*M/(n*F) = 100*107.87/96485.33 = 0.1118 g

# Using the class interface
faraday = FaradayLawsJAX()

# Electrochemical equivalent: Z = M/(n*F)
Z_ag = faraday.electrochemical_equivalent(molar_mass=107.87, valence=1.0)
Z_cu = faraday.electrochemical_equivalent(molar_mass=63.55, valence=2.0)
# Z_Cu < Z_Ag -- copper requires 2 electrons per atom

# Mass from charge directly
m = faraday.mass_from_charge(
    charge=100.0,       # 100 abcoulombs
    molar_mass=107.87,
    valence=1.0,
)

# Current required to deposit a target mass in given time
I_needed = faraday.current_for_mass_time(
    mass=1.0,           # 1 gram
    time=3600.0,        # 1 hour
    molar_mass=107.87,
    valence=1.0,
)

# Charge required for a target mass
Q_needed = faraday.required_charge(
    mass=1.0,
    molar_mass=107.87,
    valence=1.0,
)

# Standalone
Z = electrochemical_equivalent_jax(molar_mass=107.87, valence=1.0)
```

### Ion Transport & Conductivity (Arts. 257-263)

```python
# Ion migration velocity: v = u * z * E
v = ion_migration_velocity_jax(
    ion_mobility=5.0e-4,    # cm^2/(abV*s)
    electric_field=100.0,    # abV/cm
    charge_number=1.0,
)
# v = 0.05 cm/s

# Multi-ion transport system
transport = IonTransportJAX(
    ion_mobilities=jnp.array([5.0e-4, 8.0e-4]),  # cation, anion
    ion_charges=jnp.array([1.0, -1.0]),
)

# Migration velocities for both ions
v_ions = transport.migration_velocity(electric_field=100.0)
# v = [0.05, -0.08] cm/s (opposite directions)

# Electrolyte conductivity: sigma = F * sum(c*|z|*u)
sigma = transport.electrolyte_conductivity(
    concentrations=jnp.array([1.0e-6, 1.0e-6]),  # mol/cm^3
)

# Transference numbers: t_i = |z_i|*u_i / sum(|z_j|*u_j)
t = transport.transference_numbers()
# t['t_i'] -- fraction of current carried by each ion
# t['total'] -- total conductivity contribution

# Standalone transference numbers
t_numbers = transference_number_jax(
    lambda_cation=54.0,   # Cu2+ limiting ionic conductivity
    lambda_anion=80.0,    # SO4^2- limiting ionic conductivity
)
# t['t_cation'], t['t_anion'], t['Lambda_0']
```

### Polarization & Butler-Volmer (Arts. 253-256)

```python
# Polarization with activation overpotential (Butler-Volmer)
pol = PolarizationJAX(
    reversible_emf=1.23e8,         # water electrolysis, abvolts
    exchange_current_density=1e-6, # abA/cm^2
    transfer_coefficient=0.5,
    temperature=298.15,
)

# Activation overpotential via Butler-Volmer:
# eta = (RT/F) * asinh(j/(2*j0)) / alpha
eta = pol.activation_overpotential(current_density=1e-3)
# eta > 0 -- extra voltage needed beyond reversible EMF

# Concentration overpotential (mass transport limitation)
eta_conc = pol.concentration_overpotential(
    bulk_conc=1.0e-3,
    surface_conc=5.0e-4,
    diffusion_coeff=1.0e-5,
    diffusion_thickness=1.0e-3,
    current_density=1e-3,
    charge_number=1.0,
)

# Total decomposition voltage:
# E_decomp = E_rev + eta_a + |eta_c| + IR
V_decomp = pol.decomposition_voltage(
    anode_overpotential=0.4e8,
    cathode_overpotential=-0.1e8,
    ohmic_drop=0.05e8,
)
# V_decomp = E_rev + 0.4e8 + 0.1e8 + 0.05e8

# Total polarization EMF: E_rev + activation overpotential
E_total = pol.total_polarization_emf(current_density=1e-3)

# Standalone functions
E_pol = polarization_emf_jax(
    reversible_potential=1.23e8,
    current_density=1e-3,
    exchange_current_density=1e-6,
    transfer_coefficient=0.5,
    temperature=298.15,
)

V_decomp = decomposition_voltage_jax(
    reversible_emf=1.23e8,
    anode_overpotential=0.4e8,
    cathode_overpotential=-0.1e8,
    ohmic_drop=0.05e8,
)
```

### Complete Electrolysis Cell (Arts. 249-263)

```python
# Full cell model for silver electrolysis
cell = ElectrolysisCellJAX(
    electrode_area=10.0,            # cm^2
    electrode_spacing=2.0,          # cm
    electrolyte_conductivity=0.1,   # abmho/cm
    molar_mass=107.87,              # Ag, g/mol
    valence=1.0,
    reversible_emf=0.8e8,           # abvolts
)

# Cell resistance: R = d / (sigma * A)
R = cell.cell_resistance()
# R = 2.0 / (0.1 * 10.0) = 2.0 abohms

# Mass deposited at given current over time
m = cell.mass_deposited(current=1.0, time=100.0)
# m = I*t*M/(n*F) grams of silver

# Required voltage (includes IR + overpotential)
V_req = cell.required_voltage(current=1.0)
# V_req = E_rev + I*R + eta_activation

# Energy cost per gram
E_per_g = cell.energy_per_gram(current=1.0)
# erg per gram of deposited silver

# Comprehensive analysis
result = cell.analyze(current=1.0, time=100.0)
# result['mass_deposited'], result['charge_passed'],
# result['cell_resistance'], result['ir_drop'],
# result['overpotential'], result['required_voltage'],
# result['energy_consumed'], result['energy_per_gram'],
# result['power']

# Auto-differentiation: d(mass)/d(current)
from jax import grad
dm_dI = grad(lambda I: cell.mass_deposited(I, 100.0))(1.0)
# = t*M/(n*F) -- mass sensitivity to current

# Verification
result = verify_electrolysis_jax()
# result['verified'] = True
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

767 tests cover:
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
- Network analysis & Kirchhoff's laws (79 tests): NetworkSolverJAX conductance matrix, node potentials, branch currents, branch power, effective resistance, KirchhoffJAX KCL/KVL verification, WheatstoneBridgeJAX balance/Thevenin/galvanometer current, ReciprocityVerifierJAX transfer resistance, standalone functions, auto-diff
- 3D conduction & effective conductivity (75 tests): Conduction3DJAX scalar/tensor conductivity, current density, electric field recovery, power density, resistivity conversion, SpreadingResistanceJAX spherical/hemispherical/circular/cylindrical geometries, EffectiveConductivityJAX series/parallel/Maxwell-Garnett/Brickell mixing models, verification round-trip, comprehensive analysis, auto-diff
- Electrolysis & ion transport (80 tests): FaradayLawsJAX mass from charge/current, electrochemical equivalent, required charge/current, IonTransportJAX migration velocity, electrolyte conductivity, transference numbers, limiting current density, PolarizationJAX Butler-Volmer activation overpotential, concentration overpotential, decomposition voltage, total polarization EMF, ElectrolysisCellJAX cell resistance, mass deposited, required voltage, energy per gram, comprehensive analysis, standalone functions (Faraday's laws, polarization EMF, decomposition voltage, ion migration velocity, electrolyte conductivity, Kohlrausch's law, concentration polarization, battery back EMF, transference numbers), verification consistency, auto-diff

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
| NetworkSolverJAX | Arts. 276-280 |
| KirchhoffJAX | Arts. 273-275 |
| WheatstoneBridgeJAX | Arts. 281-284 |
| ReciprocityVerifierJAX | Arts. 277-278 |
| Conduction3DJAX | Arts. 285-288 |
| SpreadingResistanceJAX | Arts. 297-309 |
| EffectiveConductivityJAX | Arts. 310-324 |
| FaradayLawsJAX | Arts. 249-252 |
| IonTransportJAX | Arts. 257-263 |
| PolarizationJAX | Arts. 253-256 |
| ElectrolysisCellJAX | Arts. 249-263 |
