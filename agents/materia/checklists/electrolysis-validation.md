# Checklist: electrolysis-validation

## Purpose

Comprehensive validation checklist for electrolysis simulations and experimental data.

## Usage

Use this checklist when validating electrolysis models, simulations, or experimental results. Rate each section 1-5 stars.

---

## Section 1: Theoretical Foundation

### Maxwell Article Coverage

- [ ] Art. 236-238 (Electrolysis laws) referenced
- [ ] Art. 269-286 (Electrochemical effects) referenced
- [ ] Art. 230-235 (Electrokinematics) referenced
- [ ] Theory classification assigned (maxwell_original/user_original/standard_math)

### Governing Equations

- [ ] Nernst-Planck equation correctly formulated
- [ ] Continuity equation implemented: div(J) = -∂ρ/∂t
- [ ] Poisson equation for electric field: div(E) = 4πρ (CGS)
- [ ] Charge conservation enforced

### Boundary Conditions

- [ ] Electrode boundary conditions specified
- [ ] Bulk boundary conditions defined
- [ ] Interface conditions documented
- [ ] Initial conditions stated

**Theoretical Foundation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 2: Electrolytic Cell Definition

### Geometry

- [ ] Cell geometry fully specified
- [ ] Electrode dimensions documented
- [ ] Electrode separation defined
- [ ] Electrolyte volume specified

### Electrodes

- [ ] Anode material identified
- [ ] Cathode material identified
- [ ] Half-reactions documented
- [ ] Standard potentials specified (with reference)

### Electrolyte

- [ ] Solvent identified
- [ ] Dielectric constant specified
- [ ] Viscosity documented
- [ ] Temperature defined

**Cell Definition Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 3: Ion Transport Parameters

### Ion Properties

- [ ] All ion species identified
- [ ] Charge numbers (z) specified
- [ ] Mobilities documented (CGS: cm²/statvolt·s)
- [ ] Diffusion coefficients provided (CGS: cm²/s)

### Concentration Data

- [ ] Bulk concentrations specified
- [ ] Initial concentration profile defined
- [ ] Concentration limits checked (solubility)

### Transport Relations

- [ ] Einstein relation checked: D = (kT/q)·u
- [ ] Transport numbers sum to 1
- [ ] Ionic strength calculated

**Transport Parameters Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 4: CGS Unit Consistency

### Electrochemical Units

- [ ] Potential: statvolt (1 statvolt = 299.79 V)
- [ ] Current: statampere (1 statampere = 3.336×10⁻¹⁰ A)
- [ ] Current density: statampere/cm²
- [ ] Concentration: mol/cm³

### Derived Quantities

- [ ] Electric field: statvolt/cm
- [ ] Charge density: statcoulomb/cm³
- [ ] Mobility: cm²/statvolt·s
- [ ] Diffusion coefficient: cm²/s

### Unit Conversions

- [ ] All conversions documented
- [ ] Conversion factors verified
- [ ] No mixed unit systems

**Unit Consistency Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 5: Electrochemical Kinetics

### Overpotential

- [ ] Activation overpotential modeled
- [ ] Concentration overpotential included
- [ ] Ohmic drop accounted for
- [ ] Total overpotential balanced

### Butler-Volmer Equation

- [ ] Exchange current density specified
- [ ] Transfer coefficients defined
- [ ] Temperature dependence included

### Mass Transport Limitations

- [ ] Limiting current density calculated
- [ ] Concentration polarization modeled
- [ ] Diffusion layer thickness defined

**Kinetics Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 6: Numerical Implementation

### Discretization

- [ ] Mesh resolution documented
- [ ] Time step specified
- [ ] Convergence criteria defined

### Solver Settings

- [ ] Solver type identified
- [ ] Linear solver specified
- [ ] Tolerance settings documented
- [ ] Maximum iterations defined

### Numerical Stability

- [ ] CFL condition satisfied (if transient)
- [ ] Peclet number checked
- [ ] Grid independence verified

**Numerical Implementation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Section 7: Validation & Verification

### Code Verification

- [ ] Manufactured solution test passed
- [ ] Conservation laws verified
- [ ] Boundary conditions verified

### Model Validation

- [ ] Comparison with experimental data
- [ ] Literature values checked
- [ ] Limiting cases verified

### Output Quantities

- [ ] Current density profiles
- [ ] Concentration distributions
- [ ] Potential field
- [ ] Overpotential components
- [ ] Faradaic efficiency

**Validation Rating:** ⭐⭐⭐⭐⭐ (1-5)

---

## Overall Assessment

| Section | Rating | Weight |
|---------|--------|--------|
| Theoretical Foundation | ⭐⭐⭐⭐⭐ | 15% |
| Cell Definition | ⭐⭐⭐⭐⭐ | 15% |
| Transport Parameters | ⭐⭐⭐⭐⭐ | 15% |
| CGS Unit Consistency | ⭐⭐⭐⭐⭐ | 15% |
| Electrochemical Kinetics | ⭐⭐⭐⭐⭐ | 15% |
| Numerical Implementation | ⭐⭐⭐⭐⭐ | 15% |
| Validation | ⭐⭐⭐⭐⭐ | 10% |

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
