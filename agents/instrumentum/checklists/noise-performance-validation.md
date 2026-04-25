# Checklist: noise-performance-validation

## Purpose

Comprehensive validation checklist for instrument noise performance verification.

## Usage

Use this checklist when validating instrument noise performance. Rate each section 1-5 stars.

---

## Section 1: Noise Theory

### Maxwell/Physics Foundation

- [ ] Noise mechanisms correctly identified
- [ ] Physical principles correctly applied
- [ ] Theory classification assigned

### Noise Types Identified

- [ ] Thermal (Johnson) noise considered
- [ ] Shot noise considered
- [ ] Flicker (1/f) noise considered
- [ ] Vibration/microphonic noise considered

**Noise Theory Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Thermal Noise Analysis

### Johnson Noise Calculation

- [ ] Formula correct: e_n² = 4kTRΔf
- [ ] Temperature correctly specified
- [ ] Resistance values correct
- [ ] Bandwidth correctly defined

### Thermal Noise Measurement

- [ ] Measurement setup correct
- [ ] Bandwidth limiting applied
- [ ] Background noise subtracted
- [ ] Multiple measurements averaged

### Theory vs. Measurement

- [ ] Calculated and measured agree
- [ ] Discrepancies explained
- [ ] Corrections applied if needed

**Thermal Noise Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Shot Noise Analysis

### Shot Noise Calculation

- [ ] Formula correct: i_n² = 2qIΔf
- [ ] Current values correct
- [ ] Charge value correct (CGS: 4.803×10⁻¹⁰ statC)
- [ ] Bandwidth correctly defined

### Shot Noise Measurement

- [ ] DC bias current measured
- [ ] AC noise current measured
- [ ] Spectrum analyzed

### Theory vs. Measurement

- [ ] Calculated and measured agree
- [ ] Discrepancies explained

**Shot Noise Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: Flicker Noise Analysis

### Flicker Noise Characterization

- [ ] 1/f region identified
- [ ] Corner frequency determined
- [ ] Noise coefficient measured

### Flicker Noise Measurement

- [ ] Low-frequency measurements taken
- [ ] Log-log plot created
- [ ] Slope verified (~-10 dB/decade)

### Flicker Noise Mitigation

- [ ] Chopper stabilization (if used)
- [ ] Low-frequency filtering
- [ ] Modulation techniques

**Flicker Noise Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Vibration Noise Analysis

### Microphonic Sensitivity

- [ ] Vibration sensitivity measured
- [ ] Frequency response characterized
- [ ] Directional dependence measured

### Vibration Environment

- [ ] Ambient vibration measured
- [ ] Isolation effectiveness verified
- [ ] Critical frequencies identified

### Vibration Mitigation

- [ ] Isolation mounting used
- [ ] Damping applied
- [ ] Sensitive components secured

**Vibration Noise Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Total Noise Performance

### Noise Summation

- [ ] All noise sources identified
- [ ] RSS summation correctly applied
- [ ] Correlated noise handled correctly

### Total Noise Measurement

- [ ] Total noise measured
- [ ] Measurement bandwidth documented
- [ ] Measurement conditions recorded

### Signal-to-Noise Ratio

- [ ] SNR calculated
- [ ] SNR measured
- [ ] SNR adequate for application

**Total Noise Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Minimum Detectable Signal

### MDS Calculation

- [ ] MDS = SNR_min × noise / sensitivity
- [ ] SNR_min criterion defined (typically 1-3)
- [ ] All parameters correct

### MDS Verification

- [ ] MDS verified experimentally
- [ ] Test signal applied
- [ ] Detection confirmed

### Integration Improvement

- [ ] Integration time effects characterized
- [ ] √t improvement verified
- [ ] Optimal integration time determined

**MDS Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 8: CGS Unit Consistency

### Unit Verification

- [ ] All noise values in CGS units
- [ ] Conversions documented
- [ ] Dimensional analysis verified

### CGS Constants

- [ ] Boltzmann constant: 1.381×10⁻¹⁶ erg/K
- [ ] Elementary charge: 4.803×10⁻¹⁰ statC
- [ ] Values correctly used

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Noise Theory | ⭐⭐⭐⭐⭐ | 10% |
| Thermal Noise | ⭐⭐⭐⭐⭐ | 15% |
| Shot Noise | ⭐⭐⭐⭐⭐ | 10% |
| Flicker Noise | ⭐⭐⭐⭐⭐ | 10% |
| Vibration Noise | ⭐⭐⭐⭐⭐ | 10% |
| Total Noise | ⭐⭐⭐⭐⭐ | 15% |
| MDS | ⭐⭐⭐⭐⭐ | 15% |
| Unit Consistency | ⭐⭐⭐⭐⭐ | 15% |

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
