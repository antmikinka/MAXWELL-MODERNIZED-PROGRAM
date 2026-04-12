# Checklist: hysteresis-model-validation

## Purpose

Comprehensive validation checklist for magnetic hysteresis models and measurements.

## Usage

Use this checklist when validating hysteresis models, measurements, or simulations. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Maxwell Article Coverage

- [ ] Art. 424-448 (Magnetization) referenced
- [ ] Art. 444-447 (Weber's molecular hypothesis) referenced
- [ ] Art. 371-423 (General magnetism) referenced
- [ ] Theory classification assigned

### Constitutive Relations

- [ ] B = μH = H + 4πI (CGS) correctly implemented
- [ ] Susceptibility defined: κ = (μ - 1)/4π
- [ ] Magnetization-current relation documented

### Energy Relations

- [ ] Energy density: W = (1/4π) ∫ H·dB
- [ ] Hysteresis loss per cycle documented
- [ ] Steinmetz equation parameters specified

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Hysteresis Loop Data

### Major Loop

- [ ] Saturation field (H_sat) specified
- [ ] Remanence (B_r) documented
- [ ] Coercivity (H_c) documented
- [ ] Loop area calculated (energy loss)

### Loop Characteristics

- [ ] Saturation magnetization (M_s) specified
- [ ] Squareness ratio (M_r/M_s) calculated
- [ ] Initial permeability (μ_i) documented
- [ ] Maximum permeability (μ_max) documented

### Minor Loops

- [ ] Minor loop amplitudes specified
- [ ] Recoil curves documented
- [ ] Number of minor loops defined

**Loop Data Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Hysteresis Model Selection

### Model Type

- [ ] Model selected (Preisach/Jiles-Atherton/Stoner-Wohlfarth)
- [ ] Model applicability justified
- [ ] Model limitations documented

### Preisach Model Parameters

- [ ] Distribution type specified
- [ ] Mean coercivity documented
- [ ] Coercivity distribution width
- [ ] Interaction parameters defined
- [ ] Irreversible fraction specified

### Jiles-Atherton Parameters

- [ ] Saturation magnetization (M_s)
- [ ] Domain coupling parameter (α)
- [ ] Domain wall energy parameter (a)
- [ ] Pinning parameter (k)
- [ ] Reversible fraction (c)

**Model Selection Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: CGS Unit Consistency

### Magnetic Field Units

- [ ] H field: oersted
- [ ] B field: gauss
- [ ] Magnetization I: emu/cm³
- [ ] Permeability: dimensionless

### Energy Units

- [ ] Energy density: erg/cm³
- [ ] Hysteresis loss: erg/cycle·cm³
- [ ] Steinmetz coefficient: appropriate units

### Unit Conversions

- [ ] 1 oersted = 79.577 A/m documented
- [ ] 1 gauss = 10⁻⁴ T documented
- [ ] 1 emu/cm³ = 1000 A/m documented

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Weber's Molecular Hypothesis

### Historical Context

- [ ] Weber's theory (Art. 444-447) explained
- [ ] Molecular magnet concept described
- [ ] Friction/drag mechanism documented
- [ ] Modern interpretation (domain theory) connected

### Model Connection

- [ ] Weber theory linked to hysteresis model
- [ ] Molecular hypothesis related to domain walls
- [ ] Historical-to-modern mapping documented

**Weber Connection Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Energy Loss Analysis

### Hysteresis Loss

- [ ] Loss per cycle calculated
- [ ] Loop area integration verified
- [ ] Frequency dependence documented

### Steinmetz Equation

- [ ] Exponent n specified (typically 1.6-2.0)
- [ ] Loss coefficient η documented
- [ ] B_max dependence verified

### Additional Losses

- [ ] Eddy current loss (if applicable)
- [ ] Anomalous loss (if applicable)
- [ ] Total loss summation

**Energy Loss Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Model Validation

### Parameter Fitting

- [ ] Fitting procedure documented
- [ ] Initial parameters specified
- [ ] Convergence achieved
- [ ] Parameter uncertainty quantified

### Goodness of Fit

- [ ] R² value reported
- [ ] RMSE calculated
- [ ] Maximum error documented
- [ ] Residual analysis performed

### Physical Validity

- [ ] Parameters within physical bounds
- [ ] Model predictions physical
- [ ] Limiting cases verified

**Validation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 15% |
| Hysteresis Loop Data | ⭐⭐⭐⭐⭐ | 15% |
| Model Selection | ⭐⭐⭐⭐⭐ | 15% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 15% |
| Weber Connection | ⭐⭐⭐⭐⭐ | 10% |
| Energy Loss Analysis | ⭐⭐⭐⭐⭐ | 15% |
| Model Validation | ⭐⭐⭐⭐⭐ | 15% |

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
