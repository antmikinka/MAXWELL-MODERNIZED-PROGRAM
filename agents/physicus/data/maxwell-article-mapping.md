# Maxwell Article Mapping

## Purpose

Complete mapping of Maxwell's Treatise articles to implemented functions and modules. This document provides traceability from Maxwell's original text to modern Python implementations.

## Part I: Electrostatics (Arts. 27-229)

### Chapter I: Fundamental Concepts (Arts. 27-49)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 27-35 | Electric charge, polarity | `maxwell/core/charge.py` | `ElectricCharge`, `ChargeDistribution` |
| 36-40 | Force measurement | `maxwell/core/measurement.py` | `TorsionBalance` |
| 41-42 | Dimensions and units | `maxwell/core/units.py` | `CGSUnits`, `DimensionalAnalysis` |
| 44-49 | Electric field and potential | `maxwell/physics/electrostatics/field.py` | `electric_field_point_charge`, `potential_point_charge` |

### Chapter II: Mathematical Foundations (Arts. 63-83)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 63-65 | Mathematical definitions | `maxwell/physics/definitions.py` | `FieldDefinition`, `PotentialDefinition` |
| 66-68 | Coulomb's law | `maxwell/physics/forces.py` | `coulomb_force`, `superposition_principle` |
| 69-73 | Potential calculations | `maxwell/physics/potential.py` | `compute_potential`, `potential_integral` |
| 75-76 | Surface integrals, Gauss | `maxwell/physics/integrals.py` | `gauss_law`, `flux_integral` |
| 77-78 | Poisson/Laplace equations | `maxwell/physics/poisson.py` | `solve_poisson`, `solve_laplace` |
| 79-81 | Surface charge/force | `maxwell/physics/surface_forces.py` | `surface_charge_density`, `maxwell_pressure` |
| 82-83 | Dielectric capacity | `maxwell/physics/dielectrics.py` | `specific_inductive_capacity` |

### Chapter III: Multi-Conductor Systems (Arts. 84-94)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 84 | Superposition | `maxwell/systems/superposition.py` | `superpose_fields` |
| 85-86 | Energy, reciprocity | `maxwell/systems/energy.py` | `electrostatic_energy`, `reciprocity_theorem` |
| 87-88 | Coefficient matrices | `maxwell/systems/coefficients.py` | `CapacitanceMatrix` |
| 89-92 | Coefficient relations | `maxwell/systems/constraints.py` | `coefficient_relations` |
| 93-94 | Mechanical forces | `maxwell/systems/forces.py` | `force_on_conductor` |

### Chapter IV-VI: Advanced Theory (Arts. 95-123)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 95-98 | Green's theorem/function | `maxwell/solvers/greens.py` | `greens_function`, `greens_reciprocity` |
| 99-100 | Energy integrals, Thomson | `maxwell/solvers/thomson.py` | `thomson_minimum_theorem` |
| 101-103 | Maxwell stress tensor | `maxwell/analysis/stress.py` | `MaxwellStressTensor`, `stress_integral` |
| 104-110 | Stress objections | `maxwell/docs/stress_discussion.md` | (documentation) |
| 111-116 | Equilibrium, Earnshaw | `maxwell/analysis/stability.py` | `earnshaw_theorem` |
| 117-123 | Visualization | `maxwell/vis/contours.py` | `plot_equipotentials`, `plot_field_lines` |

### Chapter VII-XIII: Special Solutions (Arts. 124-229)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 124-127 | Standard components | `maxwell/components/plates.py`, `spheres.py`, `cylinders.py` | `ParallelPlateCapacitor`, `ConcentricSpheres` |
| 128-146 | Spherical harmonics | `maxwell/math/spherical/` | `SphericalHarmonics`, `legendre_polynomials` |
| 147-154 | Ellipsoidal coordinates | `maxwell/math/ellipsoidal/` | `EllipsoidalHarmonics` |
| 155-175 | Method of images | `maxwell/solvers/images/` | `image_charge_sphere`, `image_charge_plane` |
| 176-181 | Thomson's bowl | `maxwell/solvers/images/bowl.py` | `thomsons_bowl_solver` |
| 182-206 | 2D field theory | `maxwell/math/complex/` | `ConjugateFunctions`, `neumann_transform` |
| 207-229 | Instrumentation | `maxwell/instruments/` | `Electrometer`, `QuadrantElectrometer` |

## Part II: Electrokinematics (Arts. 230-370)

### Chapter I-II: Current Fundamentals (Arts. 230-245)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 230-235 | Electric current | `maxwell/kinematics/current.py` | `ElectricCurrent`, `current_density` |
| 236-240 | Electrolytic action | `maxwell/chemistry/electrolysis.py` | `Electrolyte`, `Ion` |
| 241 | Ohm's law | `maxwell/physics/ohm.py` | `solve_ohm_law` |
| 242 | Joule heating | `maxwell/thermodynamics/joule.py` | `calc_joule_heating` |
| 243-245 | Thermal analogy | `maxwell/thermodynamics/analogy.py` | `thermal_conduction_model` |

### Chapter III-VI: Advanced Conduction (Arts. 246-300)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 246-248 | Contact EMF | `maxwell/materials/contact.py` | `calc_contact_potential` |
| 249-254 | Thermoelectric effects | `maxwell/thermodynamics/thermoelectric.py` | `calc_seebeck`, `calc_peltier`, `calc_thomson` |
| 269-286 | 3D current flow | `maxwell/kinematics/vectors.py` | `CurrentDensity`, `TubesOfFlow` |
| 297-300 | Telegraph equation | `maxwell/telecom/cables.py` | `solve_telegraph_equation` |

### Chapter VII-XII: Networks and Measurement (Arts. 301-370)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 301-320 | Network theory | `maxwell/circuits/network.py` | `CircuitGraph`, `solve_network` |
| 321-350 | Bridge methods | `maxwell/instruments/bridges.py` | `WheatstoneBridge`, `ThomsonBridge` |
| 351-370 | Standards | `maxwell/instruments/standards.py` | `ResistanceStandard` |

## Part III: Magnetism (Arts. 371-474)

### Chapter I: Magnetic Fundamentals (Arts. 371-392)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 371-376 | Magnet properties | `maxwell/core/magnet.py` | `Magnet`, `MagneticAxis` |
| 377-380 | Magnetic matter theory | `maxwell/core/matter.py` | `MagneticMatterTheory` |
| 381-384 | Magnetic moment | `maxwell/core/moment.py` | `MagneticMoment`, `MagnetizationIntensity` |
| 385-392 | Dipole interactions | `maxwell/physics/coupling.py` | `calc_dipole_interaction` |

### Chapter II-V: Field Theory (Arts. 393-428)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 393-394 | Polarity conventions | `maxwell/config/conventions.py` | `PolarityConvention` |
| 395-400 | Field definitions | `maxwell/fields/force.py`, `induction.py` | `MagneticForce`, `MagneticInduction` |
| 401-406 | Vector potential | `maxwell/calculus/vector_potential.py` | `VectorPotential`, `A_field` |
| 407-411 | Solenoids and shells | `maxwell/geometry/solenoids.py`, `shells.py` | `Solenoid`, `MagneticShell` |
| 412-423 | Field decomposition | `maxwell/fields/decomposition.py` | `lamellar_decomposition` |
| 424-428 | Induced magnetization | `maxwell/materials/induction.py` | `InducedMagnetization` |

### Chapter VI-VIII: Materials and Instruments (Arts. 429-474)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 429-440 | Shape effects | `maxwell/solvers/shape_solvers.py` | `ellipsoid_magnetization` |
| 441-448 | Material magnetism | `maxwell/materials/saturation.py`, `hysteresis.py` | `WeberSaturation`, `HysteresisLoop` |
| 449-464 | Instruments | `maxwell/instruments/magnetometer.py` | `DeflectionMagnetometer`, `DipCircle` |
| 465-474 | Terrestrial magnetism | `maxwell/geophysics/gauss_model.py` | `TerrestrialField` |

## Part IV: Electromagnetism (Arts. 475-866)

### Chapter I-VI: EM Force and Induction (Arts. 475-600)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 475-479 | Oersted's discovery | `maxwell/electromagnetism/sources/oersted.py` | `current_creates_B_field` |
| 490-492 | Lorentz force | `maxwell/electromagnetism/forces/lorentz.py` | `lorentz_force` |
| 498-515 | Ampère's force law | `maxwell/electromagnetism/forces/ampere.py` | `ampere_force_law` |
| 528-545 | Faraday's induction | `maxwell/electromagnetism/induction/faraday.py` | `faraday_law`, `induced_emf` |
| 546-570 | Self/mutual inductance | `maxwell/electromagnetism/inductance.py` | `self_inductance`, `mutual_inductance` |

### Chapter VII-XV: Field Equations (Arts. 601-700)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 601-619 | Maxwell's equations | `maxwell/electromagnetism/theory/general_equations.py` | `MaxwellEquations` |
| 620-650 | Energy and stress | `maxwell/electromagnetism/physics/energy_dynamics.py` | `electrokinetic_energy` |
| 675-700 | EM components | `maxwell/electromagnetism/components/` | `Solenoid`, `CircularCoil` |

### Chapter XVI-XXIII: Waves and Advanced Topics (Arts. 701-866)

| Article | Topic | Module | Function/Class |
|---------|-------|--------|----------------|
| 701-750 | EM instrumentation | `maxwell/instruments/galvanometers.py` | `StandardGalvanometer` |
| 751-780 | Absolute measurements | `maxwell/instruments/absolute/` | `WeberMethod` |
| 781-797 | EM waves | `maxwell/optics/wave_equation.py` | `ElectromagneticWave` |
| 798-805 | Wave propagation | `maxwell/optics/plane_waves.py` | `PlaneWave` |
| 806-831 | Magneto-optics | `maxwell/magneto_optics/rotation.py` | `FaradayRotation` |
| 832-866 | Molecular vortices | `maxwell/vortex_engine/` | `MolecularVortexModel` |

## Cross-Reference Index

### By Physics Topic

| Topic | Part I | Part II | Part III | Part IV |
|-------|--------|---------|----------|---------|
| Energy | 85-86, 99-100 | 242, 273 | 389, 423 | 551, 630-640 |
| Force | 93-94, 103-110 | - | 387-388 | 490-492, 602-603 |
| Potential | 69-73, 95-98 | - | 385-386 | 540-541 |
| Stress | 103-110 | - | - | 641-646 |

### By Mathematical Method

| Method | Part I | Part II | Part III | Part IV |
|--------|--------|---------|----------|---------|
| Spherical harmonics | 128-146 | - | 467-470 | - |
| Images | 155-181 | - | - | - |
| Green's function | 95-98 | - | - | - |
| Variational | 99-100 | 297-300 | - | 553-567 |
