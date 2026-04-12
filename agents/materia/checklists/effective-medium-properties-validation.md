# Checklist: effective-medium-properties-validation

## Purpose

Comprehensive validation checklist for effective medium calculations and composite material property predictions.

## Usage

Use this checklist when validating effective medium models, homogenization calculations, or composite property predictions. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Model Selection

- [ ] Effective medium model selected and justified
- [ ] Model applicability range documented
- [ ] Model limitations acknowledged

### Maxwell's Contributions

- [ ] Maxwell-Garnett theory referenced
- [ ] Maxwell's Treatise citations included
- [ ] Historical context provided

### Mathematical Formulation

- [ ] Governing equations documented
- [ ] Assumptions explicitly stated
- [ ] Derivation or reference provided

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Constituent Phase Definition

### Matrix Phase

- [ ] Matrix material identified
- [ ] Volume fraction specified (f_m)
- [ ] Properties documented (K_m, μ_m, σ_m)
- [ ] Temperature conditions defined

### Inclusion Phase(s)

- [ ] Inclusion material(s) identified
- [ ] Volume fraction(s) specified (f_i)
- [ ] Properties documented
- [ ] Size/shape parameters defined

### Volume Fraction Check

- [ ] Sum of volume fractions = 1
- [ ] Porosity accounted for (if applicable)
- [ ] Uncertainty in volume fractions quantified

**Phase Definition Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Inclusion Geometry

### Shape Characterization

- [ ] Geometry type specified (sphere/ellipsoid/fiber/platelet)
- [ ] Aspect ratio documented (if non-spherical)
- [ ] Size distribution characterized

### Orientation

- [ ] Orientation distribution specified
- [ ] Alignment direction defined (if aligned)
- [ ] Random vs. aligned documented

### Spatial Distribution

- [ ] Dispersion quality characterized
- [ ] Clustering/agglomeration assessed
- [ ] Percolation threshold estimated

**Geometry Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: Effective Medium Model Application

### Maxwell-Garnett Model

- [ ] Dilute limit check (f < 0.2)
- [ ] Formula correctly applied
- [ ] Results within validity range

### Bruggeman Model

- [ ] Self-consistent equation solved
- [ ] Percolation threshold calculated
- [ ] Symmetric treatment verified

### Other Models

- [ ] Wiener bounds calculated
- [ ] Hashin-Shtrikman bounds calculated
- [ ] Model comparison provided

**Model Application Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: CGS Unit Consistency

### Property Units

- [ ] Permittivity: dimensionless (K)
- [ ] Permeability: dimensionless (μ)
- [ ] Conductivity: s⁻¹ (CGS electrostatic)

### Derived Quantities

- [ ] Effective properties in correct units
- [ ] Volume fractions dimensionless
- [ ] All intermediate calculations consistent

### Unit Conversions

- [ ] Input data converted to CGS
- [ ] Output data conversion factors provided
- [ ] No mixed unit systems

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Bounds and Limits

### Wiener Bounds

- [ ] Upper bound (parallel/Voigt) calculated
- [ ] Lower bound (series/Reuss) calculated
- [ ] Effective property within bounds

### Hashin-Shtrikman Bounds

- [ ] HS+ bound calculated
- [ ] HS- bound calculated
- [ ] Effective property within HS bounds

### Limiting Cases

- [ ] f → 0 limit verified (matrix properties)
- [ ] f → 1 limit verified (inclusion properties)
- [ ] Dilute limit compared with Maxwell-Garnett

**Bounds Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Microstructure Effects

### Interfacial Layer

- [ ] Interface presence identified
- [ ] Interface thickness specified
- [ ] Interface properties defined
- [ ] Maxwell-Wagner effect considered

### Size Effects

- [ ] Characteristic size documented
- [ ] Mean free path considered
- [ ] Knudsen number calculated (if relevant)

### Clustering/Correlation

- [ ] Correlation function characterized
- [ ] Structure factor documented
- [ ] Effective cluster properties estimated

**Microstructure Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 8: Validation

### Comparison with Data

- [ ] Experimental data available
- [ ] Numerical simulation comparison
- [ ] Literature values checked

### Error Analysis

- [ ] Relative error calculated
- [ ] Uncertainty propagation included
- [ ] Sensitivity analysis performed

### Physical Consistency

- [ ] Effective properties physically reasonable
- [ ] No unphysical values (negative, etc.)
- [ ] Monotonic behavior with volume fraction

**Validation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 10% |
| Phase Definition | ⭐⭐⭐⭐⭐ | 15% |
| Inclusion Geometry | ⭐⭐⭐⭐⭐ | 15% |
| Model Application | ⭐⭐⭐⭐⭐ | 15% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 10% |
| Bounds and Limits | ⭐⭐⭐⭐⭐ | 15% |
| Microstructure Effects | ⭐⭐⭐⭐⭐ | 10% |
| Validation | ⭐⭐⭐⭐⭐ | 10% |

**Overall Score:** ___ / 5 stars

---

## Approval Status

- [ ] **Approved** (≥ 4 stars overall, no section < 3)
- [ ] **Conditionally Approved** (≥ 3 stars, minor issues noted)
- [ ] **Rejected** (< 3 stars or critical issues)

### Issues Found

| Issue | Severity | Description |
|-------|----------|-------------|
| | Critical/Major/Minor | |

### Corrective Actions Required

- [ ]
- [ ]
- [ ]

**Reviewer:** ________________  
**Date:** ________________  
**Next Review:** ________________
