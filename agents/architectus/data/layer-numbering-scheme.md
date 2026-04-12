# Data: Layer Numbering Scheme

## Description

Official layer numbering reference for the Maxwell Treatise modernization architecture. This document defines the authoritative layer assignments for all 6 Parts.

---

## Layer Numbering Overview

| Part | Domain | Layer Range | Layer Count | Article Range |
|------|--------|-------------|-------------|---------------|
| I | Electrostatics | 0-12 | 13 | 27-229 |
| II | Electrokinematics | 13-30 | 18 | 230-370 |
| III | Magnetism | 30b-42 | 13 | 371-521 |
| IV | Electromagnetism | 43-86 | 44 | 522-710 |
| V | System Core | 90-94 | 5 | 711-780 |
| VI | Scalar Physics | 95-97 | 3 | 781-866 |

**Total Layers:** 98 (0-97, with lettered subdivisions)

---

## Part I: Electrostatics (Layers 0-12)

| Layer | Name | Purpose | Article Range |
|-------|------|---------|---------------|
| 0 | Units, Dimensions & Configuration | Fundamental physical constants, unit systems, theory configuration | 36-42 |
| 1 | Core Primitives | Charge, fields, materials, polarization | 27-35, 44-62 |
| 2 | Basic Physics Engine | Coulomb's law, potential, Gauss's law, Poisson equation | 63-83 |
| 3 | System Manager | Multi-conductor systems, coefficients, energy | 84-94 |
| 4 | Advanced Solvers | Green's theorem, Thomson's theorem, anisotropic media | 95-102 |
| 5 | Field Analysis | Maxwell stress tensor, equilibrium analysis | 103-111 |
| 6 | Visualization | Equipotential plots, field lines, harmonic figures | 112-123, 143 |
| 7 | Standard Components | Capacitors, standard configurations | 124-127 |
| 8 | Spherical Harmonics Math Kernel | Spherical harmonic functions, Legendre polynomials | 128-142 |
| 9 | Ellipsoidal Coordinates | Confocal ellipsoidal surfaces | 147-154 |
| 10 | Image Method Solvers | Method of images, sphere inversions | 155-181 |
| 11 | 2D Complex Analysis | Conjugate functions, 2D field theory | 182-195 |
| 12 | Instrumentation | Electrometers, generators, standards | 207-229 |

---

## Part II: Electrokinematics (Layers 13-30)

| Layer | Name | Purpose | Article Range |
|-------|------|---------|---------------|
| 13 | Kinetic Primitives | Electric current, EMF sources, galvanometers | 230-240 |
| 14 | Conduction & Resistance | Ohm's law, Joule heating, thermal analogy | 241-245 |
| 15 | Contact EMF | Contact potentials, electrolytes, gravity cells | 246-248 |
| 16 | Thermoelectric Coupling | Seebeck, Peltier, Thomson effects | 249-254 |
| 17 | Electrolysis I | Ionic theory, ion migration | 255-265 |
| 18 | Electrolysis II | Stoichiometry, Faraday's laws | 266-275 |
| 19 | Electrolysis III | Energetics, polarization | 276-285 |
| 20 | Network Theory | Circuit topology, Kirchhoff's laws | 286-295 |
| 21 | 3D Current Flow | Current density, tubes of flow, continuity | 296-310 |
| 22 | Anisotropic Conduction | Conductivity tensors, rotatory coefficient | 311-325 |
| 23 | Approximation Methods | Variational methods, Rayleigh bounds | 326-335 |
| 24 | Composite Materials | Effective conductivity, Maxwell-Garnett | 336-345 |
| 25 | Dielectric Leakage | Leakage, absorption, hysteresis | 346-355 |
| 26 | Transmission Lines | Telegraph equation, cable theory | 356-360 |
| 27 | Resistance Measurement | Wheatstone bridge, low resistance | 361-365 |
| 28 | High Resistance Measurement | Electrometer methods | 366-368 |
| 29 | Material Database | Conductor, electrolyte, insulator tables | 369 |
| 30 | Secondary Piles | Batteries, accumulators | 370 |

---

## Part III: Magnetism (Layers 30b-42)

| Layer | Name | Purpose | Article Range |
|-------|------|---------|---------------|
| 30b | Magnetic Primitives | Magnetic poles, magnetic moment | 371-380 |
| 31 | Magnetic Force | Magnetic field intensity, induction | 381-390 |
| 32 | Magnetic Potential | Scalar potential, vector potential | 391-400 |
| 33 | Solenoids | Solenoidal fields, magnetic shells | 401-410 |
| 34 | Magnetic Induction | Induction coefficients, mutual induction | 411-420 |
| 35 | Magnetic Materials | Permeability, susceptibility | 421-430 |
| 36 | Magnetization | Induced magnetization, permanent magnetization | 431-440 |
| 37 | Magnetic Energy | Energy of magnetic field | 441-450 |
| 38 | Magnetic Stress | Magnetic stress tensor | 451-460 |
| 39 | Earth's Magnetism | Terrestrial magnetism | 461-470 |
| 40 | Magnetic Measurements | Magnetometers, measurement techniques | 471-485 |
| 41 | Magnetic Circuits | Magnetic circuit theory | 486-500 |
| 42 | Electromagnetic Relations | Connection to electricity | 501-521 |

---

## Part IV: Electromagnetism (Layers 43-86)

| Layer Range | Domain | Article Range |
|-------------|--------|---------------|
| 43-50 | Electromagnetic Induction | 522-560 |
| 51-60 | Maxwell's Equations | 561-600 |
| 61-70 | Wave Propagation | 601-650 |
| 71-86 | Advanced Electromagnetism | 651-710 |

---

## Part V: System Core (Layers 90-94)

| Layer | Name | Purpose | Article Range |
|-------|------|---------|---------------|
| 90 | System Initialization | Package initialization, configuration loading | 711-730 |
| 91 | Data Management | Data structures, serialization | 731-750 |
| 92 | Simulation Pipeline | Pipeline orchestration, task management | 751-760 |
| 93 | Results Processing | Output generation, analysis | 761-770 |
| 94 | System Utilities | CLI tools, helpers | 771-780 |

---

## Part VI: Scalar Physics (Layers 95-97)

| Layer | Name | Purpose | Article Range |
|-------|------|---------|---------------|
| 95 | Wave Theory | Electromagnetic wave theory | 781-820 |
| 96 | Partial Differential Equations | PDE formulations, solutions | 821-850 |
| 97 | Advanced Topics | Radiation, scattering, diffraction | 851-866 |

---

## Intentional Layer Gaps

| Gap | Layers | Reason |
|-----|--------|--------|
| Part I-II Transition | None | Sequential (12→13) |
| Part II-III Transition | 30→30b | Letter suffix for magnetism distinction |
| Part III-IV Transition | 42→43 | Sequential |
| Part IV-V Transition | 86→90 | Reserved for future electromagnetic expansion (87-89) |
| Part V-VI Transition | 94→95 | Sequential |

---

## Layer Naming Conventions

### Format

```
Layer N: [Domain] [Purpose]
```

### Examples

- `Layer 0: Units, Dimensions & Configuration`
- `Layer 8: Spherical Harmonics Math Kernel`
- `Layer 10: Image Method Solvers`
- `Layer 35: Magnetic Materials`

---

## Layer Dependency Rules

1. **Lower layers are foundational**: Layer N may depend on layers < N
2. **Cross-part dependencies**: Higher parts depend on lower parts
3. **No circular dependencies**: Dependency graph is a DAG
4. **Bridge modules**: Explicit documentation for cross-part bridges

---

## Layer Version History

| Version | Date | Changes |
|---------|------------|---------|
| 2.0 | 2026-01-15 | Complete layer scheme revision |
| 1.5 | 2025-11-15 | Added Part V (90-94) |
| 1.0 | 2025-01-01 | Initial layer scheme (Part I only) |

---

**END OF DOCUMENT**
