# Command: verify-conservation

## Description

Verifies conservation laws (energy, charge, momentum, flux) in electromagnetic implementations. These fundamental laws must be satisfied for physical correctness.

## Functionality

### Conservation Laws Verified

1. **Energy Conservation**
   - Poynting theorem: ∂u/∂t + ∇·S = -J·E
   - Electrostatic: U = (1/8π)∫E² dV = (1/2)∫ρV dV
   - Magnetostatic: U = (1/8π)∫B·H dV = (1/2)LI²
   - Circuit: P_in = P_dissipated + dU/dt

2. **Charge Conservation**
   - Continuity equation: ∂ρ/∂t + ∇·J = 0
   - Integral form: dQ/dt = -∮J·dA
   - Kirchhoff's current law

3. **Momentum Conservation**
   - Maxwell stress tensor: T_ij
   - Force: F = ∮T·dA
   - Field momentum: p_field = (1/4πc)∫E×B dV

4. **Flux Conservation**
   - Gauss's law: ∮D·dA = 4πQ
   - No magnetic monopoles: ∮B·dA = 0
   - Divergence theorem

### Verification Methods

- **Direct Integration**: Numerically integrate conservation equations
- **Energy Balance**: Track all energy flows
- **Boundary Flux**: Compute surface integrals
- **Time Evolution**: Monitor conservation over time

## Usage

```python
from maxwell.quality.conservation import ConservationVerifier

# Create verifier
verifier = ConservationVerifier()

# Verify energy conservation in FDTD simulation
energy_result = verifier.verify_energy_conservation(
    simulation=fdtd_sim,
    initial_energy=U_0,
    tolerance=1e-3
)

# Verify charge conservation
charge_result = verifier.verify_charge_conservation(
    rho_func=charge_density,
    J_func=current_density,
    volume=test_volume,
    tolerance=1e-6
)

# Verify Poynting theorem
poynting_result = verifier.verify_poynting_theorem(
    E_field=E_func,
    H_field=H_func,
    J_source=J_func,
    volume=test_volume,
    time_span=[0, 1e-9]
)

# Check Maxwell stress tensor
stress_result = verifier.verify_stress_tensor(
    E_field=E_func,
    B_field=B_func,
    surface=closed_surface,
    expected_force=analytical_force
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `simulation` | Simulation | Simulation to verify |
| `tolerance` | float | Conservation tolerance |
| `volume` | Volume | Integration volume |
| `surface` | Surface | Boundary surface |
| `time_span` | array | Time range for check |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `result` | ConservationResult | Pass/fail with details |
| `balance` | dict | Input/output/dissipated/stored |
| `error` | float | Conservation error |

## Energy Conservation Checklist

### Electrostatics
- [ ] U = (1/8π)∫E² dV computed correctly
- [ ] U = (1/2)∑qᵢVᵢ for discrete charges
- [ ] Work to assemble charges = stored energy
- [ ] Force from -∇U matches direct calculation

### Magnetostatics
- [ ] U = (1/8π)∫B·H dV computed correctly
- [ ] U = (1/2)LI² for inductors
- [ ] Mutual energy: U = MI₁I₂
- [ ] Force from energy gradient correct

### Time-Varying Fields
- [ ] Poynting vector S = (c/4π)E×H
- [ ] Energy density u = (1/8π)(E² + B²)
- [ ] ∂u/∂t + ∇·S = -J·E satisfied
- [ ] Radiated power = ∮S·dA

### Circuits
- [ ] P_in = VI from sources
- [ ] P_dissipated = I²R in resistors
- [ ] dU/dt in reactive elements
- [ ] P_in = P_dissipated + dU/dt

## Output Format

```
============================================================
CONSERVATION LAW VERIFICATION
============================================================

ENERGY CONSERVATION
-------------------
Initial energy:     1.000000e-05 erg
Final energy:       9.998500e-06 erg
Energy input:       0.000000e+00 erg
Energy dissipated:  1.500000e-09 erg

Balance: U_final + U_dissipated - U_initial = 0
Error: 1.5e-10 erg (relative: 1.5e-5)
Status: PASS (tolerance: 1.0e-3)

CHARGE CONSERVATION
-------------------
Initial charge:     1.000000e-10 statcoulomb
Final charge:       1.000000e-10 statcoulomb
Net flux:           0.000000e+00 statcoulomb/s

dQ/dt + ∮J·dA = 0
Error: 0.0e+00 (relative: 0.0)
Status: PASS

============================================================
SUMMARY: 4/4 conservation laws verified
============================================================
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 85-86 | Electrostatic energy |
| 242 | Joule heating |
| 551 | Electrokinetic energy |
| 630-640 | Field energy |
| 641-646 | Maxwell stress tensor |

## Related Commands

- `validate-physics` - Full physics validation
- `check-units` - Unit consistency
- `test-analytical` - Analytical benchmarks
