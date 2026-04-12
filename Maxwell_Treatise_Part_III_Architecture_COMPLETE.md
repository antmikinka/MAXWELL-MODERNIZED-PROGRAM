# **Maxwell's Treatise: Modernized Architecture Map**

## **Part III: Magnetism — COMPLETE EDITION**

> **Status:** COMPLETE | **Date:** 2026-04-11 | **Version:** 1.0
> **Source:** Maxwell, J.C. *A Treatise on Electricity and Magnetism*, Part III (Magnetism)
> **Coverage:** Arts. 371–474 | 8 Chapters | 12 Layers | 36+ Modules

---

## **Executive Summary**

| Metric | Value |
|--------|-------|
| **Articles** | 104 (Arts. 371–474) |
| **Chapters** | 8 |
| **Layers** | 12 (Layers 30b–42) |
| **Modules** | 36+ |
| **Packages** | 13 (core, physics, fields, calculus, geometry, materials, solvers, components, engineering, instruments, geophysics, mechanics, config) |
| **Cross-part Dependencies** | Part I (Electrostatics, Layers 0–12), Part II (Electrokinematics, Layers 13–30), Part IV (Electromagnetism, Layers 43–86) |

### Part III Scope

Part III establishes the complete theory of **permanent magnetism** as a distinct phenomenon from electromagnetism (Part IV). Maxwell treats magnetism using a dual approach: the "Magnetic Matter" theory (fictitious magnetic poles for calculation) and the "Molecular Theory" (real magnetic dipoles). Key concepts include:

- **Magnetic Units** — The unit pole defined such that $f = m_1 m_2 / r^2$
- **Magnetic Moment & Magnetization** — Vector treatment of magnetic dipoles
- **B, H, I Relations** — The fundamental constitutive relation $B = H + 4\pi I$
- **Solid Angle Method** — Topological calculation of shell potentials
- **Induced Magnetization** — Susceptibility $\kappa$ and permeability $\mu$
- **Weber's Molecular Theory** — Saturation and hysteresis from dipole alignment
- **Magnetic Metrology** — Torsion balances, dip circles, and observatory methods
- **Terrestrial Magnetism** — Spherical harmonic expansion of Earth's field

### Layer Numbering

| Layer Range | Part | Domain |
|-------------|------|--------|
| 0–12 | Part I | Electrostatics |
| 13–30 | Part II | Electrokinematics |
| **30b–42** | **Part III** | **Magnetism** |
| 43–86 | Part IV | Electromagnetism |
| 90–94 | Part V | System Core |
| 95–97 | Part VI | Scalar Physics |

---

## **Package Directory Structure**

```
maxwell/
├── core/                              # [Part III, Layer 30b-31] Magnetic fundamentals
│   ├── __init__.py
│   ├── units.py                       # Art. 374: Magnetic units, dimensions
│   ├── magnet.py                      # Arts. 371-376: Magnet, axis, polarity
│   ├── matter.py                      # Arts. 377-380: Magnetic matter theory
│   └── moment.py                      # Arts. 381-384: Magnetic moment, magnetization
│
├── physics/                           # [Part III, Layers 32, 37, 39] Core physics
│   ├── __init__.py
│   ├── potentials.py                  # Arts. 385-386: Scalar potential calculations
│   ├── coupling.py                    # Arts. 387-390: Dipole interactions
│   ├── molecular_theory.py            # Art. 430: Poisson's molecular theory
│   ├── magnetostriction.py            # Arts. 447-448: Dimensional changes
│   └── induction.py                   # Arts. 424-426: Induced magnetization
│
├── fields/                            # [Part III, Layers 34-35] Field definitions
│   ├── __init__.py
│   ├── force.py                       # Arts. 395-398: Magnetic force (H)
│   ├── induction.py                   # Art. 399: Magnetic induction (B)
│   ├── constitutive.py                # Art. 400: B = H + 4πI relation
│   ├── solenoidal.py                  # Arts. 403-404: Solenoidal condition
│   └── decomposition.py               # Arts. 412-416: Lamellar/solenoidal decomposition
│
├── calculus/                          # [Part III, Layers 35-36] Vector calculus
│   ├── __init__.py
│   ├── integrals.py                   # Arts. 401-402: Line/surface integrals
│   ├── vector_potential.py            # Arts. 405-406: Vector potential A
│   └── cyclic.py                      # Arts. 417-422: Cyclic functions, solid angles
│
├── geometry/                          # [Part III, Layer 36] Magnetic geometry
│   ├── __init__.py
│   ├── solenoids.py                   # Arts. 407-408: Solenoid definitions
│   └── shells.py                      # Arts. 409-411: Magnetic shells
│
├── materials/                         # [Part III, Layers 37-38] Material response
│   ├── __init__.py
│   ├── induction.py                   # Arts. 424-426: Susceptibility κ
│   ├── saturation.py                  # Arts. 442-443: Weber saturation model
│   └── hysteresis.py                  # Arts. 444-446: Hysteresis loops
│
├── solvers/                           # [Part III, Layer 37] Induction solvers
│   ├── __init__.py
│   ├── induction_solvers.py           # Arts. 427-428: Poisson/Faraday methods
│   └── shape_solvers.py               # Arts. 431-440: Analytical shape solutions
│
├── components/                        # [Part III, Layer 38] Magnetic components
│   ├── __init__.py
│   ├── spheres.py                     # Arts. 431-433: Hollow spheres
│   └── ellipsoids.py                  # Arts. 437-438: Ellipsoidal magnets
│
├── engineering/                       # [Part III, Layer 38] Applied magnetism
│   ├── __init__.py
│   └── naval.py                       # Art. 441: Ship's magnetism
│
├── instruments/                       # [Part III, Layer 40] Measurement devices
│   ├── __init__.py
│   ├── suspension.py                  # Arts. 449-452: Unifilar/bifilar suspension
│   ├── magnetometer.py                # Arts. 453-455: Deflection magnetometers
│   ├── dynamics.py                    # Arts. 456-460: Vibration methods
│   ├── dip_circle.py                  # Arts. 461-463: Dip measurement
│   └── vertical_force.py              # Art. 464: Balance magnetometer
│
├── geophysics/                        # [Part III, Layer 41] Terrestrial magnetism
│   ├── __init__.py
│   ├── survey.py                      # Arts. 465-466: Magnetic surveys
│   ├── gauss_model.py                 # Arts. 467-470: Gauss spherical harmonics
│   └── variations.py                  # Arts. 471-473: Temporal variations
│
├── mechanics/                         # [Part III, Layer 42] Magnetic mechanics
│   ├── __init__.py
│   ├── potential_energy.py            # Art. 389: Dipole potential energy
│   └── shell_energy.py                # Art. 423: Shell work calculations
│
└── math/
    └── spherical/                     # [Part III, Layer 41] Spherical harmonics
        ├── magnetic.py                # Art. 391: Magnetic harmonic expansion
        └── terrestrial.py             # Arts. 467-470: Earth's field expansion

└── config/                            # [Part III, Layer 33] Conventions
    └── conventions.py                 # Arts. 393-394: Austral/Boreal polarity
```

---

## **Layer 30b: Magnetic Units & Dimensions**

**Source:** Chapter I — Elementary Theory of Magnetism (Art. 374)
**Goal:** Establish the fundamental dimensional constraints for Magnetism, defining the Unit Pole.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 374 | Definition of magnetic units and their dimensions | `maxwell/core/units.py` | `MagneticDimensions` — Defines unit pole $m$ such that $f = m_1 m_2 / r^2$, dimensions $[L^{3/2} M^{1/2} T^{-1}]$ |

---

## **Layer 31: The Magnetic Primitives**

**Source:** Chapter I — Elementary Theory of Magnetism (Arts. 371–376, 381–384)
**Goal:** Define the fundamental unit of magnetism — the magnetic dipole as a vector quantity.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 371 | Properties of a magnet when acted on by the earth | `maxwell/core/magnet.py` | `Magnet.earth_response()` — Magnet behavior in terrestrial field |
| 372 | Definition of the axis of the magnet and of the direction of magnetic force | `maxwell/core/magnet.py` | `MagneticAxis` — Axis definition and force direction |
| 373 | Action of magnets on one another. Law of magnetic force | `maxwell/core/magnet.py` | `Magnet.mutual_action()` — Magnet-magnet interaction |
| 374 | Definition of magnetic units and their dimensions | `maxwell/core/units.py` | `MagneticDimensions` — Unit pole definition |
| 375 | Nature of the evidence for the law of magnetic force | `maxwell/core/magnet.py` | `verify_force_law_evidence()` — Experimental basis for inverse-square |
| 376 | Magnetism as a mathematical quantity | `maxwell/core/magnet.py` | `MagneticQuantity` — Mathematical treatment framework |
| 381 | Magnetization is of the nature of a vector | `maxwell/core/moment.py` | `MagnetizationVector` — Vector nature of magnetization |
| 382 | Meaning of the term 'Magnetic Polarization' | `maxwell/core/moment.py` | `MagneticPolarization` — Polarization definition |
| 383 | Properties of a magnetic particle | `maxwell/core/moment.py` | `MagneticParticle` — Elementary dipole properties |
| 384 | Definitions of Magnetic Moment, Intensity of Magnetization, and Components of Magnetization | `maxwell/core/moment.py` | `MagneticMoment`, `MagnetizationIntensity`, `MagnetizationComponents` |

---

## **Layer 32: Magnetic Matter Theory**

**Source:** Chapter I — Elementary Theory of Magnetism (Arts. 377–380)
**Goal:** Abstraction treating N/S poles as "fictitious charges" for calculation purposes.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 377 | The quantities of the opposite kinds of magnetism in a magnet are always exactly equal | `maxwell/core/matter.py` | `verify_equal_opposite()` — Proof of equal N/S quantities |
| 378 | Effects of breaking a magnet | `maxwell/core/matter.py` | `break_magnet()` — Each fragment remains a complete magnet |
| 379 | A magnet is built up of particles each of which is a magnet | `maxwell/core/matter.py` | `MolecularMagnet` — Particle-based magnet model |
| 380 | Theory of magnetic 'matter' | `maxwell/core/matter.py` | `MagneticMatterTheory` — Fictitious magnetic charge abstraction |

---

## **Layer 33: Dipole Interactions**

**Source:** Chapter I — Elementary Theory of Magnetism (Arts. 385–392)
**Goal:** Calculate the potential and force exerted by magnets on each other.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 385 | Potential of a magnetized element of volume | `maxwell/physics/potentials.py` | `calc_element_potential()` — Potential from infinitesimal magnet |
| 386 | Potential of a magnet of finite size. Two expressions for this potential | `maxwell/physics/potentials.py` | `calc_finite_potential()` — Polarization vs magnetic matter formulations |
| 387 | Investigation of the action of one magnetic particle on another | `maxwell/physics/coupling.py` | `calc_dipole_interaction()` — Full dipole-dipole force/torque |
| 388 | Particular cases | `maxwell/physics/coupling.py` | `special_dipole_cases()` — Aligned, perpendicular, collinear cases |
| 389 | Potential energy of a magnet in any field of force | `maxwell/mechanics/potential_energy.py` | `calc_dipole_potential_energy()` — $W = -\vec{m} \cdot \vec{B}$ |
| 390 | On the magnetic moment and axis of a magnet | `maxwell/core/moment.py` | `resultant_moment_and_axis()` — Net moment of complex magnet |
| 391 | Expansion of the potential of a magnet in spherical harmonics | `maxwell/math/spherical/magnetic.py` | `expand_potential_harmonics()` — Multipole expansion |
| 392 | The centre of a magnet and the primary and secondary axes through the centre | `maxwell/core/magnet.py` | `Magnet.center_and_axes()` — Principal axes determination |

---

## **Layer 34: Coordinate Conventions**

**Source:** Chapter I — Elementary Theory of Magnetism (Arts. 393–394)
**Goal:** Strict enforcement of North/South terminology to prevent sign errors.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 393 | The north end of a magnet in this treatise is that which points north, and the south end that which points south. Boreal magnetism is that which is supposed to exist near the north pole of the earth and the south end of a magnet. Austral magnetism is that which belongs to the south pole of the earth and the north end of a magnet. Austral magnetism is considered positive | `maxwell/config/conventions.py` | `PolarityConvention` — Austral (+) vs Boreal (-) convention |
| 394 | The direction of magnetic force is that in which austral magnetism tends to move, that is, from south to north, and this is the positive direction of magnetic lines of force. A magnet is said to be magnetized from its south end towards its north end | `maxwell/config/conventions.py` | `ForceDirectionConvention` — Positive direction S→N |

---

## **Layer 35: Magnetic Force & Induction (B, H, I)**

**Source:** Chapter II — Magnetic Force and Magnetic Induction (Arts. 395–400)
**Goal:** Distinguishing the Total Field (B) from the Applied Field (H) and the Material Field (I).

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 395 | Magnetic force defined with reference to the magnetic potential | `maxwell/fields/force.py` | `MagneticForce.from_potential()` — $H = -\nabla \Omega$ |
| 396 | Magnetic force in a cylindric cavity in a magnet uniformly magnetized parallel to the axis of the cylinder | `maxwell/fields/force.py` | `cylindric_cavity_force()` — H measured via long narrow cavity |
| 397 | Application to any magnet | `maxwell/fields/force.py` | `general_magnet_force()` — Extension to arbitrary magnetization |
| 398 | An elongated cylinder.—Magnetic force | `maxwell/fields/force.py` | `elongated_cylinder_force()` — Needle cavity limit |
| 399 | A thin disk.—Magnetic induction | `maxwell/fields/induction.py` | `thin_disk_induction()` — B measured via flat disk cavity |
| 400 | Relation between magnetic force, magnetic induction, and magnetization | `maxwell/fields/constitutive.py` | `calc_constitutive_relation()` — $B = H + 4\pi I$ |

---

## **Layer 36: Magnetic Integrals & Vector Potential**

**Source:** Chapter II — Magnetic Force and Magnetic Induction (Arts. 401–406)
**Goal:** Implementing the calculus operations for magnetic fields and the vector potential.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 401 | Line-integral of magnetic force, or magnetic potential | `maxwell/calculus/integrals.py` | `calc_line_integral_force()` — $\int H \cdot dl$ |
| 402 | Surface-integral of magnetic induction | `maxwell/calculus/integrals.py` | `calc_surface_induction()` — $\iint B \cdot dA$, Gauss's law for magnetism |
| 403 | Solenoidal distribution of magnetic induction | `maxwell/fields/solenoidal.py` | `verify_solenoidal()` — $\nabla \cdot B = 0$ |
| 404 | Surfaces and tubes of magnetic induction | `maxwell/fields/solenoidal.py` | `MagneticInductionTube` — Flux tube properties |
| 405 | Vector-potential of magnetic induction | `maxwell/calculus/vector_potential.py` | `calc_vector_potential()` — $B = \nabla \times A$ |
| 406 | Relations between the scalar and the vector-potential | `maxwell/calculus/vector_potential.py` | `relate_scalar_vector_potential()` — $\Omega$ vs $A$ relationship |

---

## **Layer 37: Magnetic Solenoids & Shells**

**Source:** Chapter III — Magnetic Solenoids and Shells (Arts. 407–416)
**Goal:** Using geometric constructs to calculate potentials of complex shapes.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 407 | Definition of a magnetic solenoid | `maxwell/geometry/solenoids.py` | `Solenoid` — Tubular magnetic distribution |
| 408 | Definition of a complex solenoid and expression for its potential at any point | `maxwell/geometry/solenoids.py` | `ComplexSolenoid.potential()` — Generalized solenoid |
| 409 | The potential of a magnetic shell at any point is the product of its strength multiplied by the solid angle its boundary subtends at the point | `maxwell/geometry/shells.py` | `MagneticShell.potential()` — $\Omega = \Phi \times \omega$ |
| 410 | Another method of proof | `maxwell/geometry/shells.py` | `shell_potential_alternative_proof()` — Alternative derivation |
| 411 | The potential at a point on the positive side of a shell of strength Φ exceeds that on the nearest point on the negative side by 4πΦ | `maxwell/geometry/shells.py` | `shell_potential_discontinuity()` — Potential jump across shell |
| 412 | Lamellar distribution of magnetism | `maxwell/fields/decomposition.py` | `LamellarDistribution` — Irrotational (gradient) field |
| 413 | Complex lamellar distribution | `maxwell/fields/decomposition.py` | `ComplexLamellarDistribution` — Composite lamellar system |
| 414 | Potential of a solenoidal magnet | `maxwell/geometry/solenoids.py` | `solenoid_potential()` — Complete solenoid solution |
| 415 | Potential of a lamellar magnet | `maxwell/fields/decomposition.py` | `lamellar_potential()` — Lamellar magnet solution |
| 416 | Vector-potential of a lamellar magnet | `maxwell/fields/decomposition.py` | `lamellar_vector_potential()` — A for lamellar case |

---

## **Layer 38: Solid Angle Calculus**

**Source:** Chapter III — Magnetic Solenoids and Shells (Arts. 417–423)
**Goal:** Computing solid angles and cyclic functions for closed curve potentials.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 417 | On the solid angle subtended at a given point by a closed curve | `maxwell/calculus/cyclic.py` | `calc_solid_angle_closed_curve()` — Geometric solid angle |
| 418 | The solid angle expressed by the length of a curve on the sphere | `maxwell/calculus/cyclic.py` | `solid_angle_as_sphere_curve()` — Spherical curve length |
| 419 | Solid angle found by two line-integrations | `maxwell/calculus/cyclic.py` | `solid_angle_double_line_integral()` — Gauss's method |
| 420 | Π expressed as a determinant | `maxwell/calculus/cyclic.py` | `solid_angle_determinant()` — Determinant formulation |
| 421 | The solid angle is a cyclic function | `maxwell/calculus/cyclic.py` | `CyclicFunction` — Multi-valued nature |
| 422 | Theory of the vector-potential of a closed curve | `maxwell/calculus/cyclic.py` | `vector_potential_closed_curve()` — A for current loop |
| 423 | Potential energy of a magnetic shell placed in a magnetic field | `maxwell/mechanics/shell_energy.py` | `calc_shell_potential_energy()` — Work on shell in field |

---

## **Layer 39: Induced Magnetization**

**Source:** Chapter IV — Induced Magnetization (Arts. 424–430)
**Goal:** Modeling how neutral matter becomes magnetized under external influence.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 424 | When a body under the action of magnetic force becomes itself magnetized the phenomenon is called magnetic induction | `maxwell/materials/induction.py` | `InducedMagnetization` — Phenomenon definition |
| 425 | Magnetic induction in different substances | `maxwell/materials/induction.py` | `SubstanceInduction` — Para/dia/ferro-magnetic classification |
| 426 | Definition of the coefficient of induced magnetization | `maxwell/materials/induction.py` | `MagneticSusceptibility` — Coefficient $\kappa$ where $I = \kappa H$ |
| 427 | Mathematical theory of magnetic induction. Poisson's method | `maxwell/solvers/induction_solvers.py` | `method_poisson()` — Volume integral approach |
| 428 | Faraday's method | `maxwell/solvers/induction_solvers.py` | `method_faraday()` — Field line approach |
| 429 | Case of a body surrounded by a magnetic medium | `maxwell/solvers/induction_solvers.py` | `body_in_magnetic_medium()` — Permeability contrast |
| 430 | Poisson's physical theory of the cause of induced magnetism | `maxwell/physics/molecular_theory.py` | `simulate_poisson_molecular()` — Dipole re-orientation model |

---

## **Layer 40: Particular Problems in Induction**

**Source:** Chapter V — Particular Problems in Magnetic Induction (Arts. 431–441)
**Goal:** Exact analytical solutions for specific shapes used to benchmark solvers.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 431 | Theory of a hollow spherical shell | `maxwell/components/spheres.py` | `HollowSphere.induction()` — Shielding factor calculation |
| 432 | Case when κ is large | `maxwell/components/spheres.py` | `high_susceptibility_limit()` — Ferromagnetic limit |
| 433 | When i = 1 | `maxwell/components/spheres.py` | `unit_current_case()` — Special case solution |
| 434 | Corresponding case in two dimensions | `maxwell/components/spheres.py` | `cylindrical_shell_2d()` — 2D analogue |
| 435 | Case of a solid sphere, the coefficients of magnetization being different in different directions | `maxwell/components/spheres.py` | `anisotropic_sphere()` — Anisotropic susceptibility tensor |
| 436 | The nine coefficients reduced to six. | `maxwell/components/spheres.py` | `reduce_coefficients_9_to_6()` — Symmetry reduction |
| 437 | Theory of an ellipsoid acted on by a uniform magnetic force | `maxwell/components/ellipsoids.py` | `MagnetizedEllipsoid` — Uniform internal field solution |
| 438 | Cases of very flat and of very long ellipsoids | `maxwell/components/ellipsoids.py` | `extreme_ellipsoid_limits()` — Disk and needle limits |
| 439 | Statement of problems solved by Neumann, Kirchhoff, and Green | `maxwell/solvers/shape_solvers.py` | `classical_solutions_summary()` — Historical solutions |
| 440 | Method of approximation to a solution of the general problem when κ is very small. Magnetic bodies tend towards places of most intense magnetic force, and diamagnetic bodies tend to places of weakest force | `maxwell/solvers/shape_solvers.py` | `small_kappa_approximation()` — Weak susceptibility limit |
| 441 | On ship's magnetism | `maxwell/engineering/naval.py` | `ShipMagnetism` — Permanent and induced ship magnetism model |

---

## **Layer 41: Weber's Theory of Induced Magnetism**

**Source:** Chapter VI — Weber's Theory of Induced Magnetism (Arts. 442–448)
**Goal:** Modeling saturation, hysteresis, and magnetostriction from molecular alignment.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 442 | Experiments indicating a maximum of magnetization | `maxwell/materials/saturation.py` | `observe_saturation()` — Experimental saturation curves |
| 443 | Weber's mathematical theory of temporary magnetization | `maxwell/materials/saturation.py` | `WeberModel` — Statistical dipole alignment |
| 444 | Modification of the theory to account for residual magnetization | `maxwell/materials/hysteresis.py` | `WeberModelWithHysteresis` — Residual magnetization extension |
| 445 | Explanation of phenomena by the modified theory | `maxwell/materials/hysteresis.py` | `explain_hysteresis_phenomena()` — Theory validation |
| 446 | Magnetization, demagnetization, and remagnetization | `maxwell/materials/hysteresis.py` | `HysteresisLoop` — Full hysteresis cycle simulation |
| 447 | Effects of magnetization on the dimensions of the magnet | `maxwell/physics/magnetostriction.py` | `calc_magnetostriction()` — Dimensional change from alignment |
| 448 | Experiments of Joule | `maxwell/physics/magnetostriction.py` | `joule_magnetostriction_data()` — Experimental validation |

---

## **Layer 42: Magnetic Measurements**

**Source:** Chapter VII — Magnetic Measurements (Arts. 449–464)
**Goal:** Precise instrumentation to measure intensity, declination, and dip.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 449 | Suspension of the magnet | `maxwell/instruments/suspension.py` | `UnifilarSuspension` — Single-fiber suspension mechanics |
| 450 | Methods of observation by mirror and scale. Photographic method | `maxwell/instruments/suspension.py` | `OpticalLever`, `PhotographicMethod` — Readout techniques |
| 451 | Principle of collimation employed in the Kew magnetometer | `maxwell/instruments/suspension.py` | `KewMagnetometer.collimation()` — Collimation principle |
| 452 | Determination of the axis of a magnet and of the direction of the horizontal component of the magnetic force | `maxwell/instruments/suspension.py` | `determine_magnet_axis()` — Axis alignment procedure |
| 453 | Measurement of the moment of a magnet and of the intensity of the horizontal component of magnetic force | `maxwell/instruments/magnetometer.py` | `measure_moment_and_horizontal_force()` — Deflection method |
| 454 | Observations of deflexion | `maxwell/instruments/magnetometer.py` | `observe_deflection()` — Deflection measurement protocol |
| 455 | Method of tangents and method of sines | `maxwell/instruments/magnetometer.py` | `method_tangents()`, `method_sines()` — Calculation methods |
| 456 | Observation of vibrations | `maxwell/instruments/dynamics.py` | `observe_vibrations()` — Oscillation period measurement |
| 457 | Elimination of the effects of magnetic induction | `maxwell/instruments/dynamics.py` | `eliminate_induction_effects()` — Correction for induced magnetism |
| 458 | Statical method of measuring the horizontal force | `maxwell/instruments/dynamics.py` | `statical_horizontal_force()` — Static deflection method |
| 459 | Bifilar suspension | `maxwell/instruments/dynamics.py` | `BifilarSuspension` — Two-fiber suspension for torque |
| 460 | System of observations in an observatory | `maxwell/instruments/dynamics.py` | `ObservatorySystem` — Standard observatory protocol |
| 461 | Observation of the dip-circle | `maxwell/instruments/dip_circle.py` | `DipCircle.observe()` — Inclination measurement |
| 462 | J. A. Broun's method of correction | `maxwell/instruments/dip_circle.py` | `broun_correction()` — Dip circle error correction |
| 463 | Joule's suspension | `maxwell/instruments/dip_circle.py` | `JouleSuspension` — Alternative dip suspension |
| 464 | Balance vertical force magnetometer | `maxwell/instruments/vertical_force.py` | `BalanceVerticalForceMagnetometer` — Vertical component measurement |

---

## **Layer 43: Terrestrial Magnetism**

**Source:** Chapter VIII — On Terrestrial Magnetism (Arts. 465–474)
**Goal:** Modeling the Earth's global magnetic field using Spherical Harmonic expansions.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 465 | Elements of the magnetic force | `maxwell/geophysics/survey.py` | `MagneticElements` — Declination, inclination, intensity |
| 466 | Combination of the results of the magnetic survey of a country | `maxwell/geophysics/survey.py` | `MagneticSurvey.aggregate()` — Regional survey aggregation |
| 467 | Deduction of the expansion of the magnetic potential of the earth in spherical harmonics | `maxwell/geophysics/gauss_model.py` | `expand_earth_potential_harmonics()` — Spherical harmonic expansion |
| 468 | Definition of the earth's magnetic poles. They are not at the extremities of the magnetic axis. False poles. They do not exist on the earth's surface | `maxwell/geophysics/gauss_model.py` | `define_magnetic_poles()` — True vs false poles |
| 469 | Gauss' calculation of the 24 coefficients of the first four harmonics | `maxwell/geophysics/gauss_model.py` | `GaussExpansion` — 24-coefficient model (n=1 to 4) |
| 470 | Separation of external from internal causes of magnetic force | `maxwell/geophysics/gauss_model.py` | `separate_internal_external()` — Source separation |
| 471 | The solar and lunar variations | `maxwell/geophysics/variations.py` | `SolarLunarVariations` — Diurnal variations |
| 472 | The periodic variations | `maxwell/geophysics/variations.py` | `PeriodicVariations` — Seasonal and other periodic changes |
| 473 | The disturbances and their period of 11 years | `maxwell/geophysics/variations.py` | `MagneticDisturbances` — Sunspot cycle correlation |
| 474 | Reflexions on magnetic investigations | `maxwell/geophysics/survey.py` | `magnetic_investigation_reflections()` — Methodological conclusions |

---

## **Article Coverage Index**

### Part III: Magnetism — All Articles Mapped

| Article | Title | Module |
|---------|-------|--------|
| 371 | Properties of a magnet when acted on by the earth | `maxwell/core/magnet.py` |
| 372 | Definition of the axis of the magnet and of the direction of magnetic force | `maxwell/core/magnet.py` |
| 373 | Action of magnets on one another. Law of magnetic force | `maxwell/core/magnet.py` |
| 374 | Definition of magnetic units and their dimensions | `maxwell/core/units.py` |
| 375 | Nature of the evidence for the law of magnetic force | `maxwell/core/magnet.py` |
| 376 | Magnetism as a mathematical quantity | `maxwell/core/magnet.py` |
| 377 | The quantities of the opposite kinds of magnetism in a magnet are always exactly equal | `maxwell/core/matter.py` |
| 378 | Effects of breaking a magnet | `maxwell/core/matter.py` |
| 379 | A magnet is built up of particles each of which is a magnet | `maxwell/core/matter.py` |
| 380 | Theory of magnetic 'matter' | `maxwell/core/matter.py` |
| 381 | Magnetization is of the nature of a vector | `maxwell/core/moment.py` |
| 382 | Meaning of the term 'Magnetic Polarization' | `maxwell/core/moment.py` |
| 383 | Properties of a magnetic particle | `maxwell/core/moment.py` |
| 384 | Definitions of Magnetic Moment, Intensity of Magnetization, and Components of Magnetization | `maxwell/core/moment.py` |
| 385 | Potential of a magnetized element of volume | `maxwell/physics/potentials.py` |
| 386 | Potential of a magnet of finite size | `maxwell/physics/potentials.py` |
| 387 | Investigation of the action of one magnetic particle on another | `maxwell/physics/coupling.py` |
| 388 | Particular cases | `maxwell/physics/coupling.py` |
| 389 | Potential energy of a magnet in any field of force | `maxwell/mechanics/potential_energy.py` |
| 390 | On the magnetic moment and axis of a magnet | `maxwell/core/moment.py` |
| 391 | Expansion of the potential of a magnet in spherical harmonics | `maxwell/math/spherical/magnetic.py` |
| 392 | The centre of a magnet and the primary and secondary axes through the centre | `maxwell/core/magnet.py` |
| 393 | The north end of a magnet... Austral magnetism is considered positive | `maxwell/config/conventions.py` |
| 394 | The direction of magnetic force is that in which austral magnetism tends to move | `maxwell/config/conventions.py` |
| 395 | Magnetic force defined with reference to the magnetic potential | `maxwell/fields/force.py` |
| 396 | Magnetic force in a cylindric cavity in a magnet uniformly magnetized | `maxwell/fields/force.py` |
| 397 | Application to any magnet | `maxwell/fields/force.py` |
| 398 | An elongated cylinder.—Magnetic force | `maxwell/fields/force.py` |
| 399 | A thin disk.—Magnetic induction | `maxwell/fields/induction.py` |
| 400 | Relation between magnetic force, magnetic induction, and magnetization | `maxwell/fields/constitutive.py` |
| 401 | Line-integral of magnetic force, or magnetic potential | `maxwell/calculus/integrals.py` |
| 402 | Surface-integral of magnetic induction | `maxwell/calculus/integrals.py` |
| 403 | Solenoidal distribution of magnetic induction | `maxwell/fields/solenoidal.py` |
| 404 | Surfaces and tubes of magnetic induction | `maxwell/fields/solenoidal.py` |
| 405 | Vector-potential of magnetic induction | `maxwell/calculus/vector_potential.py` |
| 406 | Relations between the scalar and the vector-potential | `maxwell/calculus/vector_potential.py` |
| 407 | Definition of a magnetic solenoid | `maxwell/geometry/solenoids.py` |
| 408 | Definition of a complex solenoid and expression for its potential at any point | `maxwell/geometry/solenoids.py` |
| 409 | The potential of a magnetic shell at any point is the product of its strength multiplied by the solid angle | `maxwell/geometry/shells.py` |
| 410 | Another method of proof | `maxwell/geometry/shells.py` |
| 411 | The potential at a point on the positive side of a shell exceeds that on the negative side by 4πΦ | `maxwell/geometry/shells.py` |
| 412 | Lamellar distribution of magnetism | `maxwell/fields/decomposition.py` |
| 413 | Complex lamellar distribution | `maxwell/fields/decomposition.py` |
| 414 | Potential of a solenoidal magnet | `maxwell/geometry/solenoids.py` |
| 415 | Potential of a lamellar magnet | `maxwell/fields/decomposition.py` |
| 416 | Vector-potential of a lamellar magnet | `maxwell/fields/decomposition.py` |
| 417 | On the solid angle subtended at a given point by a closed curve | `maxwell/calculus/cyclic.py` |
| 418 | The solid angle expressed by the length of a curve on the sphere | `maxwell/calculus/cyclic.py` |
| 419 | Solid angle found by two line-integrations | `maxwell/calculus/cyclic.py` |
| 420 | Π expressed as a determinant | `maxwell/calculus/cyclic.py` |
| 421 | The solid angle is a cyclic function | `maxwell/calculus/cyclic.py` |
| 422 | Theory of the vector-potential of a closed curve | `maxwell/calculus/cyclic.py` |
| 423 | Potential energy of a magnetic shell placed in a magnetic field | `maxwell/mechanics/shell_energy.py` |
| 424 | When a body under the action of magnetic force becomes itself magnetized | `maxwell/materials/induction.py` |
| 425 | Magnetic induction in different substances | `maxwell/materials/induction.py` |
| 426 | Definition of the coefficient of induced magnetization | `maxwell/materials/induction.py` |
| 427 | Mathematical theory of magnetic induction. Poisson's method | `maxwell/solvers/induction_solvers.py` |
| 428 | Faraday's method | `maxwell/solvers/induction_solvers.py` |
| 429 | Case of a body surrounded by a magnetic medium | `maxwell/solvers/induction_solvers.py` |
| 430 | Poisson's physical theory of the cause of induced magnetism | `maxwell/physics/molecular_theory.py` |
| 431 | Theory of a hollow spherical shell | `maxwell/components/spheres.py` |
| 432 | Case when κ is large | `maxwell/components/spheres.py` |
| 433 | When i = 1 | `maxwell/components/spheres.py` |
| 434 | Corresponding case in two dimensions | `maxwell/components/spheres.py` |
| 435 | Case of a solid sphere, the coefficients of magnetization being different in different directions | `maxwell/components/spheres.py` |
| 436 | The nine coefficients reduced to six | `maxwell/components/spheres.py` |
| 437 | Theory of an ellipsoid acted on by a uniform magnetic force | `maxwell/components/ellipsoids.py` |
| 438 | Cases of very flat and of very long ellipsoids | `maxwell/components/ellipsoids.py` |
| 439 | Statement of problems solved by Neumann, Kirchhoff, and Green | `maxwell/solvers/shape_solvers.py` |
| 440 | Method of approximation to a solution of the general problem when κ is very small | `maxwell/solvers/shape_solvers.py` |
| 441 | On ship's magnetism | `maxwell/engineering/naval.py` |
| 442 | Experiments indicating a maximum of magnetization | `maxwell/materials/saturation.py` |
| 443 | Weber's mathematical theory of temporary magnetization | `maxwell/materials/saturation.py` |
| 444 | Modification of the theory to account for residual magnetization | `maxwell/materials/hysteresis.py` |
| 445 | Explanation of phenomena by the modified theory | `maxwell/materials/hysteresis.py` |
| 446 | Magnetization, demagnetization, and remagnetization | `maxwell/materials/hysteresis.py` |
| 447 | Effects of magnetization on the dimensions of the magnet | `maxwell/physics/magnetostriction.py` |
| 448 | Experiments of Joule | `maxwell/physics/magnetostriction.py` |
| 449 | Suspension of the magnet | `maxwell/instruments/suspension.py` |
| 450 | Methods of observation by mirror and scale. Photographic method | `maxwell/instruments/suspension.py` |
| 451 | Principle of collimation employed in the Kew magnetometer | `maxwell/instruments/suspension.py` |
| 452 | Determination of the axis of a magnet and of the direction of the horizontal component of the magnetic force | `maxwell/instruments/suspension.py` |
| 453 | Measurement of the moment of a magnet and of the intensity of the horizontal component of magnetic force | `maxwell/instruments/magnetometer.py` |
| 454 | Observations of deflexion | `maxwell/instruments/magnetometer.py` |
| 455 | Method of tangents and method of sines | `maxwell/instruments/magnetometer.py` |
| 456 | Observation of vibrations | `maxwell/instruments/dynamics.py` |
| 457 | Elimination of the effects of magnetic induction | `maxwell/instruments/dynamics.py` |
| 458 | Statical method of measuring the horizontal force | `maxwell/instruments/dynamics.py` |
| 459 | Bifilar suspension | `maxwell/instruments/dynamics.py` |
| 460 | System of observations in an observatory | `maxwell/instruments/dynamics.py` |
| 461 | Observation of the dip-circle | `maxwell/instruments/dip_circle.py` |
| 462 | J. A. Broun's method of correction | `maxwell/instruments/dip_circle.py` |
| 463 | Joule's suspension | `maxwell/instruments/dip_circle.py` |
| 464 | Balance vertical force magnetometer | `maxwell/instruments/vertical_force.py` |
| 465 | Elements of the magnetic force | `maxwell/geophysics/survey.py` |
| 466 | Combination of the results of the magnetic survey of a country | `maxwell/geophysics/survey.py` |
| 467 | Deduction of the expansion of the magnetic potential of the earth in spherical harmonics | `maxwell/geophysics/gauss_model.py` |
| 468 | Definition of the earth's magnetic poles | `maxwell/geophysics/gauss_model.py` |
| 469 | Gauss' calculation of the 24 coefficients of the first four harmonics | `maxwell/geophysics/gauss_model.py` |
| 470 | Separation of external from internal causes of magnetic force | `maxwell/geophysics/gauss_model.py` |
| 471 | The solar and lunar variations | `maxwell/geophysics/variations.py` |
| 472 | The periodic variations | `maxwell/geophysics/variations.py` |
| 473 | The disturbances and their period of 11 years | `maxwell/geophysics/variations.py` |
| 474 | Reflexions on magnetic investigations | `maxwell/geophysics/survey.py` |

**Total: 104 articles (371–474), all mapped.**

---

## **Implementation Priority Matrix**

### Phase 1: Foundation (P0 — Critical)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 30b | P0 | `units.py` | Fundamental: defines magnetic unit and dimensions |
| 31 | P0 | `magnet.py`, `moment.py` | Defines what a magnet IS — dipole, moment, axis |
| 34 | P0 | `force.py`, `induction.py`, `constitutive.py` | B, H, I definitions are universal dependencies |
| 35 | P0 | `integrals.py`, `vector_potential.py` | Vector calculus foundation for all field calculations |

### Phase 2: Core Physics (P1 — High)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 32 | P1 | `matter.py` | Magnetic matter theory for calculations |
| 33 | P1 | `potentials.py`, `coupling.py` | Dipole interaction physics |
| 36 | P1 | `solenoids.py`, `shells.py`, `cyclic.py` | Solid angle method — Maxwell's computational shortcut |
| 37 | P1 | `induction_solvers.py` | Poisson and Faraday methods for induced magnetism |
| 38 | P1 | `spheres.py`, `ellipsoids.py` | Analytical benchmark solutions |

### Phase 3: Advanced Materials (P2 — Medium)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 39 | P2 | `saturation.py`, `hysteresis.py` | Weber's nonlinear theory — essential for ferromagnetics |
| 40 | P2 | `molecular_theory.py`, `magnetostriction.py` | Physical mechanism of magnetization |
| 41 | P2 | `suspension.py`, `magnetometer.py`, `dynamics.py`, `dip_circle.py` | Complete metrology suite |

### Phase 4: Geophysics & Integration (P3 — Low)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 41 | P3 | `survey.py`, `gauss_model.py`, `variations.py` | Terrestrial magnetism — data-heavy, specialized |
| 38 | P3 | `naval.py` | Ship magnetism — niche application |
| 42 | P3 | `potential_energy.py`, `shell_energy.py` | Mechanics integration |

### Phase 5: Verification (P4 — Optional)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| All | P4 | Test suite, validation against classical solutions | Quality assurance |

---

## **Validation Checklist**

- [ ] All 104 articles (371–474) have a unique module mapping
- [ ] Each of the 8 chapters is represented by at least one layer
- [ ] No article is mapped to multiple modules (1:1 mapping)
- [ ] All 12 layers (30b–42) have per-article granularity
- [ ] Cross-part dependencies to Part I (Layers 0–12) are documented
- [ ] Cross-part dependencies to Part II (Layers 13–30) are documented
- [ ] Cross-part dependencies to Part IV (Layers 43–86) are documented
- [ ] Package directory tree is consistent with module paths
- [ ] B, H, I constitutive relation is explicitly implemented
- [ ] Solid angle method is implemented (Maxwell's geometric approach)
- [ ] Weber's hysteresis model includes both saturation and residual magnetization
- [ ] All measurement methods (deflection, vibration, dip) have separate implementations
- [ ] Gauss's 24-coefficient spherical harmonic expansion is implemented
- [ ] Ship magnetism model includes both permanent and induced components

---

## **Version History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-11 | Initial COMPLETE architecture map. 104 articles (371–474), 12 layers (30b–42), 36+ modules, 13 packages. Per-article granularity for all 8 chapters. |

---

**END OF PART III DOCUMENT**

