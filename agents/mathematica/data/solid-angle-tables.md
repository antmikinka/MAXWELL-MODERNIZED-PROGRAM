# Solid Angle Tables

## Overview

Comprehensive tables and formulas for solid angle calculations used in Maxwell's magnetic shell theory (Articles 413-429).

## Definitions

### Solid Angle

The solid angle Ω subtended by a surface S at a point P is:

```
Ω = ∫_S (r̂·n̂) dA / r²

where:
  r = distance from P to surface element
  r̂ = unit vector from P to element
  n̂ = surface normal
```

Units: steradians (sr)
Full sphere: 4π sr
Hemisphere: 2π sr

## Standard Geometries

### Circular Disk (On-Axis)

```
Ω = 2π(1 - cos α)

where:
  sin α = R / √(R² + d²)
  cos α = d / √(R² + d²)
  
  R = disk radius
  d = distance from point to disk center (on axis)

Alternative form:
Ω = 2π[1 - d/√(R² + d²)]
```

| d/R | Ω/π | Ω (degrees²) |
|-----|-----|--------------|
| 0 (at center) | 2.000 | 20626 |
| 0.1 | 1.990 | 20523 |
| 0.5 | 1.894 | 19533 |
| 1.0 | 1.586 | 16358 |
| 2.0 | 0.944 | 9738 |
| 5.0 | 0.237 | 2445 |
| 10.0 | 0.062 | 640 |

### Circular Cone

```
Ω = 2π(1 - cos θ)

where θ = half-angle of cone
```

| θ (degrees) | Ω (sr) | Ω/4π (fraction of sphere) |
|-------------|--------|---------------------------|
| 10 | 0.095 | 0.0076 |
| 30 | 0.842 | 0.067 |
| 45 | 1.840 | 0.146 |
| 60 | 3.142 | 0.250 |
| 90 | 6.283 | 0.500 |
| 120 | 9.425 | 0.750 |
| 180 | 12.566 | 1.000 |

### Rectangular Plate (On-Axis)

```
Ω = 4 arcsin[sin α sin β]

where:
  tan α = a / (2d)
  tan β = b / (2d)
  
  a, b = plate dimensions
  d = distance to center (on axis)

Alternative form:
Ω = 4 arctan[ab / (2d√(4d² + a² + b²))]
```

### Spherical Cap

```
Ω = 2π(1 - cos θ)

where θ = half-angle of cap

In terms of cap height h and sphere radius R:
Ω = 2πh/R
```

### Right Rectangular Pyramid

```
Ω = 4 arcsin[sin(α/2) sin(β/2)]

where α, β = face angles at apex
```

## General Formulas

### Triangular Surface

For a triangle with vertices A, B, C as seen from point O:

```
Ω = A + B + C - π  (spherical excess)

where A, B, C are the angles of the spherical triangle

Oosterom-Strackee formula:
tan(Ω/2) = |a·(b×c)| / (abc + (a·b)c + (b·c)a + (c·a)b)

where a, b, c are vectors from O to vertices
```

### Arbitrary Polygon

For a planar polygon with n vertices:

```
Ω = Σᵢ ωᵢ - (n-2)π

where ωᵢ are the angles between consecutive edges
```

## Magnetic Shell Applications

### Current Loop Potential

The magnetic scalar potential of a current loop:

```
φ = (I/c) × Ω

where:
  I = current (abamperes, CGS)
  c = speed of light (cm/s)
  Ω = solid angle subtended by loop

Units: φ in oersteds·cm (CGS)
```

### Magnetic Dipole Limit

For a small loop (dipole limit):

```
φ = (m·r̂) / r²

where:
  m = (I/c) × area × n̂  (magnetic moment)
  
This matches the solid angle formula for small Ω:
Ω ≈ (area × cos θ) / r²
```

### Solenoid On-Axis

For a finite solenoid on its axis:

```
Ω = 2π(cos θ₁ - cos θ₂)

where θ₁, θ₂ are angles to the two ends

B_z = (2πnI/c)(cos θ₁ - cos θ₂)

where n = turns per unit length
```

## Numerical Computation

### Monte Carlo Method

For arbitrary surfaces:

```python
def solid_angle_monte_carlo(surface, point, n_samples=10000):
    """Estimate solid angle by Monte Carlo integration"""
    # Generate random directions
    directions = random_unit_sphere(n_samples)
    
    # Count rays that hit surface
    hits = 0
    for d in directions:
        if ray_intersects_surface(point, d, surface):
            hits += 1
    
    # Solid angle = 4π × (fraction of hits)
    return 4 * np.pi * hits / n_samples
```

### Triangulation Method

For arbitrary surfaces:

```python
def solid_angle_mesh(vertices, faces, point):
    """Sum solid angles of triangular faces"""
    total = 0
    for face in faces:
        a, b, c = vertices[face]
        total += triangle_solid_angle(a - point, b - point, c - point)
    return total
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 413-417 | Magnetic shell potential |
| 418-420 | Solid angle of cone |
| 421-425 | Solid angle applications |
| 426-429 | Electromagnet applications |

## Useful Constants

```
Full sphere: 4π sr = 41253 deg²
Hemisphere: 2π sr = 20626 deg²
Square degree to steradian: 1 deg² = (π/180)² sr ≈ 3.046×10⁻⁴ sr
Steradian to square degree: 1 sr ≈ 3282.8 deg²
```
