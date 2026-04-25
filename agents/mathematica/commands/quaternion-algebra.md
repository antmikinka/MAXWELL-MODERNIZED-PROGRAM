# Command: quaternion-algebra

## Description

Implements quaternion algebra as used by Maxwell in his original electromagnetic theory. Maxwell's Treatise extensively used quaternions before vector notation was standardized. This command provides both historical quaternion formulations and modern vector equivalents.

## Functionality

### Quaternion Operations

1. **Basic Operations**
   - Addition, subtraction
   - Multiplication (non-commutative)
   - Division (multiplication by inverse)
   - Conjugation
   - Norm and normalization

2. **Quaternion Structure**
   - Scalar part (real)
   - Vector part (imaginary: i, j, k)
   - q = w + xi + yj + zk

3. **Special Quaternions**
   - Unit quaternions (rotations)
   - Pure quaternions (scalar = 0)
   - Versors (unit norm)

4. **Applications**
   - 3D rotations
   - Vector operations via quaternion products
   - Historical Maxwell equation formulation

### Quaternion Products

For quaternions p and q:
- **Scalar product**: S(pq) = -p·q (negative dot product)
- **Vector product**: V(pq) = p×i (cross product equivalent)

## Usage

```python
from maxwell.mathematics.quaternions import Quaternion
import numpy as np

# Create quaternions
q1 = Quaternion(w=1, x=2, y=3, z=4)
q2 = Quaternion(w=2, x=0, y=-1, z=1)

# Basic operations
q_sum = q1 + q2
q_diff = q1 - q2
q_prod = q1 * q2  # Non-commutative!
q_div = q1 / q2

# Properties
norm_q1 = q1.norm()
conj_q1 = q1.conjugate()
inv_q1 = q1.inverse()

# Scalar and vector parts
scalar_part = q1.scalar()  # Returns: 1
vector_part = q1.vector()  # Returns: [2, 3, 4]

# Pure quaternion from vector
v = Quaternion.pure(x=1, y=2, z=3)

# Rotation quaternion (90 degrees about z-axis)
theta = np.pi / 2
q_rot = Quaternion.rotation(axis=[0, 0, 1], angle=theta)

# Rotate a vector using quaternions
v_original = Quaternion.pure(x=1, y=0, z=0)
v_rotated = q_rot * v_original * q_rot.inverse()

# Maxwell's formulation: vector operations via quaternions
# Dot product: S(p*q) = -(p·q)
# Cross product: V(p*q) = p×q
a = Quaternion.pure(1, 0, 0)
b = Quaternion.pure(0, 1, 0)
dot_product = -1 * (a * b).scalar()  # Should be 0
cross_product = (a * b).vector()     # Should be [0, 0, 1]

# Historical: Maxwell's electromagnetic equations in quaternion form
# (Article 616-620)
def maxwell_quaternion_form(E, B, J, rho):
    """
    Maxwell's equations in quaternion form.
    E, B: pure quaternions (vector fields)
    J: current density (pure quaternion)
    rho: charge density (scalar)
    """
    # Nabla as pure quaternion operator
    nabla = Quaternion.pure_symbolic()  # ∂_x i + ∂_y j + ∂_z k
    
    # Combined electromagnetic equation
    # This is a historical formulation showing quaternion structure
    pass
```

## Implementation Notes

- Quaternion multiplication follows Hamilton convention: i² = j² = k² = ijk = -1
- Non-commutative: pq ≠ qp in general
- Multiplication table:
  - ij = k, ji = -k
  - jk = i, kj = -i
  - ki = j, ik = -j
- CGS units for physical applications
- Symbolic quaternion support via SymPy integration

## Validation

- Associativity: (pq)r = p(qr)
- Norm property: |pq| = |p||q|
- Inverse verification: q × q⁻¹ = 1
- Rotation verification: preserves vector length
- Cross product verification via quaternion product

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector quantities (quaternion basis) |
| 616-620 | Quaternion formulation of electromagnetism |
| Preface | Maxwell's discussion of quaternion methods |

## Related Commands

- `vector-calculus-ops` - Modern vector equivalent operations
- `tensor-ops` - Higher-rank generalizations
- `validate-math` - Algebraic property verification
