# Maxwell Modernized — API Reference

**Version:** 1.0.0
**Generated:** 2026-04-26
**Coverage:** 866/866 articles (100%) across all 4 Parts of Maxwell's Treatise
**Tests:** 1542/1542 passing (629 core + 847 JAX + 66 SymPy)
**Modules:** 241 Python modules, 80+ subpackages

---

## Quick Start

```python
from maxwell import (
    PointCharge, LorentzForce, MaxwellStressTensor, FaradayInduction,
    MaxwellEquations, ElectromagneticField, PlaneWave,
    SphericalHarmonicExpansion, LegendrePolynomial, EllipticIntegral,
    CGSUnitConverter, CONST, C,
)

# Speed of light in CGS
print(f"c = {C:.4e} cm/s")

# Point charge field
from maxwell import PointCharge
import numpy as np
q = PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))
E = q.field_at(np.array([1.0, 0.0, 0.0]))

# Lorentz force on a wire
from maxwell import LorentzForce
F = LorentzForce(current=1.0, length=np.array([0.0, 0.0, 10.0]),
                 B_field=np.array([0.0, 100.0, 0.0]))
force = F.force_vector()
```

---

## Public API — Top-Level Imports

All 39 symbols importable directly from `maxwell`:

### Core Primitives (5)

| Name | Type | Source | Description |
|---|---|---|---|
| `PointCharge` | class | `maxwell.core.charge` | Point charge with `q` and `position`; computes E-field via Coulomb's law |
| `ElectricField` | class | `maxwell.core.field` | Electric field abstraction with flux, tension, and Gauss law methods |
| `ElectricPotential` | class | `maxwell.core.potential` | Scalar potential with Laplace/Poisson equation solvers |
| `Magnet` | class | `maxwell.core.magnet` | Magnetic body with pole strength, axis, and mutual action methods |
| `MagneticMoment` | class | `maxwell.core.moment` | Magnetic dipole moment vector representation |

### Constants & Units (4)

| Name | Type | Source | Description |
|---|---|---|---|
| `CONST` | class | `maxwell.config.constants` | Universal constants (c, pi, e, etc.) in CGS units |
| `C` | float | `maxwell.config.constants` | Speed of light: 2.99792458e10 cm/s |
| `CGSUnitConverter` | class | `maxwell.core.units` | Convert between CGS, SI, and practical units |
| `MagneticDimensions` | class | `maxwell.core.units` | Dimensional analysis for electromagnetic quantities |

### Forces (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `LorentzForce` | class | `maxwell.electromagnetism.forces.lorentz` | Force on current-carrying conductor: F = I*L x B |
| `MaxwellStressTensor` | class | `maxwell.electromagnetism.forces.stress_tensor` | Electromagnetic stress tensor T_ij with eigenvalue analysis |

### Induction (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `FaradayInduction` | class | `maxwell.electromagnetism.induction.faraday` | Induced EMF from changing magnetic flux and motional EMF |

### Theory (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `MaxwellEquations` | class | `maxwell.electromagnetism.theory.general_equations` | All 7 Maxwell equations (A-G) with numerical verification |
| `ElectromagneticField` | class | `maxwell.electromagnetism.theory.general_equations` | Complete EM field state (E, B, H, D, J, rho, potentials) |

### Energy (3)

| Name | Type | Source | Description |
|---|---|---|---|
| `calc_magnetic_energy_density` | func | `maxwell.electromagnetism.energy.magnetic` | u = B^2/(8*pi) in CGS vacuum |
| `calc_total_magnetic_energy` | func | `maxwell.electromagnetism.energy.magnetic` | Integrate magnetic energy density over volume |
| `calc_electrostatic_energy_density` | func | `maxwell.electromagnetism.energy.electrostatic` | u = E^2/(8*pi) in CGS vacuum |

### Fields (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `AmpereMaxwellLaw` | class | `maxwell.electromagnetism.fields.ampere_maxwell` | curl H = (4*pi/c)*J + (1/c)*dD/dt |
| `DisplacementCurrent` | class | `maxwell.electromagnetism.fields.ampere_maxwell` | Displacement current density dD/dt |

### Electrostatics (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `DielectricMaterial` | class | `maxwell.electrostatics.dielectrics` | Dielectric with permittivity, polarization, bound charge |

### Electrokinematics (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `NetworkAnalyzer` | class | `maxwell.electrokinematics.network_solver` | Circuit analysis with Kirchhoff's laws, Wheatstone bridge |

### Magnetism (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `GeomagneticElements` | class | `maxwell.magnetism.terrestrial_magnetism` | Earth's magnetic field: declination, dip, intensity |

### Optics (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `PlaneWave` | class | `maxwell.optics.wave_equation` | Electromagnetic plane wave solutions |

### Mathematics (3)

| Name | Type | Source | Description |
|---|---|---|---|
| `SphericalHarmonicExpansion` | class | `maxwell.math.spherical_harmonics` | Expand functions in spherical harmonic series |
| `LegendrePolynomial` | class | `maxwell.math.spherical_harmonics` | Legendre polynomials P_l(x) and associated P_l^m(x) |
| `EllipticIntegral` | class | `maxwell.math.elliptic_integrals` | Complete and incomplete elliptic integrals K(k), E(k) |

### Instruments (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `TangentGalvanometer` | class | `maxwell.instruments.galvanometers` | Tangent galvanometer for current measurement |
| `HelmholtzCoil` | class | `maxwell.instruments.helmholtz` | Helmholtz coil pair with uniform field region |

### Materials (5)

| Name | Type | Source | Description |
|---|---|---|---|
| `Magnetization` | class | `maxwell.materials.constitutive` | B = (1 + 4*pi*chi)*H constitutive relation |
| `ElectricDisplacement` | class | `maxwell.materials.constitutive` | D = epsilon*E constitutive relation |
| `Conductivity` | class | `maxwell.materials.constitutive` | J = sigma*E Ohm's law constitutive relation |
| `Permeability` | class | `maxwell.materials.constitutive` | Magnetic permeability mu = 1 + 4*pi*chi |
| `HysteresisLoop` | class | `maxwell.materials.hysteresis` | Hysteresis loop simulation with retentivity, coercivity |

### Engineering (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `ShipMagnetism` | class | `maxwell.engineering` | Ship magnetization model with compass correction |
| `MagneticCompass` | class | `maxwell.engineering` | Magnetic compass deviation and correction analysis |

### Competing Theories (1)

| Name | Type | Source | Description |
|---|---|---|---|
| `CompetingTheory` | class | `maxwell.molecular.competing_theories` | Historical theory comparison framework |

### Citation System (2)

| Name | Type | Source | Description |
|---|---|---|---|
| `get_citation` | func | `maxwell.meta.citation` | Get citation info for a Maxwell article number |
| `get_all_citations` | func | `maxwell.meta.citation` | List all available citations |

---

## Complete Module Index

### maxwell.core — Core Physics

| Module | Public API | Articles |
|---|---|---|
| `charge` | `PointCharge(q, position)` → `field_at(point)` | 29, 30, 45, 245 |
| `field` | `ElectricField`, `gauss_law_closed_surface`, `electric_flux` | 44, 46-49, 68-71, 76 |
| `potential` | `ElectricPotential`, `laplace_equation`, `poisson_equation`, `solve_laplace`, `solve_poisson` | 45, 70, 72, 73, 77, 78, 85 |
| `magnet` | `Magnet`, `MagneticPole`, `MagneticAxis`, `mutual_action`, `earth_response` | 371-376, 392 |
| `moment` | `MagneticMoment`, `MagnetizationVector`, `MagneticParticle`, `resultant_moment_and_axis` | 381-384, 389, 390 |
| `measurement` | `cgs_unit_of`, `resistance_units`, `potential_units`, `current_units` | 2-26 |

### maxwell.core.units — Units & Dimensional Analysis

| Module | Public API | Articles |
|---|---|---|
| `units` | `CGSUnitConverter` → `cgs_to_si_*`, `si_to_cgs_*` | — |
| `dimensions` | `ElectromagneticUnit`, `ESUDimensions`, `EMUDimensions`, `get_esu_dimensions`, `get_emu_dimensions`, `calc_unit_ratio`, `verify_speed_of_light_relationship`, `convert_esu_to_emu`, `verify_dimensional_consistency` | 440-445 |

### maxwell.config — Constants & Conventions

| Module | Public API | Articles |
|---|---|---|
| `constants` | `CONST` (universal constants), `C` (speed of light), `cgs_unit_of` | — |
| `conventions` | `PolarityConvention`, `ForceDirectionConvention`, `MagneticDirection`, `verify_austral_positive`, `right_hand_rule_direction` | 28-37 |

### maxwell.calculus — Integral Theorems

| Module | Public API | Articles |
|---|---|---|
| `cyclic` | `CyclicFunction`, `calc_solid_angle_closed_curve`, `solid_angle_double_line_integral`, `vector_potential_closed_curve` | 53-54 |
| `integrals` | `MagneticLineIntegral`, `MagneticSurfaceIntegral`, `calc_line_integral_force`, `calc_surface_induction`, `amperes_law_integral` | 28-33 |
| `vector_potential` | `VectorPotential`, `calc_B_from_vector_potential`, `calc_vector_potential_from_magnetization`, `gauge_transform`, `verify_coulomb_gauge` | 39-45 |

### maxwell.electrostatics — Part I (Arts. 27-229)

| Module | Public API | Articles |
|---|---|---|
| `dielectrics` | `DielectricMaterial` → `polarization`, `bound_charge`, `susceptibility` | 55-107 |
| `general_theorems` | `greens_theorem`, `greens_reciprocity`, `uniqueness_theorem`, `electrostatic_energy` | 18-24 |
| `electric_images` | `image_point_charge_plane`, `image_point_charge_sphere`, `image_line_charge_cylinder`, `inversion_method` | 40-73 |
| `equilibrium_surfaces` | `equilibrium_points`, `saddle_point`, `equipotential_surfaces`, `field_line_tracing` | 18-22 |
| `confocal_surfaces` | `EllipsoidalHarmonic`, `confocal_ellipsoid`, `ellipsoidal_coordinates` | 73-82 |
| `surface_density` | Surface charge density calculations | 79-85, 128-134 |
| `equipotential` | Equipotential surface computation | 103-111, 135-146 |
| `instruments` | `QuadrantElectrometer`, electrometer calibration | 207-229 |

### maxwell.electrokinematics — Part II (Arts. 230-370)

| Module | Public API | Articles |
|---|---|---|
| `network_solver` | `NetworkAnalyzer` → `kirchhoff_junction`, `kirchhoff_loop`, `solve_network`, `wheatstone_bridge` | 273-284 |
| `electrolysis` | `ElectrolysisCell`, `faraday_laws`, `nernst_equation`, `ion_migration` | 249-263 |
| `emf` | `EMFSource`, `contact_potential`, `seebeck_effect`, `peltier_effect`, `thomson_effect` | 264-272 |
| `conduction_3d` | `Conduction3DAnalyzer` — 3D current flow | 285-296 |
| `resistance_distribution` | `ResistanceDistributionAnalyzer` — resistance of spheres, cylinders, shells | 297-309 |
| `heterogeneous_media` | `HeterogeneousMediaAnalyzer` — effective conductivity, Maxwell-Garnett | 310-324 |
| `dielectric_conduction` | `DielectricConductor` — conduction in dielectrics | 325-334 |
| `resistance_measurement` | `ResistanceMeasurementAnalyzer` — Wheatstone, Kelvin bridge, four-terminal | 335-358 |
| `resistance_substances` | `ResistanceSubstancesAnalyzer` — material resistance, temperature coefficients | 359-370 |
| `emf_bodies` | `ContactEMFAnalyzer` — concentration cells, junction potentials | 246-248 |

### maxwell.electromagnetism — Part IV (Arts. 475-866)

#### Theory

| Module | Public API | Articles |
|---|---|---|
| `theory.general_equations` | `ElectromagneticField`, `MaxwellEquations`, `GeneralEquationsCalculator` — all 7 equations A-G | 594-603 |
| `theory.connected_systems` | `ConnectedSystem` — coupled EM systems | 553-567 |
| `theory.dynamical_model` | `DynamicalModel` — Lagrangian formulation | 568-577 |
| `theory.comparisons` | `ForceLawComparison` — compare force laws | 526, 527 |
| `theory.conservation` | `EnergyConservation` — energy conservation checks | 543, 544 |

#### Forces

| Module | Public API | Articles |
|---|---|---|
| `forces.lorentz` | `LorentzForce` → `force_vector`, `force_on_charge`, `force_between_parallel_currents` | 490-492 |
| `forces.stress_tensor` | `MaxwellStressTensor` → `tensor`, `analyze_stress`, `verify_stress_tensor` | 641-644 |
| `forces.elemental` | `CurrentElement` — elemental force between currents | 510-515 |
| `forces.ponderomotive` | `PonderomotiveForce` — force on medium | 602, 603 |
| `forces.sliding` | `SlidingConductor` — sliding conductor dynamics | 594-597 |
| `forces.generalized` | `GeneralizedForce` — generalized EM forces | 573-575 |
| `forces.coil_forces` | Coil force computations | 697-699 |
| `forces.medium_force` | `MediumForceCalculator` | 639, 640 |

#### Induction

| Module | Public API | Articles |
|---|---|---|
| `induction.faraday` | `FaradayInduction`, `MagneticFlux`, `InducedEMF` — Faraday's law, motional EMF | 528-531, 542 |
| `induction.self` | `SelfInductance` — self-inductance calculations | 546-551 |
| `induction.lenz` | `LenzLawCalculator` — Lenz's law direction | 542 |
| `induction.generalized` | `GeneralizedEMF` — generalized EMF | 576, 577 |

#### Energy

| Module | Public API | Articles |
|---|---|---|
| `energy.magnetic` | `calc_magnetic_energy_density`, `calc_total_magnetic_energy`, `MagneticEnergy` | 632, 633 |
| `energy.electrostatic` | `calc_electrostatic_energy_density`, `ElectrostaticEnergy` | 630, 631 |
| `energy.electrokinetic` | `ElectrokineticEnergy` — electrokinetic energy | 634-638 |

#### Fields

| Module | Public API | Articles |
|---|---|---|
| `fields.ampere_maxwell` | `AmpereMaxwellLaw`, `DisplacementCurrent`, `AmpereMaxwellCalculator` | 606, 607 |
| `fields.curl_relation` | `CurlRelations` — curl relations for EM fields | 590-592 |
| `fields.electrotonic` | `ElectrotonicState` — Faraday's electrotonic state | 540, 541 |
| `fields.vector_momentum` | `VectorPotential` — vector potential momentum | 585-592 |

#### Charges & Currents

| Module | Public API | Articles |
|---|---|---|
| `charges.surface` | `SurfaceCharge` — surface charge distributions | 613 |
| `charges.volume` | `VolumeCharge` — volume charge distributions | 612 |
| `currents.total` | `TotalCurrent` — total current density | 610 |
| `currents.emf_relation` | `EMFCurrentRelation` — EMF-current relationship | 611 |

#### Current Sheets

| Module | Public API | Articles |
|---|---|---|
| `current_sheets.sheet_theory` | `CurrentSheet`, `MagneticShell`, `CurrentSheetCalculator` | 647-655 |
| `current_sheets.surface_currents` | `SurfaceCurrentDensity`, `SurfaceCurrentAnalyzer` | 656-662 |
| `current_sheets.boundary_conditions` | `ElectromagneticBoundary`, `BoundaryConditionAnalyzer` | 663-674 |

#### Components

| Module | Public API | Articles |
|---|---|---|
| `components.solenoids` | `Solenoid` — solenoid field and inductance | 675-683 |
| `components.circular_coils` | `CircularCoil`, `calc_coil_on_axis`, `calc_coil_off_axis` | 670-679 |
| `components.cylinders` | `CylindricalConductor` — cylindrical conductor fields | 680-687 |

#### Waves

| Module | Public API | Articles |
|---|---|---|
| `waves.wave_equation` | `ElectromagneticWave`, `WaveEquationSolver` | 781-785 |
| `waves.plane_wave` | `PlaneWave`, `PlaneWaveAnalyzer` | 786-790 |
| `waves.polarization` | `PolarizationState`, `PolarizationAnalyzer` | 791-795 |

#### Potentials

| Module | Public API | Articles |
|---|---|---|
| `potentials.directrix` | `DirectrixFunction` — directrix of electromagnetic action | 517-519 |
| `potentials.multivalued` | `CyclicPotential` — multivalued potentials | 480 |
| `potentials.mutual_energy` | `MutualEnergy` — mutual energy of circuits | 520, 521 |
| `potentials.surfaces` | `EquipotentialSurface`, `CurrentLoopPotential` | 486, 487 |

#### Sources

| Module | Public API | Articles |
|---|---|---|
| `sources.oersted` | `OerstedField` — Oersted's magnetic field from current | 475-479 |

#### Equivalence

| Module | Public API | Articles |
|---|---|---|
| `equivalence` | `MagneticShell`, `CurrentCircuit`, `CircuitEquivalence` — circuit-shell equivalence | 482-485 |

#### Dynamics & Applications

| Module | Public API | Articles |
|---|---|---|
| `dynamics.attraction` | `ParallelConductorForce` — force between parallel conductors | 496, 497 |
| `optimization.coil_design` | `calc_optimal_coil_radius`, `calc_uniformity_fom`, `verify_coil_design` | 706 |
| `vis.circular_fields` | `FieldLineData` — field line computation for visualization | 702 |

#### Experiments

| Module | Public API | Articles |
|---|---|---|
| `experiments.felici` | `InductionEvent`, `FeliciResult` — Felici's induction experiments | 536-539 |
| `experiments.ampere_balance` | `BalanceReading` — Ampere balance experiments | 579-584 |
| `experiments.stress_verification` | Stress tensor experimental verification | 645, 646 |

### maxwell.math — Mathematics

| Module | Public API | Articles |
|---|---|---|
| `spherical_harmonics` | `SphericalHarmonicExpansion`, `LegendrePolynomial`, `SphericalHarmonic`, `calc_legendre_polynomial`, `addition_theorem`, `multipole_expansion` | 128-146, 675-695 |
| `elliptic_integrals` | `EllipticIntegral`, `calc_complete_elliptic_integral_first_kind`, `calc_complete_elliptic_integral_second_kind`, `calc_incomplete_elliptic_integral` | 696-705 |
| `vector_operators` | `gradient`, `divergence`, `curl`, `laplacian`, `vector_laplacian`, vector identities | 71-77, 100-110 |
| `conjugate_functions` | `ConjugatePair`, conjugate harmonic functions | 182-206 |
| `potential_theorems` | Surface integrals, Gauss law, potential mean value | 11-26 |

Subpackages:

| Module | Public API | Articles |
|---|---|---|
| `algebra.quaternions` | `Quaternion` — quaternion algebra | 522 |
| `gauge.manager` | `GaugeTransformation`, `coulomb_gauge`, `lorenz_gauge` | 616, 617 |
| `geometry.gmd` | `GMDCalculator` — geometric mean distance | 691-693 |

### maxwell.materials — Materials

| Module | Public API | Articles |
|---|---|---|
| `hysteresis` | `HysteresisLoop`, `WeberModelWithHysteresis`, `simulate_cycle`, `retentivity`, `coercive_force`, `typical_hysteresis_parameters` | 444-446 |
| `induction` | `MagneticSusceptibility`, `InducedMagnetization` | 424-426 |
| `saturation` | `WeberModel` — magnetic saturation model | 442, 443 |

Subpackage `constitutive/`:

| Module | Public API | Articles |
|---|---|---|
| `conductivity` | `Conductivity` → `current_density`, `joule_heating` | 609 |
| `displacement` | `ElectricDisplacement` → `displacement_field`, `bound_charge_density` | 608 |
| `magnetization` | `Magnetization` → `magnetic_induction`, `magnetization_current` | 605 |
| `permeability` | `Permeability` → `permeability_from_susceptibility` | 614 |

### maxwell.magnetism — Part III (Arts. 371-474)

| Module | Public API | Articles |
|---|---|---|
| `terrestrial_magnetism` | `GeomagneticElements` → `earth_field_components`, `magnetic_survey`, `gauss_spherical_analysis`, `gauss_coefficients` | 465-474 |
| `magnetic_measurements` | `DeflectionMagnetometer`, `UnifilarSuspension`, `BifilarSuspension`, `KewMagnetometer`, `DipCircle`, `BalanceMagnetometer`, `MagneticSurvey` | 449-464 |

### maxwell.instruments — Instruments

| Module | Public API | Articles |
|---|---|---|
| `galvanometers` | `TangentGalvanometer`, `SineGalvanometer`, `StandardGalvanometer`, `FourCoilGalvanometer`, `ThreeCoilGalvanometer`, `UniformWireGalvanometer` | 707-720 |
| `helmholtz` | `HelmholtzCoil` → `field_at`, `uniformity_region` | 713 |
| `dynamometers` | `WeberDynamometer`, `JouleCurrentWeigher`, `TorsionDynamometer` | 725-729 |
| `suspended_coil` | `SuspendedCoil`, `ThomsonSensitiveCoil`, `ThomsonCombinedInstrument` | 721-728 |
| `optimization.sensitivity` | Galvanometer sensitivity optimization | 716-719 |

### maxwell.optics — Electromagnetic Theory of Light

| Module | Public API | Articles |
|---|---|---|
| `wave_equation` | `ElectromagneticWave`, `PlaneWave`, `WaveEquationCalculator` | 781-790 |
| `plane_waves` | `PlaneWave`, `PolarizationState` — plane wave solutions | 790-793, 801-803 |
| `velocity` | `WaveVelocity` — wave speed in media | 786, 787 |
| `crystals` | `CrystalOptics` — optics in crystals | 794, 804, 805 |
| `metals` | `MetallicReflection`, `MetalOptics` — optics in metals | 795-800 |
| `radiation_pressure` | `RadiationPressure` — light pressure | 791-794 |
| `diffusion` | `LightDiffusion`, `FieldDiffusion` — light diffusion | 801-808 |
| `constants` | `OpticalConstants` — optical constants | 788-790 |

### maxwell.molecular — Molecular Theories

| Module | Public API | Articles |
|---|---|---|
| `competing_theories` | `CompetingTheory`, `TheoryComparison`, `compare_theories` | 841-866 |
| `amperes_theory` | `AmperesTheory`, `MolecularCurrent` — Ampere's molecular currents | 832-840 |
| `webers_theory` | `WebersTheory`, `WeberForce` — Weber's magnetic molecules | 841-850 |
| `neumanns_theory` | `NeumannTheory`, `NeumannPotential` — Neumann's induction | 851-858 |

### maxwell.fields — Field Theory

| Module | Public API | Articles |
|---|---|---|
| `constitutive` | `MagneticConstitutiveRelation` — B-H constitutive relations | 400 |
| `decomposition` | `LamellarDistribution`, `ComplexLamellarDistribution` — Helmholtz decomposition | 412-416 |
| `force` | `MagneticForce` — magnetic force from potential | 395-398 |
| `induction` | `MagneticInduction` — magnetic induction B field | 399 |
| `solenoidal` | `MagneticInductionTube` — solenoidal field verification | 403, 404 |

### maxwell.circuits — Circuit Dynamics

| Module | Public API | Articles |
|---|---|---|
| `dynamics` | `Circuit`, `CoupledCircuits`, `calc_self_inductance`, `calc_mutual_inductance`, `calc_coupling_coefficient` | 578-584 |

### maxwell.components — Geometric Components

| Module | Public API | Articles |
|---|---|---|
| `spheres` | `MagneticSphere`, `HollowMagneticSphere`, `sphere_field`, `sphere_demagnetizing_field` | 431-436 |
| `ellipsoids` | `MagneticEllipsoid`, `ProlateSpheroid`, `OblateSpheroid`, `ellipsoid_field` | 437, 438 |

### maxwell.engineering — Naval Engineering

| Module | Public API | Articles |
|---|---|---|
| `naval` | `ShipMagnetism`, `MagneticCompass`, `flinders_bar_correction`, `quadrantal_correctors`, `simulate_compass_swinging` | 441, 760-790 |

### maxwell.magneto_optics — Magneto-Optic Effects

| Module | Public API | Articles |
|---|---|---|
| `rotation` | `FaradayRotator`, `VerdetTable` — Faraday rotation | 807-810 |
| `circular_polarization` | `CircularlyPolarizedRay` — circular polarization in magnetic fields | 811-817 |
| `energy_analysis` | `MagnetoOpticMedium` — magneto-optic energy | 818-821 |

### maxwell.signal_processing — Telegraph Theory

| Module | Public API | Articles |
|---|---|---|
| `telegraphy` | `TelegraphLine`, `SignalTransmission`, `signal_velocity`, `propagation_delay` | 730-735, 740, 745, 750 |

### maxwell.geometry — Geometric Structures

| Module | Public API | Articles |
|---|---|---|
| `shells` | `MagneticShell` — magnetic shell potential | 409-411 |
| `solenoids` | `Solenoid`, `ComplexSolenoid` — solenoid geometry | 407, 408, 414 |

### maxwell.mechanics — Mechanical Energy

| Module | Public API | Articles |
|---|---|---|
| `potential_energy` | `MagneticPotentialEnergy`, `ShellEnergy` | 87-95, 389 |
| `shell_energy` | `ShellEnergy` — energy of magnetic shells | 423 |

### maxwell.vortex_engine — Molecular Vortex Theory

| Module | Public API | Articles |
|---|---|---|
| `vortex_lattice` | `MolecularVortex`, `VortexLattice` | 822, 831 |
| `equations_of_motion` | `VortexEquations` — vortex dynamics | 827, 828 |
| `kinetic_energy` | Vortex kinetic energy computations | 824-826 |
| `helmholtz_law` | Helmholtz vortex law | 823 |
| `magnetic_rotation` | Magnetic rotation in vortex model | 829, 830 |

### maxwell.calibration — Calibration

| Module | Public API | Articles |
|---|---|---|
| `absolute_resistance` | `AbsoluteResistance`, `StandardResistanceCoil` — absolute resistance calibration | 758-767 |

### maxwell.experiments — Experimental Verification

| Module | Public API | Articles |
|---|---|---|
| `ratio_v.theory` | `UnitRatioExperiment` — v/c ratio experiments | 768-770, 780 |
| `ratio_v.combined` | Combined ratio experiments | 773, 775-779 |
| `ratio_v.condensers` | `CondenserMeasurement` — condenser-based ratio | 771, 772, 774 |

### maxwell.io — I/O Utilities

| Module | Public API |
|---|---|
| `json_loader` | `load_article_json`, `load_chapter_json`, `list_available_articles`, `batch_load_articles` |
| `article_parser` | `extract_article_number`, `extract_all_articles_from_chapter`, `extract_equations`, `extract_cross_references` |

### maxwell.meta — Citation System

| Module | Public API | Articles |
|---|---|---|
| `citation` | `MaxwellCitation`, `get_citation(article)`, `get_all_citations()`, `@maxwell_cite` decorator | 241 |

### maxwell.solvers — Problem Solvers

| Module | Public API | Articles |
|---|---|---|
| `induction_solvers` | `InductionProblem`, `InductionSolution` | 427-429 |
| `shape_solvers` | `CylindricalMagnet`, `RectangularMagnet` | 439, 440 |

### maxwell.vis — Visualization

| Module | Public API | Articles |
|---|---|---|
| `_compat` | `HAS_MATPLOTLIB` — graceful matplotlib availability check | — |
| `_base` | `create_meshgrid`, `evaluate_on_grid` — shared grid utilities | — |
| `field_lines` | `plot_field_lines_2d` — electric and magnetic field line plotting | 702 |
| `equipotential` | `plot_equipotentials_2d` — equipotential contour plotting | 103-111 |
| `stress` | `plot_stress_tensor_2d` — Maxwell stress tensor visualization | 641-644 |

### maxwell.physics — Legacy Physics

| Module | Public API | Articles |
|---|---|---|
| `coulomb` | `ElectrostaticForce` — Coulomb's law | 30, 38-40, 43, 44, 66-68, 84 |
| `gauss` | `SurfaceIntegral` — Gauss's law | 75, 76, 82 |
| `ohm` | Ohm's law implementations | 241, 277, 279 |
| `conduction` | `ConductivityTensor` | 230, 241, 274-279 |
| `current` | `ElectricCurrent` | 64, 150, 152, 177 |
| `potentials` | `MagneticPotential` | 385, 386 |
| `coupling` | `DipoleInteraction` | 387, 388 |
| `molecular_theory` | `MagneticMolecule`, `MolecularEnsemble` | 430 |
| `magnetostriction` | `MagnetostrictionTensor`, `MagnetostrictiveMaterial` | 447, 448 |

### maxwell.verification — Verification Framework

| Module | Public API |
|---|---|
| `verifier` | `VerificationResult`, `EquationVerifier` |
| `equation_registry` | `VerificationEntry`, `EquationRegistry` |
| `equation_extractor` | `ExtractedEquation`, `EquationExtractor` |

### maxwell.theories — Historical Theory Analysis

| Module | Public API | Articles |
|---|---|---|
| `failure_modes` | `TheoryResult` — theory failure mode analysis | 857-859 |

### maxwell.philosophy — Philosophical Checks

| Module | Public API | Articles |
|---|---|---|
| `medium_check` | `MediumProperties`, `WaveProperties` — medium property verification | 865, 866 |

### maxwell.jax — JAX GPU/TPU Acceleration

> GPU/TPU-accelerated, auto-differentiable implementations. All adapters preserve CGS-EMU units and citation traceability.
> Install with `pip install maxwell[accel]`. See `maxwell/jax/README.md` for full documentation.

#### Core Adapters

| Module | Public API | Articles |
|---|---|---|
| `core.charge` | `PointChargeJAX` — `field_at()`, `potential_at()`, `field_at_batched()` | 29-30 |
| `core.magnet` | `MagneticPoleJAX`, `MagnetJAX` — `field_at()`, `force_in_field()`, `torque_in_uniform_field()`, `mutual_action_jax()` | 371-376, 392 |

#### Electromagnetism Adapters

| Module | Public API | Articles |
|---|---|---|
| `electromagnetism.induction` | `FaradayInductionJAX` — `induced_emf()`, `magnetic_flux()`, `analyze_faraday_induction_jax()` | 528-531, 542 |
| `electromagnetism.equations` | `MaxwellEquationsJAX` — `gauss_law_electric()`, `gauss_law_magnetic()`, `equation_A_faraday()`, `verify_maxwell_equations_jax()` | 594-603 |
| `electromagnetism.forces` | `LorentzForceJAX`, `MaxwellStressTensorJAX` — `force_vector`, `stress_tensor()`, `force_on_charge_jax()`, `stress_tensor_jax()` | 490-492, 641-646 |
| `electromagnetism.ampere_maxwell` | `DisplacementCurrentJAX`, `AmpereMaxwellLawJAX` | 606-607 |
| `electromagnetism.field` | `ElectricFieldJAX` — `from_point_charge()`, `superposition()`, `electric_flux_jax()`, `gauss_law_closed_surface_jax()`, `field_from_potential_jax()` | 44-49, 68-76 |
| `electromagnetism.energy` | `ElectrostaticEnergyJAX`, `CapacitorEnergyJAX` — `energy_density`, `from_voltage()`, `from_charge()`, `calc_electrostatic_energy_density_jax()`, `calc_capacitor_energy_jax()` | 630-631 |
| `electromagnetism.electrokinetic` | `ElectrokineticEnergyJAX`, `CoupledCircuitEnergyJAX` — `from_single_circuit()`, `from_currents()`, `calc_two_circuit_energy_jax()`, `calc_coupling_coefficient_jax()` | 634-638 |
| `electromagnetism.ohms_law` | `OhmsLawJAX`, `ResistanceJAX`, `ConductivityJAX`, `PowerDissipationJAX` — `from_current_and_resistance()`, `series()`, `parallel()`, `calc_ohms_law_jax()` | 230-234, 273-288 |
| `electromagnetism.network_solver` | `NetworkSolverJAX`, `KirchhoffJAX`, `WheatstoneBridgeJAX`, `ReciprocityVerifierJAX` — `from_edges()`, `node_potentials`, `is_balanced()`, `verify()` | 273-284, 277-278 |
| `electromagnetism.conduction_3d` | `Conduction3DJAX`, `SpreadingResistanceJAX`, `EffectiveConductivityJAX` — `current_density()`, `spherical_surface()`, `maxwell_garnett()` | 285-288, 297-324 |
| `electromagnetism.electrolysis` | `FaradayLawsJAX`, `IonTransportJAX`, `PolarizationJAX`, `ElectrolysisCellJAX` — `mass_from_charge()`, `migration_velocity()`, `activation_overpotential()`, `mass_deposited()` | 249-263 |
| `electromagnetism.joule_heating` | `JouleHeatingJAX`, `HeatDissipationJAX`, `SubstanceResistanceJAX` — `power()`, `temperature_rise()`, `at_temperature()` | 351-370 |

#### Math Adapters

| Module | Public API | Articles |
|---|---|---|
| `math.spherical_harmonics` | `SphericalHarmonicExpansionJAX` — `compute_coefficients()`, `reconstruct()`, `legendre_batched()`, `addition_theorem_jax()` | 128-146 |

#### Infrastructure

| Module | Public API | Description |
|---|---|---|
| `_compat` | `jax_tree` decorator, `safe_div()`, `safe_sqrt()`, `safe_norm()` | Pytree registration, safe arithmetic |
| `_scipy_special` | `lpmv_jax()`, `legendre_jax()`, `sph_harm_y_jax()` | Pure JAX special function wrappers |
| `_elliptic` | `ellipk_jax()`, `ellipe_jax()` | AGM-based elliptic integrals (no scipy) |

---

## Citation System

Every function and class is annotated with `@maxwell_cite(article_number, part=..., chapter=...)` linking the implementation to Maxwell's original articles:

```python
from maxwell.meta.citation import get_citation

# Get citation for a specific article
info = get_citation(598)
print(info)  # Part IV, Art. 598: Faraday's Law of Induction

# List all citations
all_citations = get_all_citations()
```

## Unit System

All computations use **CGS (Gaussian) units** as Maxwell's original Treatise:

| Quantity | CGS Unit | SI Equivalent |
|---|---|---|
| Electric field E | statvolt/cm | 3e4 V/m |
| Magnetic field B | gauss | 1e-4 tesla |
| Charge | statcoulomb (ESU) / abcoulomb (EMU) | 3.336e-10 C / 10 C |
| Current | statampere (ESU) / abampere (EMU) | 3.336e-10 A / 10 A |
| Potential | statvolt | 300 V |
| Force | dyne | 1e-5 N |
| Energy | erg | 1e-7 J |

Conversion utilities available via `CGSUnitConverter` and `maxwell.core.units.dimensions`.
