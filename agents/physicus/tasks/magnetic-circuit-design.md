# Task: magnetic-circuit-design

## Description

Designs and analyzes magnetic circuits including permanent magnets, electromagnets, and magnetic shielding from Maxwell's Part III (Arts. 407-446). This task computes magnetic flux distributions, inductances, and forces.

## Workflow Steps

### 1. Magnetic Circuit Definition
- Specify core geometry and dimensions
- Define material properties (μ, B-H curve)
- Identify coil locations and turns
- Set excitation (current or permanent magnet)

### 2. Magnetic Circuit Equations
- **Magnetomotive Force (MMF)**: ℱ = NI (ampere-turns)
- **Reluctance**: ℛ = l/(μA)
- **Hopkinson's Law**: ℱ = Φℛ (magnetic Ohm's law)
- **Flux**: Φ = BA

### 3. Solution Methods
- **Magnetic Circuit**: Lumped reluctance network
- **Analytical**: For simple geometries (toroid, solenoid)
- **Numerical**: FEM for complex 3D fields

### 4. Performance Metrics
- Inductance L = N²/ℛ
- Force F = (B²A)/(8π) (Maxwell stress)
- Energy stored W = (1/2)LI²
- Leakage flux fraction

## Requirements

**Input:**
- `circuit`: dict - Magnetic core geometry
- `material`: MagneticMaterial - B-H curve or μ
- `excitation`: dict - Coil (N, I) or permanent magnet
- `method`: str - 'circuit', 'analytical', 'numerical'

**Output:**
- `flux_density`: VectorField - B(x,y,z)
- `field_intensity`: VectorField - H(x,y,z)
- `inductance`: float - Self and mutual inductances
- `force`: VectorField - Magnetic forces
- `energy`: float - Stored magnetic energy

## Implementation

```python
from maxwell.tasks.magnetics import MagneticCircuitDesigner
from maxwell.materials import MagneticMaterial

# Problem 1: Toroidal inductor
toroid = {
    'geometry': 'toroid',
    'major_radius': 5,  # cm
    'minor_radius': 1,  # cm
    'material': MagneticMaterial(name='ferrite', mu=2000),
    'coil': {'turns': 100, 'current': 0.1}  # statamperes
}

designer = MagneticCircuitDesigner(toroid)
result = designer.solve(method='analytical')

# Returns:
# - B field in core (uniform for thin toroid)
# - Inductance L = μN²A/(2πr)
# - Stored energy

# Problem 2: Horseshoe electromagnet with keeper
horseshoe = {
    'geometry': 'horseshoe',
    'core_dimensions': {...},
    'air_gap': 0.5,  # cm
    'keeper': True,
    'material': MagneticMaterial(name='soft_iron', B_H_curve=...),
    'coil': {'turns': 500, 'current': 1.0}
}

designer_hs = MagneticCircuitDesigner(horseshoe)
result_hs = designer_hs.solve(method='circuit')

# Lumped reluctance model:
# ℛ_total = ℛ_core + ℛ_gap + ℛ_keeper
# Φ = NI / ℛ_total
# B = Φ / A

# Problem 3: Permanent magnet circuit
pm_circuit = {
    'magnet': {
        'material': 'alnico_5',
        'dimensions': [2, 2, 5],  # cm
        'magnetization_direction': [0, 0, 1],
        'remanence': 12800,  # gauss
        'coercivity': 640  # oersted
    },
    'flux_concentrator': {
        'material': 'soft_iron',
        'geometry': {...}
    },
    'working_gap': 1.0  # cm
}

result_pm = MagneticCircuitDesigner(pm_circuit).solve(method='numerical')
# Returns: B in gap, operating point on demagnetization curve

# Force calculation
force = result_pm.compute_force(
    method='maxwell_stress_tensor',  # or 'energy_derivative', 'virtual_work'
    surface='keeper_surface'
)

# Inductance matrix for multi-coil system
L_matrix = result.compute_inductance_matrix(
    coils=['primary', 'secondary'],
    frequency=0  # DC
)
```

## Example Problems

### 1. Solenoid Actuator
```python
# Plunger solenoid with spring return
# Compute force vs. position, pull-in current
```

### 2. Magnetic Shielding
```python
# Mu-metal shield for sensitive equipment
# Compute shielding factor B_out/B_in
```

### 3. Halbach Array
```python
# Permanent magnet array for field enhancement
# Optimize magnet orientations
```

## Validation Criteria

- [ ] ∇ · B = 0 (no monopoles)
- [ ] ∮ H · dl = 4πNI/c (Ampère's law)
- [ ] B = μH in linear materials
- [ ] Energy: W = (1/8π) ∫B·H dV
- [ ] Force from energy derivative matches stress tensor

## Maxwell Article References

| Article | Content |
|---------|---------|
| 407-408 | Solenoids and magnetic circuits |
| 409-411 | Magnetic shells |
| 427-428 | Induced magnetization |
| 431-440 | Shape-dependent magnetization |
| 442-446 | Weber's theory, hysteresis |

## Related Tasks

- `em-induction-computation` - Time-varying effects
- `electromagnetic-force` - Force calculations
- `thermal-analysis` - Coil heating
