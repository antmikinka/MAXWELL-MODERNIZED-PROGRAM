# **Maxwell's Treatise: Modernized Architecture Map**

## **Part II: Electrokinematics — COMPLETE EDITION**

> **Status:** COMPLETE | **Date:** 2026-04-11 | **Version:** 1.0
> **Source:** Maxwell, J.C. *A Treatise on Electricity and Magnetism*, Part II (Electrokinematics)
> **Coverage:** Arts. 230–370 | 12 Chapters | 18 Layers | 50+ Modules

---

## **Executive Summary**

| Metric | Value |
|--------|-------|
| **Articles** | 141 (Arts. 230–370) |
| **Chapters** | 12 |
| **Layers** | 18 (Layers 13–30) |
| **Modules** | 50+ |
| **Packages** | 10 (kinematics, chemistry, thermodynamics, materials, physics, circuits, solvers, telecom, instruments, components) |
| **Cross-part Dependencies** | Part I (Electrostatics, Layers 0–12), Part III (Magnetism, Layers 30b–42) |

### Part II Scope

Part II bridges the static electricity of Part I to the magnetic phenomena of Part III. It covers the **movement** of electricity — electric currents, their generation, measurement, and the physical laws governing conduction through all classes of matter (metals, electrolytes, dielectrics, gases). Key concepts include:

- **Ohm's Law** as the fundamental relation between current, EMF, and resistance
- **Electrolysis** and the ionic theory of conduction
- **Thermoelectric effects** (Seebeck, Peltier, Thomson)
- **3D current flow** — tubes of flow, current sheets, continuity equation
- **Anisotropic conduction** — conductivity tensors, stratified materials
- **Dielectric leakage and electrical absorption** ("soakage")
- **Transmission line theory** — telegraph cable equations
- **Metrology** — Wheatstone bridge, Thomson bridge, resistance standards
- **Material databases** — empirical resistance values for metals, liquids, gases

### Layer Numbering

| Layer Range | Part | Domain |
|-------------|------|--------|
| 0–12 | Part I | Electrostatics |
| **13–30** | **Part II** | **Electrokinematics** |
| 30b–42 | Part III | Magnetism |
| 43–86 | Part IV | Electromagnetism |
| 90–94 | Part V | System Core |
| 95–97 | Part VI | Scalar Physics |

---

## **Package Directory Structure**

```
maxwell/
├── core/                          # [Part I] Core types, units, math
│   ├── __init__.py
│   ├── units.py                   # CGS unit conversions
│   └── math/                      # Vector calculus, quaternion algebra
│
├── kinematics/                    # [Part II, Layers 13, 21] Current flow
│   ├── __init__.py
│   ├── current.py                 # ElectricCurrent class, I=dQ/dt
│   ├── sources.py                 # VoltaicBattery, EMF sources
│   ├── vectors.py                 # 3D current density (u,v,w)
│   ├── streamfunctions.py         # Tubes of flow, current sheets
│   ├── conservation.py            # Continuity equation
│   └── gravity.py                 # Thomson gravity-driven cell
│
├── chemistry/                     # [Part II, Layers 14, 18, 19] Electrochemistry
│   ├── __init__.py
│   ├── electrolysis.py            # Electrolyte, Ion classes
│   ├── transport.py               # Ion migration, modes of passage
│   ├── stoichiometry.py           # Faraday equivalents
│   ├── energetics.py              # Energy conservation in electrolysis
│   ├── polarization.py            # PolarizationState, back EMF
│   └── dissipation.py             # Ion dissipation, leakage
│
├── thermodynamics/                # [Part II, Layers 15, 17, 20] Heat effects
│   ├── __init__.py
│   ├── joule.py                   # Joule heating: H=I²Rt
│   ├── analogy.py                 # Thermal-electrical analogy
│   ├── thermoelectric.py          # Seebeck, Peltier, Thomson effects
│   ├── inversion.py               # Thermoelectric inversion points
│   └── optimization.py            # Minimum heat principle
│
├── materials/                     # [Part II, Layers 16, 24, 25, 29] Material physics
│   ├── __init__.py
│   ├── contact.py                 # Contact potential (Volta's law)
│   ├── electrolytes.py            # Metal-liquid interface
│   ├── composites.py              # Effective conductivity (Maxwell-Garnett)
│   ├── stratified.py              # Layered anisotropy
│   ├── leakage.py                 # LeakyDielectric model
│   └── database/                  # [Layer 29] Material property tables
│       ├── __init__.py
│       ├── metals.py              # ConductorDatabase
│       ├── liquids.py             # ElectrolyteDatabase
│       ├── insulators.py          # DielectricDatabase
│       └── gases.py               # GasDischargeModel
│
├── physics/                       # [Part II, Layers 15, 22, 25] Core physics
│   ├── __init__.py
│   ├── ohm.py                     # solve_ohm_law()
│   ├── anisotropy.py              # ConductivityTensor
│   ├── rotatory.py                # Rotatory coefficient T
│   ├── hysteresis.py              # Residual charge, soakage
│   └── analogies.py               # Mechanical spring-damper analogy
│
├── circuits/                      # [Part II, Layer 20] Network theory
│   ├── __init__.py
│   ├── topology.py                # CircuitGraph, series/parallel
│   └── network.py                 # Linear system solver, conjugate conductors
│
├── solvers/                       # [Part II, Layer 23] Approximation methods
│   ├── __init__.py
│   ├── variational_3d.py          # Generalized Thomson theorem
│   └── rayleigh.py                # Rayleigh resistance bounds
│
├── telecom/                       # [Part II, Layer 26] Transmission lines
│   ├── __init__.py
│   └── cables.py                  # Telegraph equation solver
│
├── instruments/                   # [Part II, Layers 27, 28] Measurement
│   ├── __init__.py
│   ├── standards.py               # Resistance standards (Ohm)
│   ├── bridges.py                 # WheatstoneBridge, DifferentialGalvanometer
│   ├── low_resistance.py          # Thomson (Kelvin) bridge
│   ├── high_resistance.py         # Electrometer decay method
│   └── internal_resistance.py     # Mance method, galvanometer resistance
│
├── components/                    # [Part II, Layers 19, 27] Physical components
│   ├── __init__.py
│   ├── batteries.py               # DaniellCell, SecondaryPile
│   └── coils.py                   # ResistanceCoil models
│
└── magnetics/                     # [Part II → Part III bridge] EM coupling
    ├── __init__.py
    └── coupling.py                # GalvanometerInterface
```

---

## **Layer 13: The Kinetic Primitives (The "Flow")**

**Source:** Chapter I — The Electric Current (Arts. 230–240)
**Goal:** Define the movement of electricity (current) and the driving forces (EMF) that create it.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 230 | Current produced when conductors are discharged | `maxwell/kinematics/current.py` | `ElectricCurrent.from_discharge()` — Transient current from conductor discharge |
| 231 | Transference of electrification | `maxwell/kinematics/current.py` | `ElectricCurrent.transfer_charge()` — Charge transport mechanism |
| 232 | Description of the voltaic battery | `maxwell/kinematics/sources.py` | `VoltaicBattery` — Battery model with internal chemistry |
| 233 | Electromotive force | `maxwell/kinematics/sources.py` | `EMF` — Abstract base for potential difference generators |
| 234 | Production of a steady current | `maxwell/kinematics/sources.py` | `EMF.steady_state()` — Conditions for constant current |
| 235 | Properties of the current | `maxwell/kinematics/current.py` | `ElectricCurrent.properties` — Current characteristics (magnitude, direction, continuity) |
| 236 | Electrolytic action | `maxwell/chemistry/electrolysis.py` | `Electrolyte` — Chemical decomposition by current |
| 237 | Explanation of terms connected with electrolysis | `maxwell/chemistry/electrolysis.py` | `Ion` — Anode, cathode, anion, cation definitions |
| 238 | Different modes of passage of the current | `maxwell/chemistry/transport.py` | `calc_ion_migration()` — Conduction modes in solids vs liquids |
| 239 | Magnetic action of the current | `maxwell/magnetics/coupling.py` | `GalvanometerInterface.magnetic_action()` — Current produces magnetic field |
| 240 | The Galvanometer | `maxwell/magnetics/coupling.py` | `Galvanometer` — Current measurement via deflection |

---

## **Layer 14: Conduction and Resistance (The "Heat")**

**Source:** Chapter II — Conduction and Resistance (Arts. 241–245)
**Goal:** Implement the fundamental laws of resistance and energy dissipation (Ohm & Joule).

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 241 | Ohm's Law | `maxwell/physics/ohm.py` | `solve_ohm_law()` — Fundamental solver: V = IR |
| 242 | Generation of heat by the current. Joule's Law | `maxwell/thermodynamics/joule.py` | `calc_joule_heating()` — Thermal generation: H = I²Rt |
| 243 | Analogy between the conduction of electricity and that of heat | `maxwell/thermodynamics/analogy.py` | `thermal_conduction_model()` — Heat diffusion analogy for electrical distribution |
| 244 | Differences between the two classes of phenomena | `maxwell/thermodynamics/analogy.py` | `distinguish_electrical_thermal()` — Limits of the thermal analogy |
| 245 | Faraday's doctrine of the impossibility of an absolute charge | `maxwell/core/charge.py` | `Charge.isolation_proof()` — No isolated absolute charge exists |

---

## **Layer 15: Contact Electromotive Force (The "Junctions")**

**Source:** Chapter III — Electromotive Force Between Bodies in Contact (Arts. 246–248)
**Goal:** Model the specific potentials arising where two different materials touch.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 246 | Volta's law of the contact force between different metals at the same temperature | `maxwell/materials/contact.py` | `calc_contact_potential()` — Volta's law for metal-metal junctions |
| 247 | Effect of electrolytes | `maxwell/materials/electrolytes.py` | `calc_electrolyte_interface()` — Metal-liquid interface potentials |
| 248 | Thomson's voltaic current in which gravity performs the part of chemical action | `maxwell/kinematics/gravity.py` | `simulate_gravity_cell()` — Gravity-driven current (Thomson's experiment) |

---

## **Layer 16: Thermoelectric Coupling (The "Gradient")**

**Source:** Chapter IV — Electrolysis (Thermoelectric Section, Arts. 249–254)
**Goal:** Model the reversible conversion between heat and electricity (Seebeck/Peltier/Thomson effects).

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 249 | Peltier's phenomenon. Deduction of the thermoelectric electromotive force at a junction | `maxwell/thermodynamics/thermoelectric.py` | `calc_peltier_effect()` — Heat absorption/emission at junctions |
| 250 | Seebeck's discovery of thermoelectric currents | `maxwell/thermodynamics/thermoelectric.py` | `calc_seebeck_emf()` — Current from temperature gradients |
| 251 | Magnus's law of a circuit of one metal | `maxwell/thermodynamics/thermoelectric.py` | `magnus_single_metal_law()` — No thermocurrent in homogeneous metal |
| 252 | Cumming's discovery of thermoelectric inversions | `maxwell/thermodynamics/inversion.py` | `check_thermoelectric_inversion()` — Critical temperature reversal points |
| 253 | Thomson's deductions from these facts, and discovery of the reversible thermal effects of electric currents in copper and in iron | `maxwell/thermodynamics/thermoelectric.py` | `calc_thomson_effect()` — Reversible heating in single conductors |
| 254 | Tait's law of the electromotive force of a thermoelectric pair | `maxwell/thermodynamics/thermoelectric.py` | `tait_thermoelectric_emf()` — Parabolic EMF-temperature relation |

---

## **Layer 17: Molecular Stoichiometry (The "Mole")**

**Source:** Chapter IV — Electrolysis (Molecular Section, Arts. 255–263)
**Goal:** Enforce conservation of mass/energy at the molecular level using Faraday's Laws.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 255 | Faraday's law of electrochemical equivalents | `maxwell/chemistry/stoichiometry.py` | `calc_electrochemical_equivalent()` — m = zQ |
| 256 | Clausius's theory of molecular agitation | `maxwell/chemistry/stoichiometry.py` | `clausius_molecular_model()` — Statistical ion motion theory |
| 257 | Electrolytic polarization | `maxwell/chemistry/polarization.py` | `PolarizationState` — Ion accumulation at electrodes |
| 258 | Test of an electrolyte by polarization | `maxwell/chemistry/polarization.py` | `test_electrolyte()` — Polarization-based electrolyte verification |
| 259 | Difficulties in the theory of electrolysis | `maxwell/chemistry/electrolysis.py` | `ElectrolysisTheory` — Known limitations of the ionic model |
| 260 | Molecular charges | `maxwell/chemistry/stoichiometry.py` | `MolecularCharge` — Discrete charge carriers at molecular scale |
| 261 | Secondary actions observed at the electrodes | `maxwell/chemistry/energetics.py` | `calc_secondary_reactions()` — Side reactions at electrodes |
| 262 | Conservation of energy in electrolysis | `maxwell/chemistry/energetics.py` | `check_energy_conservation()` — Energy balance: ΣE = 0 |
| 263 | Measurement of chemical affinity as an electromotive force | `maxwell/chemistry/energetics.py` | `calc_chemical_affinity_emf()` — Chemical affinity expressed as EMF |

---

## **Layer 18: Polarization Dynamics (The "Back-EMF")**

**Source:** Chapter V — Electrolytic Polarization (Arts. 264–272)
**Goal:** Model the non-ideal behavior of batteries and electrodes (internal resistance and reverse voltage).

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 264 | Difficulties of applying Ohm's law to electrolytes | `maxwell/chemistry/polarization.py` | `ohm_electrolyte_limits()` — Why simple Ohm's law fails for electrolytes |
| 265 | Ohm's law nevertheless applicable | `maxwell/chemistry/polarization.py` | `apply_ohm_corrected()` — Modified Ohm's law with polarization term |
| 266 | The effect of polarization distinguished from that of resistance | `maxwell/chemistry/polarization.py` | `separate_polarization_resistance()` — Distinguishing back-EMF from IR drop |
| 267 | Relation between the electromotive force of polarization and the state of the ions at the electrodes | `maxwell/chemistry/polarization.py` | `calc_polarization_emf_from_ions()` — EMF as function of ion concentration |
| 268 | Dissipation of the ions and loss of polarization | `maxwell/chemistry/dissipation.py` | `calc_ion_dissipation()` — Ion diffusion and polarization decay |
| 269 | Limit of polarization | `maxwell/chemistry/polarization.py` | `max_polarization()` — Saturation limit of polarization |
| 270 | Ritter's secondary pile compared with the Leyden jar | `maxwell/components/batteries.py` | `SecondaryPile` — Rechargeable cell, analogy to capacitor |
| 271 | Constant voltaic elements.—Daniell's cell | `maxwell/components/batteries.py` | `DaniellCell` — Constant EMF cell model |
| 272 | Appendix: Forms of battery | `maxwell/components/batteries.py` | `BatteryCatalog` — Collection of battery types and characteristics |

---

## **Layer 19: Circuit Network Theory (The "Netlist")**

**Source:** Chapter VI — Mathematical Theory of the Distribution of Electric Currents (Arts. 273–284 + Appendix)
**Goal:** Solving complex networks of linear conductors using topological graph theory.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 273 | Linear conductors | `maxwell/circuits/topology.py` | `Conductor` — Linear conductor model |
| 274 | Ohm's Law | `maxwell/circuits/topology.py` | `Conductor.ohm_law()` — V = IR for individual elements |
| 275 | Linear conductors in series | `maxwell/circuits/topology.py` | `CircuitGraph.series()` — Series combination: R_total = ΣR |
| 276 | Linear conductors in multiple arc | `maxwell/circuits/topology.py` | `CircuitGraph.parallel()` — Parallel (multiple arc): 1/R_total = Σ(1/R) |
| 277 | Resistance of conductors of uniform section | `maxwell/circuits/topology.py` | `uniform_wire_resistance()` — R = ρL/A |
| 278 | Dimensions of the quantities involved in Ohm's law | `maxwell/core/units.py` | `dimensional_analysis_ohm()` — [R] = [L]/[T], [I] = [Q]/[T] |
| 279 | Specific resistance and conductivity in electromagnetic measure | `maxwell/core/units.py` | `convert_to_emu()` — CGS electromagnetic unit conversion |
| 280 | Linear systems of conductors in general | `maxwell/circuits/network.py` | `solve_linear_system()` — Kirchhoff's laws for arbitrary networks |
| 281 | Reciprocal property of any two conductors of the system | `maxwell/circuits/network.py` | `reciprocity_theorem()` — Reciprocal conductance relations |
| 282a | Conjugate conductors (condition) | `maxwell/circuits/network.py` | `check_conjugate_condition()` — When two conductors are conjugate (no current in one from EMF in other) |
| 282b | Conjugate conductors (applications) | `maxwell/circuits/network.py` | `apply_conjugate_theorem()` — Applications to bridge circuits |
| 283 | Heat generated in the system | `maxwell/thermodynamics/optimization.py` | `total_heat_generation()` — Σ(I²R) for entire network |
| 284 | The heat is a minimum when the current is distributed according to Ohm's law | `maxwell/thermodynamics/optimization.py` | `minimize_heat_generation()` — Variational proof: Ohm's law minimizes dissipation |
| App. Ch. VI | Appendix to Chapter VI | `tests/verification/verify_network.py` | `test_min_heat_principle()` — Mathematical verification of least heat principle |

---

## **Layer 20: 3D Flow Dynamics (The "Stream")**

**Source:** Chapter VII — Conduction in Three Dimensions (Arts. 285–296)
**Goal:** Generalizing current as a continuous vector fluid flowing through 3D space, not just wires.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 285 | Notation | `maxwell/kinematics/vectors.py` | `CurrentDensity` — Vector field J = (u, v, w) |
| 286 | Composition and resolution of electric currents | `maxwell/kinematics/vectors.py` | `calc_current_density()` — Vector decomposition and superposition |
| 287 | Determination of the quantity which flows through any surface | `maxwell/kinematics/vectors.py` | `flux_through_surface()` — Surface integral of J·dA |
| 288 | Equation of a surface of flow | `maxwell/kinematics/streamfunctions.py` | `FlowSurface` — Implicit surface equation ψ(x,y,z) = const |
| 289 | Relation between any three systems of surfaces of flow | `maxwell/kinematics/streamfunctions.py` | `relate_flow_systems()` — Orthogonality of conjugate flow surfaces |
| 290 | Tubes of flow | `maxwell/kinematics/streamfunctions.py` | `TubeOfFlow` — Quantized flux tubes (streamlines in 3D) |
| 291 | Expression for the components of the flow in terms of surfaces of flow | `maxwell/kinematics/streamfunctions.py` | `components_from_surfaces()` — J = ∇ψ₁ × ∇ψ₂ |
| 292 | Simplification of this expression by a proper choice of parameters | `maxwell/kinematics/streamfunctions.py` | `simplify_flow_expression()` — Optimal parametrization |
| 293 | Unit tubes of flow used as a complete method of determining the current | `maxwell/kinematics/streamfunctions.py` | `UnitTube` — Canonical unit flux tube for visualization |
| 294 | Current-sheets and current-functions | `maxwell/kinematics/streamfunctions.py` | `CurrentSheet` — Surface current density with stream function |
| 295 | Equation of 'continuity' | `maxwell/kinematics/conservation.py` | `continuity_equation()` — ∇·J + ∂ρ/∂t = 0 |
| 296 | Quantity of electricity which flows through a given surface | `maxwell/kinematics/conservation.py` | `total_charge_flux()` — Time integral of surface flux |

---

## **Layer 21: Anisotropic Physics (The "Tensor")**

**Source:** Chapter VIII — Resistance and Conductivity in Three Dimensions (Arts. 297–303)
**Goal:** Handling materials where resistance differs by direction (crystals), using tensors.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 297 | Equations of resistance | `maxwell/physics/anisotropy.py` | `ConductivityTensor` — 3×3 resistance matrix [R] where E = [R]·J |
| 298 | Equations of conduction | `maxwell/physics/anisotropy.py` | `ConductivityTensor.solve()` — J = [σ]·E (inverse tensor) |
| 299 | Rate of generation of heat | `maxwell/physics/anisotropy.py` | `anisotropic_joule_heating()` — J·E = Jᵀ[R]J |
| 300 | Conditions of stability | `maxwell/physics/anisotropy.py` | `check_stability()` — Positive-definiteness of [R] |
| 301 | Equation of continuity in a homogeneous medium | `maxwell/kinematics/conservation.py` | `homogeneous_continuity()` — ∇·(σ∇V) = 0 |
| 302 | Solution of the equation | `maxwell/physics/anisotropy.py` | `solve_anisotropic_potential()` — Ellipsoidal potential solution |
| 303 | Theory of the coefficient T. It probably does not exist | `maxwell/physics/rotatory.py` | `check_rotatory_coefficient()` — Hall-effect-like antisymmetric term (theoretical, unlikely) |

---

## **Layer 22: Approximation Solvers (The "Bounds")**

**Source:** Chapter VIII — Resistance and Conductivity in 3D (Arts. 304–309)
**Goal:** Using Rayleigh's Method to find upper and lower limits of resistance for irregular shapes.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 304 | Generalized form of Thomson's theorem | `maxwell/solvers/variational_3d.py` | `apply_thomson_theorem_generalized()` — Variational minimum energy principle |
| 305 | Proof without symbols | `maxwell/solvers/variational_3d.py` | `thomson_theorem_verbal_proof()` — Intuitive explanation of minimum energy |
| 306 | Lord Rayleigh's method applied to a wire of variable section.—Lower limit of the value of the resistance | `maxwell/solvers/rayleigh.py` | `calc_resistance_lower_bound()` — Rayleigh's lower bound for variable cross-section |
| 307 | Higher limit | `maxwell/solvers/rayleigh.py` | `calc_resistance_upper_bound()` — Rayleigh's upper bound |
| 308 | Lower limit for the correction for the ends of the wire | `maxwell/solvers/rayleigh.py` | `end_correction_lower()` — End effect correction (lower) |
| 309 | Higher limit | `maxwell/solvers/rayleigh.py` | `end_correction_upper()` — End effect correction (upper) |

---

## **Layer 23: Composite Materials (The "Mixture")**

**Source:** Chapter IX — Conduction through Heterogeneous Media (Arts. 310–324)
**Goal:** Modeling heterogeneous media (strata, spheres in suspension) to find effective bulk properties.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 310 | Surface-conditions | `maxwell/materials/composites.py` | `SurfaceConditions` — Boundary conditions at material interfaces |
| 311 | Spherical surface | `maxwell/materials/composites.py` | `spherical_interface_flow()` — Current flow across spherical boundary |
| 312 | Spherical shell | `maxwell/materials/composites.py` | `SphericalShell` — Resistance of concentric spherical layers |
| 313 | Spherical shell placed in a field of uniform flow | `maxwell/materials/composites.py` | `sphere_in_uniform_flow()` — Perturbation analysis |
| 314 | Medium in which small spheres are uniformly disseminated | `maxwell/materials/composites.py` | `calc_effective_conductivity()` — Maxwell-Garnett effective medium theory |
| 315 | Images in a plane surface | `maxwell/materials/composites.py` | `image_method_plane()` — Method of images for plane interfaces |
| 316 | Method of inversion not applicable in three dimensions | `maxwell/materials/composites.py` | `inversion_3d_limitation()` — Why 2D conformal mapping doesn't extend to 3D |
| 317 | Case of conduction through a stratum bounded by parallel planes | `maxwell/materials/stratified.py` | `planar_stratum_conduction()` — Layer between parallel plates |
| 318 | Infinite series of images. Application to magnetic induction | `maxwell/materials/composites.py` | `infinite_image_series()` — Multiple reflection method |
| 319 | On stratified conductors. Coefficients of conductivity of a conductor consisting of alternate strata of two different substances | `maxwell/materials/stratified.py` | `StratifiedConductor` — Effective conductivity of alternating layers |
| 320 | If neither of the substances has the rotatory property denoted by T the compound conductor is free from it | `maxwell/materials/stratified.py` | `check_no_rotatory()` — Composite of non-rotatory materials remains non-rotatory |
| 321 | If the substances are isotropic the direction of greatest resistance is normal to the strata | `maxwell/materials/stratified.py` | `principal_resistance_direction()` — Max resistance ⟂ to layering |
| 322 | Medium containing parallelepipeds of another medium | `maxwell/materials/composites.py` | `parallelepiped_inclusion()` — Rectangular inclusion effective medium |
| 323 | The rotatory property cannot be introduced by means of conducting channels | `maxwell/materials/stratified.py` | `channels_no_rotatory()` — Conducting channels cannot create antisymmetric term |
| 324 | Construction of an artificial solid having given coefficients of longitudinal and transverse conductivity | `maxwell/materials/stratified.py` | `design_artificial_solid()` — Engineered anisotropic metamaterial |

---

## **Layer 24: Dielectric Memory & Leakage (The "Soak")**

**Source:** Chapter X — Conduction in Dielectrics (Arts. 325–334)
**Goal:** Modeling real-world imperfections where insulators leak current and "remember" past charges.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 325 | In a strictly homogeneous medium there can be no internal charge | `maxwell/materials/leakage.py` | `LeakyDielectric.homogeneous_proof()` — ∇·J = 0 implies no internal charge |
| 326 | Theory of a condenser in which the dielectric is not a perfect insulator | `maxwell/materials/leakage.py` | `LeakyDielectric` — RC leakage model for capacitors |
| 327 | No residual charge due to simple conduction | `maxwell/materials/leakage.py` | `simple_conduction_residual()` — Pure conduction produces no memory effect |
| 328 | Theory of a composite accumulator | `maxwell/physics/hysteresis.py` | `CompositeAccumulator` — Multi-layer capacitor with differential leakage |
| 329 | Residual charge and electrical absorption | `maxwell/physics/hysteresis.py` | `calc_residual_charge()` — Dielectric absorption ("soakage") model |
| 330 | Total discharge | `maxwell/physics/hysteresis.py` | `total_discharge_profile()` — Complete discharge curve with recovery |
| 331 | Comparison with the conduction of heat | `maxwell/physics/analogies.py` | `dielectric_heat_analogy()` — Heat diffusion analogy for dielectric relaxation |
| 332 | Theory of telegraph cables and comparison of the equations with those of the conduction of heat | `maxwell/telecom/cables.py` | `solve_telegraph_equation()` — Signal decay: ∂V/∂t = k∂²V/∂x² |
| 333 | Opinion of Ohm on this subject | `maxwell/telecom/cables.py` | `ohm_cable_theory()` — Ohm's perspective on cable transmission |
| 334 | Mechanical illustration of the properties of a dielectric | `maxwell/physics/analogies.py` | `mechanical_dielectric_model()` — Spring-damper analogy for dielectric relaxation |

---

## **Layer 25: Metrology & Standards (The "Ohm")**

**Source:** Chapter XI — Measurement of the Electric Resistance of Conductors (Arts. 335–344)
**Goal:** Defining absolute physical units and the standard components used to represent them.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 335 | Advantage of using material standards of resistance in electrical measurements | `maxwell/instruments/standards.py` | `ResistanceStandard` — Why physical artifacts are needed |
| 336 | Different standards which have been used and different systems which have been proposed | `maxwell/instruments/standards.py` | `StandardHistory` — Survey of resistance standards |
| 337 | The electromagnetic system of units | `maxwell/core/units.py` | `UnitSystemConverter` — EMU (electromagnetic units) system |
| 338 | Weber's unit, and the British Association unit or Ohm | `maxwell/instruments/standards.py` | `BA_Ohm_Standard` — The "Ohm" = 10⁷ m/s definition |
| 339 | Professed value of the Ohm 10,000,000 metres per second | `maxwell/instruments/standards.py` | `ohm_velocity_equivalent()` — Velocity-based unit definition |
| 340 | Reproduction of standards | `maxwell/instruments/standards.py` | `reproduce_standard()` — Calibration chain for standards |
| 341 | Forms of resistance coils | `maxwell/components/coils.py` | `ResistanceCoil` — Physical resistor geometries |
| 342 | Coils of great resistance | `maxwell/components/coils.py` | `HighResistanceCoil` — Fine-wire, high-R coil design |
| 343 | Arrangement of coils in series | `maxwell/components/coils.py` | `CoilSeries` — Series combination of standard resistors |
| 344 | Arrangement in multiple arc | `maxwell/components/coils.py` | `CoilParallel` — Parallel combination of standard resistors |

---

## **Layer 26: Measurement Bridges (The "Balance")**

**Source:** Chapter XI — Measurement of Electric Resistance (Arts. 345–358)
**Goal:** Algorithms for precise measurement using null-methods and bridge topologies.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 345 | On the comparison of resistances. (1) Ohm's method | `maxwell/instruments/bridges.py` | `ohm_comparison_method()` — Direct resistance comparison |
| 346 | (2) By the differential galvanometer | `maxwell/instruments/bridges.py` | `DifferentialGalvanometer` — Null method with dual-coil galvanometer |
| 347 | (3) By Wheatstone's Bridge | `maxwell/instruments/bridges.py` | `WheatstoneBridge` — Classic four-arm bridge circuit |
| 348 | Estimation of limits of error in the determination | `maxwell/instruments/bridges.py` | `bridge_error_analysis()` — Sensitivity and uncertainty bounds |
| 349 | Best arrangement of the conductors to be compared | `maxwell/instruments/bridges.py` | `optimal_bridge_arrangement()` — Maximizing bridge sensitivity |
| 350 | On the use of Wheatstone's Bridge | `maxwell/instruments/bridges.py` | `WheatstoneBridge.operate()` — Practical usage guide and procedure |
| 351 | Thomson's method for small resistances | `maxwell/instruments/low_resistance.py` | `method_thomson_bridge()` — Kelvin double bridge for low R |
| 352 | Matthiessen and Hockin's method for small resistances | `maxwell/instruments/low_resistance.py` | `method_matthiessen_hockin()` — Potentiometric low-R measurement |
| 353 | Comparison of great resistances by the electrometer | `maxwell/instruments/high_resistance.py` | `method_electrometer()` — High-R via electrostatic voltmeter |
| 354 | By accumulation in a condenser | `maxwell/instruments/high_resistance.py` | `method_capacitor_accumulation()` — Charge accumulation method |
| 355 | Direct electrostatic method | `maxwell/instruments/high_resistance.py` | `method_direct_electrostatic()` — Direct leakage current measurement |
| 356 | Thomson's method for the resistance of a galvanometer | `maxwell/instruments/internal_resistance.py` | `method_galvanometer_resistance()` — Thomson's self-resistance method |
| 357 | Mance's method of determining the resistance of a battery | `maxwell/instruments/internal_resistance.py` | `method_mance()` — Battery internal resistance via bridge unbalance |
| 358 | Comparison of electromotive forces | `maxwell/instruments/bridges.py` | `compare_emf()` — Potentiometric EMF comparison |

---

## **Layer 27: Material Properties Database (The "Catalog")**

**Source:** Chapter XII — Electric Resistance of Substances (Arts. 359–370)
**Goal:** A database of empirical resistance values for specific substances.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 359 | Metals, electrolytes, and dielectrics | `maxwell/materials/database/__init__.py` | `MaterialCategory` — Classification framework for material types |
| 360 | Resistance of metals | `maxwell/materials/database/metals.py` | `ConductorDatabase` — Lookup for metal resistivity data |
| 361 | Resistance of mercury | `maxwell/materials/database/metals.py` | `mercury_resistance()` — Mercury as primary resistance standard |
| 362 | Table of resistance of metals | `maxwell/materials/database/metals.py` | `METAL_RESISTANCE_TABLE` — Ag, Cu, Au, Fe, Pt, Zn, etc. |
| 363 | Resistance of electrolytes | `maxwell/materials/database/liquids.py` | `ElectrolyteDatabase` — Concentration-dependent conductivity |
| 364 | Experiments of Paalzow | `maxwell/materials/database/liquids.py` | `paalzow_data()` — Experimental electrolyte resistance data |
| 365 | Experiments of Kohlrausch and Nippoldt | `maxwell/materials/database/liquids.py` | `kohlrausch_nippoldt_data()` — Weak vs strong electrolyte measurements |
| 366 | Resistance of dielectrics | `maxwell/materials/database/insulators.py` | `DielectricDatabase` — Insulator resistivity lookup |
| 367 | Gutta-percha | `maxwell/materials/database/insulators.py` | `gutta_percha_properties()` — Telegraph cable insulation material |
| 368 | Glass | `maxwell/materials/database/insulators.py` | `glass_resistance()` — Temperature-dependent glass resistivity |
| 369 | Gases | `maxwell/materials/database/gases.py` | `GasDischargeModel` — Gas resistance vs pressure (Paschen curve) |
| 370 | Experiments of Wiedemann and Ruhlmann | `maxwell/materials/database/gases.py` | `wiedemann_ruhlmann_data()` — Temperature dependence of gas resistance |

---

## **Layer 28: System Integration & Verification (The "Bridge")**

**Source:** Chapter XI (Units) & Appendix to Chapter VI
**Goal:** Integration of unit systems (Statics to Kinematics) and rigorous verification of network theorems.

| Article | Title | Module Path | Class/Function |
|---------|-------|-------------|----------------|
| 337 | The electromagnetic system of units | `maxwell/core/units/converter.py` | `UnitSystemConverter` — ESU ↔ EMU transformation (c = 3×10¹⁰ cm/s) |
| App. Ch. VI | Appendix to Chapter VI | `tests/verification/verify_network.py` | `test_min_heat_principle()` — Verification: Ohm's law minimizes ΣI²R |

> **Note:** Layer 28 serves as the integration layer between Part I (Electrostatics, ESU) and Part II (Electrokinematics, EMU). The key bridge is the unit conversion factor **c** (speed of light), which later becomes the foundation for Part IV's electromagnetic theory of light.

---

## **Article Coverage Index**

### Part II: Electrokinematics — All Articles Mapped

| Article | Title | Module |
|---------|-------|--------|
| 230 | Current produced when conductors are discharged | `maxwell/kinematics/current.py` |
| 231 | Transference of electrification | `maxwell/kinematics/current.py` |
| 232 | Description of the voltaic battery | `maxwell/kinematics/sources.py` |
| 233 | Electromotive force | `maxwell/kinematics/sources.py` |
| 234 | Production of a steady current | `maxwell/kinematics/sources.py` |
| 235 | Properties of the current | `maxwell/kinematics/current.py` |
| 236 | Electrolytic action | `maxwell/chemistry/electrolysis.py` |
| 237 | Explanation of terms connected with electrolysis | `maxwell/chemistry/electrolysis.py` |
| 238 | Different modes of passage of the current | `maxwell/chemistry/transport.py` |
| 239 | Magnetic action of the current | `maxwell/magnetics/coupling.py` |
| 240 | The Galvanometer | `maxwell/magnetics/coupling.py` |
| 241 | Ohm's Law | `maxwell/physics/ohm.py` |
| 242 | Generation of heat by the current. Joule's Law | `maxwell/thermodynamics/joule.py` |
| 243 | Analogy between the conduction of electricity and that of heat | `maxwell/thermodynamics/analogy.py` |
| 244 | Differences between the two classes of phenomena | `maxwell/thermodynamics/analogy.py` |
| 245 | Faraday's doctrine of the impossibility of an absolute charge | `maxwell/core/charge.py` |
| 246 | Volta's law of the contact force between different metals | `maxwell/materials/contact.py` |
| 247 | Effect of electrolytes | `maxwell/materials/electrolytes.py` |
| 248 | Thomson's voltaic current in which gravity performs the part of chemical action | `maxwell/kinematics/gravity.py` |
| 249 | Peltier's phenomenon | `maxwell/thermodynamics/thermoelectric.py` |
| 250 | Seebeck's discovery of thermoelectric currents | `maxwell/thermodynamics/thermoelectric.py` |
| 251 | Magnus's law of a circuit of one metal | `maxwell/thermodynamics/thermoelectric.py` |
| 252 | Cumming's discovery of thermoelectric inversions | `maxwell/thermodynamics/inversion.py` |
| 253 | Thomson's deductions and discovery of reversible thermal effects | `maxwell/thermodynamics/thermoelectric.py` |
| 254 | Tait's law of the electromotive force of a thermoelectric pair | `maxwell/thermodynamics/thermoelectric.py` |
| 255 | Faraday's law of electrochemical equivalents | `maxwell/chemistry/stoichiometry.py` |
| 256 | Clausius's theory of molecular agitation | `maxwell/chemistry/stoichiometry.py` |
| 257 | Electrolytic polarization | `maxwell/chemistry/polarization.py` |
| 258 | Test of an electrolyte by polarization | `maxwell/chemistry/polarization.py` |
| 259 | Difficulties in the theory of electrolysis | `maxwell/chemistry/electrolysis.py` |
| 260 | Molecular charges | `maxwell/chemistry/stoichiometry.py` |
| 261 | Secondary actions observed at the electrodes | `maxwell/chemistry/energetics.py` |
| 262 | Conservation of energy in electrolysis | `maxwell/chemistry/energetics.py` |
| 263 | Measurement of chemical affinity as an electromotive force | `maxwell/chemistry/energetics.py` |
| 264 | Difficulties of applying Ohm's law to electrolytes | `maxwell/chemistry/polarization.py` |
| 265 | Ohm's law nevertheless applicable | `maxwell/chemistry/polarization.py` |
| 266 | The effect of polarization distinguished from that of resistance | `maxwell/chemistry/polarization.py` |
| 267 | Relation between the electromotive force of polarization and the state of the ions | `maxwell/chemistry/polarization.py` |
| 268 | Dissipation of the ions and loss of polarization | `maxwell/chemistry/dissipation.py` |
| 269 | Limit of polarization | `maxwell/chemistry/polarization.py` |
| 270 | Ritter's secondary pile compared with the Leyden jar | `maxwell/components/batteries.py` |
| 271 | Constant voltaic elements.—Daniell's cell | `maxwell/components/batteries.py` |
| 272 | Appendix: Forms of battery | `maxwell/components/batteries.py` |
| 273 | Linear conductors | `maxwell/circuits/topology.py` |
| 274 | Ohm's Law | `maxwell/circuits/topology.py` |
| 275 | Linear conductors in series | `maxwell/circuits/topology.py` |
| 276 | Linear conductors in multiple arc | `maxwell/circuits/topology.py` |
| 277 | Resistance of conductors of uniform section | `maxwell/circuits/topology.py` |
| 278 | Dimensions of the quantities involved in Ohm's law | `maxwell/core/units.py` |
| 279 | Specific resistance and conductivity in electromagnetic measure | `maxwell/core/units.py` |
| 280 | Linear systems of conductors in general | `maxwell/circuits/network.py` |
| 281 | Reciprocal property of any two conductors of the system | `maxwell/circuits/network.py` |
| 282a,b | Conjugate conductors | `maxwell/circuits/network.py` |
| 283 | Heat generated in the system | `maxwell/thermodynamics/optimization.py` |
| 284 | The heat is a minimum when the current is distributed according to Ohm's law | `maxwell/thermodynamics/optimization.py` |
| 285 | Notation | `maxwell/kinematics/vectors.py` |
| 286 | Composition and resolution of electric currents | `maxwell/kinematics/vectors.py` |
| 287 | Determination of the quantity which flows through any surface | `maxwell/kinematics/vectors.py` |
| 288 | Equation of a surface of flow | `maxwell/kinematics/streamfunctions.py` |
| 289 | Relation between any three systems of surfaces of flow | `maxwell/kinematics/streamfunctions.py` |
| 290 | Tubes of flow | `maxwell/kinematics/streamfunctions.py` |
| 291 | Expression for the components of the flow in terms of surfaces of flow | `maxwell/kinematics/streamfunctions.py` |
| 292 | Simplification of this expression by a proper choice of parameters | `maxwell/kinematics/streamfunctions.py` |
| 293 | Unit tubes of flow used as a complete method of determining the current | `maxwell/kinematics/streamfunctions.py` |
| 294 | Current-sheets and current-functions | `maxwell/kinematics/streamfunctions.py` |
| 295 | Equation of 'continuity' | `maxwell/kinematics/conservation.py` |
| 296 | Quantity of electricity which flows through a given surface | `maxwell/kinematics/conservation.py` |
| 297 | Equations of resistance | `maxwell/physics/anisotropy.py` |
| 298 | Equations of conduction | `maxwell/physics/anisotropy.py` |
| 299 | Rate of generation of heat | `maxwell/physics/anisotropy.py` |
| 300 | Conditions of stability | `maxwell/physics/anisotropy.py` |
| 301 | Equation of continuity in a homogeneous medium | `maxwell/kinematics/conservation.py` |
| 302 | Solution of the equation | `maxwell/physics/anisotropy.py` |
| 303 | Theory of the coefficient T | `maxwell/physics/rotatory.py` |
| 304 | Generalized form of Thomson's theorem | `maxwell/solvers/variational_3d.py` |
| 305 | Proof without symbols | `maxwell/solvers/variational_3d.py` |
| 306 | Lord Rayleigh's method applied to a wire of variable section | `maxwell/solvers/rayleigh.py` |
| 307 | Higher limit | `maxwell/solvers/rayleigh.py` |
| 308 | Lower limit for the correction for the ends of the wire | `maxwell/solvers/rayleigh.py` |
| 309 | Higher limit | `maxwell/solvers/rayleigh.py` |
| 310 | Surface-conditions | `maxwell/materials/composites.py` |
| 311 | Spherical surface | `maxwell/materials/composites.py` |
| 312 | Spherical shell | `maxwell/materials/composites.py` |
| 313 | Spherical shell placed in a field of uniform flow | `maxwell/materials/composites.py` |
| 314 | Medium in which small spheres are uniformly disseminated | `maxwell/materials/composites.py` |
| 315 | Images in a plane surface | `maxwell/materials/composites.py` |
| 316 | Method of inversion not applicable in three dimensions | `maxwell/materials/composites.py` |
| 317 | Case of conduction through a stratum bounded by parallel planes | `maxwell/materials/stratified.py` |
| 318 | Infinite series of images. Application to magnetic induction | `maxwell/materials/composites.py` |
| 319 | On stratified conductors | `maxwell/materials/stratified.py` |
| 320 | If neither substance has the rotatory property, the compound conductor is free from it | `maxwell/materials/stratified.py` |
| 321 | If the substances are isotropic, the direction of greatest resistance is normal to the strata | `maxwell/materials/stratified.py` |
| 322 | Medium containing parallelepipeds of another medium | `maxwell/materials/composites.py` |
| 323 | The rotatory property cannot be introduced by means of conducting channels | `maxwell/materials/stratified.py` |
| 324 | Construction of an artificial solid having given coefficients of conductivity | `maxwell/materials/stratified.py` |
| 325 | In a strictly homogeneous medium there can be no internal charge | `maxwell/materials/leakage.py` |
| 326 | Theory of a condenser in which the dielectric is not a perfect insulator | `maxwell/materials/leakage.py` |
| 327 | No residual charge due to simple conduction | `maxwell/materials/leakage.py` |
| 328 | Theory of a composite accumulator | `maxwell/physics/hysteresis.py` |
| 329 | Residual charge and electrical absorption | `maxwell/physics/hysteresis.py` |
| 330 | Total discharge | `maxwell/physics/hysteresis.py` |
| 331 | Comparison with the conduction of heat | `maxwell/physics/analogies.py` |
| 332 | Theory of telegraph cables | `maxwell/telecom/cables.py` |
| 333 | Opinion of Ohm on this subject | `maxwell/telecom/cables.py` |
| 334 | Mechanical illustration of the properties of a dielectric | `maxwell/physics/analogies.py` |
| 335 | Advantage of using material standards of resistance | `maxwell/instruments/standards.py` |
| 336 | Different standards which have been used | `maxwell/instruments/standards.py` |
| 337 | The electromagnetic system of units | `maxwell/core/units.py` |
| 338 | Weber's unit, and the British Association unit or Ohm | `maxwell/instruments/standards.py` |
| 339 | Professed value of the Ohm 10,000,000 metres per second | `maxwell/instruments/standards.py` |
| 340 | Reproduction of standards | `maxwell/instruments/standards.py` |
| 341 | Forms of resistance coils | `maxwell/components/coils.py` |
| 342 | Coils of great resistance | `maxwell/components/coils.py` |
| 343 | Arrangement of coils in series | `maxwell/components/coils.py` |
| 344 | Arrangement in multiple arc | `maxwell/components/coils.py` |
| 345 | On the comparison of resistances. (1) Ohm's method | `maxwell/instruments/bridges.py` |
| 346 | (2) By the differential galvanometer | `maxwell/instruments/bridges.py` |
| 347 | (3) By Wheatstone's Bridge | `maxwell/instruments/bridges.py` |
| 348 | Estimation of limits of error in the determination | `maxwell/instruments/bridges.py` |
| 349 | Best arrangement of the conductors to be compared | `maxwell/instruments/bridges.py` |
| 350 | On the use of Wheatstone's Bridge | `maxwell/instruments/bridges.py` |
| 351 | Thomson's method for small resistances | `maxwell/instruments/low_resistance.py` |
| 352 | Matthiessen and Hockin's method for small resistances | `maxwell/instruments/low_resistance.py` |
| 353 | Comparison of great resistances by the electrometer | `maxwell/instruments/high_resistance.py` |
| 354 | By accumulation in a condenser | `maxwell/instruments/high_resistance.py` |
| 355 | Direct electrostatic method | `maxwell/instruments/high_resistance.py` |
| 356 | Thomson's method for the resistance of a galvanometer | `maxwell/instruments/internal_resistance.py` |
| 357 | Mance's method of determining the resistance of a battery | `maxwell/instruments/internal_resistance.py` |
| 358 | Comparison of electromotive forces | `maxwell/instruments/bridges.py` |
| 359 | Metals, electrolytes, and dielectrics | `maxwell/materials/database/__init__.py` |
| 360 | Resistance of metals | `maxwell/materials/database/metals.py` |
| 361 | Resistance of mercury | `maxwell/materials/database/metals.py` |
| 362 | Table of resistance of metals | `maxwell/materials/database/metals.py` |
| 363 | Resistance of electrolytes | `maxwell/materials/database/liquids.py` |
| 364 | Experiments of Paalzow | `maxwell/materials/database/liquids.py` |
| 365 | Experiments of Kohlrausch and Nippoldt | `maxwell/materials/database/liquids.py` |
| 366 | Resistance of dielectrics | `maxwell/materials/database/insulators.py` |
| 367 | Gutta-percha | `maxwell/materials/database/insulators.py` |
| 368 | Glass | `maxwell/materials/database/insulators.py` |
| 369 | Gases | `maxwell/materials/database/gases.py` |
| 370 | Experiments of Wiedemann and Ruhlmann | `maxwell/materials/database/gases.py` |

**Total: 141 articles (230–370), all mapped.**

---

## **Implementation Priority Matrix**

### Phase 1: Foundation (P0 — Critical)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 13 | P0 | `current.py`, `sources.py` | Fundamental: defines what current IS |
| 14 | P0 | `ohm.py`, `joule.py` | Ohm's law and Joule heating are universal dependencies |
| 19 | P0 | `topology.py`, `network.py` | Circuit network theory is prerequisite for all measurement |
| 20 | P0 | `vectors.py`, `continuity.py` | 3D current flow is the mathematical foundation |

### Phase 2: Core Physics (P1 — High)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 15 | P1 | `contact.py`, `electrolytes.py`, `gravity.py` | Interface physics needed for batteries |
| 16 | P1 | `thermoelectric.py`, `inversion.py` | Complete thermoelectric suite (Seebeck/Peltier/Thomson) |
| 17 | P1 | `stoichiometry.py`, `energetics.py` | Faraday's laws for electrochemistry |
| 18 | P1 | `polarization.py`, `dissipation.py`, `batteries.py` | Battery and electrode models |
| 25 | P1 | `standards.py`, `coils.py` | Metrology foundation for measurement |
| 26 | P1 | `bridges.py`, `low_resistance.py`, `high_resistance.py`, `internal_resistance.py` | All measurement bridge algorithms |

### Phase 3: Advanced Materials (P2 — Medium)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 21 | P2 | `anisotropy.py`, `rotatory.py` | Tensor conduction for crystalline materials |
| 22 | P2 | `variational_3d.py`, `rayleigh.py` | Approximation methods for irregular geometries |
| 23 | P2 | `composites.py`, `stratified.py` | Heterogeneous and layered materials |
| 24 | P2 | `leakage.py`, `hysteresis.py`, `analogies.py`, `cables.py` | Dielectric memory and transmission lines |

### Phase 4: Empirical Data (P3 — Low)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 27 | P3 | `database/metals.py`, `database/liquids.py`, `database/insulators.py`, `database/gases.py` | Material property tables — data-heavy but low algorithmic complexity |

### Phase 5: Integration (P4 — Verification)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 28 | P4 | `units/converter.py`, `verify_network.py` | Unit conversion bridges and network theorem verification |

---

## **Validation Checklist**

- [ ] All 141 articles (230–370) have a unique module mapping
- [ ] Each of the 12 chapters is represented by at least one layer
- [ ] No article is mapped to multiple modules (1:1 mapping)
- [ ] All 18 layers (13–30) have per-article granularity
- [ ] Cross-part dependencies to Part I (Layers 0–12) are documented
- [ ] Cross-part dependencies to Part III (Layers 30b–42) are documented
- [ ] Package directory tree is consistent with module paths
- [ ] Thermoelectric effects (Seebeck, Peltier, Thomson) are all distinct
- [ ] All measurement bridge methods (Wheatstone, Thomson, Mance) have separate implementations
- [ ] Material database covers all 4 categories (metals, liquids, insulators, gases)
- [ ] Dielectric absorption ("soakage") is modeled separately from simple leakage
- [ ] 3D flow continuity equation (∇·J + ∂ρ/∂t = 0) is explicitly implemented
- [ ] Rayleigh approximation bounds (upper + lower) are both implemented

---

## **Version History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-11 | Initial COMPLETE architecture map. 141 articles, 18 layers, 50+ modules, 10 packages. Per-article granularity for all 12 chapters. |
