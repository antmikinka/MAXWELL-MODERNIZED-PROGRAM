# Cross-Part Dependency Map

## Overview

This document maps the dependencies between Parts of Maxwell's Treatise, showing how each Part builds upon previous Parts and contributes to later Parts.

## Part Structure

| Part | Name | Articles | Layers | Dependencies |
|------|------|----------|--------|--------------|
| I | Electrostatics | 27-229 | 0-12 | None (Foundation) |
| II | Electrokinematics | 230-370 | 13-30 | Part I |
| III | Magnetism | 371-474 | 30b-42 | Part I |
| IV | Electromagnetism | 475-866 | 43-86 | Parts I, II, III |

## Dependency Graph

```
                    Part IV (Electromagnetism)
                   /           |           \
                  /            |            \
                 /             |             \
         Part II          Part III        Part I
    (Electrokinematics)  (Magnetism)   (Electrostatics)
                                 \           /
                                  \         /
                                   \       /
                                  Foundation
```

## Part I: Electrostatics (Foundation)

### Provides To:

**Part II (Electrokinematics)**:
- Electric field E concepts (Arts. 44-49)
- Potential V concepts (Arts. 69-73)
- Dielectric theory (Arts. 60-62)

**Part III (Magnetism)**:
- Field theory methodology
- Potential theory
- Inverse square law formalism

**Part IV (Electromagnetism)**:
- Gauss's law (∇·D = 4πρ)
- Electrostatic energy
- Maxwell stress tensor (electrostatic part)

### Key Concepts Exported:

| Concept | Article | Used In |
|---------|---------|---------|
| Electric field E | 44-49 | II, III, IV |
| Electric potential V | 69-73 | II, III, IV |
| Gauss's law | 75-76 | IV |
| Dielectric displacement D | 60-62 | IV |
| Electrostatic energy | 85a-b | II, IV |
| Maxwell stress (electrostatic) | 103-110 | IV |

---

## Part II: Electrokinematics

### Dependencies On:

**Part I**:
- Electric field concepts
- Potential theory
- Energy concepts

### Provides To:

**Part IV (Electromagnetism)**:
- Current density J (Arts. 285-296)
- Continuity equation (Art. 295)
- Ohm's law in 3D (Arts. 297-298)
- Circuit theory foundation
- Thermoelectric effects

### Key Concepts Imported:

| Concept | From Part I | Adapted In Part II |
|---------|-------------|-------------------|
| Electric field E | Arts. 44-49 | Drives current (J = σE) |
| Potential V | Arts. 69-73 | EMF = -dV/dx |
| Energy | Arts. 85a-b | Joule heating (H = I²Rt) |

### Key Concepts Exported:

| Concept | Article | Used In |
|---------|---------|---------|
| Current density J | 285-296 | IV |
| Continuity equation | 295 | IV |
| 3D Ohm's law | 297-298 | IV |
| Thermoelectric EMF | 249-254 | IV |

---

## Part III: Magnetism

### Dependencies On:

**Part I**:
- Field theory methodology
- Inverse square law
- Potential theory
- Spherical harmonics

### Provides To:

**Part IV (Electromagnetism)**:
- Magnetic field H (Arts. 395-398)
- Magnetic induction B (Art. 399)
- Constitutive relation B = H + 4πI (Art. 400)
- Vector potential A (Arts. 405-406)
- Solenoidal condition ∇·B = 0 (Arts. 403-404)

### Key Concepts Imported:

| Concept | From Part I | Adapted In Part III |
|---------|-------------|---------------------|
| Field concept | Arts. 44-49 | Magnetic field H |
| Potential | Arts. 69-73 | Magnetic potential Ω |
| Inverse square | Arts. 66-68 | Magnetic force law |
| Spherical harmonics | Arts. 128-146 | Terrestrial magnetism |

### Key Concepts Exported:

| Concept | Article | Used In |
|---------|---------|---------|
| Magnetic field H | 395-398 | IV |
| Magnetic induction B | 399 | IV |
| Constitutive B = μH | 400 | IV |
| Vector potential A | 405-406 | IV |
| Solenoidal condition | 403-404 | IV |
| Magnetic energy | 630-638 | IV |

---

## Part IV: Electromagnetism

### Dependencies On:

**Part I (Electrostatics)**:
- Electric field E
- Gauss's law ∇·D = 4πρ
- Electrostatic energy
- Dielectric theory

**Part II (Electrokinematics)**:
- Current density J
- Continuity equation
- Ohm's law

**Part III (Magnetism)**:
- Magnetic field H
- Magnetic induction B
- Vector potential A
- Solenoidal condition ∇·B = 0

### Integrates Into:

**Complete Maxwell Equations**:
```
∇·D = 4πρ        (from Part I)
∇·B = 0          (from Part III)
∇×E = -(1/c)∂B/∂t  (new - coupling)
∇×H = (4π/c)J + (1/c)∂D/∂t  (from Parts II, IV)
```

### New Concepts Introduced:

| Concept | Article | Builds On |
|---------|---------|-----------|
| Displacement current | 606-607 | Part I D field |
| Electromagnetic induction | 528-531 | Part III B field |
| EM wave equation | 781-785 | All previous |
| Light as EM phenomenon | 786-787 | All previous |
| Poynting vector | 792-793 | Parts I, III energy |
| Full stress tensor | 641-646 | Part I stress |

---

## Cross-Reference by Layer

### Layers 0-12 (Part I - Electrostatics)

```
Layer 0-1: Units, charge → Used by all Parts
Layer 2: Basic physics → Used by Parts II, III, IV
Layer 3: System theory → Used by Part II
Layer 4: Advanced solvers → Used by Parts III, IV
Layer 8-9: Spherical/ellipsoidal harmonics → Used by Part III
Layer 10: Image methods → Used by Parts III, IV
Layer 12: Instrumentation → Used by all Parts
```

### Layers 13-30 (Part II - Electrokinematics)

```
Layer 13-14: Current basics → Used by Part IV
Layer 15-17: Thermoelectric → Standalone
Layer 18-19: Electrolysis → Standalone
Layer 20-21: 3D flow → Used by Part IV
Layer 27-28: Metrology → Used by Part IV
```

### Layers 30b-42 (Part III - Magnetism)

```
Layer 30b-31: Magnetic units → Used by Part IV
Layer 32-34: Magnetic matter → Used by Part IV
Layer 35-36: B, H, A fields → Used by Part IV
Layer 37-38: Induction, components → Used by Part IV
Layer 40-41: Metrology, terrestrial → Standalone
```

### Layers 43-86 (Part IV - Electromagnetism)

```
Layer 43-47: EM coupling → Integrates Parts I-III
Layer 48-52: Induction → Uses Part II currents, Part III fields
Layer 53-60: Field equations → Full Maxwell system
Layer 61-64: Units, dimensions → All Parts
Layer 65-73: Instruments → All Parts
Layer 74-78: Waves → Culmination
Layer 79-82: Magneto-optics, theories → Advanced
```

---

## Dependency Verification Checklist

When implementing any module, verify:

### For Part I Modules:
- [ ] No dependencies on later Parts
- [ ] Self-contained foundation

### For Part II Modules:
- [ ] Part I concepts properly imported
- [ ] No dependency on Parts III, IV

### For Part III Modules:
- [ ] Part I concepts properly imported
- [ ] No dependency on Part II (except optionally)
- [ ] No dependency on Part IV

### For Part IV Modules:
- [ ] Part I concepts (E, D, ρ) available
- [ ] Part II concepts (J, continuity) available
- [ ] Part III concepts (B, H, A) available
- [ ] Proper integration of all Parts

---

## Example: Maxwell Stress Tensor

The full electromagnetic stress tensor demonstrates cross-part integration:

**Part I Contribution** (Arts. 103-110):
```
T_electrostatic = (1/4π)[E_i E_j - (1/2)δ_ij E²]
```

**Part III Contribution** (Arts. 641-646):
```
T_magnetic = (1/4π)[B_i B_j - (1/2)δ_ij B²]
```

**Part IV Synthesis**:
```
T_full = T_electrostatic + T_magnetic
       = (1/4π)[E_i E_j + B_i B_j - (1/2)δ_ij(E² + B²)]
```

---

## Related Documents

- `maxwell-equations-reference.md` - Complete equations
- `analytical-benchmarks.md` - Test cases by Part
- `cgs-electromagnetic-units.md` - Units across Parts
