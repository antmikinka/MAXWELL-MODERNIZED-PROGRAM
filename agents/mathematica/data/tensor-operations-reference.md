# Tensor Operations Reference

## Overview

Reference for tensor operations used in Maxwell's electromagnetic theory, particularly for stress tensors and anisotropic materials.

## Tensor Notation

### Index Notation

```
Scalar (rank 0):    φ, ρ
Vector (rank 1):    v_i (i = 1,2,3)
Tensor (rank 2):    T_ij (i,j = 1,2,3)
Tensor (rank 4):    C_ijkl
```

### Einstein Summation Convention

```
Repeated indices are summed:

a_i b_i = Σᵢ aᵢ bᵢ (dot product)

T_ij v_j = Σⱼ Tᵢⱼ vⱼ (tensor-vector product)

A_ij B_jk = Σⱼ Aᵢⱼ Bⱼₖ (matrix multiplication)
```

## Maxwell Stress Tensor

### Electrostatic Stress Tensor

```
T_ij = (1/4π) [E_i E_j - (1/2) δ_ij E²]

where:
  E² = E_k E_k
  δ_ij = Kronecker delta

CGS units: T_ij in dyne/cm² (pressure)
```

In matrix form for E = (E_x, E_y, E_z):

```
T = (1/4π) | E_x² - E²/2      E_x E_y         E_x E_z     |
           | E_y E_x          E_y² - E²/2     E_y E_z     |
           | E_z E_x          E_z E_y         E_z² - E²/2 |
```

### Magnetostatic Stress Tensor

```
T_ij = (1/4π) [B_i B_j - (1/2) δ_ij B²]

CGS units: B in gauss, T_ij in dyne/cm²
```

### Combined Electromagnetic Stress Tensor

```
T_ij = (1/4π) [E_i E_j + B_i B_j - (1/2) δ_ij (E² + B²)]
```

### Force from Stress Tensor

```
F_i = ∮_S T_ij n_j dS  (surface integral)

F_i = ∫_V ∂_j T_ij dV  (volume integral)

Force density:
f_i = ∂_j T_ij
```

### Physical Interpretation

```
Diagonal components (T_xx, T_yy, T_zz):
  - Tension along field lines (positive)
  - Pressure perpendicular to field (negative)

Off-diagonal components (T_xy, T_xz, T_yz):
  - Shear stress
```

## Material Property Tensors

### Permittivity Tensor (Anisotropic Dielectrics)

```
D_i = ε_ij E_j

For uniaxial crystal (optic axis along z):

ε = | ε_⊥  0     0    |
    | 0    ε_⊥   0    |
    | 0    0     ε_∥  |

where:
  ε_∥ = permittivity parallel to optic axis
  ε_⊥ = permittivity perpendicular to optic axis
```

### Permeability Tensor (Anisotropic Magnetic Materials)

```
B_i = μ_ij H_j

For uniaxial magnetic material:

μ = | μ_⊥  0     0    |
    | 0    μ_⊥   0    |
    | 0    0     μ_∥  |
```

### Conductivity Tensor (Anisotropic Conductors)

```
J_i = σ_ij E_j

For crystalline conductors:
  σ is symmetric (Onsager reciprocity)
  σ_ij = σ_ji
```

## Tensor Operations

### Contraction

```
Trace (rank-2 tensor):
  T_ii = T_11 + T_22 + T_33 = tr(T)

Double contraction (rank-2 tensors):
  A_ij B_ij = A:B = ΣᵢΣⱼ Aᵢⱼ Bᵢⱼ

Scalar product:
  A:B = tr(A^T B)
```

### Outer Product

```
Dyadic product of vectors:
  (a ⊗ b)_ij = a_i b_j

Tensor product:
  (A ⊗ B)_ijkl = A_ij B_kl
```

### Transformation

Under coordinate rotation x' = R x:

```
Vector:
  v'_i = R_ij v_j

Rank-2 tensor:
  T'_ij = R_ik R_jl T_kl

Matrix form:
  T' = R T R^T
```

### Rotation Matrix

For rotation by angle θ about axis n:

```
R_ij = cos θ δ_ij + (1-cos θ) n_i n_j - sin θ ε_ijk n_k

where ε_ijk is the Levi-Civita symbol
```

## Tensor Invariants

### Principal Invariants (Rank-2 Tensor)

```
I_1 = tr(T) = T_ii (trace)

I_2 = (1/2)[(tr T)² - tr(T²)] = (1/2)(T_ii T_jj - T_ij T_ji)
    = sum of 2×2 principal minors

I_3 = det(T) (determinant)
```

### Eigenvalues

```
Characteristic equation:
  det(T - λI) = 0

λ³ - I₁λ² + I₂λ - I₃ = 0

For symmetric tensor:
  - All eigenvalues are real
  - Eigenvectors are orthogonal
```

### Principal Axes

For symmetric tensor T:

```
T v = λ v

Eigenvectors v₁, v₂, v₃ define principal axes
In principal axis system, T is diagonal:

T = | λ₁  0   0  |
    | 0   λ₂  0  |
    | 0   0   λ₃ |
```

## Special Tensors

### Kronecker Delta

```
δ_ij = 1 if i=j, 0 otherwise

Properties:
  δ_ii = 3
  δ_ij a_j = a_i
  δ_ij T_jk = T_ik
```

### Levi-Civita Symbol

```
ε_ijk = +1 for (i,j,k) = (1,2,3) and cyclic permutations
ε_ijk = -1 for (i,j,k) = (3,2,1) and anticyclic
ε_ijk = 0 otherwise

Identity:
  ε_ijk ε_ilm = δ_jl δ_km - δ_jm δ_kl

Cross product:
  (a × b)_i = ε_ijk a_j b_k

Curl:
  (∇ × F)_i = ε_ijk ∂_j F_k
```

### Isotropic Tensors

```
Rank-0: Any scalar
Rank-1: None (except zero)
Rank-2: λ δ_ij
Rank-4: α δ_ij δ_kl + β δ_ik δ_jl + γ δ_il δ_jk
```

## Implementation in Python

```python
import numpy as np
from numpy import einsum

# Maxwell stress tensor
def maxwell_stress(E, B=None):
    """Compute electromagnetic stress tensor"""
    E2 = np.dot(E, E)
    T = np.outer(E, E) - 0.5 * E2 * np.eye(3)
    
    if B is not None:
        B2 = np.dot(B, B)
        T += np.outer(B, B) - 0.5 * B2 * np.eye(3)
    
    return T / (4 * np.pi)

# Tensor contraction
def contract(A, B, axes=((1,0),)):
    """Contract tensors along specified axes"""
    return einsum(A, B, axes=axes)

# Tensor transformation
def transform_tensor(T, R):
    """Transform rank-2 tensor by rotation R"""
    return R @ T @ R.T

# Eigenvalue decomposition
def principal_axes(T):
    """Find principal axes and values of symmetric tensor"""
    eigenvalues, eigenvectors = np.linalg.eigh(T)
    return eigenvalues, eigenvectors

# Tensor invariants
def tensor_invariants(T):
    """Compute principal invariants"""
    I1 = np.trace(T)
    I2 = 0.5 * (I1**2 - np.trace(T @ T))
    I3 = np.linalg.det(T)
    return I1, I2, I3
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 112-116 | Electrostatic stress tensor |
| 297-301 | Anisotropic conductivity |
| 428-432 | Magnetic anisotropy |
| 443-448 | Electromagnetic stress |
| 641-645 | Stress in dielectric media |
