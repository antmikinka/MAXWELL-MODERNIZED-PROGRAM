# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Magnetic Shell visualization** (`maxwell.vis.magnetic_shell`) -- `calc_solid_angle()`, `calc_shell_potential()`, `plot_magnetic_shell()`, `plot_shell_potential()` for 3D/2D visualization of Maxwell's magnetic shell theory with current loop equivalence and solid angle calculation (Art. 409)
- **Spherical Harmonic Globes visualization** (`maxwell.vis.spherical_harmonics`) -- `calc_gauss_harmonics()`, `calc_field_intensity()`, `plot_harmonic_globe()`, `plot_harmonic_modes()`, `plot_harmonic_contour()` for 3D globe and 2D map visualization of Gauss coefficient spherical harmonic decomposition of terrestrial magnetism (Art. 467)
- **Hysteresis Loops visualization** (`maxwell.vis.hysteresis_loops`) -- `calc_hysteresis_loop()`, `plot_hysteresis_loops()`, `plot_material_comparison()` for magnetic B-H loop with coercivity/retentivity labels, area shading, and material comparison (soft iron vs steel vs permanent magnet) (Arts. 442-446)
- **EM Wave Propagation visualization** (`maxwell.vis.em_wave_propagation`) -- `calc_em_wave()`, `plot_em_wave_propagation()`, `plot_wave_snapshot_3d()` for orthogonal E/B fields vs position with 3D vector field and linear/circular/elliptical polarization support (Art. 791)
- **Lagrangian Kernel** (`maxwell.dynamics.lagrangian`) -- Layer 52 implementation with `GeneralizedSystem` dataclass, `potential_energy()`, `kinetic_energy()`, `lagrangian()`, `derive_forces()`, and `derive_electrostatic_force()` proof-of-concept (JAX auto-diff force derivation from energy)
- **Dynamics package** (`maxwell.dynamics`) -- New top-level package for mechanics-based formulations
- **JAX adapter package** (`maxwell.jax`) -- 20+ JAX adapters enabling GPU/TPU acceleration, automatic differentiation, and JIT compilation for all four Parts of the Treatise
- **Method of Images visualization** (`maxwell.vis.method_of_images`) -- `calc_method_of_images()` and `plot_method_of_images()` for visualizing a point charge above a conducting plane with image charge technique (Art. 155)
- **Edge Singularities visualization** (`maxwell.vis.edge_singularities`) -- `calc_wedge_field()`, `calc_edge_singularity()`, `plot_edge_singularity()`, and `plot_singularity_comparison()` for visualizing power-law field enhancement near conducting wedge edges (Art. 191)
- **Test PyPI CI workflow** -- Automated Test PyPI publishing on `feat/pypi-package` branch pushes, with build verification and pip install smoke test
- **JAX classes**: `PointChargeJAX`, `MagneticPoleJAX`, `MagnetJAX`, `VectorPotentialJAX`, `ElectricFieldJAX`, `FaradayInductionJAX`, `MaxwellEquationsJAX`, `SphericalHarmonicExpansionJAX`, `LorentzForceJAX`, `MaxwellStressTensorJAX`, `DisplacementCurrentJAX`, `AmpereMaxwellLawJAX`, `ElectrostaticEnergyJAX`, `CapacitorEnergyJAX`, `MagneticEnergyJAX`, `InductorEnergyJAX`, `ElectrokineticEnergyJAX`, `CoupledCircuitEnergyJAX`, `OhmsLawJAX`, `NetworkSolverJAX`, `Conduction3DJAX`, `SpreadingResistanceJAX`, `EffectiveConductivityJAX`, `FaradayLawsJAX`, `IonTransportJAX`, `PolarizationJAX`, `ElectrolysisCellJAX`, `JouleHeatingJAX`, `HeatDissipationJAX`, `SubstanceResistanceJAX`
- **JAX classes**: `PointChargeJAX`, `MagneticPoleJAX`, `MagnetJAX`, `VectorPotentialJAX`, `ElectricFieldJAX`, `FaradayInductionJAX`, `MaxwellEquationsJAX`, `SphericalHarmonicExpansionJAX`, `LorentzForceJAX`, `MaxwellStressTensorJAX`, `DisplacementCurrentJAX`, `AmpereMaxwellLawJAX`, `ElectrostaticEnergyJAX`, `CapacitorEnergyJAX`, `MagneticEnergyJAX`, `InductorEnergyJAX`, `ElectrokineticEnergyJAX`, `CoupledCircuitEnergyJAX`, `OhmsLawJAX`, `NetworkSolverJAX`, `Conduction3DJAX`, `SpreadingResistanceJAX`, `EffectiveConductivityJAX`, `FaradayLawsJAX`, `IonTransportJAX`, `PolarizationJAX`, `ElectrolysisCellJAX`, `JouleHeatingJAX`, `HeatDissipationJAX`, `SubstanceResistanceJAX`
- **JAX infrastructure**: `@jax_tree` pytree registration, `safe_div`/`safe_sqrt`/`safe_log` arithmetic, AGM-based elliptic integrals, pure-JAX special functions (Legendre polynomials, spherical harmonics)
- **SymPy symbolic verifiers** -- 13 verifiers proving div/curl identities, Laplace equation, wave equation, Coulomb's law, Biot-Savart, Faraday's law, continuity equation, Maxwell displacement current, Stokes' theorem, Lorentz force, stress tensor properties, Ampere's law
- **Test suite growth**: 548 → 1618 tests (629 core + 847 JAX + 66 SymPy + 76 visualization), all passing
- `[all]` optional dependency in `pyproject.toml` for installing everything at once
- Python 3.13 classifier

### Changed
- `maxwell.vis` exports expanded from 20 to 29 (added `calc_solid_angle`, `calc_shell_potential`, `plot_magnetic_shell`, `plot_shell_potential`, `calc_gauss_harmonics`, `calc_field_intensity`, `plot_harmonic_globe`, `plot_harmonic_modes`, `plot_harmonic_contour`)
- Test count: 1618 -> 1662 (+44 tests: 22 magnetic shell + 22 spherical harmonics)
- CI workflows now install `.[dev,accel]` to run the full 1618-test suite in GitHub Actions
- `jax_tree` decorator converted to callable class supporting `static_fields` parameter for PyTree registration

### Fixed
- PEP 639 license classifier removed from `pyproject.toml` (build now succeeds)
- `maxwell.vis` exports expanded from 5 to 12 (Cycle 6: method of images, edge singularities), then from 12 to 20 (Cycle 7: dielectric soakage, hysteresis, EM wave propagation)
- Test count: 1542 → 1556 → 1618 (+14 Cycle 6, +62 Cycle 7)

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
