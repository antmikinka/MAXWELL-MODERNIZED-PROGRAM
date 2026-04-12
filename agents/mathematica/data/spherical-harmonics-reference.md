# Spherical Harmonics Reference

## Overview

Complete reference for spherical harmonics used throughout Maxwell's Treatise, particularly in electrostatics (Articles 125-133) and magnetism (Articles 543-555).

## Definitions

### Legendre Polynomials

```
P_n(x) = (1/2^n n!) d^n/dx^n [(x²-1)^n]  (Rodrigues formula)

Generating function:
1/|r - r'| = Σ (r_<^n / r_>^(n+1)) P_n(cos γ)

where γ is the angle between r and r'
```

### Associated Legendre Functions

```
P_n^m(x) = (-1)^m (1-x²)^(m/2) d^m/dx^m P_n(x)

P_n^m(cos θ) for m ≥ 0

P_n^(-m)(x) = (-1)^m [(n-m)!/(n+m)!] P_n^m(x)
```

### Spherical Harmonics

```
Y_l^m(θ, φ) = √[(2l+1)/(4π) × (l-m)!/(l+m)!] P_l^m(cos θ) e^(imφ)

Normalization: ∫ |Y_l^m|² dΩ = 1

Condon-Shortley phase: (-1)^m factor included
```

## Explicit Forms

### Low-Order Legendre Polynomials

```
P_0(x) = 1
P_1(x) = x
P_2(x) = (3x² - 1)/2
P_3(x) = (5x³ - 3x)/2
P_4(x) = (35x⁴ - 30x² + 3)/8
```

### Low-Order Spherical Harmonics

```
Y_0^0 = 1/√(4π)

Y_1^0 = √(3/4π) cos θ
Y_1^±1 = ∓√(3/8π) sin θ e^(±iφ)

Y_2^0 = √(5/16π) (3cos²θ - 1)
Y_2^±1 = ∓√(15/8π) sin θ cos θ e^(±iφ)
Y_2^±2 = √(15/32π) sin²θ e^(±i2φ)
```

### Real (Tesseral) Harmonics

```
For m > 0:
Y_lm^c = √2 Re[Y_l^m] = √2 × √[(2l+1)/(4π) × (l-m)!/(l+m)!] P_l^m(cos θ) cos(mφ)

Y_lm^s = √2 Im[Y_l^m] = √2 × √[(2l+1)/(4π) × (l-m)!/(l+m)!] P_l^m(cos θ) sin(mφ)

For m = 0:
Y_l0 = Y_l^0
```

## Properties

### Orthogonality

```
∫_0^π ∫_0^(2π) Y_l^m(θ,φ) Y_l'^m'*(θ,φ) sin θ dθ dφ = δ_ll' δ_mm'
```

### Completeness

```
Σ_l=0^∞ Σ_m=-l^l Y_l^m(θ,φ) Y_l^m*(θ',φ') = δ(φ-φ') δ(cos θ - cos θ')
```

### Recurrence Relations

```
(l-m+1) P_(l+1)^m(x) = (2l+1) x P_l^m(x) - (l+m) P_(l-1)^m(x)

P_n^m(x) = (-1)^m (1-x²)^(m/2) d^m/dx^m P_n(x)
```

### Addition Theorem

```
P_l(cos γ) = (4π/(2l+1)) Σ_m=-l^l Y_l^m(θ,φ) Y_l^m*(θ',φ')

where cos γ = cos θ cos θ' + sin θ sin θ' cos(φ-φ')
```

## Applications in Maxwell

### Electrostatic Potential Expansion

```
φ(r,θ,φ) = Σ_l=0^∞ Σ_m=-l^l [A_lm r^l + B_lm r^(-(l+1))] Y_l^m(θ,φ)

Interior (r < R): Use r^l terms (regular at origin)
Exterior (r > R): Use r^(-(l+1)) terms (decay at infinity)
```

### Multipole Expansion

```
φ(r) = q/r + p·r/r³ + (1/2) Σ Q_ij r_i r_j / r^5 + ...

Monopole (l=0): q
Dipole (l=1): p_i
Quadrupole (l=2): Q_ij
```

### Magnetic Potential

```
Ω(r,θ,φ) = Σ_l=0^∞ Σ_m=-l^l [C_lm r^l + D_lm r^(-(l+1))] Y_l^m(θ,φ)

B = -∇Ω
```

## Numerical Computation

### SciPy Functions

```python
from scipy.special import lpmn, sph_harm

# Associated Legendre
Pnm, dPnm = lpmn(m, n, x)  # P_n^m(x) and derivative

# Spherical harmonics
Y_lm = sph_harm(m, l, phi, theta)  # Note: phi, theta order
```

### Quadrature

```
Gauss-Legendre quadrature for θ integration
Trapezoidal rule for φ integration (periodic)
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 125-133 | Spherical harmonic theory |
| 140-145 | Electrostatic applications |
| 543-555 | Magnetic applications |
| 692-700 | Electromagnetic applications |

## Tables

### Zonal Harmonic Values

| n | P_n(0) | P_n(1) | P_n(-1) |
|---|--------|--------|---------|
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | -1 |
| 2 | -1/2 | 1 | 1 |
| 3 | 0 | 1 | -1 |
| 4 | 3/8 | 1 | 1 |

### Normalization Constants

| l | m | N_lm = √[(2l+1)/(4π) × (l-m)!/(l+m)!] |
|---|---|-------------------------------------------|
| 0 | 0 | 1/√(4π) ≈ 0.2821 |
| 1 | 0 | √(3/4π) ≈ 0.4886 |
| 1 | 1 | √(3/8π) ≈ 0.3455 |
| 2 | 0 | √(5/16π) ≈ 0.3154 |
| 2 | 1 | √(15/8π) ≈ 0.6898 |
| 2 | 2 | √(15/32π) ≈ 0.4886 |
