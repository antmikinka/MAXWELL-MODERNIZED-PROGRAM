# Task: solid-angle-magnetic-shell

## Description

Calculate solid angles for magnetic shell theory and electromagnetic applications. This implements Maxwell's magnetic shell formulation where the scalar potential is proportional to the solid angle (Articles 413-429).

## Workflow Steps

### 1. Geometry Definition
- Define shell geometry (disk, cone, arbitrary)
- Specify observation point
- Determine surface orientation

### 2. Solid Angle Calculation
- Apply appropriate formula for geometry
- Handle on-axis and off-axis cases
- Compute sign based on orientation

### 3. Magnetic Potential
- Compute potential: φ = (I/c) × Ω
- Apply to electromagnetic problems
- Verify against known results

### 4. Applications
- Current loop potential
- Electromagnet design
- Magnetic field calculation

## Requirements

**Input:**
- `geometry`: Shell geometry specification
- `observation_point`: Point where potential is computed
- `current`: Current strength (abamperes, CGS)
- `orientation`: Surface normal direction

**Output:**
- `solid_angle`: Ω in steradians
- `magnetic_potential`: φ in oersteds·cm
- `magnetic_field`: B = -∇φ
- `validation`: Comparison with known results

## Implementation

```python
from maxwell.mathematics.solid_angle import SolidAngleCalculator
from maxwell.core.constants import SPEED_OF_LIGHT_CGS

def compute_magnetic_shell_potential(
    geometry,
    observation_point,
    current,
    orientation=None
):
    """
    Compute magnetic scalar potential of a shell.
    
    Maxwell Articles: 413-429
    φ = (I/c) × Ω  (CGS units)
    B = -∇φ
    """
    calc = SolidAngleCalculator()
    
    # Compute solid angle
    solid_angle = calc.compute(
        geometry=geometry,
        observation_point=observation_point,
        orientation=orientation
    )
    
    # Compute magnetic scalar potential
    magnetic_potential = (current / SPEED_OF_LIGHT_CGS) * solid_angle
    
    # Compute magnetic field (negative gradient)
    # This requires numerical differentiation for arbitrary geometries
    magnetic_field = compute_gradient_numerical(
        lambda p: compute_magnetic_shell_potential(
            geometry, p, current, orientation
        ),
        observation_point
    )
    
    return {
        'solid_angle': solid_angle,
        'magnetic_potential': magnetic_potential,
        'magnetic_field': magnetic_field,
        'geometry_info': geometry.describe()
    }
```

## Validation

- On-axis disk formula verification
- Comparison with Biot-Savart law for current loops
- Distant field matches dipole approximation

## Maxwell Article References

| Article | Content |
|---------|---------|
| 413-417 | Magnetic shell potential |
| 418-420 | Solid angle of cone |
| 421-425 | Solid angle applications |
| 426-429 | Electromagnet applications |
