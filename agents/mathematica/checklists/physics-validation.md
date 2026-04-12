# Checklist: Physics Validation

## Purpose

Ensure mathematical implementations are physically valid and consistent with Maxwell's theory.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Physics Domain | {domain} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Fundamental Physics Laws

### Conservation Laws
- [ ] **Charge Conservation**: ∂ρ/∂t + ∇·J = 0
- [ ] **Energy Conservation**: Energy balance verified
- [ ] **Momentum Conservation**: Momentum balance (if applicable)
- [ ] **Flux Conservation**: Divergence theorem satisfied

### Maxwell's Equations Consistency
- [ ] **Gauss's Law**: ∇·E = 4πρ (CGS)
- [ ] **No Magnetic Monopoles**: ∇·B = 0
- [ ] **Faraday's Law**: ∇×E = -(1/c)∂B/∂t
- [ ] **Ampère-Maxwell**: ∇×B = (4π/c)J + (1/c)∂E/∂t

## Boundary Conditions

- [ ] **Continuity**: Field continuity at interfaces
- [ ] **Discontinuity**: Correct discontinuity for surface sources
- [ ] **Interface Conditions**: Proper matching at boundaries
- [ ] **Far-Field**: Correct behavior at infinity

## Limiting Cases

- [ ] **Static Limit**: Correct static limit (ω → 0)
- [ ] **Vacuum Limit**: Correct vacuum behavior
- [ ] **Small Parameter**: Correct asymptotic behavior
- [ ] **Large Parameter**: Correct limiting behavior
- [ ] **Symmetry Limits**: Correct behavior under symmetry

## Analytical Solutions

- [ ] **Point Charge**: Verified for point source
- [ ] **Dipole Field**: Verified for dipole
- [ ] **Uniform Field**: Verified for uniform field
- [ ] **Spherical Symmetry**: Verified for spherical case
- [ ] **Planar Symmetry**: Verified for planar case

## Dimensional Analysis

- [ ] **Dimension Check**: All equations dimensionally consistent
- [ ] **Scaling**: Correct scaling with parameters
- [ ] **Unit Conversion**: CGS/SI conversion verified

## Physical Interpretation

- [ ] **Sign Convention**: Signs match physics conventions
- [ ] **Direction**: Vector directions physically correct
- [ ] **Magnitude**: Orders of magnitude reasonable
- [ ] **Singularities**: Physical singularities handled

## Maxwell Article Traceability

| Article | Content | Verified |
|---------|---------|----------|
| {article} | {description} | [ ] |

## Experimental Comparison (if applicable)

- [ ] **Known Data**: Compared with experimental data
- [ ] **Uncertainty**: Uncertainty quantified
- [ ] **Agreement**: Within experimental uncertainty

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Math Lead | | | |
| Reviewer | | | |

## Issues Found

| Issue | Severity | Status |
|-------|----------|--------|
| {issue} | {HIGH|MEDIUM|LOW} | {OPEN|RESOLVED} |
