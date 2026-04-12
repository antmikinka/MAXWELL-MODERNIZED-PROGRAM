# Checklist: bridge-measurement-validation

## Purpose

Comprehensive validation checklist for bridge circuit measurements and analysis.

## Usage

Use this checklist when validating bridge measurement work. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Maxwell Article Coverage

- [ ] Art. 343-348 (Wheatstone bridge) referenced
- [ ] Art. 287-300 (Resistance) referenced
- [ ] Art. 541-570 (Inductance) referenced for AC bridges
- [ ] Theory classification assigned

### Bridge Theory

- [ ] Bridge topology correctly identified
- [ ] Balance condition correctly derived
- [ ] Complex impedance handling (for AC bridges)

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Bridge Configuration

### Arm Definitions

- [ ] All four arms correctly identified
- [ ] Impedance values documented
- [ ] Unknown arm correctly specified
- [ ] Standard arms traceable

### Source Configuration

- [ ] Source type correct (DC/AC)
- [ ] Source value documented
- [ ] Source impedance accounted for
- [ ] Frequency specified (for AC)

### Detector Configuration

- [ ] Detector type specified
- [ ] Detector impedance documented
- [ ] Sensitivity adequate for measurement

**Configuration Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Balance Condition

### Derivation

- [ ] Balance equation correctly derived
- [ ] Complex balance (for AC bridges)
- [ ] Both magnitude and phase conditions

### Specific Bridge Types

#### Wheatstone Bridge
- [ ] R1/R2 = R3/R4 verified
- [ ] Unknown = R3 × (R2/R1)

#### Maxwell Bridge
- [ ] L = R2 × R3 × C verified
- [ ] Balance independent of frequency

#### Kelvin Double Bridge
- [ ] Main ratio = Auxiliary ratio
- [ ] Lead resistance effect negligible

#### Schering Bridge
- [ ] Capacitance balance verified
- [ ] Loss angle correctly calculated

**Balance Condition Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: CGS Unit Consistency

### Unit Verification

- [ ] Resistance: statohm
- [ ] Capacitance: statfarad
- [ ] Inductance: cm or stathenry
- [ ] Voltage: statvolt
- [ ] Current: statampere

### Complex Quantities (AC Bridges)

- [ ] Impedance in statohm
- [ ] Admittance in s⁻¹ (CGS)
- [ ] Phase angles in degrees or radians

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Sensitivity Analysis

### Sensitivity Calculation

- [ ] Voltage sensitivity calculated
- [ ] Current sensitivity calculated
- [ ] Sensitivity at balance point evaluated

### Optimization

- [ ] Bridge ratios optimized for sensitivity
- [ ] Source voltage adequate
- [ ] Detector sensitivity adequate

**Sensitivity Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Measurement Procedure

### Setup

- [ ] Equipment calibrated
- [ ] Connections verified
- [ ] Environmental conditions recorded

### Balance Procedure

- [ ] Coarse balance achieved
- [ ] Fine balance achieved
- [ ] Multiple readings taken

### Reading and Calculation

- [ ] Standard values recorded
- [ ] Unknown calculated correctly
- [ ] Units consistent throughout

**Measurement Procedure Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Error Analysis

### Systematic Errors

- [ ] Lead resistance accounted for
- [ ] Contact resistance considered
- [ ] Thermal EMF minimized
- [ ] Stray capacitance/inductance considered

### Random Errors

- [ ] Multiple measurements taken
- [ ] Standard deviation calculated
- [ ] Outliers identified

### Uncertainty Budget

- [ ] All uncertainty sources identified
- [ ] Type A uncertainty evaluated
- [ ] Type B uncertainty evaluated
- [ ] Combined uncertainty calculated
- [ ] Expanded uncertainty reported (k=2)

**Error Analysis Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 8: Verification

### Independent Verification

- [ ] Result compared with expected value
- [ ] Result verified with alternate method
- [ ] Consistency check performed

### Physical Reasonableness

- [ ] Result within expected range
- [ ] Temperature coefficient reasonable
- [ ] No unphysical values

**Verification Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 15% |
| Bridge Configuration | ⭐⭐⭐⭐⭐ | 10% |
| Balance Condition | ⭐⭐⭐⭐⭐ | 20% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 10% |
| Sensitivity Analysis | ⭐⭐⭐⭐⭐ | 10% |
| Measurement Procedure | ⭐⭐⭐⭐⭐ | 15% |
| Error Analysis | ⭐⭐⭐⭐⭐ | 10% |
| Verification | ⭐⭐⭐⭐⭐ | 10% |

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
