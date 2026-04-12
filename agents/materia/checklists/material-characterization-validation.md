# Checklist: material-characterization-validation

## Purpose

Comprehensive validation checklist for material characterization data quality and completeness.

## Usage

Use this checklist when validating material characterization results. Rate each section 1-5 stars.

---

## Section 1: Data Completeness

### Required Properties

- [ ] Material name and classification specified
- [ ] All relevant properties measured (electrical, magnetic, mechanical)
- [ ] Temperature conditions documented
- [ ] Frequency range specified (if AC properties)
- [ ] Sample geometry documented

### Metadata

- [ ] Source/reference cited
- [ ] Measurement date recorded
- [ ] Laboratory/equipment identified
- [ ] Operator information (if applicable)

**Completeness Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: CGS Unit Consistency

### Unit Verification

- [ ] All electrical properties in CGS units
  - [ ] Permittivity: dimensionless (K)
  - [ ] Conductivity: s⁻¹ (electrostatic CGS)
  - [ ] Electric field: statvolt/cm
  - [ ] Current density: statampere/cm²

- [ ] All magnetic properties in CGS units
  - [ ] Permeability: dimensionless (mu)
  - [ ] Magnetic field: oersted
  - [ ] Magnetic induction: gauss
  - [ ] Magnetization: emu/cm³

- [ ] All mechanical properties in CGS units
  - [ ] Stress/Strength: dyne/cm²
  - [ ] Modulus: dyne/cm²
  - [ ] Energy: erg
  - [ ] Density: g/cm³

### Unit Conversions

- [ ] Conversion factors documented
- [ ] SI-to-CGS conversions verified
- [ ] Mixed unit systems avoided

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Maxwell Article Traceability

### Citation Completeness

- [ ] Relevant Maxwell articles identified
- [ ] Citations match property types:
  - [ ] Electrostatics: Art. 1-229
  - [ ] Electrokinematics: Art. 230-370
  - [ ] Magnetism: Art. 371-474
  - [ ] Electromagnetism: Art. 475-866

### Theory Classification

- [ ] Maxwell's original text identified
- [ ] User's extensions marked (DO NOT CHANGE)
- [ ] Standard math implementations noted

**Traceability Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: Measurement Quality

### Uncertainty Quantification

- [ ] Measurement uncertainty reported
- [ ] Confidence level specified (e.g., 95%)
- [ ] Systematic errors addressed
- [ ] Random errors quantified

### Calibration

- [ ] Equipment calibration current
- [ ] Traceability to standards
- [ ] Reference materials used

### Repeatability

- [ ] Multiple measurements taken
- [ ] Standard deviation reported
- [ ] Outliers identified/handled

**Measurement Quality Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Physical Consistency

### Bounds Check

- [ ] Permittivity > 1 (for passive materials)
- [ ] Permeability > 0
- [ ] Conductivity > 0 (for conductors)
- [ ] Loss tangent in valid range (0-1 typically)

### Maxwell Relations

- [ ] K ≈ n² checked (optical-high frequency)
- [ ] Constitutive relations satisfied: D = K·E = E + 4πP
- [ ] B = μ·H = H + 4πI (magnetic)

### Temperature/Frequency Behavior

- [ ] Temperature dependence physical
- [ ] Frequency dispersion follows expected model
- [ ] No unphysical discontinuities

**Physical Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Data Completeness | ⭐⭐⭐⭐⭐ | 20% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 20% |
| Maxwell Traceability | ⭐⭐⭐⭐⭐ | 20% |
| Measurement Quality | ⭐⭐⭐⭐⭐ | 20% |
| Physical Consistency | ⭐⭐⭐⭐⭐ | 20% |

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
