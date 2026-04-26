# **Maxwell's Treatise: Modernized Architecture Map**

## **Part I: Electrostatics**

This document tracks the explicit mapping of Maxwell's Chapters (Source) to Python Modules (Destination).

### **Layer 0: Units & Dimensions (The "Constants")**

Goal: Establish the fundamental physical constraints and dimensional consistency (L, M, T).  
Source: Chapter I (Preliminary Articles)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 41–42** | maxwell/core/units.py | class Dimensions, class ElectrostaticUnit Enforces dimensional analysis (e.g., $\[Q\] \= \[L^{3/2} M^{1/2} T^{-1}\]$). | **41:** Electrostatic Unit **42:** Dimensions |
| **Arts. 36–37** | maxwell/config.py | TheoryConfig Toggles between One-Fluid and Two-Fluid calculation modes (legacy support). | **36:** Two Fluids **37:** One Fluid |

### **Layer 1: The Core Primitives (The "Nouns")**

Goal: Define the fundamental objects that exist in the simulation.  
Source: Chapter I (Description of Phenomena)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 27–35** | maxwell/core/charge.py | class ElectrifiedBody Handles charge quantity, polarity (+/-), and basic attributes. | **27:** Polarity **29:** Conductors vs Insulators **34:** Charge as Quantity |
| **Arts. 44–48** | maxwell/core/fields.py | class VectorField, class Displacement Defines the grid ($E$) and Electric Displacement ($D$). | **44:** Electric Field def **60:** Electric Displacement |
| **Arts. 50–57** | maxwell/core/materials.py | class Dielectric, class BreakdownModel Properties of matter and failure modes (Sparks, Glow). | **52:** Specific Inductive Capacity **55:** Disruptive Discharge (Spark) |

### **Layer 2: The Basic Physics Engine (The "Verbs")**

Goal: Define the fundamental rules of how objects interact in isolation.  
Source: Chapter II (Elementary Mathematical Theory)

| Source Range | Modern Module Path | Function / Logic | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 63–68** | maxwell/physics/forces.py | calc\_coulomb\_force() Calculates force vectors between two static bodies. | **66:** Law of Force (Inverse Square) **68:** Resultant Intensity |
| **Arts. 69–73** | maxwell/physics/potential.py | calc\_potential\_at\_point() Calculates scalar potential ($V$) relative to a charge distribution. | **70:** Electric Potential **72:** Potential of a Conductor |
| **Arts. 77–83** | maxwell/physics/poisson.py | apply\_poisson\_equation() Basic mathematical relations between density and potential. | **77:** Poisson/Laplace Equation |

### **Layer 3: The System Manager (The "Network")**

Goal: Manage complex groups of interacting conductors using Linear Algebra.  
Source: Chapter III (Systems of Conductors)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 84–86** | maxwell/systems/energy.py | class SystemState Calculates total energy of a multi-body system. | **84:** Superposition **85:** Work & Energy |
| **Arts. 87–94** | maxwell/systems/matrices.py | build\_capacity\_matrix(), build\_induction\_matrix() Generates the linear algebra coefficients for system solving. | **87:** Coefficients of Potential **93:** Mechanical Force on System |

### **Layer 4: The Advanced Solvers (The "Kernel")**

Goal: Provide abstract mathematical theorems to solve boundary value problems.  
Source: Chapter IV (General Theorems)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 96–99** | maxwell/solvers/greens.py | apply\_greens\_theorem() Solves potential when given boundary conditions on a surface. | **96:** Green's Theorem **98:** Green's Function |
| **Arts. 100–102** | maxwell/solvers/variational.py | optimize\_thomson() Finds energy minimums for unique distributions. | **100:** Thomson's Theorem **101:** Heterogeneous Media |

### **Layer 5: Field Analysis & Diagnostics (The "Stress Test")**

Goal: Analyze the properties of the medium (space) itself.  
Source: Chapters V & VI (Mechanical Action & Equilibrium)

| Source Range | Modern Module Path | Function / Tool | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 103–111** | maxwell/analysis/stress.py | calc\_maxwell\_stress\_tensor() Calculates tension/pressure at every point in the field. | **105:** Stress in the Medium **109:** Faraday's Lines of Force |
| **Arts. 112–116** | maxwell/analysis/stability.py | find\_equilibrium\_points(), check\_earnshaw\_stability() Locates saddle points and unstable equilibria. | **112:** Points of Equilibrium **116:** Instability of Static Systems |

### **Layer 6: Visualization Engine (The "Renderer")**

Goal: Generate visual representations of fields, potentials, and flow lines.  
Source: Chapter VII (Forms of Equipotential Surfaces and Lines of Flow)

| Source Range | Modern Module Path | Function / Tool | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 117–121** | maxwell/vis/contours.py | plot\_equipotentials() Draws surfaces of constant potential for standard point ratios (e.g., 4:1). | **118:** Two points (4:1) **121:** Three points |
| **Arts. 122–123** | maxwell/vis/field\_lines.py | trace\_lines\_of\_force() Algorithmic generation of field lines orthogonal to equipotentials. | **122:** Faraday's Lines **123:** Method of Drawing |

### **Layer 7: Standard Component Library (The "Prefabs")**

Goal: A library of pre-calculated geometric shapes commonly used in engineering.  
Source: Chapter VIII (Simple Cases of Electrification)

| Source Range | Modern Module Path | Class / Component | Key Articles |
| :---- | :---- | :---- | :---- |
| **Art. 124** | maxwell/components/plates.py | class ParallelPlate Idealized infinite planes (basis for capacitors). | **124:** Two Parallel Planes |
| **Art. 125** | maxwell/components/spheres.py | class ConcentricSphere Spherical capacitor geometry. | **125:** Concentric Spherical Surfaces |
| **Art. 126–127** | maxwell/components/cylinders.py | class CoaxialCable Cylindric surfaces and longitudinal force calculations. | **126:** Coaxial Cylindric Surfaces |

### **Layer 8: Specialized Math Kernel (The "Harmonics" & "Coordinates")**

Goal: Advanced mathematical basis functions for solving spherical and ellipsoidal boundary problems.  
Source: Chapter IX (Spherical Harmonics) & Chapter X (Confocal Surfaces)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 128–146** | maxwell/math/spherical/ | calc\_surface\_harmonic() Spherical Harmonics ($Y\_n, H\_n$) logic. | **135:** Zonal Harmonics **144:** Sphere in Field |
| **Arts. 147–150** | maxwell/math/ellipsoidal/coordinates.py | transform\_ellipsoidal() Coordinate transformations for $\\alpha, \\beta, \\gamma$. | **148:** Characteristic Equation **150:** Confocal Surfaces |
| **Arts. 151–154** | maxwell/math/ellipsoidal/shapes.py | solve\_paraboloids() Solutions for cones, spheres, and paraboloids. | **153:** Cones and Spheres **154:** Confocal Paraboloids |

### **Layer 9: Geometric Solvers (The "Reflector")**

Goal: Solvers that use geometric inversion and reflection to solve complex boundaries without heavy calculus.  
Source: Chapter XI (Theory of Electric Images)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 155–161** | maxwell/solvers/images/core.py | apply\_method\_of\_images() Places "virtual" charges to satisfy zero-potential boundaries. | **155:** Thomson's Method **156:** Point & Sphere |
| **Arts. 162–165** | maxwell/math/transformations/inversion.py | geometric\_inversion() Transforms a problem space inside-out ($r' \= R^2/r$). | **162:** Electric Inversion **163:** Geometrical Theorems |
| **Arts. 166–172** | maxwell/solvers/images/spheres.py | solve\_intersecting\_spheres() Recursive image generation for spheres at angles $\\pi/n$. | **166:** Spheres at Angle **171:** Concentric Spheres |

### **Layer 10: 2D Complex Analysis Engine (The "Conjugate")**

Goal: Solves 2D problems using Complex Variables ($z \= x \+ iy$) to handle edges, grooves, and gratings.  
Source: Chapter XII (Conjugate Functions)

| Source Range | Modern Module Path | Function / Algorithm | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 182–190** | maxwell/math/complex/conjugate.py | solve\_conjugate\_functions() Uses analytic functions to solve Laplace's equation in 2D. | **183:** Conjugate Functions **186:** Transform of Poisson |
| **Arts. 191–195** | maxwell/solvers/edges.py | calc\_edge\_distribution() Solves density spikes at sharp edges of conductors. | **191:** Electricity near Edge |
| **Arts. 196–206** | maxwell/components/gratings.py | simulate\_grating(), simulate\_guard\_ring() Models for grooved surfaces and wire gratings. | **201:** Thomson's Guard Ring **203:** Grating of Wires |

### **Layer 11: Instrumentation & Metrology (The "Lab Bench")**

Goal: Virtual instruments (Sources and Sensors) to interact with the simulation like a physical experiment.  
Source: Chapter XIII (Electrostatic Instruments)

| Source Range | Modern Module Path | Class / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Arts. 207–213** | maxwell/instruments/generators.py | class HoltzMachine, class WaterDropper Dynamic sources of continuous electrification (Charge Pumps). | **211:** Thomson's Water-Dropper **212:** Holtz's Machine |
| **Arts. 214–225** | maxwell/instruments/meters.py | class QuadrantElectrometer, class ProofPlane "Virtual Sensors" that integrate field values to mimic real measurements. | **215:** Coulomb's Torsion Balance **219:** Quadrant Electrometer |
| **Arts. 226–229** | maxwell/instruments/standards.py | class LeydenJar, class GuardRingCapacitor Precision reference accumulators for calibration. | **226:** Leyden Jar **228:** Guard-ring Accumulator |

### **Layer 12: Verification & Test Suite (The "Appendices")**

Goal: Ensure mathematical accuracy using Maxwell's specific appendices and tables.  
Source: Appendices to Chap. II and XI

| Source Range | Modern Module Path | Script / Responsibility | Key Articles |
| :---- | :---- | :---- | :---- |
| **Appendix Chap II** | tests/verification/verify\_poisson.py | test\_poisson\_integrity() Verifies the Laplace extension logic against Maxwell's notes. | **App II:** Page 101 |
| **Appendix Chap XI** | tests/verification/verify\_images.py | test\_image\_sphere\_limit() Verifies that infinite series of images converge correctly. | **App XI:** Page 281 |

