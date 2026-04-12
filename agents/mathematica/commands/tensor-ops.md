# Command: tensor-ops

## Description

Implements tensor operations for electromagnetic stress, anisotropy, and general tensor calculus. Maxwell's stress tensor and material anisotropy tensors are fundamental to the treatise.

## Functionality

### Tensor Types

1. **Maxwell Stress Tensor** (Articles 112-116, 443-448)
   - Electromagnetic field stress
   - T_ij = ε₀(E_i E_j - ½δ_ij E²) + (1/μ₀)(B_i B_j - ½δ_ij B²)
   - Used for: Force calculations, radiation pressure

2. **Permittivity Tensor** (Articles 297-301)
   - Anisotropic dielectrics
   - D_i = ε_ij E_j
   - Crystalline materials

3. **Permeability Tensor** (Articles 428-432)
   - Anisotropic magnetic materials
   - B_i = μ_ij H_j
   - Magnetic crystals

4. **Conductivity Tensor** (Articles 297-301)
   - Anisotropic conductors
   - J_i = σ_ij E_j

5. **Strain and Stress Tensors**
   - Mechanical coupling (piezoelectricity, magnetostriction)

### Operations

- `create_rank2(components)` - Create rank-2 tensor
- `contract(tensor, indices)` - Tensor contraction
- `transform(tensor, rotation)` - Coordinate transformation
- `eigenvalues(tensor)` - Principal values
- `invariants(tensor)` - Scalar invariants
- `outer_product(a, b)` - Dyadic product
- `trace(tensor)` - Tensor trace
- `determinant(tensor)` - Tensor determinant

### Einstein Summation

Full support for index notation:
```python
tensor_ops.einsum('ij,jk->ik', A, B)  # Matrix multiplication
tensor_ops.einsum('ii->', T)          # Trace
tensor_ops.einsum('ij,j->i', T, v)    # Tensor-vector product
```

## Usage

```python
from maxwell.mathematics.tensors import TensorOperations
from maxwell.core.field import ElectricField, MagneticField
import numpy as np

tensors = TensorOperations()

# Maxwell stress tensor for electric field
E = ElectricField([100, 0, 0])  # V/cm (CGS: statV/cm)
T_E = tensors.maxwell_stress_electric(E)
# Result: 3x3 tensor showing tension along field, pressure perpendicular

# Maxwell stress tensor for magnetic field
B = MagneticField([0, 500, 0])  # Gauss
T_B = tensors.maxwell_stress_magnetic(B)

# Combined electromagnetic stress tensor
T_EM = tensors.maxwell_stress_combined(E, B)

# Compute force density from stress tensor
# f_i = ∂_j T_ij (divergence of stress tensor)
force_density = tensors.stress_divergence(T_EM, grid)

# Permittivity tensor for uniaxial crystal
epsilon_tensor = tensors.permittivity_uniaxial(
    epsilon_parallel=10.0,
    epsilon_perpendicular=5.0,
    optic_axis=[0, 0, 1]
)

# Transform tensor to rotated coordinate system
rotation = tensors.rotation_matrix(axis=[1, 0, 0], angle=np.pi/4)
epsilon_rotated = tensors.transform(epsilon_tensor, rotation)

# Find principal axes (eigenvalues/eigenvectors)
eigenvals, eigenvecs = tensors.eigensystem(epsilon_tensor)
print(f"Principal permittivities: {eigenvals}")

# Tensor invariants (independent of coordinate system)
invariants = tensors.invariants(epsilon_tensor)
print(f"I1 (trace): {invariants.I1}")
print(f"I2 (sum of 2x2 minors): {invariants.I2}")
print(f"I3 (determinant): {invariants.I3}")

# Einstein summation for custom operations
# Double dot product: A:B = A_ij B_ij
double_dot = tensors.einsum('ij,ij->', T_E, T_B)

# Tensor-vector product: (T·v)_i = T_ij v_j
result = tensors.einsum('ij,j->i', T_EM, [1, 0, 0])
```

## Implementation Notes

- Uses NumPy for tensor storage and operations
- einsum for index notation operations
- CGS units throughout (conversion to SI available)
- Symmetric tensors optimized for storage
- Coordinate transformation preserves tensor character

## Validation

- Tensor transformation rules verified
- Invariant quantities unchanged under rotation
- Maxwell stress tensor gives correct force on charges
- Principal axes are orthogonal for symmetric tensors
- Comparison with analytical solutions for simple fields

## Maxwell Article References

| Article | Content |
|---------|---------|
| 112-116 | Electrostatic stress tensor |
| 297-301 | Anisotropic conductivity and permittivity |
| 428-432 | Magnetic anisotropy |
| 443-448 | Electromagnetic stress and pressure |
| 641-645 | Stress in dielectric media |

## Related Commands

- `vector-calculus-ops` - Divergence of tensor fields
- `validate-math` - Tensor property verification
- `material-database` - Material tensor values
