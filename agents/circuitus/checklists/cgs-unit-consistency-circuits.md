# Checklist: cgs-unit-consistency-circuits

## Purpose

Comprehensive validation checklist for CGS unit consistency in circuit analysis.

## Usage

Use this checklist when validating that all circuit quantities are in proper CGS units. Rate each section 1-5 stars.

---

## Section 1: Electric Quantities (ESU)

### Voltage/Potential

- [ ] Unit: statvolt
- [ ] Typical range: 10⁻⁶ to 10⁶ statvolt
- [ ] Conversion: 1 statvolt = 299.79 V

### Current

- [ ] Unit: statampere
- [ ] Typical range: 10⁻¹⁰ to 10¹⁰ statampere
- [ ] Conversion: 1 statampere = 3.336×10⁻¹⁰ A

### Charge

- [ ] Unit: statcoulomb
- [ ] Typical range: 10⁻¹⁰ to 10¹⁰ statcoulomb
- [ ] Conversion: 1 statcoulomb = 3.336×10⁻¹⁰ C

### Resistance

- [ ] Unit: statohm
- [ ] Typical range: 10⁻¹² to 10¹² statohm
- [ ] Conversion: 1 statohm = 8.988×10¹¹ Ω

### Conductance

- [ ] Unit: s⁻¹ (electrostatic CGS)
- [ ] Relation: 1/statohm
- [ ] Conversion: 1 s⁻¹ (CGS) = 8.988×10¹¹ S

**Electric Quantities Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Circuit Element Parameters

### Capacitance

- [ ] Unit: statfarad
- [ ] Typical range: 10⁻¹⁵ to 10⁻³ statfarad
- [ ] Conversion: 1 statfarad = 1.113×10⁻¹² F
- [ ] Relation: C = Q/V (statfarad = statcoulomb/statvolt)

### Inductance

- [ ] Unit: cm (CGS electromagnetic) or stathenry
- [ ] Typical range: 10⁻⁴ to 10⁶ cm
- [ ] Conversion: 1 cm = 1.113×10⁻¹² H
- [ ] Relation: V = L·dI/dt (consistent units)

### Mutual Inductance

- [ ] Unit: cm (same as self-inductance)
- [ ] Coupling coefficient: 0 ≤ k ≤ 1 (dimensionless)
- [ ] Relation: M = k×√(L₁×L₂)

**Element Parameters Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Power and Energy

### Power

- [ ] Unit: erg/s
- [ ] Typical range: 10⁻⁷ to 10¹⁴ erg/s
- [ ] Conversion: 1 erg/s = 10⁻⁷ W
- [ ] Relations: P = V×I = I²×R = V²/R

### Energy

- [ ] Unit: erg
- [ ] Typical range: 10⁻¹⁰ to 10¹⁴ erg
- [ ] Conversion: 1 erg = 10⁻⁷ J
- [ ] Relations: W = ∫P dt

### Electric Energy (Capacitor)

- [ ] Formula: W = (1/2)×C×V²
- [ ] Units: statfarad × statvolt² = erg

### Magnetic Energy (Inductor)

- [ ] Formula: W = (1/2)×L×I²
- [ ] Units: cm × statampere² = erg (verify)

**Power and Energy Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: AC Circuit Quantities

### Impedance

- [ ] Unit: statohm
- [ ] Complex form: Z = R + jX
- [ ] Magnitude: |Z| in statohm

### Reactance

- [ ] Inductive: XL = ωL (statohm)
- [ ] Capacitive: XC = 1/(ωC) (statohm)
- [ ] Angular frequency: ω in rad/s

### Admittance

- [ ] Unit: s⁻¹ (CGS)
- [ ] Complex form: Y = G + jB
- [ ] Relation: Y = 1/Z

### Complex Power

- [ ] Unit: erg/s
- [ ] Form: S = P + jQ
- [ ] Magnitude: |S| in erg/s
- [ ] Relation: S = V×I* (conjugate)

**AC Quantities Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Transmission Line Parameters

### Distributed Parameters

- [ ] R: statohm/cm
- [ ] L: cm/cm (dimensionless in CGS)
- [ ] G: s⁻¹/cm
- [ ] C: statfarad/cm

### Propagation Constant

- [ ] γ: cm⁻¹
- [ ] α (attenuation): Np/cm or dB/cm
- [ ] β (phase): rad/cm

### Characteristic Impedance

- [ ] Z0: statohm
- [ ] Formula: Z0 = √(L/C) (lossless)

**Transmission Line Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Dimensional Analysis

### Key Relations Check

- [ ] V = I×R: statvolt = statampere × statohm ✓
- [ ] P = V×I: erg/s = statvolt × statampere ✓
- [ ] W = (1/2)×C×V²: erg = statfarad × statvolt² ✓
- [ ] V = L×dI/dt: statvolt = cm × statampere/s ✓

### Time Constants

- [ ] τ = RC: seconds = statohm × statfarad ✓
- [ ] τ = L/R: seconds = cm/statohm (verify CGS)

### Resonant Frequency

- [ ] ω₀ = 1/√(LC): rad/s = 1/√(cm × statfarad) ✓

**Dimensional Analysis Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Unit Conversions

### SI to CGS Conversions Documented

- [ ] Voltage: V ÷ 299.79 = statvolt
- [ ] Current: A ÷ 3.336×10⁻¹⁰ = statampere
- [ ] Resistance: Ω ÷ 8.988×10¹¹ = statohm
- [ ] Capacitance: F ÷ 1.113×10⁻¹² = statfarad
- [ ] Inductance: H ÷ 1.113×10⁻¹² = cm
- [ ] Power: W ÷ 10⁻⁷ = erg/s
- [ ] Energy: J ÷ 10⁻⁷ = erg

### Conversion Verification

- [ ] Sample conversions verified
- [ ] Round-trip conversions consistent
- [ ] No mixed unit systems in final results

**Conversion Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Electric Quantities | ⭐⭐⭐⭐⭐ | 15% |
| Element Parameters | ⭐⭐⭐⭐⭐ | 15% |
| Power and Energy | ⭐⭐⭐⭐⭐ | 15% |
| AC Circuit Quantities | ⭐⭐⭐⭐⭐ | 15% |
| Transmission Line | ⭐⭐⭐⭐⭐ | 10% |
| Dimensional Analysis | ⭐⭐⭐⭐⭐ | 15% |
| Unit Conversions | ⭐⭐⭐⭐⭐ | 15% |

**Overall Score:** ___ / 5 stars

---

## Approval Status

- [ ] **Approved** (≥ 4 stars overall, no section < 3)
- [ ] **Conditionally Approved** (≥ 3 stars, minor issues noted)
- [ ] **Rejected** (< 3 stars or critical issues)

### Critical Issues (Automatic Rejection)

- [ ] Mixed unit systems detected
- [ ] Dimensional inconsistency found
- [ ] Conversion errors identified

**Reviewer:** ________________  
**Date:** ________________  
**Next Review:** ________________
