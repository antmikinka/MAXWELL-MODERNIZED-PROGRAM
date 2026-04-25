# **Maxwell's Treatise: Modernized Architecture Map**

## **Part V: System Core & Infrastructure**

This document tracks the global shared resources, data structures, and simulation kernels required to unify Parts I–IV into a single executable library.

### **Layer 90: The Simulation Kernel (The "Ether")**

Goal: Defining the "Medium" in which all fields exist. Unlike modern "void" physics, Maxwell requires a medium that supports stress, tension, and energy density at every point.  
Responsibility: Manages the discretization of space (Mesh/Voxel/Function Space).

| Module Path | Class / Responsibility | Cross-Reference |
| :---- | :---- | :---- |
| maxwell/core/space/mesh.py | class EtherGrid A 3D voxel grid or mesh that stores field values ($\\mathfrak{E}, \\mathfrak{B}, \\mathfrak{A}$) at every coordinate. | **All Parts:** The container for all fields. |
| maxwell/core/space/medium.py | class MediumProperties A spatial map of constitutive properties ($\\mu, \\epsilon, \\sigma$) defining where "Matter" exists vs. "Vacuum." | **Part II (Ch IX):** Heterogeneous Media. |
| maxwell/core/space/boundary.py | class BoundaryManager Enforces edge conditions (Dirichlet/Neumann) at the limits of the simulation universe. | **Part I (Ch IV):** Green's Theorem. |

### **Layer 91: The Coordinate Engine (The "Transformer")**

**Goal:** Maxwell fluently switches between Cartesian, Spherical, and Ellipsoidal coordinates depending on the problem geometry. The system must handle these transformations globally.

| Module Path | Class / Responsibility | Cross-Reference |
| :---- | :---- | :---- |
| maxwell/math/coords/transform.py | class CoordinateSystem Base class for coordinate transforms (Jacobians, Metrics). | **Part III (Ch X):** Confocal Surfaces. |
| maxwell/math/coords/operators.py | class VectorOperators Implementation of $\\nabla$ (Grad, Div, Curl, Laplacian) specific to the active coordinate system. | **Part IV (Ch IX):** General Equations. |

### **Layer 92: The Time Integrator (The "Clock")**

**Goal:** Parts II and IV introduce time dynamics ($d/dt$). A central clock and integration strategy are needed to advance the simulation.

| Module Path | Class / Responsibility | Cross-Reference |
| :---- | :---- | :---- |
| maxwell/sim/time\_stepper.py | class RungeKutta4 Numerical integrator to advance the state of the system ($t \\rightarrow t \+ dt$). | **Part IV (Ch VI):** Dynamical Theory. |
| maxwell/sim/events.py | class EventQueue Handles discrete events (switch closing, spark discharge) within continuous time. | **Part II (Ch IV):** Self-Induction sparks. |

### **Layer 93: Global Constants & Units Registry (The "Standard")**

**Goal:** Preventing "Magic Numbers." Ensuring $\\epsilon\_0, \\mu\_0, v$ are consistent across Electrostatics (Part I) and Electromagnetism (Part IV).

| Module Path | Class / Responsibility | Cross-Reference |
| :---- | :---- | :---- |
| maxwell/constants.py | class UniversalConstants Single source of truth for 'v' (Speed of Light) and conversion factors. | **Part IV (Ch XIX):** Ratio of Units. |
| maxwell/config/precision.py | class SimulationConfig Controls floating-point precision (float64 vs float32) and error tolerances. | **Global** |

### **Layer 94: The "Treatise" Meta-Link (The "Citation")**

**Goal:** A software utility that links every executed function back to the specific Article in Maxwell's text, fulfilling the goal of "Modernizing the Book."

| Module Path | Class / Responsibility | Cross-Reference |
| :---- | :---- | :---- |
| maxwell/meta/citation.py | decorator @maxwell\_cite(art\_id) Decorator that tags Python functions with their source Article ID. | **Global** |
| maxwell/meta/explorer.py | function get\_theory\_text(art\_id) Returns the original text/equations for a given simulation module (In-app documentation). | **Global** |

