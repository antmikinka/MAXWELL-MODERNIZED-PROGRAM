# Maxwell Equations Reference

## Overview

This document presents Maxwell's equations in their original form from the Treatise, with modern vector notation mappings. All equations are in CGS units.

## Maxwell's Equations (Complete System)

### Modern Vector Form (CGS Gaussian)

```
(1) Gauss's Law:        ∇·D = 4πρ
(2) No Magnetic Monopoles: ∇·B = 0
(3) Faraday's Law:      ∇×E = -(1/c) ∂B/∂t
(4) Ampère-Maxwell:     ∇×H = (4π/c)J + (1/c) ∂D/∂t
```

### Constitutive Relations

```
(5) Electric:  D = εE = E + 4πP
(6) Magnetic:  B = μH = H + 4πI
(7) Conduction: J = σE
```

## Article-by-Article Derivation

### Equation (1): Gauss's Law

**Maxwell Articles**: 75-76 (Part I), 608 (Part IV)

**Original Form** (Art. 76):
```
The total induction through a closed surface equals 4π times the enclosed charge.

∯ E·dS = 4πQ_enclosed
```

**Differential Form**:
```
∇·E = 4πρ
```

**With Dielectric**:
```
∇·D = 4πρ
where D = E + 4πP
```

---

### Equation (2): No Magnetic Monopoles

**Maxwell Articles**: 403-404 (Part III)

**Original Form** (Art. 403):
```
The total magnetic induction through any closed surface is zero.

∯ B·dS = 0
```

**Differential Form**:
```
∇·B = 0
```

**Physical Meaning**: Magnetic field lines are always closed loops; no isolated magnetic poles exist.

---

### Equation (3): Faraday's Law of Induction

**Maxwell Articles**: 528-531 (Part IV), 590 (Part IV)

**Original Form** (Art. 530):
```
The electromotive force around a closed circuit equals the negative rate of change of magnetic flux through the circuit.

EMF = -(1/c) dΦ/dt

where Φ = ∫ B·dS
```

**Differential Form**:
```
∇×E = -(1/c) ∂B/∂t
```

**Key Points**:
- The factor 1/c appears in CGS Gaussian
- Lenz's law: induced EMF opposes the change (negative sign)
- Art. 542: Direction of induced current

---

### Equation (4): Ampère-Maxwell Law

**Maxwell Articles**: 606-607 (Part IV)

**Original Form** (Art. 607):
```
The line integral of magnetic force around a circuit equals (4π/c) times the total current through the circuit plus (1/c) times the rate of change of electric displacement.

∮ H·dl = (4π/c)(I_conduction + I_displacement)

where I_displacement = d/dt ∫ D·dS
```

**Differential Form**:
```
∇×H = (4π/c)J + (1/c) ∂D/∂t
```

**Maxwell's Displacement Current**:
```
J_displacement = (1/4π) ∂D/∂t
```

**Key Insight**: The displacement current term was Maxwell's crucial addition that enabled prediction of electromagnetic waves.

---

## Potential Formulations

### Scalar and Vector Potentials

**Maxwell Articles**: 405-406 (Part III), 540-541 (Part IV), 616-617 (Part IV)

**Definitions**:
```
B = ∇×A  (vector potential)
E = -∇V - (1/c) ∂A/∂t  (general)
E = -∇V  (electrostatic)
```

**In Terms of Potentials**:

Maxwell's equations become:
```
∇²V + (1/c) ∂(∇·A)/∂t = -4πρ  (from Gauss's law)

∇²A - (1/c²) ∂²A/∂t² - ∇(∇·A + (1/c)∂V/∂t) = -(4π/c)J  (from Ampère-Maxwell)
```

**Gauge Choices**:

Coulomb Gauge (∇·A = 0):
```
∇²V = -4πρ
∇²A - (1/c²) ∂²A/∂t² = -(4π/c)J + (1/c)∇(∂V/∂t)
```

Lorenz Gauge (∇·A + (1/c)∂V/∂t = 0):
```
□V = -4πρ
□A = -(4π/c)J

where □ = ∇² - (1/c²)∂²/∂t² (d'Alembertian)
```

---

## Wave Equation

### Derivation from Maxwell's Equations

**Maxwell Articles**: 781-785 (Part IV)

**In Vacuum** (ρ = 0, J = 0, ε = 1, μ = 1):

Take curl of Faraday's law:
```
∇×(∇×E) = -(1/c) ∂(∇×B)/∂t
```

Use vector identity ∇×(∇×E) = ∇(∇·E) - ∇²E:
```
∇(∇·E) - ∇²E = -(1/c) ∂(∇×B)/∂t
```

Since ∇·E = 0 in vacuum:
```
-∇²E = -(1/c) ∂(∇×B)/∂t
```

Substitute ∇×B = (1/c)∂E/∂t:
```
∇²E - (1/c²) ∂²E/∂t² = 0
```

**Similarly for B**:
```
∇²B - (1/c²) ∂²B/∂t² = 0
```

### Wave Speed

**Maxwell Articles**: 786-787 (Part IV)

**Wave Speed**:
```
v = c/√(εμ)
```

**In Vacuum**:
```
v = c
```

**Maxwell's Great Discovery** (Art. 787):
```
The speed of electromagnetic waves equals the measured speed of light.
This proves that light IS an electromagnetic phenomenon.
```

---

## Energy and Momentum

### Poynting Theorem

**Maxwell Articles**: 630-638 (Part IV), 792-793 (Part IV)

**Energy Density**:
```
u = (1/8π)(E² + B²)
```

**Poynting Vector** (energy flux):
```
S = (c/4π) E × H
```

**Poynting Theorem**:
```
∂u/∂t + ∇·S = -J·E
```

**Physical Meaning**:
- ∂u/∂t: Rate of change of field energy
- ∇·S: Energy flux out of volume
- -J·E: Work done on charges (Ohmic loss)

---

### Maxwell Stress Tensor

**Maxwell Articles**: 103-110 (Part I), 641-646 (Part IV)

**Stress Tensor**:
```
T_ij = (1/4π)[E_i E_j + B_i B_j - (1/2)δ_ij(E² + B²)]
```

**Force from Stress**:
```
F_i = ∮ T_ij n_j dS
```

**Physical Interpretation**:
- Diagonal terms: Pressure/tension
- Off-diagonal terms: Shear stress
- Field lines exert tension along their length
- Field lines exert pressure perpendicular to their length

---

## Boundary Conditions

### Interface Conditions

**Maxwell Articles**: 78a-c (Part I), 400-402 (Part III)

**At Interface Between Media**:

| Condition | Equation | Article |
|-----------|----------|---------|
| Tangential E | E₁t = E₂t | 78c |
| Normal D | D₁n - D₂n = 4πσ | 78a-b |
| Tangential H | H₁t - H₂t = (4π/c)K | 607 |
| Normal B | B₁n = B₂n | 403 |

Where:
- σ = surface charge density
- K = surface current density

---

## Component Form (Maxwell's Original Notation)

Maxwell often wrote equations in component form. Here are the equations as Maxwell might have written them:

### Faraday's Law (Component Form)

```
dR/dy - dQ/dz = -(1/c) dα/dt
dP/dz - dR/dx = -(1/c) dβ/dt
dQ/dx - dP/dy = -(1/c) dγ/dt

where (P, Q, R) = electric field components
      (α, β, γ) = magnetic induction components
```

### Ampère-Maxwell (Component Form)

```
dγ/dy - dβ/dz = (4π/c)u + (1/c) dP/dt
dα/dz - dγ/dx = (4π/c)v + (1/c) dQ/dt
dβ/dx - dα/dy = (4π/c)w + (1/c) dR/dt

where (u, v, w) = current density components
```

---

## Summary Table

| Equation | Integral Form | Differential Form | Article |
|----------|---------------|-------------------|---------|
| Gauss | ∯ D·dS = 4πQ | ∇·D = 4πρ | 76, 608 |
| No Monopoles | ∯ B·dS = 0 | ∇·B = 0 | 403 |
| Faraday | ∮ E·dl = -(1/c)dΦ/dt | ∇×E = -(1/c)∂B/∂t | 530, 590 |
| Ampère-Maxwell | ∮ H·dl = (4π/c)(I + I_D) | ∇×H = (4π/c)J + (1/c)∂D/∂t | 607 |

---

## Related Documents

- `cgs-electromagnetic-units.md` - Unit reference
- `constitutive-relations-catalog.md` - Material equations
- `cross-part-dependency-map.md` - How Parts connect
