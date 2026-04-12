# Checklist: network-theorem-application

## Purpose

Comprehensive validation checklist for network theorem applications.

## Usage

Use this checklist when validating network theorem applications. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Maxwell Article Coverage

- [ ] Art. 287-300 (Networks) referenced
- [ ] Art. 301-320 (Conduction theory) referenced
- [ ] Theory classification assigned

### Theorem Selection

- [ ] Appropriate theorem selected for problem
- [ ] Theorem conditions verified
- [ ] Limitations acknowledged

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Thevenin/Norton Theorems

### Thevenin Equivalent

- [ ] Open-circuit voltage Voc calculated correctly
- [ ] Thevenin resistance Rth calculated correctly
- [ ] Polarity of Voc correct
- [ ] Load correctly reattached

### Norton Equivalent

- [ ] Short-circuit current Isc calculated correctly
- [ ] Norton resistance Rn = Rth verified
- [ ] Current source direction correct

### Source Transformation

- [ ] Vth = Isc × Rth verified
- [ ] Transformation valid (linear circuit)

**Thevenin/Norton Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Superposition Theorem

### Application

- [ ] All independent sources identified
- [ ] Each source considered separately
- [ ] Other voltage sources shorted
- [ ] Other current sources opened

### Result Combination

- [ ] Individual contributions summed algebraically
- [ ] Direction/polarity accounted for
- [ ] Final result verified

### Limitations

- [ ] Not applied to power calculations
- [ ] Linear circuit verified

**Superposition Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: Maximum Power Transfer

### Calculation

- [ ] Load resistance for maximum power identified
- [ ] For resistive load: RL = Rth
- [ ] For complex load: ZL = Zth* (conjugate match)

### Maximum Power

- [ ] Pmax = Vth²/(4×Rth) calculated correctly
- [ ] Efficiency at maximum power = 50%

### CGS Units

- [ ] Power in erg/s
- [ ] Resistance in statohm
- [ ] Voltage in statvolt

**Maximum Power Transfer Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Reciprocity Theorem

### Conditions

- [ ] Linear bilateral network verified
- [ ] Single source present
- [ ] No dependent sources (or handled correctly)

### Application

- [ ] Source and response locations interchanged
- [ ] Transfer impedances equal
- [ ] Result verified

**Reciprocity Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Tellegen's Theorem

### Application

- [ ] All branch voltages identified
- [ ] All branch currents identified
- [ ] Consistent reference directions

### Verification

- [ ] Sum of v·i products = 0
- [ ] Power balance verified
- [ ] Result independent of element types

**Tellegen Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Millman's Theorem

### Application

- [ ] Parallel voltage sources identified
- [ ] Equivalent voltage calculated: Veq = Σ(Vi/Ri) / Σ(1/Ri)
- [ ] Equivalent resistance calculated: 1/Req = Σ(1/Ri)

### CGS Units

- [ ] Voltages in statvolt
- [ ] Resistances in statohm
- [ ] Conductances in s⁻¹ (CGS)

**Millman Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 8: Verification

### Result Verification

- [ ] Results verified by alternate method
- [ ] SPICE or numerical verification (if applicable)
- [ ] Limiting cases checked

### Physical Reasonableness

- [ ] Voltages within expected range
- [ ] Currents within expected range
- [ ] Power balance verified
- [ ] No unphysical values

**Verification Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 10% |
| Thevenin/Norton | ⭐⭐⭐⭐⭐ | 15% |
| Superposition | ⭐⭐⭐⭐⭐ | 15% |
| Maximum Power Transfer | ⭐⭐⭐⭐⭐ | 10% |
| Reciprocity | ⭐⭐⭐⭐⭐ | 10% |
| Tellegen's Theorem | ⭐⭐⭐⭐⭐ | 10% |
| Millman's Theorem | ⭐⭐⭐⭐⭐ | 10% |
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
