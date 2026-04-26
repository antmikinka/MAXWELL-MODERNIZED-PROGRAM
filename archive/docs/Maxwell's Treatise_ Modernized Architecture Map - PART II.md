# **Maxwell's Treatise: Modernized Architecture Map**

## **Part II: Electrokinematics**

This document tracks the explicit mapping of Maxwell's Chapters (Source) to Python Modules (Destination) for the study of Electric Current.

### **Layer 13: The Kinetic Primitives (The "Flow")**

Goal: Define the movement of electricity (Current) and the driving forces (EMF) that create it.  
Source: Chapter I (The Electric Current)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 230–231** | maxwell/kinematics/current.py | class ElectricCurrent Defines $I \= dQ/dt$. Handles transient vs. steady states. | **230:** Current from Discharge **231:** Transference of Electrification |
| **Arts. 232–234** | maxwell/kinematics/sources.py | class VoltaicBattery, class EMF Abstract base class for any device generating continuous potential difference. | **232:** Voltaic Battery **233:** Electromotive Force |
| **Arts. 239–240** | maxwell/magnetics/coupling.py | class GalvanometerInterface The bridge between electricity and magnetism (Deflection logic). | **240:** The Galvanometer |

### **Layer 14: The Electrochemical Engine (The "Ions")**

Goal: Model the chemical decomposition and material transport caused by current.  
Source: Chapter I (The Electric Current \- Electrolysis)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 236–237** | maxwell/chemistry/electrolysis.py | class Electrolyte, class Ion Models Anodes, Cathodes, Anions, and Cations. | **236:** Electrolytic Action **237:** Terms (Anode/Cathode) |
| **Arts. 238** | maxwell/chemistry/transport.py | calc\_ion\_migration() Logic for how current passes through liquids vs solids. | **238:** Modes of Passage |

### **Layer 15: Resistive Physics & Thermodynamics (The "Heat")**

Goal: Implement the fundamental laws of resistance and energy dissipation (Ohm & Joule).  
Source: Chapter II (Conduction and Resistance)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 241** | maxwell/physics/ohm.py | solve\_ohm\_law() The fundamental solver: $V \= IR$ (or $C \= E/R$ in Maxwell's notation). | **241:** Ohm's Law |
| **Art. 242** | maxwell/thermodynamics/joule.py | calc\_joule\_heating() Calculates thermal energy generation: $H \= I^2 R t$. | **242:** Generation of Heat |
| **Arts. 243–244** | maxwell/thermodynamics/analogy.py | thermal\_conduction\_model() Uses heat diffusion equations to model electrical distribution in solids. | **243:** Heat Analogy |

### **Layer 16: Interface Physics (The "Junctions")**

Goal: Model the specific potentials arising where two different materials touch.  
Source: Chapter III (Electromotive Force between Bodies in Contact)

| Source Range | Modern Module Path | Function / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 246** | maxwell/materials/contact.py | calc\_contact\_potential() Implementation of Volta's Law for metal-metal junctions. | **246:** Volta's Law of Contact |
| **Art. 247** | maxwell/materials/electrolytes.py | calc\_electrolyte\_interface() Logic for metal-liquid interfaces (battery chemistry). | **247:** Effect of Electrolytes |
| **Art. 248** | maxwell/kinematics/gravity.py | simulate\_gravity\_cell() Special case for Thomson's gravity-driven currents. | **248:** Thomson's Voltaic Current |

### **Layer 17: Thermoelectric Coupling (The "Gradient")**

Goal: Model the reversible conversion between heat and electricity (Seebeck/Peltier effects).  
Source: Chapter IV (Electrolysis \- Thermoelectric Section)

| Source Range | Modern Module Path | Function / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 249–254** | maxwell/thermodynamics/thermoelectric.py | calc\_peltier\_effect(), calc\_seebeck\_emf() Calculates heat absorption at junctions and current from heat gradients. | **249:** Peltier's Phenomenon **250:** Seebeck's Discovery **254:** Tait's Law |
| **Art. 252** | maxwell/thermodynamics/inversion.py | check\_thermoelectric\_inversion() Detects critical temperatures where current direction reverses (Cumming's discovery). | **252:** Thermoelectric Inversions |

### **Layer 18: Molecular Stoichiometry (The "Mole")**

Goal: Enforce conservation of mass/energy at the molecular level using Faraday's Laws.  
Source: Chapter IV (Electrolysis \- Molecular Section)

| Source Range | Modern Module Path | Function / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 255–259** | maxwell/chemistry/stoichiometry.py | calc\_electrochemical\_equivalent() Calculates mass transport based on charge: $m \= z Q$. | **255:** Faraday's Law **256:** Clausius's Molecular Agitation |
| **Arts. 260–263** | maxwell/chemistry/energetics.py | check\_energy\_conservation() Calculates Chemical Affinity as an EMF to ensure $\\sum E \= 0$. | **262:** Conservation of Energy **263:** Measurement of Affinity |

### **Layer 19: Polarization Dynamics (The "Back-EMF")**

Goal: Model the non-ideal behavior of batteries and electrodes (Internal Resistance & Reverse Voltage).  
Source: Chapter V (Electrolytic Polarization)

| Source Range | Modern Module Path | Class / Component | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 264–268** | maxwell/chemistry/polarization.py | class PolarizationState Models the accumulation of ions at electrodes creating a counter-force (Back EMF). | **266:** Polarization vs Resistance **267:** Ions at Electrodes |
| **Arts. 269–270** | maxwell/chemistry/dissipation.py | calc\_ion\_dissipation() Models the loss of charge over time (leakage/diffusion). | **269:** Dissipation of Ions **270:** Limit of Polarization |
| **Arts. 271–272** | maxwell/components/batteries.py | class DaniellCell, class SecondaryPile Implementations of constant vs. rechargeable cells. | **271:** Ritter's Secondary Pile **272:** Daniell's Cell |

### **Layer 20: Circuit Network Theory (The "Netlist")**

Goal: Solving complex networks of linear conductors (wires) using topological graph theory.  
Source: Chapter VI (Mathematical Theory of Distribution)

| Source Range | Modern Module Path | Class / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 273–277** | maxwell/circuits/topology.py | class CircuitGraph Handles series, parallel ("multiple arc"), and resistance calculations. | **275:** Conductors in Series **276:** Multiple Arc (Parallel) |
| **Arts. 280–282** | maxwell/circuits/network.py | solve\_linear\_system() Solves currents in arbitrary mesh networks; implements Conjugate Conductors. | **280:** Linear Systems **282:** Conjugate Conductors |
| **Arts. 283–284** | maxwell/thermodynamics/optimization.py | minimize\_heat\_generation() Proves Ohm's law is the condition for minimum energy waste (Principle of Least Action). | **284:** Heat is a Minimum |

### **Layer 21: 3D Flow Dynamics (The "Stream")**

Goal: Generalizing current as a continuous vector fluid flowing through 3D space, not just wires.  
Source: Chapter VII (Conduction in Three Dimensions)

| Source Range | Modern Module Path | Function / Concept | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 285–287** | maxwell/kinematics/vectors.py | calc\_current\_density() Defines the vector components ($u, v, w$) of flow per unit area. | **286:** Composition of Currents **287:** Flow through Surface |
| **Arts. 288–294** | maxwell/kinematics/streamfunctions.py | generate\_tubes\_of\_flow() Visualization logic for "Tubes of Flow" (Streamlines) and "Current Sheets". | **290:** Tubes of Flow **294:** Current Sheets |
| **Arts. 295–296** | maxwell/kinematics/conservation.py | check\_continuity\_equation() The master equation for flow: $\\nabla \\cdot J \+ \\frac{d\\rho}{dt} \= 0$. | **295:** Equation of Continuity |

### **Layer 22: Anisotropic Physics (The "Tensor")**

Goal: Handling materials where resistance differs by direction (e.g., crystals), using Tensors instead of scalars.  
Source: Chapter VIII (Resistance and Conductivity in 3D)

| Source Range | Modern Module Path | Class / Math | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 297–299** | maxwell/physics/anisotropy.py | class ConductivityTensor Solves $\[R\]$ where $V\_x \= R\_{xx}I\_x \+ R\_{xy}I\_y \+ ...$ | **297:** Equations of Resistance **299:** Rate of Heat Generation |
| **Art. 303** | maxwell/physics/rotatory.py | check\_rotatory\_coefficient() Checks for the existence of the theoretical $T$ coefficient (magnetic-like effects in conduction). | **303:** Theory of Coefficient T |

### **Layer 23: Approximation Solvers (The "Bounds")**

Goal: Using Rayleigh's Method to find upper and lower limits of resistance for irregular shapes.  
Source: Chapter VIII (Resistance and Conductivity in 3D)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 304** | maxwell/solvers/variational\_3d.py | apply\_thomson\_theorem\_generalized() Extension of minimum energy principles to 3D flow. | **304:** Generalized Thomson's Theorem |
| **Arts. 306–309** | maxwell/solvers/rayleigh.py | calc\_resistance\_bounds() Calculates the "Higher Limit" and "Lower Limit" of resistance for wires of variable section. | **306:** Lord Rayleigh's Method **308:** Correction for Ends |

### **Layer 24: Composite Materials (The "Mixture")**

Goal: Modeling heterogeneous media (Strata, spheres in suspension) to find effective bulk properties.  
Source: Chapter IX (Conduction through Heterogeneous Media)

| Source Range | Modern Module Path | Class / Model | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 310–314** | maxwell/materials/composites.py | calc\_effective\_conductivity() Models a medium with disseminated spheres (Early Maxwell-Garnett theory). | **312:** Spherical Shell **314:** Spheres Uniformly Disseminated |
| **Arts. 319–324** | maxwell/materials/stratified.py | class StratifiedConductor Creates artificial anisotropy by layering isotropic materials. | **319:** Stratified Conductors **321:** Direction of Greatest Resistance |

### **Layer 25: Dielectric Memory & Leakage (The "Soak")**

Goal: Modeling real-world imperfections where insulators leak current and "remember" past charges (Electrical Absorption).  
Source: Chapter X (Conduction in Dielectrics)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 325–327** | maxwell/materials/leakage.py | class LeakyDielectric Models conduction through imperfect insulators. | **326:** Theory of Condenser **327:** Residual Charge |
| **Arts. 328–330** | maxwell/physics/hysteresis.py | calc\_residual\_charge() Models the "soakage" effect where discharge is not instantaneous (Composite Accumulator). | **328:** Composite Accumulator **330:** Total Discharge |
| **Art. 334** | maxwell/physics/analogies.py | mechanical\_dielectric\_model() A mechanical spring-damper analogy for dielectric relaxation. | **334:** Mechanical Illustration |

### **Layer 26: Transmission Line Theory (The "Cable")**

Goal: The theory of signals traveling over long distances, using the analogy of heat diffusion.  
Source: Chapter X (Conduction in Dielectrics \- Cables)

| Source Range | Modern Module Path | Class / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 331–333** | maxwell/telecom/cables.py | solve\_telegraph\_equation() Solves the partial differential equation for signal decay over distance. | **331:** Comparison with Heat **332:** Theory of Telegraph Cables |

### **Layer 27: Metrology & Standards (The "Ohm")**

Goal: Defining the absolute physical units and the standard components used to represent them.  
Source: Chapter XI (Measurement of Electric Resistance)

| Source Range | Modern Module Path | Class / Standard | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 335–340** | maxwell/instruments/standards.py | class ResistanceStandard Defines the "BA Unit" (Ohm) based on velocity (10,000,000 m/s). | **338:** Weber's Unit (Ohm) **340:** Reproduction of Standards |
| **Arts. 341–344** | maxwell/components/coils.py | class ResistanceCoil Models physical resistor construction (Series/Parallel arrangements). | **341:** Forms of Coils **343:** Arrangement in Series |

### **Layer 28: Measurement Bridges (The "Balance")**

Goal: Algorithms for precise measurement using null-methods and bridge topologies.  
Source: Chapter XI (Measurement of Electric Resistance)

| Source Range | Modern Module Path | Class / Circuit | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 345–350** | maxwell/instruments/bridges.py | class WheatstoneBridge, class DifferentialGalvanometer Solves for unknown resistance $R\_x$ using balanced currents. | **347:** Wheatstone's Bridge **350:** Use of the Bridge |
| **Arts. 351–352** | maxwell/instruments/low\_resistance.py | method\_thomson\_bridge() Specialized algorithms for measuring very small resistances (Kelvin Bridge). | **351:** Thomson's Method **352:** Matthiessen & Hockin |
| **Arts. 353–355** | maxwell/instruments/high\_resistance.py | method\_electrometer\_decay() Measuring high resistance (Giga-Ohms) via capacitor discharge timing. | **353:** Comparison by Electrometer **354:** Accumulation in Condenser |
| **Arts. 356–357** | maxwell/instruments/internal\_resistance.py | method\_mance() Determining the internal resistance of the battery itself. | **356:** Galvanometer Resistance **357:** Mance's Method (Battery) |

### **Layer 29: Material Properties Database (The "Catalog")**

Goal: A database of empirical resistance values for specific substances (Metals, Liquids, Gases).  
Source: Chapter XII (Electric Resistance of Substances)

| Source Range | Modern Module Path | Class / Database | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 359–362** | maxwell/materials/database/metals.py | class ConductorDatabase Lookup tables for Silver, Copper, Mercury, etc., including temperature coefficients. | **360:** Resistance of Metals **362:** Table of Metals |
| **Arts. 363–365** | maxwell/materials/database/liquids.py | class ElectrolyteDatabase Resistance data for weak vs strong electrolytes (Paalzow, Kohlrausch). | **363:** Resistance of Electrolytes **365:** Kohlrausch & Nippoldt |
| **Arts. 366–368** | maxwell/materials/database/insulators.py | class DielectricDatabase High-resistance data for Gutta-percha, Glass, and Telegraph insulators. | **367:** Gutta-percha **368:** Glass |
| **Arts. 369–370** | maxwell/materials/database/gases.py | class GasDischargeModel Resistance properties of gases under varying pressures and temperatures. | **369:** Gases **370:** Wiedemann & Rühlmann |

### **Layer 30: System Integration & Verification (The "Bridge")**

Goal: Integration of unit systems (Statics to Kinematics) and rigorous verification of network theorems.  
Source: Chapter XI (Units) & Appendix to Chapter VI

| Source Range | Modern Module Path | Function / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 337** | maxwell/core/units/converter.py | class UnitSystemConverter Handles transformation between Electrostatic Units (Part I) and Electromagnetic Units (Part II). | **337:** Electromagnetic System |
| **App. Ch VI** | tests/verification/verify\_network.py | test\_min\_heat\_principle() Mathematical verification of the principle of least heat generation in networks. | **App VI:** Page 409 |

### **Appendix A: Architectural Differentiators (Restoring Lost Physics)**

**Goal:** Highlight specific Maxwellian concepts that are often simplified in modern tools but are preserved here for high-fidelity simulation.

| Concept | Source Article | Modern Gap | Implementation Value |
| :---- | :---- | :---- | :---- |
| **Dielectric Memory ("Soakage")** | **Art. 329** (Part II, Ch X) | Modern physics often treats capacitors as ideal ($Q=CV$). Maxwell models "stratified" memory layers. | Critical for simulating **Li-Ion battery recovery**, supercapacitor hysteresis, and precision analog timing circuits. |
| **Physical Vacuum Stress** | **Art. 105** (Part I, Ch V) | Modern physics uses abstract vector fields ($F=qE$). Maxwell treated the vacuum as a medium under **Tension** and **Pressure**. | Provides a more physical calculation of force (the "Rubber Band" effect) and aligns with **General Relativity** stress-tensors. |
| **Topological Tubes of Flow** | **Art. 290** (Part II, Ch VII) | Modern physics relies on local differential calculus ($\\nabla \\cdot J$). Maxwell used **Quantized Geometric Tubes**. | Aligns with modern **Topological Insulators** and Quantum Hall physics; ensures rigorous continuity in 3D visualizations. |

