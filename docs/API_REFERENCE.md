# Maxwell Modernized - API Reference Index

**Generated:** 2026-04-12  
**Codebase Coverage:** 866/866 articles (100%)  
**Total Modules:** 165 Python modules  
**Total Functions:** 1,174  
**Total Classes:** 244  
**Test Coverage:** 522/522 tests passing

---

## Table of Contents

1. [Core Physics](#core-physics)
2. [Part I - Electrostatics](#part-i---electrostatics)
3. [Part II - Electrokinematics](#part-ii---electrokinematics)
4. [Part III - Magnetism](#part-iii---magnetism)
5. [Part IV - Electromagnetism](#part-iv---electromagnetism)
6. [Mathematics](#mathematics)
7. [Field Theory](#field-theory)
8. [Materials & Constitutive Relations](#materials--constitutive-relations)
9. [Molecular Theory](#molecular-theory)
10. [Optics & Waves](#optics--waves)
11. [Instruments & Measurements](#instruments--measurements)
12. [Experiments & Calibration](#experiments--calibration)
13. [Supporting Packages](#supporting-packages)

---

## Core Physics

**Location:** `maxwell/core/`  
**Purpose:** Fundamental physics abstractions - charge, field, magnet, matter, moment, potential

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `charge.py` | 2 | 1 | 4 | 29, 30, 45, 245 |
| `field.py` | 5 | 3 | 9 | 44, 46-49, 68, 69, 71, 76 |
| `magnet.py` | 4 | 4 | 7 | 371-376, 392 |
| `matter.py` | 4 | 2 | 4 | 377-380 |
| `moment.py` | 1 | 6 | 6 | 381-384, 389, 390 |
| `potential.py` | 10 | 1 | 7 | 45, 70, 72, 73, 77, 78, 85 |

### Subpackages

#### `maxwell/core/units/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `dimensions.py` | 8 | 4 | 10 | 620-628, 771-773, 781 |
| `units.py` | 0 | 2 | 0 | N/A |
| `__init__.py` exports | 17 | 3 | 12 | Various |

**Key APIs:**
- `Charge` - Electric charge representation and operations
- `Field` - Electric and magnetic field abstractions
- `Magnet` - Magnetic body modeling
- `Potential` - Scalar and vector potential calculations
- `DimensionalAnalysis` - Unit consistency verification

---

## Part I - Electrostatics

**Location:** `maxwell/electrostatics/`  
**Purpose:** Static electric fields, potentials, and charge distributions

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `confocal_surfaces.py` | 7 | 1 | 10 | 147-156 |
| `dielectrics.py` | 14 | 1 | 14 | 157-170 |
| `electric_images.py` | 7 | 0 | 11 | 171-181 |
| `equilibrium_surfaces.py` | 12 | 0 | 16 | 112-127 |
| `general_theorems.py` | 14 | 0 | 17 | 86-102 |
| `instruments.py` | 9 | 1 | 23 | 207-229 |
| `equipotential.py` | 15 | 4 | 18 | 103-111, 135-146 |
| `surface_density.py` | 17 | 4 | 20 | 79-85, 128-134 |

**Total:** 95 functions, 11 classes, 126 articles covered

**Key APIs:**
- `ConfocalSurfaces` - Equipotential surface calculations
- `DielectricMedia` - Dielectric constant and polarization
- `ElectricImages` - Method of images for conductors
- `EquilibriumConfigurations` - Charge distribution on conductors
- `GeneralTheorems` - Gauss's law, uniqueness theorems

---

## Part II - Electrokinematics

**Location:** `maxwell/electrokinematics/`  
**Purpose:** Electric currents, conduction, resistance, and EMF

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `conduction_3d.py` | 11 | 1 | 12 | 285-296 |
| `dielectric_conduction.py` | 8 | 1 | 10 | 325-334 |
| `electrolysis.py` | 16 | 2 | 15 | 249-263 |
| `emf.py` | 15 | 1 | 9 | 264-272 |
| `emf_bodies.py` | 6 | 1 | 3 | 246-248 |
| `heterogeneous_media.py` | 8 | 1 | 15 | 310-324 |
| `network_solver.py` | 8 | 1 | 12 | 273-284 |
| `resistance_distribution.py` | 11 | 1 | 13 | 297-309 |
| `resistance_measurement.py` | 8 | 2 | 24 | 335-358 |
| `resistance_substances.py` | 11 | 2 | 12 | 359-370 |

**Total:** 102 functions, 13 classes, 125 articles covered

**Key APIs:**
- `Conduction3D` - Three-dimensional current flow
- `Electrolysis` - Chemical effects of currents
- `EMF` - Electromotive force calculations
- `NetworkSolver` - Circuit analysis (Kirchhoff's laws)
- `ResistanceMeasurement` - Resistance measurement techniques

---

## Part III - Magnetism

**Location:** `maxwell/magnetism/`  
**Purpose:** Magnetic measurements and terrestrial magnetism

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `magnetic_measurements.py` | 8 | 7 | 16 | 449-464 |
| `terrestrial_magnetism.py` | 13 | 1 | 10 | 465-474 |

**Total:** 21 functions, 8 classes, 26 articles covered

**Key APIs:**
- `MagneticMeasurements` - Magnetic moment and field measurements
- `TerrestrialMagnetism` - Earth's magnetic field modeling

---

## Part IV - Electromagnetism

**Location:** `maxwell/electromagnetism/`  
**Purpose:** Unified electromagnetic theory - the crown jewel of Maxwell's work

### Core Theory

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `equivalence.py` | 5 | 3 | 4 | 482-485 |

### Charges & Currents

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `charges/surface.py` | 12 | 1 | 1 | 613 |
| `charges/volume.py` | 9 | 1 | 1 | 612 |
| `currents/emf_relation.py` | 12 | 2 | 1 | 611 |
| `currents/total.py` | 9 | 1 | 1 | 610 |

### Current Sheets

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `current_sheets/boundary_conditions.py` | 7 | 2 | 12 | 663-674 |
| `current_sheets/sheet_theory.py` | 6 | 3 | 9 | 647-655 |
| `current_sheets/surface_currents.py` | 5 | 2 | 7 | 656-662 |

### Fields

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `fields/ampere_maxwell.py` | 7 | 3 | 2 | 606, 607 |
| `fields/curl_relation.py` | 10 | 1 | 3 | 590-592 |
| `fields/electrotonic.py` | 9 | 1 | 2 | 540, 541 |
| `fields/vector_momentum.py` | 8 | 1 | 8 | 585-592 |

### Forces

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `forces/coil_forces.py` | 7 | 0 | 3 | 697-699 |
| `forces/elemental.py` | 6 | 1 | 6 | 510-515 |
| `forces/generalized.py` | 8 | 1 | 3 | 573-575 |
| `forces/lorentz.py` | 8 | 2 | 3 | 490-492 |
| `forces/medium_force.py` | 8 | 1 | 2 | 639, 640 |
| `forces/ponderomotive.py` | 9 | 1 | 2 | 602, 603 |
| `forces/sliding.py` | 7 | 1 | 4 | 594-597 |
| `forces/stress_tensor.py` | 12 | 1 | 4 | 641-644 |

### Induction

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `induction/faraday.py` | 9 | 3 | 5 | 528-531, 542 |
| `induction/generalized.py` | 6 | 1 | 2 | 576, 577 |
| `induction/lenz.py` | 6 | 1 | 1 | 542 |
| `induction/self.py` | 8 | 1 | 6 | 546-551 |

### Energy

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `energy/electrokinetic.py` | 9 | 1 | 5 | 634-638 |
| `energy/electrostatic.py` | 8 | 1 | 2 | 630, 631 |
| `energy/magnetic.py` | 9 | 1 | 2 | 632, 633 |

### Potentials

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `potentials/directrix.py` | 6 | 1 | 3 | 517-519 |
| `potentials/multivalued.py` | 6 | 1 | 1 | 480 |
| `potentials/mutual_energy.py` | 8 | 1 | 2 | 520, 521 |
| `potentials/surfaces.py` | 6 | 2 | 2 | 486, 487 |

### Sources

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `sources/oersted.py` | 7 | 1 | 5 | 475-479 |

### Components

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `components/circular_coils.py` | 9 | 1 | 10 | 670-679 |
| `components/cylinders.py` | 6 | 1 | 8 | 680-687 |
| `components/solenoids.py` | 6 | 1 | 9 | 675-683 |

### Theory & Dynamics

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `theory/comparisons.py` | 10 | 1 | 2 | 526, 527 |
| `theory/connected_systems.py` | 8 | 1 | 15 | 553-567 |
| `theory/conservation.py` | 7 | 1 | 2 | 543, 544 |
| `theory/dynamical_model.py` | 5 | 1 | 10 | 568-577 |
| `theory/general_equations.py` | 13 | 3 | 10 | 594-603 |

### Waves

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `waves/plane_wave.py` | 3 | 2 | 5 | 786-790 |
| `waves/polarization.py` | 7 | 2 | 5 | 791-795 |
| `waves/wave_equation.py` | 5 | 2 | 5 | 781-785 |

### Experiments & Verification

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `experiments/ampere_balance.py` | 6 | 1 | 6 | 579-584 |
| `experiments/felici.py` | 7 | 2 | 4 | 536-539 |
| `experiments/stress_verification.py` | 6 | 0 | 2 | 645, 646 |

### Dynamics & Applications

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `dynamics/attraction.py` | 8 | 1 | 2 | 496, 497 |
| `physics/stress.py` | 6 | 1 | 1 | 501 |
| `vis/circular_fields.py` | 7 | 1 | 1 | 702 |
| `optimization/coil_design.py` | 6 | 0 | 1 | 706 |

**Part IV Total:** 418 functions, 71 classes, 269 articles covered

**Key APIs:**
- `AmpereMaxwell` - The Ampere-Maxwell law implementation
- `LorentzForce` - Force on charged particles
- `FaradayInduction` - Electromagnetic induction
- `StressTensor` - Maxwell stress tensor
- `WaveEquation` - Electromagnetic wave propagation
- `ConnectedSystems` - Coupled electromagnetic systems

---

## Mathematics

**Location:** `maxwell/math/`  
**Purpose:** Mathematical tools - spherical harmonics, elliptic integrals, vector calculus

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `conjugate_functions.py` | 15 | 1 | 25 | 182-206 |
| `elliptic_integrals.py` | 7 | 1 | 10 | 696-705 |
| `spherical_harmonics.py` | 13 | 6 | 34 | 128-146, 675-695 |
| `vector_operators.py` | 8 | 0 | 16 | 71-77, 100-110 |

### Subpackages

#### `maxwell/math/algebra/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `quaternions.py` | 7 | 1 | 1 | 522 |

#### `maxwell/math/gauge/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `manager.py` | 8 | 1 | 2 | 616, 617 |

#### `maxwell/math/geometry/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `gmd.py` | 8 | 1 | 3 | 691-693 |

**Total:** 68 functions, 7 classes, 109 articles covered

**Key APIs:**
- `SphericalHarmonics` - Surface harmonic expansions
- `EllipticIntegrals` - Complete and incomplete elliptic integrals
- `VectorOperators` - Gradient, divergence, curl
- `ConjugateFunctions` - Complex variable methods

---

## Field Theory

**Location:** `maxwell/fields/`  
**Purpose:** General field theory and constitutive relations

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `constitutive.py` | 8 | 2 | 1 | 400 |
| `decomposition.py` | 5 | 2 | 4 | 412, 413, 415, 416 |
| `force.py` | 6 | 1 | 4 | 395-398 |
| `induction.py` | 4 | 1 | 1 | 399 |
| `solenoidal.py` | 5 | 1 | 2 | 403, 404 |

**Total:** 28 functions, 7 classes, 12 articles covered

---

## Materials & Constitutive Relations

**Location:** `maxwell/materials/`  
**Purpose:** Material properties and constitutive equations

### Core Materials

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `hysteresis.py` | 5 | 2 | 3 | 444-446 |
| `induction.py` | 5 | 3 | 3 | 424-426 |
| `saturation.py` | 4 | 1 | 2 | 442, 443 |

### Constitutive Relations

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `constitutive/conductivity.py` | 10 | 1 | 1 | 609 |
| `constitutive/displacement.py` | 11 | 2 | 1 | 608 |
| `constitutive/magnetization.py` | 7 | 1 | 1 | 605 |
| `constitutive/permeability.py` | 11 | 1 | 1 | 614 |

**Total:** 50 functions, 10 classes, 12 articles covered

---

## Molecular Theory

**Location:** `maxwell/molecular/`  
**Purpose:** Molecular theories of magnetism and dielectrics

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `amperes_theory.py` | 4 | 2 | 9 | 832-840 |
| `competing_theories.py` | 10 | 2 | 26 | 841-866 |
| `neumanns_theory.py` | 7 | 2 | 8 | 851-858 |
| `webers_theory.py` | 6 | 2 | 10 | 841-850 |

**Total:** 27 functions, 8 classes, 53 articles covered

**Key APIs:**
- `AmperesTheory` - Ampere's molecular currents
- `WebersTheory` - Weber's magnetic molecules
- `NeumannsTheory` - Neumann's induction theory
- `CompetingTheories` - Historical theory comparisons

---

## Optics & Waves

**Location:** `maxwell/optics/`  
**Purpose:** Electromagnetic theory of light

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `constants.py` | 11 | 1 | 3 | 788-790 |
| `crystals.py` | 8 | 1 | 3 | 794, 804, 805 |
| `diffusion.py` | 12 | 2 | 7 | 801-808 |
| `metals.py` | 11 | 2 | 6 | 795-800 |
| `plane_waves.py` | 10 | 2 | 6 | 790-793, 801-803 |
| `radiation_pressure.py` | 10 | 1 | 4 | 791-794 |
| `velocity.py` | 8 | 1 | 2 | 786, 787 |
| `wave_equation.py` | 11 | 3 | 10 | 781-790 |

**Total:** 81 functions, 13 classes, 41 articles covered

**Key APIs:**
- `WaveEquation` - Electromagnetic wave equation
- `PlaneWaves` - Plane wave solutions
- `Polarization` - Wave polarization states
- `RadiationPressure` - Light pressure calculations

---

## Instruments & Measurements

**Location:** `maxwell/instruments/`  
**Purpose:** Galvanometers, dynamometers, and measurement apparatus

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `dynamometers.py` | 2 | 3 | 4 | 725-727, 729 |
| `galvanometers.py` | 6 | 7 | 10 | 707-712, 714, 715, 717, 720 |
| `helmholtz.py` | 0 | 1 | 1 | 713 |
| `suspended_coil.py` | 2 | 3 | 5 | 721-724, 728 |

### Subpackages

#### `maxwell/instruments/optimization/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `sensitivity.py` | 3 | 0 | 3 | 716, 718, 719 |

**Total:** 13 functions, 14 classes, 23 articles covered

---

## Experiments & Calibration

**Location:** `maxwell/experiments/`, `maxwell/calibration/`  
**Purpose:** Experimental verifications and absolute measurements

### Calibration

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `absolute_resistance.py` | 7 | 2 | 10 | 758-767 |

### Experiments (v/c ratio)

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `ratio_v/combined.py` | 6 | 0 | 6 | 773, 775-779 |
| `ratio_v/condensers.py` | 3 | 1 | 3 | 771, 772, 774 |
| `ratio_v/theory.py` | 4 | 1 | 4 | 768-770, 780 |

**Total:** 20 functions, 4 classes, 23 articles covered

---

## Supporting Packages

### Calculus

**Location:** `maxwell/calculus/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `cyclic.py` | 7 | 1 | 6 | 417-422 |
| `integrals.py` | 5 | 2 | 2 | 401, 402 |
| `vector_potential.py` | 6 | 1 | 2 | 405, 406 |

### Circuits

**Location:** `maxwell/circuits/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `dynamics.py` | 10 | 2 | 7 | 578-584 |

### Components

**Location:** `maxwell/components/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `ellipsoids.py` | 5 | 3 | 2 | 437, 438 |
| `spheres.py` | 6 | 2 | 6 | 431-436 |

### Geometry

**Location:** `maxwell/geometry/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `shells.py` | 5 | 1 | 3 | 409-411 |
| `solenoids.py` | 1 | 2 | 3 | 407, 408, 414 |

### Magneto-Optics

**Location:** `maxwell/magneto_optics/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `circular_polarization.py` | 6 | 1 | 7 | 811-817 |
| `energy_analysis.py` | 2 | 1 | 4 | 818-821 |
| `rotation.py` | 3 | 2 | 4 | 807-810 |

### Signal Processing

**Location:** `maxwell/signal_processing/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `telegraphy.py` | 6 | 2 | 9 | 730-735, 740, 745, 750 |

### Solvers

**Location:** `maxwell/solvers/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `induction_solvers.py` | 8 | 2 | 3 | 427-429 |
| `shape_solvers.py` | 4 | 2 | 2 | 439, 440 |

### Vortex Engine

**Location:** `maxwell/vortex_engine/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `equations_of_motion.py` | 1 | 1 | 2 | 827, 828 |
| `helmholtz_law.py` | 2 | 0 | 1 | 823 |
| `kinetic_energy.py` | 3 | 0 | 3 | 824-826 |
| `magnetic_rotation.py` | 2 | 0 | 2 | 829, 830 |
| `vortex_lattice.py` | 1 | 2 | 2 | 822, 831 |

### Configuration

**Location:** `maxwell/config/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `constants.py` | 1 | 1 | 0 | N/A |
| `conventions.py` | 5 | 3 | 2 | 393, 394 |

### I/O

**Location:** `maxwell/io/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `article_parser.py` | 5 | 0 | 1 | 1 |
| `json_loader.py` | 6 | 0 | 1 | 1 |

### Meta

**Location:** `maxwell/meta/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `citation.py` | 4 | 1 | 1 | 241 |

### Physics (Legacy)

**Location:** `maxwell/physics/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `conduction.py` | 10 | 1 | 7 | 230, 241, 274-279 |
| `coulomb.py` | 11 | 1 | 10 | 30, 38-40, 43, 44, 66-68, 84 |
| `coupling.py` | 8 | 1 | 2 | 387, 388 |
| `current.py` | 8 | 1 | 4 | 64, 150, 152, 177 |
| `gauss.py` | 11 | 1 | 3 | 75, 76, 82 |
| `magnetostriction.py` | 5 | 2 | 2 | 447, 448 |
| `molecular_theory.py` | 4 | 2 | 1 | 430 |
| `ohm.py` | 5 | 0 | 3 | 241, 277, 279 |
| `potentials.py` | 6 | 1 | 2 | 385, 386 |

### Historical Theories

**Location:** `maxwell/theories/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `failure_modes.py` | 8 | 1 | 3 | 857-859 |

### Engineering

**Location:** `maxwell/engineering/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `naval.py` | 5 | 2 | 1 | 441 |

### Mechanics

**Location:** `maxwell/mechanics/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `potential_energy.py` | 6 | 1 | 1 | 389 |
| `shell_energy.py` | 6 | 1 | 1 | 423 |

### Philosophy

**Location:** `maxwell/philosophy/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `medium_check.py` | 8 | 2 | 2 | 865, 866 |

### Verification

**Location:** `maxwell/verification/`

| Module | Functions | Classes | Articles | Article Range |
|--------|-----------|---------|----------|---------------|
| `equation_extractor.py` | 0 | 3 | 0 | N/A |
| `equation_registry.py` | 0 | 2 | 0 | N/A |
| `verifier.py` | 0 | 1 | 0 | N/A |

---

## Summary Statistics

| Package Category | Modules | Functions | Classes | Articles |
|-----------------|---------|-----------|---------|----------|
| **Part I - Electrostatics** | 8 | 95 | 11 | 126 |
| **Part II - Electrokinematics** | 10 | 102 | 13 | 125 |
| **Part III - Magnetism** | 2 | 21 | 8 | 26 |
| **Part IV - Electromagnetism** | 54 | 418 | 71 | 269 |
| **Core Physics** | 9 | 46 | 23 | 64 |
| **Mathematics** | 8 | 68 | 7 | 109 |
| **Field Theory** | 5 | 28 | 7 | 12 |
| **Materials** | 7 | 50 | 10 | 12 |
| **Molecular Theory** | 4 | 27 | 8 | 53 |
| **Optics & Waves** | 8 | 81 | 13 | 41 |
| **Instruments** | 5 | 13 | 14 | 23 |
| **Experiments & Calibration** | 3 | 13 | 2 | 13 |
| **Calibration** | 1 | 7 | 2 | 10 |
| **Supporting Packages** | 40+ | 200+ | 50+ | 80+ |
| **TOTAL** | **165** | **1,174** | **244** | **866** |

---

## Citation System

All modules use the `@maxwell_cite` decorator to link implementations to Maxwell's original articles:

```python
from maxwell.meta.citation import maxwell_cite

@maxwell_cite(528, 529, 530)
def faraday_induction(circuit, magnetic_flux):
    """Calculate induced EMF from changing magnetic flux.
    
    Implements Maxwell's formulation of Faraday's law.
    """
    ...
```

See [COVERAGE_SUMMARY.md](./COVERAGE_SUMMARY.md) for detailed coverage analysis.

---

*Generated by SCRIBA - Documentation & Technical Writing Agent*
