# Task: quaternion-rotation-transform

## Description

Implement 3D rotations using quaternion algebra. This provides efficient and numerically stable rotation operations for coordinate transformations and instrument orientation.

## Workflow Steps

### 1. Rotation Specification
- Define rotation axis
- Specify rotation angle
- Create rotation quaternion

### 2. Quaternion Construction
- Build unit quaternion from axis-angle
- Verify unit norm
- Store rotation metadata

### 3. Vector Rotation
- Convert vector to pure quaternion
- Apply rotation: v' = qvq⁻¹
- Extract rotated vector

### 4. Composition and Inversion
- Compose multiple rotations
- Compute inverse rotation
- Convert to/from rotation matrices

## Requirements

**Input:**
- `axis`: Rotation axis (unit vector)
- `angle`: Rotation angle (radians)
- `vectors`: Vectors to rotate
- `convention`: Rotation convention (active/passive)

**Output:**
- `quaternion`: Unit rotation quaternion
- `rotated_vectors`: Rotated vector array
- `rotation_matrix`: Equivalent 3×3 matrix
- `composition`: Combined rotation (if applicable)

## Implementation

```python
from maxwell.mathematics.quaternions import Quaternion
import numpy as np

def quaternion_rotation(
    axis,
    angle,
    vectors,
    convention='active'
):
    """
    Rotate vectors using quaternions.
    
    Maxwell Articles: 15-18 (quaternion foundations)
    v' = q v q⁻¹  where q = cos(θ/2) + n sin(θ/2)
    """
    # Normalize axis
    axis = np.asarray(axis)
    axis = axis / np.linalg.norm(axis)
    
    # Build rotation quaternion
    half_angle = angle / 2
    q = Quaternion(
        w=np.cos(half_angle),
        x=axis[0] * np.sin(half_angle),
        y=axis[1] * np.sin(half_angle),
        z=axis[2] * np.sin(half_angle)
    )
    
    # Verify unit norm
    assert abs(q.norm() - 1.0) < 1e-10, "Rotation quaternion must be unit"
    
    # Rotate vectors
    rotated = []
    q_inv = q.inverse()
    for v in vectors:
        v_quat = Quaternion.pure(*v)
        v_rotated = q * v_quat * q_inv
        rotated.append(v_rotated.vector())
    
    # Convert to rotation matrix
    R = q.to_rotation_matrix()
    
    return {
        'quaternion': q,
        'rotated_vectors': np.array(rotated),
        'rotation_matrix': R,
        'inverse_quaternion': q_inv
    }
```

## Validation

- Rotation preserves vector length
- Composition of rotations matches quaternion multiplication
- Inverse rotation returns to original
- Comparison with rotation matrix multiplication

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Quaternion foundations |
| 616-620 | Quaternion applications |
