# Command: implement-field

## Description

Implements electric and magnetic field computations for arbitrary source distributions. This command provides the complete field theory from Maxwell's Parts I and III (Arts. 44-49, 395-399), including both electrostatic and magnetostatic field calculations.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Articles 44-49, 395-399 (Electric and Magnetic Field definitions)
- **Standard Mathematical Implementation**: Vector field computations, gradient operations
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Electric Field Computations (Part I)

1. **Point Charge Field** (Arts. 44-49)
   ```
   E = q/r² r̂  (CGS ESU)
   V = q/r
   E = -∇V
   ```

2. **Continuous Charge Distributions** (Arts. 64-68)
   - Volume charge density ρ(x,y,z)
   - Surface charge density σ(x,y,z)
   - Line charge density λ(x,y,z)
   - Field via superposition integral

3. **Gauss's Law Applications** (Arts. 75-76)
   - Integral form: ∮ E · dA = 4πQ_enclosed
   - Differential form: ∇ · E = 4πρ
   - Symmetry-based solutions

4. **Fields in Dielectrics** (Arts. 60-62, 111)
   - Electric displacement: D = εE
   - Polarization: P = χE
   - Bound charge distributions

### Magnetic Field Computations (Part III)

5. **Magnetic Force Field H** (Arts. 395-398)
   ```
   H = -∇Ω  (from scalar potential)
   ```
   - Cylindric cavity measurement
   - Elongated cylinder limits

6. **Magnetic Induction B** (Art. 399)
   ```
   B = H + 4πI  (CGS constitutive relation)
   ```
   - Thin disk cavity measurement
   - Flux tube computations

7. **Solenoidal Condition** (Arts. 403-404)
   ```
   ∇ · B = 0  (no magnetic monopoles)
   ```
   - Surface integral verification
   - Magnetic induction tubes

### Coordinate Systems

- **Cartesian**: For planar and rectangular geometries
- **Cylindrical**: For line charges, wires, cylinders
- **Spherical**: For point sources, spheres, dipoles
- **Curvilinear**: For general orthogonal systems

## Usage

```python
from maxwell.physics.fields import ElectricField, MagneticField
from maxwell.core.charge import PointCharge, ChargeDistribution
from maxwell.core.magnet import MagneticDipole
from maxwell.core.vector import VectorField

# ===== ELECTRIC FIELD EXAMPLES =====

# Point charge field
q = PointCharge(position=[0, 0, 0], charge=1.0)  # statcoulombs
E_field = ElectricField.from_point_charge(
    charge=q,
    observation_point=[1, 0, 0],  # cm
    units='CGS_ESU'
)

# Continuous distribution
rho = ChargeDistribution(
    density_type='volume',
    function=lambda x, y, z: exp(-(x**2 + y**2 + z**2)),
    bounds={'x': [-inf, inf], 'y': [-inf, inf], 'z': [-inf, inf]}
)
E_continuous = ElectricField.from_distribution(
    distribution=rho,
    method='direct_integration'  # or 'multipole', 'fft'
)

# From potential
V = ScalarField(...)
E_from_V = ElectricField.from_potential_gradient(V)

# ===== MAGNETIC FIELD EXAMPLES =====

# Magnetic dipole field
m = MagneticDipole(moment=[0, 0, 1], position=[0, 0, 0])
H_field = MagneticField.from_dipole(
    dipole=m,
    observation_point=[1, 0, 0]
)

# From magnetization
M = MagnetizationField(...)
B_field = MagneticField.from_magnetization(
    magnetization=M,
    include_demagnetization=True
)

# Verify solenoidal condition
div_B = MagneticField.verify_solenoidal(B_field)
assert abs(div_B) < 1e-10  # Should be zero
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | PointCharge, ChargeDistribution, MagneticDipole | Field source |
| `observation_points` | ndarray | Points where field is evaluated (cm) |
| `coordinate_system` | str | 'cartesian', 'cylindrical', or 'spherical' |
| `method` | str | 'direct', 'multipole', 'images', 'numerical' |
| `boundary_conditions` | dict | Optional BCs for bounded problems |
| `material` | Dielectric, MagneticMaterial | Optional material properties |
| `citations` | list | Maxwell article references (auto-populated) |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `E_field` or `H_field` | VectorField | Field vector (statvolt/cm or Oersted) |
| `B_field` or `D_field` | VectorField | Induction field (Gauss or statvolt/cm) |
| `potential` | ScalarField | Scalar potential (statvolt or unit pole potential) |
| `metadata` | dict | Computation details, citations, validation status |

## Implementation Notes

### CGS Units
- Electric field E: statvolt/cm
- Magnetic field H: Oersted (unit pole/cm²)
- Magnetic induction B: Gauss
- Electric displacement D: statvolt/cm

### Numerical Considerations
- Singular integrals handled with appropriate quadrature
- Multipole expansions available for distant fields (Arts. 385-386)
- Method of images for conducting boundaries (Arts. 155-175)
- Numerical grid methods for complex geometries

### Field Properties
- Conservative fields: ∇ × E = 0 (electrostatics)
- Solenoidal fields: ∇ · B = 0 (magnetostatics)
- Potential-derived: E = -∇V, H = -∇Ω

## Validation

### Analytical Solutions
- Point charge: E = q/r² (Art. 44-49)
- Dipole field: E = (3(p·r̂)r̂ - p)/r³ (Art. 69-71)
- Uniformly charged sphere: E = Qr/R³ (inside), E = Q/r² (outside)
- Magnetic dipole: H = (3(m·r̂)r̂ - m)/r³ (Art. 387-388)

### Conservation Checks
- Gauss's law verification for closed surfaces (Art. 76)
- Divergence check: ∇ · E = 4πρ (Art. 77)
- Solenoidal check: ∇ · B = 0 (Art. 403)

### Unit Consistency
- All computations use CGS units by default
- Dimensional analysis verification for all outputs
- ESU vs EMU distinctions maintained

## Maxwell Article References

| Article | Content |
|---------|---------|
| 44-49 | Electric field and potential definitions |
| 64-68 | Charge density and Coulomb's law |
| 75-76 | Gauss's law and surface integrals |
| 77-78 | Laplace and Poisson equations |
| 385-386 | Magnetic potential from magnetized element |
| 387-388 | Dipole-dipole interaction |
| 395-398 | Magnetic force H definitions |
| 399 | Magnetic induction B definition |
| 400 | B = H + 4πI constitutive relation |
| 403-404 | Solenoidal condition for B |

## Related Commands

- `implement-potential` - Compute scalar and vector potentials
- `implement-constitutive` - Material response relations
- `derive-equations` - Derive field equations from first principles
- `solve-analytical` - Analytical benchmark solutions

## Error Handling

- Raises `SingularFieldError` at point source locations
- Warns about convergence for multipole expansions
- Validates charge conservation for numerical methods
- Flags theory alterations for review (should never occur for User theories)

## Theory Preservation Protocol

Before any field computation:
1. Identify source category (Maxwell/User/Standard)
2. Apply appropriate citation label
3. For User theories: IMPLEMENT EXACTLY AS SPECIFIED - DO NOT ALTER
4. For Maxwell: Implement as described in Treatise
5. Document any assumptions explicitly
