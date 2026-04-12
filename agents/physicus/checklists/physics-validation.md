# Checklist: Physics Validation

## Purpose

Ensure physics implementations are correct, consistent with Maxwell's theory, and validated against known solutions.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Physics Domain | {domain} |
| Maxwell Part | {part} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Fundamental Physics Laws

### Electrostatics (Part I)
- [ ] **Coulomb's Law**: F = q₁q₂/r² verified for point charges
- [ ] **Gauss's Law**: ∮E·dA = 4πQ verified for closed surfaces
- [ ] **Superposition**: Field from multiple charges = sum of individual fields
- [ ] **Conservative Field**: ∇×E = 0 verified
- [ ] **Potential Relation**: E = -∇V verified

### Electrokinematics (Part II)
- [ ] **Ohm's Law**: J = σE verified in conductors
- [ ] **Continuity Equation**: ∂ρ/∂t + ∇·J = 0 verified
- [ ] **Joule Heating**: P = ∫J·E dV = I²R verified
- [ ] **Kirchhoff's Laws**: Current and voltage laws satisfied
- [ ] **Energy Conservation**: Input power = dissipated + stored

### Magnetism (Part III)
- [ ] **No Magnetic Monopoles**: ∇·B = 0 verified
- [ ] **Dipole Field**: B = (3(m·r̂)r̂ - m)/r³ verified
- [ ] **Constitutive Relation**: B = H + 4πI (CGS) verified
- [ ] **Demagnetizing Field**: H_demag = -NM verified for ellipsoids
- [ ] **Energy Density**: U = B²/(8π) verified

### Electromagnetism (Part IV)
- [ ] **Faraday's Law**: ∇×E = -(1/c)∂B/∂t verified
- [ ] **Ampère-Maxwell**: ∇×H = (4π/c)J + (1/c)∂D/∂t verified
- [ ] **Lorentz Force**: F = q(E + v/c × B) verified
- [ ] **Wave Equation**: ∇²E - (1/c²)∂²E/∂t² = 0 verified
- [ ] **Speed of Light**: c = 1/√(εμ) verified

## Analytical Solution Verification

### Point Sources
- [ ] Point charge field (Art. 44-49)
- [ ] Electric dipole field (Art. 69-71, 113-116)
- [ ] Magnetic dipole field (Art. 385-392)
- [ ] Current element field (Art. 475-490)

### Standard Geometries
- [ ] Conducting sphere (Art. 144-146)
- [ ] Dielectric sphere in uniform field
- [ ] Infinite line charge (Art. 126-127)
- [ ] Parallel plate capacitor (Art. 124)
- [ ] Solenoid field (Art. 675-677)
- [ ] Circular loop on axis (Art. 694-696)

### Time-Varying Solutions
- [ ] Plane wave in vacuum (Art. 790-791)
- [ ] Plane wave in dielectric (Art. 788-789)
- [ ] Wave in conductor (skin depth) (Art. 798-801)
- [ ] Transmission line wave (Art. 297-300)

## Boundary Conditions

### Electrostatic
- [ ] D_n discontinuity: D₂ₙ - D₁ₙ = 4πσ
- [ ] E_t continuity: E₂ₜ = E₁ₜ
- [ ] V continuity at interface
- [ ] Conductor surface: E perpendicular

### Magnetostatic
- [ ] B_n continuity: B₂ₙ = B₁ₙ
- [ ] H_t discontinuity: H₂ₜ - H₁ₜ = (4π/c)K

### Time-Varying
- [ ] All four boundary conditions from Art. 604
- [ ] PML absorption (>60 dB)
- [ ] PEC boundary: E_t = 0

## Limiting Cases

- [ ] **Static limit** (ω → 0): Reduces to electrostatics/magnetostatics
- [ ] **Vacuum limit** (ε→1, μ→1): Free space behavior
- [ ] **Perfect conductor** (σ→∞): E = 0 inside
- [ ] **Small distance**: Near-field behavior correct
- [ ] **Large distance**: Far-field/radiation behavior correct
- [ ] **Low frequency**: Quasi-static approximation valid
- [ ] **High frequency**: Wave behavior dominates

## Dimensional Analysis (CGS)

- [ ] All equations dimensionally consistent
- [ ] Force: dynes = g·cm/s²
- [ ] Charge: statcoulomb = cm³/²·g¹/²·s⁻¹
- [ ] Field: statvolt/cm = dyne/statcoulomb
- [ ] Magnetic field: gauss = oersted (in vacuum)
- [ ] Energy: ergs = g·cm²/s²

## Maxwell Article Traceability

| Article | Content | Implemented | Verified |
|---------|---------|-------------|----------|
| {article} | {description} | [ ] | [ ] |

## Experimental Comparison (if applicable)

- [ ] **Known constants**: Match handbook values
- [ ] **Material properties**: Match measured ε, μ, σ
- [ ] **Device performance**: Match specifications
- [ ] **Uncertainty**: Quantified and within bounds

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Physics Lead | | | |
| Implementation | | | |
| QA | | | |

## Issues Found

| Issue ID | Severity | Description | Article | Status |
|----------|----------|-------------|---------|--------|
| {id} | {HIGH|MEDIUM|LOW} | {description} | {article} | {OPEN|RESOLVED} |

## Overall Assessment

**Physics Correctness:** {EXCELLENT | GOOD | NEEDS_WORK | INADEQUATE}

**Validation Coverage:** {COMPLETE | MOSTLY_COMPLETE | PARTIAL | INADEQUATE}

**Recommendation:** {APPROVE | APPROVE_WITH_CHANGES | REJECT}
