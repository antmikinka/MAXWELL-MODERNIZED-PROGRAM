# Command: electrostatic-field

## Description

Computes electrostatic fields and potentials for arbitrary charge distributions. This command implements the complete electrostatic theory from Maxwell's Part I (Arts. 27-229), including Coulomb's law, superposition, and potential theory.

## Functionality

### Field Computations
1. **Point Charge Field** (Arts. 44-49)
   - E = q/r² r̂ (CGS ESU)
   - Potential V = q/r

2. **Continuous Distributions** (Arts. 64-68)
   - Volume charge: ρ(x,y,z)
   - Surface charge: σ(x,y,z)
   - Line charge: λ(x,y,z)

3. **Superposition Principle** (Art. 84)
   - Linear addition of field contributions
   - Valid for all static configurations

4. **Gauss's Law** (Arts. 75-76)
   - ∮ E · dA = 4πQ_enclosed
   - Differential form: ∇ · E = 4πρ

### Potential Theory
- Laplace equation: ∇²V = 0 (charge-free regions)
- Poisson equation: ∇²V = -4πρ (with charge)
- Boundary conditions at interfaces
- Method of images for conductors

### Coordinate Systems
- Cartesian: For planar and rectangular geometries
- Cylindrical: For line charges and cylinders
- Spherical: For point charges and spheres

## Usage

```python
from maxwell.physics.electrostatics import ElectrostaticField
from maxwell.core.charge import PointCharge, ChargeDistribution
from maxwell.core.vector import VectorField

# Create point charge
q = PointCharge(position=[0, 0, 0], charge=1.0)  # statcoulombs

# Compute field at observation point
E_field = ElectrostaticField.from_point_charge(
    charge=q,
    observation_point=[1, 0, 0],  # cm
    units='CGS_ESU'
)

# Create continuous distribution
rho = ChargeDistribution(
    density_type='volume',
    function=lambda x, y, z: exp(-(x**2 + y**2 + z**2)),
    bounds={'x': [-inf, inf], 'y': [-inf, inf], 'z': [-inf, inf]}
)

# Compute potential via integration
V = ElectrostaticField.compute_potential(
    distribution=rho,
    method='direct_integration'  # or 'multipole_expansion', 'fft'
)

# Get electric field from potential
E = ElectrostaticField.field_from_gradient(V)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | PointCharge, ChargeDistribution | Source of electrostatic field |
| `observation_points` | ndarray | Points where field is evaluated (cm) |
| `coordinate_system` | str | 'cartesian', 'cylindrical', or 'spherical' |
| `method` | str | 'direct', 'multipole', 'images', 'numerical' |
| `boundary_conditions` | dict | Optional BCs for bounded problems |
| `citations` | list | Maxwell article references (auto-populated) |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `E_field` | VectorField | Electric field vector (statvolt/cm) |
| `potential` | ScalarField | Electric potential (statvolt) |
| `metadata` | dict | Computation details, citations, validation status |

## Implementation Notes

- All computations use CGS ESU units by default
- Singular integrals handled with appropriate quadrature
- Multipole expansions available for distant fields
- Method of images for conducting boundaries
- Numerical grid methods for complex geometries

## Validation

- Verified against analytical solutions:
  - Point charge: E = q/r²
  - Dipole: E = (3(p·r̂)r̂ - p)/r³
  - Uniformly charged sphere: E = Qr/R³ (inside), E = Q/r² (outside)
- Gauss's law verification for closed surfaces
- Divergence check: ∇ · E = 4πρ

## Maxwell Article References

| Article | Content |
|---------|---------|
| 44-49 | Electric field and potential definitions |
| 64-68 | Charge density and Coulomb's law |
| 75-76 | Gauss's law and surface integrals |
| 77-78 | Laplace and Poisson equations |
| 84 | Superposition principle |
| 155-175 | Method of images |

## Related Commands

- `dielectric-response` - For fields in dielectric media
- `magnetic-field` - Analogous magnetostatic computations
- `maxwell-equations` - Full time-dependent solutions

## Error Handling

- Raises `SingularFieldError` at point charge locations
- Warns about convergence for multipole expansions
- Validates charge conservation for numerical methods
