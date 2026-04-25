# **Maxwell's Treatise: Modernized Architecture Map**

## **Part VI: Scalar & Superpotential Physics (The "Hidden Understructure")**

This document tracks the explicit mapping of "Scalar Physics" concepts—restoring the scalar components removed by Heaviside—to Python Modules. This layer sits *below* Part IV (Electromagnetism).

### **Layer 95: The Primordial Superpotential (The "Chi" Field)**

Goal: Defining the root scalar field $\\chi$ (Chi) from which standard potentials arise.  
Source: Scalar Physics / Maxwell's Quaternion Real Component ($S$)

| Module Path | Class / Responsibility | Physics Relation |
| :---- | :---- | :---- |
| maxwell/scalar/superpotential.py | class SuperpotentialField ($\\chi$) A purely scalar field existing in the ether. Supports longitudinal waves. | $\\nabla \\chi \\rightarrow \\mathbf{A}$ (Vector Potential) $d\\chi/dt \\rightarrow \\Psi$ (Electric Potential) |
| maxwell/scalar/hertz\_vector.py | class HertzVector ($\\mathbf{\\Pi}$) An established formulation (Hertz/Whittaker) where Potentials are derivatives of $\\mathbf{\\Pi}$. | $\\mathbf{A} \= \\mu \\epsilon \\frac{\\partial \\mathbf{\\Pi}}{\\partial t}$, $\\Psi \= \-\\nabla \\cdot \\mathbf{\\Pi}$ |

### **Layer 96: Potential Restructuring (The "Causal Layer")**

Goal: Treating Potentials ($A, V$) as physical realities, not mathematical conveniences. This enables "Force-Free" physics.  
Source: Scalar Physics / Aharonov-Bohm Effect

| Module Path | Class / Responsibility | Physics Relation |
| :---- | :---- | :---- |
| maxwell/scalar/force\_free.py | detect\_force\_free\_potential() simulation of regions where $\\mathbf{E}=0, \\mathbf{B}=0$, but $\\mathbf{A} \\neq 0$ (The Aharonov-Bohm regime). | **Text:** "Curl-free magnetic vector potential" |
| maxwell/scalar/longitudinal.py | class LongitudinalWave Simulates waves where $\\nabla \\cdot \\mathbf{A} \\neq 0$ (Scalar waves), usually assumed zero in the Coulomb Gauge. | **Text:** "Scalar physics... meaningful effects" |

### **Layer 97: The Unification Engine (The "Bridge")**

Goal: Attempting the mathematical unification of Gravity and Electromagnetism via the potentials, as suggested by the text.  
Source: Scalar Physics / Unified Field Theory hypotheses

| Module Path | Class / Responsibility | Physics Relation |
| :---- | :---- | :---- |
| maxwell/scalar/gravity\_coupling.py | calc\_gravitational\_potential\_P() Experimental module linking Gravity ($P$) to the Vector Potential ($\\mathbf{A}$). | **Text:** "Define gravitational potential \[P\] in terms of \[A\]" |
| maxwell/scalar/detectors.py | class ScalarInterferometer A virtual instrument designed to detect phase shifts caused by potentials where standard voltmeters read 0\. | **Text:** "Specialized equipment needed to detect potential" |

