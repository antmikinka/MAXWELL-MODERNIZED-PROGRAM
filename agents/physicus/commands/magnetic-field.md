# Command: magnetic-field

## Description

Computes magnetic fields from arbitrary source distributions based on Maxwell's Part III (Arts. 371-474) and Part IV (Arts. 475-550). Implements magnetic poles, current-generated fields, and the vector potential formulation.

## Functionality

### Magnetic Source Models

1. **Magnetic Poles** (Part III, Arts. 371-384)
   - Unit pole definition: f = m₁m₂/r² (CGS)
   - Magnetic moment: m = pole_strength × length
   - Dipole field: B = (3(m·r̂)r̂ - m)/r³

2. **Current-Generated Fields** (Part IV, Arts. 475-500)
   - Oersted's discovery: current creates circular B-field
   - Biot-Savart law: dB = (I/c) dl × r̂ / r²
   - Ampère's force law between current elements

3. **Vector Potential** (Arts. 405-406, 540-541)
   - B = ∇ × A (solenoidal condition)
   - A = (I/c) ∮ dl/|r - r'| for line currents
   - Gauge freedom: A → A + ∇ψ

### Field Computation Methods

- **Direct Integration**: For simple geometries
- **Multipole Expansion**: For distant fields
- **Vector Potential**: For complex current distributions
- **Magnetic Shell Equivalent**: (Arts. 482-485) Circuit ↔ magnetic shell

### Geometries Supported

- Straight wire (infinite and finite)
- Circular loop (on and off axis)
- Solenoid (finite and infinite)
- Helmholtz coil pair
- Arbitrary wire paths

## Usage

```python
from maxwell.physics.magnetostatics import MagneticField
from maxwell.core.magnet import MagneticDipole
from maxwell.circuits import CurrentLoop, StraightWire, Solenoid

# Magnetic dipole (permanent magnet)
dipole = MagneticDipole(
    moment=[0, 0, 100],  # erg/gauss
    position=[0, 0, 0]
)

B_dipole = MagneticField.from_dipole(
    dipole=dipole,
    observation_point=[10, 0, 0]  # cm
)

# Circular current loop
loop = CurrentLoop(
    radius=5.0,  # cm
    current=1.0,  # statamperes
    center=[0, 0, 0],
    normal=[0, 0, 1]
)

B_loop = MagneticField.from_current_loop(
    loop=loop,
    observation_point=[0, 0, 10]  # on axis
)

# Finite straight wire
wire = StraightWire(
    start=[-10, 0, 0],
    end=[10, 0, 0],
    current=1.0
)

B_wire = MagneticField.from_straight_wire(wire, [0, 5, 0])

# Solenoid
solenoid = Solenoid(
    radius=2.0,  # cm
    length=20.0,  # cm
    turns=1000,
    current=0.1  # statamperes
)

B_solenoid = MagneticField.from_solenoid(
    solenoid=solenoid,
    observation_point=[0, 0, 10],  # on axis, at end
    method='elliptic_integrals'  # or 'numerical', 'approximate'
)

# Helmholtz coil (uniform field region)
helmholtz = MagneticField.helmholtz_configuration(
    radius=10.0,
    turns=100,
    current=1.0,
    separation='optimal'  # equals radius
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | MagneticSource | Dipole, current loop, wire, solenoid |
| `observation_points` | ndarray | Points for field evaluation (cm) |
| `coordinate_system` | str | 'cartesian', 'cylindrical', 'spherical' |
| `method` | str | 'direct', 'multipole', 'vector_potential', 'numerical' |
| `include_vector_potential` | bool | Also compute A field |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `B_field` | VectorField | Magnetic induction (gauss) |
| `H_field` | VectorField | Magnetic field intensity (oersted) |
| `A_field` | VectorField | Vector potential (gauss·cm) |
| `energy_density` | float | U = B²/(8π) (erg/cm³) |
| `metadata` | dict | Citations, validation, method info |

## Implementation Notes

- CGS units: B in gauss, H in oersted
- Vacuum: B = H (CGS), or B = H + 4πM in material
- Factor of c (speed of light) appears in current-generated fields
- Elliptic integrals for exact circular loop solution
- Multipole expansion valid for r >> source size

## Validation

- Dipole field matches analytical formula
- On-axis solenoid field from exact formula
- Helmholtz coil uniformity verified
- Divergence check: ∇ · B = 0

## Maxwell Article References

| Article | Content |
|---------|---------|
| 371-384 | Magnetic dipoles and moments |
| 385-392 | Dipole potentials and interactions |
| 395-400 | Magnetic field definitions |
| 405-406 | Vector potential |
| 475-490 | Oersted, Ampère discoveries |
| 502-504 | Ampère balance experiment |

## Related Commands

- `magnetization-model` - For magnetic materials
- `em-coupling` - For time-varying fields
- `electrostatic-field` - Analogous static problem

## Error Handling

- Warns near singularities (wire locations)
- Raises `MagneticError` for unphysical configurations
- Validates ∇ · B = 0 numerically
