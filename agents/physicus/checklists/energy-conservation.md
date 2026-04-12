# Checklist: Energy Conservation

## Purpose

Verify energy conservation in all electromagnetic implementations. Energy methods provide powerful validation and are central to Maxwell's theory.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Physics Domain | {domain} |
| System Type | {static|dynamic|mixed} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Electrostatic Energy (Part I)

### Energy Formulations
- [ ] **Volume integral**: U = (1/8π) ∫ E² dV
- [ ] **Charge-potential**: U = (1/2) ∫ ρV dV
- [ ] **Discrete charges**: U = Σ qᵢqⱼ/(2rᵢⱼ)
- [ ] **Capacitor**: U = (1/2)CV²

### Verification Tests
- [ ] Both formulations give same result
- [ ] Energy is positive definite
- [ ] Self-energy of point charges handled correctly
- [ ] Interaction energy matches F = -∇U

### Maxwell Stress Tensor
- [ ] Stress tensor: Tᵢⱼ = (1/4π)(EᵢEⱼ - (1/2)δᵢⱼE²)
- [ ] Force from stress: F = ∮ T · dA
- [ ] Energy from stress: U = ∫ (E²/8π) dV
- [ ] Articles 103-110 verified

## Magnetostatic Energy (Part III)

### Energy Formulations
- [ ] **Field energy**: U = (1/8π) ∫ B·H dV
- [ ] **Circuit energy**: U = (1/2)LI²
- [ ] **Dipole energy**: U = -m·B
- [ ] **Mutual energy**: U = MI₁I₂

### Verification Tests
- [ ] Field and circuit formulations agree
- [ ] Energy minimum for stable equilibrium
- [ ] Work done in magnetization matches energy change

## Electrokinetic Energy (Part II, IV)

### Energy in Current Systems
- [ ] **Joule heating**: P = ∫ J·E dV = I²R
- [ ] **Power input**: P = VI
- [ ] **Energy balance**: Input = dissipated + stored

### Coupled Circuits
- [ ] **Total energy**: U = (1/2)L₁I₁² + (1/2)L₂I₂² + MI₁I₂
- [ ] **Energy conservation**: dU/dt = P_in - P_loss
- [ ] **Reciprocity**: M₁₂ = M₂₁

## Time-Varying Fields (Part IV)

### Poynting Theorem
- [ ] **Poynting vector**: S = (c/4π) E × H
- [ ] **Energy continuity**: ∂u/∂t + ∇·S = -J·E
- [ ] **Energy density**: u = (1/8π)(E² + B²)
- [ ] **Power flow**: P = ∫ S · dA

### Verification Tests
- [ ] Poynting theorem satisfied numerically
- [ ] Energy flux matches input power
- [ ] Absorbed power matches Joule heating
- [ ] Radiated power computed correctly

### Wave Energy
- [ ] **Plane wave**: |S| = (c/8π)E₀²
- [ ] **Energy equipartition**: Electric = Magnetic
- [ ] **Intensity**: I = |<S>| (time average)
- [ ] **Radiation pressure**: p = I/c (absorbing), p = 2I/c (reflecting)

## Numerical Energy Conservation

### FDTD Simulations
- [ ] Total energy tracked at each step
- [ ] Energy drift < 1% over full simulation
- [ ] PML absorption accounted for
- [ ] Source injection energy computed

### FEM Simulations
- [ ] Weak form conserves energy
- [ ] Boundary terms handled correctly
- [ ] Time integration is energy-conserving

## Thermoelectric Energy (Part II)

### Energy Conversion
- [ ] **Seebeck**: Heat → Electricity
- [ ] **Peltier**: Electricity → Heat (reversible)
- [ ] **Thomson**: Distributed heating/cooling
- [ ] **Energy balance**: All terms accounted for

### Efficiency
- [ ] Carnot limit respected
- [ ] Figure of merit ZT computed correctly

## Mechanical Work

### Force from Energy
- [ ] **Virtual work**: F = -∂U/∂x
- [ ] **Torque**: τ = -∂U/∂θ
- [ ] **Maxwell stress**: Verified against force

### Actuator Energy
- [ ] Electrical input = mechanical work + loss
- [ ] Efficiency computed correctly

## Validation Tests

| Test | Expected | Measured | Error | Pass |
|------|----------|----------|-------|------|
| Point charge self-energy | {expected} | {measured} | {error} | [ ] |
| Capacitor energy | {expected} | {measured} | {error} | [ ] |
| Inductor energy | {expected} | {measured} | {error} | [ ] |
| Poynting flux | {expected} | {measured} | {error} | [ ] |
| Joule heating | {expected} | {measured} | {error} | [ ] |

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Implementation | | | |

## Issues Found

| Issue | Severity | Description | Status |
|-------|----------|-------------|--------|
| {issue} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |

## Overall Assessment

**Energy Conservation:** {EXACT | WITHIN_TOLERANCE | DRIFT_DETECTED | VIOLATED}

**Recommendation:** {APPROVE | APPROVE_WITH_CHANGES | REJECT}
