# Data: effective-medium-reference

## Purpose

Comprehensive reference data for effective medium calculations including mixing formulas, bounds, and composite material properties.

---

## Effective Medium Models

### Maxwell-Garnett Formula

For spherical inclusions in a matrix:

K_eff = K_m × [(K_i + 2K_m + 2f(K_i - K_m)) / (K_i + 2K_m - f(K_i - K_m))]

where:
- K_eff = effective permittivity
- K_m = matrix permittivity
- K_i = inclusion permittivity
- f = inclusion volume fraction

**Validity:** Dilute suspensions (f < 0.2)

**Maxwell Reference:** Art. 314 (Treatise, Vol. I)

---

### Bruggeman Symmetric Formula

Self-consistent equation:

f₁ × (K₁ - K_eff) / (K₁ + 2K_eff) + f₂ × (K₂ - K_eff) / (K₂ + 2K_eff) = 0

where:
- f₁, f₂ = volume fractions (f₁ + f₂ = 1)
- K₁, K₂ = phase permittivities

**Validity:** All volume fractions, symmetric treatment

---

### Wiener Bounds

**Upper Bound (Parallel/Voigt):**
K_upper = f₁K₁ + f₂K₂

**Lower Bound (Series/Reuss):**
1/K_lower = f₁/K₁ + f₂/K₂

**Validity:** All composites (rigorous bounds)

---

### Hashin-Shtrikman Bounds

For K₁ > K₂:

**HS+ Upper Bound:**
K_HS+ = K₁ + f₂ / [1/(K₂-K₁) + f₁/(K₁ + 4G₁/3)]

**HS- Lower Bound:**
K_HS- = K₂ + f₁ / [1/(K₁-K₂) + f₂/(K₂ + 4G₂/3)]

where G = shear modulus

**Validity:** Isotropic composites (tightest bounds)

---

## Percolation Thresholds

### Critical Volume Fractions

| Inclusion Geometry | f_c (percolation) | Model |
|-------------------|-------------------|-------|
| Spheres (random) | 0.16-0.29 | Continuum |
| Spheres (simple cubic) | 0.52 | Lattice |
| Spheres (BCC) | 0.17 | Lattice |
| Spheres (FCC) | 0.12 | Lattice |
| Overlapping spheres | 0.29 | Continuum |
| Cylinders (aligned, 3D) | 0.01-0.05 | High aspect ratio |
| Platelets | 0.01-0.1 | Depends on aspect ratio |
| Cubes | 0.25-0.31 | Lattice |

### Percolation Scaling

Near threshold:
σ_eff ∝ (f - f_c)^t  for f > f_c

where t ≈ 1.6-2.0 (universal exponent)

---

## Aspect Ratio Effects

### Halpin-Tsai Equations

For aligned fibers or platelets:

P/P_m = (1 + ζηf) / (1 - ηf)

where:
- η = (P_i/P_m - 1) / (P_i/P_m + ζ)
- ζ = shape parameter (depends on geometry)
- P = property of interest

**Shape Parameters:**

| Geometry | ζ |
|----------|---|
| Fibers (longitudinal) | 2(L/D) |
| Fibers (transverse) | 2 |
| Platelets | 2(a/b) |
| Spheres | 2 |

---

## Differential Effective Medium (DEM)

### Differential Equation

dK_eff/df = (K_i - K_eff) × (1 + L × (K_i - K_eff) / (K_eff + M)) / (1 - f)

where L, M depend on inclusion shape

**Integration:** from f = 0 (pure matrix) to final f

**Validity:** High volume fractions, graded microstructures

---

## Anisotropic Effective Media

### Transversely Isotropic Composites

For aligned fibers or platelets:

**Parallel Direction:**
K_∥ = fK_i + (1-f)K_m  (rule of mixtures)

**Perpendicular Direction:**
1/K_⊥ = f/K_i + (1-f)/K_m  (inverse rule of mixtures)

### General Anisotropy

Effective permittivity tensor:
[K_eff] = | K_xx  K_xy  K_xz |
          | K_yx  K_yy  K_yz |
          | K_zx  K_zy  K_zz |

Principal values found by diagonalization.

---

## Complex Permittivity

### Effective Complex Permittivity

K_eff* = K_eff' - iK_eff''

where:
- K_eff' = real part (storage)
- K_eff'' = loss factor

### Loss Tangent

tan δ_eff = K_eff'' / K_eff'

### Mixing Rules for Complex Permittivity

Apply Maxwell-Garnett or Bruggeman to complex values:

K_eff* = K_m* × [(K_i* + 2K_m* + 2f(K_i* - K_m*)) / (K_i* + 2K_m* - f(K_i* - K_m*))]

---

## Magnetic Effective Media

### Effective Permeability

Same formulas apply with μ replacing K:

μ_eff = μ_m × [(μ_i + 2μ_m + 2f(μ_i - μ_m)) / (μ_i + 2μ_m - f(μ_i - μ_m))]  (Maxwell-Garnett)

### Effective Susceptibility

κ_eff = (μ_eff - 1) / 4π

**Maxwell Reference:** Art. 424-440

---

## Conductive Composites

### Effective Conductivity

σ_eff = σ_m × [(σ_i + 2σ_m + 2f(σ_i - σ_m)) / (σ_i + 2σ_m - f(σ_i - σ_m))]  (Maxwell-Garnett)

### Percolation in Conductive Composites

Below f_c: σ_eff ≈ σ_m (insulating)
Above f_c: σ_eff ∝ (f - f_c)^t (conductive)

where t ≈ 1.6-2.0

---

## Example Calculations

### Example 1: Dielectric Composite

**Given:**
- Matrix: Epoxy (K_m = 3.5)
- Inclusions: Glass spheres (K_i = 7.0)
- Volume fraction: f = 0.15

**Maxwell-Garnett:**
K_eff = 3.5 × [(7.0 + 2×3.5 + 2×0.15×(7.0-3.5)) / (7.0 + 2×3.5 - 0.15×(7.0-3.5))]
K_eff = 3.5 × [(14.0 + 1.05) / (14.0 - 0.525)]
K_eff = 3.5 × 15.05 / 13.475
K_eff = 3.91

**Wiener Bounds:**
K_upper = 0.15×7.0 + 0.85×3.5 = 4.025
K_lower = 1 / (0.15/7.0 + 0.85/3.5) = 3.73

Check: 3.73 < 3.91 < 4.025 ✓

---

### Example 2: Magnetic Composite

**Given:**
- Matrix: Polymer (μ_m = 1.0)
- Inclusions: Iron powder (μ_i = 5000)
- Volume fraction: f = 0.30

**Bruggeman (numerical solution):**
0.30 × (5000 - μ_eff) / (5000 + 2μ_eff) + 0.70 × (1 - μ_eff) / (1 + 2μ_eff) = 0

Solution: μ_eff ≈ 3.5

---

### Example 3: Conductive Composite

**Given:**
- Matrix: Polymer (σ_m = 10⁻¹⁵ s⁻¹)
- Inclusions: Silver (σ_i = 6.3×10¹⁷ s⁻¹)
- Volume fraction: f = 0.05

**Maxwell-Garnett:**
σ_eff = 10⁻¹⁵ × [(6.3×10¹⁷ + 2×10⁻¹⁵ + 2×0.05×(6.3×10¹⁷ - 10⁻¹⁵)) / (6.3×10¹⁷ + 2×10⁻¹⁵ - 0.05×(6.3×10¹⁷ - 10⁻¹⁵))]

Since σ_i >> σ_m:
σ_eff ≈ σ_m × (1 + 2f) / (1 - f) = 10⁻¹⁵ × 1.1 / 0.95 = 1.16×10⁻¹⁵ s⁻¹

---

## Summary of Model Validity

| Model | Validity Range | Accuracy | Complexity |
|-------|---------------|----------|------------|
| Maxwell-Garnett | f < 0.2 | Good for dilute | Low |
| Bruggeman | All f | Good for symmetric | Medium |
| Wiener bounds | All f | Rigorous bounds | Low |
| Hashin-Shtrikman | All f | Tightest bounds | Medium |
| Halpin-Tsai | Aligned fibers | Good for anisotropic | Low |
| Differential | All f | Good for graded | High |
| Percolation | Near f_c | Critical behavior | Medium |

---

## Notes on Data Quality

- All formulas in dimensionless form (CGS consistent)
- Maxwell-Garnett from Maxwell's Treatise, Art. 314
- Theory classification: standard_math for mixing formulas
- Verify predictions against experimental data
- Consider microstructure effects for accurate predictions
