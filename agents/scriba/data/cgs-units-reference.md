# Data: cgs-units-reference

## Purpose

Comprehensive reference for CGS (centimeter-gram-second) units used throughout the Maxwell Treatise Modernization Project.

---

## CGS Unit System Overview

### Base Units

| Quantity | CGS Unit | Symbol | Definition |
|----------|----------|--------|------------|
| Length | centimeter | cm | 1/100 of meter |
| Mass | gram | g | 1/1000 of kilogram |
| Time | second | s | SI second |

### CGS Variants

| Variant | Usage | Characteristics |
|---------|-------|-----------------|
| CGS-ESU | Electrostatics | Based on electrostatic force |
| CGS-EMU | Electromagnetism | Based on electromagnetic force |
| Gaussian | Mixed | ESU for electric, EMU for magnetic |
| Heaviside-Lorentz | Theoretical | Rationalized units |

**Maxwell's Choice:** Gaussian CGS throughout the Treatise

---

## Electrostatic Units (CGS-ESU)

### Electric Charge

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statcoulomb | statC | 1 cm^(3/2)·g^(1/2)·s^(-1) | 3.336×10^-10 C |
| franklin | Fr | 1 statC | 3.336×10^-10 C |

### Electric Potential

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statvolt | statV | 1 erg/statC | 299.79 V |
| abvolt | abV | 10^-8 V | 10^-8 V |

### Electric Field

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statV/cm | statV/cm | 1 statV/cm | 29979 V/m |

### Capacitance

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statfarad | statF | 1 statC/statV | 1.113×10^-12 F |

### Resistance

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statohm | statΩ | 1 statV/statA | 8.988×10^11 Ω |

### Current

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| statampere | statA | 1 statC/s | 3.336×10^-10 A |

---

## Electromagnetic Units (CGS-EMU)

### Magnetic Field Strength H

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| oersted | Oe | 1 dyne/maxwell | 79.577 A/m |

### Magnetic Induction B

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| gauss | G | 1 maxwell/cm² | 10^-4 T |

### Magnetic Flux

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| maxwell | Mx | 1 G·cm² | 10^-8 Wb |

### Inductance

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| abhenry | abH | 1 abV·s/abA | 10^-9 H |
| cm | cm | 1 cm inductance | 1.113×10^-12 H |

### Current (EMU)

| Unit | Symbol | Definition | SI Equivalent |
|------|--------|------------|---------------|
| abampere | abA | 1 abC/s | 10 A |
| biot | Bi | 1 abA | 10 A |

---

## Gaussian Units (Mixed CGS)

### Combined Electric and Magnetic

| Quantity | Gaussian Unit | Symbol | SI Equivalent |
|----------|---------------|--------|---------------|
| Electric field | statV/cm | E | 29979 V/m |
| Magnetic field | gauss | B | 10^-4 T |
| Magnetic field H | oersted | H | 79.577 A/m |

### Maxwell's Equations (Gaussian CGS)

```
∇ · E = 4πρ
∇ · B = 0
∇ × E = -(1/c) ∂B/∂t
∇ × B = (4π/c)J + (1/c) ∂E/∂t

where c = speed of light = 2.998×10^10 cm/s
```

---

## Physical Constants (CGS)

### Fundamental Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Speed of light | c | 2.99792458×10^10 | cm/s |
| Gravitational constant | G | 6.674×10^-8 | cm³/(g·s²) |
| Planck constant | h | 6.626×10^-27 | erg·s |
| Reduced Planck constant | ℏ | 1.055×10^-27 | erg·s |

### Electromagnetic Constants

| Constant | Symbol | Value | Unit |
|----------|--------|-------|------|
| Elementary charge | e | 4.803×10^-10 | statC |
| Electron mass | m_e | 9.109×10^-28 | g |
| Proton mass | m_p | 1.673×10^-24 | g |
| Boltzmann constant | k_B | 1.381×10^-16 | erg/K |
| Avogadro constant | N_A | 6.022×10^23 | mol^-1 |

### Atomic Units (CGS)

| Quantity | Value | Unit |
|----------|-------|------|
| Bohr radius | 5.292×10^-9 | cm |
| Hartree energy | 4.360×10^-11 | erg |
| Fine structure constant | 1/137.036 | dimensionless |

---

## Derived Units

### Force and Energy

| Quantity | CGS Unit | Symbol | SI Equivalent |
|----------|----------|--------|---------------|
| Force | dyne | dyn | 10^-5 N |
| Energy | erg | erg | 10^-7 J |
| Power | erg/s | erg/s | 10^-7 W |

### Pressure and Stress

| Quantity | CGS Unit | Symbol | SI Equivalent |
|----------|----------|--------|---------------|
| Pressure | dyne/cm² | dyn/cm² | 0.1 Pa |
| Pressure | barye | Ba | 0.1 Pa |

### Viscosity

| Quantity | CGS Unit | Symbol | SI Equivalent |
|----------|----------|--------|---------------|
| Dynamic viscosity | poise | P | 0.1 Pa·s |
| Kinematic viscosity | stokes | St | 10^-4 m²/s |

---

## Unit Conversions

### CGS to SI Conversion Factors

| CGS Unit | Multiply by | SI Unit |
|----------|-------------|---------|
| cm | 0.01 | m |
| g | 0.001 | kg |
| dyn | 10^-5 | N |
| erg | 10^-7 | J |
| statC | 3.336×10^-10 | C |
| statV | 299.79 | V |
| statA | 3.336×10^-10 | A |
| statΩ | 8.988×10^11 | Ω |
| G | 10^-4 | T |
| Oe | 79.577 | A/m |

### SI to CGS Conversion Factors

| SI Unit | Multiply by | CGS Unit |
|---------|-------------|----------|
| m | 100 | cm |
| kg | 1000 | g |
| N | 10^5 | dyn |
| J | 10^7 | erg |
| C | 2.998×10^9 | statC |
| V | 1/299.79 | statV |
| A | 2.998×10^9 | statA |
| Ω | 1.113×10^-12 | statΩ |
| T | 10^4 | G |
| A/m | 0.01257 | Oe |

---

## Maxwell's CGS Usage

### Throughout the Treatise

Maxwell consistently uses CGS units:

| Topic | Articles | CGS Units Used |
|-------|----------|----------------|
| Electrostatics | Art. 1-229 | statC, statV, statΩ |
| Magnetism | Art. 371-474 | G, Oe, emu |
| Electromagnetism | Art. 475-866 | Mixed Gaussian |
| Instruments | Art. 730-750 | statA, statV, dyn·cm |

### Maxwell's Rationale

Maxwell chose CGS because:
- Absolute system based on fundamental units
- Coherent without arbitrary conversion factors
- Suitable for precision measurements
- Universal (independent of local gravity)

---

## CGS in Modern Context

### Fields Using CGS

| Field | CGS Usage | Reason |
|-------|-----------|--------|
| Astrophysics | gauss, oersted | Historical convention |
| Plasma physics | statV/cm | Natural units |
| Materials science | emu/cm³ | Magnetization |
| Maxwell scholarship | All CGS | Historical accuracy |

### SI Coexistence

```
Note: SI units provided for reference only.
Primary calculations and documentation use CGS
to maintain consistency with Maxwell's 1873 text.
```

---

## Quality Criteria

- [ ] All CGS units correctly defined
- [ ] SI equivalents accurate
- [ ] Physical constants verified
- [ ] Conversion factors correct
- [ ] Maxwell's usage documented
