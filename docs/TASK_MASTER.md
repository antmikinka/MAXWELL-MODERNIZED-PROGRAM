# Maxwell Modernized -- Task Master

> **Definitive task tracking document for the Maxwell Modernized project.**
> Every module, class, test, JAX adapter, visualization, CI workflow, and documentation file tracked with checkbox status.

**Generated:** 2026-05-06
**Version:** 0.1.0
**Branch:** `feat/pypi-package`
**Source:** Cross-analysis of 16 architecture maps vs. 276 actual Python modules

---

## Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total implementation tasks completed** | **~195 modules** | -- |
| **Total test tasks completed** | **27 files / 1542 tests** | 100% |
| **JAX adapters completed** | **37 classes / 17 files** | -- |
| **SymPy verifiers completed** | **13 / 13** | 100% |
| **Visualizations completed** | **3 / 17** | 18% |
| **CI workflows completed** | **5 / 5** | 100% |
| **Documentation files completed** | **13 / 13** | 100% |
| **Architecture layers complete** | **~70 / 97** | 72% |
| **Layers partially complete** | **~15 / 97** | 15% |
| **Layers not started** | **~12 / 97** | 13% |
| **Empty subpackage scaffolds** | **24 directories** | -- |
| **Maxwell articles covered** | **866 / 866** | 100% |

### Overall Task Count Estimate

| Category | Completed | Remaining | Total |
|----------|-----------|-----------|-------|
| Implementation modules | 195 | ~45 | ~240 |
| Test files | 27 | ~10 | ~37 |
| JAX adapter classes | 37 | ~15 | ~52 |
| SymPy verifiers | 13 | 0 | 13 |
| Visualizations | 3 | 14 | 17 |
| CI workflows | 5 | 1 | 6 |
| Documentation | 13 | ~6 | ~19 |
| Infrastructure layers | ~70 | ~27 | ~97 |

---

## Part I: Electrostatics (Arts. 27-229, Layers 0-12)

**Status: 95% Complete**

### Layer 0: Unit System & Dimensional Analysis

#### Completed Tasks
- [x] `maxwell/core/units/dimensions.py` -- MagneticDimensions class, dimensional analysis (Arts. 41-42)
- [x] `maxwell/core/units/units.py` -- CGSUnitConverter (Art. 41)
- [x] `maxwell/config/constants.py` -- CONST, C (speed of light), global constants
- [x] `maxwell/config/conventions.py` -- PolarityConvention (Arts. 393-394)
- [x] Tests: `test_cgs_units.py` (363 lines, 20+ tests)
- [x] Math validation: dimensional analysis checks (part of 50/50)

#### Remaining Tasks
- [ ] Add SI unit conversion completeness audit
- [ ] Add unit test for ESU-to-EMU ratio validation edge cases

### Layer 1: Core Primitives (Electrification, Dielectrics, VectorField)

#### Completed Tasks
- [x] `maxwell/core/charge.py` -- PointCharge class, field_at, potential_at (Arts. 27-35)
- [x] `maxwell/core/field.py` -- ElectricField class, gauss_law_closed_surface (Arts. 44-48)
- [x] `maxwell/core/potential.py` -- ElectricPotential class (Arts. 69-73)
- [x] `maxwell/core/matter.py` -- Matter class abstraction (Art. 52)
- [x] `maxwell/core/measurement.py` -- Measurement utilities
- [x] `maxwell/electrostatics/phenomena.py` -- Electrification phenomena (Arts. 27-35)
- [x] `maxwell/electrostatics/dielectrics.py` -- DielectricMaterial class (Arts. 50-57, 157-170)
- [x] Core tests covering PointCharge, ElectricField, ElectricPotential

#### Remaining Tasks
- [ ] Add explicit VectorField base class if not present
- [ ] Add DielectricMaterial polarization vector support

### Layer 2: Basic Physics Engine (Potential, Forces)

#### Completed Tasks
- [x] `maxwell/electrostatics/force_theory.py` -- Coulomb's law, force calculations (Arts. 63-68)
- [x] `maxwell/physics/coulomb.py` -- Coulomb's law implementation
- [x] `maxwell/physics/potentials.py` -- Potential physics
- [x] SymPy verifier: `verify_coulomb_law_symbolic`
- [x] Math validation: Coulomb law checks

#### Remaining Tasks
- [ ] Add Poisson equation solver if not present
- [ ] Add potential energy surface/volume integrals (check mechanics/potential_energy.py)

### Layer 3: System Manager (Capacity/Induction Matrices)

#### Completed Tasks
- [x] `maxwell/core/charge.py` -- ConductorSystem class (partial coverage)

#### Remaining Tasks
- [ ] Create dedicated `maxwell/systems/energy.py` -- SystemState class
- [ ] Create `maxwell/systems/matrices.py` -- Capacity and induction matrices
- [ ] Add tests for capacity coefficient calculations
- [ ] Add tests for induction coefficient calculations

### Layer 4: Advanced Solvers (Green's Function, Thomson's Theorem)

#### Completed Tasks
- [x] `maxwell/electrostatics/general_theorems.py` -- Green's theorem, general theorems (Arts. 96-102)
- [x] `maxwell/math/potential_theorems.py` -- Potential theory theorems
- [x] Math validation: Green's theorem verification

#### Remaining Tasks
- [ ] Create dedicated `maxwell/solvers/greens.py` -- Green's function solver
- [ ] Add Thomson's theorem implementation
- [ ] Add variational method solver

### Layer 5: Field Analysis (Stress Tensor, Equilibrium)

#### Completed Tasks
- [x] `maxwell/electrostatics/equilibrium_surfaces.py` -- Equilibrium surfaces (Arts. 112-116)
- [x] `maxwell/electromagnetism/forces/stress_tensor.py` -- MaxwellStressTensor (Arts. 641-643)
- [x] `maxwell/vis/stress.py` -- Stress tensor 2D visualization
- [x] `maxwell/electromagnetism/physics/stress.py` -- Stress physics (Art. 501)
- [x] SymPy verifier: `verify_stress_tensor_properties`

#### Remaining Tasks
- [ ] Implement 3D stress tensor ellipsoid visualization
- [ ] Add equilibrium stability analysis module

### Layer 6: Visualization Engine (Equipotentials, Lines of Force)

#### Completed Tasks
- [x] `maxwell/vis/equipotential.py` -- `plot_equipotentials_2d()` (Arts. 117-121)
- [x] `maxwell/vis/field_lines.py` -- `plot_field_lines_2d()` (Arts. 122-123)
- [x] `maxwell/vis/_base.py` -- Base visualization infrastructure
- [x] `maxwell/vis/_compat.py` -- Matplotlib compatibility layer
- [x] `maxwell/vis/__init__.py` -- Package exports with graceful degradation
- [x] Tests: `test_vis.py` (242 lines, 23 test functions)

#### Remaining Tasks
- [ ] Implement 3D equipotential isosurfaces (`render_isosurfaces()`)
- [ ] Implement 3D field line tracing (`trace_streamlines()`)
- [ ] Add PyVista integration for 3D rendering
- [ ] Add JAX-accelerated visualization (GPU-rendered field lines)

### Layer 7: Standard Components (Plates, Spheres, Cylinders)

#### Completed Tasks
- [x] `maxwell/components/spheres.py` -- Spherical geometries (Art. 125)
- [x] `maxwell/components/ellipsoids.py` -- Ellipsoidal geometries
- [x] `maxwell/electromagnetism/components/solenoids.py` -- Solenoid components (Arts. 675-677)
- [x] `maxwell/electromagnetism/components/cylinders.py` -- Cylindrical conductors (Arts. 682-684)
- [x] `maxwell/electromagnetism/components/circular_coils.py` -- Circular coils (Arts. 694-696)

#### Remaining Tasks
- [ ] Add `maxwell/components/plates.py` -- Parallel plate capacitor geometry
- [ ] Add coaxial cylinder geometry module

### Layer 8: Spherical Harmonics (Math)

#### Completed Tasks
- [x] `maxwell/math/spherical_harmonics.py` -- SphericalHarmonicExpansion, LegendrePolynomial (Arts. 128-146)
- [x] `maxwell/jax/math/spherical_harmonics.py` -- SphericalHarmonicExpansionJAX
- [x] SymPy verifier: `verify_laplace_spherical`
- [x] Math validation: spherical harmonics convergence

#### Remaining Tasks
- [ ] Add full (non-axisymmetric) spherical harmonic expansion tests
- [ ] Add tesseral and sectorial harmonic tests

### Layer 9: Method of Images

#### Completed Tasks
- [x] `maxwell/electrostatics/electric_images.py` -- Method of electric images (Arts. 155-172)
- [x] `maxwell/electrostatics/confocal_surfaces.py` -- Confocal coordinate systems (Arts. 147-154)

#### Remaining Tasks
- [ ] Implement Method of Images visualization (`render_virtual_images()`) -- Art. 155
- [ ] Add geometric inversion transformation module
- [ ] Add tests for image charge configurations

### Layer 10: Complex Analysis (Conjugate Functions, Edge Distributions)

#### Completed Tasks
- [x] `maxwell/math/conjugate_functions.py` -- 2D complex analysis (Arts. 182-190)
- [x] `maxwell/math/elliptic_integrals.py` -- EllipticIntegral class (K, E, Pi)
- [x] `maxwell/jax/_elliptic.py` -- Pure JAX elliptic integrals (AGM method)
- [x] `maxwell/jax/_scipy_special.py` -- JAX wrappers for scipy.special

#### Remaining Tasks
- [ ] Implement Edge Singularities visualization (`render_density_heatmap()`) -- Art. 191
- [ ] Add edge charge distribution analysis
- [ ] Add complex potential conformal mapping module

### Layer 11: Electrostatic Instruments

#### Completed Tasks
- [x] `maxwell/electrostatics/instruments.py` -- Electrostatic instruments (Arts. 207-229)

#### Remaining Tasks
- [ ] Add specific instrument classes (electrometer, electroscope)
- [ ] Add instrument calibration tests

### Layer 12: Verification

#### Completed Tasks
- [x] `maxwell/verification/framework.py` -- VerificationResult, VerificationSuite, VerificationReport
- [x] `maxwell/verification/sympy_verify.py` -- 13 SymPy symbolic verifiers (422 lines)
- [x] `maxwell/verification/module_checks.py` -- Module-level verification
- [x] `maxwell/verification/cross_validation.py` -- Cross-module consistency
- [x] `maxwell/verification/convergence.py` -- Convergence testing
- [x] Tests: `test_verification_framework.py` (213 lines)
- [x] Tests: `test_cross_validation.py` (126 lines)
- [x] Tests: `test_convergence.py` (171 lines)
- [x] Tests: `test_sympy_verify.py` (422 lines, 66 tests)
- [x] Math validation: 50/50 checks passing

#### Remaining Tasks
- [ ] Add appendix-specific verification tests (math appendices)
- [ ] Add equation extraction tests (legacy extractors)

### Part I JAX Adapters

#### Completed
- [x] `maxwell/jax/core/charge.py` -- PointChargeJAX (Arts. 27-35)
- [x] `maxwell/jax/electromagnetism/field.py` -- ElectricFieldJAX
- [x] `maxwell/jax/electromagnetism/energy.py` -- ElectrostaticEnergyJAX, CapacitorEnergyJAX (Arts. 630-631)
- [x] `maxwell/jax/math/spherical_harmonics.py` -- SphericalHarmonicExpansionJAX (Arts. 128-146)
- [x] `maxwell/jax/core/vector_potential.py` -- VectorPotentialJAX (Arts. 405-406)
- [x] Tests: `test_jax_adapter.py` (4891 lines -- includes PointChargeJAX, ElectricFieldJAX tests)

#### Remaining
- [ ] Add JAX adapter for DielectricMaterial
- [ ] Add JAX adapter for Method of Images solver

### Part I Visualization Tasks

#### Completed
- [x] `plot_equipotentials_2d()` in `equipotential.py` -- 2D equipotential contours
- [x] `plot_field_lines_2d()` in `field_lines.py` -- 2D field line streamlines

#### Remaining
- [ ] `render_virtual_images()` -- Method of Images visualization (Art. 155)
- [ ] `render_density_heatmap()` -- Edge Singularities heatmap (Art. 191)
- [ ] 3D equipotential isosurfaces
- [ ] 3D field line tracing

---

## Part II: Electrokinematics (Arts. 230-370, Layers 13-30)

**Status: 85% Complete**

### Layer 13: Kinetic Primitives (Electric Current, EMF)

#### Completed Tasks
- [x] `maxwell/electrokinematics/emf.py` -- Electromotive force (Arts. 232-234)
- [x] `maxwell/electrokinematics/emf_bodies.py` -- EMF between bodies (Arts. 246-248)
- [x] `maxwell/physics/current.py` -- Current physics
- [x] `maxwell/physics/conduction.py` -- Conduction physics (Arts. 241-244)

#### Remaining Tasks
- [ ] Add explicit ElectricCurrent class
- [ ] Add VoltaicBattery model

### Layer 14: Electrochemical Engine (Electrolysis)

#### Completed Tasks
- [x] `maxwell/electrokinematics/electrolysis.py` -- Electrolysis, Faraday's laws (Arts. 236-238, 249-263)
- [x] `maxwell/jax/electromagnetism/electrolysis.py` -- FaradayLawsJAX, IonTransportJAX, PolarizationJAX, ElectrolysisCellJAX
- [x] Tests: `test_electrolysis_jax.py` (818 lines)

#### Remaining Tasks
- [ ] Add Electrolyte and Ion domain objects
- [ ] Add ion migration visualization

### Layer 15: Resistive Physics (Ohm's Law, Joule Heating)

#### Completed Tasks
- [x] `maxwell/physics/ohm.py` -- Ohm's law (Art. 241)
- [x] `maxwell/jax/electromagnetism/ohms_law.py` -- OhmsLawJAX, ResistanceJAX, ConductivityJAX, PowerDissipationJAX (Arts. 241-242)
- [x] `maxwell/jax/electromagnetism/joule_heating.py` -- JouleHeatingJAX, HeatDissipationJAX, SubstanceResistanceJAX (Arts. 242, 359-370)
- [x] Tests: `test_ohms_law_jax.py` (623 lines)
- [x] Tests: `test_joule_heating_jax.py` (738 lines)

#### Remaining Tasks
- [ ] Implement Thermal Gradients visualization (`render_joule_heating()`) -- Art. 242/249
- [ ] Add Joule heating in 3D media
- [ ] Add temperature-dependent resistance module

### Layer 16: Interface Physics (Contact EMF, Volta's Law)

#### Completed Tasks
- [x] `maxwell/electrokinematics/emf_bodies.py` -- Partial coverage of contact potentials

#### Remaining Tasks
- [ ] Add explicit Volta's law of contact module
- [ ] Add electrolyte interface model
- [ ] Add contact potential difference tests

### Layer 17: Thermoelectric Coupling (Seebeck/Peltier)

#### Remaining Tasks
- [ ] Create `maxwell/thermodynamics/thermoelectric.py` -- Seebeck/Peltier effects
- [ ] Add thermocouple model
- [ ] Add thermoelectric coefficient database
- [ ] Add tests for Seebeck voltage calculations
- [ ] Add tests for Peltier heat calculations

### Layer 18: Molecular Stoichiometry (Faraday's Laws)

#### Completed Tasks
- [x] Covered in `maxwell/electrokinematics/electrolysis.py`
- [x] JAX: FaradayLawsJAX in `jax/electromagnetism/electrolysis.py`
- [x] Tests: `test_electrolysis_jax.py` (818 lines)

#### Remaining Tasks
- [ ] Add stoichiometry calculation module (if not covered)
- [ ] Add conservation of charge verification tests

### Layer 19: Polarization Dynamics (Dielectric Memory, Batteries)

#### Completed Tasks
- [x] `maxwell/electrokinematics/dielectric_conduction.py` -- Dielectric conduction (Arts. 325-334)
- [x] `maxwell/jax/electromagnetism/electrolysis.py` -- PolarizationJAX class

#### Remaining Tasks
- [ ] Implement Dielectric Soakage visualization (`plot_transient_recovery()`) -- Art. 329
- [ ] Add dielectric memory time-series model
- [ ] Add Daniell cell model

### Layer 20: Circuit Network Theory (Kirchhoff)

#### Completed Tasks
- [x] `maxwell/electrokinematics/network_solver.py` -- NetworkAnalyzer, circuit networks (Arts. 273-284)
- [x] `maxwell/jax/electromagnetism/network_solver.py` -- NetworkSolverJAX, KirchhoffJAX, WheatstoneBridgeJAX, ReciprocityVerifierJAX
- [x] `maxwell/circuits/dynamics.py` -- Circuit dynamics (Arts. 578-584)
- [x] Tests: `test_network_solver_jax.py` (801 lines)

#### Remaining Tasks
- [ ] Add CircuitGraph class with explicit topology
- [ ] Add non-linear circuit element support

### Layer 21: 3D Flow Dynamics (Current Density, Tubes of Flow)

#### Completed Tasks
- [x] `maxwell/electrokinematics/conduction_3d.py` -- 3D current flow (Arts. 285-296)
- [x] `maxwell/jax/electromagnetism/conduction_3d.py` -- Conduction3DJAX, SpreadingResistanceJAX, EffectiveConductivityJAX
- [x] Tests: `test_conduction_3d_jax.py` (618 lines)

#### Remaining Tasks
- [ ] Implement Unit Tubes of Flow visualization (`render_tubes()`) -- Art. 290
- [ ] Add current density vector field module
- [ ] Add stream function calculations

### Layer 22: Anisotropic Physics (Conductivity Tensor)

#### Completed Tasks
- [x] `maxwell/materials/constitutive/conductivity.py` -- Conductivity (Art. 609)
- [x] `maxwell/electrokinematics/resistance_distribution.py` -- Resistance distribution (Arts. 297-303)

#### Remaining Tasks
- [ ] Add full conductivity tensor class (3x3 anisotropic)
- [ ] Add rotatory conductivity module
- [ ] Add anisotropic conduction tests

### Layer 23: Approximation Solvers (Rayleigh's Bounds)

#### Remaining Tasks
- [ ] Create `maxwell/solvers/variational_3d.py` -- Rayleigh's resistance bounds
- [ ] Add variational principle solver
- [ ] Add upper/lower bound resistance calculations
- [ ] Add tests for Rayleigh bound accuracy

### Layer 24: Composite Materials (Effective Conductivity)

#### Completed Tasks
- [x] `maxwell/electrokinematics/heterogeneous_media.py` -- Heterogeneous media (Arts. 310-324)
- [x] `maxwell/jax/electromagnetism/conduction_3d.py` -- EffectiveConductivityJAX
- [x] `maxwell/materials/constitutive/` -- 4 constitutive relation modules

#### Remaining Tasks
- [ ] Add composite material mixing models
- [ ] Add stratified media conductor module
- [ ] Add effective medium approximation tests

### Layer 25: Dielectric Memory (Leakage, Soakage)

#### Completed Tasks
- [x] `maxwell/electrokinematics/dielectric_conduction.py` -- Dielectric conduction with leakage
- [x] Covered in Layer 19

#### Remaining Tasks
- [ ] Add dielectric absorption time-constant model
- [ ] Add transient recovery curve fitting
- [ ] Add soakage parameter extraction tests

### Layer 26: Transmission Lines (Telegraph Equation)

#### Completed Tasks
- [x] `maxwell/telecom/telegraphy.py` -- Telegraph equations (Arts. 331-333)
- [x] `maxwell/signal_processing/telegraphy.py` -- Signal processing for telegraphy

#### Remaining Tasks
- [ ] Add cable parameter extraction module
- [ ] Add signal attenuation calculations
- [ ] Add transmission line impedance tests

### Layer 27: Metrology & Standards

#### Completed Tasks
- [x] `maxwell/electrokinematics/resistance_measurement.py` -- Resistance measurement (Arts. 335-357)
- [x] `maxwell/calibration/absolute_resistance.py` -- Absolute resistance calibration

#### Remaining Tasks
- [ ] Add resistance standard definitions module
- [ ] Add metrology traceability chain
- [ ] Add calibration uncertainty analysis

### Layer 28: Measurement Bridges & Instruments

#### Completed Tasks
- [x] `maxwell/instruments/galvanometers.py` -- TangentGalvanometer (Arts. 707-712)
- [x] `maxwell/instruments/helmholtz.py` -- HelmholtzCoil (Art. 713)
- [x] `maxwell/instruments/dynamometers.py` -- Dynamometers (Art. 725)
- [x] `maxwell/instruments/suspended_coil.py` -- Suspended coil instruments (Arts. 721-724)
- [x] `maxwell/instruments/optimization/sensitivity.py` -- Sensitivity optimization (Arts. 718-719)
- [x] JAX: WheatstoneBridgeJAX in `jax/electromagnetism/network_solver.py`

#### Remaining Tasks
- [ ] Add bridge measurement module (Wheatstone, Kelvin double bridge)
- [ ] Add low/high resistance measurement instruments
- [ ] Add instrument error analysis

### Layer 29: Material Database

#### Remaining Tasks
- [ ] Populate `maxwell/materials/database/` -- Currently empty scaffold (only `__init__.py`)
- [ ] Add resistivity data for common materials
- [ ] Add dielectric constant database
- [ ] Add permeability database
- [ ] Add temperature coefficient data
- [ ] Add material property lookup API

### Layer 30: System Integration

#### Completed Tasks
- [x] Unit system in `maxwell/core/units/` (dimensions.py, units.py)
- [x] `maxwell/config/constants.py` -- Universal constants
- [x] Integration tests across all Part II modules

### Part II JAX Adapters

#### Completed
- [x] `maxwell/jax/electromagnetism/ohms_law.py` -- OhmsLawJAX, ResistanceJAX, ConductivityJAX, PowerDissipationJAX
- [x] `maxwell/jax/electromagnetism/network_solver.py` -- NetworkSolverJAX, KirchhoffJAX, WheatstoneBridgeJAX, ReciprocityVerifierJAX
- [x] `maxwell/jax/electromagnetism/conduction_3d.py` -- Conduction3DJAX, SpreadingResistanceJAX, EffectiveConductivityJAX
- [x] `maxwell/jax/electromagnetism/electrolysis.py` -- FaradayLawsJAX, IonTransportJAX, PolarizationJAX, ElectrolysisCellJAX
- [x] `maxwell/jax/electromagnetism/joule_heating.py` -- JouleHeatingJAX, HeatDissipationJAX, SubstanceResistanceJAX

#### Remaining
- [ ] Add JAX adapter for dielectric conduction
- [ ] Add JAX adapter for thermoelectric effects
- [ ] Add JAX adapter for telegraph equation solver

### Part II Visualization Tasks

#### Remaining
- [ ] `render_tubes()` -- Unit Tubes of Flow (Art. 290)
- [ ] `render_joule_heating()` -- Thermal Gradients overlay (Art. 242/249)
- [ ] `plot_transient_recovery()` -- Dielectric Soakage time-series (Art. 329)

---

## Part III: Magnetism (Arts. 371-474, Layers 30b-42)

**Status: 70% Complete**

### Layer 30b: Magnetic Units

#### Completed Tasks
- [x] Uses `maxwell/core/units/dimensions.py` -- MagneticDimensions class

#### Remaining Tasks
- [ ] Add explicit magnetic unit pole definition

### Layer 31: Magnetic Primitives

#### Completed Tasks
- [x] `maxwell/core/magnet.py` -- Magnet class (Arts. 371-376)
- [x] `maxwell/core/moment.py` -- MagneticMoment class (Arts. 381-384)
- [x] `maxwell/core/matter.py` -- Magnetic matter abstraction (Arts. 377-380)

#### Remaining Tasks
- [ ] Add magnetic pole model class
- [ ] Add distributed magnetization model

### Layer 32: Dipole Interactions

#### Completed Tasks
- [x] `maxwell/physics/coupling.py` -- Dipole interaction coupling
- [x] `maxwell/mechanics/potential_energy.py` -- Dipole potential energy (Art. 389)
- [x] `maxwell/fields/force.py` -- MagneticForce/H field (Arts. 395-398)

#### Remaining Tasks
- [ ] Add magnetic dipole-dipole interaction force module
- [ ] Add torque on dipole calculations

### Layer 33: Coordinate Conventions

#### Completed Tasks
- [x] `maxwell/config/conventions.py` -- PolarityConvention (Austral/Boreal) (Arts. 393-394)

### Layer 34: Three Vectors B, H, I

#### Completed Tasks
- [x] `maxwell/fields/force.py` -- H field (Arts. 395-398)
- [x] `maxwell/fields/induction.py` -- B field, MagneticInduction (Art. 399)
- [x] `maxwell/fields/constitutive.py` -- B = H + 4*pi*I relation (Art. 400)
- [x] `maxwell/fields/decomposition.py` -- Lamellar/Solenoidal decomposition (Arts. 412-416)
- [x] `maxwell/fields/solenoidal.py` -- Solenoidal condition (Arts. 403-404)

#### Remaining Tasks
- [ ] Add explicit Magnetization (I) vector class
- [ ] Add B-H-I vector relationship tests

### Layer 35: Vector Potential Calculus

#### Completed Tasks
- [x] `maxwell/calculus/vector_potential.py` -- Vector potential calculus (Arts. 405-406)
- [x] `maxwell/calculus/integrals.py` -- Line and surface integrals (Arts. 401-402)
- [x] `maxwell/calculus/cyclic.py` -- Cyclic potentials (Arts. 417-422)

#### Remaining Tasks
- [ ] Add magnetic scalar potential module
- [ ] Add vector potential gauge fixing

### Layer 36: Magnetic Geometry (Solenoids, Shells, Solid Angles)

#### Completed Tasks
- [x] `maxwell/geometry/solenoids.py` -- Solenoid geometries (Arts. 407-408)
- [x] `maxwell/geometry/shells.py` -- Magnetic shell geometries (Arts. 409-411)
- [x] `maxwell/electromagnetism/components/solenoids.py` -- Solenoid components

#### Remaining Tasks
- [ ] Implement Magnetic Shell visualization (`render_solid_angle_cap()`) -- Art. 409
- [ ] Add solid angle computation module
- [ ] Add shell force/torque calculations

### Layer 37: Material Response (Induced Magnetization)

#### Completed Tasks
- [x] `maxwell/materials/induction.py` -- Induced magnetization (Arts. 424-430)

#### Remaining Tasks
- [ ] Add Poisson method for induced magnetization
- [ ] Add Faraday method for induced magnetization
- [ ] Add demagnetizing factor calculations

### Layer 38: Analytical Geometries (Sphere, Ellipsoid, Naval)

#### Completed Tasks
- [x] `maxwell/components/ellipsoids.py` -- Ellipsoidal geometries (Arts. 437-438)
- [x] `maxwell/engineering/naval.py` -- ShipMagnetism (Art. 441)

#### Remaining Tasks
- [ ] Add hollow sphere magnetism module
- [ ] Add ellipsoid demagnetizing factors
- [ ] Add ship magnetism tests

### Layer 39: Nonlinear Materials (Hysteresis, Saturation)

#### Completed Tasks
- [x] `maxwell/materials/hysteresis.py` -- HysteresisLoop class (Arts. 444-446)
- [x] `maxwell/materials/saturation.py` -- Saturation modeling (Arts. 442-443)
- [x] `maxwell/physics/magnetostriction.py` -- Magnetostriction (Art. 447)
- [x] `maxwell/physics/molecular_theory.py` -- Molecular theory of magnetism (Art. 430)

#### Remaining Tasks
- [ ] Implement Hysteresis Loops animation (`animate_hysteresis_cycle()`) -- Art. 442
- [ ] Add Weber hysteresis model
- [ ] Add Preisach model for hysteresis
- [ ] Add magnetostriction strain calculations

### Layer 40: Magnetic Metrology

#### Completed Tasks
- [x] `maxwell/magnetism/magnetic_measurements.py` -- Magnetic measurements (Arts. 449-464)
- [x] Tests: `test_magnetic_measurements.py` (1005 lines)

#### Remaining Tasks
- [ ] Add magnetometer instrument classes
- [ ] Add dip circle instrument model
- [ ] Add measurement uncertainty analysis

### Layer 41: Planetary Magnetism (Terrestrial, Gauss Expansion)

#### Completed Tasks
- [x] `maxwell/magnetism/terrestrial_magnetism.py` -- GeomagneticElements (Arts. 465-473)
- [x] `maxwell/math/spherical_harmonics.py` -- Gauss expansion
- [x] `maxwell/jax/math/spherical_harmonics.py` -- SphericalHarmonicExpansionJAX

#### Remaining Tasks
- [ ] Implement Spherical Harmonic Globes visualization (`render_gauss_harmonics()`) -- Art. 467
- [ ] Populate `maxwell/magnetism/geophysics/` -- Currently empty scaffold
- [ ] Add IGRF coefficient loading
- [ ] Add geomagnetic field line tracing

### Layer 42: Magnetic Mechanics

#### Completed Tasks
- [x] `maxwell/mechanics/potential_energy.py` -- Dipole potential energy (Art. 389)
- [x] `maxwell/mechanics/shell_energy.py` -- Shell work calculations (Art. 423)

#### Remaining Tasks
- [ ] Add shell mechanical work calculations
- [ ] Add magnetic spring constant calculations

### Part III JAX Adapters

#### Completed
- [x] `maxwell/jax/core/magnet.py` -- MagneticPoleJAX, MagnetJAX (Arts. 371-376)
- [x] `maxwell/jax/core/vector_potential.py` -- VectorPotentialJAX (Arts. 405-406)
- [x] `maxwell/jax/electromagnetism/magnetic_energy.py` -- MagneticEnergyJAX, InductorEnergyJAX (Arts. 632-633)

#### Remaining
- [ ] Add JAX adapter for hysteresis loop
- [ ] Add JAX adapter for terrestrial magnetism
- [ ] Add JAX adapter for solenoid field calculations

### Part III Visualization Tasks

#### Remaining
- [ ] `render_solid_angle_cap()` -- Magnetic Shell (Art. 409)
- [ ] `render_gauss_harmonics()` -- Spherical Harmonic Globes (Art. 467)
- [ ] `animate_hysteresis_cycle()` -- Hysteresis Loops animation (Art. 442)

### Part III Empty Scaffolds
- [ ] `maxwell/magnetism/calculus/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/components/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/core/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/fields/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/geometry/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/geophysics/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/instruments/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/materials/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/mechanics/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/physics/` -- Only `__init__.py`
- [ ] `maxwell/magnetism/solvers/` -- Only `__init__.py`

---

## Part IV: Electromagnetism (Arts. 475-866, Layers 43-86)

**Status: 82% Complete**

### Layer 43: Coupling Interface (Oersted's Discovery)

#### Completed Tasks
- [x] `maxwell/electromagnetism/sources/oersted.py` -- Oersted's discovery (Arts. 475-479)
- [x] `maxwell/electromagnetism/sources/__init__.py` -- Package init

#### Remaining Tasks
- [ ] Add EM unit system derivation from Oersted

### Layer 44: Topological Potentials (Cyclic, Helicoidal)

#### Completed Tasks
- [x] `maxwell/electromagnetism/potentials/multivalued.py` -- Cyclic/multi-valued potentials (Art. 480)
- [x] `maxwell/electromagnetism/potentials/surfaces.py` -- Equipotential surfaces (Arts. 486-487)
- [x] `maxwell/calculus/cyclic.py` -- Cyclic potential calculus (Arts. 417-422)

#### Remaining Tasks
- [ ] Implement Helicoidal Potentials visualization (`render_cyclic_surface()`) -- Art. 487
- [ ] Add helicoidal surface geometry module
- [ ] Add multi-valued potential branch cut handling

### Layer 45: Equivalence Engine (Circuit-to-Shell)

#### Completed Tasks
- [x] `maxwell/electromagnetism/equivalence.py` -- Circuit-to-shell equivalence (Arts. 482-485)

#### Remaining Tasks
- [ ] Add equivalence verification tests
- [ ] Add shell-to-circuit transformation

### Layer 46: Mechanical Dynamics (Lorentz Force, Parallel Currents)

#### Completed Tasks
- [x] `maxwell/electromagnetism/forces/lorentz.py` -- LorentzForce class (Arts. 490-492)
- [x] `maxwell/electromagnetism/dynamics/attraction.py` -- Parallel current attraction (Arts. 496-497)
- [x] `maxwell/jax/electromagnetism/forces.py` -- LorentzForceJAX
- [x] SymPy verifier: `verify_lorentz_force`

#### Remaining Tasks
- [ ] Add parallel wire force calculation tests
- [ ] Add Lorentz force trajectory integration

### Layer 47: Ampere's Experiments

#### Completed Tasks
- [x] `maxwell/electromagnetism/experiments/ampere_balance.py` -- Ampere balance (Arts. 502-504)
- [x] `maxwell/electromagnetism/experiments/felici.py` -- Felici's experiments (Art. 536)
- [x] `maxwell/electromagnetism/experiments/stress_verification.py` -- Stress verification (Arts. 645-646)

#### Remaining Tasks
- [ ] Add Ampere null experiment simulation
- [ ] Add experiment data analysis module

### Layer 48: Elemental Electrodynamics

#### Completed Tasks
- [x] `maxwell/electromagnetism/forces/elemental.py` -- Elemental electrodynamics (Arts. 510-515)
- [x] `maxwell/electromagnetism/potentials/mutual_energy.py` -- Mutual potential energy (Arts. 520-521)

#### Remaining Tasks
- [ ] Add elemental force law comparison tests
- [ ] Add mutual potential energy verification

### Layer 49: Algebraic Kernels (Quaternions, Directrix)

#### Completed Tasks
- [x] `maxwell/math/algebra/quaternions.py` -- QuaternionSolver (Art. 522)
- [x] `maxwell/electromagnetism/potentials/directrix.py` -- Directrix function (Arts. 517-519)

#### Remaining Tasks
- [ ] Add quaternion field solver engine (full implementation)
- [ ] Add quaternion-to-vector conversion
- [ ] Add quaternion rotation tests

### Layer 50: Induction Engine (Faraday, Lenz, Electrotonic)

#### Completed Tasks
- [x] `maxwell/electromagnetism/induction/faraday.py` -- FaradayInduction (Arts. 528-531)
- [x] `maxwell/electromagnetism/induction/lenz.py` -- Lenz's law (Art. 542)
- [x] `maxwell/electromagnetism/induction/self.py` -- Self-induction (Arts. 546-550)
- [x] `maxwell/electromagnetism/induction/generalized.py` -- Generalized EMF (Arts. 576-577)
- [x] `maxwell/electromagnetism/fields/electrotonic.py` -- Electrotonic state (Arts. 540-541)
- [x] `maxwell/jax/electromagnetism/induction.py` -- FaradayInductionJAX
- [x] SymPy verifier: `verify_faraday_symbolic`

#### Remaining Tasks
- [ ] Add Faraday induction experiment simulation
- [ ] Add self-inductance calculation for various geometries

### Layer 51: Electrical Inertia (Self-Induction, Energy)

#### Completed Tasks
- [x] `maxwell/electromagnetism/induction/self.py` -- Self-induction (Arts. 546-550)
- [x] `maxwell/electromagnetism/energy/electrokinetic.py` -- Electrokinetic energy (Arts. 634-638)
- [x] `maxwell/jax/electromagnetism/electrokinetic.py` -- ElectrokineticEnergyJAX, CoupledCircuitEnergyJAX

#### Remaining Tasks
- [ ] Add coupled circuit inductance matrix
- [ ] Add energy dynamics verification tests

### Layer 52: Lagrangian Kernel (CRITICAL GAP)

#### Remaining Tasks
- [ ] Create `maxwell/dynamics/` directory
- [ ] Create `maxwell/dynamics/lagrangian.py` -- GeneralizedSystem class (q, p state)
- [ ] Create `maxwell/dynamics/lagrangian.py` -- KineticEnergy class (T = 1/2 L I^2)
- [ ] Create `maxwell/dynamics/lagrangian.py` -- PotentialEnergy class
- [ ] Create `maxwell/dynamics/lagrangian.py` -- LagrangianIntegrator class
- [ ] Create `maxwell/dynamics/hamiltonian.py` -- Hamiltonian mechanics
- [ ] Add JAX-based Lagrangian integrator with auto-diff
- [ ] Add force-from-energy derivation via automatic differentiation
- [ ] Add generalized coordinate tests
- [ ] Add Lagrangian verification tests

### Layer 53: Dynamical EM Theory

#### Completed Tasks
- [x] `maxwell/electromagnetism/theory/dynamical_model.py` -- Dynamical model (Arts. 568-571)
- [x] `maxwell/electromagnetism/forces/generalized.py` -- Generalized mechanical forces (Arts. 573-575)

#### Remaining Tasks
- [ ] Add dynamical theory verification tests
- [ ] Add generalized force from energy derivative

### Layer 54: Linear Circuits (Coupled Circuits)

#### Completed Tasks
- [x] `maxwell/circuits/dynamics.py` -- Circuit dynamics (Arts. 578-584)
- [x] `maxwell/electrokinematics/network_solver.py` -- Network analysis

#### Remaining Tasks
- [ ] Add mutual action module for coupled circuits
- [ ] Add coupled circuit eigenvalue analysis

### Layer 55: Electrokinetic Momentum (A-Field)

#### Completed Tasks
- [x] `maxwell/electromagnetism/potentials/vector_momentum.py` -- Vector momentum (Arts. 585-590)
- [x] `maxwell/electromagnetism/fields/curl_relation.py` -- B = curl A relation (Arts. 591-592)
- [x] `maxwell/calculus/vector_potential.py` -- Vector potential calculus
- [x] `maxwell/jax/core/vector_potential.py` -- VectorPotentialJAX

#### Remaining Tasks
- [ ] Implement Electrotonic State visualization (`render_vector_potential_A()`) -- Art. 540/617
- [ ] Add vector potential visualization (swirling field)
- [ ] Add momentum-energy relationship tests

### Layer 56: General Electrodynamics (Maxwell's Equations B, C)

#### Completed Tasks
- [x] `maxwell/electromagnetism/forces/sliding.py` -- Motional EMF, sliding piece (Arts. 594-597)
- [x] `maxwell/electromagnetism/theory/general_equations.py` -- MaxwellEquations, ElectromagneticField (Arts. 598-603)
- [x] `maxwell/jax/electromagnetism/equations.py` -- MaxwellEquationsJAX, ElectromagneticFieldJAX

#### Remaining Tasks
- [ ] Add general EMF equation B verification tests
- [ ] Add force equation C verification tests

### Layer 57: Constitutive Relations (D, F, G, L)

#### Completed Tasks
- [x] `maxwell/materials/constitutive/conductivity.py` -- Conductivity (Art. 609)
- [x] `maxwell/materials/constitutive/displacement.py` -- Displacement field
- [x] `maxwell/materials/constitutive/magnetization.py` -- Magnetization
- [x] `maxwell/materials/constitutive/permeability.py` -- Permeability

#### Remaining Tasks
- [ ] Add constitutive relation cross-verification tests
- [ ] Add non-linear constitutive relation support

### Layer 58: Current & Displacement (Ampere-Maxwell Law)

#### Completed Tasks
- [x] `maxwell/electromagnetism/fields/ampere_maxwell.py` -- AmpereMaxwellLaw, DisplacementCurrent (Arts. 606-607)
- [x] `maxwell/electromagnetism/currents/total.py` -- Total current (Art. 610)
- [x] `maxwell/electromagnetism/currents/emf_relation.py` -- Current-EMF relation (Art. 611)
- [x] `maxwell/jax/electromagnetism/ampere_maxwell.py` -- AmpereMaxwellLawJAX, DisplacementCurrentJAX
- [x] SymPy verifier: `verify_maxwell_correction`

#### Remaining Tasks
- [ ] Add displacement current verification tests
- [ ] Add total current divergence check

### Layer 59: Conservation Laws (Charge Density)

#### Completed Tasks
- [x] `maxwell/electromagnetism/charges/volume.py` -- Volume charge density (Art. 612)
- [x] `maxwell/electromagnetism/charges/surface.py` -- Surface charge density (Art. 613)
- [x] `maxwell/electromagnetism/theory/conservation.py` -- Energy/momentum conservation (Arts. 543-544)
- [x] SymPy verifier: `verify_continuity_equation`

#### Remaining Tasks
- [ ] Add charge conservation verification tests
- [ ] Add surface-to-volume charge transition

### Layer 60: Quaternion Field Solver Engine

#### Completed Tasks
- [x] `maxwell/math/algebra/quaternions.py` -- Quaternion operations (partial)

#### Remaining Tasks
- [ ] Add full quaternion field solver engine
- [ ] Add quaternion-based Maxwell equation solver
- [ ] Add quaternion rotation and transformation tests

### Layer 61: Dimensional Type System (ESU/EMU)

#### Completed Tasks
- [x] `maxwell/core/units/dimensions.py` -- Dimensional analysis
- [x] `maxwell/core/units/units.py` -- CGS-EMU unit system
- [x] `maxwell/electromagnetism/units/` -- EM unit subpackage (scaffold)
- [x] Math validation: ESU/EMU ratio verification

#### Remaining Tasks
- [ ] Add explicit ESU-to-EMU conversion module
- [ ] Add dimensional consistency checker

### Layer 62: Energy Density (Electrostatic, Magnetic, Electrokinetic)

#### Completed Tasks
- [x] `maxwell/electromagnetism/energy/electrostatic.py` -- Electrostatic energy (Arts. 630-631)
- [x] `maxwell/electromagnetism/energy/magnetic.py` -- Magnetic energy (Arts. 632-633)
- [x] `maxwell/electromagnetism/energy/electrokinetic.py` -- Electrokinetic energy (Arts. 634-638)
- [x] `maxwell/jax/electromagnetism/energy.py` -- ElectrostaticEnergyJAX, CapacitorEnergyJAX
- [x] `maxwell/jax/electromagnetism/magnetic_energy.py` -- MagneticEnergyJAX, InductorEnergyJAX
- [x] `maxwell/jax/electromagnetism/electrokinetic.py` -- ElectrokineticEnergyJAX, CoupledCircuitEnergyJAX

#### Remaining Tasks
- [ ] Add energy density field visualization
- [ ] Add total energy conservation verification tests

### Layer 63: Stress Tensor (Maxwell Stress)

#### Completed Tasks
- [x] `maxwell/electromagnetism/forces/stress_tensor.py` -- MaxwellStressTensor class (Arts. 641-643)
- [x] `maxwell/vis/stress.py` -- `plot_stress_tensor_2d()` -- 2D stress visualization
- [x] `maxwell/electromagnetism/physics/stress.py` -- Stress physics (Art. 501)
- [x] `maxwell/jax/electromagnetism/forces.py` -- MaxwellStressTensorJAX
- [x] `maxwell/electromagnetism/experiments/stress_verification.py` -- Stress verification
- [x] SymPy verifier: `verify_stress_tensor_properties`

#### Remaining Tasks
- [ ] Implement 3D stress tensor ellipsoid visualization
- [ ] Add stress tensor force integration tests

### Layer 64: Mathematical Appendices

#### Completed Tasks
- [x] `maxwell/verification/sympy_verify.py` -- 13 SymPy verifiers
- [x] `maxwell/math/elliptic_integrals.py` -- Elliptic integrals
- [x] `maxwell/verification/module_checks.py` -- Module verification

#### Remaining Tasks
- [ ] Add appendix-specific mathematical tests
- [ ] Add analytical integral verification
- [ ] Add series expansion tests

### Layer 65: Cylindrical Systems (Solenoids, GMD)

#### Completed Tasks
- [x] `maxwell/electromagnetism/components/solenoids.py` -- Solenoid components (Arts. 675-677)
- [x] `maxwell/electromagnetism/components/cylinders.py` -- Cylindrical conductors (Arts. 682-684)
- [x] `maxwell/math/geometry/gmd.py` -- Geometric Mean Distance (Art. 691)

#### Remaining Tasks
- [ ] Add cylindrical system inductance calculations
- [ ] Add GMD approximation tests

### Layer 66: Circular Coils

#### Completed Tasks
- [x] `maxwell/electromagnetism/components/circular_coils.py` -- Circular coils (Arts. 694-696)
- [x] `maxwell/electromagnetism/forces/coil_forces.py` -- Coil forces (Arts. 697-699)
- [x] `maxwell/electromagnetism/optimization/coil_design.py` -- Coil design optimization (Art. 706)
- [x] `maxwell/math/elliptic_integrals.py` -- Elliptic integrals for coil calculations

#### Remaining Tasks
- [ ] Add Helmholtz coil pair field calculations
- [ ] Add coil coefficient series expansions
- [ ] Add multi-layer coil model

### Layer 67: Advanced Coil Math

#### Completed Tasks
- [x] `maxwell/math/elliptic_integrals.py` -- Elliptic integrals (K, E, Pi)
- [x] `maxwell/jax/_elliptic.py` -- Pure JAX elliptic integrals (AGM method)

#### Remaining Tasks
- [ ] Add coil coefficient series expansion module
- [ ] Add Legendre polynomial series for coil fields
- [ ] Add advanced coil field calculation tests

### Layer 68: Electromagnetic Instruments

#### Completed Tasks
- [x] `maxwell/instruments/galvanometers.py` -- TangentGalvarometer (Arts. 707-712)
- [x] `maxwell/instruments/helmholtz.py` -- HelmholtzCoil (Art. 713)
- [x] `maxwell/instruments/suspended_coil.py` -- Suspended coil instruments (Arts. 721-724)
- [x] `maxwell/instruments/optimization/sensitivity.py` -- Sensitivity optimization (Arts. 718-719)
- [x] `maxwell/electromagnetism/measurements/galvanometers_extended.py` -- Extended galvanometer theory

#### Remaining Tasks
- [ ] Add ballistic galvanometer model
- [ ] Add moving-coil galvanometer dynamics
- [ ] Add instrument damping analysis

### Layer 69: Dynamometers

#### Completed Tasks
- [x] `maxwell/instruments/dynamometers.py` -- Dynamometers (Art. 725)

#### Remaining Tasks
- [ ] Add electrodynamometer model
- [ ] Add dynamometer calibration tests
- [ ] Add balance instrument model

### Layer 70: Signal Processing (Damping, Filtering, Ballistic)

#### Completed Tasks
- [x] `maxwell/signal_processing/telegraphy.py` -- Signal processing for telegraphy (Arts. 730-751)
- [x] `maxwell/telecom/telegraphy.py` -- Telegraph equations

#### Remaining Tasks
- [ ] Add signal damping analysis module
- [ ] Add ballistic galvanometer signal processing
- [ ] Add filtering module for noisy measurements

### Layer 71: Calibration (Coil Calibration)

#### Completed Tasks
- [x] `maxwell/calibration/absolute_resistance.py` -- Absolute resistance calibration

#### Remaining Tasks
- [ ] Populate `maxwell/instruments/calibration/` -- Currently empty scaffold
- [ ] Add coil calibration procedure
- [ ] Add calibration standard traceability
- [ ] Add calibration uncertainty calculations

### Layer 72: Absolute Resistance

#### Completed Tasks
- [x] `maxwell/calibration/absolute_resistance.py` -- Absolute resistance calibration
- [x] `maxwell/electromagnetism/measurements/galvanometers_extended.py` -- Extended measurements

#### Remaining Tasks
- [ ] Populate `maxwell/instruments/absolute/` -- Currently empty scaffold
- [ ] Add Lorenz apparatus model
- [ ] Add absolute ohm determination

### Layer 73: Velocity Ratio v (Speed of Light)

#### Completed Tasks
- [x] `maxwell/experiments/ratio_v/theory.py` -- Unit ratio theory (Arts. 768-770)
- [x] `maxwell/experiments/ratio_v/condensers.py` -- Condenser methods (Arts. 771-774)
- [x] `maxwell/experiments/ratio_v/combined.py` -- Combined methods (Arts. 775-780)

#### Remaining Tasks
- [ ] Add velocity ratio experimental data analysis
- [ ] Add speed of light comparison tests
- [ ] Add historical measurement comparison

### Layer 74: Wave Engine (Wave Equation, Light Velocity)

#### Completed Tasks
- [x] `maxwell/optics/wave_equation.py` -- PlaneWave class, wave equation (Arts. 781-785)
- [x] `maxwell/optics/velocity.py` -- Light velocity comparison (Arts. 786-787)
- [x] `maxwell/electromagnetism/waves/wave_equation.py` -- EM wave equation
- [x] SymPy verifier: `verify_wave_equation_1d`

#### Remaining Tasks
- [ ] Add wave equation in various coordinate systems
- [ ] Add wave velocity in media calculations

### Layer 75: Optical Properties (Refractive Index, Opacity)

#### Completed Tasks
- [x] `maxwell/optics/constants.py` -- Optical constants, refractive index (Arts. 788-789)
- [x] `maxwell/optics/metals.py` -- Metal opacity (Arts. 798-800)

#### Remaining Tasks
- [ ] Add refractive index dispersion model
- [ ] Add metal skin depth calculations
- [ ] Add optical property tests

### Layer 76: Radiation (Plane Waves, Radiation Pressure)

#### Completed Tasks
- [x] `maxwell/optics/plane_waves.py` -- Plane wave simulation (Arts. 790-791)
- [x] `maxwell/optics/radiation_pressure.py` -- Radiation pressure (Arts. 792-793)

#### Remaining Tasks
- [ ] Implement EM Wave Propagation visualization (`render_plane_wave()`) -- Art. 791
- [ ] Add radiation pressure force calculations
- [ ] Add plane wave superposition tests

### Layer 77: Crystal Optics (Birefringence)

#### Completed Tasks
- [x] `maxwell/optics/crystals.py` -- Crystal optics, birefringence (Arts. 794-797)

#### Remaining Tasks
- [ ] Add crystal optic axis calculations
- [ ] Add birefringence phase shift calculations
- [ ] Add crystal orientation tests

### Layer 78: Diffusion (Field Diffusion in Conductors)

#### Completed Tasks
- [x] `maxwell/optics/diffusion.py` -- Field diffusion in conductors (Arts. 801-805)

#### Remaining Tasks
- [ ] Add skin depth frequency dependence
- [ ] Add diffusion time constant calculations
- [ ] Add conductor penetration depth tests

### Layer 79: Magneto-Optics (Faraday Effect, Polarization)

#### Completed Tasks
- [x] `maxwell/magneto_optics/rotation.py` -- Faraday rotation (Arts. 807-809)
- [x] `maxwell/magneto_optics/circular_polarization.py` -- Circular polarization (Arts. 813-817)
- [x] `maxwell/magneto_optics/energy_analysis.py` -- Magneto-optics energy analysis
- [x] `maxwell/electromagnetism/waves/polarization.py` -- Wave polarization

#### Remaining Tasks
- [ ] Add Verdet constant database
- [ ] Add Faraday rotation angle calculations
- [ ] Add Kerr effect module

### Layer 80: Vortex Engine (Molecular Vortices)

#### Completed Tasks
- [x] `maxwell/vortex_engine/vortex_lattice.py` -- Vortex lattice simulation (Arts. 822-828)
- [x] `maxwell/vortex_engine/equations_of_motion.py` -- Vortex equations of motion
- [x] `maxwell/vortex_engine/helmholtz_law.py` -- Helmholtz's vortex law (Art. 823)
- [x] `maxwell/vortex_engine/kinetic_energy.py` -- Vortex kinetic energy
- [x] `maxwell/vortex_engine/magnetic_rotation.py` -- Magnetic rotation from vortices (Art. 829)

#### Remaining Tasks
- [ ] Implement Molecular Vortices animation (`animate_vortex_lattice()`) -- Art. 822
- [ ] Add vortex lattice animation with Manim
- [ ] Add vortex stability analysis

### Layer 81: Microscopic Theory (Molecular Currents, Diamagnetism)

#### Completed Tasks
- [x] `maxwell/molecular/amperes_theory.py` -- Ampere's molecular theory
- [x] `maxwell/molecular/neumanns_theory.py` -- Neumann's theory
- [x] `maxwell/molecular/webers_theory.py` -- Weber's molecular theory
- [x] `maxwell/molecular/competing_theories.py` -- Competing theory framework (Arts. 846-859)
- [x] `maxwell/physics/molecular_theory.py` -- Molecular theory of magnetism
- [x] Tests: `test_new_part_iv_molecular.py` (549 lines)

#### Remaining Tasks
- [ ] Add diamagnetism molecular model
- [ ] Add molecular current loop simulations
- [ ] Add competing theory comparison tests

### Layer 82: Competing Theories (Weber, Gauss, Neumann)

#### Completed Tasks
- [x] `maxwell/molecular/competing_theories.py` -- CompetingTheory framework
- [x] `maxwell/theories/failure_modes.py` -- Failure mode analysis (Arts. 857-859)
- [x] `maxwell/molecular/webers_theory.py` -- Weber's theory
- [x] `maxwell/molecular/amperes_theory.py` -- Ampere's theory
- [x] `maxwell/molecular/neumanns_theory.py` -- Neumann's theory

#### Remaining Tasks
- [ ] Add Gauss's electrodynamic theory module
- [ ] Add theory comparison benchmark tests
- [ ] Add failure mode demonstration scripts

### Layer 83: Philosophical Epilogue

#### Completed Tasks
- [x] `maxwell/philosophy/medium_check.py` -- Medium necessity proofs (Arts. 860-866)

#### Remaining Tasks
- [ ] Add philosophical analysis module
- [ ] Add historical context documentation

### Layer 84: Gauge Symmetries

#### Completed Tasks
- [x] `maxwell/math/gauge/manager.py` -- Gauge symmetry management

#### Remaining Tasks
- [ ] Add gauge transformation tests
- [ ] Add gauge invariance verification

### Layer 85: Visualization (Time-Domain)

#### Completed Tasks
- [x] `maxwell/vis/` -- 6 visualization modules (3 functional)
- [x] `maxwell/electromagnetism/vis/circular_fields.py` -- Circular field visualization (Art. 702)

#### Remaining Tasks
- [ ] Add time-domain visualization infrastructure
- [ ] Add animation framework for dynamic simulations

### Layer 86: Boundary Condition Manager

#### Completed Tasks
- [x] `maxwell/electromagnetism/current_sheets/boundary_conditions.py` -- Boundary conditions
- [x] `maxwell/fields/decomposition.py` -- Partial coverage

#### Remaining Tasks
- [ ] Create `maxwell/core/space/boundary.py` -- BoundaryManager class
- [ ] Add boundary condition types (Dirichlet, Neumann, Robin)
- [ ] Add boundary condition application tests

### Part IV JAX Adapters

#### Completed
- [x] `maxwell/jax/electromagnetism/ampere_maxwell.py` -- AmpereMaxwellLawJAX, DisplacementCurrentJAX (Arts. 606-607)
- [x] `maxwell/jax/electromagnetism/equations.py` -- MaxwellEquationsJAX, ElectromagneticFieldJAX
- [x] `maxwell/jax/electromagnetism/forces.py` -- LorentzForceJAX, MaxwellStressTensorJAX (Arts. 490-492, 641-646)
- [x] `maxwell/jax/electromagnetism/induction.py` -- FaradayInductionJAX (Arts. 528-531)
- [x] `maxwell/jax/electromagnetism/energy.py` -- ElectrostaticEnergyJAX, CapacitorEnergyJAX (Arts. 630-631)
- [x] `maxwell/jax/electromagnetism/magnetic_energy.py` -- MagneticEnergyJAX, InductorEnergyJAX (Arts. 632-633)
- [x] `maxwell/jax/electromagnetism/electrokinetic.py` -- ElectrokineticEnergyJAX, CoupledCircuitEnergyJAX (Arts. 634-638)
- [x] `maxwell/jax/electromagnetism/field.py` -- ElectricFieldJAX

#### Remaining
- [ ] Add JAX adapter for wave equation
- [ ] Add JAX adapter for radiation pressure
- [ ] Add JAX adapter for magneto-optics
- [ ] Add JAX adapter for vortex engine
- [ ] Add JAX adapter for vector potential visualization

### Part IV Visualization Tasks

#### Completed
- [x] `plot_stress_tensor_2d()` in `stress.py` -- 2D Maxwell stress tensor

#### Remaining
- [ ] `render_vector_potential_A()` -- Electrotonic State 3D (Art. 540/617)
- [ ] `render_cyclic_surface()` -- Helicoidal Potentials (Art. 487)
- [ ] `animate_vortex_lattice()` -- Molecular Vortices animation (Art. 822)
- [ ] `render_plane_wave()` -- EM Wave Propagation animation (Art. 791)

### Part IV Tests

#### Completed
- [x] `test_part_iv_electromagnetism.py` (1227 lines) -- Core Part IV tests
- [x] `test_part_iv_advanced.py` (1081 lines) -- Advanced Part IV tests
- [x] `test_new_part_iv_core.py` (984 lines) -- New core Part IV tests
- [x] `test_new_part_iv_math.py` (902 lines) -- Part IV mathematics tests
- [x] `test_new_part_iv_constitutive.py` (603 lines) -- Constitutive relations tests
- [x] `test_new_part_iv_charges_currents.py` (593 lines) -- Charges and currents tests
- [x] `test_new_part_iv_molecular.py` (549 lines) -- Molecular theory tests
- [x] `test_new_part_iv_optics.py` (782 lines) -- Optics tests
- [x] `test_new_part_iv_signal_calibration.py` (903 lines) -- Signal and calibration tests

---

## Part V: Infrastructure & Core (Layers 90-94)

**Status: 60% Complete**

### Layer 90: Simulation Kernel (EtherGrid)

#### Completed Tasks
- [x] `maxwell/sim/__init__.py` -- Package scaffold exists
- [x] `maxwell/solvers/induction_solvers.py` -- Induction solvers (partial)
- [x] `maxwell/solvers/shape_solvers.py` -- Shape-based solvers (partial)

#### Remaining Tasks (HIGH PRIORITY)
- [ ] Create `maxwell/sim/grid.py` -- EtherGrid class (spatial mesh / voxel / FEM)
- [ ] Create `maxwell/sim/medium.py` -- MediumProperties class
- [ ] Create `maxwell/sim/boundary.py` -- BoundaryManager class
- [ ] Add JAX jnp.sum() for parallel volume integrals
- [ ] Add spatial integrator engine
- [ ] Add grid-based field state storage
- [ ] Add FEM mesh generation
- [ ] Add voxel-based physics calculations
- [ ] Add EtherGrid initialization tests
- [ ] Add medium property assignment tests

### Layer 91: Coordinate Engine

#### Completed Tasks
- [x] `maxwell/math/vector_operators.py` -- gradient, divergence, curl
- [x] `maxwell/core/space/__init__.py` -- Space subpackage scaffold

#### Remaining Tasks
- [ ] Create `maxwell/math/coords/transform.py` -- CoordinateSystem class
- [ ] Create `maxwell/math/coords/operators.py` -- VectorOperators in various coordinates
- [ ] Add Cartesian, cylindrical, spherical, ellipsoidal coordinate systems
- [ ] Add coordinate transformation tests
- [ ] Add metric tensor calculations

### Layer 92: Time Integrator

#### Remaining Tasks (HIGH PRIORITY)
- [ ] Create `maxwell/sim/timestepper.py` -- RK4Integrator class
- [ ] Create `maxwell/sim/timestepper.py` -- SymplecticIntegrator class (energy conserving)
- [ ] Create `maxwell/sim/events.py` -- EventQueue class
- [ ] Create `maxwell/sim/timestepper.py` -- Adaptive step size controller
- [ ] Add time-stepping verification tests
- [ ] Add energy conservation verification for symplectic integrator
- [ ] Add RK4 accuracy order tests
- [ ] Add event detection and handling tests

### Layer 93: Global Constants & Configuration

#### Completed Tasks
- [x] `maxwell/config/constants.py` -- CONST, C (speed of light), universal constants
- [x] `maxwell/config/conventions.py` -- PolarityConvention, conventions
- [x] `maxwell/config/__init__.py` -- Config package init

#### Remaining Tasks
- [ ] Add SimulationConfig class with precision settings
- [ ] Add numerical tolerance configuration
- [ ] Add unit system configuration (CGS-EMU vs SI)

### Layer 94: Treatise Meta-Link (Citation Framework)

#### Completed Tasks
- [x] `maxwell/meta/citation.py` -- @maxwell_cite decorator, get_citation, get_all_citations
- [x] `maxwell/meta/__init__.py` -- Meta package init
- [x] 1,888 @maxwell_cite decorator usages across 160+ modules
- [x] Tests: `test_citation_decorator.py` (203 lines)

#### Remaining Tasks
- [ ] Create `maxwell/meta/explorer.py` -- get_theory_text function
- [ ] Add article text retrieval by number
- [ ] Add citation statistics and reporting
- [ ] Add citation compliance checker

### Part V Empty Scaffolds
- [ ] `maxwell/sim/` -- Only `__init__.py` (CRITICAL: Layer 90)
- [ ] `maxwell/core/space/` -- Only `__init__.py` (Layer 91)
- [ ] `maxwell/core/math/` -- Only `__init__.py`

---

## Part VI: Scalar Physics (Layers 95-97)

**Status: 0% Complete -- NOT STARTED**

### Layer 95: Superpotential & Hertz Vector

#### Remaining Tasks
- [ ] Create `maxwell/scalar/` directory
- [ ] Create `maxwell/scalar/__init__.py` -- Package init
- [ ] Create `maxwell/scalar/superpotential.py` -- SuperpotentialField (Chi) class
- [ ] Create `maxwell/scalar/hertz_vector.py` -- HertzVector (Pi) class
- [ ] Add superpotential-to-EM field derivation
- [ ] Add Hertz vector field calculations
- [ ] Add superpotential tests
- [ ] Add Hertz vector tests

### Layer 96: Force-Free Potentials & Longitudinal Waves

#### Remaining Tasks
- [ ] Create `maxwell/scalar/force_free.py` -- Force-free potentials
- [ ] Create `maxwell/scalar/longitudinal.py` -- Longitudinal wave propagation
- [ ] Add force-free field solutions
- [ ] Add longitudinal wave equation derivation
- [ ] Add longitudinal wave simulation
- [ ] Add force-free potential tests
- [ ] Add longitudinal wave tests

### Layer 97: Gravity-EM Unification

#### Remaining Tasks
- [ ] Create `maxwell/scalar/gravity_coupling.py` -- Gravity-EM unification (Kaluza-Klein 5D)
- [ ] Create `maxwell/scalar/detectors.py` -- ScalarInterferometer class
- [ ] Add Kaluza-Klein 5D metric
- [ ] Add scalar interferometer simulation
- [ ] Add gravity-EM coupling calculations
- [ ] Add Aharonov-Bohm phase visualization (Art. 16)
- [ ] Add Longitudinal Waves visualization (Art. 17)
- [ ] Add unification theory tests
- [ ] Add interferometer detection tests

### Part VI JAX Adapters (None Yet)
- [ ] Add SuperpotentialFieldJAX
- [ ] Add HertzVectorJAX
- [ ] Add LongitudinalWaveJAX
- [ ] Add KaluzaKleinJAX

### Part VI Tests (None Yet)
- [ ] Create `tests/test_scalar_physics.py` -- Target 200+ tests
- [ ] Create `tests/test_scalar_jax.py` -- JAX adapter tests
- [ ] Create `tests/test_kaluza_klein.py` -- 5D physics tests

---

## JAX Adapters

### JAX Infrastructure Files

#### Completed
- [x] `maxwell/jax/__init__.py` -- JAX package entry point, adapter registry
- [x] `maxwell/jax/_compat.py` -- Pytree registration, safe arithmetic
- [x] `maxwell/jax/_elliptic.py` -- Pure JAX elliptic integrals (AGM method)
- [x] `maxwell/jax/_scipy_special.py` -- JAX wrappers for scipy.special functions

### JAX Core Adapters

#### Completed
- [x] `maxwell/jax/core/charge.py` -- PointChargeJAX (Arts. 27-35)
- [x] `maxwell/jax/core/magnet.py` -- MagneticPoleJAX, MagnetJAX (Arts. 371-376)
- [x] `maxwell/jax/core/vector_potential.py` -- VectorPotentialJAX (Arts. 405-406)
- [x] `maxwell/jax/math/spherical_harmonics.py` -- SphericalHarmonicExpansionJAX (Arts. 128-146)

### JAX Electromagnetism Adapters

#### Completed
- [x] `maxwell/jax/electromagnetism/ampere_maxwell.py` -- AmpereMaxwellLawJAX, DisplacementCurrentJAX (Arts. 606-607)
- [x] `maxwell/jax/electromagnetism/conduction_3d.py` -- Conduction3DJAX, SpreadingResistanceJAX, EffectiveConductivityJAX (Arts. 285-296, 297-324)
- [x] `maxwell/jax/electromagnetism/electrokinetic.py` -- ElectrokineticEnergyJAX, CoupledCircuitEnergyJAX (Arts. 634-638)
- [x] `maxwell/jax/electromagnetism/electrolysis.py` -- FaradayLawsJAX, IonTransportJAX, PolarizationJAX, ElectrolysisCellJAX (Arts. 236-263)
- [x] `maxwell/jax/electromagnetism/energy.py` -- ElectrostaticEnergyJAX, CapacitorEnergyJAX (Arts. 630-631)
- [x] `maxwell/jax/electromagnetism/equations.py` -- MaxwellEquationsJAX, ElectromagneticFieldJAX (Arts. 598-603)
- [x] `maxwell/jax/electromagnetism/field.py` -- ElectricFieldJAX
- [x] `maxwell/jax/electromagnetism/forces.py` -- LorentzForceJAX, MaxwellStressTensorJAX (Arts. 490-492, 641-646)
- [x] `maxwell/jax/electromagnetism/induction.py` -- FaradayInductionJAX (Arts. 528-531)
- [x] `maxwell/jax/electromagnetism/joule_heating.py` -- JouleHeatingJAX, HeatDissipationJAX, SubstanceResistanceJAX (Arts. 242, 359-370)
- [x] `maxwell/jax/electromagnetism/magnetic_energy.py` -- MagneticEnergyJAX, InductorEnergyJAX (Arts. 632-633)
- [x] `maxwell/jax/electromagnetism/network_solver.py` -- NetworkSolverJAX, KirchhoffJAX, WheatstoneBridgeJAX, ReciprocityVerifierJAX (Arts. 273-284)
- [x] `maxwell/jax/electromagnetism/ohms_law.py` -- OhmsLawJAX, ResistanceJAX, ConductivityJAX, PowerDissipationJAX (Arts. 241-242)

### JAX Remaining Tasks
- [ ] Add JAX adapter for Lagrangian kernel (Layer 52)
- [ ] Add JAX adapter for EtherGrid (Layer 90)
- [ ] Add JAX adapter for time integrator (Layer 92)
- [ ] Add JAX adapter for wave equation
- [ ] Add JAX adapter for radiation pressure
- [ ] Add JAX adapter for magneto-optics (Faraday rotation)
- [ ] Add JAX adapter for vortex engine
- [ ] Add JAX adapter for hysteresis loop
- [ ] Add JAX adapter for terrestrial magnetism
- [ ] Add JAX adapter for dielectric conduction
- [ ] Add JAX adapter for thermoelectric effects
- [ ] Add JAX adapter for telegraph equation
- [ ] Add JAX adapter for Method of Images
- [ ] Add JAX adapter for scalar physics (Part VI -- 4 adapters)
- [ ] Add JAX adapter for vector potential visualization
- [ ] Add JAX GPU benchmarking suite
- [ ] Add JAX TPU compatibility tests
- [ ] Add JAX auto-diff gradient verification tests

---

## SymPy Symbolic Verifiers

### Completed (13/13)
- [x] `verify_div_curl` -- Divergence and curl identity (div(curl(F)) = 0)
- [x] `verify_grad_curl` -- Gradient-curl relationship (curl(grad(f)) = 0)
- [x] `verify_wave_equation_1d` -- 1D wave equation
- [x] `verify_laplace_spherical` -- Laplace equation in spherical coordinates
- [x] `verify_coulomb_law_symbolic` -- Coulomb's law symbolic proof
- [x] `verify_biot_savart` -- Biot-Savart law verification
- [x] `verify_faraday_symbolic` -- Faraday's law symbolic
- [x] `verify_continuity_equation` -- Charge conservation
- [x] `verify_maxwell_correction` -- Maxwell's displacement current correction
- [x] `verify_stokes_theorem` -- Stokes' theorem
- [x] `verify_lorentz_force` -- Lorentz force properties
- [x] `verify_stress_tensor_properties` -- Stress tensor identities
- [x] `verify_ampere_law` -- Ampere's law verification

### Remaining
- [ ] Add symbolic verification for quaternion identities
- [ ] Add symbolic verification for spherical harmonic orthogonality
- [ ] Add symbolic verification for gauge invariance
- [ ] Add symbolic verification for energy conservation
- [ ] Add symbolic verification for Lagrangian equations of motion

---

## Visualization

### Completed (3/17)

#### Visualization Infrastructure
- [x] `maxwell/vis/__init__.py` -- Package exports with graceful degradation (37 lines)
- [x] `maxwell/vis/_base.py` -- Mesh grid and evaluation utilities (89 lines)
- [x] `maxwell/vis/_compat.py` -- Matplotlib import with graceful fallback (100 lines)

#### Implemented Visualizations
- [x] `maxwell/vis/field_lines.py` -- `plot_field_lines_2d()` (154 lines) -- 2D electric/magnetic field line streamlines
- [x] `maxwell/vis/equipotential.py` -- `plot_equipotentials_2d()` (134 lines) -- 2D equipotential contour lines
- [x] `maxwell/vis/stress.py` -- `plot_stress_tensor_2d()` (159 lines) -- 2D Maxwell stress tensor quiver field
- [x] `maxwell/electromagnetism/vis/circular_fields.py` -- Circular field visualization (Art. 702)
- [x] Tests: `test_vis.py` (242 lines, 23 test functions)

### Remaining Visualizations by Part

#### Part I: Electrostatics (2 remaining)
- [ ] `render_virtual_images()` -- Method of Images visualization (Art. 155) -- Module: `maxwell/vis/geometry.py`
- [ ] `render_density_heatmap()` -- Edge Singularities heatmap (Art. 191) -- Module: `maxwell/vis/scalar.py`

#### Part II: Electrokinematics (3 remaining)
- [ ] `render_tubes()` -- Unit Tubes of Flow (Art. 290) -- Module: `maxwell/vis/flow.py`
- [ ] `render_joule_heating()` -- Thermal Gradients overlay (Art. 242/249) -- Module: `maxwell/vis/scalar.py`
- [ ] `plot_transient_recovery()` -- Dielectric Soakage time-series (Art. 329) -- Module: `maxwell/vis/plots.py`

#### Part III: Magnetism (3 remaining)
- [ ] `render_solid_angle_cap()` -- Magnetic Shell (Art. 409) -- Module: `maxwell/vis/geometry.py`
- [ ] `render_gauss_harmonics()` -- Spherical Harmonic Globes (Art. 467) -- Module: `maxwell/vis/geophysics.py`
- [ ] `animate_hysteresis_cycle()` -- Hysteresis Loops animation (Art. 442) -- Module: `maxwell/vis/plots.py`

#### Part IV: Electromagnetism (5 remaining)
- [ ] `render_vector_potential_A()` -- Electrotonic State 3D (Art. 540/617) -- Module: `maxwell/vis/vector.py`
- [ ] 3D Stress Tensor ellipsoids (Art. 641) -- Extend `maxwell/vis/stress.py`
- [ ] `render_cyclic_surface()` -- Helicoidal Potentials (Art. 487) -- Module: `maxwell/vis/topology.py`
- [ ] `animate_vortex_lattice()` -- Molecular Vortices (Art. 822) -- Module: `maxwell/vis/mechanical.py`
- [ ] `render_plane_wave()` -- EM Wave Propagation (Art. 791) -- Module: `maxwell/vis/optics.py`

#### Part VI: Scalar Physics (2 remaining)
- [ ] `render_potential_fog()` -- Aharonov-Bohm Phase (Extension) -- Requires Part VI implementation
- [ ] `animate_longitudinal_pulse()` -- Longitudinal Waves (Extension) -- Requires Part VI implementation

### Visualization Technology Stack Tasks

#### Completed
- [x] Matplotlib integration with graceful degradation
- [x] Base visualization infrastructure
- [x] 23 visualization test functions

#### Remaining
- [ ] Integrate PyVista as optional dependency (`[viz3d]` extra)
- [ ] Integrate Manim as optional dependency (`[anim]` extra)
- [ ] Add PyVista 3D mesh rendering support
- [ ] Add Manim animation rendering support
- [ ] Add JAX-accelerated visualization (GPU field line rendering)
- [ ] Add interactive visualization support (matplotlib widgets)
- [ ] Add static image export (PNG, SVG, PDF)
- [ ] Add animated GIF export
- [ ] Add video export (MP4)
- [ ] Add visualization performance benchmarks

---

## CI/CD

### Completed Workflows (5/5)

- [x] `.github/workflows/test.yml` -- Tests (3 OS x 4 Python = 12 jobs, installs `.[dev,accel]`)
- [x] `.github/workflows/lint.yml` -- Lint (Black, isort, mypy on ubuntu-latest, Python 3.12)
- [x] `.github/workflows/coverage.yml` -- Coverage (pytest-cov with term-missing, XML report)
- [x] `.github/workflows/math-verification.yml` -- Math Verification (50 validations, `.[dev,accel]`)
- [x] `.github/workflows/publish.yml` -- PyPI Publish (build -> twine check -> OIDC publish -> smoke test)

### Remaining CI/CD Tasks
- [ ] Create JAX-specific CI workflow (JAX GPU tests, TPU compatibility checks)
- [ ] Create visualization CI workflow (matplotlib rendering tests, image diff tests)
- [ ] Create documentation build CI workflow (Sphinx/Markdown docs)
- [ ] Add Codecov integration for coverage reporting
- [ ] Add dependabot configuration for dependency updates
- [ ] Add release notes automation
- [ ] Add version bump automation
- [ ] Add branch protection rules documentation
- [ ] Add PR template
- [ ] Add issue templates (bug report, feature request)
- [ ] Add pre-commit hooks (black, isort, mypy, pytest)

---

## Documentation

### Completed Documentation Files

#### Root-Level (7 files)
- [x] `README.md` -- Primary documentation (~330 lines, updated for 1542 tests)
- [x] `CHANGELOG.md` -- Version history in Keep a Changelog format
- [x] `CONTRIBUTING.md` -- Developer contribution guide with pytest markers
- [x] `LICENSE` -- MIT License
- [x] `CITATION.cff` -- Citation metadata for academic use
- [x] `MANIFEST.in` -- Source distribution manifest
- [x] `pyproject.toml` -- Build configuration with optional dependencies

#### docs/ Directory (13 files)
- [x] `docs/API_REFERENCE.md` -- Module-by-module API index (updated for 1542 tests)
- [x] `docs/COVERAGE_SUMMARY.md` -- Article coverage by Part (866/866)
- [x] `docs/USE_CASES.md` -- Practical guide with 20+ code examples
- [x] `docs/validation_report.md` -- Test results, math validation, import verification
- [x] `docs/FAQ.md` -- Frequently asked questions
- [x] `docs/MASTER_PLAN.md` -- 1361-line comprehensive audit (created Loop 12)
- [x] `docs/ARCHITECTURE_ANALYSIS_REPORT.md` -- 614-line cross-analysis report
- [x] `docs/PIPELINE_SUMMARY.md` -- 608-line pipeline completion summary
- [x] `docs/VISUALIZATION_AUDIT.md` -- 289-line visualization gap audit
- [x] `docs/INTEROP.md` -- Interoperability guide
- [x] `docs/JOSS_PAPER_PLAN.md` -- JOSS paper planning document
- [x] `docs/PHASE2_EXECUTION_PLAN.md` -- Phase 2 planning document
- [x] `docs/STRATEGIC_ROADMAP.md` -- Strategic roadmap

#### Package-Level Documentation
- [x] `maxwell/jax/README.md` -- JAX adapter registry documentation

### Remaining Documentation Tasks
- [ ] Create `examples/` directory with 5-10 Jupyter notebooks
  - [ ] Notebook: Coulomb's law and electric fields
  - [ ] Notebook: Lorentz force and particle trajectories
  - [ ] Notebook: Faraday induction and self-inductance
  - [ ] Notebook: Maxwell's equations in differential form
  - [ ] Notebook: JAX acceleration comparison (CPU vs GPU)
  - [ ] Notebook: Spherical harmonic expansion
  - [ ] Notebook: Network solver and circuit analysis
  - [ ] Notebook: Electromagnetic wave propagation
  - [ ] Notebook: Hysteresis modeling
  - [ ] Notebook: Molecular vortex simulation
- [ ] Update API_REFERENCE.md for all 37 JAX adapter classes
- [ ] Create type stubs (`.pyi` files) for public API
- [ ] Create tutorials for each Part of the Treatise
- [ ] Create installation troubleshooting guide
- [ ] Create JAX GPU setup guide
- [ ] Create Manim animation tutorial
- [ ] Create PyVista 3D visualization tutorial
- [ ] Document all empty subpackage purposes in their `__init__.py` files
- [ ] Create architecture decision records (ADRs)
- [ ] Create JOSS paper manuscript
- [ ] Create Zenodo archival DOI

---

## Package Infrastructure

### Completed
- [x] `maxwell/__init__.py` -- Package entry point with exports
- [x] `pyproject.toml` -- Build system, metadata, dependencies, optional deps
- [x] Optional dependency groups: `dev`, `enhanced`, `viz`, `symbolic`, `accel`, `all`
- [x] Python 3.10-3.13 classifiers
- [x] Pytest markers: `jax`, `sympy`, `slow`, `visualization`
- [x] Black target-version configuration
- [x] mypy type checking configuration
- [x] isort import ordering configuration
- [x] Tests: `test_version_sync.py` (50 lines) -- Version synchronization
- [x] Tests: `test_module_checks.py` (252 lines) -- Module-level verification
- [x] Tests: `run_quality_checks.py` (704 lines) -- Quality check runner
- [x] Tests: `conftest.py` -- pytest fixtures and configuration

### Remaining Package Infrastructure Tasks
- [ ] Add version bump to 1.0.0 for stable release
- [ ] Add type stubs (`.pyi` files) for IDE support
- [ ] Add package entry points for CLI tools
- [ ] Add `maxwell --version` CLI command
- [ ] Add `maxwell --test` CLI command
- [ ] Add `maxwell --cite` CLI command
- [ ] Add examples directory with sample scripts
- [ ] Add MANIFEST.in completeness verification
- [ ] Add setup.cfg if needed for additional config
- [ ] Add py.typed marker file for PEP 561 compliance

---

## Test Suite

### Completed Test Files (27 files)

#### Core Physics Tests (9 files)
- [x] `tests/test_cgs_units.py` (363 lines) -- CGS unit tests
- [x] `tests/test_citation_decorator.py` (203 lines) -- Citation system tests
- [x] `tests/test_part_iv_electromagnetism.py` (1227 lines) -- Core Part IV tests
- [x] `tests/test_part_iv_advanced.py` (1081 lines) -- Advanced Part IV tests
- [x] `tests/test_magnetic_measurements.py` (1005 lines) -- Magnetic measurement tests
- [x] `tests/test_vis.py` (242 lines) -- Visualization tests
- [x] `tests/test_verification_framework.py` (213 lines) -- Verification framework tests
- [x] `tests/test_convergence.py` (171 lines) -- Convergence tests
- [x] `tests/test_cross_validation.py` (126 lines) -- Cross-validation tests

#### Part IV Specialized Tests (7 files)
- [x] `tests/test_new_part_iv_core.py` (984 lines) -- New core Part IV tests
- [x] `tests/test_new_part_iv_math.py` (902 lines) -- Part IV mathematics tests
- [x] `tests/test_new_part_iv_signal_calibration.py` (903 lines) -- Signal and calibration tests
- [x] `tests/test_new_part_iv_optics.py` (782 lines) -- Optics tests
- [x] `tests/test_new_part_iv_constitutive.py` (603 lines) -- Constitutive relations tests
- [x] `tests/test_new_part_iv_charges_currents.py` (593 lines) -- Charges and currents tests
- [x] `tests/test_new_part_iv_molecular.py` (549 lines) -- Molecular theory tests

#### JAX Adapter Tests (6 files)
- [x] `tests/test_jax_adapter.py` (4891 lines) -- Comprehensive JAX adapter tests
- [x] `tests/test_ohms_law_jax.py` (623 lines) -- Ohm's law JAX tests
- [x] `tests/test_network_solver_jax.py` (801 lines) -- Network solver JAX tests
- [x] `tests/test_conduction_3d_jax.py` (618 lines) -- 3D conduction JAX tests
- [x] `tests/test_electrolysis_jax.py` (818 lines) -- Electrolysis JAX tests
- [x] `tests/test_joule_heating_jax.py` (738 lines) -- Joule heating JAX tests

#### SymPy & Quality Tests (3 files)
- [x] `tests/test_sympy_verify.py` (422 lines) -- 13 SymPy symbolic verifiers
- [x] `tests/test_module_checks.py` (252 lines) -- Module-level verification
- [x] `tests/run_quality_checks.py` (704 lines) -- Quality check runner

#### Configuration (2 files)
- [x] `tests/conftest.py` -- pytest fixtures
- [x] `tests/test_version_sync.py` (50 lines) -- Version synchronization

### Remaining Test Tasks
- [ ] Create `tests/test_lagrangian.py` -- Lagrangian kernel tests (Layer 52)
- [ ] Create `tests/test_ether_grid.py` -- EtherGrid tests (Layer 90)
- [ ] Create `tests/test_timestepper.py` -- Time integrator tests (Layer 92)
- [ ] Create `tests/test_scalar_physics.py` -- Part VI scalar physics tests
- [ ] Create `tests/test_boundary_conditions.py` -- Boundary condition manager tests (Layer 86)
- [ ] Create `tests/test_coordinate_transforms.py` -- Coordinate system tests (Layer 91)
- [ ] Create `tests/test_material_database.py` -- Material database tests (Layer 29)
- [ ] Create `tests/test_thermoelectric.py` -- Thermoelectric effect tests (Layer 17)
- [ ] Create `tests/test_hysteresis.py` -- Hysteresis model tests
- [ ] Create `tests/test_wave_equation_jax.py` -- JAX wave equation tests
- [ ] Add line coverage measurement (currently unmeasured)
- [ ] Target 80%+ line coverage
- [ ] Add mutation testing
- [ ] Add property-based tests (hypothesis library)
- [ ] Add performance benchmark tests
- [ ] Add regression tests for known issues

---

## Cross-Repo Architecture Repo

### Tasks
- [ ] Create `maxwell-treatise/architecture` GitHub repository
- [ ] Copy 16 architecture documents from `archive/docs/` to `maps/` directory:
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART I.md`
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART II.md`
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART III.md`
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART IV.md`
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART V.md`
  - [ ] `Maxwell's Treatise_ Modernized Architecture Map - PART VI.md`
  - [ ] `Maxwell_Treatise_Part_I_Architecture_COMPLETE.md`
  - [ ] `Maxwell_Treatise_Part_II_Architecture_COMPLETE.md`
  - [ ] `Maxwell_Treatise_Part_III_Architecture_COMPLETE.md`
  - [ ] `Maxwell_Treatise_Part_IV_Architecture_COMPLETE.md`
  - [ ] `Maxwell_Treatise_Part_V_Architecture_COMPLETE.md`
  - [ ] `Maxwell_Treatise_Part_VI_Architecture_COMPLETE.md`
  - [ ] `Maxwell's Treatise_ The Visualization Strategy.md`
  - [ ] `Maxwell's Treatise_ The Master Synthesis - A Modern Computational Architecture for Classical Physics.md`
  - [ ] Plus: `future-where-to-resume-left-off.md`
  - [ ] Plus: `Maxwell-Treatise-Version3-Volume1-PART I - ELECTROSTATICS.md` through `PART IV`
- [ ] Create `validation/` directory with cross-analysis scripts:
  - [ ] `validation/cross_check.py` -- Planned vs. implemented analyzer
  - [ ] `validation/layer_coverage.py` -- Layer-by-layer coverage tracker
  - [ ] `validation/visualization_audit.py` -- 17 vis vs. implemented checker
  - [ ] `validation/article_traceability.py` -- Article-to-code mapping validator
  - [ ] `validation/report.py` -- Cross-repo report generator
- [ ] Create `reports/` directory:
  - [ ] `reports/coverage_report.json` -- Machine-readable coverage
  - [ ] `reports/visualization_report.md` -- Visualization gap report
  - [ ] `reports/master_audit.md` -- Full cross-analysis report
- [ ] Create `sync/sync_from_codebase.sh` -- Script to pull latest from codebase repo
- [ ] Set up CI workflow in architecture repo:
  - [ ] Weekly cross-analysis run
  - [ ] Fetch latest codebase state via GitHub API
  - [ ] Run cross-analysis scripts
  - [ ] Commit updated coverage reports
  - [ ] Open issues for missing implementations
- [ ] Create architecture repo README.md
- [ ] Set up repo-level branch protection

---

## Empty Subpackage Scaffolds (26 directories with only __init__.py)

### High Priority (Critical Path)
- [ ] `maxwell/sim/` -- Layer 90 EtherGrid (needed for dynamic simulation)
- [ ] `maxwell/materials/database/` -- Layer 29 material database (needed for realistic simulations)

### Medium Priority
- [ ] `maxwell/core/space/` -- Layer 91 coordinate transforms
- [ ] `maxwell/magnetism/geophysics/` -- Layer 41 geophysics applications
- [ ] `maxwell/magnetism/instruments/` -- Layer 42 magnetic instruments
- [ ] `maxwell/instruments/absolute/` -- Layer 72 absolute resistance
- [ ] `maxwell/instruments/calibration/` -- Layer 71 coil calibration

### Low Priority (Existing Coverage Elsewhere)
- [ ] `maxwell/chemistry/` -- Part II extension
- [ ] `maxwell/thermodynamics/` -- Part II extension (thermoelectric)
- [ ] `maxwell/kinematics/` -- Part IV extension
- [ ] `maxwell/telecom/` -- Part V extension (note: telegraphy.py exists at root level)
- [ ] `maxwell/core/math/` -- Layer 60 math kernel (covered elsewhere)
- [ ] `maxwell/fields/` -- Part IV fields (covered in electromagnetism/)
- [ ] `maxwell/magnetism/calculus/` -- Part III math (covered in calculus/)
- [ ] `maxwell/magnetism/components/` -- Part III (covered in components/)
- [ ] `maxwell/magnetism/core/` -- Part III (covered in core/)
- [ ] `maxwell/magnetism/fields/` -- Part III (covered in fields/)
- [ ] `maxwell/magnetism/geometry/` -- Part III (covered in geometry/)
- [ ] `maxwell/magnetism/materials/` -- Part III (covered in materials/)
- [ ] `maxwell/magnetism/mechanics/` -- Part III (covered in mechanics/)
- [ ] `maxwell/magnetism/physics/` -- Part III physics
- [ ] `maxwell/magnetism/solvers/` -- Part III solvers
- [ ] `maxwell/electromagnetism/field_theory/` -- Only `__init__.py`
- [ ] `maxwell/electromagnetism/units/` -- Only `__init__.py`
- [ ] `maxwell/magnetics/` -- Only `__init__.py`
- [ ] `maxwell/experiments/` -- Only `__init__.py` (note: ratio_v/ has implementations)

### Part VI (Does Not Exist At All)
- [ ] `maxwell/scalar/` -- Directory does not exist; needs to be created

---

## Archive Documents (27 files in archive/docs/)

### Architecture Maps (6 files)
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART I.md`
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART II.md`
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART III.md`
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART IV.md`
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART V.md`
- [x] `Maxwell's Treatise_ Modernized Architecture Map - PART VI.md`

### Architecture Complete Documents (6 files)
- [x] `Maxwell_Treatise_Part_I_Architecture_COMPLETE.md`
- [x] `Maxwell_Treatise_Part_II_Architecture_COMPLETE.md`
- [x] `Maxwell_Treatise_Part_III_Architecture_COMPLETE.md`
- [x] `Maxwell_Treatise_Part_IV_Architecture_COMPLETE.md`
- [x] `Maxwell_Treatise_Part_V_Architecture_COMPLETE.md`
- [x] `Maxwell_Treatise_Part_VI_Architecture_COMPLETE.md`

### Strategy Documents (2 files)
- [x] `Maxwell's Treatise_ The Visualization Strategy.md`
- [x] `Maxwell's Treatise_ The Master Synthesis - A Modern Computational Architecture for Classical Physics.md`

### Source Documents (4 files)
- [x] `Maxwell-Treatise-Version3-Volume1-PART I - ELECTROSTATICS.md`
- [x] `Maxwell-Treatise-Version3-Volume1-PART II - ELECTROKINEMATICS.md`
- [x] `Maxwell-Treatise-Version3-Volume2-PART III - MAGNETISM.md`
- [x] `Maxwell-Treatise-Version3-Volume2-PART IV - ELECTROMAGNETISM.md`

### Historical Documents (9 files)
- [x] `future-where-to-resume-left-off.md`
- [x] `IMPLEMENTATION_CHECKLIST.md`
- [x] `INTEGRATION_REPORT.md`
- [x] `math_infrastructure_assessment.md`
- [x] `MAXWELL_OCR_AUDIT_REPORT.md`
- [x] `QUALITY_REVIEW_REPORT.md`
- [x] `start.md`
- [x] `validation_report.md`
- [x] `verification_report.md`

---

## Priority Phases

### Phase 1: Critical Path (Immediate -- Complete Core Architecture)

| Priority | Task | Layer | Effort | Dependencies |
|----------|------|-------|--------|-------------|
| **P0** | Implement Lagrangian Kernel (GeneralizedSystem) | 52 | High | JAX auto-diff (available) |
| **P0** | Implement EtherGrid simulation kernel | 90 | High | JAX jnp.sum() (available) |
| **P0** | Implement TimeStepper (RK4 + Symplectic) | 92 | Medium | EtherGrid (above) |
| **P1** | Populate materials database | 29 | Medium | None |
| **P1** | Implement BoundaryManager | 86 | Medium | EtherGrid |
| **P1** | Implement coordinate transforms | 91 | Medium | Vector operators exist |

### Phase 2: Visualization Completion (Near-term)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| **P1** | Method of Images visualization (Art. 155) | Medium | Image solver exists |
| **P1** | Edge singularities heatmap (Art. 191) | Low-Medium | Grid tools exist |
| **P1** | Hysteresis loop animation (Art. 442) | Low | Hysteresis model exists |
| **P2** | Dielectric soakage transient plot (Art. 329) | Low | Time-series needed |
| **P2** | Thermal gradients overlay (Art. 242/249) | Medium | Joule heating exists |
| **P2** | Integrate PyVista for 3D rendering | Medium | New dependency |
| **P2** | Magnetic Shell visualization (Art. 409) | Medium | Solid angle exists |
| **P2** | Spherical Harmonic Globes (Art. 467) | High | Gauss expansion exists |

### Phase 3: Completeness (Medium-term)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| **P2** | Implement geophysics module (Layer 41) | High | Spherical harmonics exist |
| **P2** | Implement magnetic instruments (Layer 42) | Medium | Instruments framework exists |
| **P3** | Complete 3D visualizations (stress ellipsoids, vector potential) | High | PyVista needed |
| **P3** | Integrate Manim for animations | High | New dependency |
| **P3** | EM Wave Propagation animation (Art. 791) | High | Plane wave module exists |
| **P3** | Molecular Vortices animation (Art. 822) | Very High | Vortex engine exists |

### Phase 4: Documentation & Examples (Medium-term)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| **P1** | Create examples/ directory with Jupyter notebooks | High | All Parts I-V complete |
| **P1** | Update API_REFERENCE.md for all JAX adapters | Medium | Current codebase |
| **P2** | Create type stubs (.pyi files) | Medium | Current codebase |
| **P2** | Create JOSS paper manuscript | High | All Parts complete |
| **P3** | Populate empty subpackage __init__.py docstrings | Low | Current codebase |

### Phase 5: Research Frontier (Long-term)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| **P3** | Implement Scalar Physics (Part VI) | Very High | All Parts I-V complete |
| **P3** | Aharonov-Bohm phase visualization | Very High | Part VI complete |
| **P3** | Longitudinal wave simulation | Very High | Part VI complete |
| **P3** | Kaluza-Klein 5D implementation | Very High | Part VI complete |

### Phase 6: Cross-Repo Architecture (Parallel)

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| **P2** | Create maxwell-treatise/architecture repo | Low | None |
| **P2** | Copy 16 architecture documents | Low | Repo created |
| **P2** | Build cross-analysis script | Medium | Repo created |
| **P2** | Set up CI workflow | Medium | Scripts complete |

---

## Metrics Tracking

### Completion by Part

| Part | Articles | Layers | Modules | Tests | JAX Classes | Visualizations | % Complete |
|------|----------|--------|---------|-------|-------------|----------------|------------|
| I: Electrostatics | 203 | 13 | 15+ | 629+ | 5 | 2/4 | 95% |
| II: Electrokinematics | 141 | 18 | 15+ | 847+ | 13 | 0/3 | 85% |
| III: Magnetism | 104 | 13 | 10+ | 1005+ | 3 | 0/3 | 70% |
| IV: Electromagnetism | 392 | 44 | 50+ | 6000+ | 9 | 1/5 | 82% |
| V: Infrastructure | 16 | 5 | 5+ | 213+ | 0 | 0/0 | 60% |
| VI: Scalar Physics | 10 | 3 | 0 | 0 | 0 | 0/2 | 0% |

### Cumulative Statistics

| Metric | Value |
|--------|-------|
| Total Python modules | 276 (81 init + 195 implementation) |
| Total test files | 27 |
| Total test functions | 1,542 |
| Total lines of test code | ~19,142 |
| JAX adapter files | 24 |
| JAX adapter classes | 37 |
| SymPy verifiers | 13 |
| CI workflows | 5 |
| Documentation files | 13 (docs/) + 7 (root) + 1 (package) |
| Architecture documents | 27 (archive/docs/) |
| Empty subpackage scaffolds | 24 |
| Maxwell articles covered | 866 / 866 (100%) |
| @maxwell_cite decorator usages | 1,889 |
| PyPI version | 0.1.0 |
| PyPI URL | https://pypi.org/p/maxwell |

---

*This is the definitive task tracking document for the Maxwell Modernized project. All checkboxes reflect the actual state of the codebase as of 2026-05-06. Update this document as tasks are completed.*
