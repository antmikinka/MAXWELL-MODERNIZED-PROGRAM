# CGS Electromagnetic Units Reference

## Overview

This document provides the complete reference for CGS (centimeter-gram-second) electromagnetic units used throughout Maxwell's Treatise. All implementations must use CGS units by default.

## Maxwell Article References

- **Articles 41-42**: Electrostatic unit definitions, dimensions
- **Articles 495**: Electromagnetic unit definitions
- **Articles 620-629**: Physical dimensions and unit systems

## CGS Unit Systems

Maxwell's Treatise uses three related CGS systems:

### 1. CGS Electrostatic (ESU)

Based on defining Coulomb's law as F = q₁q₂/r² (no 4πε₀ factor).

| Quantity | Unit Name | Symbol | Dimensions | Relation to Base |
|----------|-----------|--------|------------|------------------|
| Charge | statcoulomb | statC | L^(3/2) M^(1/2) T^(-1) | 1 statC = 1 dyne^(1/2)·cm |
| Electric Field | statvolt/cm | statV/cm | L^(-1/2) M^(1/2) T^(-1) | E = F/q |
| Potential | statvolt | statV | L^(1/2) M^(1/2) T^(-1) | V = W/q |
| Displacement | statcoulomb/cm² | D | L^(-1/2) M^(1/2) T^(-1) | D = εE |
| Permittivity | - | ε | dimensionless | D = εE |

### 2. CGS Electromagnetic (EMU)

Based on defining magnetic force law between poles.

| Quantity | Unit Name | Symbol | Dimensions | Relation to Base |
|----------|-----------|--------|------------|------------------|
| Magnetic Pole | unit pole | - | L^(3/2) M^(1/2) T^(-1) | F = m₁m₂/r² |
| Magnetic Field | Oersted | Oe | L^(-1/2) M^(1/2) T^(-1) | H = F/m |
| Magnetic Induction | Gauss | G | L^(-1/2) M^(1/2) T^(-1) | B = μH |
| Current | abampere | abA | L^(1/2) M^(1/2) T^(-1) | B = 2I/(cr) |
| Resistance | abohm | abΩ | L^(-1) T | R = V/I |
| Inductance | cm | cm | L | L = Φ/I |
| Permeability | - | μ | dimensionless | B = μH |

### 3. CGS Gaussian

Combines ESU for electric quantities and EMU for magnetic quantities, with c appearing in coupling equations.

| Equation | Gaussian Form |
|----------|---------------|
| Coulomb's Law | F = q₁q₂/r² |
| Biot-Savart | B = (I/c) ∮ dl×r̂/r² |
| Faraday's Law | ∇×E = -(1/c)∂B/∂t |
| Ampère-Maxwell | ∇×H = (4π/c)J + (1/c)∂D/∂t |
| Lorentz Force | F = q(E + v/c × B) |

## Fundamental Constants (CGS)

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Speed of Light | c | 2.99792458×10¹⁰ | cm/s |
| Electron Charge | e | 4.8032047×10⁻¹⁰ | statC |
| Electron Mass | mₑ | 9.10938356×10⁻²⁸ | g |
| Planck Constant | ℏ | 1.0545718×10⁻²⁷ | erg·s |
| Boltzmann Constant | k_B | 1.380649×10⁻¹⁶ | erg/K |
| Gravitational Constant | G | 6.67430×10⁻⁸ | dyne·cm²/g² |

## Unit Conversions

### ESU to SI

| CGS (ESU) | SI | Conversion Factor |
|-----------|-----|-------------------|
| 1 statC | C | 3.33564×10⁻¹⁰ |
| 1 statV/cm | V/m | 2.9979×10⁴ |
| 1 statV | V | 299.79 |
| 1 cm (capacitance) | F | 1.1126×10⁻¹² |

### EMU to SI

| CGS (EMU) | SI | Conversion Factor |
|-----------|-----|-------------------|
| 1 abA | A | 10 |
| 1 abV | V | 10⁻⁸ |
| 1 G | T | 10⁻⁴ |
| 1 Oe | A/m | 79.577 |
| 1 abΩ | Ω | 10⁻⁹ |
| 1 cm (inductance) | H | 10⁻⁹ |

### Gaussian to SI

| CGS (Gaussian) | SI | Conversion Factor |
|----------------|-----|-------------------|
| 1 statC | C | 3.33564×10⁻¹⁰ |
| 1 G | T | 10⁻⁴ |
| 1 Oe | A/m | 1000/(4π) ≈ 79.577 |
| E (statV/cm) | E (V/m) | 2.9979×10⁴ |
| B (G) | B (T) | 10⁻⁴ |

## Dimensional Analysis

### Base Dimensions

| Dimension | Symbol | CGS Unit |
|-----------|--------|----------|
| Length | L | cm |
| Mass | M | g |
| Time | T | s |

### Derived Dimensions

| Quantity | Dimensions | CGS Unit |
|----------|------------|----------|
| Force | L M T⁻² | dyne |
| Energy | L² M T⁻² | erg |
| Power | L² M T⁻³ | erg/s |
| Charge (ESU) | L^(3/2) M^(1/2) T⁻¹ | statC |
| Current (ESU) | L^(3/2) M^(1/2) T⁻² | statA |
| Current (EMU) | L^(1/2) M^(1/2) T⁻¹ | abA |

### Dimensional Verification

All equations must satisfy dimensional consistency. Example verification:

```
E = q/r² (CGS ESU)
[E] = [q]/[r]² = (L^(3/2) M^(1/2) T⁻¹) / L² = L^(-1/2) M^(1/2) T⁻¹ ✓
```

## Key Equations in CGS

### Electrostatics (Part I)

```
Coulomb's Law:    F = q₁q₂/r²
Gauss's Law:      ∇·E = 4πρ
Potential:        V = q/r
Energy:           U = (1/8π) ∫ E² dτ
```

### Magnetostatics (Part III)

```
Magnetic Force:   F = m₁m₂/r²
Constitutive:     B = H + 4πI = μH
Vector Potential: B = ∇×A
Energy:           U = (1/8π) ∫ B² dτ
```

### Electrodynamics (Part IV)

```
Faraday's Law:    ∇×E = -(1/c) ∂B/∂t
Ampère-Maxwell:   ∇×H = (4π/c)J + (1/c) ∂D/∂t
Lorentz Force:    F = q(E + v/c × B)
Wave Speed:       v = c/√(εμ)
Poynting Vector:  S = (c/4π) E × H
```

## Common Pitfalls

1. **4π Factors**: CGS is unrationalized - 4π appears in Coulomb's law and source equations
2. **c in Equations**: Speed of light appears explicitly in electromagnetic equations
3. **E and B Same Dimensions**: In Gaussian CGS, E and B have identical dimensions
4. **Capacitance and Inductance**: Both have dimensions of length (cm)

## Implementation Requirements

All physics implementations must:

1. Use CGS units by default
2. Clearly document unit assumptions
3. Provide unit conversion utilities
4. Verify dimensional consistency
5. Include c explicitly in electromagnetic equations

## Related Documents

- `analytical-benchmarks.md` - Test cases with CGS values
- `maxwell-equations-reference.md` - Equations in CGS form
- `unit_converter.py.md` - Conversion utilities
