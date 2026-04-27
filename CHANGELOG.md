# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-25

### Added
- Complete computational implementation of Maxwell's 1873 Treatise on Electricity and Magnetism
- All 866 articles covered across 4 Parts (electrostatics, electrokinematics, magnetism, electromagnetism)
- 241 Python modules across 81 subpackages
- Citation-based traceability via `@maxwell_cite` decorator linking every function to source articles
- CGS-EMU unit system throughout with ESU/SI conversion utilities
- 548 passing tests (522 core + 23 visualization + 3 version sync) covering all major functionality
- 50/50 mathematical validation checks (dimensional analysis, vector calculus, spherical harmonics, elliptic integrals)
- Electrostatic visualization engine (2D field lines, equipotentials, stress tensor plots)
- Visualization scaffold with matplotlib optional dependency (`pip install maxwell[viz]`)
- CI/CD pipeline with multi-OS, multi-Python test matrix (3 OS x 3 Python versions)
- Spherical harmonics infrastructure (Legendre polynomials, associated Legendre functions, Y_lm, coefficient expansion)
- Vector calculus operators (gradient, divergence, curl) in CGS
- Elliptic integral computation (complete and incomplete, K, E, Pi)
- Maxwell stress tensor with symmetry and trace verification
- Electromagnetic field theory (Maxwell equations, Poynting vector, energy-momentum)
- Material property models (hysteresis, magnetization, permeability, conductivity)
- Instrument models (galvanometers, Helmholtz coils, dynamometers)
- Competing theory implementations (Ampere, Weber, Neumann formulations)

### Key Features
- **Electrostatics** (Part I, Arts. 27-229): Point charges, fields, dielectrics, image charges, capacitance, Green's theorem
- **Electrokinematics** (Part II, Arts. 230-370): Ohm's law, electrolysis, EMF, network analysis, Wheatstone bridge
- **Magnetism** (Part III, Arts. 371-474): Terrestrial magnetism, hysteresis, demagnetizing factors, compass deviation
- **Electromagnetism** (Part IV, Arts. 475-866): Induction, Lorentz force, Ampere-Maxwell law, all Maxwell equations, stress tensor, EM waves
- **Optics** (Arts. 781-808): Wave equation, radiation pressure, metal reflectance, birefringence, Faraday rotation
- **Mathematics**: Spherical harmonics, elliptic integrals, vector calculus, gauge theory
- **Instruments**: Galvanometers, dynamometers, Helmholtz coils, suspended coils
- **Materials**: Magnetization, electric displacement, conductivity, permeability
- **Competing Theories**: Ampere, Weber, and Neumann formulations with quantitative comparison

### Technical
- NumPy >= 1.24 and SciPy >= 1.10 for numerical computation
- Matplotlib >= 3.5 for optional visualization
- Python 3.10, 3.11, 3.12 support
- MIT License

## [0.0.2] - 2026-04-24

### Added
- Visualization scaffold with matplotlib integration
- 2D electrostatic field line plotting
- 2D equipotential contour plotting
- 2D Maxwell stress tensor visualization
- Graceful degradation when matplotlib is absent
- 23 visualization tests

### Fixed
- Deprecation warnings in test suite

## [0.0.1] - 2026-04-23

### Added
- Initial 100% article coverage of Maxwell's 1873 Treatise (866 articles)
- Core primitives: PointCharge, ElectricField, ElectricPotential, Magnet, MagneticMoment
- Maxwell equations implementation (all 7 equations)
- Lorentz force and stress tensor calculations
- Faraday induction and Ampere-Maxwell law
- Spherical harmonic expansion with full coefficient computation
- CGS unit system with dimensional analysis
- 522 initial tests
- `@maxwell_cite` decorator and citation query system
