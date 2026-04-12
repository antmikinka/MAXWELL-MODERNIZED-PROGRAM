# Checklist: dielectric-response-validation

## Purpose

Comprehensive validation checklist for dielectric response measurements and models.

## Usage

Use this checklist when validating dielectric characterization data, models, or simulations. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Maxwell Article Coverage

- [ ] Art. 50-62 (Dielectrics) referenced
- [ ] Art. 79-83 (Dielectric absorption, specific inductive capacity) referenced
- [ ] Art. 103-111 (Electrification, absorption) referenced
- [ ] Theory classification assigned

### Constitutive Relations

- [ ] D = KE = E + 4πP (CGS) correctly implemented
- [ ] Susceptibility defined: χ = (K - 1)/4π
- [ ] Polarization relation documented

### Maxwell Relations

- [ ] K = n² (optical limit) checked
- [ ] Frequency dispersion relation documented
- [ ] Temperature dependence modeled

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Static Dielectric Properties

### Permittivity Data

- [ ] Static permittivity (K_s) specified
- [ ] High-frequency permittivity (K_∞) documented
- [ ] Permittivity tensor (if anisotropic) complete

### Loss Properties

- [ ] Loss tangent (tan δ) specified
- [ ] Loss factor (ε'') calculated
- [ ] Quality factor (Q = 1/tan δ) computed

### Resistivity

- [ ] Volume resistivity documented (CGS: statohm·cm)
- [ ] Surface resistivity documented (CGS: statohm)
- [ ] Temperature dependence specified

**Static Properties Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Frequency Response

### Measurement Range

- [ ] Frequency range specified
- [ ] Number of data points documented
- [ ] Measurement temperature defined

### Dispersion Model

- [ ] Model selected (Debye/Cole-Cole/Havriliak-Negami/Jonscher)
- [ ] Model parameters fitted
- [ ] Fit quality documented

### Debye Parameters

- [ ] Static permittivity (ε_s)
- [ ] High-frequency permittivity (ε_∞)
- [ ] Relaxation time (τ)
- [ ] Distribution parameter (α, if Cole-Cole)

**Frequency Response Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: CGS Unit Consistency

### Electric Field Units

- [ ] Electric field E: statvolt/cm
- [ ] Electric displacement D: statvolt/cm (CGS)
- [ ] Polarization P: statvolt/cm (CGS)

### Material Properties

- [ ] Permittivity K: dimensionless
- [ ] Conductivity: s⁻¹ (electrostatic CGS)
- [ ] Resistivity: statohm·cm
- [ ] Capacitance: statfarad

### Unit Conversions

- [ ] 1 statvolt/cm = 29979 V/m documented
- [ ] 1 statfarad = 1.113×10⁻¹² F documented
- [ ] 1 statohm = 8.987×10¹¹ Ω documented

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Dielectric Absorption

### Absorption Characterization

- [ ] Absorption coefficient specified
- [ ] Absorption current decay modeled
- [ ] Time constants identified

### Maxwell-Wagner Polarization

- [ ] Interfacial polarization identified
- [ ] Heterogeneous medium characterized
- [ ] Relaxation time documented

### Absorption Models

- [ ] Curie-von Schweidler law checked
- [ ] Stretched exponential fit (if applicable)
- [ ] Power law exponent documented

**Absorption Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Breakdown Characteristics

### Breakdown Strength

- [ ] Intrinsic breakdown field specified
- [ ] Thermal breakdown field documented
- [ ] Practical breakdown field defined

### Breakdown Mechanism

- [ ] Dominant mechanism identified
- [ ] Temperature dependence documented
- [ ] Thickness effect accounted for

### Safety Margins

- [ ] Operating field specified
- [ ] Safety factor calculated
- [ ] Degradation mechanisms considered

**Breakdown Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Temperature Dependence

### Thermal Characterization

- [ ] Temperature range specified
- [ ] Reference temperature defined
- [ ] Temperature coefficients documented

### Dispersion Models

- [ ] Arrhenius parameters (if applicable)
  - [ ] Activation energy (E_a)
  - [ ] Pre-exponential factor (τ₀)
- [ ] VFT parameters (if applicable)
- [ ] Linear coefficients (if applicable)

### Thermal Limits

- [ ] Glass transition temperature (T_g)
- [ ] Melting/decomposition temperature
- [ ] Operating temperature range

**Temperature Dependence Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 8: Anisotropy (if applicable)

### Crystal System

- [ ] Crystal symmetry specified
- [ ] Principal axes identified
- [ ] Optic axis direction defined

### Tensor Properties

- [ ] K_xx, K_yy, K_zz specified
- [ ] Off-diagonal terms (if any)
- [ ] Principal values calculated

**Anisotropy Rating:** ⭐⭐⭐⭐⭐ (1-5) or N/A

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 15% |
| Static Properties | ⭐⭐⭐⭐⭐ | 15% |
| Frequency Response | ⭐⭐⭐⭐⭐ | 15% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 15% |
| Dielectric Absorption | ⭐⭐⭐⭐⭐ | 10% |
| Breakdown Characteristics | ⭐⭐⭐⭐⭐ | 10% |
| Temperature Dependence | ⭐⭐⭐⭐⭐ | 10% |
| Anisotropy | ⭐⭐⭐⭐⭐ | 10% |

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
