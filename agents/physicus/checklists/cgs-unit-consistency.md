# Checklist: CGS Unit Consistency

## Purpose

Verify all implementations use CGS units consistently and correctly. CGS is Maxwell's chosen system and must be maintained throughout.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Unit System Variant | {ESU|EMU|Gaussian} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## CGS Base Units

- [ ] **Length**: centimeter (cm)
- [ ] **Mass**: gram (g)
- [ ] **Time**: second (s)

## CGS Electrostatic Units (ESU)

### Charge and Current
- [ ] Charge: statcoulomb (cm³/²·g¹/²·s⁻¹)
- [ ] Current: statampere (statcoulomb/s)
- [ ] Charge density: statcoulomb/cm³
- [ ] Current density: statampere/cm²

### Field Quantities
- [ ] Electric field: statvolt/cm (dyne/statcoulomb)
- [ ] Potential: statvolt (erg/statcoulomb)
- [ ] Displacement D: statvolt/cm (same as E in CGS)
- [ ] Polarization P: statvolt/cm

### Constants
- [ ] Coulomb's law: F = q₁q₂/r² (no 4πε₀)
- [ ] Permittivity: dimensionless (relative to vacuum)
- [ ] ε_vacuum = 1 (CGS ESU)

## CGS Electromagnetic Units (EMU)

### Magnetic Quantities
- [ ] Magnetic field H: oersted
- [ ] Magnetic induction B: gauss
- [ ] In vacuum: B = H (CGS)
- [ ] Magnetization M: erg/(gauss·cm³)
- [ ] Magnetic moment: erg/gauss

### Current and Inductance
- [ ] Current: abampere (EMU)
- [ ] Inductance: cm (CGS EMU)
- [ ] 1 cm inductance = 10⁻⁹ H (SI)

### Constants
- [ ] Permeability: dimensionless (relative to vacuum)
- [ ] μ_vacuum = 1 (CGS EMU)

## CGS Gaussian (Mixed) Units

### Combined Electromagnetism
- [ ] E in statvolt/cm (ESU)
- [ ] B in gauss (EMU)
- [ ] Factor of c in Lorentz force: F = q(E + v/c × B)
- [ ] Factor of c in Maxwell's equations

### Maxwell's Equations (CGS Gaussian)
- [ ] ∇·D = 4πρ
- [ ] ∇·B = 0
- [ ] ∇×E = -(1/c)∂B/∂t
- [ ] ∇×H = (4π/c)J + (1/c)∂D/∂t

### Constitutive Relations
- [ ] D = E + 4πP (not D = ε₀E + P)
- [ ] B = H + 4πM (not B = μ₀(H + M))
- [ ] D = εE where ε is dimensionless
- [ ] B = μH where μ is dimensionless

## Speed of Light

- [ ] c = 2.99792458 × 10¹⁰ cm/s
- [ ] c appears explicitly in EM equations
- [ ] c² = 1/(εμ) in vacuum
- [ ] Wave speed: v = c/√(ε_r μ_r)

## Common Conversion Factors

### To SI
- [ ] Force: 1 dyne = 10⁻⁵ N
- [ ] Energy: 1 erg = 10⁻⁷ J
- [ ] Charge: 1 statcoulomb = 3.336 × 10⁻¹⁰ C
- [ ] Field: 1 statvolt/cm = 29979 V/m
- [ ] B-field: 1 gauss = 10⁻⁴ T

### From SI
- [ ] ε₀(SI) → 1/4π (CGS factor)
- [ ] μ₀(SI) → 4π/c² (CGS factor)
- [ ] Q(C) → Q/3.336e-10 (statcoulomb)

## Dimensional Analysis Checks

### Force Dimensions
- [ ] [F] = g·cm/s² (dyne)
- [ ] Electrostatic: [q²/r²] = (cm³·g/s⁴)/cm² = g·cm/s² ✓
- [ ] Magnetic: [qvB/c] has same dimensions ✓

### Energy Dimensions
- [ ] [U] = g·cm²/s² (erg)
- [ ] Electrostatic: [qV] = statcoulomb × statvolt = erg ✓
- [ ] Field energy: [E²V/8π] = erg ✓

### Field Dimensions
- [ ] [E] = [D] in CGS (both statvolt/cm)
- [ ] [B] = [H] in vacuum (both gauss/oersted)
- [ ] [P] = [M] = dipole moment per volume

## Common CGS Errors to Avoid

- [ ] Using ε₀ or μ₀ (these are SI concepts)
- [ ] Missing factors of 4π in source terms
- [ ] Missing factors of c in time-varying equations
- [ ] Confusing ESU and EMU for current
- [ ] Using SI constitutive relations

## Unit Documentation

- [ ] All functions document input units
- [ ] All functions document output units
- [ ] Constants defined with units
- [ ] Examples use correct CGS units
- [ ] Error messages mention expected units

## Validation Tests

| Test | Expected | Actual | Pass |
|------|----------|--------|------|
| Point charge field dimensions | statvolt/cm | | |
| Dipole moment dimensions | statcoulomb·cm | | |
| B-field from current dimensions | gauss | | |
| Energy density dimensions | erg/cm³ | | |
| Inductance dimensions | cm | | |

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Implementation | | | |

## Issues Found

| Issue | Severity | Description | Status |
|-------|----------|-------------|--------|
| {issue} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |
