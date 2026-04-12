# Command: em-coupling

## Description

Analyzes electromagnetic interactions and coupling between electric and magnetic phenomena from Maxwell's Part IV (Arts. 475-600). Implements electromagnetic force, induction, and the fundamental coupling mechanisms.

## Functionality

### Electromagnetic Force (Layer 43-46)

1. **Oersted's Discovery** (Arts. 475-479)
   - Current-carrying wire deflects compass
   - Circular magnetic field around wire
   - Right-hand rule

2. **Ampère's Force Law** (Arts. 498-515)
   - Force between current elements
   - Parallel currents attract
   - Antiparallel currents repel
   - F = (I₁I₂/c²) ∮∮ (dl₁·dl₂)/r²

3. **Lorentz Force** (Arts. 490-492)
   - F = q(E + v/c × B)
   - Force on current: F = (I/c) ∫ dl × B
   - Motor principle

### Electromagnetic Induction (Layer 47-51)

4. **Faraday's Law** (Arts. 528-545)
   - EMF = -(1/c) dΦ/dt
   - Φ = ∫ B · dA (magnetic flux)
   - Lenz's law: direction opposes change

5. **Self and Mutual Inductance** (Arts. 546-570)
   - Self: EMF = -L dI/dt
   - Mutual: EMF₂ = -M dI₁/dt
   - Reciprocity: M₁₂ = M₂₁

6. **Vector Potential Formulation** (Arts. 540-541)
   - EMF = -(1/c) d/dt ∫ A · dl
   - A is electrokinetic momentum

### Energy and Dynamics (Layer 52-56)

7. **Electrokinetic Energy** (Arts. 551-567)
   - T = (1/2) Σ L_ij I_i I_j
   - Lagrangian formulation
   - Generalized forces

8. **Field Energy** (Arts. 630-640)
   - U = (1/8π) ∫ (E² + B²) dV
   - Energy localization in field

## Usage

```python
from maxwell.physics.electromagnetism import EMCoupling
from maxwell.circuits import CurrentLoop, Solenoid
from maxwell.core import VectorField

# Force between parallel wires
F_per_length = EMCoupling.ampere_force_parallel_wires(
    I1=1.0,  # statamperes
    I2=1.0,
    separation=1.0,  # cm
    length=100  # cm
)
# Attractive force in dynes

# Force on current in magnetic field
wire = StraightWire(start=[0,0,0], end=[10,0,0], current=1.0)
B_field = VectorField([0, 0, 1000])  # gauss

F = EMCoupling.lorentz_force_on_wire(
    wire=wire,
    B_field=B_field
)

# Mutual inductance between coils
coil1 = CurrentLoop(radius=5, current=1, center=[0,0,0])
coil2 = CurrentLoop(radius=5, current=0, center=[0,0,10])

M = EMCoupling.mutual_inductance(
    coil1=coil1,
    coil2=coil2,
    method='neumann_formula'  # or 'elliptic_integrals', 'numerical'
)

# Self-inductance of solenoid
solenoid = Solenoid(radius=2, length=20, turns=1000)

L = EMCoupling.self_inductance(
    solenoid=solenoid,
    include_end_effects=True
)

# Induced EMF from changing current
EMF = EMCoupling.induced_emf(
    inductance=L,
    dI_dt=0.1  # statamperes/s
)

# Moving conductor (motional EMF)
EMF_motional = EMCoupling.motional_emf(
    conductor_length=10,  # cm
    velocity=[100, 0, 0],  # cm/s
    B_field=[0, 0, 1000]  # gauss
)

# Energy in coupled circuit system
energy = EMCoupling.electrokinetic_energy(
    currents=[I1, I2],
    inductance_matrix=[[L1, M], [M, L2]]
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `circuit1` | CurrentCarrier | First current source |
| `circuit2` | CurrentCarrier | Second current source (optional) |
| `B_field` | VectorField | Magnetic field (gauss) |
| `E_field` | VectorField | Electric field (statvolt/cm) |
| `velocity` | VectorField | Conductor velocity (cm/s) |
| `inductance` | float | Self or mutual inductance (cm) |
| `frequency` | float | AC frequency (Hz, optional) |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `F` | VectorField | Force (dynes) |
| `EMF` | float | Induced electromotive force (statvolts) |
| `M` | float | Mutual inductance (cm in CGS) |
| `L` | float | Self inductance (cm in CGS) |
| `energy` | float | Electrokinetic energy (ergs) |
| `metadata` | dict | Citations, validation, method info |

## Implementation Notes

- CGS inductance has dimensions of length (cm)
- Conversion: 1 cm inductance = 10⁻⁹ H (SI)
- Neumann formula: M = (1/c²) ∮∮ (dl₁·dl₂)/r
- Elliptic integrals for exact coil solutions
- Motional EMF: EMF = (1/c) ∫ (v × B) · dl

## Validation

- Force between wires matches Ampère's law
- Faraday's law verified with moving magnet
- Mutual inductance reciprocity: M₁₂ = M₂₁
- Energy conservation in coupled systems

## Maxwell Article References

| Article | Content |
|---------|---------|
| 475-479 | Oersted's discovery |
| 490-492 | Electromagnetic force |
| 498-515 | Ampère's force law |
| 520-521 | Mutual potential of circuits |
| 528-535 | Faraday's induction experiments |
| 540-545 | Vector potential and induction |
| 546-570 | Self and mutual inductance |
| 551-567 | Electrokinetic energy |

## Related Commands

- `magnetic-field` - For B-field sources
- `maxwell-equations` - For full field dynamics
- `circuit-analysis` - For lumped inductances

## Error Handling

- Warns about numerical instability for close conductors
- Raises `InductanceError` for ill-posed geometries
- Validates energy conservation
