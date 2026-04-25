# Task: current-distribution-analysis

## Description

Analyzes three-dimensional current flow in conductors of arbitrary shape from Maxwell's Part II (Arts. 241-300). This task computes current density distributions, resistance, and power dissipation.

## Workflow Steps

### 1. Conductor Definition
- Specify geometry and dimensions
- Define conductivity σ(x,y,z) - may be tensor
- Identify contact locations (electrodes)
- Set electrode potentials or currents

### 2. Governing Equations
- Ohm's law: J = σE
- Steady state: ∇ · J = 0
- Combined: ∇ · (σ∇V) = 0 (generalized Laplace)

### 3. Solution Methods
- **Analytical**: For simple shapes (wire, plate, cylinder)
- **Conformal Mapping**: For 2D problems
- **Variational**: Thomson's minimum heat theorem
- **Numerical**: FEM for complex 3D geometries

### 4. Post-Processing
- Current density J(x,y,z)
- Total resistance R = V/I
- Power dissipation P = ∫J·E dV
- Current flow visualization

## Requirements

**Input:**
- `conductor`: dict - Geometry and material properties
- `electrodes`: list - Contact locations and BCs
- `conductivity`: float or ndarray - σ (may be anisotropic)
- `method`: str - 'analytical', 'variational', 'numerical'

**Output:**
- `potential`: ScalarField - V(x,y,z)
- `current_density`: VectorField - J(x,y,z)
- `resistance`: float - Total resistance (ohms)
- `power_dissipation`: float - Total I²R loss (erg/s)
- `current_flow_lines`: Streamlines - Tubes of flow

## Implementation

```python
from maxwell.tasks.electrokinematics import CurrentDistributionAnalyzer
from maxwell.materials import ConductorDatabase

# Problem 1: Simple wire
wire = {
    'geometry': 'cylinder',
    'radius': 0.1,  # cm
    'length': 100,  # cm
    'material': 'copper'
}
electrodes = [
    {'location': 'z=0', 'potential': 1.0},  # statvolt
    {'location': 'z=100', 'potential': 0}
]

analyzer = CurrentDistributionAnalyzer(wire, electrodes)
result = analyzer.solve(method='analytical')
# Returns: R = ρL/A, uniform J

# Problem 2: Anisotropic conductor (stratified material)
stratified = {
    'geometry': 'rectangular',
    'dimensions': [10, 10, 1],  # cm
    'conductivity_tensor': [
        [1e17, 0, 0],
        [0, 1e15, 0],
        [0, 0, 1e17]
    ]
}
electrodes = [
    {'location': 'x=0', 'potential': 1.0},
    {'location': 'x=10', 'potential': 0}
]

analyzer_aniso = CurrentDistributionAnalyzer(stratified, electrodes)
result_aniso = analyzer_aniso.solve(method='numerical')
# Current flows preferentially in high-σ direction

# Problem 3: Complex geometry (variational method)
complex_shape = {
    'geometry': 'custom',
    'mesh': 'conductor_geometry.msh',
    'conductivity': 'copper'
}

analyzer_var = CurrentDistributionAnalyzer(complex_shape, electrodes)
result_var = analyzer_var.solve(
    method='variational',
    basis_functions='tetrahedral',
    minimize='joule_heating'
)
# Thomson's theorem: actual current distribution minimizes heat

# Visualization
flow_lines = result.compute_streamlines(
    seed_points=[...],
    density=10
)

# Export for circuit analysis
lumped_model = result.extract_lumped_parameters()
# Returns: R, L (if AC), thermal resistance
```

## Example Problems

### 1. Spreading Resistance
```python
# Point contact on semi-infinite conductor
# R = 1/(2σa) where a is contact radius
```

### 2. Current Crowding
```python
# Conductor with sudden expansion
# Current density peaks at corner
```

### 3. Stratum with Contact Resistance
```python
# Two materials with interface resistance
# Discontinuity in normal J
```

## Validation Criteria

- [ ] ∇ · J = 0 everywhere (steady state)
- [ ] J = σE satisfied at all points
- [ ] Boundary conditions at electrodes
- [ ] Power: P = VI = ∫J·E dV
- [ ] R = V/I from solution matches expected

## Maxwell Article References

| Article | Content |
|---------|---------|
| 241 | Ohm's law |
| 243 | Thermal-electrical analogy |
| 269-275 | 3D current flow theory |
| 283-286 | Tubes of flow, current sheets |
| 297-300 | Variational principles |

## Related Tasks

- `electrostatic-problem-solution` - Mathematical analog
- `thermal-analysis` - Coupled heat equation
- `circuit-analysis` - Lumped element model
