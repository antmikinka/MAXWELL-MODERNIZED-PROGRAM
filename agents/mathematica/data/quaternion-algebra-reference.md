# Quaternion Algebra Reference

## Overview

Reference for quaternion operations as used by Maxwell in his electromagnetic theory. Maxwell extensively used quaternions before vector notation was standardized (Articles 616-620).

## Historical Context

Maxwell's original formulation of electromagnetism used quaternions extensively. The modern vector notation (∇·, ∇×) was derived from quaternion operations by Maxwell himself, then simplified by Heaviside and Gibbs.

## Quaternion Definition

### Basic Structure

```
q = w + xi + yj + zk

where:
  w = scalar (real) part
  xi + yj + zk = vector (imaginary) part
  i² = j² = k² = ijk = -1
```

### Maxwell's Notation

Maxwell often wrote quaternions as:
```
q = Sq + Vq

where:
  Sq = scalar part (w)
  Vq = vector part (xi + yj + zk)
```

## Multiplication Rules

### Basic Products

```
i² = j² = k² = -1

ij = k    ji = -k
jk = i    kj = -i
ki = j    ik = -j
```

### General Quaternion Product

For p = w₁ + x₁i + y₁j + z₁k and q = w₂ + x₂i + y₂j + z₂k:

```
pq = (w₁w₂ - x₁x₂ - y₁y₂ - z₁z₂)
   + (w₁x₂ + x₁w₂ + y₁z₂ - z₁y₂)i
   + (w₁y₂ - x₁z₂ + y₁w₂ + z₁x₂)j
   + (w₁z₂ + x₁y₂ - y₁x₂ + z₁w₂)k
```

### Scalar and Vector Products

```
S(pq) = w₁w₂ - x₁x₂ - y₁y₂ - z₁z₂ = w₁w₂ - v₁·v₂

V(pq) = w₁v₂ + w₂v₁ + v₁×v₂

where v₁×v₂ is the cross product
```

## Operations

### Conjugation

```
q* = w - xi - yj - zk

Properties:
  (pq)* = q*p*
  (q*)* = q
```

### Norm

```
|q| = √(qq*) = √(w² + x² + y² + z²)

Properties:
  |pq| = |p||q|
  |q*| = |q|
```

### Inverse

```
q⁻¹ = q*/|q|²  (for q ≠ 0)

Properties:
  qq⁻¹ = q⁻¹q = 1
  (pq)⁻¹ = q⁻¹p⁻¹
```

### Division

```
p/q = pq⁻¹ = pq*/|q|²

Note: p/q ≠ q/p (non-commutative)
```

## Unit Quaternions and Rotations

### Unit Quaternion

```
q is a unit quaternion if |q| = 1

Can be written as:
q = cos(θ/2) + n sin(θ/2)

where n is a unit vector (pure quaternion)
```

### Rotation

To rotate a vector v by angle θ about axis n:

```
1. Convert v to pure quaternion: v_q = 0 + xi + yj + zk

2. Build rotation quaternion: q = cos(θ/2) + n sin(θ/2)

3. Apply rotation: v'_q = q v_q q⁻¹

4. Extract rotated vector from v'_q
```

### Rotation Matrix from Quaternion

For q = w + xi + yj + zk:

```
R = | 1-2y²-2z²   2xy-2wz     2xz+2wy    |
    | 2xy+2wz     1-2x²-2z²   2yz-2wx    |
    | 2xz-2wy     2yz+2wx     1-2x²-2y²  |
```

## Maxwell's Electromagnetic Formulation

### Quaternion Form of Maxwell's Equations

Maxwell's original equations can be written compactly using quaternions:

```
Nabla operator as quaternion:
∇ = i ∂/∂x + j ∂/∂y + k ∂/∂z

For scalar φ and vector A:
∇(φ + A) = -∇·A + ∇φ + ∇×A

Scalar part: -∇·A
Vector part: ∇φ + ∇×A
```

### Combined Electromagnetic Equation

Maxwell's unified equation (Article 616):

```
∇F = J

where:
  F = electromagnetic field quaternion
  J = current-source quaternion
```

## Implementation in Python

```python
class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __mul__(self, other):
        """Non-commutative quaternion multiplication"""
        return Quaternion(
            w=self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
            x=self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
            y=self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
            z=self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w
        )
    
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    def norm(self):
        return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def inverse(self):
        n2 = self.norm()**2
        return self.conjugate() / n2
    
    @classmethod
    def pure(cls, x, y, z):
        """Create pure quaternion from vector"""
        return cls(0, x, y, z)
    
    @classmethod
    def rotation(cls, axis, angle):
        """Create rotation quaternion"""
        axis = axis / np.linalg.norm(axis)
        half = angle / 2
        return cls(
            np.cos(half),
            axis[0]*np.sin(half),
            axis[1]*np.sin(half),
            axis[2]*np.sin(half)
        )
    
    def rotate(self, vector):
        """Rotate a vector using this quaternion"""
        v_q = Quaternion.pure(*vector)
        result = self * v_q * self.inverse()
        return np.array([result.x, result.y, result.z])
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector quantities (quaternion foundations) |
| 616-620 | Quaternion formulation of electromagnetism |
| Preface | Maxwell's discussion of quaternion methods |

## Comparison with Vector Notation

| Quaternion | Vector Notation |
|------------|-----------------|
| S(∇F) | -∇·F |
| V(∇F) | ∇×F |
| ∇² (quaternion) | Laplacian |
