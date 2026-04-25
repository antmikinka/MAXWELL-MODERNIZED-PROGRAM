# Vector Calculus Standards

## Overview

This document defines the standard conventions for vector calculus operations in the Maxwell package, consistent with Maxwell's original formulations.

## Notation Conventions

### Vector Notation

```
Vector fields:    E, B, J, A (boldface in print, arrow in handwriting)
Scalar fields:    φ, ψ, ρ (italic)
Unit vectors:     x̂, ŷ, ẑ or î, ĵ, k̂
Components:       E_x, E_y, E_z or E^i, E^j, E^k
```

### Differential Operators

| Operator | Notation | Maxwell Article |
|----------|----------|-----------------|
| Gradient | ∇φ, grad φ | 23-27 |
| Divergence | ∇·F, div F | 20-22 |
| Curl | ∇×F, curl F | 23-27 |
| Laplacian | ∇²φ, Δφ | 77-78 |

## Coordinate Systems

### Cartesian (x, y, z)

```
Position: r = x x̂ + y ŷ + z ẑ

Gradient: ∇φ = ∂φ/∂x x̂ + ∂φ/∂y ŷ + ∂φ/∂z ẑ

Divergence: ∇·F = ∂F_x/∂x + ∂F_y/∂y + ∂F_z/∂z

Curl: ∇×F = | x̂    ŷ    ẑ   |
            | ∂/∂x ∂/∂y ∂/∂z |
            | F_x  F_y  F_z  |

Laplacian: ∇²φ = ∂²φ/∂x² + ∂²φ/∂y² + ∂²φ/∂z²
```

### Cylindrical (ρ, φ, z)

```
Position: r = ρ ρ̂ + z ẑ

Scale factors: h_ρ = 1, h_φ = ρ, h_z = 1

Gradient: ∇φ = ∂φ/∂ρ ρ̂ + (1/ρ)∂φ/∂φ φ̂ + ∂φ/∂z ẑ

Divergence: ∇·F = (1/ρ)∂(ρF_ρ)/∂ρ + (1/ρ)∂F_φ/∂φ + ∂F_z/∂z

Curl: ∇×F = [(1/ρ)∂F_z/∂φ - ∂F_φ/∂z] ρ̂
        + [∂F_ρ/∂z - ∂F_z/∂ρ] φ̂
        + (1/ρ)[∂(ρF_φ)/∂ρ - ∂F_ρ/∂φ] ẑ

Laplacian: ∇²φ = (1/ρ)∂/∂ρ(ρ∂φ/∂ρ) + (1/ρ²)∂²φ/∂φ² + ∂²φ/∂z²
```

### Spherical (r, θ, φ)

```
Position: r = r r̂

Scale factors: h_r = 1, h_θ = r, h_φ = r sin θ

Gradient: ∇φ = ∂φ/∂r r̂ + (1/r)∂φ/∂θ θ̂ + (1/(r sin θ))∂φ/∂φ φ̂

Divergence: ∇·F = (1/r²)∂(r²F_r)/∂r + (1/(r sin θ))∂(sin θ F_θ)/∂θ 
                    + (1/(r sin θ))∂F_φ/∂φ

Curl: ∇×F = (1/(r sin θ))[∂(sin θ F_φ)/∂θ - ∂F_θ/∂φ] r̂
        + (1/r)[(1/sin θ)∂F_r/∂φ - ∂(rF_φ)/∂r] θ̂
        + (1/r)[∂(rF_θ)/∂r - ∂F_r/∂θ] φ̂

Laplacian: ∇²φ = (1/r²)∂/∂r(r²∂φ/∂r) + (1/(r² sin θ))∂/∂θ(sin θ ∂φ/∂θ)
                   + (1/(r² sin²θ))∂²φ/∂φ²
```

## Vector Identities

### Product Rules

```
∇(φψ) = φ∇ψ + ψ∇φ

∇·(φF) = φ(∇·F) + F·(∇φ)

∇×(φF) = φ(∇×F) + (∇φ)×F

∇·(F×G) = G·(∇×F) - F·(∇×G)

∇·(∇×F) = 0  (identically)

∇×(∇φ) = 0  (identically)

∇×(∇×F) = ∇(∇·F) - ∇²F
```

### Second Derivative Identities

```
∇²φ = ∇·(∇φ)  (definition)

∇²F = ∇(∇·F) - ∇×(∇×F)  (vector Laplacian)
```

## Integral Theorems

### Divergence Theorem (Gauss's Theorem)

```
∫_V (∇·F) dV = ∮_S F·n dS

Maxwell Articles: 20-22, 77-78
```

### Stokes' Theorem

```
∫_S (∇×F)·n dS = ∮_C F·dl

Maxwell Articles: 23-27
```

### Green's Theorem

```
∫_V (φ∇²ψ - ψ∇²φ) dV = ∮_S (φ∂ψ/∂n - ψ∂φ/∂n) dS

Maxwell Articles: 100-103
```

## CGS Unit Conventions

### Electric Field

```
E in statvolt/cm (CGS electrostatic)
E in abvolt/cm (CGS electromagnetic)
```

### Magnetic Field

```
B in gauss (CGS)
H in oersted (CGS)
```

### Potential

```
φ in statvolt (CGS electrostatic)
φ in abvolt (CGS electromagnetic)
```

### Constants

```
c = 2.99792458 × 10^10 cm/s (speed of light)
4π appears in Coulomb's law (unrationalized CGS)
```

## Implementation Notes

1. All operations default to CGS units
2. Coordinate system must be explicitly specified
3. Numerical differentiation uses central differences
4. Symbolic verification available via SymPy
5. All functions decorated with article citations
