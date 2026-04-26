# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-25

### Added
- Complete computational implementation of Maxwell's 1873 Treatise
- 866 articles covered across 4 Parts (electrostatics, electrokinematics, magnetism, electromagnetism)
- 241 Python modules across 80+ subpackages
- Citation-based traceability via `@maxwell_cite` decorator
- CGS-EMU unit system throughout with ESU/SI conversion utilities
- 522 passing tests covering all major functionality

### Key Features
- **Electrostatics** (Part I): Point charges, fields, dielectrics, image charges, capacitance, Green's theorem
- **Electrokinematics** (Part II): Ohm's law, electrolysis, EMF, network analysis, Wheatstone bridge
- **Magnetism** (Part III): Terrestrial magnetism, hysteresis, demagnetizing factors, compass deviation
- **Electromagnetism** (Part IV): Induction, Lorentz force, Ampere-Maxwell law, all 9 Maxwell equations, stress tensor, EM waves
- **Optics** (Arts. 781-808): Wave equation, radiation pressure, metal reflectance, birefringence, Faraday rotation
- **Mathematics**: Spherical harmonics, elliptic integrals, vector calculus, gauge theory, conjugate functions
- **Instruments**: Galvanometers, dynamometers, Helmholtz coils, suspended coils
- **Materials**: Magnetization, electric displacement, conductivity, permeability relations
- **Competing Theories**: Ampere, Weber, and Neumann formulations with quantitative comparison

### Technical
- NumPy + SciPy for numerical computation
- Python 3.10+ support
- MIT License
