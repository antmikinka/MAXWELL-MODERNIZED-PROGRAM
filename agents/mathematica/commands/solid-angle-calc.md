# Command: solid-angle-calc

## Description

Computes solid angles subtended by various surfaces at observation points. This is critical for Maxwell's magnetic shell theory (Articles 413-429) and electromagnetic field calculations.

## Functionality

### Solid Angle Geometries

1. **Circular Disk**
   - On-axis: Ω = 2π(1 - cos α)
   - Off-axis: Elliptic integral formulation
   - Article references: 413-417

2. **Circular Cone**
   - Ω = 2π(1 - cos θ)
   - Article references: 418-420

3. **Rectangular Plate**
   - Analytical formula using arctangents
   - Useful for coil winding calculations

4. **Polygonal Mesh**
   - General surface via triangulation
   - Sum of triangular solid angles

5. **Spherical Cap**
   - Ω = 2π(1 - cos θ)
   - Article references: 421-425

6. **Magnetic Shell**
   - Equivalent current loop
   - Potential = (I/c) × Ω
   - Article references: 413-429

### Operations

- `disk(on_axis_distance, radius)` - Circular disk solid angle
- `cone(half_angle)` - Cone solid angle
- `rectangle(dist, width, height)` - Rectangular plate
- `mesh(vertices, observation_point)` - General mesh
- `spherical_cap(radius, height)` - Spherical cap
- `magnetic_shell(current, geometry)` - Magnetic shell potential

## Usage

```python
from maxwell.mathematics.solid_angle import SolidAngleCalculator
import numpy as np

calc = SolidAngleCalculator()

# Circular disk (on-axis)
# Distance = 5 cm, Radius = 3 cm
omega_disk = calc.disk(distance=5.0, radius=3.0)
print(f"Solid angle: {omega_disk:.6f} steradians")

# Circular cone (half-angle = 30 degrees)
omega_cone = calc.cone(half_angle=np.radians(30))
print(f"Cone solid angle: {omega_cone:.6f} sr")

# Rectangular plate
# Distance = 10 cm, Width = 4 cm, Height = 6 cm
omega_rect = calc.rectangle(distance=10.0, width=4.0, height=6.0)

# Triangular mesh (arbitrary surface)
vertices = [
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Base
    [0.5, 0.5, 1]  # Apex
]
obs_point = [0.5, 0.5, 2.0]
omega_mesh = calc.mesh(vertices, obs_point)

# Magnetic shell potential (CGS units)
# Current I = 1 abampere, geometry = disk
potential = calc.magnetic_shell(
    current=1.0,  # abamperes
    geometry='disk',
    distance=5.0,
    radius=3.0
)
print(f"Magnetic scalar potential: {potential:.6f} oersteds·cm")
```

## Implementation Notes

- All angles in radians, distances in centimeters (CGS)
- On-axis formulas are analytical
- Off-axis disk uses elliptic integrals (scipy.special.ellipk, ellipe)
- Mesh calculation uses spherical excess formula for triangles
- Sign convention: positive when surface normal points toward observer

## Validation

- Full sphere: Ω = 4π steradians
- Hemisphere: Ω = 2π steradians
- Infinite plane (one side): Ω = 2π steradians
- Comparison with Monte Carlo integration for complex geometries

## Maxwell Article References

| Article | Content |
|---------|---------|
| 413-417 | Magnetic potential of a shell |
| 418-420 | Solid angle of a cone |
| 421-425 | Solid angle of a sphere |
| 426-429 | Applications to electromagnets |

## Related Commands

- `quaternion-algebra` - For rotation of geometries
- `tensor-ops` - For solid angle tensors in anisotropic media
- `validate-math` - Verification of solid angle calculations
