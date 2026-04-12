# Command: current-flow

## Description

Analyzes steady current distributions and conduction phenomena from Maxwell's Part II (Arts. 230-300). Implements Ohm's law in 3D, current density, continuity equation, and network theory.

## Functionality

### Current Fundamentals (Layer 13)
1. **Electric Current** (Arts. 230-235)
   - I = dQ/dt (definition)
   - Current density: J = ρv = σE
   - Continuity equation: ∂ρ/∂t + ∇ · J = 0

2. **Ohm's Law** (Art. 241)
   - 1D: V = IR
   - 3D: J = σE (constitutive relation)
   - Anisotropic: J = σ̿ · E (tensor conductivity)

3. **Current Flow Geometry** (Arts. 235-240)
   - Tubes of flow
   - Current sheets
   - Stream functions

### Conduction Physics (Layer 14-16)
- **Joule Heating** (Art. 242): H = I²Rt = ∫ J · E dV
- **Contact EMF** (Arts. 246-248): Volta potential at junctions
- **Thermoelectric Effects** (Arts. 249-254): Seebeck, Peltier, Thomson

### Network Analysis (Layer 20)
- Kirchhoff's laws from first principles
- Series and parallel combinations
- Bridge circuits (Wheatstone, Thomson)
- Minimum heat principle (variational)

### Transmission Lines (Layer 26)
- Telegraph equation: ∂²V/∂x² = RC ∂V/∂t + LC ∂²V/∂t²
- Characteristic impedance
- Reflection and transmission

## Usage

```python
from maxwell.physics.electrokinematics import CurrentFlow
from maxwell.circuits import CircuitGraph, Resistor, Battery
from maxwell.materials import ConductorDatabase

# Simple conductor
copper = ConductorDatabase.get('copper')  # σ = 5.96e17 s⁻¹ (CGS)
E_field = VectorField([0.01, 0, 0])  # statvolt/cm

J = CurrentFlow.compute_current_density(
    conductivity=copper.conductivity,
    E_field=E_field
)

# Anisotropic conduction (stratified material)
sigma_tensor = [
    [1e17, 0, 0],
    [0, 1e15, 0],
    [0, 0, 1e17]
]
J_aniso = CurrentFlow.anisotropic_conduction(sigma_tensor, E_field)

# Build circuit graph
circuit = CircuitGraph()
circuit.add_node('A', 'B', 'C', 'D')
circuit.add_component(Resistor('R1', 'A', 'B', 100))  # ohms
circuit.add_component(Resistor('R2', 'B', 'C', 200))
circuit.add_component(Battery('V1', 'C', 'D', 1.5))  # volts
circuit.add_component(Resistor('R3', 'D', 'A', 150))

# Solve network
solution = CurrentFlow.solve_network(
    circuit=circuit,
    method='nodal_analysis'  # or 'mesh', 'modified_nodal'
)

# Telegraph cable equation
cable_params = {
    'R': 10,  # ohm/km
    'L': 1e-3,  # H/km
    'C': 1e-6,  # F/km
    'G': 1e-6  # S/km
}
V_xt = CurrentFlow.solve_telegraph_equation(
    params=cable_params,
    boundary_conditions={'x=0': 'step(1V)', 'x=L': 'open'},
    time_span=[0, 1e-3]  # seconds
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `conductivity` | float or ndarray | σ in s⁻¹ (CGS) or tensor |
| `E_field` | VectorField | Electric field (statvolt/cm) |
| `circuit` | CircuitGraph | Network topology |
| `sources` | list | Voltage and current sources |
| `method` | str | 'nodal', 'mesh', 'modified_nodal', 'numerical' |
| `temperature` | float | Temperature coefficient (optional) |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `J` | VectorField | Current density (statampere/cm²) |
| `I_branch` | dict | Branch currents in network |
| `V_node` | dict | Node potentials |
| `power_dissipation` | float | Total I²R loss (erg/s) |
| `metadata` | dict | Citations, validation, convergence info |

## Implementation Notes

- CGS conductivity: 1 s⁻¹ ≈ 1.11e-12 S/m
- Temperature dependence: σ(T) = σ₀[1 + α(T - T₀)]
- Thermoelectric effects require coupled heat equation
- Telegraph equation uses Crank-Nicolson for stability

## Validation

- Ohm's law verified against known resistances
- Kirchhoff's laws satisfied to numerical precision
- Joule heating matches ∫J·E dV
- Telegraph equation matches analytical step response

## Maxwell Article References

| Article | Content |
|---------|---------|
| 230-235 | Electric current definition |
| 241 | Ohm's law |
| 242 | Joule heating |
| 243-245 | Thermal-electrical analogy |
| 246-248 | Contact electromotive force |
| 249-254 | Thermoelectric effects |
| 269-286 | Network theory |
| 297-300 | Telegraph equation |

## Related Commands

- `electrostatic-field` - For E-field from charge
- `electrolysis-model` - For ionic conduction
- `circuit-analysis` - For lumped network analysis

## Error Handling

- Warns if current density exceeds material limits
- Raises `NetworkError` if circuit is ill-posed
- Validates energy conservation in steady state
