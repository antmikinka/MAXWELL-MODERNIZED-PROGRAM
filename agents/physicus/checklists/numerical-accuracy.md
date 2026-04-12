# Checklist: Numerical Accuracy

## Purpose

Verify numerical implementations achieve expected accuracy, convergence, and stability. Numerical methods must be validated against analytical solutions.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Numerical Method | {FDTD|FEM|BEM|Spectral} |
| Order of Accuracy | {order} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Discretization Error

### Spatial Discretization
- [ ] Grid spacing documented (dx, dy, dz)
- [ ] Cells per wavelength ≥ 10 (for waves)
- [ ] Subcell features resolved
- [ ] Staircasing error quantified

### Temporal Discretization
- [ ] Time step documented (dt)
- [ ] CFL condition satisfied
- [ ] Temporal resolution adequate for dynamics
- [ ] Dispersion error quantified

### Order Verification
- [ ] Method order documented (1st, 2nd, 4th)
- [ ] Convergence rate matches theoretical order
- [ ] Richardson extrapolation applied (if useful)

## Convergence Tests

### Mesh Refinement
| Resolution | Error | Ratio | Expected Order |
|------------|-------|-------|----------------|
| h | E₁ | - | - |
| h/2 | E₂ | E₁/E₂ | {order} |
| h/4 | E₃ | E₂/E₃ | {order} |

- [ ] Error decreases with refinement
- [ ] Convergence rate matches theory
- [ ] Asymptotic range achieved

### Time Step Refinement
| dt | Error | Ratio | Expected Order |
|----|-------|-------|----------------|
| dt | E₁ | - | - |
| dt/2 | E₂ | E₁/E₂ | {order} |
| dt/4 | E₃ | E₂/E₃ | {order} |

- [ ] Temporal convergence verified
- [ ] Combined space-time convergence

## Stability Analysis

### CFL Condition
- [ ] CFL number documented
- [ ] Stability limit verified numerically
- [ ] Safety margin included (e.g., 0.99 × CFL_limit)

### Numerical Dispersion
- [ ] Phase error quantified
- [ ] Group velocity error
- [ ] Anisotropy in dispersion

### Long-Time Stability
- [ ] Energy drift < 1% per 1000 steps
- [ ] No growing modes
- [ ] Boundary reflections controlled

## Validation Against Analytical Solutions

### Point Source Tests
| Solution | Relative Error | Tolerance | Pass |
|----------|---------------|-----------|------|
| Point charge | {error} | 1e-4 | [ ] |
| Dipole | {error} | 1e-3 | [ ] |
| Line charge | {error} | 1e-2 | [ ] |

### Wave Propagation Tests
| Test | Error | Tolerance | Pass |
|------|-------|-----------|------|
| Plane wave speed | {error} | 1e-4 | [ ] |
| Plane wave attenuation | {error} | 1e-3 | [ ] |
| Waveguide cutoff | {error} | 1e-3 | [ ] |

### Cavity Resonance Tests
| Mode | Analytical f | Numerical f | Error | Pass |
|------|-------------|-------------|-------|------|
| TE₁₀₁ | {f_ana} | {f_num} | {err} | [ ] |
| TM₁₁₀ | {f_ana} | {f_num} | {err} | [ ] |

## Error Metrics

### L₂ Norm (RMS Error)
```
||e||₂ = sqrt(Σ |u_numerical - u_analytical|² / N)
```
- [ ] L₂ error computed
- [ ] Within tolerance

### L_∞ Norm (Maximum Error)
```
||e||_∞ = max |u_numerical - u_analytical|
```
- [ ] L_∞ error computed
- [ ] No localized large errors

### Relative Error
```
ε_rel = |u_num - u_ana| / |u_ana|
```
- [ ] Relative error < tolerance
- [ ] Handles small denominators correctly

## Numerical Diffusion/Dispersion

### Diffusion Error
- [ ] Amplitude decay quantified
- [ ] Matches theoretical numerical diffusion
- [ ] Acceptable for application

### Dispersion Error
- [ ] Phase velocity error vs. kΔx
- [ ] Group velocity error
- [ ] Anisotropy in different directions

## Round-off and Precision

### Floating Point
- [ ] Using float64 (double precision)
- [ ] Round-off error ~ 1e-15
- [ ] No catastrophic cancellation

### Accumulation
- [ ] Summation order optimized
- [ ] Kahan summation if needed
- [ ] Long simulations stable

## Performance Metrics

### Computational Cost
| Resolution | Time (s) | Memory (MB) |
|------------|----------|-------------|
| Coarse | {time} | {mem} |
| Medium | {time} | {mem} |
| Fine | {time} | {mem} |

- [ ] Scaling matches theory (O(N), O(N log N), O(N²))
- [ ] Memory within limits

### Parallel Efficiency
- [ ] Strong scaling measured
- [ ] Weak scaling measured
- [ ] Communication overhead acceptable

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Numerics Lead | | | |
| Implementation | | | |

## Issues Found

| Issue ID | Category | Severity | Description | Status |
|----------|----------|----------|-------------|--------|
| {id} | {convergence|stability|accuracy} | {HIGH|MEDIUM|LOW} | {description} | {OPEN|RESOLVED} |

## Overall Assessment

**Accuracy:** {EXCELLENT | GOOD | ACCEPTABLE | NEEDS_WORK}

**Convergence:** {VERIFIED | PARTIAL | NOT_VERIFIED}

**Stability:** {STABLE | CONDITIONALLY_STABLE | UNSTABLE}

**Recommendation:** {APPROVE | APPROVE_WITH_CHANGES | REJECT}
