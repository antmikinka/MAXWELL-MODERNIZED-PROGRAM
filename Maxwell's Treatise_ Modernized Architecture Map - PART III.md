# **Maxwell's Treatise: Modernized Architecture Map**

## **Part III: Magnetism**

This document tracks the explicit mapping of Maxwell's Chapters (Source) to Python Modules (Destination) for the study of Magnetic Fields.

### **Layer 30b: Magnetic Units & Dimensions (The "Pole Strength")**

Goal: Establish the fundamental dimensional constraints for Magnetism (Unit Pole), distinct from Electrostatics.  
Source: Chapter I (Elementary Theory)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 374** | maxwell/magnetism/core/units.py | class MagneticDimensions Defines the "Unit Pole" ($m$) such that $f \= m\_1 m\_2 / r^2$. Dimensions: $\[L^{3/2} M^{1/2} T^{-1}\]$. | **374:** Magnetic Units |

### **Layer 31: The Magnetic Primitives (The "Dipole")**

Goal: Define the fundamental unit of magnetism. Unlike electricity, there are no "monopoles" (Art. 377); the atomic unit is the Dipole (Vector).  
Source: Chapter I (Elementary Theory of Magnetism)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 371–376** | maxwell/magnetism/core/magnet.py | class Magnet, class MagneticAxis Defines the axis, polarity, and response to external fields (Earth). | **371:** Properties of a Magnet **372:** Axis of the Magnet |
| **Arts. 377–380** | maxwell/magnetism/core/matter.py | class MagneticMatter Abstraction that treats N/S poles as "fictitious charges" for calculation purposes only. | **377:** Equality of Kinds **379:** Particle Theory |
| **Arts. 381–384** | maxwell/magnetism/core/moment.py | class MagneticMoment Defines Magnetization as a Vector quantity ($I$ or $M$). | **381:** Magnetization as Vector **384:** Magnetic Moment |

### **Layer 32: Dipole Interactions (The "Force")**

Goal: Calculate the potential and force exerted by magnets on each other.  
Source: Chapter I (Elementary Theory of Magnetism)

| Source Range | Modern Module Path | Function / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 385–386** | maxwell/magnetism/physics/potentials.py | calc\_scalar\_mag\_potential() Calculates potential ($\\Omega$) assuming the "Magnetic Matter" model. | **386:** Potential of Finite Magnet |
| **Arts. 387–390** | maxwell/magnetism/physics/coupling.py | calc\_dipole\_interaction() The energy/torque between two particles: $E \= \-\\vec{m} \\cdot \\vec{B}$. | **387:** Particle on Particle **389:** Potential Energy |
| **Arts. 391–392** | maxwell/math/spherical/magnetic.py | expand\_magnetic\_harmonics() *Dependency:* Extends Layer 8 (Part I) to solve magnetic fields using Spherical Harmonics. | **391:** Expansion of Potential **392:** Secondary Axes |

### **Layer 33: Coordinate Conventions (The "Compass")**

Goal: Strict enforcement of North/South terminology to prevent sign errors, codified in Maxwell's specific definitions.  
Source: Chapter I (Elementary Theory \- Terminology)

| Source Range | Modern Module Path | Class / Config | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 393–394** | maxwell/config/conventions.py | class PolarityConvention Enforces "Austral" (Southern Earth Pole) \= Positive, "Boreal" \= Negative. | **393:** Austral vs Boreal **394:** Direction of Force |

### **Layer 34: The Three Vectors: B, H, I (The "Definitions")**

Goal: Distinguishing the Total Field ($B$) from the Applied Field ($H$) and the Material Field ($I$).  
Source: Chapter II (Magnetic Force and Magnetic Induction)

| Source Range | Modern Module Path | Class / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 395–398** | maxwell/magnetism/fields/force.py | class MagneticForce ($H$) Defined by measuring force inside a "Cylindrical Cavity". | **396:** Cylindric Cavity **398:** Elongated Cylinder |
| **Art. 399** | maxwell/magnetism/fields/induction.py | class MagneticInduction ($B$) Defined by measuring force inside a "Thin Disk" (Flux Density). | **399:** A Thin Disk |
| **Art. 400** | maxwell/magnetism/fields/constitutive.py | calc\_constitutive\_relation() The master equation: $B \= H \+ 4\\pi I$. | **400:** Relation between B, H, I |

### **Layer 35: The Vector Potential (The "Curl")**

Goal: Moving from scalar potentials ($\\Omega$) to the Vector Potential ($A$), the primary tool for Electromagnetism.  
Source: Chapter II (Magnetic Force and Magnetic Induction)

| Source Range | Modern Module Path | Function / Calculus | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 401–402** | maxwell/magnetism/calculus/integrals.py | calc\_line\_integral(), calc\_surface\_flux() Implements Gauss's Law for Magnetism ($\\nabla \\cdot B \= 0$). | **401:** Line Integral **402:** Surface Integral |
| **Arts. 403–404** | maxwell/magnetism/fields/solenoidal.py | enforce\_solenoidal\_condition() Ensures magnetic lines form closed loops (Tubes of Induction). | **403:** Solenoidal Distribution **404:** Surfaces/Tubes |
| **Arts. 405–406** | maxwell/magnetism/calculus/vector\_potential.py | calc\_vector\_potential() Defines $A$ such that $B \= \\nabla \\times A$. | **405:** Vector-Potential **406:** Relation to Scalar |

### **Layer 36: Magnetic Geometry & Potentials (The "Shell")**

Goal: Using geometric constructs (Solid Angles) to calculate potentials of complex shapes without brute-force integration.  
Source: Chapter III (Magnetic Solenoids and Shells)

| Source Range | Modern Module Path | Class / Math | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 407–408** | maxwell/magnetism/geometry/solenoids.py | class Solenoid, class ComplexSolenoid Models tubular distributions of magnetism. | **407:** Definition of Solenoid **408:** Complex Solenoid |
| **Arts. 409–411** | maxwell/math/geometry/solid\_angle.py | calc\_solid\_angle() Calculates Potential as $\\Omega \= \\Phi \\times \\omega$ (Strength $\\times$ Solid Angle). | **409:** Potential of Shell **411:** Discontinuity at Surface |
| **Arts. 412–416** | maxwell/magnetism/fields/decomposition.py | decompose\_vector\_field() Separates fields into "Lamellar" (Gradient) and "Solenoidal" (Curl) components. | **412:** Lamellar Distribution **416:** Vector-Potential of Shell |
| **Arts. 417–422** | maxwell/magnetism/calculus/cyclic.py | calc\_cyclic\_potential() Handles multi-valued potentials (Cyclic Functions) essential for current loops. | **421:** Cyclic Function **422:** Vector-Potential of Curve |

### **Layer 37: Material Response & Induction (The "Susceptibility")**

Goal: Modeling how neutral matter becomes magnetized under external influence (Induced Magnetism).  
Source: Chapter IV (Induced Magnetization)

| Source Range | Modern Module Path | Class / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 424–426** | maxwell/magnetism/materials/induction.py | class InducedMagnetization Defines the coefficient $\\kappa$ (kappa) where $I \= \\kappa H$. | **424:** Definition of Induction **426:** Coefficient $\\kappa$ |
| **Arts. 427–428** | maxwell/magnetism/solvers/induction\_solvers.py | method\_poisson(), method\_faraday() Two competing algorithms for solving induced fields (Volume Integral vs Field Lines). | **427:** Poisson's Method **428:** Faraday's Method |
| **Art. 430** | maxwell/magnetism/physics/molecular\_theory.py | simulate\_molecular\_alignment() Poisson’s physical theory: re-orienting internal dipoles. | **430:** Physical Theory |

### **Layer 38: Analytical Geometries (The "Ellipsoid")**

Goal: Exact analytical solutions for specific shapes, used to benchmark numerical solvers and model shielding.  
Source: Chapter V (Particular Problems in Magnetic Induction)

| Source Range | Modern Module Path | Class / Component | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 431–433** | maxwell/magnetism/components/spheres.py | class HollowSphere Calculates magnetic shielding factors for hollow shells (permeability contrast). | **431:** Hollow Spherical Shell **432:** Large $\\kappa$ Case |
| **Arts. 437–438** | maxwell/magnetism/components/ellipsoids.py | class MagnetizedEllipsoid The only shape with a uniform internal field; base class for needles and disks. | **437:** Theory of Ellipsoid **438:** Flat/Long Ellipsoids |
| **Art. 441** | maxwell/magnetism/engineering/naval.py | class ShipMagnetism Practical application: Modeling the permanent and induced magnetism of iron ships. | **441:** On Ship's Magnetism |

### **Layer 39: Nonlinear Material Physics (The "Hysteresis")**

Goal: Moving beyond linear susceptibility ($\\mu$) to model Saturation, Retentivity, and Magnetostriction.  
Source: Chapter VI (Weber's Theory of Induced Magnetism)

| Source Range | Modern Module Path | Class / Model | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 442–443** | maxwell/magnetism/materials/saturation.py | class WeberModel Models the upper limit of magnetization (Saturation) as dipoles align fully. | **442:** Maximum Magnetization **443:** Weber's Theory |
| **Arts. 444–446** | maxwell/magnetism/materials/hysteresis.py | class HysteresisLoop Models memory effects: Residual Magnetization and Coercivity (History Dependence). | **444:** Residual Magnetization **446:** Demagnetization cycles |
| **Art. 447** | maxwell/magnetism/physics/magnetostriction.py | calc\_joule\_expansion() Calculates physical dimensional changes (strain) caused by magnetic fields. | **447:** Effects on Dimensions **448:** Experiments of Joule |

### **Layer 40: Magnetic Metrology (The "Magnetometer")**

Goal: Precise instrumentation to measure intensity, declination, and dip using torsion and vibration.  
Source: Chapter VII (Magnetic Measurements)

| Source Range | Modern Module Path | Class / Instrument | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 449–452** | maxwell/magnetism/instruments/suspension.py | class UnifilarSuspension, class OpticalLever Mechanics of suspending magnets; Mirror/Scale readout logic. | **449:** Suspension **450:** Mirror and Scale |
| **Arts. 453–455** | maxwell/magnetism/instruments/magnetometer.py | method\_deflection() Calculates force by observing the deflection of a suspended needle (Tangent/Sine methods). | **453:** Measurement of Moment **455:** Method of Tangents |
| **Arts. 456–459** | maxwell/magnetism/instruments/dynamics.py | method\_vibration(), class BifilarSuspension Determines force by timing the oscillation period of a magnet. | **456:** Observation of Vibrations **459:** Bifilar Suspension |
| **Arts. 461–464** | maxwell/magnetism/instruments/dip\_circle.py | class DipCircle, class BalanceMagnetometer Measuring the vertical component of Earth's field. | **461:** Dip-Circle **464:** Balance Vertical Force |

### **Layer 41: Planetary Magnetism (The "Geodynamo")**

Goal: Modeling the Earth's global magnetic field using Spherical Harmonic expansions.  
Source: Chapter VIII (On Terrestrial Magnetism)

| Source Range | Modern Module Path | Class / Model | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 465–466** | maxwell/magnetism/geophysics/survey.py | class MagneticSurvey Aggregates local measurements (Dip, Declination, Intensity) into a global dataset. | **465:** Elements of Force **466:** Combination of Results |
| **Arts. 467–470** | maxwell/magnetism/geophysics/gauss\_model.py | class GaussExpansion The 24-coefficient spherical harmonic model of Earth's potential. | **467:** Expansion of Potential **469:** Gauss' Calculation |
| **Arts. 471–473** | maxwell/magnetism/geophysics/variations.py | class MagneticWeather Simulating temporal shifts: Solar/Lunar variations and the 11-year sunspot cycle. | **471:** Solar/Lunar Variations **473:** 11-Year Period |

### **Layer 42: Magnetic Mechanics & Work (The "Motor" Principle)**

Goal: Calculating the potential energy and mechanical work done by magnetic fields on shells and particles.  
Source: Chapter I & III (Energy)

| Source Range | Modern Module Path | Function / Physics | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 389** | maxwell/magnetism/mechanics/potential\_energy.py | calc\_dipole\_potential\_energy() Calculates work done when a magnet moves in a field: $W \= \-\\Delta(\\vec{m} \\cdot \\vec{B})$. | **389:** Potential Energy of Magnet |
| **Art. 423** | maxwell/magnetism/mechanics/shell\_energy.py | calc\_shell\_work() Calculates the mechanical potential of a magnetic shell (current loop) in a field. Basis of Electromagnetism. | **423:** Potential Energy of Shell |

### **Appendix A: Architectural Differentiators (Restoring Lost Physics)**

**Goal:** Highlight specific Maxwellian concepts in Magnetism that provide superior geometric intuition or computational efficiency compared to standard brute-force methods.

| Concept | Source Article | Modern Gap | Implementation Value |
| :---- | :---- | :---- | :---- |
| **The "Solid Angle" Method** | **Art. 409** (Part III, Ch III) | Modern physics relies on Biot-Savart integration. Maxwell used **Topology** (Solid Angles). | Enables instant calculation of potentials for complex coil shapes; computationally superior for Mutual Inductance. |
| **Geometric Definition of B & H** | **Art. 396–400** (Part III, Ch II) | Modern physics defines $B/H$ algebraically. Maxwell defined them via **Cavity Shapes** (Disk vs Cylinder). | Provides a physical "Virtual Probe" model for simulating fields inside hard magnetic materials. |
| **Weber's Molecular Friction** | **Art. 443** (Part III, Ch VI) | Modern engineering uses empirical curve-fitting for Hysteresis. Weber provided a **Mechanistic** theory. | Simulates the actual thermodynamics of magnetic loss (heating) and saturation limits based on molecular alignment. |

