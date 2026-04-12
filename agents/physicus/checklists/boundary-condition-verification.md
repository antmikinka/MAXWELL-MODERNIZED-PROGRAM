# Checklist: Boundary Condition Verification

## Purpose

Ensure boundary conditions are correctly implemented at all material interfaces. Boundary conditions are essential for unique solutions to Maxwell's equations.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Interface Types | {interfaces} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Electrostatic Boundary Conditions (Part I)

### Dielectric-Dielectric Interface
- [ ] **Normal D**: D₂ₙ - D₁ₙ = 4πσ_free
- [ ] **Tangential E**: E₂ₜ = E₁ₜ
- [ ] **Potential**: V continuous across interface
- [ ] **Field lines**: Refract according to ε₁/ε₂

### Conductor-Dielectric Interface
- [ ] **Inside conductor**: E = 0
- [ ] **Normal D**: Dₙ = 4πσ (surface charge)
- [ ] **Tangential E**: Eₜ = 0
- [ ] **Surface**: Equipotential

### Verification Tests
- [ ] Pillbox integral: ∮D·dA = 4πQ
- [ ] Loop integral: ∮E·dl = 0
- [ ] Surface charge from field discontinuity

## Magnetostatic Boundary Conditions (Part III)

### Magnetic Material Interface
- [ ] **Normal B**: B₂ₙ = B₁ₙ (continuous)
- [ ] **Tangential H**: H₂ₜ - H₁ₜ = (4π/c)K_free
- [ ] **No surface current**: H₂ₜ = H₁ₜ

### Perfect Magnetic Conductor
- [ ] **Inside**: B = 0
- [ ] **Normal B**: Bₙ = 0 at surface
- [ ] **Tangential H**: Hₜ = surface current

### Verification Tests
- [ ] Pillbox: ∮B·dA = 0 (no monopoles)
- [ ] Loop: ∮H·dl = (4π/c)I_enclosed

## Time-Varying Boundary Conditions (Part IV)

### General Interface (Art. 604)
- [ ] **Normal D**: D₂ₙ - D₁ₙ = 4πσ
- [ ] **Normal B**: B₂ₙ = B₁ₙ
- [ ] **Tangential E**: E₂ₜ = E₁ₜ
- [ ] **Tangential H**: H₂ₜ - H₁ₜ = (4π/c)K

### Perfect Electric Conductor (PEC)
- [ ] **Inside**: E = 0, B = 0
- [ ] **Tangential E**: Eₜ = 0 at surface
- [ ] **Normal B**: Bₙ = 0 at surface
- [ ] **Surface current**: K = (c/4π) n̂ × H

### Absorbing Boundaries (PML)
- [ ] **Reflection**: < 10⁻⁶ (60 dB absorption)
- [ ] **Impedance matching**: No artificial reflection
- [ ] **Evanescent waves**: Properly absorbed

## Numerical Boundary Implementation

### FDTD Boundaries
- [ ] **Yee cell**: Fields on correct faces/edges
- [ ] **PEC**: E_tangent set to 0
- [ ] **PMC**: H_tangent set to 0
- [ ] **PML**: Graded absorption profile

### FEM Boundaries
- [ ] **Essential BC**: V specified (Dirichlet)
- [ ] **Natural BC**: ∂V/∂n specified (Neumann)
- [ ] **Mixed BC**: Robin condition
- [ ] **Periodic**: Field matching

## Special Boundary Conditions

### Symmetry Planes
- [ ] **Electric symmetry**: E_normal = 0, E_tangent free
- [ ] **Magnetic symmetry**: H_normal = 0, H_tangent free
- [ ] **Periodic**: Field(r) = Field(r + period)

### Open Boundaries
- [ ] **Radiation condition**: Outgoing waves only
- [ ] **Far-field**: Match analytical asymptotics
- [ ] **Infinite element**: Proper decay

### Interface with Sources
- [ ] **Point charge**: Field singularity handled
- [ ] **Current sheet**: H discontinuity = (4π/c)K
- [ ] **Dipole layer**: V discontinuity

## Verification Tests

| Test ID | Interface | Condition | Expected | Measured | Pass |
|---------|-----------|-----------|----------|----------|------|
| BC-001 | Dielectric | D_n jump | 4πσ | {measured} | [ ] |
| BC-002 | Dielectric | E_t cont. | 0 diff | {measured} | [ ] |
| BC-003 | Conductor | E_t = 0 | < tol | {measured} | [ ] |
| BC-004 | Magnetic | B_n cont. | 0 diff | {measured} | [ ] |
| BC-005 | PEC | E_t = 0 | < tol | {measured} | [ ] |
| BC-006 | PML | Reflection | < 1e-6 | {measured} | [ ] |

## Multi-Region Problems

### Region Connectivity
- [ ] All interfaces identified
- [ ] Material assignments correct
- [ ] No gaps or overlaps

### Interface Conditions
- [ ] All four BCs checked at each interface
- [ ] Surface charges/currents included
- [ ] Corner/edge conditions handled

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Implementation | | | |

## Issues Found

| Issue ID | Interface | Severity | Description | Status |
|----------|-----------|----------|-------------|--------|
| {id} | {interface} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |

## Overall Assessment

**Boundary Condition Accuracy:** {EXCELLENT | GOOD | ACCEPTABLE | NEEDS_WORK}

**Numerical Implementation:** {CORRECT | MINOR_ISSUES | MAJOR_ISSUES}

**Recommendation:** {APPROVE | APPROVE_WITH_CHANGES | REJECT}
