# Data: maxwell-article-mapping-circuits

## Purpose

Comprehensive mapping of Maxwell's treatise articles to circuit analysis topics.

---

## Part II: Electrokinematics (Art. 230-370)

### Circuit Fundamentals

| Article Range | Topic | Relevance to Circuits |
|---------------|-------|----------------------|
| Art. 230-235 | Currents, continuity | **Foundation for KCL, current flow** |
| Art. 236-238 | Electrolysis laws | Electrochemical circuits |
| Art. 269-286 | Electrochemical effects | Battery modeling |
| Art. 287-300 | Networks, conduction | **Primary reference for circuit theory** |
| Art. 301-320 | Conduction theory | **Resistance, network analysis** |
| Art. 321-342 | Resistance measurement | Measurement techniques |
| Art. 343-348 | Wheatstone bridge | **Bridge circuit analysis** |

### Key Circuit Articles (Detailed)

**Art. 230-235: Currents and Continuity**
- Current definition
- Continuity equation: div(J) = -∂ρ/∂t
- Integral form: ΣI = 0 (KCL foundation)
- Steady current conditions

**Art. 287-300: Networks and Conduction**
- Ohm's law formulation
- Network equations
- Current distribution
- Power dissipation (I²R loss)
- Network solution methods

**Art. 301-320: Conduction Theory**
- Conductivity definition
- Temperature effects
- Material properties
- Non-linear conduction

**Art. 343-348: Wheatstone Bridge**
- Bridge balance condition
- Sensitivity analysis
- Measurement accuracy
- Practical procedures

---

## Part IV: Electromagnetism (Art. 475-866)

### Inductance and Coupling

| Article Range | Topic | Relevance to Circuits |
|---------------|-------|----------------------|
| Art. 475-500 | Electromagnetic force | Motor/generator action |
| Art. 501-520 | Ampère's law | Magnetic field from current |
| Art. 521-540 | Induction | **Faraday's law, induced EMF** |
| Art. 541-570 | Mutual inductance, self-inductance | **L, M, coupled circuits** |
| Art. 604-619 | Field equations | **Maxwell's equations** |
| Art. 781-797 | Electromagnetic waves | **Transmission lines, waves** |

### Key Inductance Articles (Detailed)

**Art. 521-540: Induction**
- Faraday's law
- Induced EMF: ε = -dΦ/dt
- Lenz's law
- Self-induction

**Art. 541-570: Mutual and Self Inductance**
- Self-inductance definition: L = Φ/I
- Mutual inductance: M = Φ₂₁/I₁
- Energy in magnetic field
- Coupled circuit equations
- Maxwell's bridge analysis

**Art. 604-619: Field Equations**
- Complete Maxwell equations
- Displacement current
- Wave equation
- Field-to-circuit connection

**Art. 781-797: Electromagnetic Waves**
- Wave propagation
- Speed of light derivation
- Energy transport
- Transmission line theory

---

## Part I: Electrostatics (Art. 1-229)

### Capacitance and Electric Fields

| Article Range | Topic | Relevance to Circuits |
|---------------|-------|----------------------|
| Art. 44-49 | Electric potential | Voltage definition |
| Art. 50-62 | Dielectrics | Capacitor dielectrics |
| Art. 75-76 | Capacity | **Capacitance definition** |
| Art. 155-175 | Mathematical theory | Field analysis |

### Key Capacitance Articles

**Art. 75-76: Capacity**
- Capacitance definition: C = Q/V
- Energy storage: W = ½CV²
- Series/parallel combinations

---

## Cross-Reference by Circuit Topic

### Kirchhoff's Laws

Primary references:
- **Art. 230-235** (Current continuity → KCL)
- **Art. 287-300** (Network equations → KVL)

### Resistance and Ohm's Law

Primary references:
- **Art. 287-300** (Conduction, networks)
- **Art. 301-320** (Conduction theory)

### Bridge Circuits

Primary references:
- **Art. 343-348** (Wheatstone bridge)
- **Art. 287-300** (Resistance measurement)

### Inductance

Primary references:
- **Art. 541-570** (Self and mutual inductance)
- **Art. 521-540** (Induction)

### Capacitance

Primary references:
- **Art. 75-76** (Capacity)
- **Art. 50-62** (Dielectrics)

### Transmission Lines

Primary references:
- **Art. 604-619** (Field equations)
- **Art. 781-797** (Electromagnetic waves)
- **Art. 287-300** (Conduction for loss)

### Network Theorems

Primary references:
- **Art. 287-300** (Network theory)
- **Art. 301-320** (Conduction)

---

## Theory Classification Guide

### Maxwell's Original Text (maxwell_original)

- All articles from 1873 Treatise
- CGS unit system (Maxwell's choice)
- Original derivations and formulations
- Historical terminology and notation

### User's Original Extensions (user_original)

- **NEVER alter or falsify**
- Clearly mark as user_original
- Authoritative status maintained
- Distinct from standard implementations

### Standard Mathematical Implementations (standard_math)

- Circuit theory (Kirchhoff, Thevenin, etc.)
- Phasor analysis
- Laplace transform methods
- Network synthesis

---

## Article Citation Format

### Standard Citation

```
Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism.
  Part II, Chapter VII, Art. 287-300: Networks and Conduction
  Part IV, Chapter XI, Art. 541-570: Mutual Inductance
```

### In-Text Citation

```
According to Maxwell (Art. 287-300), the current distribution
in a network follows from the principle of minimum heat.

Maxwell's discussion of mutual inductance (Art. 541-570)
establishes M = k√(L₁L₂).
```

---

## Key Maxwell Contributions to Circuit Theory

### Network Theory (Art. 287-300)

- Systematic network analysis
- Current distribution principles
- Minimum heat theorem (precursor to variational methods)
- Resistance measurement techniques

### Bridge Analysis (Art. 343-348)

- Wheatstone bridge theory
- Sensitivity optimization
- Error analysis
- Practical measurement procedures

### Inductance Theory (Art. 541-570)

- Self-inductance definition and calculation
- Mutual inductance and coupling
- Energy storage in magnetic fields
- Coupled circuit equations

### Field-Circuit Connection (Art. 604-619, 781-797)

- Maxwell's equations
- Displacement current
- Wave propagation
- Transmission line theory

---

## Quick Reference Card

| Circuit Topic | Primary Articles | Secondary Articles |
|--------------|------------------|-------------------|
| KCL, Current | 230-235 | 287-300 |
| KVL, Networks | 287-300 | 301-320 |
| Resistance | 287-300, 301-320 | 321-342 |
| Bridges | 343-348 | 287-300 |
| Inductance | 541-570 | 521-540 |
| Capacitance | 75-76 | 50-62 |
| Transmission Lines | 604-619, 781-797 | 287-300 |
| Network Theorems | 287-300 | 301-320 |

---

## CGS Unit References in Treatise

Maxwell consistently uses CGS units throughout:

| Quantity | CGS Unit | Maxwell's Usage |
|----------|----------|-----------------|
| Potential | statvolt | Throughout |
| Current | statampere (via charge/time) | Throughout |
| Resistance | statohm (via V/I) | Art. 287-300 |
| Capacitance | statfarad (via Q/V) | Art. 75-76 |
| Inductance | cm (CGS EMU) | Art. 541-570 |
| Magnetic Field | oersted | Art. 371-474 |
| Electric Field | statvolt/cm | Art. 1-229 |

---

## Notes on Article Numbering

- Article numbers are consistent across editions
- Some editions have slight variations in article ranges
- Always verify against specific edition used
- CGS units are used throughout (Maxwell's choice)

---

## Historical Context

Maxwell's Treatise (1873) predates modern circuit theory notation:

- No phasor notation (developed later by Steinmetz)
- No Laplace transforms (developed later)
- No matrix methods (developed later)
- Original geometric/physical approach

Modern circuit theory builds on Maxwell's foundation while using more efficient mathematical tools.
