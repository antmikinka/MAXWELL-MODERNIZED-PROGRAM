# Constitutive Relations Catalog

## Overview

This document catalogs all material constitutive relations from Maxwell's Treatise, connecting electromagnetic fields to material response.

## Dielectric Relations (Part I)

### Electric Displacement

**Maxwell Articles**: 60-62, 111

**General Form**:
```
D = E + 4πP
```

**Linear Isotropic**:
```
D = εE
P = χ_e E
ε = 1 + 4πχ_e
```

**Linear Anisotropic** (Arts. 101a-h):
```
D_i = ε_ij E_j

where ε_ij is the permittivity tensor
```

**Energy Density**:
```
u_e = (1/8π) E·D
```

---

### Specific Inductive Capacity (Dielectric Constant)

**Maxwell Articles**: 52-53

**Definition**:
```
K = ε = D/E (for linear isotropic)
```

**Typical Values (CGS, dimensionless)**:

| Material | K (CGS) |
|----------|---------|
| Vacuum | 1 |
| Air | 1.0006 |
| Glass | 4-10 |
| Water | 80 |
| Mica | 3-6 |

---

### Electric Polarization

**Maxwell Articles**: 60-62, 111

**Definition**:
```
P = dipole moment per unit volume
```

**Relation to Bound Charge**:
```
ρ_bound = -∇·P
σ_bound = P·n̂
```

**For Linear Dielectric**:
```
P = χ_e E = (ε-1)/(4π) E
```

---

## Magnetic Relations (Part III)

### Magnetic Induction

**Maxwell Articles**: 399-400

**General Form**:
```
B = H + 4πI
```

**Linear Isotropic**:
```
B = μH
I = κH
μ = 1 + 4πκ
```

**Linear Anisotropic**:
```
B_i = μ_ij H_j

where μ_ij is the permeability tensor
```

**Energy Density**:
```
u_m = (1/8π) B·H
```

---

### Magnetic Susceptibility

**Maxwell Articles**: 424-426

**Definition**:
```
κ = I/H (for linear isotropic)
```

**Classification**:

| Type | κ Value | Example |
|------|---------|---------|
| Diamagnetic | κ < 0 (small) | Water, Copper |
| Paramagnetic | κ > 0 (small) | Aluminum, Platinum |
| Ferromagnetic | κ >> 1 | Iron, Nickel |

---

### Permeability

**Maxwell Articles**: 426

**Definition**:
```
μ = B/H = 1 + 4πκ
```

**Typical Values (CGS, dimensionless)**:

| Material | μ (CGS) |
|----------|---------|
| Vacuum | 1 |
| Air | 1.0000004 |
| Iron (pure) | 5000 |
| Permalloy | 100000 |

---

### Induced Magnetization

**Maxwell Articles**: 427-430

**Linear Response**:
```
I = κH
```

**Poisson's Theory** (Art. 430):
Molecular dipoles align with applied field.

**Weber's Molecular Theory** (Arts. 442-444):
```
I = I_s tanh(H/H_0)

where I_s = saturation magnetization
      H_0 = characteristic field
```

---

### Hysteresis

**Maxwell Articles**: 444-446

**Phenomenological Model**:
```
I = f(H, history)

Hysteresis loop area = energy loss per cycle
```

**Key Parameters**:
- Coercivity H_c: Field to reduce I to zero
- Remanence I_r: Magnetization at H = 0
- Saturation I_s: Maximum magnetization

---

## Conductive Relations (Part II)

### Ohm's Law (3D)

**Maxwell Articles**: 241, 297-298

**Linear Isotropic**:
```
J = σE
```

**Linear Anisotropic**:
```
J_i = σ_ij E_j

where σ_ij is the conductivity tensor
```

**Energy Dissipation**:
```
Power density = J·E = σE²
```

---

### Conductivity

**Maxwell Articles**: 241, 297-303

**Definition**:
```
σ = J/E (for linear isotropic)
```

**CGS Units**: s⁻¹

**Typical Values**:

| Material | σ (CGS, s⁻¹) |
|----------|--------------|
| Copper | 5.96×10¹⁷ |
| Aluminum | 3.77×10¹⁷ |
| Seawater | 5×10¹³ |
| Distilled Water | 10⁴ |
| Glass | 10⁻⁶ |

---

### Anisotropic Conduction

**Maxwell Articles**: 297-303

**Conductivity Tensor**:
```
J_i = σ_ij E_j
```

**Principal Axes**:
Diagonalize σ_ij to find principal conductivities.

**Stability Condition** (Art. 300):
```
σ_ij must be positive definite
All eigenvalues > 0
```

---

### Stratified Materials

**Maxwell Articles**: 301-303

**Effective Conductivity** (layered):
```
σ_parallel = (Σ f_i σ_i)
σ_perpendicular = 1/(Σ f_i/σ_i)

where f_i = volume fraction of layer i
```

---

## Thermoelectric Relations (Part II)

### Seebeck Effect

**Maxwell Articles**: 249-250

**EMF from Temperature Gradient**:
```
E = S ∇T

where S = Seebeck coefficient
```

---

### Peltier Effect

**Maxwell Articles**: 249

**Heat Absorption at Junction**:
```
q = Π J

where Π = Peltier coefficient
```

---

### Thomson Effect

**Maxwell Articles**: 253

**Heat Along Conductor**:
```
q = -τ (J·∇T)

where τ = Thomson coefficient
```

---

## Electrochemical Relations (Part II)

### Faraday's Laws

**Maxwell Articles**: 255-263

**First Law**:
```
m = zQ

where m = mass deposited
      z = electrochemical equivalent
      Q = total charge
```

**Second Law**:
```
z ∝ M/n

where M = molar mass
      n = valence
```

---

### Polarization (Back EMF)

**Maxwell Articles**: 257-269

**Polarization EMF**:
```
E_pol = f(ion concentration, electrode state)
```

**Limiting Polarization** (Art. 269):
```
E_pol ≤ E_decomposition
```

---

## Summary Table

| Relation | Equation | Articles |
|----------|----------|----------|
| Dielectric | D = εE | 60-62, 111 |
| Magnetic | B = μH | 400 |
| Conduction | J = σE | 241, 297-298 |
| Anisotropic | D_i = ε_ij E_j | 101a-h |
| Anisotropic | B_i = μ_ij H_j | 400 |
| Anisotropic | J_i = σ_ij E_j | 297-303 |
| Thermoelectric | E = S∇T | 249-250 |
| Electrochemical | m = zQ | 255 |

---

## Implementation Notes

### Linearity Check

```python
def is_linear(material):
    """Check if material response is linear."""
    return material.response_type == 'linear'
```

### Anisotropy Check

```python
def is_anisotropic(material):
    """Check if material is anisotropic."""
    return material.tensor is not None
```

### Stability Verification

```python
def verify_stability(tensor):
    """Verify constitutive tensor is positive definite."""
    eigenvalues = np.linalg.eigvalsh(tensor)
    return np.all(eigenvalues > 0)
```

---

## Related Documents

- `cgs-electromagnetic-units.md` - Units for constitutive parameters
- `material-properties-reference.md` - Numerical values
- `analytical-benchmarks.md` - Test cases with materials
